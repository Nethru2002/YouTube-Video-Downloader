# YouTube Downloader

A robust, enterprise-ready Python desktop application designed to download YouTube high-definition videos and high-fidelity audio streams securely **without requiring external toolchain installations like FFmpeg**.

---

## 🚀 Key Features

* **Zero FFmpeg Dependencies:** Intelligently queries and extracts standalone container formats (`.mp4` video codecs and `.m4a` audio containers) natively without merge failures.
* **Universal Resolution Targeting:** Supports downloading media streams across any user-defined target quality scale—ranging from custom options like `4K (2160p)`, `1440p`, `1080p`, `720p`, down to lower specifications—or defaulting to absolute highest system optimization.
* **Interactive Progress Tracking:** Integrates dynamic real-time progress bars using `tqdm` to monitor download speeds, bytes transferred, and ETA percentage rates accurately.
* **Network Fault Resilience:** Built-in connection socket timeout buffers, automatic fragment re-tries, and chunk-recovery error handling to prevent dropouts on weak connections.
* **Structured Domain Exceptions:** Clean abstraction layers handling invalid URL inputs, age-restricted token walls, and unavailable stream qualities gracefully.
* **Persistent Logging Infrastructure:** Comprehensive logging design routing diagnostic execution events seamlessly to local rotation handlers (`logs/downloader.log`).

---

## 🛠️ Project Directory Structure

```text
youtube_downloader/
│
├── pyproject.toml             # Modern build system & entry point definitions
├── requirements.txt           # Explicit core dependency pin configurations
├── README.md                  # Project documentation manual
├── youtube_downloader/        # Source package directory
│   ├── __init__.py
│   ├── main.py                # Interactive CLI runtime entry controller
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py        # Centralized path and dictionary logging configs
│   └── downloader/
│       ├── __init__.py
│       ├── core.py            # Core engine executing yt-dlp abstractions
│       ├── exceptions.py      # Custom domain-specific exception hierarchy
│       └── utils.py           # Sanitization, sizing, and URL validators
└── tests/                     # Automated testing suite
    ├── __init__.py
    ├── test_core.py           # Core component validation tests
    └── test_utils.py          # Utility logic tests
```

---

## 📦 Installation & Setup

### 1. Clone or Navigate to Project Root
Open your terminal inside the root folder containing `pyproject.toml`.

### 2. Create and Activate a Virtual Environment
```bash
python -m venv .venv
```
* **Windows (PowerShell):**
  ```bash
  .venv\Scripts\Activate.ps1
  ```
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Package & Dependencies
Install the package in editable mode along with development dependencies:
```bash
pip install --editable .[dev]
```

---

## 💡 Usage Guide

You can launch the application through either of the following execution methods:

### Method A: Using the Registered Command-Line Script
```bash
yt-download
```

### Method B: Running as an Executable Python Module
```bash
python -m youtube_downloader.main
```

### Interactive Steps:
1. Paste a standard YouTube video link (e.g., `https://www.youtube.com/watch?v=...`). *(Note: Playlist mix URLs automatically filter out sequence queues to safeguard individual downloads).*
2. Review the fetched metadata overview (Title, Duration, Author, and View Count).
3. Select your preferred download option:
   * **`1` (Video):** Input your preferred target resolution scale (e.g., `2160p`, `1440p`, `1080p`, `720p`) or press **Enter** to target the absolute best native MP4 configuration.
   * **`2` (Audio Only):** Automatically extracts and saves the direct stream as an `.m4a` file.
4. Track progress live via the console progress bar. Completed files populate neatly into the automatically generated `downloads/videos/` or `downloads/audio/` directories.

---

## 🧪 Running Tests

To verify package integrity and run the test suite via `pytest`:
```bash
python -m pytest
```

---

## 📝 Troubleshooting

* **`The read operation timed out`:** This happens if your network provider or YouTube throttles high-bandwidth streams. The application includes a built-in auto-retry sequence (up to 15 attempts), but switching to a lower resolution (e.g., `720p` or `1080p`) usually bypasses unstable speed caps.
* **`Import could not be resolved (Pylance)`:** Ensure VS Code's active interpreter matches your `.venv` virtual environment path (`Ctrl + Shift + P` -> `Python: Select Interpreter`).