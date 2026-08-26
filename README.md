# Legal Metrology Compliance Enforcement System (SIH 2026 — SIH26034)

> **Software System to check compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by scanning products, images and labels.**

---

## 🏛️ Executive Summary & Value Proposition

In traditional Legal Metrology enforcement, inspecting officers manually examine packaged goods in retail markets, cross-verify multiple statutory declarations, consult rulebooks, write manual inspection memos, and maintain physical files. This process is time-consuming, prone to human oversight, and difficult to scale across millions of consumer packaged commodities and e-commerce listings.

**The StegoAI Legal Metrology Compliance System** provides an interactive, AI-assisted screening workflow that scans product packaging, automatically extracts mandatory statutory declarations via OCR, validates them against a configurable Legal Metrology Rule Engine, flags violations with visual bounding box evidence, calculates weighted compliance scores, verifies digital e-commerce listings, and generates official Government of India-style inspection reports in PDF.

```
BEFORE (Manual Enforcement):
Manual Store Inspection ➔ Officer Reads Package ➔ Manual Cross-Checking ➔ Paper Rulebook Lookup ➔ Manual Memo Writing ➔ Physical Record Filing

AFTER (AI-Assisted Legal Metrology System):
Scan / Capture Package ➔ Image Preprocessing & OCR ➔ Mandatory Declaration Extraction ➔ Configurable Rule Engine ➔ Violation Detection & Evidence Bounding Boxes ➔ Compliance Score ➔ Officer Review / Edit ➔ Automated Official PDF Report ➔ Real-Time Analytics Dashboard
```

> [!IMPORTANT]
> **Legal Disclaimer:** This prototype is an AI-assisted compliance screening system designed to aid enforcement officers. The AI findings are advisory; the final legal determination and prosecution/compounding decisions under the Legal Metrology Act, 2009 rest solely with authorized Legal Metrology Officers.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend UI/UX** | React.js (v19), Vite, Tailwind CSS | High-performance, responsive government portal with official aesthetics |
| **Data Visualizations**| Recharts, Lucide React Icons | Interactive compliance donut charts, violation category bar charts, trend lines |
| **Backend API** | Python 3.11, FastAPI, Uvicorn | High-speed asynchronous REST API with modular routers |
| **Database & ORM** | SQLite, SQLAlchemy ORM | Lightweight relational storage for rules, products, inspections, violations & audit logs |
| **AI / OCR Vision** | Pillow (PIL), OpenCV, Modular OCR Engine | Image preprocessing, text detection, entity parsing, visual bounding box generation |
| **PDF Reporting** | ReportLab | Generation of official Government of India compliance inspection certificates |
| **Security & Auth** | JWT (PyJWT), Bcrypt password hashing | Role-based officer authentication and tamper-evident audit logging |

---

## 🚀 Quick Start Guide (Running Locally)

### 1. Prerequisites
- **Python 3.10+** (Python 3.11 recommended)
- **Node.js 18+** & **npm**

---

### 2. Backend Setup & Startup

```bash
# Navigate to the backend directory
cd backend

# Install Python backend dependencies
pip install -r requirements.txt
# (Includes fastapi, uvicorn, sqlalchemy, reportlab, pillow, pyjwt, bcrypt, passlib)

# Start the FastAPI backend server (Runs on port 8000)
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Backend API will be live at:
- **API Base:** `http://127.0.0.1:8000`
- **Interactive OpenAPI / Swagger Docs:** `http://127.0.0.1:8000/docs`

---

### 3. Frontend Setup & Startup

```bash
# In project root directory
npm install

# Start the Vite development server (Runs on port 5173)
npm run dev
```

Open your browser and navigate to: `http://localhost:5173`

---

## 🔑 Demo Officer Credentials

| Role | Officer ID | Password | Access Level |
|---|---|---|---|
| **Senior Legal Metrology Officer** | `LMO001` | `admin123` | Full Inspection, Rule Config, PDF Generation, Auditing |

*(A 1-click **"Auto Fill"** button is provided on the login page for instant hackathon evaluation).*

---

## 📦 Preloaded Demo Products Dataset

The system includes 6 realistic Indian packaged commodities pre-configured to demonstrate diverse Legal Metrology compliance outcomes:

