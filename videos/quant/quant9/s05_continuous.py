from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, P_C, PART, Q_C, answer_under, illustration, load,
                                        pause_at)


class Continuous(VoiceoverScene):
    def construct(self):
        g = load("girsanov")
        self.card()
        self.theorems()
        self.girsanov()
        self.reweight(g)
        self.result(g)
        self.predict(g)

    def card(self):
        c = chapter_card(9, r"Continuous time: Girsanov as reweighting", r"What does changing the measure do to a "
                         r"path?", lit=(1981,), part=PART)
        with self.voiceover("Chapter nine. Continuous time: Girsanov as reweighting."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def theorems(self):
        items = [
            (r"1979", r"Harrison and Kreps", r"finitely many dates and states: no arbitrage $\iff$ an equivalent "
                                             r"martingale measure; prices are expectations under it"),
            (r"1981", r"Harrison and Pliska", r"continuous trading: gains are stochastic integrals (Part 5); the "
                                              r"market is complete $\iff$ the measure is unique, and martingale "
                                              r"representation gives the hedge"),
        ]
        cards = VGroup(*[history_card(y, n, t, width=6.2, font_size=21) for y, n, t in items])
        cards.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.9)
        foot = MathTex(r"\frac{S_t}{B_t} = \mathbb{E}^Q\!\left[\frac{S_T}{B_T}\,\Big|\,\mathcal{F}_t\right]", font_size=40,
                       color=Q_C).next_to(cards, DOWN, buff=0.6)
        fn = wrapped_label(r"NFLVR gives an equivalent local martingale measure; lower-bounded wealth is a supermartingale. The expectation equality above needs a true martingale (as in our GBM example)", 11.0, 21,
                           GREY_A).next_to(foot, DOWN, buff=0.35)
        with self.voiceover(
            """The theorem grew up. In finite frictionless markets, no arbitrage is equivalent to an equivalent martingale measure. <bookmark mark='a'/> In continuous time the general locally bounded semimartingale theorem uses no free lunch with vanishing risk and an equivalent local martingale measure. Completeness and uniqueness require a specified filtration and claim class. <bookmark mark='b'/> A lower-bounded admissible discounted wealth process is generally a supermartingale, not automatically a true martingale. Replication agrees with expectation when the replicated discounted value is a true martingale with the required integrability. Our constant-coefficient Black-Scholes example has these properties."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(fn))
        self.wait(0.3)
        self.clear_scene()

    def girsanov(self):
        rows = [cmath(r"dS_t", r"=", r"\mu S_t\, dt + \sigma S_t\, dW_t", font_size=36, colors={r"dS_t": FWD}),
                cmath(r"d\tilde S_t", r"=", r"(\mu - r)\,\tilde S_t\, dt + \sigma \tilde S_t\, dW_t,\quad \tilde S = S/B",
                      font_size=34),
                cmath(r"W^Q_t = W_t + \lambda t", r"\Rightarrow", r"d\tilde S_t = \sigma\tilde S_t\, dW^Q_t,\quad \lambda = "
                      r"\frac{\mu - r}{\sigma}", font_size=34, colors={r"W^Q_t = W_t + \lambda t": Q_C}),
                cmath(r"Z_T = \frac{dQ}{dP}", r"=", r"e^{-\lambda W_T - \frac12\lambda^2 T}", font_size=36,
                      colors={r"Z_T = \frac{dQ}{dP}": Q_C}),
                cmath(r"V_0", r"=", r"\mathbb{E}^P\!\left[Z_T\, \frac{X}{B_T}\right] = \mathbb{E}^Q\!\left[\frac{X}{B_T}"
                      r"\right],\qquad \mathbb{E}^P[Z_T^2] = e^{\lambda^2 T}", font_size=32, colors={r"V_0": CALL})]
        whys = [why(r"the stock under the real measure $P$: drift $\mu$", 21),
                why(r"discount by the bank account $B_t = e^{rt}$: the product rule", 21),
                why(r"absorb the excess drift into the noise: $\lambda$ is the market price of risk", 21),
                why(r"Girsanov: under this density, $W^Q$ is a Brownian motion", 21),
                why(r"constant coefficients give a mean-one density; weight dispersion affects efficiency, while the weighted payoff variance determines pricing error", 21)]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-0.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Continuous-time state prices come from Girsanov's theorem. The stock grows at mu under P. <bookmark mark='a'/> Discounted, it drifts at mu minus r. <bookmark mark='b'/> Fold the excess drift into the noise, shifted by lambda, the market price of risk: the discounted stock becomes a martingale. <bookmark mark='c'/> Girsanov: the new noise is Brownian under this exponential density. <bookmark mark='d'/> So a price is a weighted P-expectation, or a plain Q-expectation; weight dispersion affects Monte Carlo efficiency; weighted-payoff variance determines error. For our numbers, ten percent drift and twenty-five percent volatility, lambda is zero point four: each unit of risk earns zero point four units of excess return. Assume a finite horizon, constant sigma greater than zero, and the bank account starting at one. Constant lambda satisfies Novikov, so the density has mean one. Pricing equality here is for integrable claims in this complete Brownian model. The variance of the weighted payoff, not the weight alone, determines Monte Carlo error."
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.3)
        self.clear_scene()

    def reweight(self, g):
        t, paths, Z = np.asarray(g["t"]), np.asarray(g["paths"]), np.asarray(g["Zp"])
        gr = axes([0, 1.0], [30, 285], x_length=7.4, y_length=4.8, xlabel=r"time (years)", ylabel=r"stock price",
                  xticks=[0, 0.5, 1.0], yticks=[50, 100, 150, 200], font_size=16)
        gr.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = gr.ax
        w = ValueTracker(0.0)
        zs = Z / Z.max()

        def fan():
            a = w.get_value()
            out = VGroup()
            for row, z in zip(paths, zs):
                op = (1 - a) * 0.35 + a * min(0.08 + 0.9 * z, 1.0)
                sw = (1 - a) * 1.2 + a * (0.4 + 3.0 * z)
                col = interpolate_color(ManimColor(P_C), ManimColor(Q_C), a)
                m = VMobject(stroke_width=sw, stroke_color=col, stroke_opacity=op)
                m.set_points_as_corners([ax.c2p(x, y) for x, y in zip(t, row)])
                out.add(m)
            return out

        F_ = always_redraw(fan)
        mean = always_redraw(lambda: curve(ax, t, (1 - w.get_value()) * np.asarray(g["mean_P"]) +
                                           w.get_value() * np.asarray(g["mean_Q"]),
                                           interpolate_color(ManimColor(P_C), ManimColor(Q_C), w.get_value()),
                                           stroke_width=5))
        s0 = DashedLine(ax.c2p(0, 100), ax.c2p(1, 100), color=GREY_B, stroke_width=1.5)
        ST = np.asarray(g["ST"])
        Zs = np.asarray(g["Z"])
        bins = np.linspace(30, 285, 40)
        hp, _ = np.histogram(ST, bins)
        hq, _ = np.histogram(ST, bins, weights=Zs)
        hq = hq / Zs.sum() * len(ST)
        scale = max(hp.max(), hq.max())
        hp, hq = hp / scale, hq / scale

        def side():
            a = w.get_value()
            h = (1 - a) * hp + a * hq
            col = interpolate_color(ManimColor(P_C), ManimColor(Q_C), a)
            x0 = ax.get_right()[0] + 0.15
            return VGroup(*[Rectangle(width=1.3 * v, height=ax.c2p(0, bins[1])[1] - ax.c2p(0, bins[0])[1] - 0.01,
                                      stroke_width=0, fill_color=col, fill_opacity=0.75).move_to(
                [x0 + 0.65 * v, (ax.c2p(0, bins[i])[1] + ax.c2p(0, bins[i + 1])[1]) / 2, 0]) for i, v in enumerate(h)
                if v > 0])

        SD = always_redraw(side)
        lab = VGroup(label(r"amber: 150 paths under $P$, drift 10\% a year", font_size=20, color=P_C),
                     label(r"purple: the same paths, each weighted by $Z_T$", font_size=20, color=Q_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.35)
        ml = label(r"thick line: the (weighted) average path", font_size=19, color=GREY_A).next_to(lab, DOWN, buff=0.15,
                                                                                                  aligned_edge=LEFT)
        src = illustration(rf"simulated: $\mu = {100 * g['mu']:.0f}\%$, $\sigma = {100 * g['sigma']:.0f}\%$, $r = 0$")
        with self.voiceover(
            "Here is what a change of measure looks like. A hundred and fifty stock paths under the real measure, with ten percent drift a year; their average, the thick line, climbs, and on the right, where they end. <bookmark mark='a'/> Now move no path. Give each one the weight Girsanov prescribes, which depends only on where its noise ended: paths that rose a lot thin out, paths that fell thicken. <bookmark mark='b'/> The weighted average flattens onto today's price: under Q the stock is a fair game. The histogram of endings slides from P to Q. Nothing about the paths changed, only how much each one counts. The Q-density is the P-density times the weight, and its mean is today's price, a hundred. Stroke widths rescale weights by their largest value for visibility. The two terminal histograms use one common probability scale and include all simulated observations. The terminal histograms use twenty thousand stored terminal observations; the visible fan and its weighted average use a hundred and fifty paths. That finite average need not be exactly flat."
        ) as vo:
            self.add(F_, mean)
            self.play(FadeIn(gr), Create(s0), FadeIn(lab[0]), FadeIn(ml), FadeIn(src))
            self.add(SD)
            vo.wait_until("a")
            self.play(FadeIn(lab[1]))
            self.play(w.animate.set_value(0.6), run_time=3)
            vo.wait_until("b")
            self.play(w.animate.set_value(1.0), run_time=2.5)
            for m in (F_, mean, SD):
                m.clear_updaters()
        for m in (F_, mean, SD):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def result(self, g):
        z = (g["price_weighted"] - g["bs"]) / g["se"]
        verdict = (r"within two standard errors of Black--Scholes" if abs(z) < 2 else
                   r"more than two standard errors from Black--Scholes")
        rows = VGroup(
            MathTex(rf"\text{{unweighted }} P\text{{-average: }} {g['price_naive']:.3f}", font_size=32, color=P_C),
            MathTex(rf"\text{{weighted by }} Z_T:\ {g['price_weighted']:.3f} \pm {g['se']:.3f}", font_size=34, color=Q_C),
            MathTex(rf"\text{{Black--Scholes: }} {g['bs']:.3f}", font_size=32, color=CALL),
            label(verdict, font_size=26, color=Q_C),
            MathTex(rf"\text{{effective sample: }} {100 * g['ess']:.1f}\%\ \text{{measured}},\ \ e^{{-\lambda^2 T}} = "
                    rf"{100 * g['ess_pred']:.1f}\%\ \text{{predicted}}", font_size=30, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.2)
        head = label(rf"{g['n']:,} simulated paths, an at-the-money call".replace(",", "{,}"), font_size=28).to_edge(UP, buff=0.5)
        tail = ("Within two standard errors. " if abs(z) < 2 else "More than two standard errors away: worth a second look. ")
        with self.voiceover(
            f"With {g['n']:,} paths, the plain average payoff is {g['price_naive']:.2f}: the wrong price, ignoring risk. <bookmark mark='a'/> Weighted, {g['price_weighted']:.2f}, standard error {g['se']:.3f}, against Black and Scholes' {g['bs']:.2f}. {tail}<bookmark mark='b'/> The effective sample is {100 * g['ess']:.1f} percent of the paths; the formula predicted {100 * g['ess_pred']:.1f}. The unweighted average is too high because under P the stock drifts up ten percent a year: it prices the call as if that drift were free. The effective-sample formula is the large-sample relative limit; finite samples fluctuate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
        self.wait(0.3)
        self.clear_scene()

    def predict(self, g):
        card = pause_at(r"Raise the drift to 60\% a year, everything else the same. What happens to the weights?")
        with self.voiceover(
            "Pause and predict. Raise the drift to sixty percent. What happens to the weights? "
            f"<bookmark mark='a'/> They collapse: the effective sample falls to about {100 * g['ess60_pred']:.1f} "
            f"percent, measured {100 * g['ess60']:.1f}. A few paths carry the price, which is why "
            "pricers simulate under Q."
            " Continuous time brings new ways to cheat. Next: free lunches, doubling and bubbles."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, rf"they degenerate: $\lambda = 2.4$, effective sample $e^{{-5.76}} "
                                                rf"\approx {100 * g['ess60_pred']:.1f}\%$ (measured "
                                                rf"{100 * g['ess60']:.1f}\%)")))
        self.wait(0.4)
        self.clear_scene()
