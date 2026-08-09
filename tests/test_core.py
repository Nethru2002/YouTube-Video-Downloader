import pytest
from youtube_downloader.downloader.core import YouTubeDownloader
from youtube_downloader.downloader.exceptions import InvalidURLError

def test_downloader_initialization(tmp_path):
    downloader = YouTubeDownloader(tmp_path)
    assert downloader.video_path.exists()
    assert downloader.audio_path.exists()

def test_invalid_url_handling(tmp_path):
    downloader = YouTubeDownloader(tmp_path)
    with pytest.raises(InvalidURLError):
        downloader.download_video("https://not-a-youtube-site.com/watch?v=123")
    with pytest.raises(InvalidURLError):
        downloader.download_audio("not_a_url")