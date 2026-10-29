from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, PART, SEM_C, SND_C, TEXT_C, load, node_box

ME_C = C.TRUE_P


class Omni(VoiceoverScene):
    def construct(self):
        self.card()
        self.cascade()
        self.duplex()
        self.thinker()
        self.budget()

    def card(self):
        card = chapter_card(16, r"Every sense at once", r"Can one model see, listen and talk, all at once?", part=PART)
        with self.voiceover("Chapter sixteen. Every sense at once."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cascade(self):
        boxes = VGroup(node_box(r"speech recognizer", SND_C, font_size=22), node_box(r"language model", TEXT_C, font_size=22),
                       node_box(r"speech synthesizer", C.MODEL_Q, font_size=22)).arrange(RIGHT, buff=0.9).move_to(UP * 1.6)
        arr = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B) for a, b in zip(boxes, boxes[1:])])
        cl = label(r"a cascade: \ each waits for the one before, \ and tone of voice is lost in the text between",
                   font_size=22, color=GREY_A).next_to(boxes, DOWN, buff=0.35)
        one = node_box(r"one network: \ sound, \ pictures and text in; \ sound and text out", WHITE, font_size=24)
        one.move_to(DOWN * 1.2)
        ol = label(r"GPT-4o (OpenAI, May 2024): \ answers speech in as little as $232$ ms, \ $320$ ms on average",
                   font_size=22, color=GREY_A).next_to(one, DOWN, buff=0.3)
        with self.voiceover(
            "The voice assistants of the 2010s were cascades: <bookmark mark='a'/> a recognizer turned your speech "
            "into text, a language model wrote a reply, and a synthesizer read it out. Each stage waits for the one "
            "before, and everything the text can't hold, the tone, the laugh, the hesitation, is lost on the way. "
            "<bookmark mark='b'/> In May 2024 OpenAI's GPT-4o put it all in one network trained end to end on text, "
            "pictures and sound, answering speech in as little as 232 milliseconds, 320 on average, about as fast as "
            "people take turns."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.4), LaggedStart(*[GrowArrow(a_) for a_ in arr],
                                                                                        lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(one), FadeIn(ol))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duplex(self):
        T = 12
        rows = VGroup()
        for name, col, pattern in ((r"you", ME_C, "110000110011"), (r"Moshi's words", TEXT_C, "000110001100"),
                                   (r"Moshi's speech", SND_C, "001110001100")):
            cells = VGroup(*[Rectangle(width=0.62, height=0.45, stroke_color=GREY_D, stroke_width=1, fill_color=col,
                                       fill_opacity=0.75 if p == "1" else 0.08) for p in pattern]).arrange(RIGHT, buff=0.04)
            rows.add(VGroup(label(name, font_size=24, color=col), cells).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.3).move_to(UP * 0.4)
        tl = label(r"time $\to$, \ in frames of $80$ ms", font_size=22, color=GREY_B).next_to(rows, DOWN, buff=0.3)
        head = label(r"full duplex: \ listening and speaking at once", font_size=30).to_edge(UP, buff=0.5)
        facts = VGroup(*[label(t, font_size=20, color=GREY_A) for t in (
            r"Moshi (Kyutai, September 2024): \ a $7$-billion-parameter text model, \ Mimi's tokens for both streams",
            r"the text runs slightly ahead of its speech: \ an inner monologue",
            r"$160$ ms in theory, \ $200$ ms in practice")]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        tag = note(r"schematic", font_size=18).to_corner(DR, buff=0.3)
        cite_ = cite(r"A.~D\'efossez et al., \textit{Moshi} (2024)", corner=UR)
        with self.voiceover(
            "GPT-4o still took turns. Conversation doesn't: people interrupt, overlap and murmur mm-hm while the "
            "other one talks. <bookmark mark='a'/> In September 2024 Kyutai's Moshi modelled two streams of sound at "
            "once, the user's and its own, eighty milliseconds at a time, so it is always listening, even while it "
            "speaks. <bookmark mark='b'/> Alongside its own speech it writes the words it is saying, slightly ahead "
            "of the sound, an inner monologue that keeps the speech on track. Its latency: 160 milliseconds in "
            "theory, about 200 in practice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            fills = [[c_.get_fill_opacity() for c_ in r_[1]] for r_ in rows]
            for r_ in rows:
                r_[1].set_fill(opacity=0.08)
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3), FadeIn(tl))
            cur = Line(rows[0][1][0].get_corner(UL) + UP * 0.15, rows[2][1][0].get_corner(DL) + DOWN * 0.15, color=WHITE,
                       stroke_width=3)
            self.play(Create(cur), run_time=0.3)
            for t in range(T):
                self.play(cur.animate.move_to([rows[0][1][t].get_right()[0], cur.get_y(), 0]),
                          *[r_[1][t].animate.set_fill(opacity=f_[t]) for r_, f_ in zip(rows, fills)], run_time=0.28,
                          rate_func=linear)
            self.play(FadeOut(cur), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def thinker(self):
        def chips(n, col):
            return VGroup(*[Square(0.3, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.25) for _ in range(n)])

        seq = VGroup(chips(4, TEXT_C), chips(6, IMG_C), chips(3, TEXT_C), chips(5, SND_C)).arrange(RIGHT, buff=0.15)
        for g_ in seq:
            g_.arrange(RIGHT, buff=0.04)
        seq.arrange(RIGHT, buff=0.15).move_to([-2.0, -1.0, 0])
        sl = label(r"text, \ picture, \ text, \ sound: \ one sequence, \ positions aligned by time", font_size=20,
                   color=GREY_A).next_to(seq, DOWN, buff=0.2)
        thinker = RoundedRectangle(width=4.2, height=1.1, corner_radius=0.15, stroke_color=WHITE, stroke_width=2.5).move_to([-2.0, 1.0, 0])
        talker = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.15, stroke_color=SND_C, stroke_width=2.5).move_to([3.6, 1.0, 0])
        tl = label(r"the Thinker: \ a language model \\ reading every kind of token", font_size=20, color=WHITE).move_to(thinker)
        kl = label(r"the Talker: \\ writes speech codes", font_size=20, color=SND_C).move_to(talker)
        a1 = Arrow(seq.get_top(), thinker.get_bottom(), buff=0.15, color=GREY_B)
        a2 = Arrow(thinker.get_right(), talker.get_left(), buff=0.1, color=GREY_B)
        a2l = label(r"its words \\ (Qwen2.5-Omni: \ also its \\ hidden states)", font_size=15, color=GREY_B).next_to(a2, UP, buff=0.05)
        wave = FunctionGraph(lambda x: 0.25 * np.sin(9 * x) * np.exp(-0.3 * x * x), x_range=[-1.3, 1.3], color=SND_C)
        wave.next_to(talker, DOWN, buff=0.5)
        facts = VGroup(*[label(t, font_size=19, color=c_) for t, c_ in (
            (r"Qwen2.5-Omni (March 2025): \ Thinker and Talker; \ time-aligned rotary positions", GREY_A),
            (r"Qwen3-Omni (September 2025): \ both mixtures of experts; \ open weights; \\ first sound in $234$ ms "
             r"(theory); \ text in $119$ languages, \ speech in $19$, \ out in $10$", GREY_A),
            (r"Qwen3.5-Omni (April 2026): \ hybrid-attention experts; \ over $10$ hours of audio in one context", GREY_A),
            (r"PersonaPlex (NVIDIA, January 2026): \ full duplex, \ steered by a role and a voice", GREY_A))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_edge(UP, buff=0.25)
        if facts.width > 13.2:
            facts.width = 13.2
        tag = note(r"schematic", font_size=18).to_corner(DL, buff=0.3)
        thinker.shift(DOWN * 0.3)
        tl.shift(DOWN * 0.3)
        talker.shift(DOWN * 0.3)
        kl.shift(DOWN * 0.3)
        with self.voiceover(
            "Alibaba's open omni models split the work in two. <bookmark mark='a'/> A Thinker, a language model, "
            "reads one sequence of text, picture and sound tokens, with rotary positions aligned by time, and writes "
            "text. <bookmark mark='b'/> A smaller Talker writes speech codes as it goes, and a decoder turns them into "
            "sound; in Qwen3-Omni, twelve and a half frames a second through a small convolutional decoder. In "
            "Qwen2.5-Omni the Talker read the "
            "Thinker's hidden states; in Qwen3-Omni it reads only the words and the sound and picture features, so "
            "tools and safety filters can step in on the text before it is spoken. <bookmark mark='c'/> Qwen3-Omni, "
            "in September 2025, made both halves mixtures of experts and released the weights; Qwen3.5-Omni, in "
            "April 2026, holds more than ten hours of audio in one context. And NVIDIA's PersonaPlex, in January "
            "2026, carried full-duplex talk forward with a voice and a role to play."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for g_ in seq for c_ in g_], lag_ratio=0.03), FadeIn(sl),
                      FadeIn(tag), run_time=1.6)
            vo.wait_until("a")
            self.play(GrowArrow(a1), Create(thinker), FadeIn(tl), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a2), FadeIn(a2l), Create(talker), FadeIn(kl))
            self.play(Create(wave))
            vo.wait_until("c")
            self.play(FadeIn(facts[1:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def budget(self):
        w = load("whisper")
        cd = load("codec")
        v = load("vlm")
        nr = load("narrator")
        frame = next(r for r in v["rows"] if int(r["h"]) == 720)
        q_hz, q_n = (float(nr["hz"]), int(nr["n_q"])) if bool(nr["available"]) else (12.5, 16)
        items = [
            (r"the words of speech \ (Whisper's BPE, \ measured)", float(w["tokens_per_second"]), TEXT_C),
            (r"Mimi \ ($12.5 \times 8$)", 12.5 * 8, SEM_C),
            (r"Qwen3-TTS \ ($12.5 \times 16$)", q_hz * q_n, SEM_C),
            (rf"our codec \ (${int(cd['hz'])} \times 8$)", float(int(cd["hz"]) * 8), SND_C),
            (r"EnCodec, \ $6$ kbps \ ($75 \times 8$)", 75.0 * 8, SND_C),
            (r"one $720$p frame \ (Qwen2-VL)", float(frame["tokens"]), IMG_C)]
        lo, hi = 0.0, math.log10(max(v_ for _, v_, _ in items) * 2)
        W = 6.0
        bars = VGroup()
        for i, (nm, val, col) in enumerate(items):
            y = 1.8 - 0.62 * i
            wdt = W * (math.log10(max(val, 1)) - lo) / (hi - lo)
            bar = Rectangle(width=max(wdt, 0.05), height=0.36, stroke_width=0, fill_color=col, fill_opacity=0.6)
            bar.move_to([-1.0 + wdt / 2, y, 0])
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to([-1.15, y, 0], LEFT, buff=0.0), bar,
                            MathTex(f"{val:,.0f}".replace(",", "{,}"), font_size=22, color=col).next_to(bar, RIGHT, buff=0.12)))
        axl = label(r"tokens a second, \ log scale \ (a picture: \ tokens per frame)", font_size=18, color=GREY_B)
        axl.next_to(bars, DOWN, buff=0.3).align_to(bars[0][1], LEFT)
        mimi_min = 12.5 * 8 * 60
        bh = label(r"what each sense costs, \ in tokens", font_size=40).to_edge(UP, buff=0.4)
        with self.voiceover(
            "In the end, every sense is a stream of tokens, and what differs is how many. <bookmark mark='a'/> The "
            f"words of speech come at about {float(w['tokens_per_second']):.0f} tokens a second, by Whisper's own "
            "tokenizer on our voices. <bookmark mark='b'/> The same speech as Mimi's codes is 100 a second, as the "
            f"narrator's tokenizer {q_hz * q_n:.0f}, and a single high-definition frame of video is "
            f"{int(frame['tokens']):,} tokens. <bookmark mark='c'/> A minute of conversation is {mimi_min:,.0f} tokens per "
            "stream at Mimi's rate, so much of the engineering in these models is in spending fewer: lower frame "
            "rates, fewer codebooks, smaller pictures where they will do."
        ) as vo:
            self.play(FadeIn(bh), FadeIn(axl))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.1) for b_ in bars[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(bars[1], scale_factor=1.04))
        self.wait(0.3)
        self.clear_scene()
