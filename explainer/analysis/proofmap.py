"""The proof map (instrument 6 of the series plan): a long proof's four or five steps as a small flowchart that
lights up as the narration reaches each step.  Steps already done turn green, the current one yellow, later ones
stay dim, so the viewer always knows where in the argument the line-by-line work on screen belongs."""

from __future__ import annotations

from manim import DOWN, RIGHT, Arrow, RoundedRectangle, VGroup

from explainer.style import BACKGROUND, C, GREY_D, TEX_TEMPLATE  # noqa: F401
from manim import Tex


class ProofMap(VGroup):
    def __init__(self, steps, font_size=20, width=2.6, buff=0.32, direction=RIGHT, numbered=True):
        boxes = VGroup()
        for i, s in enumerate(steps):
            t = Tex((rf"\textbf{{{i + 1}.}} " if numbered else "") + s, font_size=font_size, tex_template=TEX_TEMPLATE)
            if t.width > width - 0.22:
                t.width = width - 0.22
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
