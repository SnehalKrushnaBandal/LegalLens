"""
Generate labeled CSV + JSON train/test dataset for Legal Metrology Compliance System (SIH26034).
Produces:
  dataset/train.csv         - 200 labeled training samples
  dataset/test.csv          - 60 labeled test samples
  dataset/train.json        - Full JSON version of training set
  dataset/test.json         - Full JSON version of test set
  dataset/dataset_info.md   - Dataset card / documentation
"""

import csv
import json
import random
import os
from datetime import datetime, timedelta

random.seed(42)
os.makedirs("dataset", exist_ok=True)

# ─── Reference Data ──────────────────────────────────────────────────────────
PRODUCT_NAMES = [
    "Premium Basmati Rice", "Whole Wheat Atta", "Refined Sunflower Oil",
    "Fortified Cow Ghee", "Tata Salt (Iodized)", "Parle-G Biscuits",
    "Britannia Good Day Cookies", "Maggi 2-Minute Noodles", "Amul Pure Milk",
    "MDH Garam Masala", "Saffola Active Oil", "Fortune Chana Dal",
    "Ariel Matic Detergent", "Surf Excel Easy Wash", "Head & Shoulders Shampoo",
    "Dettol Original Soap", "Colgate MaxFresh Toothpaste", "Vim Dishwash Bar",
    "Bournvita Health Drink", "Horlicks Original", "Nescafe Classic Coffee",
    "Lipton Green Tea", "Kwality Wall's Ice Cream", "Mother Dairy Dahi",
    "Amul Butter", "Kissan Mixed Fruit Jam", "Glucon-D Nimbu Pani",
    "Tang Orange Drink Mix", "Hajmola Digestive Tablets", "Dabur Honey"
]

MANUFACTURERS = [
    ("KRBL Limited", "KRBL Ltd., Post Box No. 3, 5, Community Centre, New Delhi - 110017"),
    ("ITC Limited", "ITC Limited, Virginia House, 37, J.L. Nehru Road, Kolkata - 700071"),
    ("Adani Wilmar Ltd", "Fortune House, Near Navrangpura Bus Stop, Ahmedabad, Gujarat - 380009"),
    ("Amul (GCMMF)", "P.O. Box 10, Amul Dairy Road, Anand, Gujarat - 388001"),
    ("Tata Consumer Products", "1 Bishop Lefroy Road, Kolkata, West Bengal - 700020"),
    ("Parle Products Pvt. Ltd.", "Parle Products, V.J.T.I. Campus, Matunga, Mumbai - 400019"),
    ("Britannia Industries Ltd", "No. 5/1A, Hungerford Street, Kolkata, West Bengal - 700017"),
    ("Nestle India Ltd", "100/101, World Trade Centre, Barakhamba Lane, New Delhi - 110001"),
    ("Hindustan Unilever Ltd", "Unilever House, B.D. Sawant Marg, Chakala, Andheri (E), Mumbai - 400099"),
    ("Dabur India Ltd", "Dabur India Ltd., 8/3, Asaf Ali Road, New Delhi - 110002"),
    ("Procter & Gamble", "P&G Plaza, Cardinal Gracias Road, Chakala, Andheri East, Mumbai - 400099"),
    ("Marico Limited", "7th Floor, Grande Palladium, 175, CST Road, Santacruz (E), Mumbai - 400098")
]

CATEGORIES = ["Food & Beverages", "Personal Care", "Household Cleaning", "Health & Nutrition", "Dairy Products"]
COUNTRIES = ["India", "India", "India", "India", "Made in India", "Manufactured in India"]
HELPLINES = [
    ("1800-123-4567", "care@company.in"),
    ("1800-267-8900", "consumer@brand.com"),
    ("1800-120-3345", "support@india.com"),
    ("1800-425-6789", "grievance@brand.in"),
]

STANDARD_UNITS = ["g", "kg", "ml", "l", "N", "m"]
NON_STANDARD_UNITS = ["gms", "Gms", "GMS", "kilos", "Kgs", "lts", "Liters", "grm"]

