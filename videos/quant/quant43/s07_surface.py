from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, load)


class Surface(VoiceoverScene):
    def construct(self):
        s=load('surface')
        self.card()
        self.board(s)
        self.evaluation(s)
        self.design()
        self.desk_use()
        self.scope()
        self.question()

    def card(self):
        c=chapter_card(6,r"Compare the pricing summaries carefully",
                       r"Do the target, metric and evaluation design match?",part=PART)
        with self.voiceover(
            "Chapter six. The answer to the pause is more than a date. Before ranking models, match quote "
            "eligibility, targets, weights, error units and evaluation design. The earlier public summaries are "
            "authenticated, but the original aggregation mixes price-over-vega and direct implied-volatility "
            "errors, uses different quote subsets and groups different evaluation exercises. This chapter labels "
            "those differences rather than treating the table as one common-design contest."
        ):
            self.play(FadeIn(c[0],shift=UP*.2),FadeIn(c[1]))
        self.play(FadeOut(c))

    def board(self,s):
        by={r['model']:r for r in s['rows']}
        names=['Black--Scholes, one volatility','Heston','SSVI (one surface)',
               'Merton jumps','Kou jumps','variance gamma','NIG','rough Heston','rough Bergomi']
        tab=VGroup(VGroup(label(r"model",font_size=19,color=QC.IDEA),
                          label(r"reported metric / quote set",font_size=18,color=QC.IDEA),
                          label(r"error",font_size=19,color=QC.IDEA)))
        for i,name in enumerate(names):
            metric=r"IV RMSE / 193" if i<3 else r"price/vega RMS / 193" if i<7 else r"IV RMSE / 175"
            tab.add(VGroup(label(name,font_size=18),label(metric,font_size=17,color=HURDLE),
                           label(rf"{by[name]['rmse']:.2f}",font_size=19,color=MKT_C)))
        for j,row in enumerate(tab):
            for cell,x in zip(row,(-3.9,1.2,5.6)):
                cell.move_to([x,3.05-.53*j,0])
        note=wrapped_label(r"As reported for 10 December 2025. Nominal vol-point scales; metric and quote-set "
                           r"differences prevent a single ranking. Rows grouped by design, not error.",12.5,18,GREY_B).to_edge(DOWN,buff=.25)
        with self.voiceover(
            "The reported errors, grouped by design. <bookmark mark='a'/> The one-volatility Black model, Heston "
            "and SSVI use direct vega-weighted implied-volatility errors on one hundred ninety-three eligible targets. "
            "<bookmark mark='b'/> The four jump rows instead carry the calibrator's price-over-market-vega residual "
            "RMS, not the separate direct-IV error available in their parent output. "
            "<bookmark mark='c'/> The rough-model rows use a narrower set of one hundred seventy-five quotes, and "
            "their error routines retain finite model IVs. Numbers on a nominal vol-point scale are not "
            "interchangeable when residual definitions or eligible targets differ. A smaller number in this mixed "
            "table does not establish a universal winner or prove roughness is necessary."
        ) as vo:
            self.play(FadeIn(tab[0]),FadeIn(tab[1]),FadeIn(note))
            vo.wait_until('a');self.play(FadeIn(tab[2]),FadeIn(tab[3]))
            vo.wait_until('b');self.play(LaggedStart(*[FadeIn(r)for r in tab[4:8]],lag_ratio=.2),run_time=1.4)
            vo.wait_until('c');self.play(FadeIn(tab[8]),FadeIn(tab[9]))
        self.clear_scene()

    def evaluation(self,s):
        rows=s['oos']
        names=[r"flat vol per expiry: day 1 / day 2",
               r"rough replay: trace min / fresh paths",
               r"signature vol: fit paths / fresh paths"]
        tab=VGroup(VGroup(label(r"evaluation design",font_size=19,color=QC.IDEA),
                          label(r"first",font_size=19,color=QC.IDEA),label(r"second",font_size=19,color=QC.IDEA)))
        for name,x in zip(names,rows):
            tab.add(VGroup(label(name,font_size=18),label(rf"{x['in']:.2f}",font_size=20),
                           label(rf"{x['out']:.2f}",font_size=20,color=HURDLE)))
        for j,row in enumerate(tab):
            for cell,x in zip(row,(-2.8,2.5,5.2)):cell.move_to([x,1.8-.85*j,0])
        note=wrapped_label(r"Part 10 uses next-day quotes on common expiries. Part 14 uses fresh random numbers "
                           r"against the same dated quotes. These are different validation questions.",12.1,20,BAD).to_edge(DOWN,buff=.5)
        with self.voiceover(
            "What the second column actually tests. <bookmark mark='a'/> The flat-volatility-per-expiry model "
            f"reports {rows[0]['in']:.2f} on day one and {rows[0]['out']:.2f} on actual next-day marks with common "
            "expiries. <bookmark mark='b'/> Rough Bergomi replay instead averages minimum training-trace errors "
            f"and final-parameter fresh-path errors, {rows[1]['in']:.2f} and {rows[1]['out']:.2f}, against the same "
            "dated quotes. The first quantity is not necessarily the final parameter's training error. "
            "<bookmark mark='c'/> Signature volatility compares final parameters on fitted and fresh simulation "
            f"paths, {rows[2]['in']:.2f} and {rows[2]['out']:.2f}, also on the same quotes. Fresh random numbers "
            "test simulation-fit sensitivity; they do not test tomorrow's market or hedge performance."
        ) as vo:
            self.play(FadeIn(tab[0]),FadeIn(tab[1]),FadeIn(note))
            vo.wait_until('a');vo.wait_until('b');self.play(FadeIn(tab[2]))
            vo.wait_until('c');self.play(FadeIn(tab[3]))
        self.clear_scene()

    def design(self):
        cards=VGroup(
            desk_question(r"same target",r"match quote dates, expiry and moneyness filters, marks, weights and missing-value policy",width=12.4,font_size=19),
            desk_question(r"same task",r"distinguish calibration fit, fresh-path numerical robustness, next-day pricing and executable hedging",width=12.4,font_size=19),
            desk_question(r"same decision",r"use evaluation data and loss appropriate to the desk's proposed application",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "A comparison design. <bookmark mark='a'/> Hold the target quotes, units, weights and handling of "
            "invalid values fixed when the question requires a direct error comparison. "
            "<bookmark mark='b'/> Keep calibration, numerical robustness, next-day pricing and hedging as separate "
            "tasks. <bookmark mark='c'/> Evaluate the decision the desk actually needs. A good surface fit can be "
            "useful for quoting without establishing a dynamic law, and a dynamic law still needs empirical "
            "evaluation for its intended application."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def desk_use(self):
        cards=VGroup(
            desk_question(r"to quote",r"fit diagnostics plus no-arbitrage conditions over the relevant domain; a sampled check has limited coverage",width=12.4,font_size=19),
            desk_question(r"to hedge or price exotics",r"state the pricing measure, dynamics and market incompleteness; test the actual hedge or payoff",width=12.4,font_size=19),
            desk_question(r"to adopt",r"compare with a simpler justified baseline using matched application data and implementation costs",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "The desk use follows the task. <bookmark mark='a'/> Quoting requires useful fit and appropriate "
            "no-arbitrage conditions; passing a sampled grid check is not a proof over every strike and maturity. "
            "<bookmark mark='b'/> Hedging or exotic pricing needs assumptions about the pricing measure and "
            "dynamics, followed by evaluation on the actual application. <bookmark mark='c'/> A proposed adoption "
            "should beat a justified baseline on matched data with costs and uncertainty reported. The mixed "
            "summary table alone is not an adoption decision."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def scope(self):
        cards=VGroup(
            desk_question(r"provenance",r"all eight public derived inputs match exact hashes in committed earlier-part approvals",width=12.4,font_size=19),
            desk_question(r"scope",r"a retrospective pool of option marks, not one executable simultaneous market snapshot",width=12.4,font_size=19),
            desk_question(r"further evidence",r"additional dates, markets, numerical checks and application-level losses",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "Provenance and scope. <bookmark mark='a'/> All eight reused public derived inputs match their "
            "committed earlier approvals; no model was refitted for this chapter. "
            "<bookmark mark='b'/> The Surface is a retrospective pool of marks over a collection window, rather "
            "than a single simultaneously executable quote sheet. <bookmark mark='c'/> General conclusions need "
            "additional dates, markets, numerical checks and losses tied to the application. The summary is a "
            "lesson in comparing evidence, not a ranking for all pricing tasks."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def question(self):
        q=pause_card(r"fresh random numbers price the same dated quotes. Does that test tomorrow's market, "
                     r"simulation robustness, or realised hedge P\&L?")
        with self.voiceover(
            "Pause and predict. Fresh random numbers price the same dated quotes. Does that test tomorrow's "
            "market, simulation robustness, or realised hedge profit and loss? State the extra data each other "
            "question would require."
        ):self.play(FadeIn(q))
        self.wait(6.0);self.clear_scene()
