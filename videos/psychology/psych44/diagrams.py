"""Small path diagrams shared by the scenes of Part 44."""

from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403


def node(text: str, color=WHITE, latent: bool = False, r: float = 0.36) -> VGroup:
    shape = Circle(radius=r, color=color, stroke_width=2.5) if latent else Square(2 * r, color=color, stroke_width=2.5)
    return VGroup(shape, label(text, font_size=20, color=color).move_to(shape))


def arrow(a: VGroup, b: VGroup, color=GREY_A, text: str | None = None, double: bool = False) -> VGroup:
    cls = DoubleArrow if double else Arrow
    ar = cls(a.get_center(), b.get_center(), buff=0.42, color=color, stroke_width=3,
             max_tip_length_to_length_ratio=0.18)
    g = VGroup(ar)
    if text:
        g.add(label(text, font_size=16, color=color).next_to(ar.get_center(), UP, buff=0.08))
    return g


def three(kind: str, color=PERSON) -> VGroup:
    """X, M, Y in a row with arrows for a chain ('chain'), the reverse ('reverse'), a fork ('fork') or a collider."""
    X, M, Y = node("X", color), node("M", color), node("Y", color)
    VGroup(X, M, Y).arrange(RIGHT, buff=1.0)
    if kind == "chain":
        arr = VGroup(arrow(X, M), arrow(M, Y))
    elif kind == "reverse":
        arr = VGroup(arrow(M, X), arrow(Y, M))
    elif kind == "fork":
        arr = VGroup(arrow(M, X), arrow(M, Y))
    else:
        arr = VGroup(arrow(X, M), arrow(Y, M))
    return VGroup(X, M, Y, arr)
