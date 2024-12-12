import json
import time
from flask import Flask, jsonify, request
import jwt
from app.key_manager import load_key_from_file
from app.config import JWT_EXPIRY_DURATION, JWT_ALGORITHM

app = Flask(__name__)

# Load RSA key data
key_data = load_key_from_file()

@app.route('/')
def home():
    """Simple home route to indicate that the server is running."""
    return "JWKS Server Running!"

@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    """Serve JWKS with the public key if it has not expired."""
    if key_data and key_data['expiry'] > time.time():
        return jsonify({
            "keys": [
                {
                    "kty": "RSA",
                    "kid": key_data['kid'],
                    "use": "sig",
                    "alg": JWT_ALGORITHM,
                    "n": key_data['public_key'],
                    "e": "AQAB"
                }
            ]
        })
    return jsonify({"keys": []})

@app.route('/auth', methods=['POST'])
def auth():
    """Generate a JWT token, with an optional expired token based on a query parameter."""
    expired = request.args.get('expired')
    now = time.time()

    payload = {
        "sub": "user123",
        "iat": now,
        "exp": now + JWT_EXPIRY_DURATION if not expired else now - 60
    }

    if key_data:
        token = jwt.encode(payload, key_data['private_key'], algorithm=JWT_ALGORITHM, headers={"kid": key_data['kid']})
        return jsonify({"token": token})
    return jsonify({"error": "Key data is not available"}), 500

if __name__ == '__main__':
    app.run(debug=True)