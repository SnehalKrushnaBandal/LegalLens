import os
import uuid
import shutil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.config import UPLOAD_DIR
from app.database.connection import get_db
from app.database.models import User, Product, Inspection, AuditLog
from app.schemas.schemas import ProductResponse, ProductCreate
from app.services.auth_service import get_current_user
from app.services.ocr_service import OCRService, DEMO_PRODUCTS

router = APIRouter(prefix="/api/products", tags=["Products & Scanning"])

@router.post("/upload")
async def upload_product_image(
    file: Optional[UploadFile] = File(None),
    demo_product_id: Optional[str] = Form(None),
    product_name: Optional[str] = Form(None),
    category: Optional[str] = Form("Packaged Food / Grocery"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Uploads or selects a product package image for inspection.
    """
    image_path = None
    original_filename = None
    
    if demo_product_id and demo_product_id in DEMO_PRODUCTS:
        # Generate or locate synthetic demo image
        synth_img = OCRService.generate_synthetic_package_image(demo_product_id)
        saved_name = f"demo_{demo_product_id}_{uuid.uuid4().hex[:6]}.jpg"
        target_path = UPLOAD_DIR / saved_name
        synth_img.save(target_path, quality=95)
        image_path = str(target_path)
        original_filename = f"{demo_product_id}.jpg"
    elif file:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload JPG or PNG.")
        
        saved_name = f"scan_{uuid.uuid4().hex[:8]}{ext}"
        target_path = UPLOAD_DIR / saved_name
        with open(target_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        image_path = str(target_path)
        original_filename = file.filename
    else:
        # Default fallback to Basmati Rice demo
        demo_product_id = "basmati_rice"
        synth_img = OCRService.generate_synthetic_package_image(demo_product_id)
        saved_name = f"demo_{demo_product_id}_{uuid.uuid4().hex[:6]}.jpg"
        target_path = UPLOAD_DIR / saved_name
        synth_img.save(target_path, quality=95)
        image_path = str(target_path)
        original_filename = "basmati_rice.jpg"

    # Preprocess image & estimate quality
    preprocess_metrics = OCRService.preprocess_image(image_path)

    return {
        "status": "UPLOADED",
        "image_path": f"/uploads/{os.path.basename(image_path)}",
        "raw_image_path": image_path,
        "filename": original_filename,
        "demo_product_id": demo_product_id,
        "product_name": product_name or (DEMO_PRODUCTS[demo_product_id]["product_name"] if demo_product_id in DEMO_PRODUCTS else "Scanned Packaged Commodity"),
        "category": category or (DEMO_PRODUCTS[demo_product_id]["category"] if demo_product_id in DEMO_PRODUCTS else "General"),
        "image_metrics": preprocess_metrics
    }

@router.post("/analyze")
async def analyze_product(
    raw_image_path: str = Form(...),
    demo_product_id: Optional[str] = Form(None),
    product_name: Optional[str] = Form(None),
    category: Optional[str] = Form("General Food / Grocery"),
    current_user: User = Depends(get_current_user)
):
    """
    Performs OCR extraction, identifies mandatory declarations, and extracts visual bounding boxes.
    """
    if not os.path.exists(raw_image_path):
        # Try finding in upload directory
        raw_image_path = str(UPLOAD_DIR / os.path.basename(raw_image_path))
        if not os.path.exists(raw_image_path):
            raise HTTPException(status_code=404, detail="Uploaded package image not found on server")

    declarations, evidence_items, evidence_img_path = OCRService.extract_declarations(
        image_path=raw_image_path,
        demo_product_id=demo_product_id,
        custom_product_name=product_name,
        category=category
    )

    return {
        "status": "ANALYZED",
        "raw_image_path": raw_image_path,
        "evidence_image_path": f"/uploads/evidence/{os.path.basename(evidence_img_path)}",
        "declarations": declarations,
        "evidence_items": evidence_items,
        "demo_product_id": demo_product_id
    }

@router.get("", response_model=List[ProductResponse])
def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product)
    if category:
        query = query.filter(Product.category == category)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%") | Product.manufacturer_name.ilike(f"%{search}%"))
    
    products = query.order_by(Product.id.desc()).all()
    results = []
    for p in products:
        insp_count = len(p.inspections)
        latest_status = p.inspections[-1].compliance_status if p.inspections else "NOT_INSPECTED"
        results.append(ProductResponse(
            id=p.id,
            product_code=p.product_code,
            name=p.name,
            category=p.category,
            manufacturer_name=p.manufacturer_name,
            manufacturer_address=p.manufacturer_address,
            standard_mrp=p.standard_mrp,
            net_quantity=p.net_quantity,
            image_url=p.image_url,
            created_at=p.created_at,
            updated_at=p.updated_at,
            inspection_count=insp_count,
            latest_status=latest_status
        ))
    return results

@router.get("/{id}", response_model=ProductResponse)
def get_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    p = db.query(Product).filter(Product.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    insp_count = len(p.inspections)
    latest_status = p.inspections[-1].compliance_status if p.inspections else "NOT_INSPECTED"
    return ProductResponse(
        id=p.id,
        product_code=p.product_code,
        name=p.name,
        category=p.category,
        manufacturer_name=p.manufacturer_name,
        manufacturer_address=p.manufacturer_address,
        standard_mrp=p.standard_mrp,
        net_quantity=p.net_quantity,
        image_url=p.image_url,
        created_at=p.created_at,
        updated_at=p.updated_at,
        inspection_count=insp_count,
        latest_status=latest_status
    )
