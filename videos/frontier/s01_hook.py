from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import (
    Mono, Plot, label, load, mono_lines, note, pipeline_map, pocket_total_flops, pow10_label, schematic_tag, sci,
    source,
)

HIGHLIGHTS = [  # (Epoch model name, on-screen name, label direction)
    ("GPT-2 (1.5B)", r"GPT-2", UL),
    ("GPT-3 175B (davinci)", r"GPT-3", UL),
    ("GPT-4 (Mar 2023)", r"GPT-4", UL),
    ("Llama 3.1-405B", r"Llama 3.1 405B", DR),
    ("Grok 4", r"Grok 4", UL),
    ("GPT-6 Astra", r"GPT-6 Astra", UL),
]


class Hook(VoiceoverScene):
    def construct(self):
        self.chat()
        self.compute_scatter()
        self.pipeline()
        self.roadmap()

    # ------------------------------------------------------------------
    def chat(self):
        win = RoundedRectangle(width=10.5, height=4.8, corner_radius=0.2, stroke_color=GREY_B, stroke_width=2,
                               fill_color=BACKGROUND, fill_opacity=1)
        bar = Rectangle(width=10.5, height=0.42, stroke_width=0, fill_color=GREY_D, fill_opacity=0.6)
        bar.move_to(win.get_top() + DOWN * 0.21)
        dots = VGroup(*[Dot(radius=0.06, color=c) for c in (RED_C, YELLOW_C, GREEN_C)]).arrange(RIGHT, buff=0.1)
        dots.move_to(bar.get_left() + RIGHT * 0.4)
        q = Mono("How were you trained?", font_size=26)
        qb = RoundedRectangle(width=q.width + 0.5, height=q.height + 0.35, corner_radius=0.18, stroke_width=0,
                              fill_color=C.USER, fill_opacity=0.35)
        q.move_to(qb)
        quest = VGroup(qb, q).next_to(bar, DOWN, buff=0.35).align_to(win, RIGHT).shift(LEFT * 0.4)
        answer = ("In stages. First I read trillions of words from the web and learned to predict the next one. "
                  "Then I was trained on conversations, and with reinforcement learning, to be helpful and to "
                  "reason step by step.")
        ans = mono_lines(answer, width=58, max_lines=5, font_size=24, color=WHITE, line_buff=0.14)
        ans.next_to(quest, DOWN, buff=0.4).align_to(win, LEFT).shift(RIGHT * 0.45)
        glyphs = [g for line in ans for g in line.glyphs]
        chunks = [glyphs[i:i + 4] for i in range(0, len(glyphs), 4)]  # "tokens" of ~4 characters
        window = VGroup(win, bar, dots, quest)
        tag = schematic_tag()

        with self.voiceover(
            "You ask a question, and a moment later the answer starts streaming back, one token at a time. "
            "<bookmark mark='m'/> The model writing it is the result of one of the largest computations people "
            "have ever run."
        ) as vo:
            self.play(FadeIn(window), FadeIn(tag), run_time=0.8)
            self.add(*[line.frame for line in ans])
            per = max(0.02, (vo.until("m") + 2.5) / len(chunks))
            for ch in chunks:
                self.add(*ch)
                self.wait(per)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compute_scatter(self):
        rows = [r for r in load("epoch")["rows"] if r["t"] >= 2012 and r["flop"] >= 1e14]
        by_name = {r["model"]: r for r in rows}
        plot = Plot(x_range=(2012, 2027.2), y_range=(1e14, 1e28), width=10.6, height=5.3, log_y=True,
                    x_ticks=list(range(2012, 2027, 2)), y_ticks=[1e14, 1e16, 1e18, 1e20, 1e22, 1e24, 1e26, 1e28],
                    x_fmt=lambda v: MathTex(str(v), font_size=24, color=GREY_A),
                    y_fmt=lambda v: pow10_label(int(round(np.log10(v)))),
                    y_label=r"training compute (operations)")
        plot.move_to(DOWN * 0.25 + RIGHT * 0.35)
        dots = VGroup()
        for r in rows:
            frontier = r["frontier"] == "True"
            d = Dot(plot.c2p(r["t"], r["flop"]), radius=0.04 if frontier else 0.03,
                    color=C.COMPUTE if frontier else GREY_B)
            d.set_opacity(0.85 if frontier else 0.45)
            dots.add(d)
        src = source(r"Epoch AI, \emph{Data on AI models} (CC BY 4.0), retrieved Oct 2026; estimates")
        assert abs(np.log10(by_name["GPT-2 (1.5B)"]["flop"]) - 21.3) < 0.2
        assert 100 < by_name["GPT-3 175B (davinci)"]["flop"] / by_name["GPT-2 (1.5B)"]["flop"] < 300
        assert 50 < by_name["GPT-4 (Mar 2023)"]["flop"] / by_name["GPT-3 175B (davinci)"]["flop"] < 90

        marks = {}
        for name, shown, direction in HIGHLIGHTS:
            r = by_name[name]
            ring = Circle(radius=0.11, color=WHITE, stroke_width=2.5).move_to(plot.c2p(r["t"], r["flop"]))
            lab = label(shown, font_size=24).next_to(ring, direction, buff=0.05)
            marks[name] = VGroup(ring, lab)

        with self.voiceover(
            "Here is every notable AI model with a published estimate of its training compute, placed by release "
            "date and by how many arithmetic operations it took to train, on a logarithmic scale. "
            "<bookmark mark='g2'/> GPT-2, in 2019: about ten to the twenty-one operations. <bookmark mark='g3'/> "
            "GPT-3, a year later: more than a hundred times that. <bookmark mark='g4'/> GPT-4: about seventy times "
            "more again."
        ) as vo:
            self.play(FadeIn(plot), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.004), run_time=2.5)
            for key, name in [("g2", "GPT-2 (1.5B)"), ("g3", "GPT-3 175B (davinci)"), ("g4", "GPT-4 (Mar 2023)")]:
                vo.wait_until(key)
                self.play(Create(marks[name][0]), FadeIn(marks[name][1]), run_time=0.8)

        fr = [r for r in rows if r["frontier"] == "True" and r["t"] > 2018]
        slope, icpt = np.polyfit([r["t"] for r in fr], np.log10([r["flop"] for r in fr]), 1)
        growth = 10**slope
        assert 4.0 < growth < 5.5, growth
        xs = np.array([2018.0, 2027.0])
        trend = DashedLine(plot.c2p(xs[0], 10 ** (icpt + slope * xs[0])), plot.c2p(xs[1], 10 ** (icpt + slope * xs[1])),
                           color=C.COMPUTE, stroke_width=3, dash_length=0.12)
        tl = label(rf"frontier: $\times{growth:.1f}$ per year", font_size=28, color=C.COMPUTE)
        tl.next_to(plot.c2p(2019.3, 3e25), UP, buff=0.0)

        with self.voiceover(
            "The largest runs of 2025 and 2026 are estimated at ten to the twenty-six operations and beyond. "
            "<bookmark mark='trend'/> At the frontier, training compute has been growing almost five times, "
            "every single year."
        ) as vo:
            for name in ["Llama 3.1-405B", "Grok 4", "GPT-6 Astra"]:
                self.play(Create(marks[name][0]), FadeIn(marks[name][1]), run_time=0.7)
            vo.wait_until("trend")
            self.play(Create(trend), FadeIn(tl), run_time=1.5)

        pocket = pocket_total_flops()
        e = int(np.floor(np.log10(pocket)))
        ratio = 1e26 / pocket
        pd = Dot(plot.c2p(2026.7, pocket), radius=0.08, color=C.KEPT)
        pl = label(r"every experiment in this video\\(a 4-core CPU)", font_size=24, color=C.KEPT)
        pl.next_to(pd, LEFT, buff=0.2)
        gap = DoubleArrow(plot.c2p(2026.95, pocket * 2), plot.c2p(2026.95, 1e26 / 2), buff=0, color=GREY_A,
                          stroke_width=3, tip_length=0.2)
        gl = MathTex(rf"\sim {sci(ratio, 0)}\times", font_size=30, color=GREY_A).next_to(gap, LEFT, buff=0.15)
        gl.shift(UP * 0.6)
        assert 14 <= e <= 16, pocket

        with self.voiceover(
            "And so that none of this is a cartoon: every experiment in this video was actually run, in miniature, "
            "on the four-core computer that rendered it. <bookmark mark='dot'/> All of them together took about "
            "ten to the fifteen operations, <bookmark mark='gap'/> roughly a hundred billion times less than a "
            "frontier run. The scale is different. The ideas are the same."
        ) as vo:
            vo.wait_until("dot")
            self.play(FadeIn(pd, scale=2), FadeIn(pl))
            vo.wait_until("gap")
            self.play(GrowFromCenter(gap), FadeIn(gl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipeline(self):
        m = pipeline_map(width=13.4).move_to(UP * 0.7)
        subs = [
            r"crawled pages,\\billions of them",
            r"filtered, deduped,\\mixed: $10^{13}$ tokens",
            r"predict the\\next token",
            r"$10^4$--$10^5$ GPUs,\\for months",
            r"instructions,\\preferences, RL",
            r"helpful,\\and it reasons",
        ]
        sub = VGroup(*[note(s, font_size=21, color=GREY_A).next_to(g.text, DOWN, buff=0.2)
                       for s, g in zip(subs, m.stages)])
        head = label(r"Training a frontier model, end to end", font_size=40).to_edge(UP, buff=0.5)
        keys = ["web", "data", "pre", "gpu", "post", "asst"]

        with self.voiceover(
            "This video follows one of those training runs from end to end. It starts with <bookmark mark='web'/> "
            "a crawl of the public web, <bookmark mark='data'/> which is filtered, deduplicated and mixed into a "
            "dataset of tens of trillions of tokens. <bookmark mark='pre'/> Pretraining teaches a network to "
            "predict the next token of that text, <bookmark mark='gpu'/> with the work spread across tens of "
            "thousands of GPUs for months. <bookmark mark='post'/> Post-training then turns that raw text "
            "predictor into something that follows instructions and reasons, <bookmark mark='asst'/> and the "
            "result is the assistant."
        ) as vo:
            self.play(FadeIn(head))
            for i, k in enumerate(keys):
                vo.wait_until(k)
                anims = [FadeIn(m.stages[i], shift=UP * 0.15), FadeIn(sub[i])]
                if i:
                    anims.append(GrowArrow(m.arrows[i - 1]))
                self.play(*anims, run_time=0.8)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def roadmap(self):
        parts = VGroup(
            label(r"\textbf{1.} The data: from raw web pages to trillions of clean tokens", font_size=34),
            label(r"\textbf{2.} The recipe: scaling laws, architecture, optimizer, precision", font_size=34),
            label(r"\textbf{3.} Scaling out: memory, parallelism, and keeping 16{,}000 GPUs alive", font_size=34),
            label(r"\textbf{4.} Post-training: from text predictor to assistant", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        with self.voiceover(
            "We'll go in four parts: <bookmark mark='a'/> the data, <bookmark mark='b'/> the training recipe, "
            "<bookmark mark='c'/> scaling it out across a cluster, <bookmark mark='d'/> and post-training. Along "
            "the way, we'll look at what the labs have actually published about how they do it, as of October "
            "2026."
        ) as vo:
            for i, k in enumerate("abcd"):
                vo.wait_until(k)
                self.play(FadeIn(parts[i], shift=RIGHT * 0.2), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(parts))
        card = VGroup(
            label(r"How Frontier AI Models Are Trained", font_size=64),
            label(r"end to end, from the raw web to a reasoning assistant", font_size=36, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(card, scale=1.05), run_time=1.2)
        self.wait(2.5)
        self.play(FadeOut(card))
