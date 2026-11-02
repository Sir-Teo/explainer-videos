"""The House's first rule: point in time, and the sealed envelope (Part 1; videos/quant/SYLLABUS.md, "The Track
Record and the sealed envelope").

**Point in time.**  A number used at time t may only depend on data stamped at or before t.  :func:`asof` is the one
way the House slices a dated series, so a signal can't read tomorrow's price by accident.

**The sealed envelope.**  All research in the series uses data up to 31 December 2020 (:data:`RESEARCH_END`).  The
hold-out, 1 January 2021 to the freeze date, is sealed: its SHA-256 is recorded the first time it is seen (in
``videos/quant/data/envelope.json``, committed), so it cannot be quietly changed.  A strategy is opened onto it once,
after it has been registered with the hash of its code, its parameters and the number of configurations tried; the
opening is recorded and a second opening refused.  Part 1 seals it; Parts 24-43 open it.
"""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
RESEARCH_END = 20201231
HOLDOUT_START = 20210101
ENVELOPE = Path(os.environ.get("EXPLAINER_ENVELOPE", ROOT / "videos" / "quant" / "data" / "envelope.json"))


def asof(dates, values, t: int):
    """The part of a dated series known at ``t`` (dates as YYYYMMDD ints, inclusive)."""
    d = np.asarray(dates)
    m = d <= t
    return d[m], np.asarray(values)[m]


def research(dates, values):
    """The research window: everything up to :data:`RESEARCH_END`."""
    return asof(dates, values, RESEARCH_END)


def _digest(dates, values) -> str:
    payload = json.dumps([np.asarray(dates).astype(int).tolist(), np.round(np.asarray(values, float), 10).tolist()],
                         separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def _read() -> dict:
    return json.loads(ENVELOPE.read_text()) if ENVELOPE.exists() else {"sealed": {}, "registered": {}, "opened": {}}


def _write(env: dict) -> None:
    ENVELOPE.parent.mkdir(parents=True, exist_ok=True)
    tmp = ENVELOPE.with_suffix(".tmp")
    tmp.write_text(json.dumps(env, indent=1, sort_keys=True) + "\n")
    tmp.replace(ENVELOPE)


def seal(name: str, dates, values) -> dict:
    """Seal a dataset's hold-out (dates >= :data:`HOLDOUT_START`): record its digest the first time, check it after.
    Returns the record (``digest``, ``first``/``last`` date, ``n``)."""
    d = np.asarray(dates)
    m = d >= HOLDOUT_START
    rec = {"digest": _digest(d[m], np.asarray(values)[m]), "first": int(d[m][0]), "last": int(d[m][-1]),
           "n": int(m.sum())}
    env = _read()
    old = env["sealed"].get(name)
    if old is None:
        env["sealed"][name] = rec
        _write(env)
    elif old != rec:
        raise RuntimeError(f"the sealed hold-out of {name} changed: {old} != {rec}")
    return rec


def register(strategy: str, code: str, params: dict, trials: int) -> dict:
    """Register a strategy before its hold-out is opened: the hash of its code, its parameters, and how many
    configurations were tried to arrive at it (the trial counter's input)."""
    env = _read()
    rec = {"code_sha256": hashlib.sha256(code.encode()).hexdigest(), "params": params, "trials": int(trials)}
    old = env["registered"].get(strategy)
    if old is not None and old != rec:
        raise RuntimeError(f"{strategy} is already registered with different code or parameters")
    env["registered"][strategy] = rec
    _write(env)
    return rec


def open_envelope(strategy: str, name: str, dates, values):
    """The hold-out of dataset ``name``, for a registered ``strategy``, once.  A second opening is refused (rerunning
    the same registered strategy re-reads it: the record is idempotent)."""
    env = _read()
    if strategy not in env["registered"]:
        raise RuntimeError(f"register {strategy} before opening the envelope")
    seal(name, dates, values)
    key = f"{strategy}|{name}"
    reg = env["registered"][strategy]
    if key in env["opened"] and env["opened"][key]["code_sha256"] != reg["code_sha256"]:
        raise RuntimeError(f"the envelope was already opened for {strategy} with other code: no second look")
    if key not in env["opened"]:
        env = _read()
        env["opened"][key] = {"code_sha256": reg["code_sha256"],
                              "at": datetime.now(timezone.utc).strftime("%Y-%m-%d")}
        _write(env)
    d = np.asarray(dates)
    m = d >= HOLDOUT_START
    return d[m], np.asarray(values)[m]


def trials_so_far() -> int:
    """The trial counter: configurations tried, summed over every registered strategy."""
    return int(sum(r["trials"] for r in _read()["registered"].values()))
