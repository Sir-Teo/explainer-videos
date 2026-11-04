"""Every number in Part 29 (Alpha Mining and Automated Research), computed and cached in .cache/quant29/.

    python -m videos.quant.quant29.compute [items] [--force]

The mining ground is Part 27's survivorship-free panel of every coin Binance has quoted in USDT: daily candles,
a coin eligible on a day when it has 60 days of history and a median quote volume of at least 250,000 USDT over the
past four weeks.  Signals on day t, scored against the return from the close of t to the close of t + 1.
Train 2018-01 to 2019-12, validate 2020; 2021-2025 is sealed and read once, in ``envelope``.

* ``grid``       the mining grid: days, coins, eligibility;
* ``classic``    three of Kakushadze's 101 formulaic alphas, computed on coins;
* ``space``      how many formulas exist by depth;
* ``random``     10,000 random formulas: the winner's curse in IC;
* ``gp``         genetic programming, three seeds, replayed generation by generation;
* ``rl``         a REINFORCE token generator rewarded by its pool's combined IC (AlphaGen's idea);
* ``combine``    combining the mined alphas: correlation, breadth, equal weight against estimated weights;
* ``decay``      the best alpha's IC by horizon, and by year;
* ``theory``     the research chapter: the out-of-sample Sharpe ratio of an estimated combination, by K and T;
* ``envelope``   the mined combination, registered and opened on 2021-2025.
"""

from __future__ import annotations

import functools
import json
import math
import warnings

import numpy as np

from explainer.ai.cache import Cache
from explainer.quant.house import alphas as A, pit

warnings.filterwarnings("ignore", category=RuntimeWarning)

CACHE = Cache("quant29")
load = pit.counted(CACHE.load, 29)
MIN_QV = 2.5e5
START, TRAIN_END, VALID_END = 20180101, 20191231, 20201231


def _json(d):
    return json.loads(json.dumps(d, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o)))


def _ymd(day):
    from datetime import datetime, timezone
    return int(datetime.fromtimestamp(int(day) * 86400, timezone.utc).strftime("%Y%m%d"))


@functools.lru_cache(maxsize=None)
def _full_grid():
    from videos.quant.quant27.compute import _grid
    d0, names, G = _grid()
    dates = np.array([_ymd(d0 + t) for t in range(G["close"].shape[0])])
    return dates, names, G


def _fields(G, rows, cols):
    C, H, L, Q = (G[k][rows][:, cols] for k in ("close", "high", "low", "quote"))
    ret = np.vstack([np.full((1, C.shape[1]), np.nan), np.diff(np.log(C), axis=0)])
    F = {"close": C, "high": H, "low": L, "volume": Q, "ret": ret, "vwap": (H + L + C) / 3}
    fwd = np.vstack([ret[1:], np.full((1, C.shape[1]), np.nan)])
    return F, fwd


def _mask(G, rows, cols):
    C, Q = G["close"][:, cols], G["quote"][:, cols]
    first = np.array([np.flatnonzero(np.isfinite(C[:, j]))[0] if np.isfinite(C[:, j]).any() else 10 ** 9
                      for j in range(C.shape[1])])
    m = np.zeros((len(rows), len(cols)), bool)
    for i, t in enumerate(rows):
        med = np.nanmedian(Q[max(t - 27, 0):t + 1], axis=0)
        m[i] = np.isfinite(C[t]) & (first <= t - 60) & (med >= MIN_QV)
    return m


@functools.lru_cache(maxsize=None)
def _research():
    """The mining grid: 2018-2020 plus 30 days of warm-up, the coins eligible at least once, and the masks."""
    dates, names, G = _full_grid()
    lo = int(np.searchsorted(dates, START)) - 30
    hi = int(np.searchsorted(dates, VALID_END, side="right"))
    rows = np.arange(lo, hi)
    m_all = _mask(G, rows, np.arange(len(names)))
    cols = np.flatnonzero(m_all[30:].any(axis=0))
    F, fwd = _fields(G, rows, cols)
    mask = m_all[:, cols].copy()
    mask[:30] = False
    d = dates[rows]
    train = np.flatnonzero((d >= START) & (d <= TRAIN_END))
    valid = np.flatnonzero((d > TRAIN_END) & (d <= VALID_END))
    return d, [names[j] for j in cols], F, fwd, mask, train, valid


