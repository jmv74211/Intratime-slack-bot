import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

from config import settings


def generate_cipher_key():
    """
    Function to generate the key hash needed to encrypt the password

    Returns
    ------
    key: bytes
        Key hash
    """
    password = settings.CIPHER_KEY.encode()

    salt = b"\xf6A\x99\x8b\xf4\x92C\x14y\xf2\xd0\xdb\x94d\xbf\t"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    return key


def encrypt(text):
    """
    Function to encrypt a text, like a password

    Parameters
    ----------
    text: str
        Text to cipher

    Returns
    -------
    ciphered_text: str
        Ciphered text
    """
    cipher = Fernet(generate_cipher_key())
    ciphered_text = cipher.encrypt(text.encode()).decode()

    return ciphered_text


def decrypt(encrypted_text):
    """
    Function to decrypt a ciphered text

    Parameters
    ----------
    encrypted_text: str
        Text to decipher

    Returns
    -------
    deciphered_text: str
        Deciphered text
    """
    cipher = Fernet(generate_cipher_key())
    deciphered_text = cipher.decrypt(encrypted_text.encode()).decode()

    return deciphered_text
