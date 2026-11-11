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
        self.act()
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
        # a jittered 4 x 15 grid: a flood, but every formula legible
        for k, f in enumerate(forms):
            t = label(tt(f, 38), font_size=13, color=cols[k % 4])
            if t.width > 3.1:
                t.scale_to_fit_width(3.1)
            col, row = k % 4, k // 4
            t.move_to([-5.1 + 3.4 * col + rng.uniform(-0.15, 0.15), 3.25 - 0.465 * row, 0])
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
            "take, because the full adaptive search history affects interpretation. This part studies all three, then specifies an evaluation protocol. The sealed strategy result is excluded; no payoff is read or scored."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(lt), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(q_, shift=LEFT * 0.2) for q_ in qs], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. This is the last part of the series' fourth act, on return premia. Parts twenty-three to "
            "twenty-five asked which risks are paid and how many factors are real; Part twenty-six built the tools to "
            "test a backtest without fooling yourself; twenty-seven turned machine learning on returns, and twenty-eight "
            "turned it on words. This part hands the whole research loop to machines, and asks what is left of those "
            "tests when the search itself is automatic."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        entries = [(1992, r"Koza: genetic programming", I), (1999, r"Allen--Karjalainen: GP trading rules", I),
                   (2007, r"WorldQuant founded", I), (2016, r"101 formulaic alphas", I),
                   (2023, r"AlphaGen; Alpha-GPT", I), (2024, r"A reported crowding episode", I),
                   (2025, r"AlphaAgent; R\&D-Agent-Quant", I)]
        strip = era_strip(entries, y0=1988, y1=2027, font_size=13).move_to(DOWN * 0.3)
        head = label(r"Machines learn to search for signals", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 2), (2, 4), (4, 7)]
        with self.voiceover(
            "The idea predates today's language models. John Koza described genetic programming in 1992, and Franklin Allen and Risto Karjalainen studied evolved technical trading rules for the S and P 500 in 1999. <bookmark mark='a'/> WorldQuant's industrial research example and Kakushadze's 2016 formula publication provide further chronology. <bookmark mark='b'/> Since 2023, the cited papers describe reinforcement learning and language models as miners and researchers. AlphaAgent's version 1 cites early 2024 small-cap factor underperformance as motivation. These dates and author reports provide context; attributing a loss to crowding requires positions, flows, funding and a defined comparison."
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
            r"evaluation protocol and fixed arithmetic; sealed strategy result excluded",
            r"For the researcher: how many alphas an estimated combination can carry",
        ], color=QC.IDEA)
        with self.voiceover(
            'The plan: a formula grammar, random search, genetic programming and a small reinforcement-learning miner, using their stored ordinary calculations. Then versioned research-agent reports; selected combinations and estimation risk; computational bookkeeping and its limits; decay, possible crowding channels and scoped industry accounts. We separate reports from causal conclusions and keep information, selection and execution assumptions visible. Finally, evaluate what human judgement contributes and specify a protocol with a fixed arithmetic example. Sealed strategy results remain unread and unscored.'
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research",))
        with self.voiceover(
            'The research desk now has a formula grammar, three search mechanisms, combination tools and records of the supplied computations. Those counts are partial bookkeeping. Valid evaluation also needs the full adaptive history, information provenance, dependence assumptions and attainable execution. This part develops those distinctions while leaving sealed strategy results excluded.'
        ):
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["research"], color=QC.HOUSE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()
