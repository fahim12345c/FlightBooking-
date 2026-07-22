# """
# Authentication utilities for FastAPI dependency injection.

# This module provides:
# - HTTP Bearer token extraction
# - Current user verification from tokens
# - Authentication exception handling
# """

# import logging
# from typing import Optional

# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthCredentials

# from utils.security import verify_token, get_user_id_from_token

# logger = logging.getLogger(__name__)

# security = HTTPBearer(description="JWT Bearer token authentication")


# async def get_current_user_id(credentials: HTTPAuthCredentials = Depends(security)) -> str:
#     """
#     Dependency to extract and verify the current user ID from JWT token.

#     Args:
#         credentials: HTTP Bearer token credentials (injected by FastAPI)

#     Returns:
#         User ID if token is valid

#     Raises:
#         HTTPException: If token is missing, invalid, or expired (401 Unauthorized)
#     """
#     token = credentials.credentials

#     user_id = get_user_id_from_token(token)
#     if not user_id:
#         logger.warning("Invalid or expired token")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     return user_id


# async def get_optional_user_id(
#     credentials: Optional[HTTPAuthCredentials] = Depends(HTTPBearer(auto_error=False))
# ) -> Optional[str]:
#     """
#     Optional dependency to extract user ID from JWT token if provided.

#     Args:
#         credentials: HTTP Bearer token credentials (optional, injected by FastAPI)

#     Returns:
#         User ID if valid token provided, None if no token provided or invalid
#     """
#     if not credentials:
#         return None

#     user_id = get_user_id_from_token(credentials.credentials)
#     if not user_id:
#         logger.debug("Invalid or expired token provided in optional auth")
#         return None

#     return user_id


# def verify_token_validity(token: str) -> bool:
#     """
#     Check if a token is valid without extracting user ID.

#     Args:
#         token: JWT token string to verify

#     Returns:
#         True if token is valid, False otherwise
#     """
#     payload = verify_token(token, token_type="access")
#     return payload is not None
