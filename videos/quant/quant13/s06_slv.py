from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load


class SLV(VoiceoverScene):
    def construct(self):
        s = load("slv")
        self.card()
        self.model()
        self.leverage(s)

    def card(self):
        c = chapter_card(5, r"Stochastic local volatility", r"Can one model fit today's smile and keep tomorrow's?",
                         part=PART)
        with self.voiceover("Chapter five. Stochastic local volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"\frac{dS}{S}", r"=", r"L(S, t)\,\sqrt{v_t}\,dW^1_t,\qquad dv_t = \kappa(\theta - v_t)\,dt + "
                      r"\xi\sqrt{v_t}\,dW^2_t", font_size=34, colors={r"\frac{dS}{S}": SPOT}),
                cmath(r"\sigma^2_{\text{loc}}(S, t)", r"=", r"L^2(S, t)\ \mathbb{E}\big[v_t \mid S_t = S\big]", font_size=36,
                      colors={r"\sigma^2_{\text{loc}}(S, t)": MODEL_COL["LV"]}),
                cmath(r"L(S, t)", r"=", r"\frac{\sigma_{\text{loc}}(S, t)}{\sqrt{\sum_i v^i_t\,K_h(S^i_t - S) \,/\, "
                      r"\sum_i K_h(S^i_t - S)}}", font_size=34, colors={r"L(S, t)": MODEL_COL["SLV"]})]
        whys = [why(r"Heston's variance, scaled by a leverage function $L$ of the price and the date"),
                why(r"Gy\"ongy's theorem (chapter 3 of Part 12): the model reprices every vanilla exactly when this holds"),
                why(r"Guyon and Henry-Labord\`ere (2012): simulate many particles together, and estimate the conditional "
                    r"expectation across them, step by step, with a kernel $K_h$: the particle method")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.85, edge=6.9)
        with self.voiceover(
            "Local volatility fits today's surface exactly, and predicts the wrong future. Stochastic volatility gets "
            "the future's shape about right, and misses today by a point or more. Desks want both, so they multiply. "
            "Take Heston's variance and scale it by a leverage function of the price and the date. "
            "<bookmark mark='a'/> Gyöngy's theorem, from Part twelve, says exactly when such a model reprices every "
            "vanilla: when the leverage squared, times the expected variance given the price, equals Dupire's local "
            "variance. <bookmark mark='b'/> The catch is that the expectation depends on the model's own "
            "distribution, which depends on the leverage. Julien Guyon and Pierre Henry-Labordère cut the knot in "
            "2012: simulate a crowd of particles together, and at every step estimate the expectation across the "
            "crowd itself. The model calibrates while it simulates."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def leverage(self, s):
        grid = np.asarray(s["grid"])
        Ls = s["L"]
        pick = [i for i, x in enumerate(Ls) if round(x["t"] * 365) in (10, 30, 60, 120)]
        cols = [BAD, IV, OPT, VAR]
        g = axes([-0.5, 0.5], [0.4, 2.2], x_length=6.0, y_length=4.0, xlabel=r"log-moneyness $\ln S/S_0$",
                 ylabel=r"leverage $L(S, t)$", xticks=[-0.4, -0.2, 0, 0.2, 0.4], yticks=[0.5, 1.0, 1.5, 2.0], font_size=16)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        m = np.abs(grid) <= 0.5
        lines = VGroup(*[curve(g.ax, grid[m], np.clip(np.asarray(Ls[i]["L"])[m], 0.4, 2.2), c, stroke_width=2.6)
                         for i, c in zip(pick, cols)])
        leg = legend([(c, rf"day {round(Ls[i]['t'] * 365)}") for i, c in zip(pick, cols)], font_size=17)
        leg.arrange(RIGHT, buff=0.35).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        rep = s["reprice"]
        tab = VGroup(label(r"repricing the Surface's smile (13 strikes)", font_size=20, color=GREY_A),
                     *[MathTex(rf"{r['days']}\ \text{{days: }} {r['err']:.2f}\ \text{{vol points}}", font_size=28)
                       for r in rep]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        note_ = wrapped_label(r"with half of Heston's vol of vol (the mixing fraction), 40{,}000 particles, four steps a "
                              r"day; the rest of the error is Monte Carlo and the finite-difference local vol, and shrinks "
                              r"with more of both", 4.4, 18, GREY_A)
        side = VGroup(tab, note_).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        src = illustration(r"the House's particle method on the SSVI local vol of the Surface; Heston from chapter 2")
        with self.voiceover(
            "Here is the leverage function the particles found for the Surface, at four dates. It is below one near "
            "the money and above it in the wings, most of all at short dates: where Heston's own variance is too "
            "calm to match the local volatility, the leverage turns it up, and where it is too wild, down. <bookmark mark='a'/> And the model "
            "reprices the Surface's smile to under a volatility point at every horizon. The remaining error is "
            "simulation noise and the finite differences in the local volatility. <bookmark mark='b'/> One knob is "
            "left: how much of the volatility comes from the random variance and how much from the leverage. That "
            "mixing fraction does not change today's prices at all. It decides tomorrow's smile, and in chapter "
            "seven, the price of an exotic."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=3),
                      FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3, run_time=2))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
