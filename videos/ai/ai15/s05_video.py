from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import PATCH, gray_image, load


class Video(VoiceoverScene):
    def construct(self):
        self.card()
        self.tokens()
        self.causal()
        self.rope3d()

    def card(self):
        card = chapter_card(6, r"Squeezing time", r"How many tokens is a clip?", part=15)
        with self.voiceover("Chapter six. Squeezing time."):
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
    def causal(self):
        d = load("vae3d")
        orig, rec = np.asarray(d["orig"])[0], np.asarray(d["rec"])[0]
        T, Cc = int(d["T"]), int(d["C"])
        lat = [int(x) for x in d["latent_shape"]]  # channels, latent frames, rows, columns
        S = 1.05
        top = Group(*[gray_image(f_, S) for f_ in orig]).arrange(RIGHT, buff=0.12).move_to([0, 2.3, 0])
        bot = Group(*[gray_image(f_, S) for f_ in rec]).arrange(RIGHT, buff=0.12).move_to([0, -1.9, 0])
        tl = label(r"$9$ frames: \ a letter bouncing", font_size=20, color=GREY_A).next_to(top, UP, buff=0.12)
        bl = label(r"rebuilt from the latent", font_size=20, color=GREY_A).next_to(bot, DOWN, buff=0.12)
        groups = [(0, 0), (1, 4), (5, 8)]
        braces = VGroup(*[Brace(Group(*top[a:b + 1]), DOWN, buff=0.08, color=PATCH) for a, b in groups])

        def stack(cx):
            g = VGroup()
            for c in range(Cc):
                g.add(Square(0.75, stroke_color=PATCH, stroke_width=1.5, fill_color="#121722", fill_opacity=1)
                      .move_to([cx + 0.1 * c, 0.15 + 0.08 * c, 0]))
            return g

        lats = VGroup(*[stack(b_.get_center()[0] - 0.15) for b_ in braces])
        ll = VGroup(*[MathTex(rf"z_{k}", font_size=26, color=PATCH).next_to(l_, LEFT, buff=0.12) for k, l_ in enumerate(lats)])
        down = VGroup(*[Arrow(l_.get_bottom(), [l_.get_center()[0], -1.25, 0], buff=0.08, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.2) for l_ in lats])
        size = label(rf"each: \ ${lat[0]}$ channels $\times\,{lat[2]} \times {lat[3]}$", font_size=20, color=PATCH)
        size.next_to(lats[2], RIGHT, buff=0.3)
        rule = label(r"latent frame $k$ sees \\ only frames up to $4k$: \\ the first alone, \ then four at a time",
                     font_size=20, color=GREY_A).next_to(size, DOWN, buff=0.25).align_to(size, LEFT)
        ratio = int(d["pixels"]) / int(d["numbers"])
        num = label(rf"${int(d['pixels']):,}$ pixels $\to$ ${int(d['numbers'])}$ numbers \ (${ratio:.0f}\times$); \ "
                    rf"rebuild error ${float(d['rmse']):.3f}$".replace(",", "{,}"), font_size=22, color=PATCH).to_edge(DOWN, buff=0.2)
        cite_ = cite(r"e.g.\ Wan~2.1, \ HunyuanVideo, \ Cosmos (2024--25): \ causal 3D autoencoders", corner=UL)
        with self.voiceover(
            "Where does that squeeze come from? A video autoencoder, with convolutions that run in time as well as "
            "space. We trained a small one on clips of a bouncing letter. <bookmark mark='a'/> The first frame is "
            "squeezed on its own; <bookmark mark='b'/> after that, every four frames become one latent frame, and "
            "each is only allowed to see frames up to its own. It's causal, like a language model. "
            "<bookmark mark='c'/> That has two payoffs: a single picture is just a one-frame video, so the same model "
            "handles both, and a clip can be encoded as it streams in. <bookmark mark='d'/> "
            f"Here, {int(d['pixels']):,} pixels become {int(d['numbers'])} numbers, {ratio:.0f} times fewer. Real "
            "video models squeeze four times in time and eight in each direction of space, the same recipe."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(GrowFromCenter(braces[0]), FadeIn(lats[0]), FadeIn(ll[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(braces[1]), FadeIn(lats[1]), FadeIn(ll[1]), GrowFromCenter(braces[2]), FadeIn(lats[2]),
                      FadeIn(ll[2]), FadeIn(size))
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in down], lag_ratio=0.2), FadeIn(bot), FadeIn(bl))
            vo.wait_until("d")
            self.play(FadeIn(num))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rope3d(self):
        v = load("video")
        rows = v["rows"]
        t720 = next(r for r in rows if r["res"] == "720p" and r["sec"] == 5)
        t10 = next(r for r in rows if r["res"] == "720p" and r["sec"] == 10)
        # a little block of tokens: frames x rows x columns
        cube = VGroup()
        nf, nh, nw, u = 3, 4, 5, 0.42
        q = (0, 2, 3)  # the query token, in the front frame
        for f in reversed(range(nf)):  # back frames first, so the front one is drawn on top
            for h in range(nh):
                for w in range(nw):
                    on = (f, h, w) == q
                    sq = Square(u * 0.9, stroke_color=C.BITS if on else PATCH, stroke_width=2.5 if on else 1.2,
                                fill_color=C.BITS if on else "#121722", fill_opacity=0.95)
                    sq.set_stroke(opacity=1.0 if on else 0.9 - 0.25 * f)
                    cube.add(sq.move_to([w * u + f * 0.8, -h * u + f * 0.62, 0]))
        cube.move_to([-3.8, 0.4, 0])
        qi = ((nf - 1 - q[0]) * nh + q[1]) * nw + q[2]  # the cube was drawn back to front
        axes_ = VGroup(Arrow(cube.get_corner(DL) + DL * 0.3, cube.get_corner(DL) + DL * 0.3 + RIGHT * 1.2, buff=0, stroke_width=2.5,
                             color=C.TRUE_P, max_tip_length_to_length_ratio=0.2),
                       Arrow(cube.get_corner(DL) + DL * 0.3, cube.get_corner(DL) + DL * 0.3 + UP * 1.0, buff=0, stroke_width=2.5,
                             color=C.INTERVAL, max_tip_length_to_length_ratio=0.2),
                       Arrow(cube.get_corner(DL) + DL * 0.3, cube.get_corner(DL) + DL * 0.3 + np.array([0.7, 0.5, 0]), buff=0,
                             stroke_width=2.5, color=C.SURPRISE, max_tip_length_to_length_ratio=0.2))
        al = VGroup(MathTex(r"w", font_size=24, color=C.TRUE_P).next_to(axes_[0].get_end(), RIGHT, buff=0.05),
                    MathTex(r"h", font_size=24, color=C.INTERVAL).next_to(axes_[1].get_end(), UP, buff=0.05),
                    MathTex(r"f", font_size=24, color=C.SURPRISE).next_to(axes_[2].get_end(), UR, buff=0.02))
        # the head's numbers, in pairs, split three ways
        segs = VGroup(*[Rectangle(width=wd, height=0.36, stroke_width=1, stroke_color=GREY_D, fill_color=c_, fill_opacity=0.7)
                        for wd, c_ in ((1.2, C.SURPRISE), (2.0, C.INTERVAL), (2.0, C.TRUE_P))]).arrange(RIGHT, buff=0)
        segs.move_to([2.9, 2.2, 0])
        sl = VGroup(*[label(t_, font_size=18, color=c_).next_to(s_, UP, buff=0.08)
                      for t_, c_, s_ in ((r"pairs turned by $f$", C.SURPRISE, segs[0]), (r"by $h$", C.INTERVAL, segs[1]),
                                         (r"by $w$", C.TRUE_P, segs[2]))])
        hl = label(r"one head's query, \ in pairs of numbers", font_size=20, color=GREY_A).next_to(segs, DOWN, buff=0.12)
        f = MathTex(r"R(f, h, w) = R_{f\,\theta^{(f)}} \oplus R_{h\,\theta^{(h)}} \oplus R_{w\,\theta^{(w)}}", font_size=32).move_to([2.9, 0.6, 0])
        f2 = MathTex(r"\big(R(p)\,q\big)^{\top}\big(R(p')\,k\big) = q^{\top} R(p' - p)\, k", font_size=32).next_to(f, DOWN, buff=0.35)
        f2l = label(r"scores depend only on the offset \ $(\Delta f, \Delta h, \Delta w)$", font_size=20, color=GREY_A).next_to(f2, DOWN, buff=0.12)
        n5, n10 = int(t720["tokens"]), int(t10["tokens"])
        cost = label(rf"$5$ s of 720p: \ ${n5:,}$ tokens, \ ${n5 * n5 / 1e9:.1f}$ billion pairs; \ "
                     rf"$10$ s: \ ${n10 * n10 / n5 / n5:.1f}\times$ the pairs".replace(",", "{,}"), font_size=22, color=PATCH)
        cost.to_edge(DOWN, buff=0.4)
        cite_ = cite(r"J.~Su et al., \textit{RoFormer} (2021), \ extended to three axes in video models", corner=UR)
        with self.voiceover(
            "A token now has three coordinates: which frame, which row, which column. Part eleven's rotary positions "
            "extend naturally. <bookmark mark='a'/> Split each head's pairs of numbers three ways: some are turned by "
            "the frame number, some by the row, some by the column, each group with its own frequencies. "
            "<bookmark mark='b'/> Since each group is a rotation, the score between two tokens depends only on how "
            "far apart they are in time, height and width, exactly as in one dimension. <bookmark mark='c'/> What "
            "doesn't extend gracefully is the cost. "
            f"Five seconds of 720p is about {round(n5, -3):,.0f} tokens, and attention compares every pair: "
            f"{n5 * n5 / 1e9:.1f} billion of them, in every layer, at every denoising step. Double the length and the "
            "pairs quadruple. That's why video models lean on every trick from parts twelve and thirteen."
        ) as vo:
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(c_) for c_ in cube], lag_ratio=0.005), run_time=1.5)
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in axes_], lag_ratio=0.2), FadeIn(al), Indicate(cube[qi], color=C.BITS))
            vo.wait_until("a")
            self.play(FadeIn(segs), FadeIn(sl), FadeIn(hl))
            self.play(Write(f))
            vo.wait_until("b")
            self.play(Write(f2), FadeIn(f2l))
            vo.wait_until("c")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()
