from __future__ import annotations

import numpy as np

from videos.stats.stats59.common import *  # noqa: F403


class Corrected(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. Corrected inference: rescaled tests, debiased estimates, and a real design.", 9,
                            r"Corrected inference", r"Repairing the textbook", lit=(2019,))
        self.rescale()
        self.debias()
        self.worked_interval()
        self.estimate_gamma()
        self.real()
        self.real_chart()
        self.board()
        self.other()

    def rescale(self):
        d = load("lrt")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The first correction is to the likelihood-ratio test. Under the null, twice the log "
            f"likelihood ratio converges to kappa sigma star squared over lambda star, times a chi-squared with one degree "
            f"of freedom. <bookmark mark='b'/> So divide the statistic by that factor before comparing it with the "
            f"chi-squared table. <bookmark mark='c'/> Here the factor is {say(d['factor'], 3)}, and the simulated mean of "
            f"the statistic is {say(d['mean_llr'], 3)}, against the factor's prediction of the same. <bookmark mark='d'/> For "
            f"k coefficients tested jointly, the same factor multiplies a chi-squared with k degrees of freedom.",
            [(r"2\Lambda_j", r"\Rightarrow", r"\frac{\kappa\sigma_\star^2}{\lambda_\star}\,\chi^2_1", 40),
             (r"\text{rescaled}", r":", r"2\Lambda_j\big/\tfrac{\kappa\sigma_\star^2}{\lambda_\star} \approx \chi^2_1", 40),
             (r"\text{here}", r":", rf"\text{{factor }} {d['factor']:.3f}; \ \ E[2\Lambda] = {d['mean_llr']:.3f}", 38),
             (r"k \text{ coefficients}", r":", r"\frac{\kappa\sigma_\star^2}{\lambda_\star}\,\chi^2_k", 40)],
            [r"Sur \& Cand\`es", r"one division", r"simulated", r"joint tests"],
            colors=[(0, PROPC), (1, PROPC)])

    def debias(self):
        d = load("hook")
        self.lad_voiceover(
            f"<bookmark mark='a'/> The second correction is to the estimates: divide the MLE by alpha star. <bookmark "
            f"mark='b'/> Then each coordinate is approximately unbiased, with standard deviation sigma star over alpha star "
            f"in the same units. <bookmark mark='c'/> A confidence interval for beta j is the debiased estimate, plus or "
            f"minus one point nine six times that standard deviation, after the right normalization. <bookmark mark='d'/> At "
            f"kappa a fifth and gamma squared five, alpha star is {say(d['alpha'], 3)} and sigma star {say(d['sigma'], 2)}: "
            f"the textbook interval is centred in the wrong place and is too narrow.",
            [(r"\tilde\beta_j", r"=", r"\hat\beta_j/\alpha_\star", 40),
             (r"\tilde\beta_j", r"\approx", r"\beta_j + (\sigma_\star/\alpha_\star)\,Z", 40),
             (r"\text{interval}", r":", r"\tilde\beta_j \pm 1.96\,\sigma_\star/(\alpha_\star\tau_j)", 40),
             (r"\text{here}", r":", rf"\alpha_\star = {d['alpha']:.3f}, \ \sigma_\star = {d['sigma']:.2f}", 40)],
            [r"remove the inflation", r"approximately normal", r"$\tau_j$: the design's scale", r"chapter 0's numbers"],
            colors=[(0, PROPC), (2, PROPC)])

    def estimate_gamma(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> But the corrections need gamma, the signal strength, which is unknown. <bookmark "
            "mark='b'/> Sur and Candès estimate it with ProbeFrontier: subsample the observations and find the sample size "
            "at which the data become separable, since chapter one's boundary depends on gamma. <bookmark mark='c'/> Later "
            "work by Yadlowsky, Yun, McLean and D'Amour gave a faster method, SLOE, from the leave-one-out residuals. "
            "<bookmark mark='d'/> Either way, gamma is estimated from the data, and the corrected intervals and tests are "
            "feasible.",
            [(r"\text{needed}", r":", r"\gamma^2 = \mathrm{Var}(x'\beta), \ \text{unknown}", 40),
             (r"\text{ProbeFrontier}", r":", r"\text{find where subsamples become separable}", 40),
             (r"\text{SLOE}", r":", r"\text{leave-one-out residuals}", 40),
             (r"\text{so}", r":", r"\text{feasible corrections}", 40)],
            [r"a nuisance parameter", r"Sur \& Cand\`es (2019)", r"Yadlowsky et al. (2021)", r"in practice"],
            colors=[(3, PROPC)])

    def real(self):
        d = load("real")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Does the theory survive a real design? The thirty features of the Wisconsin breast cancer "
            f"biopsies are strongly correlated, nothing like independent Gaussians. <bookmark mark='b'/> Take {d['n']} biopsies "
            f"at a time, so kappa is a fifth, and simulate logistic outcomes from a known coefficient vector, with gamma "
            f"squared five as in the hook. <bookmark mark='c'/> Fit the MLE, and measure the inflation on the other biopsies, "
            f"as the slope of the fitted linear predictor on the true one: with features this correlated, single coefficients "
            f"are barely identified, but the predictor is. <bookmark mark='d'/> The data are real, the outcomes are simulated, "
            f"and the truth is known: a semi-synthetic test.",
            [(r"\text{design}", r":", r"\text{30 standardized biopsy features, \ correlated}", 40),
             (r"n = 150", r":", r"\kappa = 0.2", 40),
             (r"\text{outcomes}", r":", r"\text{logistic, \ known } \beta, \ \gamma^2 = 5", 40),
             (r"\text{measure}", r":", r"\text{slope of } x'\hat\beta \text{ on } x'\beta, \ \text{held out}", 40)],
            [r"the Museum's", r"chapter 0's ratio", r"the hook's signal", r"semi-synthetic"],
            colors=[(3, AMPC)])

    def real_chart(self):
        d = load("real")
        sl = np.asarray(d["slopes"])
        edges = np.linspace(0.5, 3.0, 26)
        A = axes([0.5, 3.0], [0, 0.2], x_length=7.4, y_length=4.4, xlabel=r"inflation: \ slope of $x'\hat\beta$ on $x'\beta$, \ held out",
                 ylabel=r"fraction of subsamples", xticks=[0.5, 1, 1.5, 2, 2.5, 3], yticks=[0, 0.1, 0.2], center=[-2.5, 0.2, 0])
        ax = A.ax
        h = hist_bars(ax, edges, np.histogram(np.clip(sl, 0.5, 3.0 - 1e-9), edges)[0] / len(sl), color=SIMC, opacity=0.6)
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 0.2), color=CLASSC, stroke_width=3)
        th = DashedLine(ax.c2p(d["alpha_theory"], 0), ax.c2p(d["alpha_theory"], 0.2), color=PROPC, stroke_width=3)
        side = fit_rows(VGroup(
            label(rf"{d['reps']} subsamples of {d['n']} biopsies; \ $\gamma^2 = {d['gamma2']:g}$", font_size=22),
            label(r"red: \ the textbook, \ no inflation", font_size=22, color=CLASSC),
            label(rf"green: \ the Gaussian-design theory, \ $\alpha_\star = {d['alpha_theory']:.2f}$", font_size=22, color=PROPC),
            label(rf"measured: \ median {d['slope_q'][1]:.2f}, \ mean {d['slope_mean']:.2f}", font_size=22, color=SIMC),
            label(rf"80\% between {d['slope_q'][0]:.2f} and {d['slope_q'][2]:.2f}", font_size=22, color=GREY_A),
        ), 4.6, 0.38, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Over {d['reps']} subsamples of the biopsies. <bookmark mark='b'/> The textbook expects a "
            f"slope of one: no inflation. <bookmark mark='c'/> The theory for a Gaussian design predicts "
            f"{say(d['alpha_theory'], 2)}. <bookmark mark='d'/> The measured slopes have a median of "
            f"{say(d['slope_q'][1], 2)} and a mean of {say(d['slope_mean'], 2)}. <bookmark mark='e'/> Eighty percent fall "
            f"between {say(d['slope_q'][0], 2)} and {say(d['slope_q'][2], 2)}: on a real, strongly correlated design the "
            f"predictor is inflated about as the Gaussian theory says, a hint of the universality chapter one promised, and a "
            f"reason to apply the corrections beyond the textbook's assumptions, with care."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995); \ outcomes simulated")))
            vo.wait_until("a")
            self.play(FadeIn(h, lag_ratio=0.03), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(one), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(th), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def board(self):
        br = load("board")["rows"]
        show_board(self, board_rows("approximation", "rescaled"),
                   f"<bookmark mark='a'/> The Board again, with the correction in hand: the chi-squared test's size is "
                   f"{100 * br[0]['achieved']:.1f} percent, broken; <bookmark mark='b'/> the rescaled test's "
                   f"{100 * br[1]['achieved']:.1f} percent, kept.", [("a", [0]), ("b", [1])])

    def other(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Other corrections in the proportional regime. <bookmark mark='b'/> Debiased lasso "
            "intervals need a degrees-of-freedom adjustment when the support is a constant fraction of n, as Pierre Bellec "
            "and Cun-Hui Zhang showed. <bookmark mark='c'/> Cross-validation's estimate of risk is consistent, but its "
            "uncertainty is not what the fixed-p formulas say. <bookmark mark='d'/> The bootstrap can fail: El Karoui and "
            "Purdom showed in 2018 that resampling residuals or pairs misstates the variance of regression estimates when p "
            "is a fraction of n.",
            [(r"other corrections:", GREY_A),
             (r"debiased lasso: \ a degrees-of-freedom adjustment \ (Bellec \& Zhang)", PROPC),
             (r"cross-validation: \ consistent for risk, \ not for its uncertainty", SIMC),
             (r"the bootstrap can fail \ (El Karoui \& Purdom 2018)", CLASSC)])

    def worked_interval(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A worked interval in the hook's units. Suppose a coefficient's MLE is 15. <bookmark mark='b'/> The textbook reports it as 15, with a standard error of 3.9 from the Fisher information: an interval from 7.4 to 22.6. <bookmark mark='c'/> The corrected estimate is 15 over 1.50, which is 10, with standard error 4.74 over 1.50, about 3.2. <bookmark mark='d'/> So the corrected interval runs from 3.8 to 16.2: centred a third lower, and shaped by the right noise level.",
            [('\\hat\\beta_j', '=', '15', 40),
             ('\\text{textbook}', ':', '15 \\pm 1.96 \\times 3.9 = (7.4, \\ 22.6)', 40),
             ('\\text{corrected}', ':', '15/1.50 = 10, \\ \\ \\mathrm{se} = 4.74/1.50 \\approx 3.2', 40),
             ('\\text{interval}', ':', '(3.8, \\ 16.2)', 40)],
            ['one coefficient', 'wrong centre', 'debiased', 'honest'],
            colors=[(1, CLASSC), (3, PROPC)])
