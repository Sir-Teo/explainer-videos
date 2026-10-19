"""Build ``kernels.c`` with the machine's C compiler and call it through ctypes.

The library goes to ``.cache/ai17/`` (named by a hash of the source and flags). ``load()`` returns None when no compiler
works, and compute.py then measures with numpy instead and says so.  Tried in order: ``cc``, ``gcc``, ``clang``, each with
``-O3 -march=native`` and then plain ``-O3`` (Apple clang on arm64 may refuse ``-march=native``).  No ``-ffast-math``:
the naive loop's dot product stays a sequential sum, as written.
"""

from __future__ import annotations

import ctypes
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

SRC = Path(__file__).with_name("kernels.c")
OUT = REPO_ROOT / ".cache" / "ai17"
F32 = ctypes.POINTER(ctypes.c_float)
I64 = ctypes.POINTER(ctypes.c_int64)
_LIB = None
INFO: dict = {}


def _try(cc: str, flags: list[str]) -> Path | None:
    tag = hashlib.sha1((SRC.read_text() + cc + " ".join(flags) + sys.platform).encode()).hexdigest()[:12]
    lib = OUT / f"kernels-{tag}.so"
    if lib.exists():
        return lib
    OUT.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([cc, *flags, "-shared", "-fPIC", "-o", str(lib), str(SRC)], capture_output=True, text=True)
    return lib if r.returncode == 0 and lib.exists() else None


def load():
    global _LIB
    if _LIB is not None:
        return _LIB
    for cc in ("cc", "gcc", "clang"):
        path = shutil.which(cc)
        if not path:
            continue
        for flags in (["-O3", "-march=native"], ["-O3"]):
            lib = _try(cc, flags)
            if lib is None:
                continue
            ver = subprocess.run([cc, "--version"], capture_output=True, text=True).stdout.splitlines()
            INFO.update(compiler=cc, version=(ver[0] if ver else cc), flags=" ".join(flags))
            L = ctypes.CDLL(str(lib))
            L.read_sum.argtypes = [F32, ctypes.c_long, ctypes.c_long]
            L.read_sum.restype = ctypes.c_float
            L.triad.argtypes = [F32, F32, F32, ctypes.c_float, ctypes.c_long, ctypes.c_long]
            L.copy.argtypes = [F32, F32, ctypes.c_long, ctypes.c_long]
            L.chase.argtypes = [I64, ctypes.c_long]
            L.chase.restype = ctypes.c_int64
            for f in (L.mm_naive, L.mm_ikj):
                f.argtypes = [F32, F32, F32, ctypes.c_int]
            L.mm_blocked.argtypes = [F32, F32, F32, ctypes.c_int, ctypes.c_int]
            L.alloc_big.argtypes = [ctypes.c_size_t]
            L.alloc_big.restype = ctypes.c_void_p
            L.free_big.argtypes = [ctypes.c_void_p]
            _LIB = L
            return L
    return None


def ptr(a: np.ndarray):
    assert a.flags["C_CONTIGUOUS"]
    return a.ctypes.data_as(I64 if a.dtype == np.int64 else F32)


class BigArray:
    """A numpy view of memory from ``alloc_big`` (huge pages on Linux); freed when closed."""

    def __init__(self, lib, n: int, dtype):
        self.lib = lib
        nbytes = n * np.dtype(dtype).itemsize
        self.p = lib.alloc_big(nbytes)
        if not self.p:
            raise MemoryError(nbytes)
        buf = (ctypes.c_char * nbytes).from_address(self.p)
        self.a = np.frombuffer(buf, dtype=dtype, count=n)

    def close(self):
        if self.p:
            self.a = None
            self.lib.free_big(self.p)
            self.p = None
