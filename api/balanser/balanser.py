from api.server import redis_client

# функция для установки лимита N, также можно поставить и временной счетчик period: timedelta
async def request_is_limited(r: redis_client, key: str, limit: int):
    """
    :param r: экземпляр класса SanicRedis()
    :param key: url_ оригинального сервера
    :param limit: сколько раз будет редиректиться на CDN_HOST
    """
    await r.setnx(key, limit)
    # await r.expire(key, int(period.total_seconds()))
    value = await r.get(key)
    if value and int(value) > 0:
        await r.decrby(key, 1)
        return False
    return True