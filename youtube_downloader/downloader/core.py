import logging
from pathlib import Path
from typing import Optional, Dict, Any
import yt_dlp
from tqdm import tqdm

from .exceptions import (
    DownloadError,
    InvalidURLError,
    ResolutionNotAvailableError,
    AgeRestrictedError
)
from .utils import is_valid_youtube_url, format_duration

logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self, base_path: str | Path):
        self.base_path = Path(base_path)
        self.video_path = self.base_path / 'videos'
        self.audio_path = self.base_path / 'audio'
        self._setup_directories()

    def _setup_directories(self) -> None:
        self.video_path.mkdir(parents=True, exist_ok=True)
        self.audio_path.mkdir(parents=True, exist_ok=True)

    def _get_progress_hook(self, pbar: tqdm):
        def hook(d: Dict[str, Any]):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                if total > 0:
                    pbar.total = total
                pbar.update(downloaded - pbar.n)
            elif d['status'] == 'finished':
                pbar.n = pbar.total or pbar.n
                pbar.refresh()
        return hook

    def get_video_info(self, url: str) -> Dict[str, Any]:
        if not is_valid_youtube_url(url):
            raise InvalidURLError(f"Invalid or unsupported YouTube URL: {url}")
        
        ydl_opts = {'quiet': True, 'no_warnings': True, 'noplaylist': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            error_str = str(e).lower()
            if "sign in" in error_str or "age" in error_str:
                raise AgeRestrictedError("Video is age-restricted and requires authorization.")
            raise DownloadError(f"Failed to extract video info: {e}")

    def print_video_info(self, info: Dict[str, Any]) -> None:
        print(f"\n🎬 Title    : {info.get('title', 'N/A')}")
        print(f"⏱️ Duration : {format_duration(info.get('duration'))}")
        print(f"👤 Author   : {info.get('uploader', 'N/A')}")
        print(f"👀 Views    : {info.get('view_count', 0):,}")

    def download_video(self, url: str, resolution: Optional[str] = None) -> str:
        if not is_valid_youtube_url(url):
            raise InvalidURLError(f"Invalid YouTube URL provided: {url}")

        if resolution:
            clean_res = resolution.lower().replace('p', '').strip()
            format_selector = f'bestvideo[height<={clean_res}][ext=mp4]/best[height<={clean_res}][ext=mp4]/best[height<={clean_res}]'
        else:
            format_selector = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

        with tqdm(total=0, unit='B', unit_scale=True, unit_divisor=1024, desc="Downloading Video") as pbar:
            ydl_opts = {
                'format': format_selector,
                'outtmpl': str(self.video_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'socket_timeout': 60,
                'retries': 15,
                'fragment_retries': 15,
                'skip_unavailable_fragments': True,
                'progress_hooks': [self._get_progress_hook(pbar)]
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    logger.info(f"Video successfully downloaded: {filename}")
                    print(f"\n✅ Video saved to: {filename}")
                    return filename
            except Exception as e:
                error_str = str(e)
                logger.error(f"Video download failed: {error_str}")
                if "requested format is not available" in error_str.lower():
                    raise ResolutionNotAvailableError(f"Resolution {resolution} is not available for this video.")
                if "sign in" in error_str.lower() or "age" in error_str.lower():
                    raise AgeRestrictedError("Content is age-restricted.")
                raise DownloadError(f"Video download failed: {error_str}")

    def download_audio(self, url: str) -> str:
        if not is_valid_youtube_url(url):
            raise InvalidURLError(f"Invalid YouTube URL provided: {url}")

        with tqdm(total=0, unit='B', unit_scale=True, unit_divisor=1024, desc="Downloading Audio") as pbar:
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio',
                'outtmpl': str(self.audio_path / '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'socket_timeout': 60,
                'retries': 15,
                'fragment_retries': 15,
                'skip_unavailable_fragments': True,
                'progress_hooks': [self._get_progress_hook(pbar)]
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    logger.info(f"Audio successfully downloaded: {filename}")
                    print(f"\n✅ Audio saved as M4A: {filename}")
                    return filename
            except Exception as e:
                error_str = str(e)
                logger.error(f"Audio download failed: {error_str}")
                if "sign in" in error_str.lower() or "age" in error_str.lower():
                    raise AgeRestrictedError("Content is age-restricted.")
                raise DownloadError(f"Audio download failed: {error_str}")