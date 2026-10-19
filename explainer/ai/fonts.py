"""Font files for the letter pictures (Parts 21-23), on Linux as on macOS.

The pictures were designed on Linux, where the DejaVu and Liberation families live in /usr/share/fonts. Elsewhere
(macOS has no /usr/share/fonts) the same two families are fetched once into .cache/fonts, so the parts compute the
same kind of letters on any machine.
"""

from __future__ import annotations

import glob
import io
import tarfile
import urllib.request
import zipfile
from pathlib import Path

from explainer.paths import ROOT

SYSTEM = Path("/usr/share/fonts")
LOCAL = ROOT / ".cache" / "fonts"
SOURCES = [
    ("https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip", "dejavu"),
    ("https://github.com/liberationfonts/liberation-fonts/files/7261482/liberation-fonts-ttf-2.1.5.tar.gz",
     "liberation"),
]


def _fetch():
    for url, name in SOURCES:
        dest = LOCAL / name
        if any(dest.rglob("*.ttf")):
            continue
        dest.mkdir(parents=True, exist_ok=True)
        data = urllib.request.urlopen(url, timeout=300).read()
        if url.endswith(".zip"):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for m in z.namelist():
                    if m.endswith(".ttf"):
                        (dest / Path(m).name).write_bytes(z.read(m))
        else:
            with tarfile.open(fileobj=io.BytesIO(data)) as t:
                for m in t.getmembers():
                    if m.name.endswith(".ttf"):
                        (dest / Path(m.name).name).write_bytes(t.extractfile(m).read())


def font_files(pattern: str = "**/*.ttf") -> list[str]:
    """Sorted font files matching ``pattern`` under the system font directory (Linux), else under .cache/fonts."""
    if any(SYSTEM.rglob("*.ttf")) if SYSTEM.exists() else False:
        root = SYSTEM
    else:
        _fetch()
        root = LOCAL
    return sorted(set(glob.glob(str(root / pattern), recursive=True)))
