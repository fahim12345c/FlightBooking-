"""
Authentication utilities for FastAPI dependency injection.

This module provides:
- OAuth2 bearer token extraction
- Current user verification from tokens
- Authentication exception handling
"""

from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from utils.security import get_user_id_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    user_id = get_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_optional_user_id(
    token: Optional[str] = Depends(optional_oauth2_scheme),
) -> Optional[str]:
    if not token:
        return None

    return get_user_id_from_token(token)


def verify_token_validity(token: str) -> bool:
    return get_user_id_from_token(token) is not None
