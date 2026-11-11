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
        self.protocol()
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
            self.play(LaggedStart(*[FadeIn(b) for b in boxes[:3]], lag_ratio=0.3), *[GrowArrow(a) for a in arrows[:2]])
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(boxes[3]), GrowArrow(arrows[2]), Create(back))
        self.wait(0.4)
        self.clear_scene()

    def alphagpt(self):
        card = firm_card(r"Alpha-GPT (Wang et al., 2023)", r"`Human-AI interactive alpha mining': language models as the "
                         r"mediator between a quant researcher and the search. Agents polish a trading idea, write seed "
                         r"formulas, and analyse the backtests; a search then refines the seeds",
                         numbers=((r"2023", r"version 1: human--AI interactive alpha mining"),
                                  (r"\text{scope}", r"an authored framework and experiments, not independent performance verification")),
                         source=r"arXiv 2308.00016v1, 31 July 2023", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "Three papers illustrate different approaches. <bookmark mark='a'/> Alpha-GPT's July2023 version1 puts human-language interaction between a researcher and conventional formula search: trading ideas can be translated into seeds and backtests can be interpreted. <bookmark mark='b'/> This version describes a framework and its chosen experiments. It does not establish independent live profitability. Competition rankings and later publication claims are not used as evidence for this version."
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
                         source=r"arXiv 2502.16789v1, February 2025", kind=r"Paper file", width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "AlphaAgent's February2025 version1 uses regularised exploration. <bookmark mark='a'/> It compares proposed syntax trees with an existing library for originality, and uses semantic checks to align factors with hypotheses. Syntactic novelty does not guarantee an economically independent exposure. <bookmark mark='b'/> The authors report resistance to decay in their CSI500 and S-and-P500 experiments. These are author-selected historical comparisons; they do not isolate crowding causally or establish independent live performance, valid model chronology, capacity or net returns under every implementation."
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
                         source=r"arXiv 2505.15155v1, 21 May 2025; Table 1 and experimental settings", kind=r"Paper file",
                         width=10.6, font_size=22).move_to(ORIGIN)
        with self.voiceover(
            "R-and-D-Agent-Quant's May2025 version1 combines research and development. <bookmark mark='a'/> Hypotheses become tasks, a code agent implements them, and a multi-armed bandit chooses directions for factor and model optimisation. <bookmark mark='b'/> The abstract reports up to twice the annualised return of classical factor libraries using seventy percent fewer factors. Its displayed experimental split is2008-2014 training,2015-2016 validation and January2017 through August2020 testing, on the CSI300 setting. These are the authors' comparisons, not an independent replication or proof that the language-model research process could have run with only information available then."
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
            desk_question(r"audit model and context chronology", r"Part 28's look-ahead, now in the researcher: "
                          r"a hypothesis can be a memory of what worked", width=12.4, font_size=19),
            desk_question(r"every iteration is a trial", r"an agent that runs a thousand loops has tried a thousand "
                          r"strategies, whatever it calls them; the counter applies", width=12.4, font_size=19),
            desk_question(r"the reported numbers are the authors'", 'versioned author comparisons; no independent live-performance or full chronology validation is established here', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three cautions. <bookmark mark='a'/> A language model or its research context may contain information from the historical test period. A declared cutoff alone does not prove what the model saw. <bookmark mark='b'/> Record all loops, prompt changes, failed runs and human choices as adaptive selection history; loop count is not an independent-trial count. <bookmark mark='c'/> The reported outcomes belong to specific paper versions and selected markets. A paper's held-out period does not establish live feasibility, public-data vintages, complete costs or an absence of leakage. No external agent experiment is run or sealed strategy scored here."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def protocol(self):
        rows = [cmath(r"1.", r"\ ", r"\text{audit model, retrieval and supplied information provenance}", font_size=28),
                cmath(r"2.", r"\ ", r"\text{log the full adaptive history, including human choices}", font_size=28),
                cmath(r"3.", r"\ ", r"\text{freeze the complete procedure, data rules and portfolio}", font_size=28),
                cmath(r"4.", r"\ ", r"\text{use valid inference, attainable execution and fair benchmarks}", font_size=28)]
        whys = [why(r"a stated training cutoff alone does not establish what the model and context contain"),
                why(r"record prompts, code, failed runs and selection; adaptive loops are not independent trials"),
                why(r"register the whole research and trading procedure, including preprocessing and costs"),
                why(r"an untouched evaluation is useful, but one opening alone guarantees neither validity nor power")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover("Evaluate the whole research procedure. <bookmark mark='a'/> Audit the model's information provenance, retrieved documents and supplied context; a declared training cutoff alone is insufficient. <bookmark mark='b'/> Preserve prompts, code versions, failed runs, backtests and human choices as a full adaptive history, not a count of independent trials. <bookmark mark='c'/> Freeze preprocessing, data vintages, tools, selection rules, portfolio construction and costs as well as the model. <bookmark mark='d'/> Use inference suited to dependence and selection, attainable execution assumptions and appropriate benchmarks. An untouched evaluation is valuable, but opening data once does not by itself guarantee validity, power or live feasibility. No external agent experiment is run here.") as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
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
