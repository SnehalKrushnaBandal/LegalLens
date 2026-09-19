import datetime
from sqlalchemy.orm import Session
from app.config import DEMO_ASSETS_DIR
from app.database.models import User, Product, Rule, Inspection, ExtractedDeclaration, Violation, InspectionEvidence, AuditLog
from app.services.auth_service import get_password_hash
from app.services.ocr_service import OCRService, DEMO_PRODUCTS
from app.services.rule_engine import RuleEngine

INITIAL_RULES = [
    {
        "rule_code": "LM-PC-001",
        "category": "Product Identification",
        "description": "Mandatory declaration of the generic or common name of the commodity on the principal display panel.",
        "legal_reference": "Rule 6(1)(a), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "The name or generic identity of the packaged commodity must be clearly and prominently declared.",
        "validation_type": "TEXT_PRESENCE",
        "severity": "CRITICAL",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-002",
        "category": "Manufacturer Details",
        "description": "Name of Manufacturer, Packer or Importer.",
        "legal_reference": "Rule 6(1)(b), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "The name and complete identity of the manufacturer, packer or importer must be declared.",
        "validation_type": "TEXT_PRESENCE",
        "severity": "HIGH",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-003",
        "category": "Manufacturer Address",
        "description": "Complete factory/registered address of manufacturer or packer.",
        "legal_reference": "Rule 6(1)(b), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Complete address with street, city, state and PIN code to guarantee manufacturer traceability.",
        "validation_type": "TEXT_PRESENCE",
        "severity": "HIGH",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-004",
        "category": "Net Quantity & Units",
        "description": "Net quantity in standard SI units (g, kg, ml, l, m, N).",
        "legal_reference": "Rule 6(1)(c) & Rule 12, Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Net quantity must be declared using standard SI symbols ('g', 'kg', 'ml', 'l', 'N') without non-standard symbols like 'gms' or 'kilos'.",
        "validation_type": "PATTERN",
        "severity": "CRITICAL",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-005",
        "category": "Maximum Retail Price (MRP)",
        "description": "MRP in Indian Rupees inclusive of all taxes.",
        "legal_reference": "Rule 6(1)(e), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Retail price must be written in format 'MRP Rs. / ₹ ... (inclusive of all taxes)'.",
        "validation_type": "PATTERN",
        "severity": "CRITICAL",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-006",
        "category": "Date of Packing / Mfg",
        "description": "Month and Year of manufacture, packing, or import.",
        "legal_reference": "Rule 6(1)(d), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Month and Year must be declared clearly (e.g. MM/YYYY or Month YYYY) on every package.",
        "validation_type": "PATTERN",
        "severity": "HIGH",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-007",
        "category": "Consumer Care Details",
        "description": "Consumer care cell name, address, telephone number, and email address.",
        "legal_reference": "Rule 6(1)(n), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Name, address, telephone helpline and email address for consumer grievance redressal.",
        "validation_type": "TEXT_PRESENCE",
        "severity": "HIGH",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-008",
        "category": "Country of Origin",
        "description": "Country of origin or assembly for all packaged commodities.",
        "legal_reference": "Rule 6(10), Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Declaration of Country of Origin is mandatory on all packages and e-commerce listings.",
        "validation_type": "TEXT_PRESENCE",
        "severity": "HIGH",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-009",
        "category": "Unit Sale Price (USP)",
        "description": "Unit Sale Price per g/kg/ml/l/piece for packaged retail commodities.",
        "legal_reference": "Rule 6(11), Legal Metrology (PC) Amendment Rules, 2021",
        "requirement_text": "Unit Sale Price must be stated alongside MRP on packages weighing greater than 1g/1ml.",
        "validation_type": "NUMERICAL",
        "severity": "MEDIUM",
        "is_active": True
    },
    {
        "rule_code": "LM-PC-010",
        "category": "Font Readability & Size",
        "description": "Minimum numeral and letter font height based on package area.",
        "legal_reference": "Rule 7 & Schedule II, Legal Metrology (PC) Rules, 2011",
        "requirement_text": "Numeral height must meet prescribed minimum millimeter height based on principal display panel area.",
        "validation_type": "READABILITY",
        "severity": "MEDIUM",
        "is_active": True
    }
]

