from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEFAULT_DOWNLOAD_PATH = BASE_DIR / 'downloads'

LOGS_PATH = BASE_DIR / 'logs'
LOGS_PATH.mkdir(parents=True, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': LOGS_PATH / 'downloader.log',
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}