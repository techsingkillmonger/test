import sys
import subprocess
import importlib.util

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check if pycryptodome is installed
package_name = 'pycryptodome'
spec = importlib.util.find_spec('Crypto')
if spec is None:
    print(f"Installing {package_name}...")
    install(package_name)

from Crypto.Cipher import AES
import hashlib
import os

def decrypt_file(input_file, output_file, password, salt_hex, iv_hex):
    salt = bytes.fromhex(salt_hex)
    iv = bytes.fromhex(iv_hex)

    # Derive the AES key from the password and salt
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)

    with open(input_file, 'rb') as f:
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    # Remove padding (PKCS7)
    padding_len = plaintext[-1]
    plaintext = plaintext[:-padding_len]

    with open(output_file, 'wb') as f:
        f.write(plaintext)

if __name__ == '__main__':
    # Arguments passed from Pro Micro: input file, output file, password, salt, iv
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    password = sys.argv[3]
    salt = sys.argv[4]
    iv = sys.argv[5]

    decrypt_file(input_file, output_file, password, salt, iv)
