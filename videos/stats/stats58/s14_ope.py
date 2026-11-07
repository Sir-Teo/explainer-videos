from __future__ import annotations

from videos.stats.stats58.common import *  # noqa: F403


class OffPolicy(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter thirteen. Off-policy evaluation: what would have happened under a policy we did not "
                       "run?", 13, r"Off-policy evaluation", r"Evaluating the policy you did not run")
        self.question()
        self.ipw()
        self.dr()
        self.results()
        self.variance()
        self.uses()

    def question(self):
        heading = label('A fixed target policy and logged actions', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> The adaptive experiment is over, and its logs record, for each visitor, the "
            "design shown, the probability of showing it, and the response. <bookmark mark='b'/> A manager asks: "
            "what would the conversion rate have been if we had always shown design A? <bookmark mark='c'/> That "
            'policy was never run; but every visitor who happened to see A is evidence about it. <bookmark '
            "mark='d'/> This is Part thirty-five's potential outcomes question, with a known, changing assignment "
            'mechanism.'
        ),
            [(r"\text{logs}", r":", r"(A_t, \ e_t(A_t), \ Y_t), \ t = 1, \dots, T", 40),
             (r"\text{target}", r":", r"V(\pi) = E[Y(\pi)] \text{ for a policy } \pi", 40),
             (r"\text{e.g.}", r":", r"\pi = \text{always show A}", 40),
             (r"\text{a causal question}", r":", r"\text{with a known assignment mechanism}", 38)],
            [r"recorded propensities", r"a counterfactual", r"never run", r"Part 35"],
            colors=[(1, BANDITC)])

    def ipw(self):
        heading = label('Known positive conditional propensities', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> For a fixed target policy, weight each logged response by target action "
            "probability divided by its known conditional logging probability. <bookmark mark='b'/> Under "
            'sequential randomization and the stationary outcome model, each score has the target value in '
            'conditional expectation. Its mean is unbiased over repetitions of the experiment, not conditional on '
            "the complete realized logs. <bookmark mark='c'/> Every action used by the target needs positive "
            'logging probability. With contextual policies these probabilities and outcome models must condition on '
            "the relevant context. <bookmark mark='d'/> Small overlap can produce large variance. Normal confidence "
            'intervals need additional variance and martingale limit conditions.'
        ),
            [(r"\hat V_{\mathrm{IPW}}", r"=", r"\frac1T\textstyle\sum_t \frac{\pi(A_t)}{e_t(A_t)}\,Y_t", 40),
             (r"E[\hat V_{\mathrm{IPW}}]", r"=", r"V(\pi)", 40),
             (r"\text{needs}", r":", r"e_t(a) > 0 \text{ wherever } \pi(a) > 0", 40),
             (r"\text{variance}", r"\propto", r"E[\pi^2/e]: \ \text{large weights hurt}", 38)],
            [r"importance sampling", r"unbiased", r"overlap", r"Part 36's lesson"],
            colors=[(0, WEALTHC)])

    def dr(self):
        heading = label('Predictable outcome models and augmentation', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Add a fixed or predictable model of each arm's mean to obtain an augmented "
            "estimator. <bookmark mark='b'/> Predict the target value, then correct it using weighted residuals for "
            "the actions actually taken. <bookmark mark='c'/> With the true positive logging probabilities, the "
            'estimator remains unbiased even if this predictable model is wrong. A model fitted using the same '
            'future responses needs additional justification, such as a suitable independent evaluation design. A '
            'good model can reduce variance, but improvement is not automatic for an arbitrary fit. <bookmark '
            "mark='d'/> Dudik, Langford and Li developed this approach for bandit policy evaluation in 2011. Our "
            'numerical example uses a fixed constant model and asymptotic normal intervals.'
        ),
            [(r"\hat V_{\mathrm{DR}}", r"=", r"\frac1T\textstyle\sum_t \Big\{\sum_a \pi(a)\hat m(a) + \frac{\pi(A_t)}{e_t(A_t)}\big(Y_t - \hat m(A_t)\big)\Big\}", 34),
             (r"\text{model term}", r":", r"\text{the prediction}", 40),
             (r"\text{unbiased}", r":", r"\text{known propensities, predictable model; \ potential variance gain}", 38),
             (r"\text{history}", r":", r"\text{Dud\'ik, \ Langford \& Li (2011)}", 38)],
            [r"Part 36's AIPW", r"plug in", r"double robustness", r"bandit logs"],
            colors=[(0, CSC)])

    def results(self):
        d = load("ope")
        m0 = d["means"][0]
        hdr = [r"estimator", r"mean", r"SD across runs", r"95\% coverage"]
        body = [[r"IPW", f"{d['ipw_mean']:.4f}", f"{d['ipw_sd']:.4f}", f"{100 * d['ipw_cov']:.0f}\\%"],
                [r"doubly robust", f"{d['dr_mean']:.4f}", f"{d['dr_sd']:.4f}", f"{100 * d['dr_cov']:.0f}\\%"]]
        tab = table_rows([hdr] + body, font_size=30, col_buff=1.0, row_buff=0.35, colors=[GREY_B, WEALTHC, CSC]).move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"the policy ``always show A'', \ true value {m0:.2f}; \ logs from Thompson sampling, \ floor 0.05", font_size=24, color=GREY_A),
            label(rf"{d['reps']} runs of {d['T']:,} visitors; \ the model $\hat m$ is a crude constant, \ 0.11, \ for both designs", font_size=24, color=GREY_A),
            label(r"both unbiased; \ the model's help is small when it knows little", font_size=26, color=CSC),
        ), 12.4, 0.22, [0, -1.9, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> On the A/B logs: the policy always show design A, whose true value is {say(m0, 2)}. <bookmark "
            f"mark='b'/> Over {d['reps']} runs, inverse-propensity weighting averages {say(d['ipw_mean'], 4)}, with a "
            f"standard deviation of {say(d['ipw_sd'], 4)}, and its intervals cover {100 * d['ipw_cov']:.0f} percent. <bookmark "
            f"mark='c'/> The doubly robust estimator, with a crude constant model, averages {say(d['dr_mean'], 4)}, standard "
            f"deviation {say(d['dr_sd'], 4)}, coverage {100 * d['dr_cov']:.0f} percent. <bookmark mark='d'/> Both are unbiased; "
            f"the model's help is small when it knows little, and grows with a better model."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(simulated_tag(r"the World's A/B platform")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def variance(self):
        heading = label('An actual minimum assignment probability', font_size=30, color=WEALTHC).move_to([0, 3.35, 0])
        if heading.width > 12.5:
            heading.width = 12.5
        self.add(heading)
        self.lad_voiceover(
            (
            "<bookmark mark='a'/> Why did the experiment's floor matter? The weight on a visitor who saw design A "
            "is one over the probability of showing A. <bookmark mark='b'/> Thompson sampling drove that "
            'probability down as A looked worse; without a floor it can become very small, and a single such '
            "visitor would carry a weight of a thousand. <bookmark mark='c'/> The floor of five percent caps every "
            "weight at twenty. <bookmark mark='d'/> So an adaptive experiment meant for later evaluation should "
            "keep every arm's probability above a floor: a small cost in welfare, a large gain in what the logs can "
            'answer.'
        ),
            [(r"\text{weight}", r"=", r"1/e_t(\mathrm{A})", 40),
             (r"\text{no floor}", r":", r"e_t \to 0.001: \ \text{weight } 1{,}000", 40),
             (r"\text{floor } 0.05", r":", r"\text{weights} \le 20", 40),
             (r"\text{design rule}", r":", r"\text{floor the propensities}", 40)],
            [r"inverse propensity", r"one visitor dominates", r"capped", r"welfare vs evaluation"],
            colors=[(1, FIXEDC), (2, CSC)])

    def uses(self):
        self.list_voiceover(
            (
            "<bookmark mark='a'/> Where off-policy evaluation is used. <bookmark mark='b'/> Recommendation systems "
            "and advertising, to test a new ranking policy on old logs before deploying it. <bookmark mark='c'/> "
            'Medicine, to evaluate dynamic treatment regimes from sequentially randomized trials, a subject for '
            "Part sixty-two. <bookmark mark='d'/> And reinforcement learning, where the policy acts over many steps "
            'and the weights multiply, the hardest case of all.'
        ),
            [(r"where it is used:", GREY_A),
             (r"recommenders and advertising: \ test a policy on old logs", BANDITC),
             (r"medicine: \ dynamic treatment regimes \ (Part 62)", CSC),
             (r"reinforcement learning: \ weights multiply over steps", FIXEDC)])
