from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import TEST, curve, load

POS, NEG = "#58A6FF", "#E86F8A"


def find_line(P, s):
    """A separating line (w, b) for the labels s, or None."""
    for th in np.linspace(0, 2 * math.pi, 720, endpoint=False):
        w = np.array([math.cos(th), math.sin(th)])
        pr = P @ w
        pos, neg = pr[s > 0], pr[s < 0]
        if len(pos) == 0:
            return w, -(pr.max() + 0.6)
        if len(neg) == 0:
            return w, -(pr.min() - 0.6)
        if pos.min() > neg.max() + 0.05:
            return w, -0.5 * (pos.min() + neg.max())
    return None


class Capacity(VoiceoverScene):
    def construct(self):
        self.card()
        self.shatter()
        self.coins()

    def card(self):
        card = chapter_card(2, r"How much can a model fit?", r"Capacity, and what it promises", part=7)
        with self.voiceover("Chapter two. Measuring how much a model can fit."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def panel(self, P, s, center, size=1.15):
        box = Square(2 * size + 0.6, stroke_color=GREY_D, stroke_width=1.5).move_to(center)
        dots = VGroup(*[Dot(np.asarray(center) + size * np.array([*p, 0]) * 0.8, radius=0.09, color=POS if v > 0 else NEG)
                        for p, v in zip(P, s)])
        fl = find_line(P, s)
        if fl is None:
            mark = Cross(box, stroke_color=C.SURPRISE, stroke_width=4).scale(0.35)
            return VGroup(box, dots, mark), False
        w, b = fl
        d = np.array([-w[1], w[0]])
        p0 = -b * w  # a point on the line
        half = 0.5 * box.width
        a_ = np.asarray(center) + size * 0.8 * np.array([*(p0 - 3 * d), 0])
        b_ = np.asarray(center) + size * 0.8 * np.array([*(p0 + 3 * d), 0])
        line = Line(a_, b_, color=C.BITS, stroke_width=3)
        # clip to the box
        line.put_start_and_end_on(*self.clip(a_, b_, np.asarray(center), half))
        return VGroup(box, dots, line), True

    @staticmethod
    def clip(a, b, c, h):
        pts = []
        for t in np.linspace(0, 1, 400):
            p = a + t * (b - a)
            if abs(p[0] - c[0]) <= h and abs(p[1] - c[1]) <= h:
                pts.append(p)
        return (pts[0], pts[-1]) if pts else (c, c)

    def shatter(self):
        s = load("shatter")
        P3, P4 = np.asarray(s["P3"]), np.asarray(s["P4"])
        L3, L4 = np.asarray(s["labs3"]), np.asarray(s["labs4"])
        p3 = VGroup(*[self.panel(P3, L3[k], [-5.6 + 1.6 * (k % 4) * 1.0, 1.7 - 2.0 * (k // 4), 0], size=0.55)[0]
                      for k in range(8)])
        p3.move_to([-3.3, 0.4, 0])
        bad = [k for k in range(16) if not s["ok4"][k]]
        good = [k for k in range(16) if s["ok4"][k]][:2]
        p4 = VGroup(*[self.panel(P4, L4[k], ORIGIN, size=0.55)[0] for k in good + bad])
        p4.arrange_in_grid(rows=2, cols=2, buff=0.25).move_to([3.6, 0.4, 0])
        t3 = label(r"$3$ points: \ all $8$ labellings, \ a line for each", font_size=26).next_to(p3, UP, buff=0.3)
        t4 = label(r"$4$ points: \ no line for these two", font_size=26).next_to(p4, UP, buff=0.3)
        vc = label(r"lines in the plane: \ VC dimension $3$", font_size=30, color=C.BITS).to_edge(DOWN, buff=1.45)
        colors = {r"d": C.BITS, r"n": TEST}
        bound = cmath(r"\text{error}_{\text{new}}", r"\le", r"\text{error}_{\text{train}}", "+",
                      r"\sqrt{\frac{d\,(\ln(2n/d) + 1) + \ln(4/\delta)}{n}}", colors=colors, font_size=32)
        bound.to_edge(DOWN, buff=0.3)
        gap = label(r"the gap shrinks \\ as the examples $n$ \\ outnumber the capacity $d$", font_size=22, color=GREY_A)
        gap.next_to(bound, RIGHT, buff=0.35)
        cite_ = cite(r"V.~Vapnik \& A.~Chervonenkis (1971)", corner=UR)
        with self.voiceover(
            "Here's the classical way to measure what a family of models can fit. Take straight lines in the plane, "
            "and three points. <bookmark mark='a'/> Colour the points any of the eight possible ways, and some line "
            "separates the colours every time. <bookmark mark='b'/> With four points, it fails: these two labellings "
            "can't be split by any line. <bookmark mark='c'/> The largest number of points a family can split in "
            "every way is its VC dimension, after Vapnik and Chervonenkis: three, for lines in the plane. "
            "<bookmark mark='d'/> And it buys a guarantee: with n examples, the error on new data exceeds the "
            "training error by at most about the square root of d over n. In plain words: the gap between training "
            "and new error shrinks as the examples outnumber the capacity."
        ) as vo:
            self.play(FadeIn(t3), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in p3], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(t4), LaggedStart(*[FadeIn(p) for p in p4], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(vc))
            vo.wait_until("d")
            self.play(Write(bound))
            self.play(FadeIn(gap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def coins(self):
        r = load("rademacher")
        ds, acc = np.asarray(r["ds"]), np.asarray(r["acc"])
        ax = Axes(x_range=[0, 70, 10], y_range=[0.5, 0.8, 0.1], x_length=8.0, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.4, -0.5, 0])
        yl = VGroup(*[MathTex(rf"{int(round(100 * v))}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0.5, 0.6, 0.7, 0.8)])
        xl = label(r"how many of the $70$ word rates the line may use", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.25)
        yn = label(r"coin flips fitted", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        c = curve(ax, ds, np.clip(acc, 0.5, 0.8), C.MODEL_Q)
        dots = VGroup(*[Dot(ax.c2p(d, min(a, 0.8)), radius=0.06, color=C.MODEL_Q) for d, a in zip(ds, acc)])
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(70, 0.5), color=GREY_B)
        hl = label(r"guessing", font_size=22, color=GREY_B).next_to(half, DOWN, buff=0.08).align_to(half, RIGHT)
        note_ = label(r"the better a family fits pure noise, \\ the less its training score proves", font_size=28,
                      color=C.BITS).move_to([4.4, 1.4, 0])
        rad = label(r"Rademacher complexity", font_size=26, color=GREY_A).next_to(note_, DOWN, buff=0.25)
        with self.voiceover(
            "There's a more direct test. Give each of the training pages a random label, a coin flip, and ask a "
            "linear model to fit them. <bookmark mark='a'/> Using one word rate, it gets barely more than half. "
            f"Using all seventy, it fits {100 * acc[-1]:.0f} percent of the coin flips: pure noise. "
            "<bookmark mark='b'/> The better a family can fit noise, the less a good training score proves. That's "
            "Rademacher complexity, and like the VC dimension, it grows with the number of things a model can adjust."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), Create(half), FadeIn(hl))
            vo.wait_until("a")
            self.play(Create(c), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(note_), FadeIn(rad))
        self.wait(0.3)
        self.clear_scene()
