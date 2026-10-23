from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import MONO, PART, load


class Scoreboard(VoiceoverScene):
    def construct(self):
        self.card()
        self.fill()
        self.reading()
        self.lmzip()
        self.model_size()
        self.ahead()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(15, r"The scoreboard: language modeling is compression", r"How far has guessing come?",
                            lit=(1948, 1951, 2019), part=PART)
        with self.voiceover("Chapter fifteen. Time to keep score."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fill(self):
        sb = load("scoreboard")
        raw = load("raw")
        rows = sb["rows"]
        keys = [r["key"] for r in rows]
        b = {r["key"]: r.get("bits") for r in rows}
        hum = next(r for r in rows if r["key"] == "human")
        head = label(r"Bits per character on the Falcon passage, as printed", font_size=32).to_edge(UP, buff=0.25)
        sub = note(rf"${sb['chars']:,}$ characters: \ capitals, punctuation and line breaks included".replace(",", "{,}"),
                   font_size=22).next_to(head, DOWN, buff=0.12)

        def board(shown):
            return scoreboard(rows, shown=shown, row_h=0.405, font_size=21).move_to(DOWN * 0.3)

        bd = board(1)
        legend = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=col, fill_opacity=0.9),
                                 label(t, font_size=20, color=col)).arrange(RIGHT, buff=0.12)
                          for t, col in ((r"counting", C.COUNTING), (r"compressors", C.COMPRESSOR),
                                         (r"neural models", C.NEURAL), (r"people", C.HUMAN))])
        legend.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(head), FadeIn(sub), FadeIn(bd), FadeIn(legend))
        state = {"b": bd, "n": 1}

        def reveal(key, run_time=1.0):
            upto = keys.index(key) + 1
            nb = board(upto)
            self.play(*[ReplacementTransform(state["b"].rows[i], nb.rows[i]) for i in range(state["n"], upto)],
                      run_time=run_time)
            self.remove(state["b"])
            self.add(nb)
            state["b"], state["n"] = nb, upto

        k = int(raw["best"])
        comp = sorted(("gzip", "xz", "bzip2"), key=lambda c: -b[c])
        comp_said = ", ".join(f"{c}, {b[c]:.2f}" for c in comp)
        q06, gxl = b["Qwen3-0.6B"], b["GPT-2 XL"]
        q06_said = ("already matches the largest GPT-2" if abs(q06 - gxl) < 0.02 else
                    ("already beats the largest GPT-2" if q06 < gxl else f"gets {q06:.2f} bits per character"))
        with self.voiceover(
            "Here's the board, for the Falcon passage as printed: capitals, punctuation, everything. "
            "<bookmark mark='a'/> Plain text spends eight bits per character. <bookmark mark='b'/> The passage uses "
            f"only {raw['passage_symbols']} different symbols, so a blind guess among them costs "
            f"{b['uniform']:.2f} bits. <bookmark mark='c'/> Letter frequencies, "
            f"counted in our thirty books, bring it to {b['order0']:.2f}, <bookmark mark='d'/> and one character of "
            f"context, to {b['order1']:.2f}."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(bd.rows[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            reveal("uniform")
            vo.wait_until("c")
            reveal("order0")
            vo.wait_until("d")
            reveal("order1")
        with self.voiceover(
            f"Next, the compressors on your computer. <bookmark mark='a'/> {comp_said}. They know nothing about "
            "English in advance, and learn only from the passage, as they go. <bookmark mark='b'/> Our best counting "
            f"model, which read the thirty books first and looks at the previous {k} characters, gets "
            f"{b['best']:.2f}."
        ) as vo:
            vo.wait_until("a")
            reveal("bzip2", run_time=1.5)
            vo.wait_until("b")
            reveal("best")
        with self.voiceover(
            "And then, the neural language models. <bookmark mark='a'/> GPT-2, the smallest version, from 2019: "
            f"{b['GPT-2 small']:.2f} bits. Its largest version, {gxl:.2f}. <bookmark mark='b'/> Qwen3, from 2025: the "
            f"0.6 billion parameter model {q06_said}, <bookmark mark='c'/> and four billion parameters bring it to "
            f"{b['Qwen3-4B']:.2f} bits per character. <bookmark mark='d'/> For comparison, Shannon's estimate for "
            f"people, on letters alone, was {hum['lo']:.1f} to {hum['hi']:.1f}."
        ) as vo:
            vo.wait_until("a")
            reveal("GPT-2 XL", run_time=1.5)
            vo.wait_until("b")
            reveal("Qwen3-0.6B")
            vo.wait_until("c")
            reveal("Qwen3-4B")
            vo.wait_until("d")
            reveal("human")
        self.b = state["b"]
        self.bits = b
        self.keys = keys

    # ------------------------------------------------------------------
    def reading(self):
        sb = load("scoreboard")
        bits, n = self.bits, int(sb["chars"])
        ib, iq = self.keys.index("best"), self.keys.index("Qwen3-4B")
        gap = Brace(VGroup(self.b.rows[ib].bar, self.b.rows[iq].bar), RIGHT, color=C.BITS)
        gap.next_to(VGroup(self.b.rows[ib], self.b.rows[iq]), RIGHT, buff=0.1)
        gap_l = label(r"this gap \\ is the series", font_size=24, color=C.BITS).next_to(gap, RIGHT, buff=0.15)
        low = bits["Qwen3-4B"]
        low_said = "under one" if low < 1 else f"{low:.2f}"
        with self.voiceover(
            f"The jump from counting, at {bits['best']:.1f} bits, to {low_said}, is what this series is about: what "
            "these models learned, and how."
        ):
            self.play(GrowFromCenter(gap), FadeIn(gap_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lmzip(self):
        z = load("lmzip")
        nb = int(math.ceil(z["bits"] / 8))
        comp = {k: int(v) for k, v in z["compressors"].items()}
        head = label(r"We built one: \ GPT-2 as a compressor", font_size=36).to_edge(UP, buff=0.3)
        # the pipeline
        def box(t, col, w=2.3):
            r = RoundedRectangle(width=w, height=0.8, corner_radius=0.12, stroke_color=col, stroke_width=2.5)
            return VGroup(r, label(t, font_size=22, color=col).move_to(r))

        stages = VGroup(box(r"text", C.TOKEN, 1.4), box(r"GPT-2 small", C.NEURAL), box(r"arithmetic \\ coder", C.INTERVAL),
                        box(rf"${nb}$ bytes", C.BITS, 1.7), box(r"decoder \\ $+$ GPT-2", C.INTERVAL),
                        box(r"text", C.TOKEN, 1.4))
        stages.arrange(RIGHT, buff=0.42).move_to(UP * 1.6)
        if stages.width > 13.4:
            stages.scale_to_fit_width(13.4)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=GREY_B, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(stages, stages[1:])])
        probs = label(r"probabilities", font_size=18, color=GREY_B).next_to(arrows[1], UP, buff=0.05)
        # sizes, as bars
        items = [(r"plain text", z["bytes"], GREY_B), (r"gzip", comp["gzip"], C.COMPRESSOR),
                 (r"bzip2", comp["bzip2"], C.COMPRESSOR), (r"xz", comp["xz"], C.COMPRESSOR),
                 (r"GPT-2 small $+$ our coder", nb, C.NEURAL)]
        top = max(v for _, v, _ in items)
        bars = VGroup()
        for i, (name, v, col) in enumerate(items):
            y = -0.4 - 0.55 * i
            nm = label(name, font_size=22, color=col).move_to([-2.4, y, 0], aligned_edge=RIGHT)
            w = 6.0 * v / top
            r = Rectangle(width=w, height=0.34, stroke_width=0, fill_color=col, fill_opacity=0.85)
            r.move_to([-2.2 + w / 2, y, 0])
            t = MathTex(f"{v:,}".replace(",", "{,}") + r"\ \text{bytes}", font_size=24, color=col).next_to(r, RIGHT, buff=0.15)
            bars.add(VGroup(nm, r, t))
        cap = note(rf"the first ${z['chars']:,}$ characters of the passage (${z['tokens']:,}$ tokens: one full GPT-2 "
                   r"window); \ computed".replace(",", "{,}")).to_edge(DOWN, buff=0.25)
        ok_said = ("and decoded it back, with a second run of the model, letter for letter." if z["ok"] else
                   "but decoding it back with a second run of the model did not reproduce it exactly: the two runs "
                   "disagreed somewhere in the last digits of a probability.")
        ratio = comp["xz"] / nb
        with self.voiceover(
            "Arithmetic coding turns any predictor into a compressor, so we built one. <bookmark mark='a'/> GPT-2 "
            "small reads the start of the Falcon passage a token at a time, feeding chapter eight's 32-bit coder. Out come {nb} bytes, {z['bits'] - z['ideal']:.1f} bits more than "
            f"GPT-2's own surprise, <bookmark mark='b'/> {ok_said} <bookmark mark='c'/> On the same "
            f"{z['chars']:,} characters, xz needs {comp['xz']:,} bytes: {ratio:.1f} times as many."
        ) as vo:
            self.play(FadeIn(head), FadeIn(stages[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(s_)) for a, s_ in zip(arrows[:3], stages[1:4])],
                                  lag_ratio=0.6), FadeIn(probs), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(s_)) for a, s_ in zip(arrows[3:], stages[4:])],
                                  lag_ratio=0.6), run_time=1.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.25), FadeIn(cap), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def model_size(self):
        c = load("compress")
        plain = int(c["plain"])
        adj = c["adjusted"]
        size_g2 = c["sizes"]["GPT-2 small"]
        mb = c["model_bytes"]["GPT-2 small"] / 1e6
        head = label(r"The catch: \ the decompressor needs the model", font_size=34).to_edge(UP, buff=0.3)
        ours = VGroup(
            label(rf"the whole passage with GPT-2 small: \ ${size_g2 / 1000:.1f}$ KB", font_size=26, color=C.NEURAL),
            label(rf"plus GPT-2 small itself, \ $2$ bytes a parameter: \ ${mb:,.0f}$ MB".replace(",", "{,}"), font_size=26,
                  color=GREY_A),
            label(rf"together: \ ${adj['GPT-2 small']:,.0f}$ times the passage".replace(",", "{,}"), font_size=26,
                  color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        tab_h = label(r"$1$ GB of Wikipedia (enwik9): \ compressed size, \ share of the original", font_size=24,
                      color=GREY_B)
        rows = [(r"gzip", r"32.3\%", C.COMPRESSOR), (r"LZMA2 \ (xz)", r"23.0\%", C.COMPRESSOR),
                (r"Chinchilla 70B $+$ arithmetic coding", r"8.3\%", C.NEURAL),
                (r"\ldots counting its $140$ GB of weights", r"14{,}008\%", C.SURPRISE)]
        tab = VGroup(*[VGroup(label(n_, font_size=24, color=col), label(rf"${v}$", font_size=26, color=col))
                       for n_, v, col in rows])
        for r in tab:
            r[1].move_to([4.2, 0, 0], aligned_edge=RIGHT)
            r[0].move_to([-3.4, 0, 0], aligned_edge=LEFT)
        tab.arrange(DOWN, buff=0.18)
        for r in tab:
            r[0].set_x(-3.4 + r[0].width / 2)
            r[1].set_x(4.2 - r[1].width / 2)
        blk = VGroup(tab_h, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0.4, -1.1, 0])
        src = cite(r"G.~Del\'etang et al., \textit{Language Modeling Is Compression} (ICLR 2024), Table 1; \ "
                   r"hutter1.net (record of 24 July 2026)")
        hut = label(r"Hutter Prize record, \ July 2026: \ enwik9 in $100.4$ MB, \ decompressor included: \ "
                    r"$0.80$ bits per character", font_size=22, color=C.BITS).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "There's a catch: the decompressor needs the model, and the model is big. <bookmark mark='a'/> GPT-2 "
            f"small squeezes the whole passage into {size_g2 / 1000:.1f} kilobytes, but its weights take "
            f"{mb:,.0f} megabytes: count them, and the file is {adj['GPT-2 small']:,.0f} times the passage. "
            "<bookmark mark='b'/> In 2024, a DeepMind paper titled Language Modeling Is Compression put a "
            "70-billion-parameter model on a gigabyte of Wikipedia: 8.3 percent of the original size, against 32 "
            "for gzip and 23 for xz; fourteen thousand percent, counting its weights. Trained on text, it also beat "
            "PNG and FLAC on images and audio. <bookmark mark='c'/> The Hutter Prize, started in 2006, counts "
            "everything: the record, set in July 2026, packs that gigabyte, decompressor included, into 100.4 "
            "megabytes, 0.80 bits per character, mixing many predictors. <bookmark mark='d'/> Prediction is "
            "compression, and the predictor's size is part of the bill."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in ours], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(tab_h), LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.4), FadeIn(src), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(hut))
            vo.wait_until("d")
            self.play(Indicate(tab[3], color=C.SURPRISE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ahead(self):
        sb = load("scoreboard")
        rows = [r for r in sb["rows"] if r["key"] in ("best", "GPT-2 small", "Qwen3-4B")]
        future = [
            dict(label=r"Kneser--Ney counting (Part 7)", kind="count"),
            dict(label=r"a neural network over $n$ characters (Part 9)", kind="lm"),
            dict(label=r"a character LSTM (Part 10)", kind="lm"),
            dict(label=r"our own small transformer (Part 13)", kind="lm"),
        ]
        filled = scoreboard(rows[:1] + future + rows[1:], row_h=0.5, font_size=24).move_to(DOWN * 0.2)
        head = label(r"Rows still to fill, with models we will build", font_size=32).to_edge(UP, buff=0.5)
        with self.voiceover(
            "And the board isn't finished. We'll build our own models and add their rows: <bookmark mark='a'/> "
            "better counting in Part 7, <bookmark mark='b'/> a neural network in Part 9, <bookmark mark='c'/> a "
            "network with memory in Part 10, <bookmark mark='d'/> and our own small transformer in Part 13, each "
            "trained on these thirty books, and scored on this page."
        ) as vo:
            self.play(FadeIn(head), FadeIn(filled.axis), FadeIn(filled.rows[0]), FadeIn(filled.rows[5]),
                      FadeIn(filled.rows[6]))
            for k, mark in zip((1, 2, 3, 4), "abcd"):
                vo.wait_until(mark)
                self.play(FadeIn(filled.rows[k]))
        self.wait(0.5)
        self.clear_scene()
