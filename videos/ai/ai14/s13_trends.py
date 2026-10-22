from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (CLOSED, C_COL, DECODER, D_COL, N_COL, OPEN, PART, PRIOR, F, human, load, year_of)


class Trends(VoiceoverScene):
    def construct(self):
        self.card()
        self.tower()
        self.fit()
        self.cost()
        self.tokens()

    def card(self):
        card = chapter_card(12, r"Compute, cost and data", r"How fast has all of this grown?", lit=(2020, 2022),
                            part=PART)
        with self.voiceover("Chapter twelve. Compute, cost, and data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tower(self):
        E = load("epoch")
        tw = E["tower"]
        lo, hi = 18, 27
        H = 6.0
        ybase = -3.0
        n = len(tw)
        xs = np.linspace(-5.6, 5.0, n)
        axis = Line([-6.5, ybase, 0], [-6.5, ybase + H, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for e in range(lo, hi + 1, 2):
            y = ybase + H * (e - lo) / (hi - lo)
            ticks.add(Line([-6.6, y, 0], [-6.4, y, 0], color=GREY_C, stroke_width=2),
                      MathTex(rf"10^{{{e}}}", font_size=22, color=GREY_B).next_to([-6.6, y, 0], LEFT, buff=0.08))
        al = label(r"training operations \ (log scale)", font_size=20, color=GREY_A)
        al.move_to([-6.75, ybase + H + 0.3, 0], aligned_edge=LEFT)
        bars = VGroup()
        for x, t in zip(xs, tw):
            h = H * (math.log10(t["flop"]) - lo) / (hi - lo)
            est = t["src"] == "Epoch"
            b = Rectangle(width=0.62, height=h, stroke_color=C_COL, stroke_width=2,
                          fill_color=C_COL, fill_opacity=0.15 if est else 0.75).move_to([x, ybase, 0], aligned_edge=DOWN)
            nm = label(t["label"], font_size=17, color=WHITE).rotate(PI / 2)
            nm.move_to(b.get_bottom() + UP * (nm.height / 2 + 0.12))
            if nm.height > h - 0.2:
                nm.next_to(b, UP, buff=0.08 + 0.3)
            yr = label(t["date"][:4], font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.08)
            v = MathTex(sci(t["flop"], 1).replace(r" \times ", r"\!\times\!"), font_size=16, color=C_COL)
            v.next_to(b, UP, buff=0.06)
            if nm.get_bottom()[1] > b.get_top()[1]:
                v.next_to(nm, UP, buff=0.06)
            bars.add(VGroup(b, nm, yr, v))
        key = VGroup(VGroup(Square(0.22, stroke_color=C_COL, fill_color=C_COL, fill_opacity=0.75),
                            label(r"reported by the paper", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.22, stroke_color=C_COL, fill_color=C_COL, fill_opacity=0.15),
                            label(r"Epoch AI's estimate", font_size=18, color=GREY_A)).arrange(RIGHT, buff=0.12))
        key.arrange(RIGHT, buff=0.6).move_to([-0.5, 3.6, 0])
        ratio = E["tower_ratio"]
        yrs = E["tower_span_years"]
        with self.voiceover(
            "Line up the training compute of the models in this part, on a scale where each step up is a hundred "
            "times more. <bookmark mark='a'/> The 2017 Transformer: two times ten to the nineteen operations. GPT-1, "
            "BERT, GPT-2, T5. <bookmark mark='b'/> GPT-3: three times ten to the twenty-three. PaLM. "
            "<bookmark mark='c'/> GPT-4, about two times ten to the twenty-five by Epoch AI's estimate; Llama 3.1, "
            "3.8 times ten to the twenty-five, as Meta reported; and xAI's Grok 3, in 2025, about 3.5 times ten to the "
            f"twenty-six, again an outside estimate. <bookmark mark='d'/> In {yrs:.1f} years, a factor of about "
            f"{ratio / 1e6:.0f} million."
        ) as vo:
            self.play(Create(axis), FadeIn(ticks), FadeIn(al), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]), FadeIn(b[3]))
                                    for b in bars[:5]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]), FadeIn(b[3]))
                                    for b in bars[5:7]], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]), FadeIn(b[3]))
                                    for b in bars[7:]], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(bars[-1], color=YELLOW, scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fit(self):
        E = load("epoch")
        f = E["frontier"]
        x, y = np.asarray(f["x"]), np.asarray(f["y"])
        g = axes([2017, 2026.5], [18, 27.5], x_length=6.6, y_length=4.6, xlabel=r"publication date",
                 ylabel=r"training operations", xticks=[2018, 2020, 2022, 2024, 2026], yticks=[19, 21, 23, 25, 27],
                 xfmt=lambda v: f"{int(v)}", yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.9, -0.4, 0])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.055, color=C_COL) for a, b in zip(x, y)])
        xs = np.array([2017.3, 2026.4])
        line = Line(ax.c2p(xs[0], f["icept"] + f["slope"] * (xs[0] - 2020)),
                    ax.c2p(xs[1], f["icept"] + f["slope"] * (xs[1] - 2020)), color=WHITE, stroke_width=3)
        rows = [
            cmath(r"\log_{10} C", r"=", r"a + b\, t", font_size=32),
            cmath(r"b", r"=", rf"{f['slope']:.3f}", font_size=32),
            cmath(r"10^{b}", r"=", rf"{f['per_year']:.1f}\ \text{{per year}}", font_size=32),
            cmath(r"T_2", r"=", rf"\frac{{12 \log_{{10}} 2}}{{b}} = {f['doubling_months']:.1f}\ \text{{months}}",
                  font_size=32),
        ]
        for r in rows:
            r[0].set_color(C_COL)
        whys = [why(r"least squares, \ $t$ in years"),
                why(rf"${f['n']}$ frontier language models"),
                why(rf"90\% interval: \ ${f['lo']:.1f}$ to ${f['hi']:.1f}$"),
                why(r"the doubling time")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=2.5, buff=0.32, edge=6.95)
        ep = F.EPOCH
        their = label(rf"Epoch's own analysis: \ ${ep['headline'][0]}$--${ep['headline'][1]}\times$ a year; \\ frontier "
                      rf"language models since mid-2020: \ about ${ep['growth_frontier_lm']:g}\times$", font_size=22,
                      color=GREY_A).move_to([3.6, -3.1, 0])
        cite_ = cite(r"data: \ Epoch AI, \textit{Notable AI Models} (downloaded 19 October 2026); \ fit: ours", corner=DL,
                     font_size=17)
        agree = abs(f["per_year"] - ep["growth_frontier_lm"]) < 1.0
        tail = ("Our fit agrees with theirs." if agree else
                f"Our fit, {f['per_year']:.1f}, differs from theirs, because it covers a different span of models.")
        with self.voiceover(
            "How fast is that, as a rate? Epoch AI keeps a database of notable models. Here are the language models "
            "it marks as frontier, those near the top in compute when they appeared, since 2017. <bookmark mark='a'/> "
            "Fit a straight line to the logarithm of the compute against the date. <bookmark mark='b'/> The slope, b, "
            f"comes out at {f['slope']:.3f} powers of ten per year. <bookmark mark='c'/> So the compute grows by a "
            f"factor of ten to the b: about {f['per_year']:.1f} times a year. <bookmark mark='d'/> It doubles every "
            f"{f['doubling_months']:.1f} months. Epoch's own analysis puts frontier models at four to five times a "
            "year. " + tail
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.03), FadeIn(cite_), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(line))
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(their))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cost(self):
        ep, P = F.EPOCH, load("published")
        items = [(r"GPT-4 \ (2023)", ep["gpt4_usd"], CLOSED, r"Epoch estimate: \ hardware and energy, final run"),
                 (r"Gemini 1.0 Ultra \ (2023)", ep["gemini_usd"], CLOSED, r"Epoch estimate"),
                 (r"DeepSeek-V3 \ (2024)", P["dsv3_usd"], OPEN, r"reported: \ GPU-hours $\times$ \$2")]
        bars = VGroup()
        for i, (nm, v, col, src) in enumerate(items):
            w = 6.0 * v / 4.5e7
            n_ = label(nm, font_size=22, color=GREY_A).move_to([-1.4, 1.2 - 0.95 * i, 0], aligned_edge=RIGHT)
            b = Rectangle(width=w, height=0.45, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-1.2, 1.2 - 0.95 * i, 0], aligned_edge=LEFT)
            t = label(rf"\${v / 1e6:.1f} million", font_size=24, color=col).next_to(b, RIGHT, buff=0.15)
            s_ = note(src, font_size=16).next_to(b, DOWN, buff=0.06).align_to(b, LEFT)
            bars.add(VGroup(n_, b, t, s_))
        head = label(r"the cost of a frontier training run", font_size=30, color=WHITE).to_edge(UP, buff=0.6)
        trend = label(rf"Epoch: \ costs grew ${ep['cost_growth']}\times$ a year since 2016; \ on that trend, \\ the "
                      rf"largest runs cost over a billion dollars by {ep['billion_by']}", font_size=24,
                      color=C_COL).move_to(DOWN * 2.0)
        caveat = note(r"every such figure leaves out the research and failed runs before the final one").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Cost grew more slowly than compute, because each operation got cheaper, but it grew. "
            "<bookmark mark='a'/> Epoch AI estimates that the hardware and energy for GPT-4's final training run cost "
            "about forty million dollars, and Gemini Ultra's about thirty. <bookmark mark='b'/> Across frontier models, "
            "costs grew about 2.4 times a year since 2016; on that trend, the largest runs pass a billion dollars by "
            "2027. <bookmark mark='c'/> Against that, DeepSeek reported about 5.6 million dollars for V3's final run: "
            "what sparse models, careful engineering and cheap 8-bit arithmetic buy. Like every such figure, it leaves "
            "out the research and the failed runs before the final one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(caveat))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2]), FadeIn(b[3]))
                                    for b in bars[:2]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(trend))
            vo.wait_until("c")
            self.play(FadeIn(bars[2][0]), GrowFromEdge(bars[2][1], LEFT), FadeIn(bars[2][2]), FadeIn(bars[2][3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tokens(self):
        P = load("published")
        tpp = P["tpp"]
        g = axes([2019.8, 2026.5], [-0.3, 5.2], x_length=8.2, y_length=4.8, xlabel=r"year",
                 ylabel=r"training tokens per parameter \ (log scale; \ active parameters for experts)",
                 xticks=[2020, 2022, 2024, 2026], yticks=[0, 1, 2, 3, 4, 5], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-1.6, -0.4, 0])
        ax = g.ax
        opt = DashedLine(ax.c2p(2019.8, math.log10(20)), ax.c2p(2026.5, math.log10(20)), color=C.TRUE_P,
                         dash_length=0.08)
        ol = label(r"Chinchilla: \ about $20$", font_size=18, color=C.TRUE_P).next_to(opt, UP, buff=0.05)
        ol.align_to(opt, LEFT).shift(RIGHT * 0.15)
        dots, names = VGroup(), VGroup()
        side = {"GPT-3": UP, "Gopher": DOWN, "Chinchilla": DOWN, "PaLM": UR, "LLaMA-7B": UL, "LLaMA-65B": DR,
                "Llama 2 70B": UR, "Llama 3.1 405B": RIGHT, "DeepSeek-V3": UL, "Qwen3-0.6B": RIGHT, "Kimi K2": DR,
                "GLM-5": UP}
        for r in tpp:
            col = PRIOR if r["year"] < 2022.5 else OPEN
            if r["name"] == "Chinchilla":
                col = C.TRUE_P
            d = Dot(ax.c2p(r["year"], math.log10(r["ratio"])), radius=0.08, color=col)
            dots.add(d)
            names.add(label(r["name"], font_size=17, color=col).next_to(d, side.get(r["name"], UP), buff=0.06))
        old = [i for i, r in enumerate(tpp) if r["year"] < 2022.5]
        new = [i for i, r in enumerate(tpp) if r["year"] >= 2022.5]
        qw = next(r for r in tpp if r["name"] == "Qwen3-0.6B")
        side_t = VGroup(label(r"small models are \\ over-trained on purpose: \\ they run most often", font_size=22,
                              color=OPEN),
                        label(r"and good text is finite: \\ where the tokens come from \\ is Part 18", font_size=22,
                              color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([5.0, 0.2, 0])
        with self.voiceover(
            "Finally the data: how many tokens each model read per parameter. <bookmark mark='a'/> In 2020 and 2021, "
            "GPT-3 and Gopher read fewer than two tokens per parameter. <bookmark mark='b'/> Chinchilla, in 2022, "
            "showed that about twenty is compute-optimal. <bookmark mark='c'/> Since then, open models have gone far "
            "past it: LLaMA's 7-billion-parameter model a hundred and fifty, DeepSeek-V3 four hundred per active "
            f"parameter, and Qwen3's smallest model, {qw['n'] / 1e9:.1f} billion parameters, read about "
            f"{qw['d'] / 1e12:.0f} trillion tokens: {qw['ratio']:,.0f} per parameter. <bookmark mark='d'/> Small models "
            "are over-trained on purpose, because they are the ones that run most often. And good text is finite: "
            "where the tokens come from is Part 18."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(*[FadeIn(dots[i], scale=1.5) for i in old if tpp[i]["name"] != "Chinchilla"],
                      *[FadeIn(names[i]) for i in old if tpp[i]["name"] != "Chinchilla"])
            vo.wait_until("b")
            ci = [r["name"] for r in tpp].index("Chinchilla")
            self.play(FadeIn(dots[ci], scale=1.5), FadeIn(names[ci]), Create(opt), FadeIn(ol))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i], scale=1.5), FadeIn(names[i])) for i in new],
                                  lag_ratio=0.25), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(side_t, shift=LEFT * 0.1))
        self.wait(0.3)
        self.clear_scene()
