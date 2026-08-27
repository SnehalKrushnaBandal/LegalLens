"""
General-Purpose Legal Metrology Compliance Dataset Generator (SIH26034)
Generates a product-agnostic, reusable labeled dataset covering:
  - Any packaged commodity category
  - All 10 Legal Metrology (PC) Rules 2011 violation types
  - Realistic Indian market data with wide product diversity

Output:
  dataset/general/train.csv        - Training split (~70%)
  dataset/general/test.csv         - Test split (~20%)
  dataset/general/validation.csv   - Validation split (~10%)
  dataset/general/train.json
  dataset/general/test.json
  dataset/general/validation.json
  dataset/general/dataset_card.md
"""

import csv
import json
import random
import os
from datetime import datetime, timedelta

random.seed(2026)
os.makedirs("dataset/general", exist_ok=True)

# ─── Broad Product Universe ───────────────────────────────────────────────────
PRODUCTS = [
    # Food & Beverages
    {"name": "Basmati Rice", "category": "Staples", "typical_qty": "1kg", "unit": "kg"},
    {"name": "Wheat Flour (Atta)", "category": "Staples", "typical_qty": "5kg", "unit": "kg"},
    {"name": "Sugar", "category": "Staples", "typical_qty": "1kg", "unit": "kg"},
    {"name": "Rock Salt", "category": "Staples", "typical_qty": "500g", "unit": "g"},
    {"name": "Chana Dal", "category": "Pulses", "typical_qty": "500g", "unit": "g"},
    {"name": "Moong Dal", "category": "Pulses", "typical_qty": "500g", "unit": "g"},
    {"name": "Toor Dal", "category": "Pulses", "typical_qty": "1kg", "unit": "kg"},
    {"name": "Refined Sunflower Oil", "category": "Edible Oil", "typical_qty": "1l", "unit": "l"},
    {"name": "Mustard Oil", "category": "Edible Oil", "typical_qty": "500ml", "unit": "ml"},
    {"name": "Extra Virgin Olive Oil", "category": "Edible Oil", "typical_qty": "250ml", "unit": "ml"},
    {"name": "Cow Ghee", "category": "Dairy", "typical_qty": "500g", "unit": "g"},
    {"name": "Butter", "category": "Dairy", "typical_qty": "100g", "unit": "g"},
    {"name": "Paneer", "category": "Dairy", "typical_qty": "200g", "unit": "g"},
    {"name": "Curd (Dahi)", "category": "Dairy", "typical_qty": "400g", "unit": "g"},
    {"name": "Full Cream Milk Powder", "category": "Dairy", "typical_qty": "500g", "unit": "g"},
    {"name": "Plain Biscuits", "category": "Snacks & Bakery", "typical_qty": "200g", "unit": "g"},
    {"name": "Cream Biscuits", "category": "Snacks & Bakery", "typical_qty": "100g", "unit": "g"},
    {"name": "Instant Noodles", "category": "Snacks & Bakery", "typical_qty": "70g", "unit": "g"},
    {"name": "Potato Chips", "category": "Snacks & Bakery", "typical_qty": "50g", "unit": "g"},
    {"name": "Namkeen Mix", "category": "Snacks & Bakery", "typical_qty": "250g", "unit": "g"},
    {"name": "Fruit Jam", "category": "Condiments", "typical_qty": "500g", "unit": "g"},
    {"name": "Tomato Ketchup", "category": "Condiments", "typical_qty": "500g", "unit": "g"},
    {"name": "Pickle (Achar)", "category": "Condiments", "typical_qty": "400g", "unit": "g"},
    {"name": "Honey", "category": "Condiments", "typical_qty": "250g", "unit": "g"},
    {"name": "Garam Masala", "category": "Spices", "typical_qty": "100g", "unit": "g"},
    {"name": "Turmeric Powder", "category": "Spices", "typical_qty": "200g", "unit": "g"},
    {"name": "Red Chilli Powder", "category": "Spices", "typical_qty": "100g", "unit": "g"},
    {"name": "Cumin Seeds", "category": "Spices", "typical_qty": "100g", "unit": "g"},
    {"name": "Coriander Powder", "category": "Spices", "typical_qty": "100g", "unit": "g"},
    {"name": "Instant Coffee", "category": "Beverages", "typical_qty": "50g", "unit": "g"},
    {"name": "Tea Bags", "category": "Beverages", "typical_qty": "100g", "unit": "g"},
    {"name": "Health Drink Mix", "category": "Beverages", "typical_qty": "500g", "unit": "g"},
    {"name": "Carbonated Soft Drink", "category": "Beverages", "typical_qty": "500ml", "unit": "ml"},
    {"name": "Fruit Juice (Tetra Pack)", "category": "Beverages", "typical_qty": "200ml", "unit": "ml"},
    {"name": "Drinking Water", "category": "Beverages", "typical_qty": "1l", "unit": "l"},
    {"name": "Glucose Powder", "category": "Health", "typical_qty": "200g", "unit": "g"},
    {"name": "Multivitamin Tablets", "category": "Health", "typical_qty": "60N", "unit": "N"},
    {"name": "Ayurvedic Churan", "category": "Health", "typical_qty": "100g", "unit": "g"},
    {"name": "Protein Supplement", "category": "Health", "typical_qty": "500g", "unit": "g"},
    {"name": "Digestive Tablets", "category": "Health", "typical_qty": "30N", "unit": "N"},
    # Personal Care
    {"name": "Shampoo", "category": "Personal Care", "typical_qty": "200ml", "unit": "ml"},
    {"name": "Hair Conditioner", "category": "Personal Care", "typical_qty": "175ml", "unit": "ml"},
    {"name": "Body Lotion", "category": "Personal Care", "typical_qty": "400ml", "unit": "ml"},
    {"name": "Face Wash", "category": "Personal Care", "typical_qty": "100ml", "unit": "ml"},
    {"name": "Bathing Soap", "category": "Personal Care", "typical_qty": "125g", "unit": "g"},
    {"name": "Toothpaste", "category": "Personal Care", "typical_qty": "200g", "unit": "g"},
    {"name": "Toothbrush", "category": "Personal Care", "typical_qty": "1N", "unit": "N"},
    {"name": "Deodorant Spray", "category": "Personal Care", "typical_qty": "150ml", "unit": "ml"},
    {"name": "Sunscreen Lotion", "category": "Personal Care", "typical_qty": "100ml", "unit": "ml"},
    {"name": "Talcum Powder", "category": "Personal Care", "typical_qty": "200g", "unit": "g"},
    {"name": "Hair Oil", "category": "Personal Care", "typical_qty": "200ml", "unit": "ml"},
    {"name": "Shaving Cream", "category": "Personal Care", "typical_qty": "70g", "unit": "g"},
    {"name": "Moisturizing Cream", "category": "Personal Care", "typical_qty": "100ml", "unit": "ml"},
    {"name": "Lip Balm", "category": "Personal Care", "typical_qty": "4g", "unit": "g"},
    # Household Cleaning
    {"name": "Dish Wash Bar", "category": "Household", "typical_qty": "250g", "unit": "g"},
    {"name": "Detergent Powder", "category": "Household", "typical_qty": "1kg", "unit": "kg"},
    {"name": "Liquid Detergent", "category": "Household", "typical_qty": "500ml", "unit": "ml"},
    {"name": "Toilet Cleaner", "category": "Household", "typical_qty": "500ml", "unit": "ml"},
    {"name": "Floor Cleaner", "category": "Household", "typical_qty": "1l", "unit": "l"},
    {"name": "Glass Cleaner", "category": "Household", "typical_qty": "500ml", "unit": "ml"},
    {"name": "Mosquito Repellent Liquid", "category": "Household", "typical_qty": "45ml", "unit": "ml"},
    {"name": "Air Freshener Spray", "category": "Household", "typical_qty": "200ml", "unit": "ml"},
    {"name": "Fabric Softener", "category": "Household", "typical_qty": "500ml", "unit": "ml"},
    # Stationery & Other
    {"name": "Eraser", "category": "Stationery", "typical_qty": "10N", "unit": "N"},
    {"name": "Pen (Ball Point)", "category": "Stationery", "typical_qty": "5N", "unit": "N"},
    {"name": "Notebook", "category": "Stationery", "typical_qty": "1N", "unit": "N"},
    {"name": "Adhesive Tape", "category": "Stationery", "typical_qty": "25m", "unit": "m"},
    # Agricultural / Seeds
    {"name": "Hybrid Tomato Seeds", "category": "Agriculture", "typical_qty": "10g", "unit": "g"},
    {"name": "Fertilizer (NPK)", "category": "Agriculture", "typical_qty": "1kg", "unit": "kg"},
    {"name": "Pesticide Spray", "category": "Agriculture", "typical_qty": "500ml", "unit": "ml"},
]

