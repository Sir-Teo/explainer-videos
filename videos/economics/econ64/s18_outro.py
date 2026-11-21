from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403
from videos.economics.econ64.s01_hook import courtroom

PROBLEMS = [
    r"Prediction policy: \ a programme helps only people who would otherwise fail, \ by a fixed amount; \ show that "
    r"ranking by the chance of failing is then optimal, \ and give an example where it is not.",
    r"Selective labels: \ if judges detain on a signal $s$ that raises risk and the model omits it, \ show that "
    r"filling in the detained's outcomes with the model's prediction understates their failures.",
    r"Double ML: \ in $y = \theta d + g(X) + \varepsilon$, \ $d = m(X) + v$, \ show that the residual-on-residual "
    r"estimator's error depends on $(\hat m - m)(\hat\ell - \ell)$ to first order.",
    r"Prediction-powered inference: \ show that $\bar f_{N} + \overline{(y - f)}_{n}$ is unbiased for the mean "
    r"of $y$, \ and find its variance.",
    r"Brock and Mirman: \ with log utility and full depreciation, \ guess $k' = s\,k^{\alpha}$ and verify that "
    r"$s = \alpha\beta$ solves the Euler equation.",
    r"$\bigstar$ \ Chouldechova: \ derive "
    r"$\text{FPR} = \frac{p}{1-p}\,\frac{1-\text{PPV}}{\text{PPV}}\,(1-\text{FNR})$, \ and show that "
    r"equal PPV and unequal base rates force unequal error rates.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).move_to(UP * 2.4)
        a = wrapped_label(r"It makes prediction cheap, \ and so separates the questions that need only a forecast "
                          r"from those that need a cause. \ For the first, \ it can beat experts, \ if the outcomes "
                          r"the decision hid are handled by design. \ For the second, \ it helps only inside a "
                          r"design: \ double machine learning, \ causal forests, \ corrected measurements. \ It can "
                          r"solve models, \ act in markets and propose hypotheses; \ it cannot say what would have "
                          r"happened, \ or which errors matter more.", 11.6, 26, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        g, _, _ = courtroom()
        fl = g.scale(0.4).next_to(a, DOWN, buff=0.4)
        with self.voiceover(
            "So: what does machine learning change in how economics is done? <bookmark mark='a'/> It makes "
            "prediction cheap, and so separates the questions that need only a forecast from those that need a "
            "cause. For the first, it can beat experts, if the outcomes the decision hid are handled by design. For "
            "the second, it helps only inside a design: double machine learning, causal forests, corrected "
            "measurements. It can solve our models, act in our markets and propose hypotheses. It cannot tell us "
            "what would have happened, or which errors matter more."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(FadeIn(fl), run_time=1.5)
        self.clear_scene()

    def recap(self):
        Cc, K, T, D, X, E_, A, F = (load(x) for x in ("courts", "contraction", "targeting", "dml", "text", "euler",
                                                      "agents", "fairness"))
        P = T["per100"]
        items = [
            (r"prediction policy: \ the umbrella, \ not the rain dance; \ Meehl, \ right", ALGO),
            (r"Play it: \ the algorithm detains the missed dates, \ the judge the violent charges", JUDGE),
            (rf"the Island's courts: \ {100 * Cc['crime_cut']:.0f}\% fewer failures, \ or "
             rf"{100 * Cc['detain_cut']:.0f}\% fewer detained", GAIN),
            (rf"selective labels: \ filling in says {100 * K['naive']:.1f}, \ the truth {100 * K['truth']:.1f}; \ "
             r"contraction", JUDGE),
            (rf"not causation: \ by risk {P['highest risk']:.0f}, \ by estimated effect "
             rf"{P['largest effect (estimated)']:.0f} per 100 places", NAIVE),
            (rf"double ML: \ {D['double ML']['mean']:.2f} against 1; \ linear controls "
             rf"{D['linear controls']['mean']:.2f}", CAUSE),
            (r"causal forests and policy learning: \ close to the best allocation", ALGO),
            (rf"predicted labels: \ a classifier's {100 * X['classifier']['mean']:.1f}\% against "
             rf"{100 * X['share']:.0f}\%; \ PPI corrects", TEXT),
            (rf"a network learns $s = \alpha\beta$ to within {E_['max_err']:.5f}", NET),
            (rf"Q-learners price {A['mean_gain']:.0%} of the way to monopoly".replace("%", r"\%"), COST),
            (r"language models: \ cheap pilots and assistants, \ validated against people", NET),
            (rf"fairness: \ false positives {100 * F['A']['fpr']:.0f}\% and {100 * F['B']['fpr']:.0f}\% from a "
             r"calibrated score", GROUPB),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=27, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 64, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        with self.voiceover(
            "Part sixty-four in twelve lines. <bookmark mark='r1'/> Some decisions need only a forecast. <bookmark "
            "mark='r2'/> Judges weigh vivid facts; algorithms weigh predictive ones. <bookmark mark='r3'/> Ranking "
            "by a model can prevent more failures, or jail fewer people. <bookmark mark='r4'/> The outcomes a "
            "decision hides need a design, not a guess. <bookmark mark='r5'/> The most at risk are not always the "
            "most helped. <bookmark mark='r6'/> Double machine learning keeps the learner's errors out of the "
            "effect. <bookmark mark='r7'/> Causal forests find who gains, and policy learning allocates. <bookmark "
            "mark='r8'/> A predicted label is a measurement, and can be corrected. <bookmark mark='r9'/> Networks "
            "can solve models. <bookmark mark='r10'/> Learning agents can learn to collude. <bookmark mark='r11'/> "
            "Language models are pilots and assistants, not people. <bookmark mark='r12'/> And no score is fair in "
            "every sense at once."
        ) as vo:
            self.play(FadeIn(head))
            for i, r_ in enumerate(rows):
                vo.wait_until(f"r{i + 1}")
                self.play(FadeIn(r_, shift=RIGHT * 0.15), run_time=0.8)
            self.play(Indicate(rows, color=WHITE, scale_factor=1.0), run_time=2.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20, width=13.0)
        with self.voiceover(
            "The problems: when ranking by risk is optimal; why filling in hidden outcomes misleads; double machine "
            "learning's product of errors; the variance of prediction-powered inference; Brock and Mirman's saving "
            "rate; and a starred problem deriving Chouldechova's identity. Full solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Susan Athey and Guido Imbens, \ ``Machine Learning Methods That Economists Should Know About'', "
             r"\emph{Annual Review of Economics} (2019)",
             r"Sendhil Mullainathan and Jann Spiess, \ ``Machine Learning: \ An Applied Econometric Approach'', "
             r"\emph{Journal of Economic Perspectives} (2017)",
             r"Trevor Hastie, \ Robert Tibshirani and Jerome Friedman, \emph{The Elements of Statistical Learning} "
             r"(2nd ed., \ 2009)"],
            [r"Meehl (1954); \ Brock and Mirman (1972); \ Robinson (1988); \ Kleinberg et al.\ (2015, \ 2017, \ 2018)",
             r"Chernozhukov et al.\ (2018); \ Wager and Athey (2018); \ Kitagawa and Tetenov (2018); \ Athey and "
             r"Wager (2021)",
             r"Jean et al.\ (2016); \ Gentzkow, \ Kelly and Taddy (2019); \ Obermeyer et al.\ (2019); \ "
             r"Angelopoulos et al.\ (2023)",
             r"Calvano et al.\ (2020); \ Chouldechova (2017); \ Zheng et al.\ (2022); \ Horton (2023); \ Ludwig and "
             r"Mullainathan (2024)"])
        with self.voiceover(
            "The reading: Susan Athey and Guido Imbens on the machine-learning methods economists should know; "
            "Mullainathan and Spiess's applied econometric approach; and Hastie, Tibshirani and Friedman's Elements "
            "of Statistical Learning. Then the papers, from Meehl to the language models."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1930, r"Keynes writes to his grandchildren", r"in a hundred years, \ he says, \ the "
                          r"standard of living will be four to eight times higher and the working week fifteen "
                          r"hours; \ the hundred years are up in 2030", color=E.ACCENT, width=10.4, font_size=23)
        nxt = VGroup(label(r"Next: \ Part 65 \ $\cdot$ \ Act XII, \ The Frontier", font_size=30, color=GREY_B),
                     label(r"The Economics of AI", font_size=46),
                     label(r"what happens to work, \ growth and incomes if machines can do most tasks?", font_size=24,
                           color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from machines that help economists to machines that change the economy", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        steps_ = VGroup(*[VGroup(RoundedRectangle(width=2.9, height=0.9, corner_radius=0.12, stroke_color=c_,
                                                  stroke_width=2.0), label(t_, font_size=18, color=c_))
                          for t_, c_ in ((r"the task model", ALGO), (r"the experiments", GAIN),
                                         (r"wages and the labour share", GDP), (r"growth and ideas", NET))])
        for s_ in steps_:
            s_[1].move_to(s_[0])
        steps_.arrange(RIGHT, buff=0.3)
        VGroup(hc, steps_, nxt).arrange(DOWN, buff=0.45).next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Next time, from machines that help economists to machines that change the economy. <bookmark "
            "mark='a'/> In 1930, in the first year of the Depression, John Maynard Keynes wrote an essay for his "
            "grandchildren. In a hundred years, he said, the standard of living would be four to eight times "
            "higher, and the working week fifteen hours. He was right about the first. The hundred years are up in "
            "2030. <bookmark mark='b'/> The task model, the experiments with AI at work, wages and the labour "
            "share, and growth when ideas can be automated. <bookmark mark='c'/> Part sixty-five: the economics of "
            "AI."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