| # | Product Name | Category | Stamped Net Qty | Stamped MRP | Compliance Outcome | Violated Statutory Rule |
|---|---|---|---|---|---|---|
| **1** | **Premium Basmati Rice** | Packaged Food | 5 kg | ₹650.00 (Incl. of all taxes) | 🟢 **COMPLIANT (98%)** | All mandatory declarations valid |
| **2** | **Butter Delight Biscuits** | Bakery | 200 g | ₹35.00 (Incl. of all taxes) | 🔴 **NON-COMPLIANT (78%)** | Missing Consumer Care Helpline & Email (Rule 6(1)(n)) |
| **3** | **Pure Mustard Cooking Oil** | Edible Oils | 1 L | ₹195.00 | 🔴 **NON-COMPLIANT (72%)** | Missing mandatory "inclusive of all taxes" declaration (Rule 6(1)(e)) |
| **4** | **Active Clean Detergent Powder**| Household | 1000 GMS | ₹140.00 (Incl. of all taxes) | 🔴 **NON-COMPLIANT (80%)** | Non-standard unit symbol "GMS" (Rule 12) & Missing Unit Sale Price |
| **5** | **Herbal Glow Shampoo** | Cosmetics | 180 ml | ₹120.00 (Incl. of all taxes) | 🔴 **NON-COMPLIANT (68%)** | Incomplete manufacturer address - missing city/PIN (Rule 6(1)(b)) |
| **6** | **Royal Garam Masala** | Spices | 100 g | ₹75.00 (Incl. of all taxes) | 🟡 **MANUAL VERIFICATION (85%)** | Packing date stamp blurred / ambiguous month format (Rule 6(1)(d)) |

---

## ⚙️ Configurable Rule Engine (Legal Metrology Rules, 2011)

The backend features a dynamic, database-persisted rule engine where parameters can be toggled, adjusted, or extended as new Gazette amendments are notified:

1. **LM-PC-001 (Rule 6(1)(a)):** Mandatory prominent declaration of the generic/common name of the commodity on the principal display panel.
2. **LM-PC-002 (Rule 6(1)(b)):** Name of Manufacturer, Packer, or Importer.
3. **LM-PC-003 (Rule 6(1)(b)):** Complete registered factory address including street, city, state, and PIN code for consumer traceability.
4. **LM-PC-004 (Rule 6(1)(c) & Rule 12):** Declaration of Net Quantity in standard SI units (`g`, `kg`, `ml`, `l`, `N`) and prohibition of non-standard units (e.g. `gms`, `kilos`, `pkts`).
5. **LM-PC-005 (Rule 6(1)(e)):** Maximum Retail Price (MRP) in ₹ inclusive of all taxes (`MRP Rs. ... (inclusive of all taxes)`).
6. **LM-PC-006 (Rule 6(1)(d)):** Month and Year of Manufacture / Packing / Import.
7. **LM-PC-007 (Rule 6(1)(n)):** Consumer Care Cell details (Name, Telephone Helpline Number, and Email Address).
8. **LM-PC-008 (Rule 6(10)):** Mandatory declaration of Country of Origin on packaging and e-commerce listings.
9. **LM-PC-009 (Rule 6(11)):** Unit Sale Price (USP) per unit/g/kg/ml for retail packaged commodities.
10. **LM-PC-010 (Rule 7 & Schedule II):** Minimum numeral and letter height readability estimation.

---

## 🌐 E-Commerce Marketplace Dual-Verification (Rule 6(11))

The system features a specialized **Online Listing Inspector** that compares physical package ground truth against digital marketplace listings (Amazon, Flipkart, Blinkit, Zepto, Meesho):
- **Overcharging Detection:** Flags listings where the declared online MRP exceeds the physical packaging MRP (e.g. Package MRP ₹650 vs Listing MRP ₹720).
- **Net Quantity Discrepancy:** Identifies misleading online quantity claims (e.g. Online says 250g, Package contains 200g).
- **Missing Origin:** Identifies listings lacking mandatory Country of Origin disclosure.
- **Enforcement Directives:** Recommends statutory compounding notices under Section 36 of the Legal Metrology Act, 2009.

---

## 📄 Official PDF Inspection Report

Generated via **ReportLab**, the downloadable PDF report includes:
- Official Government of India & Ministry of Consumer Affairs header
- Unique Inspection ID (`INSP-2026-XXXXX`), Officer ID, Timestamp, Geolocation
- Overall Compliance Score Meter & Weighted Category Breakdown
- Itemized Declarations Table with detection status, confidence, and font readability metrics
- Itemized Violations Table with statutory rule references, severity, and legal requirements
- Officer Verification & Digital Stamping block with legal disclaimers.

