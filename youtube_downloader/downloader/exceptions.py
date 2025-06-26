class DownloadError(Exception):
    """Base exception for download failures"""
    pass

class InvalidURLError(DownloadError):
    """Invalid YouTube URL"""
    pass

class ResolutionNotAvailableError(DownloadError):
    """Requested resolution not available"""
    pass

class AgeRestrictedError(DownloadError):
    """Age-restricted content"""
    pass