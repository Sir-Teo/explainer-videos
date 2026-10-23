"""The precomputed numbers of one part of *AI, Built*: ``.cache/<part>/<name>.json`` (+ ``.npz`` for arrays).

    CACHE = Cache("ai3")
    CACHE.main(ITEMS, __doc__)          # in the part's compute.py: python -m videos.ai.ai3.compute [names] [--force]
    load = CACHE.load                   # in the part's scenes: load("words")["neighbours"]

A long item saves its finished pieces as it goes, so a killed run resumes (and draws the same random numbers, if the
generator's state is one of the pieces):

    part = CACHE.partial("sat3", params)          # pieces computed with other params are discarded
    for cell in cells:
        if cell not in part:
            part[cell] = run(cell)                # saved at once (atomically)
    return {... part[cell] ...}                   # saving the item removes the partial file

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


class Partial:
    """The finished pieces of a long compute item, saved as they come (``.cache/<part>/<name>.partial.json``), so a run
    that is killed resumes where it stopped.  Pieces computed with other parameters are discarded; the file goes when
    the item itself is saved."""

    def __init__(self, path: Path, params, name: str = ""):
        self.path = path
        self.params = json.loads(json.dumps(params, default=float))
        data = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.done = data.get("done", {}) if data.get("params") == self.params else {}
        if self.done:
            print(f"  resuming {name}: {len(self.done)} pieces done", flush=True)

    def __contains__(self, key: str) -> bool:
        return key in self.done

    def __getitem__(self, key: str):
        return self.done[key]

    def __setitem__(self, key: str, value) -> None:
        self.done[key] = json.loads(json.dumps(value, default=float))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"params": self.params, "done": self.done}, default=float))
        tmp.replace(self.path)

    def finish(self) -> None:
        self.path.unlink(missing_ok=True)


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

    def partial(self, name: str, params) -> Partial:
        return Partial(self.dir / f"{name}.partial.json", params, f"{self.part}/{name}")

    def save(self, name: str, out: dict) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
        rest = {k: v for k, v in out.items() if k not in arrays}
        # arrays first, the .json last: an item is cached exactly when its .json exists, so a run killed halfway
        # leaves it missing (and recomputed), never half-written
        npz = self.path(name).with_suffix(".npz")
        if arrays:
            np.savez_compressed(self.path(name).with_suffix(".tmp.npz"), **arrays)
            self.path(name).with_suffix(".tmp.npz").replace(npz)
        else:
            npz.unlink(missing_ok=True)
        tmp = self.path(name).with_suffix(".tmp.json")
        tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
        tmp.replace(self.path(name))
        (self.dir / f"{name}.partial.json").unlink(missing_ok=True)  # the item is whole: its pieces can go
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
