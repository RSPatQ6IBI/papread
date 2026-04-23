	"""
main.py  —  PDF Upload API
==========================
Accepts one or more PDF files from a client and returns detailed file size info.

Run:
    pip install fastapi uvicorn python-multipart pypdf
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Docs available at:
    http://localhost:8000/docs   (Swagger UI)
    http://localhost:8000/redoc  (ReDoc)
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pypdf import PdfReader
from io import BytesIO
from typing import List
import math

app = FastAPI(
    title="PDF File Info API",
    description="Upload PDF files and get back file size and metadata.",
    version="1.0.0",
)


# ── Helper: bytes → human-readable size ────────────────────────
def human_readable_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0 B"
    units = ["B", "KB", "MB", "GB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    i = min(i, len(units) - 1)
    p = math.pow(1024, i)
    return f"{size_bytes / p:.2f} {units[i]}"


# ── Helper: validate file is a PDF ─────────────────────────────
def validate_pdf(content: bytes, filename: str) -> None:
    if not content.startswith(b"%PDF"):
        raise HTTPException(
            status_code=400,
            detail=f"'{filename}' does not appear to be a valid PDF file."
        )


# =============================================================
# ROUTE 1: Single PDF upload
# =============================================================
@app.post("/upload/pdf", summary="Upload a single PDF and get its file size")
async def upload_single_pdf(file: UploadFile = File(...)):
    """
    Upload a single PDF file.

    Returns:
    - filename
    - size in bytes
    - human-readable size (KB / MB)
    - number of pages
    - PDF metadata (title, author, etc.)
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    content = await file.read()
    validate_pdf(content, file.filename)

    size_bytes = len(content)

    # Extract page count and metadata via pypdf
    try:
        reader = PdfReader(BytesIO(content))
        num_pages = len(reader.pages)
        meta      = reader.metadata or {}
        metadata  = {
            "title"   : meta.get("/Title",    None),
            "author"  : meta.get("/Author",   None),
            "subject" : meta.get("/Subject",  None),
            "creator" : meta.get("/Creator",  None),
            "producer": meta.get("/Producer", None),
        }
    except Exception:
        num_pages = None
        metadata  = {}

    return JSONResponse(content={
        "filename"          : file.filename,
        "content_type"      : file.content_type,
        "size_bytes"        : size_bytes,
        "size_kb"           : round(size_bytes / 1024, 2),
        "size_mb"           : round(size_bytes / (1024 ** 2), 4),
        "size_human_readable": human_readable_size(size_bytes),
        "num_pages"         : num_pages,
        "metadata"          : metadata,
    })


# =============================================================
# ROUTE 2: Multiple PDF upload
# =============================================================
@app.post("/upload/pdfs", summary="Upload multiple PDFs and get file sizes")
async def upload_multiple_pdfs(files: List[UploadFile] = File(...)):
    """
    Upload multiple PDF files at once.

    Returns a list of results for each file, plus a summary with total size.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files were uploaded.")

    results     = []
    total_bytes = 0

    for file in files:
        if not file.filename.lower().endswith(".pdf"):
            results.append({
                "filename": file.filename,
                "error"   : "Skipped — not a PDF file."
            })
            continue

        content = await file.read()

        try:
            validate_pdf(content, file.filename)
        except HTTPException as e:
            results.append({"filename": file.filename, "error": e.detail})
            continue

        size_bytes   = len(content)
        total_bytes += size_bytes

        try:
            reader    = PdfReader(BytesIO(content))
            num_pages = len(reader.pages)
        except Exception:
            num_pages = None

        results.append({
            "filename"           : file.filename,
            "size_bytes"         : size_bytes,
            "size_kb"            : round(size_bytes / 1024, 2),
            "size_mb"            : round(size_bytes / (1024 ** 2), 4),
            "size_human_readable": human_readable_size(size_bytes),
            "num_pages"          : num_pages,
        })

    return JSONResponse(content={
        "files": results,
        "summary": {
            "total_files_received" : len(files),
            "total_files_processed": sum(1 for r in results if "error" not in r),
            "total_size_bytes"     : total_bytes,
            "total_size_human"     : human_readable_size(total_bytes),
        }
    })


# =============================================================
# ROUTE 3: Health check
# =============================================================
@app.get("/health", summary="Health check")
def health():
    return {"status": "ok", "message": "PDF API is running."}