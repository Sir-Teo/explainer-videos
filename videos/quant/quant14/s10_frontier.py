from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, pause

CARDS = [
    (2023, r"Bayer and Breneis (Quantitative Finance 23(1))",
     'Gaussian-quadrature Markovian approximations: superpolynomial strong convergence for fractional-kernel equations with Lipschitz coefficients. Not the geometric lift\\textquotesingle s universal rate.'),
    (2023, r"Bolko, Christensen, Pakkanen and Veliyev",
     r"GMM with the realized-variance error corrected: $H \approx 0.05$ (chapter 11)."),
    (2024, r"Chong, Hoffmann, Liu, Rosenbaum and Szymanski",
     r"Minimax rates and central limit theorems for estimating $H$ (chapter 11)."),
    (2024, r"Cont and Das", 'Brownian-regular variance can give low daily-proxy scaling estimates (chapter 11).'),
    (2024, r"Guyon (Finance and Stochastics 28(1))",
     r"The dispersion-constrained martingale Schr\"odinger problem: an exact joint S\&P 500/VIX fit (chapter 15)."),
    (2024, 'Nutz and Riveros Valdevenito (2024); Andr\\`es and Jourdain (2025)',
     'Well-posedness under stated parameter, kernel and initial-state assumptions; positivity and martingality require separate results.'),
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
        c = chapter_card(18, 'Selected research, 2023--2025', r"Where is the field now?", lit=(2024, 2025), part=PART)
        with self.voiceover("""Chapter eighteen. Selected research, 2023 to 2025."""):
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
            """Selected results published from 2023 through 2025. Bayer and Breneis obtain superpolynomial strong convergence for a Gaussian-quadrature approximation under Lipschitz-coefficient assumptions. It is not a theorem about our geometric lift for every nonlinear volatility equation. Bolko and co-authors study error-corrected roughness estimation. <bookmark mark='a'/> The 2024 studies include minimax estimation, estimator artifacts, Guyon's constrained joint calibration, and Nutz and Riveros Valdevenito's four-factor existence result. General-kernel conditions are developed by Andrès and Jourdain, with a 2025 version. <bookmark mark='b'/> The 2025 SPX model comparison and joint signature models widen the alternatives. These selected studies compare particular models, data and assumptions; they do not establish that all rough models are either necessary or obsolete."""
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
                         'Forest-organized expansions for forward-variance models; leading small-vol-of-vol skew is one application. Truncation and convergence need their own assumptions.',
                         color=VAR, width=6.2, font_size=19)
        b = history_card(r"ch.\ 10", r"Bayer, Friz, Gassiat, Martin and Stemper: regularity structures",
                         'Regularity structures analyze singular rough-volatility expansions. The adapted stock It\\^o integral remains well defined; ordinary finite-state It\\^o formulas do not resolve all singular products.',
                         color=VAR, width=6.2, font_size=19)
        g = VGroup(a, b).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.6)
        q = pause(r"If volatility is a function of the path, is it still rough?", width=7.0, font_size=24).to_edge(DOWN, buff=0.4)
        p = load("pdv")
        with self.voiceover(
            f"""Two mathematical directions. Friz and Gatheral organize forward-variance expansions as forests; the first-order skew is one application. Convergence and truncation accuracy require assumptions, so an expansion is not automatically an exact usable formula for every model. <bookmark mark='a'/> Regularity structures provide tools for singular rough-volatility expansions. The stock's adapted Itô integral still exists; the difficulty is handling singular products and expansions beyond ordinary finite-state calculus. <bookmark mark='b'/> If volatility depends on a path, must it be rough? <bookmark mark='c'/> No. Regularity depends on the kernels and the dynamics. A bounded shifted kernel can produce Brownian-scale stochastic volatility at the shortest lags; bounded does not mean differentiable. The fitted discrete return proxy by itself has no uniquely identified continuous-time local regularity."""
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
        left = VGroup(label('same-date Surface error (vol points; numerical methods differ)', font_size=20, color=GREY_A))
        for y, n_, v in prices:
            left.add(VGroup(MathTex(str(y), font_size=22, color=GREY_B), label(n_, font_size=19),
                            MathTex(f"{v:.2f}", font_size=24, color=YELLOW if v == best[2] else WHITE)).arrange(RIGHT, buff=0.3))
        left.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        right = VGroup(label('time-series comparisons (different information sets)', font_size=20, color=GREY_A),
                       label(rf"2018: rough forecast vs HAR: {f['rough_wins']} of 6 races", font_size=19),
                       label(rf"2023: PDV on DVOL: $R^2$ {pd['r2_test']:.2f} (baseline {pd['r2_base_test']:.2f})", font_size=19),
                       label(rf"2023: 4-factor PDV on DVOL: $R^2$ {p4['r2_test']:.2f}", font_size=19),
                       label(rf"2023: PDV on the VIX: $R^2$ {ps['r2_test']:.2f} (baseline {ps['r2_base_test']:.2f})", font_size=19)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        g = VGroup(left, right).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to(UP * 0.4)
        if g.width > 13.0:
            g.scale_to_fit_width(13.0)
        with self.voiceover(
            f"""On the same-date Bitcoin marks, the lowest recorded numerical error belongs to {best[1]}, at {best[2]:.2f} volatility points. This is calibration evidence, without future-date pricing or hedging validation. <bookmark mark='a'/> The rough forecast comparison fixes H using full-era data; the implied-index models instead freeze fitted coefficients and track held-out dates using same-day returns. For the VIX proxy, held-out R squared is {100 * ps['r2_test']:.0f} percent. These are different questions with different information sets. Low finite-lag scaling exponents, option fit and index reconstruction each provide evidence about their own target. None alone identifies the true volatility law or certifies model adoption."""
        ) as vo:
            self.play(FadeIn(left))
            vo.wait_until("a")
            self.play(FadeIn(right))
        self.wait(0.5)
        self.clear_scene()
