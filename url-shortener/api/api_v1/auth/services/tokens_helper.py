import secrets
from abc import ABC, abstractmethod


class AbstractTokensHelpers(ABC):
    """
    Что мне нужно от обертки:
     - проверять на наличие токена
     - добавлять токен в хранилище
     - сгенерировать и добавить токен
    """

    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Check if token exist.
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Save token in to storage.
        :param token:
        :return:
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generate_and_save_token(
        self,
    ) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token

    @abstractmethod
    def get_tokens(self) -> list[str]:
        """
        Возвращает список всех токенов
        :return: list[str] - список строковых токенов
        """

    @abstractmethod
    def delete_token(self, token: str) -> None:
        """
        Delete token from storage.
        """
