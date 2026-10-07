"""Precompute every fluid simulation used in the Navier–Stokes video.

    python -m videos.navier_stokes.simulate            # everything missing
    python -m videos.navier_stokes.simulate kh turb    # specific runs
    python -m videos.navier_stokes.simulate --force    # recompute

Results are cached in ``.cache/sims/<name>.npz``; scenes call ``load(name)``.
All footage is played back at 30 frames per second of video.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np

from explainer.tts import REPO_ROOT

SIM_DIR = REPO_ROOT / ".cache" / "sims"


# ---------------------------------------------------------------------------
# Runs
# ---------------------------------------------------------------------------
def _cylinder(re, u0=0.08, smag=0.0, frames=240, warmup_flow_throughs=3.5):
    from explainer.fluids.lbm import run_cylinder

    nx = 720
    # Same physical playback speed for every run: the free stream moves
    # 2.4 lattice cells per video frame regardless of the lattice velocity.
    steps_per_frame = int(round(2.4 / u0))
    warmup = int(warmup_flow_throughs * nx / u0)
    return lambda: run_cylinder(
        re=re,
        n_frames=frames,
        steps_per_frame=steps_per_frame,
        warmup_steps=warmup,
        smagorinsky=smag,
        u0=u0,
        nx=nx,
        ny=240,
        diameter=36,
    )


def _kh():
    from explainer.fluids.spectral import Spectral2D, record, shear_layer_ic

    sim = Spectral2D(n=384, nu=1.5e-4, kappa=3e-4)
    w, dye = shear_layer_ic(sim, delta=0.09, amp=0.04, modes=2)
    sim.set_vorticity(w)
    sim.set_scalar(dye)
    frames, dye, energy = record(sim, n_frames=540, frame_dt=1 / 30, scalar=True)
    return {"vorticity": frames, "dye": dye, "energy": energy}


def _turb():
    from explainer.fluids.spectral import Spectral2D, random_vorticity_ic, record

    sim = Spectral2D(n=384, nu=1.5e-4)
    sim.set_vorticity(random_vorticity_ic(sim, k_peak=14, rms=12, seed=3))
    frames, _, energy = record(sim, n_frames=720, frame_dt=1 / 24)
    return {"vorticity": frames, "energy": energy}


def _viscous_pair():
    from explainer.fluids.spectral import Spectral2D, random_vorticity_ic, record

    out = {}
    for name, nu in [("water", 4e-4), ("honey", 2e-2)]:
        sim = Spectral2D(n=256, nu=nu)
        sim.set_vorticity(random_vorticity_ic(sim, k_peak=6, rms=6, seed=7))
        frames, _, energy = record(sim, n_frames=360, frame_dt=1 / 30)
        out[f"{name}_vorticity"] = frames
        out[f"{name}_energy"] = energy
    return out


RUNS = {
    "cyl_re150": _cylinder(150, frames=720),
    "cyl_re1": _cylinder(1, u0=0.02, frames=240, warmup_flow_throughs=2.0),
    "cyl_re40": _cylinder(40, frames=240),
    "cyl_re1000": _cylinder(1000, smag=0.15, frames=240),
    "kh": _kh,
    "turb": _turb,
    "viscous_pair": _viscous_pair,
}


# ---------------------------------------------------------------------------
def path(name: str) -> Path:
    return SIM_DIR / f"{name}.npz"


_loaded: dict[str, dict] = {}


def load(name: str) -> dict:
    if name not in _loaded:
        p = path(name)
        if not p.exists():
            raise FileNotFoundError(f"Missing simulation '{name}'. Run: python -m videos.navier_stokes.simulate {name}")
        with np.load(p) as data:
            _loaded[name] = {k: data[k] for k in data.files}
    return _loaded[name]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", default=list(RUNS))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    SIM_DIR.mkdir(parents=True, exist_ok=True)
    for name in args.names:
        if path(name).exists() and not args.force:
            print(f"[skip] {name} (cached)")
            continue
        t = time.time()
        print(f"[run ] {name} ...", flush=True)
        data = RUNS[name]()
        tmp = path(name).with_suffix(".tmp.npz")
        np.savez(tmp, **data)
        tmp.replace(path(name))
        print(f"[done] {name} in {time.time() - t:.0f}s", flush=True)


if __name__ == "__main__":
    main()
