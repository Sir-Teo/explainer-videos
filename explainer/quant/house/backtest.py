"""The House's backtester, and the statistics that keep a backtest honest (Part 26).

**The engine.**  :class:`Backtester` is event-driven: bar by bar it applies corporate actions (splits change the
share count, dividends pay cash to longs and charge shorts), fills the orders that are due (after a latency, at the
open or the close, paying half the spread, a square-root impact and a commission), marks the book, charges borrow on
short positions, and only then shows the strategy the history *up to and including* that bar: the strategy can never
see a later price, because it is never handed one.  :func:`vectorized` is the one-line alternative, right only when
its assumptions are.

**The statistics.**  The Sharpe ratio's standard error (Lo 2002; Mertens 2002 for skew and fat tails); the expected
maximum Sharpe ratio of ``n`` trials from extreme-value theory; the probabilistic and deflated Sharpe ratios (Bailey
and Lopez de Prado 2012, 2014); the minimum backtest length (Bailey, Borwein, Lopez de Prado and Zhu 2014); the
probability of backtest overfitting by combinatorially symmetric cross-validation (Bailey, Borwein, Lopez de Prado
and Zhu 2017); purged and embargoed k-fold cross-validation and walk-forward splits (Lopez de Prado 2018); and the
bootstrap reality checks of White (2000), Hansen (2005) and Romano and Wolf (2005), on Politis and Romano's (1994)
stationary bootstrap.

**The rules.**  A universe of technical trading rules in the families of Brock, Lakonishok and LeBaron (1992) and
Sullivan, Timmermann and White (1999): filters, moving-average crossovers, support and resistance, and channel
breakouts, each with bands, delays and holding periods; :func:`random_rules` draws from it and
:func:`rule_positions` runs one on a price series, point in time.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field

import numba
import numpy as np
from scipy import stats

EULER = 0.5772156649015329


# ---------------------------------------------------------------------------
# The Sharpe ratio and its error
# ---------------------------------------------------------------------------
def sharpe(r, periods: float = 1.0) -> float:
    """Mean over standard deviation (ddof 1), times sqrt(periods) to annualise."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    s = r.std(ddof=1)
    return float(r.mean() / s * math.sqrt(periods)) if s > 0 else 0.0


def sharpe_se(r, kind: str = "iid") -> float:
    """Standard error of the per-period Sharpe ratio estimate.  ``iid`` (Lo 2002): sqrt((1 + SR^2/2)/T) for normal
    returns.  ``nonnormal`` (Mertens 2002): sqrt((1 - g3 SR + (g4 - 1)/4 SR^2)/T), g3 the skewness and g4 the
    kurtosis (3 for the normal, which gives back the iid formula)."""
    r = np.asarray(r, float)
    r = r[np.isfinite(r)]
    T, sr = len(r), sharpe(r)
    if kind == "iid":
        return math.sqrt((1 + 0.5 * sr ** 2) / T)
    g3 = float(stats.skew(r))
    g4 = float(stats.kurtosis(r, fisher=False))
    return math.sqrt(max(1 - g3 * sr + (g4 - 1) / 4 * sr ** 2, 1e-12) / T)


def lo_eta(rho, q: int) -> float:
    """Lo's (2002) annualisation factor for autocorrelated returns: SR(q) = eta(q) SR, with
    eta(q) = q / sqrt(q + 2 sum_{k=1}^{q-1} (q - k) rho_k).  With rho = 0 it is sqrt(q), the usual rule."""
    rho = np.asarray(rho, float)
    s = q + 2 * sum((q - k) * rho[k - 1] for k in range(1, q))
    return float(q / math.sqrt(s))


def psr(sr: float, sr0: float, T: int, skew: float = 0.0, kurt: float = 3.0) -> float:
    """The probabilistic Sharpe ratio (Bailey and Lopez de Prado 2012): the probability that the true per-period
    Sharpe ratio exceeds ``sr0``, given an estimate ``sr`` from ``T`` observations with this skewness and kurtosis."""
    den = math.sqrt(max(1 - skew * sr + (kurt - 1) / 4 * sr ** 2, 1e-12))
    return float(stats.norm.cdf((sr - sr0) * math.sqrt(T - 1) / den))


