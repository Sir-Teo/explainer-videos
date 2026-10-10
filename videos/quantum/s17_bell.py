from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum import colormap as qcm
from videos.quantum.common import (boxed, corner_wheel, image_on, label, load, mtex, note, num, place_whys, polyline,
                                   stack, why)
from videos.quantum.compute import CHSH_ANGLES


class Bell(VoiceoverScene):
    def construct(self):
        self.configuration_space()
        self.singlet()
        self.hidden_variables()
        self.chsh()
        self.simulate()
        self.experiments()

    # ------------------------------------------------------------------
    def configuration_space(self):
        pr = load("pair")
        u, prod, ent = pr["u"], pr["prod"], pr["ent"]
        sd_p, sd_e = pr["prod_sd"], pr["ent_sd"]
        axL = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1], x_length=4.6, y_length=4.6, tips=False,
                   axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 3.4 + DOWN * 0.35)
        axR = axL.copy().move_to(RIGHT * 2.0 + DOWN * 0.35)
        imL = image_on(axL, qcm.rgba(qcm.phase_rgb(prod[::-1], gamma=0.7)), (-5, 5), (-5, 5))
        imR = image_on(axR, qcm.rgba(qcm.phase_rgb(ent[::-1], gamma=0.7)), (-5, 5), (-5, 5))
        labs = VGroup(*[VGroup(MathTex(r"x_1", font_size=28, color=C.ALICE).next_to(a.x_axis.get_end(), RIGHT, buff=0.08),
                               MathTex(r"x_2", font_size=28, color=C.BOB).next_to(a.y_axis.get_end(), UP, buff=0.08))
                        for a in (axL, axR)])
        tL = MathTex(r"\psi(x_1, x_2) = f(x_1)\,g(x_2)", font_size=30).next_to(axL, UP, buff=0.35)
        tR = MathTex(r"\psi(x_1, x_2) \ne f(x_1)\,g(x_2)", font_size=30).next_to(axR, UP, buff=0.35)
        nL = label(r"product state:\\independent", font_size=26, color=GREY_A).next_to(axL, DOWN, buff=0.2)
        nR = label(r"entangled:\\where 1 is says where 2 is", font_size=26, color=GREY_A).next_to(axR, DOWN, buff=0.2)
        cut = DashedLine(axR.c2p(1.5, -5), axR.c2p(1.5, 5), color=C.ALICE, stroke_width=2.5)
        cl = MathTex(r"x_1 = 1.5", font_size=24, color=C.ALICE).next_to(axR.c2p(1.5, -4.4), RIGHT, buff=0.1)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.26)
        # the opening: not two wavefunctions, one -- on the plane of pairs
        q0 = MathTex(r"\psi_1(x_1)", r"\ \text{and}\ ", r"\psi_2(x_2)\ ?", font_size=44).move_to(UP * 0.4)
        q0[0].set_color(C.ALICE)
        q0[2].set_color(C.BOB)
        no = Cross(q0, stroke_color=C.WIGNER_NEG, stroke_width=5).scale(1.05)
        one = MathTex(r"\psi(x_1, x_2)", font_size=40)
        one_n = label(r"one complex number for every pair of positions", font_size=28, color=GREY_A)
        hd = VGroup(one, one_n).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.3)
        side = VGroup(
            MathTex(r"\sigma(x_2) = " + num(float(sd_e[0]), 2), font_size=26, color=C.BOB),
            MathTex(r"\sigma(x_2 \mid x_1) = " + num(float(sd_e[1]), 2), font_size=26, color=C.BOB),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(axR, RIGHT, buff=0.55).shift(UP * 0.9)
        assert side.get_right()[0] < 7.0
        assert abs(sd_e[0] - 1.14) < 0.01 and abs(sd_e[1] - 0.28) < 0.01
        with self.voiceover(
            "With two particles, quantum mechanics gets truly strange. The key point first: two particles don't have "
            "two wavefunctions. <bookmark mark='o'/> They share one, a single complex number for every pair of positions, "
            "<bookmark mark='x'/> x one and x two. "
            "<bookmark mark='p'/> If it factors into a function of x one times a function of x two, the particles are "
            "independent. <bookmark mark='e'/> But most two-particle states don't factor. In this one, the probability "
            "lies along the diagonal: <bookmark mark='c'/> find particle one at 1.5, and particle two is pinned near 1.5 "
            "too, though on its own it could have been almost anywhere. That's entanglement."
        ) as vo:
            self.play(FadeIn(wheel), Write(q0))
            vo.wait_until("o")
            self.play(Create(no))
            self.play(FadeOut(VGroup(q0, no)), Write(one), FadeIn(one_n))
            vo.wait_until("x")
            self.play(Create(axL), Create(axR), FadeIn(labs))
            vo.wait_until("p")
            self.play(FadeIn(imL), Write(tL), FadeIn(nL))
            vo.wait_until("e")
            self.play(FadeIn(imR), Write(tR), FadeIn(nR))
            vo.wait_until("c")
            self.play(Create(cut), FadeIn(cl), FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def singlet(self):
        s1 = MathTex(r"\ket{\Psi^-}", r"=", r"\frac{1}{\sqrt2}\Big(\ket{\uparrow}_A\ket{\downarrow}_B - \ket{\downarrow}_A\ket{\uparrow}_B\Big)",
                     font_size=42).to_edge(UP, buff=0.45)
        sn = label(r"two spins in a total-spin-zero state: the same form along every axis", font_size=26, color=GREY_A).next_to(s1, DOWN, buff=0.15)
        d1 = MathTex(r"P(\text{same})", r"=", r"\sin^2\frac{\theta}{2}", r",\qquad", r"P(\text{opposite})", r"=", r"\cos^2\frac{\theta}{2}",
                     font_size=38)
        d2 = MathTex(r"E(\mathbf a, \mathbf b)", r"=", r"P(\text{same}) - P(\text{opposite})", r"=", r"-\cos\theta", font_size=40)
        col = VGroup(d1, d2).arrange(DOWN, buff=0.45).next_to(sn, DOWN, buff=0.6)
        d2[4].set_color(C.QUANTUM_BOUND)
        en = label(r"$\theta$: angle between Alice's axis $\mathbf a$ and Bob's axis $\mathbf b$; outcomes $\pm 1$", font_size=26,
                   color=GREY_A).next_to(col, DOWN, buff=0.35)
        al = label(r"each side alone: always 50/50", font_size=28, color=C.ALICE).next_to(en, DOWN, buff=0.5)
        with self.voiceover(
            "The cleanest example uses spin. Two spin-half particles can be prepared in the singlet state, with total "
            "spin zero: up-down minus down-up. They fly apart, to Alice and to Bob, who each measure spin along an axis "
            "of their choosing. <bookmark mark='p'/> Work out the Born rule: if their axes differ by an angle theta, "
            "they get the same answer with probability sine squared of theta over two, and opposite answers with "
            "cosine squared. <bookmark mark='e'/> Score plus one for same and minus one for opposite. The average score, "
            "the correlation, is minus cosine theta. <bookmark mark='m'/> Yet each side, looked at alone, is a perfect "
            "coin flip."
        ) as vo:
            self.play(Write(s1), FadeIn(sn))
            vo.wait_until("p")
            self.play(Write(d1))
            vo.wait_until("e")
            self.play(Write(d2), FadeIn(en))
            vo.wait_until("m")
            self.play(FadeIn(al))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hidden_variables(self):
        epr = label(r"Einstein, Podolsky \& Rosen (1935): maybe the answers were decided at the source", font_size=30)
        epr.to_edge(UP, buff=0.5)
        h1 = MathTex(r"A(\mathbf a, \lambda)", r",\ ", r"B(\mathbf b, \lambda)", r"\;\in\; \{+1, -1\}", font_size=40)
        h1[0].set_color(C.ALICE)
        h1[2].set_color(C.BOB)
        h1.next_to(epr, DOWN, buff=0.5)
        hn = label(r"$\lambda$: hidden instructions carried by each pair; Alice's answer can't depend on Bob's setting",
                   font_size=26, color=GREY_A).next_to(h1, DOWN, buff=0.2)
        b1 = MathTex(r"A\,(B - B')", r"+", r"A'\,(B + B')", r"=", r"\pm 2", font_size=44)
        b1.next_to(hn, DOWN, buff=0.6)
        b1n = label(r"$B, B' = \pm 1$: one bracket is $0$, the other is $\pm 2$", font_size=28).next_to(b1, DOWN, buff=0.25)
        b2 = MathTex(r"|S|", r"=", r"\big|E(\mathbf a, \mathbf b) - E(\mathbf a, \mathbf b') + E(\mathbf a', \mathbf b) + E(\mathbf a', \mathbf b')\big|",
                     r"\le", r"2", font_size=38)
        b2[4].set_color(C.CLASSICAL)
        b2b = boxed(b2, color=C.CLASSICAL, buff=0.18).next_to(b1n, DOWN, buff=0.5)
        b2l = label(r"Bell (1964); this form: Clauser, Horne, Shimony \& Holt (1969)", font_size=24, color=GREY_A).next_to(b2b, DOWN, buff=0.15)
        with self.voiceover(
            "In 1935 Einstein, Podolsky and Rosen argued that such correlations mean quantum mechanics is incomplete: "
            "surely each pair leaves the source carrying hidden instructions, lambda, that decide every possible answer "
            "in advance. <bookmark mark='h'/> In 1964 John Bell showed that this idea can be tested. Suppose Alice's "
            "answer depends only on her own setting and the instructions, and Bob's on his. Give Alice two possible "
            "settings, a and a prime, and Bob two, b and b prime."
        ) as vo:
            self.play(FadeIn(epr))
            vo.wait_until("h")
            self.play(Write(h1), FadeIn(hn))
        with self.voiceover(
            "For any one pair, all four answers are plus or minus one. <bookmark mark='a'/> Look at this combination: "
            "B and B prime either agree or disagree, <bookmark mark='b'/> so one of the brackets is zero and the other is "
            "plus or minus two. The whole thing is always plus or minus two. <bookmark mark='c'/> Average over many "
            "pairs, and the combination of four correlations, called S, can never exceed two in size. That's the CHSH "
            "inequality, and it follows from nothing but pre-existing answers and locality."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(b1))
            vo.wait_until("b")
            self.play(FadeIn(b1n))
            vo.wait_until("c")
            self.play(Write(b2), Create(b2b[0]), FadeIn(b2l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chsh(self):
        ang = CHSH_ANGLES
        c0 = LEFT * 3.6 + DOWN * 0.3
        R = 2.2
        circle = Circle(radius=R, color=GREY_D, stroke_width=1.5).move_to(c0)
        def axis(deg, color, lab):
            v = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0])
            return VGroup(Arrow(c0, c0 + R * v, buff=0, color=color, stroke_width=5, tip_length=0.2),
                          MathTex(lab, font_size=32, color=color).move_to(c0 + (R + 0.4) * v))
        axs = VGroup(axis(ang["a"], C.ALICE, r"\mathbf a"), axis(ang["a2"], C.ALICE, r"\mathbf a'"),
                     axis(ang["b"], C.BOB, r"\mathbf b"), axis(ang["b2"], C.BOB, r"\mathbf b'"))
        al = label(r"settings $45^\circ$ apart", font_size=26, color=GREY_A).next_to(circle, DOWN, buff=0.5)
        q = VGroup(
            MathTex(r"E(\mathbf a, \mathbf b) = -\cos 45^\circ = -0.707", font_size=32),
            MathTex(r"E(\mathbf a, \mathbf b') = -\cos 135^\circ = +0.707", font_size=32),
            MathTex(r"E(\mathbf a', \mathbf b) = -\cos 45^\circ = -0.707", font_size=32),
            MathTex(r"E(\mathbf a', \mathbf b') = -\cos 45^\circ = -0.707", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 3.0 + UP * 1.0)
        res = MathTex(r"|S| = 4 \times 0.707 = 2\sqrt2 \approx 2.83", r"\;>\;", r"2", font_size=40)
        res[0].set_color(C.QUANTUM_BOUND)
        res[2].set_color(C.CLASSICAL)
        res.next_to(q, DOWN, buff=0.5)
        ts = label(r"the most quantum mechanics allows: $2\sqrt2$ (Tsirelson, 1980)", font_size=26, color=GREY_A).next_to(res, DOWN, buff=0.25)
        with self.voiceover(
            "Now ask what quantum mechanics predicts. <bookmark mark='s'/> Choose the four directions forty-five "
            "degrees apart. <bookmark mark='c'/> Three of the correlations are minus cosine forty-five, about minus 0.707, "
            "and the fourth, at one hundred thirty-five degrees, is plus 0.707, which enters S with a minus sign. "
            "<bookmark mark='r'/> All four contributions point the same way: S is two root two, about 2.83. More than "
            "two. No theory of pre-existing local answers can produce these correlations. <bookmark mark='t'/> And two "
            "root two is itself a hard ceiling for quantum mechanics."
        ) as vo:
            self.play(Create(circle))
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(a) for a in axs], lag_ratio=0.25), FadeIn(al))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in q], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("r")
            self.play(Write(res))
            vo.wait_until("t")
            self.play(FadeIn(ts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulate(self):
        b = load("bell")
        th, Eq, El = b["th"], b["Eq_curve"], b["El_curve"]
        Sq, Sl, n = float(b["S_q"][0]), float(b["S_lhv"][0]), int(b["n"][0])
        assert abs(abs(Sq) - 2.828) < 0.005 and abs(abs(Sl) - 1.996) < 0.005
        ax = Axes(x_range=[0, 180, 45], y_range=[-1.05, 1.05, 0.5], x_length=6.6, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(LEFT * 2.6 + DOWN * 0.4)
        qc = ax.plot(lambda d: -np.cos(np.radians(d)), x_range=[0, 180], color=C.QUANTUM_BOUND, stroke_width=3.5)
        lc = ax.plot(lambda d: -1 + 2 * d / 180, x_range=[0, 180], color=C.CLASSICAL, stroke_width=3.5)
        qd = VGroup(*[Dot(ax.c2p(np.degrees(t), e), radius=0.06, color=WHITE) for t, e in zip(th, Eq)])
        ld = VGroup(*[Dot(ax.c2p(np.degrees(t), e), radius=0.06, color=GREY_B) for t, e in zip(th, El)])
        xl = MathTex(r"\theta", font_size=30).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"E(\theta)", font_size=30).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        ticks = VGroup(*[MathTex(s_, font_size=24, color=GREY_B).next_to(ax.c2p(v, -1.05), DOWN, buff=0.1)
                         for v, s_ in ((0, r"0^\circ"), (45, r"45^\circ"), (90, r"90^\circ"), (135, r"135^\circ"), (180, r"180^\circ"))])
        g45 = DoubleArrow(ax.c2p(45, -0.5), ax.c2p(45, -0.707), buff=0, color=WHITE, stroke_width=2.5, tip_length=0.12)
        leg = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=C.QUANTUM_BOUND, stroke_width=4), MathTex(r"\text{quantum: } -\cos\theta", font_size=28)).arrange(RIGHT, buff=0.15),
            VGroup(Line(ORIGIN, RIGHT * 0.4, color=C.CLASSICAL, stroke_width=4), label(r"hidden instructions: $A = \mathrm{sign}(\mathbf a\cdot\boldsymbol\lambda)$", font_size=26)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.4)
        sres = VGroup(MathTex(r"|S|_{\text{quantum}} = " + num(abs(Sq), 3), font_size=34, color=C.QUANTUM_BOUND),
                      MathTex(r"|S|_{\text{hidden}} = " + num(abs(Sl), 3), font_size=34, color=C.CLASSICAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        sn = note(r"$10^5$ pairs per setting,\\each side sampled independently from its rule").next_to(sres, DOWN, buff=0.2).align_to(sres, LEFT)
        ns = label(r"either way, Alice alone sees 50/50:\\no message travels between them", font_size=26, color=GREY_A).next_to(sn, DOWN, buff=0.4).align_to(sn, LEFT)
        with self.voiceover(
            "We can watch the difference in a simulation. <bookmark mark='q'/> Sample a hundred thousand pairs per "
            "setting from the Born rule, and the correlation traces out minus cosine theta. <bookmark mark='l'/> Now a "
            "classical model with hidden instructions: each pair carries a random direction, and each side answers "
            "according to which side of it their axis falls on. Its correlation is a straight line. "
            "<bookmark mark='g'/> The two agree at zero, ninety and one hundred eighty degrees, but the cosine bulges "
            "past the straight line in between, and that bulge is exactly what CHSH detects. <bookmark mark='s'/> From "
            "the samples: S is 2.828 for quantum mechanics, and 1.996 for hidden instructions, within noise of the "
            "bound of two."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ticks))
            vo.wait_until("q")
            self.play(Create(qc), LaggedStart(*[FadeIn(d) for d in qd], lag_ratio=0.05), FadeIn(leg[0]))
            vo.wait_until("l")
            self.play(Create(lc), LaggedStart(*[FadeIn(d) for d in ld], lag_ratio=0.05), FadeIn(leg[1]))
            vo.wait_until("g")
            self.play(GrowFromCenter(g45))
            vo.wait_until("s")
            self.play(FadeIn(sres), FadeIn(sn))
        with self.voiceover(
            "And in both cases, Alice's results on their own are always fifty-fifty, whatever Bob does. The correlation "
            "only appears when they compare notes, so entanglement can't be used to send a message."
        ):
            self.play(FadeIn(ns))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiments(self):
        rows = VGroup(
            label(r"\textbf{1972} \ Freedman \& Clauser: entangled photons violate Bell's inequality", font_size=28),
            label(r"\textbf{1982} \ Alain Aspect and colleagues: settings switched while the photons are in flight", font_size=28),
            label(r"\textbf{2015} \ Delft: electron spins $1.3$ km apart, $S = 2.42 \pm 0.20$, the first loophole-free test", font_size=28),
            label(r"\phantom{\textbf{2015}} \ Vienna and NIST: loophole-free tests with photons", font_size=28),
            label(r"\textbf{2022} \ Nobel Prize: Aspect, Clauser, Zeilinger", font_size=28, color=C.BORN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.4)
        concl = label(r"Nature violates the bound. Measurement outcomes were not written in advance.", font_size=32,
                      color=C.QUANTUM_BOUND).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Experiment decided it. <bookmark mark='a'/> Freedman and Clauser saw the violation with photons in 1972. "
            "<bookmark mark='b'/> Alain Aspect's group switched the settings while the photons were in flight in 1982. "
            "<bookmark mark='c'/> In 2015, a team in Delft closed the remaining loopholes with electron spins 1.3 "
            "kilometers apart, measuring S equals 2.42, plus or minus 0.20, <bookmark mark='d'/> and groups in Vienna "
            "and at NIST did the same with photons. <bookmark mark='e'/> The 2022 Nobel Prize went to Aspect, Clauser "
            "and Zeilinger. Nature violates Bell's bound: the outcomes are not simply written in advance, in any local way."
        ) as vo:
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            self.play(FadeIn(concl))
        self.wait(0.5)
        self.clear_scene()
