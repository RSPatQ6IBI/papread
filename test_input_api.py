"""
test_api.py  —  Test the PDF Upload API
========================================
Make sure the API server is running first:
    uvicorn main:app --reload

Then run:
    python test_api.py
"""

import requests

BASE_URL = "http://localhost:8000"
PDF_PATH = "sample.pdf"          # ← replace with a real PDF file path


# ── Test 1: Single PDF ─────────────────────────────────────────
def test_single_upload():
    print("\n── Test 1: Single PDF Upload ──")
    with open(PDF_PATH, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/upload/pdf",
            files={"file": (PDF_PATH, f, "application/pdf")}
        )
    print(f"Status : {response.status_code}")
    print(f"Response: {response.json()}")


# ── Test 2: Multiple PDFs ──────────────────────────────────────
def test_multiple_upload():
    print("\n── Test 2: Multiple PDF Upload ──")
    files = [
        ("files", (PDF_PATH, open(PDF_PATH, "rb"), "application/pdf")),
        ("files", (PDF_PATH, open(PDF_PATH, "rb"), "application/pdf")),
    ]
    response = requests.post(f"{BASE_URL}/upload/pdfs", files=files)
    print(f"Status : {response.status_code}")
    print(f"Response: {response.json()}")


# ── Test 3: Health check ───────────────────────────────────────
def test_health():
    print("\n── Test 3: Health Check ──")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status : {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    test_health()
    test_single_upload()
    test_multiple_upload()