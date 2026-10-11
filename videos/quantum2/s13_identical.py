from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (corner_wheel, label, ladder, lframe, load, mtex, note, part_card, phase_img, plain_axes,
                                    polyline, tick_labels, why)


def config_square(psi, size=3.4, center=ORIGIN, labels=True, vmax=None):
    """A real two-particle wavefunction on the (x1, x2) plane: hue = sign (red +, cyan -), brightness = |psi|."""
    img = phase_img(psi[::-1].astype(complex), height=size, width=size, vmax=vmax, gamma=0.7).move_to(center)
    fr = Rectangle(width=size, height=size, stroke_color=GREY_C, stroke_width=1.5).move_to(center)
    diag = DashedLine(fr.get_corner(DL), fr.get_corner(UR), color=GREY_A, stroke_width=1.5, dash_length=0.08)
    g = Group(img, fr, diag)
    if labels:
        g.add(MathTex("x_1", font_size=24, color=C.XPOS).next_to(fr, DOWN, buff=0.08),
              MathTex("x_2", font_size=24, color=C.XPOS).next_to(fr, LEFT, buff=0.08))
    return g


class Identical(VoiceoverScene):
    def construct(self):
        self.card()
        self.exchange()
        self.three()
        self.pauli()
        self.hom()

    # ------------------------------------------------------------------
    def card(self):
        c = part_card(4, r"Many particles", r"identical particles, atoms and solids")
        with self.voiceover("Part 4: Many particles."):
            self.play(FadeIn(c))
        self.wait(0.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def exchange(self):
        d = load("identical")
        sq = config_square(d["dist"], size=3.8, center=LEFT * 3.6 + DOWN * 0.3)
        sw = config_square(d["dist"].T, size=3.8, center=LEFT * 3.6 + DOWN * 0.3)
        P = MathTex(r"(\hat P\psi)(x_1, x_2)", r"=", r"\psi(x_2, x_1)", font_size=36).to_edge(UP, buff=0.5).shift(RIGHT * 2.8)
        refl = label(r"swapping = reflecting across the diagonal", font_size=26, color=GREY_A).next_to(P, DOWN, buff=0.25)
        r1 = MathTex(r"\text{identical}", r"\;\Rightarrow\;", r"\hat P \text{ is a symmetry}", font_size=32)
        r2 = MathTex(r"\hat P^2 = 1", r"\;\Rightarrow\;", r"\hat P\psi = \pm\psi", font_size=36)
        r3 = VGroup(MathTex(r"+1:\ \text{bosons (photons, } {}^4\text{He)}", font_size=30, color=C.BOSON),
                    MathTex(r"-1:\ \text{fermions (electrons, quarks)}", font_size=30, color=C.FERMION)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        ss = label(r"spin--statistics: integer spin $\leftrightarrow$ boson, half-integer $\leftrightarrow$ fermion\\(Fierz 1939, Pauli 1940; the proof needs relativity)",
                   font_size=22, color=GREY_B)
        col = VGroup(r1, r2, r3, ss).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(refl, DOWN, buff=0.45).shift(LEFT * 0.4)
        any_ = note(r"in two dimensions, exchanges can wind around each other: anyons (Leinaas \& Myrheim 1977, Wilczek 1982)").to_edge(DOWN, buff=0.2)
        cap = label(r"one wavefunction, two positions", font_size=24, color=GREY_B).next_to(sq, UP, buff=0.2)
        wheel = corner_wheel(corner=UL, buff=0.2, radius=0.25)
        with self.voiceover(
            "Two particles share one wavefunction on the plane of their positions, x one and x two, as in Part 1. "
            "<bookmark mark='a'/> If the particles are identical, two electrons say, swapping them can't change any "
            "prediction. <bookmark mark='b'/> And swapping is reflecting the picture across the diagonal. "
            "<bookmark mark='c'/> So the swap, P, is a symmetry, and since swapping twice does nothing, P squared is "
            "one: its only possible eigenvalues are plus one and minus one."
        ) as vo:
            self.play(FadeIn(sq), FadeIn(cap), FadeIn(wheel))
            vo.wait_until("a")
            self.play(Write(P))
            vo.wait_until("b")
            self.play(FadeIn(refl), FadeTransform(sq[0], sw[0]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(r1))
            self.play(Write(r2))
        with self.voiceover(
            "Every kind of particle picks one: <bookmark mark='a'/> symmetric wavefunctions for bosons, like photons, "
            "antisymmetric ones for fermions, like electrons. <bookmark mark='b'/> Which particles are which is the "
            "spin-statistics theorem: integer spin means boson, half-integer means fermion; its proof needs relativity. "
            "<bookmark mark='c'/> In a flat, two-dimensional world there's a third option, called anyons."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(r3))
            vo.wait_until("b")
            self.play(FadeIn(ss))
            vo.wait_until("c")
            self.play(FadeIn(any_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("identical")
        vmax = max(np.abs(d[k]).max() for k in ("dist", "bos", "fer"))
        sqs = Group(*[config_square(d[k], size=3.5, vmax=vmax) for k in ("dist", "bos", "fer")]).arrange(RIGHT, buff=0.75).move_to(UP * 0.2)
        names = [(r"distinguishable", WHITE), (r"bosons: $\psi_S$", C.BOSON), (r"fermions: $\psi_A$", C.FERMION)]
        tl = VGroup(*[label(n, font_size=28, color=c).next_to(s, UP, buff=0.2) for (n, c), s in zip(names, sqs)])
        forms = VGroup(MathTex(r"\phi_1(x_1)\phi_2(x_2)", font_size=26),
                       MathTex(r"\tfrac{1}{\sqrt2}\big(\phi_1\phi_2 + \phi_2\phi_1\big)", font_size=26, color=C.BOSON),
                       MathTex(r"\tfrac{1}{\sqrt2}\big(\phi_1\phi_2 - \phi_2\phi_1\big)", font_size=26, color=C.FERMION))
        for f, s in zip(forms, sqs):
            f.next_to(s, DOWN, buff=0.45)
        pn = [float(d[f"near_{k}"]) for k in ("dist", "bos", "fer")]
        assert abs(pn[0] - 0.200) < 0.002 and abs(pn[1] - 0.385) < 0.002 and pn[2] < 0.02
        nums = VGroup(*[MathTex(r"P(|x_1 - x_2| < 0.1L) = " + f"{100 * v:.0f}" + r"\%", font_size=24, color=c).next_to(f, DOWN, buff=0.15)
                        for v, f, c in zip(pn, forms, (WHITE, C.BOSON, C.FERMION))])
        nums[2].become(MathTex(r"P(|x_1 - x_2| < 0.1L) = 1.6\%", font_size=24, color=C.FERMION).next_to(forms[2], DOWN, buff=0.15))
        fr2 = sqs[2][1]
        node = VGroup(Line(fr2.get_corner(DL), fr2.get_corner(UR), color=C.FERMION, stroke_width=4),
                      MathTex(r"\psi_A = 0", font_size=24, color=C.FERMION).next_to(fr2.get_corner(UR), UR, buff=0.05))
        nf = label(r"no force: the same Hamiltonian in all three; a correlation from symmetry alone", font_size=26, color=GREY_A).to_edge(DOWN, buff=0.25)
        tag = note(r"two particles in a box, in the lowest two states; color = sign of $\psi$ (red $+$, cyan $-$), brightness = $|\psi|$").to_edge(UP, buff=0.15)
        with self.voiceover(
            "Here's what that does. Two particles in a box, one in the lowest state and one in the second. "
            "<bookmark mark='a'/> If they were distinguishable, the wavefunction would be this. <bookmark mark='b'/> "
            "Symmetrize it, and it piles up along the diagonal: bosons are found close together more often. "
            "<bookmark mark='c'/> Antisymmetrize it, and it vanishes along the entire diagonal: two identical fermions "
            "are never found at the same place."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sqs[0]), FadeIn(tl[0]), FadeIn(forms[0]))
            vo.wait_until("b")
            self.play(FadeIn(sqs[1]), FadeIn(tl[1]), FadeIn(forms[1]))
            vo.wait_until("c")
            self.play(FadeIn(sqs[2]), FadeIn(tl[2]), FadeIn(forms[2]))
            self.play(FadeIn(node))
        with self.voiceover(
            "The chance of finding the two within a tenth of the box of each other: <bookmark mark='a'/> twenty percent "
            "if they're distinguishable, thirty-eight for bosons, under two for fermions. <bookmark mark='b'/> There's no "
            "force here. The Hamiltonian is the same in all three cases; this is a correlation produced by symmetry "
            "alone."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(nf))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pauli(self):
        d = load("identical")
        x = d["x"]
        same = MathTex(r"\phi_a(x_1)\phi_a(x_2) - \phi_a(x_2)\phi_a(x_1)", r"=", r"0", font_size=36).to_edge(UP, buff=0.4)
        same[2].set_color(C.FERMION)
        pl = label(r"the exclusion principle: no two fermions in the same state (Pauli, 1925)", font_size=26, color=C.FERMION).next_to(same, DOWN, buff=0.2)
        slater = MathTex(r"\psi(x_1, \dots, x_N)", r"=", r"\frac{1}{\sqrt{N!}}\begin{vmatrix} \phi_1(x_1) & \cdots & \phi_1(x_N) \\ \vdots & & \vdots \\ \phi_N(x_1) & \cdots & \phi_N(x_N)\end{vmatrix}",
                         font_size=32).next_to(pl, DOWN, buff=0.35).shift(LEFT * 3.1)
        sl = label(r"two equal rows (or columns) $\Rightarrow$ zero", font_size=22, color=GREY_B).next_to(slater, DOWN, buff=0.15)
        ax = plain_axes((0, 1), (0, 4.2), 5.6, 3.0).move_to(RIGHT * 3.3 + DOWN * 1.2)
        dens = polyline(ax, x, d["dens3"], color=C.BORN, stroke_width=3.5)
        pair = polyline(ax, x, d["pair3"] / d["dens3"][np.argmin(np.abs(x - 0.3))], color=C.FERMION, stroke_width=3.5)
        held = Dot(ax.c2p(0.3, 0), radius=0.09, color=WHITE)
        hl = label(r"held here", font_size=20, color=WHITE).next_to(held, DOWN, buff=0.1)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.35, color=C.BORN, stroke_width=4), label(r"density of 3 fermions", font_size=22)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.35, color=C.FERMION, stroke_width=4), label(r"the other two, given one at $0.3L$", font_size=22, color=C.FERMION)).arrange(RIGHT, buff=0.1)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax, UP, buff=0.15)
        hole = label(r"the exchange hole", font_size=24, color=C.FERMION).next_to(ax.c2p(0.3, 0.2), DOWN, buff=0.45).shift(RIGHT * 1.2)
        with self.voiceover(
            "<bookmark mark='a'/> Put two fermions in the same state, and the antisymmetric combination is zero: there's "
            "no such state. That's Pauli's exclusion principle, from 1925. <bookmark mark='b'/> For N fermions, the "
            "antisymmetric state is a determinant of their single-particle wavefunctions, and a determinant with two "
            "equal rows vanishes. <bookmark mark='c'/> Hold one fermion still, and the others are kept away from it: a "
            "hole travels with every electron."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(same), FadeIn(pl))
            vo.wait_until("b")
            self.play(Write(slater), FadeIn(sl))
            vo.wait_until("c")
            self.play(Create(ax), Create(dens), FadeIn(leg[0]))
            self.play(Create(pair), FadeIn(held), FadeIn(hl), FadeIn(leg[1]), FadeIn(hole))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hom(self):
        d = load("identical")
        # the beam splitter: inputs from the left (a) and from below (b); outputs right (c) and up (d)
        def splitter(center, scale=1.0):
            g = VGroup()
            bs = Line(center + (LEFT + DOWN) * 0.45 * scale, center + (RIGHT + UP) * 0.45 * scale, color=GREY_A, stroke_width=5)
            g.add(Square(side_length=0.9 * scale, stroke_color=GREY_C, stroke_width=1.5).move_to(center), bs)
            return g

        big = VGroup(splitter(LEFT * 4.2 + UP * 0.6, 1.4))
        c0 = LEFT * 4.2 + UP * 0.6
        ina = Arrow(c0 + LEFT * 2.2, c0 + LEFT * 0.7, buff=0, color=C.BOSON, stroke_width=5)
        inb = Arrow(c0 + DOWN * 2.2, c0 + DOWN * 0.7, buff=0, color=C.BOSON, stroke_width=5)
        out_c = DashedLine(c0 + RIGHT * 0.7, c0 + RIGHT * 2.0, color=GREY_B)
        out_d = DashedLine(c0 + UP * 0.7, c0 + UP * 2.0, color=GREY_B)
        lab = VGroup(label(r"photon 1", font_size=22, color=C.BOSON).next_to(ina, UP, buff=0.08),
                     label(r"photon 2", font_size=22, color=C.BOSON).next_to(inb, RIGHT, buff=0.08),
                     label(r"detector C", font_size=20, color=GREY_B).next_to(out_c, RIGHT, buff=0.08),
                     label(r"detector D", font_size=20, color=GREY_B).next_to(out_d, UP, buff=0.08))
        amps = MathTex(r"t = \tfrac{1}{\sqrt2}", r",\qquad", r"r = \tfrac{i}{\sqrt2}", font_size=32).next_to(big, DOWN, buff=1.7)
        # the two ways to get one photon in each detector
        o1, o2 = RIGHT * 1.2 + UP * 1.7, RIGHT * 4.6 + UP * 1.7

        def mini(center, kind):
            g = VGroup(splitter(center, 0.8))
            if kind == "tt":
                g.add(Arrow(center + LEFT * 1.1, center + RIGHT * 1.1, buff=0, color=C.BOSON, stroke_width=3, tip_length=0.15),
                      Arrow(center + DOWN * 1.1, center + UP * 1.1, buff=0, color=C.BOSON, stroke_width=3, tip_length=0.15))
            else:
                g.add(VMobject(stroke_color=C.BOSON, stroke_width=3).set_points_as_corners([center + LEFT * 1.1, center, center + UP * 1.0]),
                      VMobject(stroke_color=C.BOSON, stroke_width=3).set_points_as_corners([center + DOWN * 1.1, center, center + RIGHT * 1.0]))
            return g

        m1, m2 = mini(o1, "tt"), mini(o2, "rr")
        a1 = MathTex(r"t\cdot t = \tfrac12", font_size=30).next_to(m1, DOWN, buff=0.25)
        a2 = MathTex(r"r\cdot r = -\tfrac12", font_size=30).next_to(m2, DOWN, buff=0.25)
        n1 = label(r"both transmitted", font_size=22, color=GREY_B).next_to(m1, UP, buff=0.1)
        n2 = label(r"both reflected", font_size=22, color=GREY_B).next_to(m2, UP, buff=0.1)
        tot = MathTex(r"\tfrac12 - \tfrac12 = 0", r":\ \text{they always leave together}", font_size=32).move_to(RIGHT * 2.9 + DOWN * 0.9)
        tot[0].set_color(C.BOSON)
        op = MathTex(r"\hat a^\dagger\hat b^\dagger \to \tfrac{i}{2}\big(\hat c^{\dagger 2} + \hat d^{\dagger 2}\big)", font_size=30).next_to(tot, DOWN, buff=0.3)
        with self.voiceover(
            "Bosons do the opposite, and the most striking demonstration uses light. <bookmark mark='a'/> Send two "
            "identical photons into a half-silvered mirror, one from each side. <bookmark mark='b'/> Each photon is "
            "either transmitted, with amplitude one over root two, or reflected, with amplitude i over root two. "
            "<bookmark mark='c'/> For the photons to leave by different ports, both must be transmitted, "
            "<bookmark mark='d'/> or both reflected. <bookmark mark='e'/> Those two amplitudes are one half and minus "
            "one half: they cancel exactly. The photons always leave together."
        ) as vo:
            self.play(FadeIn(big))
            vo.wait_until("a")
            self.play(GrowArrow(ina), GrowArrow(inb), Create(out_c), Create(out_d), FadeIn(lab))
            vo.wait_until("b")
            self.play(Write(amps))
            vo.wait_until("c")
            self.play(FadeIn(m1), FadeIn(n1), Write(a1))
            vo.wait_until("d")
            self.play(FadeIn(m2), FadeIn(n2), Write(a2))
            vo.wait_until("e")
            self.play(Write(tot), FadeIn(op))
        self.wait(0.3)
        self.clear_scene()
        tau, pc, counts, N = d["hom_tau"], d["hom_p"], d["hom_counts"], int(d["hom_n"])
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1150, 250], x_length=9.0, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(DOWN * 0.4)
        fr = lframe(ax)
        tks = VGroup(tick_labels(ax, xs=(-3, -2, -1, 0, 1, 2, 3)), tick_labels(ax, ys=(0, 500, 1000)))
        xl = MathTex(r"\text{delay } \tau \ (\text{in units of the photon's coherence time})", font_size=26).next_to(fr[0], DOWN, buff=0.5)
        yl = label(r"coincidences (of 2{,}000 pairs)", font_size=24).next_to(fr[1].get_end(), UP, buff=0.1)
        th = polyline(ax, np.linspace(-3, 3, 300), N * 0.5 * (1 - np.exp(-np.linspace(-3, 3, 300) ** 2)), color=C.BOSON, stroke_width=3)
        pts = VGroup(*[Dot(ax.c2p(t, c), radius=0.06, color=WHITE) for t, c in zip(tau, counts)])
        assert counts[len(counts) // 2] < 25
        half = DashedLine(ax.c2p(-3, N / 2), ax.c2p(3, N / 2), color=GREY_C)
        hl = label(r"independent: half the time", font_size=22, color=GREY_B).next_to(ax.c2p(1.6, N / 2), UP, buff=0.08)
        dip = label(r"identical and simultaneous:\\ never", font_size=24, color=C.BOSON).next_to(ax.c2p(0.55, 120), RIGHT, buff=0.1)
        src = note(r"simulated counts (seeded) on the ideal curve $P = \tfrac12(1 - e^{-\tau^2})$; measured by Hong, Ou \& Mandel (1987)").to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> Delay one photon so they no longer overlap, and they act independently, splitting up "
            "half the time. <bookmark mark='b'/> As the delay goes to zero, coincidences vanish. This dip was measured by "
            "Hong, Ou and Mandel in 1987, and it's now a standard test of whether two photons are truly identical."
        ) as vo:
            self.play(Create(fr), FadeIn(tks), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(half), FadeIn(hl), LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.03))
            vo.wait_until("b")
            self.play(Create(th), FadeIn(dip))
        self.wait(0.4)
        self.clear_scene()
