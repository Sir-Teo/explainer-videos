"""Monochord's money (Part 60, *The Business of Music*).

Every number here is a model on illustrative terms, dated 2026, mostly American; it is not legal or financial advice.
The point is the arithmetic: where a subscription goes, how long an advance takes to repay, what two ways of dividing a
streaming pool do to different artists, how social influence makes hits unequal and unpredictable, what a quartet's
productivity has to do with ticket prices, and how often two melodies written independently coincide.

    Terms, waterfall, per_million           one subscription and one million streams, divided among their claimants
    recoup                                  an artist's account under a label deal, stream by stream
    population, pro_rata, user_centric      a simulated service's month, divided two ways
    musiclab                                Salganik, Dodds and Watts's experiment in cumulative advantage, simulated
    gini, top_share                         inequality of a market
    baumol                                  the cost disease: a performance's relative price when productivity elsewhere grows
    tickets                                 face value against a market-clearing or dynamic price; who keeps the difference
    collision, effective_melodies           how many distinct k-note melodies a melody model really makes
    shared_window_prob                      the chance two songs share some k-note phrase somewhere

No manim.  Checked in ``tests/music/test_business.py``.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

import numpy as np


# --------------------------------------------------------------------------------------------- the waterfall
@dataclass
class Terms:
    """Illustrative terms (2026; US-style).  Shares are fractions of what reaches each party."""
    price: float = 11.99                 # an individual premium subscription, per month (US dollars)
    service: float = 0.30                # the service keeps this share of revenue
    publishing: float = 0.15             # of revenue, to the composition (mechanical + performance); the rest of the
                                         # rights holders' share goes to the recording
    distributor: float = 0.0             # a distributor's fee, as a share of the recording's money (label deal: none)
    artist_royalty: float = 0.18         # a label deal: the artist's royalty, as a share of the label's receipts
    producer_points: float = 0.03        # the producer's royalty, from the same receipts
    publisher: float = 0.25              # the publisher's share of the composition's money (a co-publishing deal)
    society: float = 0.10                # the collecting societies' and administrators' costs, on the composition
    writers: int = 3                     # songwriters sharing the writer's share equally

    def recording(self) -> float:
        return 1 - self.service - self.publishing


def waterfall(gross: float, t: Terms = Terms()) -> list[dict]:
    """Divide ``gross`` revenue (a month's subscription, or what a number of streams earned) among its claimants.
    Returns rows (who, amount, of what), in the order the money flows."""
    rows = [{"who": "the service", "amount": gross * t.service}]
    rec = gross * t.recording()
    dist = rec * t.distributor
    label_in = rec - dist
    artist = label_in * t.artist_royalty
    producer = label_in * t.producer_points
    rows += [{"who": "the distributor", "amount": dist},
             {"who": "the label", "amount": label_in - artist - producer},
             {"who": "the artist (credited, against the advance)", "amount": artist},
             {"who": "the producer", "amount": producer}]
    pub = gross * t.publishing
    society = pub * t.society
    after = pub - society
    publisher = after * t.publisher
    writers = after - publisher
    rows += [{"who": "collecting societies and administrators", "amount": society},
             {"who": "the publisher", "amount": publisher},
             {"who": f"the songwriters ({t.writers})", "amount": writers},
             {"who": "each songwriter", "amount": writers / t.writers, "part": True}]
    return rows


def per_million(rate: float, t: Terms = Terms()) -> dict:
    """What a million streams pay each claimant when the service pays ``rate`` per stream to all rights holders
    (recording and composition together)."""
    gross = 1e6 * rate / (1 - t.service)
    return {r["who"]: r["amount"] for r in waterfall(gross, t)}


def recoup(advance: float, streams, rate_label: float, royalty: float = 0.18, costs: float = 0.0) -> dict:
    """An artist's account: ``advance`` plus recoupable ``costs`` are charged; each stream credits ``royalty`` of what
    the label receives (``rate_label`` per stream).  The artist is paid nothing more until the account is positive.
    Returns the balance after each count of streams, and the streams needed to recoup."""
    streams = np.asarray(streams, float)
    credit = streams * rate_label * royalty
    balance = credit - advance - costs
    need = (advance + costs) / (rate_label * royalty)
    label = streams * rate_label * (1 - royalty) - advance - costs   # the label's position: its share, less what it paid
    return {"balance": balance, "need": need, "paid_beyond_advance": np.maximum(balance, 0.0), "label": label}


# --------------------------------------------------------------------------------------------- dividing the pool
@dataclass
class Population:
    fees: np.ndarray                    # what each user's month pays the rights holders
    plays: np.ndarray                   # users x artists: streams in the month
    groups: list = field(default_factory=list)      # each artist's group name
    kinds: list = field(default_factory=list)       # each user's kind


def population(n_users: int = 4000, seed: int = 0, bots: int = 20, bot_streams: int = 14000,
               price: float = 11.99, service: float = 0.30, free_share: float = 0.45, free_fee: float = 0.3) -> Population:
    """A month on a simulated service.  Three kinds of listener: younger heavy users who mostly stream the charts;
    lighter users who listen to niche artists (jazz, classical, local scenes); and free users (ads pay much less).
    Plus ``bots`` fraudulent premium accounts that stream one fake artist all month.  Artists: 20 chart stars, 200 niche
    artists, 1 fake.  Streams per user are lognormal; within a group, artists are chosen with Zipf weights."""
    rng = np.random.default_rng(seed)
    stars, niche = 20, 200
    groups = ["chart"] * stars + ["niche"] * niche + ["fraud"]
    A = len(groups)
    wz_s = 1 / np.arange(1, stars + 1)
    wz_n = 1 / np.arange(1, niche + 1) ** 0.8
    fees, kinds, rows = [], [], []
    for u in range(n_users):
        r = rng.random()
        if r < free_share:
            kind, fee, mu, chart = "free", free_fee, math.log(400), 0.75
        elif r < free_share + (1 - free_share) * 0.55:
            kind, fee, mu, chart = "heavy", price * (1 - service), math.log(1800), 0.85
        else:
            kind, fee, mu, chart = "light", price * (1 - service), math.log(300), 0.15
        n = int(rng.lognormal(mu, 0.6))
        k_chart = rng.binomial(n, chart)
        row = np.zeros(A)
        if k_chart:
            row[:stars] = rng.multinomial(k_chart, wz_s / wz_s.sum())
        if n - k_chart:
            # each user has a few favourite niche artists
            fav = rng.choice(niche, size=6, replace=False, p=wz_n / wz_n.sum())
            row[stars + fav] = rng.multinomial(n - k_chart, np.full(6, 1 / 6))
        fees.append(fee)
        kinds.append(kind)
        rows.append(row)
    for b in range(bots):
        row = np.zeros(A)
        row[-1] = bot_streams
        fees.append(price * (1 - service))
        kinds.append("bot")
        rows.append(row)
    return Population(np.array(fees), np.array(rows), groups, kinds)


def pro_rata(p: Population) -> np.ndarray:
    """One pool: every fee together, divided by each artist's share of all streams."""
    total = p.plays.sum()
    return p.fees.sum() * p.plays.sum(axis=0) / total


def user_centric(p: Population) -> np.ndarray:
    """Each user's fee divided among the artists that user played (a user who played nothing pays no one, here)."""
    per_user = p.plays.sum(axis=1, keepdims=True)
    share = np.divide(p.plays, per_user, out=np.zeros_like(p.plays), where=per_user > 0)
    return (share * p.fees[:, None]).sum(axis=0)


def by_group(p: Population, payout: np.ndarray) -> dict:
    out = defaultdict(float)
    for g, v in zip(p.groups, payout):
        out[g] += float(v)
    return dict(out)


# --------------------------------------------------------------------------------------------- cumulative advantage
def gini(x) -> float:
    x = np.sort(np.asarray(x, float))
    n = len(x)
    if x.sum() == 0:
        return 0.0
    return float((2 * np.arange(1, n + 1) - n - 1) @ x / (n * x.sum()))


def top_share(x, frac: float) -> float:
    x = np.sort(np.asarray(x, float))[::-1]
    k = max(1, int(round(frac * len(x))))
    return float(x[:k].sum() / x.sum())


def musiclab(songs: int = 48, participants: int = 700, worlds: int = 8, influence: float = 0.8, seed: int = 0,
             appeal=None, quality=None) -> dict:
    """Salganik, Dodds and Watts (Science, 2006): participants arrive one by one, choose a song to listen to, and
    download it with a probability set by its quality.  In the independent world they choose by the song's appeal
    alone; in each social-influence world, partly (``influence``) by the downloads so far, as a ranked list shows them.
    Returns market shares per world, Gini coefficients and the unpredictability U (the mean, over songs, of the mean
    absolute difference in market share between pairs of social worlds)."""
    rng = np.random.default_rng(seed)
    if quality is None:
        quality = rng.beta(2, 5, songs)
    if appeal is None:
        appeal = 0.5 + 0.5 * quality + 0.3 * rng.random(songs)       # appeal is related to quality, loosely
    appeal = np.asarray(appeal, float)

    def world(w, social):
        r = np.random.default_rng(seed * 1000 + w + (0 if social else 777))
        d = np.zeros(songs)
        for _ in range(participants):
            base = appeal / appeal.sum()
            if social:
                pop = (d + 1) / (d + 1).sum()
                p = influence * pop + (1 - influence) * base
            else:
                p = base
            i = r.choice(songs, p=p)
            if r.random() < quality[i]:
                d[i] += 1
        return d

    social = [world(w, True) for w in range(worlds)]
    indep = [world(w, False) for w in range(2)]
    share = lambda d: d / max(d.sum(), 1)

    def unpredictability(ds):
        sh = np.array([share(d) for d in ds])
        tot, k = 0.0, 0
        for a in range(len(sh)):
            for b in range(a + 1, len(sh)):
                tot += np.abs(sh[a] - sh[b]).mean()
                k += 1
        return tot / max(k, 1)

    return {"quality": quality, "appeal": appeal, "social": [share(d) for d in social], "independent": [share(d) for d in indep],
            "gini_social": float(np.mean([gini(d) for d in social])), "gini_independent": float(np.mean([gini(d) for d in indep])),
            "U_social": unpredictability(social), "U_independent": unpredictability(indep),
            "winners": [int(np.argmax(d)) for d in social]}


# --------------------------------------------------------------------------------------------- live music
def baumol(years, growth: float = 0.02, start: int = 1790) -> np.ndarray:
    """The cost disease (Baumol and Bowen, 1966): a quartet still needs four players and the same half hour, while
    output per hour elsewhere grows by ``growth`` a year and wages follow it; so a performance's price relative to
    manufactured goods grows as exp(growth (year - start))."""
    years = np.asarray(years, float)
    return np.exp(growth * (years - start))


def tickets(seats: int = 20000, fans: int = 60000, median: float = 120.0, sigma: float = 0.8, face: float = 90.0,
            resellers: float = 0.25, seed: int = 0) -> dict:
    """A tour date with more fans than seats.  Fans' willingness to pay is lognormal.  Three ways to sell:
    *face*: a fixed price under the market; seats go at random to those willing to pay it, a share ``resellers`` of
    them bought by resellers who sell on at the market-clearing price; *clearing*: one price at which demand equals the
    seats; *dynamic*: each seat to the highest bidders, each at their own willingness (an upper bound on what any
    pricing can take).  Returns revenue to the artist side, to resellers, fans' surplus, and who gets in."""
    rng = np.random.default_rng(seed)
    wtp = np.sort(rng.lognormal(math.log(median), sigma, fans))[::-1]
    clearing = float(wtp[seats - 1])
    keen = wtp[wtp >= face]
    rng.shuffle(keen)
    sold = keen[:seats]
    n_resale = int(round(resellers * len(sold)))
    # resold seats go to the highest-paying fans who did not get one at face value
    left = np.sort(np.r_[keen[seats:], wtp[wtp < face]])[::-1]
    buyers = left[:n_resale]
    resale_price = float(buyers[-1]) if n_resale else clearing
    face_artist = face * len(sold)
    face_resale = (resale_price - face) * n_resale
    face_surplus = float((sold[n_resale:] - face).sum() + (buyers - resale_price).sum())
    top = wtp[:seats]
    return {"clearing": clearing, "face": face, "seats": seats,
            "face_value": {"artist": face_artist, "resellers": face_resale, "fans": face_surplus},
            "clearing_price": {"artist": clearing * seats, "resellers": 0.0, "fans": float((top - clearing).sum())},
            "dynamic": {"artist": float(top.sum()), "resellers": 0.0, "fans": 0.0},
            "resale_price": resale_price}


# --------------------------------------------------------------------------------------------- how many melodies
def collision(model, k: int) -> float:
    """The probability that two melodies drawn independently from ``model`` (Part 14's NGram) have the same first k
    notes: sum over k-note sequences s of P(s)^2, by dynamic programming over the model's context (its last
    ``order`` notes)."""
    order = model.order
    S = {(): 1.0}                       # context -> sum of P(prefix)^2 over prefixes with that context
    for _ in range(k):
        nxt: dict = defaultdict(float)
        for ctx, v in S.items():
            d = model.distribution(ctx)
            for x, px in d.items():
                if px <= 0:
                    continue
                c2 = (ctx + (x,))[-order:] if order else ()
                nxt[c2] += v * px * px
        S = nxt
    return float(sum(S.values()))


def effective_melodies(model, k: int) -> float:
    """1 / collision: the number of equally likely melodies that would collide as often."""
    return 1.0 / collision(model, k)


def shared_window_prob(q: float, windows_a: int, windows_b: int) -> float:
    """The chance that some k-note window of one song equals some k-note window of another, treating the windows as
    independent draws with collision probability ``q`` (an approximation: it ignores overlaps within a song)."""
    return float(-math.expm1(-windows_a * windows_b * q))


def birthday(q: float, songs: float) -> float:
    """The expected number of pairs among ``songs`` that share their k-note opening."""
    return songs * (songs - 1) / 2 * q
