from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
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
            'Chapter eight. The dated twenty twenty-four IMF and Financial Stability Board reports identified correlation and provider concentration among potential risks, alongside cyber, operational and model risks. They discussed mechanisms and important information gaps. This chapter describes that historical assessment, not a claim about the current prevalence or absence of AI-driven instability.'
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
            desk_question(r"common to both", 'the 2024 reports discussed potential vulnerabilities and monitoring gaps; this is not a current prevalence estimate', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The reports in their historical framing. <bookmark mark='a'/> The IMF's October twenty twenty-four report discussed faster trading, correlated strategies and potential stress amplification, with implications for market safeguards. <bookmark mark='b'/> The FSB's November report highlighted provider dependence, market correlations, cyber risk, model risk and governance. <bookmark mark='c'/> It called for better monitoring and closing information gaps. Those reports are dated evidence about potential vulnerabilities, not a current estimate of realised systemic effects."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
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
                why('covered broker-dealers with market access must maintain specified financial and regulatory risk controls'),
                why('AI Act examples: natural-person creditworthiness and life/health insurance risk assessment; scope and phased application matter'),
                why(r"the SEC proposed in 2023 to regulate conflicts in brokers' predictive analytics, and withdrew the "
                    r"proposal in 2025, as reported")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Selected rules and historical dates, rather than a complete legal survey. <bookmark mark='a'/> EU requirements for covered investment firms engaged in algorithmic trading include testing, pre-trade controls and kill functionality. <bookmark mark='b'/> The US market-access rule applies to broker-dealers with relevant market access and requires financial and regulatory controls. <bookmark mark='c'/> The EU AI Act names natural-person creditworthiness and life or health insurance risk assessment among high-risk uses. Its scope and phased application require separate analysis; trading is not categorically exempt from AI, data or financial law. <bookmark mark='d'/> The SEC withdrew its twenty twenty-three predictive-analytics conflicts proposal in June twenty twenty-five. This is the history of that proposal, not a statement that no other duties apply."
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
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def episodes(self):
        events = [(r"6 May 2010", r"the flash crash: liquidity withdrew in minutes (Part 35)", BAD),
                  (r"1 Aug 2012", 'Knight Capital: deployment/routing failure; SEC later reported losses above \\$460m', BAD),
                  (r"15 Oct 2014", 'US Treasuries: 16 bp yield round trip in 12 minutes; no apparent new public catalyst in that window', BAD),
                  (r"7 Oct 2016", r"sterling fell about 6\% in two minutes in thin Asian trading, as reported", BAD),
                  (r"common", 'distinct operational and liquidity mechanisms; no single common cause established', HURDLE)]
        rows = VGroup(*[VGroup(label(d_, font_size=20, color=c_), label(w_, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.35)
                        for d_, w_, c_ in events]).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(ORIGIN)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        head = label(r"Machine-speed failures so far, from the public record", font_size=28).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Different historical failures illustrate different controls. <bookmark mark='a'/> The twenty ten flash crash involved stressed order flow and liquidity feedback. <bookmark mark='b'/> Knight Capital's twenty twelve deployment and routing failure generated unwanted positions; the SEC later reported losses above four hundred sixty million dollars. <bookmark mark='c'/> The twenty fourteen Treasury event included a sixteen-basis-point yield round trip in twelve minutes, without an apparent new public catalyst in that narrow window. <bookmark mark='d'/> Sterling fell sharply in thin Asian trading in twenty sixteen. <bookmark mark='e'/> These are not established examples of language-model trading failures, nor do they share one proven cause. Knight in particular was an operational failure, not simply simultaneous liquidity withdrawal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            for k, m_ in enumerate(("a", "b", "c", "d", "e")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def model_risk(self):
        cards = VGroup(
            desk_question(r"model risk management", 'US banking guidance issued in 2011 (SR 11-7): validation, limitations and monitoring proportional to model risk', width=12.4, font_size=19),
            desk_question(r"what learning breaks", r"a model that retrains itself is a new model every time; validation "
                          r"must cover the procedure that makes models, not one model", width=12.4, font_size=19),
            desk_question(r"accountability", 'firms and designated people retain responsibilities under the applicable rules; model output does not replace accountability', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Model-risk management offers an older framework. <bookmark mark='a'/> US banking guidance issued in twenty eleven emphasised independent validation, documented limitations and monitoring, scaled to model use and risk. <bookmark mark='b'/> Retraining changes the model, so validation should address the training procedure, data changes and deployment controls as well as individual versions. <bookmark mark='c'/> Firms and designated people retain responsibilities under the applicable regimes. A simulator's approval label does not substitute for those duties."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def controls(self):
        cards = VGroup(
            desk_question(r"inside the firm", r"limits and kill switches outside the model, that the model cannot "
                          r"learn its way around", width=12.4, font_size=19),
            desk_question(r"at the exchange", r"price bands, pauses and batch auctions that slow the crowd (Parts 38 "
                          r"and 41)", width=12.4, font_size=19),
            desk_question(r"in the system", 'diversity of models, data and providers; better data to measure common exposures', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So the controls come in three layers. <bookmark mark='a'/> Inside the firm: limits and kill switches "
            "outside the model, which it cannot learn its way around. <bookmark mark='b'/> At the exchange: price bands, "
            "pauses and batch auctions that slow a crowd down. <bookmark mark='c'/> And in the system: diversity of "
            "models, data and providers, and better data to measure concentration and common exposures."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
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
        self.wait(6.0)
        self.clear_scene()
