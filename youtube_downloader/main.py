from downloader.core import YouTubeDownloader
from config.settings import DEFAULT_DOWNLOAD_PATH
import logging
from downloader.exceptions import DownloadError

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/downloader.log'),
            logging.StreamHandler()
        ]
    )

def main():
    setup_logging()
    print("=== YouTube Video/Audio Downloader (No FFmpeg) ===")
    print("Note: Downloads MP4 videos and M4A audio without conversion")
    downloader = YouTubeDownloader(DEFAULT_DOWNLOAD_PATH)
    
    while True:
        try:
            url = input("\nEnter YouTube URL (or 'quit' to exit): ").strip()
            if url.lower() in ['quit', 'exit']:
                break
            
            if not url.startswith(('http://', 'https://')):
                print("❌ Invalid URL. Please include http:// or https://")
                continue
            
            print("\nDownload Options:")
            print("1. Video (MP4)")
            print("2. Audio Only (M4A)")
            
            choice = input("Select option (1-2): ").strip()
            
            if choice == '1':
                res = input("Resolution (720p or 1080p) [Enter for best MP4]: ").strip() or None
                if res and res not in ['720p', '1080p']:
                    print("⚠️ Only 720p or 1080p supported without FFmpeg. Using best MP4.")
                    res = None
                downloader.download_video(url, res)
            elif choice == '2':
                downloader.download_audio(url)
            else:
                print("❌ Invalid choice")
                
        except DownloadError as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print("❌ An unexpected error occurred. Check logs for details.")

if __name__ == "__main__":
    main()