"""Secure file storage service for logos, PDFs, and attachments.
"""
import os
import shutil
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import BinaryIO, Tuple
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import ValidationException

# Allowed MIME types for uploads
ALLOWED_LOGO_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_LOGO_SIZE = 5 * 1024 * 1024  # 5 MB

class FileStorageService:
    """Handles safe file storage outside the web root."""
    
    @staticmethod
    def _get_storage_path() -> Path:
        path = Path(settings.storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def _safe_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        name = os.path.basename(filename)
        name = "".join(c for c in name if c.isalnum() or c in "._-")
        if not name:
            name = "file"
        return name
    
    @staticmethod
    def _validate_image(upload: UploadFile) -> Tuple[str, int]:
        """Validate uploaded image. Returns (mime_type, size)."""
        content_type = upload.content_type or ""
        if content_type not in ALLOWED_LOGO_TYPES:
            raise ValidationException(
                f"Invalid file type: {content_type}. Allowed: PNG, JPEG, WEBP"
            )
        
        # Read first chunk to verify it is actually an image
        header = upload.file.read(8192)
        upload.file.seek(0)
        
        # Basic magic number checks
        if content_type == "image/png" and not header.startswith(b"\\x89PNG"):
            raise ValidationException("File does not appear to be a valid PNG")
        if content_type == "image/jpeg" and not header.startswith(b"\\xff\\xd8"):
            raise ValidationException("File does not appear to be a valid JPEG")
        if content_type == "image/webp" and not header.startswith(b"RIFF"):
            raise ValidationException("File does not appear to be a valid WEBP")
        
        # Check size
        upload.file.seek(0, os.SEEK_END)
        size = upload.file.tell()
        upload.file.seek(0)
        if size > MAX_LOGO_SIZE:
            raise ValidationException(f"File too large. Max size: {MAX_LOGO_SIZE // 1024 // 1024}MB")
        
        return content_type, size
    
    @classmethod
    def save_company_logo(cls, company_id: str, upload: UploadFile) -> dict:
        """Save company logo to storage.
        
        Returns metadata dict with path, mime_type, size.
        """
        mime_type, size = cls._validate_image(upload)
        
        storage = cls._get_storage_path()
        logo_dir = storage / "company-logos" / company_id
        logo_dir.mkdir(parents=True, exist_ok=True)
        
        ext = mimetypes.guess_extension(mime_type) or ".png"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"logo_{timestamp}{ext}"
        safe_name = cls._safe_filename(filename)
        
        file_path = logo_dir / safe_name
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        
        return {
            "file_path": str(file_path.relative_to(storage)),
            "mime_type": mime_type,
            "file_size": size,
            "filename": safe_name,
        }
    
    @classmethod
    def save_invoice_pdf(cls, company_id: str, invoice_id: str, pdf_bytes: bytes) -> Path:
        """Save generated invoice PDF."""
        storage = cls._get_storage_path()
        pdf_dir = storage / "invoices" / company_id
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = pdf_dir / f"{invoice_id}.pdf"
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        return file_path
    
    @classmethod
    def get_file_path(cls, relative_path: str) -> Path:
        """Resolve a stored relative path to absolute path."""
        storage = cls._get_storage_path()
        target = storage / relative_path
        # Security: ensure resolved path is within storage
        try:
            target.resolve().relative_to(storage.resolve())
        except ValueError:
            raise ValidationException("Invalid file path")
        return target