from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Default download path
DEFAULT_DOWNLOAD_PATH = BASE_DIR / 'downloads'

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'downloader.log',
            'formatter': 'standard'
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}