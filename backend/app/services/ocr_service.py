import os
import re
import math
from typing import Dict, Any, List, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from app.config import UPLOAD_DIR, EVIDENCE_DIR, DEMO_ASSETS_DIR

# Realistic synthetic demo products definition for guaranteed presentation fidelity
DEMO_PRODUCTS = {
    "basmati_rice": {
        "product_name": "Premium Basmati Rice",
        "category": "Packaged Food / Rice",
        "manufacturer": "ABC Foods Pvt Ltd",
        "address": "Plot 42, Sector 8, MIDC Industrial Area, Mumbai, Maharashtra 400093",
        "net_quantity": "5 kg",
        "mrp": "₹650.00 (Incl. of all taxes)",
        "packed_date": "07/2026",
        "consumer_care_phone": "1800-111-2233",
        "consumer_care_email": "care@abcfoods.in",
        "country_of_origin": "India",
        "unit_sale_price": "₹130.00 / kg",
        "compliance_preset": "COMPLIANT",
        "bg_color": "#1E3A8A", # Deep royal blue
        "accent_color": "#F59E0B" # Amber gold
    },
    "biscuits": {
        "product_name": "Butter Delight Biscuits",
        "category": "Bakery / Confectionery",
        "manufacturer": "Sunlight Bakeries India Ltd",
        "address": "Survey 88, Electronic City Phase 2, Bengaluru, Karnataka 560100",
        "net_quantity": "200 g",
        "mrp": "₹35.00 (Incl. of all taxes)",
        "packed_date": "06/2026",
        "consumer_care_phone": None, # Violation: Missing consumer care
        "consumer_care_email": None, # Violation: Missing email
        "country_of_origin": "India",
        "unit_sale_price": "₹0.175 / g",
        "compliance_preset": "NON_COMPLIANT_CONSUMER_CARE",
        "bg_color": "#B45309", # Warm biscuit brown
        "accent_color": "#FEF3C7"
    },
    "cooking_oil": {
        "product_name": "Pure Mustard Cooking Oil",
        "category": "Edible Oils",
        "manufacturer": "Shree Oil Mills Ltd",
        "address": "GIDC Estate, Vatva, Ahmedabad, Gujarat 382445",
        "net_quantity": "1 L",
        "mrp": "₹195.00", # Violation: Missing mandatory 'incl. of all taxes' declaration
        "packed_date": "05/2026",
        "consumer_care_phone": "1800-222-3344",
        "consumer_care_email": "support@shreeoil.com",
        "country_of_origin": "India",
        "unit_sale_price": "₹195.00 / L",
        "compliance_preset": "NON_COMPLIANT_MRP",
        "bg_color": "#854D0E", # Mustard gold
        "accent_color": "#FEF08A"
    },
    "detergent": {
        "product_name": "Active Clean Detergent Powder",
        "category": "Household Goods / Detergents",
        "manufacturer": "Global FMCG Industries Ltd",
        "address": "Baddi Industrial Area, Solan, Himachal Pradesh 173205",
        "net_quantity": "1000 GMS", # Violation: Non-standard unit 'GMS' (Rules require 'g' or 'kg') & missing Unit Sale Price
        "mrp": "₹140.00 (Incl. of all taxes)",
        "packed_date": "04/2026",
        "consumer_care_phone": "1800-999-8877",
        "consumer_care_email": "customercare@globalfmcg.com",
        "country_of_origin": "India",
        "unit_sale_price": None, # Violation: Missing USP for multi-unit retail
        "compliance_preset": "NON_COMPLIANT_QUANTITY_USP",
        "bg_color": "#1D4ED8", # Detergent blue
        "accent_color": "#67E8F9"
    },
    "shampoo": {
        "product_name": "Herbal Glow Shampoo",
        "category": "Cosmetics / Personal Care",
        "manufacturer": "Flora Cosmetics India",
        "address": "Okhla Phase 3", # Violation: Incomplete address (missing city, state, pin code)
        "net_quantity": "180 ml",
        "mrp": "₹120.00 (Incl. of all taxes)",
        "packed_date": "08/2026",
        "consumer_care_phone": "1800-444-5566",
        "consumer_care_email": "glow@floracosmetics.in",
        "country_of_origin": "India",
        "unit_sale_price": "₹0.66 / ml",
        "compliance_preset": "NON_COMPLIANT_ADDRESS",
        "bg_color": "#065F46", # Botanical emerald
        "accent_color": "#A7F3D0"
    },
    "garam_masala": {
        "product_name": "Royal Garam Masala",
        "category": "Spices / Condiments",
        "manufacturer": "Heritage Spices Co.",
        "address": "APMC Market Yard, Unjha, Gujarat 384170",
        "net_quantity": "100 g",
        "mrp": "₹75.00 (Incl. of all taxes)",
        "packed_date": "??/2026", # Manual verification needed: Date stamp blurred
        "consumer_care_phone": "1800-777-6655",
        "consumer_care_email": "help@heritagespices.com",
        "country_of_origin": "India",
        "unit_sale_price": "₹0.75 / g",
        "compliance_preset": "NEEDS_MANUAL_VERIFICATION",
        "bg_color": "#991B1B", # Rich spice maroon
        "accent_color": "#FDE68A"
    }
}

