from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User, Rule, AuditLog
from app.schemas.schemas import RuleResponse, RuleCreate, RuleUpdate
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/rules", tags=["Rule Repository"])

@router.get("", response_model=List[RuleResponse])
def list_rules(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Rule)
    if category and category != "ALL":
        query = query.filter(Rule.category == category)
    return query.order_by(Rule.rule_code.asc()).all()

@router.post("", response_model=RuleResponse)
def create_rule(
    rule_in: RuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Rule).filter(Rule.rule_code == rule_in.rule_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Rule with this rule code already exists")
    
    rule = Rule(**rule_in.dict())
    db.add(rule)
    db.commit()
    db.refresh(rule)

    audit = AuditLog(
        officer_id=current_user.id,
        action="RULE_CREATE",
        target_entity="RULE",
        entity_id=rule.rule_code,
        details=f"Created new Legal Metrology rule {rule.rule_code}: {rule.description[:50]}"
    )
    db.add(audit)
    db.commit()

    return rule

@router.put("/{id}", response_model=RuleResponse)
def update_rule(
    id: int,
    rule_update: RuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rule = db.query(Rule).filter(Rule.id == id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    for key, value in rule_update.dict(exclude_unset=True).items():
        setattr(rule, key, value)
    
    db.commit()
    db.refresh(rule)

    audit = AuditLog(
        officer_id=current_user.id,
        action="RULE_UPDATE",
        target_entity="RULE",
        entity_id=rule.rule_code,
        details=f"Updated Rule {rule.rule_code} parameters"
    )
    db.add(audit)
    db.commit()

    return rule

@router.post("/{id}/toggle", response_model=RuleResponse)
def toggle_rule_status(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rule = db.query(Rule).filter(Rule.id == id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    rule.is_active = not rule.is_active
    db.commit()
    db.refresh(rule)

    audit = AuditLog(
        officer_id=current_user.id,
        action="RULE_TOGGLE",
        target_entity="RULE",
        entity_id=rule.rule_code,
        details=f"Rule {rule.rule_code} active status toggled to {rule.is_active}"
    )
    db.add(audit)
    db.commit()

    return rule
