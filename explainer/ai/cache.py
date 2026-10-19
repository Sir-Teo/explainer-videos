"""The precomputed numbers of one part of *AI, Built*: ``.cache/<part>/<name>.json`` (+ ``.npz`` for arrays).

    CACHE = Cache("ai3")
    CACHE.main(ITEMS, __doc__)          # in the part's compute.py: python -m videos.ai.ai3.compute [names] [--force]
    load = CACHE.load                   # in the part's scenes: load("words")["neighbours"]

Part 1 predates this module and keeps its own copy of the same helpers (``videos/ai/ai1/compute.py``).
"""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT


class Cache:
    def __init__(self, part: str):
        self.part = part
        self.dir = REPO_ROOT / ".cache" / part
        self._loaded: dict = {}
        self.items: dict = {}

    def path(self, name: str) -> Path:
        return self.dir / f"{name}.json"

    def load(self, name: str) -> dict:
        if name not in self._loaded:
            p = self.path(name)
            if not p.exists():  # compute on first use (a scene rendered before compute was run)
                if not self.items:
                    import importlib

                    from explainer.paths import video_package

                    self.items = importlib.import_module(f"{video_package(self.part)}.compute").ITEMS
                if name not in self.items:
                    raise FileNotFoundError(f"{p} missing, and no compute item {name!r} for {self.part}")
                print(f"  computing {self.part}/{name} (first use) ...", flush=True)
                self.save(name, self.items[name]())
            self._loaded[name] = json.loads(p.read_text())
            npz = p.with_suffix(".npz")
            if npz.exists():
                with np.load(npz) as z:
                    self._loaded[name].update({k: z[k] for k in z.files})
        return self._loaded[name]

    def save(self, name: str, out: dict) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
        rest = {k: v for k, v in out.items() if k not in arrays}
        tmp = self.path(name).with_suffix(".tmp.json")
        tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
        tmp.replace(self.path(name))
        if arrays:
            np.savez_compressed(self.path(name).with_suffix(".tmp.npz"), **arrays)
            self.path(name).with_suffix(".tmp.npz").replace(self.path(name).with_suffix(".npz"))
        self._loaded.pop(name, None)

    def main(self, items: dict, doc: str | None = None) -> None:
        self.items = items
        ap = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
        ap.add_argument("names", nargs="*", default=list(items))
        ap.add_argument("--force", action="store_true")
        args = ap.parse_args()
        self.dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")
        for name in args.names:
            if self.path(name).exists() and not args.force:
                print(f"  cached  {name}")
                continue
            t = time.time()
            print(f"  compute {name} ...", flush=True)
            self.save(name, items[name]())
            print(f"  done    {name} in {time.time() - t:.0f}s", flush=True)
