"""Helpers shared by the scenes of Part 31 ("Can We Trust It?"), the finale of *AI, Built*."""

from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403

from .compute import load  # noqa: F401

PART = 31
MONO = "DejaVu Sans Mono"

# one meaning per colour, for the whole part
TRUTH = C.TRUE_P  # the true value: true strengths, gold, the world
EST = C.MODEL_Q  # an estimate of it: a rating, a measured score
CI = C.INTERVAL  # confidence intervals, bootstrap resamples
LEAK = C.PENALTY  # contamination, leaked text, a backdoor, a hack
CLEAN = C.TRUE_P  # clean, unseen text
JUDGE = C.KL  # a judge (person or model), an auditor
WEAK = GREY_B  # the weak supervisor
STRONG = C.NEURAL  # the strong student
CEIL = C.REWARD  # the ceiling: the strong model on the truth
RED = C.PENALTY  # the red team, the untrusted model's attacks
BLUE = C.TRUE_P  # the blue team, its protocol
TRUSTED = C.REWARD  # the trusted model
HACK = C.PENALTY  # the gamed objective
INTENDED = C.REWARD  # what was meant
SECRET = C.SURPRISE  # a planted secret, memorized text
PRIVATE = C.INTERVAL  # differential privacy
FUTURE = C.CONTEXT  # forecasts, extrapolations

# ten simulated models, A (weakest) to J, for the arena and the judge
ARENA_COLORS = ["#7F8EA3", "#58A6FF", "#5BD17A", "#9BE37B", "#E8C547", "#FF9F45", "#FF6B8B", "#D4A5FF", "#B39DDB",
                "#F2A541"]


def node_box(text: str, color, font_size=24, pad=0.22, height=0.62) -> VGroup:
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 2 * pad, height=max(height, t.height + 0.25), corner_radius=0.12,
                           stroke_color=color, stroke_width=2.2, fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


def tagline(text: str, corner=DR, font_size=20) -> Tex:
    """The 'computed' / 'simulated' / 'schematic' / 'published' tag in a corner."""
    return note(text, font_size=font_size).to_corner(corner, buff=0.2)


def stat_card(value: str, caption: str, color, width=3.2, value_size=44, caption_size=20) -> VGroup:
    """A big number over a caption, in a dark rounded box."""
    v = MathTex(value, font_size=value_size, color=color)
    c = label(caption, font_size=caption_size, color=GREY_A)
    if c.width > width - 0.3:
        c.width = width - 0.3
    body = VGroup(v, c).arrange(DOWN, buff=0.15)
    box = RoundedRectangle(width=width, height=body.height + 0.45, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.6, fill_color="#0B0F17", fill_opacity=0.94)
    return VGroup(box, body.move_to(box))


def interval_bar(ax, y, lo, hi, color, est=None, stroke_width=5, dot_r=0.06) -> VGroup:
    """A horizontal confidence interval on axes ``ax`` at height y, with its estimate as a dot."""
    g = VGroup(Line(ax.c2p(lo, y), ax.c2p(hi, y), color=color, stroke_width=stroke_width))
    for x in (lo, hi):
        g.add(Line(ax.c2p(x, y) + UP * 0.08, ax.c2p(x, y) + DOWN * 0.08, color=color, stroke_width=3))
    if est is not None:
        g.add(Dot(ax.c2p(est, y), radius=dot_r, color=WHITE))
    return g


def hist_bars(ax, values, bins, color, opacity=0.8, scale=1.0, ymax=None) -> VGroup:
    """A histogram of ``values`` drawn as bars on ``ax`` (counts normalized to a density, times ``scale``)."""
    h, e = np.histogram(values, bins=bins, density=True)
    h = h * scale
    if ymax is not None:
        h = np.minimum(h, ymax)
    g = VGroup()
    for k in range(len(h)):
        if h[k] <= 0:
            continue
        p0, p1 = ax.c2p(e[k], 0), ax.c2p(e[k + 1], h[k])
        g.add(Rectangle(width=max(p1[0] - p0[0], 0.005), height=max(p1[1] - p0[1], 0.005), stroke_width=0,
                        fill_color=color, fill_opacity=opacity).move_to((p0 + p1) / 2))
    return g


