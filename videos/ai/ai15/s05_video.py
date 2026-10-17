from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import PATCH, gray_image, load


class Video(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokens()
        self.scales()

    def card(self):
        card = chapter_card(4, r"Video, and other orders", r"How many tokens is a clip?", part=15)
        with self.voiceover("Chapter four. Video, and other orders."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tokens(self):
        v = load("video")
        rows = v["rows"]
        fps = int(v["fps"])
        frames = VGroup(*[Rectangle(width=2.0, height=1.13, stroke_color=GREY_B, stroke_width=1.5, fill_color="#121722",
                                    fill_opacity=1).shift(RIGHT * 0.22 * i + UP * 0.16 * i) for i in range(8)])
        frames.move_to([-4.0, 0.8, 0])
        cube = VGroup(*[Rectangle(width=0.5, height=0.5, stroke_color=PATCH, stroke_width=2, fill_color=PATCH, fill_opacity=0.2)
                        .shift(RIGHT * 0.1 * i + UP * 0.08 * i) for i in range(3)]).move_to([4.6, 0.9, 0])
        cl = label(r"a token: \ a little block \\ of space and time", font_size=22, color=PATCH).next_to(cube, DOWN, buff=0.2)
        comp = label(r"compressed $8\times$ in each direction of space, \ $4\times$ in time, \ then $2\times2$ patches",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.35)
        tab = VGroup()
        for r in rows:
            if r["sec"] != 5:
                continue
            tab.add(VGroup(label(rf"5 seconds, \ {r['res']}", font_size=24, color=WHITE),
                           MathTex(f"{r['tokens']:,}".replace(",", "{,}") + r"\ \text{tokens}", font_size=30, color=PATCH))
                    .arrange(RIGHT, buff=0.4))
        tab.arrange(DOWN, aligned_edge=RIGHT, buff=0.25).move_to([3.6, -1.6, 0])
        t720 = next(r for r in rows if r["res"] == "720p" and r["sec"] == 5)
        tag = note(r"a typical compression, \ for illustration; \ at $16$ frames a second").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Video is pictures in time. The autoencoder now squeezes time as well as space, and a token is a little "
            "block of both. <bookmark mark='a'/> With a typical squeeze, five seconds of 720p video at sixteen frames "
            f"a second is about {round(t720['tokens'], -3):,.0f} tokens, and attention between every pair of them "
            "is part twelve's cost problem all over again. That's why video models need every trick from parts twelve "
            "and thirteen."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(f_) for f_ in frames], lag_ratio=0.1), FadeIn(comp), FadeIn(tag))
            # the squeeze, step by step: 4x fewer frames, 8x smaller each way, then cut into blocks
            two = VGroup(*[f_.copy() for f_ in frames[:2]]).move_to(frames)
            s1 = label(r"$4\times$ fewer in time", font_size=22, color=GREY_A).next_to(frames, DOWN, buff=0.35)
            self.play(Transform(frames, two), FadeIn(s1), run_time=1.0)
            small = frames.copy().scale(0.45).move_to(frames)
            s2 = label(r"$8\times$ smaller each way", font_size=22, color=GREY_A).next_to(small, DOWN, buff=0.35)
            self.play(Transform(frames, small), ReplacementTransform(s1, s2), run_time=1.0)
            grid = VGroup()
            for layer in range(2):
                for r_ in range(3):
                    for c_ in range(4):
                        grid.add(Square(0.2, stroke_color=PATCH, stroke_width=1.2, fill_color=PATCH, fill_opacity=0.25)
                                 .move_to(frames[layer].get_center() + np.array([(c_ - 1.5) * 0.22, (1 - r_) * 0.22, 0])))
            s3 = label(r"cut into blocks: \ tokens", font_size=22, color=PATCH).move_to(s2)
            self.play(FadeIn(grid, lag_ratio=0.03), ReplacementTransform(s2, s3), run_time=1.0)
            line = grid.copy().arrange(RIGHT, buff=0.05).move_to([0.6, 0.8, 0])
            self.play(TransformFromCopy(grid, line), run_time=1.2)
            self.play(FadeIn(cube), FadeIn(cl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.2) for r_ in tab], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scales(self):
        s = load("scales")
        pyr = np.asarray(s["pyramid"])
        sizes = [int(x) for x in s["sizes"]]
        pics = Group(*[gray_image(p, 1.5) for p in pyr]).arrange(RIGHT, buff=0.35).move_to(UP * 0.3)
        lab = VGroup(*[MathTex(rf"{k}\times{k}", font_size=24, color=PATCH).next_to(p, DOWN, buff=0.15) for k, p in zip(sizes, pics)])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(pics, pics[1:])])
        head = label(r"next-scale prediction: \ first a rough picture, \ then ever finer detail", font_size=28)
        head.to_edge(UP, buff=0.5)
        foot = label(r"each scale's tokens are predicted all at once, \ from the coarser ones", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.8)
        cite_ = cite(r"K.~Tian et al., \textit{Visual Autoregressive Modeling} (2024)", corner=DR)
        with self.voiceover(
            "There's another way to make pictures token by token, without diffusion. Instead of left to right, go "
            "coarse to fine: <bookmark mark='a'/> one token for the whole picture, then two by two, four by four, "
            "and so on, each scale predicted all at once from the ones before. It's how a painter works, and it "
            "won the NeurIPS best paper award in 2024."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_))
            vo.wait_until("a")
            for i, p in enumerate(pics):
                self.play(FadeIn(p), FadeIn(lab[i]), *([GrowArrow(arrows[i - 1])] if i > 0 else []), run_time=0.6)
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
