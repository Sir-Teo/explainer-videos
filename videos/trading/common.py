"""Helpers shared by the trading-system scenes: text, plots with log axes, the order-book ladder, byte strips,
machines and wires, the map."""

from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403

from .compute import load  # noqa: F401

# ---------------------------------------------------------------------------
# Facts quoted on screen that do not come from our own data (sources: videos/trading/README.md).
# ---------------------------------------------------------------------------
FACTS = dict(
    # Budish, Cramton & Shim (QJE 2015), ES vs SPY, 2011 medians; arbitrage durations 2005 -> 2011
    bcs_corr_10ms=0.0923, bcs_corr_1ms=0.0073, bcs_dur_2005_ms=97, bcs_dur_2011_ms=7, bcs_arbs_per_day=1000,
    bcs_dollars_per_year=75e6,
    # Aquilina, Budish & O'Neill (QJE 2022), LSE message data, FTSE 350, 2015
    abo_race_us=(5, 10), abo_volume_share=0.20, abo_tax_bp=0.5, abo_global_per_year=5e9, abo_top6_share=0.80,
    abo_races_per_min=1,
    # Jane Street tech talk "How to Build an Exchange" (Brian Nigito) and Signals and Threads ep. 3
    nigito_peak_msgs=3e6, nigito_exec_share=(1, 2), nigito_rebuild_s=(30, 60), nigito_component_rate=500e3,
    nigito_unicast_600_us=600, nigito_cut_through_ns=(300, 500), nigito_l1_switch_ns=(3, 5),
    nigito_store_forward_us=(7, 10), nigito_pcie_ns=(300, 600), nigito_ctx_switch_us=(1, 2),
    # HRT Beat, "Low Latency Optimization, Part 1" (Guillaume Morin, Nov 2022)
    hrt_walk_loads=3, hrt_mem_ns=70, hrt_walk_ns=210, hrt_tlb_entries=(1500, 2000), hrt_speedup=4.5,
    # Microwave and fiber, Chicago <-> New Jersey
    quincy_carteret_ms=3.982, quincy_mahwah_ms=3.986, quincy_ny2_ms=4.015, quincy_year=2016,
    spread_rtt_ms=13.33, spread_miles=825, spread_year=2010,
    # STAC-T0 (AMD + Exegy, June 2024): minimum actionable latency, last bit in to first bit out
    stac_t0_ns=13.9, stac_t0_prev_ns=24.2,
    # SEC order against Knight Capital Americas (Release 34-70694, Oct 16, 2013)
    knight_parent=212, knight_execs=4e6, knight_stocks=154, knight_shares=397e6, knight_minutes=45,
    knight_long=3.5e9, knight_long_n=80, knight_short=3.15e9, knight_short_n=74, knight_loss=460e6,
    knight_emails=97, knight_servers=8, knight_limit_33=2e6,
    # MiFID II RTS 25: high-frequency trading clocks
    rts25_max_div_us=100, rts25_granularity_us=1,
    # Firms (public statements and press reports)
    js_venues=200, js_countries=45, js_rev_2025=39.6e9,
)
DAY_LABEL = r"Wednesday, December 10, 2025"

# ---------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------
WIDE_TEX = TEX_TEMPLATE.copy()
WIDE_TEX.add_to_preamble(r"\setlength{\textwidth}{40cm}")
MAX_TEXT_WIDTH = 13.6
MONO = "DejaVu Sans Mono"


def label(text: str, color=WHITE, font_size=32, **kw) -> Tex:
    """A Tex label that never wraps on its own (line breaks are explicit) and shrinks to fit the frame."""
    kw.setdefault("tex_template", WIDE_TEX)
    t = Tex(text, color=color, font_size=font_size, **kw)
    if t.width > MAX_TEXT_WIDTH:
        t.width = MAX_TEXT_WIDTH
    return t


def mtex(tex: str, color=WHITE, font_size=36, **kw) -> MathTex:
    return MathTex(tex, color=color, font_size=font_size, **kw)


def note(text: str, font_size=22, color=GREY_B) -> Tex:
    return label(text, font_size=font_size, color=color)


def source(text: str, font_size=20) -> Tex:
    return label(r"Source: " + text, font_size=font_size, color=GREY_B).to_corner(DR, buff=0.25)


