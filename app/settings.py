from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from strivelogger import StriveLogger


class ClientSecret(BaseModel):
    client_id: str
    client_secret: str


class Settings(BaseSettings):
    access_token_expiration_minutes: int = 30
    refresh_token_expiration_minutes: int = 180
    subject: str = "mock_user"
    issuer: str = "DEFAULT_ISSUER"
    audience: str = "DEFAULT_AUDIENCE"
    additional_claims: dict = {}
    client_secrets: list[ClientSecret] | ClientSecret | None = None

    def print(self) -> str:
        # print out all fields in the format "key=value"
        for key, value in self.model_dump().items():
            StriveLogger.debug(f"{key}={value}")

    def get_secret_for_client(self, client_id: str) -> str | None:
        if self.client_secrets is None:
            return None

        secrets = self.client_secrets if isinstance(self.client_secrets, list) else [self.client_secrets]

        return next((secret.client_secret for secret in secrets if secret.client_id == client_id), None)


@lru_cache
def get_settings() -> Settings:
    return Settings(_env_file=".env")
