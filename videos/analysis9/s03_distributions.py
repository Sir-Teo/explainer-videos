from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis9.common import area_under, load, plain_axes, polyline


def phi_pv(x):
    return np.exp(-(x - 0.5) ** 2) * (1 + 0.3 * x)


class Distributions(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.pv()
        self.comb()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"Distributions", r"What is a generalized function?", lit=(1945,), part=9)
        with self.voiceover("Chapter two: distributions, the continuous linear functionals on test functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def definition(self):
        d = load("pv")
        dphi0 = float(d["dphi0"])
        ax = plain_axes([-2.5, 2.5, 1], [-0.4, 1.4, 0.5], 6.0, 2.6).move_to([-3.2, 0.6, 0])
        x = np.linspace(-2.5, 2.5, 2001)
        ph = phi_pv(x)
        g = polyline(ax, x, ph, color=C.TEST_FN, stroke_width=3.5)
        f = 0.6 + 0.3 * np.sign(x - 0.8)
        gf = polyline(ax, x, f, color=C.FUNC, stroke_width=2.5)
        prod = area_under(ax, x, f * ph, C.FUNC, 0.25)
        tang = Line(ax.c2p(-0.6, phi_pv(np.array([0.0]))[0] - 0.6 * dphi0), ax.c2p(0.6, phi_pv(np.array([0.0]))[0] + 0.6 * dphi0),
                    color=C.DISTRIBUTION, stroke_width=3)
        dot0 = Dot(ax.c2p(0, phi_pv(np.array([0.0]))[0]), radius=0.08, color=C.DISTRIBUTION)
        l_phi = MathTex(r"\varphi", font_size=28, color=C.TEST_FN).next_to(ax.c2p(1.5, phi_pv(np.array([1.5]))[0]), UR,
                                                                         buff=0.05)
        rows = VGroup(
            label(r"\textbf{FA 6.7} \ a \emph{distribution} is a continuous linear functional on $\mathcal D(\Omega)$",
                  font_size=24),
            MathTex(r"\text{a function } f: \quad \langle f, \varphi\rangle = \int f\varphi", font_size=28, color=C.FUNC),
            MathTex(rf"\delta: \quad \langle \delta, \varphi\rangle = \varphi(0) = {phi_pv(np.array([0.0]))[0]:.4f}",
                    font_size=28, color=C.DISTRIBUTION),
            MathTex(rf"\delta': \quad \langle \delta', \varphi\rangle = -\varphi'(0) = {-dphi0:.4f}", font_size=28,
                    color=C.DISTRIBUTION),
            label(r"\textbf{FA 6.8} \ on each compact $K$: \ $|\langle T, \varphi\rangle| \le C\sum_{|\alpha| \le N} "
                  r"\sup|\partial^\alpha\varphi|$", font_size=22),
            label(r"the least such $N$ is the \emph{order}: \ $f$ and $\delta$ have order $0$, \ $\delta'$ order $1$",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0.0, -2.0, 0])
        for r_ in rows:
            if r_.width > 12.6:
                r_.width = 12.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0.0, -2.0, 0])
        rows[0].to_edge(UP, buff=0.3)
        rest = VGroup(*rows[1:]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.4, 0.2, 0])
        for r_ in rest:
            if r_.width > 6.6:
                r_.width = 6.6
        rest.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A distribution is a continuous linear functional on the test functions. "
            "<bookmark mark='b'/> Every locally integrable function is one: it acts by integrating against phi. "
            "<bookmark mark='c'/> Delta is one: it reads off the value at zero. <bookmark mark='d'/> So is delta "
            "prime, which reads off minus the slope at zero. <bookmark mark='e'/> Continuity means: on each compact "
            "set, the action is bounded by finitely many sup norms of derivatives. The number of derivatives needed "
            "is the order: zero for functions and delta, one for delta prime."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ax), Create(g), FadeIn(l_phi))
            vo.wait_until("b")
            self.play(Create(gf), FadeIn(prod), FadeIn(rest[0]))
            vo.wait_until("c")
            self.play(FadeIn(dot0, scale=2), FadeIn(rest[1]))
            vo.wait_until("d")
            self.play(Create(tang), FadeIn(rest[2]))
            vo.wait_until("e")
            self.play(FadeIn(rest[3:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pv(self):
        d = load("pv")
        eps, vals, lim = d["eps"], d["vals"], float(d["lim"])
        ax = plain_axes([-2.5, 2.5, 1], [-6, 6, 2], 6.4, 4.0).move_to([-3.1, -0.6, 0])
        x1 = np.linspace(0.02, 2.5, 1500)
        x2 = -x1[::-1]
        g = VGroup(runs(ax, x2, phi_pv(x2) / x2, C.DISTRIBUTION, 3),  # both branches cut where they leave the axes
                   runs(ax, x1, phi_pv(x1) / x1, C.DISTRIBUTION, 3))
        eT = ValueTracker(0.5)

        def shade():
            e = eT.get_value()
            xr = np.linspace(e, 2.5, 600)
            xl = -xr[::-1]
            return VGroup(area_under(ax, xr, np.minimum(phi_pv(xr) / xr, 6), C.MEASURE, 0.35),
                          area_under(ax, xl, np.maximum(phi_pv(xl) / xl, -6), C.SEQ, 0.35))

        sh = always_redraw(shade)
        f_l = MathTex(r"\frac{\varphi(x)}{x}", font_size=30, color=C.DISTRIBUTION).next_to(ax.c2p(0.4, 4.5), RIGHT, buff=0.1)
        tab = VGroup(MathTex(r"\varepsilon", r"\quad \int_{|x| > \varepsilon} \frac{\varphi(x)}{x}\,dx", font_size=24,
                             color=GREY_A))
        for e, v in zip(eps, vals):
            tab.add(MathTex(sci(float(e), 0), rf"\quad {v:.6f}", font_size=24))
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, 0.8, 0])
        regrid(tab)
        rows = VGroup(
            MathTex(rf"\to \int_0^\infty \frac{{\varphi(x) - \varphi(-x)}}{{x}}\,dx = {lim:.6f}", font_size=26, color=C.EPS),
            label(r"each half diverges like $\log\varepsilon$; \ the halves cancel", font_size=22),
            label(r"order $1$, \ and no measure gives it", font_size=22, color=C.PATHOLOGY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(tab, DOWN, buff=0.25)
        assert abs(vals[-1] - lim) < 1e-5
        head = label(r"The principal value of $1/x$: \ cancel the two infinities", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> A subtler distribution: one over x. It isn't integrable near zero, so integrating "
            "it against phi makes no sense. <bookmark mark='b'/> But cut out a symmetric window around zero. The "
            "right half pulls up, the left half pulls down, each by about the log of epsilon, and they cancel. "
            "<bookmark mark='c'/> As the window shrinks, the truncated integrals converge: here to 2.036324. "
            "<bookmark mark='d'/> That limit is the principal value of one over x: a distribution of order one, "
            "which no function or measure gives."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), Create(g), FadeIn(f_l))
            vo.wait_until("b")
            self.play(FadeIn(sh))
            self.play(eT.animate.set_value(0.05), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(rows))
        sh.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def comb(self):
        ax = plain_axes([-14, 14, 2 * math.pi], [-0.3, 1.6, 0.5], 12.0, 2.6).move_to([0, 0.3, 0])
        ks = np.arange(-2, 3)
        spikes = VGroup(*[Arrow(ax.c2p(2 * math.pi * k, 0), ax.c2p(2 * math.pi * k, 1.5), buff=0, color=C.DISTRIBUTION,
                                stroke_width=5, tip_length=0.2) for k in ks])
        lab = VGroup(*[MathTex(rf"{2 * k}\pi" if k not in (0, 1, -1) else ("0" if k == 0 else rf"{'-' if k < 0 else ''}2\pi"),
                               font_size=22).next_to(ax.c2p(2 * math.pi * k, 0), DOWN, buff=0.12) for k in ks])
        x = np.linspace(-14, 14, 3000)
        ph = np.exp(-((x - 1.5) ** 2) / 30)
        gp = polyline(ax, x, ph, color=C.TEST_FN, stroke_width=3)
        val = float(np.sum(np.exp(-((2 * math.pi * np.arange(-50, 51) - 1.5) ** 2) / 30)))
        rows = VGroup(
            MathTex(r"\text{the Dirac comb } \ \mathrm{III} = \sum_{k \in \Z} \delta_{2\pi k}: \quad \langle \mathrm{III}, \varphi\rangle "
                    r"= \sum_k \varphi(2\pi k)", font_size=30),
            MathTex(rf"\varphi = e^{{-(x - 1.5)^2/30}}: \ \langle \mathrm{{III}}, \varphi\rangle = {val:.6f}", font_size=28,
                    color=C.TEST_FN),
            label(r"a periodic train of spikes: \ it will be the derivative of the sawtooth, \ and its own Fourier "
                  r"transform", font_size=24, color=C.EPS),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        head = label(r"A distribution that lives on a lattice", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> One more, which will keep coming back: the Dirac comb, a delta at every multiple of "
            "two pi. <bookmark mark='b'/> It acts on a test function by summing its values on the lattice. "
            "<bookmark mark='c'/> It's the derivative of the sawtooth, up to a constant, and it is its own Fourier "
            "transform, as we'll see."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), LaggedStart(*[GrowArrow(s_) for s_ in spikes], lag_ratio=0.15), FadeIn(lab))
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(gp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()
