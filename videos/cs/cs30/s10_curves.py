from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


def f(x):
    return x ** 3 - x + 1


class Curves(VoiceoverScene):
    def construct(self):
        self.card()
        self.chord()
        self.tangent()
        self.finite()
        self.why()

    def card(self):
        card = chapter_card(9, r"Elliptic curves", r"Can a curve be a group?", lit=(1985, 2006),
                            extra=((1985, r"Miller; \ Koblitz"), (2006, r"Curve25519")), part=PART)
        with self.voiceover("Chapter nine. Elliptic curves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def axes(self):
        ax = Axes(x_range=[-2, 4, 1], y_range=[-6, 6, 2], x_length=5.6, y_length=5.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        x0 = -1.3247179572
        xs = [x0 + (3.6 - x0) * (i / 400) ** 2 for i in range(401)]
        up = [ax.c2p(x, math.sqrt(max(f(x), 0))) for x in xs if math.sqrt(max(f(x), 0)) <= 6.2]
        dn = [ax.c2p(x, -math.sqrt(max(f(x), 0))) for x in xs if math.sqrt(max(f(x), 0)) <= 6.2]
        curve = VMobject(color=DATA, stroke_width=3).set_points_smoothly(dn[::-1] + up)
        return ax, curve

    def chord(self):
        head = label(r"$y^2 = x^3 - x + 1$: \ adding points", font_size=34).to_edge(UP, buff=0.3)
        ax, curve = self.axes()
        P, Q, R, S = (-1, 1), (0, 1), (1, 1), (1, -1)
        dP = Dot(ax.c2p(*P), color=HEAD)
        dQ = Dot(ax.c2p(*Q), color=HEAD)
        dR = Dot(ax.c2p(*R), color=GREY_B)
        dS = Dot(ax.c2p(*S), color=YES, radius=0.1)
        lP = label(r"$P$", font_size=24, color=HEAD).next_to(dP, UL, buff=0.08)
        lQ = label(r"$Q$", font_size=24, color=HEAD).next_to(dQ, UP, buff=0.12)
        lR = label(r"$R$", font_size=24, color=GREY_B).next_to(dR, UR, buff=0.08)
        lS = label(r"$P + Q$", font_size=24, color=YES).next_to(dS, RIGHT, buff=0.12)
        line = Line(ax.c2p(-2, 1), ax.c2p(3.2, 1), color=GREY_B, stroke_width=2)
        refl = DashedLine(ax.c2p(1, 1), ax.c2p(1, -1), color=YES, stroke_width=2)
        notes = VGroup(
            label(r"the line through $P$ and $Q$ \\ meets the curve once more, \ at $R$", font_size=22, color=WHITE),
            label(r"reflect in the $x$-axis: \\ that point is $P + Q$", font_size=22, color=YES),
            label(r"$(-1, 1) + (0, 1) = (1, -1)$", font_size=24, color=YES),
            label(r"the rules form a \textbf{group}: \\ identity $\mathcal{O}$, \ the point at infinity \\ (vertical "
                  r"lines), \ inverse $-(x, y) = (x, -y)$", font_size=22, color=HEAD),
            label(r"associativity is true, \\ and surprisingly hard to prove", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "An elliptic curve is the set of points where y squared equals a cubic in x. Here is y squared equals x "
            "cubed minus x plus one. The remarkable fact is that its points can be added. <bookmark mark='a'/> Take "
            "two points, P and Q. The line through them meets the curve in exactly one more point, R: a cubic has "
            "three roots, and we know two. <bookmark mark='b'/> Reflect R in the x-axis. That point is defined to be P "
            "plus Q. <bookmark mark='c'/> With these whole-number points, minus one, one plus zero, one is one, minus "
            "one. <bookmark mark='d'/> With one extra point at infinity as zero, where vertical lines meet, and "
            "reflection as negation, the points form a group. <bookmark mark='e'/> Associativity, that adding P and Q "
            "first then R gives the same as Q and R first, is true and takes real work to prove. It is the curve's "
            "deepest property, and we will simply check it numerically."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(curve), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(dP), FadeIn(lP), FadeIn(dQ), FadeIn(lQ))
            self.play(Create(line), FadeIn(dR), FadeIn(lR), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(refl), FadeIn(dS), FadeIn(lS), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def tangent(self):
        head = label(r"Doubling: \ the tangent", font_size=34).to_edge(UP, buff=0.3)
        ax, curve = self.axes()
        P = (-1, 1)
        dP = Dot(ax.c2p(*P), color=HEAD)
        lP = label(r"$P$", font_size=24, color=HEAD).next_to(dP, UL, buff=0.08)
        tan = Line(ax.c2p(-2, 0), ax.c2p(3.6, 5.6), color=GREY_B, stroke_width=2)
        dR = Dot(ax.c2p(3, 5), color=GREY_B)
        dS = Dot(ax.c2p(3, -5), color=YES, radius=0.1)
        lS = label(r"$2P$", font_size=24, color=YES).next_to(dS, LEFT, buff=0.12)
        refl = DashedLine(ax.c2p(3, 5), ax.c2p(3, -5), color=YES, stroke_width=2)
        notes = VGroup(
            label(r"$P + P$: \ use the tangent at $P$", font_size=22, color=WHITE),
            label(r"slope $\lambda = \dfrac{3x^2 + a}{2y} = 1$ \ at $(-1, 1)$", font_size=22, color=GREY_A),
            label(r"it meets the curve at $(3, 5)$; \ reflect: \ $2P = (3, -5)$", font_size=22, color=YES),
            label(r"in coordinates: \\ $x_3 = \lambda^2 - x_1 - x_2$, \\ $y_3 = \lambda(x_1 - x_3) - y_1$", font_size=22,
                  color=HEAD),
            label(r"only $+$, \ $-$, \ $\times$, \ $\div$: \ so the same \\ formulas work in any \textbf{field}",
                  font_size=22, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Adding a point to itself uses the tangent line. <bookmark mark='a'/> At P, minus one, one, the slope of "
            "the curve is one. <bookmark mark='b'/> The tangent meets the curve again at three, five. Reflect, and "
            "two P is three, minus five. <bookmark mark='c'/> In coordinates, the slope, the new x and the new y come "
            "from a few lines of algebra. <bookmark mark='d'/> They use only addition, subtraction, multiplication and "
            "division. So the same formulas make sense over any field, including the integers modulo a prime, where "
            "the curve stops being a curve and becomes a scatter of points."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(curve), FadeIn(dP), FadeIn(lP), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(tan), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(dR), Create(refl), FadeIn(dS), FadeIn(lS), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def finite(self):
        c = load("curves")
        p = c["p"]
        head = label(rf"$y^2 = x^3 + 2x + 3$ \ over $\mathrm{{GF}}({p})$", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, p, 16], y_range=[0, p, 16], x_length=5.4, y_length=5.4,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=GREY_B) for x, y in c["points"]])
        mult = [m for m in c["multiples"] if m]
        path = VGroup(*[Line(ax.c2p(*a), ax.c2p(*b), stroke_width=1.2, color=HEAD, stroke_opacity=0.6)
                        for a, b in zip(mult[:16], mult[1:17])])
        hl = VGroup(*[Dot(ax.c2p(*m), radius=0.06, color=HEAD) for m in mult[:17]])
        G = Dot(ax.c2p(*c["G"]), radius=0.09, color=YES)
        notes = VGroup(
            label(rf"{len(c['points'])} points, \ plus $\mathcal{{O}}$: \ a group of {c['N']}", font_size=22,
                  color=WHITE),
            label(r"symmetric about $y = p/2$: \ the reflection $y \to -y$", font_size=20, color=GREY_A),
            label(rf"$G = ({c['G'][0]}, {c['G'][1]})$: \ $G, 2G, 3G, \ldots$ jump around: \ order {c['order']}",
                  font_size=22, color=HEAD),
            label(r"the elliptic-curve discrete log: \\ given $Q = kG$, \ find $k$", font_size=22, color=NO),
            label(rf"computing $kG$: \ double-and-add, \\ like chapter 2: \ P-256 in {c['p256_ms']:.0f} ms \\ in "
                  r"Python", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "Over the integers modulo ninety-seven, the curve y squared equals x cubed plus two x plus three becomes "
            "this. <bookmark mark='a'/> Ninety-nine points, and the point at infinity: a group of a hundred. <bookmark "
            "mark='b'/> The symmetry about the middle is the reflection, y to minus y. <bookmark mark='c'/> Take a "
            "point G and keep adding it: G, two G, three G. The multiples jump around the grid with no visible order, "
            "fifty of them before they return to zero. <bookmark mark='d'/> Given a multiple Q equals k times G, "
            "finding k is the elliptic-curve discrete logarithm. <bookmark mark='e'/> Computing k times G is easy: "
            "double and add, chapter two's square and multiply in new clothes. On the standard curve P-256, with "
            "two-hundred-and-fifty-six-bit numbers, it takes twenty milliseconds in Python."
        ) as vo:
            self.play(FadeIn(head), Create(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.01), FadeIn(notes[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(G), FadeIn(notes[2]))
            self.play(LaggedStart(*[AnimationGroup(Create(l_), FadeIn(d_)) for l_, d_ in zip(path, hl[1:])],
                                  lag_ratio=0.4), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    def why(self):
        c = load("curves")
        head = label(r"Why curves won", font_size=34).to_edge(UP, buff=0.3)
        rows = [(r"128-bit security", "3072-bit RSA", "256-bit curve"),
                (r"192-bit security", "7680-bit RSA", "384-bit curve"),
                (r"256-bit security", "15360-bit RSA", "521-bit curve")]
        tab = VGroup()
        for a, b, cc in rows:
            tab.add(VGroup(label(a, font_size=22, color=GREY_A), label(b, font_size=22, color=NO),
                           label(cc, font_size=22, color=YES)))
        for r in tab:
            r[1].next_to(r[0], RIGHT, buff=0.8)
            r[2].next_to(r[1], RIGHT, buff=0.8)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.6)
        for r in tab:
            r[1].set_x(0.2)
            r[2].set_x(3.6)
        lines = VGroup(
            label(r"for good curves, \ no index calculus: \ points don't factor; \ the best attack is rho, \ "
                  r"$\sqrt{n}$", font_size=21, color=WHITE),
            label(r"Miller and Koblitz \ (1985) \ proposed them; \ NIST's P-256 \ (2000); \ Bernstein's Curve25519 \ "
                  r"(2006)", font_size=21, color=HEAD),
            label(r"X25519: \ a Montgomery ladder, \ the same steps whatever the key: \ constant time by design",
                  font_size=21, color=DATA),
            label(rf"ours matches RFC 7748: \ \texttt{{{c['x25519_vector'][:16]}}}$\ldots$; \ and two parties agree: \ "
                  rf"{'yes' if c['x25519_equal'] else 'no'}", font_size=21, color=YES),
            label(r"almost every TLS connection today begins with X25519", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why use curves at all? <bookmark mark='a'/> Because their keys are small. For the same security, RSA "
            "needs a three-thousand-bit modulus where a curve needs two hundred and fifty-six bits; at higher levels "
            "the gap widens. <bookmark mark='b'/> The reason is the last chapter's index calculus: points on a good "
            "curve cannot be broken into small factors, so the only known attack is a generic square root. <bookmark "
            "mark='c'/> Victor Miller and Neal Koblitz proposed curve cryptography independently in 1985. NIST "
            "standardised P-256, and in 2006 Daniel Bernstein designed Curve25519 to be fast and hard to implement "
            "wrongly. <bookmark mark='d'/> Its X25519 function uses a Montgomery ladder, which performs the same "
            "operations whatever the key bits are. <bookmark mark='e'/> Ours matches the RFC's test vector, and two "
            "parties agree on a secret. <bookmark mark='f'/> Almost every TLS connection today begins with exactly "
            "this computation."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.3))
            for mk, ln in zip("bcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