VIOLATION_SCENARIOS = {
    "no_product_name": "MISSING",
    "no_manufacturer": "MISSING",
    "incomplete_address": "PARTIAL",
    "non_standard_unit": "WRONG_FORMAT",
    "mrp_no_tax_phrase": "WRONG_FORMAT",
    "no_packing_date": "MISSING",
    "no_consumer_care": "MISSING",
    "no_country_of_origin": "MISSING",
    "no_usp": "MISSING",
    "poor_readability": "LOW",
}

# ─── Generation Helpers ───────────────────────────────────────────────────────
def random_date():
    start = datetime(2023, 1, 1)
    delta = timedelta(days=random.randint(0, 900))
    d = start + delta
    return d.strftime("%m/%Y")

def random_mrp():
    return round(random.uniform(15, 1200), 2)

def random_qty(unit):
    if unit in ["g", "kg"]:
        return f"{random.choice([100, 200, 250, 500, 1000, 5])}{unit}"
    elif unit in ["ml", "l"]:
        return f"{random.choice([100, 200, 500, 750, 1, 2])}{unit}"
    else:
        return f"{random.randint(1, 100)}{unit}"

def random_usp(mrp, qty_str):
    try:
        num = float(''.join(filter(lambda c: c.isdigit() or c == '.', qty_str)))
        return round(mrp / max(num, 1), 2)
    except:
        return round(mrp / 100, 2)

def make_sample(idx, force_compliant=None, injected_violations=None):
    """Generate one labeled record."""
    product_name = random.choice(PRODUCT_NAMES)
    mfr_name, mfr_address = random.choice(MANUFACTURERS)
    category = random.choice(CATEGORIES)
    helpline_no, helpline_email = random.choice(HELPLINES)
    country = random.choice(COUNTRIES)
    standard_unit = random.choice(STANDARD_UNITS)
    mrp = random_mrp()
    qty = random_qty(standard_unit)
    usp = random_usp(mrp, qty)
    packing_date = random_date()
    readability = random.choice(["GOOD", "GOOD", "GOOD", "MODERATE", "POOR"])

    # Decide violation pattern
    violations = injected_violations or []
    is_compliant = (force_compliant is True) or (not violations and random.random() > 0.45)

    # ── Field values (default = correct) ──
    f_product_name = product_name
    f_manufacturer = mfr_name
    f_address = mfr_address
    f_net_quantity = qty
    f_unit = standard_unit
    f_mrp = f"Rs. {mrp} (Incl. of all taxes)"
    f_mrp_raw = mrp
    f_packing_date = packing_date
    f_consumer_care_phone = helpline_no
    f_consumer_care_email = helpline_email
    f_country_of_origin = country
    f_usp = f"Rs. {usp} per {standard_unit}"
    f_readability = readability

    # ── Apply violation injections ──
    violation_labels = []

    if not is_compliant:
        if not violations:
            # Randomly pick 1–4 violations
            n = random.randint(1, 4)
            violations = random.sample(list(VIOLATION_SCENARIOS.keys()), n)

        for viol in violations:
            if viol == "no_product_name":
                f_product_name = ""
                violation_labels.append("LM-PC-001: Missing product name")
            elif viol == "no_manufacturer":
                f_manufacturer = ""
                violation_labels.append("LM-PC-002: Missing manufacturer name")
            elif viol == "incomplete_address":
                f_address = f_address.split(",")[0]  # Only first part
                violation_labels.append("LM-PC-003: Incomplete address (no PIN/State)")
            elif viol == "non_standard_unit":
                bad_unit = random.choice(NON_STANDARD_UNITS)
                f_unit = bad_unit
                f_net_quantity = qty.replace(standard_unit, bad_unit)
                violation_labels.append(f"LM-PC-004: Non-standard unit '{bad_unit}'")
            elif viol == "mrp_no_tax_phrase":
                f_mrp = f"Rs. {mrp}"  # Missing inclusive of all taxes
                violation_labels.append("LM-PC-005: MRP missing 'inclusive of all taxes' phrase")
            elif viol == "no_packing_date":
                f_packing_date = ""
                violation_labels.append("LM-PC-006: Missing packing/manufacturing date")
            elif viol == "no_consumer_care":
                f_consumer_care_phone = ""
                f_consumer_care_email = ""
                violation_labels.append("LM-PC-007: Missing consumer care contact")
            elif viol == "no_country_of_origin":
                f_country_of_origin = ""
                violation_labels.append("LM-PC-008: Missing country of origin")
            elif viol == "no_usp":
                f_usp = ""
                violation_labels.append("LM-PC-009: Missing unit sale price")
            elif viol == "poor_readability":
                f_readability = "POOR"
                violation_labels.append("LM-PC-010: Poor label readability")

    compliance_status = "COMPLIANT" if (is_compliant and not violation_labels) else "NON_COMPLIANT"
    # Compliance score (0-100)
    deduction_per_critical = 20
    deduction_per_high = 15
    deduction_per_medium = 10

    score = 100
    for v in violation_labels:
        rule = v.split(":")[0].strip()
        if rule in ["LM-PC-001", "LM-PC-004", "LM-PC-005"]:
            score -= deduction_per_critical
        elif rule in ["LM-PC-002", "LM-PC-003", "LM-PC-006", "LM-PC-007", "LM-PC-008"]:
            score -= deduction_per_high
        else:
            score -= deduction_per_medium
    score = max(0, score)

    if is_compliant and not violation_labels:
        score = 100

    return {
        "sample_id": f"SIH26034-{idx:05d}",
        "product_name": f_product_name,
        "manufacturer_name": f_manufacturer,
        "manufacturer_address": f_address,
        "net_quantity": f_net_quantity,
        "unit_of_measurement": f_unit,
        "mrp_declaration": f_mrp,
        "mrp_value_rupees": f_mrp_raw,
        "packing_date": f_packing_date,
        "consumer_care_phone": f_consumer_care_phone,
        "consumer_care_email": f_consumer_care_email,
        "country_of_origin": f_country_of_origin,
        "unit_sale_price": f_usp,
        "label_readability": f_readability,
        "product_category": category,
        "compliance_status": compliance_status,
        "compliance_score": score,
        "violations_count": len(violation_labels),
        "violation_labels": "; ".join(violation_labels) if violation_labels else "None",
        "violations_detail": violation_labels
    }

