from fastapi import Depends, Request

from ..settings import Settings, get_settings


def get_oauth2_configuration(request: Request, settings: Settings = Depends(get_settings)) -> dict:
    base_url = str(request.base_url).removesuffix("/")

    return {
        "issuer": settings.issuer,
        "authorization_endpoint": f"{base_url}/authorize",
        "token_endpoint": f"{base_url}/token",
        "jwks_uri": f"{base_url}/keys",
    }
