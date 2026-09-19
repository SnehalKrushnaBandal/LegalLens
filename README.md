# 🔍 LegalLens — AI-Powered Legal Metrology Compliance System

> **SIH 2026 — Problem Statement SIH26034**

An AI-assisted Legal Metrology compliance system designed to help enforcement officers inspect packaged commodities by analyzing product images, extracting mandatory declarations through OCR, checking compliance against configurable rules, and generating inspection reports.

---

## 🚀 Key Features

- 📸 **AI-Assisted Product Scanning**
  - Upload packaged commodity images for analysis.
  - OCR-based extraction of product declarations.

- 🔎 **Automated Compliance Verification**
  - Checks mandatory declarations against configurable Legal Metrology rules.
  - Detects missing or invalid declarations.
  - Provides compliance status and violation details.

- 📦 **Product Repository**
  - Manage and review packaged commodity information.
  - Preloaded demo products for testing and demonstration.

- 🌐 **E-Commerce Listing Verification**
  - Compare online product information with physical package data.
  - Detect discrepancies in MRP, quantity, country of origin, etc.

- 📊 **Compliance Dashboard**
  - View inspection statistics, compliance scores, violations, and trends.

- 📄 **Automated PDF Reports**
  - Generate structured inspection reports containing inspection details, violations, compliance information, and officer verification.

- ⚙️ **Configurable Rule Engine**
  - Legal Metrology compliance rules can be managed and updated through the application.

- 🔐 **Officer Authentication**
  - JWT-based authentication with role-based access.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Vite, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn |
| Database | SQLite, Supabase |
| OCR / Image Processing | Google Vision , OpenCV |
| PDF Generation | ReportLab |
| Authentication | JWT |
| Data Visualization | Recharts |
| AI / ML | Gemini, YOLO |

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │     React Frontend  │
                    │   Vite + Tailwind   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI API     │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
        OCR / Vision      Rule Engine       E-Commerce
        Processing        & Validation       Verification
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ SQLite + SQLAlchemy │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   PDF Report        │
                    │     Generation      │
                    └─────────────────────┘