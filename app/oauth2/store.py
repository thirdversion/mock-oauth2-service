from datetime import datetime

from .models import CodeRequest


class Store:
    def __init__(self):
        self._refresh_tokens: dict[str, datetime] = {}
        self._auth_data: dict[str, CodeRequest] = {}

    def store_refresh_token(self, token: str, expiration: datetime):
        self._refresh_tokens[token] = expiration

    def get_refresh_token_expiration(self, token: str) -> datetime | None:
        return self._refresh_tokens.get(token)

    def remove_refresh_token(self, token: str):
        self._refresh_tokens.pop(token, None)

    def store_code_request(self, code: str, code_request: CodeRequest):
        self._auth_data[code] = code_request

    def get_code_request_once(self, code: str) -> CodeRequest | None:
        return self._auth_data.pop(code, None)


_store_instance = None


def get_store() -> Store:
    global _store_instance
    if _store_instance is None:
        _store_instance = Store()
    return _store_instance
