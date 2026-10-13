"""
File Encryption & Decryption System
-----------------------------------
Encrypts/decrypts any file with a password using AES-256-GCM.

- Key derivation : Scrypt (password -> 256-bit key, random salt per file)
- Encryption     : AES-256-GCM (confidentiality + tamper detection)
- File format    : MAGIC (5 bytes) | salt (16) | nonce (12) | ciphertext+tag

Install:  pip install cryptography
Usage:
    python file_crypto.py encrypt report.pdf          -> report.pdf.enc
    python file_crypto.py decrypt report.pdf.enc      -> report.pdf
    python file_crypto.py encrypt notes.txt -o secret.enc
"""

import argparse
import getpass
import os
import sys

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"FENC1"
SALT_SIZE = 16
NONCE_SIZE = 12
EXT = ".enc"


def derive_key(password: str, salt: bytes) -> bytes:
    """Turn a password into a 256-bit key using Scrypt."""
    kdf = Scrypt(salt=salt, length=32, n=2**15, r=8, p=1)
    return kdf.derive(password.encode("utf-8"))


def encrypt_file(in_path: str, out_path: str, password: str) -> None:
    with open(in_path, "rb") as f:
        data = f.read()

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = derive_key(password, salt)

    # The header is authenticated too, so tampering with it is detected.
    header = MAGIC + salt + nonce
    ciphertext = AESGCM(key).encrypt(nonce, data, header)

    with open(out_path, "wb") as f:
        f.write(header + ciphertext)


def decrypt_file(in_path: str, out_path: str, password: str) -> None:
    with open(in_path, "rb") as f:
        blob = f.read()

    header_len = len(MAGIC) + SALT_SIZE + NONCE_SIZE
    if len(blob) < header_len or not blob.startswith(MAGIC):
        raise ValueError("Not a valid encrypted file (bad header).")

    header = blob[:header_len]
    salt = blob[len(MAGIC):len(MAGIC) + SALT_SIZE]
    nonce = blob[len(MAGIC) + SALT_SIZE:header_len]
    ciphertext = blob[header_len:]

    key = derive_key(password, salt)
    try:
        data = AESGCM(key).decrypt(nonce, ciphertext, header)
    except InvalidTag:
        raise ValueError("Wrong password or the file has been tampered with.")

    with open(out_path, "wb") as f:
        f.write(data)


def get_password(confirm: bool) -> str:
    pw = getpass.getpass("Password: ")
    if not pw:
        sys.exit("Password cannot be empty.")
    if confirm and getpass.getpass("Confirm password: ") != pw:
        sys.exit("Passwords do not match.")
    return pw


def main() -> None:
    parser = argparse.ArgumentParser(description="AES-256-GCM file encryptor")
    parser.add_argument("mode", choices=["encrypt", "decrypt"])
    parser.add_argument("file", help="input file path")
    parser.add_argument("-o", "--output", help="output file path (optional)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        sys.exit(f"File not found: {args.file}")

    if args.mode == "encrypt":
        out = args.output or args.file + EXT
        password = get_password(confirm=True)
        encrypt_file(args.file, out, password)
        print(f"Encrypted -> {out}")
    else:
        if args.output:
            out = args.output
        elif args.file.endswith(EXT):
            out = args.file[: -len(EXT)]
        else:
            out = args.file + ".dec"
        password = get_password(confirm=False)
        try:
            decrypt_file(args.file, out, password)
        except ValueError as e:
            sys.exit(f"Error: {e}")
        print(f"Decrypted -> {out}")


if __name__ == "__main__":
    main()
