from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.stochastic.common import (boxed, density, gauss_pdf, hist_shape, label, load, mtex, note, num, part_card,
                                      pdf_curve, polyline)
from videos.stochastic.compute import OU_SIGMA, OU_THETA, OU_X0


class SDEs(VoiceoverScene):
    def construct(self):
        self.card()
        self.meaning()
        self.euler_maruyama()
        self.ou_paths()
        self.ou_solve()
        self.ou_live()

    def card(self):
        c = part_card(4, r"Equations of noise", r"SDEs, and the PDEs hiding behind them")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.6)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def meaning(self):
        sde = MathTex(r"dX_t", r"=", r"\mu(X_t, t)\,dt", r"+", r"\sigma(X_t, t)\,dW_t", font_size=50).move_to(UP * 1.6)
        sde[2].set_color(C.DRIFT)
        sde[4].set_color(C.BROWNIAN)
        means = MathTex(r"X_t", r"=", r"X_0", r"+", r"\int_0^t \mu(X_s, s)\,ds", r"+", r"\int_0^t \sigma(X_s, s)\,dW_s",
                        font_size=42).next_to(sde, DOWN, buff=0.8)
        means[4].set_color(C.DRIFT)
        means[6].set_color(C.BROWNIAN)
        sh = label(r"shorthand for", font_size=26, color=GREY_B).next_to(means, UP, buff=0.2).shift(LEFT * 3.5)
        b1 = Brace(sde[2], DOWN, buff=0.1, color=C.DRIFT)
        b1l = label(r"drift: a steady push", font_size=26, color=C.DRIFT).next_to(b1, DOWN, buff=0.05)
        b2 = Brace(sde[4], DOWN, buff=0.1, color=C.BROWNIAN)
        b2l = label(r"diffusion: random kicks", font_size=26, color=C.BROWNIAN).next_to(b2, DOWN, buff=0.05)
        with self.voiceover(
            "With the integral and Itô's lemma in hand, we can finally write down noisy differential equations, and "
            "solve them. <bookmark mark='s'/> A stochastic differential equation says that over each instant, X changes "
            "by a drift, <bookmark mark='d'/> a steady push that depends on where X is, <bookmark mark='k'/> plus a "
            "random kick, whose size can also depend on where X is."
        ) as vo:
            self.play(Write(sde), run_time=2)
            vo.wait_until("d")
            self.play(GrowFromCenter(b1), FadeIn(b1l))
            vo.wait_until("k")
            self.play(GrowFromCenter(b2), FadeIn(b2l))
        with self.voiceover(
            "Remember, it's shorthand <bookmark mark='m'/> for an integral equation: X at time t is where it started, "
            "plus the accumulated drift, plus an Itô integral of the noise."
        ) as vo:
            self.play(FadeOut(VGroup(b1, b1l, b2, b2l)))
            vo.wait_until("m")
            self.play(FadeIn(sh), Write(means))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def euler_maruyama(self):
        em = MathTex(r"X_{k+1}", r"=", r"X_k", r"+", r"\mu(X_k)\,\Delta t", r"+", r"\sigma(X_k)\,\sqrt{\Delta t}\;Z_k",
                     font_size=42).to_edge(UP, buff=0.45)
        em[4].set_color(C.DRIFT)
        em[6].set_color(C.BROWNIAN)
        zl = label(r"$Z_k$: a fresh standard normal at each step", font_size=24, color=GREY_B).next_to(em, DOWN, buff=0.15)
        name = note(r"the Euler--Maruyama scheme").to_corner(UR, buff=0.3)
        th, sig = OU_THETA, OU_SIGMA
        ax = Axes(x_range=[0, 1.6, 0.4], y_range=[-1.0, 2.6, 1], x_length=10.5, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False}).move_to(DOWN * 1.2)
        dt = 0.2
        rng = np.random.default_rng(4)
        x, t = 2.0, 0.0
        steps = []
        for _ in range(8):
            drift = -th * x * dt
            z = rng.standard_normal()
            steps.append((t, x, drift, sig * np.sqrt(dt) * z))
            x = x + drift + sig * np.sqrt(dt) * z
            t += dt
        path = VGroup()
        anims = []
        for k, (t0, x0, dr, kick) in enumerate(steps):
            p0 = ax.c2p(t0, x0)
            p1 = ax.c2p(t0 + dt, x0 + dr)
            p2 = ax.c2p(t0 + dt, x0 + dr + kick)
            a = Arrow(p0, p1, buff=0, color=C.DRIFT, stroke_width=4, max_tip_length_to_length_ratio=0.15)
            ys = np.linspace(-3, 3, 60) * sig * np.sqrt(dt)
            bell = VMobject(color=C.BROWNIAN, stroke_width=2.5)
            bell.set_points_smoothly([ax.c2p(t0 + dt, x0 + dr + y) + RIGHT * 0.9 * gauss_pdf(y, 0, sig**2 * dt) *
                                      np.sqrt(sig**2 * dt) for y in ys])
            land = Dot(p2, radius=0.06, color=WHITE)
            kick_a = Arrow(p1, p2, buff=0, color=C.BROWNIAN, stroke_width=4, max_tip_length_to_length_ratio=0.2)
            seg = Line(p0, p2, color=WHITE, stroke_width=3)
            anims.append((a, bell, kick_a, land, seg))
        start = Dot(ax.c2p(0, 2.0), radius=0.06, color=WHITE)

        with self.voiceover(
            "And we can simulate them directly. <bookmark mark='e'/> Step forward by delta t: add the drift times delta "
            "t, then add a random kick, the noise amplitude times root delta t times a fresh standard normal. "
            "<bookmark mark='a'/> Here's one step: <bookmark mark='g'/> the green arrow is the drift. "
            "<bookmark mark='b'/> The bell shows where the kick might land you. <bookmark mark='k'/> And a draw from it "
            "picks the next point."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(em), FadeIn(zl), FadeIn(name))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(start))
            a, bell, kick_a, land, seg = anims[0]
            vo.wait_until("g")
            self.play(GrowArrow(a))
            vo.wait_until("b")
            self.play(Create(bell))
            vo.wait_until("k")
            self.play(GrowArrow(kick_a), FadeIn(land))
        with self.voiceover(
            "Repeat, and you've drawn a sample path. This is how nearly every simulation of a stochastic differential "
            "equation works, from molecules to markets."
        ) as vo:
            self.play(FadeOut(VGroup(a, bell, kick_a)), Create(seg))
            for a, bell, kick_a, land, seg in anims[1:]:
                self.play(GrowArrow(a), FadeIn(bell), run_time=0.35)
                self.play(GrowArrow(kick_a), FadeIn(land), run_time=0.3)
                self.play(FadeOut(VGroup(a, bell, kick_a)), Create(seg), run_time=0.25)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ou_axes(self):
        ax = Axes(x_range=[0, 5, 1], y_range=[-2.2, 2.6, 1], x_length=8.6, y_length=5.0, tips=False,
                  axis_config={"stroke_color": GREY_B, "include_ticks": False})
        return ax

    def ou_paths(self):
        d = load("ou")
        F, ts = d["frames"], d["ts"]
        th, sig = OU_THETA, OU_SIGMA
        sde = MathTex(r"dX", r"=", r"-\theta X\,dt", r"+", r"\sigma\,dW", font_size=46).to_edge(UP, buff=0.4)
        sde[2].set_color(C.DRIFT)
        sde[4].set_color(C.BROWNIAN)
        name = label(r"the Ornstein--Uhlenbeck process", font_size=28, color=GREY_A).next_to(sde, DOWN, buff=0.12)
        params = MathTex(rf"\theta = {th:g},\;\; \sigma = {sig:g},\;\; X_0 = {OU_X0:g}", font_size=28, color=GREY_A)
        params.to_corner(UR, buff=0.45)
        ax = self.ou_axes().move_to(DOWN * 0.7)
        xl = MathTex("t", font_size=28, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        yl = MathTex("X_t", font_size=28).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        field = VGroup()
        for t in np.linspace(0.25, 4.75, 10):
            for x in np.linspace(-2.0, 2.4, 9):
                v = -th * x
                L = 0.22 * v
                if abs(L) < 0.02:
                    continue
                a = Arrow(ax.c2p(t, x), ax.c2p(t, x) + UP * L * 1.0, buff=0, color=C.DRIFT, stroke_width=2.5,
                          max_tip_length_to_length_ratio=0.35).set_opacity(0.55)
                field.add(a)
        paths = VGroup(*[polyline(ax, ts, F[:, i], color=C.BROWNIAN, stroke_width=1.3).set_stroke(opacity=0.45)
                         for i in range(40)])
        band = VGroup(*[DashedLine(ax.c2p(0, s * sig / np.sqrt(2 * th)), ax.c2p(5, s * sig / np.sqrt(2 * th)),
                                   color=C.PDF, stroke_width=2) for s in (1, -1)])
        band_l = MathTex(r"\pm\frac{\sigma}{\sqrt{2\theta}}", font_size=28, color=C.PDF).next_to(band[0], RIGHT, buff=0.1)
        with self.voiceover(
            "Here's the most important example after Brownian motion itself. <bookmark mark='s'/> The drift is minus "
            "theta X: always pulling back toward zero, harder the farther away you are. <bookmark mark='f'/> The green "
            "arrows show that pull. It's the Ornstein–Uhlenbeck process, invented in 1930 as the velocity of a Brownian "
            "particle slowed by friction. Today it also models interest rates, and anything that wanders but is pulled "
            "back to a mean."
        ) as vo:
            vo.wait_until("s")
            self.play(Write(sde), FadeIn(name), FadeIn(params))
            vo.wait_until("f")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(LaggedStart(*[GrowArrow(a) for a in field], lag_ratio=0.01), run_time=1.5)
        with self.voiceover(
            "Start forty particles at two, and let them go. <bookmark mark='p'/> The drift pulls them in, and the noise "
            "keeps them jittering. <bookmark mark='b'/> They settle into a band around zero, where the pull and the kicks "
            "balance."
        ) as vo:
            vo.wait_until("p")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.03), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(*[Create(b) for b in band], FadeIn(band_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ou_solve(self):
        l0 = MathTex(r"f(t, x) = e^{\theta t} x:", r"\quad f_t = \theta e^{\theta t} x,\quad f_x = e^{\theta t},\quad",
                     r"f_{xx} = 0", font_size=34).to_edge(UP, buff=0.45)
        l0[2].set_color(C.QV)
        l1 = MathTex(r"d\big(e^{\theta t} X_t\big)", r"=", r"\theta e^{\theta t} X\,dt", r"+",
                     r"e^{\theta t}\big(-\theta X\,dt + \sigma\,dW\big)", font_size=40)
        l2 = MathTex(r"d\big(e^{\theta t} X_t\big)", r"=", r"\sigma e^{\theta t}\,dW_t", font_size=40)
        l2[2].set_color(C.BROWNIAN)
        l3 = MathTex(r"X_t", r"=", r"e^{-\theta t} X_0", r"+", r"\sigma \int_0^t e^{-\theta(t-s)}\,dW_s", font_size=42)
        l3[2].set_color(C.DRIFT)
        l3[4].set_color(C.BROWNIAN)
        col = VGroup(l1, l2, l3).arrange(DOWN, buff=0.4).next_to(l0, DOWN, buff=0.5)
        for m in (l2, l3):
            m.shift((l1[1].get_center()[0] - m[1].get_center()[0]) * RIGHT)
        mean = MathTex(r"\mathbb E[X_t]", r"=", r"e^{-\theta t} X_0", font_size=38)
        mean[2].set_color(C.DRIFT)
        var = MathTex(r"\operatorname{Var}[X_t]", r"=", r"\sigma^2 \int_0^t e^{-2\theta(t-s)}\,ds", r"=",
                      r"\frac{\sigma^2}{2\theta}\big(1 - e^{-2\theta t}\big)", font_size=38)
        var[4].set_color(C.PDF)
        mv = VGroup(mean, var).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(col, DOWN, buff=0.55)
        mn = label(r"the It\^o integral has mean zero", font_size=24, color=GREY_B).next_to(mean, RIGHT, buff=0.5)
        vn = label(r"It\^o isometry", font_size=24, color=GREY_B).next_to(var[2], DOWN, buff=0.12)
        lim = MathTex(r"\xrightarrow{\;t\to\infty\;}\;\mathcal N\Big(0,\ \frac{\sigma^2}{2\theta}\Big)", font_size=36,
                      color=C.PDF).next_to(var, DOWN, buff=0.3).align_to(var, RIGHT)
        with self.voiceover(
            "And we can solve it exactly, with a trick from ordinary differential equations: an integrating factor. "
            "<bookmark mark='f'/> Look at e to the theta t, times X. Its time derivative is theta times itself, its slope "
            "in x is e to the theta t, and its curvature in x is zero: it's linear in x. <bookmark mark='a'/> So Itô's "
            "lemma gives the ordinary chain rule, with no correction, <bookmark mark='b'/> and the drift terms cancel "
            "exactly. Only the noise is left."
        ) as vo:
            head = label(r"solving it: an integrating factor", font_size=34, color=GREY_A).move_to(UP * 0.5)
            self.play(FadeIn(head))
            vo.wait_until("f")
            self.play(FadeOut(head), Write(l0))
            vo.wait_until("a")
            self.play(Write(l1))
            vo.wait_until("b")
            self.play(Write(l2))
        with self.voiceover(
            "Integrate, and multiply back: <bookmark mark='x'/> X at time t is the starting point, decayed by e to the "
            "minus theta t, plus a weighted Itô integral of the noise, where old kicks are forgotten exponentially. "
            "<bookmark mark='m'/> The Itô integral has mean zero, so the mean just decays. <bookmark mark='v'/> And the "
            "isometry gives the variance as an ordinary integral: sigma squared over two theta, times one minus e to the "
            "minus two theta t. <bookmark mark='l'/> As time goes on, every particle forgets where it started, and the "
            "distribution settles to a bell curve with variance sigma squared over two theta."
        ) as vo:
            vo.wait_until("x")
            self.play(Write(l3))
            vo.wait_until("m")
            self.play(Write(mean), FadeIn(mn))
            vo.wait_until("v")
            self.play(Write(var), FadeIn(vn))
            vo.wait_until("l")
            self.play(Write(lim))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ou_live(self):
        d = load("ou")
        F, ts, mth, vth = d["frames"], d["ts"], d["mean"], d["var"]
        th, sig = OU_THETA, OU_SIGMA
        ax = self.ou_axes().scale(0.92).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        xl = MathTex("t", font_size=28, color=C.CLOCK).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        hax = Axes(x_range=[0, 1.6, 0.5], y_range=[-2.2, 2.6, 1], x_length=3.2, y_length=ax.y_length, tips=False,
                   axis_config={"stroke_color": GREY_C, "include_ticks": False}).next_to(ax, RIGHT, buff=0.35)
        hax.x_axis.set_opacity(0)
        k = ValueTracker(0.0)
        edges = np.linspace(-2.2, 2.6, 49)
        ys = np.linspace(-2.2, 2.6, 240)
        n_frames = len(ts) - 1
        paths = VGroup(*[polyline(ax, ts, F[:, i], color=C.BROWNIAN, stroke_width=1.1).set_stroke(opacity=0.3)
                         for i in range(60)])

        def now_line():
            t = ts[int(round(k.get_value()))]
            return DashedLine(ax.c2p(t, -2.2), ax.c2p(t, 2.6), color=WHITE, stroke_width=2)

        def hist():
            j = int(round(k.get_value()))
            return hist_shape(hax, edges, np.minimum(density(F[j], edges), 1.6), sideways=True, color=C.PDF)

        def theory():
            j = max(1, int(round(k.get_value())))
            return pdf_curve(hax, ys, np.minimum(gauss_pdf(ys, mth[j], vth[j]), 1.6), sideways=True, color=WHITE,
                             stroke_width=2.5)

        tval = DecimalNumber(0, num_decimal_places=2, font_size=30)
        tval.add_updater(lambda m: m.set_value(ts[int(round(k.get_value()))]))
        ro = VGroup(MathTex("t =", font_size=30), tval).arrange(RIGHT, buff=0.12).next_to(hax, UP, buff=0.15)

        nl, hs, tc = always_redraw(now_line), always_redraw(hist), always_redraw(theory)
        leg = VGroup(label(r"3{,}000 simulated particles", font_size=24, color=C.PDF),
                     label(r"theory: $\mathcal N\big(e^{-\theta t}X_0,\ \tfrac{\sigma^2}{2\theta}(1 - e^{-2\theta t})\big)$",
                           font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.35)
        checks = []
        for t_ in (0.25, 1.0, 4.0):
            j = int(round(t_ / (ts[1] - ts[0])))
            checks.append((t_, F[j].mean(), F[j].var(), mth[j], vth[j]))
        assert all(abs(c[1] - c[3]) < 0.045 and abs(c[2] / c[4] - 1) < 0.08 for c in checks), checks
        with self.voiceover(
            "Here's the prediction against three thousand simulated particles. <bookmark mark='g'/> As time runs, the "
            "histogram of where they are slides toward zero and widens, and the theoretical bell curve tracks it the "
            "whole way, <bookmark mark='e'/> until it locks into the stationary bell curve, with variance one half."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(paths), Create(hax.y_axis), FadeIn(leg))
            self.add(nl, hs, tc, ro)
            vo.wait_until("g")
            self.play(k.animate.set_value(n_frames * 0.6), run_time=vo.until("e"), rate_func=linear)
            self.play(k.animate.set_value(n_frames), run_time=vo.remaining() + 1.0, rate_func=linear)
        with self.voiceover(
            "Notice what changed in this picture. We stopped following individual paths, and started watching the "
            "density of the whole cloud evolve, smoothly and deterministically. That density obeys a partial "
            "differential equation of its own, and Itô's lemma is how we find it."
        ):
            self.play(paths.animate.set_stroke(opacity=0.12))
        self.wait(0.3)
        self.clear_scene()
