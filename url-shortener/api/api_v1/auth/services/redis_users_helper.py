from redis import Redis

from api.api_v1.auth.services.users_helper import AbstractUsersHelpers
from core import config


class RedisUsersHelper(AbstractUsersHelpers):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
    ) -> None:
        self.redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )

    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        result = self.redis.get(username)
        if result is None:
            return None
        return str(result)


redis_users = RedisUsersHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_USERS,
)
