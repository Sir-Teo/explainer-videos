from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
from explainer.quant.house import rough as R
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, SPOT, VAR, illustration, load,
                                         loglog_curve, loglog_skew_axes, pause, real_data, running_min)

SMILE_DAYS = (4, 16, 79)


class RBergomi(VoiceoverScene):
    def construct(self):
        rb = load("rbergomi")
        rs = load("rbskew")
        rp = load("rb_replay")
        self.card()
        self.model()
        self.proof()
        self.scheme(rb)
        self.replay(rb, rp, rs)

    def card(self):
        c = chapter_card(5, r"Rough Bergomi", r"What is the simplest rough model that prices options?", lit=(2016,),
                         part=PART)
        with self.voiceover("Chapter five. Rough Bergomi."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"v_t", r"=", r"\xi_0(t)\,\exp\!\Big(\eta\,W^H_t - \tfrac12\eta^2 t^{2H}\Big)", font_size=38,
                      colors={r"v_t": VAR}),
                cmath(r"\frac{dS}{S}", r"=", r"\sqrt{v_t}\,\big(\rho\,dW_t + \sqrt{1 - \rho^2}\,dW^\perp_t\big)",
                      font_size=38, colors={r"\frac{dS}{S}": SPOT})]
        whys = [why('Riemann--Liouville rough driver; initial forward-variance curve supplied from Part 13'),
                why('three fitted numbers plus an externally supplied forward-variance curve')]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.2, buff=1.0, edge=6.9)
        with self.voiceover(
            """Bayer, Friz and Gatheral introduced rough Bergomi in 2016. Its instantaneous variance is the initial forward-variance curve multiplied by a compensated Gaussian exponential. The driver here is a Riemann--Liouville Volterra process, not full fractional Brownian motion with stationary increments. The input curve is extracted from Part thirteen's finite-strike market construction and held fixed. <bookmark mark='a'/> Three fitted parameters remain: H, eta and rho. Matching the expected variance to that input curve is a model identity; it is not exact matching of every option mark."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\mathrm{Var}\,W^H_t", r"=", r"2H\int_0^t (t - s)^{2H - 1}\,ds = t^{2H}", font_size=38,
                      colors={r"\mathrm{Var}\,W^H_t": ROUGH}),
                cmath(r"\mathbb{E}\,v_t", r"=", r"\xi_0(t)\,\mathbb{E}\,e^{\eta W^H_t - \frac12\eta^2 t^{2H}} = \xi_0(t)",
                      font_size=38, colors={r"\mathbb{E}\,v_t": VAR}),
                cmath(r"\xi_s(t)", r"=", r"\xi_0(t)\exp\!\Big(\eta\sqrt{2H}\!\int_0^s\!(t - u)^{H - \frac12}dW_u - "
                      r"\tfrac{\eta^2}{2}\!\int_0^s\! 2H(t - u)^{2H - 1}du\Big)", font_size=32, colors={r"\xi_s(t)": OPT}),
                cmath(r"\text{state at } s", r"=", r"\text{the whole curve } \xi_s(\cdot)", font_size=38,
                      colors={r"\text{state at } s": GREY_A})]
        whys = [why(r"the Itô isometry, with $W^H_t = \sqrt{2H}\int_0^t (t - s)^{H - 1/2}dW_s$"),
                why('Gaussian exponential mean identity: matches the supplied expected-variance curve, not every option price'),
                why(r"condition on $\mathcal{F}_s$: the rest of the integral is independent and Gaussian; $\xi_s(t) = "
                    r"\mathbb{E}_s v_t$ is an exponential martingale in $s$"),
                why(r"not Markov in $(S, v)$: what is known at $s$ is a whole curve (Bergomi's forward variance)")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.2, buff=0.75, edge=6.9)
        q = pause(r"Double $\eta$. What happens to $\mathbb{E}[v_t]$?", width=5.0, font_size=22).to_corner(DR, buff=0.3)
        with self.voiceover(
            """The Itô isometry gives the driver's variance as t to two H. <bookmark mark='a'/> A centered Gaussian exponential with the compensator shown has mean one, so expected instantaneous variance equals the input xi zero of t. Double eta: does that expectation change? <bookmark mark='b'/> No. At a fixed future date t, conditioning at s gives the displayed exponential martingale in s. This proves the forward-variance identity. It does not make instantaneous variance a martingale, or by itself prove the stock is a true martingale. Standard rough Bergomi results give that stock property for nonpositive rho under the usual conditions. <bookmark mark='c'/> The natural state remains a curve; spot and current variance alone do not form a finite-dimensional Markov state."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(q))
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def scheme(self, rb):
        p = rb["params"]
        S, v = R.rbergomi_paths(p["H"], p["eta"], p["rho"], 0.2, 60 / 365, 240, 4, seed=5, return_v=True)
        t = np.linspace(0, 60, 241)
        vr = data_range(np.sqrt(v), zero=True)
        sr = data_range(S)
        g1 = axes([0, 60], list(vr), x_length=9.0, y_length=2.6, ylabel=r"volatility $\sqrt{v_t}$", xticks=[0, 20, 40, 60],
                  yticks=[0, 0.5, 1.0, 1.5], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        g2 = axes([0, 60], list(sr), x_length=9.0, y_length=2.6, xlabel=r"days", ylabel=r"price", xticks=[0, 20, 40, 60],
                  yticks=[0.8, 1.0, 1.2, 1.4], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        cols = [ROUGH, IV, RV, OPT]
        tr = ValueTracker(0)
        lv = VGroup(*[tracing(g1.ax, t, np.sqrt(v[:, i]), tr, c, stroke_width=1.6)
                      for i, c in enumerate(cols)])
        ls = VGroup(*[tracing(g2.ax, t, S[:, i], tr, c, stroke_width=2) for i, c in enumerate(cols)])
        side = VGroup(
            wrapped_label('no finite Markov state in spot and variance; numerical simulation used here', 3.6,
                          19, GREY_A),
            wrapped_label(r"Bennedsen, Lunde and Pakkanen's hybrid scheme (2017): the singular first step exactly, the rest "
                          r"as a convolution by FFT; opened up in chapter 6", 3.6, 19, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"four paths, $H = {p['H']:.2f}$, $\eta = {p['eta']:.1f}$, $\rho = {p['rho']:.2f}$, flat "
                           r"variance curve, 4 steps a day")
        with self.voiceover(
            """The kernel is singular, so a finite-grid simulator needs care. The hybrid scheme handles its nearest cell analytically and approximates the rest. <bookmark mark='a'/> These four simulated paths use fitted parameters but an illustrative flat variance curve. Negative rho couples the drivers and tends to associate price declines with volatility increases; it does not make every volatility spike coincide with a price fall. Every displayed sample remains a finite-grid realization."""
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(g1), FadeIn(g2), FadeIn(src), FadeIn(lv), FadeIn(ls))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), tr.animate.set_value(240), run_time=max(vo.remaining(0.0), 4), rate_func=linear)
        for m in (*lv, *ls):
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def replay(self, rb, rp, rs):
        seeds = rp["seeds"]
        s3 = seeds["3"]
        curves = [running_min(seeds[k]["curve"]) for k in ("3", "4", "5")]
        n = max(len(c) for c in curves)
        L = np.array([np.r_[c, np.full(n - len(c), c[-1])] for c in curves])
        steps = np.arange(n)
        best = s3["best"]
        idx = sorted(set([0, 1, 2, len(best) // 2, len(best) - 1]))
        ck = [best[i]["eval"] for i in idx]
        T = np.asarray(rp["T"])
        k = np.asarray(rp["k"])
        iv = np.asarray(rp["iv"])
        Td = np.round(T * 365).astype(int)
        cols = [ROUGH, IV, OPT]

        xr = data_range(k)
        yr = data_range(iv, *[b["iv"] for b in best])
        def frame(j):
            b = best[idx[j]]
            biv = np.asarray(b["iv"], float)
            g = axes(list(xr), list(yr), x_length=5.0, y_length=3.4, xlabel=r"log-moneyness $k$",
                     ylabel=r"implied volatility", xticks=[-0.4, 0, 0.4], yticks=[0.4, 0.6, 0.8, 1.0],
                     yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=13)
            grp = VGroup(g)
            for d, c in zip(SMILE_DAYS, cols):
                m = Td == d
                o = np.argsort(k[m])
                grp.add(VGroup(*[Dot(g.ax.c2p(a, y), radius=0.04, color=c)
                                 for a, y in zip(k[m], iv[m])]))
                ok = np.isfinite(biv[m][o])
                if ok.sum() > 1:
                    grp.add(curve(g.ax, k[m][o][ok], biv[m][o][ok], c, stroke_width=2.5))
            x = b["x"]
            grp.add(MathTex(rf"H = {x[0]:.2f},\ \eta = {x[1]:.2f},\ \rho = {x[2]:.2f}", font_size=24,
                            color=MODEL_COL["rBergomi"]).next_to(g, UP, buff=0.1))
            return grp

        rpl = TrainingReplay(steps, L, frame, ck, ylabel=r"fit error (vol points)", xlabel=r"model evaluation",
                             color=MODEL_COL["rBergomi"])
        leg = legend([(c, rf"{d}-day expiry") for d, c in zip(SMILE_DAYS, cols)], font_size=15).arrange(
            RIGHT, buff=0.3).to_edge(DOWN, buff=0.3)
        Hs = [seeds[s]["x"][0] for s in ("3", "4", "5")]
        oos = [seeds[s]["oos_rmse"] for s in ("3", "4", "5")]
        src = real_data(rf"the Surface; {rp['paths']:,} paths per seed, three seeds (band)".replace(",", "{,}"),
                        corner=UR)
        with self.voiceover(
            f"Now watch it calibrate. On the right, the fit error after every evaluation of the model, best so far; the band is the spread over three sets of random numbers. On the left, the model's smiles at three expiries, against the Surface's quotes as dots. <bookmark mark='a'/> It starts from a guess, H of a tenth and modest vol of vol. The optimizer pushes H down and eta up: the short smile steepens to meet the quotes. <bookmark mark='b'/> Across the three seeds, the fitted H lands between {min(Hs):.2f} and {max(Hs):.2f}, and re-priced on fresh paths the error is between {min(oos):.2f} and {max(oos):.2f} volatility points. The roughness the options ask for is extreme. These are fresh simulation seeds on the same market marks, not unseen market dates. The displayed H range also reflects the optimizer, grid and fixed variance-curve choice."
        ) as vo:
            self.play(FadeIn(rpl), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            rpl.play(self, run_time=max(vo.remaining(0.0) - 6.0, 6))
            vo.wait_until("b")
        self.wait(0.4)
        self.clear_scene()
        p = rb["params"]
        tab = VGroup(
            MathTex(rf"H = {p['H']:.2f},\quad \eta = {p['eta']:.2f},\quad \rho = {p['rho']:.2f}", font_size=36,
                    color=MODEL_COL["rBergomi"]),
            MathTex(rf"\text{{error}}\ {rb['rmse']:.2f}\ \text{{vol points}}\ \ (\text{{{rb['n']} quotes, up to 200 days}})",
                    font_size=30),
            wrapped_label(rf"the headline fit: {rb['n_paths']:,} paths with common random numbers, re-priced on fresh "
                          r"paths; the forward variance curve is Part 13's, from variance swaps".replace(",", "{,}"),
                          10.0, 20, GREY_A),
            wrapped_label('Heston uses five fitted parameters; rough Bergomi additionally takes a fixed market-derived variance curve. These are different model restrictions.', 10.0, 20, GREY_A),
            wrapped_label(r"Part 17 calibrates this model every week of 2024--2025 with a neural network trained on its "
                          r"prices", 10.0, 20, QC.HOUSE),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        src = real_data(r"the Surface, 10 December 2025")
        with self.voiceover(
            f"The headline fit, on twenty thousand paths: roughness {p['H']:.2f}, vol of vol {p['eta']:.1f}, correlation {p['rho']:.2f}, and an error of {rb['rmse']:.2f} volatility points on fresh paths. <bookmark mark='a'/> On the same quotes, Part thirteen's Heston misses by {rs['heston_rmse_same']:.2f}, with five free numbers and an absurd vol of vol. Three numbers and the market's variance curve beat five. Part seventeen calibrates this model every week, with a neural network standing in for the Monte Carlo. Every number from that model comes from simulating a rough path. Next: how to do it right. The variance curve is a separate market input. Different model structures and finite numerical budgets limit this one-date comparison."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()
