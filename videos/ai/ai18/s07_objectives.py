from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (EDU, F, KEPT, PART, REMOVED, chip, hbars, load, take_away)

TGT = C.PROB  # a prediction target
CTX = GREY_B  # context only


def chips(toks, colors, font_size=18, max_width=13.2):
    row = VGroup(*[chip(t.replace(" ", "·") if t.strip() else t, c, font_size=font_size, height=0.42)
                   for t, c in zip(toks, colors)]).arrange(RIGHT, buff=0.05)
    if row.width > max_width:
        row.width = max_width
    return row


class Objectives(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.targets()

    def card(self):
        card = chapter_card(6, r"What the model is asked to predict", r"Next token, masked token, missing span, or "
                            r"the middle?", lit=(2018,), part=PART)
        with self.voiceover("Chapter six. What the model is asked to predict."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def four(self):
        O = load("objectives")
        toks = O["tokens"]
        n = len(toks)
        y = [2.55, 1.05, -0.45, -2.0]
        names = [r"causal: \ every next token", r"masked (BERT): \ the hidden $15\%$",
                 r"span corruption (T5): \ the missing spans", r"fill in the middle: \ moved to the end"]
        heads = VGroup(*[label(t, font_size=22, color=EDU).move_to([-6.6, yy + 0.5, 0], aligned_edge=LEFT)
                         for t, yy in zip(names, y)])
        causal = chips(toks, [TGT] * n).move_to([0, y[0], 0])
        mlm = chips([t for t, _ in O["mlm"]], [TGT if m else CTX for _, m in O["mlm"]]).move_to([0, y[1], 0])
        span_in = chips(O["span_input"], [C.ATTN if t.startswith("<") else CTX for t in O["span_input"]], font_size=16)
        span_out = chips(O["span_target"], [C.ATTN if t.startswith("<") else TGT for t in O["span_target"]],
                         font_size=16, max_width=5.0)
        arrow = MathTex(r"\Rightarrow", font_size=30, color=GREY_B)
        span = VGroup(span_in, arrow, span_out).arrange(RIGHT, buff=0.15)
        if span.width > 13.2:
            span.width = 13.2
        span.move_to([0, y[2], 0])
        fm = O["fim"]
        fim_t = ["<PRE>"] + fm["prefix"] + ["<SUF>"] + fm["suffix"] + ["<MID>"] + fm["middle"]
        fim_c = [C.ATTN] + [TGT] * len(fm["prefix"]) + [C.ATTN] + [TGT] * len(fm["suffix"]) + [C.ATTN] + \
            [TGT] * len(fm["middle"])
        fim = chips(fim_t, fim_c, font_size=16).move_to([0, y[3], 0])
        lg = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=TGT, fill_opacity=0.6),
                           label(r"a prediction target", font_size=18, color=TGT)).arrange(RIGHT, buff=0.1),
                    VGroup(Square(0.22, stroke_width=0, fill_color=C.ATTN, fill_opacity=0.6),
                           label(r"a marker token", font_size=18, color=C.ATTN)).arrange(RIGHT, buff=0.1)
                    ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        src = cite(r"Devlin et al.\ (2019); \ Raffel et al.\ (2020); \ Bavarian et al.\ (2022)", corner=DR,
                   font_size=17)
        with self.voiceover(
            "Pretraining needs a question to ask of every piece of text. Here is the first sentence of Pride and "
            f"Prejudice, cut into our tokenizer's {n} tokens, and the four questions labs have asked of it. "
            "<bookmark mark='a'/> GPT's causal objective: predict every token from the ones before it; every token is a "
            "target. <bookmark mark='b'/> BERT's masked objective: hide fifteen percent of the tokens, mostly behind a "
            "mask, and predict only those. <bookmark mark='c'/> T5's span corruption: replace short runs of tokens with "
            "single markers, and have the model write out what each marker hid. <bookmark mark='d'/> And fill in the "
            "middle. In 2022 OpenAI's Bavarian and colleagues cut documents at two random points and moved the middle to "
            "the end, behind markers for prefix, suffix and middle. The model still predicts the next token, but given a "
            "beginning and an end it can now write what goes between: exactly what a code editor needs."
        ) as vo:
            self.play(FadeIn(heads[0]), FadeIn(causal), FadeIn(lg), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(c_, color=TGT, scale_factor=1.15) for c_ in causal], lag_ratio=0.05),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(heads[1]), FadeIn(mlm))
            vo.wait_until("c")
            self.play(FadeIn(heads[2]), FadeIn(span))
            vo.wait_until("d")
            self.play(FadeIn(heads[3]), FadeIn(fim))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def targets(self):
        O = load("objectives")
        T = O["T"]
        tg = O["targets"]
        rows = hbars([(r"causal", tg["causal"], TGT), (r"fill in the middle", tg["fim"], TGT),
                      (r"span corruption \ (targets incl.\ markers)", tg["span"], EDU),
                      (r"masked", tg["mlm"], REMOVED)], T, width=5.6, font_size=22, label_width=4.6,
                     fmt=lambda v: rf"${int(v)}$")
        rows.move_to([0.8, 1.4, 0])
        rh = label(rf"prediction targets in a sequence of ${T}$ tokens", font_size=24, color=GREY_A)
        rh.next_to(rows, UP, buff=0.3)
        fimc = VGroup(
            label(rf"Bavarian et al.: \ half the documents in FIM order, \ and left-to-right perplexity unchanged",
                  font_size=22, color=GREY_A),
            label(rf"DeepSeek-V3: \ FIM on ${100 * F.DSV3['fim']:.0f}\%$ of documents, \ prefix--suffix--middle order",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(DOWN * 1.5)
        tw = take_away(r"every token a target, \ text that can be sampled and scored, \ infilling for free",
                       color=TGT, font_size=26)
        src = cite(r"Bavarian et al.\ (2022), Fig.\ 1; \ DeepSeek-AI (2024), Sec.\ 4.1", font_size=17)
        with self.voiceover(
            "Count the targets. In a sequence of 256 tokens, the causal objective gives 255 predictions to learn "
            f"from; masking gives about {tg['mlm']}, and span corruption about {tg['span']}, markers included. "
            "<bookmark mark='a'/> Fill in the middle keeps all of them: it is still next-token prediction, on rearranged "
            "text. Bavarian's team put half their documents in that order and found the ordinary left-to-right "
            "perplexity unchanged: infilling for free. <bookmark mark='b'/> DeepSeek-V3 rearranges ten percent of its "
            "documents this way. <bookmark mark='c'/> So the 2026 answer is Part 14's: predict every next token, because "
            "that model can be sampled, scored and prompted; and teach it to fill gaps by rearranging the data, not by "
            "changing the objective."
        ) as vo:
            self.play(FadeIn(rh), FadeIn(src), LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT),
                                                                           FadeIn(r_[2])) for r_ in rows],
                                                          lag_ratio=0.4), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(fimc[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(fimc[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