def schematic_tag(corner=UR) -> Tex:
    return note(r"schematic").to_corner(corner, buff=0.3)


def real_tag(text: str = r"real Nasdaq data, Dec 10, 2025", corner=DR) -> Tex:
    return note(text, color=GREY_A).to_corner(corner, buff=0.3)


def machine_tag(corner=DR) -> Tex:
    return note(r"measured on a 4-core Intel Xeon virtual machine", color=GREY_A).to_corner(corner, buff=0.3)


def tagged(text: str, color=WHITE, font_size=28, opacity=0.85) -> Tex:
    t = label(text, color=color, font_size=font_size)
    t.add_background_rectangle(color=BACKGROUND, opacity=opacity, buff=0.06)
    return t


def title(text: str, font_size=40, color=WHITE) -> Tex:
    return label(text, font_size=font_size, color=color).to_edge(UP, buff=0.4)


class Mono(VGroup):
    """Monospace text whose bounding box always includes ascenders and descenders, so rows line up.
    ``self.glyphs`` are the visible characters (spaces have none)."""

    def __init__(self, s: str, font_size=24, color=WHITE, **kw):
        strut = "Ég"
        t = Text(strut + s, font=MONO, font_size=font_size, color=color, **kw)
        struts, glyphs = t[:2], t[2:]
        if len(glyphs):
            x0, x1 = glyphs.get_left()[0], glyphs.get_right()[0]
        else:
            x0 = struts.get_right()[0]
            x1 = x0 + 0.2
        frame = VGroup(VectorizedPoint([x0, struts.get_top()[1], 0]), VectorizedPoint([x1, struts.get_bottom()[1], 0]))
        super().__init__(frame, *glyphs)
        self.frame = frame
        self.glyphs = VGroup(*glyphs)


def chip(text: str, color=GREY_B, font_size=22, fill=0.18, mono=False, text_color=WHITE) -> VGroup:
    t = Mono(text, font_size=font_size, color=text_color) if mono else label(text, font_size=font_size, color=text_color)
    box = RoundedRectangle(width=t.width + 0.28, height=t.height + 0.18, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.5, fill_color=color, fill_opacity=fill)
    t.move_to(box)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def node(text: str, color=GREY_B, width=None, height=0.8, font_size=26, fill=0.15, corner=0.12) -> VGroup:
    """A labeled box for system diagrams."""
    t = label(text, font_size=font_size)
    w = width or t.width + 0.5
    box = RoundedRectangle(width=w, height=max(height, t.height + 0.3), corner_radius=corner, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=fill)
    t.move_to(box)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def fmt_int(n) -> str:
    """12345678 -> '12{,}345{,}678' for TeX."""
    return f"{int(round(n)):,}".replace(",", "{,}")


def fmt_ns(x: float, tex: bool = True) -> str:
    """A duration in ns as a short human string: 1.2 ns, 450 ns, 3.4 us, 12 ms, 2 s."""
    for scale, unit in [(1e9, "s"), (1e6, "ms"), (1e3, r"\mu s" if tex else "us"), (1, "ns")]:
        if x >= scale or scale == 1:
            q = x / scale
            s = f"{q:.0f}" if q >= 100 else (f"{q:.1f}".rstrip("0").rstrip(".") if q >= 10 else f"{q:.2g}")
            if q < 10 and "." not in s and len(s) == 1 and q != int(q):
                s = f"{q:.1f}"
            if tex:
                u = r"\mu\mathrm{s}" if unit == r"\mu s" else rf"\mathrm{{{unit}}}"
                return rf"{s}\,{u}"
            return f"{s} {unit}"
    return str(x)


def decade_label(x: float) -> str:
    """Tick label for a power of ten in nanoseconds: 1 ns, 10 ns, 100 ns, 1 us, ..."""
    return fmt_ns(x)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
