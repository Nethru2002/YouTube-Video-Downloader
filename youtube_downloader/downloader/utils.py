import re
import math
from urllib.parse import urlparse

def sanitize_filename(filename: str) -> str:
    """Remove invalid filename characters."""
    return re.sub(r'[\\/*?:"<>|]', "", filename).strip()

def is_valid_youtube_url(url: str) -> bool:
    """Validates if the string is a genuine YouTube URL."""
    if not url:
        return False
    try:
        parsed = urlparse(url)
        valid_netlocs = {'www.youtube.com', 'youtube.com', 'youtu.be', 'm.youtube.com'}
        return parsed.netloc in valid_netlocs and bool(parsed.path)
    except Exception:
        return False

def format_duration(seconds: int) -> str:
    """Convert seconds to HH:MM:SS."""
    if not seconds:
        return "N/A"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"

def format_size(bytes_val: int) -> str:
    """Convert bytes to human-readable size."""
    if not bytes_val or bytes_val == 0:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(bytes_val, 1024)))
    size = round(bytes_val / math.pow(1024, i), 2)
    return f"{size} {units[i]}"