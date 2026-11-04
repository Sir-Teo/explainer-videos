from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import (FORMULA, GP_C, HURDLE, PART, RAND_C, RL_C, TRAIN_C, VALID_C, comma, era_strip,
                                         load, tt)


class Hook(VoiceoverScene):
    def construct(self):
        r = load("random")
        c = load("combine")
        self.title_card()
        self.flood(r)
        self.climb(r, c)
        self.history()
        self.objectives()
        self.house()

    def title_card(self):
        card = part_title(PART, r"Alpha Mining and Automated Research")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part twenty-nine. Alpha mining and automated research: machines that search through formulas for trading "
            "signals, write their own research, and test it; what they find; and how easily the search itself fools you."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def flood(self, r):
        from explainer.quant.house import alphas as A
        rng = np.random.default_rng(29)
        forms = [A.to_str(A.random_tree(rng, 4)) for _ in range(60)]
        cols = [RAND_C, FORMULA, GP_C, RL_C]
        labs = VGroup()
        for k, f in enumerate(forms):
            t = label(tt(f, 46), font_size=13, color=cols[k % 4])
            t.move_to([rng.uniform(-5.4, 5.4), rng.uniform(-3.2, 3.2), 0])
            t.set_opacity(0.35 + 0.5 * rng.random())
            labs.add(t)
        count = MathTex(rf"{comma(r['n'])}\ \text{{formulas}}", font_size=56, color=HURDLE)
        box = BackgroundRectangle(count, color=BLACK, fill_opacity=0.85, buff=0.25)
        with self.voiceover(
            "Here are sixty formulas, drawn at random from a small grammar of prices, volumes and a few operators. "
            "<bookmark mark='a'/> Each one is a trading signal: rank the coins by it every day, buy the top, sell the "
            "bottom. <bookmark mark='b'/> We drew ten thousand of them, and asked each one how well it would have "
            "predicted tomorrow's returns on the coins Binance traded in 2018 and 2019."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in labs], lag_ratio=0.03, run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(box), FadeIn(count))
        self.wait(0.4)
        self.clear_scene()

    def climb(self, r, c):
        b = r["best_by_n"]
        Ns = np.array([x["n"] for x in b], float)
        xs = np.log10(Ns)
        trs = [x["train"] for x in b]
        top = float(np.ceil(max(trs) * 100 + 1) / 100)
        g = axes([1, 4], [0, top], x_length=7.0, y_length=4.2, xlabel=r"formulas tried (log scale)",
                 ylabel=r"the best one's score on 2018--19 (IC)", xticks=[1, 2, 3, 4], yticks=[0, top / 2, top],
                 xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.2f}",
                 font_size=15).move_to(LEFT * 1.9 + DOWN * 0.2)
        ax = g.ax
        lt = curve(ax, xs, trs, TRAIN_C, stroke_width=3)
        best = b[-1]
        qs = VGroup(label(r"is it real?", font_size=24, color=VALID_C),
                    label(r"how many different ideas are in there?", font_size=24, color=HURDLE),
                    label(r"how many tries did it take?", font_size=24, color=QC.HOUSE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Keep the best so far. <bookmark mark='a'/> The more formulas we try, the better the winner looks: by ten "
            f"thousand, a score of {best['train']:.3f}, the kind of number a research note would celebrate. "
            "<bookmark mark='b'/> Three questions decide whether it means anything. Is it real, or the luck of the "
            "largest search? How many different ideas are hiding among the ten thousand? And how many tries did it "
            "take, because every try raises the bar. This part answers all three, and then opens a sealed envelope."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lt), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q_, shift=LEFT * 0.2) for q_ in qs], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1992, r"Koza: genetic programming", I), (1999, r"Allen--Karjalainen: GP trading rules", I),
                   (2007, r"WorldQuant founded", I), (2016, r"101 formulaic alphas", I),
                   (2023, r"AlphaGen; Alpha-GPT", I), (2024, r"China's quant quake", I),
                   (2025, r"AlphaAgent; R\&D-Agent-Quant", I)]
        strip = era_strip(entries, y0=1988, y1=2027, font_size=13).move_to(DOWN * 0.3)
        head = label(r"Machines learn to search for signals", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 2), (2, 4), (4, 7)]
        with self.voiceover(
            "The idea is older than the machines that now run it. John Koza's genetic programming in 1992; Franklin "
            "Allen and Risto Karjalainen breeding technical trading rules for the S&P 500 in 1999. <bookmark mark='a'/> "
            "Then the industrial version: WorldQuant's alpha factory, and in 2016 Zura Kakushadze's publication of a "
            "hundred and one such formulas. <bookmark mark='b'/> And since 2023, reinforcement learning and language models "
            "as miners and researchers, and in 2024 a crash in China that showed what crowded mining costs."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), m in zip(groups, [None, "a", "b"]):
                if m:
                    vo.wait_until(m)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Formulaic alphas, and the size of the space they live in",
            r"Three miners: random search, genetic programming, a reinforcement-learning generator",
            r"Language-model research agents, and what their reported numbers mean",
            r"Combining weak alphas; the trial counter; decay, crowding and the alpha factory",
            r"China's quant industry, February 2024, and High-Flyer's road to DeepSeek",
            r"What remains for humans; the mined combination, registered and opened",
            r"For the researcher: how many alphas an estimated combination can carry",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: formulaic alphas and the space they live in; three miners, built here and run on coins; the "
            "language-model agents; how weak alphas combine, and what the search does to the trial counter; decay and "
            "crowding; China's quant industry and its crash; the fund that became DeepSeek; what is left for people; "
            "one registered strategy, opened on sealed years; and a theorem on how many alphas an estimated "
            "combination can carry before more of them hurt."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            "In the House, the research desk gets an alpha factory: a grammar of formulas, three ways to search it, a "
            "way to combine what it finds, and a counter that records every try."
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
