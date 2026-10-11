from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (BlochSphere, Projector, Raster, label, ladder, lframe, load, mtex, note, num_table,
                                    plain_axes, polyline, segments_3d, signed_rgba, tick_labels, why)


class Decoherence(VoiceoverScene):
    def construct(self):
        self.record()
        self.environment()
        self.which_path()
        self.cat()
        self.numbers()
        self.what_it_explains()

    # ------------------------------------------------------------------
    def record(self):
        rows = [
            MathTex(r"\big(a\ket{0} + b\ket{1}\big)\ket{E}", r"\;\longrightarrow\;", r"a\ket{0}\ket{E_0} + b\ket{1}\ket{E_1}", font_size=38),
            MathTex(r"\hat\rho_S = \operatorname{tr}_E\ket{\Psi}\bra{\Psi}", r"=",
                    r"\begin{pmatrix} |a|^2 & a b^*\,\braket{E_1}{E_0} \\ a^* b\,\braket{E_0}{E_1} & |b|^2 \end{pmatrix}", font_size=36),
            MathTex(r"\braket{E_1}{E_0} \to 0", r"\;\Rightarrow\;", r"\hat\rho_S \to \begin{pmatrix} |a|^2 & 0 \\ 0 & |b|^2\end{pmatrix}", font_size=36),
        ]
        rows[0][2].set_color(C.ENVIRONMENT)
        rows[2][2].set_color(C.BORN)
        whys = [why(rows[0], r"the environment records which: an ordinary unitary interaction"),
                why(rows[1], r"trace out the environment"), why(rows[2], r"a perfect record: the coherences are gone")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.7)
        intro = label(r"why don't we see superpositions of everyday things?", font_size=30).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why don't we see cats in superpositions? The answer starts with the density matrix. <bookmark mark='a'/> "
            "Take a qubit, a times zero plus b times one, and let it interact with its environment: a stray photon, an "
            "air molecule. If the environment ends up in a state that depends on the qubit, E zero or E one, the qubit "
            "and its environment are now entangled. <bookmark mark='b'/> Trace out the environment, and the qubit's "
            "density matrix keeps its diagonal, the probabilities, but its coherences are multiplied by the overlap of "
            "the two environment states. <bookmark mark='c'/> Once the environment has recorded the difference, the "
            "overlap is zero, and so are the coherences."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def environment(self):
        d = load("decoherence")
        t = d["env_t"]
        ax = plain_axes((0, 12), (0, 1.05), 7.2, 3.9).move_to(LEFT * 2.6 + DOWN * 0.75)
        tks = VGroup(tick_labels(ax, xs=(0, 4, 8, 12)), tick_labels(ax, ys=(0, 0.5, 1)))
        tl = MathTex("t", font_size=28, color=C.QTIME).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"|\braket{E_1(t)}{E_0(t)}|", font_size=28, color=C.COHERENCE).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        Ns = (1, 5, 20, 200)
        cols = ["#E9D5FF", "#C4B5FD", "#A78BFA", C.COHERENCE]
        curves = VGroup(*[polyline(ax, t, d[f"env_{N}"], color=c, stroke_width=3 if N < 200 else 4.5) for N, c in zip(Ns, cols)])
        labs = VGroup(*[MathTex(f"N = {N}", font_size=26, color=c) for N, c in zip(Ns, cols)]).arrange(RIGHT, buff=0.5)
        labs.next_to(ax, DOWN, buff=0.45)
        model = MathTex(r"\braket{E_1}{E_0} = \prod_{k=1}^{N}\big(p_k e^{2ig_kt} + (1 - p_k)e^{-2ig_kt}\big)", font_size=30).to_edge(UP, buff=0.3).shift(LEFT * 2.0)
        mn = note(r"a qubit dephased by $N$ environment spins; random couplings $g_k$ (seeded), $p_k \in [0.3, 0.7]$").next_to(model, DOWN, buff=0.1)
        # Bloch ball: the arrow shrinks onto the z axis as the coherence decays (N = 200)
        proj = Projector(az=-0.55, el=0.3, scale=1.0, center=RIGHT * 4.4 + DOWN * 0.6)
        bs = BlochSphere(proj, radius=1.7, labels=True, font_size=22)
        k = ValueTracker(0)
        th0 = 1.0
        rr = d["env_200"]

        def arr():
            i = int(k.get_value())
            c = float(rr[i])
            v = np.array([math.sin(th0) * c, 0.0, math.cos(th0)])
            return bs.arrow(v, stroke_width=5)

        ar = always_redraw(arr)
        bl = label(r"$N = 200$: the Bloch arrow\\shrinks onto the $z$ axis", font_size=22, color=GREY_A).next_to(bs, DOWN, buff=0.15)
        with self.voiceover(
            "A real environment has many parts, and each takes a slightly different record. <bookmark mark='a'/> The "
            "overlap is a product of many numbers, each a little less than one. Here's a computed example: one qubit, "
            "dephased by N environment spins. <bookmark mark='b'/> With one, the coherence oscillates and comes back. "
            "<bookmark mark='c'/> With five, it comes back in bursts. <bookmark mark='d'/> With twenty, it's gone and "
            "barely flickers. <bookmark mark='e'/> With two hundred, it decays and never comes back on any time scale "
            "we could wait for. <bookmark mark='f'/> On the Bloch ball, the state's arrow shrinks onto the axis: a "
            "superposition has become a mixture."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(model), FadeIn(mn), Create(ax), FadeIn(tks), FadeIn(tl), FadeIn(yl))
            for m, i in zip("bcde", range(4)):
                vo.wait_until(m)
                self.play(Create(curves[i]), FadeIn(labs[i]), run_time=1.5)
            vo.wait_until("f")
            self.add(ar)
            self.play(FadeIn(bs), FadeIn(ar), FadeIn(bl))
            self.play(k.animate.set_value(int(np.searchsorted(t, 3.0))), run_time=3, rate_func=linear)
        ar.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def which_path(self):
        V = ValueTracker(1.0)
        y = np.linspace(-1, 1, 1200)
        ax = plain_axes((-1, 1), (0, 2.1), 10.0, 3.6).move_to(DOWN * 0.9)
        env = np.sinc(2.2 * y) ** 2

        def I(v):
            return env * (1 + v * np.cos(2 * np.pi * 6.0 * y))

        cur = always_redraw(lambda: polyline(ax, y, I(V.get_value()), color=C.BORN, stroke_width=3.5))
        two = polyline(ax, y, env, color=GREY_C, stroke_width=2).set_stroke(opacity=0.7)
        f = MathTex(r"P(y)", r"=", r"P_1 + P_2", r"+", r"2\,\mathrm{Re}\big(\psi_1^*\psi_2\,\braket{E_1}{E_2}\big)", font_size=36).to_edge(UP, buff=0.5)
        f[4].set_color(C.COHERENCE)
        vl = always_redraw(lambda: MathTex(r"|\braket{E_1}{E_2}| = " + f"{V.get_value():.2f}", font_size=32, color=C.COHERENCE).next_to(f, DOWN, buff=0.3))
        gl = label(r"no record: full fringes", font_size=26, color=C.BORN)
        gr = label(r"perfect record: $P_1 + P_2$, no fringes", font_size=26, color=GREY_A)
        VGroup(gl, gr).arrange(RIGHT, buff=1.5).to_edge(DOWN, buff=0.35)
        sch = note(r"schematic far-field pattern of two slits").to_corner(DR, buff=0.2).shift(UP * 0.5)
        with self.voiceover(
            "<bookmark mark='a'/> For the double slit, the environment records which slit the electron went through, and "
            "the interference term is multiplied by the overlap of the two records. <bookmark mark='b'/> A perfect "
            "record erases the fringes completely, leaving the sum of the two single-slit patterns; a partial record "
            "leaves faded fringes. This is complementarity, made quantitative."
        ) as vo:
            vo.wait_until("a")
            self.add(cur, vl)
            self.play(Write(f), Create(ax), FadeIn(cur), FadeIn(vl), FadeIn(gl), FadeIn(sch))
            vo.wait_until("b")
            self.play(V.animate.set_value(0.0), FadeIn(two), run_time=4)
            self.play(FadeIn(gr))
        cur.clear_updaters()
        vl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cat(self):
        d = load("decoherence")
        W, x, p, s = d["W"], d["x"], d["p"], d["s"]
        vmax = float(np.abs(W[0]).max())
        k = ValueTracker(0)
        img = Raster(lambda v: signed_rgba(W[int(round(v))][::-1], vmax=vmax), k, 6.4, 4.2, center=LEFT * 2.6 + DOWN * 0.2)
        fr = Rectangle(width=6.42, height=4.22, stroke_color=GREY_C, stroke_width=1.5).move_to(img)
        xl = MathTex("x", font_size=28, color=C.XPOS).next_to(fr, DOWN, buff=0.1)
        pl = MathTex("p", font_size=28, color=C.MOMENTUM).next_to(fr, LEFT, buff=0.1)
        sl = always_redraw(lambda: MathTex(r"\Lambda t = " + f"{s[int(round(k.get_value()))]:.3f}", font_size=30, color=C.QTIME).next_to(fr, UP, buff=0.15))
        rule = MathTex(r"\rho(x, x', t) = \rho(x, x', 0)\,e^{-\Lambda t\,(x - x')^2}", font_size=32).to_edge(UP, buff=0.3).shift(RIGHT * 2.6)
        # fringe amplitude vs time, with theory
        ax = plain_axes((0, 0.15), (0, 1.05), 4.4, 2.6).move_to(RIGHT * 4.3 + DOWN * 0.3)
        tks = VGroup(tick_labels(ax, xs=(0, 0.05, 0.1, 0.15)), tick_labels(ax, ys=(0, 0.5, 1)))
        th = polyline(ax, s, d["fringe_theory"], color=C.COHERENCE, stroke_width=3)
        dots_ = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=WHITE) for a, b in zip(s, d["fringe"])])
        bl = polyline(ax, s, d["blob"], color=C.WIGNER_POS, stroke_width=3)
        lab = VGroup(VGroup(Dot(radius=0.05, color=WHITE), label(r"fringe height (computed)", font_size=20)).arrange(RIGHT, buff=0.08),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, color=C.COHERENCE, stroke_width=3), label(r"theory: $e^{-4\Lambda t x_0^2}$ (Gaussian-corrected)", font_size=20, color=C.COHERENCE)).arrange(RIGHT, buff=0.08),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, color=C.WIGNER_POS, stroke_width=3), label(r"blob height", font_size=20, color=C.WIGNER_POS)).arrange(RIGHT, buff=0.08)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, DOWN, buff=0.45)
        rl = label(r"rate $\propto$ (separation)$^2$", font_size=26, color=C.COHERENCE).next_to(ax, UP, buff=0.2)
        cap = note(r"a cat state ($x_0 = \pm 3$) losing coherence to scattering; Wigner function, amber $> 0$, blue $< 0$").to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here's a Schrödinger cat state, two separated packets, as a Wigner function, losing its coherence to a "
            "scattering environment. <bookmark mark='a'/> Each scattered particle multiplies the density matrix by a "
            "factor that depends on how far apart the two positions are: the off-diagonal terms decay like e to the minus "
            "Lambda t times the separation squared. <bookmark mark='b'/> The interference fringes between the blobs fade, "
            "exactly at the predicted rate, while the blobs themselves survive."
        ) as vo:
            self.add(img, sl)
            self.play(FadeIn(img), Create(fr), FadeIn(xl), FadeIn(pl), FadeIn(sl), FadeIn(cap))
            vo.wait_until("a")
            self.play(Write(rule))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(tks), FadeIn(lab), FadeIn(rl), Create(th), Create(bl))
            self.play(k.animate.set_value(len(s) - 1), LaggedStart(*[FadeIn(d_) for d_ in dots_], lag_ratio=0.1), run_time=5, rate_func=linear)
        img.clear_updaters()
        sl.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        rows = [[r"\text{cosmic background}", r"1\ \text{s}", r"10^{24}\ \text{s}"],
                [r"\text{room-temperature light}", r"10^{-18}\ \text{s}", r"10^{6}\ \text{s}"],
                [r"\text{best laboratory vacuum}", r"10^{-14}\ \text{s}", r"10^{-2}\ \text{s}"],
                [r"\text{air}", r"10^{-31}\ \text{s}", r"10^{-19}\ \text{s}"]]
        tab = num_table([r"\text{environment}", r"\text{dust grain } (10\,\mu\text{m})", r"\text{large molecule } (10\,\text{nm})"], rows,
                        font_size=32, col_colors=[GREY_A, C.COHERENCE, C.COHERENCE]).move_to(DOWN * 0.1)
        t = label(r"how long a superposition of two positions, one object-size apart, survives", font_size=28).to_edge(UP, buff=0.6)
        src = note(r"order-of-magnitude estimates: Joos \& Zeh (1985); table from Schlosshauer, Phys.\ Rep.\ 831 (2019)").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And because the rate grows with the square of the separation, big superpositions die fast. "
            "<bookmark mark='a'/> Estimates from the literature: a dust grain a hundredth of a millimeter across, in "
            "air, loses a superposition of two positions its own size apart in about ten to the minus thirty-one "
            "seconds. <bookmark mark='b'/> Even the cosmic microwave background alone would do it in about a second."
        ) as vo:
            self.play(FadeIn(t), FadeIn(tab.header), Create(tab.rule), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.3), run_time=2)
            self.play(Indicate(tab.rows[3], color=C.COHERENCE))
            vo.wait_until("b")
            self.play(Indicate(tab.rows[0], color=C.COHERENCE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def what_it_explains(self):
        yes = VGroup(label(r"decoherence explains", font_size=32, color=C.BORN),
                     label(r"why interference between macroscopically different states is never seen", font_size=24),
                     label(r"why positions (not their superpositions) are what survive: ``pointer states''", font_size=24),
                     label(r"how fast: $10^{-31}$ s for a dust grain in air", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        no = VGroup(label(r"it does not explain", font_size=32, color=C.FERMION),
                    label(r"why one particular outcome occurs:", font_size=24),
                    label(r"$\hat\rho_S$ looks like a list of possibilities, but the whole state is still one superposition", font_size=24),
                    label(r"the measurement problem; the interpretations part ways here", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        VGroup(yes, no).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP * 0.2)
        h = note(r"observed step by step: Brune et al.\ (Haroche group), PRL 77, 4887 (1996); Nobel Prize 2012 (Haroche, Wineland)").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> That's why the world looks classical: the environment is constantly measuring "
            "positions, and only states that survive that are ever seen. Serge Haroche's group watched it happen, step "
            "by step, with photons in a cavity in 1996. <bookmark mark='b'/> But decoherence doesn't explain why one "
            "particular outcome occurs. The density matrix ends up looking like a list of possibilities with "
            "probabilities, yet the whole state is still one superposition; which outcome we see is the measurement "
            "problem, and the interpretations of quantum mechanics part ways exactly there."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(yes), FadeIn(h))
            vo.wait_until("b")
            self.play(FadeIn(no))
        self.wait(0.4)
        self.clear_scene()
