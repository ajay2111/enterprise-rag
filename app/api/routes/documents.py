from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"]
)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    allowed_types = {
        "application/pdf"
    }

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    file_id = str(uuid.uuid4())

    file_path = (
        UPLOAD_DIR /
        f"{file_id}.pdf"
    )

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "path": str(file_path),
        "status": "UPLOADED"
    }