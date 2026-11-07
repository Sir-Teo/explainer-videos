from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, axes, data_range, pause_card


class Frontier(VoiceoverScene):
    def construct(self):
        p = load("pathwise_digital")
        self.card()
        self.derive()
        self.race(p)
        self.papers()

    def card(self):
        c = chapter_card(18, r"Frontier, 2023--2026", r"Where is exotics computation going?", part=PART)
        with self.voiceover("Chapter eighteen. The frontier, 2023 to 2026."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [
            cmath(r"\partial_{S_0}\mathbf 1_{\{S_T > K\}}", r"=", r"0\quad\text{almost surely}", font_size=38,
                  colors={r"\partial_{S_0}\mathbf 1_{\{S_T > K\}}": BAD}),
            cmath(r"\partial_{S_0}\mathbb E[F]", r"=", r"\mathbb E\Big[F\cdot\frac{Z_1}{S_0\,\sigma\sqrt{\Delta t}}\Big]",
                  font_size=36, colors={r"\partial_{S_0}\mathbb E[F]": IV}),
            cmath(r"\partial_{S_0}\mathbb E[F]", r"=", r"\mathbb E[\partial_{S_0}F] - \mathbb E_w\big[[F]\,\phi(z^{*})\,"
                  r"\partial_{S_0}z^{*}\big]", font_size=36, colors={r"\partial_{S_0}\mathbb E[F]": GOOD}),
        ]
        whys = [why(r"pathwise (and AAD): an indicator is flat almost everywhere, so its derivative on every path is "
                    r"zero, and the estimate of the delta is zero: biased"),
                why(r"GBM first-step likelihood ratio, $\Delta t=T/21$, $F$ discounted; shift the first Gaussian density ($S_T = S_0 e^{\cdots + "
                    r"\sigma\sqrt T Z}$); unbiased, but noisy"),
                why(r"pathwise plus the boundary term: the jump $[F]$ times the density at the boundary times the "
                    r"negative boundary speed, with $[F]=F_{right}-F_{left}$; regular roots, integrability and all boundaries accounted for (Lakshtanov 2026)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.8, buff=0.9, edge=6.9)
        pp = pause_card(r"Automatic differentiation gives a digital's delta as exactly zero. Bug or feature?",
                        width=6.0).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Adjoint differentiation efficiently computes pathwise Greeks, but discontinuities need care. For the digital indicator, the sampled pathwise derivative is zero almost surely. <bookmark mark='a'/> Interchanging that derivative with expectation is invalid here, so averaging zeros misses a positive delta. Other discontinuous payoffs can have nonzero but biased pathwise contributions. <bookmark mark='b'/> Our likelihood-ratio estimator shifts the first Gaussian step of GBM; its score uses delta t, not the terminal-time Gaussian score. Both approaches can be valid but have different variance. <bookmark mark='c'/> Conditioning across a regular boundary adds the missing jump term. With jump defined as right value minus left value, the displayed moving-root term has a minus sign. The general result requires regular boundaries, integrability and accounting for all roots. Numerically finding boundaries and simulating continuous barriers add separate errors."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def race(self, p):
        n = np.log10(np.asarray(p["n"], float))
        ex = p["exact"]
        g = axes([2, 5], data_range(p["lr"], p["boundary"], p["pathwise"], zero=True), x_length=8.4, y_length=4.4, xlabel=r"paths (log scale)",
                 ylabel=r"estimate of the digital's delta", xticks=[2, 3, 4, 5], xfmt=lambda u: f"10^{{{int(u)}}}",
                 yticks=[0, round(ex, 3), 0.1], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        exact = DashedLine(ax.c2p(2, ex), ax.c2p(5, ex), stroke_color=WHITE, stroke_width=2)
        el = label(rf"exact: $\phi(d_2)/(S\sigma\sqrt T) = {ex:.4f}$", font_size=19).next_to(ax.c2p(5, 0.095), UP, buff=0.1)  # above the bands, clear of the curves
        el.align_to(exact, RIGHT)
        tr = ValueTracker(2.0)

        def band(key, col):
            R = np.asarray(p[key], float)

            def make():
                x = tr.get_value()
                m = n <= x + 1e-9
                if m.sum() < 2:
                    return VGroup()
                return seed_band(ax, n[m], R[:, m], col)
            return always_redraw(make)
        bands = [band("pathwise", BAD), band("lr", IV), band("boundary", GOOD)]
        leg = legend([(BAD, r"pathwise / AAD: zero on every path"), (IV, r"likelihood ratio: unbiased, noisy"),
                      (GOOD, r"pathwise + boundary term: unbiased, quiet")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = wrapped_label(rf"five-seed min--max bands, not confidence intervals. Per path, the boundary estimator's variance is "
                             rf"{p['ratio']:.0f} times smaller than the likelihood ratio's: the same accuracy with "
                             rf"{p['ratio']:.0f} times fewer paths", 3.6, 18, GREY_A).to_edge(RIGHT, buff=0.3)
        src = illustration(r"a one-month digital call, $S = K = 100$, 25\% volatility, 21 daily steps")
        with self.voiceover(
            f"The race uses the same one-month GBM digital and five seeds, with full, unclipped min-max bands as the path count grows. These bands are not confidence intervals. <bookmark mark='a'/> The naive pathwise mean stays zero. First-step likelihood ratio is noisy but unbiased for this model. The green estimator analytically integrates the last step conditional on the preceding path, then differentiates that smooth conditional probability. It is a simple conditional-Monte-Carlo boundary correction, not the general automatic root-finding algorithm from the paper. <bookmark mark='b'/> On the separate fixed sample used for the variance comparison, the green per-path variance is {p['ratio']:.0f} times smaller. That ratio is specific to these estimators and parameters; it is not a universal advantage over all likelihood-ratio constructions or a certified speedup for autocallables."
        ) as vo:
            self.play(FadeIn(g), Create(exact), FadeIn(el), FadeIn(leg), FadeIn(src))
            self.add(*bands)
            vo.wait_until("a")
            self.play(tr.animate.set_value(5.0), run_time=7, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(side))
        for b in bands:
            b.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def papers(self):
        items = [
            (r"Glasserman, Karmarkar (2025)", r"Differential ML with a difference: pathwise labels are biased for "
             r"digitals and barriers; likelihood-ratio labels, and a hybrid with gamma, cut test errors", IV),
            (r"Lakshtanov (2026)", r"unbiased Monte Carlo Greeks for discontinuous payoffs: AAD plus boundary "
             r"corrections located by root-finding, for barriers, autocallables, digitals", GOOD),
            (r"Lopez-Piqueres, Acharya, Sun, Kumar (2026)", r"functional tensor trains for high-order Greeks and "
             r"exposure tails of worst-of autocallables", OPT),
            (r"Sharma, Chen, Noh, DeJesus, Schlener (2024)", r"distributional RL to hedge autocallable portfolios; "
             r"three-asset autocallables priced 250 times faster than Monte Carlo (ICAIF 2024)", QC.HOUSE),
            (r"Zeron, Wu, Ruiz (2023)", r"FRTB internal models for equity autocallables with Chebyshev proxies", IV),
            (r"Cibrario et al.\ (2025)", r"quantum circuits for autocallable payoffs, about 50 times lower payoff-component T-depth; no demonstrated "
             r"end-to-end hardware speedup in this benchmark (Part 16)", GREY_A),
            (r"Fukasawa (2026)", r"up-and-out puts with strike and barrier approaching spot at diffusive scale, continuous stochastic "
             r"volatility", BAD),
            (r"Higgins (2026)", r"stochastic spot--vol correlation and FX barrier pricing", BAD),
            (r"Gouden\`ege, Molent, Zanette (2025 preprint; 2026 journal)", r"uncertain volatility for cliquet-style equity-indexed annuities", GOOD),
            (r"Che, Lim, Sun (2026)", r"multi-period, multi-asset martingale optimal transport: model-free bounds for "
             r"worst-of autocallables (Part 9)", QC.Q),
        ]
        rows = VGroup(*[VGroup(label(a, font_size=19, color=c), wrapped_label(b, 7.6, 18, GREY_A)).arrange(
            RIGHT, buff=0.3, aligned_edge=UP) for a, b, c in items])
        for r_ in rows:
            r_[1].align_to(rows, LEFT).shift(RIGHT * 4.9)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        for r_ in rows:
            r_[0].align_to(rows, LEFT)
            r_[1].set_x(rows.get_left()[0] + 4.9 + r_[1].width / 2)
        rows.move_to(ORIGIN)
        if rows.height > 7.3:
            rows.scale_to_fit_height(7.3)
        if rows.width > 13.4:
            rows.scale_to_fit_width(13.4)
        with self.voiceover(
            "Selected papers, each within its own scope. Glasserman and Karmarkar's 2025 preprint, revised in 2026, studies likelihood-ratio labels for differential learning with discontinuous payoffs. Lakshtanov's 2026 preprint develops regular-boundary corrections. Tensor trains offer high-order Greeks for monthly multi-asset autocallables; Monte Carlo remains cheaper for some low-accuracy delta tasks. <bookmark mark='a'/> Sharma and co-authors report a 250-fold pricing benchmark and distributional reinforcement-learning hedges in their specified simulations. Zeron, Wu and Ruiz report about ninety-percent computational savings with passing attribution metrics in their tested setup. Cibrario's factor of fifty concerns the payoff-loading circuit's T-depth, not end-to-end hardware runtime. <bookmark mark='b'/> Fukasawa studies up-and-out puts with strike and barrier approaching spot at the diffusive scale. Higgins models stochastic spot-volatility correlation in FX. Goudenège and co-authors combine uncertain volatility, stochastic rates and annuity surrender. Che, Lim and Sun prove dual attainment under regularity and irreducibility assumptions and compute discrete autocallable transport examples. These are research results and benchmarks, not evidence of universal production adoption."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:3]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[3:6]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[6:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
