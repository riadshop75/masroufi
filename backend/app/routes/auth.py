from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas.user import (
    UserSignup, UserLogin, TokenResponse, TokenRefresh, UserResponse, UserUpdate
)
from app.security import (
    hash_password, verify_password, create_access_token, create_refresh_token, verify_token
)
from app.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/signup", response_model=TokenResponse)
async def signup(
    user_data: UserSignup,
    db: Session = Depends(get_db)
):
    # Vérifier que l'email n'existe pas
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Créer l'utilisateur
    new_user = User(
        user_id=uuid.uuid4(),
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        name=user_data.name,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Générer les tokens
    access_token = create_access_token(str(new_user.user_id))
    refresh_token = create_refresh_token(str(new_user.user_id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(new_user)
    )

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    # Chercher l'utilisateur
    user = db.query(User).filter(User.email == credentials.email).first()
    if user is None or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Générer les tokens
    access_token = create_access_token(str(user.user_id))
    refresh_token = create_refresh_token(str(user.user_id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user)
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    refresh_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    # Vérifier le refresh token
    user_id = verify_token(refresh_data.refresh_token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    # Chercher l'utilisateur
    try:
        user = db.query(User).filter(User.user_id == uuid.UUID(user_id)).first()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Générer un nouveau access token
    access_token = create_access_token(str(user.user_id))
    refresh_token = create_refresh_token(str(user.user_id))

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user)
    )

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.from_orm(user)

@router.put("/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.name:
        user.name = user_update.name

    if user_update.password:
        user.password_hash = hash_password(user_update.password)

    db.commit()
    db.refresh(user)
    return UserResponse.from_orm(user)

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