def wrap_data(text: str, chars: int = 46, font_size: int = 20, color=WHITE, max_lines: int = 4) -> Text:
    """Words a model read or wrote, monospaced and wrapped: data, never translated."""
    import textwrap

    lines = textwrap.wrap(" ".join(text.split()), chars) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: chars - 3] + "..."
    return data_text("\n".join(lines), font=MONO, font_size=font_size, color=color, line_spacing=0.8)


# ---------------------------------------------------------------------------
# The final scoreboard: every row the series has computed, read through each part's own compute module (so
# tools/make.py computes those parts first); a part not yet computed contributes no row, and nothing is computed here
# ---------------------------------------------------------------------------
def _result(mod, name: str) -> dict | None:
    path = mod.CACHE.path(name) if hasattr(mod, "CACHE") else mod.path(name)
    return mod.load(name) if path.exists() else None


def board_rows() -> tuple[list[dict], dict]:
    """The scoreboard's rows in the order Part 1 drew them, with the rows later parts added slotted in after the
    counting models.  Returns the rows and the index of named rows ('best', 'novels', 'human', 'top')."""
    from videos.ai.ai1 import compute as c1
    from videos.ai.ai7 import compute as c7
    from videos.ai.ai9 import compute as c9
    from videos.ai.ai13 import compute as c13

    sb, raw = _result(c1, "scoreboard"), _result(c1, "raw")
    if sb:
        rows = [dict(r) for r in sb["rows"]]
    else:
        plain_bits = 8 * raw["n_bytes"] / raw["n_chars"] if raw else 8.0
        rows = [dict(key="ascii", label="plain text file", bits=plain_bits, part=1, kind="baseline")]
        if raw:
            rows += [
                dict(key="uniform", label=f"uniform over its {raw['passage_symbols']} symbols", bits=raw["uniform"],
                     part=1, kind="count"),
                dict(key="order0", label="letter frequencies", bits=raw["rows"][0]["test"], part=1, kind="count"),
                dict(key="order1", label="the previous character", bits=raw["rows"][1]["test"], part=1, kind="count"),
                dict(key="gzip", label="gzip", bits=raw["compressors"]["gzip"], part=1, kind="compressor"),
                dict(key="xz", label="xz", bits=raw["compressors"]["xz"], part=1, kind="compressor"),
                dict(key="bzip2", label="bzip2", bits=raw["compressors"]["bzip2"], part=1, kind="compressor"),
                dict(key="best", label=f"the previous {raw['best']} characters", bits=raw["best_bits"], part=1,
                     kind="count"),
            ]
        rows.append(dict(key="human", label="people (Shannon 1951, letters only)", lo=0.6, hi=1.3, part=1,
                         kind="human"))
    later = []
    kn = _result(c7, "kn")
    if kn:
        later.append(dict(key="kn", label=rf"Kneser--Ney, \ ${kn['best']}$ characters", bits=kn["best_bits"], part=7,
                          kind="count"))
    nlm = _result(c9, "lm")
    if nlm:
        later.append(dict(key="nlm", label=rf"a neural model, \ ${nlm['n_ctx']}$ characters", bits=nlm["passage_bits"],
                          part=9, kind="lm"))
        later.append(dict(key="mix", label=r"the neural model $+$ Kneser--Ney", bits=nlm["mix_bits"], part=9,
                          kind="lm"))
    tf = _result(c13, "tf")
    if tf:
        later.append(dict(key="tf", label=rf"our transformer, \ ${tf['ctx']}$ characters", bits=tf["passage_bits"],
                          part=13, kind="lm"))
    nb = load("novels_bits")
    if nb:
        later.append(dict(key="novels", label=r"our model, \ trained on thirty novels", bits=nb["bpc"], part=31,
                          kind="lm"))
    keys = [r["key"] for r in rows]
    at = keys.index("best") + 1 if "best" in keys else len(rows) - 1
    rows[at:at] = later
    keys = [r["key"] for r in rows]
    lms = [k for k, r in enumerate(rows) if r.get("kind") == "lm" and r.get("part") == 1 and "bits" in r]
    named = {k: keys.index(k) for k in ("best", "novels", "human", "kn", "tf") if k in keys}
    if lms:
        named["top"] = min(lms, key=lambda k: rows[k]["bits"])
    return rows, named
