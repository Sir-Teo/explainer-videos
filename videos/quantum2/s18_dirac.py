from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (WaveView, corner_wheel, label, ladder, lframe, load, mtex, note, part_card, plain_axes,
                                    polyline, tick_labels, wave_axes, why)


class Dirac(VoiceoverScene):
    def construct(self):
        self.card()
        self.klein_gordon()
        self.linearize()
        self.matrices()
        self.energies()
        self.zitter()

    # ------------------------------------------------------------------
    def card(self):
        c = part_card(6, r"Relativity", r"the Dirac equation")
        with self.voiceover("Part 6: Relativity."):
            self.play(FadeIn(c))
        self.wait(0.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def klein_gordon(self):
        e1 = MathTex(r"E^2 = p^2c^2 + m^2c^4", font_size=46).to_edge(UP, buff=0.6)
        e2 = MathTex(r"-\hbar^2\frac{\partial^2\psi}{\partial t^2}", r"=", r"-\hbar^2c^2\nabla^2\psi + m^2c^4\psi", font_size=40).next_to(e1, DOWN, buff=0.6)
        kg = note(r"the Klein--Gordon equation (1926)").next_to(e2, DOWN, buff=0.15)
        probs = VGroup(label(r"second order in time: $\psi$ now no longer fixes the future", font_size=28),
                       label(r"its conserved ``density'' can be negative", font_size=28)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(kg, DOWN, buff=0.5)
        want = label(r"Dirac (1928): keep $i\hbar\,\partial_t\psi = \hat H\psi$, first order, and make $\hat H$ linear in $\hat{\mathbf p}$", font_size=28,
                     color=C.DIRAC_POS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Everything so far has been non-relativistic. Relativity demands that energy and momentum be related by E "
            "squared equals p squared c squared plus m squared c to the fourth. <bookmark mark='a'/> The obvious move is "
            "to replace E and p by their operators. That gives the Klein-Gordon equation, <bookmark mark='b'/> but it's "
            "second order in time, so the wavefunction now no longer determines its own future, and the quantity it "
            "conserves can be negative: it can't be a probability. <bookmark mark='c'/> In 1928 Paul Dirac insisted on "
            "keeping the Schrödinger form, first order in time, which means a Hamiltonian that is linear in momentum."
        ) as vo:
            self.play(Write(e1))
            vo.wait_until("a")
            self.play(Write(e2), FadeIn(kg))
            vo.wait_until("b")
            self.play(FadeIn(probs))
            vo.wait_until("c")
            self.play(FadeIn(want))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linearize(self):
        rows = [
            MathTex(r"\hat H", r"=", r"c\,\boldsymbol\alpha\cdot\hat{\mathbf p} + \beta\,mc^2", font_size=42),
            MathTex(r"\hat H^2", r"=", r"c^2\sum_i\alpha_i^2p_i^2 + c^2\sum_{i<j}(\alpha_i\alpha_j + \alpha_j\alpha_i)p_ip_j + mc^3\sum_i(\alpha_i\beta + \beta\alpha_i)p_i + \beta^2m^2c^4",
                    font_size=30),
            MathTex(r"\hat H^2", r"=", r"p^2c^2 + m^2c^4", font_size=40),
            MathTex(r"\alpha_i^2 = \beta^2 = 1", r",\quad", r"\alpha_i\alpha_j + \alpha_j\alpha_i = 0\ (i \ne j),\quad \alpha_i\beta + \beta\alpha_i = 0", font_size=34),
        ]
        rows[0][2].set_color(C.DIRAC_POS)
        rows[3].set_color(C.DIRAC_POS)
        whys = [why(rows[0], r"linear in $\hat{\mathbf p}$; $\alpha_i$, $\beta$ unknown"), why(rows[1], r"square it, keeping the order of the factors"),
                why(rows[2], r"what relativity demands"), why(rows[3], r"so: four quantities that \emph{anticommute}")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-2.0, buff=0.55)
        num = label(r"no numbers can do this: $\alpha_i$ and $\beta$ must be matrices", font_size=28, color=C.DIRAC_POS).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "<bookmark mark='a'/> So write H as c times alpha dot p, plus beta m c squared, with four unknown "
            "coefficients. <bookmark mark='b'/> Square it, carefully keeping the order of the factors. "
            "<bookmark mark='c'/> For this to equal p squared c squared plus m squared c to the fourth, "
            "<bookmark mark='d'/> each alpha and beta must square to one, and every pair must anticommute: alpha i times "
            "alpha j equals minus alpha j times alpha i. <bookmark mark='e'/> No numbers behave like that. They have to "
            "be matrices."
        ) as vo:
            for m, i in zip("abcd", range(4)):
                vo.wait_until(m)
                step(i)
            vo.wait_until("e")
            self.play(FadeIn(num))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def matrices(self):
        a = MathTex(r"\alpha_i = \begin{pmatrix} 0 & \sigma_i \\ \sigma_i & 0\end{pmatrix}", r",\qquad", r"\beta = \begin{pmatrix} \mathbb{I} & 0 \\ 0 & -\mathbb{I}\end{pmatrix}",
                    font_size=40).to_edge(UP, buff=0.6)
        why2 = label(r"$2\times 2$ is too small: only the three Pauli matrices anticommute, and we need four", font_size=26, color=GREY_A).next_to(a, DOWN, buff=0.35)
        chk = note(r"all ten anticommutators checked numerically (compute.py)").next_to(why2, DOWN, buff=0.15)
        psi = MathTex(r"\psi = \begin{pmatrix}\psi_1\\ \psi_2\\ \psi_3\\ \psi_4\end{pmatrix}", font_size=40).move_to(LEFT * 3.0 + DOWN * 1.4)
        brace_t = BraceBetweenPoints(psi.get_corner(UR) + RIGHT * 0.1, psi.get_right() + RIGHT * 0.1 + DOWN * 0.05, direction=RIGHT, color=C.SPIN_UP)
        brace_b = BraceBetweenPoints(psi.get_right() + RIGHT * 0.1 + UP * 0.05, psi.get_corner(DR) + RIGHT * 0.1, direction=RIGHT, color=C.SPIN_DOWN)
        mean = VGroup(label(r"four components:", font_size=28),
                      label(r"spin up and down (spin $\tfrac12$ appears unasked),", font_size=28, color=C.SPIN_UP),
                      label(r"for positive and negative energy", font_size=28, color=C.DIRAC_NEG)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 2.4 + DOWN * 1.4)
        ll = note(r"(L\'evy-Leblond, 1967: linearizing the \emph{non}-relativistic equation also gives spin $\tfrac12$; relativity adds the negative energies)").to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "<bookmark mark='a'/> The smallest matrices that work are four by four, built from the Pauli matrices of "
            "Part 1. Two by two is too small: only three two-by-two matrices anticommute, and we need four. "
            "<bookmark mark='b'/> So the wavefunction has four components. <bookmark mark='c'/> Two of them are spin up "
            "and spin down: spin one half appears without being put in. <bookmark mark='d'/> The doubling comes from "
            "something new: solutions with negative energy."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(a), FadeIn(why2), FadeIn(chk))
            vo.wait_until("b")
            self.play(Write(psi), FadeIn(mean[0]))
            vo.wait_until("c")
            self.play(GrowFromCenter(brace_t), GrowFromCenter(brace_b), FadeIn(mean[1]), FadeIn(ll))
            vo.wait_until("d")
            self.play(FadeIn(mean[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def energies(self):
        d = load("dirac")
        k, E = d["Ek_k"], d["Ek"]
        ax = plain_axes((-4, 4), (-4.4, 4.4), 6.4, 5.8).move_to(LEFT * 3.0 + DOWN * 0.3)
        pl = MathTex(r"p", font_size=30, color=C.MOMENTUM).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        el = MathTex(r"E", font_size=30, color=C.ENERGY).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        up = polyline(ax, k, E, color=C.DIRAC_POS, stroke_width=4)
        dn = polyline(ax, k, -E, color=C.DIRAC_NEG, stroke_width=4)
        gap = BraceBetweenPoints(ax.c2p(0.15, -1), ax.c2p(0.15, 1), direction=RIGHT, color=GREY_A)
        gl = MathTex(r"2mc^2", font_size=28).next_to(gap, RIGHT, buff=0.1)
        f = MathTex(r"E = \pm\sqrt{p^2c^2 + m^2c^4}", font_size=36).to_edge(UP, buff=0.4).shift(RIGHT * 3.2)
        def para(*lines, color=WHITE):
            return VGroup(*[label(t, font_size=24, color=color) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        hist = VGroup(
            para(r"Dirac (1930): the negative-energy states", r"are all filled; a hole acts like a positive charge"),
            para(r"Dirac (1931): an ``anti-electron'' of the same mass"),
            para(r"Anderson (1932): the positron, in cosmic rays", color=C.DIRAC_NEG),
            para(r"today: the negative-energy solutions", r"describe antiparticles (quantum field theory)", color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        if hist.width > 5.7:
            hist.width = 5.7
        hist.move_to(RIGHT * 4.0 + DOWN * 0.3)
        # the Dirac sea: every negative-energy state filled; lift one electron out and leave a hole
        ks = np.linspace(-3.6, 3.6, 19)
        Ek = np.interp(ks, k, E)
        sea = VGroup(*[Dot(ax.c2p(kk, -ee), radius=0.075, color=C.DIRAC_NEG) for kk, ee in zip(ks, Ek)])
        j = 14
        assert abs(ks[j] - 2.0) < 1e-9
        hole = Circle(radius=0.075, color=C.DIRAC_NEG, stroke_width=2.5).move_to(sea[j])
        up_pt = ax.c2p(ks[j], Ek[j])
        el_l = label(r"electron", font_size=24, color=C.DIRAC_POS).move_to(ax.c2p(3.1, 0.75))
        ho_l = label(r"hole: charge $+e$", font_size=24, color=C.DIRAC_NEG).move_to(ax.c2p(2.9, -0.75))
        el_a = Arrow(el_l.get_top(), up_pt, buff=0.12, stroke_width=2, color=GREY_B, max_tip_length_to_length_ratio=0.15)
        ho_a = Arrow(ho_l.get_bottom(), hole.get_center(), buff=0.12, stroke_width=2, color=GREY_B, max_tip_length_to_length_ratio=0.15)
        with self.voiceover(
            "<bookmark mark='a'/> The energies come in pairs: plus and minus the square root of p squared c squared plus m "
            "squared c to the fourth, two branches separated by a gap of two m c squared. <bookmark mark='b'/> The "
            "negative branch was a crisis. Dirac proposed in 1930 that those states are all filled, so that a missing "
            "one, a hole, would act like a particle of positive charge; <bookmark mark='c'/> a year later he predicted an "
            "anti-electron with the electron's mass. <bookmark mark='d'/> Carl Anderson found it in cosmic rays in 1932: "
            "the positron. <bookmark mark='e'/> Today the negative-energy solutions are understood through quantum field "
            "theory, as describing antiparticles."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(pl), FadeIn(el), Create(up), Create(dn), GrowFromCenter(gap), FadeIn(gl), Write(f))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(dd, scale=0.5) for dd in sea], lag_ratio=0.05), FadeIn(hist[0]), run_time=1.6)
            self.add(hole)
            self.play(sea[j].animate.move_to(up_pt).set_color(C.DIRAC_POS), run_time=1.4)
            self.play(FadeIn(el_l), GrowArrow(el_a), FadeIn(ho_l), GrowArrow(ho_a), run_time=1.0)
            for m, i in zip("cde", range(1, 4)):
                vo.wait_until(m)
                self.play(FadeIn(hist[i]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zitter(self):
        d = load("dirac")
        x, fr, ts = d["x"], d["frames"], d["t"][::2]
        xm, xp = d["xm_mix"], d["xm_pos"]
        t = ValueTracker(0)
        sel = np.abs(x) < 9
        xs = x[sel]
        top = wave_axes((-9, 9), (0, 0.32), x_length=6.0, y_length=1.5).move_to(LEFT * 3.2 + UP * 1.5)
        bot = wave_axes((-9, 9), (0, 0.32), x_length=6.0, y_length=1.5).move_to(LEFT * 3.2 + DOWN * 0.4)
        # the packet spreads (its peak falls ~5x by the end): show each frame rescaled to the starting peak height
        peak = np.array([np.max(np.abs(fr_i[:, sel]) ** 2) for fr_i in fr])
        gain = np.sqrt(peak[0] / peak)
        f0 = lambda v: fr[int(round(v))][0][sel] * gain[int(round(v))]  # noqa: E731
        f1 = lambda v: fr[int(round(v))][1][sel] * gain[int(round(v))]  # noqa: E731
        w0 = WaveView(top, xs, f0(0), mode="density").follow(t, f0)
        w1 = WaveView(bot, xs, f1(0), mode="density").follow(t, f1)
        l0 = MathTex(r"|\psi_1|^2", font_size=26).next_to(top, LEFT, buff=0.1)
        l1 = MathTex(r"|\psi_2|^2", font_size=26).next_to(bot, LEFT, buff=0.1)
        rs = note(r"each frame rescaled to the same peak height (the packet spreads)").next_to(bot, DOWN, buff=0.25)
        ax = plain_axes((0, 24), (-1.0, 0.1), 5.8, 3.0).move_to(RIGHT * 3.6 + UP * 0.6)
        frm = lframe(ax)
        tks = VGroup(tick_labels(ax, xs=(0, 8, 16, 24)), tick_labels(ax, ys=(-1, -0.5, 0)))
        tl = MathTex(r"t", font_size=26, color=C.QTIME).next_to(frm[0].get_end(), RIGHT, buff=0.1)
        yl = MathTex(r"\langle x\rangle", font_size=26).next_to(frm[1].get_end(), UP, buff=0.05)
        tt = d["t"]
        cm = always_redraw(lambda: polyline(ax, tt[: 2 * int(round(t.get_value())) + 2], xm[: 2 * int(round(t.get_value())) + 2], color=C.DIRAC_POS, stroke_width=3))
        cp = polyline(ax, tt, xp, color=C.DIRAC_NEG, stroke_width=3)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.3, color=C.DIRAC_POS, stroke_width=3), label(r"this packet: half $E > 0$, half $E < 0$", font_size=20)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, color=C.DIRAC_NEG, stroke_width=3), label(r"its $E > 0$ part alone", font_size=20)).arrange(RIGHT, buff=0.1)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, DOWN, buff=0.45)
        w = float(d["zb_omega"])
        assert 1.9 < w < 2.6
        n = load("numbers")
        expl = VGroup(label(r"interference between the two branches, at $\omega \approx 2mc^2/\hbar$ (here " + f"{w:.2f}" + r")", font_size=22),
                      label(r"for an electron: $\hbar/2mc = 1.9\times 10^{-13}$ m, $2mc^2/\hbar = 1.6\times 10^{21}\ \text{s}^{-1}$", font_size=22, color=GREY_A),
                      label(r"never seen for free electrons; simulated with trapped ions (Gerritsma et al., 2010)", font_size=22, color=GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.3)
        assert abs(float(n["zb_amp_m"]) - 1.931e-13) < 1e-16 and abs(float(n["zb_omega"]) - 1.5527e21) < 1e18
        cap = note(r"1 + 1 dimensions, $\hbar = m = c = 1$; computed exactly").to_corner(UR, buff=0.2)
        wheel = corner_wheel(corner=UL, buff=0.15, radius=0.22)
        with self.voiceover(
            "Mixing the two branches has a strange consequence. <bookmark mark='a'/> Here's a packet in a one-dimensional "
            "version of the Dirac equation, half positive energy and half negative, solved exactly. "
            "<bookmark mark='b'/> Its center doesn't sit still: it trembles, at a frequency of about two m c squared over "
            "h-bar, around the center of its positive-energy part, which doesn't move at all. Schrödinger called this "
            "Zitterbewegung, trembling motion. <bookmark mark='c'/> It isn't a point particle jittering; it's the "
            "interference between the two energy branches, beating at their energy difference. For a free electron it "
            "would be far too small and fast to see, but it has been simulated with trapped ions."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(top), Create(bot), FadeIn(w0), FadeIn(w1), FadeIn(l0), FadeIn(l1), FadeIn(rs), FadeIn(cap), FadeIn(wheel))
            vo.wait_until("b")
            self.add(cm)
            self.play(Create(frm), FadeIn(tks), FadeIn(tl), FadeIn(yl), Create(cp), FadeIn(leg))
            self.play(t.animate.set_value(len(ts) - 1), run_time=max(6, vo.mark_time("c") - vo.elapsed()), rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(expl))
        for m in (w0, w1, cm):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
