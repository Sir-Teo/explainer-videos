"""Helpers shared by the scenes of Part 39 (Crypto and DeFi)."""

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import CACHE as _CACHE, load as _original_load

# Populated only after successful, audited, unchanged ordinary computations.
_ORDINARY_SHA = {'amm': '47e2aac1783d5c550e56f8f37cc9b6ac4965fa579cfc7685eeda89460f442bf3', 'lvr': '6c21293fc88dafaef8b82de5dc8057585879fd6b50080610ab9e65c059818c66', 'fees': '3876812aeee71e3f888f277bc4bda97f58de4f2357f1de27c50362e9643afd6e', 'v3': '3dc0ca7ab8ecc142040107fb2979f79127e9fdca6f0d29dc2042abe78a08eef9', 'rl': '28df8a815694cb2b34ac07366d9884a121461940a7f963507ecaaa1d21e7ff51', 'mev': 'e7bea1c1f3468690dcf513e8c27a68fe73a3dc6cacda2534281219e084759731', 'funding': 'e3ef086b4e0ad6787d7d7b865a55ad8af265384ffd168d57052ce6e80c3b221f', 'stable': '756c379962933c4610eb3fb2baf8d324c371073f2bda834f6350b5f730e54d4f', 'etf': '0af67d0d1510949644e3ac8bec0bddce136ee3757a2de490d9281d25ca2e9c9f', 'research': 'c77ce167ba8503066b9d1ad55c879bb06c8f8f1a75af48bd369e0654de1728cb'}


def load(name):
    import hashlib

    if name == "carry" or str(name).casefold().startswith(("house", "envelope", "track", "holdout")):
        raise RuntimeError("Excluded experiment rejected before cache or counted access")
    if name not in _ORDINARY_SHA:
        raise RuntimeError("No verified ordinary Part 39 cache is approved for this input")
    path = _CACHE.path(name)
    if not path.is_file():
        raise RuntimeError("Rendering requires an existing verified ordinary cache")
    if hashlib.sha256(path.read_bytes()).hexdigest() != _ORDINARY_SHA[name]:
        raise RuntimeError("Ordinary cache bytes differ from the audited result")
    return _original_load(name)


PART = 39

POOL_C = QC.DELTA        # the pool, the LP
ARB_C = QC.LOSS          # arbitrageurs, LVR, losses to them
FEE_C = QC.GAIN          # fees earned
REBAL_C = QC.VEGA        # the rebalancing portfolio
PERP_C = QC.OPTION       # perpetuals and funding
SPOT_C = QC.SPOT         # spot prices
STABLE_C = QC.IMPLIED    # stablecoins
BAD = QC.LOSS
GOOD = QC.GAIN
HURDLE = QC.DELTA


def fit_right(m, edge: float = 6.75):
    """Shift ``m`` left until its right edge is inside the frame (side panels aligned to a narrow legend)."""
    m.shift(LEFT * max(0.0, m.get_right()[0] - edge))
    return m


def illustration(text: str = r"illustration", corner=DR):
    return note(text, font_size=18, color=GREY_B).to_corner(corner, buff=0.25)


def sci(x: float, digits: int = 0) -> str:
    """A number in scientific notation for MathTex: 2\\times 10^{-2}, not 2e-02."""
    import math
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    if round(m, digits) >= 10:
        m, e = m / 10, e + 1
    return rf"{m:.{digits}f}\times 10^{{{e}}}"


def comma(n) -> str:
    """12,000 for TeX: the comma braced so it is not read as punctuation spacing."""
    return f"{int(round(n)):,}".replace(",", "{,}")


