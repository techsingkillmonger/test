import sys
import subprocess
import importlib.util
import os
import tempfile

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

def read_credentials(credential_file):
    with open(credential_file, 'r') as f:
        lines = f.readlines()
        return lines[0].strip(), lines[1].strip()  # return password and salt

if __name__ == '__main__':
    # Arguments passed from Pro Micro: input file, output file
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Create a temporary file to store the password and salt
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(b'YourPassword\n')  # Replace with actual password
        temp_file.write(b'a726d3cd829c72204ae1add61be23ffa\n')  # Replace with actual salt
        temp_file.flush()  # Make sure the file is written

        password, salt = read_credentials(temp_file.name)

        # IVs for both files
        iv_bat = "c835c64d5b9d758fd29823f7ee855801"  # Example IV for .bat
        iv_vbs = "d990fa53364de877296723a207f91ac5"  # Example IV for .vbs

        if input_file.endswith('bat.enc'):
            decrypt_file(input_file, output_file, password, salt, iv_bat)
        elif input_file.endswith('vbs.enc'):
            decrypt_file(input_file, output_file, password, salt, iv_vbs)
