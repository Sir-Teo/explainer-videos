from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, pause

CARDS = [
    (2023, r"Bayer and Breneis (Quantitative Finance 23(1))",
     r"Markovian approximations of Volterra equations with the fractional kernel: Gaussian-quadrature nodes, error "
     r"falling faster than any power of $N$ (chapter 10)."),
    (2023, r"Bolko, Christensen, Pakkanen and Veliyev",
     r"GMM with the realized-variance error corrected: $H \approx 0.05$ (chapter 11)."),
    (2024, r"Chong, Hoffmann, Liu, Rosenbaum and Szymanski",
     r"Minimax rates and central limit theorems for estimating $H$ (chapter 11)."),
    (2024, r"Cont and Das", r"The estimator's artefact: smooth volatility can read as rough (chapter 11)."),
    (2024, r"Guyon (Finance and Stochastics 28(1))",
     r"The dispersion-constrained martingale Schr\"odinger problem: an exact joint S\&P 500/VIX fit (chapter 15)."),
    (2024, r"Nutz and Riveros Valdevenito; Andr\`es and Jourdain",
     r"The path-dependent volatility SDE is well posed (chapter 13)."),
    (2025, r"Abi Jaber and Li (Mathematical Finance 35(4))",
     r"Rough, path-dependent or Markovian? On SPX smiles, rough loses to path-dependent and two-factor Markov models "
     r"(chapter 12)."),
    (2025, r"Cuchiero, Gazzani, M\"oller and Svaluto-Ferro (Mathematical Finance 35(1))",
     r"Signature models fit SPX and VIX jointly, without jumps or roughness (chapter 16)."),
]


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.ribbon()
        self.theory()
        self.board()

    def card(self):
        c = chapter_card(18, r"The frontier, 2023--2026", r"Where is the field now?", lit=(2024, 2025), part=PART)
        with self.voiceover("Chapter eighteen. The frontier, 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ribbon(self):
        y0, y1, width = 2022.5, 2026.0, 12.4
        X = lambda yr: -width / 2 + width * (yr - y0) / (y1 - y0)  # noqa: E731
        axis = Line([X(y0), 3.0, 0], [X(y1), 3.0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[Text(str(y), font_size=16, color=GREY_B).move_to([X(y + 0.5), 3.3, 0]) for y in (2023, 2024, 2025)])
        cards = VGroup(*[history_card(y, who, what, color=QC.IDEA, width=3.0, font_size=15) for y, who, what in CARDS])
        grid = VGroup(VGroup(*cards[:4]).arrange(RIGHT, buff=0.15, aligned_edge=UP),
                      VGroup(*cards[4:]).arrange(RIGHT, buff=0.15, aligned_edge=UP)).arrange(DOWN, buff=0.2)
        if grid.width > 13.2:
            grid.scale_to_fit_width(13.2)
        if grid.height > 5.9:
            grid.scale_to_fit_height(5.9)
        grid.next_to(axis, DOWN, buff=0.3)
        with self.voiceover(
            "Where is the field now? Eight results from the last three years, each one met in this part. In 2023, "
            "Christian Bayer and Simon Breneis made Markovian approximations converge faster than any power of the "
            "number of factors, and Bolko and co-authors corrected the estimator's error and still found H near "
            "0.05. <bookmark mark='a'/> In 2024 came the minimax theory of Chong, Hoffmann, Liu, Rosenbaum and "
            "Szymanski; Cont and Das's artefact; Guyon's exact joint fit in Finance and Stochastics; and the proofs "
            "that path-dependent volatility is a well-posed model. <bookmark mark='b'/> In 2025, Abi Jaber and Li's "
            "horse race went against one-factor rough models on S&P smiles, and signature models fitted S&P and VIX "
            "jointly. The direction of travel is clear: from one rough factor towards path dependence, several "
            "time scales, and exact constructions."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks))
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cards[:2]], lag_ratio=0.5))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cards[2:6]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in cards[6:]], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def theory(self):
        a = history_card(r"ch.\ 9", r"Friz and Gatheral: the forest expansion of forward variance models",
                         r"An exact series for the smile in powers of vol of vol, organised as forests of trees; chapter 2's "
                         r"first-order skew is its first term. \textit{Rough Volatility} (SIAM 2023), chapter 9.",
                         color=VAR, width=6.2, font_size=19)
        b = history_card(r"ch.\ 10", r"Bayer, Friz, Gassiat, Martin and Stemper: regularity structures",
                         r"Hairer's theory of regularity structures applied to rough volatility: a renormalised Taylor "
                         r"expansion for pricing, where the usual It\^o calculus breaks down. \textit{Rough Volatility} "
                         r"chapter 10; Friz and Hairer (2nd ed., 2020), section 14.5. Beyond this series.",
                         color=VAR, width=6.2, font_size=19)
        g = VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.6)
        q = pause(r"If volatility is a function of the path, is it still rough?", width=7.0, font_size=24).to_edge(DOWN, buff=0.4)
        p = load("pdv")
        with self.voiceover(
            "Two theoretical lines go beyond this course. Peter Friz and Jim Gatheral's forest expansion gives the "
            "smile of any forward variance model as an exact series in the vol of vol: chapter two's skew formula is "
            "its first term. <bookmark mark='a'/> And regularity structures, Martin Hairer's theory, give rough "
            "volatility a rigorous Taylor expansion where ordinary Itô calculus breaks down. <bookmark mark='b'/> "
            "One last question to pause on: if volatility is a function of the path, is it still rough? "
            "<bookmark mark='c'/> It can look rough if the kernel is singular. But Guyon and Lekeufack's fitted "
            "kernels are shifted power laws, bounded at zero lag: on Bitcoin the activity kernel is shifted by "
            f"{365 * p['delta2']:.0f} days. Such a volatility is smooth at the very shortest scales and power-law "
            "beyond them. The two views differ exactly where measurement is hardest."
        ) as vo:
            self.play(FadeIn(a, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(b, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
        self.wait(0.4)
        self.clear_scene()

    def board(self):
        rb, b2, sg, rh = load("rbergomi"), load("bergomi2f"), load("sigvol"), load("rheston")
        rs = load("rbskew")
        pd, p4, ps = load("pdv"), load("pdv4"), load("pdv_spx")
        f = load("rfsv_forecast")
        prices = [(1993, r"Heston", rs["heston_rmse_same"]), (2004, r"two-factor Bergomi", b2["rmse"]),
                  (2016, r"rough Bergomi", rb["rmse"]), (2019, r"rough Heston (free)", rh["rmse"]),
                  (2023, r"signature model", sg["rmse_out"])]
        best = min(prices, key=lambda r: r[2])
        left = VGroup(label(r"pricing the Surface (vol points, fresh paths)", font_size=20, color=GREY_A))
        for y, n_, v in prices:
            left.add(VGroup(MathTex(str(y), font_size=22, color=GREY_B), label(n_, font_size=19),
                            MathTex(f"{v:.2f}", font_size=24, color=YELLOW if v == best[2] else WHITE)).arrange(RIGHT, buff=0.3))
        left.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        right = VGroup(label(r"out of sample, on time series", font_size=20, color=GREY_A),
                       label(rf"2018: rough forecast vs HAR: {f['rough_wins']} of 6 races", font_size=19),
                       label(rf"2023: PDV on DVOL: $R^2$ {pd['r2_test']:.2f} (baseline {pd['r2_base_test']:.2f})", font_size=19),
                       label(rf"2023: 4-factor PDV on DVOL: $R^2$ {p4['r2_test']:.2f}", font_size=19),
                       label(rf"2023: PDV on the VIX: $R^2$ {ps['r2_test']:.2f} (baseline {ps['r2_base_test']:.2f})", font_size=19)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(UP * 0.4)
        if g.width > 13.0:
            g.scale_to_fit_width(13.0)
        with self.voiceover(
            "And the verdict this part's own numbers give, every model by the year of its idea. On pricing one "
            f"day's bitcoin Surface, the lowest error belongs to {best[1]}, at {best[2]:.2f} volatility points. "
            "<bookmark mark='a'/> On the time series, the rough forecast trades blows with HAR, and the "
            "path-dependent models track implied volatility out of sample far better than a realized-volatility "
            f"baseline: {100 * ps['r2_test']:.0f} percent of the VIX. Roughness is a superb description of how "
            "volatility looks; path dependence, of where it comes from in prices. Both are tools, and the House "
            "keeps both, under its fourteenth rule."
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right))
        self.wait(0.5)
        self.clear_scene()
