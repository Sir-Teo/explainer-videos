from __future__ import annotations

import numpy as np

from videos.stats.stats62.common import *  # noqa: F403


class Fusion(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter eight. Data fusion and transportability: carrying an effect to a new population.", 8,
                            r"Transportability", r"From the trial to the target", lit=(2016,))
        self.problem()
        self.selection()
        self.formula()
        self.chart()
        self.fusion()
        self.meta()
        self.sites()
        self.limits()

    def problem(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A trial answers its question for the people it enrolled. Trials enrol the young, the "
            "healthy, the nearby. <bookmark mark='b'/> If the effect varies with age, the trial's average effect is not the "
            "target population's. <bookmark mark='c'/> Elias Bareinboim and Judea Pearl formalized when an effect can be "
            "carried across, transportability, in a series of papers culminating in 2016. <bookmark mark='d'/> Part "
            "thirty-five gave the inverse-odds estimator; this chapter gives the conditions and their graph.",
            [(r"\text{trial}", r":", r"\text{its own population}", 40),
             (r"\text{if}", r":", r"\tau(x) \text{ varies and } P_{\text{trial}}(x) \ne P_{\text{target}}(x)", 40),
             (r"\text{transportability}", r":", r"\text{Bareinboim \& Pearl (2016)}", 40),
             (r"\text{estimator}", r":", r"\text{Part 35's inverse odds}", 40)],
            [r"external validity", r"effect modification", r"selection diagrams", r"Westreich et al.; \ Dahabreh et al."],
            colors=[(1, NAIVEC)])

    def selection(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> A selection diagram marks mechanisms that may differ across populations; its selection nodes are not automatically the same as a sample-membership indicator. <bookmark mark='b'/> Transport of conditional responses needs an appropriate separation condition in the post-intervention graph, together with support. Selection pointing at covariates alone does not make every conditioning set admissible. <bookmark mark='c'/> If conditional causal effects are invariant given suitable measured covariates, averaging the trial's conditional effect over the target covariates identifies the target effect. <bookmark mark='d'/> An outcome-mechanism difference can invalidate response transport, but an additive baseline shift might still preserve a treatment contrast. The exact target functional and invariances determine the answer.",
            [(r"\text{selection diagram}", r":", r"S \to \text{what differs}", 40),
             (r"Y\perp S\mid X,do(A)\ \text{and overlap}", r"\Rightarrow", r"\tau_{\text{trial}}(x) = \tau_{\text{target}}(x)", 40),
             (r"\tau_{\text{target}}", r"=", r"\int \tau_{\text{trial}}(x)\,dP_{\text{target}}(x)", 40),
             (r"S \to Y", r":", r"\text{response transport may fail; \ contrast invariance can differ}", 40)],
            [r"Pearl \& Bareinboim (2011)", r"$S \perp Y \mid X, A$", r"standardization", r"the limit"],
            colors=[(2, IDC), (3, NAIVEC)])

    def formula(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Two estimators, mirroring Part thirty-six. <bookmark mark='b'/> Outcome modelling: fit the "
            "conditional effect in the trial, and average it over the target's covariates. <bookmark mark='c'/> Weighting: "
            "fit the probability of being in the trial given X, on the stacked samples, and weight each trial participant by "
            "the odds of being in the target instead. <bookmark mark='d'/> Issa Dahabreh and co-authors gave the doubly "
            "robust combination in 2019, efficient when both models are right and consistent when either is.",
            [(r"\text{outcome model}", r":", r"\tfrac1m\sum_{j \in \text{target}} \hat\tau(x_j)", 40),
             (r"\text{inverse odds}", r":", r"w_i = \frac{1 - \hat p(x_i)}{\hat p(x_i)}, \ \ p = P(\text{trial} \mid x)", 40),
             (r"\text{doubly robust}", r":", r"\text{either model}", 40),
             (r"\text{needs}", r":", r"\text{overlap of covariates}", 40)],
            [r"g-computation", r"Westreich et al. (2017)", r"Dahabreh et al. (2019)", r"Part 60's weights again"],
            colors=[(2, IDC)])

    def chart(self):
        d = load("fusion")
        a, b = np.asarray(d["tr_est"]), np.asarray(d["tp_est"])
        xs = np.linspace(0.2, 2.4, 300)

        def kde(v, h):
            return np.exp(-0.5 * ((xs[:, None] - v[None]) / h) ** 2).sum(1) / (len(v) * h * np.sqrt(2 * np.pi))
        ya, yb = kde(a, 0.03), kde(b, 0.06)
        top = float(max(ya.max(), yb.max())) * 1.1
        A = axes([0.2, 2.4], [0, top], x_length=7.4, y_length=4.4, xlabel=r"estimated average effect in the target population", ylabel=r"density over 200 trials",
                 xticks=[0.5, 1, 1.5, 2], yticks=[0, 1, 2, 3, 4], center=[-2.5, 0.2, 0])
        ax = A.ax
        ca = VGroup(shade(ax, xs, ya, NAIVEC, 0.25), curve(ax, xs, ya, NAIVEC, 3.5))
        cb = VGroup(shade(ax, xs, yb, IDC, 0.25), curve(ax, xs, yb, IDC, 3.5))
        tl = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], top * 0.98), color=GOLDC, stroke_width=2.5)
        side = side_groups([
            [(r"effect $= 0.05(\mathrm{age} - 20)$", WHITE), (rf"trial mean age {d['mean_age_trial']:.0f}, \ target {d['mean_age_target']:.0f}", GREY_A)],
            [(rf"gold: \ mean nonparticipant target effect, \ {d['truth']:.2f}", GOLDC)],
            [(rf"red: \ the trial's own estimate, \ {d['trial']:.2f}", NAIVEC)],
            [(rf"green: \ oracle selection-odds weighted, \ {d['transported']:.2f}", IDC), (rf"sd {d['transported_sd']:.2f}; \ ESS {d['ess']:.0f} of {d['n_trial']}", IDC)],
        ])
        with self.voiceover(
            "<bookmark mark='a'/> In this simulation the treatment effect increases with age and trial selection favors younger adults. <bookmark mark='b'/> The target is each repetition's nonparticipant population, rather than the entire original pool. The gold line displays its average true effect; the individual target truths are also recorded. <bookmark mark='c'/> The trial's arm difference describes its selected participants and is lower than that target effect. <bookmark mark='d'/> The green estimate uses the known, simulated selection odds, so this is an oracle weighting example rather than a validated fitted membership model. It has greater variability and some observed finite-sample error; normalized weighting is not exactly unbiased. Kish ESS diagnoses concentration but is not a complete variance calculation."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated, \ 200 trials")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(tl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(ca), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(cb), FadeIn(side[3]), run_time=1.5)
        self.clear_scene()

    def fusion(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Data fusion goes further: combine several studies, each partial. <bookmark mark='b'/> A "
            "small trial and a large observational study can be combined so the trial corrects the observational study's "
            "confounding, and the observational study extends the trial's reach: Kallus, Puli and Shalit, and others. "
            "<bookmark mark='c'/> Bareinboim and Pearl's do-calculus for fusion decides, from a set of selection diagrams, "
            "which combinations identify the target effect. <bookmark mark='d'/> Part sixty-three's privacy constraints add "
            "a twist: studies that cannot share individual records must be fused from summaries.",
            [(r"\text{fusion}", r":", r"\text{several partial studies}", 40),
             (r"\text{trial + observational}", r":", r"\text{each corrects the other}", 40),
             (r"\text{decision}", r":", r"\text{do-calculus with selection diagrams}", 40),
             (r"\text{privacy}", r":", r"\text{fuse from summaries}", 40)],
            [r"the general problem", r"Kallus, \ Puli \& Shalit (2018)", r"Bareinboim \& Pearl (2016)", r"Part 63"],
            colors=[(2, IDC)])

    def limits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Transport requires a clearly specified target and assumptions connecting it to the study. <bookmark mark='b'/> Without target-support coverage in the trial, reweighting cannot identify the missing response surface without extrapolation assumptions. <bookmark mark='c'/> Measured covariates must suffice for the required conditional effect invariance. An unmeasured modifier need not bias transport if its relevant distribution does not differ after conditioning; it is not necessary to measure every conceivable modifier. <bookmark mark='d'/> Sensitivity analyses can study violations within a specified model, rather than making transport assumption-free.",
            [(r"\text{overlap}", r":", r"\text{or extrapolation}", 40),
             (r"\text{sufficient modifiers for population differences}", r":", r"\text{measured in both samples}", 40),
             (r"\text{else}", r":", r"\text{biased, \ like a hidden confounder}", 40),
             (r"\text{remedy}", r":", r"\text{sensitivity bounds}", 40)],
            [r"Part 60", r"the transport assumption", r"untestable", r"chapter 2"],
            colors=[(2, NAIVEC)])

    def meta(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Meta-analysis is the oldest form of fusion. <bookmark mark='b'/> Part twenty-five's "
            "random-effects model treats each study's effect as a draw from a distribution, and estimates its mean and "
            "spread. <bookmark mark='c'/> Transportability adds a reason for the spread: studies enrol different people, so "
            "their effects differ by their covariate mix. <bookmark mark='d'/> Transporting each study to a common target "
            "population before combining, as Dahabreh and co-authors propose, separates genuine effect heterogeneity from "
            "differences in who was studied.",
            [(r"\text{meta-analysis}", r":", r"\text{effects as random draws}", 40),
             (r"\text{transport}", r":", r"\text{a reason for heterogeneity}", 40),
             (r"\text{standardize}", r":", r"\text{each study to one target}", 40),
             (r"\text{then}", r":", r"\text{combine}", 40)],
            [r"Part 25", r"case mix", r"causally interpretable meta-analysis", r"Dahabreh et al. (2020)"],
            colors=[(2, IDC)])

    def sites(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Meager's analysis pooled seven randomized microcredit evaluations with a Bayesian hierarchical model. <bookmark mark='b'/> It separates sampling noise from estimated between-site effect variation under that model. <bookmark mark='c'/> Limited estimated heterogeneity for some outcomes does not establish equality of effects or describe every new population. Posterior uncertainty and outcome-specific findings matter. <bookmark mark='d'/> Predicting effects in a new site additionally needs a model for how that site relates to the studied sites. Between-site spread alone is not a complete measure of generalizability.",
            [(r"\text{seven sites}", r":", r"\text{microcredit, \ randomized}", 40),
             (r"\text{model}", r":", r"\text{Bayesian hierarchical}", 40),
             (r"\text{finding}", r":", r"\text{small effects, \ little true heterogeneity}", 40),
             (r"\text{lesson}", r":", r"\text{new-site prediction needs a model and uncertainty}", 38)],
            [r"Meager (2019)", r"Part 25", r"noise, \ not difference", r"partial pooling"],
            colors=[(3, IDC)])
