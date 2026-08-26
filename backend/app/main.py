import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import UPLOAD_DIR, DEMO_ASSETS_DIR, REPORTS_DIR
from app.database.connection import engine, Base, SessionLocal
from app.database.seed_data import seed_database
from app.routers import auth, products, inspections, rules, ecommerce, dashboard, reports

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize seed data
db = SessionLocal()
try:
    seed_database(db)
finally:
    db.close()

app = FastAPI(
    title="Legal Metrology Compliance System (SIH26034)",
    description="Software System to check compliance of Packaged Commodities under Legal Metrology (Packaged Commodities) Rules, 2011 by scanning products, images and labels.",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directories
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")
app.mount("/demo_assets", StaticFiles(directory=str(DEMO_ASSETS_DIR)), name="demo_assets")
app.mount("/reports", StaticFiles(directory=str(REPORTS_DIR)), name="reports")

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(inspections.router)
app.include_router(rules.router)
app.include_router(ecommerce.router)
app.include_router(dashboard.router)
app.include_router(reports.router)

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "Legal Metrology Compliance Enforcement Engine",
        "standard": "Legal Metrology (Packaged Commodities) Rules, 2011",
        "prototype_version": "SIH26034-v1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
