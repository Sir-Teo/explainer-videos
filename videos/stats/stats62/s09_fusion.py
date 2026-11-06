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
            "<bookmark mark='a'/> The tool is a selection diagram: the causal graph plus a node S, pointing at whatever "
            "differs between the populations. <bookmark mark='b'/> If S points only at covariates X, and X blocks every path "
            "from S to the outcome given treatment, then conditional effects are the same in both populations. <bookmark "
            "mark='c'/> The target's effect is the trial's conditional effect, averaged over the target's distribution of X. "
            "<bookmark mark='d'/> If S points at the outcome mechanism itself, no reweighting can help: the populations "
            "respond differently, and only target data can say how.",
            [(r"\text{selection diagram}", r":", r"S \to \text{what differs}", 40),
             (r"S \to X \text{ only}", r"\Rightarrow", r"\tau_{\text{trial}}(x) = \tau_{\text{target}}(x)", 40),
             (r"\tau_{\text{target}}", r"=", r"\int \tau_{\text{trial}}(x)\,dP_{\text{target}}(x)", 40),
             (r"S \to Y", r":", r"\text{not transportable}", 40)],
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
            [(rf"gold: \ the target's effect, \ {d['truth']:.2f}", GOLDC)],
            [(rf"red: \ the trial's own estimate, \ {d['trial']:.2f}", NAIVEC)],
            [(rf"green: \ inverse-odds transported, \ {d['transported']:.2f}", IDC), (rf"sd {d['transported_sd']:.2f}; \ ESS {d['ess']:.0f} of {d['n_trial']}", IDC)],
        ])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation. The effect grows with age, a twentieth of a unit per year. The trial "
            f"recruits the young: its mean age is {d['mean_age_trial']:.0f}, the target's {d['mean_age_target']:.0f}. "
            f"<bookmark mark='b'/> The target's average effect is {say(d['truth'], 2)}. <bookmark mark='c'/> Over two hundred "
            f"simulated trials, the trial's own estimate averages {say(d['trial'], 2)}: precise, and correct for the trial, "
            f"but less than half the target's effect. <bookmark mark='d'/> Transported by inverse odds of trial membership, "
            f"it averages {say(d['transported'], 2)}, with twice the spread: the effective sample size falls to about "
            f"{d['ess']:.0f} of {d['n_trial']}, because old participants are rare and heavily weighted."
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
            "<bookmark mark='a'/> The limits are the ones Part sixty met under covariate shift. <bookmark mark='b'/> Overlap: "
            "if the target contains people unlike anyone in the trial, there is nothing to reweight, only extrapolation. "
            "<bookmark mark='c'/> The effect modifiers must all be measured in both samples; one missing modifier breaks the "
            "transport as surely as a hidden confounder breaks adjustment. <bookmark mark='d'/> And sensitivity analysis, as "
            "in chapter two, can bound how far an unmeasured modifier could move the transported answer.",
            [(r"\text{overlap}", r":", r"\text{or extrapolation}", 40),
             (r"\text{all modifiers}", r":", r"\text{measured in both samples}", 40),
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
            "<bookmark mark='a'/> External validity across real sites. <bookmark mark='b'/> Rachael Meager pooled seven "
            "randomized evaluations of microcredit, from Bosnia to Mongolia, with a Bayesian hierarchical model in 2019. "
            "<bookmark mark='c'/> The average effects on household business profit were small and similar across sites once "
            "sampling noise was accounted for: much of the apparent disagreement among the studies was noise. <bookmark "
            "mark='d'/> Partial pooling, Part twenty-five's idea, is how one learns how far a result travels: the estimated "
            "between-site spread is the honest answer to whether it generalizes.",
            [(r"\text{seven sites}", r":", r"\text{microcredit, \ randomized}", 40),
             (r"\text{model}", r":", r"\text{Bayesian hierarchical}", 40),
             (r"\text{finding}", r":", r"\text{small effects, \ little true heterogeneity}", 40),
             (r"\text{lesson}", r":", r"\text{the between-site spread measures generalizability}", 38)],
            [r"Meager (2019)", r"Part 25", r"noise, \ not difference", r"partial pooling"],
            colors=[(3, IDC)])
