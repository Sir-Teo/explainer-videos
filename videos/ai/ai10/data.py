"""The two image datasets of Part 10, downloaded once into ``.cache/ai10/`` and checked against SHA-256.

* **MNIST** (LeCun, Cortes & Burges 1998): 70,000 handwritten digits, 28 x 28 grey levels, 60,000 for training and
  10,000 for testing, from the US National Institute of Standards and Technology's special databases 1 and 3.
  Downloaded from PyTorch's mirror of the original files (the four ``.gz`` files, about 11 MB).
* **CIFAR-10** (Krizhevsky 2009): 60,000 colour photographs, 32 x 32, ten classes, 50,000 for training and 10,000 for
  testing. Downloaded from Alex Krizhevsky's page at the University of Toronto (about 163 MB), unpacked once into a
  compressed ``.npz``.

A download resumes where it stopped (an HTTP range request), tries each mirror in turn, and is accepted only if its
SHA-256 matches the published files'; a mismatch deletes it and tries again.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import pickle
import tarfile
import time
import urllib.request
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

DIR = REPO_ROOT / ".cache" / "ai10"

MNIST_FILES = {
    "train-images-idx3-ubyte.gz": "440fcabf73cc546fa21475e81ea370265605f56be210a4024d2ca8f203523609",
    "train-labels-idx1-ubyte.gz": "3552534a0a558bbed6aed32b30c495cca23d567ec52cac8be1a0730e8010255c",
    "t10k-images-idx3-ubyte.gz": "8d422c7b0a1c1c79245a5bcf07fe86e33eeafee792b84584aec276f5a2dbc4e6",
    "t10k-labels-idx1-ubyte.gz": "f7ae60f92e00ec6debd23a6088c31dbd2371eca3ffa0defaefb259924204aec6",
}
MNIST_MIRRORS = ["https://ossci-datasets.s3.amazonaws.com/mnist/",
                 "https://storage.googleapis.com/cvdf-datasets/mnist/"]
CIFAR_FILE = "cifar-10-python.tar.gz"
CIFAR_SHA256 = "6d958be074577803d12ecdefd02955f39262c83c16fe9348329d7fe0b5c001ce"  # MD5 c58f3010..., as published
CIFAR_URLS = ["https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"]
CIFAR_CLASSES = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def download(urls, dst: Path, digest: str, tries: int = 6) -> Path:
    """Fetch ``dst`` from the first of ``urls`` that works, resuming a partial file, and check its SHA-256."""
    if dst.exists() and sha256(dst) == digest:
        return dst
    dst.parent.mkdir(parents=True, exist_ok=True)
    part = dst.with_suffix(dst.suffix + ".part")
    for attempt in range(tries):
        for url in urls:
            try:
                have = part.stat().st_size if part.exists() else 0
                req = urllib.request.Request(url, headers={"User-Agent": "explainer-videos (ai10)"})
                if have:
                    req.add_header("Range", f"bytes={have}-")
                with urllib.request.urlopen(req, timeout=60) as r:
                    mode = "ab" if have and r.status == 206 else "wb"
                    if mode == "wb":
                        have = 0
                    total = have + int(r.headers.get("Content-Length") or 0)
                    print(f"    downloading {url} ({total / 1e6:.0f} MB){' from ' + str(have) if have else ''}",
                          flush=True)
                    with open(part, mode) as f:
                        while True:
                            block = r.read(1 << 18)
                            if not block:
                                break
                            f.write(block)
                if sha256(part) == digest:
                    part.replace(dst)
                    return dst
                print(f"    checksum mismatch for {url}: discarded", flush=True)
                part.unlink(missing_ok=True)
            except OSError as e:  # urllib errors are OSErrors: retry, resuming
                print(f"    {url}: {e}; retrying", flush=True)
                time.sleep(min(30, 2 ** attempt))
    raise RuntimeError(f"could not download {dst.name}")


# ---------------------------------------------------------------------------
# MNIST
# ---------------------------------------------------------------------------
_mnist: dict = {}


def _idx(path: Path) -> np.ndarray:
    raw = gzip.decompress(path.read_bytes())
    dims = raw[3]
    shape = tuple(int.from_bytes(raw[4 + 4 * i:8 + 4 * i], "big") for i in range(dims))
    return np.frombuffer(raw, np.uint8, offset=4 + 4 * dims).reshape(shape)


def mnist() -> dict:
    """{'xtr', 'ytr', 'xte', 'yte'}: uint8 images (n, 28, 28) and labels."""
    if not _mnist:
        d = DIR / "mnist"
        files = {n: download([m + n for m in MNIST_MIRRORS], d / n, h) for n, h in MNIST_FILES.items()}
        _mnist.update(xtr=_idx(files["train-images-idx3-ubyte.gz"]), ytr=_idx(files["train-labels-idx1-ubyte.gz"]),
                      xte=_idx(files["t10k-images-idx3-ubyte.gz"]), yte=_idx(files["t10k-labels-idx1-ubyte.gz"]))
        assert _mnist["xtr"].shape == (60000, 28, 28) and _mnist["xte"].shape == (10000, 28, 28)
    return _mnist


# ---------------------------------------------------------------------------
# CIFAR-10
# ---------------------------------------------------------------------------
_cifar: dict = {}


def cifar() -> dict:
    """{'xtr', 'ytr', 'xte', 'yte'}: uint8 images (n, 32, 32, 3) and labels."""
    if not _cifar:
        d = DIR / "cifar"
        npz = d / "cifar10.npz"
        if not npz.exists():
            arc = download(CIFAR_URLS, d / CIFAR_FILE, CIFAR_SHA256)
            parts = {}
            with tarfile.open(arc, "r:gz") as tar:
                for m in tar.getmembers():
                    name = Path(m.name).name
                    if name.startswith(("data_batch_", "test_batch")):
                        # the archive's own batches (checked by its SHA-256 above): pickled dicts of arrays
                        parts[name] = pickle.load(io.BytesIO(tar.extractfile(m).read()), encoding="bytes")

            def stack(names):
                x = np.concatenate([parts[n][b"data"] for n in names]).reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
                y = np.concatenate([np.asarray(parts[n][b"labels"]) for n in names]).astype(np.uint8)
                return np.ascontiguousarray(x), y

            xtr, ytr = stack([f"data_batch_{i}" for i in range(1, 6)])
            xte, yte = stack(["test_batch"])
            tmp = d / "cifar10.tmp.npz"
            np.savez_compressed(tmp, xtr=xtr, ytr=ytr, xte=xte, yte=yte)
            tmp.replace(npz)
        with np.load(npz) as z:
            _cifar.update({k: z[k] for k in z.files})
        assert _cifar["xtr"].shape == (50000, 32, 32, 3) and _cifar["xte"].shape == (10000, 32, 32, 3)
    return _cifar
