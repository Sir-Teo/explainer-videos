from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class Ridge(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter three. Exact ridge and ridgeless risk, and double descent derived.", 3,
                            r"Exact ridge and ridgeless risk", r"Double descent, \ derived", lit=(2018, 2022))
        self.formula()
        self.risk_chart()
        self.optimal()
        self.ridgeless()
        self.ridgeless_worked()
        self.dd_chart()
        self.why_peak()
        self.benign()

    def formula(self):
        heading = label('The limiting risk and its normalization', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Edgar Dobriban and Stefan Wager computed the exact risk of ridge regression in "
            'the proportional regime, in 2018. With isotropic features, ratio gamma, signal energy r squared and '
            'noise variance sigma squared, everything is a function of the Marchenko–Pastur Stieltjes transform at '
            "minus lambda. <bookmark mark='b'/> The bias is r squared lambda squared times the derivative of m: "
            "shrinkage pulls the estimate toward zero. <bookmark mark='c'/> The variance is sigma squared gamma "
            "times m minus lambda times its derivative. <bookmark mark='d'/> These are limiting excess prediction "
            'risks under the stated isotropic model and signal energy. Bias here means its squared-risk '
            'contribution; irreducible test noise is excluded.'
        ),
            [(r"\text{ridge}", r":", r"\hat\beta_\lambda = (X'X/n + \lambda I)^{-1}X'y/n", 38),
             (r"\text{bias}", r"=", r"r^2\lambda^2\,m'(-\lambda)", 40),
             (r"\text{variance}", r"=", r"\sigma^2\gamma\,\big(m(-\lambda) - \lambda m'(-\lambda)\big)", 38),
             (r"m", r"=", r"\text{the MP Stieltjes transform at ratio } \gamma", 38)],
            [r"Dobriban \& Wager (2018)", r"shrinkage", r"noise fitted", r"chapter 2's tool"],
            colors=[(1, CLASSC), (2, SIMC)])

    def risk_chart(self):
        d = load("ridge")
        lams = np.log10(d["lams"])
        A = axes([-2.0, 0.5], [0, 2.5], x_length=7.4, y_length=4.4, xlabel=r"penalty $\lambda$ (log scale)", ylabel=r"excess risk",
                 xticks=[-2, -1, 0], xfmt=lambda v: f"{10 ** v:g}", yticks=[0, 1, 2], center=[-2.5, 0.2, 0])
        ax = A.ax
        g = d["0.5"]
        bias = polyline(ax, lams, g["bias"], CLASSC, 3)
        var = polyline(ax, lams, g["var"], SIMC, 3)
        risk = polyline(ax, lams, g["risk"], THEORYC, 4)
        sims = VGroup(*[Dot(ax.c2p(math.log10(l), s), radius=0.08, color=AMPC) for l, s in zip(g["sim_l"], g["sim"])])
        best = Dot(ax.c2p(math.log10(g["opt_lam"]), g["opt_risk"]), radius=0.1, color=PROPC)
        side = fit_rows(VGroup(
            label(rf"$\gamma = 0.5$, \ $r^2/\sigma^2 = {d['snr']:g}$", font_size=22),
            label(r"red: \ bias, \ rising with $\lambda$", font_size=22, color=CLASSC),
            label(r"blue: \ variance, \ falling", font_size=22, color=SIMC),
            label(r"white: \ the risk; \ gold: \ simulation, \ $n = 400$", font_size=22, color=AMPC),
            label(rf"green: \ the best $\lambda = \gamma\sigma^2/r^2 = {g['opt_lam']:.3f}$, \ risk {g['opt_risk']:.3f}", font_size=22, color=PROPC),
        ), 4.6, 0.38, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The curves, at half as many variables as observations and a signal-to-noise ratio of four. "
            f"<bookmark mark='b'/> The bias rises with the penalty. <bookmark mark='c'/> The variance falls. <bookmark "
            f"mark='d'/> Their sum is the risk, and simulations at four hundred observations sit on it. <bookmark mark='e'/> "
            f"Its minimum is at lambda equal to gamma over the signal-to-noise ratio, {say(g['opt_lam'], 3)}, with risk "
            f"{say(g['opt_risk'], 3)}: Dobriban and Wager's optimal penalty, in closed form."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"theory exact; \ dots simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(bias), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(var), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(risk), FadeIn(sims), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(best, scale=0.5), FadeIn(side[4]))
        self.clear_scene()

    def optimal(self):
        d = load("ridge")
        g = d["0.5"]
        heading = label('Optimal isotropic ridge penalty', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            f"<bookmark mark='a'/> The optimal penalty has a Bayesian reading. If the coefficients were drawn from a normal prior with total energy r squared, ridge at lambda equal to gamma sigma squared over r squared would be the posterior mean. <bookmark mark='b'/> In the proportional regime the risk does not depend on the coefficients' direction, only their energy, so the same expected-risk-optimal ridge penalty applies to any fixed vector of that energy in this isotropic model. This is optimality among ridge penalties, not every imaginable estimator. <bookmark mark='c'/> Here its risk is {say(g['opt_risk'], 3)}. <bookmark mark='d'/> Leave-one-out or generalized cross-validation can estimate risk under suitable assumptions. Ordinary fixed-fold cross-validation trains at a different aspect ratio and may require an adjustment to select a full-sample penalty.",
            [(r"\lambda_\star", r"=", r"\gamma\sigma^2/r^2", 40),
             (r"\text{reading}", r":", r"\text{the posterior mean under } \beta \sim N(0, \tfrac{r^2}{p}I)", 38),
             (r"\text{risk}", r"=", rf"{g['opt_risk']:.3f} \ \ (\gamma = 0.5)", 40),
             (r"\text{from data}", r":", r"\text{GCV is consistent here}", 40)],
            [r"Dobriban \& Wager", r"Part 26's ridge as Bayes", r"the minimum", r"Part 29's GCV"],
            colors=[(0, PROPC)])

    def ridgeless(self):
        heading = label('Limiting min-norm excess risk', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Now let the penalty go to zero. When gamma is below one, ridge becomes least "
            'squares. When gamma exceeds one, there are infinitely many interpolating solutions, and the limit '
            "picks the one of minimum norm. <bookmark mark='b'/> Trevor Hastie, Andrea Montanari, Saharon Rosset "
            'and Ryan Tibshirani wrote its risk exactly: sigma squared gamma over one minus gamma below the '
            "threshold, <bookmark mark='c'/> and r squared times one minus one over gamma, plus sigma squared over "
            "gamma minus one, above it. <bookmark mark='d'/> With positive observation noise, risk diverges on "
            'approaching gamma one. Past that threshold it first falls; the signal-dependent bias can make it rise '
            'again later. These are exact limiting risk formulas, not exact risks of every finite dataset.'
        ),
            [(r"\lambda \to 0", r":", r"\text{least squares, \ or the minimum-norm interpolator}", 38),
             (r"\gamma < 1", r":", r"\sigma^2\,\frac{\gamma}{1 - \gamma}", 40),
             (r"\gamma > 1", r":", r"r^2\Big(1 - \frac1\gamma\Big) + \frac{\sigma^2}{\gamma - 1}", 40),
             (r"\gamma \to 1^\pm", r":", r"\infty: \ \text{double descent}", 40)],
            [r"ridgeless", r"Hastie et al. (2022)", r"bias plus variance", r"Part 54's curve, \ derived"],
            colors=[(1, SIMC), (2, SIMC), (3, CLASSC)])

    def dd_chart(self):
        d = load("ridge")
        gs = np.asarray(d["gammas"])
        rl = np.asarray(d["ridgeless"])
        ymax = float(5*np.ceil(max(max(rl), max(d["sim_ridgeless"]), 8)/5))
        A = axes([0, 4.1], [0, ymax], x_length=7.4, y_length=4.4, xlabel=r"$\gamma = p/n$", ylabel=r"excess risk",
                 xticks=[0, 1, 2, 3, 4], yticks=list(np.arange(0, ymax+1, 5)), center=[-2.5, 0.2, 0])
        ax = A.ax
        lo, hi = gs < 1, gs > 1
        c1 = polyline(ax, gs[lo], rl[lo], SIMC, 4)
        c2 = polyline(ax, gs[hi], rl[hi], SIMC, 4)
        opt = polyline(ax, gs, d["opt_curve"], PROPC, 4)
        null = DashedLine(ax.c2p(0, d["null_risk"]), ax.c2p(4.1, d["null_risk"]), color=GREY_B, stroke_width=2)
        sims = VGroup(*[Dot(ax.c2p(g_, s), radius=0.08, color=AMPC) for g_, s in zip(d["sim_g"], d["sim_ridgeless"])])
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, ymax), color=CLASSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"blue: \ ridgeless, \ $r^2 = {d['snr']:g}$, \ $\sigma^2 = 1$", font_size=22, color=SIMC),
            label(r"gold: \ simulated, \ $n = 300$", font_size=22, color=AMPC),
            label(r"red: \ the interpolation threshold $\gamma = 1$", font_size=22, color=CLASSC),
            label(r"grey: \ predicting zero; \ green: \ optimally tuned ridge", font_size=22, color=PROPC),
            label(r"tuned ridge never descends twice: \ the peak is an artefact of $\lambda = 0$", font_size=22, color=GREY_A),
        ), 4.6, 0.38, [4.45, 0.4, 0])
        with self.voiceover(
            (
            "<bookmark mark='a'/> The ridgeless risk across gamma, with signal energy four and noise variance one. "
            "<bookmark mark='b'/> Simulations, in gold, follow it. <bookmark mark='c'/> It explodes at the "
            "interpolation threshold, where the design is square. <bookmark mark='d'/> Beyond it the risk first "
            'falls. For signal energy four it reaches a minimum at gamma two, then increases toward the risk of '
            'predicting zero, shown in grey. The green curve is ridge with the optimal penalty: <bookmark '
            "mark='e'/> it rises smoothly with dimension, without the interpolation spike. The second descent is "
            'real, but the peak is an artefact of not regularizing.'
        )
        ) as vo:
            self.play(FadeIn(A), Create(null), FadeIn(simulated_tag(r"theory exact; \ dots simulated")))
            vo.wait_until("a")
            self.play(Create(c1), Create(c2), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(sims), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(one), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(opt), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def why_peak(self):
        heading = label('Noise amplification near the square design', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Why the peak? At gamma equal to one the design matrix is square, and its smallest "
            "singular value is close to zero: the Marchenko–Pastur law's left edge, one minus root gamma squared, "
            "touches zero. <bookmark mark='b'/> Least squares divides the noise by that singular value, and the "
            "variance explodes. <bookmark mark='c'/> Past the threshold, the minimum-norm solution spreads the fit "
            'over more directions than there are observations, and the smallest nonzero singular values move away '
            "from zero again. <bookmark mark='d'/> So the variance falls, while the bias rises because the "
            'interpolator cannot see the part of the signal outside the row space.'
        ),
            [(r"\gamma = 1", r":", r"(1 - \sqrt\gamma)^2 = 0: \ \text{a singular value near } 0", 38),
             (r"\text{variance}", r"\propto", r"\textstyle\sum 1/s_i^2: \ \text{explodes}", 40),
             (r"\gamma > 1", r":", r"\text{the nonzero } s_i \text{ move away from } 0", 40),
             (r"\text{bias}", r":", r"r^2(1 - 1/\gamma): \ \text{the unseen part of } \beta", 40)],
            [r"chapter 1's edge", r"noise amplified", r"variance falls", r"bias rises"],
            colors=[(1, CLASSC), (3, SIMC)])

    def benign(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> What this says about interpolation. <bookmark mark='b'/> Fitting the training "
            'data exactly is not automatically a disaster: past the threshold, the minimum-norm interpolator can '
            "generalize. <bookmark mark='c'/> With isotropic features it is never better than tuned ridge; with "
            "features whose spectrum decays in the right way, Part fifty-four's benign overfitting, it can be "
            "nearly as good. <bookmark mark='d'/> And the formulas are exact: the whole curve, peak included, is "
            'determined by gamma, r squared and sigma squared.'
        ),
            [(r"interpolation:", GREY_A),
             (r"fitting the training data exactly can still generalize", SIMC),
             (r"isotropic: \ never beats tuned ridge; \ decaying spectra: \ benign overfitting", PROPC),
             (r"the whole curve is exact, \ peak included", THEORYC)])

    def ridgeless_worked(self):
        heading = label('Bias and variance beyond interpolation', font_size=30, color=PROPC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Worked numbers, with signal energy four and noise variance one. At gamma a half, "
            "least squares' risk is one times a half over a half: one. <bookmark mark='b'/> At gamma nine tenths, "
            "it is nine: close to the threshold, noise dominates. <bookmark mark='c'/> At gamma two, the "
            "interpolator's risk is four times a half plus one over one: three. <bookmark mark='d'/> At gamma four, "
            'four times three quarters plus a third: about 3.33, approaching the risk of predicting zero, which is '
            'four.'
        ),
            [('\\gamma = 0.5', ':', '1 \\times 0.5/0.5 = 1', 40),
             ('\\gamma = 0.9', ':', '0.9/0.1 = 9', 40),
             ('\\gamma = 2', ':', '4(1 - \\tfrac12) + 1 = 3', 40),
             ('\\gamma = 4', ':', '4 \\times \\tfrac34 + \\tfrac13 \\approx 3.33 \\ \\to 4', 40)],
            ['below the threshold', 'near it', 'past it', 'toward the null risk'],
            colors=[(1, CLASSC)])