---

## 🏗️ Project Architecture & File Tree

```
c:\StegoAI-VI_MPL\
├── backend/
│   ├── app/
│   │   ├── config.py                # Environment, JWT secrets, storage paths
│   │   ├── main.py                  # FastAPI app entrypoint, CORS, static mounts
│   │   ├── database/
│   │   │   ├── connection.py        # SQLite engine & session maker
│   │   │   ├── models.py            # SQLAlchemy schema models
│   │   │   └── seed_data.py         # Seed dataset for demo products & rules
│   │   ├── schemas/
│   │   │   └── schemas.py           # Pydantic request/response schemas
│   │   ├── services/
│   │   │   ├── auth_service.py      # JWT token management & bcrypt password hashing
│   │   │   ├── ocr_service.py       # Modular OCR, bounding boxes & synthetic image generator
│   │   │   ├── rule_engine.py       # Configurable Legal Metrology rule engine & scoring
│   │   │   ├── pdf_service.py       # ReportLab PDF report generation
│   │   │   └── ecommerce_service.py # E-commerce listing verification
│   │   └── routers/
│   │       ├── auth.py              # Login & authentication routes
│   │       ├── products.py          # Upload, analyze & product repository
│   │       ├── inspections.py       # Rule check execution, verification & violation updates
│   │       ├── rules.py             # Configurable rule CRUD & toggle
│   │       ├── ecommerce.py         # E-commerce listing discrepancy audit
│   │       ├── dashboard.py         # Real-time analytics & chart statistics
│   │       └── reports.py           # PDF report generation & download
│   ├── demo_assets/                 # Synthetic high-resolution packaged commodity samples
│   ├── uploads/                     # Secure upload storage
│   └── requirements.txt
│
├── src/
│   ├── components/
│   │   ├── Navbar.jsx               # Government portal topbar with officer badge
│   │   ├── Sidebar.jsx              # Module navigation with authority disclaimer
│   │   ├── BoundingBoxViewer.jsx    # Interactive visual evidence viewer
│   │   ├── ComplianceScoreGauge.jsx # Circular score meter & category progress bars
│   │   ├── ViolationCard.jsx        # Rich violation finding card with officer actions
│   │   ├── ProcessingTimeline.jsx   # 5-stage OCR & rule evaluation visual timeline
│   │   └── ReadabilityBadge.jsx     # Readability metric with statutory measurement tooltip
│   ├── pages/
│   │   ├── LoginPage.jsx            # Secure officer authentication screen
│   │   ├── DashboardPage.jsx        # Recharts dashboard with KPIs & trendlines
│   │   ├── ScanProductPage.jsx      # Product scan, editable OCR & compliance check
│   │   ├── InspectionDetailsPage.jsx# Complete audit view & digital verification
│   │   ├── OnlineListingPage.jsx    # E-Commerce listing vs physical package auditor
│   │   ├── InspectionHistoryPage.jsx# Filterable & searchable statutory audit logs
│   │   ├── ProductRepositoryPage.jsx# Packaged goods catalog
│   │   └── RuleRepositoryPage.jsx   # Configurable Rule Engine management
│   ├── services/
│   │   └── api.js                   # Fetch API client with JWT interceptors
│   ├── App.jsx                      # React Router & protected layout
│   ├── index.css                    # Tailwind CSS styles & custom scrollbars
│   └── main.jsx
│
├── reports/                         # Generated official PDF inspection reports
└── README.md
```

---

## 🔮 Limitations & Future Enhancements

1. **Physical Calibrated Dimensions:** The prototype estimates font height in pixels from digital images; integration with depth-sensing mobile cameras (LiDAR/Stereo) will enable precise physical millimeter measurement for Rule 7 font compliance.
2. **Multi-Lingual OCR:** Expansion to regional Indian languages (Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati) for regional packaged commodities.
3. **Automated E-Commerce Scraping:** Integration with real-time web crawlers to continuously audit millions of marketplace product listings against the central Legal Metrology repository.
4. **Barcode / QR Code Barcode Cross-Verification:** Automatic decoding of GS1 / EAN barcodes to cross-check manufacturer registration with official government databases.
