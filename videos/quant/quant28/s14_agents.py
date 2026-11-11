from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant28.common import BAD, GOOD, HURDLE, PART, WORD

ROLES = [("fundamentals analyst", QC.CASH), ("sentiment analyst", QC.VEGA), ("news analyst", QC.SPOT),
         ("technical analyst", QC.OPTION)]


class Agents(VoiceoverScene):
    def construct(self):
        self.card()
        self.loop()
        self.firm()
        self.checks()
        self.question()

    def card(self):
        c = chapter_card(13, r"LLM trading agents", r"What happens when the model does not just read, but decides?",
                         part=PART)
        with self.voiceover("Chapter thirteen. So far the language model has been a reader that produces a score. The "
                            "newest systems go further: teams of models that argue, decide and trade. What do we know "
                            "about them?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def loop(self):
        steps = [
            (r"observe", r"prices, news, filings and past decisions", QC.SPOT),
            (r"reason", r"a language model writes an analysis", QC.OPTION),
            (r"act", r"a tool call: trade, hold or fetch data", QC.DELTA),
            (r"remember", r"the result enters later context", QC.CASH),
        ]
        nodes, descriptions = VGroup(), VGroup()
        for k,(title,body,color) in enumerate(steps):
            box = RoundedRectangle(width=2.6, height=0.75, corner_radius=0.12, stroke_color=color, fill_color=color, fill_opacity=0.15)
            name = label(title, font_size=25, color=color).move_to(box)
            node = VGroup(box,name).move_to([-4.8 + 3.2*k,0.7,0])
            nodes.add(node)
            descriptions.add(wrapped_label(body,2.65,20,GREY_A).next_to(node,DOWN,buff=0.24))
        arrows = VGroup(*[Arrow(nodes[k].get_right(),nodes[k+1].get_left(),buff=0.10,color=GREY_B,stroke_width=2)for k in range(3)])
        points = [nodes[-1].get_right(),np.array([6.6,0.7,0]),np.array([6.6,-1.5,0]),np.array([-6.6,-1.5,0]),np.array([-6.6,0.7,0])]
        back = VGroup(*[Line(a,b,color=GREY_C,stroke_width=1.6)for a,b in zip(points,points[1:])],Arrow(points[-1],nodes[0].get_left(),buff=0.05,color=GREY_C,stroke_width=1.6))
        head = label(r"An agent: a loop around a language model",font_size=30).to_edge(UP,buff=0.5)
        explanation = wrapped_label(r"ReAct (Yao et al.2023): interleave reasoning and tools. In this schematic the model weights stay fixed; context and memory change.",12.0,23,GREY_A).to_edge(DOWN,buff=0.5)
        with self.voiceover("An agent is a loop around a language model. <bookmark mark='a'/> It observes: prices, news, its own past trades. It reasons, in words. It acts, by calling a tool: trade, or fetch more data. And it remembers, by writing the outcome back into what it will be shown next time. <bookmark mark='b'/> This is the ReAct pattern, reasoning interleaved with action. Nothing in the model is retrained. Only what it is shown changes, which is why a prompt, a memory and a set of tools are all part of the strategy.") as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(a,b))for a,b in zip(nodes,descriptions)],lag_ratio=0.2),FadeIn(arrows),FadeIn(back),run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(explanation))
        self.clear_scene()



    def firm(self):
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.7, height=0.75, corner_radius=0.12, stroke_color=c, fill_color=c,
                                                 fill_opacity=0.15), label(n, font_size=18, color=c)) for n, c in ROLES])
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.35).shift(UP * 2.2)
        bull = VGroup(RoundedRectangle(width=2.6, height=0.75, corner_radius=0.12, stroke_color=GOOD, fill_color=GOOD,
                                       fill_opacity=0.15), label(r"bull researcher", font_size=18, color=GOOD))
        bear = VGroup(RoundedRectangle(width=2.6, height=0.75, corner_radius=0.12, stroke_color=BAD, fill_color=BAD,
                                       fill_opacity=0.15), label(r"bear researcher", font_size=18, color=BAD))
        for b in (bull, bear):
            b[1].move_to(b[0])
        debate = VGroup(bull, bear).arrange(RIGHT, buff=2.0).shift(UP * 0.5)
        dv = DoubleArrow(bull.get_right(), bear.get_left(), color=GREY_B, buff=0.1)
        dl = label(r"debate", font_size=16, color=GREY_B).next_to(dv, UP, buff=0.05)
        trader = VGroup(RoundedRectangle(width=2.6, height=0.75, corner_radius=0.12, stroke_color=HURDLE, fill_color=HURDLE,
                                         fill_opacity=0.15), label(r"trader", font_size=18, color=HURDLE))
        risk = VGroup(RoundedRectangle(width=3.0, height=0.75, corner_radius=0.12, stroke_color=WORD, fill_color=WORD,
                                       fill_opacity=0.15), label(r"risk-management team", font_size=18, color=WORD))
        for b in (trader, risk):
            b[1].move_to(b[0])
        trader.shift(DOWN * 1.1)
        risk.shift(DOWN * 2.5)
        arrows = VGroup(*[Arrow(b.get_bottom(), debate.get_top(), buff=0.1, stroke_width=2, color=GREY_C) for b in boxes],
                        Arrow(debate.get_bottom(), trader.get_top(), buff=0.1, stroke_width=2, color=GREY_C),
                        Arrow(trader.get_bottom(), risk.get_top(), buff=0.1, stroke_width=2, color=GREY_C))
        src = note(r"TradingAgents (Xiao, Sun, Luo and Wang 2024, arXiv 2412.20138): every box is an LLM with its own "
                   r"prompt and tools", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.25)
        head = label(r"TradingAgents: an investment firm played by prompts", font_size=26).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the design of one of the most discussed, TradingAgents, by Yijia Xiao, Edward Sun, Di Luo and Wei "
            "Wang. <bookmark mark='a'/> Four analyst agents read fundamentals, social-media sentiment, news and price "
            "charts. <bookmark mark='b'/> A bullish and a bearish researcher debate what the analysts found. "
            "<bookmark mark='c'/> A trader agent decides, and a risk-management team checks the exposure. Every box "
            "is a language model with its own instructions and tools: an investment firm's org chart, played by "
            "prompts. The authors report better cumulative returns, Sharpe ratios and drawdowns than standard rules "
            "on the stocks they tested."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(debate), GrowArrow(dv), FadeIn(dl), *[GrowArrow(a) for a in arrows[:4]])
            vo.wait_until("c")
            self.play(FadeIn(trader), GrowArrow(arrows[4]), FadeIn(risk), GrowArrow(arrows[5]))
        self.wait(0.4)
        self.clear_scene()

    def checks(self):
        cards = VGroup(
            desk_question(r"when did the model stop reading?", r"an agent tested on months that its language model "
                          r"may have read about has Chapter 11's problem many times over: every analyst, every debate",
                          width=12.4, font_size=19),
            desk_question(r"how many stocks, how many months?", r"a few stocks over a few months is a handful of "
                          r"possibly correlated bets; Sharpe precision needs observation frequency, years, dependence and selection",
                          width=12.4, font_size=19),
            desk_question(r"how many prompts were tried?", r"every prompt, role and tool is a trial; the counter "
                          r"applies to agents as it does to the 10{,}000 rules of Part 26", width=12.4, font_size=19),
            desk_question(r"what does it cost to run?", r"a dozen model calls per stock per day, and a vendor's model "
                          r"that may change between the backtest and the trade", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        head = label(r"Part 26's questions, put to an agent", font_size=28).to_edge(UP, buff=0.3)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            "Before believing any such result, ask Part twenty-six's questions. <bookmark mark='a'/> When did the "
            "underlying model stop reading? Every agent in the chart can leak the future. <bookmark mark='b'/> How "
            "many stocks and months? A few stocks for a few months is a handful of possibly dependent bets. A numerical Sharpe standard error also needs sampling frequency, tail and dependence assumptions; stock count alone cannot supply it. <bookmark mark='c'/> How many prompts, roles and tools were tried before "
            "this one? Each is a trial for the counter. <bookmark mark='d'/> And what does it cost to run a dozen "
            "model calls per stock per day? The architecture is interesting; the evidence, so far, is thin."
        ) as vo:
            self.play(FadeIn(head, shift=DOWN * 0.2))
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an agent's backtest shows a Sharpe ratio of 5 on three stocks over three months. What is its "
                       r"standard error: what additional assumptions are needed?")
        with self.voiceover(
            "Pause and predict. An agent's backtest shows a Sharpe ratio of five, on three stocks over three months. "
            "What observation frequency, dependence assumptions and selection history would you need before calculating its standard error?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