def expected_max_sr(n: float, var: float = 1.0) -> float:
    """The expected maximum of ``n`` independent normal Sharpe estimates with mean zero and variance ``var``
    (Bailey and Lopez de Prado 2014, from the Gumbel limit): sqrt(var) ((1 - g) Z(1 - 1/n) + g Z(1 - 1/(n e)))."""
    if n <= 1:
        return 0.0
    z = stats.norm.ppf
    return float(math.sqrt(var) * ((1 - EULER) * z(1 - 1 / n) + EULER * z(1 - 1 / (n * math.e))))


def deflated_sharpe(sr: float, T: int, n: float, var: float, skew: float = 0.0, kurt: float = 3.0) -> dict:
    """The deflated Sharpe ratio (Bailey and Lopez de Prado 2014): the PSR of ``sr`` against the expected best of
    ``n`` trials whose Sharpe estimates have variance ``var`` (all per period)."""
    sr0 = expected_max_sr(n, var)
    return {"sr0": sr0, "dsr": psr(sr, sr0, T, skew, kurt)}


def min_btl(n: float, sr: float) -> float:
    """Minimum backtest length, in years, so that the best of ``n`` independent zero-skill configurations is not
    expected to show an annualised Sharpe ratio of ``sr`` (Bailey, Borwein, Lopez de Prado and Zhu 2014)."""
    return expected_max_sr(n, 1.0) ** 2 / sr ** 2


def noise_max_sr(n: int, T: int, sims: int = 2000, seed=0) -> np.ndarray:
    """The best per-period Sharpe ratio among ``n`` strategies of iid normal noise with ``T`` observations each,
    ``sims`` times: SR_hat = t / sqrt(T) with t Student-t on T - 1 degrees of freedom, exactly."""
    rng = np.random.default_rng(seed)
    out = np.empty(sims)
    for s in range(sims):
        out[s] = rng.standard_t(T - 1, size=n).max() / math.sqrt(T)
    return out


