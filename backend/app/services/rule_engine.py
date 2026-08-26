import re
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.database.models import Rule, ExtractedDeclaration, Violation

# Standard SI units allowed by Legal Metrology (Packaged Commodities) Rules, 2011
VALID_MASS_UNITS = ["g", "kg", "mg"]
VALID_VOLUME_UNITS = ["ml", "l", "kl", "ltr", "liter", "litre"]
VALID_LENGTH_UNITS = ["m", "cm", "mm"]
VALID_NUMBER_UNITS = ["n", "u", "unit", "units", "piece", "pieces"]

# Non-standard forbidden representations (Rule 12 & Schedule III)
FORBIDDEN_UNIT_PATTERNS = [r"\bgms\b", r"\bgm\b", r"\bkilos\b", r"\bltrs\b", r"\bpkts\b"]

class RuleEngine:
    """
    Configurable Rule Engine for Legal Metrology (Packaged Commodities) Rules, 2011.
    Evaluates extracted declarations against active rules loaded from the database.
    """

    @classmethod
    def evaluate_compliance(
        cls, 
        declarations: List[Dict[str, Any]], 
        db_rules: List[Rule] = None
    ) -> Tuple[str, float, Dict[str, float], List[Dict[str, Any]]]:
        """
        Runs rule evaluations and returns:
            - Overall compliance status (COMPLIANT, NON-COMPLIANT, NEEDS_MANUAL_VERIFICATION)
            - Total compliance score (0-100)
            - Category score breakdown
            - List of detected violations
        """
        # Map declaration dicts for quick lookup
        dec_map = {d["field_name"]: d for d in declarations}
        
        violations = []
        scores = {
            "mandatory_declarations": 100.0,
            "readability_formatting": 100.0,
            "mrp_compliance": 100.0,
            "quantity_declaration": 100.0,
            "consumer_care": 100.0
        }

        # --- Rule 1: Product Generic Name (LM-PC-001) ---
        p_name_dec = dec_map.get("product_name")
        if not p_name_dec or not p_name_dec.get("is_present") or not p_name_dec.get("detected_value"):
            violations.append({
                "rule_code": "LM-PC-001",
                "category": "Product Identification",
                "issue": "Product identity / generic name not clearly declared on principal display panel.",
                "detected_value": "Missing / Null",
                "expected_requirement": "The generic name or common name of the commodity must be prominently declared (Rule 6(1)(a)).",
                "severity": "CRITICAL",
                "confidence": 0.98,
                "legal_reference": "Rule 6(1)(a), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Product Name Zone"
            })
            scores["mandatory_declarations"] -= 25.0

        # --- Rule 2: Manufacturer / Packer Name (LM-PC-002) ---
        mfg_dec = dec_map.get("manufacturer")
        if not mfg_dec or not mfg_dec.get("is_present") or not mfg_dec.get("detected_value") or "missing" in str(mfg_dec.get("detected_value")).lower():
            violations.append({
                "rule_code": "LM-PC-002",
                "category": "Manufacturer Details",
                "issue": "Name of Manufacturer, Packer or Importer missing from package.",
                "detected_value": mfg_dec.get("detected_value") if mfg_dec else "Missing",
                "expected_requirement": "Name and complete address of the manufacturer or packer must be stated (Rule 6(1)(b)).",
                "severity": "HIGH",
                "confidence": 0.96,
                "legal_reference": "Rule 6(1)(b), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Manufacturer Zone"
            })
            scores["mandatory_declarations"] -= 20.0

        # --- Rule 3: Manufacturer Complete Address (LM-PC-003) ---
        addr_dec = dec_map.get("address")
        addr_val = str(addr_dec.get("detected_value") or "").strip() if addr_dec else ""
        if not addr_dec or not addr_dec.get("is_present") or len(addr_val) < 15 or "missing" in addr_val.lower():
            violations.append({
                "rule_code": "LM-PC-003",
                "category": "Manufacturer Address",
                "issue": "Incomplete or missing factory/registered address.",
                "detected_value": addr_val or "Missing",
                "expected_requirement": "Complete address including street, city, state, and PIN code must be provided to enable traceability (Rule 6(1)(b)).",
                "severity": "HIGH",
                "confidence": 0.92,
                "legal_reference": "Rule 6(1)(b), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Address Zone"
            })
            scores["mandatory_declarations"] -= 15.0

        # --- Rule 4: Net Quantity & Standard Units (LM-PC-004) ---
        qty_dec = dec_map.get("net_quantity")
        qty_val = str(qty_dec.get("detected_value") or "").strip() if qty_dec else ""
        if not qty_dec or not qty_dec.get("is_present") or not qty_val:
            violations.append({
                "rule_code": "LM-PC-004",
                "category": "Net Quantity",
                "issue": "Net quantity declaration missing.",
                "detected_value": "Missing",
                "expected_requirement": "Net quantity in terms of standard unit of weight or measure must be declared (Rule 6(1)(c)).",
                "severity": "CRITICAL",
                "confidence": 0.99,
                "legal_reference": "Rule 6(1)(c) & Rule 12, Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Net Quantity Zone"
            })
            scores["quantity_declaration"] -= 50.0
        else:
            # Check for non-standard unit abbreviations (e.g. 'GMS', 'KILOS')
            for forbidden_pattern in FORBIDDEN_UNIT_PATTERNS:
                if re.search(forbidden_pattern, qty_val, re.IGNORECASE):
                    violations.append({
                        "rule_code": "LM-PC-004",
                        "category": "Unit of Measurement",
                        "issue": f"Non-standard unit abbreviation detected: '{qty_val}'. Legal Metrology mandates standard SI symbols (e.g., 'g', 'kg', 'ml', 'l').",
                        "detected_value": qty_val,
                        "expected_requirement": "Symbols must conform strictly to SI standard units (e.g., 'g' not 'gms', 'kg' not 'kilos') as per Rule 12.",
                        "severity": "MEDIUM",
                        "confidence": 0.95,
                        "legal_reference": "Rule 12 & Schedule III, Legal Metrology (PC) Rules, 2011",
                        "evidence_zone": "Net Quantity Zone"
                    })
                    scores["quantity_declaration"] -= 30.0
                    break

        # --- Rule 5: MRP & Tax Inclusion (LM-PC-005) ---
        mrp_dec = dec_map.get("mrp")
        mrp_val = str(mrp_dec.get("detected_value") or "").strip() if mrp_dec else ""
        if not mrp_dec or not mrp_dec.get("is_present") or not mrp_val:
            violations.append({
                "rule_code": "LM-PC-005",
                "category": "Maximum Retail Price (MRP)",
                "issue": "MRP declaration missing on package.",
                "detected_value": "Missing",
                "expected_requirement": "Maximum Retail Price (MRP) in Indian Rupees inclusive of all taxes must be declared (Rule 6(1)(e)).",
                "severity": "CRITICAL",
                "confidence": 0.98,
                "legal_reference": "Rule 6(1)(e), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "MRP Zone"
            })
            scores["mrp_compliance"] -= 50.0
        else:
            # Check if "inclusive of all taxes" or "incl." is present
            if not re.search(r"(?:incl|taxes|tax)", mrp_val, re.IGNORECASE):
                violations.append({
                    "rule_code": "LM-PC-005",
                    "category": "Maximum Retail Price (MRP)",
                    "issue": "MRP declared without mandatory 'inclusive of all taxes' or 'incl. of all taxes' statutory phrase.",
                    "detected_value": mrp_val,
                    "expected_requirement": "Retail price must be written in format 'MRP Rs. / ₹ ... (inclusive of all taxes)' (Rule 6(1)(e)).",
                    "severity": "HIGH",
                    "confidence": 0.94,
                    "legal_reference": "Rule 6(1)(e), Legal Metrology (PC) Rules, 2011",
                    "evidence_zone": "MRP Zone"
                })
                scores["mrp_compliance"] -= 35.0

        # --- Rule 6: Date / Month / Year of Packing (LM-PC-006) ---
        date_dec = dec_map.get("packed_date")
        date_val = str(date_dec.get("detected_value") or "").strip() if date_dec else ""
        if not date_dec or not date_dec.get("is_present") or not date_val:
            violations.append({
                "rule_code": "LM-PC-006",
                "category": "Date of Packing / Mfg",
                "issue": "Month and Year of manufacture or packing missing.",
                "detected_value": "Missing",
                "expected_requirement": "Month and year of manufacture, packing, or import must be declared on every package (Rule 6(1)(d)).",
                "severity": "HIGH",
                "confidence": 0.95,
                "legal_reference": "Rule 6(1)(d), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Date Zone"
            })
            scores["mandatory_declarations"] -= 20.0
        elif "??" in date_val or date_dec.get("readability_status") == "MANUAL_VERIFICATION":
            violations.append({
                "rule_code": "LM-PC-006",
                "category": "Date Readability / Verification",
                "issue": f"Packing date is ambiguous or partially obscured: '{date_val}'.",
                "detected_value": date_val,
                "expected_requirement": "Clear and legible declaration of Month/Year (e.g. MM/YYYY or Month YYYY) is mandatory.",
                "severity": "MEDIUM",
                "confidence": 0.70,
                "legal_reference": "Rule 6(1)(d), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Date Zone"
            })
            scores["readability_formatting"] -= 25.0

        # --- Rule 7: Consumer Care Details (LM-PC-007) ---
        cc_dec = dec_map.get("consumer_care")
        cc_val = str(cc_dec.get("detected_value") or "").strip() if cc_dec else ""
        if not cc_dec or not cc_dec.get("is_present") or "no consumer care" in cc_val.lower() or "missing" in cc_val.lower():
            violations.append({
                "rule_code": "LM-PC-007",
                "category": "Consumer Care Details",
                "issue": "No Consumer Care contact details found (Helpline Number and Email are mandatory).",
                "detected_value": "Missing",
                "expected_requirement": "Name, address, telephone number and e-mail address of the person or office to contact in case of consumer complaints (Rule 6(1)(n)).",
                "severity": "HIGH",
                "confidence": 0.97,
                "legal_reference": "Rule 6(1)(n), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Consumer Care Zone"
            })
            scores["consumer_care"] -= 60.0

        # --- Rule 8: Country of Origin (LM-PC-008) ---
        coo_dec = dec_map.get("country_of_origin")
        if not coo_dec or not coo_dec.get("is_present") or not coo_dec.get("detected_value"):
            violations.append({
                "rule_code": "LM-PC-008",
                "category": "Country of Origin",
                "issue": "Country of origin / manufacturing country not stated.",
                "detected_value": "Missing",
                "expected_requirement": "The name of the country of origin or manufacture or assembly must be mentioned (Rule 6(10)).",
                "severity": "HIGH",
                "confidence": 0.94,
                "legal_reference": "Rule 6(10), Legal Metrology (PC) Rules, 2011",
                "evidence_zone": "Origin Zone"
            })
            scores["mandatory_declarations"] -= 15.0

        # --- Rule 9: Unit Sale Price (USP) (LM-PC-009) ---
        usp_dec = dec_map.get("unit_sale_price")
        if not usp_dec or not usp_dec.get("is_present") or not usp_dec.get("detected_value"):
            # USP is a recent mandatory requirement for packages with net quantity > 1g/1ml
            violations.append({
                "rule_code": "LM-PC-009",
                "category": "Unit Sale Price (USP)",
                "issue": "Unit Sale Price (e.g. ₹ per g / kg / ml / L / unit) missing on package.",
                "detected_value": "Missing",
                "expected_requirement": "Declaration of Unit Sale Price is mandatory to enable transparent consumer price comparison (Rule 6(11) Amendment).",
                "severity": "MEDIUM",
                "confidence": 0.91,
                "legal_reference": "Rule 6(11), Legal Metrology (PC) Amendment Rules, 2021",
                "evidence_zone": "Unit Sale Price Zone"
            })
            scores["mrp_compliance"] -= 15.0

        # Ensure all score components are within [0, 100]
        for k in scores:
            scores[k] = max(0.0, min(100.0, round(scores[k], 1)))

        # Weighted Overall Score:
        # Mandatory: 30%, Quantity: 20%, MRP: 20%, Consumer Care: 20%, Readability: 10%
        overall_score = round(
            scores["mandatory_declarations"] * 0.30 +
            scores["quantity_declaration"] * 0.20 +
            scores["mrp_compliance"] * 0.20 +
            scores["consumer_care"] * 0.20 +
            scores["readability_formatting"] * 0.10,
            1
        )

        # Determine Final Compliance Status
        critical_violations = [v for v in violations if v["severity"] == "CRITICAL"]
        high_violations = [v for v in violations if v["severity"] == "HIGH"]
        medium_violations = [v for v in violations if v["severity"] == "MEDIUM"]

        if len(critical_violations) > 0 or len(high_violations) > 0 or overall_score < 80.0:
            status = "NON-COMPLIANT"
        elif len(medium_violations) > 0 or any("??" in str(d.get("detected_value", "")) for d in declarations):
            status = "NEEDS_MANUAL_VERIFICATION"
        else:
            status = "COMPLIANT"

        return status, overall_score, scores, violations
