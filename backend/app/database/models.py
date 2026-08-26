import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    officer_id = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    designation = Column(String(100), default="Legal Metrology Inspector")
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="LEGAL_METROLOGY_OFFICER")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    inspections = relationship("Inspection", back_populates="officer")
    audit_logs = relationship("AuditLog", back_populates="officer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    manufacturer_name = Column(String(150), nullable=True)
    manufacturer_address = Column(Text, nullable=True)
    standard_mrp = Column(Float, nullable=True)
    net_quantity = Column(String(50), nullable=True)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    inspections = relationship("Inspection", back_populates="product")


class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_code = Column(String(50), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    legal_reference = Column(String(150), nullable=False) # e.g. "Rule 6(1)(a), Legal Metrology (PC) Rules 2011"
    requirement_text = Column(Text, nullable=False)
    validation_type = Column(String(50), default="TEXT_PRESENCE") # TEXT_PRESENCE, PATTERN, NUMERICAL, READABILITY
    severity = Column(String(20), default="HIGH") # CRITICAL, HIGH, MEDIUM, LOW
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    violations = relationship("Violation", back_populates="rule")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    inspection_number = Column(String(50), unique=True, index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Visual Assets
    image_path = Column(String(255), nullable=False)
    evidence_image_path = Column(String(255), nullable=True)
    
    # Results
    compliance_status = Column(String(50), default="PENDING") # COMPLIANT, NON-COMPLIANT, NEEDS_MANUAL_VERIFICATION
    compliance_score = Column(Float, default=0.0) # 0 to 100
    score_breakdown = Column(JSON, nullable=True) # { mandatory: 90, readability: 75, mrp: 100, quantity: 100, consumer_care: 50 }
    
    # Verification & Meta
    inspection_date = Column(DateTime, default=datetime.datetime.utcnow)
    remarks = Column(Text, nullable=True)
    officer_verified = Column(Boolean, default=False)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inspections")
    officer = relationship("User", back_populates="inspections")
    declarations = relationship("ExtractedDeclaration", back_populates="inspection", cascade="all, delete-orphan")
    violations = relationship("Violation", back_populates="inspection", cascade="all, delete-orphan")
    evidence_items = relationship("InspectionEvidence", back_populates="inspection", cascade="all, delete-orphan")


class ExtractedDeclaration(Base):
    __tablename__ = "extracted_declarations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    field_name = Column(String(100), nullable=False) # product_name, manufacturer, address, net_quantity, mrp, packed_date, consumer_care_phone, consumer_care_email, country_of_origin, unit_sale_price
    detected_value = Column(Text, nullable=True)
    is_present = Column(Boolean, default=True)
    confidence = Column(Float, default=0.95)
    estimated_font_size_px = Column(Float, nullable=True)
    readability_status = Column(String(50), default="PASS") # PASS, WARNING, MANUAL_VERIFICATION
    raw_bounding_box = Column(JSON, nullable=True) # {x: 10, y: 20, width: 100, height: 30}
    is_officer_edited = Column(Boolean, default=False)

    inspection = relationship("Inspection", back_populates="declarations")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("rules.id"), nullable=True)
    
    category = Column(String(100), nullable=False)
    issue = Column(Text, nullable=False)
    detected_value = Column(Text, nullable=True)
    expected_requirement = Column(Text, nullable=False)
    severity = Column(String(20), default="HIGH") # CRITICAL, HIGH, MEDIUM, LOW
    confidence = Column(Float, default=0.95)
    status = Column(String(50), default="ACTIVE") # ACTIVE, VERIFIED, DISMISSED, MANUAL_REVIEW
    evidence_zone = Column(String(100), nullable=True) # Zone label or bounding box reference
    
    inspection = relationship("Inspection", back_populates="violations")
    rule = relationship("Rule", back_populates="violations")


class InspectionEvidence(Base):
    __tablename__ = "inspection_evidence"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    evidence_type = Column(String(50), default="BOUNDING_BOX")
    label = Column(String(100), nullable=False) # e.g. "MRP Zone", "Net Quantity", "Manufacturer Details"
    bounding_box_json = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    file_path = Column(String(255), nullable=True)

    inspection = relationship("Inspection", back_populates="evidence_items")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    officer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False) # LOGIN, SCAN_UPLOAD, OCR_EDIT, RULE_UPDATE, REPORT_GENERATE, VERIFICATION_SIGN
    target_entity = Column(String(50), nullable=True) # INSPECTION, RULE, PRODUCT
    entity_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    officer = relationship("User", back_populates="audit_logs")
