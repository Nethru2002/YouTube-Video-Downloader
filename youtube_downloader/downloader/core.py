import yt_dlp
import os
from pathlib import Path
import logging
from typing import Optional
from .exceptions import DownloadError
from .utils import sanitize_filename

class YouTubeDownloader:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.video_path = self.base_path / 'videos'
        self.audio_path = self.base_path / 'audio'
        self._setup_directories()
    
    def _setup_directories(self):
        self.video_path.mkdir(parents=True, exist_ok=True)
        self.audio_path.mkdir(parents=True, exist_ok=True)
    
    def download_video(self, url: str, resolution: Optional[str] = None) -> str:
        """Download video without requiring FFmpeg merging"""
        try:
            # Format selection that avoids merging
            format_selector = {
                '1080p': 'bestvideo[height<=1080][ext=mp4]',
                '720p': 'bestvideo[height<=720][ext=mp4]',
                None: 'best[ext=mp4]'  # Single-file MP4
            }.get(resolution, 'best[ext=mp4]')
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': str(self.video_path / '%(title)s.%(ext)s'),
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"✅ Video saved to: {filename}")
                return filename
                
        except Exception as e:
            logging.error(f"Video download failed: {e}")
            raise DownloadError(f"Video download failed: {str(e)}")

    def download_audio(self, url: str) -> str:
        """Download audio without requiring FFmpeg conversion"""
        try:
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]',  # Directly download M4A format
                'outtmpl': str(self.audio_path / '%(title)s.%(ext)s'),
                'quiet': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"✅ Audio saved as M4A: {filename}")
                return filename
                
        except Exception as e:
            logging.error(f"Audio download failed: {e}")
            raise DownloadError(f"Audio download failed: {str(e)}")

    def _print_video_info(self, info: dict):
        """Print basic video information"""
        print(f"\n🎬 Title: {info.get('title', 'N/A')}")
        print(f"⏱️ Duration: {info.get('duration_string', 'N/A')}")
        print(f"👤 Author: {info.get('uploader', 'N/A')}")
        print(f"👀 Views: {info.get('view_count', 'N/A'):,}")