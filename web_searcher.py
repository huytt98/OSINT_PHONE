import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from urllib.parse import quote_plus
import time
from utils import RateLimiter, AsyncRetry, AsyncSession, with_timeout, ConnectionPool, MemoryManager
import logging
from tqdm import tqdm

class WebSearcher:
    def __init__(self, cache_manager=None):
        self.ua = UserAgent()
        self.cache_manager = cache_manager
        self.current_proxy = 0
        self.session = None
        self.proxies = self._load_proxies()
        self.additional_sites = {
            'yandex': 'https://yandex.com/search/',
            'baidu': 'https://www.baidu.com/s',
            'searx': 'https://searx.be/search'
        }
        self.logger = logging.getLogger('osint.websearcher')
        self.rate_limiter = RateLimiter(calls_per_second=0.5, burst_limit=3)
        self.session_manager = AsyncSession(timeout=30)
        self.connection_pool = ConnectionPool(size=5)
        self.memory_manager = MemoryManager(threshold=85)
        self.batch_size = 3

    def _load_proxies(self):
        # Rotating proxies list (add your proxies here)
        return [
            'http://proxy1.com:8080',
            'http://proxy2.com:8080',
            # Add more proxies
        ]

    def _get_next_proxy(self):
        self.current_proxy = (self.current_proxy + 1) % len(self.proxies)
        return self.proxies[self.current_proxy]

    def _get_headers(self):
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
        }

    @AsyncRetry(retries=3, delay=1, backoff=2)
    @with_timeout(30)
    async def _fetch_with_retry(self, url, engine):
        await self.rate_limiter.acquire()
        self.logger.debug(f"Fetching {url} with engine {engine}")
        
        async with self.session_manager as session:
            proxy = self._get_next_proxy()
            async with session.get(url, headers=self._get_headers(), proxy=proxy) as response:
                if response.status == 200:
                    return await response.text()
        return None

    async def _fetch_async(self, url, engine):
        html = await self._fetch_with_retry(url, engine)
        if html:
            return self._parse_results(html, engine)
        return []

    def _parse_results(self, html, engine):
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        if engine == 'google':
            results = self._parse_google_results(soup)
        elif engine == 'bing':
            results = self._parse_bing_results(soup)
        elif engine == 'yandex':
            results = self._parse_yandex_results(soup)
        
        return self._clean_results(results)

    def _parse_google_results(self, soup):
        results = []
        for link in soup.find_all('a', href=True):
            if link['href'].startswith('/url?q='):
                url = link['href'].split('/url?q=')[1].split('&sa=')[0]
                if not any(x in url for x in ['google.', 'youtube.', 'facebook.']):
                    results.append(url)
        return results

    def _parse_bing_results(self, soup):
        results = []
        for link in soup.find_all('a', {'class': 'b_algo'}):
            if href := link.get('href'):
                results.append(href)
        return results

    def _parse_yandex_results(self, soup):
        results = []
        for link in soup.find_all('a', {'class': 'organic__url'}):
            if href := link.get('href'):
                results.append(href)
        return results

    def _clean_results(self, urls):
        cleaned = []
        blacklist = ['google.', 'bing.', 'facebook.', 'youtube.']
        for url in urls:
            if not any(x in url.lower() for x in blacklist):
                cleaned.append(url)
        return list(dict.fromkeys(cleaned))  # Remove duplicates

    async def search_all_engines(self, query):
        if cached := await self._get_cached_results(query):
            return cached

        results = []
        engines = list(self.additional_sites.items())
        
        # Process in batches
        for i in range(0, len(engines), self.batch_size):
            batch = engines[i:i + self.batch_size]
            batch_tasks = []
            
            for engine, base_url in batch:
                url = f"{base_url}?q={quote_plus(query)}"
                task = self._fetch_async(url, engine)
                batch_tasks.append(task)
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            valid_results = [r for r in batch_results if not isinstance(r, Exception)]
            results.extend([item for sublist in valid_results for item in sublist])
            
            if self.memory_manager.check_memory():
                self.logger.info("Memory threshold reached, performing cleanup")
            
            await asyncio.sleep(0.5)
        
        # Format results before returning
        formatted_results = {
            'search_results': list(dict.fromkeys(results))[:20],  # Top 20 unique results
            'search_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if self.cache_manager:
            await self._cache_results(query, formatted_results)
        
        return formatted_results

    async def _get_cached_results(self, query):
        if self.cache_manager:
            return await asyncio.to_thread(self.cache_manager.get, query, 'search')
        return None

    async def _cache_results(self, query, results):
        await asyncio.to_thread(self.cache_manager.set, query, results, 'search')

    async def __aenter__(self):
        await self.session_manager.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.session_manager.__aexit__(exc_type, exc_val, exc_tb)
        except Exception as e:
            self.logger.error(f"Error closing session: {e}")
        finally:
            if self.session:
                await self.session.close()

def find_related_info(phone_number):
    searcher = WebSearcher()
    results = {}
    
    # Clean number and generate queries
    formatted_number = phone_number.replace('+', '').replace(' ', '')
    queries = [
        f'"{phone_number}"',
        f'"{formatted_number}"',
        f'"{formatted_number}" contact',
        f'"{formatted_number}" profile',
        # Advanced search operators
        f'intext:"{formatted_number}" site:linkedin.com OR site:facebook.com OR site:twitter.com',
        f'filetype:pdf OR filetype:doc intext:"{formatted_number}"',
        f'inurl:contact intext:"{formatted_number}"',
        f'intext:email AROUND(5) "{formatted_number}"'
    ]
    
    # Run async searches
    loop = asyncio.get_event_loop()
    all_results = []
    for query in queries:
        results = loop.run_until_complete(searcher.search_all_engines(query))
        all_results.extend(results)
        time.sleep(1)  # Respect rate limits
    
    # Group and clean results
    return {
        'search_results': list(dict.fromkeys(all_results))[:20],  # Top 20 unique results
        'search_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
