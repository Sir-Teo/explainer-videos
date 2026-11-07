from __future__ import annotations

import numpy as np

from videos.stats.stats65.common import *  # noqa: F403


class Application(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter six. Real data: blood pressure for a population a study under-sampled.", 6,
                            r"An application", r"NHANES, \ with a designed selection")
        self.design()
        self.method()
        self.chart()
        self.diagnostics()
        self.workflow()
        self.reading()

    def design(self):
        d = load("nhanes")
        self.lad_voiceover(
            "<bookmark mark='a'/> Use the 5,176-adult NHANES complete-case extract as a fixed empirical distribution, without survey weights. This is not a claim about national population coverage. <bookmark mark='b'/> Assign each stored row a source probability proportional to the logistic age-selection function, and target probability proportional to its complement. Age is top-coded at eighty and pressure averages available measurements. <bookmark mark='c'/> Draw training and calibration observations independently with replacement from the source, and independent test observations from the target. Repeated rows are allowed under this empirical resampling model. <bookmark mark='d'/> The source underrepresents older adults and the designed ratio is known. The target represents the complement-weighted empirical law, not a literal held-out list of unique people or a new national survey.",
            [(r"\text{data}", r":", rf"\text{{NHANES, \ {d['N']:,} adults}}".replace(",", "{,}"), 40),
             (r"P(\text{in study} \mid \text{age})", r"=", r"1 / (1 + e^{(\text{age} - 45)/8})", 40),
             (r"\text{65 and over}", r":", rf"{100 * d['frac_old_pop']:.0f}\% \text{{ of adults, \ }} {100 * d['frac_old_sel']:.0f}\% \text{{ of the study}}", 40),
             (r"\text{target}", r":", r"\text{complement-weighted empirical NHANES law}", 40)],
            [r"the Museum", r"fixed source/target resampling design", r"a skewed sample", r"ratio known; coverage estimated by resampling"],
            colors=[(2, NAIVEC)])

    def method(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Fit the blood-pressure regression on an independent source training sample and compute absolute residual scores on a separate source calibration sample. <bookmark mark='b'/> Fit a density-ratio classifier on another thousand auxiliary source and thousand auxiliary target covariate draws, independent of training, calibration and test draws. The predictor is fixed when calibration begins. <bookmark mark='c'/> Equal auxiliary sample sizes make target odds proportional to the required ratio; its constant does not affect the weighted quantile. We no longer fit weights using calibration covariates. <bookmark mark='d'/> Compare no weights, oracle ratio and fitted ratio over two hundred repetitions, each evaluated on three thousand fresh target draws. The result is repeated empirical-distribution resampling evidence with saved Monte Carlo errors, not validation on independently collected new patients.",
            [(r"\text{model}", r":", r"\text{regression on age, \ BMI}", 40),
             (r"\text{scores}", r":", r"|y - \hat m(x)| \ \text{on independent calibration data}", 40),
             (r"\hat w(x)", r"=", r"\hat p_Q(x) / (1 - \hat p_Q(x))", 40),
             (r"\text{compare}", r":", r"\text{none, \ true, \ estimated; \ 200 draws}", 40)],
            [r"independent training sample", r"split conformal", r"target-class probability", r"replicated"],
            colors=[(2, ESTC)])

    def chart(self):
        d = load("nhanes")
        meth = ["none", "oracle", "estimated"]
        A = axes([-0.6, 1.6], [0.5, 1.0], x_length=6.8, y_length=4.4, xlabel=r"", ylabel=r"coverage of the 90\% interval, \ 200 draws",
                 xticks=None, yticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0], yfmt=lambda v: f"{100 * v:.0f}\\%", center=[-2.6, 0.3, 0])
        ax = A.ax
        nom = DashedLine(ax.c2p(-0.6, 0.9), ax.c2p(1.6, 0.9), color=GREY_B, stroke_width=2)
        groups = VGroup()
        for gi, key in enumerate(["young", "old"]):
            g = VGroup()
            for k, m in enumerate(meth):
                v = d[key][m]
                x = gi + (k - 1) * 0.26
                b = Rectangle(width=0.22, height=ax.c2p(0, v)[1] - ax.c2p(0, 0.5)[1], stroke_width=0, fill_color=METHC[m], fill_opacity=0.85)
                b.move_to(ax.c2p(x, 0.5), aligned_edge=DOWN)
                g.add(VGroup(b, label(rf"{100 * v:.0f}", font_size=18, color=METHC[m]).next_to(b, UP, buff=0.06)))
            groups.add(g)
        ticks = VGroup(label(r"under 65", font_size=22, color=GREY_A).next_to(ax.c2p(0, 0.5), DOWN, buff=0.2),
                       label(r"65 and over", font_size=22, color=GREY_A).next_to(ax.c2p(1, 0.5), DOWN, buff=0.2))
        c = d["coverage"]
        side = side_groups([
            [(rf"red: \ no weights, \ {100 * c['none']:.1f}\% overall", NAIVEC)],
            [(rf"green: \ true weights, \ {100 * c['oracle']:.1f}\%", HONC)],
            [(rf"blue: \ estimated weights, \ {100 * c['estimated']:.1f}\%", ESTC)],
            [(rf"intervals: \ {d['width']['none']:.0f} mmHg wide unweighted,", GREY_A), (rf"{d['width']['estimated']:.0f} weighted", GREY_A)],
        ], pos=(3.6, 0.3, 0))
        with self.voiceover(
            f"<bookmark mark='a'/> The results, for adults under sixty-five and for those sixty-five and over. <bookmark mark='b'/> Without weights, the interval promises ninety percent and covers {100 * c['none']:.1f} percent overall, and only {100 * d['old']['none']:.0f} percent of the old, whose blood pressure is more variable and whom the study barely saw. <bookmark mark='c'/> With the true weights, coverage is {100 * c['oracle']:.1f} percent. <bookmark mark='d'/> With the estimated weights, {100 * c['estimated']:.1f} percent: in this finite resampling experiment. The classifier family can represent the true ratio, but finite-sample errors remain; similar coverages do not prove equality of methods. The honest interval is wider, about {d['width']['estimated']:.0f} millimetres of mercury against {d['width']['none']:.0f}: the price of covering the people the study missed."
        ) as vo:
            self.play(FadeIn(A), Create(nom), FadeIn(ticks), FadeIn(museum_tag(r"NHANES (the Museum)")))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(groups[0][0]), FadeIn(groups[1][0]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(groups[0][1]), FadeIn(groups[1][1]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(groups[0][2]), FadeIn(groups[1][2]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(1.0)
        self.clear_scene()

    def reading(self):
        d = load("nhanes")
        self.lad_voiceover(
            f"<bookmark mark='a'/> How to read it. <bookmark mark='b'/> The weighted intervals still under-cover the old "
            f"slightly, {100 * d['old']['oracle']:.0f} percent: the guarantee is marginal over the target, and the old are a "
            f"subgroup of it, Part sixty-three's lesson about subgroups. <bookmark mark='c'/> The application supports the "
            f"study's message in one setting where the classifier was well specified. <bookmark mark='d'/> It does not show "
            f"what happens when the selection depends on something the classifier cannot see; that is a limitation to state, "
            f"not to hide.",
            [(r"\text{the old}", r":", rf"{100 * d['old']['oracle']:.0f}\% \ \text{{even with true weights}}", 40),
             (r"\text{why}", r":", r"\text{marginal, \ not conditional}", 40),
             (r"\text{supports}", r":", r"\text{the study, \ here}", 40),
             (r"\text{limitation}", r":", r"\text{selection on unseen variables}", 40)],
            [r"a subgroup", r"Parts 57 and 63", r"one setting", r"stated"],
            colors=[(0, NAIVEC), (3, NAIVEC)])

    def diagnostics(self):
        d = load("nhanes")
        self.lad_voiceover(
            f"<bookmark mark='a'/> Before trusting weighted intervals, check the weights. <bookmark mark='b'/> The estimated log weights correlate {d['corr_logw']:.3f} with the true ones: high correlation indicates similar ranking of weights, but is invariant to scale and does not establish an accurate density ratio. The revised experiment also saves the normalized empirical target-law TV error. <bookmark mark='c'/> But the weights are very unequal. Kish's effective sample size, Part eighteen's, is the square of their sum over the sum of their squares: about {d['ess']['estimated']:.0f}, out of about {d['n_cal']:,.0f} calibration points. <bookmark mark='d'/> The intervals rest mostly on the few older adults the study did include, and the single largest weight carries {100 * d['wmax']['estimated']:.0f} percent of the total. Report the effective sample size beside every weighted interval.",
            [(r"\mathrm{corr}(\log\hat w, \log w)", r"=", rf"{d['corr_logw']:.3f}", 40),
             (r"n_{\text{eff}}", r"=", r"(\textstyle\sum w_i)^2 / \sum w_i^2", 40),
             (r"\text{here}", r":", rf"{d['ess']['estimated']:.0f} \ \text{{of}} \ {d['n_cal']:,.0f}".replace(",", "{,}"), 40),
             (r"\text{largest weight}", r":", rf"{100 * d['wmax']['estimated']:.0f}\% \ \text{{of the total}}", 40)],
            [r"ranking is not ratio accuracy", r"Part 18's Kish", r"weight concentration", r"report it"],
            colors=[(2, NAIVEC)])

    def workflow(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In practice no one knows the truth, so here is the workflow the application suggests. <bookmark mark='b'/> Fit the classifier for the weights on data separate from the calibration set, and check it, by its calibration and its area under the curve, as in Part thirty-four. <bookmark mark='c'/> Compute the effective sample size of the weighted calibration set, and the share of the largest weight; large maximum shares or low Kish effective size flag concentration and potential instability, not a formal impossibility of target inference. AUC measures discrimination and does not itself certify density-ratio accuracy or interval coverage. <bookmark mark='d'/> Then report the weighted interval beside the unweighted one. A large difference is itself the finding: weighting changes this particular calibrated residual distribution. That interval difference alone does not measure a unique amount of population shift.",
            [(r"\text{weights}", r":", r"\text{a checked classifier, \ separate data}", 40),
             (r"\text{diagnose}", r":", r"n_{\text{eff}}, \ \text{the largest weight}", 40),
             (r"\text{alarm}", r":", r"\text{concentrated weights; \ check overlap}", 40),
             (r"\text{report}", r":", r"\text{weighted beside unweighted}", 40)],
            [r"Part 34", r"Part 18", r"diagnostic, not a theorem", r"sensitivity to weighting"],
            colors=[(3, HONC)])
