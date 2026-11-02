from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, CALL, FWD, PART, PUT, Q_C, load, real_data


class Density(VoiceoverScene):
    def construct(self):
        d = load("density")
        self.card()
        self.formula()
        self.surface(d)

    def card(self):
        c = chapter_card(5, r"The density inside the Surface", r"What does the market think could happen?", lit=(1978,),
                         part=PART)
        with self.voiceover("Chapter five. The density inside the Surface."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def formula(self):
        rows = [cmath(r"C(K)", r"=", r"e^{-rT}\int_K^\infty (s - K)\, q(s)\, ds", font_size=36, colors={r"C(K)": CALL}),
                cmath(r"q(K)", r"=", r"e^{rT}\,\frac{\partial^2 C}{\partial K^2}", font_size=40, colors={r"q(K)": Q_C})]
        whys = [why(r"a call is an expectation under $Q$ of the payoff above the strike"),
                why(r"differentiate twice in the strike: the risk-neutral density is the curvature of call prices "
                    r"(Breeden and Litzenberger 1978); a butterfly spread buys it directly")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=1.0, edge=6.9)
        with self.voiceover(
            "If prices are expectations under Q, then the prices of calls at every strike tell us Q itself. A call "
            "is the expected payoff above its strike. <bookmark mark='a'/> Differentiate twice with respect to the "
            "strike and the payoff's kink becomes a spike: the second derivative of call prices is the risk-neutral "
            "density. Douglas Breeden and Robert Litzenberger showed this in 1978. In trading terms, a tight "
            "butterfly spread pays only if the price ends near its middle strike, so its price is the density there."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def surface(self, d):
        a, b = d["expiries"]
        g1 = axes([50000, 150000], [0.2, 1.2], x_length=5.6, y_length=2.6, ylabel=r"implied volatility",
                  xticks=[60000, 90000, 120000, 150000], xfmt=lambda u: f"{u / 1000:.0f}k", yticks=[0.4, 0.8, 1.2],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g2 = axes([30000, 180000], [0, 1.0], x_length=5.6, y_length=2.6, ylabel=r"risk-neutral density (scaled)",
                  xlabel=r"bitcoin price at expiry (\$)", xticks=[50000, 100000, 150000], xfmt=lambda u: f"{u / 1000:.0f}k",
                  yticks=[], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.7).shift(DOWN * 0.1)
        cols = [ALT, Q_C]
        smiles, dots, dens = VGroup(), VGroup(), VGroup()
        top = max(max(e["density"]) for e in (a, b))
        for e, c in zip((a, b), cols):
            K = np.asarray(e["K"])
            ok = (K > 50000) & (K < 150000)
            smiles.add(curve(g1.ax, K[ok], np.clip(np.asarray(e["iv_fit"])[ok], 0.2, 1.2), c, stroke_width=3))
            kq, iq = np.asarray(e["K_quotes"]), np.asarray(e["iv_quotes"])
            ok2 = (kq > 50000) & (kq < 150000) & (iq < 1.2)
            dots.add(VGroup(*[Dot(g1.ax.c2p(x, y), radius=0.035, color=WHITE) for x, y in zip(kq[ok2], iq[ok2])]))
            ok3 = (K > 30000) & (K < 180000)
            dens.add(curve(g2.ax, K[ok3], np.asarray(e["density"])[ok3] / top, c, stroke_width=3.5))
        leg = legend([(ALT, rf"{a['expiry']}: {a['T'] * 365:.0f} days"), (Q_C, rf"{b['expiry']}: {b['T'] * 365:.0f} days")],
                     font_size=19).next_to(g1, UP, buff=0.1).align_to(g1, LEFT)
        side = VGroup(
            wrapped_label(r"each expiry's quotes fitted by SVI (Part 1), then differentiated twice", 4.4, 20, GREY_A),
            MathTex(rf"{a['T'] * 365:.0f}\text{{ days: down 20\%: }} {100 * a['p_down20']:.1f}\%,\ \text{{up 20\%: }} "
                    rf"{100 * a['p_up20']:.1f}\%", font_size=25, color=ALT),
            MathTex(rf"{b['T'] * 365:.0f}\text{{ days: down 20\%: }} {100 * b['p_down20']:.1f}\%,\ \text{{up 20\%: }} "
                    rf"{100 * b['p_up20']:.1f}\%", font_size=25, color=Q_C),
            wrapped_label(r"a 20\% fall is further than a 20\% rise in log terms, yet no less likely: the smile's skew is "
                          r"this asymmetry, in other units", 4.4, 20, GREY_A),
            wrapped_label(r"the checker passes both: calls decreasing and convex in the strike, within their bounds, and "
                          r"total variance rising with maturity", 4.4, 20, CALL),
            wrapped_label(r"$Q$ is not a forecast: it weights the crash states more than their real chances", 4.4, 20,
                          PUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.4)
        src = real_data(r"the Surface: Deribit BTC options, 10 December 2025, 08:00 UTC")
        with self.voiceover(
            "Here it is on the Surface, the frozen day of Bitcoin options this series prices against. Two expiries: "
            f"one in {a['T'] * 365:.0f} days, one in {b['T'] * 365:.0f}. The dots are the market's implied "
            "volatilities, the lines are smooth fits. <bookmark mark='a'/> Differentiate the fitted call prices twice, "
            "and the density emerges: the market's risk-neutral distribution of Bitcoin's price at each expiry. "
            "The later one is wider, as it must be. <bookmark mark='b'/> Read off a number: the risk-neutral chance "
            f"of a fall of twenty percent or more is {100 * a['p_down20']:.1f} percent within {a['T'] * 365:.0f} days, "
            f"and {100 * b['p_down20']:.0f} percent within {b['T'] * 365:.0f}, at least as likely as a rise of twenty "
            "percent, though a fall that size is the bigger move in log terms. That asymmetry is the smile's skew, "
            "in other units. <bookmark mark='c'/> The House's checker "
            "passes both expiries: no negative butterflies, no calendar arbitrage. And a reminder: Q weights the "
            "crash states more heavily than their real chances. It is a price, not a forecast."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(leg), FadeIn(src), FadeIn(dots), Create(smiles), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(dens), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()
