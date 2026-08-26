import datetime
import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import (
    User, Product, Inspection, ExtractedDeclaration, Violation, InspectionEvidence, Rule, AuditLog
)
from app.schemas.schemas import (
    InspectionResponse, InspectionDetailResponse, InspectionVerifyRequest, ViolationStatusUpdate
)
from app.services.auth_service import get_current_user
from app.services.rule_engine import RuleEngine

router = APIRouter(prefix="/api/inspections", tags=["Inspections"])

@router.post("", response_model=InspectionDetailResponse)
def create_inspection(
    payload: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Finalizes OCR declarations, evaluates Legal Metrology rules, and stores inspection record.
    """
    raw_image_path = payload.get("raw_image_path", "")
    evidence_image_path = payload.get("evidence_image_path")
    product_name = payload.get("product_name", "Packaged Commodity")
    category = payload.get("category", "Food & Grocery")
    declarations_in = payload.get("declarations", [])
    evidence_items_in = payload.get("evidence_items", [])
    demo_product_id = payload.get("demo_product_id")

    # 1. Look up or create Product record
    product = db.query(Product).filter(Product.name == product_name).first()
    if not product:
        # Extract mfg and mrp from declarations
        dec_dict = {d["field_name"]: d.get("detected_value") for d in declarations_in}
        product = Product(
            product_code=f"PRD-{uuid.uuid4().hex[:6].upper()}",
            name=product_name,
            category=category,
            manufacturer_name=dec_dict.get("manufacturer"),
            manufacturer_address=dec_dict.get("address"),
            net_quantity=dec_dict.get("net_quantity"),
            image_url=evidence_image_path or raw_image_path
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    # 2. Run Configurable Rule Engine
    active_rules = db.query(Rule).filter(Rule.is_active == True).all()
    compliance_status, overall_score, breakdown, violations_list = RuleEngine.evaluate_compliance(
        declarations=declarations_in,
        db_rules=active_rules
    )

    # 3. Create Inspection record
    inspection_num = f"INSP-2026-{uuid.uuid4().hex[:6].upper()}"
    inspection = Inspection(
        inspection_number=inspection_num,
        product_id=product.id,
        officer_id=current_user.id,
        image_path=raw_image_path,
        evidence_image_path=evidence_image_path,
        compliance_status=compliance_status,
        compliance_score=overall_score,
        score_breakdown=breakdown,
        inspection_date=datetime.datetime.utcnow(),
        remarks=payload.get("remarks", "AI-assisted screening completed."),
        officer_verified=False
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)

    # 4. Save Extracted Declarations
    for dec in declarations_in:
        d_record = ExtractedDeclaration(
            inspection_id=inspection.id,
            field_name=dec.get("field_name"),
            detected_value=dec.get("detected_value"),
            is_present=dec.get("is_present", True),
            confidence=dec.get("confidence", 0.95),
            estimated_font_size_px=dec.get("estimated_font_size_px", 14.0),
            readability_status=dec.get("readability_status", "PASS"),
            raw_bounding_box=dec.get("raw_bounding_box"),
            is_officer_edited=dec.get("is_officer_edited", False)
        )
        db.add(d_record)

    # 5. Save Violations
    for v in violations_list:
        rule_obj = db.query(Rule).filter(Rule.rule_code == v.get("rule_code")).first()
        viol = Violation(
            inspection_id=inspection.id,
            rule_id=rule_obj.id if rule_obj else None,
            category=v.get("category", "General"),
            issue=v.get("issue", ""),
            detected_value=v.get("detected_value"),
            expected_requirement=v.get("expected_requirement", ""),
            severity=v.get("severity", "HIGH"),
            confidence=v.get("confidence", 0.95),
            status="ACTIVE",
            evidence_zone=v.get("evidence_zone")
        )
        db.add(viol)

    # 6. Save Evidence Items
    for ev in evidence_items_in:
        ev_item = InspectionEvidence(
            inspection_id=inspection.id,
            evidence_type=ev.get("evidence_type", "BOUNDING_BOX"),
            label=ev.get("label", "Zone"),
            bounding_box_json=ev.get("bounding_box_json", {}),
            description=ev.get("description", "")
        )
        db.add(ev_item)

    # 7. Audit Log
    audit = AuditLog(
        officer_id=current_user.id,
        action="INSPECTION_CREATED",
        target_entity="INSPECTION",
        entity_id=inspection.inspection_number,
        details=f"Compliance check finalized with status: {compliance_status} ({overall_score}/100)"
    )
    db.add(audit)
    db.commit()

    return get_inspection_detail_response(inspection.id, db)

@router.get("", response_model=List[InspectionResponse])
def list_inspections(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Inspection)
    
    if status and status != "ALL":
        query = query.filter(Inspection.compliance_status == status)
    
    inspections = query.order_by(Inspection.inspection_date.desc()).all()
    results = []
    for insp in inspections:
        prod = insp.product
        p_name = prod.name if prod else "Packaged Commodity"
        p_cat = prod.category if prod else "General"
        p_mfg = prod.manufacturer_name if prod else "Declared on Package"
        
        if search:
            s_lower = search.lower()
            if s_lower not in p_name.lower() and s_lower not in p_mfg.lower() and s_lower not in insp.inspection_number.lower():
                continue
        
        if category and category != "ALL" and category.lower() not in p_cat.lower():
            continue

        results.append(InspectionResponse(
            id=insp.id,
            inspection_number=insp.inspection_number,
            product_id=insp.product_id,
            product_name=p_name,
            category=p_cat,
            manufacturer=p_mfg,
            officer_id=insp.officer_id,
            officer_name=insp.officer.full_name if insp.officer else "Officer",
            image_path=insp.image_path,
            evidence_image_path=insp.evidence_image_path,
            compliance_status=insp.compliance_status,
            compliance_score=insp.compliance_score,
            score_breakdown=insp.score_breakdown,
            inspection_date=insp.inspection_date,
            remarks=insp.remarks,
            officer_verified=insp.officer_verified,
            violations_count=len(insp.violations)
        ))
    return results

@router.get("/{id}", response_model=InspectionDetailResponse)
def get_inspection(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_inspection_detail_response(id, db)

@router.put("/{id}/verify", response_model=InspectionDetailResponse)
def verify_inspection(
    id: int,
    req: InspectionVerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    insp = db.query(Inspection).filter(Inspection.id == id).first()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    insp.officer_verified = True
    insp.verified_at = datetime.datetime.utcnow()
    if req.remarks:
        insp.remarks = req.remarks
    if req.final_status:
        insp.compliance_status = req.final_status

    audit = AuditLog(
        officer_id=current_user.id,
        action="VERIFICATION_SIGN",
        target_entity="INSPECTION",
        entity_id=insp.inspection_number,
        details=f"Officer {current_user.officer_id} verified inspection with final status: {insp.compliance_status}"
    )
    db.add(audit)
    db.commit()
    db.refresh(insp)

    return get_inspection_detail_response(id, db)

@router.put("/{id}/violations/{viol_id}")
def update_violation_status(
    id: int,
    viol_id: int,
    status_update: ViolationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    viol = db.query(Violation).filter(Violation.id == viol_id, Violation.inspection_id == id).first()
    if not viol:
        raise HTTPException(status_code=404, detail="Violation not found")
    
    viol.status = status_update.status
    db.commit()
    return {"status": "UPDATED", "violation_id": viol_id, "new_status": viol.status}

def get_inspection_detail_response(insp_id: int, db: Session) -> InspectionDetailResponse:
    insp = db.query(Inspection).filter(Inspection.id == insp_id).first()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    prod = insp.product
    p_name = prod.name if prod else "Packaged Commodity"
    p_cat = prod.category if prod else "General"
    p_mfg = prod.manufacturer_name if prod else "Declared on Package"

    # Format violations with rule codes & legal references
    violations_formatted = []
    for v in insp.violations:
        violations_formatted.append({
            "id": v.id,
            "inspection_id": v.inspection_id,
            "rule_id": v.rule_id,
            "category": v.category,
            "issue": v.issue,
            "detected_value": v.detected_value,
            "expected_requirement": v.expected_requirement,
            "severity": v.severity,
            "confidence": v.confidence,
            "status": v.status,
            "evidence_zone": v.evidence_zone,
            "legal_reference": v.rule.legal_reference if v.rule else "Legal Metrology (PC) Rules, 2011"
        })

    return InspectionDetailResponse(
        id=insp.id,
        inspection_number=insp.inspection_number,
        product_id=insp.product_id,
        product_name=p_name,
        category=p_cat,
        manufacturer=p_mfg,
        officer_id=insp.officer_id,
        officer_name=insp.officer.full_name if insp.officer else "Officer",
        image_path=insp.image_path,
        evidence_image_path=insp.evidence_image_path,
        compliance_status=insp.compliance_status,
        compliance_score=insp.compliance_score,
        score_breakdown=insp.score_breakdown,
        inspection_date=insp.inspection_date,
        remarks=insp.remarks,
        officer_verified=insp.officer_verified,
        violations_count=len(insp.violations),
        declarations=insp.declarations,
        violations=violations_formatted,
        evidence_items=insp.evidence_items,
        product=prod,
        officer=insp.officer
    )
