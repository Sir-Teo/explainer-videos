from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, FORMULA, GOOD, HURDLE, PART


class Agents(VoiceoverScene):
    def construct(self):
        self.card()
        self.loop()
        self.alphagpt()
        self.alphaagent()
        self.rdagent()
        self.checks()
        self.question()

    def card(self):
        c = chapter_card(6, r"LLM research agents", r"Can a language model do the researcher's job, not just the "
                         r"search's?", part=PART)
        with self.voiceover("Chapter six. Genetic programming and reinforcement learning search blindly over symbols. A "
                            "language model can read papers, propose a hypothesis in words, write the code and read the "
                            "backtest. Can it do the researcher's job?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def loop(self):
        steps = [(r"hypothesis", r"in words: `volume spikes that fade predict reversals'", QC.SPOT),
                 (r"code", r"a formula or a function the backtester can run", QC.OPTION),
                 (r"backtest", r"IC, Sharpe ratio, turnover, correlation with what we have", QC.DELTA),
                 (r"critique", r"what worked, what to try next, written back as context", QC.CASH)]
        boxes = VGroup()
        for k, (a, b, c) in enumerate(steps):
            box = VGroup(RoundedRectangle(width=2.6, height=0.7, corner_radius=0.12, stroke_color=c, fill_color=c,
                                          fill_opacity=0.15), label(a, font_size=22, color=c))
            box[1].move_to(box[0])
            d = wrapped_label(b, 2.9, 15, GREY_A).next_to(box, DOWN, buff=0.12)
            boxes.add(VGroup(box, d))
        boxes.arrange(RIGHT, buff=0.55, aligned_edge=UP).move_to(UP * 0.4)
        arrows = VGroup(*[Arrow(boxes[k][0].get_right(), boxes[k + 1][0].get_left(), buff=0.08, stroke_width=2,
                                color=GREY_C) for k in range(3)])
        back = CurvedArrow(boxes[3][0].get_bottom() + DOWN * 1.0, boxes[0][0].get_bottom() + DOWN * 1.0, angle=-PI / 4,
                           color=GREY_C, stroke_width=2)
        with self.voiceover(
            "The agent's loop is the researcher's loop. <bookmark mark='a'/> A hypothesis, in words. Code that tests it. "
            "A backtest. <bookmark mark='b'/> And a critique that becomes the next round's context: what worked, what to "
            "try next. The search is no longer over symbols but over ideas, and the language model's reading of the "
            "literature is the prior."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[:3]], lag_ratio=0.3), *[GrowArrow(a) for a in arrows[:2]])
            vo.wait_until("b")
            self.play(FadeIn(boxes[3]), GrowArrow(arrows[2]), Create(back))
        self.wait(0.4)
        self.clear_scene()

    def alphagpt(self):
        card = firm_card(r"Alpha-GPT (Wang et al., 2023)", r"`Human-AI interactive alpha mining': language models as the "
                         r"mediator between a quant researcher and the search. Agents polish a trading idea, write seed "
                         r"formulas, and analyse the backtests; a search then refines the seeds",
                         numbers=((r"\text{top }10", r"of more than 41{,}000 teams in WorldQuant's International Quant "
                                                    r"Championship, as the authors report"),
                                  (r"2025", r"published at EMNLP, system demonstrations")),
                         source=r"arXiv 2308.00016", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "Three systems mark the path. <bookmark mark='a'/> Alpha-GPT, in 2023, put language models between a human "
            "researcher and the search. One agent polishes the trading idea, another writes seed formulas, a third "
            "reads the backtests; a conventional search refines the seeds. <bookmark mark='b'/> The authors report a "
            "top-ten finish among more than forty-one thousand teams in WorldQuant's international quant championship."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def alphaagent(self):
        card = firm_card(r"AlphaAgent (2025)", r"`LLM-driven alpha mining with regularized exploration to counteract "
                         r"alpha decay': the agent is penalised for proposing formulas too similar to known ones (a "
                         r"similarity of their syntax trees) and for formulas that do not match the hypothesis they claim "
                         r"to test",
                         numbers=((r"\text{AST}", r"originality enforced by comparing syntax trees with the existing library"),
                                  (r"\checkmark", r"reported to resist decay better than earlier miners, in China's CSI 500 "
                                                  r"and the S\&P 500")),
                         source=r"arXiv 2502.16789", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "AlphaAgent, in 2025, attacked the miners' main failure: they rediscover the same crowded signals. "
            "<bookmark mark='a'/> It penalises a proposed formula whose syntax tree is too close to one already in the "
            "library, and one that does not actually express the hypothesis it claims to test. <bookmark mark='b'/> "
            "The authors report signals that decay more slowly, on China's CSI 500 and on the S&P 500."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def rdagent(self):
        card = firm_card(r"R\&D-Agent-Quant (Li et al., Microsoft, 2025)", r"a research stage that forms hypotheses and "
                         r"turns them into tasks, and a development stage whose code agent implements and backtests them on "
                         r"real markets; a multi-armed bandit decides whether to work on factors or on the model next",
                         numbers=((r"2\times", r"the annualized return of classical factor libraries, as reported"),
                                  (r"-70\%", r"with seventy percent fewer factors")),
                         source=r"NeurIPS 2025, datasets and benchmarks track; arXiv 2505.15155", kind=r"Paper file",
                         width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "And Microsoft's R and D agent for quant, in 2025, automates the whole research desk. <bookmark mark='a'/> "
            "A research stage forms hypotheses; a development stage writes and runs the code; a bandit decides whether "
            "the next round should work on the factors or on the model. <bookmark mark='b'/> The authors report up to "
            "twice the annualized return of classical factor libraries, using seventy percent fewer factors."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(Indicate(card.submobjects[-1], color=QC.FIRM, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def checks(self):
        cards = VGroup(
            desk_question(r"the language model has read the test period", r"Part 28's look-ahead, now in the researcher: "
                          r"a hypothesis can be a memory of what worked", width=12.4, font_size=19),
            desk_question(r"every iteration is a trial", r"an agent that runs a thousand loops has tried a thousand "
                          r"strategies, whatever it calls them; the counter applies", width=12.4, font_size=19),
            desk_question(r"the reported numbers are the authors'", r"on their chosen markets and periods; none has been "
                          r"opened on a sealed envelope like this series'", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three cautions. <bookmark mark='a'/> The language model may have read the very period it is tested on: a "
            "hypothesis can be a memory. <bookmark mark='b'/> Every loop of an agent is a trial, whatever it is called. "
            "<bookmark mark='c'/> And every number on these cards is the authors' own, on markets and periods they chose. "
            "None has yet been opened on a sealed envelope."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an agent proposes 500 hypotheses and keeps the 5 with the best backtest. How many trials does "
                       r"the counter record?")
        with self.voiceover(
            "Pause and predict. An agent proposes five hundred hypotheses and keeps the five with the best backtests. How "
            "many trials does the counter record?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
