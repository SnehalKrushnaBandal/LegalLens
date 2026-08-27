# Legal Metrology Compliance Dataset (SIH26034)
**Smart India Hackathon 2026 | Problem Statement: SIH26034**
**Standard:** Legal Metrology (Packaged Commodities) Rules, 2011

## Dataset Summary
| Split | Total | Compliant | Non-Compliant |
|-------|-------|-----------|---------------|
| Train | 200 | 105 | 95 |
| Test  | 60 | 25 | 35 |
| **Total** | **260** | **130** | **130** |

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

Generated: 2026-08-27 07:19:54
