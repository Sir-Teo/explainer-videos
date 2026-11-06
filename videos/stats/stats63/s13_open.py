from __future__ import annotations

from videos.stats.stats63.common import *  # noqa: F403


class OpenProblems(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter twelve. Open problems in privacy and fairness.", 12, r"Open problems",
                            r"Where the guarantees stop")
        self.map_()
        self.op_inference()
        self.op_epsilon()
        self.op_models()
        self.op_dynamics()
        self.op_together()
        self.problems()

    def map_(self):
        hdr = [r"the worry", r"the tool", r"what it costs"]
        body = [
            [r"linkage and reconstruction", r"differential privacy", r"noise"],
            [r"an attacker's test", r"trade-off curves, \ GDP", r"a curve, \ not one number"],
            [r"many releases", r"R\'enyi and zCDP accountants", r"nothing: \ tighter bounds"],
            [r"no trusted curator", r"local privacy", r"$n \to n\varepsilon^2$"],
            [r"intervals on noisy data", r"noise-aware inference", r"wider, \ honest intervals"],
            [r"consistent published tables", r"post-processing", r"bias in small cells"],
            [r"memorizing models", r"DP-SGD, \ audits", r"accuracy, \ unequally"],
            [r"unequal error rates", r"a choice of criterion", r"another criterion"],
            [r"miscalibrated subgroups", r"multicalibration", r"data per cell"],
            [r"unfair paths", r"counterfactual fairness", r"a causal model"],
        ]
        cols = [GREY_B, PRIVC, PRIVC, OKC, BADC, OKC, PRIVC, PRIVC, GRPA, OKC, GRPB]
        tab = table_rows([hdr] + body, font_size=24, col_buff=0.7, row_buff=0.22, colors=cols).move_to([0, 0.1, 0])
        if tab.width > 13.4:
            tab.width = 13.4
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table: each worry, the tool that answers it, and what the tool costs. "
            "<bookmark mark='b'/> Linkage and reconstruction, answered by differential privacy, at the price of noise. An "
            "attacker's test, read off a trade-off curve. Many releases, tracked by accountants that cost nothing but "
            "mathematics. No trusted curator, local privacy, at the price of a smaller effective sample. Intervals on noisy "
            "data, which must widen to be honest. Consistent tables, bought with bias in small cells. Memorizing models, "
            "trained privately at a cost in accuracy that falls unequally. <bookmark mark='c'/> Then fairness: unequal "
            "error rates, where choosing one criterion gives up another; miscalibrated subgroups, repaired by "
            "multicalibration with enough data per cell; and unfair paths, which need a causal model to name."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:8]], lag_ratio=0.6), run_time=16.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[8:]], lag_ratio=0.6), run_time=6.0)
        self.wait(1.0)
        self.clear_scene()

    def op_inference(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem one: private inference beyond simple statistics. <bookmark mark='b'/> For a "
            "proportion or a mean, noise-aware intervals are understood. For a regression with many coefficients, a "
            "mixed model, or a survival analysis on privatized data, valid finite-sample intervals are mostly not known, "
            "and the parametric bootstrap can fail when the privacy noise and clipping interact. <bookmark mark='c'/> "
            "Private synthetic data, released for analysts to explore freely, is a promising route, but inference from it "
            "is valid only for the analyses its generator anticipated. <bookmark mark='d'/> Efficient, valid private "
            "inference for the models of Parts twenty-three to forty is open.",
            [(r"\text{problem 1}", r":", r"\text{private inference, \ beyond the mean}", 40),
             (r"\text{regression, \ mixed models}", r":", r"\text{finite-sample validity unknown}", 40),
             (r"\text{synthetic data}", r":", r"\text{valid for anticipated analyses}", 40),
             (r"\text{open}", r":", r"\text{efficient valid private inference}", 40)],
            [r"chapter 5's limits", r"clipping and noise", r"Raghunathan, \ Reiter \& Rubin (2003)", r"Parts 23--40"],
            colors=[(3, BADC)])

    def op_epsilon(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem two: what epsilon means. <bookmark mark='b'/> Deployed systems use budgets from "
            "below one to above ten, and the worst-case guarantee at epsilon of ten says almost nothing. <bookmark "
            "mark='c'/> Yet attacks on such systems often fail, which suggests the worst case is far from the typical case. "
            "Per-person accounting, which charges each individual for their actual influence, and the trade-off curves of "
            "chapter two are partial answers. <bookmark mark='d'/> A principled way to choose and to explain a budget, "
            "connecting the guarantee to the harms people care about, is open.",
            [(r"\text{problem 2}", r":", r"\text{the meaning of } \varepsilon", 40),
             (r"\text{deployed}", r":", r"\varepsilon \text{ from } {<}1 \text{ to } {>}10", 40),
             (r"\text{typical vs worst}", r":", r"\text{individual accounting, \ curves}", 40),
             (r"\text{open}", r":", r"\text{choosing and explaining a budget}", 40)],
            [r"chapter 6", r"weak bounds", r"partial answers", r"Abowd \& Schmutte (2019)"],
            colors=[(3, BADC)])

    def op_models(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem three: privacy for foundation models. <bookmark mark='b'/> Training with "
            "DP-SGD at the scale of modern language models costs accuracy and computation, and the unit of privacy is "
            "unclear: one document, one user who wrote thousands, or one fact repeated across the web. <bookmark mark='c'/> "
            "Fine-tuning a publicly pretrained model privately works far better than training from scratch, but the "
            "pretraining data were not private. <bookmark mark='d'/> What guarantee is meaningful for a model trained on "
            "the internet, and how to audit it with one training run, is open.",
            [(r"\text{problem 3}", r":", r"\text{privacy for foundation models}", 40),
             (r"\text{the unit}", r":", r"\text{document, \ user, \ or fact?}", 40),
             (r"\text{public pretraining}", r":", r"\text{private fine-tuning works}", 40),
             (r"\text{open}", r":", r"\text{meaningful, \ auditable guarantees}", 40)],
            [r"chapter 7", r"user-level privacy", r"not private upstream", r"Part 64"],
            colors=[(3, BADC)])

    def op_dynamics(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem four: fairness over time. <bookmark mark='b'/> Decisions change the data: a "
            "lending rule changes who repays, and a policing model changes where arrests are recorded, which changes the "
            "next model's training labels. Danielle Ensign and colleagues showed how predictive policing can run away in "
            "such a loop. <bookmark mark='c'/> Static criteria, checked once, can make the long-run outcome worse. "
            "<bookmark mark='d'/> Criteria and procedures with guarantees over the dynamics, which need causal models of the "
            "feedback, are open.",
            [(r"\text{problem 4}", r":", r"\text{fairness over time}", 40),
             (r"\text{feedback}", r":", r"\text{decisions change future labels}", 40),
             (r"\text{static criteria}", r":", r"\text{can worsen the long run}", 40),
             (r"\text{open}", r":", r"\text{guarantees over the dynamics}", 40)],
            [r"Liu et al. (2018)", r"Ensign et al. (2018)", r"delayed impact", r"Part 58's adaptivity"],
            colors=[(3, BADC)])

    def op_together(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Problem five: privacy and fairness together. <bookmark mark='b'/> Checking fairness "
            "needs group labels, often the most sensitive attributes of all, and auditing error rates by group from "
            "privatized data adds noise to the very small groups that most need checking. <bookmark mark='c'/> And chapter "
            "seven showed privacy's accuracy cost falls hardest on small groups. <bookmark mark='d'/> Procedures that are "
            "private, fair across many groups, and statistically efficient at once, with the trade-offs among the three "
            "priced exactly, are open.",
            [(r"\text{problem 5}", r":", r"\text{privacy and fairness at once}", 40),
             (r"\text{auditing}", r":", r"\text{needs sensitive group labels}", 40),
             (r"\text{DP's cost}", r":", r"\text{largest for small groups}", 40),
             (r"\text{open}", r":", r"\text{the three-way trade-off}", 40)],
            [r"sensitive attributes", r"chapter 5's noise", r"Bagdasaryan et al. (2019)", r"the frontier"],
            colors=[(3, BADC)])

    def problems(self):
        self.list_voiceover(
            "<bookmark mark='a'/> Five open problems. <bookmark mark='b'/> Private inference beyond simple statistics. "
            "<bookmark mark='c'/> The meaning of epsilon. <bookmark mark='d'/> Privacy for foundation models. <bookmark "
            "mark='e'/> Fairness over time. <bookmark mark='f'/> And privacy and fairness together.",
            [(r"Open problems", S.ACCENT),
             (r"1. \ private inference beyond simple statistics", WHITE),
             (r"2. \ the meaning of $\varepsilon$", WHITE),
             (r"3. \ privacy for foundation models", WHITE),
             (r"4. \ fairness over time", WHITE),
             (r"5. \ privacy, \ fairness and efficiency together", WHITE)],
            buff=0.42, font_size=25, head_size=40)
