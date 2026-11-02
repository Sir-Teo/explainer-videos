from __future__ import annotations

import numpy as np
from scipy.special import gammaln

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import (BAD, IV, MODEL_COL, NAMES, OPT, PART, RV, SPOT, VAR, illustration, load, pause,
                                         real_data)


class Jumps(VoiceoverScene):
    def construct(self):
        c = load("calibrate")
        lf = load("levy_fits")
        br = load("bates_replay")
        self.card()
        self.cake()
        self.derive()
        self.scores(c, lf)
        self.replay(br, lf)
        self.cards()

    def card(self):
        c = chapter_card(8, r"Jumps: Merton, Kou and Bates", r"What if prices do not move continuously?", lit=(1987,),
                         part=PART)
        with self.voiceover("Chapter eight. Jumps: Merton, Kou, and Bates."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cake(self):
        sig, mj, sj, T = 0.3, -0.12, 0.08, 0.25
        xs = np.linspace(-0.9, 0.5, 241)
        kbar = np.exp(mj + 0.5 * sj * sj) - 1

        def layers(lam):
            lt = lam * T
            out = []
            for n in range(6):
                w = float(np.exp(-lt + (n * np.log(lt) if lt > 0 else 0) - gammaln(n + 1)))
                mu = -lam * kbar * T - 0.5 * sig ** 2 * T + n * mj
                var = sig ** 2 * T + n * sj ** 2
                out.append((w, w * np.exp(-0.5 * (xs - mu) ** 2 / var) / np.sqrt(2 * np.pi * var)))
            return out

        g = axes([-0.9, 0.5], [0, 3.0], x_length=7.2, y_length=4.2, xlabel=r"$\ln S_T / S_0$, three months",
                 ylabel=r"density", xticks=[-0.8, -0.4, 0, 0.4], yticks=[0, 1, 2, 3], font_size=16).to_edge(LEFT, buff=0.6)
        ax = g.ax
        cols = [SPOT, BAD, OPT, VAR, IV, GREY_B]

        def draw(lam):
            L = layers(lam)
            base = np.zeros_like(xs)
            grp = VGroup()
            for n, (w, d) in enumerate(L):
                top = base + d
                poly = Polygon(*[ax.c2p(x, y) for x, y in zip(xs, np.clip(top, 0, 3))],
                               *[ax.c2p(x, y) for x, y in zip(xs[::-1], np.clip(base[::-1], 0, 3))],
                               stroke_width=0, fill_color=cols[n], fill_opacity=0.7)
                grp.add(poly)
                base = top
            env = curve(ax, xs, np.clip(base, 0, 3), WHITE, stroke_width=2.5)
            wbars = VGroup(*[VGroup(Rectangle(width=0.32, height=max(2.4 * w, 0.01), stroke_width=0, fill_color=cols[n],
                                              fill_opacity=0.85),
                                    MathTex(str(n), font_size=20, color=GREY_A)).arrange(DOWN, buff=0.08)
                             for n, (w, _) in enumerate(L)])
            wbars.arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
            lab = MathTex(rf"\lambda = {lam:g}\ \text{{a year}}", font_size=30, color=WHITE)
            panel = VGroup(lab, wbars, label(r"Poisson weight of $n$ jumps", font_size=18, color=GREY_B)).arrange(
                DOWN, buff=0.25).to_edge(RIGHT, buff=0.8).shift(UP * 0.5)
            return VGroup(grp, env, panel)

        cur = draw(1.0)
        src = illustration(r"$\sigma = 30\%$, jumps $\mathcal{N}(-12\%, 8\%^2)$, three months")
        with self.voiceover(
            (
            "A diffusion cannot gap. Robert Merton added jumps in 1976, and his model has an exact solution best seen "
            "as a layer cake. Over three months the price jumps zero times, once, twice; given the count, the log "
            "price is Gaussian. <bookmark mark='a'/> So the law is a stack of Gaussian layers, each shifted by its "
            "jumps and weighted by its Poisson probability. <bookmark mark='b'/> Raise the intensity: weight moves "
            "into the jump layers and the left tail fattens, the crash insurance a put buys. <bookmark mark='c'/> "
            "Lower it, and the cake collapses toward Black and Scholes."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(cur[2]), LaggedStart(*[FadeIn(p_) for p_ in cur[0]], lag_ratio=0.4),
                      Create(cur[1]), run_time=3)
            vo.wait_until("b")
            self.play(Transform(cur, draw(4.0)), run_time=2.5)
            vo.wait_until("c")
            self.play(Transform(cur, draw(0.3)), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\frac{dS}{S_-}", r"=", r"-\lambda\bar k\,dt + \sigma\,dW + (e^J - 1)\,dN,\quad "
                      r"\bar k = e^{\mu_J + \sigma_J^2/2} - 1", font_size=32, colors={r"\frac{dS}{S_-}": SPOT}),
                cmath(r"\ln S_T \mid N_T = n", r"\sim", r"\mathcal{N}\big(\ln S_0 - \lambda\bar kT - \tfrac12\sigma^2T + "
                      r"n\mu_J,\ \ \sigma^2T + n\sigma_J^2\big)", font_size=32, colors={r"\ln S_T \mid N_T = n": SPOT}),
                cmath(r"C", r"=", r"\sum_{n\ge0} e^{-\lambda T}\frac{(\lambda T)^n}{n!}\ "
                      r"C_{\text{BS}}\big(S_0 e^{-\lambda\bar kT + n(\mu_J + \sigma_J^2/2)},\ K,\ T,\ \sigma_n\big),\ "
                      r"\sigma_n^2 = \sigma^2 + \tfrac{n\sigma_J^2}{T}", font_size=28, colors={r"C": OPT}),
                cmath(r"\varphi_{\text{Bates}}", r"=", r"\varphi_{\text{Heston}}\cdot\exp\Big(\lambda T\big(e^{iu\mu_J - "
                      r"\frac12\sigma_J^2u^2} - 1 - iu\bar k\big)\Big)", font_size=32, colors={r"\varphi_{\text{Bates}}": OPT})]
        whys = [why(r"Merton (1976): Poisson jumps at rate $\lambda$; the drift $-\lambda\bar k$ compensates them so that "
                    r"$S$ (zero rates) is a martingale", 20),
                why(r"given $n$ jumps, a sum of independent Gaussians", 20),
                why(r"condition on $n$, price by Black--Scholes, and weight by the Poisson law (Shreve II, 11.7); the "
                    r"House's merton\_series matches COS to $10^{-8}$", 20),
                why(r"independent factors multiply: Bates (1996) is Heston times Merton's jump factor", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            (
            "In symbols: the price diffuses, and jumps by e to the J when a Poisson clock rings; the drift minus "
            "lambda k bar keeps it a fair game. <bookmark mark='a'/> Given n jumps, the log price is a sum of "
            "independent Gaussians. <bookmark mark='b'/> Condition on n, price by Black–Scholes, weight by Poisson: "
            "Merton's series, which the House matches to Fourier pricing at eight decimals. <bookmark mark='c'/> "
            "Independent factors multiply, so Bates's 1996 model is Heston times Merton's jump factor. Kou's 2002 "
            "jumps are double exponential, and their memoryless overshoot prices barriers in closed form, as Kou and "
            "Wang showed."
        )
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def scores(self, c, lf):
        F = lf["fits"]
        names = ["BS", "Merton", "Kou", "VG", "NIG", "CGMY_inf", "Heston", "Bates", "SABR"]
        vals = []
        for n in names:
            if n == "SABR":
                vals.append(c["sabr_rmse"])
            elif n in ("BS", "Heston", "Bates"):
                vals.append(c["fits"][n]["rmse"])
            else:
                vals.append(F[n]["rmse_iv"])
        npar = {"BS": 1, "Merton": 4, "Kou": 5, "VG": 3, "NIG": 3, "CGMY_inf": 4, "Heston": 5, "Bates": 8,
                "SABR": 3 * len(c["sabr"])}
        g = axes([0, 4.5], [-0.5, len(names) - 0.5], x_length=6.0, y_length=4.8, xlabel=r"fit error (vol points, vega-weighted)",
                 xticks=[0, 1, 2, 3, 4], yticks=[], font_size=15).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.1)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, (n, v) in enumerate(zip(names, vals)):
            y = len(names) - 1 - i
            bars.add(Rectangle(width=max(abs(ax.c2p(min(v, 4.5), 0)[0] - ax.c2p(0, 0)[0]), 1e-3), height=0.38,
                               stroke_width=0, fill_color=MODEL_COL[n], fill_opacity=0.85).move_to(ax.c2p(min(v, 4.5) / 2, y)))
            labs.add(VGroup(label(NAMES[n], font_size=18, color=MODEL_COL[n]),
                            label(rf"{npar[n]} parameter" + ("s" if npar[n] > 1 else ""), font_size=14, color=GREY_B))
                     .arrange(DOWN, aligned_edge=RIGHT, buff=0.03).next_to(ax.c2p(0, y), LEFT, buff=0.15))
            labs[-1].add(MathTex(f"{v:.2f}", font_size=20).next_to(bars[-1], RIGHT, buff=0.1))
        m, k = F["Merton"]["params"], F["Kou"]["params"]
        b = c["fits"]["Bates"]["params"]
        rare = m["lam"] < 2 and m["mj"] < -0.15
        side = VGroup(
            wrapped_label(rf"every model fitted to the same {c['n']} quotes by the same calibrator", 4.6, 19, GREY_A),
            MathTex(rf"\text{{Merton:}}\ \lambda = {m['lam']:.2f},\ \mu_J = {100 * m['mj']:.0f}\%,\ \sigma_J = {100 * m['sj']:.0f}\%",
                    font_size=24, color=MODEL_COL["Merton"]),
            MathTex(rf"\text{{Kou:}}\ \lambda = {k['lam']:.1f},\ p = {k['p']:.2f},\ \eta_1 = {k['eta1']:.1f},\ \eta_2 = {k['eta2']:.1f}",
                    font_size=24, color=MODEL_COL["Kou"]),
            MathTex(rf"\text{{Bates:}}\ \lambda = {b['lam']:.0f},\ \mu_J = {100 * b['mj']:.1f}\%,\ \sigma_J = {100 * b['sj']:.0f}\%",
                    font_size=24, color=MODEL_COL["Bates"]),
            wrapped_label(r"without stochastic volatility the jumps become crash insurance; with it, the optimizer spends "
                          r"them on the body of the smile" if rare else
                          r"the jumps are spent on the body of the smile, with or without stochastic volatility", 4.6, 19,
                          WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(LEFT, buff=0.5)
        src = real_data(r"the Surface, 10 December 2025; the House's calibrator, COS pricing")
        mv = F["Merton"]["by_expiry"]
        shape = ("Rare and huge: crash insurance, the only way a constant-volatility model can make the short-dated "
                 "puts dear." if rare else "Frequent and moderate: the jumps act as extra curvature.")
        d0 = sorted(mv, key=lambda z: int(z))[0]
        with self.voiceover(
            (
            f"Now fit every model in the part to the same {c['n']} quotes. One Black–Scholes vol misses by "
            f"{c['fits']['BS']['rmse']:.1f} points. <bookmark mark='a'/> Merton reaches {F['Merton']['rmse_iv']:.1f}, "
            f"with jumps {m['lam']:.2f} a year, each about {100 * abs(m['mj']):.0f} percent down. {shape} Its "
            f"{d0}-day expiry is still off by {mv[d0]:.1f}. Kou: {F['Kou']['rmse_iv']:.1f}. <bookmark mark='b'/> "
            f"Heston: {c['fits']['Heston']['rmse']:.2f}. Bates: {c['fits']['Bates']['rmse']:.2f}, with "
            f"{b['lam']:.0f} jumps a year of {100 * abs(b['mj']):.0f} percent. <bookmark mark='c'/> The same jumps "
            "mean opposite things: without stochastic volatility, a crash; with it, a second diffusion. On this calm "
            "day the Surface priced no crash that stochastic volatility could not explain."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), GrowFromEdge(bars[0], LEFT), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(*[AnimationGroup(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i])) for i in (1, 2)], FadeIn(side[1:3]))
            self.play(*[AnimationGroup(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i])) for i in (3, 4, 5)])
            vo.wait_until("b")
            self.play(*[AnimationGroup(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i])) for i in (6, 7, 8)], FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def replay(self, br, lf):
        runs = br["runs"]
        hi = br["hi"]
        n_max = max(r["trace"]["eval"][-1] for r in runs)
        cols = [MODEL_COL["Bates"], IV, VAR]

        def panel(ylab, lo_, hi_, yt, fmt=None):
            return axes([0, n_max], [lo_, hi_], x_length=3.8, y_length=3.0, xlabel=r"evaluations", ylabel=ylab,
                        xticks=[0, n_max], yticks=yt, yfmt=fmt, font_size=13)

        pL = panel(r"loss, best so far", 1.0, 6.0, [1, 3, 5])
        pl = panel(r"jump rate $\lambda$ (a year)", 0, 21, [0, 10, 20])
        ps = panel(r"jump size $\sigma_J$", 0, 0.3, [0, 0.1, 0.2, 0.3], fmt=lambda u: f"{100 * u:.0f}\\%")
        P = VGroup(pL, pl, ps).arrange(RIGHT, buff=0.55).to_edge(UP, buff=0.9)
        bound = DashedLine(pl.ax.c2p(0, hi[5]), pl.ax.c2p(n_max, hi[5]), stroke_color=BAD, stroke_width=2)
        bl = label(r"bound", font_size=14, color=BAD).next_to(pl.ax.c2p(n_max, hi[5]), UP, buff=0.05).align_to(bound, RIGHT)
        floor = DashedLine(ps.ax.c2p(0, br["lo"][7]), ps.ax.c2p(n_max, br["lo"][7]), stroke_color=BAD, stroke_width=2)
        t = ValueTracker(0)

        def series(r, j, ax, lo_, hi_, col):
            ev = np.asarray(r["trace"]["eval"])
            y = np.asarray(r["trace"]["best"]) if j is None else np.asarray(r["trace"]["x"])[:, j]
            y = np.clip(y, lo_, hi_)

            def mk():
                k = max(int(np.searchsorted(ev, t.get_value(), side="right")), 2)
                return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(
                    [ax.c2p(a, b) for a, b in zip(ev[:k], y[:k])])
            return always_redraw(mk)

        lines = VGroup()
        for r, col in zip(runs, cols):
            lines.add(series(r, None, pL.ax, 1.0, 6.0, col), series(r, 5, pl.ax, 0, 21, col), series(r, 7, ps.ax, 0, 0.3, col))
        leg = legend([(c_, rf"start {i + 1}") for i, c_ in enumerate(cols)], font_size=17).arrange(RIGHT, buff=0.4)
        leg.next_to(P, DOWN, buff=0.35)
        fin = [r["x"] for r in runs]
        foot = wrapped_label(rf"all three starts end with $\lambda$ at its bound of {hi[5]:.0f} and $\sigma_J$ at its floor of "
                             rf"{100 * br['lo'][7]:.0f}\%; the loss ends at {min(r['rmse'] for r in runs):.3f}: frequent "
                             r"tiny jumps, a second diffusion", 12.0, 21, WHITE).next_to(leg, DOWN, buff=0.35)
        at_bound = all(x[5] > 0.99 * hi[5] for x in fin)
        src = real_data(r"the Surface; Bates calibrated from three starts, every evaluation recorded")
        drift = ("The intensity climbs, all the way to the bound of twenty a year that we allowed, and the jump size "
                 "shrinks to its floor, while the loss barely moves." if at_bound else
                 "The intensity and the size trade off against each other while the loss barely moves.")
        with self.voiceover(
            (
            f"Watch the Bates fit from three starts: loss, jump intensity, jump size. <bookmark mark='a'/> The loss "
            f"drops as the Heston part settles; then the jumps drift. {drift} <bookmark mark='b'/> Many small jumps "
            "look exactly like more diffusion. Pause: with Merton's intensity, what is the chance of no jump before "
            f"a three-day option expires? About {100 * np.exp(-lf['fits']['Merton']['params']['lam'] * 3 / 365):.1f} "
            "percent. Short options price the possibility, not the frequency."
        )
        ) as vo:
            self.play(FadeIn(P), FadeIn(src), Create(bound), FadeIn(bl), Create(floor), FadeIn(leg))
            self.add(lines)
            self.play(t.animate.set_value(n_max), run_time=max(vo.until("b") - 0.3, 3), rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        for l_ in lines:
            l_.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def cards(self):
        c1 = history_card(2000, r"Duffie, Pan and Singleton; Eraker, Johannes and Polson (2003)",
                          r"SVCJ: jumps in volatility too, arriving with the price jumps. Broadie, Chernov and Johannes "
                          r"(2007) found volatility jumps and jump risk premia necessary for S\&P 500 index options.",
                          color=QC.IDEA, width=4.2)
        c2 = history_card(2020, r"Hou, Wang, Chen and H\"ardle, \textit{J. Fin. Econometrics}",
                          r"``Pricing cryptocurrency options'': SVCJ fitted to bitcoin finds jumps in returns and in "
                          r"variance, anti-correlated: down jumps in price with up jumps in volatility.", color=QC.IDEA,
                          width=4.2)
        c3 = history_card(2006, r"Jump to default (Gatheral, ch.\ 6)",
                          r"A jump to zero at rate $\lambda$: the simplest credit model inside an equity smile; it steepens "
                          r"the skew at every maturity. Part 20 builds credit on it.", color=QC.CRISIS, width=4.2)
        G = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        if G.width > 13.2:
            G.scale_to_fit_width(13.2)
        with self.voiceover(
            (
            "Extensions. Duffie, Pan and Singleton, and Eraker, Johannes and Polson, let volatility jump with the "
            "price; Broadie, Chernov and Johannes found such jumps needed for S&P options. <bookmark mark='a'/> On "
            "Bitcoin, Hou, Wang, Chen and Härdle found jumps in price and variance, anti-correlated. "
            "<bookmark mark='b'/> The extreme jump, to zero, is default: Part twenty."
            " Next: pure-jump models, and time changes."
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c3, shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
