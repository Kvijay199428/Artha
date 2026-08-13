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
    async def save_company_logo(cls, company_id: str, upload: UploadFile) -> dict:
        """Save and process company logo. Returns metadata dict."""
        from PIL import Image
        import io
        
        content_type = upload.content_type or ""
        if content_type not in ALLOWED_LOGO_TYPES:
            raise ValidationException(
                f"Invalid file type. Allowed: PNG, JPEG, WebP"
            )
        
        # Read file content
        data = await upload.read()
        if len(data) > MAX_LOGO_SIZE:
            raise ValidationException(f"File too large. Maximum: {MAX_LOGO_SIZE // 1024 // 1024}MB")
        
        # Open with Pillow
        try:
            img = Image.open(io.BytesIO(data))
            img.verify()  # Check integrity
            img = Image.open(io.BytesIO(data))  # Reopen after verify (verify closes it)
        except Exception:
            raise ValidationException("Invalid or corrupt image file")
        
        original_width, original_height = img.size
        if original_width < 100 or original_height < 100:
            raise ValidationException("Image too small. Minimum: 100x100 pixels")
        
        # Convert to RGB for WebP (handles RGBA/P mode)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if img.mode in ("P", "LA") else "RGB")
        
        # Center crop to square
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        
        # Resize to standard 600x600
        TARGET_SIZE = 600
        img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)
        
        # Convert RGBA to RGB for WebP saving (WebP supports RGBA, but keep as RGBA for transparency)
        # Save as WebP
        storage = cls._get_storage_path()
        logo_dir = storage / "company-logos" / company_id
        logo_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = logo_dir / "company_logo.webp"
        
        # Save
        output = io.BytesIO()
        img.save(output, format="WEBP", quality=95)
        output.seek(0)
        with open(file_path, "wb") as f:
            f.write(output.getvalue())
        
        return {
            "file_path": str(file_path.relative_to(storage)),
            "mime_type": "image/webp",
            "file_size": len(output.getvalue()),
            "filename": "company_logo.webp",
            "original_width": original_width,
            "original_height": original_height,
            "standardized_width": TARGET_SIZE,
            "standardized_height": TARGET_SIZE,
        }

    @staticmethod
    def get_logo_serve_url(company_id: str) -> str | None:
        """Get the URL to serve the company logo."""
        return f"/api/v1/company/logo/{company_id}"
    
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