# ─── Manufacturer Pool (generic Indian companies) ────────────────────────────
MANUFACTURERS = [
    ("Sunrise Foods Pvt. Ltd.", "Plot No. 14, MIDC Industrial Area, Pune, Maharashtra - 411026"),
    ("GreenLeaf Agro Industries", "Survey No. 87, Rajkot Industrial Estate, Rajkot, Gujarat - 360002"),
    ("National Packaged Goods Ltd.", "B-12, Okhla Industrial Phase II, New Delhi - 110020"),
    ("Apex Consumer Products", "No. 7, 3rd Cross, Peenya Industrial Area, Bengaluru, Karnataka - 560058"),
    ("Bharat Organic Farms", "Village Narsingpur, Tehsil Harda, Madhya Pradesh - 461331"),
    ("Star FMCG Corporation", "Sector 63, NOIDA, Uttar Pradesh - 201301"),
    ("Prime Industries Ltd.", "Survey 45/A, Vatva GIDC, Ahmedabad, Gujarat - 382445"),
    ("Evergreen Manufacturing Co.", "Phase II, Industrial Zone, Ludhiana, Punjab - 141010"),
    ("Hindustan Consumer Goods", "Andheri East, MIDC, Mumbai, Maharashtra - 400093"),
    ("Royal Produce Pvt. Ltd.", "NH-44 Bypass Road, Hyderabad, Telangana - 500072"),
    ("Agro Vision Industries", "Kumbargaon MIDC, Ahmednagar, Maharashtra - 414003"),
    ("Disha Exports & Imports", "No. 34, Anna Salai, Chennai, Tamil Nadu - 600002"),
    ("Shree Ganesh Processors", "Near Water Tank, Sikar Road, Jaipur, Rajasthan - 302023"),
    ("Pushpak Packaging Pvt. Ltd.", "Industrial Area Phase 1, Chandigarh - 160002"),
    ("JR Manufacturing", "K-18, RIICO Industrial Area, Bhiwadi, Rajasthan - 301019"),
    ("Bengal Foods International", "Park Circus, Kolkata, West Bengal - 700017"),
    ("Kerala Naturals Pvt. Ltd.", "SY 22/3, Edapally, Kochi, Kerala - 682024"),
    ("Odisha Produce Ltd.", "Chandaka Industrial Estate, Bhubaneswar, Odisha - 751024"),
    ("MP Agro Industries", "Pologround Industrial Area, Indore, Madhya Pradesh - 452015"),
    ("TechPack Solutions", "EPIP Zone, Whitefield, Bengaluru, Karnataka - 560066"),
    ("Unknown Brand", ""),   # For missing-address violation
    ("XYZ Products", "Shop 2"),  # Incomplete address
]

