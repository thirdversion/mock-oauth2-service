from http import HTTPStatus
from typing import Literal

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from ..oauth2.authorize import create_authorization_form
from ..oauth2.code_creator import CodeCreator, create_code_creator
from ..oauth2.configuration import get_oauth2_configuration
from ..oauth2.keys import get_jwks
from ..oauth2.models import ClientCredentialsRequest, CodeExchangeRequest, RefreshTokenRequest, TokenRequest
from ..oauth2.token_creator import TokenCreator, TokenResponse, create_token_creator

router = APIRouter()


@router.get("/authorize", response_class=HTMLResponse)
async def authorize_get(
    client_id: str,
    redirect_uri: str,
    scope: str,
    response_type: Literal["code"],
    code_challenge: str | None = None,
    code_challenge_method: str | None = None,
):
    return create_authorization_form(client_id, redirect_uri, scope, response_type, code_challenge, code_challenge_method)


@router.post("/authorize")
async def authorize_post(
    client_id: str = Form(),
    redirect_uri: str = Form(),
    scope: str = Form(),
    response_type: Literal["code"] = Form(),
    code_challenge: str | None = Form(default=None),
    code_challenge_method: str | None = Form(default=None),
    code_creator: CodeCreator = Depends(create_code_creator),
):
    auth_code = code_creator.create_code(client_id, redirect_uri, scope, response_type, code_challenge, code_challenge_method)
    redirect_uri = f"{redirect_uri}?code={auth_code}"
    return RedirectResponse(url=redirect_uri, status_code=HTTPStatus.SEE_OTHER)


@router.post("/token", response_model=TokenResponse)
async def token(
    request: TokenRequest = Depends(),
    oauth2: TokenCreator = Depends(create_token_creator),
):
    request = request.validated()

    match request:
        case CodeExchangeRequest():
            return oauth2.token_from_code(request)

        case RefreshTokenRequest():
            return oauth2.token_from_refresh(request)

        case ClientCredentialsRequest():
            return oauth2.token_from_client_credentials(request)

        case _:
            raise NotImplementedError()


@router.get("/keys")
async def keys(
    jwks=Depends(get_jwks),
):
    return JSONResponse(content=jwks)


@router.get("/.well-known/openid-configuration")
async def openid_configuration(
    configuration=Depends(get_oauth2_configuration),
):
    return JSONResponse(content=configuration)
