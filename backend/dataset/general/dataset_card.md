# General Legal Metrology Compliance Dataset
### SIH26034 — Smart India Hackathon 2026
**Standard:** Legal Metrology (Packaged Commodities) Rules, 2011  
**Scope:** Any packaged commodity sold in India  
**Generated:** 2026-08-27 07:25:55

---

## Overview
A product-agnostic, general-purpose labeled dataset for training, evaluating, and benchmarking
automated Legal Metrology compliance checking systems. Covers 70 distinct product
types across 13 industry categories, with all 10 statutory rule violation types
systematically represented.

---

## Dataset Splits

| Split | Total | COMPLIANT | NON_COMPLIANT |
|-------|-------|-----------|---------------|
| **Train** | 510 | 188 | 322 |
| **Validation** | 73 | 21 | 52 |
| **Test** | 147 | 51 | 96 |
| **Total** | **730** | **260** | **470** |

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
| Personal Care | 149 |
| Household | 77 |
| Beverages | 60 |
| Health | 57 |
| Dairy | 54 |
| Snacks & Bakery | 51 |
| Spices | 50 |
| Staples | 45 |
| Condiments | 42 |
| Edible Oil | 40 |
| Stationery | 39 |
| Pulses | 36 |
| Agriculture | 30 |

---

## Violation Rule Coverage
| Rule Code | Category | Severity | Samples |
|-----------|----------|----------|---------|
| LM-PC-001 | Product Identification | CRITICAL | 95 |
| LM-PC-002 | Manufacturer Details | HIGH | 101 |
| LM-PC-003 | Manufacturer Address | HIGH | 82 |
| LM-PC-004 | Net Quantity & Units | CRITICAL | 82 |
| LM-PC-005 | MRP Declaration | CRITICAL | 100 |
| LM-PC-006 | Date of Packing | HIGH | 95 |
| LM-PC-007 | Consumer Care Details | HIGH | 85 |
| LM-PC-008 | Country of Origin | HIGH | 94 |
| LM-PC-009 | Unit Sale Price (USP) | MEDIUM | 96 |
| LM-PC-010 | Font Readability | MEDIUM | 65 |

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