class Plot(VGroup):
    """Axes along the bottom and left of a box, linear or log in each direction, light gridlines.
    Built centered on the origin; move it freely, c2p() follows."""

    def __init__(self, x_range, y_range, width=10.0, height=5.0, log_x=False, log_y=False, x_ticks=(), y_ticks=(),
                 x_fmt=None, y_fmt=None, font_size=24, grid=True, x_grid=False, color=GREY_B, tick_color=GREY_A):
        super().__init__()
        self.x_range, self.y_range, self.w, self.h = x_range, y_range, width, height
        self.log_x, self.log_y = log_x, log_y
        x_fmt = x_fmt or (lambda v: f"{v:g}")
        y_fmt = y_fmt or (lambda v: f"{v:g}")
        self.x_axis = Line(ORIGIN, RIGHT * width, color=color, stroke_width=2)
        self.y_axis = Line(ORIGIN, UP * height, color=color, stroke_width=2)
        self.grid = VGroup()
        if grid:
            for t in y_ticks:
                if t != y_range[0]:
                    self.grid.add(Line(self.c2p(x_range[0], t), self.c2p(x_range[1], t), color=GREY_D, stroke_width=1,
                                       stroke_opacity=0.7))
        if x_grid:
            for t in x_ticks:
                if t != x_range[0]:
                    self.grid.add(Line(self.c2p(t, y_range[0]), self.c2p(t, y_range[1]), color=GREY_D, stroke_width=1,
                                       stroke_opacity=0.5))
        self.x_labels, self.y_labels = VGroup(), VGroup()
        for t in x_ticks:
            p = self.c2p(t, y_range[0])
            self.x_labels.add(Line(p, p + DOWN * 0.08, color=color, stroke_width=2))
            lab = x_fmt(t)
            m = lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=tick_color)
            self.x_labels.add(m.next_to(p, DOWN, buff=0.14))
        for t in y_ticks:
            p = self.c2p(x_range[0], t)
            lab = y_fmt(t)
            m = lab if isinstance(lab, Mobject) else MathTex(lab, font_size=font_size, color=tick_color)
            self.y_labels.add(m.next_to(p, LEFT, buff=0.14))
        self.add(self.grid, self.x_axis, self.y_axis, self.x_labels, self.y_labels)
        self.shift(-(self.x_axis.get_start() + np.array([width / 2, height / 2, 0])))

    def _f(self, v, rng, log):
        lo, hi = rng
        if log:
            v = np.maximum(v, lo * 1e-6) if isinstance(v, np.ndarray) else max(v, lo * 1e-6)
            return (np.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))
        return (v - lo) / (hi - lo)

    def c2p(self, x, y):
        o = self.x_axis.get_start()
        return o + RIGHT * self.w * self._f(x, self.x_range, self.log_x) + UP * self.h * self._f(y, self.y_range, self.log_y)

    def x_to(self, x) -> float:
        return float(self.c2p(x, self.y_range[0])[0])

    def y_to(self, y) -> float:
        return float(self.c2p(self.x_range[0], y)[1])

    def line(self, xs, ys, color, stroke_width=4, clip=True) -> VMobject:
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        m = np.isfinite(xs) & np.isfinite(ys)
        if clip:
            lo, hi = self.y_range
            ys = np.clip(ys, lo, hi)
        pts = [self.c2p(a, b) for a, b in zip(xs[m], ys[m])]
        return VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width).set_fill(opacity=0)

    def area(self, xs, ys, color, opacity=0.3, base=None) -> VMobject:
        base = self.y_range[0] if base is None else base
        xs, ys = np.asarray(xs, float), np.asarray(ys, float)
        pts = [self.c2p(xs[0], base)] + [self.c2p(a, b) for a, b in zip(xs, ys)] + [self.c2p(xs[-1], base)]
        return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)

    def histogram(self, edges, counts, color, opacity=0.75, stroke_width=0, gap=0.0) -> VGroup:
        """Bars between consecutive edges (len(edges) == len(counts) + 1)."""
        g = VGroup()
        y0 = self.y_range[0]
        for a, b, c in zip(edges[:-1], edges[1:], counts):
            if c <= y0:
                continue
            c = min(c, self.y_range[1])
            p0, p1 = self.c2p(a, y0), self.c2p(b, c)
            w = max(p1[0] - p0[0] - gap, 1e-3)
            r = Rectangle(width=w, height=max(p1[1] - p0[1], 1e-3), stroke_width=stroke_width, stroke_color=color,
                          fill_color=color, fill_opacity=opacity)
            r.move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0])
            g.add(r)
        return g

    def bar(self, x, y, width, color, opacity=0.85, base=None) -> Rectangle:
        base = self.y_range[0] if base is None else base
        p0, p1 = self.c2p(x, base), self.c2p(x, y)
        w = abs(self.c2p(x + width / 2, base)[0] - self.c2p(x - width / 2, base)[0])
        r = Rectangle(width=w, height=max(abs(p1[1] - p0[1]), 1e-3), stroke_width=0, fill_color=color,
                      fill_opacity=opacity)
        return r.move_to((p0 + p1) / 2)

    def hline(self, y, color=GREY_B, stroke_width=2, dashed=True, x0=None, x1=None) -> VMobject:
        a = self.c2p(self.x_range[0] if x0 is None else x0, y)
        b = self.c2p(self.x_range[1] if x1 is None else x1, y)
        return DashedLine(a, b, color=color, stroke_width=stroke_width, dash_length=0.08) if dashed else \
            Line(a, b, color=color, stroke_width=stroke_width)

    def vline(self, x, color=GREY_B, stroke_width=2, dashed=True, y0=None, y1=None) -> VMobject:
        a = self.c2p(x, self.y_range[0] if y0 is None else y0)
        b = self.c2p(x, self.y_range[1] if y1 is None else y1)
        return DashedLine(a, b, color=color, stroke_width=stroke_width, dash_length=0.08) if dashed else \
            Line(a, b, color=color, stroke_width=stroke_width)

    def span(self, x0, x1, color=GREY_B, opacity=0.15) -> Rectangle:
        a, b = self.c2p(x0, self.y_range[0]), self.c2p(x1, self.y_range[1])
        r = Rectangle(width=abs(b[0] - a[0]), height=abs(b[1] - a[1]), stroke_width=0, fill_color=color,
                      fill_opacity=opacity)
        return r.move_to((a + b) / 2)

    def dot(self, x, y, color=WHITE, radius=0.07) -> Dot:
        return Dot(self.c2p(x, y), radius=radius, color=color)

    def x_title(self, text, color=GREY_A, font_size=26) -> Tex:
        return label(text, color=color, font_size=font_size).next_to(self.x_labels, DOWN, buff=0.15)

    def y_title(self, text, color=GREY_A, font_size=26) -> Tex:
        return label(text, color=color, font_size=font_size).next_to(self.y_axis, UP, buff=0.2).align_to(self.y_axis, LEFT)


