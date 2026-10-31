"""Part-local completed-cache identity. Validation never invokes a numerical producer."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
import zipfile

import numpy as np

from explainer.ai.cache import Cache
from explainer.cache_lock import cache_lock, locked_item


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=float).encode()).hexdigest()


REQUIRED = {
    "params": "gpt2 qwen3_4b provenance", "tiny": "inputs values grads",
    "linapprox": "hs err slope rs perr ang D grad", "depth": "w L seeds gains mean0 lo0 hi0",
    "jacobians": "J_sm J_ln dX dW sm_diff ln_diff mm_diff jac_entries vjp_flops",
    "modes": "P net sizes fwd rev madds_fwd madds_rev benchmark work_count",
    "mlp2": "B dims loss d_lib d_torch dW1 dW2", "tape": "tape tape2 n_tape wgrad",
    "check": "loss torch_loss torch_diff fd_diff shown n_params",
    "train": "curve bits_train bits_valid H_cond corr logp snaps snaps_logp snap_steps metrics",
    "grad0": "grad diff pairs top", "gdlr": "lam0 etas steps H_cond bitcurve0 lamcurve0 metrics",
    "floats": "info xs rounding acc_steps lse_p lse", "cancel": "xs exact naive_fp32 stable_fp32 x_dead32",
    "vcurve": "hs ndir directions meas pred central_fp64 central_fp32 forward_fp64 forward_fp32",
    "checkpoint": "ks peak evals worst kbest memory_scope benchmark",
    "newton": "gd gd_path_steps newton newton_steps convergence reference eta L",
    "hessian": "P keep eig0 lam_est lam_dominant spectrum_thresholds metrics benchmark",
    "valley": "gd gd_f newton gd_steps_to_1pct convergence",
    "quad": "kappas rate_opt rate_L steps_opt steps_L esc convergence",
    "lagrange": "p_dice pi_star solvers comparisons resid dice_diff rl_diff",
    "kkt": "X y w b alpha margins solvers residuals tolerances grid nc_gap",
    "deq": "solves parameter_count curve fits d gradient_scope contraction_caps",
}


def valid_structure(name, payload):
    if name not in REQUIRED or not isinstance(payload, dict) or not set(REQUIRED[name].split()) <= payload.keys():
        return False
    if name == "params":
        return all(type(payload[key]) is int and payload[key] > 0 and
                   payload["provenance"][key]["source"] in ("pinned-safetensors-headers", "historical-fallback")
                   for key in ("gpt2", "qwen3_4b"))
    if name == "train":
        return all(np.asarray(payload[key]).shape == (27, 27) for key in ("logp",)) and \
            np.asarray(payload["snaps_logp"]).shape == (len(payload["snap_steps"]), 27, 27)
    if name == "grad0":
        return np.asarray(payload["grad"]).shape == (27, 27) and payload["pairs"] > 0
    return True


class SchemaCache(Cache):
    """All Part4 items use one conservative source recipe, explicit dependencies and exact payload integrity."""
    def recipe(self, name):
        root = Path(__file__).resolve().parents[3]
        sources = [Path(__file__), Path(__file__).with_name("compute.py"), Path(__file__).with_name("contracts.py"),
                   root / "explainer/ai/autodiff.py"]
        if name in ("train", "grad0", "gdlr"):
            sources.append(root / "videos/ai/ai1/compute.py")
        libraries = {}
        for package in ("numpy", "scipy", "torch"):
            try:
                libraries[package] = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                libraries[package] = None
        return dict(item=name, schema_version=1, source_hashes={str(p.relative_to(root)): digest(p) for p in sources},
                    libraries=libraries, invalidation_scope="conservative whole Part4 producer/helper source identity")

    def dependencies(self, name):
        files = []
        if name in ("train", "grad0", "gdlr"):
            files.append(self.dir.parent / "ai1/train.txt")
        if name == "train":
            files.append(self.dir.parent / "ai1/valid.txt")
        return {str(p.relative_to(self.dir.parent)): digest(p) for p in files}

    @locked_item(lambda self, name: self.path(name))
    def current(self, name):
        if name not in REQUIRED:
            return False
        try:
            data = json.loads(self.path(name).read_text())
            if not isinstance(data, dict):
                return False
            meta = data.pop("_cache")
            arrays = self.path(name).with_suffix(".npz")
            if meta != dict(schema_version=1, recipe=self.recipe(name), dependencies=self.dependencies(name),
                            payload_sha256=canonical(data), arrays_sha256=digest(arrays) if arrays.exists() else None,
                            origin="producer-save"):
                return False
            if arrays.exists():
                # CRC/decompression/type validation, not just file existence.
                with np.load(arrays, allow_pickle=False) as z:
                    for key in z.files:
                        if key in data or z[key].dtype.hasobject:
                            return False
                    data.update({key: z[key] for key in z.files})
            return valid_structure(name, data)
        except (OSError, ValueError, TypeError, KeyError, EOFError, zipfile.BadZipFile):
            return False

    def _produce(self, name, producer):
        before = self.dependencies(name)
        recipe = self.recipe(name)
        out = producer()
        if self.recipe(name) != recipe:
            raise ValueError(f"{name}: producer/helper source changed during generation; cache not published")
        if self.dependencies(name) != before:
            raise ValueError(f"{name}: consumed corpus changed during generation; cache not published")
        self.save(name, out, dependencies=before)

    @locked_item(lambda self, name: self.path(name))
    def load(self, name):
        if not self.current(name):
            self._produce(name, self.items[name])
        return super().load(name)

    @locked_item(lambda self, name, out, **kwargs: self.path(name))
    def save(self, name, out, *, dependencies=None):
        if not isinstance(out, dict) or "_cache" in out:
            raise ValueError("producer must return a dictionary without reserved _cache metadata")
        if not valid_structure(name, out):
            raise ValueError(f"{name}: incomplete or malformed producer payload")
        arrays = {k: v for k, v in out.items() if isinstance(v, np.ndarray)}
        rest = {k: v for k, v in out.items() if k not in arrays}
        # Match exactly the JSON representation that will be read back.
        rest = json.loads(json.dumps(rest, default=float))
        dependencies = self.dependencies(name) if dependencies is None else dependencies
        if dependencies != self.dependencies(name):
            raise ValueError("dependency changed before save")
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path(name).unlink(missing_ok=True)
        self._loaded.pop(name, None)
        npz = self.path(name).with_suffix(".npz")
        if arrays:
            tmp = self.path(name).with_suffix(".tmp.npz")
            np.savez_compressed(tmp, **arrays)
            tmp.replace(npz)
        else:
            npz.unlink(missing_ok=True)
        rest["_cache"] = dict(schema_version=1, recipe=self.recipe(name), dependencies=dependencies,
                              payload_sha256=canonical(rest), arrays_sha256=digest(npz) if arrays else None,
                              origin="producer-save")
        tmp = self.path(name).with_suffix(".tmp.json")
        tmp.write_text(json.dumps(rest, ensure_ascii=False, indent=1, default=float))
        tmp.replace(self.path(name))

    def main(self, items, doc=None):
        self.items = items
        parser = argparse.ArgumentParser(description=doc, formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument("names", nargs="*", default=list(items))
        parser.add_argument("--force", action="store_true")
        args = parser.parse_args()
        for name in args.names:
            with cache_lock(self.path(name)):
                if self.current(name) and not args.force:
                    print(f"  cached  {name}", flush=True)
                    continue
                start = time.monotonic()
                print(f"  compute {name} ...", flush=True)
                self._produce(name, items[name])
                print(f"  done    {name} in {time.monotonic() - start:.1f}s", flush=True)