def era_strip(entries, width=12.6, y0=1985, y1=2027, font_size=17, step=10):
    """A custom time strip for this part's own history: entries (year, text, colour); dots on a line, labels
    alternating above and below. Returns the group, with ``.items`` one (dot, leader, label) group per entry."""
    x0 = -width / 2

    def X(y):
        return x0 + width * (y - y0) / (y1 - y0)
    line = Line([X(y0), 0, 0], [X(y1), 0, 0], color=GREY_D, stroke_width=2)
    ticks = VGroup(*[VGroup(Line([X(y), -0.06, 0], [X(y), 0.06, 0], color=GREY_D, stroke_width=1.5),
                            Text(str(y), font_size=13, color=GREY_D).next_to([X(y), 0, 0], DOWN, buff=0.12))
                     for y in range(int(np.ceil(y0 / 10) * 10), y1, step)])
    items = VGroup()
    side = 1
    levels = {1: [], -1: []}
    for yr, text, col in entries:
        d = Dot([X(yr), 0, 0], radius=0.07, color=col)
        lab = label(rf"{int(yr)}\; {text}", font_size=font_size, color=col)
        lvl = 0
        while any(abs(lab.width / 2 + w / 2) > abs(X(yr) - x) - 0.15 and lv == lvl for x, w, lv in levels[side]):
            lvl += 1
        lab.move_to([X(yr), side * (0.55 + 0.42 * lvl), 0])
        levels[side].append((X(yr), lab.width, lvl))
        keep_in_frame(lab, margin=0.25)
        lead = Line([X(yr), side * 0.08, 0], [X(yr), side * (0.55 + 0.42 * lvl) - side * 0.16, 0], color=GREY_C,
                    stroke_width=1, stroke_opacity=0.6)
        items.add(VGroup(d, lead, lab))
        side = -side
    g = VGroup(line, ticks, items)
    g.items = items
    return g


def step_xy(t, h):
    """Points of a step line: holding h[k] held from t[k] to t[k+1]."""
    xs, ys = [], []
    for k in range(len(h)):
        xs += [t[k], t[k + 1]]
        ys += [h[k], h[k]]
    return np.array(xs), np.array(ys)


def grid_fn(xs, ys, Z):
    """f(x, y) by bilinear interpolation of Z (len(ys), len(xs)) on a grid, for surfaces drawn from cached arrays."""
    from scipy.interpolate import RegularGridInterpolator

    it = RegularGridInterpolator((np.asarray(ys, float), np.asarray(xs, float)), np.asarray(Z, float),
                                 bounds_error=False, fill_value=None)
    return lambda x, y: float(it([[y, x]])[0])


def ask(text: str):
    """The pause-and-predict banner at the foot of the frame."""
    return wrapped_label(rf"Pause and predict: {text}", 12.4, 25, QC.IDEA).to_edge(DOWN, buff=0.3)


def surf3d_axes(x_range, y_range, z_range, x_length=7.0, y_length=4.6, z_length=3.4):
    ax = ThreeDAxes(x_range=x_range, y_range=y_range, z_range=z_range, x_length=x_length, y_length=y_length,
                    z_length=z_length, tips=False,
                    axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
    return ax


def src_lines(obj, first: str, count: int):
    """``count`` lines of the House's own source of ``obj``, starting at the line that contains ``first``, dedented:
    the lab shows the code exactly as it is in the library."""
    import inspect
    import textwrap

    lines = inspect.getsource(obj).splitlines()
    i = next(k for k, ln in enumerate(lines) if first in ln)
    return textwrap.dedent("\n".join(lines[i:i + count])).splitlines()


def house_lab(title, obj, first, count, extra=(), width=6.6):
    """A lab card for the House function ``obj`` (its file shown as the source); ``extra`` adds (obj, first, count)
    excerpts below, separated by a blank line."""
    import inspect

    lines = src_lines(obj, first, count)
    for o, f, c in extra:
        lines += [""] + src_lines(o, f, c)
    src = inspect.getsourcefile(obj).split("explainer-videos/")[-1]
    return lab_card(title, lines, source=f"{src}: {obj.__qualname__}", width=width)


def tt(formula: str, n: int = 70) -> str:
    """A formula string for TeX in typewriter type: cut to ``n`` characters (before escaping, so a cut never splits an
    escape), then escaped."""
    f = formula if len(formula) <= n else formula[:n - 3].rstrip() + "..."
    f = f.replace("\\", "").replace("_", r"\_").replace("#", r"\#").replace("^", r"\^{}").replace("%", r"\%")
    f = f.replace("...", r"\ldots")
    return r"\texttt{" + f + "}"


def prediction_card(text):
    head = label(r"Pause and predict", font_size=32, color=HURDLE)
    body = wrapped_label(text, 12.0, 31)
    return VGroup(head, body).arrange(DOWN, buff=0.42).move_to(ORIGIN)
