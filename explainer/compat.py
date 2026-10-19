"""Work-arounds for library releases newer than the manim we build on."""

from __future__ import annotations

import numpy as np
from PIL import Image

_fromarray = Image.fromarray


def _fromarray_compat(obj, mode=None):
    # manim 0.22 draws every ImageMobject onto a blank canvas made as fromarray(zeros((h, w)), mode="RGBA"); Pillow 13
    # no longer reinterprets a buffer to fit the mode and raises.  The canvas is just transparent black.
    if mode == "RGBA" and isinstance(obj, np.ndarray) and obj.ndim == 2:
        return Image.new("RGBA", (obj.shape[1], obj.shape[0]))
    return _fromarray(obj) if mode is None else _fromarray(obj, mode)


Image.fromarray = _fromarray_compat