def log_ticks_ns(lo_exp: int, hi_exp: int):
    """Ticks at powers of ten (ns) and their labels."""
    ticks = [10.0**e for e in range(lo_exp, hi_exp + 1)]
    return ticks, (lambda v: fmt_ns(v))


# ---------------------------------------------------------------------------
# Bytes and packets
# ---------------------------------------------------------------------------
def byte_strip(data: bytes, colors=None, cell=0.42, font_size=20, gap=0.04, fill=0.22) -> VGroup:
    """A row of byte cells, each showing its two hex digits."""
    g = VGroup()
    for i, b in enumerate(data):
        col = colors[i] if colors else GREY_B
        sq = RoundedRectangle(width=cell, height=cell * 1.15, corner_radius=0.04, stroke_width=1.2, stroke_color=col,
                              fill_color=col, fill_opacity=fill)
        t = Mono(f"{b:02X}", font_size=font_size, color=WHITE).move_to(sq)
        c = VGroup(sq, t)
        c.box, c.text = sq, t
        g.add(c)
    g.arrange(RIGHT, buff=gap)
    return g


def field_brace(cells: VGroup, text: str, color=WHITE, direction=DOWN, font_size=22, buff=0.06) -> VGroup:
    b = Brace(cells, direction=direction, buff=buff, color=color, sharpness=1.5)
    t = label(text, font_size=font_size, color=color).next_to(b, direction, buff=0.08)
    return VGroup(b, t)


def packet(color=C.MSG, width=0.55, height=0.32, text=None, font_size=16) -> VGroup:
    r = RoundedRectangle(width=width, height=height, corner_radius=0.06, stroke_width=1.5, stroke_color=color,
                         fill_color=color, fill_opacity=0.6)
    g = VGroup(r)
    if text:
        g.add(Mono(text, font_size=font_size, color=WHITE).move_to(r))
    return g


