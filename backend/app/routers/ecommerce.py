from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.models import User, Inspection
from app.schemas.schemas import EcommerceVerificationRequest, EcommerceVerificationResponse
from app.services.auth_service import get_current_user
from app.services.ecommerce_service import EcommerceService

router = APIRouter(prefix="/api/ecommerce", tags=["E-Commerce Verification"])

@router.post("/verify", response_model=EcommerceVerificationResponse)
def verify_ecommerce_listing(
    req: EcommerceVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    package_data = None
    if req.package_inspection_id:
        insp = db.query(Inspection).filter(Inspection.id == req.package_inspection_id).first()
        if insp:
            dec_map = {d.field_name: d.detected_value for d in insp.declarations}
            package_data = {
                "product_name": insp.product.name if insp.product else None,
                "mrp": dec_map.get("mrp"),
                "net_quantity": dec_map.get("net_quantity"),
                "manufacturer": dec_map.get("manufacturer"),
                "country_of_origin": dec_map.get("country_of_origin")
            }

    return EcommerceService.verify_listing(req, package_data)