# ─── Generate Samples ─────────────────────────────────────────────────────────
all_samples = []

# Force ~50% compliant in train
for i in range(1, 101):
    all_samples.append(make_sample(i, force_compliant=True))

# Non-compliant with specific single-violation scenarios for each violation type
for idx, viol_key in enumerate(VIOLATION_SCENARIOS.keys(), 101):
    for repeat in range(10):
        s = make_sample(idx * 10 + repeat, force_compliant=False, injected_violations=[viol_key])
        all_samples.append(s)

# Mixed multi-violation non-compliant
for i in range(201, 261):
    all_samples.append(make_sample(i, force_compliant=False))

random.shuffle(all_samples)

# Reassign IDs after shuffle
for i, s in enumerate(all_samples, 1):
    s["sample_id"] = f"SIH26034-{i:05d}"

# 77% train / 23% test
train_cutoff = int(len(all_samples) * 0.77)
train_data = all_samples[:train_cutoff]
test_data = all_samples[train_cutoff:]

CSV_FIELDS = [
    "sample_id", "product_name", "manufacturer_name", "manufacturer_address",
    "net_quantity", "unit_of_measurement", "mrp_declaration", "mrp_value_rupees",
    "packing_date", "consumer_care_phone", "consumer_care_email",
    "country_of_origin", "unit_sale_price", "label_readability",
    "product_category", "compliance_status", "compliance_score",
    "violations_count", "violation_labels"
]

def write_csv(filename, data):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for row in data:
            flat = {k: row[k] for k in CSV_FIELDS}
            writer.writerow(flat)

def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

write_csv("dataset/train.csv", train_data)
write_csv("dataset/test.csv", test_data)
write_json("dataset/train.json", train_data)
write_json("dataset/test.json", test_data)

