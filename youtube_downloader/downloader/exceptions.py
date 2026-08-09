class DownloadError(Exception):
    """Base exception for download failures."""
    pass

class InvalidURLError(DownloadError):
    """Raised when the provided URL is malformed or not a valid YouTube link."""
    pass

class ResolutionNotAvailableError(DownloadError):
    """Raised when the requested resolution is unavailable for the target video."""
    pass

class AgeRestrictedError(DownloadError):
    """Raised when content is age-restricted and requires authentication."""
    pass