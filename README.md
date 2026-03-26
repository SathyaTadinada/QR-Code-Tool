# Clipboard QR Code Tool

A lightweight macOS command-line utility that works both ways with QR codes, entirely through the clipboard.

- **Copy a URL** → run the script → a QR code image is copied to your clipboard, ready to paste anywhere.
- **Copy a screenshot or image containing a QR code** → run the script → the decoded text is copied to your clipboard.

## How it works

The script inspects your clipboard on each run:

1. If it finds a URL, it uses `pyqrcode` to generate a QR code PNG and copies it as an image via `pyperclipimg`.
2. If it finds an image, it passes it directly to `pyzbar` (backed by the native `zbar` library) for decoding and copies the result as text via `pyperclip`.

## Requirements

- macOS (uses `ImageGrab` for clipboard image access, which is macOS/Windows only)
- Python 3.11+
- [Homebrew](https://brew.sh)

## Installation

```bash
# 1. Install the native zbar library
brew install zbar

# 2. Clone the repo
git clone https://github.com/YOUR_USERNAME/qr-code-tool.git
cd qr-code-tool

# 3. Install Python dependencies (using uv)
uv add pillow pyperclip pyperclipimg pyqrcode pypng pyzbar

# or with pip
pip install pillow pyperclip pyperclipimg pyqrcode pypng pyzbar
```

> **Note on zbar + macOS:** `pyzbar` uses `ctypes.util.find_library` to locate the zbar shared library, which doesn't search Homebrew paths by default. This project includes a small patch that checks `/opt/homebrew/lib` (Apple Silicon) and `/usr/local/lib` (Intel) before falling back to the system search, so no manual `DYLD_LIBRARY_PATH` export is needed.

## Usage

```bash
# With uv
uv run qr_code.py

# Or directly if dependencies are installed
python qr_code.py
```

For convenience, you can bind this to a keyboard shortcut or add it to your `$PATH`.

## Roadmap

- [ ] macOS menu bar app (likely via [`rumps`](https://github.com/jaredks/rumps)) so the conversion is a single button press from the menu bar
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
