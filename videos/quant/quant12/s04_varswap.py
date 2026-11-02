from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, load, real_data


class VarSwap(VoiceoverScene):
    def construct(self):
        w = load("varswap")
        self.card()
        self.replicate()
        self.strip(w)

    def card(self):
        c = chapter_card(4, r"Variance swaps and the VIX", r"How do you buy volatility itself?", part=PART)
        with self.voiceover("Chapter four. Variance swaps, and the VIX."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def replicate(self):
        rows = [cmath(r"\int_0^T \sigma_t^2\,dt", r"=", r"2\int_0^T \frac{dS_t}{S_t} - 2\log\frac{S_T}{S_0}", font_size=34,
                      colors={r"\int_0^T \sigma_t^2\,dt": RV}),
                cmath(r"-\log\frac{S_T}{F}", r"=", r"-\frac{S_T - F}{F} + \int_0^F \frac{(K - S_T)^+}{K^2}dK + \int_F^\infty "
                      r"\frac{(S_T - K)^+}{K^2}dK", font_size=30, colors={r"-\log\frac{S_T}{F}": OPT}),
                cmath(r"K_{\text{var}}", r"=", r"\frac{2}{T}\int_0^\infty \frac{\text{OTM}(K)}{K^2}\,dK", font_size=36,
                      colors={r"K_{\text{var}}": IV})]
        whys = [why(r"It\^o (Part 5): realized variance is a delta-hedging gain minus a log contract; the hedge is free, "
                    r"so variance costs what the log contract costs"),
                why(r"Carr and Madan (1998): any payoff is a strip of options; the log contract is out-of-the-money options "
                    r"weighted by $1/K^2$"),
                why(r"the fair variance strike (Demeterfi, Derman, Kamal and Zou 1999); the VIX is this integral on the "
                    r"S\&P 500's options, since 2003")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Part eleven's straddle paid realized variance only near the strike. A variance swap pays it everywhere: "
            "at expiry, realized variance minus a fixed strike. How do you hedge one? Itô's formula, from Part five, "
            "splits realized variance into the gains of a simple hedge and a log contract. <bookmark mark='a'/> And "
            "Peter Carr and Dilip Madan showed that any payoff is a strip of options: the log contract is all the "
            "out-of-the-money options, each weighted by one over the strike squared. <bookmark mark='b'/> So the fair "
            "variance is a weighted sum of option prices. This is exactly what the VIX index has computed from the "
            "options on the S&P 500 since 2003."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def strip(self, w):
        K, wt, otm = np.asarray(w["K"]), np.asarray(w["weights"]), np.asarray(w["otm"])
        F = w["F"]
        m = (K > 0.4 * F) & (K < 1.8 * F)
        contrib = otm / K ** 2
        contrib = contrib / contrib[m].max()
        g = axes([0.4 * F, 1.8 * F], [0, 1.05], x_length=7.0, y_length=3.8, xlabel=r"strike (\$)",
                 ylabel=r"each option's share of the variance strike", xticks=[50000, 100000, 150000],
                 xfmt=lambda u: f"{u / 1000:.0f}k", yticks=[0, 0.5, 1], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        Km = K[m][::10]
        cm = contrib[m][::10]
        bars = VGroup(*[Line(ax.c2p(x, 0), ax.c2p(x, y), color=IV if x > F else BAD, stroke_width=3) for x, y in zip(Km, cm)])
        wl = curve(ax, K[m], np.clip(wt[m] / wt[m].max(), 0, 1.05), GREY_B, stroke_width=1.5)
        side = VGroup(
            label(r"puts below the forward, calls above, weighted by $1/K^2$", font_size=21, color=GREY_A),
            MathTex(rf"\sqrt{{K_{{\text{{var}}}}}} = {100 * w['kvar']:.1f}\%\quad \text{{vs ATM }} {100 * w['atm']:.1f}\%",
                    font_size=30, color=IV),
            wrapped_label(r"the variance strike sits above at-the-money vol: the strip owns the expensive downside "
                          r"wing, a convexity and skew premium", 4.2, 20, GREY_A),
            MathTex(rf"\text{{our VIX recipe: }} {100 * w['our_vix']:.1f}\%\quad \text{{DVOL: }} {100 * w['dvol']:.1f}\%",
                    font_size=30, color=OPT),
            wrapped_label(r"Deribit's DVOL applies the same recipe to its own quotes; the gap is most likely the wings: "
                          r"our fit extrapolates them, an index stops where quotes stop", 4.2, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(r"30-day strip from the SSVI fit to the Surface; DVOL at 08:00 UTC, 10 December 2025")
        with self.voiceover(
            "Here is the strip for thirty-day Bitcoin variance on the Surface. Puts below the forward, calls above, "
            "each weighted by one over its strike squared, so the downside options carry the most weight. "
            f"<bookmark mark='a'/> The fair variance strike, as a volatility, is {100 * w['kvar']:.1f} percent, above "
            f"the at-the-money {100 * w['atm']:.1f}: the strip owns the expensive downside wing. <bookmark mark='b'/> "
            "Apply the VIX's own recipe to the Surface, at Deribit's strikes, interpolated to thirty days, and you get "
            f"{100 * w['our_vix']:.1f} percent. Deribit's own index, DVOL, read {100 * w['dvol']:.1f} at the same "
            "moment. The likely difference is the wings: how far beyond the last quotes each method reaches."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(wl), FadeIn(side[0]))
            self.play(LaggedStart(*[Create(b_) for b_ in bars], lag_ratio=0.02, run_time=2))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
