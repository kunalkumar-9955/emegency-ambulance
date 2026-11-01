"""End-to-end encryption helpers using PyNaCl."""

import base64
import hashlib

import nacl.public
import nacl.secret
import nacl.utils
from django.conf import settings


def derive_key(passphrase: str, salt: str | None = None) -> bytes:
    salt = (salt or settings.E2E_SERVER_SALT).encode()
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode(), salt, 100000, dklen=32)


def encrypt_message(plaintext: str, recipient_public_key_b64: str, sender_private_key: nacl.public.PrivateKey) -> str:
    recipient_key = nacl.public.PublicKey(base64.b64decode(recipient_public_key_b64))
    box = nacl.public.Box(sender_private_key, recipient_key)
    encrypted = box.encrypt(plaintext.encode())
    return base64.b64encode(encrypted).decode()


def decrypt_message(ciphertext_b64: str, sender_public_key_b64: str, recipient_private_key: nacl.public.PrivateKey) -> str:
    sender_key = nacl.public.PublicKey(base64.b64decode(sender_public_key_b64))
    box = nacl.public.Box(recipient_private_key, sender_key)
    decrypted = box.decrypt(base64.b64decode(ciphertext_b64))
    return decrypted.decode()


def generate_keypair() -> tuple[str, str]:
    private_key = nacl.public.PrivateKey.generate()
    public_key = private_key.public_key
    return (
        base64.b64encode(bytes(private_key)).decode(),
        base64.b64encode(bytes(public_key)).decode(),
    )


def encrypt_at_rest(data: bytes) -> tuple[bytes, bytes]:
    """Server-side AES-like secretbox for cloud storage."""
    key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
    box = nacl.secret.SecretBox(key)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    return key, nonce + box.encrypt(data, nonce)
