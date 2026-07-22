"""
CRUD operations for User management.

This module provides all database operations for users:
- Create new users with password hashing
- Retrieve users by ID or email
- Update user information
- Delete users
- List active/inactive users
"""

from sqlmodel import select, Session
from schemas.users import UserCreate
from models.users import UserInDB
from utils.security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.exec(select(UserInDB).where(UserInDB.email == email)).first()


def create_user(db: Session, user: UserCreate):
    print("Password:", repr(user.password))
    print("Length:", len(user.password))
    hashed_password = hash_password(user.password)

    # Create new user instance
    db_user = UserInDB(
        email=user.email,
        password=hashed_password,
    )

    # Add to session and commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# def verify_password_for_user(password: str, password_hash: str) -> bool:
#     """
#     Verify a plaintext password against a user's stored hash.

#     Args:
#         password: Plaintext password to verify
#         password_hash: Hashed password to verify against

#     Returns:
#         True if password matches, False otherwise
#     """
#     return verify_password(password, password_hash)


# def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
#     """
#     Update user information.

#     Args:
#         db: Database session
#         user_id: UUID of the user to update
#         user_update: UserUpdate schema with fields to update

#     Returns:
#         Updated User object if found, None otherwise

#     Raises:
#         ValueError: If trying to update to an existing email
#     """
#     db_user = get_user_by_id(db, user_id)
#     if not db_user:
#         logger.warning(f"Attempted to update non-existent user: {user_id}")
#         return None

#     try:
#         # Check if new email already exists (if email is being updated)
#         if user_update.email and user_update.email != db_user.email:
#             existing_user = get_user_by_email(db, user_update.email)
#             if existing_user:
#                 logger.warning(f"Attempted to update user email to existing email: {user_update.email}")
#                 raise ValueError(f"Email {user_update.email} is already in use")

#         # Update fields if provided
#         update_data = user_update.dict(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(db_user, field, value)

#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)

#         logger.info(f"Updated user: {user_id}")
#         return db_user

#     except IntegrityError as e:
#         db.rollback()
#         logger.error(f"Database integrity error while updating user: {str(e)}")
#         raise ValueError("Email already in use") from e
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Unexpected error while updating user: {str(e)}")
#         raise


# def delete_user(db: Session, user_id: str) -> bool:
#     """
#     Delete a user by ID.

#     Args:
#         db: Database session
#         user_id: UUID of the user to delete

#     Returns:
#         True if user was deleted, False if user not found
#     """
#     db_user = get_user_by_id(db, user_id)
#     if not db_user:
#         logger.warning(f"Attempted to delete non-existent user: {user_id}")
#         return False

#     try:
#         db.delete(db_user)
#         db.commit()
#         logger.info(f"Deleted user: {user_id}")
#         return True

#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error while deleting user {user_id}: {str(e)}")
#         raise


# def list_users(
#     db: Session,
#     skip: int = 0,
#     limit: int = 100,
#     is_active: Optional[bool] = None
# ) -> list[User]:
#     """
#     List users with optional filtering.

#     Args:
#         db: Database session
#         skip: Number of records to skip (pagination)
#         limit: Maximum number of records to return
#         is_active: Filter by active status (None = no filter)

#     Returns:
#         List of User objects
#     """
#     query = db.query(User)

#     if is_active is not None:
#         query = query.filter(User.is_active == is_active)

#     return query.offset(skip).limit(limit).all()


# def get_active_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
#     """
#     Get all active users.

#     Args:
#         db: Database session
#         skip: Number of records to skip (pagination)
#         limit: Maximum number of records to return

#     Returns:
#         List of active User objects
#     """
#     return list_users(db, skip=skip, limit=limit, is_active=True)


# def get_inactive_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
#     """
#     Get all inactive users.

#     Args:
#         db: Database session
#         skip: Number of records to skip (pagination)
#         limit: Maximum number of records to return

#     Returns:
#         List of inactive User objects
#     """
#     return list_users(db, skip=skip, limit=limit, is_active=False)


# def update_user(db: Session, user_id: str, user_update: UserUpdate) -> Optional[User]:
#     """
#     Update user information.

#     Args:
#         db: Database session
#         user_id: UUID of the user to update
#         user_update: UserUpdate schema with fields to update

#     Returns:
#         Updated User object if found, None otherwise

#     Raises:
#         ValueError: If trying to update to an existing email
#     """
#     db_user = get_user_by_id(db, user_id)
#     if not db_user:
#         logger.warning(f"Attempted to update non-existent user: {user_id}")
#         return None

#     try:
#         # Check if new email already exists (if email is being updated)
#         if user_update.email and user_update.email != db_user.email:
#             existing_user = get_user_by_email(db, user_update.email)
#             if existing_user:
#                 logger.warning(f"Attempted to update user email to existing email: {user_update.email}")
#                 raise ValueError(f"Email {user_update.email} is already in use")

#         # Update fields if provided
#         update_data = user_update.dict(exclude_unset=True)
#         for field, value in update_data.items():
#             setattr(db_user, field, value)

#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)

#         logger.info(f"Updated user: {user_id}")
#         return db_user

#     except IntegrityError as e:
#         db.rollback()
#         logger.error(f"Database integrity error while updating user: {str(e)}")
#         raise ValueError("Email already in use") from e
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Unexpected error while updating user: {str(e)}")
#         raise


# def delete_user(db: Session, user_id: str) -> bool:
#     """
#     Delete a user by ID.

#     Args:
#         db: Database session
#         user_id: UUID of the user to delete

#     Returns:
#         True if user was deleted, False if user not found
#     """
#     db_user = get_user_by_id(db, user_id)
#     if not db_user:
#         logger.warning(f"Attempted to delete non-existent user: {user_id}")
#         return False

#     try:
#         db.delete(db_user)
#         db.commit()
#         logger.info(f"Deleted user: {user_id}")
#         return True

#     except Exception as e:
#         db.rollback()
#         logger.error(f"Error while deleting user {user_id}: {str(e)}")
#         raise


# def list_users(
#     db: Session,
#     skip: int = 0,
#     limit: int = 100,
#     is_active: Optional[bool] = None
# ) -> list[User]:
#     """
#     List users with optional filtering.

#     Args:
#         db: Database session
#         skip: Number of records to skip (pagination)
#         limit: Maximum number of records to return
#         is_active: Filter by active status (None = no filter)

#     Returns:
#         List of User objects
#     """
#     query = db.query(User)

#     if is_active is not None:
#         query = query.filter(User.is_active == is_active)

#     return query.offset(skip).limit(limit).all()


# def get_active_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
#     """
#     Get all active users.

#     Args:
#         db: Database session
#         skip: Number of records to skip (pagination)
#         limit: Maximum number of records to return

#     Returns:
#         List of active User objects
#     """
#     return list_users(db, skip=skip, limit=limit, is_active=True)


# def get_inactive_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
#     """
#     Get all inactive users.

#     Args:
#         db: Database session
#         skip: Number of records to skip (pagination)
#         limit: Maximum number of records to return

#     Returns:
#         List of inactive User objects
#     """
#     return list_users(db, skip=skip, limit=limit, is_active=False)
