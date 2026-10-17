from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import FM_C, gray_image, load


class Glyphs(VoiceoverScene):
    def construct(self):
        self.card()
        self.pictures()
        self.journey()

    def card(self):
        card = chapter_card(5, r"From points to pictures", r"What is an image, to a diffusion model?", part=14)
        with self.voiceover("Chapter five. From points to pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pictures(self):
        g = load("glyphs")
        tr = np.asarray(g["train"])
        n = int(np.asarray(tr).shape[-1])
        grid = Group(*[gray_image(im, 0.62) for im in tr[:32]]).arrange_in_grid(rows=4, cols=8, buff=0.06).move_to([-3.4, -0.3, 0])
        tl = label(rf"training pictures: \ ${int(g['n_train']):,}$ capital letters \\ from ${int(g['n_fonts'])}$ fonts, \ "
                   rf"${n}\times{n}$ pixels".replace(",", "{,}"), font_size=24, color=GREY_A).next_to(grid, UP, buff=0.25)
        pt = label(rf"one picture $=$ a point in ${n * n}$ dimensions", font_size=30, color=FM_C).move_to([3.6, 2.6, 0])
        # one training picture as a grid of pixel squares, which then unrolls into a list of n*n numbers
        im = np.clip(np.asarray(tr[0], float), 0, 1)
        px = 0.1
        sq = VGroup(*[Square(px, stroke_width=0, fill_color=interpolate_color(ManimColor("#000000"), ManimColor(WHITE), float(v)),
                             fill_opacity=1).move_to([3.6 + (c - (n - 1) / 2) * px, 0.9 - (r - (n - 1) / 2) * px, 0])
                      for r, row in enumerate(im) for c, v in enumerate(row)])
        per = 100
        cw = 6.0 / per

        def spot(k):  # where pixel k sits once unrolled: lines of 100 numbers, read like text
            return [3.6 - 3.0 + cw * (k % per + 0.5), -0.6 - 0.24 * (k // per), 0]

        rows = VGroup(*[Rectangle(width=6.0, height=0.2, stroke_color=GREY_C, stroke_width=1).move_to([3.6, -0.6 - 0.24 * k, 0])
                        for k in range(n * n // per)])
        vl = MathTex(rf"x \in \mathbb{{R}}^{{{n * n}}}", font_size=34, color=FM_C).move_to([3.6, -1.75, 0])
        same = label(r"the same flow matching, \\ just in more dimensions", font_size=26, color=GREY_A).move_to([3.6, -2.9, 0])
        with self.voiceover(
            "Points in a plane were a warm-up. A picture is also a point: here, letters from many fonts, twenty by "
            f"twenty pixels. <bookmark mark='a'/> Each picture is a list of {n * n} numbers, one point in a space of "
            f"{n * n} dimensions. <bookmark mark='b'/> The model is exactly the one we trained on the A I points, "
            "flow matching from noise, just with more numbers."
        ) as vo:
            self.play(FadeIn(tl), LaggedStart(*[FadeIn(i_) for i_ in grid], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(pt), FadeIn(sq, lag_ratio=0.002), run_time=1.2)
            self.play(LaggedStart(*[AnimationGroup(*[sq[r * n + c].animate.move_to(spot(r * n + c)).stretch_to_fit_width(cw * 0.92)
                                                     .stretch_to_fit_height(0.17) for c in range(n)]) for r in range(n)],
                                  lag_ratio=0.12), run_time=3.0)
            self.play(Create(rows), FadeIn(vl))
            vo.wait_until("b")
            self.play(FadeIn(same))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def journey(self):
        g = load("glyphs")
        J = np.asarray(g["journey"])
        S = np.asarray(g["samples"])
        near = np.asarray(g["nearest"])
        steps = Group(*[gray_image(im, 1.0) for im in J]).arrange(RIGHT, buff=0.12).move_to(UP * 1.9)
        sl = label(r"one sample, \ from noise to a letter, \ every $5$ steps of $50$", font_size=22, color=GREY_A)
        sl.next_to(steps, UP, buff=0.15)
        grid = Group(*[gray_image(im, 0.6) for im in S[:32]]).arrange_in_grid(rows=4, cols=8, buff=0.06).move_to([-2.0, -1.4, 0])
        gl = label(r"$32$ samples, \ none of them copies", font_size=22, color=FM_C).next_to(grid, DOWN, buff=0.15)
        nn = label(rf"each is ${near.mean():.2f}$ on average \\ from its nearest training picture \\ (pixels from $0$ to $1$)",
                   font_size=22, color=GREY_A).move_to([4.2, -1.2, 0])
        nxt = label(r"real models do this in a compressed space \\ of image patches: \ Part 15", font_size=24, color=C.BITS)
        nxt.next_to(nn, DOWN, buff=0.4)
        with self.voiceover(
            "Here's one picture being born. <bookmark mark='a'/> Static, then a blur, then a shape, then a letter. "
            "<bookmark mark='b'/> And a batch of samples: rough, speckled, but mostly recognizable capitals, in a mix of styles, not copies "
            "of the training pictures. <bookmark mark='c'/> Real image models do the same thing at a million times "
            "the scale, in a compressed space of image patches: that's part fifteen."
        ) as vo:
            self.play(FadeIn(sl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in grid], lag_ratio=0.03), FadeIn(gl), FadeIn(nn), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