def seed_database(db: Session):
    # 1. Seed Officer User
    admin_user = db.query(User).filter(User.officer_id == "LMO001").first()
    if not admin_user:
        admin_user = User(
            officer_id="LMO001",
            full_name="Inspector Snehal Bandal",
            designation="Senior Legal Metrology Officer",
            email="lmo001@legalmetrology.gov.in",
            hashed_password=get_password_hash("admin123"),
            role="LEGAL_METROLOGY_OFFICER",
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Officer LMO001 created successfully.")

    # 2. Seed Rules
    for r_data in INITIAL_RULES:
        existing_rule = db.query(Rule).filter(Rule.rule_code == r_data["rule_code"]).first()
        if not existing_rule:
            rule = Rule(**r_data)
            db.add(rule)
    db.commit()
    print("Legal Metrology Rules seeded.")

    # 3. Seed Demo Products & Inspections if none exist
    demo_keys = ["basmati_rice", "biscuits", "cooking_oil", "detergent", "shampoo", "garam_masala"]
    
    for idx, key in enumerate(demo_keys, 1):
        demo = DEMO_PRODUCTS[key]
        
        # Check if product already exists
        prod = db.query(Product).filter(Product.name == demo["product_name"]).first()
        if not prod:
            prod = Product(
                product_code=f"PRD-2026-00{idx}",
                name=demo["product_name"],
                category=demo["category"],
                manufacturer_name=demo["manufacturer"] or "Unknown Manufacturer",
                manufacturer_address=demo["address"] or "Not Provided",
                standard_mrp=650.0 if idx == 1 else (35.0 if idx == 2 else (195.0 if idx == 3 else (140.0 if idx == 4 else (120.0 if idx == 5 else 75.0)))),
                net_quantity=demo["net_quantity"],
                image_url=f"/demo_assets/{key}.jpg"
            )
            db.add(prod)
            db.commit()
            db.refresh(prod)

        # Check if inspection already exists for this product
        existing_insp = db.query(Inspection).filter(Inspection.product_id == prod.id).first()
        if not existing_insp:
            # Generate synthetic image for this demo product
            synth_img = OCRService.generate_synthetic_package_image(key)
            target_file = DEMO_ASSETS_DIR / f"{key}.jpg"
            synth_img.save(str(target_file), quality=95)
            img_path = str(target_file)

            # Run OCR & Rule Engine
            declarations, evidence_items, evidence_img_path = OCRService.extract_declarations(
                image_path=img_path,
                demo_product_id=key
            )
            
            status, score, breakdown, violations = RuleEngine.evaluate_compliance(declarations)

            # Create Inspection
            insp = Inspection(
                inspection_number=f"INSP-2026-00{idx}",
                product_id=prod.id,
                officer_id=admin_user.id,
                image_path=img_path,
                evidence_image_path=evidence_img_path,
                compliance_status=status,
                compliance_score=score,
                score_breakdown=breakdown,
                inspection_date=datetime.datetime.utcnow() - datetime.timedelta(days=(6 - idx) * 2, hours=idx * 3),
                remarks=f"Initial compliance screening for {demo['product_name']}.",
                officer_verified=True if status == "COMPLIANT" else False,
                verified_at=datetime.datetime.utcnow() if status == "COMPLIANT" else None
            )
            db.add(insp)
            db.commit()
            db.refresh(insp)

            # Add Declarations
            for dec in declarations:
                ext_dec = ExtractedDeclaration(
                    inspection_id=insp.id,
                    field_name=dec["field_name"],
                    detected_value=dec["detected_value"],
                    is_present=dec["is_present"],
                    confidence=dec["confidence"],
                    estimated_font_size_px=dec["estimated_font_size_px"],
                    readability_status=dec["readability_status"],
                    raw_bounding_box=dec["raw_bounding_box"]
                )
                db.add(ext_dec)

            # Add Violations
            for v in violations:
                rule_obj = db.query(Rule).filter(Rule.rule_code == v.get("rule_code")).first()
                viol = Violation(
                    inspection_id=insp.id,
                    rule_id=rule_obj.id if rule_obj else None,
                    category=v["category"],
                    issue=v["issue"],
                    detected_value=v["detected_value"],
                    expected_requirement=v["expected_requirement"],
                    severity=v["severity"],
                    confidence=v["confidence"],
                    status="ACTIVE",
                    evidence_zone=v.get("evidence_zone")
                )
                db.add(viol)

            # Add Evidence Items
            for ev in evidence_items:
                ev_item = InspectionEvidence(
                    inspection_id=insp.id,
                    evidence_type=ev["evidence_type"],
                    label=ev["label"],
                    bounding_box_json=ev["bounding_box_json"],
                    description=ev["description"]
                )
                db.add(ev_item)

            # Audit Log
            audit = AuditLog(
                officer_id=admin_user.id,
                action="SCAN_UPLOAD",
                target_entity="INSPECTION",
                entity_id=insp.inspection_number,
                details=f"Compliance check run for {demo['product_name']} with result {status} ({score}/100)."
            )
            db.add(audit)
            db.commit()

        print("Seeded 6 comprehensive demo products & inspections.")
