# """
# FastAPI dependency injection utilities.

# This module provides:
# - Database session dependency for CRUD operations
# - Pagination parameters
# """

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, Session
# import os

# # Database configuration from environment variables
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "sqlite:///./flightbooking.db"
# )

# # Create engine
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
# )

# # Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db() -> Session:
#     """
#     Dependency that provides a database session.

#     Yields:
#         SQLAlchemy Session object

#     Usage:
#         @router.get("/items")
#         def get_items(db: Session = Depends(get_db)):
#             return crud.get_items(db)
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# def get_pagination_params(skip: int = 0, limit: int = 100):
#     """
#     Dependency for pagination parameters.

#     Args:
#         skip: Number of records to skip
#         limit: Maximum number of records to return

#     Returns:
#         Dictionary with skip and limit parameters
#     """
#     return {"skip": max(0, skip), "limit": min(limit, 100)}
