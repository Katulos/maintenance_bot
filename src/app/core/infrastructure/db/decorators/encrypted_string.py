from sqlalchemy import String, TypeDecorator
from sqlalchemy.ext.asyncio import async_object_session


class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        session = async_object_session(self)
        return session.cipher_suite.encrypt(value.encode()).decode()

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        session = async_object_session(self)
        return session.cipher_suite.decrypt(value.encode()).decode()
