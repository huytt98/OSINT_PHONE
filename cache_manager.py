import json
import os
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_dir="cache", expiry_days=7):
        self.cache_dir = os.path.join(os.path.dirname(__file__), cache_dir)
        self.expiry_days = timedelta(days=expiry_days)
        os.makedirs(self.cache_dir, exist_ok=True)

    def get(self, key, cache_type):
        cache_file = os.path.join(self.cache_dir, f"{cache_type}.json")
        try:
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
                    if key in cache:
                        stored = cache[key]
                        stored_date = datetime.fromisoformat(stored['timestamp'])
                        if datetime.now() - stored_date < self.expiry_days:
                            return stored['data']
        except Exception:
            pass
        return None

    def set(self, key, data, cache_type):
        cache_file = os.path.join(self.cache_dir, f"{cache_type}.json")
        try:
            cache = {}
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache = json.load(f)
            
            cache[key] = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache, f)
        except Exception:
            pass
