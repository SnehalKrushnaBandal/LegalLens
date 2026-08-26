import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Auth Schemas ---
class LoginRequest(BaseModel):
    officer_id: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    officer: Dict[str, Any]

class UserResponse(BaseModel):
    id: int
    officer_id: str
    full_name: str
    designation: str
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True

# --- Declaration Schemas ---
class DeclarationBase(BaseModel):
    field_name: str
    detected_value: Optional[str] = None
    is_present: bool = True
    confidence: float = 0.95
    estimated_font_size_px: Optional[float] = None
    readability_status: Optional[str] = "PASS"
    raw_bounding_box: Optional[Dict[str, Any]] = None
    is_officer_edited: bool = False

class DeclarationUpdate(BaseModel):
    field_name: str
    detected_value: Optional[str] = None
    is_present: bool = True

class DeclarationResponse(DeclarationBase):
    id: int
    inspection_id: int

    class Config:
        from_attributes = True

# --- Violation Schemas ---
class ViolationResponse(BaseModel):
    id: int
    inspection_id: int
    rule_id: Optional[int] = None
    category: str
    issue: str
    detected_value: Optional[str] = None
    expected_requirement: str
    severity: str
    confidence: float
    status: str
    evidence_zone: Optional[str] = None
    legal_reference: Optional[str] = None

    class Config:
        from_attributes = True

class ViolationStatusUpdate(BaseModel):
    status: str # VERIFIED, DISMISSED, MANUAL_REVIEW

# --- Evidence Schemas ---
class EvidenceResponse(BaseModel):
    id: int
    evidence_type: str
    label: str
    bounding_box_json: Dict[str, Any]
    description: Optional[str] = None
    file_path: Optional[str] = None

    class Config:
        from_attributes = True

# --- Rule Schemas ---
class RuleBase(BaseModel):
    rule_code: str
    category: str
    description: str
    legal_reference: str
    requirement_text: str
    validation_type: str = "TEXT_PRESENCE"
    severity: str = "HIGH"
    is_active: bool = True

class RuleCreate(RuleBase):
    pass

class RuleUpdate(BaseModel):
    category: Optional[str] = None
    description: Optional[str] = None
    legal_reference: Optional[str] = None
    requirement_text: Optional[str] = None
    validation_type: Optional[str] = None
    severity: Optional[str] = None
    is_active: Optional[bool] = None

class RuleResponse(RuleBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    product_code: str
    name: str
    category: str
    manufacturer_name: Optional[str] = None
    manufacturer_address: Optional[str] = None
    standard_mrp: Optional[float] = None
    net_quantity: Optional[str] = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    inspection_count: Optional[int] = 0
    latest_status: Optional[str] = "COMPLIANT"

    class Config:
        from_attributes = True

# --- Inspection Schemas ---
class InspectionAnalysisRequest(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = "General Food / Grocery"
    demo_product_id: Optional[str] = None # e.g. "basmati_rice", "biscuits", etc.

class InspectionEditDeclarationsRequest(BaseModel):
    declarations: List[DeclarationUpdate]

class InspectionVerifyRequest(BaseModel):
    remarks: Optional[str] = None
    final_status: Optional[str] = None # COMPLIANT, NON-COMPLIANT, NEEDS_MANUAL_VERIFICATION

class InspectionResponse(BaseModel):
    id: int
    inspection_number: str
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    officer_id: int
    officer_name: Optional[str] = None
    image_path: str
    evidence_image_path: Optional[str] = None
    compliance_status: str
    compliance_score: float
    score_breakdown: Optional[Dict[str, Any]] = None
    inspection_date: datetime.datetime
    remarks: Optional[str] = None
    officer_verified: bool
    violations_count: Optional[int] = 0

    class Config:
        from_attributes = True

class InspectionDetailResponse(InspectionResponse):
    declarations: List[DeclarationResponse] = []
    violations: List[ViolationResponse] = []
    evidence_items: List[EvidenceResponse] = []
    product: Optional[ProductResponse] = None
    officer: Optional[UserResponse] = None

# --- E-Commerce Verification Schemas ---
class EcommerceVerificationRequest(BaseModel):
    platform_name: str = "Amazon India"
    listing_url: Optional[str] = None
    listing_title: str
    listing_mrp: float
    listing_selling_price: Optional[float] = None
    listing_net_quantity: str
    listing_manufacturer: Optional[str] = None
    listing_country_of_origin: Optional[str] = None
    package_inspection_id: Optional[int] = None
    # If direct package values supplied:
    package_mrp: Optional[float] = None
    package_net_quantity: Optional[str] = None
    package_manufacturer: Optional[str] = None

class DiscrepancyItem(BaseModel):
    field: str
    package_value: str
    listing_value: str
    issue_type: str # MRP_MISMATCH, QUANTITY_MISMATCH, ORIGIN_MISMATCH, MISSING_DECLARATION
    severity: str
    legal_rule: str
    description: str

class EcommerceVerificationResponse(BaseModel):
    status: str # PASS, MISMATCH_DETECTED, HIGH_RISK
    compliance_score: float
    discrepancies: List[DiscrepancyItem]
    recommendation: str

# --- Dashboard Stats Schemas ---
class DashboardStatsResponse(BaseModel):
    total_inspections: int
    compliant_products: int
    non_compliant_products: int
    manual_verification_required: int
    violations_detected: int
    compliance_rate: float
    compliance_distribution: List[Dict[str, Any]]
    violations_by_category: List[Dict[str, Any]]
    inspections_trend: List[Dict[str, Any]]
    most_common_violations: List[Dict[str, Any]]
    recent_inspections: List[InspectionResponse]