# ---------------------------------------------------------------------------
# Overfitting: CSCV, purged CV, walk-forward
# ---------------------------------------------------------------------------
def cscv(M, S: int = 16, max_combos: int | None = None, seed=0) -> dict:
    """Combinatorially symmetric cross-validation (Bailey, Borwein, Lopez de Prado and Zhu 2017).  ``M`` is T x N:
    the returns of N configurations.  Split the rows into S blocks; for every way of choosing S/2 of them as the
    in-sample set (the rest out of sample), pick the configuration with the best in-sample Sharpe ratio and find its
    relative rank w out of sample; the logit is ln(w / (1 - w)).  PBO is the share of logits <= 0: how often the
    in-sample winner is below the out-of-sample median."""
    M = np.asarray(M)
    T, N = M.shape
    edges = np.linspace(0, T, S + 1).astype(int)
    s1 = np.stack([M[a:b].sum(0, dtype=np.float64) for a, b in zip(edges[:-1], edges[1:])])          # S x N
    s2 = np.stack([np.square(M[a:b], dtype=np.float64).sum(0) for a, b in zip(edges[:-1], edges[1:])])
    cnt = np.diff(edges).astype(float)
    combos = list(itertools.combinations(range(S), S // 2))
    if max_combos is not None and len(combos) > max_combos:
        rng = np.random.default_rng(seed)
        combos = [combos[i] for i in sorted(rng.choice(len(combos), max_combos, replace=False))]
    logits, is_sr, oos_sr = [], [], []
    for c in combos:
        m = np.zeros(S, bool)
        m[list(c)] = True

        def sr(mask):
            n_ = cnt[mask].sum()
            mu = s1[mask].sum(0) / n_
            var = s2[mask].sum(0) / n_ - mu ** 2
            return mu / np.sqrt(np.maximum(var, 1e-18))
        a, b = sr(m), sr(~m)
        k = int(np.argmax(a))
        w = (np.sum(b < b[k]) + 0.5 * np.sum(b == b[k]) + 0.5) / (N + 1)  # relative rank in (0, 1)
        logits.append(math.log(w / (1 - w)))
        is_sr.append(a[k])
        oos_sr.append(b[k])
    logits = np.asarray(logits)
    return {"logits": logits, "pbo": float(np.mean(logits <= 0)), "is_sr": np.asarray(is_sr),
            "oos_sr": np.asarray(oos_sr), "n_combos": len(combos)}


def kfold(n: int, k: int, shuffle: bool = True, seed=0):
    """Plain k-fold splits of range(n): (train, test) index arrays."""
    idx = np.arange(n)
    if shuffle:
        idx = np.random.default_rng(seed).permutation(n)
    for f in np.array_split(idx, k):
        test = np.sort(f)
        yield np.setdiff1d(np.arange(n), test), test


def purged_kfold(t0, t1, k: int, embargo: int = 0):
    """Purged, embargoed k-fold (Lopez de Prado 2018, ch. 7).  Observation i's label spans [t0[i], t1[i]] (sorted by
    t0).  Folds are contiguous; a training observation is purged if its label span overlaps the test fold's span,
    and embargoed if it starts within ``embargo`` periods after the test fold ends."""
    t0, t1 = np.asarray(t0), np.asarray(t1)
    n = len(t0)
    for test in np.array_split(np.arange(n), k):
        a, b = t0[test].min(), t1[test].max()
        overlap = (t0 <= b) & (t1 >= a)
        emb = (t0 > b) & (t0 <= b + embargo)
        train = np.flatnonzero(~overlap & ~emb)
        yield train, test


def walk_forward(n: int, train: int, test: int, expanding: bool = True):
    """Walk-forward splits: fit on the past (all of it, or the last ``train`` periods), test on the next ``test``."""
    s = train
    while s < n:
        e = min(s + test, n)
        yield np.arange(0 if expanding else s - train, s), np.arange(s, e)
        s = e


# ---------------------------------------------------------------------------
# Reality checks on the stationary bootstrap
# ---------------------------------------------------------------------------
@numba.njit(cache=True)
def _sb_counts(T, B, p, seed):
    np.random.seed(seed)
    out = np.zeros((B, T), np.float32)
    for b in range(B):
        i = np.random.randint(T)
        for t in range(T):
            if t > 0:
                if np.random.random() < p:
                    i = np.random.randint(T)
                else:
                    i = (i + 1) % T
            out[b, i] += 1.0
    return out


def stationary_bootstrap_counts(T: int, B: int, mean_block: float = 10.0, seed=0) -> np.ndarray:
    """Politis and Romano's (1994) stationary bootstrap, as counts: row b says how many times each period appears
    in resample b (blocks of geometric length with mean ``mean_block``, wrapping round).  A resample's mean of any
    series x is counts[b] @ x / T, so thousands of strategies can be bootstrapped with one matrix product."""
    return _sb_counts(int(T), int(B), 1.0 / mean_block, int(seed))


def boot_means(d, counts, chunk: int = 2000) -> np.ndarray:
    """B x K resampled means of the T x K matrix ``d``."""
    d = np.asarray(d, np.float32)
    T, K = d.shape
    out = np.empty((counts.shape[0], K), np.float64)
    for a in range(0, K, chunk):
        out[:, a:a + chunk] = counts @ d[:, a:a + chunk] / T
    return out


def reality_check(mean, bmean, T: int) -> dict:
    """White's (2000) reality check: H0 that no strategy beats the benchmark.  ``mean`` (K) are the sample mean
    differentials, ``bmean`` (B x K) their bootstrap means.  V = sqrt(T) max_k mean_k; V*_b = sqrt(T) max_k
    (bmean_bk - mean_k); the p-value is the share of V* at or above V."""
    mean = np.asarray(mean)
    V = math.sqrt(T) * mean.max()
    Vb = math.sqrt(T) * (bmean - mean).max(axis=1)
    return {"V": float(V), "p": float(np.mean(Vb >= V)), "best": int(np.argmax(mean))}


def spa(mean, bmean, sd, T: int) -> dict:
    """Hansen's (2005) test of superior predictive ability, consistent version: studentised by each strategy's
    standard deviation ``sd``, and strategies that are clearly worse than the benchmark (mean below
    -sd sqrt(2 ln ln T / T)) are not allowed to inflate the null distribution."""
    mean, sd = np.asarray(mean), np.asarray(sd)
    tstat = math.sqrt(T) * mean / sd
    stat = max(0.0, float(tstat.max()))
    keep = mean >= -sd * math.sqrt(2 * math.log(math.log(T)) / T)
    g = np.where(keep, mean, 0.0)        # recentre the plausible strategies; leave the clearly poor ones negative
    zb = math.sqrt(T) * (bmean - g) / sd
    sb = np.maximum(0.0, zb.max(axis=1))
    return {"stat": stat, "p": float(np.mean(sb >= stat)), "best": int(np.argmax(tstat))}


def romano_wolf(mean, bmean, sd, T: int, alpha: float = 0.05) -> dict:
    """Romano and Wolf's (2005) studentised step-down: reject every strategy whose t exceeds the (1 - alpha)
    bootstrap quantile of the maximum t over the strategies not yet rejected; repeat until none is added.  Controls
    the familywise error rate, with more power than a single-step check."""
    mean, sd = np.asarray(mean), np.asarray(sd)
    t = math.sqrt(T) * mean / sd
    tb = math.sqrt(T) * (bmean - mean) / sd
    active = np.ones(len(t), bool)
    rejected = np.zeros(len(t), bool)
    crit = []
    while active.any():
        c = float(np.quantile(tb[:, active].max(axis=1), 1 - alpha))
        crit.append(c)
        new = active & (t > c)
        if not new.any():
            break
        rejected |= new
        active &= ~new
    return {"rejected": np.flatnonzero(rejected), "crit": crit, "t": t}


# ---------------------------------------------------------------------------
# Technical trading rules (Brock, Lakonishok and LeBaron 1992; Sullivan, Timmermann and White 1999)
# ---------------------------------------------------------------------------
FILTER_X = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.12,
            0.14, 0.16, 0.18, 0.2, 0.25, 0.3, 0.4, 0.5]
MA_N = [2, 5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200, 250]
SR_N = [5, 10, 15, 20, 25, 50, 100, 150, 200, 250]
CB_N = [5, 10, 15, 20, 25, 50, 100, 150, 200, 250]
CB_X = [0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15]
BANDS = [0.0, 0.001, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]
DELAYS = [0, 2, 3, 4, 5]
HOLDS = [0, 5, 10, 25, 50]
FAMILIES = ("filter", "ma", "sr", "cb")


def rule_grid() -> list[dict]:
    """Every rule in the House's universe: four families, with bands, delays and holding periods (0 = hold until
    the opposite signal).  Shorts are allowed: a position is +1, 0 or -1."""
    rules = []
    for x, d, c in itertools.product(FILTER_X, DELAYS, HOLDS):
        rules.append({"family": "filter", "x": x, "delay": d, "hold": c})
    for (n1, n2), b, d, c in itertools.product([(a, b) for a in [1] + MA_N for b in MA_N if a < b], BANDS, DELAYS, HOLDS):
        rules.append({"family": "ma", "fast": n1, "slow": n2, "band": b, "delay": d, "hold": c})
    for n, b, d, c in itertools.product(SR_N, BANDS, DELAYS, HOLDS):
        rules.append({"family": "sr", "n": n, "band": b, "delay": d, "hold": c})
    for n, x, b, c in itertools.product(CB_N, CB_X, BANDS, HOLDS[1:]):
        rules.append({"family": "cb", "n": n, "x": x, "band": b, "hold": c})
    return rules


def random_rules(n: int, seed=0) -> list[dict]:
    """``n`` rules drawn without replacement from :func:`rule_grid`, spread as evenly over the four families as
    their sizes allow (a family smaller than its share is taken whole, and the rest shared among the others)."""
    rng = np.random.default_rng(seed)
    grid = rule_grid()
    pools = {f: [r for r in grid if r["family"] == f] for f in FAMILIES}
    take, left, fams = {}, n, sorted(FAMILIES, key=lambda f: len(pools[f]))
    for i, f in enumerate(fams):
        k = min(len(pools[f]), left // (len(fams) - i))
        take[f] = k
        left -= k
    out = []
    for f in FAMILIES:
        pool = pools[f]
        out += [pool[i] for i in sorted(rng.choice(len(pool), take[f], replace=False))]
    return out


def rule_label(r: dict) -> str:
    f = r["family"]
    tail = (f", delay {r['delay']}" if r.get("delay") else "") + (f", hold {r['hold']}d" if r.get("hold") else "")
    if f == "filter":
        return f"filter {100 * r['x']:g}%" + tail
    if f == "ma":
        return f"MA {r['fast']}/{r['slow']}, band {100 * r['band']:g}%" + tail
    if f == "sr":
        return f"support/resistance {r['n']}d, band {100 * r['band']:g}%" + tail
    return f"channel {r['n']}d, width {100 * r['x']:g}%, band {100 * r['band']:g}%" + tail


@numba.njit(cache=True)
def _apply(trig, delay, hold):
    """Positions from raw triggers (+1 buy, -1 sell, 0 none): a trigger acts only after it has held ``delay``
    consecutive days; with ``hold`` > 0 a position is kept that many days and then closed, ignoring other signals;
    with ``hold`` = 0 it is kept until the opposite trigger."""
    T = len(trig)
    pos = np.zeros(T, np.int8)
    p, left, run, last = 0, 0, 0, 0
    for t in range(T):
        g = trig[t]
        if g != 0 and g == last:
            run += 1
        elif g != 0:
            run = 1
        else:
            run = 0
        last = g
        act = g != 0 and run == max(delay, 1)   # the day the trigger first completes its delay
        if hold > 0:
            if left > 0:
                left -= 1
                if left == 0:
                    p = 0
            elif act:
                p = g
                left = hold
        elif act:
            p = g
        pos[t] = p
    return pos


@numba.njit(cache=True)
def _filter_trig(P, x):
    """A filter rule: buy when the price rises x above its lowest close since the last signal, sell when it falls x
    below its highest; the extremes reset at each signal (Alexander 1961, Fama and Blume 1966)."""
    T = len(P)
    trig = np.zeros(T, np.int8)
    hi, lo, state = P[0], P[0], 0
    for t in range(1, T):
        if P[t] > hi:
            hi = P[t]
        if P[t] < lo:
            lo = P[t]
        if state <= 0 and P[t] >= lo * (1 + x):
            state = 1
            hi = P[t]
        elif state >= 0 and P[t] <= hi * (1 - x):
            state = -1
            lo = P[t]
        trig[t] = state
    return trig


def _rolling(P, n, fn):
    from numpy.lib.stride_tricks import sliding_window_view
    out = np.full(len(P), np.nan)
    if len(P) > n:
        out[n:] = fn(sliding_window_view(P[:-1], n), axis=1)[: len(P) - n]  # the n closes before t
    return out


class RuleEngine:
    """Runs many rules on one price series, sharing the moving averages and rolling extremes between them."""

    def __init__(self, price):
        self.P = np.asarray(price, float)
        c = np.concatenate([[0.0], np.cumsum(self.P)])
        self._ma = {}
        self._mx, self._mn = {}, {}
        self._c = c

    def ma(self, n):
        if n not in self._ma:
            m = np.full(len(self.P), np.nan)
            m[n - 1:] = (self._c[n:] - self._c[:-n]) / n
            self._ma[n] = m
        return self._ma[n]

    def mx(self, n):
        if n not in self._mx:
            self._mx[n] = _rolling(self.P, n, np.max)
            self._mn[n] = _rolling(self.P, n, np.min)
        return self._mx[n], self._mn[n]

    def positions(self, r: dict) -> np.ndarray:
        P, f = self.P, r["family"]
        if f == "filter":
            trig = _filter_trig(P, r["x"])
            # the filter's state is itself a position; delay and hold act on its changes
            return _apply(trig, r["delay"], r["hold"])
        if f == "ma":
            a, b = self.ma(r["fast"]), self.ma(r["slow"])
            with np.errstate(invalid="ignore"):
                trig = np.where(a > b * (1 + r["band"]), 1, np.where(a < b * (1 - r["band"]), -1, 0))
        elif f == "sr":
            hi, lo = self.mx(r["n"])
            with np.errstate(invalid="ignore"):
                trig = np.where(P > hi * (1 + r["band"]), 1, np.where(P < lo * (1 - r["band"]), -1, 0))
        else:
            hi, lo = self.mx(r["n"])
            with np.errstate(invalid="ignore"):
                chan = (hi - lo) / lo <= r["x"]
                trig = np.where(chan & (P > hi * (1 + r["band"])), 1,
                                np.where(chan & (P < lo * (1 - r["band"])), -1, 0))
        return _apply(trig.astype(np.int8), r.get("delay", 0), r["hold"])


def rule_positions(price, rule: dict) -> np.ndarray:
    """One rule's position at each close (+1, 0, -1), from closes up to and including that day only."""
    return RuleEngine(price).positions(rule)


def rule_returns(pos, excess) -> np.ndarray:
    """The rule's return: the position held at close t earns the next day's excess return, r_{t+1} s_t."""
    pos = np.asarray(pos, float)
    out = np.zeros(len(pos))
    out[1:] = pos[:-1] * np.asarray(excess, float)[1:]
    return out


# ---------------------------------------------------------------------------
# The event-driven backtester
# ---------------------------------------------------------------------------
@dataclass
class Costs:
    half_spread_bps: float = 0.0     # paid on every fill
    impact: float = 0.0              # square-root impact: impact * daily vol * sqrt(shares / ADV)
    commission_per_share: float = 0.0
    borrow_bps_year: float = 0.0     # charged daily on the value of short positions


@dataclass
class Result:
    date: np.ndarray
    equity: np.ndarray
    shares: np.ndarray
    trades: list = field(default_factory=list)
    costs: dict = field(default_factory=dict)

    @property
    def returns(self):
        e = self.equity
        return np.concatenate([[0.0], e[1:] / e[:-1] - 1])


class Backtester:
    """An event-driven backtest of one instrument.  ``bars`` holds arrays ``date``, ``open``, ``high``, ``low``,
    ``close``, ``volume`` and optionally ``dividend`` (cash per share, on the ex-date) and ``split`` (new shares per
    old share, effective at that bar's open; 1 when none).  ``strategy(view)`` receives a dict of the bars up to and
    including the current close and returns a target weight of equity (or None to do nothing).  Orders fill
    ``latency`` bars later at ``fill`` ('open' or 'close'), with :class:`Costs`; ``adjust_splits=False`` plants the
    classic error of ignoring the split events (the share count is not changed)."""

    def __init__(self, bars: dict, strategy, cash: float = 1e6, latency: int = 1, fill: str = "open",
                 costs: Costs | None = None, adjust_splits: bool = True, warmup: int = 1):
        self.b = {k: np.asarray(v) for k, v in bars.items()}
        n = len(self.b["close"])
        self.b.setdefault("dividend", np.zeros(n))
        self.b.setdefault("split", np.ones(n))
        self.strategy, self.cash0, self.latency, self.fill = strategy, cash, latency, fill
        self.costs, self.adjust_splits, self.warmup = costs or Costs(), adjust_splits, warmup

    def run(self) -> Result:
        b, c = self.b, self.costs
        n = len(b["close"])
        cash, sh = self.cash0, 0.0
        due: dict[int, float] = {}
        equity, shares, trades = np.empty(n), np.empty(n), []
        paid = {"spread": 0.0, "impact": 0.0, "commission": 0.0, "borrow": 0.0, "dividends": 0.0}
        lr = np.diff(np.log(b["close"]), prepend=np.log(b["close"][0]))
        adv = np.convolve(b["volume"].astype(float), np.ones(20) / 20, mode="full")[:n]
        for t in range(n):
            # 1. corporate actions at the open
            if self.adjust_splits and b["split"][t] != 1.0:
                sh *= b["split"][t]
                due = {k: v * b["split"][t] for k, v in due.items()}
            if b["dividend"][t] and sh:
                cash += sh * b["dividend"][t]
                paid["dividends"] += sh * b["dividend"][t]
            # 2. fills
            q = due.pop(t, 0.0)
            if q:
                cash, sh = self._fill(t, q, b[self.fill][t], cash, sh, lr, adv, paid, trades)
            # 3. mark, borrow
            if sh < 0:
                fee = c.borrow_bps_year * 1e-4 / 252 * (-sh) * b["close"][t]
                cash -= fee
                paid["borrow"] += fee
            eq = cash + sh * b["close"][t]
            equity[t], shares[t] = eq, sh
            # 4. the strategy sees bars 0..t only
            if t >= self.warmup and t + max(self.latency, 0) < n:
                view = {k: v[: t + 1] for k, v in b.items()}
                w = self.strategy(view)
                if w is not None:
                    target = w * eq / b["close"][t]
                    pending = sum(due.values())
                    dq = target - sh - pending
                    if abs(dq) * b["close"][t] > 1e-6 * max(eq, 1.0):
                        if self.latency == 0:   # the vectorised assumption: filled at the close it was computed from
                            cash, sh = self._fill(t, dq, b["close"][t], cash, sh, lr, adv, paid, trades)
                            equity[t], shares[t] = cash + sh * b["close"][t], sh
                        else:
                            due[t + self.latency] = due.get(t + self.latency, 0.0) + dq
        return Result(b["date"], equity, shares, trades, paid)

    def _fill(self, t, q, px, cash, sh, lr, adv, paid, trades):
        c, b = self.costs, self.b
        vol = lr[max(1, t - 21):t].std() if t > 3 else 0.01
        part = abs(q) / max(adv[t - 1] if t else b["volume"][t], 1.0)
        sp = c.half_spread_bps * 1e-4 * px * abs(q)
        im = c.impact * vol * math.sqrt(part) * px * abs(q)
        cm = c.commission_per_share * abs(q)
        paid["spread"] += sp
        paid["impact"] += im
        paid["commission"] += cm
        trades.append((int(b["date"][t]), float(q), float(px)))
        return cash - q * px - sp - im - cm, sh + q


def vectorized(weights, close, cost_bps: float = 0.0, lag: int = 1) -> np.ndarray:
    """The vectorised backtest: the weight decided at close t earns close-to-close returns from t + lag - 1 to
    t + lag, less ``cost_bps`` on each change of weight.  ``lag=0`` is the look-ahead bug: today's signal earns
    today's return."""
    w = np.asarray(weights, float)
    r = np.concatenate([[0.0], np.asarray(close[1:], float) / np.asarray(close[:-1], float) - 1])
    out = np.zeros(len(w))
    if lag == 0:
        out = w * r
    else:
        out[lag:] = w[:-lag] * r[lag:]
    cost = cost_bps * 1e-4 * np.abs(np.diff(w, prepend=0.0))   # paid on the change decided at close t
    if lag == 0:
        out -= cost
    else:
        out[lag:] -= cost[:-lag]
    return out


# ---------------------------------------------------------------------------
# Planted alpha, and survivorship
# ---------------------------------------------------------------------------
def planted_market(n: int, n_true: int, sr_true: float, T: int, rho: float = 0.0, seed=0) -> dict:
    """A simulated market of ``n`` strategies, ``T`` days each, with unit daily volatility: ``n_true`` of them have
    an annualised Sharpe ratio of ``sr_true`` planted in them, the rest none; all share a common factor with
    correlation ``rho``.  Returns the T x n returns and which were planted."""
    rng = np.random.default_rng(seed)
    f = rng.standard_normal((T, 1))
    e = rng.standard_normal((T, n))
    R = math.sqrt(rho) * f + math.sqrt(1 - rho) * e
    planted = np.zeros(n, bool)
    planted[rng.choice(n, n_true, replace=False)] = True
    R[:, planted] += sr_true / math.sqrt(252)
    return {"R": R, "planted": planted}


def survivorship(n: int = 5000, years: int = 8, sig_lo: float = 0.05, sig_hi: float = 0.35, cut: float = -0.3,
                 seed=0) -> dict:
    """Brown, Goetzmann, Ibbotson and Ross (1992), simulated: ``n`` managers with no skill (log returns of mean zero)
    and annual volatilities spread from ``sig_lo`` to ``sig_hi``; a manager whose cumulative return ever falls below
    ``cut`` leaves the database, and their record goes with them.  Returns the annual log returns, the volatilities
    and who survived."""
    rng = np.random.default_rng(seed)
    sig = rng.uniform(sig_lo, sig_hi, n)
    r = rng.standard_normal((n, years)) * sig[:, None]
    alive = np.minimum.accumulate(np.cumsum(r, axis=1), axis=1)[:, -1] > np.log1p(cut)
    return {"r": r, "sigma": sig, "alive": alive}
