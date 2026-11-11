from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant30.common import BAD, EST_C, GOOD, HURDLE, PART, RMT_C, SAMPLE_C, SHRINK_C, fit_right, load

EST_COL = {"sample": SAMPLE_C, "LW identity": QC.OPTION, "LW const-corr": SHRINK_C, "RMT clipped": RMT_C,
           "nonlinear": GOOD}


class Shrink(VoiceoverScene):
    def construct(self):
        s = load("shrink")
        self.card()
        self.linear()
        self.constcorr()
        self.nonlinear()
        self.eigs(s)
        self.horse(s)
        self.factors(load("factor"), load("rolling"))
        self.intensity(s)
        self.window()
        self.question()

    def card(self):
        c = chapter_card(4, r"Shrinkage: Ledoit and Wolf", r"If the sample covariance is too extreme, how far should we "
                         r"pull it back, and toward what?", part=PART)
        with self.voiceover("Chapter four. The sample covariance spreads its eigenvalues too far apart. How far should we "
                            "pull it back, and toward what?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def linear(self):
        rows = [cmath(r"\hat\Sigma_\delta", r"=", r"\delta F + (1 - \delta) S", font_size=36, colors={r"\hat\Sigma_\delta": SHRINK_C}),
                cmath(r"\delta^*", r"=", r"\arg\min_\delta \mathbb E\|\hat\Sigma_\delta - \Sigma\|_F^2 = "
                      r"\frac{\mathbb E\|S - \Sigma\|_F^2}{\mathbb E\|S - F\|_F^2}", font_size=30, colors={r"\delta^*": HURDLE}),
                cmath(r"F = m I", r":", r"\hat\delta = \frac{\hat b^2}{\hat d^2},\ \ \hat b^2 = \tfrac{1}{T^2}\textstyle\sum_t "
                      r"\|x_t x_t^\top - S\|^2,\ \ \hat d^2 = \|S - mI\|^2", font_size=28)]
        whys = [why(r"a weighted average of the sample matrix $S$ and a simple target $F$: less variance, some bias"),
                why(r"the best weight in squared error, when $F$ is fixed and $S$ unbiased: the sample matrix's own noise over its distance "
                    r"from the target"),
                why(r"Ledoit and Wolf (2004a): with the scaled identity as target, both are estimable from the data, and "
                    r"the estimate converges to the optimum as $N, T \to \infty$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Shrinkage trades variance for bias. <bookmark mark='a'/> Blend a sample covariance S with a structured target F, which can still be badly misspecified. <bookmark mark='b'/> For a fixed target and unbiased S, the unconstrained squared-Frobenius-error optimum has the displayed noise-over-distance ratio; restricting the blend to zero through one clips the optimum. A target estimated from the same data needs covariance terms. <bookmark mark='c'/> Ledoit and Wolf estimate intensities under stated large-dimensional assumptions. The local scaled-identity routine uses demeaned divisor-T moments and caps its estimated ratio at one."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def constcorr(self):
        cards = VGroup(
            desk_question(r"the constant-correlation target", r"keep every variance, set every correlation to the "
                          r"average: Ledoit and Wolf's `Honey, I shrunk the sample covariance matrix' (2004b), with its own "
                          r"estimated intensity", width=12.4, font_size=19),
            desk_question(r"a factor-model target", r"the covariance implied by a one-factor (market) model, Ledoit and "
                          r"Wolf (2003): the target is itself a structured estimate", width=12.4, font_size=19),
            desk_question(r"why targets work", 'structured targets can reduce variance while adding misspecification bias; fitted targets share estimation noise with the sample matrix',
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Different targets encode different beliefs. <bookmark mark='a'/> The constant-correlation target retains individual estimated variances and uses an estimated average correlation. Its fitted-target dependence requires its own intensity formula. <bookmark mark='b'/> A single-index covariance instead uses estimated loadings and residual variances. <bookmark mark='c'/> Structure can reduce variance but introduces bias and parameter uncertainty. A small parameter count alone does not guarantee a good target, and the appropriate loss may be portfolio risk rather than covariance Frobenius error."
        ) as vo:
            self.add(cards[0])
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def nonlinear(self):
        rows = [cmath(r"\hat\Sigma", r"=", r"U\,\operatorname{diag}(d_1, \dots, d_N)\,U^\top", font_size=34,
                      colors={r"\hat\Sigma": GOOD}),
                cmath(r"d_i^{\text{or}}", r"=", r"u_i^\top\Sigma u_i", font_size=34, colors={r"d_i^{\text{or}}": HURDLE}),
                cmath(r"d_i", r"=", r"\frac{\lambda_i}{\big(\pi q\lambda_i \hat f(\lambda_i)\big)^2 + \big(1 - q - \pi q "
                      r"\lambda_i \mathcal H\hat f(\lambda_i)\big)^2}", font_size=30, colors={r"d_i": GOOD})]
        whys = [why(r"keep the sample eigenvectors $U$, choose new eigenvalues: the rotation-equivariant estimators"),
                why(r"the best such choice, if we knew $\Sigma$: the true variance along each sample eigenvector"),
                why(r"Ledoit and Wolf (2020): the oracle in the large-dimensional limit, from a kernel estimate of the "
                    r"eigenvalues' density $\hat f$ and its Hilbert transform; each eigenvalue gets its own shrinkage")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Nonlinear spectral shrinkage. <bookmark mark='a'/> Keep sample eigenvectors and choose directional variances. A scaled-identity linear target shares those eigenvectors; a constant-correlation target generally does not. <bookmark mark='b'/> Under squared Frobenius loss, the rotation-equivariant oracle is each sample eigenvector's true directional variance. It is not a portfolio-loss oracle. <bookmark mark='c'/> Ledoit and Wolf's analytical estimator uses spectral density and Hilbert-transform estimates under large-dimensional assumptions. It estimates, rather than equals, the oracle; the local implementation covers fewer assets than demeaned observations."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def eigs(self, s):
        e = s["eig"]
        k = np.arange(1, 50)
        ys = {key: np.log10(np.asarray(e[key], float)) for key in ("true", "sample", "oracle", "nonlinear")}
        lo = float(np.floor(min(v.min() for v in ys.values())))
        hi = float(np.ceil(max(v.max() for v in ys.values())))
        g = axes([1, 49], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue rank", ylabel=r"eigenvalue (log scale)",
                 xticks=[1, 10, 25, 49], yticks=list(range(int(lo), int(hi) + 1)), yfmt=lambda v: f"10^{{{int(v)}}}",
                 font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        cols = {"true": GREY_A, "sample": SAMPLE_C, "oracle": HURDLE, "nonlinear": GOOD}
        lines = {key: curve(ax, k, ys[key], cols[key], stroke_width=3 if key != "oracle" else 2) for key in ys}
        leg = legend([(GREY_A, r"the true eigenvalues"), (SAMPLE_C, r"the sample's"),
                      (HURDLE, r"the oracle: $u_i^\top\Sigma u_i$"), (GOOD, r"nonlinear shrinkage")], font_size=15
                     ).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        side = wrapped_label(r"one simulated ten-year window from the industries' covariance; the oracle uses the sample's "
                             r"eigenvectors, which are themselves noisy, so it is not the truth", 3.4, 15, GREY_A
                             ).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        t_lo, s_lo = e["true"][-1], e["sample"][-1]
        with self.voiceover(
            f"""One simulated hundred-and-twenty-observation window. <bookmark mark='a'/> Grey shows sorted population eigenvalues, red sorted sample eigenvalues; the smallest population eigenvalue is {t_lo / s_lo:.1f} times the smallest sample value. This comparison does not match eigenvector directions. <bookmark mark='b'/> The oracle curve instead evaluates population variance along sample eigenvectors, ordered by sample eigenvalue. It is optimal within that eigenbasis under Frobenius loss. <bookmark mark='c'/> The saved nonlinear estimator is compared with that oracle. Closeness is an observed finite example, not exact oracle recovery or a guarantee of portfolio-optimal shrinkage."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(lines["true"]), Create(lines["sample"]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines["oracle"]))
            vo.wait_until("c")
            self.play(Create(lines["nonlinear"]))
        self.wait(0.4)
        self.clear_scene()

    def horse(self, s):
        est = s["estimators"]
        Ts = ["60", "120", "240"]
        hx = [-4.4, -1.6, 0.9, 3.4]
        head = VGroup(label(r"estimator", font_size=18, color=GREY_B),
                      *[label(rf"$T = {t}$ months", font_size=18, color=GREY_B) for t in Ts])
        tab = VGroup(head)
        for e in est:
            tab.add(VGroup(label(e, font_size=19, color=EST_COL[e]),
                           *[MathTex(rf"{s['sims'][t][e]['gmv']:.2f}", font_size=26) for t in Ts]))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.1 - 0.7 * j, 0])
        foot = wrapped_label(r"the true variance of each estimator's minimum-variance portfolio, as a multiple of the "
                             r"lowest possible; the truth is the industries' 1970--2020 covariance, 100 simulated windows each",
                             11.4, 16, GREY_A).to_edge(DOWN, buff=0.5)
        s60 = s["sims"]["60"]
        with self.voiceover(
            f"""A fixed Gaussian population experiment. <bookmark mark='a'/> Compare each fitted GMV portfolio's true variance with the population minimum, averaged over a hundred draws per sample size. <bookmark mark='b'/> With sixty observations, sample GMV has ratio {s60['sample']['gmv']:.1f}; constant-correlation shrinkage has {s60['LW const-corr']['gmv']:.1f}, and nonlinear shrinkage {s60['nonlinear']['gmv']:.2f}. At two hundred and forty observations, clipping has {s['sims']['240']['RMT clipped']['gmv']:.2f} versus sample {s['sims']['240']['sample']['gmv']:.2f}. These outcomes are conditional on this population and implementation. Linear shrinkage uses divisor T, while the sample and nonlinear routines use T minus one. No universal dominance follows."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[2], r_[3])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def factors(self, f, ro):
        rows = [cmath(r"\Sigma_F", r"=", r"B\,\Sigma_f B^\top + D", font_size=36, colors={r"\Sigma_F": SHRINK_C}),
                cmath(r"k = 1", r":", '\\beta\\beta^\\top\\sigma_m^2 + D\\quad\\text{(market single-index target)}', font_size=28)]
        whys = [why(r"a factor model: $k$ common factors with loadings $B$, and independent idiosyncratic variances $D$"),
                why('a fitted market single-index target differs from a first-PCA factor; the saved comparison below uses PCA factors')]
        step = ladder(self, rows, whys, keep=2, top=2.7, x=-0.3, buff=0.5, edge=6.9)
        res = f["res"]
        r120 = ro["res"]["120"]
        names = [("1 PCA factor", res["1 PCA factor"], SHRINK_C), ("5 PCA factors", res["5 PCA factors"], QC.OPTION),
                 ("single index", res["single index"], GOOD), ("LW const-corr", r120["LW const-corr GMV"], RMT_C),
                 ("sample", r120["sample GMV"], SAMPLE_C)]
        hx = [-3.6, -0.6, 1.8, 4.2]
        head = VGroup(label(r"minimum variance with", font_size=17, color=GREY_B), label(r"Sharpe", font_size=17, color=GREY_B),
                      label(r"volatility", font_size=17, color=GREY_B), label(r"sample-risk proxy", font_size=17, color=GREY_B))
        tab = VGroup(head)
        for n, x, col in names:
            tab.add(VGroup(label(n, font_size=18, color=col), MathTex(f"{x['sharpe']:.2f}", font_size=24),
                           MathTex(rf"{100 * x['vol']:.1f}\%", font_size=24), MathTex(rf"{100 * x['pred_vol']:.1f}\%",
                                                                                     font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 0.4 - 0.55 * j, 0])
        foot = wrapped_label(r"rolling ten-year windows, 1980--2020, as in Chapter 2 (studied after the envelope was "
                             r"registered, so not part of its count)", 11.4, 15, GREY_A).to_edge(DOWN, buff=0.3)
        p1 = res["1 PCA factor"]
        with self.voiceover(
            f"""Structure is another regularizer. <bookmark mark='a'/> A factor covariance models common variation plus diagonal residual risk; low parameter count reduces some estimation burden but does not eliminate noise or misspecification. <bookmark mark='b'/> A market-index factor and a first principal component are distinct constructions. The saved one-PCA-factor rule uses the latter. <bookmark mark='c'/> Its retrospective rolling Sharpe is {p1['sharpe']:.2f}, with {100 * p1['pred_vol']:.1f} percent trailing sample-covariance risk and {100 * p1['vol']:.1f} percent realised volatility. The first number is not its factor-model covariance forecast. This is selected research evidence, not a causal identification of improvement."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def intensity(self, s):
        x = np.asarray(s["dates"], float)
        x = x // 100 + ((x % 100) - 0.5) / 12
        ki, kc = np.asarray(s["k_identity"]), np.asarray(s["k_constcorr"])
        g = axes([x[0], x[-1]], [0, 0.6], x_length=9.0, y_length=4.0, xlabel=r"", ylabel=r"estimated shrinkage intensity",
                 xticks=[1980, 2000, 2020], yticks=[0, 0.3, 0.6], xfmt=lambda v: f"{v:.0f}", font_size=15
                 ).move_to(LEFT * 0.6 + DOWN * 0.2)
        ax = g.ax
        li, lc = curve(ax, x, ki, QC.OPTION, stroke_width=3), curve(ax, x, kc, SHRINK_C, stroke_width=3)
        kmin, kmax, kimax = float(kc.min()), float(kc.max()), float(ki.max())
        leg = legend([(QC.OPTION, r"toward the scaled identity"), (SHRINK_C, r"toward constant correlation")],
                     font_size=15).to_corner(UR, buff=0.4)
        with self.voiceover(
            f"""Estimated intensities over ten-year research windows. <bookmark mark='a'/> The constant-correlation blend ranges from {kmin:.2f} to {kmax:.2f}; the scaled-identity intensity stays below {kimax:.2f}. Different targets and denominators produce different intensities. A smaller intensity does not by itself prove a target is better or worse. Here the identity removes common correlations, whereas the constant-correlation target preserves an estimated average relationship."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lc), Create(li), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def window(self):
        rows = [cmath(r"\text{error}(T)", r"\approx", r"\underbrace{c_1\,\frac{N}{T}}_{\text{noise}} + "
                      r"\underbrace{c_2\,(\text{drift over } T)^2}_{\text{staleness}}", font_size=30, colors={r"\text{error}(T)": HURDLE}),
                cmath(r"\text{EWMA}", r":", r"\hat\Sigma_t = \lambda\hat\Sigma_{t-1} + (1 - \lambda)r_tr_t^\top,\ \ T_{\text{eff}} "
                      r"\approx \frac{1 + \lambda}{1 - \lambda}", font_size=28),
                cmath(r"\text{daily data}", r":", r"T\ \text{twentyfold for the same calendar window}", font_size=30)]
        whys = [why(r"a longer window averages away noise but mixes in a covariance that has since changed; the best "
                    r"window balances the two"),
                why(r"exponential weighting (Part 7's RiskMetrics) trades the same two errors smoothly"),
                why(r"more observations need not mean proportionally more information; horizon and dependence matter, while "
                    r"daily covariance and longer-horizon mean forecasts need different models")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "A practical trade-off. <bookmark mark='a'/> A longer history can reduce sampling error while mixing different covariance regimes. The displayed noise and drift terms are schematic, not an estimated universal loss curve. <bookmark mark='b'/> For independent, equally informative observations, an infinite geometric weight sequence has Kish effective size one plus lambda over one minus lambda; serial dependence changes the information content. <bookmark mark='c'/> Daily data supply roughly twenty observations per month, but neither independence nor a twentyfold precision gain is automatic. Forecast horizon, asynchronous trading and changing volatility still matter."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def question(self):
        q = pause_card('if a fixed target equals the known population covariance, which blend minimises Frobenius loss? What changes when its scale is estimated from the same data?')
        with self.voiceover(
            'Pause and predict. If a fixed target equals the known population covariance exactly, which blend minimises Frobenius loss? How does estimating the target scale from the same data change the question?'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
