import pickle
from redis import Redis


class CacheProxy:
    """
    CacheProxy is a class that provides a proxy to the cache server.
    This is the interface for DI, making cache server optional.
    """

    def __init__(self):
        pass

    def set(self, key, value):
        raise NotImplementedError("set method is not implemented")

    def get(self, key):
        raise NotImplementedError("get method is not implemented")

    def get_or_set(self, key, value):
        result = self.get(key)
        if result is None:
            self.set(key, value)
            return value
        return result

    def clear(self):
        raise NotImplementedError("clear method is not implemented")

    @classmethod
    def _serialize(cls, value):
        return None if value is None else pickle.dumps(value)

    @classmethod
    def _deserialize(cls, value):
        return None if value is None else pickle.loads(value)


class NoCacheProxy(CacheProxy):
    """
    The no cache.
    """

    def __init__(self):
        super().__init__()

    def set(self, key, value):
        pass

    def get(self, key):
        return None

    def clear(self):
        pass


class RedisProxy(CacheProxy):
    """
    RedisProxy is a class that provides a proxy to the Redis server.
    """

    def __init__(self, host, port=6379, db=0, password=None):
        super().__init__()
        self.redis = Redis(host=host, port=6379, db=0, password=password)

    def set(self, key, value):
        self.redis.set(key, self._serialize(value))

    def get(self, key):
        return self._deserialize(self.redis.get(key))

    def clear(self):
        self.redis.flushdb()


class MemoryProxy(CacheProxy):
    """
    Provide support for memory cache.
    """

    def __init__(self):
        super().__init__()
        self.db = {}

    def set(self, key, value):
        self.db[key] = self._serialize(value)

    def get(self, key):
        return self._deserialize(self.db.get(key, None))

    def clear(self):
        self.db.clear()
