from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis.analysis1.common import SQRT2, Window, dim, endpoint, polyline
from videos.analysis.analysis1.s02_holes import below_sqrt2


def bar(x0, x1, y, color, lc=True, rc=True, sw=7):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=sw),
                  endpoint([x0, y, 0], lc, color), endpoint([x1, y, 0], rc, color))


class Connected(VoiceoverScene):
    def construct(self):
        self.card()
        self.separated()
        self.intervals()
        self.rationals()
        self.sine_curve()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(10, r"Connectedness", r"What does it mean for a set to be in one piece?", lit=(1883,), part=1)
        with self.voiceover("Chapter ten. What does it mean for a set to be all in one piece?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def separated(self):
        X = lambda v: -5.6 + v * 3.0  # noqa: E731
        defs = VGroup(
            label(r"$A$ and $B$ are \textbf{separated} if \ $\overline{A} \cap B = \emptyset$ \ and \ $A \cap \overline{B} = \emptyset$.",
                  font_size=30),
            label(r"$E$ is \textbf{connected} if it is not a union of two nonempty separated sets. \ (Rudin 2.45)",
                  font_size=30, color=C.CONNECTED_SET),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)
        y1, y2 = 0.4, -1.4
        r1 = VGroup(bar(X(0), X(1), y1, C.SEQ, True, False), bar(X(1), X(2), y1, C.DELTA, True, True))
        l1 = MathTex(r"[0,1) \text{ and } [1,2]", font_size=32).move_to([X(1), y1 + 0.6, 0])
        v1 = VGroup(label(r"disjoint, but $1 \in \overline{[0,1)}$:", font_size=28, color=C.PATHOLOGY),
                    label(r"they touch", font_size=28, color=C.PATHOLOGY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        v1.next_to(r1, RIGHT, buff=0.5)
        r2 = VGroup(bar(X(0), X(1), y2, C.SEQ, False, False), bar(X(1), X(2), y2, C.DELTA, False, False))
        l2 = MathTex(r"(0,1) \text{ and } (1,2)", font_size=32).move_to([X(1), y2 + 0.6, 0])
        v2 = VGroup(label(r"separated: no point of either", font_size=28, color=C.CONNECTED_SET),
                    label(r"is a limit of the other", font_size=28, color=C.CONNECTED_SET)).arrange(DOWN, aligned_edge=LEFT,
                                                                                             buff=0.1)
        v2.next_to(r2, RIGHT, buff=0.5)
        # around the point 1, where the open intervals meet without touching
        gap = DashedVMobject(Circle(radius=0.38, color=C.EPS, stroke_width=2.5).move_to([X(1), y2, 0]), num_dashes=24)
        gap_l = label(r"$1$ is in neither", font_size=24, color=C.EPS).next_to(gap, DOWN, buff=0.12)
        with self.voiceover(
            "Rudin's definition is careful. <bookmark mark='s'/> Two sets are separated if neither one contains a point "
            "of the other's closure: they don't touch, even at a limit point. <bookmark mark='c'/> A set is connected if "
            "it can't be split into two nonempty separated pieces. <bookmark mark='a'/> The half-open interval from zero "
            "to one and the closed interval from one to two are disjoint, but they touch at one, which is a limit point "
            "of the first. Not separated. <bookmark mark='b'/> Remove the point one, and the two open intervals are "
            "separated."
        ) as vo:
            self.play(FadeIn(defs[0]), FadeIn(dim(r1, 0.3)), FadeIn(dim(r2, 0.3)))
            vo.wait_until("s")
            self.play(ApplyFunction(lambda m_: dim(m_, 1.0), r2), Create(gap), FadeIn(gap_l))
            vo.wait_until("c")
            self.play(FadeIn(defs[1]), ApplyFunction(lambda m_: dim(m_, 0.3), r2), FadeOut(gap), FadeOut(gap_l))
            vo.wait_until("a")
            self.play(ApplyFunction(lambda m_: dim(m_, 1.0), r1), FadeIn(l1))
            self.play(FadeIn(v1))
            vo.wait_until("b")
            self.play(ApplyFunction(lambda m_: dim(m_, 1.0), r2), FadeIn(l2))
            self.play(FadeIn(v2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def intervals(self):
        stmt = VGroup(label(r"\textbf{Theorem} (Rudin 2.47)", font_size=28, color=GREY_A),
                      label(r"$E \subset \R$ is connected \ $\iff$ \ $x, y \in E$ and $x < z < y$ imply $z \in E$.",
                            font_size=32)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.45)
        sub = label(r"The connected subsets of the line are exactly the intervals.", font_size=28, color=C.CONNECTED_SET)
        sub.next_to(stmt, DOWN, buff=0.2)
        X = lambda v: -5.6 + v * 3.6  # noqa: E731
        # three sets first: two intervals, and one with a gap
        ye1, ye2 = 0.6, -1.1
        exa = VGroup(bar(X(0), X(1), ye1, C.CONNECTED_SET), bar(X(2), X(2.5), ye1, C.CONNECTED_SET, lc=False),
                     Dot([X(0.5), ye2, 0], radius=0.075, color=C.PATHOLOGY), bar(X(1), X(1.5), ye2, C.PATHOLOGY))
        exa_l = VGroup(MathTex(r"[0, 1]", font_size=30, color=C.CONNECTED_SET).next_to([X(0.5), ye1, 0], UP, buff=0.2),
                       MathTex(r"(2, 2.5]", font_size=30, color=C.CONNECTED_SET).next_to([X(2.25), ye1, 0], UP, buff=0.2),
                       MathTex(r"\{0.5\} \cup [1, 1.5]", font_size=30, color=C.PATHOLOGY).next_to([X(1.0), ye2, 0], UP,
                                                                                                 buff=0.2))
        exa_v = VGroup(label(r"interval", font_size=24, color=C.CONNECTED_SET).next_to([X(0.5), ye1, 0], DOWN, buff=0.2),
                       label(r"interval", font_size=24, color=C.CONNECTED_SET).next_to([X(2.25), ye1, 0], DOWN, buff=0.2),
                       label(r"not an interval: $0.7$ is skipped", font_size=24, color=C.PATHOLOGY).next_to(
                           [X(1.0), ye2, 0], DOWN, buff=0.2))
        y0 = 0.2
        E = VGroup(bar(X(0), X(1), y0, C.SEQ), bar(X(2), X(3), y0, C.DELTA))
        zx = X(1.5)
        z = VGroup(DashedLine([zx, y0 - 0.7, 0], [zx, y0 + 0.7, 0], color=C.PATHOLOGY, stroke_width=3),
                   MathTex(r"z \notin E", font_size=30, color=C.PATHOLOGY).move_to([zx, y0 + 1.0, 0]))
        cut = VGroup(MathTex(r"E \cap (-\infty, z)", font_size=30, color=C.SEQ).move_to([X(0.5), y0 - 0.65, 0]),
                     MathTex(r"E \cap (z, \infty)", font_size=30, color=C.DELTA).move_to([X(2.5), y0 - 0.65, 0]))
        with self.voiceover(
            "On the real line, connected sets are exactly what you'd hope: <bookmark mark='s'/> the intervals, the sets "
            "with no gaps, where any number between two members is also a member. <bookmark mark='g'/> One direction is "
            "easy. If a set skips some z between two of its points, then the part below z and the part above z are "
            "nonempty and separated, since nothing in either piece is a limit of the other."
        ) as vo:
            self.play(FadeIn(stmt), FadeIn(sub), FadeIn(exa), FadeIn(exa_l))
            vo.wait_until("s")
            self.play(FadeIn(exa_v))
            vo.wait_until("g")
            self.play(FadeOut(VGroup(exa, exa_l, exa_v)))
            self.play(FadeIn(E))
            self.play(Create(z[0]), FadeIn(z[1]))
            self.play(FadeIn(cut), E[0].animate.shift(LEFT * 0.4), E[1].animate.shift(RIGHT * 0.4))
        self.wait(0.3)
        self.play(FadeOut(VGroup(E, z, cut)))

        # the other direction: the supremum finds the seam
        X2 = lambda v: -5.6 + v * 11.2  # noqa: E731
        y1 = -0.4
        line = bar(X2(0), X2(1), y1, GREY_C, sw=3)
        A_parts = [(0.0, 0.18), (0.31, 0.47)]
        B_parts = [(0.18, 0.31), (0.47, 1.0)]
        A = VGroup(*[Line([X2(a), y1, 0], [X2(b), y1, 0], color=C.SEQ, stroke_width=10) for a, b in A_parts])
        B = VGroup(*[Line([X2(a), y1, 0], [X2(b), y1, 0], color=C.DELTA, stroke_width=10) for a, b in B_parts])
        xl = MathTex(r"x \in A", font_size=30, color=C.SEQ).move_to([X2(0.05), y1 - 0.55, 0])
        yl = MathTex(r"y \in B", font_size=30, color=C.DELTA).move_to([X2(0.95), y1 - 0.55, 0])
        zs = X2(0.47)
        zm = VGroup(Line([zs, y1 - 0.45, 0], [zs, y1 + 0.45, 0], color=C.EPS, stroke_width=4),
                    MathTex(r"z = \sup(A \cap [x, y])", font_size=32, color=C.EPS).move_to([zs, y1 + 0.85, 0]))
        steps = VGroup(
            label(r"$z \in \overline{A}$ \ (2.28), \ so $z \notin B$", font_size=28),
            label(r"if $z \notin A$: \ $z \notin E$, a gap between $x$ and $y$", font_size=28),
            label(r"if $z \in A$: \ $z \notin \overline{B}$, so just right of $z$ lies a point in neither $A$ nor $B$",
                  font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The other direction is where the real numbers earn their keep. <bookmark mark='a'/> Suppose an interval were "
            "split into two nonempty separated pieces, A and B, with a point x of A to the left of a point y of B. "
            "<bookmark mark='z'/> Let z be the supremum of the part of A between x and y: the least-upper-bound property "
            "again, finding the seam. <bookmark mark='b'/> z is in the closure of A, so it can't be in B. "
            "<bookmark mark='c'/> If z isn't in A either, the interval has a gap at z. <bookmark mark='d'/> If z is in A, "
            "it's not in the closure of B, so some point just to the right of z is in neither piece: again a gap. Either "
            "way, the interval wasn't an interval."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(line), FadeIn(A), FadeIn(B), FadeIn(xl), FadeIn(yl))
            vo.wait_until("z")
            self.play(Create(zm[0]), FadeIn(zm[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rationals(self):
        win = Window(1.4, 0.5, y=-0.4)
        axis, labs = win.axis(), win.labels()
        dust = win.dust(height=1.3, split=below_sqrt2, color=C.CUT_LOW, color_hi=C.CUT_HIGH)
        hd = MathTex(r"\Q = \big(\Q \cap (-\infty, \sqrt2)\big) \;\cup\; \big(\Q \cap (\sqrt2, \infty)\big)", font_size=38)
        hd.to_edge(UP, buff=0.6)
        sep = label(r"two nonempty separated pieces: \ $\Q$ is not connected", font_size=30, color=C.PATHOLOGY)
        sep.next_to(hd, DOWN, buff=0.3)
        with self.voiceover(
            "Now look at the rationals with this definition. <bookmark mark='s'/> Split them at root two: the fractions "
            "below it and the fractions above it. Since root two isn't a fraction, every fraction lands on one side, "
            "<bookmark mark='p'/> and neither side contains a limit point of the other that's actually a fraction. "
            "So the two sides are separated, and the rationals are not connected. <bookmark mark='h'/> The hole from "
            "chapter one is literally a seam you can pull apart."
        ) as vo:
            self.play(Create(axis), FadeIn(labs), FadeIn(dust))
            vo.wait_until("s")
            self.play(Write(hd))
            vo.wait_until("p")
            self.play(FadeIn(sep))
            vo.wait_until("h")
            for m in (axis, labs, dust):
                m.clear_updaters()
            # split the line itself at root 2 and pull the halves apart sideways, each with its fractions
            xs2 = win.X(SQRT2)
            half_l = Line([win.L - 0.15, win.y, 0], [xs2, win.y, 0], color=GREY_C, stroke_width=2)
            half_r = Line([xs2, win.y, 0], [win.R + 0.15, win.y, 0], color=GREY_C, stroke_width=2)
            seam = endpoint([xs2, win.y, 0], False, C.HOLE, radius=0.1)
            self.remove(axis)
            self.add(half_l, half_r)
            self.play(FadeOut(labs), run_time=0.5)
            lo_g, hi_g = dust[0], dust[1]
            self.play(VGroup(lo_g, half_l).animate.shift(LEFT * 0.35), VGroup(hi_g, half_r).animate.shift(RIGHT * 0.35),
                      FadeIn(seam, scale=2), run_time=1.5)
        tot = label(r"In fact any subset of $\Q$ with two points splits this way: $\Q$ is \textbf{totally disconnected}.",
                    font_size=28, color=GREY_A).to_edge(DOWN, buff=0.5)
        nxt = label(r"Part 2: continuous images of connected sets are connected $\Rightarrow$ the intermediate value theorem",
                    font_size=26, color=C.EPS).next_to(tot, UP, buff=0.25)
        with self.voiceover(
            "In fact, there's an irrational number between any two fractions, so every set of fractions with at least "
            "two points splits like this. <bookmark mark='n'/> In Part 2 we'll see that continuous functions carry "
            "connected sets to connected sets, which is the real reason behind the intermediate value theorem."
        ) as vo:
            self.play(FadeIn(tot))
            vo.wait_until("n")
            self.play(FadeIn(nxt))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sine_curve(self):
        ax = Axes(x_range=[-0.1, 1.05, 0.5], y_range=[-1.3, 1.3, 1], x_length=7.8, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_C}).shift(LEFT * 2.6 + DOWN * 0.4)
        # sample sin(1/x) on (0, 1] with points spaced evenly in phase, so the oscillations near 0 are resolved
        u = np.linspace(1.0, 1 / 0.0012, 60000)
        x = 1 / u
        y = np.sin(u)
        assert abs(x.max() - 1.0) < 1e-12
        curve = polyline(ax, x[::-1], y[::-1], color=C.CONNECTED_SET, stroke_width=1.6)
        seg = Line(ax.c2p(0, -1), ax.c2p(0, 1), color=C.EPS, stroke_width=6)  # the segment {0} x [-1, 1]
        nums = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, -1.3), DOWN, buff=0.12)
                        for t, v in (("0", 0), ("0.5", 0.5), ("1", 1))],
                      *[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                        for t, v in (("-1", -1), ("1", 1))])
        lab = MathTex(r"\{(x, \sin\tfrac1x) : 0 < x \le 1\} \;\cup\; \{0\} \times [-1, 1]", font_size=32)
        lab.to_edge(UP, buff=0.45)
        txt = VGroup(label(r"connected: the segment is", font_size=26),
                     label(r"in the closure of the curve", font_size=26),
                     label(r"but no continuous path", font_size=26, color=C.PATHOLOGY),
                     label(r"reaches the segment from the curve", font_size=26, color=C.PATHOLOGY)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.3, 0.6, 0])
        card = museum_card(r"The topologist's sine curve", r"a standard example (not in Rudin; Munkres \S 24)",
                           r"``connected means path-connected''").scale(0.8).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Connectedness can be subtler than it looks. <bookmark mark='c'/> Here's the graph of sine of one over x, for "
            "x between zero and one, oscillating faster and faster as x approaches zero, <bookmark mark='s'/> together "
            "with the vertical segment it piles up against. <bookmark mark='t'/> The whole thing is connected: the "
            "segment lies in the closure of the curve, so they can't be separated. <bookmark mark='p'/> But you can't "
            "walk from the segment onto the curve along a continuous path: the curve wiggles infinitely often before "
            "reaching it. Connected, but not path-connected."
        ) as vo:
            self.play(Create(ax), FadeIn(nums), FadeIn(lab))
            vo.wait_until("c")
            self.play(Create(curve), run_time=3)
            vo.wait_until("s")
            self.play(Create(seg))
            self.bring_to_front(seg)
            vo.wait_until("t")
            self.play(FadeIn(txt[:2]))
            vo.wait_until("p")
            self.play(FadeIn(txt[2:]), FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.6)
        self.clear_scene()
