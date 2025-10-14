from unittest import TestCase

import pytest

from api.api_v1.auth.services import redis_tokens


@pytest.mark.apitest
class RedisTokensHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token()
        self.assertTrue(
            redis_tokens.token_exists(new_token),
        )
