import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.config import REPORTS_DIR
from app.database.connection import get_db
from app.database.models import User, Inspection
from app.services.auth_service import get_current_user
from app.services.pdf_service import PDFReportService

router = APIRouter(prefix="/api/reports", tags=["Inspection Reports (PDF)"])

@router.post("/{inspection_id}/generate")
def generate_pdf_report(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    insp = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection record not found")

    # Assemble report payload
    prod = insp.product
    inspection_data = {
        "inspection_number": insp.inspection_number,
        "inspection_date": insp.inspection_date.strftime("%d %B %Y, %I:%M %p"),
        "officer_id": insp.officer.officer_id if insp.officer else current_user.officer_id,
        "officer_name": insp.officer.full_name if insp.officer else current_user.full_name,
        "product_name": prod.name if prod else "Packaged Commodity",
        "category": prod.category if prod else "General Goods",
        "manufacturer": prod.manufacturer_name if prod else "Declared on Package",
        "compliance_status": insp.compliance_status,
        "compliance_score": insp.compliance_score,
        "score_breakdown": insp.score_breakdown or {},
        "remarks": insp.remarks,
        "declarations": [
            {
                "field_name": d.field_name,
                "detected_value": d.detected_value,
                "is_present": d.is_present,
                "confidence": d.confidence,
                "estimated_font_size_px": d.estimated_font_size_px,
                "readability_status": d.readability_status
            } for d in insp.declarations
        ],
        "violations": [
            {
                "rule_code": v.rule.rule_code if v.rule else "LM-PC",
                "category": v.category,
                "issue": v.issue,
                "detected_value": v.detected_value,
                "expected_requirement": v.expected_requirement,
                "severity": v.severity,
                "legal_reference": v.rule.legal_reference if v.rule else "Legal Metrology Rules 2011"
            } for v in insp.violations
        ]
    }

    pdf_file_path = PDFReportService.generate_inspection_pdf(inspection_data)
    filename = os.path.basename(pdf_file_path)

    return {
        "status": "GENERATED",
        "inspection_id": inspection_id,
        "filename": filename,
        "download_url": f"/api/reports/{inspection_id}/download"
    }

@router.get("/{inspection_id}/download")
def download_pdf_report(
    inspection_id: int,
    db: Session = Depends(get_db)
):
    insp = db.query(Inspection).filter(Inspection.id == inspection_id).first()
    if not insp:
        raise HTTPException(status_code=404, detail="Inspection record not found")

    pdf_filename = f"Inspection_Report_{insp.inspection_number}.pdf"
    pdf_path = REPORTS_DIR / pdf_filename

    # If not already generated on disk, generate it now
    if not os.path.exists(pdf_path):
        prod = insp.product
        inspection_data = {
            "inspection_number": insp.inspection_number,
            "inspection_date": insp.inspection_date.strftime("%d %B %Y, %I:%M %p"),
            "officer_id": insp.officer.officer_id if insp.officer else "LMO001",
            "officer_name": insp.officer.full_name if insp.officer else "Inspector Rajesh Sharma",
            "product_name": prod.name if prod else "Packaged Commodity",
            "category": prod.category if prod else "General Goods",
            "manufacturer": prod.manufacturer_name if prod else "Declared on Package",
            "compliance_status": insp.compliance_status,
            "compliance_score": insp.compliance_score,
            "score_breakdown": insp.score_breakdown or {},
            "remarks": insp.remarks,
            "declarations": [
                {
                    "field_name": d.field_name,
                    "detected_value": d.detected_value,
                    "is_present": d.is_present,
                    "confidence": d.confidence,
                    "estimated_font_size_px": d.estimated_font_size_px,
                    "readability_status": d.readability_status
                } for d in insp.declarations
            ],
            "violations": [
                {
                    "rule_code": v.rule.rule_code if v.rule else "LM-PC",
                    "category": v.category,
                    "issue": v.issue,
                    "detected_value": v.detected_value,
                    "expected_requirement": v.expected_requirement,
                    "severity": v.severity,
                    "legal_reference": v.rule.legal_reference if v.rule else "Legal Metrology Rules 2011"
                } for v in insp.violations
            ]
        }
        pdf_path = PDFReportService.generate_inspection_pdf(inspection_data)

    return FileResponse(
        path=str(pdf_path),
        filename=pdf_filename,
        media_type="application/pdf"
    )