# ---------------------------------------------------------------------------
# Machines
# ---------------------------------------------------------------------------
def server_box(text: str = "", color=GREY_B, width=2.2, height=1.3, font_size=24) -> VGroup:
    body = RoundedRectangle(width=width, height=height, corner_radius=0.1, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.12)
    slots = VGroup(*[Line(LEFT * width * 0.38, RIGHT * width * 0.38, stroke_width=1.5, color=color, stroke_opacity=0.6)
                     for _ in range(3)]).arrange(DOWN, buff=height * 0.12).move_to(body).shift(UP * height * 0.18)
    leds = VGroup(*[Dot(radius=0.035, color=GREEN) for _ in range(3)]).arrange(RIGHT, buff=0.08)
    leds.next_to(body.get_corner(DR), UL, buff=0.12)
    g = VGroup(body, slots, leds)
    if text:
        g.add(label(text, font_size=font_size).move_to(body).shift(DOWN * height * 0.22))
    g.body = body
    return g


def cpu_die(n_cores=4, color=GREY_B, size=2.4, labels=None) -> VGroup:
    """A chip outline with a grid of cores; .cores[i] is a Square."""
    die = RoundedRectangle(width=size, height=size, corner_radius=0.08, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.08)
    pins = VGroup()
    for k in range(8):
        for side in (UP, DOWN, LEFT, RIGHT):
            off = (k - 3.5) * size / 9
            p = die.get_edge_center(side) + (RIGHT if side[1] != 0 else UP) * off
            pins.add(Line(p, p + side * 0.12, color=color, stroke_width=2))
    m = int(math.ceil(math.sqrt(n_cores)))
    cores = VGroup(*[Square(size / (m + 0.9), stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=0.15)
                     for _ in range(n_cores)]).arrange_in_grid(m, m, buff=size * 0.06).move_to(die)
    g = VGroup(pins, die, cores)
    if labels:
        for c, t in zip(cores, labels):
            g.add(label(t, font_size=20).move_to(c))
    g.die, g.cores = die, cores
    return g


def flow_arrow(a, b, color=GREY_B, stroke_width=3, buff=0.1, tip=0.18) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke_width, max_tip_length_to_length_ratio=0.3,
                 tip_length=tip)


# ---------------------------------------------------------------------------
# Animated dots travelling along paths (packets on wires, photons)
# ---------------------------------------------------------------------------
def travel(dot: Mobject, path: VMobject, run_time=1.0, rate_func=linear, **kw) -> Animation:
    return MoveAlongPath(dot, path, run_time=run_time, rate_func=rate_func, **kw)


# ---------------------------------------------------------------------------
# The map (Natural Earth lakes, US state outlines; equirectangular, scaled by cos(latitude))
# ---------------------------------------------------------------------------
class GeoMap(VGroup):
    def __init__(self, width=13.4, lat_c=41.6, lon_c=-81.0, state_color=GREY_D, lake_color="#1C3550"):
        super().__init__()
        g = load("geo")
        lon0, lon1, lat0, lat1 = g["box"]
        self.k = width / ((lon1 - lon0) * math.cos(math.radians(lat_c)))
        self.lat_c, self.lon_c = lat_c, lon_c
        self.sea = Polygon(self.p(lat0, lon0), self.p(lat0, lon1), self.p(lat1, lon1), self.p(lat1, lon0), stroke_width=0,
                           fill_color=lake_color, fill_opacity=0.55)
        self.land = VGroup(*[Polygon(*[self.p(lat, lon) for lon, lat in ring], stroke_width=0, fill_color="#161C25",
                                     fill_opacity=1.0) for ring in g["land"]])
        self.states = VGroup()
        for name, rings in g["states"].items():
            for ring in rings:
                pts = [self.p(lat, lon) for lon, lat in ring]
                self.states.add(Polygon(*pts, stroke_color=state_color, stroke_width=1.2, fill_opacity=0))
        self.lakes = VGroup()
        for name, rings in g["lakes"].items():
            for ring in rings:
                pts = [self.p(lat, lon) for lon, lat in ring]
                self.lakes.add(Polygon(*pts, stroke_width=0, fill_color=lake_color, fill_opacity=1.0))
        self.add(self.sea, self.land, self.lakes, self.states)
        self.sites = g["sites"]
        self.routes = g["routes"]

    def p(self, lat, lon):
        x = (lon - self.lon_c) * math.cos(math.radians(self.lat_c)) * self.k
        y = (lat - self.lat_c) * self.k
        return np.array([x, y, 0.0])

    def site(self, key):
        s = self.sites[key]
        return self.p(s["lat"], s["lon"])

    def route(self, key, color=C.LIGHT, stroke_width=4) -> VMobject:
        pts = [self.p(lat, lon) for lon, lat in self.routes[key]["path"]]
        return VMobject().set_points_smoothly(pts).set_stroke(color, stroke_width)