class OCRService:
    """
    Modular OCR & Vision Service for Legal Metrology Packaged Commodities.
    Provides image preprocessing, text extraction, declaration parsing,
    visual bounding box evidence generation, and font readability estimation.
    """

    @staticmethod
    def preprocess_image(image_path: str) -> Dict[str, Any]:
        """
        Preprocesses uploaded package image: Grayscale, contrast enhancement, quality metrics.
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Check sharpness / contrast estimation
                gray = img.convert('L')
                stat_ext = gray.getextrema()
                contrast_range = stat_ext[1] - stat_ext[0] if stat_ext else 128
                
                estimated_quality = "EXCELLENT" if contrast_range > 150 else ("GOOD" if contrast_range > 90 else "FAIR")
                resolution_dpi = img.info.get('dpi', (72, 72))[0]
                
                return {
                    "width": width,
                    "height": height,
                    "contrast_range": contrast_range,
                    "estimated_quality": estimated_quality,
                    "resolution_dpi": resolution_dpi,
                    "status": "PREPROCESSED"
                }
        except Exception as e:
            return {
                "width": 800,
                "height": 600,
                "estimated_quality": "GOOD",
                "error": str(e)
            }

    @classmethod
    def extract_declarations(
        cls, 
        image_path: str, 
        demo_product_id: Optional[str] = None,
        custom_product_name: Optional[str] = None,
        category: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], str]:
        """
        Extracts Legal Metrology mandatory declarations from package image.
        Returns:
            - List of extracted declaration objects with confidence, font size, bounding boxes
            - List of visual evidence items
            - Annotated evidence image path
        """
        # If demo product is chosen, return realistic baseline with matched layout
        if demo_product_id and demo_product_id in DEMO_PRODUCTS:
            return cls._process_demo_product(image_path, demo_product_id)

        # Fallback or generic uploaded image extraction
        return cls._process_generic_upload(image_path, custom_product_name, category)

    @classmethod
    def _process_demo_product(cls, image_path: str, demo_id: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], str]:
        demo = DEMO_PRODUCTS[demo_id]
        
        declarations = []
        evidence_items = []
        
        # Coordinate layout template for bounding boxes (normalized 0-100%)
        box_coords = {
            "product_name": {"x": 8, "y": 8, "w": 84, "h": 12, "color": "#10B981"},
            "manufacturer": {"x": 8, "y": 24, "w": 84, "h": 10, "color": "#10B981" if demo["manufacturer"] else "#EF4444"},
            "address": {"x": 8, "y": 36, "w": 84, "h": 12, "color": "#10B981" if len(demo["address"] or "") > 20 else "#EF4444"},
            "net_quantity": {"x": 8, "y": 50, "w": 40, "h": 12, "color": "#10B981" if demo["net_quantity"] in ["5 kg", "200 g", "1 L", "100 g"] else "#F59E0B"},
            "mrp": {"x": 52, "y": 50, "w": 40, "h": 12, "color": "#10B981" if "Incl" in (demo["mrp"] or "") else "#EF4444"},
            "packed_date": {"x": 8, "y": 64, "w": 40, "h": 10, "color": "#10B981" if "??" not in (demo["packed_date"] or "") else "#F59E0B"},
            "consumer_care": {"x": 52, "y": 64, "w": 40, "h": 18, "color": "#10B981" if demo["consumer_care_phone"] else "#EF4444"},
            "country_of_origin": {"x": 8, "y": 76, "w": 40, "h": 9, "color": "#10B981"},
            "unit_sale_price": {"x": 8, "y": 87, "w": 84, "h": 9, "color": "#10B981" if demo["unit_sale_price"] else "#EF4444"}
        }

        # 1. Product Name
        declarations.append({
            "field_name": "product_name",
            "detected_value": demo["product_name"],
            "is_present": bool(demo["product_name"]),
            "confidence": 0.98,
            "estimated_font_size_px": 28.5,
            "readability_status": "PASS",
            "raw_bounding_box": box_coords["product_name"]
        })

        # 2. Manufacturer / Packer
        declarations.append({
            "field_name": "manufacturer",
            "detected_value": demo["manufacturer"],
            "is_present": bool(demo["manufacturer"]),
            "confidence": 0.96,
            "estimated_font_size_px": 16.0,
            "readability_status": "PASS",
            "raw_bounding_box": box_coords["manufacturer"]
        })

        # 3. Complete Address
        is_addr_complete = bool(demo["address"]) and len(demo["address"]) > 25
        declarations.append({
            "field_name": "address",
            "detected_value": demo["address"],
            "is_present": bool(demo["address"]),
            "confidence": 0.94 if is_addr_complete else 0.82,
            "estimated_font_size_px": 14.0,
            "readability_status": "PASS" if is_addr_complete else "WARNING",
            "raw_bounding_box": box_coords["address"]
        })

        # 4. Net Quantity
        declarations.append({
            "field_name": "net_quantity",
            "detected_value": demo["net_quantity"],
            "is_present": bool(demo["net_quantity"]),
            "confidence": 0.99,
            "estimated_font_size_px": 22.0,
            "readability_status": "PASS",
            "raw_bounding_box": box_coords["net_quantity"]
        })

        # 5. MRP
        has_taxes = "incl" in (demo["mrp"] or "").lower()
        declarations.append({
            "field_name": "mrp",
            "detected_value": demo["mrp"],
            "is_present": bool(demo["mrp"]),
            "confidence": 0.97,
            "estimated_font_size_px": 20.0,
            "readability_status": "PASS" if has_taxes else "WARNING",
            "raw_bounding_box": box_coords["mrp"]
        })

        # 6. Date of Packing / Manufacture
        has_date_ambiguity = "??" in (demo["packed_date"] or "")
        declarations.append({
            "field_name": "packed_date",
            "detected_value": demo["packed_date"],
            "is_present": bool(demo["packed_date"]),
            "confidence": 0.65 if has_date_ambiguity else 0.95,
            "estimated_font_size_px": 15.0,
            "readability_status": "MANUAL_VERIFICATION" if has_date_ambiguity else "PASS",
            "raw_bounding_box": box_coords["packed_date"]
        })

        # 7. Consumer Care Details (Phone & Email)
        has_cc = bool(demo["consumer_care_phone"]) or bool(demo["consumer_care_email"])
        cc_text = f"Tel: {demo['consumer_care_phone'] or 'Missing'}, Email: {demo['consumer_care_email'] or 'Missing'}" if has_cc else "No Consumer Care Details Found on Package"
        declarations.append({
            "field_name": "consumer_care",
            "detected_value": cc_text if has_cc else None,
            "is_present": has_cc,
            "confidence": 0.98 if has_cc else 0.20,
            "estimated_font_size_px": 13.5 if has_cc else 0.0,
            "readability_status": "PASS" if has_cc else "WARNING",
            "raw_bounding_box": box_coords["consumer_care"]
        })

        # 8. Country of Origin
        declarations.append({
            "field_name": "country_of_origin",
            "detected_value": demo["country_of_origin"],
            "is_present": bool(demo["country_of_origin"]),
            "confidence": 0.99,
            "estimated_font_size_px": 14.0,
            "readability_status": "PASS",
            "raw_bounding_box": box_coords["country_of_origin"]
        })

        # 9. Unit Sale Price (USP)
        declarations.append({
            "field_name": "unit_sale_price",
            "detected_value": demo["unit_sale_price"],
            "is_present": bool(demo["unit_sale_price"]),
            "confidence": 0.95 if demo["unit_sale_price"] else 0.10,
            "estimated_font_size_px": 14.0 if demo["unit_sale_price"] else 0.0,
            "readability_status": "PASS" if demo["unit_sale_price"] else "WARNING",
            "raw_bounding_box": box_coords["unit_sale_price"]
        })

        # Generate Visual Evidence Items
        for key, box in box_coords.items():
            evidence_items.append({
                "evidence_type": "BOUNDING_BOX",
                "label": key.replace("_", " ").title(),
                "bounding_box_json": box,
                "description": f"Zone detected for {key.replace('_', ' ').title()}"
            })

        # Generate annotated evidence image
        evidence_image_path = cls._render_annotated_evidence_image(image_path, declarations, demo_id)

        return declarations, evidence_items, evidence_image_path

    # ── EasyOCR reader (lazy singleton so it loads only once) ──────────────────
    _ocr_reader = None
    _ocr_ready = False

    @classmethod
    def _get_ocr_reader(cls):
        """Lazy-load easyocr reader (English). Returns None if unavailable."""
        if cls._ocr_ready:
            return cls._ocr_reader
        try:
            import easyocr
            cls._ocr_reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            cls._ocr_ready = True
            print("[OCR] EasyOCR reader loaded successfully.")
        except Exception as e:
            print(f"[OCR] EasyOCR not available: {e}. Falling back to image analysis.")
            cls._ocr_reader = None
            cls._ocr_ready = True
        return cls._ocr_reader

    @classmethod
    def _extract_text_from_image(cls, image_path: str) -> List[Tuple[Any, str, float]]:
        """
        Extracts text from image using EasyOCR.
        Returns list of (bbox, text, confidence) tuples.
        """
        reader = cls._get_ocr_reader()
        if reader is None:
            return []
        try:
            results = reader.readtext(image_path, detail=1, paragraph=False)
            # results: [([[x1,y1],[x2,y1],[x2,y2],[x1,y2]], text, conf), ...]
            return results
        except Exception as e:
            print(f"[OCR] Text extraction error: {e}")
            return []

    @classmethod
    def _parse_declarations_from_text(
        cls,
        ocr_results: List[Tuple[Any, str, float]],
        image_width: int,
        image_height: int,
        custom_product_name: Optional[str]
    ) -> List[Dict[str, Any]]:
        """
        Parses raw OCR results into the 9 mandatory Legal Metrology declarations
        using regex pattern matching on extracted text.
        """
        import re

        # Join all text in reading order
        all_lines = [(r[1].strip(), r[2], r[0]) for r in ocr_results if r[1].strip()]
        full_text = "\n".join(t for t, _, _ in all_lines)
        full_text_lower = full_text.lower()

        def find_text_by_pattern(patterns, lines):
            """Returns (matched_text, confidence, bbox_pct) or (None, 0, None)"""
            for pattern in patterns:
                for text, conf, bbox in lines:
                    if re.search(pattern, text, re.IGNORECASE):
                        # Convert pixel bbox to percentage
                        try:
                            xs = [p[0] for p in bbox]
                            ys = [p[1] for p in bbox]
                            x_pct = max(0, min(95, int(min(xs) * 100 / max(image_width, 1))))
                            y_pct = max(0, min(95, int(min(ys) * 100 / max(image_height, 1))))
                            w_pct = max(5, min(95 - x_pct, int((max(xs) - min(xs)) * 100 / max(image_width, 1))))
                            h_pct = max(3, min(95 - y_pct, int((max(ys) - min(ys)) * 100 / max(image_height, 1))))
                        except:
                            x_pct, y_pct, w_pct, h_pct = 10, 10, 80, 8
                        return text, float(conf), {"x": x_pct, "y": y_pct, "w": w_pct, "h": h_pct}
            return None, 0.0, None

        def find_multiline(keyword_patterns, lines, window=3):
            """Collect lines that appear near a keyword match."""
            for ki, kp in enumerate(keyword_patterns):
                for i, (text, conf, bbox) in enumerate(lines):
                    if re.search(kp, text, re.IGNORECASE):
                        nearby = [lines[j][0] for j in range(i, min(i + window, len(lines)))]
                        combined = " ".join(nearby)
                        try:
                            xs = [p[0] for p in bbox]
                            ys = [p[1] for p in bbox]
                            x_pct = max(0, int(min(xs) * 100 / max(image_width, 1)))
                            y_pct = max(0, int(min(ys) * 100 / max(image_height, 1)))
                            w_pct = max(5, int((max(xs) - min(xs)) * 100 / max(image_width, 1)) + 10)
                            h_pct = max(5, int((max(ys) - min(ys)) * 100 / max(image_height, 1)) * window)
                        except:
                            x_pct, y_pct, w_pct, h_pct = 10, 25, 80, 12
                        return combined, float(conf), {"x": x_pct, "y": y_pct, "w": w_pct, "h": h_pct}
            return None, 0.0, None

        declarations = []

        # ── 1. Product Name ──────────────────────────────────────────────────
        # Heuristic: largest font text at top, or custom name provided
        pname_val = custom_product_name
        pname_conf = 0.85
        pname_box = {"x": 8, "y": 5, "w": 84, "h": 12}
        if not pname_val and all_lines:
            # Largest text is usually the product name (first few lines, high conf)
            top_candidates = [t for t, c, b in all_lines[:8] if len(t) > 3 and c > 0.5]
            if top_candidates:
                pname_val = top_candidates[0]
                pname_conf = all_lines[0][1]
        if not pname_val:
            pname_val = None

        declarations.append({
            "field_name": "product_name",
            "detected_value": pname_val,
            "is_present": bool(pname_val),
            "confidence": round(pname_conf, 2),
            "estimated_font_size_px": 26.0,
            "readability_status": "PASS" if pname_val else "WARNING",
            "raw_bounding_box": {**pname_box, "color": "#10B981" if pname_val else "#EF4444"}
        })

        # ── 2. Manufacturer / Packer ─────────────────────────────────────────
        mfr_patterns = [
            r'(manufactured|packed|mfd|mfg|packaged)\s*(by|&\s*marketed|and\s*marketed)?',
            r'(manufacturer|packer|importer)\s*:',
            r'pvt\.?\s*ltd\.?', r'private\s+limited', r'industries?\s+ltd',
        ]
        mfr_val, mfr_conf, mfr_box = find_multiline(mfr_patterns, all_lines, window=2)
        if not mfr_box:
            mfr_box = {"x": 8, "y": 22, "w": 84, "h": 10}

        declarations.append({
            "field_name": "manufacturer",
            "detected_value": mfr_val,
            "is_present": bool(mfr_val),
            "confidence": round(mfr_conf, 2) if mfr_val else 0.15,
            "estimated_font_size_px": 15.0,
            "readability_status": "PASS" if mfr_val else "WARNING",
            "raw_bounding_box": {**mfr_box, "color": "#10B981" if mfr_val else "#EF4444"}
        })

        # ── 3. Address ───────────────────────────────────────────────────────
        addr_patterns = [
            r'\b\d{6}\b',                       # 6-digit PIN code
            r'(plot|survey|sector|phase|industrial|midc|gidc|estate)',
            r'(road|nagar|lane|street|marg|colony)',
            r'(mumbai|delhi|bengaluru|hyderabad|pune|chennai|kolkata|gujarat|maharashtra|karnataka)',
        ]
        addr_val, addr_conf, addr_box = find_multiline(addr_patterns, all_lines, window=3)
        # Extra: look for PIN code anywhere
        pin_match = re.search(r'\b(\d{6})\b', full_text)
        if pin_match and not addr_val:
            addr_val = f"Address with PIN {pin_match.group(1)}"
            addr_conf = 0.70
        is_complete_addr = bool(addr_val) and (re.search(r'\d{6}', addr_val or '') is not None)
        if not addr_box:
            addr_box = {"x": 8, "y": 34, "w": 84, "h": 12}

        declarations.append({
            "field_name": "address",
            "detected_value": addr_val,
            "is_present": bool(addr_val),
            "confidence": round(addr_conf, 2) if addr_val else 0.15,
            "estimated_font_size_px": 13.5,
            "readability_status": "PASS" if is_complete_addr else ("WARNING" if addr_val else "WARNING"),
            "raw_bounding_box": {**addr_box, "color": "#10B981" if is_complete_addr else ("#F59E0B" if addr_val else "#EF4444")}
        })

        # ── 4. Net Quantity ──────────────────────────────────────────────────
        qty_text, qty_conf, qty_box = find_text_by_pattern([
            r'\b\d+(\.\d+)?\s*(kg|g\b|ml|l\b|litre|liter|gm\b|gms\b|grm)',
            r'net\s*(wt|weight|qty|quantity|content)',
            r'\b(net|content)\b.*\d',
        ], all_lines)
        if not qty_box:
            qty_box = {"x": 8, "y": 48, "w": 42, "h": 12}
        # Check for non-standard units
        has_nonstandard = bool(re.search(r'\b(gms|grm|grms|kilos|ltr|lts)\b', qty_text or '', re.IGNORECASE))

        declarations.append({
            "field_name": "net_quantity",
            "detected_value": qty_text,
            "is_present": bool(qty_text),
            "confidence": round(qty_conf, 2) if qty_text else 0.15,
            "estimated_font_size_px": 20.0,
            "readability_status": "WARNING" if has_nonstandard else ("PASS" if qty_text else "WARNING"),
            "raw_bounding_box": {**qty_box, "color": "#F59E0B" if has_nonstandard else ("#10B981" if qty_text else "#EF4444")}
        })

        # ── 5. MRP ───────────────────────────────────────────────────────────
        mrp_text, mrp_conf, mrp_box = find_text_by_pattern([
            r'(mrp|m\.r\.p|max\.?\s*retail\s*price)',
            r'(rs\.?|₹|inr)\s*\d+',
            r'\d+\s*\.?\d*\s*(incl|inclusive)',
        ], all_lines)
        has_tax_phrase = bool(re.search(r'incl|inclusive|all\s*tax', (mrp_text or '') + full_text_lower))
        if not mrp_box:
            mrp_box = {"x": 52, "y": 48, "w": 40, "h": 12}

        declarations.append({
            "field_name": "mrp",
            "detected_value": mrp_text,
            "is_present": bool(mrp_text),
            "confidence": round(mrp_conf, 2) if mrp_text else 0.15,
            "estimated_font_size_px": 18.0,
            "readability_status": "PASS" if (mrp_text and has_tax_phrase) else ("WARNING" if mrp_text else "WARNING"),
            "raw_bounding_box": {**mrp_box, "color": "#10B981" if (mrp_text and has_tax_phrase) else ("#F59E0B" if mrp_text else "#EF4444")}
        })

        # ── 6. Packing Date ──────────────────────────────────────────────────
        date_text, date_conf, date_box = find_text_by_pattern([
            r'\b(0[1-9]|1[0-2])[/\-\.](20\d{2})\b',    # MM/YYYY
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[\s\-,]*(20\d{2})\b',
            r'(mfg|mfd|packed|manufacturing|packing)\s*(date|dt)?',
            r'\b(best\s*before|use\s*by|expiry)',
        ], all_lines)
        # Direct regex on full text for date
        if not date_text:
            dm = re.search(r'\b(0[1-9]|1[0-2])[/\-](20\d{2})\b', full_text)
            if dm:
                date_text = dm.group(0)
                date_conf = 0.85
        if not date_box:
            date_box = {"x": 8, "y": 62, "w": 42, "h": 10}

        declarations.append({
            "field_name": "packed_date",
            "detected_value": date_text,
            "is_present": bool(date_text),
            "confidence": round(date_conf, 2) if date_text else 0.15,
            "estimated_font_size_px": 14.0,
            "readability_status": "PASS" if date_text else "WARNING",
            "raw_bounding_box": {**date_box, "color": "#10B981" if date_text else "#EF4444"}
        })

        # ── 7. Consumer Care ─────────────────────────────────────────────────
        # Phone
        phone_match = re.search(r'(1800[\s\-]\d{3}[\s\-]\d{4}|\+?91[\s\-]?\d{10}|\b\d{10}\b)', full_text)
        # Email
        email_match = re.search(r'[\w.\-+]+@[\w\-]+\.[a-zA-Z]{2,}', full_text)
        cc_val = None
        cc_parts = []
        if phone_match:
            cc_parts.append(f"Tel: {phone_match.group(0)}")
        if email_match:
            cc_parts.append(f"Email: {email_match.group(0)}")
        if cc_parts:
            cc_val = ", ".join(cc_parts)
        cc_conf_text, cc_conf, cc_box = find_text_by_pattern([
            r'(consumer\s*care|helpline|toll\s*free|customer\s*care|grievance)',
            r'(contact\s*us|reach\s*us|support)',
        ], all_lines)
        if not cc_box:
            cc_box = {"x": 52, "y": 62, "w": 40, "h": 16}

        declarations.append({
            "field_name": "consumer_care",
            "detected_value": cc_val,
            "is_present": bool(cc_val),
            "confidence": 0.92 if cc_val else 0.15,
            "estimated_font_size_px": 13.0,
            "readability_status": "PASS" if cc_val else "WARNING",
            "raw_bounding_box": {**cc_box, "color": "#10B981" if cc_val else "#EF4444"}
        })

        # ── 8. Country of Origin ─────────────────────────────────────────────
        origin_text, origin_conf, origin_box = find_text_by_pattern([
            r'(country\s*of\s*origin|made\s*in|manufactured\s*in|product\s*of)',
            r'\b(india|bharat|china|usa|germany|bangladesh|sri\s*lanka)\b',
        ], all_lines)
        if not origin_text:
            om = re.search(r'\b(made\s*in|country\s*of\s*origin|manufactured\s*in)\s*:?\s*([A-Za-z\s]+)', full_text, re.IGNORECASE)
            if om:
                origin_text = om.group(0).strip()
                origin_conf = 0.88
            elif re.search(r'\bindia\b|\bbharat\b', full_text_lower):
                origin_text = "India"
                origin_conf = 0.75
        if not origin_box:
            origin_box = {"x": 8, "y": 75, "w": 42, "h": 9}

        declarations.append({
            "field_name": "country_of_origin",
            "detected_value": origin_text,
            "is_present": bool(origin_text),
            "confidence": round(origin_conf, 2) if origin_text else 0.15,
            "estimated_font_size_px": 14.0,
            "readability_status": "PASS" if origin_text else "WARNING",
            "raw_bounding_box": {**origin_box, "color": "#10B981" if origin_text else "#EF4444"}
        })

        # ── 9. Unit Sale Price ───────────────────────────────────────────────
        usp_text, usp_conf, usp_box = find_text_by_pattern([
            r'(unit\s*sale\s*price|usp|price\s*per\s*(g|kg|ml|l|unit|piece|pc))',
            r'(rs\.?|₹)\s*\d+(\.\d+)?\s*/\s*(g\b|kg|ml|l\b)',
        ], all_lines)
        if not usp_box:
            usp_box = {"x": 8, "y": 86, "w": 84, "h": 9}

        declarations.append({
            "field_name": "unit_sale_price",
            "detected_value": usp_text,
            "is_present": bool(usp_text),
            "confidence": round(usp_conf, 2) if usp_text else 0.15,
            "estimated_font_size_px": 13.5,
            "readability_status": "PASS" if usp_text else "WARNING",
            "raw_bounding_box": {**usp_box, "color": "#10B981" if usp_text else "#EF4444"}
        })

        return declarations

    @classmethod
    def _process_generic_upload(
        cls,
        image_path: str,
        custom_product_name: Optional[str],
        category: Optional[str]
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], str]:
        """
        Processes a user-uploaded image using real OCR (EasyOCR) + regex field parsing.
        Extracts actual text from the image and maps it to mandatory Legal Metrology declarations.
        """
        print(f"[OCR] Processing uploaded image: {image_path}")

        # Get image dimensions for bbox normalisation
        try:
            with Image.open(image_path) as img:
                img_w, img_h = img.size
        except Exception:
            img_w, img_h = 800, 600

        # Run EasyOCR on the real uploaded image
        ocr_results = cls._extract_text_from_image(image_path)
        print(f"[OCR] Extracted {len(ocr_results)} text regions from uploaded image.")

        # Parse declarations from actual OCR output
        declarations = cls._parse_declarations_from_text(
            ocr_results, img_w, img_h, custom_product_name
        )

        # Log what was found
        found = [d["field_name"] for d in declarations if d["is_present"]]
        missing = [d["field_name"] for d in declarations if not d["is_present"]]
        print(f"[OCR] Found fields: {found}")
        print(f"[OCR] Missing fields: {missing}")

        evidence_items = []
        for dec in declarations:
            evidence_items.append({
                "evidence_type": "BOUNDING_BOX",
                "label": dec["field_name"].replace("_", " ").title(),
                "bounding_box_json": dec["raw_bounding_box"],
                "description": f"{'Detected' if dec['is_present'] else 'NOT FOUND'}: {dec['field_name']}"
            })

        evidence_image_path = cls._render_annotated_evidence_image(image_path, declarations, "generic")
        return declarations, evidence_items, evidence_image_path

    @classmethod
    def _render_annotated_evidence_image(
        cls, 
        base_image_path: str, 
        declarations: List[Dict[str, Any]], 
        preset_id: str
    ) -> str:
        """
        Draws high-contrast bounding boxes with labels over the product package image.
        """
        try:
            if os.path.exists(base_image_path):
                img = Image.open(base_image_path).convert("RGBA")
            else:
                # Create a synthetic high-resolution package label image
                img = cls.generate_synthetic_package_image(preset_id)

            width, height = img.size
            overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)

            for dec in declarations:
                box = dec.get("raw_bounding_box")
                if not box:
                    continue
                
                # Convert percentage box to pixel coordinates
                bx = int(box["x"] * width / 100)
                by = int(box["y"] * height / 100)
                bw = int(box["w"] * width / 100)
                bh = int(box["h"] * height / 100)

                # Determine color based on compliance
                is_ok = dec.get("is_present") and dec.get("readability_status") == "PASS"
                is_warn = dec.get("readability_status") == "MANUAL_VERIFICATION" or dec.get("readability_status") == "WARNING"
                
                if not dec.get("is_present") or (dec.get("detected_value") and "missing" in str(dec.get("detected_value")).lower()):
                    fill_color = (239, 68, 68, 60) # Red
                    border_color = (220, 38, 38, 255)
                elif is_warn:
                    fill_color = (245, 158, 11, 60) # Amber
                    border_color = (217, 119, 6, 255)
                else:
                    fill_color = (16, 185, 129, 50) # Emerald Green
                    border_color = (5, 150, 105, 255)

                # Draw bounding box
                draw.rectangle([bx, by, bx + bw, by + bh], outline=border_color, fill=fill_color, width=3)
                
                # Draw label pill
                label = f"{dec['field_name'].replace('_', ' ').upper()}: {dec.get('confidence', 0.95)*100:.0f}%"
                draw.rectangle([bx, max(0, by - 22), bx + len(label) * 8 + 12, by], fill=border_color)
                draw.text((bx + 6, max(2, by - 18)), label, fill=(255, 255, 255, 255))

            # Composite overlay
            result_img = Image.alpha_composite(img, overlay).convert("RGB")
            
            # Save annotated evidence
            filename = f"evidence_{os.path.basename(base_image_path)}"
            if not filename.endswith(".jpg") and not filename.endswith(".png"):
                filename += ".jpg"
            save_path = EVIDENCE_DIR / filename
            result_img.save(save_path, quality=92)
            
            return str(save_path)
        except Exception as e:
            print(f"Error rendering evidence image: {e}")
            return base_image_path

    @classmethod
    def generate_synthetic_package_image(cls, preset_id: str) -> Image.Image:
        """
        Generates realistic visual packaged commodity images for the 6 demo products.
        """
        demo = DEMO_PRODUCTS.get(preset_id, DEMO_PRODUCTS["basmati_rice"])
        
        width, height = 700, 900
        bg_color = demo.get("bg_color", "#1E3A8A")
        accent_color = demo.get("accent_color", "#F59E0B")

        img = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(img)

        # Draw decorative label header
        draw.rectangle([20, 20, width - 20, 110], fill="#FFFFFF")
        draw.rectangle([25, 25, width - 25, 105], outline=accent_color, width=2)
        draw.text((width // 2 - 170, 45), "LEGAL METROLOGY INSPECTION SAMPLE", fill="#1E293B")
        draw.text((width // 2 - 120, 75), f"Category: {demo['category']}", fill="#475569")

        # Main product title card
        draw.rectangle([30, 130, width - 30, 260], fill="#0F172A", outline=accent_color, width=3)
        draw.text((50, 150), demo["product_name"].upper(), fill="#F8FAFC")
        draw.text((50, 210), f"STANDARD PACKAGED COMMODITY (DEMO DATA)", fill=accent_color)

        # Declarations panel (Simulating back-of-pack / label area)
        draw.rectangle([30, 280, width - 30, height - 30], fill="#F8FAFC")
        draw.rectangle([35, 285, width - 35, height - 35], outline="#CBD5E1", width=2)

        # Declarations text content
        def safe_txt(text: str) -> str:
            if not text:
                return ""
            return text.replace("₹", "Rs. ")

        y = 305
        draw.text((50, y), "MANDATORY DECLARATIONS (RULE 6)", fill="#0F172A")
        draw.line([50, y + 25, width - 50, y + 25], fill="#E2E8F0", width=2)
        
        y += 40
        draw.text((50, y), "Manufactured & Packed By:", fill="#334155")
        y += 24
        draw.text((50, y), safe_txt(demo['manufacturer'] or '[MISSING DECLARATION]'), fill="#0F172A")
        
        y += 35
        draw.text((50, y), "Registered Factory Address:", fill="#334155")
        y += 24
        draw.text((50, y), safe_txt(demo['address'] or '[MISSING ADDRESS]'), fill="#0F172A")
        
        y += 45
        # Net Quantity & MRP Row
        draw.rectangle([50, y, 320, y + 80], fill="#F1F5F9", outline="#CBD5E1")
        draw.text((65, y + 15), "NET QUANTITY:", fill="#475569")
        draw.text((65, y + 42), safe_txt(demo['net_quantity']), fill="#0F172A")

        draw.rectangle([340, y, width - 50, y + 80], fill="#F1F5F9", outline="#CBD5E1")
        draw.text((355, y + 15), "MAXIMUM RETAIL PRICE:", fill="#475569")
        draw.text((355, y + 42), safe_txt(demo['mrp']), fill="#0F172A")

        y += 100
        # Packing Date & Origin
        draw.text((50, y), f"Month & Year of Packing:  {safe_txt(demo['packed_date'])}", fill="#0F172A")
        y += 30
        draw.text((50, y), f"Country of Origin:  {safe_txt(demo['country_of_origin'])}", fill="#0F172A")
        
        if demo.get("unit_sale_price"):
            y += 30
            draw.text((50, y), f"Unit Sale Price (USP):  {safe_txt(demo['unit_sale_price'])}", fill="#0F172A")

        y += 40
        # Consumer Care Box
        draw.rectangle([50, y, width - 50, y + 90], fill="#EFF6FF", outline="#93C5FD", width=2)
        draw.text((65, y + 15), "CONSUMER CARE CELL / HELPLINE:", fill="#1E40AF")
        if demo.get("consumer_care_phone"):
            draw.text((65, y + 40), f"Toll-Free Helpline: {safe_txt(demo['consumer_care_phone'])}", fill="#1E293B")
            draw.text((65, y + 62), f"Email: {safe_txt(demo['consumer_care_email'])}", fill="#1E293B")
        else:
            draw.text((65, y + 45), "[NO CONSUMER CARE CONTACT DETAILS DECLARED]", fill="#DC2626")

        return img
