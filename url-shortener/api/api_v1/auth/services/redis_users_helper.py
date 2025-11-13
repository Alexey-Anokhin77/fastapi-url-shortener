from redis import Redis

from api.api_v1.auth.services.users_helper import AbstractUsersHelpers
from core.config import settings


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
    host=settings.redis.connection.host,
    port=settings.redis.connection.port,
    db=settings.redis.database.redis_db_users,
)
