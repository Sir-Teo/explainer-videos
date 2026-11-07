from __future__ import annotations

from videos.stats.stats56.common import *  # noqa: F403


class OpenProblems(VoiceoverScene):
    def construct(self):
        self.card()
        self.prices()
        self.referee()
        self.problems()

    def card(self):
        card = chapter_card(10, r"Open problems", r"Where the frontier is", part=PART)
        with self.voiceover("Chapter ten. Open problems: where the frontier of selective inference is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def prices(self):
        hdr = [r"approach", r"what it needs", r"what it costs"]
        body = [
            [r"PoSI, \ projection", r"nothing about the rule", r"up to $\sqrt p$ in width"],
            [r"conditional (polyhedral)", r"the exact rule; \ Gaussian noise", r"long intervals near the edge"],
            [r"randomization, \ carving", r"to randomize the rule", r"noisier selection"],
            [r"splitting, \ fission, \ thinning", r"a divisible family", r"half the information"],
            [r"knockoffs, \ conformal selection", r"known covariate law, \ or stated sampling conditions", r"an error rate, \ not intervals"],
            [r"hybrid (winners)", r"a simultaneous band", r"$\beta$ of the level"],
        ]
        tab = table_rows([hdr] + body, font_size=28, col_buff=0.7, row_buff=0.3,
                         colors=[GREY_B, SIMC, CONDC, SPLITC, SPLITC, HYBC, HYBC]).move_to([0, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The part in one table: what each approach needs, and what it costs. <bookmark mark='b'/> PoSI needs nothing about the selection rule and costs up to root p in width. Conditional inference needs the exact rule and Gaussian noise, and its intervals grow long near the edge of the selection region. Randomization needs you to randomize, and costs noisier selection. Splitting, fission and thinning need a divisible family, and cost information. Knockoffs and conformal selection need the law of the covariates or the stated independent or conditional exchangeability assumptions, and give an error rate instead of intervals. And the hybrid needs a simultaneous band, and costs a small slice of the level."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in tab[1:]], lag_ratio=0.6), run_time=18.0)
        self.wait(1.0)
        self.clear_scene()

    def referee(self):
        rows = [
            cmath(r"\text{ask}", r":", r"\text{was the question fixed before the data were seen?}", font_size=34),
            cmath(r"\text{if not}", r":", r"\text{what selected it, \ and was the selection reported?}", font_size=34),
            cmath(r"\text{then}", r":", r"\text{which guarantee, \ and is it delivered?}", font_size=34),
            cmath(r"\text{and}", r":", r"\text{a replication, \ holdout, \ or pre-registration?}", font_size=34),
        ]
        rows[3][-1].set_color(HYBC)
        whys = [why(r"the first question"), why(r"the forking paths"), why(r"conditional or average"), why(r"the cheapest fixes")]
        head = label('Referee', font_size=32, color=SELC).move_to([0, 3.3, 0])
        if head.width > 12.5: head.width = 12.5
        self.add(head)
        with self.voiceover(
            "<bookmark mark='a'/> The part also gives a referee's checklist. Was the question fixed before the data "
            "were seen? <bookmark mark='b'/> If not, what selected it, and was the selection reported, including the "
            "analyses that were tried and dropped? <bookmark mark='c'/> Which guarantee does the paper claim, "
            "conditional or on average, and does the method it used actually deliver that guarantee? <bookmark "
            "mark='d'/> And is there a replication, a held-out set, or a pre-registration? Those remain the cheapest "
            "and most convincing fixes of all."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def problems(self):
        rows = fit_rows(VGroup(
            label(r"Open problems", font_size=40, color=S.ACCENT),
            label(r"1. \ Non-Gaussian and dependent data: \ exact conditional inference beyond the normal model", font_size=25),
            label(r"2. \ Iterative selection: \ what is conditioned on when an analyst tries twenty models?", font_size=25),
            label(r"3. \ Optimal trade-offs: \ how much randomization or fission maximizes power?", font_size=25),
            label(r"4. \ Machine-learning selection: \ honest inference on what a forest or network selects", font_size=25),
            label(r"5. \ Replication: \ combining selected findings without the winner's curse", font_size=25),
            label(r"6. \ Causal effects chosen after looking: \ subgroups, \ outcomes, \ specifications", font_size=25),
        ), 12.6, 0.42, [0, 0, 0])
        rows[0].set_x(0)
        with self.voiceover(
            "<bookmark mark='a'/> Six open problems. <bookmark mark='b'/> First, exact conditional inference beyond the Gaussian linear model, including non-Gaussian dependent estimates and unknown high dimensional covariance. Gaussian dependence with known covariance is already covered by the lemma. <bookmark mark='c'/> Second, complex, iterative selection: what exactly was conditioned on when an analyst tried twenty models and looked at a plot? <bookmark mark='d'/> Third, optimal trade-offs: how much randomization or fission maximizes power for a given task? <bookmark mark='e'/> Fourth, honest inference on what a forest or a neural network selects. <bookmark mark='f'/> Fifth, combining selected findings across studies without the winner's curse. <bookmark mark='g'/> And sixth, selective inference for causal effects chosen after looking: the subgroup, the outcome, the specification."
        ) as vo:
            for k, m_ in enumerate("abcdefg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.wait(1.5)
        self.clear_scene()
