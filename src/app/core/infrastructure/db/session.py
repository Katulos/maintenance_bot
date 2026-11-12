import base64
import hashlib

from cryptography.fernet import Fernet
from sqlalchemy.ext.asyncio import AsyncSession as SaAsyncSession

from ...config import settings


class AsyncSession(SaAsyncSession):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        secret_key = settings.get("core.secret_key").encode()
        hashed_key = hashlib.sha256(secret_key).digest()
        key = base64.urlsafe_b64encode(hashed_key)
        self.cipher_suite = Fernet(key)
