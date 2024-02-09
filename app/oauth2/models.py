from dataclasses import dataclass
from typing import Literal

from fastapi import Form
from pydantic import BaseModel


class CodeRequest(BaseModel):
    client_id: str
    redirect_uri: str
    scope: str
    response_type: str
    code_challenge: str | None
    code_challenge_method: str | None


class CodeExchangeRequest(BaseModel):
    grant_type: Literal["authorization_code"]
    code: str
    redirect_uri: str
    client_id: str
    code_verifier: str


class RefreshTokenRequest(BaseModel):
    grant_type: Literal["refresh_token"]
    client_id: str
    refresh_token: str


class ClientCredentialsRequest(BaseModel):
    grant_type: Literal["client_credentials"]
    client_id: str
    client_secret: str


@dataclass
class TokenRequest:
    grant_type: Literal["authorization_code", "refresh_token", "client_credentials"] = Form()
    client_id: str = Form()

    # code request
    code: str | None = Form(default=None)
    redirect_uri: str | None = Form(default=None)
    code_verifier: str | None = Form(default=None)

    # refresh
    refresh_token: str | None = Form(default=None)

    # client credentials
    client_secret: str | None = Form(default=None)

    def validated(self) -> CodeExchangeRequest | RefreshTokenRequest:
        match self.grant_type:
            case "authorization_code":
                return CodeExchangeRequest(**self.__dict__)
            case "refresh_token":
                return RefreshTokenRequest(**self.__dict__)
            case "client_credentials":
                return ClientCredentialsRequest(**self.__dict__)
            case _:
                raise ValueError("Invalid or unsupported grant_type")


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
