from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from videos.quant.quant43.common import BAD, HURDLE, MKT_C, PART, REC_C, SKILL_C, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.claims(load("arith"), load("luck"), load("fdr"), load("adaptive"))
        self.desk_q()
        self.stakes()
        self.history_cards()
        self.not_this()
        self.act()
        self.objectives()
        self.house()
        self.question()

    def title_card(self):
        card = part_title(PART, r"Can You Beat the Market?")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-three, the last. Can you beat the market? The question every part of this series has been "
            "circling, asked directly: with arithmetic, with statistics, with the economics of skill, and with "
            "an evidence protocol, and explicit limits on what the examples establish."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def claims(self, a, luck, fdr, ad):
        p15=a['theory'][4];d=ad['by_decade'];q=fdr['q']['0.1']
        cards=VGroup(
            desk_question(r"luck after costs",rf"in an additive Gaussian active-return model, zero skill still beats zero after 15 years {100*p15:.0f}\% of the time",width=12.4,font_size=19),
            desk_question(r"selection among funds",rf"the best statistic among 2,000 simulated zero-alpha funds is {luck['best_null']:.2f}; this is not a bootstrap of real funds",width=12.4,font_size=19),
            desk_question(r"an error fraction",rf"ordinary BH at 10\% selects {q['bh']} simulated funds, with realised false fraction {100*q['bh_fdr']:.0f}\%; expected FDR is a different quantity",width=12.4,font_size=19),
            desk_question(r"a changing sample statistic",rf"daily market autocorrelation: {d['1970']['ac1']:+.2f} in the 1970s and {d['2010']['ac1']:+.2f} in the 2010s; cause unidentified",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.22)
        with self.voiceover(
            "Four findings, with their scope. <bookmark mark='a'/> In the stylised additive Gaussian model, a zero-skill "
            f"manager facing a one percent annual cost is ahead after fifteen years {100*p15:.0f} percent of the time. "
            f"<bookmark mark='b'/> The best statistic among two thousand simulated zero-alpha funds is {luck['best_null']:.2f}. "
            f"<bookmark mark='c'/> In a different simulated population, ordinary BH selects {q['bh']} funds at its ten "
            f"percent level, with realised false fraction {100*q['bh_fdr']:.0f} percent. That is not expected FDR. "
            "<bookmark mark='d'/> Finally, daily market autocorrelation differs across historical windows. This "
            "describes a sample pattern; it does not identify learning as its cause or establish an executable return."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c','d')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def desk_q(self):
        rows = VGroup(label(r"your fund beat the market five years running", font_size=26),
                      label(r"two thousand other funds were trying", font_size=26, color=GREY_A),
                      label(r"skill, or luck?", font_size=26, color=HURDLE))
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        with self.voiceover(
            "The desk question, answered in Chapter two. <bookmark mark='a'/> Your fund beat the market five years "
            "running. <bookmark mark='b'/> Two thousand other funds were trying. <bookmark mark='c'/> Skill, or luck? "
            "And how would you ever tell?"
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards=VGroup(
            desk_question(r"the investor's question",r"which benchmark, costs and risks define an improvement?",width=12.4,font_size=19),
            desk_question(r"the researcher's question",r"how much apparent success can selection and noise create?",width=12.4,font_size=19),
            desk_question(r"the House's question",r"what evidence would justify changing a proposed decision rule?",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "Why the question matters. <bookmark mark='a'/> An investor needs a benchmark, risk definition and "
            "implementation costs before an improvement can be measured. <bookmark mark='b'/> A researcher must "
            "account for selection as well as noise. <bookmark mark='c'/> The House's governance example asks what "
            "evidence would justify changing a decision rule. That question remains meaningful without claiming "
            "any particular portfolio has passed its test."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def history_cards(self):
        cards = VGroup(
            desk_question(r"Cowles (1933)", r"``Can stock market forecasters forecast?'': Alfred Cowles studied "
                          r"forecasters and reported weak evidence of forecasting ability in his sample",
                          width=12.4, font_size=19),
            desk_question(r"Jensen (1968)", r"Michael Jensen measured 115 mutual funds against the market's risk-adjusted "
                          r"return in an influential study of fund alpha", width=12.4,
                          font_size=19),
            desk_question(r"the index fund (1976)", r"John Bogle's first retail index fund turned the arithmetic into "
                          r"a product; Charles Ellis had called active investing ``the loser's game'' a year earlier",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The question is older than the field. <bookmark mark='a'/> In nineteen thirty-three Alfred Cowles scored "
            "professional forecasts and reported weak evidence of ability in his sample. "
            "<bookmark mark='b'/> In nineteen sixty-eight Michael Jensen measured mutual funds against the market's "
            "risk-adjusted return, in an influential empirical study of fund alpha. "
            "<bookmark mark='c'/> And in nineteen seventy-six John Bogle's first retail index fund turned Sharpe's "
            "arithmetic, before Sharpe wrote it down, into a product."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_this(self):
        cards=VGroup(
            desk_question(r"fund examples",r"fixed-seed simulated populations; their truth labels are known by construction",width=12.4,font_size=19),
            desk_question(r"market examples",r"French daily returns through 2020 and authenticated earlier public pricing summaries",width=12.4,font_size=19),
            desk_question(r"evidence design",r"prospective protocol, analytical examples and proposed governance; no sealed strategy outcomes",width=12.4,font_size=19)
        ).arrange(DOWN,buff=.25)
        with self.voiceover(
            "The scope. <bookmark mark='a'/> The fund examples use fixed-seed simulated populations with known truth, "
            "rather than an empirical census of managers. <bookmark mark='b'/> The market examples use French daily "
            "returns through twenty twenty and authenticated earlier public pricing summaries. "
            "<bookmark mark='c'/> The record chapter is a prospective protocol and the House is a governance teaching "
            "example. Sealed strategy outcomes are excluded from this presentation; no strategy ensemble is run here."
        ) as vo:
            self.play(FadeIn(cards[0]))
            for k,mark in enumerate(('a','b','c')):
                vo.wait_until(mark)
                if k:self.play(FadeIn(cards[k],shift=UP*.2))
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits: the separate finale after the seven acts, and the last part of the series. Risk measured, crises followed, machines "
            "let loose; and now the question that all forty-two before it were preparing."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Sharpe's arithmetic, its proof and Pedersen's correction",
            r"Luck or skill: a fund population, Fama--French, Barras--Scaillet--Wermers",
            r"Skill, scale and money: Berk and Green, value added",
            r"Adaptive markets: ninety years of autocorrelation",
            r"A prospective record: selection, costs, uncertainty and monitoring",
            r"The Surface's scoreboard; open problems; back to Bachelier",
            r"For the researcher: raw and capped estimators; Bayesian allocation",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: Sharpe's arithmetic; luck against skill; where skill's rewards go; markets that adapt; the "
            "design of a performance record; pricing comparisons; the open problems; a return to where the series "
            "began; and the theorem behind counting skill."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=tuple(DESKS.keys()))
        with self.voiceover(
            "In the House, every desk is built. For the last time, they report together, and the question is not what "
            "each one can do, but what evidence and risk controls a combined decision would need."
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()

    def question(self):
        q = pause_card(r"before costs, what is the average return of all actively managed money, relative to the market?")
        with self.voiceover(
            "Pause and predict. Before costs, what is the average return of all actively managed money, relative to "
            "the market?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
