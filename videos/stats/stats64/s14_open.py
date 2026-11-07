from __future__ import annotations

from videos.stats.stats64.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter thirteen. Open problems for statistics in the age of AI.", 13, r"Open problems",
                            r"What the degree cannot yet answer")
        self.map_()
        self.op_construct()
        self.op_moving()
        self.op_agents()
        self.op_feedback()
        self.op_conditional()
        self.problems()

    def map_(self):
        hdr = [r"the claim", r"the old tool", r"the new setting"]
        body = [
            [r"a model's accuracy", r"a mean and its SE", r"clustered questions"],
            [r"model A beats model B", r"a paired test", r"correlated errors"],
            [r"the leaderboard's order", r"Bradley--Terry", r"crowds, \ style, \ selection"],
            [r"a cheap estimate", r"item response theory", r"many models, \ few items"],
            [r"a clean test score", r"a holdout", r"adaptive reuse, \ leakage"],
            [r"a judged score", r"prediction-powered inference", r"model-made labels"],
            [r"stable training data", r"the MLE", r"models fitted to models"],
            [r"a trustworthy answer", r"conformal sets", r"claims and generations"],
            [r"who wrote this", r"a binomial test", r"keyed word choices"],
            [r"a posterior", r"coverage checks", r"neural simulators"],
            [r"an effect on people", r"randomized designs", r"markets, \ long horizons"],
        ]
        cols = [GREY_B, MODB, MODB, MODB, MODB, HONC, JUDGEC, NAIVEC, HONC, MODB, JUDGEC, HONC]
        tab = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.2, colors=cols).move_to([0, 0.1, 0])
        if tab.width > 13.4:
            tab.width = 13.4
        if tab.height > 6.8:
            tab.height = 6.8
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table: each claim made about AI systems, the old statistical tool that "
            "checks it, and what is new about the setting. <bookmark mark='b'/> A model's accuracy is a mean with a standard "
            "error, clustered. A comparison is a paired test. A leaderboard's order is a Bradley-Terry fit, with crowds, style "
            "and selection to account for. A cheap estimate is item response theory. A clean test score needs a holdout "
            "protected from reuse and leakage. <bookmark mark='c'/> A judged score needs a few human labels to rectify it. "
            "Training data fitted to models must keep its anchor in real data. A trustworthy answer is a conformal set of "
            "claims. Authorship is a binomial test. A posterior from a simulator needs its coverage checked. And an effect on "
            "people needs a randomized design that respects how people interact."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:6]], lag_ratio=0.6), run_time=12.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[6:]], lag_ratio=0.6), run_time=14.0)
        self.wait(1.0)
        self.clear_scene()

    def op_construct(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem one: what benchmarks measure. <bookmark mark='b'/> A benchmark score is used as evidence of reasoning, or coding ability, or knowledge: a latent construct, in Part forty-one's and psychometrics' language. <bookmark mark='c'/> Whether a score measures its construct, and nothing else, is the question of construct validity, which educational testing spent a century on, and which model evaluation has barely begun. <bookmark mark='d'/> IRT and other measurement models already address parts of this question. Validating and transporting constructs across changing model families and uses remains an active research problem.",
            [(r"\text{problem 1}", r":", r"\text{construct validity}", 40),
             (r"\text{scores as evidence}", r":", r"\text{of a latent ability}", 40),
             (r"\text{psychometrics}", r":", r"\text{a century of method}", 40),
             (r"\text{open}", r":", r"\text{validated measurement of model abilities}", 40)],
            [r"what is measured", r"Part 41", r"Cronbach \& Meehl (1955)", r"chapter 4's IRT, \ extended"],
            colors=[(3, NAIVEC)])

    def op_moving(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem two: benchmarks that outlive their usefulness. <bookmark mark='b'/> Models now "
            "saturate a new benchmark within a year or two, and test questions leak into training data. <bookmark mark='c'/> "
            "Dynamic benchmarks, refreshed continually, can reduce leakage while complicating comparability across time: Part "
            "seventeen's problem of a changing measuring instrument. <bookmark mark='d'/> Designs for evaluation that stay "
            "comparable as the questions change, with linking and equating from testing, and that resist contamination, "
            "are open.",
            [(r"\text{problem 2}", r":", r"\text{saturation and leakage}", 40),
             (r"\text{dynamic benchmarks}", r":", r"\text{fresh, \ but not comparable}", 40),
             (r"\text{testing's answer}", r":", r"\text{linking and equating}", 40),
             (r"\text{open}", r":", r"\text{comparable, \ contamination-resistant designs}", 40)],
            [r"a short life", r"Part 17's drifting instrument", r"anchor items", r"chapter 5"],
            colors=[(3, NAIVEC)])

    def op_agents(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem three: evaluating agents. <bookmark mark='b'/> A model that acts over many "
            "steps, using tools and a computer, produces long trajectories whose outcomes are noisy and expensive: each "
            "episode can take hours. <bookmark mark='c'/> The relevant statistics are Part fifty-eight's sequential "
            "designs and Part sixty-two's off-policy evaluation: few, costly, highly variable episodes, and the wish to stop "
            "early. <bookmark mark='d'/> Variance reduction, anytime-valid comparisons and honest error bars for long-horizon "
            "agent evaluations are open.",
            [(r"\text{problem 3}", r":", r"\text{agents over many steps}", 40),
             (r"\text{episodes}", r":", r"\text{long, \ noisy, \ expensive}", 40),
             (r"\text{tools}", r":", r"\text{sequential tests, \ off-policy evaluation}", 40),
             (r"\text{open}", r":", r"\text{efficient, \ valid agent evaluation}", 40)],
            [r"interactive tasks", r"high variance", r"Parts 58 and 62", r"the frontier"],
            colors=[(3, NAIVEC)])

    def op_feedback(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem four: statistics with models in every loop. <bookmark mark='b'/> Models label "
            "the data, generate the data, judge the outputs, and are trained on the judgements: chapter six, chapter seven and "
            "chapter three at once. <bookmark mark='c'/> Each step's errors can be correlated with the next step's, which "
            "can break the sampling and conditional-mean assumptions used by a simple analysis. Prediction-powered inference permits predictor errors correlated with outcomes; the issue is uncontrolled fitting dependence, selection or shift, not any correlation of errors. <bookmark "
            "mark='d'/> Inference that remains valid when the measuring instruments are themselves trained on what they "
            "measure is open.",
            [(r"\text{problem 4}", r":", r"\text{models in every loop}", 40),
             (r"\text{label, \ generate, \ judge}", r":", r"\text{and train on it}", 40),
             (r"\text{breaks}", r":", r"\text{independence of errors}", 40),
             (r"\text{open}", r":", r"\text{validity with self-trained instruments}", 40)],
            [r"chapters 3, 6, 7", r"feedback", r"Parts 34 and 62", r"Part 65's question"],
            colors=[(3, NAIVEC)])

    def op_conditional(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem five: guarantees for this question. <bookmark mark='b'/> The conformal and coverage demonstrations average over their specified sampling experiments. Other guarantees, such as fixed-model testing bounds, condition on different objects; not every guarantee in this part is the same kind of marginal statement. <bookmark mark='c'/> A person relying on one answer wants a conditional statement, about their question, which Part fifty-seven proved impossible without assumptions, in general. <bookmark mark='d'/> Which useful conditional guarantees are achievable for generative models, over which classes of questions, and at what price in informativeness, is open.",
            [(r"\text{problem 5}", r":", r"\text{conditional guarantees}", 40),
             (r"\text{so far}", r":", r"\text{marginal, \ on average}", 40),
             (r"\text{impossible in general}", r":", r"\text{without assumptions}", 40),
             (r"\text{open}", r":", r"\text{which classes, \ at what price}", 40)],
            [r"for one person", r"chapters 1--12", r"Part 57", r"chapter 8"],
            colors=[(3, NAIVEC)])

    def problems(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> Construct validity for model evaluations. "
            "<bookmark mark='c'/> Benchmarks that stay comparable and clean. <bookmark mark='d'/> Evaluating agents. "
            "<bookmark mark='e'/> Inference with models in every loop. <bookmark mark='f'/> And conditional guarantees for "
            "generation.",
            [(r"Open problems", S.ACCENT),
             (r"1. \ construct validity of benchmarks", WHITE),
             (r"2. \ comparable, \ contamination-resistant evaluation", WHITE),
             (r"3. \ evaluating long-horizon agents", WHITE),
             (r"4. \ inference with models in every loop", WHITE),
             (r"5. \ conditional guarantees for generation", WHITE)],
            buff=0.42, font_size=25, head_size=40)
