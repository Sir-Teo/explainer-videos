from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import BAD, HURDLE, MKT_C, PART, REC_C, SKILL_C, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.claims(load("arith"), load("record"), load("ensemble"), load("adaptive"))
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
            "circling, asked directly: with arithmetic, with statistics, with the economics of skill, and with the "
            "House's own record, opened in full."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def claims(self, a, r, e, ad):
        p15 = a["theory"][4]
        h = e["row"]["holdout"]
        d = ad["by_decade"]
        cards = VGroup(
            desk_question(r"luck is generous", rf"a manager with no skill and a 1\% cost is still ahead of the index "
                          rf"after fifteen years {100 * p15:.0f}\% of the time", width=12.4, font_size=19),
            desk_question(r"research shrinks", rf"across the House's 25 registered strategies, a research Sharpe ratio "
                          rf"one point higher bought {r['slope']:.2f} more in the sealed hold-out", width=12.4, font_size=19),
            desk_question(r"the dull wins", rf"the House's own equal-risk mix of ten published premia: hold-out Sharpe "
                          rf"{h['sharpe']:.2f}, {h['sharpe_net']:.2f} after costs", width=12.4, font_size=19),
            desk_question(r"markets learn", rf"the US market's daily autocorrelation: {d['1970']['ac1']:+.2f} in the 1970s, "
                          rf"{d['2010']['ac1']:+.2f} in the 2010s", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        hs, hn, sl = h["sharpe"], h["sharpe_net"], r["slope"]
        with self.voiceover(
            "What this part finds. <bookmark mark='a'/> Luck is generous: a manager with no skill and a one percent cost "
            f"is still ahead of the index after fifteen years {100 * p15:.0f} percent of the time. "
            "<bookmark mark='b'/> Research shrinks: across the House's twenty-five registered strategies, a research "
            f"Sharpe ratio one point higher bought only {sl:.2f} more in the sealed hold-out. <bookmark mark='c'/> The "
            f"dull wins: the House's own mix of published premia earned {hs:.2f} in the hold-out, {hn:.2f} after costs. "
            "<bookmark mark='d'/> And markets learn: the patterns of the nineteen seventies are gone."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
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
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question(r"for savers", r"most of the world's savings are managed by someone paid to beat the market; "
                          r"whether they can is worth trillions in fees", width=12.4, font_size=19),
            desk_question(r"for the field", r"every strategy in this series was an attempt; this part asks what the "
                          r"attempts, together, deliver", width=12.4, font_size=19),
            desk_question(r"for the House", r"it has kept a record since Part 1 precisely so that this question could "
                          r"be answered honestly at the end", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> Most savings are managed by someone paid to beat the market, and "
            "whether they can is worth a great deal in fees. <bookmark mark='b'/> Every strategy in this series was an "
            "attempt; this part asks what the attempts deliver together. <bookmark mark='c'/> And the House kept its "
            "record from the first part precisely so this question could be answered honestly at the end."
        ) as vo:
            for k, mk_ in enumerate(("a", "b", "c")):
                vo.wait_until(mk_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def history_cards(self):
        cards = VGroup(
            desk_question(r"Cowles (1933)", r"``Can stock market forecasters forecast?'': Alfred Cowles scored 45 "
                          r"forecasting services over four years and found no evidence of skill, as he reported",
                          width=12.4, font_size=19),
            desk_question(r"Jensen (1968)", r"Michael Jensen measured 115 mutual funds against the market's risk-adjusted "
                          r"return: on average they trailed it by about their costs, the first alpha", width=12.4,
                          font_size=19),
            desk_question(r"the index fund (1976)", r"John Bogle's first retail index fund turned the arithmetic into "
                          r"a product; Charles Ellis had called active investing ``the loser's game'' a year earlier",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The question is older than the field. <bookmark mark='a'/> In nineteen thirty-three Alfred Cowles scored "
            "forty-five forecasting services over four years, and found no evidence they could forecast. "
            "<bookmark mark='b'/> In nineteen sixty-eight Michael Jensen measured mutual funds against the market's "
            "risk-adjusted return, and found they trailed it by about their costs: the first alpha. "
            "<bookmark mark='c'/> And in nineteen seventy-six John Bogle's first retail index fund turned Sharpe's "
            "arithmetic, before Sharpe wrote it down, into a product."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_this(self):
        cards = VGroup(
            desk_question(r"not advice", r"the House's portfolio in Chapter 10 is a teaching example, not a recommendation "
                          r"to anyone", width=12.4, font_size=19),
            desk_question(r"not real funds' data", r"fund-level data are licensed; the populations here are simulated "
                          r"and calibrated to published estimates, which are cited as reported", width=12.4, font_size=19),
            desk_question(r"not the last word", r"five years of hold-out is short; the record is a first honest "
                          r"measurement, not a verdict for all time", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And what this part is not. <bookmark mark='a'/> It is not advice. <bookmark mark='b'/> It does not use real "
            "funds' data, which are licensed; the fund populations are simulated, calibrated to published estimates. "
            "<bookmark mark='c'/> And it is not the last word: five years of hold-out is a first honest measurement, "
            "not a verdict for all time."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits: the last part of Act seven, and of the series. Risk measured, crises followed, machines "
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
            r"The Track Record, all 25 rows, and the House's own strategy",
            r"The Surface's scoreboard; open problems; back to Bachelier",
            r"For the researcher: Storey's estimator, proved and checked",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: Sharpe's arithmetic; luck against skill; where skill's rewards go; markets that adapt; the "
            "Track Record opened in full; the pricing scoreboard; the open problems; a return to where the series "
            "began; and the theorem behind counting skill."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=tuple(DESKS.keys()))
        with self.voiceover(
            "In the House, every desk is built. For the last time, they report together, and the question is not what "
            "each one can do, but what all of them, together, have earned."
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
        self.wait(0.5)
        self.clear_scene()
