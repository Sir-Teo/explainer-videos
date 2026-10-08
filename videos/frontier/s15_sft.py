from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Mono, bar_rows, label, load, mono_lines, part_card, pipeline_map, source

SPECIAL = ("<|im_start|>", "<|im_end|>", "<think>", "</think>")


def show_piece(p: str) -> str:
    return p.replace("\n", "↵")


class SFT(VoiceoverScene):
    def construct(self):
        self.c = load("chat")
        self.opening()
        self.base_vs_chat()
        self.template()
        self.data()

    # ------------------------------------------------------------------
    def opening(self):
        card = part_card(4, r"Post-training", r"from text predictor to assistant").to_edge(UP, buff=1.0)
        m = pipeline_map(width=13.0, highlight="post").to_edge(DOWN, buff=0.7)
        with self.voiceover("Part four: post-training."):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(m), run_time=1.2)
        self.wait(0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def base_vs_chat(self):
        c = self.c
        q = c["base_prompt"].strip()
        assert q == "Where is the Eiffel Tower?" and c["base_output"].startswith("A. Paris\nB. London")
        assert "Paris" in c["chat_output"]

        def panel(title, body, color, x):
            t = label(title, font_size=28, color=color)
            qq = Mono(q, font_size=22, color=C.USER)
            out = mono_lines(body.replace("**", ""), width=34, max_lines=9, font_size=20, color=WHITE)
            g = VGroup(t, qq, out).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            box = SurroundingRectangle(g, buff=0.3, color=color, corner_radius=0.12, stroke_width=2)
            return VGroup(box, g).move_to([x, -0.3, 0]), out

        lp, lout = panel(r"Qwen3-0.6B-Base (after pretraining)", c["base_output"], C.PAGE, -3.5)
        rp, rout = panel(r"Qwen3-0.6B (after post-training)", c["chat_output"], C.ASSISTANT, 3.5)
        rp.align_to(lp, UP)
        head = label(r"Same question, same network size, greedy decoding", font_size=32).to_edge(UP, buff=0.4)
        tag = label(r"real outputs", font_size=22, color=GREY_B).to_corner(UR, buff=0.3)
        with self.voiceover(
            "After pretraining, we have a base model: a superb document completer, but not an assistant. Ask the "
            "base version of Qwen3's smallest model where the Eiffel Tower is, <bookmark mark='b'/> and it decides "
            "it's reading a quiz. It writes the multiple-choice options, the answer key, and then the next question. "
            "<bookmark mark='c'/> The same model after post-training simply answers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(FadeIn(lp[0]), FadeIn(lp[1][:2]), FadeIn(rp[0]), FadeIn(rp[1][:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(ln) for ln in lout], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(ln) for ln in rout], lag_ratio=0.25), run_time=1.2)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def template(self):
        c = self.c
        pieces = c["pieces"]
        n_prompt = c["n_prompt"]
        assert pieces[0] == "<|im_start|>" and pieces[n_prompt - 1] == "\n" and "<think>" in pieces
        boxes = VGroup()
        role = "system"
        for i, p in enumerate(pieces):
            if i > 0 and pieces[i - 1] == "<|im_start|>":
                role = p
            special = p in SPECIAL
            col = C.ASSISTANT if i >= n_prompt else (C.USER if role == "user" else GREY_B)
            t = Mono(show_piece(p), font_size=19, color=GOLD_B if special else WHITE)
            b = RoundedRectangle(width=t.width + 0.14, height=0.42, corner_radius=0.06, stroke_color=col,
                                 stroke_width=1.5, fill_color=col, fill_opacity=0.18)
            t.move_to(b)
            boxes.add(VGroup(b, t))
        # flow the boxes into lines that break after each <|im_end|>\n
        lines, cur = [], []
        for i, b in enumerate(boxes):
            cur.append(b)
            if pieces[i] == "\n" and i > 0 and pieces[i - 1] == "<|im_end|>":
                lines.append(cur)
                cur = []
        if cur:
            lines.append(cur)
        rows = VGroup()
        for ln in lines:
            row = VGroup(*ln).arrange(RIGHT, buff=0.05)
            if row.width > 13.2:
                half = len(ln) // 2
                rows.add(VGroup(*ln[:half]).arrange(RIGHT, buff=0.05))
                rows.add(VGroup(*ln[half:]).arrange(RIGHT, buff=0.05))
            else:
                rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(DOWN * 0.1)
        head = label(rf"One conversation $=$ one stream of {len(pieces)} tokens (Qwen3's real chat format)", font_size=32)
        head.to_edge(UP, buff=0.45)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=col, fill_opacity=0.5),
                                 label(t, font_size=22)).arrange(RIGHT, buff=0.12)
                          for col, t in [(GREY_B, r"system"), (C.USER, r"user"), (C.ASSISTANT, r"assistant"),
                                         (GOLD_B, r"special tokens")]]).arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.2)
        with self.voiceover(
            "The first step is supervised fine-tuning. Conversations are written out as a single stream of tokens, "
            "with special tokens marking who is speaking. <bookmark mark='q'/> Here is Qwen3's actual format: a "
            "start marker, the speaker's role, the message, and an end marker. <bookmark mark='t'/> The assistant's "
            "turn even begins with a thinking block, empty here because thinking was switched off."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend))
            vo.wait_until("q")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.02), run_time=2.5)
            vo.wait_until("t")
            think = [boxes[i] for i, p in enumerate(pieces) if p in ("<think>", "</think>")]
            self.play(*[Indicate(t, color=GOLD_B, scale_factor=1.15) for t in think])

        dim = [b for i, b in enumerate(boxes) if i < n_prompt]
        train = [b for i, b in enumerate(boxes) if i >= n_prompt]
        loss = MathTex(r"\mathcal{L} = -\!\!\sum_{t\,\in\,\text{assistant}} \log p(\text{token}_t \mid \text{everything before})",
                       font_size=34, color=C.ASSISTANT).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Training is the same next-token prediction as before, with one change: <bookmark mark='m'/> the loss is "
            "only counted on the assistant's tokens. The model isn't learning to predict what users say. It's "
            "learning how the assistant replies."
        ) as vo:
            vo.wait_until("m")
            self.play(*[b.animate.set_opacity(0.25) for b in dim], *[b[0].animate.set_fill(opacity=0.45) for b in train],
                      FadeIn(loss))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def data(self):
        sets = [  # (name, year, examples, what)
            (r"\textbf{InstructGPT}", 2022, 13_000, r"human-written demonstrations"),
            (r"\textbf{LIMA}", 2023, 1_000, r"carefully curated examples"),
            (r"\textbf{T\"ulu 3}", 2024, 939_344, r"prompts, mostly synthetic, filtered"),
            (r"\textbf{OLMo 3 Think}", 2025, 2_300_000, r"prompts ($\approx$45B tokens)"),
        ]
        fmt = {13_000: r"$\approx$13{,}000", 1_000: r"1{,}000", 939_344: r"939{,}344", 2_300_000: r"$\approx$2.3M"}
        rows = bar_rows([(rf"{n} ({y})", np.log10(v) - 2, C.USER if y < 2024 else C.ASSISTANT, fmt[v]) for n, y, v, _ in sets],
                        6.0 / (np.log10(2_300_000) - 2), font_size=26, bar_h=0.42, buff=0.32)
        whats = VGroup(*[label(w, font_size=20, color=GREY_A).next_to(r[1], DOWN, buff=0.06).align_to(r[1], LEFT)
                         for r, (_, _, _, w) in zip(rows, sets)])
        chart = VGroup(rows, whats).move_to(UP * 0.9)
        head = label(r"Supervised fine-tuning data: how many examples (log scale)", font_size=32).to_edge(UP, buff=0.35)
        aime = bar_rows([(r"distilled from R1 (fine-tuning only)", 72.6, C.ASSISTANT, r"72.6\%"),
                         (r"RL directly on the same base", 47.0, C.RL_POLICY, r"47.0\%")],
                        5.0 / 100, font_size=24, bar_h=0.36, buff=0.18)
        at = label(r"Qwen2.5-32B base, AIME 2024 (pass@1)", font_size=24).next_to(aime, UP, buff=0.18).align_to(aime, LEFT)
        dist = VGroup(at, aime).to_edge(DOWN, buff=0.75).set_x(0)
        src = source(r"Ouyang et al.\ 2022; Zhou et al.\ 2023; Lambert et al.\ 2024; OLMo 3 (2025); DeepSeek-R1 (2025), Table 6")
        with self.voiceover(
            "Where do the conversations come from? <bookmark mark='a'/> Early on, from people: OpenAI's InstructGPT "
            "used about thirteen thousand demonstrations written by contractors. <bookmark mark='b'/> The LIMA paper "
            "showed that a thousand carefully chosen examples go a long way, because the knowledge is already there "
            "from pretraining. <bookmark mark='c'/> Today most of the data is generated by stronger models and then "
            "filtered: Allen AI's Tülu 3 mix has 939 thousand prompts, <bookmark mark='d'/> and OLMo 3's reasoning "
            "set has 2.3 million, about forty-five billion tokens. <bookmark mark='e'/> This kind of imitation is "
            "powerful. DeepSeek distilled R1's reasoning into a 32-billion-parameter Qwen model with fine-tuning "
            "alone, and it scored 72.6 percent on the AIME 2024 math competition, far above the 47 percent that "
            "reinforcement learning reached directly on the same base."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                r = rows[i]
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), FadeIn(whats[i]), run_time=0.9)
            vo.wait_until("e")
            self.play(FadeIn(at), *[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in aime],
                      run_time=1.2)
        self.wait(0.5)
        self.clear_scene()
