"""
UNNÖTIG ABER DOCH:

FORMEL ZUM VERGLEICHEN VON ZWEI WERTEN
1 => Gleich
0 => nicht gleich

f = lambda a, b: 0**(((a-b)**2)**0.5)


WARUM DOCH KEINE VERSCHLÜSSELUNG:

meine ideen, die eventl schwerer zum brute forcen war, hatten ein großes problem: Ich muss wissen, wie viel richtig war und nicht
usw.
"""
import base64
import binascii

import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


# Do not change!
salt = b"\x85\xda\x94(\x98\xe8\xcf\xdc\xea?1\x18\xee\xd3u|"


def encrypt_code(code: list) -> str:
    msg = None

    for color_name in code[::-1]:
        key = generate_key(color_name)
        return ""


def test(code: list) -> str:
    pass


print(test(['orange', 'gruen', 'lila', 'blau', 'rot', 'gelb']))


def generate_key(pwd: str) -> bytes:
    """ Generate a key from a password
    :param pwd: the password
    """
    global salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(pwd.encode("utf8")))


def encrypt_message(pwd: str, msg: str) -> bytes:
    """ Encrypt a message via Fernet
    :param pwd: the password
    :param msg: the message
    """
    global salt

    return Fernet(generate_key(pwd)).encrypt(msg.encode("utf8"))


def decrypt_message(pwd: str, msg: str) -> str:
    """ Decrypt a encrypted message via Fernet
    :param pwd: the password
    :param msg: the message
    """
    global salt

    try:
        return Fernet(generate_key(pwd)).decrypt(msg.encode("utf8")).decode("utf8")

    except cryptography.fernet.InvalidToken:
        return None
