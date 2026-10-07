"""Helpers shared by the "Opposing Forces" scenes: data, time-series charts, labels."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np

from explainer import *  # noqa: F403

DATA = Path(__file__).with_name("data.json")

# ---------------------------------------------------------------------------
# What the note says (Jurrien Timmer, Fidelity, "Opposing Forces", week of 10/5/26).
# Scenes quote these; wherever public data can check a figure, the scene asserts
# that the data agrees before saying it.
# ---------------------------------------------------------------------------
NOTE = dict(
    trailing_eps_growth=30,  # "trailing EPS are up 30% y/y" (later in the note: 28%)
    n12m_eps_growth=20,  # next-12-month EPS expected to grow another 20%
    margin=17.4,  # profit margins, "another new high"
    risk_free_nominal=5.3,
    risk_free_real=2.9,
    ten_year=5.34,
    real_ten_year=2.91,
    above_50dma=25,  # % of stocks above their 50-day moving average
    above_200dma=46,
    sideways_months=4,
    debt_trillions=40,
    debt_since_covid=16,  # "up more than $16 trillion since COVID"
    debt_service_gdp=4.0,
    term_premium_bp=89,
    gdp_survey=(2.1, 2.2),  # Bloomberg survey of real GDP growth, 2026-2028
    q3_growth=(30, 35),  # "Q3 could come in at 30-35%"
    trailing_pe_change=-10,
    fwd_pe_cap=19.7,
    fwd_pe_equal=17.3,
    us_payout_cagr=10,
    secular_bull_start=2009,
)

# FactSet, "Earnings Insight", October 2, 2026 (John Butters).
FACTSET = dict(
    q3_growth=29.5,  # estimated y/y EPS growth for Q3 2026
    q3_growth_june30=26.7,
    q4_growth=27.6,
    cy2026_growth=32.4,
    cy2027_growth=15.8,
    q1_2027_growth=19.1,
    q2_2027_growth=2.3,
    fwd_pe=19.0,
    fwd_pe_june30=20.4,
    fwd_pe_10y_avg=19.1,
    fwd_pe_feb13=21.5,  # Earnings Insight, Feb 13, 2026
    price_chg_q3=2.0,  # price change of the index, June 30 -> Sep 30
    fwd_eps_chg_q3=9.3,  # change in forward 12-month EPS over the same span
    trailing_pe=25.7,
    margin_q2=17.0,  # record net profit margin (Q2 2026), since 2009
    positive_guidance=72,
    positive_guidance_prior_record=65,
)


# ---------------------------------------------------------------------------
# Data access
# ---------------------------------------------------------------------------
@lru_cache(maxsize=1)
def data() -> dict:
    if not DATA.exists():
        raise FileNotFoundError(f"Missing {DATA}. Run: python -m videos.opposing_forces.fetch")
    return json.loads(DATA.read_text())


def ts(key: str, sub: str | None = None) -> tuple[np.ndarray, np.ndarray]:
    """(t, v) arrays of a stored series; t is a decimal year."""
    s = data()[key] if sub is None else data()[key][sub]
    return np.asarray(s["t"], dtype=float), np.asarray(s["v"], dtype=float)


def window(t, v, t0=-np.inf, t1=np.inf):
    m = (t >= t0) & (t <= t1)
    return t[m], v[m]


def index_at(t, when: float) -> int:
    """Index of the last observation on or before ``when`` (stored times are rounded to
    1e-4 years, so allow a few hours of slack; daily data are 0.0027 years apart)."""
    return max(int(np.searchsorted(t, when + 1e-3)) - 1, 0)


def at(t, v, when: float) -> float:
    """Value of the series at the last observation on or before ``when``."""
    return float(v[index_at(t, when)])


def last(key: str) -> float:
    return float(data()[key]["v"][-1])


@lru_cache(maxsize=1)
def shiller() -> dict:
    s = data()["shiller"]
    out = {"t": np.asarray(s["t"], dtype=float)}
    for k in ("P", "D", "E", "CPI", "GS10", "CAPE", "ECY"):
        out[k] = np.array([np.nan if x is None else x for x in s[k]], dtype=float)
    out["PE"] = out["P"] / out["E"]
    return out


def ym(year: int, month: int, day: int = 1) -> float:
    """Decimal year for a calendar date (for chart annotations)."""
    import datetime as dt

    d = dt.date(year, month, day)
    start = dt.date(year, 1, 1)
    return year + (d - start).days / (dt.date(year + 1, 1, 1) - start).days


def yoy(t, v, months=12):
    """Percent change over ``months`` for a monthly series."""
    out = np.full_like(v, np.nan)
    out[months:] = 100 * (v[months:] / v[:-months] - 1)
    return out


# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    return Tex(text, color=color, font_size=font_size, **kw)


def caption_box(mob: Mobject, color=WHITE, buff=0.18) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=2)


def source(text: str, font_size=20) -> Tex:
    """Small source line, bottom-right, as on any well-made chart."""
    return Tex(r"Source: " + text, font_size=font_size, color=GREY_B).to_corner(DR, buff=0.25)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def pct(v: float, d: int = 1, sign: bool = False) -> str:
    s = f"{v:+.{d}f}" if sign else f"{v:.{d}f}"
    return s.replace("-", "−") + r"\%"


def chapter_card(number: int, text: str) -> VGroup:
    num = Tex(f"Chapter {number}", font_size=32, color=C.DIM)
    title = Tex(text, font_size=60)
    return VGroup(num, title).arrange(DOWN, buff=0.25)


def show_chapter_card(scene: Scene, number: int, text: str, hold: float = 1.2):
    card = chapter_card(number, text)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=UP * 0.2), run_time=0.6)


def pe_equation(font_size=60) -> MathTex:
    """P = E x P/E with the concept colors; parts: 0 P, 1 =, 2 E, 3 x, 4 P/E."""
    eq = MathTex(r"P", r"=", r"E", r"\times", r"P/E", font_size=font_size)
    eq[0].set_color(C.PRICE)
    eq[2].set_color(C.EARNINGS)
    eq[4].set_color(C.MULTIPLE)
    return eq


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
class TimeChart(VGroup):
    """A time-series chart: x is a decimal year, y a value.  Axes run along the
    bottom and left of the box, with light horizontal gridlines.  Coordinates are
    measured from the axes' corner, so the chart can be moved freely before or
    after plotting.  It is built centered on the origin."""

    def __init__(self, x_range, y_range, width=10.0, height=4.6, x_ticks=None, y_ticks=(), y_fmt=None, x_fmt=None,
                 font_size=24, grid=True, log_y=False, color=GREY_B):
        super().__init__()
        self.x_range, self.y_range, self.w, self.h, self.log_y = x_range, y_range, width, height, log_y
        y_fmt = y_fmt or (lambda v: f"{v:g}")
        x_fmt = x_fmt or (lambda v: f"{int(v)}")
        if x_ticks is None:
            x_ticks = range(int(np.ceil(x_range[0])), int(x_range[1]) + 1)
        self.x_axis = Line(ORIGIN, RIGHT * width, color=color, stroke_width=2)
        self.y_axis = Line(ORIGIN, UP * height, color=color, stroke_width=2)
        self.grid = VGroup()
        if grid:
            for t in y_ticks:
                if t != y_range[0]:
                    self.grid.add(Line(self.c2p(x_range[0], t), self.c2p(x_range[1], t), color=GREY_D, stroke_width=1,
                                       stroke_opacity=0.7))
        self.x_labels, self.y_labels = VGroup(), VGroup()
        for t in x_ticks:
            p = self.c2p(t, y_range[0])
            self.x_labels.add(Line(p, p + DOWN * 0.08, color=color, stroke_width=2))
            lab = x_fmt(t)
            m = lab if isinstance(lab, Mobject) else Tex(lab, font_size=font_size, color=GREY_A)
            self.x_labels.add(m.next_to(p, DOWN, buff=0.14))
        for t in y_ticks:
            p = self.c2p(x_range[0], t)
            lab = y_fmt(t)
            m = lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=GREY_A)
            self.y_labels.add(m.next_to(p, LEFT, buff=0.14))
        self.add(self.grid, self.x_axis, self.y_axis, self.x_labels, self.y_labels)
        self.shift(-(self.x_axis.get_start() + np.array([width / 2, height / 2, 0])))

    def _fy(self, v):
        lo, hi = self.y_range
        if self.log_y:
            return (np.log10(v) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))
        return (v - lo) / (hi - lo)

    def c2p(self, t, v):
        x0, x1 = self.x_range
        o = self.x_axis.get_start()
        return o + RIGHT * self.w * (t - x0) / (x1 - x0) + UP * self.h * self._fy(v)

    def line(self, t, v, color, stroke_width=4) -> VMobject:
        t, v = np.asarray(t, float), np.asarray(v, float)
        m = np.isfinite(v)
        pts = [self.c2p(a, b) for a, b in zip(t[m], v[m])]
        return VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width).set_fill(opacity=0)

    def area(self, t, v, color, opacity=0.25, base=None) -> VMobject:
        base = self.y_range[0] if base is None else base
        pts = [self.c2p(t[0], base)] + [self.c2p(a, b) for a, b in zip(t, v)] + [self.c2p(t[-1], base)]
        return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)

    def hline(self, v, color=GREY_B, stroke_width=2, dashed=True, t0=None, t1=None) -> VMobject:
        a = self.c2p(self.x_range[0] if t0 is None else t0, v)
        b = self.c2p(self.x_range[1] if t1 is None else t1, v)
        return DashedLine(a, b, color=color, stroke_width=stroke_width, dash_length=0.08) if dashed else \
            Line(a, b, color=color, stroke_width=stroke_width)

    def vline(self, t, color=GREY_B, stroke_width=2, dashed=True) -> VMobject:
        a, b = self.c2p(t, self.y_range[0]), self.c2p(t, self.y_range[1])
        return DashedLine(a, b, color=color, stroke_width=stroke_width, dash_length=0.08) if dashed else \
            Line(a, b, color=color, stroke_width=stroke_width)

    def span(self, t0, t1, color=GREY_B, opacity=0.15) -> Rectangle:
        a, b = self.c2p(t0, self.y_range[0]), self.c2p(t1, self.y_range[1])
        r = Rectangle(width=abs(b[0] - a[0]), height=abs(b[1] - a[1]), stroke_width=0, fill_color=color,
                      fill_opacity=opacity)
        return r.move_to((a + b) / 2)

    def dot(self, t, v, color=WHITE, radius=0.07) -> Dot:
        return Dot(self.c2p(t, v), radius=radius, color=color)

    def y_title(self, text, color=GREY_A, font_size=28) -> Tex:
        return label(text, color=color, font_size=font_size).next_to(self.y_axis, UP, buff=0.2).align_to(self.y_axis, LEFT)


def money(v) -> str:
    return f"{v:,.0f}".replace(",", "{,}")


def month_index(t, when) -> int:
    return int(np.argmin(np.abs(t - when)))


def pe_plane() -> VGroup:
    """Earnings on x, P/E on y, curves of constant price, and the S&P 500's real path:
    Oct 2022 -> Dec 2024 (the multiple did the work) and Dec 2024 -> June 2026 (earnings did).
    Attributes: ch, xl, yl, curves, clabels, iso, leg1, leg2, dots, tags, k (indices), E, PE."""
    s = shiller()
    ch = TimeChart((150, 320), (14, 32), width=8.6, height=5.2, x_ticks=[150, 200, 250, 300],
                   x_fmt=lambda v: rf"\${v:.0f}", y_ticks=[15, 20, 25, 30]).move_to(LEFT * 1.9 + DOWN * 0.1)
    g = VGroup()
    g.ch = ch
    g.xl = label(r"earnings per share, $E$", font_size=28, color=C.EARNINGS).next_to(ch, DOWN, buff=0.1).align_to(ch.x_axis, RIGHT)
    g.yl = ch.y_title(r"multiple, P/E", color=C.MULTIPLE)
    g.curves, g.clabels = VGroup(), VGroup()
    for P in (3000, 4000, 5000, 6000, 7000, 8000, 9000):
        es = np.linspace(max(150, P / 32), min(320, P / 14), 120)
        g.curves.add(ch.line(es, P / es, C.PRICE, 2).set_stroke(opacity=0.55))
        end_e = min(320, P / 14.5)
        g.clabels.add(MathTex(money(P), font_size=22, color=C.PRICE).next_to(ch.c2p(end_e, P / end_e), UR, buff=0.04))
    g.iso = label(r"curves of constant price $P = E \times$ P/E", font_size=28, color=C.PRICE).move_to(RIGHT * 4.6 + UP * 3.2)
    t, E, PE = s["t"], s["E"], s["PE"]
    k = (month_index(t, ym(2022, 10)), month_index(t, ym(2024, 12)), month_index(t, ym(2026, 6)))
    g.k, g.E, g.PE = k, E, PE
    g.leg1 = ch.line(E[k[0]:k[1] + 1], PE[k[0]:k[1] + 1], C.MULTIPLE, 5)
    g.leg2 = ch.line(E[k[1]:k[2] + 1], PE[k[1]:k[2] + 1], C.EARNINGS, 5)
    g.dots = VGroup(*[ch.dot(E[i], PE[i], WHITE) for i in k])
    g.tags = VGroup(tagged(r"Oct 2022", font_size=24).next_to(g.dots[0], DOWN, buff=0.12),
                    tagged(r"Dec 2024", font_size=24).next_to(g.dots[1], UP, buff=0.12),
                    tagged(r"June 2026", font_size=24).next_to(g.dots[2], DOWN, buff=0.12))
    g.add(ch, g.xl, g.yl, g.curves, g.clabels)
    return g
