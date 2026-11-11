from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant43.common import ladder
from videos.quant.quant43.common import (ACT_C, BAD, COST_C, GOOD, HURDLE, LUCK_C, MKT_C, PART, REC_C, SKILL_C, comma,
                                         load)


class Journey(VoiceoverScene):
    def construct(self):
        self.card()
        self.act1()
        self.act2()
        self.act3()
        self.act4()
        self.act5()
        self.act6()
        self.act7()
        self.counts()
        self.question()

    def card(self):
        c = chapter_card(9, r"The House's journey", r"What did each act build, and what did it prove?", part=PART)
        with self.voiceover(
            "Chapter nine, and the answer to the pause, act by act. Each act developed models and research sections, with arguments under stated assumptions and "
            "checks by simulation or data. This is the list, briefly, as a map of "
            "what the House now knows."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _act(self,index):
        title,(first,last)=ACTS[index]
        heading=label(title,font_size=28,color=QC.IDEA).move_to(UP*2.75)
        numbers=list(range(first,last+1));split=(len(numbers)+1)//2
        columns=VGroup()
        for subset in (numbers[:split],numbers[split:]):
            if subset:
                column=VGroup(*[label(rf"{n}.\ {PARTS[n]}",font_size=22) for n in subset])
                column.arrange(DOWN,aligned_edge=LEFT,buff=.22);columns.add(column)
        columns.arrange(RIGHT,aligned_edge=UP,buff=.9)
        if columns.width>12.6:columns.width=12.6
        if columns.height>5.2:columns.height=5.2
        columns.move_to(DOWN*.15)
        return VGroup(heading,columns)

    def act1(self):
        g=self._act(0)
        with self.voiceover("Act one, markets and money. <bookmark mark='a'/> Parts one to three introduced the fair game, point-in-time information, market machinery and accounting. <bookmark mark='b'/> The selected arguments connect information, trading and valuation under their assumptions. The practical lesson is to specify the information and the economic object before interpreting a result.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def act2(self):
        g=self._act(1)
        with self.voiceover("Act two, the toolkit. <bookmark mark='a'/> Parts four to eight develop martingales and measure, stochastic calculus, econometrics, time series and decisions. <bookmark mark='b'/> Research arguments include fluctuation laws, forecast comparisons and estimation risk in portfolio choice. Each proof has a domain; a theorem under one model is not automatic validation of an empirical application.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def act3(self):
        g=self._act(2)
        with self.voiceover("Act three, derivatives under the pricing measure. <bookmark mark='a'/> Parts nine to twenty-two cover no-arbitrage, option models, surfaces, exotics, numerical and deep methods, then curves, credit, clearing, currencies and commodities. <bookmark mark='b'/> Arguments about hedges, noisy prices, approximation and risk transfer retain their assumptions. Comparing models requires matched targets, error definitions and evaluation designs.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def act4(self):
        g=self._act(3)
        with self.voiceover("Act four, return premia under the physical measure. <bookmark mark='a'/> Parts twenty-three to twenty-nine move from risk and return through factors, validation, backtesting, machine learning, text and automated research. <bookmark mark='b'/> Selection and uncertainty matter for claims of predictability. Factor labels, an attractive backtest and a pricing-measure theorem do not by themselves establish an independently evaluated net return.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def act5(self):
        g=self._act(4)
        with self.voiceover("Act five, portfolios and the firm. <bookmark mark='a'/> Parts thirty to thirty-four connect portfolio construction, risk models, costs and trading through time, systematic macro, statistical arbitrage and the quant firm. <bookmark mark='b'/> Estimation and trading-control arguments depend on objectives, constraints and cost models. Implementation and risk governance are part of the economic decision, not consequences of a single fitted alpha.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def act6(self):
        g=self._act(5)
        with self.voiceover("Act six, microstructure. <bookmark mark='a'/> Parts thirty-five to thirty-nine study counterparties, order books, impact, execution, market making, funds, speed competition, crypto and decentralised finance. <bookmark mark='b'/> Selected models explain information in order flow, execution schedules and liquidity-provider losses. Equilibrium and welfare claims remain conditional on the strategic and market-design assumptions.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def act7(self):
        g=self._act(6)
        with self.voiceover("Act seven, the system. <bookmark mark='a'/> Parts forty to forty-two examine risk measurement, leverage, liquidity, crises and machines in markets. This forty-third part is the separate finale in the canonical map. <bookmark mark='b'/> Risk tests, clearing and agent interaction reveal different system questions. Combining models can change outcomes, and a curriculum map is not an audit or approval of a combined trading system.") as vo:
            self.play(FadeIn(g))
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Indicate(g[0],color=QC.IDEA,scale_factor=1.02))
        self.clear_scene()

    def counts(self):
        rows=VGroup(
            label(r"43 parts: 7 acts + finale",font_size=28,color=QC.IDEA),
            label(r"models, proofs with assumptions, simulations and public-data examples",font_size=23),
            label(r"a proposed workflow: define, freeze, evaluate, report",font_size=24,color=REC_C),
            wrapped_label(r"This map is curriculum structure, not a count or score of strategy outcomes.",11.6,21,GREY_A)
        ).arrange(DOWN,buff=.45)
        with self.voiceover(
            "The structural count. <bookmark mark='a'/> Forty-three parts: seven acts followed by this separate finale. "
            "<bookmark mark='b'/> Models, proofs with assumptions, simulations and public-data examples. "
            "<bookmark mark='c'/> A proposed workflow: define the question, freeze choices, evaluate and report. "
            "This curriculum map is not an audit or score of strategy outcomes. It does not assert that a registry "
            "or a sealed file by itself guarantees an independent experiment."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until('a');vo.wait_until('b');self.play(FadeIn(rows[1]))
            vo.wait_until('c');self.play(FadeIn(rows[2]),FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        q = pause_card(r"forty-two rules later, what should the House's last rule be?")
        with self.voiceover(
            "Pause and predict. Forty-two rules later, what should the House's last rule be?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
