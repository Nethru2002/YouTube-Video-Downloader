import re
from pathlib import Path
from typing import Union
import math

def sanitize_filename(filename: str) -> str:
    """Remove invalid filename characters"""
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def format_duration(seconds: int) -> str:
    """Convert seconds to HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"

def format_size(bytes: int) -> str:
    """Convert bytes to human-readable size"""
    if bytes == 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(bytes, 1024)))
    size = round(bytes / math.pow(1024, i), 2)
    return f"{size} {units[i]}"