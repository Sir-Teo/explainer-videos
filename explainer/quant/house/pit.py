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


# Which part registered each strategy, and in what order within it.  The counter a part shows is the series'
# count up to that point: every earlier part's registrations, plus this part's up to the one just made.
PARTS = {
    "accounting_signals_part3": (3, 1), "cape_forecast_2021_2030": (3, 2), "osap_predictors_part3": (3, 3),
    "earnings_forecaster_part3": (3, 4),
    "btc_mean_confseq": (4, 1), "sign_continuation_ons": (4, 2), "sign_continuation_eprocess_btc": (4, 3),
    "sign_continuation_eprocess_us": (4, 4),
    "cir_mle_dtb3": (5, 1), "btc_hawkes_large_moves": (5, 2), "btc_rough_hurst": (5, 3), "btc_nsde_generator": (5, 4),
    "capm_two_pass": (6, 1), "industry_capm_alphas": (6, 2), "industry_momentum_panel": (6, 3),
    "fomc_announcement_days": (6, 4), "turn_of_month_event": (6, 5), "lookahead_rotation_toy": (6, 6),
    "shiller_oos_predictors": (6, 7),
    "btc_vol_race_2020": (7, 1), "btc_vol_harnet_2020": (7, 2), "btc_vol_toy_tsfm_2020": (7, 3),
    "btc_vol_toy_tsfm_np_2020": (7, 4),
    "kelly_us_split": (8, 1), "myopic_loss_aversion_us": (8, 2), "vol_target_us_market": (8, 3),
    "btc_vol_forecast_edge": (11, 1), "btc_hedged_straddle_ml": (11, 2),
    "pca_fly_2s5s10s": (18, 1),
    "cp_tent_oos": (19, 1), "mlp_bond_premia_oos": (19, 2),
    "logit_default_holdout": (20, 1), "gbm_default_holdout": (20, 2),
    "classic_mkt_part24": (24, 1), "classic_smb_part24": (24, 2), "classic_hml_part24": (24, 3),
    "classic_umd_part24": (24, 4), "classic_rmw_part24": (24, 5), "classic_cma_part24": (24, 6),
    "classic_bab_part24": (24, 7), "classic_qmj_part24": (24, 8), "classic_tsmom_part24": (24, 9),
    "classic_valmom_part24": (24, 10),
    "kns_sdf_part25": (25, 1), "zoo_equal_weight_part25": (25, 2),
    "stw_best_rule_part26": (26, 1),
    "nn3_coin_ls_part27": (27, 1), "kmz_timer_part27": (27, 2),
    "mined_combination_part29": (29, 1),
    "lw_gmv_part30": (30, 1), "hrp_part30": (30, 2), "equal_weight_part30": (30, 3),
    "gp_calm_reversal_part31": (31, 1),
    "trend_part32": (32, 1), "riskparity_part32": (32, 2),
    "residual_sscore_part33": (33, 1),
    "sestm_fomc_drift_part28": (28, 1),
}


def trials_upto(part: int, through: str | None = None) -> int:
    """The trial counter as Part ``part`` shows it: all registrations of earlier parts, plus this part's, or only
    those up to and including ``through``.  Every registered strategy must have a part."""
    reg = _read()["registered"]
    missing = sorted(set(reg) - set(PARTS))
    if missing:
        raise RuntimeError(f"give these registrations a part in pit.PARTS: {missing}")
    cut = PARTS[through] if through is not None else (part, 10 ** 9)
    return int(sum(r["trials"] for k, r in reg.items() if PARTS[k] <= cut))


def counted(loader, part: int, through: dict | None = None, items=("frontier_ml",)):
    """Wrap a part's cache loader so every envelope item (and ``items``) reports the series counter as of that part,
    whenever its cache was computed: Part 3's trials do not appear in Part 11's count, and later parts never see a
    count that went down.  ``through`` maps an item to the registration it should count up to."""
    through = through or {}

    def load(name: str):
        d = loader(name)
        if isinstance(d, dict) and "trials" in d and (name.startswith("envelope") or name in items):
            d = dict(d)
            d["trials"] = trials_upto(part, through.get(name))
        return d
    return load
