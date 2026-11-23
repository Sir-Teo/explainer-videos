"""Helpers shared by the scenes of Part 1 of *Industry, Built* ("Where the Money Goes"): the computed numbers,
the colours of each slice of the Dollar, the phone, the price tag."""

from __future__ import annotations

import numpy as np  # noqa: F401
from manim import *  # noqa: F403

from explainer.ai.viz import CornerAxes, glow_dot  # noqa: F401
from explainer.industry import draw  # noqa: F401
from explainer.industry import viz  # noqa: F401
from explainer.industry.kit import *  # noqa: F403
from explainer.industry.kit import chapter
from explainer.voiceover import VoiceoverScene  # noqa: F401

from .compute import results

PART = 1
ASK = "When you pay for something, who gets the money, and why them?"
R = results()

COL = {"channel": I.CHANNEL, "display": I.DISPLAY, "chip": I.CHIP, "camera": I.CAMERA, "rf": I.RF,
       "memory": I.MEMORY, "case": I.CASE, "power": I.POWER, "other": I.OTHER, "assembly": I.ASSEMBLY,
       "other_cogs": I.UNKNOWN, "opex": I.BRAND, "tax": I.TAX, "profit": I.PROFIT, "parts": "#8FA3BF"}
BODY_17 = "#3B2F2A"  # the phone's body colour (a dark copper), the same in every scene of this part


def card(scene, n, title: str, question: str, say: str, lit=()):
    chapter(scene, PART, n, title, question, say, lit=lit)


def price_tag(text: str, size: float = 34, color: str = I.MONEY) -> VGroup:
    t = TB(text, size, "#0E1117")
    box = RoundedRectangle(corner_radius=0.12, width=t.width + 0.5, height=t.height + 0.3, fill_color=color,
                           fill_opacity=1, stroke_width=0)
    hole = Circle(radius=0.06, fill_color="#0E1117", fill_opacity=1, stroke_width=0).move_to(
        box.get_left() + RIGHT * 0.16)
    t.move_to(box).shift(RIGHT * 0.08)
    return VGroup(box, hole, t)


def slices(which: str = "dollar17", collapse_parts: bool = False):
    """The Dollar's items for :class:`viz.DollarColumn`: (label, amount, colour, note)."""
    out = []
    parts = 0.0
    for s in R[which]["slices"]:
        if collapse_parts and s["group"] == "parts":
            parts += s["amount"]
            continue
        out.append((s["label"], s["amount"], COL[s["key"]], s["who"]))
    if collapse_parts:
        out.insert(1, ("All the parts", parts, COL["parts"], "about 200 suppliers"))
    return out


def amount(key: str, which: str = "dollar17") -> float:
    for s in R[which]["slices"]:
        if s["key"] == key:
            return s["amount"]
    raise KeyError(key)


def ipod(h: float = 3.0) -> VGroup:
    """A fifth-generation iPod: white body, screen, click wheel."""
    w = h * 0.6
    body = RoundedRectangle(corner_radius=h * 0.07, width=w, height=h, fill_color="#E9EBEE", fill_opacity=1,
                            stroke_color="#B8BDC6", stroke_width=2)
    scr = RoundedRectangle(corner_radius=0.04, width=w * 0.8, height=h * 0.36, fill_color="#1B2B3F",
                           fill_opacity=1, stroke_width=0).move_to(body.get_top() + DOWN * h * 0.24)
    wheel = Circle(radius=w * 0.3, fill_color="#F7F8FA", fill_opacity=1, stroke_color="#C9CDD4",
                   stroke_width=2).move_to(body.get_bottom() + UP * h * 0.27)
    hub = Circle(radius=w * 0.11, fill_color="#E9EBEE", fill_opacity=1, stroke_color="#C9CDD4",
                 stroke_width=1.5).move_to(wheel)
    return VGroup(body, scr, wheel, hub)
