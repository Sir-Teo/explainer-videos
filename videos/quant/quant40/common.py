"""Helpers shared by the scenes of Part 40 (Measuring Risk)."""

from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403

from .compute import load as _counted_load

# Only closed approved ordinary outputs, with rejection before path/count access.
_ORDINARY_SHA = {'var3': '202a05062e6761c722322e39537268f66ec841dd6f17167f4bc74b6731700dd0', 'sqrt': 'ab97d85fae1a1db2a2a5938654e091143265a425535b9bb06b7614b1af70e4ea', 'coherent': 'a3ea37706075c936aa2f780d84a6cac1757d654b8b1af4f7f83c4c634fcafd02', 'backtest': '875765aaa2df40280d921fc0ce871111b2e0431ab6292949eae1d66840272f4f', 'evt': '877ffd52709635e218c00817f817c4024d8361f9a8b827039dd41dbcafbc1aa2', 'depend': '6c8bc7bfcb074690c44f7412b90c9e6d1a8f97d5a2d440605eeda6fc3194a722', 'stress': '070e7e3475eab36becfc0bd9e0dd59799f6450dd4c11a10b0e5e3e71692708d3', 'ra': '1ccb99ce684b2569a8b33e648535b01b984b3ca11bc9f7f789c1677d6e7741d0', 'learned': 'fda792e7b8828bbd24c5e7cf466df72b933e703f9e5690a792c9ee83403499c9', 'liq': '1296edae0b2f41806aa276fff27c2dc8ad5ed1940ea2dea2315fa0334fda20ac', 'research': '160aeaaec62428a640b12910dabfea0336a7515a9751a3e17e447f429e34f2ee', 'options': 'a3a1fbfb93a5d8ca4428e9aa3be6b085e25b151c330490b69f7d36c4d0fd75a2'}

def load(name):
    if not isinstance(name,str) or name.casefold().startswith(('house','envelope','track','holdout')) or name not in _ORDINARY_SHA:
        raise RuntimeError('Excluded before cache path/count access: '+str(name))
    import hashlib
    from pathlib import Path
    path=Path(__file__).resolve().parents[3]/'.cache'/'quant40'/(name+'.json')
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=_ORDINARY_SHA[name]:
        raise RuntimeError('Missing or changed ordinary output; implicit computation forbidden: '+name)
    return _counted_load(name)

from explainer.analysis import ladder as _base_ladder

def ladder(*args,**kwargs):
    reveal=_base_ladder(*args,**kwargs)
    def step(i,run_time=1.2,transform=False):
        return reveal(i,run_time=run_time,transform=transform)
    return step


PART = 40

VAR_C = QC.DELTA         # value at risk, the quantile line
ES_C = QC.LOSS           # expected shortfall, the tail mass
HIT_C = QC.IMPLIED       # exceedances
MODEL_C = QC.VEGA        # a model's forecast
DATA_C = QC.SPOT         # realised returns
TAIL_C = QC.OPTION       # tails, EVT
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


from explainer.quant import desk_question as _base_desk_question

def desk_question(question,answer_hint="",width=8.4,font_size=28):
    return _base_desk_question(question,answer_hint,width=width,font_size=max(28,font_size))

def pause_card(text):
    head=label(r"Pause and predict",font_size=32,color=QC.IDEA)
    body=wrapped_label(text,11.8,30)
    content=VGroup(head,body).arrange(DOWN,buff=0.4)
    if content.height>6.7:content.scale_to_fit_height(6.7)
    return content.move_to(ORIGIN)
