import os, json, base64
from typing import Dict, Any
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

PBKDF2_ITERATIONS = 600_000
KEY_LEN   = 32
SALT_LEN  = 16
NONCE_LEN = 12

def _b64e(b: bytes) -> str: return base64.b64encode(b).decode()
def _b64d(s: str) -> bytes: return base64.b64decode(s)

def _derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return kdf.derive(password.encode())

def encrypt_with_password(plaintext: str, password: str) -> Dict[str, Any]:
    if not plaintext: raise ValueError("Lege tekst")
    if not password:  raise ValueError("Geen wachtwoord")

    salt  = os.urandom(SALT_LEN)
    key   = _derive_key(password, salt)
    nonce = os.urandom(NONCE_LEN)
    aes   = AESGCM(key)

    ct = aes.encrypt(nonce, plaintext.encode(), None)

    return {
        "alg": "AES-256-GCM",
        "kdf": "PBKDF2-HMAC-SHA256",
        "params": {"iterations": PBKDF2_ITERATIONS, "salt": _b64e(salt)},
        "nonce": _b64e(nonce),
        "ciphertext": _b64e(ct)
    }

def decrypt_with_password(package_json: str, password: str) -> str:
    if not package_json: raise ValueError("Lege input")
    if not password: raise ValueError("Geen wachtwoord")

    pkg = json.loads(package_json)
    salt  = _b64d(pkg["params"]["salt"])
    nonce = _b64d(pkg["nonce"])
    ct    = _b64d(pkg["ciphertext"])

    key = _derive_key(password, salt)
    aes = AESGCM(key)
    try:
        pt = aes.decrypt(nonce, ct, None)
    except Exception:
        raise ValueError("Authenticatie mislukt (verkeerd wachtwoord of beschadigd pakket)")
    return pt.decode()