import pytest
from youtube_downloader.downloader.utils import sanitize_filename, is_valid_youtube_url, format_duration, format_size

def test_sanitize_filename():
    assert sanitize_filename('test?file*name.mp4') == 'testfilename.mp4'
    assert sanitize_filename('  clean_file.mp4  ') == 'clean_file.mp4'

def test_is_valid_youtube_url():
    assert is_valid_youtube_url('https://www.youtube.com/watch?v=dQw4w9WgXcQ') is True
    assert is_valid_youtube_url('https://youtu.be/dQw4w9WgXcQ') is True
    assert is_valid_youtube_url('https://google.com') is False
    assert is_valid_youtube_url('invalid_string') is False

def test_format_duration():
    assert format_duration(75) == '1:15'
    assert format_duration(3665) == '1:01:05'
    assert format_duration(0) == 'N/A'

def test_format_size():
    assert format_size(0) == '0B'
    assert format_size(1024) == '1.0 KB'