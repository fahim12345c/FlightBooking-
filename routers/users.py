"""
User management routes.

This module provides endpoints for:
- User registration with email verification
- User login with JWT tokens
- User profile management
- User logout
"""

from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from crud import users as crud_users
from crud.database import get_session
from schemas.users import UserCreate, UserRead
from external_services import emails
from sqlmodel import Session


router = APIRouter()


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_session),
):
    existing_user = crud_users.get_user_by_email(db, user_in.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = crud_users.create_user(db, user_in)

    background_tasks.add_task(emails.send_welcome_email, user_email=user.email)

    return user


# @router.post("/login")
# def login(
#     email: str,
#     password: str,
#     db: Session = Depends(get_db)
# ):
#     """
#     Authenticate user and return JWT tokens.

#     Args:
#         email: User email address
#         password: User password
#         db: Database session (dependency injection)

#     Returns:
#         Dictionary with access_token, refresh_token, and token_type

#     Raises:
#         HTTPException: 401 if credentials are invalid
#     """
#     try:
#         # Get user by email
#         user = crud_users.get_user_by_email(db, email)
#         if not user:
#             logger.warning(f"Login attempt with non-existent email: {email}")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid email or password"
#             )

#         # Verify password
#         if not crud_users.verify_password_for_user(password, user.hashed_password):
#             logger.warning(f"Login attempt with invalid password for: {email}")
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid email or password"
#             )

#         # Check if user is active
#         if not user.is_active:
#             logger.warning(f"Login attempt for inactive user: {email}")
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="User account is inactive"
#             )

#         # Create tokens
#         tokens = create_tokens(user.id)
#         logger.info(f"User logged in: {user.id}")

#         return tokens

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error during login: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error logging in"
#         )


# @router.get("/me", response_model=UserRead)
# def get_current_user(
#     user_id: str = Depends(get_current_user_id),
#     db: Session = Depends(get_db)
# ):
#     """
#     Get current authenticated user's profile.

#     Args:
#         user_id: Current user ID (dependency injection from JWT)
#         db: Database session (dependency injection)

#     Returns:
#         UserRead schema with user details

#     Raises:
#         HTTPException: 404 if user not found
#     """
#     user = crud_users.get_user_by_id(db, user_id)
#     if not user:
#         logger.warning(f"User not found: {user_id}")
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found"
#         )

#     return user


# @router.put("/me", response_model=UserRead)
# def update_current_user(
#     user_update: UserUpdate,
#     user_id: str = Depends(get_current_user_id),
#     db: Session = Depends(get_db)
# ):
#     """
#     Update current authenticated user's profile.

#     Args:
#         user_update: UserUpdate schema with fields to update
#         user_id: Current user ID (dependency injection from JWT)
#         db: Database session (dependency injection)

#     Returns:
#         Updated UserRead schema

#     Raises:
#         HTTPException:
#             - 404 if user not found
#             - 400 if validation fails
#     """
#     try:
#         user = crud_users.update_user(db, user_id, user_update)
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found"
#             )

#         logger.info(f"User updated: {user_id}")
#         return user

#     except ValueError as e:
#         logger.error(f"Validation error updating user: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
#     except Exception as e:
#         logger.error(f"Error updating user: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error updating user profile"
#         )


# @router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
# def delete_current_user(
#     user_id: str = Depends(get_current_user_id),
#     db: Session = Depends(get_db)
# ):
#     """
#     Delete current authenticated user's account.

#     Args:
#         user_id: Current user ID (dependency injection from JWT)
#         db: Database session (dependency injection)

#     Returns:
#         No content (204 status)

#     Raises:
#         HTTPException: 404 if user not found
#     """
#     try:
#         success = crud_users.delete_user(db, user_id)
#         if not success:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="User not found"
#             )

#         logger.info(f"User deleted: {user_id}")
#         return None

#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error deleting user: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error deleting user account"
#         )


# @router.get("/", response_model=list[UserRead])
# def list_users(
#     skip: int = 0,
#     limit: int = 100,
#     is_active: Optional[bool] = None,
#     user_id: str = Depends(get_current_user_id),
#     db: Session = Depends(get_db)
# ):
#     """
#     List all users (admin only - requires authentication).

#     Args:
#         skip: Number of records to skip (pagination)
#         limit: Maximum records to return
#         is_active: Filter by active status (optional)
#         user_id: Current user ID (dependency injection from JWT)
#         db: Database session (dependency injection)

#     Returns:
#         List of UserRead schemas
#     """
#     users = crud_users.list_users(
#         db,
#         skip=skip,
#         limit=limit,
#         is_active=is_active
#     )

#     logger.info(f"Listed users (skip={skip}, limit={limit})")
#     return users
