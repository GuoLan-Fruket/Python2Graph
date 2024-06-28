from lib.shared.logger import logger
from core.cache.cache_proxy import CacheProxy, MemoryProxy, NoCacheProxy, RedisProxy

_CACHE_PROXY: CacheProxy = None


def resolve_cache(section: dict) -> CacheProxy:
    global _CACHE_PROXY
    if _CACHE_PROXY is not None:
        raise Exception("Cache proxy already initialized")
    _CACHE_PROXY = _resolve_cache(section)
    return _CACHE_PROXY


def _resolve_cache(section: dict) -> CacheProxy:
    """
    Handle cache configuration. The YAML form of the config is as follows:
    CACHE:
      DATABASE: (none | memory | redis)
      REDIS:
        HOST: "211.71.15.48"
        PORT: 6379
        DB: 1
        PASSWORD: sdp123456
    """
    db = str(section["DATABASE"]).lower()
    if db == "none":
        logger().warning("No cache provider selected")
        return NoCacheProxy()
    if db == "memory":
        logger().info("Using in memory cache")
        return MemoryProxy()
    if db == "redis":
        logger().info("Using redis cache")
        return RedisProxy(
            section["REDIS"]["HOST"],
            section["REDIS"]["PORT"],
            section["REDIS"]["DB"],
            section["REDIS"]["PASSWORD"],
        )
    logger().error(f"Cache provider {db} is not supported")
    return NoCacheProxy()


def get_cache_proxy() -> CacheProxy:
    if _CACHE_PROXY is None:
        raise Exception("Cache proxy not initialized")
    return _CACHE_PROXY
