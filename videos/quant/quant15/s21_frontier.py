from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load


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
            cmath(r"\partial_{S_0}\mathbb E[F]", r"=", r"\mathbb E\Big[F\cdot\frac{Z}{S_0\,\sigma\sqrt{T}}\Big]",
                  font_size=36, colors={r"\partial_{S_0}\mathbb E[F]": IV}),
            cmath(r"\partial_{S_0}\mathbb E[F]", r"=", r"\mathbb E[\partial_{S_0}F] + [F]\,\phi(z^{*})\,"
                  r"\partial_{S_0}z^{*}", font_size=36, colors={r"\partial_{S_0}\mathbb E[F]": GOOD}),
        ]
        whys = [why(r"pathwise (and AAD): an indicator is flat almost everywhere, so its derivative on every path is "
                    r"zero, and the estimate of the delta is zero: biased"),
                why(r"likelihood ratio: differentiate the density, not the payoff ($S_T = S_0 e^{\cdots + "
                    r"\sigma\sqrt T Z}$); unbiased, but noisy"),
                why(r"pathwise plus the boundary term: the jump $[F]$ times the density at the boundary times the "
                    r"boundary's speed. It is the missing term (Lakshtanov 2026)")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.8, buff=0.9, edge=6.9)
        pp = pause_card(r"Automatic differentiation gives a digital's delta as exactly zero. Bug or feature?",
                        width=6.0).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Every desk now computes Greeks by algorithmic differentiation, the adjoint method of Part sixteen. "
            "Pause and predict: automatic differentiation says a digital's delta is exactly zero. Is that a bug? "
            "<bookmark mark='a'/> It is what the method must say. On every single path, the payoff is an indicator, "
            "flat almost everywhere, so its derivative is zero, and so is the average. The pathwise estimate is "
            "biased, for digitals, barriers and autocalls alike. <bookmark mark='b'/> One cure is old: "
            "differentiate the probability density instead of the payoff, the likelihood ratio method. It is "
            "unbiased, but noisy. <bookmark mark='c'/> The other is to put back what the pathwise method misses: a "
            "boundary term, the size of the payoff's jump, times the density at the boundary, times how fast the "
            "boundary moves when the spot moves."
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
        g = axes([2, 5], [-0.01, 0.12], x_length=8.4, y_length=4.4, xlabel=r"paths (log scale)",
                 ylabel=r"estimate of the digital's delta", xticks=[2, 3, 4, 5], xfmt=lambda u: f"10^{{{int(u)}}}",
                 yticks=[0, round(ex, 3), 0.1], font_size=15).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        exact = DashedLine(ax.c2p(2, ex), ax.c2p(5, ex), stroke_color=WHITE, stroke_width=2)
        el = label(rf"exact: $\phi(d_2)/(S\sigma\sqrt T) = {ex:.4f}$", font_size=19).next_to(ax.c2p(5, 0.095), UP, buff=0.1)  # above the bands, clear of the curves
        el.align_to(exact, RIGHT)
        tr = ValueTracker(2.0)

        def band(key, col):
            R = np.clip(np.asarray(p[key], float), -0.01, 0.12)

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
        side = wrapped_label(rf"five seeds each, as bands. Per path, the boundary estimator's variance is "
                             rf"{p['ratio']:.0f} times smaller than the likelihood ratio's: the same accuracy with "
                             rf"{p['ratio']:.0f} times fewer paths", 3.6, 18, GREY_A).to_edge(RIGHT, buff=0.3)
        src = illustration(r"a one-month digital call, $S = K = 100$, 25\% volatility, 21 daily steps")
        with self.voiceover(
            "Race the three estimators on a one-month digital, five seeds each, as paths are added. "
            "<bookmark mark='a'/> The pathwise estimate sits at zero, however many paths you run. The likelihood "
            "ratio wanders toward the truth, its band wide and slow to close. The pathwise estimate with the "
            "boundary term put back is on the truth almost at once. <bookmark mark='b'/> Per path, its variance "
            f"here is {p['ratio']:.0f} times smaller than the likelihood ratio's, the same accuracy with "
            f"{p['ratio']:.0f} times fewer paths. On a barrier or an autocall the boundary is a surface in many "
            "dimensions, and finding it automatically is the research."
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
            (r"Cibrario et al.\ (2025)", r"quantum circuits for autocallable payoffs, about 50 times lower T-depth; no "
             r"advantage on today's hardware (Part 16)", GREY_A),
            (r"Fukasawa (2026)", r"short-maturity expansion of barrier prices under rough and regular stochastic "
             r"volatility", BAD),
            (r"Higgins (2026)", r"stochastic spot--vol correlation and FX barrier pricing", BAD),
            (r"Gouden\`ege, Molent, Zanette (2025)", r"uncertain volatility for cliquet-style equity-indexed annuities", GOOD),
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
            "The frontier, paper by paper. Paul Glasserman and Siddharth Karmarkar show that differential machine "
            "learning, which trains pricers on pathwise Greeks, inherits exactly this bias on digitals and barriers, "
            "and fix it with likelihood-ratio labels. Evgeny Lakshtanov's correction makes adjoint Greeks unbiased "
            "for barriers, autocallables and digitals, finding the boundaries automatically. Tensor trains now give "
            "high-order Greeks of worst-of autocallables without sampling noise. <bookmark mark='a'/> On the "
            "business side: reinforcement learning to hedge books of autocallables, and networks pricing "
            "three-asset notes two hundred and fifty times faster than simulation; Chebyshev proxies to make the "
            "capital rules affordable; and quantum circuits for autocallable payoffs, which use far fewer gates, "
            "with no advantage on today's machines. <bookmark mark='b'/> And the theory keeps moving: barrier "
            "prices under rough volatility, stochastic spot–volatility correlation, uncertain volatility for "
            "cliquet-style annuities, and model-free bounds on worst-of autocallables by martingale optimal "
            "transport."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[:3]], lag_ratio=0.4))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[3:6]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[6:]], lag_ratio=0.4))
        self.wait(0.4)
        self.clear_scene()
