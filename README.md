# Clipboard QR Code Tool

A small macOS utility that converts between URLs and QR codes using the clipboard.

- **Copy a URL** -> run the script -> a QR code image is copied to your clipboard, ready to paste anywhere.
- **Copy an image containing a QR code** -> run the script -> the decoded text is copied to your clipboard.

## How it works

The script checks your clipboard on each run:

1. If it finds a URL, it uses `pyqrcode` to generate a QR code PNG and copies it as an image via `pyperclipimg`.
2. If it finds an image, it passes it to `pyzbar` (backed by the native `zbar` library) for decoding and copies the result as text via `pyperclip`.

## Requirements

- macOS (uses `ImageGrab` for clipboard image access, which is macOS/Windows only)
- Python 3.11+
- [Homebrew](https://brew.sh)

## Installation

```bash
# 1. Install the native zbar library
brew install zbar

# 2. Clone the repo
git clone https://github.com/SathyaTadinada/QR-Code-Tool.git
cd QR-Code-Tool

# 3. Install Python dependencies
uv add pillow pyperclip pyperclipimg pyqrcode pypng pyzbar

# or with pip
pip install pillow pyperclip pyperclipimg pyqrcode pypng pyzbar
```

> **Note:** `pyzbar` looks for the zbar shared library in standard system paths, which does not include Homebrew by default. The script patches this at startup to check `/opt/homebrew/lib` (Apple Silicon) and `/usr/local/lib` (Intel), so you don't need to set `DYLD_LIBRARY_PATH` manually.

## Usage

```bash
# With uv
uv run qr_code.py

# Or directly if dependencies are installed
python qr_code.py
```

You can bind this to a keyboard shortcut or add it to your `$PATH` for quick access.

## Roadmap

- [ ] macOS menu bar app via [`rumps`](https://github.com/jaredks/rumps) for one-click conversions
- [ ] Support for reading QR codes from files (drag-and-drop)
- [ ] Distributable `.app` bundle via PyInstaller

## Dependencies

| Package | Purpose |
|---|---|
| `pyzbar` | QR code decoding via the native `zbar` library |
| `pyqrcode` + `pypng` | QR code generation and PNG export |
| `pillow` | Image handling and clipboard image reading |
| `pyperclip` | Read/write text clipboard |
| `pyperclipimg` | Write images to the clipboard |