# ---------------------------------------------------------------------------
# The loop: the trading system as one cycle (a recurring "you are here" map)
# ---------------------------------------------------------------------------
LOOP_STAGES = [
    ("exchange", r"Exchange", C.TRADE),
    ("feed", r"Feed\\handler", C.MSG),
    ("book", r"Order\\book", C.MSG),
    ("signal", r"Fair\\value", C.SIGNAL),
    ("quote", r"Quoting", C.OURS),
    ("risk", r"Risk\\checks", C.RISK),
    ("gateway", r"Order\\gateway", C.ORDER),
]


def loop_diagram(width=12.6, box_w=1.45, box_h=1.05, font_size=22) -> VGroup:
    """Seven boxes in a row with arrows (market data flowing right), and a return path along the bottom
    (orders flowing back to the exchange).  ``.nodes[name]`` gives each box; ``.arrows`` the forward arrows;
    ``.ret`` the return path."""
    g = VGroup()
    nodes = {}
    xs = np.linspace(-width / 2 + box_w / 2, width / 2 - box_w / 2, len(LOOP_STAGES))
    for (key, text, col), x in zip(LOOP_STAGES, xs):
        n = node(text, color=col, width=box_w, height=box_h, font_size=font_size)
        n.move_to([x, 0, 0])
        nodes[key] = n
        g.add(n)
    arrows = VGroup()
    keys = [k for k, _, _ in LOOP_STAGES]
    for a, b in zip(keys[:-1], keys[1:]):
        col = C.MSG if b in ("feed", "book", "signal") else (C.ORDER if b in ("risk", "gateway") else GREY_B)
        arrows.add(Arrow(nodes[a].get_right(), nodes[b].get_left(), buff=0.06, color=col, stroke_width=3,
                         max_tip_length_to_length_ratio=0.35, tip_length=0.14))
    y = -box_h / 2 - 0.45
    p0, p3 = nodes["gateway"].get_bottom(), nodes["exchange"].get_bottom()
    ret = VMobject().set_points_as_corners([p0, [p0[0], y, 0], [p3[0], y, 0], p3 + DOWN * 0.06])
    ret.set_stroke(C.ORDER, 3)
    tip = Triangle(fill_color=C.ORDER, fill_opacity=1, stroke_width=0).scale(0.09).rotate(0).move_to(p3 + DOWN * 0.13)
    g.add(arrows, ret, tip)
    g.nodes, g.arrows, g.ret, g.ret_tip, g.keys = nodes, arrows, VGroup(ret, tip), tip, keys
    return g


def loop_focus(loop: VGroup, keys, dim=0.25):
    """Animations that dim every stage except ``keys``."""
    keys = [keys] if isinstance(keys, str) else keys
    anims = []
    for k, n in loop.nodes.items():
        op = 1.0 if k in keys else dim
        anims.append(n.box.animate.set_stroke(opacity=op).set_fill(opacity=(0.35 if k in keys else 0.15) * op))
        anims.append(n.text.animate.set_opacity(op))
    for a in loop.arrows:
        anims.append(a.animate.set_opacity(dim))
    anims.append(loop.ret.animate.set_stroke(opacity=dim).set_fill(opacity=dim))
    return anims


def loop_reset(loop: VGroup):
    anims = []
    for n in loop.nodes.values():
        anims.append(n.box.animate.set_stroke(opacity=1).set_fill(opacity=0.15))
        anims.append(n.text.animate.set_opacity(1))
    for a in loop.arrows:
        anims.append(a.animate.set_opacity(1))
    anims.append(loop.ret.animate.set_stroke(opacity=1).set_fill(opacity=1))
    return anims


