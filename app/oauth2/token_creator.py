from datetime import datetime, timedelta, timezone

from fastapi import Depends
from jose import jwt
from strivelogger import StriveLogger

from ..responses.http_exception_if import invalid_client_if, invalid_grant_if, invalid_token_if
from ..settings import Settings, get_settings
from .code_challenge import encode_code_challenge
from .keys import ALGORITHM, KEY_ID, get_pem_key
from .models import ClientCredentialsRequest, CodeExchangeRequest, RefreshTokenRequest, TokenResponse
from .store import Store, get_store


class TokenCreator:
    def __init__(self, store: Store, settings: Settings):
        self.store = store
        self.settings = settings

    def _create_token(self, expiration_minutes: int) -> tuple[str, datetime]:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expiration_minutes)

        data = {
            "sub": self.settings.subject,
            "iss": self.settings.issuer,
            "exp": expire,
            "iat": datetime.now(tz=timezone.utc),
            "aud": self.settings.audience,
        }
        if self.settings.additional_claims:
            data.update(self.settings.additional_claims)

        encoded_jwt = jwt.encode(
            data,
            get_pem_key(),
            algorithm=ALGORITHM,
            headers={
                "kid": KEY_ID,
            },
        )
        return encoded_jwt, expire

    def _create_access_token(self) -> tuple[str, datetime]:
        return self._create_token(self.settings.access_token_expiration_minutes)

    def _create_refresh_token(self) -> tuple[str, datetime]:
        return self._create_token(self.settings.refresh_token_expiration_minutes)

    def token_from_code(self, request: CodeExchangeRequest) -> TokenResponse:
        code_request = self.store.get_code_request_once(request.code)

        invalid_grant_if(code_request is None, detail="Invalid code")
        invalid_grant_if(code_request.client_id != request.client_id, detail="Invalid client_id")
        invalid_grant_if(code_request.redirect_uri != request.redirect_uri, detail="Invalid redirect_uri")

        if "code_challenge_method" in code_request:
            challenge = encode_code_challenge(request.code_verifier, code_request.code_challenge_method)
            invalid_grant_if(challenge != code_request.code_challenge, detail="Invalid code_verifier")

        access_token, access_expiration = self._create_access_token()
        refresh_token, refresh_expiration = self._create_refresh_token()

        self.store.store_refresh_token(refresh_token, refresh_expiration)

        StriveLogger.info(f"Created tokens for client {request.client_id}. Access token expires at {access_expiration}; refresh token expires at {refresh_expiration}")

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)

    def token_from_refresh(self, request: RefreshTokenRequest) -> TokenResponse:
        refresh_expiration = self.store.get_refresh_token_expiration(request.refresh_token)

        invalid_grant_if(refresh_expiration is None, detail="Invalid refresh_token")
        invalid_token_if(refresh_expiration < datetime.now(tz=timezone.utc), detail="Refresh token expired")

        access_token, access_expiration = self._create_access_token()

        StriveLogger.info(f"Access token created from refresh token.  Access token expires at {access_expiration}, refresh token expires at {refresh_expiration}")

        return TokenResponse(access_token=access_token, refresh_token=request.refresh_token)

    def token_from_client_credentials(self, request: ClientCredentialsRequest) -> TokenResponse:
        secret = self.settings.get_secret_for_client(request.client_id)

        invalid_client_if(secret is None, detail="Invalid client_id")
        invalid_client_if(secret != request.client_secret, detail="Invalid client_secret")

        access_token, access_expiration = self._create_access_token()
        refresh_token, refresh_expiration = self._create_refresh_token()

        self.store.store_refresh_token(refresh_token, refresh_expiration)

        StriveLogger.info(f"Created tokens for client {request.client_id}. Access token expires at {access_expiration}; refresh token expires at {refresh_expiration}")

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)


def create_token_creator(
    store: Store = Depends(get_store),
    settings: Settings = Depends(get_settings),
) -> TokenCreator:
    return TokenCreator(
        store=store,
        settings=settings,
    )