NON_STANDARD_UNITS = ["gms", "Gms", "GMS", "kilos", "Kgs", "lts", "Liters", "Ltr", "grms", "grm", "mls"]
COUNTRIES = ["India", "India", "India", "India", "India", "Made in India", "Manufactured in India", "Bharat", "China", "Germany", "USA", "Bangladesh"]
HELPLINES = [
    ("1800-103-1234", "support@company.in"),
    ("1800-200-5678", "care@brand.com"),
    ("1800-419-8900", "consumer@product.in"),
    ("1800-890-0011", "help@business.co.in"),
    ("1800-572-3344", "grievance@goods.in"),
    ("011-23456789", "contact@firm.co.in"),
    ("1800-123-7890", "info@pack.in"),
    ("", ""),  # For missing-consumer-care violation
]
READABILITIES = ["GOOD", "GOOD", "GOOD", "GOOD", "MODERATE", "MODERATE", "POOR"]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def random_qty_value(unit, base_qty_str):
    """Return randomised quantity string."""
    try:
        base_num = float(''.join(filter(lambda c: c.isdigit() or c == '.', base_qty_str)))
        variations = [base_num * 0.5, base_num, base_num * 2]
        val = random.choice(variations)
        if val == int(val):
            return f"{int(val)}{unit}"
        return f"{val}{unit}"
    except:
        return base_qty_str

