"""Precompute everything numerical in Part 44 of *Computer Science, Built* ("People and Products").

    python -m videos.cs.cs44.compute              # everything missing
    python -m videos.cs.cs44.compute --force peeking

Results are cached in ``.cache/cs44/<name>.json``; scenes call ``load(name)``.  The instruments are
``explainer/cs/people/`` (hci, colour, experiments); tests in tests/test_cs44_people.py.

Items:
    fitts       simulated pointing by corrected submovements: movement time against log2(D/W + 1)
    edge        a target at the screen edge against the same target in the middle
    hick        choice by halving: reaction time against log2(n + 1); a skewed menu's entropy
    klm         keystroke-level predictions for four ways to do two tasks
    users       problems found by n test users: Nielsen–Landauer, and with problems of unequal visibility
    colour      this series' palette in OKLab and under three colour-vision deficiencies; contrast on the background
    gamma       code values against light; checks against published reference values
    size        sample sizes for detecting lifts on a 5% conversion rate
    power       simulated power at the computed sample size
    peeking     A/A tests checked daily: the false-positive rate by day, and p-value paths
    sequential  the mixture SPRT: false positives under peeking, and power
    cuped       variance with and without the pre-period covariate, for several correlations
    metrics     twenty metrics with no real effect: any false positive, naively and with Benjamini–Hochberg
    srm         a sample-ratio mismatch detected by chi-squared
    simpson     a redesign that wins in every segment and loses overall
    interference a marketplace with limited supply: the A/B estimate against the effect of launching to everyone
    privacy     randomized response: a deniable answer per person, the population rate recovered
    glyph       the word "Job" rasterized at 8-24 px, one bit per pixel and antialiased (PNG files)
    bandit      Thompson sampling against a 50/50 split: regret and precision
"""

from __future__ import annotations

from explainer.ai.cache import Cache

CACHE = Cache("cs44")
load = CACHE.load


def compute_fitts() -> dict:
    from explainer.cs.people import hci
    return hci.fitts_experiment()


def compute_edge() -> dict:
    from explainer.cs.people import hci
    return hci.edge_target()


def compute_hick() -> dict:
    from explainer.cs.people import hci
    return hci.hick_experiment()


def compute_klm() -> dict:
    from explainer.cs.people import hci
    return {"operators": hci.KLM, "cases": hci.klm_cases()}


def compute_users() -> dict:
    from explainer.cs.people import hci
    return {"uniform": hci.nielsen_landauer(), "varied": hci.heterogeneous()}


def compute_colour() -> dict:
    from explainer.cs.people import colour
    r = colour.palette_report()
    r["oklab"] = {n: colour.oklab(c) for n, c in colour.PALETTE.items()}
    return r


def compute_gamma() -> dict:
    from explainer.cs.people import colour
    return {**colour.gamma_ramp(), "checks": colour.checks()}


def compute_size() -> dict:
    from explainer.cs.people import experiments as E
    return {"rows": [E.sample_size(0.05, lift) for lift in (0.01, 0.02, 0.05, 0.1, 0.2)]}


def compute_power() -> dict:
    from explainer.cs.people import experiments as E
    return {"at_n": E.power_sim(0.05, 0.05), "half_n": E.power_sim(0.05, 0.05, n=59_651)}


def compute_peeking() -> dict:
    from explainer.cs.people import experiments as E
    return E.peeking(days=30, per_day=1000, trials=4000)


def compute_sequential() -> dict:
    from explainer.cs.people import experiments as E
    return {"null": E.msprt(lift=0.0, trials=4000), "lift10": E.msprt(lift=0.1, trials=4000),
            "lift10_tau": E.msprt(lift=0.1, tau2=(0.05 * 0.1) ** 2, trials=4000),
            "null_tau": E.msprt(lift=0.0, tau2=(0.05 * 0.1) ** 2, trials=4000),
            "fixed_n_lift10": E.sample_size(0.05, 0.1)}


def compute_cuped() -> dict:
    from explainer.cs.people import experiments as E
    return {"rows": [E.cuped(rho=r, trials=2000) for r in (0.0, 0.3, 0.5, 0.7, 0.9)]}


def compute_metrics() -> dict:
    from explainer.cs.people import experiments as E
    return E.many_metrics()


def compute_srm() -> dict:
    from explainer.cs.people import experiments as E
    return {"bad": E.srm(50_000, 49_000), "fine": E.srm(50_100, 49_900)}


def compute_simpson() -> dict:
    from explainer.cs.people import experiments as E
    return E.simpson()


def compute_bandit() -> dict:
    from explainer.cs.people import experiments as E
    return E.bandit(trials=200)


def compute_glyph() -> dict:
    """The word "Job" rasterized at small pixel sizes, as one bit per pixel and with grey-level antialiasing, each
    enlarged with visible pixels for the screen; saved as PNGs in the cache."""
    from PIL import Image, ImageDraw, ImageFont
    from explainer.tts import REPO_ROOT
    CACHE.dir.mkdir(parents=True, exist_ok=True)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    out = []
    for px in (8, 12, 16, 24):
        f = ImageFont.truetype(font_path, px)
        for mode in ("1", "L"):
            w, h = int(px * 2.4) + 4, int(px * 1.4)
            im = Image.new(mode, (w, h), 0)
            d = ImageDraw.Draw(im)
            if mode == "1":
                d.fontmode = "1"
            d.text((3, 0), "Job", font=f, fill=255 if mode == "L" else 1)
            im = im.convert("L")
            big = im.resize((w * 12, h * 12), Image.NEAREST)
            path = CACHE.dir / f"glyph_{px}_{'mono' if mode == '1' else 'aa'}.png"
            big.save(path)
            levels = len(set(im.getdata()))
            out.append({"px": px, "mode": "mono" if mode == "1" else "antialiased", "w": w, "h": h,
                        "grey_levels": levels, "png": str(path.relative_to(REPO_ROOT))})
    return {"rows": out}


def compute_interference() -> dict:
    from explainer.cs.people import experiments as E
    return {"limited": E.interference(supply=3000, trials=100), "ample": E.interference(supply=10_000, trials=100)}


def compute_privacy() -> dict:
    from explainer.cs.people import experiments as E
    return E.randomized_response()


ITEMS = {k[8:]: v for k, v in globals().items() if k.startswith("compute_")}

if __name__ == "__main__":
    CACHE.main(ITEMS, __doc__)
