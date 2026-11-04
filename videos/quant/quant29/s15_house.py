from __future__ import annotations

from explainer.quant import *  # noqa: F403
from explainer.quant.house import alphas as A
from videos.quant.quant29.common import BAD, COMB, FORMULA, GOOD, GP_C, HURDLE, PART, RAND_C, RL_C, comma, house_lab, load


class House(VoiceoverScene):
    def construct(self):
        self.card()
        self.sheet(load("space"), load("random"), load("gp"), load("rl"), load("combine"), load("envelope"))
        self.lab()
        self.module()
        self.test()

    def card(self):
        c = chapter_card(14, r"Rule 29: the alpha factory", r"What must a machine-found signal survive before the House "
                         r"trades it?", part=PART)
        with self.voiceover("Chapter fourteen. The House's twenty-ninth rule: what a signal found by a machine must "
                            "survive."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, sp, r, g, rl, c, env):
        best = r["best_by_n"][-1]
        gp_last = [run[-1] for run in g["runs"]]
        gp_tr = sum(x["train"] for x in gp_last) / len(gp_last)
        gp_va = sum(x["valid"] for x in gp_last) / len(gp_last)
        h = env["row"]["holdout"]
        rows = [(r"formulas of depth 4 in the grammar", sci_(sp["count"][3]), FORMULA),
                (r"10{,}000 random formulas: correlation of 2018--19 and 2020 IC", rf"{r['corr']:.2f}", RAND_C),
                (r"the best of 10{,}000: IC on 2018--19, then on 2020", rf"{best['train']:.3f}\ \to\ {best['valid']:+.3f}",
                 HURDLE),
                (r"genetic programming, best of the last generation (3 runs)", rf"{gp_tr:.3f}\ \to\ {gp_va:+.3f}", GP_C),
                (r"the RL generator's pool", rf"{rl['train']['ic']:.3f}\ \to\ {rl['valid']['ic']:+.3f}", RL_C),
                (r"average correlation among the top 40 alphas", rf"{c['rho']:.2f}", COMB),
                (r"the combination on 2021--25: Sharpe ratio, gross and net", rf"{h['sharpe']:.2f} \pm {h['sharpe_se']:.2f},\ "
                 rf"{h['sharpe_net']:.2f}", GOOD if h["sharpe"] > 0 else BAD),
                (r"the trial counter", comma(env["trials"]), QC.HOUSE)]
        hx = [-2.4, 4.3]
        tab = VGroup()
        for j, (txt, v, col) in enumerate(rows):
            y = 2.4 - 0.6 * j
            tab.add(VGroup(label(txt, font_size=18, color=col).move_to([hx[0], y, 0]),
                           MathTex(v, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The alpha factory's first sheet", font_size=28).to_edge(UP, buff=0.3)
        foot = wrapped_label(r"every number computed in this part from public exchange data; none is a forecast, and none "
                             r"is advice", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The first sheet. <bookmark mark='a'/> A grammar of six fields and a few operators already holds more "
            "formulas of depth four than anyone could test. Ten thousand random ones largely remembered their training "
            "years in the next, because most of them restate a few real patterns. Evolution and the learned generator "
            "found the same patterns, and their most elaborate fits held up least. The top forty alphas were cousins. "
            "And the combination, opened on the sealed years, held up before costs and thinned after them, next to a "
            "counter that moved further in this part than in all the others together."
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
            "The heart of the miner is one small function in the House. A formula is a tree of tuples: a field at each "
            "leaf, an operator at each node. Evaluating it walks the tree, and every time-series operator looks only "
            "backward, at the days up to today. That single property, enforced in one place, is what keeps ten "
            "thousand formulas from reading the future."
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
        rule = wrapped_label(r"Rule 29: a machine-found signal enters the House only if every formula, generation and agent "
                             r"loop that produced it is counted as a trial; it clears the hurdle for that count on data the "
                             r"search never saw; it adds to the library's combination after the cost of estimating its "
                             r"weight; and its correlation with the signals already held is recorded, so that a crowded "
                             r"library is seen as one bet.", 12.4, 18, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Formulas as trees; the space they live in; scoring; search; "
            "combination; and the cost of estimating it. <bookmark mark='b'/> And the twenty-ninth rule. A signal found "
            "by a machine enters the House only if every formula, generation and agent loop that produced it is counted "
            "as a trial; it clears the hurdle for that count on data the search never saw; it improves the library's "
            "combination after the cost of estimating its weight; and its correlation with the signals already held is "
            "recorded, so that a crowded library is seen for what it is: one bet."
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
            "The rule against three cases. <bookmark mark='a'/> A genetic program reports a training IC of point zero "
            "eight: ask how many trees it evaluated, then for the IC on a year it never touched. <bookmark mark='b'/> An "
            "agent reports a Sharpe ratio of three: count its loops, check its language model's cut-off against the test "
            "period, and re-run it on a sealed envelope. <bookmark mark='c'/> The fiftieth alpha in the library: does the "
            "combination improve when it is added, after its weight is estimated? The research chapter gives the bar."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


def sci_(x: float) -> str:
    import math
    e = int(math.floor(math.log10(x)))
    return rf"{x / 10 ** e:.1f}\times 10^{{{e}}}"
