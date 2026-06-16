import hashlib
import os
from cryptography.fernet import Fernet

PHONE_KEY = os.getenv("PHONE_ENCRYPT_KEY", Fernet.generate_key().decode())
_cipher = Fernet(PHONE_KEY.encode() if isinstance(PHONE_KEY, str) else PHONE_KEY)


def hash_pan(pan: str) -> str:
    return hashlib.sha256(pan.strip().upper().encode()).hexdigest()


def hash_email(email: str) -> str:
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()


def encrypt_phone(phone: str) -> str:
    return _cipher.encrypt(phone.strip().encode()).decode()


def decrypt_phone(encrypted: str) -> str:
    return _cipher.decrypt(encrypted.encode()).decode()