def compute_grid() -> dict:
    d, names, F, fwd, mask, train, valid = _research()
    n_day = mask.sum(1)
    return _json({"n_days": int(len(train) + len(valid)), "n_train": int(len(train)), "n_valid": int(len(valid)),
                  "n_coins": len(names), "median_per_day": float(np.median(n_day[30:])), "min_per_day": int(n_day[30:].min()),
                  "max_per_day": int(n_day[30:].max()), "dates": d[30:], "per_day": n_day[30:]})


# ---------------------------------------------------------------------------
# Kakushadze's formulas on coins
# ---------------------------------------------------------------------------
CLASSIC = {
    "Alpha#12": "sign(delta(volume, 1)) * (-1 * delta(close, 1))",
    "Alpha#41": "((high * low)^0.5) - vwap",
    "Alpha#101": "(close - open) / ((high - low) + 0.001), open = yesterday's close on a 24-hour market",
}


def _classic_trees():
    return {
        "Alpha#12": ("mul", ("sign", ("delta", ("field", "volume"), 1)), ("neg", ("delta", ("field", "close"), 1))),
        "Alpha#41": ("sub", ("field", "geo_hl"), ("field", "vwap")),
        "Alpha#101": ("div", ("sub", ("field", "close"), ("delay", ("field", "close"), 1)),
                      ("add", ("sub", ("field", "high"), ("field", "low")), ("const", 0.001))),
    }


def compute_classic() -> dict:
    d, names, F, fwd, mask, train, valid = _research()
    F = dict(F)
    F["geo_hl"] = np.sqrt(F["high"] * F["low"])
    out = {}
    for name, tr in _classic_trees().items():
        ic = A.ic_series(A.evaluate(tr, F), fwd, mask)
        ls = A.ls_returns(A.evaluate(tr, F), fwd, mask)
        out[name] = {"formula": CLASSIC[name], "train": A.score(ic, train), "valid": A.score(ic, valid),
                     "sr_train": A.sharpe(ls[train]), "sr_valid": A.sharpe(ls[valid]),
                     "cum": np.nancumsum(np.nan_to_num(ls[30:])), "monthly_ic": _monthly(d, ic)}
    return _json({"rows": out, "dates": d[30:]})


def _monthly(d, x):
    ym = d // 100
    keys = np.unique(ym[30:])
    return {"ym": keys, "v": np.array([np.nanmean(x[ym == k]) for k in keys])}


def compute_space() -> dict:
    n = A.count_trees(6)
    return _json({"depth": list(range(1, 7)), "count": [float(v) for v in n], "fields": list(A.FIELDS),
                  "unary": list(A.UNARY), "ts": list(A.TS), "binary": list(A.BINARY), "windows": list(A.WINDOWS)})


# ---------------------------------------------------------------------------
# Random search, GP, RL
# ---------------------------------------------------------------------------
N_RANDOM = 10_000


def compute_random() -> dict:
    d, names, F, fwd, mask, train, valid = _research()
    rng = np.random.default_rng(2929)
    res = A.random_search(F, fwd, mask, train, valid, N_RANDOM, rng, max_depth=4)
    tr = np.array([r[0] for r in res])
    va = np.array([r[1] for r in res])
    # sign each formula by its training IC (a miner would flip a negative one)
    s = np.sign(tr)
    s[s == 0] = 1
    tr_s, va_s = tr * s, va * s
    order = np.argsort(-tr_s)
    Ns = [10, 30, 100, 300, 1000, 3000, 10000]
    best_by_n = []
    for n in Ns:
        k = int(np.argmax(tr_s[:n]))
        best_by_n.append({"n": n, "train": float(tr_s[k]), "valid": float(va_s[k]), "formula": res[k][2]})
    top = [{"train": float(tr_s[k]), "valid": float(va_s[k]), "formula": res[k][2]} for k in order[:15]]
    ok = np.isfinite(tr_s) & np.isfinite(va_s)
    sd_null = float(np.std(tr[ok]))
    return _json({"n": N_RANDOM, "train": tr_s, "valid": va_s, "best_by_n": best_by_n, "top": top,
                  "corr": float(np.corrcoef(tr_s[ok], va_s[ok])[0, 1]), "sd_train": sd_null,
                  "n_train_days": int(len(train)), "frac_same_sign": float(np.mean(va_s[ok] > 0)),
                  "top100_valid_mean": float(np.mean(va_s[order[:100]])), "top100_train_mean": float(np.mean(tr_s[order[:100]]))})


