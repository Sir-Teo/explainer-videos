"""Helpers shared by the scenes of Part 41 (Leverage, Liquidity and Crises)."""

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import load as _counted_load

# All thirteen names were classified by a transitive source audit before any output-path access.
_ORDINARY_SHA = {'desk': '2d77362fc61c91f6be316dfbd043db10760b3456215fb807e8bb914859949857', 'spiral': '0a5e375a81d9784279f80ca53eda7a536b8a4017dc38e85d531f064ee77f1b9f', 'firesale': '82bad3bf60e07c08cd756ca058a0391a2b753a58ffee4f7f2e22677bc536b74d', 'network': '2bbd9503488f55cc71fac4e27312c71370c0290898d56f8afa3b022f4871e6bc', 'systemic': '8ac134a5b87eca7bebd995a10814c7620e84654cbe4e65b6aa459c3720282e9d', 'gfc': '0037effa6865e3355bdbb81cab6289db25452ef40507bb1f97939cb8b2799dc1', 'dash': '9e2c082490a139ef32f4b59968b110c0fc8e6718e3404d76d92631ed09ec2773', 'china': '1208c5a646d8e6c2b174da15c2bbafd169c881ab4dea717cd90e10b04488c567', 'y2023': '1ca89c25abe5319732067cacf618e624d8515eff500f43fb7cac3dc76adc8561', 'research': '9c357404d9dc9b8f031d213d377f751194cfdffba79999c8700c91879f70fbf4', 'ltcm': 'cb74b7c3ec1529492d6b6698f9f3f20466e8bdb3d624508ad56d190b1b63f4c8', 'dd': 'bf2976d60a2a5b809d5ce6bd5173e87888c38f11fa6b828d7951851f184c9985', 'house': 'fe59fb0a1d84d34056563f81d98195b15d0a0c551c362f27a37a33e9f5d055c0'}

def load(name):
    if not isinstance(name, str) or name not in _ORDINARY_SHA or name.casefold().startswith(('envelope','track','holdout')):
        raise RuntimeError('Excluded before cache path/count access: '+str(name))
    import hashlib
    from pathlib import Path
    path=Path(__file__).resolve().parents[3]/'.cache'/'quant41'/(name+'.json')
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=_ORDINARY_SHA[name]:
        raise RuntimeError('Missing or changed ordinary output; implicit computation forbidden: '+name)
    return _counted_load(name)

from explainer.analysis import ladder as _base_ladder

def ladder(*args, **kwargs):
    # Center the entire formula before fitting: long RHS terms can otherwise place
    # their center past the frame and collapse under operator-aligned scaling.
    kwargs.setdefault('align_index', None)
    reveal=_base_ladder(*args, **kwargs)
    def step(i, run_time=1.2, transform=False):
        return reveal(i, run_time=run_time, transform=transform)
    return step

def calendar_year(dates):
    from datetime import date
    values=[]
    for value in dates:
        s=str(value).replace('-', '')[:8]
        d=date(int(s[:4]), int(s[4:6]), int(s[6:8]))
        a=date(d.year, 1, 1);b=date(d.year+1, 1, 1)
        values.append(d.year+(d-a).days/(b-a).days)
    return np.asarray(values, float)


PART = 41

LEV_C = QC.DELTA         # leverage, balance sheets
SPIRAL_C = QC.LOSS       # forced sales, spirals, defaults
FUND_C = QC.IMPLIED      # funding, haircuts, runs
NET_C = QC.VEGA          # networks, links
PRICE_C = QC.SPOT        # prices and markets
SAFE_C = QC.GAIN         # survivors, backstops
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
