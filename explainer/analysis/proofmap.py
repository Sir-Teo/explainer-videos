"""The proof map (instrument 6 of the series plan): a long proof's four or five steps as a small flowchart that
lights up as the narration reaches each step.  Steps already done turn green, the current one yellow, later ones
stay dim, so the viewer always knows where in the argument the line-by-line work on screen belongs."""

from __future__ import annotations

from manim import DOWN, RIGHT, Arrow, RoundedRectangle, VGroup

from explainer.style import BACKGROUND, C, GREY_D, TEX_TEMPLATE  # noqa: F401
from manim import Tex


def _split(s: str):
    """Split a step's text in two at the break (a space or a TeX "\\ " outside math and braces) nearest its middle."""
    cuts, depth, math, i = [], 0, False, 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            if s[i + 1] == " " and depth == 0 and not math:
                cuts.append((i, i + 2))
            i += 2
            continue
        if ch == "$":
            math = not math
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif ch == " " and depth == 0 and not math:
            cuts.append((i, i + 1))
        i += 1
    if not cuts:
        return None
    a, b = min(cuts, key=lambda c: abs(c[0] - len(s) / 2))
    first, second = s[:a].strip(), s[b:].strip()
    while second.startswith("\\ "):  # a TeX space at the start of the second line
        second = second[2:].lstrip()
    while first.endswith("\\"):
        first = first[:-1].rstrip()
    return (first, second) if first and second else None


def _fit(text: str, prefix: str, font_size, inner: float):
    """The step's Tex at its font size; too wide, it goes onto two centred lines before it is ever shrunk."""
    t = Tex(prefix + text, font_size=font_size, tex_template=TEX_TEMPLATE)
    if t.width <= inner:
        return t
    if inner / t.width < 0.85:
        cut = _split(text)
        if cut:
            t2 = Tex(r"\begin{tabular}{@{}c@{}}" + prefix + cut[0] + r" \\ " + cut[1] + r"\end{tabular}",
                     font_size=font_size, tex_template=TEX_TEMPLATE)
            if t2.width < t.width:
                t = t2
    if t.width > inner:
        t.width = inner
    return t


class ProofMap(VGroup):
    def __init__(self, steps, font_size=20, width=2.6, buff=0.32, direction=RIGHT, numbered=True):
        boxes = VGroup()
        for i, s in enumerate(steps):
            t = _fit(s, rf"\textbf{{{i + 1}.}} " if numbered else "", font_size, width - 0.22)
            r = RoundedRectangle(corner_radius=0.1, width=width, height=t.height + 0.28, stroke_color=GREY_D,
                                 stroke_width=2, fill_color=BACKGROUND, fill_opacity=0.0)
            boxes.add(VGroup(r, t))
        h = max(b[0].height for b in boxes)
        for b in boxes:
            b[0].stretch_to_fit_height(h)
            b[1].move_to(b[0])
            b[1].set_opacity(0.45)
        boxes.arrange(direction, buff=buff)
        arrows = VGroup()
        for a, b in zip(boxes[:-1], boxes[1:]):
            if direction is RIGHT or tuple(direction) == tuple(RIGHT):
                p, q = a.get_right(), b.get_left()
            else:
                p, q = a.get_bottom(), b.get_top()
            arrows.add(Arrow(p, q, buff=0.04, color=GREY_D, stroke_width=2.5, tip_length=0.12,
                             max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20))
        super().__init__(boxes, arrows)
        self.boxes, self.arrows = boxes, arrows

    def light(self, i):
        """Animations that make step i current (earlier steps done, later ones dim)."""
        anims = []
        for j, b in enumerate(self.boxes):
            if j < i:
                anims += [b[0].animate.set_stroke(C.CONNECTED_SET, 2).set_fill(C.CONNECTED_SET, 0.10),
                          b[1].animate.set_opacity(0.8)]
            elif j == i:
                anims += [b[0].animate.set_stroke(C.EPS, 3).set_fill(C.EPS, 0.16), b[1].animate.set_opacity(1.0)]
            else:
                anims += [b[0].animate.set_stroke(GREY_D, 2).set_fill(BACKGROUND, 0.0), b[1].animate.set_opacity(0.45)]
        for j, a in enumerate(self.arrows):
            anims.append(a.animate.set_color(C.CONNECTED_SET if j < i else GREY_D))
        return anims

    def done(self):
        """Every step green."""
        return self.light(len(self.boxes))
