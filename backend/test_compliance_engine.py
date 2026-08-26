import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def test_full_system():
    print("\n" + "=" * 60)
    print("  RUNNING LEGAL METROLOGY (SIH26034) AUTOMATED TEST SUITE")
    print("=" * 60)

    # 1. Health check
    print("\n[TEST 1] Checking API Health...")
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print(" [OK] Health Check Passed:", r.json().get("service"))

    # 2. Login
    print("\n[TEST 2] Testing Officer Login (LMO001)...")
    r = requests.post(f"{BASE_URL}/auth/login", json={"officer_id": "LMO001", "password": "admin123"})
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(" [OK] Officer Logged in successfully:", r.json()["officer"]["full_name"])

    # 3. Dashboard Stats
    print("\n[TEST 3] Fetching Dashboard Analytics...")
    r = requests.get(f"{BASE_URL}/dashboard/statistics", headers=headers)
    assert r.status_code == 200, f"Dashboard stats failed: {r.text}"
    stats = r.json()
    print(f" [OK] Total Inspections: {stats['total_inspections']}, Compliant: {stats['compliant_products']}, Non-Compliant: {stats['non_compliant_products']}")

    # 4. Product Scanning & OCR Analysis (Demo Basmati Rice)
    print("\n[TEST 4] Scanning Product (Basmati Rice)...")
    r = requests.post(f"{BASE_URL}/products/upload", data={"demo_product_id": "basmati_rice"}, headers=headers)
    assert r.status_code == 200, f"Upload failed: {r.text}"
    upload_data = r.json()
    print(" [OK] Uploaded & Preprocessed:", upload_data["product_name"])

    r = requests.post(f"{BASE_URL}/products/analyze", data={
        "raw_image_path": upload_data["raw_image_path"],
        "demo_product_id": "basmati_rice",
        "product_name": upload_data["product_name"],
        "category": upload_data["category"]
    }, headers=headers)
    assert r.status_code == 200, f"Analyze failed: {r.text}"
    analysis = r.json()
    print(f" [OK] Extracted {len(analysis['declarations'])} mandatory declarations and {len(analysis['evidence_items'])} evidence zones.")

    # 5. Create Inspection & Evaluate Rule Engine
    print("\n[TEST 5] Executing Legal Metrology Rule Engine...")
    r = requests.post(f"{BASE_URL}/inspections", json={
        "raw_image_path": upload_data["raw_image_path"],
        "evidence_image_path": analysis["evidence_image_path"],
        "product_name": upload_data["product_name"],
        "category": upload_data["category"],
        "declarations": analysis["declarations"],
        "evidence_items": analysis["evidence_items"],
        "demo_product_id": "basmati_rice",
        "remarks": "Automated verification test."
    }, headers=headers)
    assert r.status_code == 200, f"Inspection creation failed: {r.text}"
    insp_res = r.json()
    print(f" [OK] Compliance Status: {insp_res['compliance_status']}, Score: {insp_res['compliance_score']}/100, Violations: {len(insp_res['violations'])}")

    # 6. Generate Official PDF Report
    print("\n[TEST 6] Generating Official PDF Inspection Report...")
    r = requests.post(f"{BASE_URL}/reports/{insp_res['id']}/generate", headers=headers)
    assert r.status_code == 200, f"Report generation failed: {r.text}"
    rep_res = r.json()
    print(" [OK] Generated PDF Report:", rep_res["filename"])

    # 7. E-Commerce Dual Verification Test (MRP Discrepancy)
    print("\n[TEST 7] Testing E-Commerce Listing vs Package Verification...")
    r = requests.post(f"{BASE_URL}/ecommerce/verify", json={
        "platform_name": "Amazon India",
        "listing_title": "Basmati Rice 5kg Pack",
        "listing_mrp": 720.0, # Inflated MRP!
        "listing_net_quantity": "5 kg",
        "package_mrp": 650.0, # Physical package MRP
        "package_net_quantity": "5 kg"
    }, headers=headers)
    assert r.status_code == 200, f"E-commerce verify failed: {r.text}"
    ecomm = r.json()
    print(f" [OK] E-Commerce Status: {ecomm['status']}, Discrepancies Flagged: {len(ecomm['discrepancies'])}")

    # 8. Rules Repository
    print("\n[TEST 8] Checking Rule Repository...")
    r = requests.get(f"{BASE_URL}/rules", headers=headers)
    assert r.status_code == 200, f"Rules fetch failed: {r.text}"
    rules = r.json()
    print(f" [OK] Loaded {len(rules)} Legal Metrology Rules.")

    print("\n" + "=" * 60)
    print("  ALL 8 TEST SUITES PASSED PERFECTLY!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    test_full_system()
