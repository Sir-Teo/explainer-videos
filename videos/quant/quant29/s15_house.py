from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import alphas as A, pit
from videos.quant.quant29.common import BAD, COMB, FORMULA, GOOD, GP_C, HURDLE, PART, RAND_C, RL_C, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("space"), load("random"), load("gp"), load("rl"), load("combine"))
        self.lab()
        self.gp_lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(14, r"Rule 29: the alpha factory", r"What must a machine-found signal survive before the House "
                         r"trades it?", part=PART)
        with self.voiceover("Chapter fourteen. The House's twenty-ninth rule: what a signal found by a machine must "
                            "survive."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, sp, r, g, rl, c):
        best = r["best_by_n"][-1]
        gp_last = [run[-1] for run in g["runs"]]
        gp_tr = sum(x["train"] for x in gp_last) / len(gp_last)
        gp_va = sum(x["valid"] for x in gp_last) / len(gp_last)
        rows = [(r"formulas of depth 4 in the grammar", sci_(sp["count"][3]), FORMULA),
                (r"10{,}000 random formulas: correlation of 2018--19 and 2020 IC", rf"{r['corr']:.2f}", RAND_C),
                (r"the best of 10{,}000: IC on 2018--19, then on 2020", rf"{best['train']:.3f}\ \to\ {best['valid']:+.3f}",
                 HURDLE),
                (r"genetic programming, best of the last generation (3 runs)", rf"{gp_tr:.3f}\ \to\ {gp_va:+.3f}", GP_C),
                (r"the RL generator's pool", rf"{rl['train']['ic']:.3f}\ \to\ {rl['valid']['ic']:+.3f}", RL_C),
                (r"average correlation among the top 40 alphas", rf"{c['rho']:.2f}", COMB),
                (r"sealed strategy result", r"\text{excluded; not read or scored}", BAD),
                (r"existing registrations through Part 29", comma(pit.trials_upto(PART)), QC.HOUSE)]
        hx = [-2.4, 4.3]
        tab = VGroup()
        for j, (txt, v, col) in enumerate(rows):
            y = 2.4 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=18, color=col).move_to([hx[0], y, 0]),
                           MathTex(v, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The alpha factory's first sheet", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label('ordinary original calculations and existing registry metadata; illustrative scores, not executable forecasts', 12.0, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first sheet records ordinary research calculations. <bookmark mark='a'/> Grammar size, random-search scores, three GP runs, the RL pool and selected-formula correlations describe their supplied data and conventions. Validation is repeatedly inspected, counts are not independent trials and covariance directions are not independent bets. The strategy experiment is excluded: no payoff or score is read, and no sealed experiment is opened. The counter through Part twenty-nine is existing registration metadata,23,480; restoration makes no new registration or market trial. Separate those facts before drawing an investment conclusion."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"A formula, evaluated", A.evaluate, "if op == \"field\"", 12, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            'The evaluator recursively walks the original expression tree. Time-series operators use current and earlier array rows. That local property is useful, but insufficient for point-in-time validity. The archive, universe construction, current-close eligibility, missing future outcomes, token definitions, selection procedure and attainable execution all need separate checks. A backward-looking operator does not certify a future-free end-to-end research process.'
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def gp_lab(self):
        card = house_lab(r"One generation of a genetic program", A.gp, "nxt = [P[best]]", 15, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Here is the original generation update. The penalised-fitness champion is copied first. Tournament selection chooses parents; crossover, mutation or copying form children, with the depth rule rejecting overgrown trees. A string is scored when fitting first encounters it in that seed's cache. Validation is computed then but not used in the selection criterion. The offspring bred after the last scored generation are discarded without evaluation. Unique strings across seeds, repeated episodes and adaptive decisions belong in the search history; they are not independent tests."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("research",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{evaluate}, \texttt{to\_str}, \texttt{size}, \texttt{depth}", r"formulas as trees"),
            (r"\texttt{random\_tree}, \texttt{count\_trees}", r"the space"),
            (r"\texttt{ic\_series}, \texttt{ls\_returns}, \texttt{score}", r"scoring"),
            (r"\texttt{random\_search}, \texttt{gp}", r"search"),
            (r"\texttt{combine}, \texttt{sharpe}", r"combination"),
            (r"\texttt{sr\_oos\_theory}, \texttt{sr\_oos\_sim}", r"estimation risk"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 8.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label('Rule 29: record the full adaptive search; audit information and execution timing; validate the complete selection and weighting rule with appropriate dependence and multiplicity assumptions; include costs, funding and capacity; record common exposures. A raw count supplies no universal hurdle.', 12.4, 18, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Formula trees, search, scoring, combination and estimation-risk calculations remain the unchanged originals. <bookmark mark='b'/> Rule twenty-nine is to record the full adaptive search, audit data and execution timing, and validate the complete selection and weighting process. Inference must address dependence and multiplicity rather than treating the raw count as independent tests. Include costs, funding, borrow and capacity, and measure common exposures. A low pairwise correlation or one fresh interval alone cannot certify a machine-found signal."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the GP run with a training IC of 0.08", r"ask for the number of trees it evaluated, then "
                          r"for the IC on a year the run never touched", width=12.0, font_size=19),
            desk_question(r"the agent that reports a Sharpe ratio of 3", r"count its loops as trials, check the language "
                          r"model's cut-off against the test period, and re-run on a sealed envelope", width=12.0,
                          font_size=19),
            desk_question(r"the fiftieth alpha in the library", r"does the combination's out-of-sample Sharpe ratio rise "
                          r"when it is added, after its weight is estimated? The research chapter's bar", width=12.0,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Apply the rule to three cases. <bookmark mark='a'/> For GP training IC0.08, ask about data timing, penalised fitness, seeds, cached evaluations, discarded searches and a selection-aware validation protocol. <bookmark mark='b'/> For an agent's Sharpe3, audit model and retrieval provenance, prompt and human choices, dates, costs and dependence; a declared cutoff is insufficient. <bookmark mark='c'/> For a new library member, estimate its incremental effect after selection, weight estimation and costs. The research model's true-strength threshold is conditional, not an automatic admission test using its fitted Sharpe."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


def sci_(x: float) -> str:
    import math
    e = int(math.floor(math.log10(x)))
    return rf"{x / 10 ** e:.1f}\times 10^{{{e}}}"
