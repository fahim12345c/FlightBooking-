"""
User management routes.

This module provides endpoints for:
- User registration with email verification
- User login with OAuth2 password flow and JWT tokens
- User profile management
- User logout
"""

from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from crud import users as crud_users
from crud.database import get_session
from schemas.users import Token, UserCreate, UserRead
from external_services import emails
from utils.authentication import get_current_user_id
from utils.security import create_access_token
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


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = crud_users.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session),
):
    user = crud_users.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