def compute_gp() -> dict:
    d, names, F, fwd, mask, train, valid = _research()
    runs = []
    for seed in (1, 2, 3):
        rng = np.random.default_rng(seed)
        runs.append(A.gp(F, fwd, mask, train, valid, rng, pop=100, gens=25))
    return _json({"runs": runs, "pop": 100, "gens": 25})


TOKENS = list(A.FIELDS) + [f"{op}_{w}" for op in A.TS for w in A.WINDOWS] + list(A.UNARY) + list(A.BINARY)


def _decode(tokens):
    """Reverse-Polish tokens to a tree, or None if the sequence is not a single well-formed expression."""
    st = []
    for tk in tokens:
        if tk in A.FIELDS:
            st.append(("field", tk))
        elif tk in A.UNARY:
            if not st:
                return None
            st.append((tk, st.pop()))
        elif tk in A.BINARY:
            if len(st) < 2:
                return None
            b, a = st.pop(), st.pop()
            st.append((tk, a, b))
        else:
            op, w = tk.rsplit("_", 1)
            if not st:
                return None
            st.append((op, st.pop(), int(w)))
    return st[0] if len(st) == 1 else None


def compute_rl(episodes: int = 1500, pool_max: int = 10, max_len: int = 9) -> dict:
    """A REINFORCE token generator: a GRU policy writes a formula token by token (reverse Polish, a stack-validity
    mask); the reward is the increase in the training IC of a linear combination of the pool when the new alpha is
    added (Yu et al. 2023's synergy reward), minus a penalty for invalid formulas."""
    import torch
    import torch.nn as nn
    torch.manual_seed(29)
    torch.set_num_threads(2)
    d, names, F, fwd, mask, train, valid = _research()
    V = len(TOKENS) + 1                     # + END
    END = V - 1
    arity = {tk: (0 if tk in A.FIELDS else 2 if tk in A.BINARY else 1) for tk in TOKENS}

    class Policy(nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = nn.Embedding(V + 1, 32)
            self.gru = nn.GRU(32, 64, batch_first=True)
            self.out = nn.Linear(64, V)

        def forward(self, x, h=None):
            o, h = self.gru(self.emb(x), h)
            return self.out(o[:, -1]), h

    pol = Policy()
    opt = torch.optim.Adam(pol.parameters(), lr=3e-3)
    pool, pool_sig = [], []
    cache = {}

    def signal(tree):
        k = A.to_str(tree)
        if k not in cache:
            v = A.rank(np.where(mask, A.evaluate(tree, F), np.nan))
            cache[k] = np.nan_to_num(v)
        return cache[k]

    def pool_ic(sigs):
        if not sigs:
            return 0.0
        X = np.stack([s[train] for s in sigs], -1)              # (days, coins, k)
        y = np.nan_to_num(fwd[train])
        m = mask[train]
        Xf, yf = X[m], y[m]
        w = np.linalg.lstsq(Xf, yf, rcond=None)[0]
        comb = np.tensordot(np.stack(sigs, -1), w, axes=([2], [0]))
        return A.score(A.ic_series(comb, fwd, mask), train)["ic"]

    base = 0.0
    hist = []
    for ep in range(episodes):
        x = torch.tensor([[V]])
        h = None
        toks, logps, depth_ = [], [], 0
        for step in range(max_len):
            logits, h = pol(x, h)
            mvec = torch.zeros(V)
            for i, tk in enumerate(TOKENS):
                need = arity[tk]
                if depth_ < need or (depth_ - need + 1) > max_len - step - 1 + 1:
                    mvec[i] = -1e9
            if depth_ != 1:
                mvec[END] = -1e9
            dist = torch.distributions.Categorical(logits=logits[0] + mvec)
            a = dist.sample()
            logps.append(dist.log_prob(a))
            if int(a) == END:
                break
            tk = TOKENS[int(a)]
            toks.append(tk)
            depth_ += 1 - arity[tk]
            x = torch.tensor([[int(a)]])
        tree = _decode(toks)
        if tree is None:
            reward = -0.01
        else:
            s = signal(tree)
            ic_new = pool_ic(pool_sig + [s])
            reward = ic_new - base
            if reward > 0.0005 and A.to_str(tree) not in [A.to_str(p) for p in pool]:
                pool.append(tree)
                pool_sig.append(s)
                if len(pool) > pool_max:                   # drop the member whose removal costs least
                    losses = [pool_ic(pool_sig[:i] + pool_sig[i + 1:]) for i in range(len(pool))]
                    j = int(np.argmax(losses))
                    pool.pop(j)
                    pool_sig.pop(j)
                base = pool_ic(pool_sig)
        loss = -reward * 100 * torch.stack(logps).sum()
        opt.zero_grad()
        loss.backward()
        opt.step()
        if ep % 25 == 0 or ep == episodes - 1:
            hist.append({"ep": ep, "pool_ic": base, "pool": len(pool), "valid_frac": None})
    # the final pool on the validation year
    if pool_sig:
        X = np.stack([s[train] for s in pool_sig], -1)
        w = np.linalg.lstsq(X[mask[train]], np.nan_to_num(fwd[train])[mask[train]], rcond=None)[0]
        comb = np.tensordot(np.stack(pool_sig, -1), w, axes=([2], [0]))
        ic = A.ic_series(comb, fwd, mask)
        tr_ic, va_ic = A.score(ic, train), A.score(ic, valid)
    else:
        tr_ic = va_ic = {"ic": 0.0, "t": 0.0, "n": 0}
    return _json({"episodes": episodes, "hist": hist, "pool": [A.to_str(p) for p in pool], "train": tr_ic, "valid": va_ic,
                  "evaluated": len(cache), "tokens": len(TOKENS)})


# ---------------------------------------------------------------------------
# Combination
# ---------------------------------------------------------------------------
def _top_alphas(k: int = 40, return_trees: bool = False):
    """The k best random formulas by |train IC|, de-duplicated by correlation of their signals (|rho| < 0.9)."""
    from explainer.quant.house.alphas import random_tree
    d, names, F, fwd, mask, train, valid = _research()
    rng = np.random.default_rng(2929)
    trees = [random_tree(rng, 4) for _ in range(N_RANDOM)]       # the same draws as ``random``
    r = load("random")
    tr = np.asarray(r["train"], float)
    order = np.argsort(-np.nan_to_num(tr))
    picked, sigs, rets, kept = [], [], [], []
    for i in order:
        t = trees[i]
        raw = A.evaluate(t, F)
        sgn = 1.0 if np.nan_to_num(r["train"][i]) >= 0 else -1.0
        s = A.rank(np.where(mask, sgn * raw, np.nan))
        sv = np.nan_to_num(s[train]).ravel()
        if any(abs(np.corrcoef(sv, np.nan_to_num(q[train]).ravel())[0, 1]) > 0.9 for q in sigs):
            continue
        picked.append(A.to_str(t))
        kept.append((t, sgn))
        sigs.append(s)
        rets.append(A.ls_returns(s, fwd, mask))
        if len(picked) == k:
            break
    if return_trees:
        return picked, sigs, np.array(rets).T, kept
    return picked, sigs, np.array(rets).T


def compute_combine() -> dict:
    d, names, F, fwd, mask, train, valid = _research()
    picked, sigs, R = _top_alphas(40)
    Rt, Rv = R[train], R[valid]
    C = np.corrcoef(np.nan_to_num(Rt), rowvar=False)
    rho = float(np.mean(C[np.triu_indices_from(C, 1)]))
    Ks = [1, 2, 5, 10, 20, 40]
    rows = []
    for K in Ks:
        ew_t, ew_v = np.nanmean(Rt[:, :K], 1), np.nanmean(Rv[:, :K], 1)
        w = A.combine(Rt[:, :K])
        mv_t, mv_v = np.nan_to_num(Rt[:, :K]) @ w, np.nan_to_num(Rv[:, :K]) @ w
        ws = A.combine(Rt[:, :K], shrink=1.0)
        sh_v = np.nan_to_num(Rv[:, :K]) @ ws
        rows.append({"K": K, "ew_train": A.sharpe(ew_t), "ew_valid": A.sharpe(ew_v), "mv_train": A.sharpe(mv_t),
                     "mv_valid": A.sharpe(mv_v), "shrunk_valid": A.sharpe(sh_v)})
    single_t = [A.sharpe(Rt[:, i]) for i in range(R.shape[1])]
    single_v = [A.sharpe(Rv[:, i]) for i in range(R.shape[1])]
    eig = np.sort(np.linalg.eigvalsh(C))[::-1]
    return _json({"formulas": picked, "rho": rho, "rows": rows, "single_train": single_t, "single_valid": single_v,
                  "eig": eig, "n_eff": float(eig.sum() ** 2 / (eig ** 2).sum()), "corr": C})


def compute_decay() -> dict:
    d, names, F, fwd, mask, train, valid = _research()
    picked, sigs, R = _top_alphas(5)
    s = sigs[0]
    ret = F["ret"]
    out = {}
    for h in (1, 2, 3, 5, 10, 20):
        fw = np.full_like(ret, np.nan)
        for t in range(len(ret) - h):
            fw[t] = np.nansum(ret[t + 1:t + 1 + h], axis=0)
        ic = A.ic_series(s, fw, mask)
        out[str(h)] = {"train": A.score(ic, train), "valid": A.score(ic, valid)}
    ic1 = A.ic_series(s, fwd, mask)
    years = sorted(set(d[30:] // 10000))
    by_year = {str(y): A.score(ic1, np.flatnonzero((d // 10000 == y) & (np.arange(len(d)) >= 30)))["ic"] for y in years}
    return _json({"formula": picked[0], "horizons": out, "by_year": by_year})


# ---------------------------------------------------------------------------
# Research: the out-of-sample Sharpe ratio of an estimated combination
# ---------------------------------------------------------------------------
def compute_theory() -> dict:
    rng = np.random.default_rng(2930)
    Ts = [250, 500, 1000]
    Ks = [1, 2, 5, 10, 20, 40, 80]
    sr_each = 0.03                                   # each signal's per-day Sharpe ratio (about 0.57 a year)
    sims = {}
    for T in Ts:
        rows = []
        for K in Ks:
            theta = np.full(K, sr_each)
            star = float(np.linalg.norm(theta))
            known = A.sr_oos_sim(theta, T, 300, rng)
            est = A.sr_oos_sim(theta, T, 300, rng, known_cov=False) if K < T - 2 else np.array([np.nan])
            rows.append({"K": K, "star": star, "theory": A.sr_oos_theory(star, K, T), "known": float(np.mean(known)),
                         "known_sd": float(np.std(known)), "estimated": float(np.nanmean(est))})
        sims[str(T)] = rows
    # diminishing signals: the k-th signal has Sharpe ratio sr1 / sqrt(k): SR*^2 grows like a harmonic sum
    T = 500
    dim = []
    for K in Ks:
        theta = 0.06 / np.sqrt(np.arange(1, K + 1))
        star = float(np.linalg.norm(theta))
        dim.append({"K": K, "star": star, "theory": A.sr_oos_theory(star, K, T),
                    "known": float(np.mean(A.sr_oos_sim(theta, T, 300, rng)))})
    # the mined alphas: estimated weights on 2018-19, measured on 2020, against the theory with the train Sharpe
    c = load("combine")
    data = [{"K": r["K"], "mv_valid": r["mv_valid"], "ew_valid": r["ew_valid"], "mv_train": r["mv_train"]} for r in c["rows"]]
    return _json({"Ts": Ts, "Ks": Ks, "sr_each": sr_each, "sims": sims, "diminishing": dim, "data": data,
                  "best_K_dim": int(Ks[int(np.argmax([r["theory"] for r in dim]))])})


# ---------------------------------------------------------------------------
# The envelope
# ---------------------------------------------------------------------------
STRATEGY = "mined_combination_part29"
COST_BP = 10.0          # a round trip on a liquid coin, in basis points of the traded notional


def compute_envelope() -> dict:
    import inspect
    from explainer.quant.house import track
    c = load("combine")
    rows = c["rows"]
    K = max(rows, key=lambda r: r["mv_valid"])["K"]              # the number of alphas, chosen on 2020
    gp_ev = sum(r[-1]["evaluated"] for r in load("gp")["runs"])
    n_trials = N_RANDOM + gp_ev + load("rl")["evaluated"] + len(rows)
    code = inspect.getsource(_top_alphas) + inspect.getsource(A.combine) + inspect.getsource(A.ls_returns) + \
        inspect.getsource(A.evaluate)
    pit.register(STRATEGY, code, {"alphas": f"the {K} best random formulas by 2018-19 IC, de-duplicated",
                                  "weights": "mean-variance on 2018-2020 daily long-short returns",
                                  "universe": f"Binance USDT coins, 60 days listed, median volume >= {MIN_QV:.0f}",
                                  "cost_bp": COST_BP}, trials=n_trials)
    picked, sigs, R, kept = _top_alphas(K, return_trees=True)
    d, names, F, fwd, mask, train, valid = _research()
    research = np.r_[train, valid]
    w = A.combine(R[research])
    # the sealed years: the same formulas on every coin of the full grid
    dates, all_names, G = _full_grid()
    lo = int(np.searchsorted(dates, START)) - 30
    rows_all = np.arange(lo, len(dates))
    cols = np.arange(len(all_names))
    Fa, fwda = _fields(G, rows_all, cols)
    ma = _mask(G, rows_all, cols)
    ma[:30] = False
    da = dates[rows_all]
    fin = np.isfinite(fwda)
    hd, hv = pit.open_envelope(STRATEGY, "binance/usdt_daily_returns", da, np.where(fin, np.round(fwda, 8), -999.0))
    rets = []
    for t_, s in kept:
        sig = A.rank(np.where(ma, s * A.evaluate(t_, Fa), np.nan))
        rets.append(A.ls_returns(sig, fwda, ma))
    P = np.nan_to_num(np.array(rets).T) @ w
    hold = da > VALID_END
    res = (da >= START) & (da <= VALID_END)
    cost_day = 2 * COST_BP / 1e4 * 0.5                         # assumed: half the book turns over each day
    def monthly(m):
        ym = da[m] // 100
        keys = np.unique(ym)
        return keys, np.array([np.prod(1 + P[m][ym == k]) - 1 for k in keys])
    kr, mr = monthly(res)
    kh, mh = monthly(hold)
    row = track.record(STRATEGY, 29, mr, mh, cost_day * 365, note="daily long-short of the mined combination, gross; "
                       "cost charged at 10 bp a round trip, half the book a day")
    cum_h = np.cumsum(np.log1p(np.clip(P[hold], -0.99, None)))
    return _json({"trials": pit.trials_so_far(), "n_trials": n_trials, "K": K, "formulas": picked, "weights": w,
                  "row": row, "sr_hold": A.sharpe(P[hold]), "sr_res": A.sharpe(P[res]), "cum_hold": cum_h,
                  "hold_dates": da[hold], "first": int(da[hold][0]), "last": int(da[hold][-1]), "cost_year": cost_day * 365,
                  "by_year": {str(y): A.sharpe(P[hold & (da // 10000 == y)]) for y in range(2021, 2026)}})


ITEMS = {"grid": compute_grid, "classic": compute_classic, "space": compute_space, "random": compute_random,
         "gp": compute_gp, "rl": compute_rl, "combine": compute_combine, "decay": compute_decay, "theory": compute_theory,
         "envelope": compute_envelope}


if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
