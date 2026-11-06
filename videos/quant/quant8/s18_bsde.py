from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import predict, ALT, GOOD, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class BSDE(VoiceoverScene):
    def construct(self):
        b = load("bsde")
        rp = load("bsde_replay")
        self.card()
        self.derive()
        self.replay(rp)
        self.converge(b)

    def card(self):
        c = chapter_card(14, r"Backward stochastic differential equations", r"How do you price when the price is "
                         r"not linear?", part=PART)
        with self.voiceover("Chapter fourteen. Backward stochastic differential equations."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"-dY_t", r"=", r"f(t, Y_t, Z_t)\,dt - Z_t\,dW_t,\qquad Y_T = \xi", font_size=32,
                      colors={r"-dY_t": VALUE}),
                cmath(r"f", r"=", r"-rY - \theta Z\ \Rightarrow\ Y_t = \mathbb{E}^{\mathbb{Q}}\big[e^{-r(T-t)}\xi \mid "
                      r"\mathcal{F}_t\big],\ \ Z = \sigma S\,\Delta", font_size=30),
                cmath(r"f", r"=", r"-rY - \theta Z + (R - r)\Big(Y - \frac{Z}{\sigma}\Big)^-", font_size=32,
                      colors={r"(R - r)": OVER}),
                cmath(r"Z_n \approx \frac{\mathbb{E}[Y_{n+1}\Delta W_n \mid S_n]}{\Delta t}", r",\ ",
                      r"Y_n \approx \mathbb{E}[Y_{n+1} \mid S_n] + f(Y_n, Z_n)\,\Delta t", font_size=30)]
        whys = [why(r"Brownian representation; square-integrable terminal payoff and driver at zero; uniformly Lipschitz driver: unique $(Y,Z)$ in $S^2\times H^2$", font_size=21),
                why(r"a linear driver is Black--Scholes: $Y$ is the price and $Z$ the hedge (El Karoui, Peng and Quenez "
                    r"1997)", font_size=21),
                why(r"borrow at $R$, lend at $r$: the cash account $Y - Z/\sigma$ costs more when negative (Bergman 1995); "
                    r"a larger driver gives a larger price (the comparison theorem): at least Black--Scholes at $r$",
                    font_size=21),
                why(r"the scheme: conditional expectations by least squares on the simulated paths (Gobet, Lemor and "
                    r"Warin 2005)", font_size=21)]
        step = ladder(self, rows, whys, keep=4, top=3.1, x=-0.2, buff=0.72, edge=6.9)
        with self.voiceover(
            "The control problems so far ran forward in time and were solved backwards. A backward stochastic differential equation makes that the definition. Find a pair of processes, Y and Z, that use only the information available at each time and end at a given payoff. Étienne Pardoux and Shige Peng proved in 1990 that a square-integrable adapted pair exists uniquely in a Brownian filtration with representation, for a uniformly Lipschitz driver, square-integrable terminal payoff and suitable integrability of the driver at zero. <bookmark mark='a'/> With a linear driver, Y is the Black-Scholes value; in a smooth Markov model Z is sigma S times delta: Nicole El Karoui, Peng and Marie-Claire Quenez showed in 1997 that pricing and hedging are exactly this. <bookmark mark='b'/> The point is the nonlinear case. Suppose the hedger borrows at six percent and lends at one. The driver gains a term that switches on only when the hedge's cash account is negative, and the price is no longer linear in the payoff. The comparison theorem says a larger driver gives a larger price, so it is at least the Black-Scholes price at the lending rate. <bookmark mark='c'/> To solve it, simulate the stock forward, then step backwards, replacing each conditional expectation by a regression across the simulated paths: the method of Gobet, Lemor and Warin. Comparison also requires compatible scalar-driver assumptions and the same terminal payoff."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, rp):
        t = np.asarray(rp["t"])
        fan = np.asarray(rp["fan"])
        grid = np.asarray(rp["grid"])
        frames = rp["frames"]
        g1 = axes([0, 0.5], [10 * np.floor(fan.min()/10), 10 * np.ceil(fan.max()/10)], x_length=4.6, y_length=3.6, xlabel=r"years", ylabel=r"stock, forward",
                  xticks=[0, 0.25, 0.5], yticks=[80, 100, 120], font_size=15).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        paths = path_fan(g1.ax, t, fan, color=UNDER, opacity=0.45)
        g2 = axes([75, 125], [-12, 12], x_length=6.4, y_length=4.2, xlabel=r"stock at step $n$",
                  ylabel=r"$Y_{n+1}$ on each path, and its regression", xticks=[80, 95, 105, 120], yticks=[-10, 0, 10],
                  font_size=15).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        ax = g2.ax

        def frame(i):
            fr = frames[i]
            S, Y = np.asarray(fr["S"]), np.asarray(fr["Ynext"])
            m = (S > 75) & (S < 125) & (Y >= -12) & (Y <= 12)
            dots = VGroup(*[Dot(ax.c2p(a, float(b)), radius=0.025, color=GREY_B).set_opacity(0.6)
                            for a, b in zip(S[m], Y[m])])
            values = np.asarray(fr["fit"])
            visible = (values >= -12) & (values <= 12)
            fit = curve(ax, grid[visible], values[visible], VALUE, stroke_width=4)
            tag = MathTex(rf"n = {fr['n']}", font_size=30, color=VALUE).next_to(g2, UP, buff=0.1).align_to(g2, RIGHT)
            return VGroup(dots, fit, tag)

        cur = frame(0)
        pay = curve(ax, grid, np.asarray(rp["payoff"]), GREY_C, stroke_width=2)
        res = VGroup(
            MathTex(rf"Y_0 = {rp['Y0']:.3f}", font_size=34, color=VALUE),
            MathTex(rf"\text{{BS at }} r = 1\%:\ {rp['bs_r']:.3f}", font_size=26, color=UNDER),
            MathTex(rf"\text{{BS at }} R = 6\%:\ {rp['bs_R']:.3f}", font_size=26, color=OVER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(g1, UP, buff=0.3).align_to(g1, LEFT)
        q = predict(r"Will the two-rate price lie between Black--Scholes at 1\% and at 6\%?", width=5.0,
                       font_size=20).next_to(g1, UP, buff=0.3).align_to(g1, LEFT)
        with self.voiceover(
            f"Here is the scheme running, on a ratio call spread: long one call at ninety-five, short two at a hundred and five, half a year. First twenty thousand stock paths are simulated forward. <bookmark mark='a'/> Then, backwards from the last step: each grey cloud is the next step's value on every path, plotted against today's stock price. The regression through the cloud is the conditional expectation, and after the driver's correction it becomes the value one step earlier, which feeds the next cloud. Watch the payoff's corners round off as we move toward today. <bookmark mark='b'/> Pause and predict: will the price lie between the Black-Scholes prices at one and at six percent? <bookmark mark='c'/> No: {rp['Y0']:.3f}, above both, {rp['bs_r']:.3f} and {rp['bs_R']:.3f}. The spread's hedge borrows in some states and lends in others, and each side is charged its own rate: funding depends on the cash sign, so this pricing operator is not one uniform linear-rate operator. The ratio spread has negative unbounded payoff at high stock prices. The regression panel shows stock prices from seventy-five to one hundred and twenty-five and values from minus twelve to twelve; points outside that window are omitted, not placed on its edges."
        ) as vo:
            self.play(FadeIn(g1), LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.03, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(pay), FadeIn(cur))
            per = max(min((vo.remaining(8.0) - 6) / len(frames), 1.0), 0.5)
            for i in range(1, len(frames)):
                self.play(Transform(cur, frame(i)), run_time=per)
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeOut(q), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def converge(self, b):
        runs = b["runs"]
        ns = [int(k) for k in runs]
        means = [np.mean(runs[k]) for k in runs]
        sds = [np.std(runs[k]) for k in runs]
        g = axes([np.log10(3000), np.log10(500000)], [0.5, 1.4], x_length=6.4, y_length=3.8,
                 xlabel=r"simulated paths", ylabel=r"price of the call spread", xticks=[4, 5],
                 xfmt=lambda u: f"10^{{{int(u)}}}", yticks=[0.6, 0.8, 1.0, 1.2, 1.4], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        lines = VGroup()
        for val, col, txt in ((b["pde"], GOOD, r"nonlinear PDE"), (b["bs_r"], UNDER, r"Black--Scholes at $r$"),
                              (b["bs_R"], OVER, r"Black--Scholes at $R$")):
            ln = DashedLine(ax.c2p(np.log10(3000), val), ax.c2p(np.log10(500000), val), color=col, stroke_width=2)
            ref_label = label(txt + f": {val:.3f}", font_size=17, color=col)
            ref_label.next_to(ln, UP, buff=0.1).align_to(ln, RIGHT)
            lines.add(VGroup(ln, ref_label))
        pts = VGroup(*[VGroup(Line(ax.c2p(np.log10(n), m - 2 * s), ax.c2p(np.log10(n), m + 2 * s), color=VALUE,
                                   stroke_width=3), Dot(ax.c2p(np.log10(n), m), radius=0.06, color=VALUE))
                       for n, m, s in zip(ns, means, sds)])
        side = VGroup(
            wrapped_label(r"dots: regression BSDE, 3 runs each; $\pm2$ run standard deviations describe dispersion, not a confidence interval or convergence proof", 4.0, 19, GREY_A),
            MathTex(rf"\text{{polynomial basis: }}{b['poly']:.3f}", font_size=26, color=GREY_B),
            wrapped_label(r"in this fixed discretization the degree-6 polynomial estimate is lower; local hat functions are closer to the PDE. Basis and discretization errors both matter. Han et al.\ (2018): high-dimensional deep BSDE examples",
                          4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"""As path counts increase, these estimates approach the PDE reference {b['pde']:.3f} in this fixed discretization. Three repetitions at each size give the displayed plus-or-minus two standard deviations, a dispersion summary, not a confidence interval or proof of convergence. <bookmark mark='a'/> The degree-six polynomial estimate is {b['poly']:.3f}; local hat functions are closer here. This comparison alone does not isolate the source of the basis error. Han, Jentzen and E demonstrated high-dimensional neural BSDE methods in 2018. Part seventeen trains one. Next: investors interacting with a crowd."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(lines))
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.3), FadeIn(side[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
