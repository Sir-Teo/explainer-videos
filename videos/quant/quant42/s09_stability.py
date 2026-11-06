from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C, load)


class Stability(VoiceoverScene):
    def construct(self):
        self.card()
        self.reports()
        self.rules()
        self.murphy()
        self.episodes()
        self.model_risk()
        self.controls()
        self.question()

    def card(self):
        c = chapter_card(8, r"AI and financial stability", r"What do the supervisors fear?", part=PART)
        with self.voiceover(
            "Chapter eight, and the answer to the pause: the last two chapters. Both reports put correlation and "
            "concentration near the top: many firms relying on the same few models and providers, trading in the "
            "same direction at machine speed, so that markets move faster and further under stress. Neither said it "
            "had happened yet at scale; both said the conditions were forming."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def reports(self):
        cards = VGroup(
            desk_question(r"IMF, Global Financial Stability Report, October 2024", r"AI could raise trading speed and "
                          r"volume and the correlation of strategies, and amplify moves under stress; it suggested "
                          r"circuit breakers and margin rules be reviewed, as the report describes", width=12.4,
                          font_size=19),
            desk_question(r"Financial Stability Board, November 2024", r"third-party dependence and concentration among "
                          r"model and cloud providers, market correlations, cyber risk and model risk, as listed in its "
                          r"report", width=12.4, font_size=19),
            desk_question(r"common to both", r"no evidence yet of AI-driven instability at scale, and limited data to "
                          r"look for it with", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the reports said, in their own framing. <bookmark mark='a'/> The IMF's October twenty twenty-four "
            "stability report: AI could raise trading speed, volume and the correlation of strategies, and amplify moves "
            "under stress; it suggested reviewing circuit breakers and margin rules. <bookmark mark='b'/> The Financial "
            "Stability Board, a month later: dependence on a concentrated set of model and cloud providers, market "
            "correlations, cyber risk and model risk. <bookmark mark='c'/> Common to both: no evidence yet of "
            "instability driven by AI at scale, and little data with which to look."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        rows = [cmath(r"\text{Europe, 2018}", r":", r"\text{MiFID II: test every algorithm; kill switches; limits}", font_size=34,
                      colors={r"\text{Europe, 2018}": COMP_C}),
                cmath(r"\text{US, 2010}", r":", r"\text{the market access rule: pre-trade risk checks}", font_size=36,
                      colors={r"\text{US, 2010}": COMP_C}),
                cmath(r"\text{Europe, 2024}", r":", r"\text{the AI Act: rules by use, high risk named}", font_size=36,
                      colors={r"\text{Europe, 2024}": HURDLE}),
                cmath(r"\text{US, 2023--25}", r":", r"\text{a proposed rule on predictive analytics, withdrawn}", font_size=34,
                      colors={r"\text{US, 2023--25}": GREY_B})]
        whys = [why(r"algorithmic trading firms must test algorithms before use, be able to stop them at once, and cap "
                    r"what they can send"),
                why(r"brokers must block orders that breach credit or size limits before they reach the market"),
                why(r"the EU's AI Act regulates by use; in finance it names credit scoring of people and some insurance "
                    r"pricing as high risk, while trading stays under MiFID"),
                why(r"the SEC proposed in 2023 to regulate conflicts in brokers' predictive analytics, and withdrew the "
                    r"proposal in 2025, as reported")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The rules that exist, as of this part. <bookmark mark='a'/> In Europe since twenty eighteen, algorithmic "
            "traders must test every algorithm before use, be able to stop it at once, and cap what it can send. "
            "<bookmark mark='b'/> In America since twenty ten, brokers must block orders that breach risk limits before "
            "they reach the market. <bookmark mark='c'/> Europe's AI Act regulates by use, and in finance names credit "
            "scoring and some insurance pricing as high risk, leaving trading to the older rules. "
            "<bookmark mark='d'/> And an American proposal on brokers' predictive analytics, made in twenty twenty-three, "
            "was withdrawn in twenty twenty-five, as reported."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def murphy(self):
        cards = VGroup(
            desk_question(r"Moore's law", r"computing power and speed keep growing, so ever more trading is "
                          r"automated, faster", width=12.4, font_size=19),
            desk_question(r"Murphy's law", r"whatever can go wrong will, and at machine speed it goes wrong before "
                          r"anyone can intervene", width=12.4, font_size=19),
            desk_question(r"Kirilenko and Lo (2013)", r"the gap between them is the risk: technology outruns the "
                          r"controls built for slower markets", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Kirilenko and Lo: the problem in two laws", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Andrei Kirilenko and Andrew Lo put the problem in two laws. <bookmark mark='a'/> Moore's law: computing "
            "keeps getting faster and cheaper, so more trading is automated. <bookmark mark='b'/> Murphy's law: "
            "whatever can go wrong will, and at machine speed it goes wrong before anyone can step in. "
            "<bookmark mark='c'/> The risk is the gap between them: technology that outruns the controls built for "
            "slower markets."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def episodes(self):
        events = [(r"6 May 2010", r"the flash crash: liquidity withdrew in minutes (Part 35)", BAD),
                  (r"1 Aug 2012", r"Knight Capital: old code reactivated, about \$440m lost in 45 minutes, as reported (Part 34)", BAD),
                  (r"15 Oct 2014", r"US Treasuries: the 10-year yield fell 16 bp and recovered within 12 minutes, with no news, as the official report found", BAD),
                  (r"7 Oct 2016", r"sterling fell about 6\% in two minutes in thin Asian trading, as reported", BAD),
                  (r"common", r"automated liquidity that withdraws together, and controls that act too late", HURDLE)]
        rows = VGroup(*[VGroup(label(d_, font_size=20, color=c_), label(w_, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.35)
                        for d_, w_, c_ in events]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        head = label(r"Machine-speed failures so far, from the public record", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "What machine-speed failures have looked like so far, from the public record. <bookmark mark='a'/> The "
            "flash crash of twenty ten, Part thirty-five. <bookmark mark='b'/> Knight Capital in twenty twelve, which "
            "lost about four hundred and forty million dollars in forty-five minutes when old code was switched back "
            "on, as reported. <bookmark mark='c'/> The Treasury market in October twenty fourteen, where the ten-year yield "
            "fell sixteen basis points and recovered within twelve minutes, with no news. <bookmark mark='d'/> Sterling's two-minute "
            "fall of about six percent in twenty sixteen. <bookmark mark='e'/> None was caused by learning machines. "
            "All were automated liquidity withdrawing together, faster than controls could act."
        ) as vo:
            self.play(FadeIn(head))
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def model_risk(self):
        cards = VGroup(
            desk_question(r"model risk management", r"US banking guidance since 2011 (SR 11-7): every model "
                          r"independently validated, its limits documented, its use monitored", width=12.4, font_size=19),
            desk_question(r"what learning breaks", r"a model that retrains itself is a new model every time; validation "
                          r"must cover the procedure that makes models, not one model", width=12.4, font_size=19),
            desk_question(r"accountability", r"a person, not an algorithm, answers for each agent's trades, which is "
                          r"what every regime above has in common", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And inside the firm, an older discipline. <bookmark mark='a'/> American banking supervisors' model-risk "
            "guidance of twenty eleven requires every model to be independently validated, its limits written down, "
            "its use monitored. <bookmark mark='b'/> Learning breaks the unit of account: a model that retrains itself "
            "is a new model each time, so validation must cover the procedure that makes models. "
            "<bookmark mark='c'/> And a person, not an algorithm, answers for each agent's trades. That is what every "
            "regime above has in common."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def controls(self):
        cards = VGroup(
            desk_question(r"inside the firm", r"limits and kill switches outside the model, that the model cannot "
                          r"learn its way around", width=12.4, font_size=19),
            desk_question(r"at the exchange", r"price bands, pauses and batch auctions that slow the crowd (Parts 38 "
                          r"and 41)", width=12.4, font_size=19),
            desk_question(r"in the system", r"diversity of models, data and providers, and the means to measure it", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So the controls come in three layers. <bookmark mark='a'/> Inside the firm: limits and kill switches "
            "outside the model, which it cannot learn its way around. <bookmark mark='b'/> At the exchange: price bands, "
            "pauses and batch auctions that slow a crowd down. <bookmark mark='c'/> And in the system: diversity of "
            "models, data and providers, and the means to measure it, which no one yet has."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"before the House lets a learned agent trade, what should it be tested against, besides the "
                       r"market it was trained on?")
        with self.voiceover(
            "Pause and predict. Before the House lets a learned agent trade, what should it be tested against, besides "
            "the market it was trained on?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
