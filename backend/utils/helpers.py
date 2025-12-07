"""
Utility functions for file handling, validation, and common operations.
"""

import os
import uuid
import asyncio
from pathlib import Path
from typing import Optional, Tuple
import mimetypes

from backend.config import SUPPORTED_FORMATS, MIME_TYPES


def generate_unique_filename(original_filename: str, extension: str = None) -> str:
    """
    Generate a unique filename using UUID.
    
    Args:
        original_filename: Original name of the file
        extension: Optional new extension
    
    Returns:
        Unique filename with extension
    """
    base_name = Path(original_filename).stem
    if extension:
        ext = extension.lstrip('.')
    else:
        ext = Path(original_filename).suffix.lstrip('.')
    
    unique_id = str(uuid.uuid4())[:8]
    return f"{base_name}_{unique_id}.{ext}"


def get_file_extension(filename: str) -> str:
    """Get the lowercase extension of a file."""
    return Path(filename).suffix.lower().lstrip('.')


def get_file_category(extension: str) -> Optional[str]:
    """
    Determine the category of a file based on its extension.
    
    Args:
        extension: File extension without dot
    
    Returns:
        Category name or None if not supported
    """
    ext = extension.lower().lstrip('.')
    for category, extensions in SUPPORTED_FORMATS.items():
        if ext in extensions:
            return category
    return None


def validate_conversion(source_ext: str, target_ext: str) -> Tuple[bool, str]:
    """
    Validate if conversion between two formats is supported.
    
    Args:
        source_ext: Source file extension
        target_ext: Target file extension
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    source_ext = source_ext.lower().lstrip('.')
    target_ext = target_ext.lower().lstrip('.')
    
    source_category = get_file_category(source_ext)
    target_category = get_file_category(target_ext)
    
    if not source_category:
        return False, f"Source format '{source_ext}' is not supported"
    
    if not target_category:
        return False, f"Target format '{target_ext}' is not supported"
    
    # Check if conversion is within same category or compatible
    compatible_conversions = {
        ("video", "audio"): True,  # Extract audio from video
        ("video", "video"): True,
        ("audio", "audio"): True,
        ("image", "image"): True,
        ("document", "document"): True,
        ("spreadsheet", "spreadsheet"): True,
        ("document", "spreadsheet"): True,  # PDF to Excel
        ("spreadsheet", "document"): True,  # Excel to PDF
    }
    
    if (source_category, target_category) not in compatible_conversions:
        return False, f"Cannot convert from {source_category} to {target_category}"
    
    return True, ""


def get_mime_type(extension: str) -> str:
    """Get MIME type for a file extension."""
    ext = extension.lower().lstrip('.')
    return MIME_TYPES.get(ext, "application/octet-stream")


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"


import subprocess
from functools import partial

async def run_command_async(command: list) -> Tuple[int, str, str]:
    """
    Run a command asynchronously using thread executor.
    This avoids Windows asyncio subprocess issues (NotImplementedError).
    
    Args:
        command: List of command arguments
    
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    loop = asyncio.get_event_loop()
    
    def _run():
        # Hide console window on Windows
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        # Run command - avoiding massive memory buffering
        # We don't need stdout for FFmpeg (it writes to file)
        # We only capture stderr for error logging
        try:
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,  # Don't buffer stdout
                stderr=subprocess.PIPE,     # Buffer stderr for errors
                text=True,
                encoding='utf-8',
                errors='ignore',
                startupinfo=startupinfo,
                timeout=300 # 5 minute timeout safety
            )
            return result.returncode, "", result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Process timed out"
        except Exception as e:
            return 1, "", str(e)
            
    return await loop.run_in_executor(None, _run)
        
    return await loop.run_in_executor(None, _run)


def cleanup_file(filepath: Path) -> bool:
    """
    Safely delete a file.
    
    Args:
        filepath: Path to the file to delete
    
    Returns:
        True if deleted successfully, False otherwise
    """
    try:
        if filepath.exists():
            filepath.unlink()
            return True
        return False
    except Exception:
        return False