def random_mrp():
    return round(random.choice([9.5, 15, 20, 25, 30, 35, 50, 75, 99, 120, 150, 180, 200,
                                 250, 299, 350, 399, 450, 499, 550, 650, 750, 850, 999, 1199, 1499]), 2)

def random_date():
    start = datetime(2022, 1, 1)
    delta = timedelta(days=random.randint(0, 1000))
    return (start + delta).strftime("%m/%Y")

def compute_usp(mrp, qty_str, unit):
    try:
        num = float(''.join(filter(lambda c: c.isdigit() or c == '.', qty_str.replace(unit, ''))))
        return round(mrp / max(num, 0.001), 4)
    except:
        return round(mrp / 100, 4)

VIOLATION_TYPES = [
    "no_product_name",
    "no_manufacturer",
    "incomplete_address",
    "non_standard_unit",
    "mrp_no_tax_phrase",
    "no_packing_date",
    "no_consumer_care",
    "no_country_of_origin",
    "no_usp",
    "poor_readability",
]

RULE_SEVERITY = {
    "LM-PC-001": "CRITICAL",
    "LM-PC-002": "HIGH",
    "LM-PC-003": "HIGH",
    "LM-PC-004": "CRITICAL",
    "LM-PC-005": "CRITICAL",
    "LM-PC-006": "HIGH",
    "LM-PC-007": "HIGH",
    "LM-PC-008": "HIGH",
    "LM-PC-009": "MEDIUM",
    "LM-PC-010": "MEDIUM",
}

SCORE_DEDUCTIONS = {
    "CRITICAL": 25,
    "HIGH": 15,
    "MEDIUM": 8,
    "LOW": 4,
}