# ---------------------------------------------------------------------------
# The order book as a ladder: prices down the middle, every resting order a block in its queue
# ---------------------------------------------------------------------------
def order_width(shares: float) -> float:
    return float(np.clip(0.085 * np.sqrt(shares), 0.07, 1.9))


class Ladder(VGroup):
    """Asks above, bids below, prices in the middle column.  Each order is a block whose width grows with
    its size (square root, capped); the front of each queue touches the price column, so a level's queue
    reads outward from the middle (bids to the left, asks to the right).

    bids / asks: [(price_cents, [shares, ...] front to back), ...], best first.
    ``.blocks[(side, price)]`` is the VGroup of a level's order blocks; ``.row_y[price]`` its y."""

    def __init__(self, bids, asks, row_h=0.46, price_w=1.5, gap=0.035, font_size=24, show_totals=True,
                 max_len=4.9):
        super().__init__()
        self.row_h, self.price_w, self.gap, self.max_len = row_h, price_w, gap, max_len
        self.origin = VectorizedPoint(ORIGIN)
        self.add(self.origin)
        prices = sorted({p for p, _ in bids} | {p for p, _ in asks}, reverse=True)
        lo, hi = min(prices), max(prices)
        self.prices = list(range(hi, lo - 1, -1))
        self.row_y = {p: (len(self.prices) - 1) / 2 * row_h - i * row_h for i, p in enumerate(self.prices)}
        self.price_labels = VGroup()
        self.rows_bg = VGroup()
        best_bid = bids[0][0] if bids else None
        best_ask = asks[0][0] if asks else None
        for p in self.prices:
            y = self.row_y[p]
            col = C.ASK if (best_ask is not None and p >= best_ask) else (C.BID if (best_bid is not None and p <= best_bid) else GREY_B)
            t = MathTex(f"{p / 100:.2f}", font_size=font_size, color=col).move_to([0, y, 0])
            self.price_labels.add(t)
            bg = Rectangle(width=2 * max_len + price_w, height=row_h * 0.92, stroke_width=0, fill_color=WHITE,
                           fill_opacity=0.025).move_to([0, y, 0])
            self.rows_bg.add(bg)
        self.add(self.rows_bg, self.price_labels)
        self.blocks = {}
        self.totals = VGroup()
        for side, levels in (("B", bids), ("S", asks)):
            for p, sizes in levels:
                g = self.make_queue(side, p, sizes)
                self.blocks[(side, p)] = g
                self.add(g)
                if show_totals and sizes:
                    tot = MathTex(fmt_int(sum(sizes)), font_size=18, color=GREY_B)
                    self.place_total(tot, side, p, g)
                    self.totals.add(tot)
        self.add(self.totals)

    def side_color(self, side):
        return C.BID if side == "B" else C.ASK

    def block(self, side, shares, color=None) -> Rectangle:
        col = color or self.side_color(side)
        return Rectangle(width=order_width(shares), height=self.row_h * 0.7, stroke_width=1.2, stroke_color=col,
                         fill_color=col, fill_opacity=0.55)

    def anchor(self, side, price):
        """Where the front of a queue starts (the edge of the price column)."""
        x = -self.price_w / 2 if side == "B" else self.price_w / 2
        return self.origin.get_center() + np.array([x, self.row_y[price], 0])

    def make_queue(self, side, price, sizes) -> VGroup:
        g = VGroup()
        x = self.anchor(side, price)[0]
        y = self.anchor(side, price)[1]
        d = -1 if side == "B" else 1
        used = 0.0
        for s in sizes:
            b = self.block(side, s)
            w = b.width
            if used + w > self.max_len:
                b = Rectangle(width=max(self.max_len - used - self.gap, 0.05), height=self.row_h * 0.7, stroke_width=0,
                              fill_color=self.side_color(side), fill_opacity=0.2)
                w = b.width
                b.move_to([x + d * (used + self.gap + w / 2), y, 0])
                g.add(b)  # a faded stub: the queue continues off the ladder
                break
            b.move_to([x + d * (used + self.gap + w / 2), y, 0])
            used += w + self.gap
            g.add(b)
        return g

    def queue_end(self, side, price) -> np.ndarray:
        g = self.blocks.get((side, price))
        a = self.anchor(side, price)
        if g is None or not len(g):
            return a
        return g.get_left() if side == "B" else g.get_right()

    def place_total(self, tot, side, price, g):
        end = self.queue_end(side, price)
        tot.move_to(end + (LEFT if side == "B" else RIGHT) * (0.15 + tot.width / 2))
        tot.set_y(self.anchor(side, price)[1])

    def append_anim(self, side, price, shares, color=None, run_time=0.4):
        """A new order joins the back of a queue."""
        end = self.queue_end(side, price)
        b = self.block(side, shares, color)
        d = LEFT if side == "B" else RIGHT
        b.move_to(end + d * (self.gap + b.width / 2))
        g = self.blocks.setdefault((side, price), VGroup())
        g.add(b)
        return FadeIn(b, shift=-d * 0.3, run_time=run_time), b

    def remove_anim(self, side, price, index, color=None, run_time=0.4):
        """Remove the order at queue position ``index``; the ones behind slide forward."""
        g = self.blocks[(side, price)]
        b = g[index]
        w = b.width + self.gap
        d = RIGHT if side == "B" else LEFT  # toward the price column
        behind = VGroup(*g[index + 1:])
        g.remove(b)
        anims = [FadeOut(b, scale=0.6)]
        if color is not None:
            anims = [b.animate.set_fill(color, 0.9).set_stroke(color).scale(0.6).set_opacity(0)]
        if len(behind):
            anims.append(behind.animate.shift(d * w))
        return AnimationGroup(*anims, run_time=run_time)


