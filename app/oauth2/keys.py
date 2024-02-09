import os
from base64 import urlsafe_b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from strivelogger import StriveLogger

KEY_ID = "1"
ALGORITHM = "RS256"


def to_pem(key: rsa.RSAPrivateKey):
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def load_or_generate_key():
    PRIVATE_KEY_FILE = "private_key.pem"
    if os.path.exists(PRIVATE_KEY_FILE):
        # Load the existing private key
        StriveLogger.info("Loading existing private key")
        with open(PRIVATE_KEY_FILE, "rb") as key_file:
            return serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
    else:
        # Generate a new private key
        StriveLogger.info("Generating new private key")
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        # Save the private key to a file
        with open(PRIVATE_KEY_FILE, "wb") as key_file:
            key_file.write(to_pem(private_key))
        StriveLogger.info("Private key saved")
        return private_key


PRIVATE_KEY = load_or_generate_key()

# Get the public key
PUBLIC_KEY = PRIVATE_KEY.public_key()


def get_pem_key():
    return to_pem(PRIVATE_KEY)


def _int_to_base64(n):
    return urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big")).rstrip(b"=").decode("utf-8")


def get_jwks() -> dict:
    public_num = PUBLIC_KEY.public_numbers()
    return {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "kid": KEY_ID,
                "n": _int_to_base64(public_num.n),
                "e": _int_to_base64(public_num.e),
            }
        ]
    }
