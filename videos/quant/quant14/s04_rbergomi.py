from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import rough as R
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, SPOT, VAR, illustration, load, real_data


class RBergomi(VoiceoverScene):
    def construct(self):
        rb = load("rbergomi")
        rs = load("rbskew")
        self.card()
        self.model()
        self.scheme(rb)
        self.fit(rb, rs)

    def card(self):
        c = chapter_card(3, r"Rough Bergomi", r"What is the simplest rough model that prices options?", lit=(2016,),
                         part=PART)
        with self.voiceover("Chapter three. Rough Bergomi."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"v_t", r"=", r"\xi_0(t)\,\exp\!\Big(\eta\,W^H_t - \tfrac12\eta^2 t^{2H}\Big)", font_size=38,
                      colors={r"v_t": VAR}),
                cmath(r"\frac{dS}{S}", r"=", r"\sqrt{v_t}\,\big(\rho\,dW_t + \sqrt{1 - \rho^2}\,dW^\perp_t\big)",
                      font_size=38, colors={r"\frac{dS}{S}": SPOT})]
        whys = [why(r"Bayer, Friz and Gatheral (2016): Bergomi's variance curve (Part 13), driven by a rough Volterra "
                    r"process instead of exponentials; $\xi_0$ is read from the market, so the term structure is free"),
                why(r"three numbers: roughness $H$, vol of vol $\eta$, and the correlation $\rho$ that makes the skew")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-1.2, buff=1.0, edge=6.9)
        with self.voiceover(
            "Christian Bayer, Peter Friz and Jim Gatheral wrote down the simplest rough model in 2016. Take Part "
            "thirteen's Bergomi model, whose state is the forward variance curve, and drive it with a rough Volterra "
            "process instead of exponentials. The curve itself comes from the market, so the term structure of "
            "variance is matched by construction. <bookmark mark='a'/> What is left is three numbers: the roughness "
            "H, the vol of vol eta, and the correlation rho that makes the skew. They called it rough Bergomi."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def scheme(self, rb):
        p = rb["params"]
        S, v = R.rbergomi_paths(p["H"], p["eta"], p["rho"], 0.2, 60 / 365, 240, 4, seed=5, return_v=True)
        t = np.linspace(0, 60, 241)
        g1 = axes([0, 60], [0, 2.0], x_length=9.0, y_length=2.6, ylabel=r"volatility $\sqrt{v_t}$", xticks=[0, 20, 40, 60],
                  yticks=[0, 0.5, 1.0, 1.5], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15)
        g2 = axes([0, 60], [0.6, 1.5], x_length=9.0, y_length=2.6, xlabel=r"days", ylabel=r"price", xticks=[0, 20, 40, 60],
                  yticks=[0.8, 1.0, 1.2, 1.4], font_size=15)
        VGroup(g1, g2).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        cols = [ROUGH, IV, RV, OPT]
        lv = VGroup(*[curve(g1.ax, t, np.clip(np.sqrt(v[:, i]), 0, 2.0), c, stroke_width=1.6) for i, c in enumerate(cols)])
        ls = VGroup(*[curve(g2.ax, t, np.clip(S[:, i], 0.6, 1.5), c, stroke_width=2) for i, c in enumerate(cols)])
        side = VGroup(
            wrapped_label(r"no Markov state and no closed form: it must be simulated, and the kernel blows up at zero lag", 3.6,
                          19, GREY_A),
            wrapped_label(r"Bennedsen, Lunde and Pakkanen's hybrid scheme (2017): the singular first step exactly, the rest "
                          r"as a convolution by FFT, $O(n\log n)$ a path", 3.6, 19, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = illustration(rf"four paths, $H = {p['H']:.2f}$, $\eta = {p['eta']:.1f}$, $\rho = {p['rho']:.2f}$, flat "
                           r"variance curve, 4 steps a day")
        with self.voiceover(
            "The price of that simplicity is that rough Bergomi has no Markov state and no closed form. It must be "
            "simulated, and the kernel blows up at zero lag, which breaks naive schemes. <bookmark mark='a'/> Mikkel "
            "Bennedsen, Asger Lunde and Mikko Pakkanen's hybrid scheme integrates the singular first step exactly and "
            "the rest as a convolution, computed by fast Fourier transform. Here are four paths with the parameters "
            "fitted to the Surface: the volatility on top is jagged at every scale, and its spikes come with falls."
        ) as vo:
            self.play(FadeIn(side[0]), FadeIn(g1), FadeIn(g2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), LaggedStart(*[AnimationGroup(Create(a), Create(b)) for a, b in zip(lv, ls)],
                                                   lag_ratio=0.3, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def fit(self, rb, rs):
        p = rb["params"]
        tab = VGroup(
            MathTex(rf"H = {p['H']:.2f},\quad \eta = {p['eta']:.2f},\quad \rho = {p['rho']:.2f}", font_size=36,
                    color=MODEL_COL["rBergomi"]),
            MathTex(rf"\text{{error}}\ {rb['rmse']:.2f}\ \text{{vol points}}\ \ (\text{{{rb['n']} quotes, up to 200 days}})",
                    font_size=30),
            wrapped_label(rf"fitted by least squares on {rb['n_paths']:,} simulated paths with common random numbers, then "
                          r"re-priced on fresh paths; the forward variance curve is Part 13's, from variance swaps",
                          10.0, 20, GREY_A),
            wrapped_label(rf"on the same quotes, Part 13's Heston misses by {rs['heston_rmse_same']:.2f}, with five free numbers "
                          r"and a vol of vol of 460\%", 10.0, 20, GREY_A),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        src = real_data(r"the Surface, 10 December 2025")
        with self.voiceover(
            "Fit it to the Surface, by least squares on twenty thousand simulated paths, and price again on fresh "
            "paths to make sure the fit is not an artefact of the random numbers. <bookmark mark='a'/> Roughness "
            f"comes out at {p['H']:.2f}, with a vol of vol of {p['eta']:.1f} and a correlation of {p['rho']:.2f}. The "
            f"error is {rb['rmse']:.2f} volatility points. On the same quotes, Part thirteen's Heston misses by "
            f"{rs['heston_rmse_same']:.2f}, with five free numbers and an absurd vol of vol."
        ) as vo:
            self.play(FadeIn(tab[2]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()