def part_card(number: int, title: str, subtitle: str = "") -> VGroup:
    num = label(rf"Part {number}", font_size=34, color=C.DIM)
    t = label(title, font_size=60)
    g = VGroup(num, t)
    if subtitle:
        g.add(label(subtitle, font_size=30, color=GREY_A))
    return g.arrange(DOWN, buff=0.3)


def show_part(scene, number: int, title: str, subtitle: str = "", hold=1.6):
    card = part_card(number, title, subtitle)
    scene.play(FadeIn(card, shift=UP * 0.2), run_time=0.8)
    scene.wait(hold)
    scene.play(FadeOut(card, shift=UP * 0.2), run_time=0.6)


def person(color=GREY_B, scale=1.0) -> VGroup:
    head = Circle(radius=0.16, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.25)
    body = Arc(radius=0.3, start_angle=0, angle=PI, stroke_color=color, stroke_width=2.5)
    body.next_to(head, DOWN, buff=0.05)
    body.add(Line(body.get_start(), body.get_end(), stroke_color=color, stroke_width=2.5))
    return VGroup(head, body).scale(scale)


def stack_braces(strip: VGroup, specs, font_size=21, step=0.62, x_margin=6.95) -> VGroup:
    """Braces under/over byte cells whose labels never overlap: a label that would collide with an earlier one
    on the same side is pushed one row further out.  specs: [(first_cell, n_cells, text, color, UP|DOWN)]."""
    placed = {"up": [], "down": []}
    out = VGroup()
    for first, n, text, color, direction in specs:
        cells = strip[first:first + n]
        key = "up" if direction[1] > 0 else "down"
        level = 0
        while True:
            br = Brace(cells, direction=direction, buff=0.06 + level * step, color=color, sharpness=1.5)
            t = label(text, font_size=font_size, color=color).next_to(br, direction, buff=0.08)
            if t.get_left()[0] < -x_margin:
                t.shift(RIGHT * (-x_margin - t.get_left()[0]))
            if t.get_right()[0] > x_margin:
                t.shift(LEFT * (t.get_right()[0] - x_margin))
            box = (t.get_left()[0] - 0.08, t.get_right()[0] + 0.08, level)
            if any(lv == level and not (box[1] < a or box[0] > b) for a, b, lv in placed[key]):
                level += 1
                continue
            placed[key].append(box)
            out.add(VGroup(br, t))
            break
    return out


def scatter(points, color=WHITE, size=3, opacity=0.85) -> PMobject:
    """Many points as one point cloud (far cheaper than thousands of Dots)."""
    pm = PMobject(stroke_width=size)
    pts = np.asarray(points, float)
    if len(pts):
        rgba = np.tile(np.r_[color_to_rgb(color), opacity], (len(pts), 1))
        pm.add_points(pts, rgbas=rgba)
    return pm
