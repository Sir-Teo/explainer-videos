from __future__ import annotations

import math


from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import load


class Scoreboard(VoiceoverScene):
    def construct(self):
        self.card()
        self.fill()
        self.reading()
        self.ahead()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(11, r"The scoreboard", r"How far has guessing come?", lit=(1948, 1951), part=1)
        with self.voiceover("Chapter eleven. Time to keep score.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def fill(self):
        sb = load("scoreboard")
        raw = load("raw")
        rows = sb["rows"]
        keys = [r["key"] for r in rows]
        assert keys == ["ascii", "uniform", "order0", "order1", "gzip", "xz", "bzip2", "best", "GPT-2 small",
                        "GPT-2 XL", "Qwen3-0.6B", "Qwen3-4B", "human"]
        bits = {r["key"]: r.get("bits") for r in rows}
        assert raw["passage_symbols"] == 61 and abs(bits["uniform"] - math.log2(61)) < 1e-9
        assert abs(bits["Qwen3-4B"] - 0.867) < 0.001 and abs(bits["GPT-2 small"] - 1.166) < 0.001
        head = label(r"Bits per character on the Falcon passage, as printed", font_size=32).to_edge(UP, buff=0.25)
        sub = note(rf"${sb['chars']:,}$ characters: \ capitals, punctuation and line breaks included".replace(",", "{,}"),
                   font_size=22).next_to(head, DOWN, buff=0.12)

        def board(shown):
            return scoreboard(rows, shown=shown, row_h=0.405, font_size=21).move_to(DOWN * 0.3)

        b = board(1)
        legend = VGroup(*[VGroup(Square(0.18, stroke_width=0, fill_color=col, fill_opacity=0.9),
                                 label(t, font_size=20, color=col)).arrange(RIGHT, buff=0.12)
                          for t, col in ((r"counting", C.COUNTING), (r"compressors", C.COMPRESSOR),
                                         (r"neural models", C.NEURAL), (r"people", C.HUMAN))])
        legend.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(head), FadeIn(sub), FadeIn(b), FadeIn(legend))
        state = {"b": b, "n": 1}

        def reveal(upto, run_time=1.0):
            nb = board(upto)
            anims = []
            for i in range(state["n"], upto):
                anims += [ReplacementTransform(state["b"].rows[i], nb.rows[i])]
            self.play(*anims, run_time=run_time)
            self.remove(state["b"])
            self.add(nb)
            state["b"], state["n"] = nb, upto

        with self.voiceover(
            "Here's the board, for the Falcon passage as printed: capitals, punctuation, everything. "
            "<bookmark mark='a'/> A plain text file spends eight bits on every character. <bookmark mark='b'/> The "
            "passage uses only sixty-one different symbols, so guessing blindly among them costs log two of "
            "sixty-one: 5.93 bits. <bookmark mark='c'/> Letter frequencies, counted in our thirty books, bring it to "
            "4.55, <bookmark mark='d'/> and one character of context, to 3.58."
        ) as vo:
            vo.wait_until("a")
            self.play(Indicate(b.rows[0], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            reveal(2)
            vo.wait_until("c")
            reveal(3)
            vo.wait_until("d")
            reveal(4)
        with self.voiceover(
            "Next, the compressors on your computer. <bookmark mark='a'/> gzip, 3.31 bits per character; xz, 3.20; "
            "bzip2, 2.92. They know nothing about English in advance. They learn only from the passage itself, as "
            "they go. <bookmark mark='b'/> Our best counting model, which read the thirty books first and looks at "
            "the previous four characters, gets 2.32."
        ) as vo:
            vo.wait_until("a")
            reveal(7, run_time=1.5)
            vo.wait_until("b")
            reveal(8)
        with self.voiceover(
            "And then, the neural language models. <bookmark mark='a'/> GPT-2, the smallest version, from 2019: "
            "1.17 bits. Its largest version, 1.01. <bookmark mark='b'/> Qwen3, from 2025: the 0.6 billion parameter "
            "model already matches the largest GPT-2, <bookmark mark='c'/> and four billion parameters bring it to "
            "0.87 bits per character. <bookmark mark='d'/> For comparison, Shannon's estimate for people, on letters "
            "alone, was 0.6 to 1.3."
        ) as vo:
            vo.wait_until("a")
            reveal(10, run_time=1.5)
            vo.wait_until("b")
            reveal(11)
            vo.wait_until("c")
            reveal(12)
            vo.wait_until("d")
            reveal(13)
        self.b = state["b"]
        self.head, self.sub, self.legend = head, sub, legend
        self.bits = bits

    # ------------------------------------------------------------------
    def reading(self):
        sb = load("scoreboard")
        bits, n = self.bits, int(sb["chars"])
        kb = {k: bits[k] * n / 8 / 1000 for k in ("ascii", "gzip", "Qwen3-4B")}
        assert abs(kb["ascii"] - 21.4) < 0.05 and abs(kb["gzip"] - 8.9) < 0.05 and abs(kb["Qwen3-4B"] - 2.3) < 0.05
        side = VGroup(
            label(r"as files:", font_size=24, color=GREY_A),
            label(rf"plain text: \ ${kb['ascii']:.1f}$ KB", font_size=24, color=GREY_B),
            label(rf"gzip: \ ${kb['gzip']:.1f}$ KB", font_size=24, color=C.COMPRESSOR),
            label(rf"Qwen3-4B $+$ arithmetic coding: \ ${kb['Qwen3-4B']:.1f}$ KB", font_size=24, color=C.NEURAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.9, -1.75, 0])
        gap = Brace(VGroup(self.b.rows[7].bar, self.b.rows[11].bar), RIGHT, color=C.BITS)
        gap.next_to(VGroup(self.b.rows[7], self.b.rows[11]), RIGHT, buff=0.1)
        gap_l = label(r"this gap \\ is the series", font_size=24, color=C.BITS).next_to(gap, RIGHT, buff=0.15)
        with self.voiceover(
            "In file sizes: the passage is 21.4 kilobytes as plain text, 8.9 with gzip, <bookmark mark='a'/> and 2.3 "
            "with Qwen3 driving an arithmetic coder. <bookmark mark='b'/> The jump from counting, at 2.3 bits, to "
            "under one, is what this series is about: what these models learned, and how."
        ) as vo:
            self.play(FadeIn(side[:3]))
            vo.wait_until("a")
            self.play(FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeOut(side), GrowFromCenter(gap), FadeIn(gap_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ahead(self):
        sb = load("scoreboard")
        rows = [r for r in sb["rows"] if r["key"] in ("best", "GPT-2 small", "Qwen3-4B")]
        future = [
            dict(label=r"Kneser--Ney counting (Part 6)", kind="count"),
            dict(label=r"a neural network over $n$ characters (Part 8)", kind="lm"),
            dict(label=r"our own small transformer (Part 11)", kind="lm"),
        ]
        filled = scoreboard(rows[:1] + future + rows[1:], row_h=0.5, font_size=24).move_to(DOWN * 0.2)
        head = label(r"Rows still to fill, with models we will build", font_size=32).to_edge(UP, buff=0.5)
        with self.voiceover(
            "And the board isn't finished. As the series goes on, we'll build our own models and add their rows: "
            "<bookmark mark='a'/> better counting in part six, <bookmark mark='b'/> a neural network in part eight, "
            "<bookmark mark='c'/> and our own small transformer in part eleven, each one trained on these same thirty "
            "books, and scored on this same page."
        ) as vo:
            self.play(FadeIn(head), FadeIn(filled.axis), FadeIn(filled.rows[0]), FadeIn(filled.rows[4]),
                      FadeIn(filled.rows[5]))
            for k, mark in zip((1, 2, 3), "abc"):
                vo.wait_until(mark)
                self.play(FadeIn(filled.rows[k]))
        self.wait(0.5)
        self.clear_scene()
