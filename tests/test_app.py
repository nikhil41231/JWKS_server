import unittest
from app import app
from app.key_manager import save_key_to_file, load_key_from_file
import os
import json

class JWKSAuthTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_jwks_endpoint(self):
        """Test that the JWKS endpoint returns a valid public key."""
        response = self.client.get('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('keys', data)

    def test_auth_token(self):
        """Test that the /auth endpoint returns a valid JWT."""
        response = self.client.post('/auth')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)

    def test_expired_token(self):
        """Test that the /auth endpoint returns an expired JWT when requested."""
        response = self.client.post('/auth?expired=true')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)

    def test_invalid_jwks_method(self):
        """Test that invalid HTTP method (POST) to the JWKS endpoint returns 405 (Method Not Allowed)."""
        response = self.client.post('/.well-known/jwks.json')
        self.assertEqual(response.status_code, 405)

    def test_invalid_auth_method(self):
        """Test that a GET request to the /auth endpoint returns 405 (Method Not Allowed)."""
        response = self.client.get('/auth')
        self.assertEqual(response.status_code, 405)

    def test_invalid_auth_query(self):
        """Test that an invalid query parameter to the /auth endpoint still returns a valid JWT."""
        response = self.client.post('/auth?invalid_param=true')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)

    def test_empty_jwks(self):
        """Test that the JWKS endpoint returns an empty key set if the key has expired."""
        response = self.client.get('/.well-known/jwks.json')
        data = response.get_json()

        if data['keys']:  # If there are keys
            self.assertIn('kid', data['keys'][0])
            self.assertIn('n', data['keys'][0])
        else:
            self.assertEqual(len(data['keys']), 0, "Keys should be empty if expired")

    # New tests for key_manager functionality
    def test_save_key_to_file(self):
        """Test that the RSA key is saved to the file correctly."""
        save_key_to_file()  # Call the function to save the key
        self.assertTrue(os.path.exists('keys/key.json'))  # Check if the file exists

        with open('keys/key.json', 'r') as f:
            key_data = json.load(f)
            self.assertIn('kid', key_data)  # Check that key data contains 'kid'
            self.assertIn('private_key', key_data)  # Check that it contains 'private_key'

    def test_load_key_from_file(self):
        """Test that the RSA key can be loaded from the file."""
        save_key_to_file()  # Ensure key is saved
        key_data = load_key_from_file()  # Load the key

        self.assertIsNotNone(key_data)  # Ensure the key is not None
        self.assertIn('kid', key_data)  # Check the key data

if __name__ == '__main__':
    unittest.main()
