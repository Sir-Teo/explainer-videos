from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load


class LocalVol(VoiceoverScene):
    def construct(self):
        lv = load("localvol")
        self.card()
        self.dupire()
        self.forward(lv)

    def card(self):
        c = chapter_card(3, r"Local volatility", r"Which single model reprices the whole surface?", lit=(1994,), part=PART)
        with self.voiceover("Chapter three. Dupire's local volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def dupire(self):
        rows = [cmath(r"\frac{dS}{S}", r"=", r"\sigma_{\text{loc}}(S, t)\,dW", font_size=36, colors={r"\frac{dS}{S}": SPOT}),
                cmath(r"\sigma_{\text{loc}}^2(K, T)", r"=", r"\frac{\partial_T C}{\tfrac12 K^2\,\partial_{KK} C} = "
                      r"\frac{\partial_T w}{g(k)}", font_size=36, colors={r"\sigma_{\text{loc}}^2(K, T)": LV}),
                cmath(r"\sigma_{\text{loc}}^2(K, T)", r"=", r"\mathbb{E}^Q\big[\sigma_T^2 \mid S_T = K\big]", font_size=34,
                      colors={r"\sigma_{\text{loc}}^2(K, T)": LV})]
        whys = [why(r"let volatility depend on the price and the date, and nothing else; Derman and Kani built it on a "
                    r"tree the same year"),
                why(r"Dupire (1994): there is exactly one such function that reprices every option, read off the surface's "
                    r"slopes; the denominator is Part 9's density"),
                why(r"Gy\"ongy (1986): any model with random volatility has a local-volatility twin with the same vanilla "
                    r"prices: the conditional expectation of its variance")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Can one model reprice every option on the surface at once? In 1994 Bruno Dupire, and Emanuel Derman "
            "and Iraj Kani on a tree, gave the same answer. Let volatility depend only on the price and the date. "
            "<bookmark mark='a'/> Then there is exactly one such function that matches every vanilla price, and it "
            "can be read off the surface: the slope of call prices in maturity, over their curvature in strike. "
            "<bookmark mark='b'/> Gyöngy's theorem says why it works: any model with random volatility has a "
            "local-volatility twin with the same vanilla prices, whose variance is the expected variance given "
            "where the price ends up."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def forward(self, lv):
        k, T, L = np.asarray(lv["k"]), np.asarray(lv["T"]), np.asarray(lv["lv"])
        g1 = axes([-0.4, 0.4], [0.2, 1.0], x_length=5.6, y_length=3.6, xlabel=r"log-moneyness",
                  ylabel=r"local volatility", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.2, 0.6, 1.0],
                  yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=16)
        g2 = axes([-0.25, 0.25], [0.3, 0.7], x_length=5.6, y_length=3.6, xlabel=r"log-moneyness of a 30-day option",
                  ylabel=r"implied volatility", xticks=[-0.2, 0, 0.2], yticks=[0.4, 0.5, 0.6], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.8)
        cols = [BAD, IV, OPT, LV]
        sel = [0, 2, 3, 5]
        lines = VGroup(*[curve(g1.ax, k, np.clip(L[i], 0.2, 1.0), c, stroke_width=2.5) for i, c in zip(sel, cols)])
        leg = legend([(c, f"{T[i] * 365:.0f} days") for i, c in zip(sel, cols)], font_size=16).next_to(g1, DOWN, buff=0.2)
        fk = np.asarray(lv["fwd_k"])
        today = curve(g2.ax, fk, np.asarray(lv["spot_iv_30d"]), IV, stroke_width=3)
        fwd = curve(g2.ax, fk, np.asarray(lv["fwd_iv"]), LV, stroke_width=3)
        leg2 = legend([(IV, r"today's 30-day smile"), (LV, r"local vol's smile, 60 days from now")], font_size=16).next_to(
            g2, DOWN, buff=0.2)
        note_ = wrapped_label(rf"skew (90\% minus 110\% strike): today {100 * lv['spot_skew']:.1f} vol points, in 60 days "
                              rf"{100 * lv['fwd_skew']:.1f}. Local vol says the smile will flatten; real smiles keep "
                              r"theirs, so local vol misprices anything that depends on future smiles (Part 13)", 11.0, 21,
                              GREY_A).to_edge(DOWN, buff=0.4)
        src = illustration(r"Dupire from the SSVI fit to the Surface; forward smile by Monte Carlo, 40{,}000 paths")
        with self.voiceover(
            "Here is the Surface's local volatility, read from the fitted SSVI. It is steeper than the implied "
            "smile it came from: local volatility changes twice as fast with the strike as implied does. "
            "<bookmark mark='a'/> It reprices today's options perfectly. The trouble is tomorrow. Simulate the model "
            "and ask what thirty-day smile it predicts sixty days from now: the forward smile. "
            "<bookmark mark='b'/> It is much flatter than today's. Real markets keep their skew; local volatility "
            "predicts it will fade. So it misprices anything whose value depends on future smiles, like forward-start "
            "options and cliquets, and that is why Part thirteen's stochastic volatility exists."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), FadeIn(leg),
                      run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(today), FadeIn(leg2[0]))
            vo.wait_until("b")
            self.play(Create(fwd), FadeIn(leg2[1]), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