def make_sample(idx, force_compliant=False, forced_violations=None):
    product = random.choice(PRODUCTS)
    mfr_name, mfr_address = random.choice(MANUFACTURERS[:-2])  # Usually pick valid
    helpline_phone, helpline_email = random.choice(HELPLINES[:-1])
    country = random.choice(COUNTRIES)
    readability = random.choice(READABILITIES)
    unit = product["unit"]
    base_qty = product["typical_qty"]
    qty = random_qty_value(unit, base_qty)
    mrp = random_mrp()
    usp = compute_usp(mrp, qty, unit)
    packing_date = random_date()
    batch_no = f"BN{random.randint(1000,9999)}"
    barcode = f"890{random.randint(1000000000, 9999999999)}"

    # Default correct values
    f_product_name = product["name"]
    f_category = product["category"]
    f_mfr_name = mfr_name
    f_mfr_address = mfr_address
    f_net_qty = qty
    f_unit = unit
    f_mrp_text = f"MRP Rs. {mrp} (Incl. of all taxes)"
    f_mrp_val = mrp
    f_packing_date = packing_date
    f_phone = helpline_phone
    f_email = helpline_email
    f_country = country
    f_usp = f"Rs. {usp} per {unit}"
    f_readability = readability
    f_batch = batch_no
    f_barcode = barcode

    violations_found = []
    violation_rules = []

    if not force_compliant:
        v_list = forced_violations or random.sample(
            VIOLATION_TYPES, k=random.choice([1, 1, 1, 2, 2, 3, 4])
        )

        for v in v_list:
            if v == "no_product_name":
                f_product_name = ""
                violations_found.append("Missing product/commodity name on label")
                violation_rules.append("LM-PC-001")
            elif v == "no_manufacturer":
                f_mfr_name = ""
                violations_found.append("Manufacturer/packer name not declared")
                violation_rules.append("LM-PC-002")
            elif v == "incomplete_address":
                if f_mfr_address:
                    f_mfr_address = f_mfr_address.split(",")[0].strip()
                else:
                    f_mfr_address = "India"
                violations_found.append("Incomplete address — PIN code / State missing")
                violation_rules.append("LM-PC-003")
            elif v == "non_standard_unit":
                bad = random.choice(NON_STANDARD_UNITS)
                f_unit = bad
                f_net_qty = qty.replace(unit, bad)
                violations_found.append(f"Non-standard unit '{bad}' used (must be SI: g/kg/ml/l/N/m)")
                violation_rules.append("LM-PC-004")
            elif v == "mrp_no_tax_phrase":
                f_mrp_text = f"MRP Rs. {mrp}"
                violations_found.append("MRP missing mandatory phrase 'inclusive of all taxes'")
                violation_rules.append("LM-PC-005")
            elif v == "no_packing_date":
                f_packing_date = ""
                violations_found.append("Month and year of manufacture / packing not declared")
                violation_rules.append("LM-PC-006")
            elif v == "no_consumer_care":
                f_phone = ""
                f_email = ""
                violations_found.append("Consumer care helpline and email not provided")
                violation_rules.append("LM-PC-007")
            elif v == "no_country_of_origin":
                f_country = ""
                violations_found.append("Country of Origin declaration missing")
                violation_rules.append("LM-PC-008")
            elif v == "no_usp":
                f_usp = ""
                violations_found.append("Unit Sale Price (USP) not declared")
                violation_rules.append("LM-PC-009")
            elif v == "poor_readability":
                f_readability = "POOR"
                violations_found.append("Label text readability below minimum statutory requirement (Rule 7)")
                violation_rules.append("LM-PC-010")

    # Compute score
    score = 100
    for rule in violation_rules:
        sev = RULE_SEVERITY.get(rule, "MEDIUM")
        score -= SCORE_DEDUCTIONS.get(sev, 8)
    score = max(0, score)

    compliance = "COMPLIANT" if not violations_found else "NON_COMPLIANT"
    if force_compliant:
        compliance = "COMPLIANT"
        score = 100
        violations_found = []
        violation_rules = []

    # Determine risk tier
    if score == 100:
        risk = "NONE"
    elif score >= 80:
        risk = "LOW"
    elif score >= 60:
        risk = "MEDIUM"
    elif score >= 40:
        risk = "HIGH"
    else:
        risk = "CRITICAL"

    return {
        # Identifiers
        "sample_id": f"LM-GEN-{idx:05d}",
        "batch_number": f_batch,
        "barcode": f_barcode,

        # Product Info
        "product_name": f_product_name,
        "product_category": f_category,

        # Manufacturer Info
        "manufacturer_name": f_mfr_name,
        "manufacturer_address": f_mfr_address,

        # Quantity
        "net_quantity": f_net_qty,
        "unit_of_measurement": f_unit,

        # Price
        "mrp_declaration": f_mrp_text,
        "mrp_value_inr": f_mrp_val,
        "unit_sale_price": f_usp,

        # Date
        "packing_date": f_packing_date,

        # Consumer Care
        "consumer_care_phone": f_phone,
        "consumer_care_email": f_email,

        # Origin & Readability
        "country_of_origin": f_country,
        "label_readability": f_readability,

        # Labels (Target Outputs)
        "compliance_status": compliance,
        "compliance_score": score,
        "risk_tier": risk,
        "violation_count": len(violations_found),
        "violated_rules": "; ".join(violation_rules) if violation_rules else "None",
        "violation_descriptions": " | ".join(violations_found) if violations_found else "None",
    }

