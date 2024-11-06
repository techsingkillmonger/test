import argparse
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import sys

def parse_args():
    """Parse command-line arguments without revealing what each argument does."""
    parser = argparse.ArgumentParser(description="Decrypt an encrypted file.", add_help=False)
    parser.add_argument("arg1", help="First argument (, )")
    parser.add_argument("arg2", help="Second argument (, )")
    parser.add_argument("arg3", help="Third argument (, )")
    parser.add_argument("arg4", help="Fourth argument (, )")
    
    try:
        return parser.parse_args()
    except SystemExit:
        sys.exit(1)  


def decrypt_file(filename, key):
    """Decrypt the given file with the provided key."""
    with open(filename, "rb") as f:
        encrypted_data = f.read()

    iv = encrypted_data[:16]  
    ciphertext = encrypted_data[16:]  

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    decrypted_filename = "decrypted_" + filename
    with open(decrypted_filename, "wb") as f:
        f.write(decrypted_data)

    print(f"{filename} has been decrypted successfully as {decrypted_filename}!")


def main():
    args = parse_args()

    
    try:
        salt = base64.b64decode(args.arg2)
        key = base64.b64decode(args.arg3)
    except Exception as e:
        print("Error decoding Base64 salt or key.")
        sys.exit(1)

    password = args.arg1.encode()

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    try:
        derived_key = kdf.derive(password)
    except Exception as e:
        print("Error deriving the key.")
        sys.exit(1)

    if key != derived_key:
        print("Error: The provided key does not match the derived key.")
        sys.exit(1)

    decrypt_file(args.arg4, key)


if __name__ == "__main__":
    main()
