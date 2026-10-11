from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (BlochSphere, Projector, bloch_vector, label, ladder, line_3d, mtex, note, part_card,
                                    segments_3d, why)


def mat2(entries, colors=None, font_size=34):
    m = MathTex(r"\begin{pmatrix} " + entries[0] + " & " + entries[1] + r" \\ " + entries[2] + " & " + entries[3] + r" \end{pmatrix}",
                font_size=font_size)
    return m


class Density(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_uncertainties()
        self.ball()
        self.partial_trace()
        self.gleason()

    # ------------------------------------------------------------------
    def card(self):
        c = part_card(5, r"Open systems", r"density matrices, decoherence, measurement")
        with self.voiceover("Part 5: Open systems."):
            self.play(FadeIn(c))
        self.wait(0.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def two_uncertainties(self):
        sup = VGroup(label(r"a superposition", font_size=30, color=C.COHERENCE),
                     MathTex(r"\ket{+x} = \tfrac{1}{\sqrt2}\big(\ket{\uparrow} + \ket{\downarrow}\big)", font_size=32)).arrange(DOWN, buff=0.2)
        mix = VGroup(label(r"a coin flip", font_size=30, color=C.BORN),
                     MathTex(r"\ket{\uparrow} \text{ or } \ket{\downarrow},\ \text{50/50}", font_size=32)).arrange(DOWN, buff=0.2)
        VGroup(sup, mix).arrange(RIGHT, buff=2.2).to_edge(UP, buff=0.4)
        z1 = MathTex(r"\text{along } z:\ 50/50", font_size=30).next_to(sup, DOWN, buff=0.35)
        z2 = MathTex(r"\text{along } z:\ 50/50", font_size=30).next_to(mix, DOWN, buff=0.35)
        x1 = MathTex(r"\text{along } x:\ +\ \text{always}", font_size=30, color=C.COHERENCE).next_to(z1, DOWN, buff=0.2)
        x2 = MathTex(r"\text{along } x:\ 50/50", font_size=30, color=C.BORN).next_to(z2, DOWN, buff=0.2)
        rho = MathTex(r"\hat\rho", r"=", r"\sum_i p_i\,\ket{\psi_i}\bra{\psi_i}", r",\qquad", r"P(a) = \operatorname{tr}\big(\hat\rho\,\hat P_a\big)", font_size=36).move_to(UP * 0.55)
        r1 = mat2([r"\tfrac12", r"\tfrac12", r"\tfrac12", r"\tfrac12"])
        r2 = mat2([r"\tfrac12", "0", "0", r"\tfrac12"])
        r1.move_to([x1.get_x(), -1.15, 0])
        r2.move_to([x2.get_x(), -1.15, 0])
        off = label(r"off-diagonal: coherences", font_size=22, color=C.COHERENCE).next_to(r1, DOWN, buff=0.15)
        pur = VGroup(MathTex(r"\operatorname{tr}\hat\rho^2 = 1:\ \text{pure}", font_size=26, color=C.COHERENCE).next_to(off, DOWN, buff=0.1),
                     MathTex(r"\operatorname{tr}\hat\rho^2 = \tfrac12:\ \text{mixed}", font_size=26, color=C.BORN).next_to(r2, DOWN, buff=0.4))
        with self.voiceover(
            "Here are two very different kinds of uncertainty. <bookmark mark='a'/> A spin in the superposition up plus "
            "down, over root two: pointing along x. <bookmark mark='b'/> And a spin that's up or down depending on a coin "
            "toss. <bookmark mark='c'/> Measure either one along z, and you get up half the time. <bookmark mark='d'/> "
            "But measure along x, and the superposition gives plus every time, while the coin-flip spin is still "
            "fifty-fifty."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(sup))
            vo.wait_until("b")
            self.play(FadeIn(mix))
            vo.wait_until("c")
            self.play(FadeIn(z1), FadeIn(z2))
            vo.wait_until("d")
            self.play(FadeIn(x1), FadeIn(x2))
        with self.voiceover(
            "A list of states with probabilities is not a superposition, and to describe it we need a new object: "
            "<bookmark mark='a'/> the density matrix, rho, the probability-weighted sum of projectors onto the states. "
            "The Born rule becomes the trace of rho times the projector for the outcome. <bookmark mark='b'/> The "
            "superposition's density matrix has off-diagonal terms, called coherences; <bookmark mark='c'/> the coin "
            "flip's has none."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(rho))
            vo.wait_until("b")
            self.play(Write(r1), FadeIn(off), FadeIn(pur[0]))
            vo.wait_until("c")
            self.play(Write(r2), FadeIn(pur[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ball(self):
        proj = Projector(az=-0.55, el=0.32, scale=1.0, center=LEFT * 2.8 + DOWN * 0.4)
        bs = BlochSphere(proj, radius=2.4, labels=True, font_size=26)
        shell = Circle(radius=2.4, color=GREY_C, fill_color=C.BLOCH, fill_opacity=0.08, stroke_width=0).move_to(proj.center)
        f = MathTex(r"\hat\rho", r"=", r"\tfrac12\big(1 + \vec r\cdot\vec\sigma\big)", r",\quad |\vec r| \le 1", font_size=36).to_edge(UP, buff=0.4).shift(RIGHT * 3.2)
        pure = label(r"$|\vec r| = 1$: pure (the sphere)", font_size=26).next_to(f, DOWN, buff=0.3)
        mixed = label(r"$|\vec r| < 1$: mixed (the inside)", font_size=26, color=C.BORN).next_to(pure, DOWN, buff=0.15)
        purity = MathTex(r"\operatorname{tr}\hat\rho^2 = \tfrac12\big(1 + |\vec r|^2\big)", font_size=30).next_to(mixed, DOWN, buff=0.25)
        center = proj.center
        up, dn = bs.bloch_to_screen([0, 0, 1])[0], bs.bloch_to_screen([0, 0, -1])[0]
        px, mx = bs.bloch_to_screen([1, 0, 0])[0], bs.bloch_to_screen([-1, 0, 0])[0]
        a1 = VGroup(Dot(up, color=C.SPIN_UP, radius=0.1), Dot(dn, color=C.SPIN_DOWN, radius=0.1))
        a2 = VGroup(Dot(px, color=C.COHERENCE, radius=0.1), Dot(mx, color=C.COHERENCE, radius=0.1))
        mid = Dot(center, color=C.BORN, radius=0.12)
        l1 = label(r"$\uparrow$ or $\downarrow$, 50/50", font_size=24, color=C.SPIN_UP).move_to(RIGHT * 3.2 + DOWN * 1.2)
        l2 = label(r"$+x$ or $-x$, 50/50", font_size=24, color=C.COHERENCE).next_to(l1, DOWN, buff=0.15)
        same = label(r"the same $\hat\rho = \tfrac12$: no experiment can tell them apart", font_size=26, color=C.BORN).next_to(l2, DOWN, buff=0.3)
        with self.voiceover(
            "For a spin, every density matrix is one half, times one plus r dot sigma, with r a vector no longer than "
            "one. <bookmark mark='a'/> Pure states have length one: the Bloch sphere. <bookmark mark='b'/> Mixtures fill "
            "the inside: the Bloch ball. <bookmark mark='c'/> And different mixtures can give the same rho: a coin flip "
            "between up and down, <bookmark mark='d'/> or between plus x and minus x, <bookmark mark='e'/> both land at "
            "the center, and no measurement can ever tell them apart. The density matrix is everything there is to "
            "know."
        ) as vo:
            self.play(Write(f), FadeIn(bs))
            vo.wait_until("a")
            self.play(FadeIn(pure), GrowArrow(bs.arrow(bloch_vector(0.9, 0.6))))
            vo.wait_until("b")
            self.play(FadeIn(shell), FadeIn(mixed), FadeIn(purity))
            vo.wait_until("c")
            self.play(FadeIn(a1), FadeIn(l1))
            self.play(*[d.animate.move_to(center) for d in a1], run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(a2), FadeIn(l2))
            self.play(*[d.animate.move_to(center) for d in a2], run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(mid), FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def partial_trace(self):
        rows = [
            MathTex(r"\ket{\psi}", r"=", r"\tfrac{1}{\sqrt2}\big(\ket{\uparrow\downarrow} - \ket{\downarrow\uparrow}\big)", font_size=38),
            MathTex(r"\hat\rho_A", r"=", r"\operatorname{tr}_B\ket{\psi}\bra{\psi} = \sum_{b = \uparrow, \downarrow}\bra{b}_B\,\ket{\psi}\bra{\psi}\,\ket{b}_B", font_size=36),
            MathTex(r"\hat\rho_A", r"=", r"\tfrac12\ket{\uparrow}\bra{\uparrow} + \tfrac12\ket{\downarrow}\bra{\downarrow} = \tfrac12\,\mathbb{I}", font_size=38),
            MathTex(r"S", r"=", r"-\operatorname{tr}\hat\rho_A\ln\hat\rho_A = \ln 2", font_size=36),
        ]
        rows[2][2].set_color(C.BORN)
        whys = [why(rows[0], r"the singlet: a pure state of two spins"), why(rows[1], r"Alice alone: sum over Bob's outcomes"),
                why(rows[2], r"the center of the ball"), why(rows[3], r"the most entropy a spin can have")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.4, buff=0.55)
        msg = label(r"the whole is perfectly definite; each part alone is completely random", font_size=28, color=C.BORN).to_edge(DOWN, buff=0.9)
        imp = note(r"an ``improper'' mixture: nothing here is unknown --- the randomness comes from entanglement").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Mixed states don't only come from ignorance. <bookmark mark='a'/> Take two spins in the singlet: a pure "
            "state of the pair. <bookmark mark='b'/> Ask what Alice alone can measure, by tracing out Bob's spin: summing "
            "over his possible outcomes. <bookmark mark='c'/> The result is one half times the identity, the center of "
            "the ball, <bookmark mark='d'/> with the largest entropy a spin can have. <bookmark mark='e'/> The whole is "
            "perfectly definite; each part, on its own, is completely random. That's entanglement, seen from one side."
        ) as vo:
            for m, i in zip("abcd", range(4)):
                vo.wait_until(m)
                step(i)
            vo.wait_until("e")
            self.play(FadeIn(msg), FadeIn(imp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gleason(self):
        proj = Projector(az=-0.6, el=0.35, scale=1.9, center=LEFT * 3.4 + DOWN * 0.5)
        rho = np.array([[0.55, 0.12, 0.05], [0.12, 0.30, -0.08], [0.05, -0.08, 0.15]])
        assert abs(np.trace(rho) - 1) < 1e-12 and np.linalg.eigvalsh(rho).min() > 0
        t = ValueTracker(0.0)

        def frame(tt):
            a, b = 0.9 * tt, 0.6 * math.sin(1.3 * tt)
            R1 = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
            R2 = np.array([[1, 0, 0], [0, math.cos(b), -math.sin(b)], [0, math.sin(b), math.cos(b)]])
            return R2 @ R1

        cols = [C.XPOS, C.MOMENTUM, C.ENERGY]

        def pic():
            F = frame(t.get_value())
            g = VGroup()
            o = proj.point([0, 0, 0])
            for i in range(3):
                e = F[:, i]
                g.add(Arrow(o, proj.point(e), buff=0, color=cols[i], stroke_width=5, tip_length=0.18))
            return g

        def bars():
            F = frame(t.get_value())
            ps = [float(F[:, i] @ rho @ F[:, i]) for i in range(3)]
            g = VGroup()
            base = LEFT * 0.9 + DOWN * 2.6
            x = 0
            for i, p in enumerate(ps):
                g.add(Rectangle(width=0.55, height=4.0 * p, stroke_width=0, fill_color=cols[i], fill_opacity=0.85).move_to(base + RIGHT * x + UP * 2.0 * p))
                x += 0.8
            g.add(MathTex(r"\textstyle\sum = " + f"{sum(ps):.3f}", font_size=28).move_to(base + RIGHT * 0.8 + DOWN * 0.35))
            return g

        pg, bg = always_redraw(pic), always_redraw(bars)
        cond = VGroup(
            label(r"assign a probability $P(e)$ to every outcome $e$,", font_size=26),
            label(r"so that perpendicular outcomes always add to 1:", font_size=26),
            MathTex(r"P(e_1) + P(e_2) + P(e_3) = 1 \text{ for every frame}", font_size=30),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).to_edge(UP, buff=0.4).shift(RIGHT * 1.5)
        thm = VGroup(label(r"Gleason (1957), dimension $\ge 3$:", font_size=28, color=C.BORN),
                     MathTex(r"P(e) = \bra{e}\hat\rho\ket{e} = \operatorname{tr}\big(\hat\rho\,\ket{e}\bra{e}\big)", font_size=36, color=C.BORN),
                     label(r"the Born rule is the \emph{only} consistent rule", font_size=28, color=C.BORN)).arrange(DOWN, buff=0.2)
        if thm.width > 5.4:
            thm.width = 5.4
        thm.move_to(RIGHT * 4.1 + DOWN * 1.0)
        with self.voiceover(
            "And the density matrix closes a gap from the start of this video: why the Born rule? "
            "<bookmark mark='a'/> Suppose you assign a probability to every possible outcome of every measurement, "
            "<bookmark mark='b'/> such that for any set of mutually perpendicular outcomes, the probabilities add to one. "
            "<bookmark mark='c'/> In 1957 Andrew Gleason proved that in three or more dimensions, the only such "
            "assignments are the trace of rho times the projector, for some density matrix rho. <bookmark mark='d'/> "
            "Given the vector structure of quantum states, the Born rule is the only consistent way to get probabilities "
            "out of them."
        ) as vo:
            vo.wait_until("a")
            self.add(pg, bg)
            self.play(FadeIn(cond[0]), FadeIn(pg), FadeIn(bg))
            vo.wait_until("b")
            self.play(FadeIn(cond[1]), FadeIn(cond[2]), t.animate.set_value(3.0), run_time=3.5, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(thm[0]), Write(thm[1]), t.animate.set_value(5.0), run_time=2.5, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(thm[2]), t.animate.set_value(6.5), run_time=2.0, rate_func=linear)
        pg.clear_updaters()
        bg.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
