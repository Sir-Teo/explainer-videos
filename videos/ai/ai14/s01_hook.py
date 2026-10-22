from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import (ARCH_COLOR, DECODER, ENCDEC, ENCODER, F, N_COL, PART, arch_diagram, human, load,
                                   log_axes, node_box, year_of)


class Hook(VoiceoverScene):
    def construct(self):
        self.era()
        self.question()
        self.ours()
        self.plan()

    # ------------------------------------------------------------------
    def era(self):
        T = F.TRANSFORMER
        tf, k3 = F.CFG["transformer"], F.CFG["kimik3"]
        hc = history_card(2017, r"Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser \& Polosukhin "
                          r"(Google)", r"\textit{Attention Is All You Need}: \ a new architecture for translating "
                          r"English into German and French", width=8.6, color=ENCDEC).move_to(UP * 1.6)
        stats = VGroup(
            VGroup(label(human(tf["params"]), font_size=46, color=ENCDEC), label(r"parameters", font_size=20, color=GREY_A))
            .arrange(DOWN, buff=0.1),
            VGroup(label(rf"${T['big']['hours'] / 24:.1f}$ days", font_size=46, color=ENCDEC),
                   label(rf"on ${T['gpus']}$ graphics cards", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.1),
        ).arrange(RIGHT, buff=1.6).move_to(DOWN * 1.2)
        # every model of this part with a published size, by date and parameters (log scale)
        pts = [c for c in F.CONFIGS if c.get("params")]
        g = log_axes([2017, 2027], [8, 13], x_length=10.0, y_length=4.9, xlabel=r"year",
                     ylabel=r"parameters \ (log scale: each step is $10\times$)", center=[0.3, -0.35, 0],
                     xticks=[2017, 2019, 2021, 2023, 2025, 2027], yticks=[8, 9, 10, 11, 12, 13])
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(year_of(c["date"]), math.log10(c["params"])), radius=0.08,
                            color=ARCH_COLOR[c["arch"]]) for c in pts])
        names = {"transformer": (UR, r"Transformer"), "gpt2": (UL, r"GPT-2"), "gpt3": (UL, r"GPT-3"),
                 "llama": (DR, r"LLaMA"), "kimik3": (LEFT, r"Kimi K3")}
        tags = VGroup()
        for c, d in zip(pts, dots):
            if c["key"] in names:
                dirn, t = names[c["key"]]
                tags.add(label(t, font_size=20, color=ARCH_COLOR[c["arch"]]).next_to(d, dirn, buff=0.08))
        key = VGroup(*[VGroup(Dot(radius=0.07, color=col), label(t, font_size=18, color=col)).arrange(RIGHT, buff=0.1)
                       for col, t in ((ENCDEC, r"encoder--decoder"), (ENCODER, r"encoder only"),
                                      (DECODER, r"decoder only"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.move_to(ax.c2p(2017.3, 12.9), aligned_edge=UL)
        x_chat = year_of(F.CHATGPT["date"])
        chat = DashedLine(ax.c2p(x_chat, 8), ax.c2p(x_chat, 13), color=GREY_B, dash_length=0.08)
        chat_l = label(r"ChatGPT, \ Nov 2022", font_size=20, color=GREY_A).next_to(chat, UP, buff=0.08)
        ratio = k3["params"] / tf["params"]
        k3dot = dots[[c["key"] for c in pts].index("kimik3")]
        ring = Circle(radius=0.2, color=YELLOW, stroke_width=3).move_to(k3dot)
        tag = cite(r"published sizes: \ Vaswani et al.\ (2017) \dots\ Kimi K3 model card (2026)")
        with self.voiceover(
            "June 2017. Eight researchers at Google publish a paper with a confident title: Attention Is All You "
            "Need. <bookmark mark='a'/> Their model translates English into German and French. The larger version has "
            f"{human(tf['params'])[:-1]} million parameters, and it trained for three and a half days on eight graphics "
            "cards. <bookmark mark='b'/> Here is every model this part will meet, placed by the date it appeared and by "
            "its size, on a scale where each step up is ten times more. <bookmark mark='c'/> By November 2022, the "
            "same building block, made much larger, was answering questions for anyone who asked: ChatGPT. "
            "<bookmark mark='d'/> And by the autumn of 2026, models you can download and run yourself have trillions "
            f"of parameters. Moonshot AI's Kimi K3 has {k3['params'] / 1e12:.1f} trillion, about "
            f"{round(ratio, -3):,.0f} times the 2017 Transformer."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in stats], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeOut(hc), FadeOut(stats), FadeIn(g), FadeIn(key), FadeIn(tag))
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.15), FadeIn(tags, lag_ratio=0.2),
                      run_time=3.5)
            vo.wait_until("c")
            self.play(Create(chat), FadeIn(chat_l))
            vo.wait_until("d")
            self.play(Create(ring), Indicate(tags[-1], color=YELLOW))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"How did a model built to translate sentences \\ become the engine of nearly everything?",
                  font_size=40).move_to(UP * 1.9)
        steps = [(r"Transformer", ENCDEC), (r"GPT", DECODER), (r"BERT", ENCODER), (r"T5", ENCDEC),
                 (r"GPT-2", DECODER), (r"GPT-3", DECODER), (r"ChatGPT", DECODER), (r"LLaMA", DECODER),
                 (r"DeepSeek", DECODER), (r"Qwen", DECODER), (r"Kimi", DECODER)]
        path = VGroup()
        for i, (t, c) in enumerate(steps):
            if i:
                path.add(MathTex(r"\to", font_size=30, color=GREY_C))
            path.add(label(t, font_size=26, color=c))
        path.arrange(RIGHT, buff=0.16)
        if path.width > 13.2:
            path.width = 13.2
        path.move_to(DOWN * 0.1).set_opacity(0.25)
        asks = VGroup(label(r"who built what, \ and when", font_size=28, color=GREY_A),
                      label(r"what each step changed", font_size=28, color=GREY_A),
                      label(r"why it worked", font_size=28, color=GREY_A)).arrange(RIGHT, buff=0.9)
        asks.to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "How did a model built to translate sentences become the engine of nearly everything? That is the story of "
            "this part. <bookmark mark='a'/> It runs from the translation Transformer, through GPT and BERT, T5, GPT-2 "
            "and GPT-3, to ChatGPT, and on to the open-weight models of today. <bookmark mark='b'/> At each step we'll "
            "ask who built what, and when; what the step changed; and why it worked."
        ) as vo:
            self.play(FadeIn(q), FadeIn(path))
            vo.wait_until("a")
            self.play(LaggedStart(*[m.animate.set_opacity(1) for m in path], lag_ratio=0.08), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a, shift=UP * 0.1) for a in asks], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        fam = load("family")
        rows = fam["rows"]
        gpt = VGroup(arch_diagram("decoder", 0.9), label(r"GPT-style: \\ predict the next token", font_size=22,
                                                         color=DECODER)).arrange(DOWN, buff=0.25)
        bert = VGroup(arch_diagram("encoder", 0.9), label(r"BERT-style: \\ fill in the blanks", font_size=22,
                                                          color=ENCODER)).arrange(DOWN, buff=0.25)
        pair = VGroup(gpt, bert).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([-2.9, 0.7, 0])
        pair.to_edge(LEFT, buff=0.6)
        same = label(rf"same shape, \ same starting weights, \\ same ${fam['tokens'] / 1e6:.0f}$ million tokens of the "
                     r"novels", font_size=24, color=GREY_A).next_to(pair, DOWN, buff=0.45)
        sch = note(r"schematic").to_corner(UL, buff=0.3)
        # the family: a bar per model, as long as its parameter count (log scale)
        lo, hi = 5.0, 7.0
        bars = VGroup()
        for i, r in enumerate(rows):
            w = 3.2 * (math.log10(r["total"]) - lo) / (hi - lo)
            b = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=DECODER, fill_opacity=0.35 + 0.15 * i)
            t = label(human(r["total"], 2), font_size=20, color=WHITE)
            bars.add(VGroup(b, t))
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        for b in bars:
            b[1].next_to(b[0], RIGHT, buff=0.12)
        fl = label(r"a family of growing size: \\ does learning from examples \\ in the prompt appear?", font_size=24,
                   color=DECODER)
        famg = VGroup(fl, bars).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.2, 0.4, 0])
        books = note(r"all trained on this computer, \ on the thirty novels of Part 1").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Along the way we'll rebuild the lineage in miniature, on the computer making this video, with the thirty "
            "novels this series reads. <bookmark mark='a'/> A GPT-style model, which learns to predict the next "
            "word, and a BERT-style model, which learns to fill in blanks, of exactly the same size, trained with "
            "exactly the same compute, and compared fairly. <bookmark mark='b'/> And a family of GPT-style models of "
            f"growing size, from {human(rows[0]['total'], 2)[:-1]} thousand to {rows[-1]['total'] / 1e6:.1f} million "
            "parameters, to see whether learning from examples in the prompt, the surprise of GPT-3, shows up at our "
            "scale."
        ) as vo:
            self.play(FadeIn(books), FadeIn(pair, shift=UP * 0.15), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(same), Indicate(pair, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeIn(fl), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ The Language-Model Lineage", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"the 2017 Transformer, \ and the three ways to cut it",
            r"pretraining: \ ULMFiT, ELMo, GPT-1, BERT, T5, \ and what they were measured on",
            r"scale: \ GPT-2, scaling laws, GPT-3, \ learning in context, \ $C \approx 6ND$",
            r"from predictor to assistant: \ Codex, instruction tuning, ChatGPT, GPT-4",
            r"open weights, \ the architecture they converged on, \ the frontier of 2026",
            r"trends in compute, cost and data; \ our own GPT against BERT, \ and learning in context",
        ], font_size=26)
        with self.voiceover(
            "This is Part 14 of AI, Built, in its third act, the transformer era. <bookmark mark='a'/> In this part: "
            "the 2017 Transformer, and the three ways to cut it; pretraining, from ULMFiT and GPT-1 to BERT and T5; "
            "scale, from GPT-2 to GPT-3, and learning from the prompt; how a predictor of text became an assistant; "
            "open weights, the design they converged on, and the frontier of 2026; the trends in compute, cost and "
            "data; and our own experiments."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
