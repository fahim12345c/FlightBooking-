"""
Security utilities for authentication and password management.

This module provides:
- JWT token generation and verification
- Password hashing and verification using passlib
- Configuration for security settings
"""

from datetime import datetime, timedelta, timezone
import os

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext

# Security configuration constants
SECRET_KEY = os.getenv(
    "SECRET_KEY", "your-secret-key-change-this-in-production-12345678"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Bcrypt hash to verify against

    Returns:
        True if password matches, False otherwise
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except (ExpiredSignatureError, InvalidTokenError):
        return None


def get_user_id_from_token(token: str) -> str | None:
    payload = decode_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    return str(user_id)
