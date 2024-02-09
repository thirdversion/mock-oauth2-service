import uuid

from fastapi import Depends
from strivelogger import StriveLogger

from .models import CodeRequest
from .store import Store, get_store


class CodeCreator:
    def __init__(self, store: Store):
        self.store = store

    def create_code(
        self,
        client_id: str,
        redirect_uri: str,
        scope: str,
        response_type: str,
        code_challenge: str,
        code_challenge_method: str,
    ) -> str:
        auth_code = str(uuid.uuid4())

        code_request = CodeRequest(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            response_type=response_type,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
        )

        self.store.store_code_request(auth_code, code_request)

        StriveLogger.info(f"Created code {auth_code} for client {client_id}")

        return auth_code


def create_code_creator(store: Store = Depends(get_store)) -> CodeCreator:
    return CodeCreator(store)
