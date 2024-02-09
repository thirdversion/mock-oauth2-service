import base64
import hashlib


def encode_code_challenge(code_verifier: str, method: str) -> str:
    if method == "S256":
        return base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b"=").decode()
    else:  # plain
        return code_verifier
