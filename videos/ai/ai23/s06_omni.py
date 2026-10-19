from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, SND_C, TEXT_C


class Omni(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_model()
        self.duplex()

    def card(self):
        card = chapter_card(5, r"One model, every sense", r"Can one model read, see, listen and speak?", part=23)
        with self.voiceover("Chapter five. One model, every sense."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def one_model(self):
        def chips(n, col):
            return VGroup(*[Square(0.32, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.25) for _ in range(n)])

        seq = VGroup(chips(4, TEXT_C), chips(6, IMG_C), chips(3, TEXT_C), chips(5, SND_C)).arrange(RIGHT, buff=0.12)
        for g_ in seq:
            g_.arrange(RIGHT, buff=0.04)
        seq.arrange(RIGHT, buff=0.15).move_to(DOWN * 1.6)
        sl = label(r"one sequence: \ text, \ picture codes, \ text, \ sound codes", font_size=22, color=GREY_A).next_to(seq, DOWN, buff=0.2)
        thinker = RoundedRectangle(width=4.2, height=1.1, corner_radius=0.15, stroke_color=WHITE, stroke_width=2.5).move_to([-2.4, 0.9, 0])
        talker = RoundedRectangle(width=3.0, height=1.1, corner_radius=0.15, stroke_color=SND_C, stroke_width=2.5).move_to([3.4, 0.9, 0])
        tl = label(r"the Thinker: \ a language model \\ reading every kind of token", font_size=22, color=WHITE).move_to(thinker)
        kl = label(r"the Talker: \\ writes sound codes", font_size=22, color=SND_C).move_to(talker)
        a1 = Arrow(seq.get_top(), thinker.get_bottom(), buff=0.15, color=GREY_B)
        a2 = Arrow(thinker.get_right(), talker.get_left(), buff=0.1, color=GREY_B)
        wave = FunctionGraph(lambda x: 0.25 * np.sin(9 * x) * np.exp(-0.3 * x * x), x_range=[-1.4, 1.4], color=SND_C)
        wave.next_to(talker, UP, buff=0.4)
        cite_ = cite(r"Qwen Team, \textit{Qwen2.5-Omni} (2025), \textit{Qwen3-Omni} (2025)", corner=UR)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Once everything is tokens, one model can take them all. <bookmark mark='a'/> Text, picture codes and "
            "sound codes go into one sequence, and one transformer reads them all, part thirteen's attention looking "
            "across senses. <bookmark mark='b'/> To answer out loud, Qwen's omni models add a second, smaller "
            "transformer, the Talker, which turns the first one's thoughts into sound codes, and a decoder turns "
            f"those into a wave. This video's narrator, {narration_credit()}, is a speech model too: text in, "
            "sound out."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for g_ in seq for c_ in g_], lag_ratio=0.03), FadeIn(sl),
                      FadeIn(tag), run_time=1.6)
            vo.wait_until("a")
            self.play(GrowArrow(a1), Create(thinker), FadeIn(tl))
            q_ = seq[3][2]  # a sound token, attending back across the senses
            arcs = VGroup(*[ArcBetweenPoints(q_.get_top(), k_.get_top(), angle=PI / 2.5, stroke_width=1.5 + 3 * w_, color=C.ATTN)
                            .set_stroke(opacity=0.35 + 0.6 * w_)
                            for k_, w_ in ((seq[0][1], 0.5), (seq[1][2], 0.9), (seq[1][4], 0.7), (seq[2][0], 0.4), (seq[3][0], 0.6))])
            self.play(LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.15), run_time=1.2)
            vo.wait_until("b")
            self.play(FadeOut(arcs), GrowArrow(a2), Create(talker), FadeIn(kl), FadeIn(cite_))
            outs = VGroup(*[Square(0.22, stroke_color=SND_C, stroke_width=1.2, fill_color=SND_C, fill_opacity=0.6) for _ in range(6)])
            path = Line(talker.get_top(), wave.get_bottom() + DOWN * 0.05)
            self.play(LaggedStart(*[MoveAlongPath(o_, path) for o_ in outs], lag_ratio=0.25), run_time=1.6)
            self.remove(outs)
            self.play(Create(wave))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def duplex(self):
        T = 12
        rows = VGroup()
        for name, col, pattern in ((r"you", C.TRUE_P, "110000110011"), (r"the model", SND_C, "001110001100")):
            cells = VGroup(*[Rectangle(width=0.6, height=0.45, stroke_color=GREY_D, stroke_width=1, fill_color=col,
                                       fill_opacity=0.75 if p == "1" else 0.08) for p in pattern]).arrange(RIGHT, buff=0.04)
            rows.add(VGroup(label(name, font_size=26, color=col), cells).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.35).move_to(UP * 0.2)
        tl = label(r"time $\to$, \ in frames of sound", font_size=22, color=GREY_B).next_to(rows, DOWN, buff=0.3)
        head = label(r"full duplex: \ listening and speaking at once, \ two streams", font_size=28).to_edge(UP, buff=0.5)
        foot = label(r"it can be interrupted, \ and it can say ``mm-hm'' while you talk", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"A.~D\'efossez et al., \textit{Moshi} (2024)", corner=DR)
        tag = note(r"schematic").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Conversation is harder than speech. People interrupt, overlap and murmur agreement. <bookmark mark='a'/> "
            "Moshi, in 2024, models two streams of sound at once, the user's and its own, every eighty "
            "milliseconds, so it's always listening, even while it talks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            fills = [[c_.get_fill_opacity() for c_ in r_[1]] for r_ in rows]
            for r_ in rows:
                r_[1].set_fill(opacity=0.08)
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.3), FadeIn(tl))
            cur = Line(rows[0][1][0].get_corner(UL) + UP * 0.15, rows[1][1][0].get_corner(DL) + DOWN * 0.15, color=WHITE, stroke_width=3)
            self.play(Create(cur), run_time=0.3)
            for t in range(T):
                self.play(cur.animate.move_to([rows[0][1][t].get_right()[0], cur.get_y(), 0]),
                          *[r_[1][t].animate.set_fill(opacity=f_[t]) for r_, f_ in zip(rows, fills)], run_time=0.28, rate_func=linear)
            self.play(FadeOut(cur), FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
