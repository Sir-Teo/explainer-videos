"""Helpers shared by the scenes of Part 36 ("Networks I: Moving Bits")."""

from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs6.common import box, fmt, sci  # noqa: F401
from videos.cs.cs7.common import mono  # noqa: F401
from videos.cs.cs8.common import bar_chart, grid_table  # noqa: F401
from videos.cs.cs11.common import code  # noqa: F401
from videos.cs.cs30.common import curve, fit_right, flow_box, log_axes  # noqa: F401
from videos.cs.cs31.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, KERN, LAM, NO, YES, edge_arrow,  # noqa: F401
                                   kv_rows)
from videos.cs.cs34.common import ms, num  # noqa: F401

from .compute import load  # noqa: F401

PART = 36
ETH, IPC, UDPC, PAY = KERN, HEAD, LAM, YES          # layer colours: link, network, transport, data
LAYERC = {"Ethernet": ETH, "IP": IPC, "UDP": UDPC, "TCP": UDPC, "data": PAY, "FCS": ETH}


def header_strip(parts, unit=0.075, h=0.62, font=17, min_w=0.9):
    """Boxes side by side, one per (name, bytes, colour); width grows with the byte count."""
    g = VGroup()
    for name, n, c in parts:
        w = max(min_w, unit * n)
        r = Rectangle(width=w, height=h, stroke_color=c, stroke_width=1.8, fill_color=c, fill_opacity=0.18)
        t = label(rf"{name} \ {n}", font_size=font, color=c).move_to(r)
        if t.width > w - 0.08:
            t.width = w - 0.08
        g.add(VGroup(r, t))
    g.arrange(RIGHT, buff=0)
    return g


def project(lat: float, lon: float, w: float = 12.4, h: float = 5.6, lon0: float = 10.0):
    """An equirectangular map, centred on longitude lon0, wrapped into [-180, 180)."""
    x = ((lon - lon0 + 180) % 360) - 180
    return np.array([x / 180 * w / 2, lat / 90 * h / 2, 0.0])


NAMES = {"sfo": "San Francisco", "nyc": "New York", "lon": "London", "ams": "Amsterdam", "fra": "Frankfurt",
         "par": "Paris", "sgp": "Singapore", "tok": "Tokyo"}


SCHEMATIC = {"sfo": (-5.6, 0.2), "nyc": (-2.9, 0.7), "lon": (0.1, 1.5), "ams": (1.5, 2.2), "fra": (2.4, 0.9),
             "par": (0.7, 0.0), "sgp": (4.4, -1.6), "tok": (5.7, 0.4)}


def world(cities: dict, links: list, scale: float = 1.0, shift=ORIGIN, names: bool = True, font: int = 17,
          lon0: float = 10.0):
    """Routers at their cities on a schematic map (not to scale), cables between them; the Pacific cable from
    Tokyo to San Francisco leaves the right edge and comes back at the left.  Returns a VGroup with .pos, .dots, .edges (keyed by a
    sorted pair) and .labels."""
    g = VGroup()
    g.pos = {c: np.array([*SCHEMATIC[c], 0.0]) * scale + np.array(shift) if c in SCHEMATIC
             else project(*cities[c], lon0=lon0) * scale + np.array(shift) for c in cities}
    g.edges = {}
    edges = VGroup()
    for a, b, _ in links:
        if {a, b} == {"tok", "sfo"}:          # the Pacific: off the right edge, back in at the left
            ln = VGroup(DashedLine(g.pos["tok"], g.pos["tok"] + RIGHT * (6.95 - g.pos["tok"][0]), color=GREY_C,
                                   stroke_width=2),
                        DashedLine(g.pos["sfo"] + LEFT * (g.pos["sfo"][0] + 6.95), g.pos["sfo"], color=GREY_C,
                                   stroke_width=2))
        else:
            ln = Line(g.pos[a], g.pos[b], color=GREY_C, stroke_width=2)
        g.edges[tuple(sorted((a, b)))] = ln
        edges.add(ln)
    g.dots = {c: Dot(g.pos[c], radius=0.08, color=HEAD) for c in cities}
    g.labels = {}
    labs = VGroup()
    side = {"par": DOWN, "fra": RIGHT, "sgp": DOWN, "ams": UP, "lon": LEFT + UP * 0.3, "tok": UP, "sfo": UP,
            "nyc": UP}
    if names:
        for c in cities:
            lab = label(NAMES.get(c, c), font_size=font, color=GREY_A).next_to(g.pos[c], side.get(c, UP), buff=0.1)
            g.labels[c] = lab
            labs.add(lab)
    g.add(edges, VGroup(*g.dots.values()), labs)
    return g


def graph(pos: dict, edges, color=GREY_C, node_color=HEAD, r=0.28, font=20, weights=None):
    """A small graph with named circular nodes at ``pos``; ``weights`` labels edges."""
    g = VGroup()
    g.nodes, g.edges, g.wl = {}, {}, {}
    ev = VGroup()
    for a, b in edges:
        ln = Line(pos[a], pos[b], color=color, stroke_width=2.2)
        g.edges[tuple(sorted((a, b)))] = ln
        ev.add(ln)
        if weights:
            w = weights.get((a, b), weights.get((b, a)))
            if w is not None:
                t = label(str(w), font_size=font - 4, color=GREY_B).move_to(ln.get_center() + UP * 0.18)
                g.wl[tuple(sorted((a, b)))] = t
                ev.add(t)
    nv = VGroup()
    for n, p in pos.items():
        c = Circle(radius=r, stroke_color=node_color, stroke_width=2.2, fill_color=BG, fill_opacity=1).move_to(p)
        t = label(str(n), font_size=font, color=node_color).move_to(c)
        g.nodes[n] = VGroup(c, t)
        nv.add(g.nodes[n])
    g.add(ev, nv)
    return g