# ─── Dataset Card ─────────────────────────────────────────────────────────────
train_compliant = sum(1 for s in train_data if s["compliance_status"] == "COMPLIANT")
test_compliant = sum(1 for s in test_data if s["compliance_status"] == "COMPLIANT")
train_nc = len(train_data) - train_compliant
test_nc = len(test_data) - test_compliant

card = f"""# Legal Metrology Compliance Dataset (SIH26034)
**Smart India Hackathon 2026 | Problem Statement: SIH26034**
**Standard:** Legal Metrology (Packaged Commodities) Rules, 2011

## Dataset Summary
| Split | Total | Compliant | Non-Compliant |
|-------|-------|-----------|---------------|
| Train | {len(train_data)} | {train_compliant} | {train_nc} |
| Test  | {len(test_data)} | {test_compliant} | {test_nc} |
| **Total** | **{len(all_samples)}** | **{train_compliant+test_compliant}** | **{train_nc+test_nc}** |

## Features (19 columns)
| Column | Type | Description |
|--------|------|-------------|
| sample_id | string | Unique dataset record ID |
| product_name | string | Generic/common product name on pack |
| manufacturer_name | string | Name of manufacturer/packer/importer |
| manufacturer_address | string | Complete registered factory address |
| net_quantity | string | Declared net quantity with unit |
| unit_of_measurement | string | SI unit (g, kg, ml, l, N, m) or non-standard |
| mrp_declaration | string | Full MRP declaration text on label |
| mrp_value_rupees | float | Numeric MRP value in INR |
| packing_date | string | Month/Year of manufacture (MM/YYYY) |
| consumer_care_phone | string | Consumer helpline toll-free number |
| consumer_care_email | string | Consumer grievance email |
| country_of_origin | string | Country of origin declaration |
| unit_sale_price | string | Unit sale price declaration |
| label_readability | string | GOOD / MODERATE / POOR |
| product_category | string | Food/Personal Care/Cleaning/etc. |
| compliance_status | string | **COMPLIANT** or **NON_COMPLIANT** (target label) |
| compliance_score | int | 0-100 weighted compliance score |
| violations_count | int | Number of violations detected |
| violation_labels | string | Semicolon-separated rule violation codes |

## Violation Types Covered
| Rule Code | Category | Violation Type |
|-----------|----------|----------------|
| LM-PC-001 | Product Identification | Missing generic product name |
| LM-PC-002 | Manufacturer Details | Missing manufacturer name |
| LM-PC-003 | Manufacturer Address | Incomplete address |
| LM-PC-004 | Net Quantity & Units | Non-standard unit (gms, kilos, lts) |
| LM-PC-005 | MRP Declaration | MRP without 'inclusive of all taxes' |
| LM-PC-006 | Date of Packing | Missing manufacturing/packing date |
| LM-PC-007 | Consumer Care | Missing helpline phone/email |
| LM-PC-008 | Country of Origin | Missing origin declaration |
| LM-PC-009 | Unit Sale Price | Missing USP |
| LM-PC-010 | Font Readability | Poor label readability |

## Legal Reference
- Legal Metrology (Packaged Commodities) Rules, 2011
- Ministry of Consumer Affairs, Food & Public Distribution, Government of India
- Gazette Amendments including Rule 6(11) Amendment 2021 (USP)
- Consumer Protection (E-Commerce) Rules, 2020

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

with open("dataset/dataset_info.md", "w", encoding="utf-8") as f:
    f.write(card)

print("=" * 60)
print("  LEGAL METROLOGY DATASET GENERATION COMPLETE")
print("=" * 60)
print(f"  Train: {len(train_data)} samples ({train_compliant} compliant, {train_nc} non-compliant)")
print(f"  Test:  {len(test_data)} samples ({test_compliant} compliant, {test_nc} non-compliant)")
print(f"  Total: {len(all_samples)} samples")
print("  Files saved to: backend/dataset/")
print("    - dataset/train.csv")
print("    - dataset/test.csv")
print("    - dataset/train.json")
print("    - dataset/test.json")
print("    - dataset/dataset_info.md")
print("=" * 60)
