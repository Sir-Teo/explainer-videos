from __future__ import annotations

import numpy as np
from scipy.interpolate import RegularGridInterpolator

from explainer.quant import *  # noqa: F403
from explainer.quant.house import sim
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, real_data

DGS10_DEC2020 = 0.0093  # FRED DGS10, 31 December 2020
ZMAX = 40.0


class PDE(VoiceoverScene, ThreeDScene):
    def construct(self):
        fp = load("fp_surface")
        fk = load("fk_check")
        r = load("rates")
        self.card()
        self.surface(fp, r)
        self.forward()
        self.backward(fk, r)
        self.dynkin(fk)

    def card(self):
        c = chapter_card(7, r"From paths to PDEs: Fokker--Planck and Feynman--Kac", r"What equation does a cloud of "
                         r"paths obey?", part=PART)
        with self.voiceover(
            'Chapter seven. From paths to partial differential equations: Fokker-Planck and Feynman-Kac.'
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def surface(self, fp, r):
        ts, xs = np.asarray(fp["ts"]), np.asarray(fp["xs"])
        ax = ThreeDAxes(x_range=[0, 10, 2], y_range=[0, 0.12, 0.04], z_range=[0, ZMAX, 10], x_length=6.6, y_length=5.0,
                        z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def surf_of(P):
            f = RegularGridInterpolator((ts, xs), np.minimum(np.asarray(P), ZMAX), bounds_error=False, fill_value=None)
            return loss_surface(ax, lambda u, v: float(f([[u, v]])[0]), [ts[0], ts[-1]], [xs[0], xs[-1]],
                                resolution=(24, 30), z_lo=0, z_hi=ZMAX * 0.8, opacity=0.8)
        s_fit, s_two = surf_of(fp["p_fit"]), surf_of(fp["p_two"])
        k, th, s = r["cir"]["kappa"], r["cir"]["theta"], r["cir"]["sigma"]
        P = sim.cir_exact(fp["x0"], k, th, s, 10.0, 120, 40, seed=70)
        tt = np.linspace(0, 10, 121)
        fan = VGroup(*[VMobject(stroke_width=1.2, stroke_color=BM, stroke_opacity=0.5).set_points_as_corners(
            [ax.c2p(a, min(b, 0.12), 0) for a, b in zip(tt, row)]) for row in P])
        hint = VGroup(label(r"floor: CIR paths from $x_0 = 4\%$ (time, rate)", font_size=21, color=BM),
                      label(r"height: their density $p(t, x)$", font_size=21, color=GREY_A),
                      MathTex(rf"\nu = 2\kappa\theta/\sigma^2 = {fp['nu_fit']:.2f}", font_size=28, color=JUMP)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.35)
        nu2 = MathTex(r"\nu = 2", font_size=28, color=DRIFT).move_to(hint[2], aligned_edge=LEFT)
        cap = label(r"the edge at $x = 0$: a wall when $\nu < 1$, a pinch when $\nu \ge 1$", font_size=22,
                    color=GREY_A).to_corner(DL, buff=0.35)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, nu2, cap)
        self.remove(hint, nu2, cap)
        with self.voiceover(
            'One path is random; its population distribution follows a deterministic equation. A finite simulated'
            ' cloud still has sampling noise. Here are forty CIR paths on the floor, time running away from us, '
            "all starting at four percent. <bookmark mark='a'/> Above them, their density: a surface that rises "
            'from a spike and spreads as time passes. It obeys the Fokker-Planck equation, derived next. '
            "<bookmark mark='b'/> Look at the edge where the rate is zero. With the fitted parameters nu is below"
            " one, and probability piles up against the floor: a wall. <bookmark mark='c'/> Lower the volatility "
            'until nu equals two, and the same edge pinches to zero. The density near zero scales as the rate to '
            'the power nu minus one; zero is inaccessible already at nu at least one. Nu equal to two is a clear '
            "example on that inaccessible side, not the threshold. <bookmark mark='d'/> Looking down the time "
            'axis, each slice is the histogram of the paths stopped at that moment.'
        ) as vo:
            self.play(Create(ax), FadeIn(hint[:2]), LaggedStart(*[Create(p) for p in fan], lag_ratio=0.05, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(s_fit), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(hint[2]), FadeIn(cap))
            self.move_camera(theta=-130 * DEGREES, phi=72 * DEGREES, run_time=3)
            vo.wait_until("c")
            self.play(ReplacementTransform(s_fit, s_two), FadeTransform(hint[2], nu2), run_time=2.5)
            vo.wait_until("d")
            self.move_camera(theta=-90 * DEGREES, phi=80 * DEGREES, run_time=max(vo.remaining(0.5) - 0.5, 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, s_two, fan)), FadeOut(hint[:2]), FadeOut(nu2), FadeOut(cap)],
                         run_time=1.0)
        self.clear_scene(run_time=0.2)

    def forward(self):
        rows = [cmath(r"\mathcal{L}\varphi", r"=", r"a\,\varphi' + \tfrac12 b^2 \varphi''", font_size=36,
                      colors={r"a\,\varphi' + \tfrac12 b^2 \varphi''": ITO}),
                cmath(r"\frac{d}{dt}\mathbb{E}\,\varphi(X_t)", r"=", r"\mathbb{E}\big[\mathcal{L}\varphi(X_t)\big]", font_size=36),
                cmath(r"\int \varphi\,\partial_t p\,dx", r"=", r"\int (\mathcal{L}\varphi)\,p\,dx = \int \varphi\,\mathcal{L}^* p\,dx",
                      font_size=36),
                cmath(r"\partial_t p", r"=", r"-\partial_x (a\,p) + \tfrac12 \partial_{xx}(b^2 p)", font_size=38,
                      colors={r"-\partial_x (a\,p) + \tfrac12 \partial_{xx}(b^2 p)": STRAT})]
        whys = [why(r"the generator of $dX = a(X)\,dt + b(X)\,dW$"),
                why(r"It\^o's lemma for $\varphi(X_t)$; the $dW$ term has mean zero (Dynkin's formula)"),
                why(r"write the expectation with the density; integrate by parts twice"),
                why(r"true for every test function $\varphi$: the Fokker--Planck (forward Kolmogorov) equation")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.8, buff=0.65, edge=6.9)
        with self.voiceover(
            'The derivation starts from the generator: for a smooth test function phi, the drift times its slope,'
            " plus half the squared volatility times its curvature. <bookmark mark='a'/> By Itô's lemma, phi of X"
            ' changes by the generator times d t plus a Brownian term with mean zero, so the expected value of '
            "phi of X changes at the rate of the expected generator: Dynkin's formula in differential form. "
            "<bookmark mark='b'/> Write that expectation as an integral against the density p, and integrate by "
            'parts twice, once for the slope and twice for the curvature, to move every derivative from phi onto '
            'a times p and onto b squared times p. The boundary terms vanish because phi has compact support. '
            "<bookmark mark='c'/> The identity holds for every test function, so the density itself obeys the "
            'Fokker-Planck equation: the time derivative of p equals minus the slope of the drift flux plus half '
            'the curvature of the variance flux. It is carried forward by the adjoint of the generator.'
        ) as vo:
            step(0, run_time=0.4)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def backward(self, fk, r):
        rows = [cmath(r"M_s", r"=", r"e^{-\int_t^s r_u\,du}\,u(s, X_s)", font_size=32),
                cmath(r"dM_s", r"=", r"e^{-\int_t^s r}\big(u_s + \mathcal{L}u - r\,u\big)\,ds + e^{-\int_t^s r}\,b\,u_x\,dW_s",
                      font_size=30, colors={r"\big(u_s + \mathcal{L}u - r\,u\big)": JUMP}),
                cmath(r"u(t, x)", r"=", r"\mathbb{E}\big[M_T \mid X_t = x\big] = \mathbb{E}\Big[e^{-\int_t^T r\,du}\,g(X_T) "
                      r"\,\Big|\, X_t = x\Big]", font_size=30, colors={r"u(t, x)": ITO}),
                cmath(r"P(t, T)", r"=", r"e^{A(\tau) - B(\tau)\,r_t},\quad B' = 1 - \kappa B,\quad "
                      r"A' = -\kappa\theta B + \tfrac12\sigma^2 B^2", font_size=30)]
        whys = [why(r"the discounted value along a path", 20),
                why(r"the lemma and the product rule", 20),
                why(r"if $u_t + \mathcal{L}u - r u = 0$ and $u(T, \cdot) = g$, the drift vanishes: $M$ is a martingale "
                    r"(Feynman 1948, Kac 1949)", 20),
                why(r"Vasicek: try the exponential-affine form; match the coefficients of $r$ and of 1", 20)]
        step = ladder(self, rows, whys, keep=4, top=3.45, x=-2.2, buff=0.3, edge=6.9)
        g = axes([0, 30], [0, 0.03], x_length=4.6, y_length=2.2, xlabel=r"maturity (years)", ylabel=r"Vasicek yield",
                 xticks=[0, 10, 20, 30], yticks=[0, 0.01, 0.02, 0.03], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=15).to_corner(DR, buff=0.2)  # below the last ladder row
        ax = g.ax
        line = curve(ax, fk["taus"], fk["curve"], ITO, stroke_width=3)
        dot = Dot(ax.c2p(10, DGS10_DEC2020), radius=0.07, color=JUMP)
        dl = label(r"actual, 31 Dec.\ 2020", font_size=16, color=JUMP).next_to(dot, DOWN, buff=0.08)
        res = VGroup(
            MathTex(rf"\text{{10-year bond, Monte Carlo: }} {fk['mc']:.4f} \pm {fk['mc_se']:.4f}", font_size=26, color=ITO),
            MathTex(rf"\text{{closed form: }} {fk['closed']:.4f}", font_size=26, color=ITO),
            label(r"20{,}000 exact paths, daily steps, trapezoid $\int r$", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.35)
        within = abs(fk["mc"] - fk["closed"]) < 2 * fk["mc_se"]
        verdict = ("within two standard errors" if within else "a little more than two standard errors apart")
        with self.voiceover(
            f'Now backwards. Follow the discounted value of a function u along a path. <bookmark '
            f"mark='a'/> Its drift is u's time derivative plus the generator minus the rate. <bookmark "
            f"mark='b'/> If u solves that equation, with the payoff as final condition, with the "
            f'regularity and integrability that make the stochastic integral a true martingale, today’s '
            f'value is the expected discounted payoff: the Feynman-Kac formula, from 1949. <bookmark '
            f"mark='c'/> For Vasicek, an exponential-affine guess turns it into two ordinary "
            f"differential equations. <bookmark mark='d'/> Twenty thousand rate paths price a ten-year bond at "
            f"{fk['mc']:.4f}; the formula says {fk['closed']:.4f}: {verdict}"
            f". <bookmark mark='e'/> But from December 2020's bill rate the model's ten-year yield is "
            f"{100 * fk['closed_yield']:.2f}"
            f' percent, against an actual 0.93: using historical parameters as pricing parameters '
            f'amounts to an extra zero-risk-premium assumption, and this curve misses the observed '
            f'yield. Part nineteen specifies the pricing measure and calibrates to the curve.'
        ) as vo:
            step(0, run_time=0.4)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(res))
            vo.wait_until("e")
            self.play(FadeIn(g), Create(line), FadeIn(dot), FadeIn(dl))
        self.wait(0.4)
        self.clear_scene()

    def dynkin(self, fk):
        rows = [cmath(r"\mathbb{E}\,W_{\tau\wedge t}^2", r"=", r"\mathbb{E}(\tau\wedge t)\le4", font_size=36),
                cmath(r"\mathbb{E}\,W_\tau^2", r"=", r"\mathbb{E}\,\tau", font_size=36),
                cmath(r"\mathbb{E}\,\tau", r"=", r"b^2\,\tfrac{a}{a+b} + a^2\,\tfrac{b}{a+b} = ab", font_size=36,
                      colors={r"b^2\,\tfrac{a}{a+b} + a^2\,\tfrac{b}{a+b} = ab": ITO})]
        whys = [why(r"Dynkin at a bounded stop; bounded positions give $\mathbb E\tau<\infty$ by monotone convergence"),
                why(r"$f = x^2$ for Brownian motion: $\mathcal{L}f = 1$"),
                why(r"the exit probabilities from $(-a, b)$ are $\tfrac{a}{a+b}$ (up) and $\tfrac{b}{a+b}$ (down)")]
        step = ladder(self, rows, whys, keep=3, top=1.6, x=-1.2, buff=0.6, edge=6.9)
        pc, ans = pause(r"Brownian motion from 0 exits $(-1, 2)$. The expected exit time?",
                        rf"$ab = 2$. Simulated: {fk['dynkin']:.3f} $\pm$ {fk['dynkin_se']:.3f} (20{{,}}000 paths, "
                        rf"$dt = 10^{{-4}}$).", width=6.2, font_size=22)
        pc.to_edge(UP, buff=0.35)
        ans.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f'A pause: Brownian motion starts at zero. How long, on average, until it leaves the '
            f"interval from minus one to two? <bookmark mark='a'/> First stop at the exit time or a "
            f'fixed horizon, whichever comes first. Dynkin with f equal to x squared gives an expected '
            f'stopped time bounded by four. Monotone convergence gives a finite expected exit time; '
            f"bounded stopped positions then justify passing to the actual exit. <bookmark mark='b'/> "
            f'The exit point is two with probability one third, so the time is a times b: two. <bookmark'
            f" mark='c'/> Simulated: {fk['dynkin']:.3f}"
            f', the small excess being the overshoot of a discrete path. Expectations depend on the '
            f'probabilities. Next: how to change them, by re-weighting paths.'
        ) as vo:
            self.play(FadeIn(pc))
            vo.wait_until("a")
            step(0)
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
