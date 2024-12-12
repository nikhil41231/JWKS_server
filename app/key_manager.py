"""
This module is responsible for generating RSA keys and managing their storage in a file.
"""
import json
import time
import uuid
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEY_FILE = 'keys/key_data.json'
EXPIRY_DURATION = 3600  # 1 hour in seconds

def create_rsa_key(expiry=EXPIRY_DURATION):
    """
    Create a new RSA key pair, assign a unique key ID (kid), and set an expiry time.
    Returns:
        dict: A dictionary containing the key ID (kid), the private key, the public key,
              and the expiry timestamp for the key.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    key_id = str(uuid.uuid4())  # Generate a unique key ID
    expiry_time = time.time() + expiry  # Calculate the expiry time

    return {
        "kid": key_id,
        "private_key": private_pem.decode('utf-8'),
        "public_key": public_pem.decode('utf-8'),
        "expiry": expiry_time
    }

def store_key_to_file():
    """
    Create a new RSA key pair and save the key data to a JSON file.
    """
    try:
        key_info = create_rsa_key()
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)  # Ensure the directory exists
        with open(KEY_FILE, 'w', encoding='utf-8') as file:
            json.dump(key_info, file, indent=4)  # Write JSON data to file
        print("Key successfully saved.")
    except Exception as error:
        print(f"Error saving key: {error}")

def retrieve_key_from_file():
    """
    Retrieve the RSA key data from the JSON file.
    Returns:
        dict: The key data if the file exists and is valid; otherwise, None.
    """
    try:
        if os.path.isfile(KEY_FILE):
            with open(KEY_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        else:
            print("Key file not found.")
            return None
    except Exception as error:
        print(f"Error loading key: {error}")
        return None

# Example call to store the key (you can remove or comment this line in production)
store_key_to_file()
