from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause, real_data


class MeanReversion(VoiceoverScene):
    def construct(self):
        r = load("rates")
        lab = load("ou_lab")
        m = load("cir_mle")
        self.card()
        self.lab(r, lab)
        self.solve(r)
        self.cir(r)
        self.replay(r, m)

    def card(self):
        c = chapter_card(6, r"Mean reversion: solved and fitted", r"What pulls an interest rate back, and how fast?",
                         lit=(1977,), part=PART)
        with self.voiceover("Chapter six. Mean reversion: the Ornstein-Uhlenbeck and Cox-Ingersoll-Ross processes, "
                            "solved exactly and fitted to Treasury bills."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def lab(self, r, lab):
        t, x = np.asarray(r["t"]), np.asarray(r["r"])
        v = r["vasicek"]
        g = axes([1954, 2021], [-0.06, 0.18], x_length=6.4, y_length=3.3, ylabel=r"3-month Treasury bill rate",
                 xticks=[1960, 1980, 2000, 2020], xfmt=lambda u: f"{int(u)}", yticks=[-0.04, 0, 0.04, 0.08, 0.12, 0.16],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16).to_corner(DL, buff=0.5)
        ax = g.ax
        real = curve(ax, t, x, BM, stroke_width=2.5)
        zero = DashedLine(ax.c2p(1954, 0), ax.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        P = np.asarray(lab["paths"])
        tt = lab["t0"] + np.linspace(0, lab["years"], P.shape[1])
        fan = path_fan(ax, tt, np.clip(P, -0.06, 0.18), color=ITO, stroke_width=1.0, opacity=0.2)
        side = side_density(ax, P[:, -1], (-0.06, 0.18), bins=24, width=0.9, color=ITO)
        card = lab_card(r"exact Ornstein--Uhlenbeck", [
            "def ou_exact(x0, kappa, theta, sigma, T, n, n_paths, seed=0):",
            "    rng = np.random.default_rng(seed); dt = T / n",
            "    e = np.exp(-kappa * dt)",
            "    sd = sigma * np.sqrt((1 - e**2) / (2 * kappa))",
            "    X = np.empty((n_paths, n + 1)); X[:, 0] = x0",
            "    for k in range(n):",
            "        X[:, k+1] = theta + (X[:, k] - theta)*e + sd*rng.standard_normal(n_paths)",
            "    return X",
        ], source="explainer/quant/house/sim.py", width=7.0, font_size=16).to_corner(UR, buff=0.3)
        outs = [f"kappa={v['kappa']:.3f}  theta={v['theta']:.4f}  sigma={v['sigma']:.4f}   (regression, 1954-2020)",
                f"X_T: mean {lab['mean_T']:.4f}  sd {lab['sd_T']:.4f}",
                f"theory: mean {lab['mean_theory']:.4f}  sd {lab['sd_theory']:.4f}   below zero {100 * lab['frac_neg_T']:.0f}%"]
        src = real_data(r"FRED DTB3, monthly averages, January 1954 -- December 2020", corner=UL)
        with self.voiceover(
            "Interest rates are pulled back. Here is the three-month bill rate since 1954, and Oldřich Vasicek's 1977 "
            "model: the rate drifts toward theta at speed kappa, plus noise, the Ornstein-Uhlenbeck process. "
            "<bookmark mark='a'/> The House simulates it exactly: each month the gap to theta shrinks by e to the "
            "minus kappa d t, and a Gaussian of exactly the right variance is added. <bookmark mark='b'/> Two hundred "
            "paths from the 1954 rate, with a regression's parameters. <bookmark mark='c'/> The fan settles into a "
            f"fixed Gaussian, mean {100 * lab['mean_T']:.1f} percent, spread {100 * lab['sd_T']:.1f}, as theory says, "
            f"with {100 * lab['frac_neg_T']:.0f} percent below zero."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(zero), Create(real), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(real.animate.set_stroke(opacity=0.3), LaggedStart(*[Create(p) for p in fan], lag_ratio=0.01,
                                                                        run_time=4))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in side], lag_ratio=0.05))
            lab_run(self, card, outs, font_size=17)
        self.wait(0.4)
        self.clear_scene()

    def solve(self, r):
        v = r["vasicek"]
        rows = [cmath(r"d\big(e^{\kappa t} X_t\big)", r"=", r"e^{\kappa t}\big(\kappa X_t\,dt + dX_t\big) = \kappa\theta\, e^{\kappa t}\,dt "
                      r"+ \sigma e^{\kappa t}\,dW_t", font_size=32),
                cmath(r"X_t", r"=", r"\theta + (x_0 - \theta)e^{-\kappa t} + \sigma \int_0^t e^{-\kappa(t-s)}\,dW_s",
                      font_size=34, colors={r"\sigma \int_0^t e^{-\kappa(t-s)}\,dW_s": ITO}),
                cmath(r"X_t", r"\sim", r"N\Big(\theta + (x_0 - \theta)e^{-\kappa t},\ \tfrac{\sigma^2}{2\kappa}\big(1 - e^{-2\kappa t}\big)\Big)",
                      font_size=34, colors={r"\tfrac{\sigma^2}{2\kappa}\big(1 - e^{-2\kappa t}\big)": ITO})]
        whys = [why(r"the product rule with an integrating factor; the covariation term is zero, since $e^{\kappa t}$ "
                    r"is smooth"),
                why(r"integrate from 0 to $t$"),
                why(r"a Wiener integral of a deterministic integrand is Gaussian; its variance is the isometry, "
                    r"$\sigma^2\int_0^t e^{-2\kappa(t-s)}ds$")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.6, buff=0.7, edge=6.9)
        pc, ans = pause(r"OU from a rate far above $\theta$. When is it halfway back?",
                        rf"After $\ln 2 / \kappa = {v['half_life']:.1f}$ years: the mean gap decays like "
                        rf"$e^{{-\kappa t}}$.", width=6.4, font_size=22)
        VGroup(pc, ans).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why the recipe is exact. Multiply by e to the kappa t and apply the product rule; the factor is smooth, "
            "so there is no covariation term. <bookmark mark='a'/> Integrate: the long-run level, plus the starting "
            "gap decaying exponentially, plus a stochastic integral of a deterministic function. <bookmark mark='b'/> "
            "That integral is Gaussian, with variance from the isometry, settling at sigma squared over two kappa. "
            "<bookmark mark='c'/> A pause: a rate starts far above theta. When is it halfway back? "
            f"<bookmark mark='d'/> At log two over kappa: about {v['half_life']:.0f} years with the fitted kappa."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    def cir(self, r):
        c = r["cir"]
        t, x = np.asarray(r["t"]), np.asarray(r["r"])
        g = axes([1954, 2021], [-0.01, 0.18], x_length=6.2, y_length=3.8, ylabel=r"rate", xticks=[1960, 1980, 2000, 2020],
                 xfmt=lambda u: f"{int(u)}", yticks=[0, 0.08, 0.16], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        ax = g.ax
        tt = t[0] + np.arange(np.asarray(r["cir_paths"]).shape[1]) / 12
        ci = VGroup(*[curve(ax, tt, np.clip(p, -0.01, 0.18), STRAT, stroke_width=1.6).set_stroke(opacity=0.8)
                      for p in r["cir_paths"]])
        zero = DashedLine(ax.c2p(1954, 0), ax.c2p(2021, 0), color=GREY_C, stroke_width=1.5)
        rows = VGroup(
            MathTex(r"dr = \kappa(\theta - r)\,dt + \sigma\sqrt{r}\,dW", font_size=30, color=STRAT),
            MathTex(r"r_{t+h} = c\,\chi'^2_{d}(\lambda),\quad c = \tfrac{\sigma^2(1 - e^{-\kappa h})}{4\kappa},\quad "
                    r"d = \tfrac{4\kappa\theta}{\sigma^2}", font_size=26),
            label(r"a scaled non-central chi-square: a squared Bessel process, time-changed", font_size=19,
                  color=GREY_A),
            label(r"stationary law: Gamma, shape $2\kappa\theta/\sigma^2$, rate $2\kappa/\sigma^2$", font_size=19,
                  color=GREY_A),
            MathTex(r"0 \text{ unattainable} \iff \nu = \frac{2\kappa\theta}{\sigma^2} \ge 1", font_size=30, color=JUMP),
            label(rf"Feller's test (1951). Regression fit: $\nu = {c['feller']:.2f}$", font_size=20, color=JUMP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Cox, Ingersoll and Ross removed the negative rates in 1985: let the noise shrink with the square root of "
            "the rate. Near zero the noise dies and the pull wins. <bookmark mark='a'/> This process can also be "
            "sampled exactly. Its transition law is a scaled non-central chi-square, because the square-root process "
            "is a squared Bessel process of dimension four kappa theta over sigma squared, run on a different clock "
            "and scaled; its long-run law is a Gamma distribution. <bookmark mark='b'/> Does it touch zero? William "
            "Feller's boundary test, from 1951, says zero is unattainable exactly when two kappa theta over sigma "
            "squared is at least one: equivalently, when the Bessel dimension is at least two, the dimension in which "
            "a Brownian motion never returns to the origin. <bookmark mark='c'/> A regression puts the ratio at "
            f"{c['feller']:.2f}, and the paths kiss the floor, as American bill rates did in 2009 and 2020. But a "
            "regression is not the likelihood."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(p) for p in ci], lag_ratio=0.3, run_time=3), FadeIn(rows[5]))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, r, m):
        curves = np.asarray(m["curves"])
        steps = np.arange(curves.shape[1])
        xg = np.asarray(m["xg"])
        edges = np.asarray(m["edges"])
        hist = np.asarray(m["hist"])
        ck = list(m["ck"])
        ymax = max(float(np.max(m["dens"][-1])), float(hist.max())) * 1.1

        def frame(i):
            a = axes([0, 0.16], [0, ymax], x_length=5.2, y_length=3.2, xlabel=r"bill rate", ylabel=r"density",
                     xticks=[0, 0.08, 0.16], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[], font_size=15)
            w = edges[1] - edges[0]
            bars = VGroup(*[Rectangle(width=a.ax.c2p(w * 0.92, 0)[0] - a.ax.c2p(0, 0)[0],
                                      height=max(a.ax.c2p(0, h)[1] - a.ax.c2p(0, 0)[1], 0.001), stroke_width=0,
                                      fill_color=BM, fill_opacity=0.45).move_to(a.ax.c2p(e0 + w / 2, 0), aligned_edge=DOWN)
                            for e0, h in zip(edges[:-1], hist)])
            d = np.minimum(np.asarray(m["dens"][min(i, len(ck) - 1)]), ymax)
            p = m["ck_params"][min(i, len(ck) - 1)]
            nu = 2 * p[0] * p[1] / p[2] ** 2
            txt = MathTex(rf"\kappa = {p[0]:.3f},\ \theta = {100 * p[1]:.2f}\%,\ \sigma = {p[2]:.3f},\ \nu = {nu:.2f}",
                          font_size=22, color=STRAT).next_to(a, UP, buff=0.1)
            return VGroup(a, bars, curve(a.ax, xg, d, STRAT, stroke_width=3), txt)
        lo = float(np.percentile(curves, 2))
        rp = TrainingReplay(steps, np.clip(curves, lo, None), frame, checkpoints=ck, ylabel=r"log-likelihood",
                            xlabel=r"Nelder--Mead iteration", color=STRAT)
        base = DashedLine(rp.ax.c2p(steps[0], m["reg_loglik"]), rp.ax.c2p(steps[-1], m["reg_loglik"]), color=GREY_B,
                          stroke_width=2)
        bl = label(r"regression estimate", font_size=17, color=GREY_B).next_to(base, DOWN, buff=0.08).align_to(base,
                                                                                                       RIGHT)
        b = m["best"]
        res = VGroup(MathTex(rf"\text{{exact MLE: }} \nu = {b['feller']:.2f}", font_size=30, color=STRAT),
                     label(rf"log-likelihood {b['loglik']:.1f} against {m['reg_loglik']:.1f}; five starts agree",
                           font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        res.to_edge(DOWN, buff=0.3)
        below = b["feller"] < 1
        verdict = (f"just below one, {b['feller']:.2f}: the fitted rate can still touch zero, barely."
                   if below else f"{b['feller']:.2f}, at or above one: by the likelihood, zero is out of reach.")
        with self.voiceover(
            "So fit it properly. The likelihood of the whole history is a product of non-central chi-square "
            "densities, and the House maximizes it by Nelder-Mead from five starts, one of them the regression "
            "estimate. <bookmark mark='a'/> On the right, the log-likelihood climbing, the starts as a band and the "
            "regression's value dashed. On the left, the fitted long-run Gamma density morphing over sixty-seven "
            "years of rates. <bookmark mark='b'/> All five starts end at the same place, and the Feller ratio moves "
            f"from {r['cir']['feller']:.2f} to {verdict} Part nineteen fits rate models to bond prices instead."
            " A simulated path is one view of an SDE; a PDE is the other. Next: why they are the same thing."
        ) as vo:
            self.play(FadeIn(rp), Create(base), FadeIn(bl))
            vo.wait_until("a")
            rp.play(self, run_time=7)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
