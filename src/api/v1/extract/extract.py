import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from services import extract as service_extract

extract_router = APIRouter(prefix="/extract")


@extract_router.post("")
async def extract_document(file: UploadFile = File(...)):
    allowed_extensions = {".pdf", ".jpg", ".jpeg", ".png", ".tiff", ".bmp"}
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}",
        )

    content = await file.read()
    return await service_extract.extract_document(
        content, file.content_type or "application/octet-stream"
    )
