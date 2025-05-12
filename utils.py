import logging
import asyncio
import time
from datetime import datetime
import os
from tqdm import tqdm
from functools import wraps
import aiohttp
import signal
from logging.handlers import RotatingFileHandler
import psutil
import gc

class RateLimiter:
    def __init__(self, calls_per_second=1, burst_limit=3):
        self.calls_per_second = calls_per_second
        self.burst_limit = burst_limit
        self.calls = []
        self.last_call = 0
        
    async def acquire(self):
        now = time.time()
        self.calls = [t for t in self.calls if now - t <= 1.0]
        
        if len(self.calls) >= self.burst_limit:
            sleep_time = self.calls[0] + 1.0 - now
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        self.calls.append(now)
        self.last_call = now

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Operation timed out")

def with_timeout(seconds=30):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                return await func(*args, **kwargs)
            finally:
                signal.alarm(0)
        return wrapper
    return decorator

class AsyncRetry:
    def __init__(self, retries=3, delay=1, backoff=2, exceptions=(Exception,)):
        self.retries = retries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            delay = self.delay
            for i in range(self.retries):
                try:
                    return await func(*args, **kwargs)
                except self.exceptions as e:
                    if i == self.retries - 1:
                        raise
                    await asyncio.sleep(delay)
                    delay *= self.backoff
            return None
        return wrapper

class ConnectionPool:
    def __init__(self, size=10):
        self.size = size
        self.pool = []
        self.in_use = set()
    
    async def get_connection(self):
        if not self.pool and len(self.in_use) < self.size:
            conn = aiohttp.TCPConnector(ttl_dns_cache=300)
            session = aiohttp.ClientSession(connector=conn)
            self.pool.append(session)
        
        while not self.pool:
            await asyncio.sleep(0.1)
            
        session = self.pool.pop(0)
        self.in_use.add(session)
        return session
    
    async def release_connection(self, session):
        self.in_use.remove(session)
        self.pool.append(session)

class MemoryManager:
    def __init__(self, threshold=90):
        self.threshold = threshold
    
    def check_memory(self):
        memory = psutil.Process().memory_percent()
        if memory > self.threshold:
            gc.collect()
            return True
        return False

class AsyncSession:
    def __init__(self, timeout=30, pool=None):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
        self.pool = pool or ConnectionPool()
        
    async def __aenter__(self):
        self.session = await self.pool.get_connection()
        return self.session
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.pool.release_connection(self.session)

def setup_logging():
    """Setup logging with file and console handlers."""
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"osint_{datetime.now().strftime('%Y%m%d')}.log")
    
    # Create logger
    logger = logging.getLogger('osint')
    logger.setLevel(logging.INFO)
    
    # Create handlers
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    console_handler = logging.StreamHandler()
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
