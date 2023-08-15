from fastapi import HTTPException
from redis.exceptions import ConnectionError, ResponseError


class RedisHandler:
    @staticmethod
    def handle_redis_exceptions(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except ConnectionError:
                raise HTTPException(
                    status_code=503,
                    detail='Service Unavailable: Unable to connect to Redis.'
                )
            except ResponseError:
                raise HTTPException(
                    status_code=503,
                    detail='Internal Server Error: Unexpected response from Redis.'
                )
        return wrap

    @handle_redis_exceptions
    def set_redis(self, redis, key: str, value: str, expiry_time: int):
        redis.set(key, value, ex=expiry_time)

    @handle_redis_exceptions
    def get_redis_value(self, redis, key: str):
        return redis.get(key)

    @handle_redis_exceptions
    def delete_redis(self, redis, key: str):
        redis.delete(key)
