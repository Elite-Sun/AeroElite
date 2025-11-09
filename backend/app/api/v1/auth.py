"""Authentication API Routes"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register new user"""
    logger.info(f"Registering user: {user_data.email}")

    try:
        from app.models.user import User
        from sqlalchemy import select, insert
        from passlib.context import CryptContext

        # Check if user exists
        stmt = select(User).where(User.email == user_data.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(user_data.password)

        # Create user
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_verified": False,  # TODO: Email verification
        }

        stmt = insert(User).values(**user_dict).returning(User)
        result = await db.execute(stmt)
        user = result.scalar_one()
        await db.commit()

        logger.info(f"User registered: {user.id}")
        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login user"""
    logger.info(f"Login attempt: {credentials.email}")

    try:
        from app.models.user import User
        from sqlalchemy import select
        from passlib.context import CryptContext
        from jose import jwt
        from datetime import datetime, timedelta
        from app.core.config import settings

        # Find user
        stmt = select(User).where(User.email == credentials.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Verify password
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if not pwd_context.verify(credentials.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Create token
        expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expires
        }

        access_token = jwt.encode(
            token_data,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM
        )

        logger.info(f"User logged in: {user.id}")

        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    # TODO: Add authentication dependency
    db: AsyncSession = Depends(get_db)
):
    """Get current user profile"""
    # For now, return dummy user
    from app.models.user import User
    from sqlalchemy import select

    stmt = select(User).limit(1)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