# ─── Generate Samples ─────────────────────────────────────────────────────────
all_samples = []
idx = 1

# 1. One compliant sample per product (65 products)
for p in PRODUCTS:
    s = make_sample(idx, force_compliant=True)
    s["product_name"] = p["name"]
    s["product_category"] = p["category"]
    s["net_quantity"] = p["typical_qty"]
    s["unit_of_measurement"] = p["unit"]
    s["compliance_status"] = "COMPLIANT"
    s["compliance_score"] = 100
    s["risk_tier"] = "NONE"
    s["violation_count"] = 0
    s["violated_rules"] = "None"
    s["violation_descriptions"] = "None"
    all_samples.append(s)
    idx += 1

# 2. One dedicated sample per violation type per product category (covers all rules)
categories = list({p["category"] for p in PRODUCTS})
for viol in VIOLATION_TYPES:
    for cat in categories:
        s = make_sample(idx, force_compliant=False, forced_violations=[viol])
        s["product_category"] = cat
        all_samples.append(s)
        idx += 1

# 3. Multi-violation combos — 2 violations
two_combos = [
    ["no_product_name", "mrp_no_tax_phrase"],
    ["no_manufacturer", "no_country_of_origin"],
    ["incomplete_address", "no_consumer_care"],
    ["non_standard_unit", "no_usp"],
    ["no_packing_date", "poor_readability"],
    ["no_country_of_origin", "no_usp"],
    ["mrp_no_tax_phrase", "no_packing_date"],
    ["no_product_name", "no_manufacturer"],
    ["non_standard_unit", "mrp_no_tax_phrase"],
    ["no_consumer_care", "no_usp"],
]
for combo in two_combos:
    for _ in range(8):
        all_samples.append(make_sample(idx, force_compliant=False, forced_violations=combo))
        idx += 1

# 4. Multi-violation combos — 3+ violations
three_combos = [
    ["no_product_name", "mrp_no_tax_phrase", "no_country_of_origin"],
    ["no_manufacturer", "incomplete_address", "no_consumer_care"],
    ["non_standard_unit", "no_packing_date", "no_usp"],
    ["no_product_name", "no_manufacturer", "no_packing_date", "no_consumer_care"],
    ["mrp_no_tax_phrase", "no_country_of_origin", "no_usp", "poor_readability"],
]
for combo in three_combos:
    for _ in range(10):
        all_samples.append(make_sample(idx, force_compliant=False, forced_violations=combo))
        idx += 1

# 5. Random varied samples (bulk)
for _ in range(400):
    all_samples.append(make_sample(idx, force_compliant=random.random() > 0.5))
    idx += 1

# Shuffle
random.shuffle(all_samples)
for i, s in enumerate(all_samples, 1):
    s["sample_id"] = f"LM-GEN-{i:05d}"

# ─── Split 70 / 20 / 10 ──────────────────────────────────────────────────────
n = len(all_samples)
n_train = int(n * 0.70)
n_val   = int(n * 0.10)
train_data = all_samples[:n_train]
val_data   = all_samples[n_train:n_train + n_val]
test_data  = all_samples[n_train + n_val:]

CSV_FIELDS = [
    "sample_id", "batch_number", "barcode",
    "product_name", "product_category",
    "manufacturer_name", "manufacturer_address",
    "net_quantity", "unit_of_measurement",
    "mrp_declaration", "mrp_value_inr", "unit_sale_price",
    "packing_date",
    "consumer_care_phone", "consumer_care_email",
    "country_of_origin", "label_readability",
    "compliance_status", "compliance_score", "risk_tier",
    "violation_count", "violated_rules", "violation_descriptions"
]

