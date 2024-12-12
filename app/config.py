"""
Configuration module for the JWKS server.
Currently, this file contains settings for the server (can be expanded as needed).
"""

# JWT Settings
JWT_EXPIRY_DURATION = 600  # 10 minutes (can be used in routes.py)
JWT_ALGORITHM = "RS256"
