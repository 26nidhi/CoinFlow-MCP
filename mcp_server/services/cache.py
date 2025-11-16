import time

class InMemoryCache:
    def __init__(self):
        self.store = {}

    async def get(self, key):
        entry = self.store.get(key)
        if not entry:
            return None

        value, expires_at = entry
        if expires_at < time.time():
            del self.store[key]
            return None

        return value

    async def set(self, key, value, ttl=10):
        expires_at = time.time() + ttl
        self.store[key] = (value, expires_at)

cache = InMemoryCache()
