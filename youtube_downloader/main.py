import sys
import logging
import logging.config

from youtube_downloader.config.settings import DEFAULT_DOWNLOAD_PATH, LOGGING_CONFIG
from youtube_downloader.downloader.core import YouTubeDownloader
from youtube_downloader.downloader.exceptions import DownloadError

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main() -> None:
    print("=== YouTube Video/Audio Downloader (Production Grade) ===")
    print("Note: Downloads media streams safely without FFmpeg.")
    
    try:
        downloader = YouTubeDownloader(DEFAULT_DOWNLOAD_PATH)
    except Exception as e:
        print(f"❌ Fatal Initialization Error: {e}")
        sys.exit(1)
    
    while True:
        try:
            url = input("\nEnter YouTube URL (or type 'quit' to exit): ").strip()
            if url.lower() in ['quit', 'exit']:
                print("Exiting application. Goodbye!")
                break
            
            if not url:
                continue

            print("🔍 Fetching media details...")
            try:
                info = downloader.get_video_info(url)
                downloader.print_video_info(info)
            except DownloadError as de:
                print(f"❌ {de}")
                continue

            print("\nDownload Options:")
            print("1. Video")
            print("2. Audio Only (M4A)")
            
            choice = input("Select option (1-2): ").strip()
            
            if choice == '1':
                res = input("Target Resolution (e.g. 2160p, 1440p, 1080p, 720p) [Press Enter for absolute best]: ").strip() or None
                downloader.download_video(url, res)
            elif choice == '2':
                downloader.download_audio(url)
            else:
                print("❌ Invalid input option selected. Please choose 1 or 2.")
                
        except DownloadError as de:
            print(f"❌ Download Error: {de}")
        except KeyboardInterrupt:
            print("\nOperation aborted by user. Exiting...")
            sys.exit(0)
        except Exception as e:
            logger.exception("An unexpected critical system error occurred.")
            print("❌ An unexpected error occurred. Check logs/downloader.log for more details.")

if __name__ == "__main__":
    main()