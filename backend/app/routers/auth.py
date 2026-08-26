import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User, AuditLog
from app.schemas.schemas import LoginRequest, Token, UserResponse
from app.services.auth_service import verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.officer_id == req.officer_id.strip()).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Officer ID or Password. Demo credentials: Officer ID: LMO001, Password: admin123"
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Officer account is inactive")

    # Create token
    access_token = create_access_token(data={"sub": user.officer_id, "role": user.role})
    
    # Audit log
    audit = AuditLog(
        officer_id=user.id,
        action="LOGIN",
        target_entity="USER",
        entity_id=user.officer_id,
        details="Officer logged into Legal Metrology Compliance Enforcement Portal"
    )
    db.add(audit)
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "officer": {
            "id": user.id,
            "officer_id": user.officer_id,
            "full_name": user.full_name,
            "designation": user.designation,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
