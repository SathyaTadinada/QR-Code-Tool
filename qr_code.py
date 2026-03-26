"""
qr_code.py - Clipboard QR Code Tool

Reads from the macOS clipboard and does one of two things:
  - If the clipboard contains a URL: generates a QR code and copies it as an image.
  - If the clipboard contains an image with a QR code: decodes it and copies the text.

Dependencies:
  brew install zbar          # native zbar library (required by pyzbar)
  uv add pillow              # image handling
  uv add pyperclip           # read/write text clipboard
  uv add pyperclipimg        # write image to clipboard
  uv add pyqrcode            # QR code generation
  uv add pypng               # PNG support for pyqrcode
  uv add pyzbar              # QR code decoding via zbar
"""

import ctypes
import os
import platform
import re
import tempfile

# pyzbar uses ctypes.util.find_library('zbar'), which doesn't search Homebrew
# paths on macOS. This patch checks the Homebrew lib locations directly and
# must run before pyzbar is imported.
if platform.system() == "Darwin":
    from ctypes.util import find_library

    if not find_library("zbar"):
        import pyzbar.zbar_library as _zbar_lib

        def _patched_load():
            for _path in ("/opt/homebrew/lib/libzbar.dylib", "/usr/local/lib/libzbar.dylib"):
                if os.path.exists(_path):
                    return ctypes.cdll.LoadLibrary(_path), []
            raise ImportError("Unable to find zbar shared library. Run: brew install zbar")

        _zbar_lib.load = _patched_load

import pyperclip
import pyqrcode
import pyperclipimg as pci
from PIL import Image, ImageGrab
from pyzbar.pyzbar import decode

_URL_RE = re.compile(r"\bhttps?://[^\s/$.?#].[^\s]*\b")


def generate_qr_code(data: str) -> None:
    """Generate a QR code image from a URL and copy it to the clipboard."""
    tmp = tempfile.mktemp(suffix=".png")
    qr = pyqrcode.create(data)
    qr.png(tmp, scale=8)
    pci.copy(tmp)
    os.remove(tmp)
    print("QR code copied to clipboard.")


def decode_qr_code(image: Image.Image) -> None:
    """Decode a QR code from a PIL Image and copy the result to the clipboard."""
    try:
        text = decode(image)[0][0].decode("utf-8")
        pyperclip.copy(text)
        print("Decoded:", text)
    except Exception as e:
        print("Error decoding QR code:", e)


def main() -> None:
    text = pyperclip.paste()
    try:
        if text and _URL_RE.search(text):
            generate_qr_code(text)
        elif isinstance(img := ImageGrab.grabclipboard(), Image.Image):
            decode_qr_code(img)
        else:
            print("Clipboard does not contain a URL or QR code image.")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
