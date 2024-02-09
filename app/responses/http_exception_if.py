from fastapi import HTTPException
from strivelogger import StriveLogger


def invalid_response(code: int, error: str, error_description: str):
    StriveLogger.warn(f"{error}: {error_description}")

    raise HTTPException(
        status_code=code,
        detail={
            "error": error,
            "error_description": error_description,
        },
    )


def invalid_grant_if(condition: bool, detail: str):
    if condition:
        invalid_response(400, "invalid_grant", detail)


def invalid_token_if(condition: bool, detail: str):
    if condition:
        invalid_response(401, "invalid_token", detail)


def invalid_client_if(condition: bool, detail: str):
    if condition:
        invalid_response(401, "invalid_client", detail)
