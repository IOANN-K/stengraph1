from cryptography.fernet import Fernet


def generate_key() -> bytes:
    return Fernet.generate_key()


def encrypt(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt(data: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(data)
