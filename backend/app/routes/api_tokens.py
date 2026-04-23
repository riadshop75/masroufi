from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.models import User, ApiToken
from app.schemas.api_token import ApiTokenCreate, ApiTokenResponse, ApiTokenWithSecret
from app.dependencies import get_current_user
from app.security import generate_api_token, hash_api_token, verify_api_token
from datetime import datetime

router = APIRouter(prefix="/api/v1/api-tokens", tags=["api-tokens"])

@router.post("", response_model=ApiTokenWithSecret)
async def create_api_token(
    token_data: ApiTokenCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Générer le token
    plain_token = generate_api_token()
    hashed_token = hash_api_token(plain_token)

    api_token = ApiToken(
        user_id=user.user_id,
        name=token_data.name,
        token_hash=hashed_token,
        scopes=token_data.scopes,
        is_active=True
    )
    db.add(api_token)
    db.commit()
    db.refresh(api_token)

    return ApiTokenWithSecret(
        token_id=api_token.token_id,
        name=api_token.name,
        scopes=api_token.scopes,
        is_active=api_token.is_active,
        last_used=api_token.last_used,
        created_at=api_token.created_at,
        token=plain_token
    )

@router.get("", response_model=list[ApiTokenResponse])
async def list_api_tokens(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tokens = db.query(ApiToken).filter(ApiToken.user_id == user.user_id).all()
    return [ApiTokenResponse.from_orm(t) for t in tokens]

@router.get("/{token_id}", response_model=ApiTokenResponse)
async def get_api_token(
    token_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    token = db.query(ApiToken).filter(
        ApiToken.token_id == token_id,
        ApiToken.user_id == user.user_id
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API token not found"
        )

    return ApiTokenResponse.from_orm(token)

@router.put("/{token_id}")
async def revoke_api_token(
    token_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    token = db.query(ApiToken).filter(
        ApiToken.token_id == token_id,
        ApiToken.user_id == user.user_id
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API token not found"
        )

    token.is_active = not token.is_active
    db.commit()
    db.refresh(token)

    return {
        "message": f"API token {'disabled' if not token.is_active else 'enabled'}",
        "is_active": token.is_active
    }

@router.delete("/{token_id}")
async def delete_api_token(
    token_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    token = db.query(ApiToken).filter(
        ApiToken.token_id == token_id,
        ApiToken.user_id == user.user_id
    ).first()

    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API token not found"
        )

    db.delete(token)
    db.commit()

    return {"message": "API token deleted"}