def write_csv(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

write_csv("dataset/general/train.csv", train_data)
write_csv("dataset/general/validation.csv", val_data)
write_csv("dataset/general/test.csv", test_data)
write_json("dataset/general/train.json", train_data)
write_json("dataset/general/validation.json", val_data)
write_json("dataset/general/test.json", test_data)

# ─── Stats ────────────────────────────────────────────────────────────────────
def stats(data):
    comp = sum(1 for s in data if s["compliance_status"] == "COMPLIANT")
    return len(data), comp, len(data) - comp

t_n, t_c, t_nc = stats(train_data)
v_n, v_c, v_nc = stats(val_data)
te_n, te_c, te_nc = stats(test_data)
total = t_n + v_n + te_n

# Category counts
cat_counts = {}
for s in all_samples:
    c = s["product_category"]
    cat_counts[c] = cat_counts.get(c, 0) + 1

# Violation rule frequency
rule_freq = {}
for s in all_samples:
    if s["violated_rules"] != "None":
        for r in s["violated_rules"].split("; "):
            r = r.strip()
            if r:
                rule_freq[r] = rule_freq.get(r, 0) + 1

# ─── Dataset Card ─────────────────────────────────────────────────────────────
card = f"""# General Legal Metrology Compliance Dataset
### SIH26034 — Smart India Hackathon 2026
**Standard:** Legal Metrology (Packaged Commodities) Rules, 2011  
**Scope:** Any packaged commodity sold in India  
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Overview
A product-agnostic, general-purpose labeled dataset for training, evaluating, and benchmarking
automated Legal Metrology compliance checking systems. Covers {len(PRODUCTS)} distinct product
types across {len(categories)} industry categories, with all 10 statutory rule violation types
systematically represented.

---

## Dataset Splits

| Split | Total | COMPLIANT | NON_COMPLIANT |
|-------|-------|-----------|---------------|
| **Train** | {t_n} | {t_c} | {t_nc} |
| **Validation** | {v_n} | {v_c} | {v_nc} |
| **Test** | {te_n} | {te_c} | {te_nc} |
| **Total** | **{total}** | **{t_c+v_c+te_c}** | **{t_nc+v_nc+te_nc}** |

---

## Feature Schema (23 columns)

| # | Column | Type | Description |
|---|--------|------|-------------|
| 1 | `sample_id` | str | Unique record identifier (LM-GEN-XXXXX) |
| 2 | `batch_number` | str | Product batch / lot number |
| 3 | `barcode` | str | EAN-13 style barcode number |
| 4 | `product_name` | str | Generic/common commodity name on label *(may be blank — violation)* |
| 5 | `product_category` | str | Product category (Staples, Dairy, Personal Care, etc.) |
| 6 | `manufacturer_name` | str | Name of manufacturer / packer / importer *(may be blank — violation)* |
| 7 | `manufacturer_address` | str | Factory/registered address *(may be incomplete — violation)* |
| 8 | `net_quantity` | str | Net quantity with unit (e.g. `500g`, `1l`) *(may use non-SI — violation)* |
| 9 | `unit_of_measurement` | str | Unit symbol — SI (`g`,`kg`,`ml`,`l`,`N`,`m`) or non-standard |
| 10 | `mrp_declaration` | str | Full MRP text on label *(may lack tax phrase — violation)* |
| 11 | `mrp_value_inr` | float | Numeric MRP value (₹) |
| 12 | `unit_sale_price` | str | USP declaration (e.g. `Rs. 0.09 per g`) *(may be blank — violation)* |
| 13 | `packing_date` | str | Month/Year of manufacture (MM/YYYY) *(may be blank — violation)* |
| 14 | `consumer_care_phone` | str | Toll-free helpline number *(may be blank — violation)* |
| 15 | `consumer_care_email` | str | Consumer grievance email *(may be blank — violation)* |
| 16 | `country_of_origin` | str | Country of manufacture/origin *(may be blank — violation)* |
| 17 | `label_readability` | str | GOOD / MODERATE / POOR |
| 18 | `compliance_status` | str | **Target label**: `COMPLIANT` or `NON_COMPLIANT` |
| 19 | `compliance_score` | int | 0–100 weighted compliance score |
| 20 | `risk_tier` | str | NONE / LOW / MEDIUM / HIGH / CRITICAL |
| 21 | `violation_count` | int | Number of rule violations detected |
| 22 | `violated_rules` | str | Semicolon-separated rule codes (e.g. `LM-PC-004; LM-PC-005`) |
| 23 | `violation_descriptions` | str | Human-readable violation descriptions |

---

## Product Categories
| Category | Samples |
|----------|---------|
{chr(10).join(f'| {k} | {v} |' for k, v in sorted(cat_counts.items(), key=lambda x: -x[1]))}

---

## Violation Rule Coverage
| Rule Code | Category | Severity | Samples |
|-----------|----------|----------|---------|
| LM-PC-001 | Product Identification | CRITICAL | {rule_freq.get('LM-PC-001', 0)} |
| LM-PC-002 | Manufacturer Details | HIGH | {rule_freq.get('LM-PC-002', 0)} |
| LM-PC-003 | Manufacturer Address | HIGH | {rule_freq.get('LM-PC-003', 0)} |
| LM-PC-004 | Net Quantity & Units | CRITICAL | {rule_freq.get('LM-PC-004', 0)} |
| LM-PC-005 | MRP Declaration | CRITICAL | {rule_freq.get('LM-PC-005', 0)} |
| LM-PC-006 | Date of Packing | HIGH | {rule_freq.get('LM-PC-006', 0)} |
| LM-PC-007 | Consumer Care Details | HIGH | {rule_freq.get('LM-PC-007', 0)} |
| LM-PC-008 | Country of Origin | HIGH | {rule_freq.get('LM-PC-008', 0)} |
| LM-PC-009 | Unit Sale Price (USP) | MEDIUM | {rule_freq.get('LM-PC-009', 0)} |
| LM-PC-010 | Font Readability | MEDIUM | {rule_freq.get('LM-PC-010', 0)} |

---

## Legal References
- Legal Metrology (Packaged Commodities) Rules, 2011
- Legal Metrology Act, 2009
- Rule 6(11) Amendment — Unit Sale Price (2021)
- Consumer Protection Act, 2019
- BIS (Bureau of Indian Standards) standards for labelling

## Use Cases
- Binary classification: `compliance_status` (COMPLIANT / NON_COMPLIANT)
- Multi-label classification: which specific rules are violated
- Regression: predict `compliance_score` (0–100)
- Rule-based validation engine benchmarking
- NLP/OCR post-processing accuracy evaluation
"""

with open("dataset/general/dataset_card.md", "w", encoding="utf-8") as f:
    f.write(card)

print("=" * 65)
print("  GENERAL LEGAL METROLOGY DATASET — GENERATION COMPLETE")
print("=" * 65)
print(f"  Products covered : {len(PRODUCTS)} unique products")
print(f"  Categories       : {len(categories)}")
print(f"  Total samples    : {total}")
print(f"  Train            : {t_n}  ({t_c} compliant, {t_nc} non-compliant)")
print(f"  Validation       : {v_n}  ({v_c} compliant, {v_nc} non-compliant)")
print(f"  Test             : {te_n}  ({te_c} compliant, {te_nc} non-compliant)")
print()
print("  Violation Rule Coverage:")
for rule in ["LM-PC-001","LM-PC-002","LM-PC-003","LM-PC-004","LM-PC-005",
             "LM-PC-006","LM-PC-007","LM-PC-008","LM-PC-009","LM-PC-010"]:
    print(f"    {rule}: {rule_freq.get(rule, 0)} samples")
print()
print("  Files saved to: backend/dataset/general/")
print("    train.csv / train.json")
print("    validation.csv / validation.json")
print("    test.csv / test.json")
print("    dataset_card.md")
print("=" * 65)
