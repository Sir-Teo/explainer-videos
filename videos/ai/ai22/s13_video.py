from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, PANEL, PART, PATCH, fmt_int, gray_image, load


def causal_conv_picture(cell=0.22) -> VGroup:
    """A causal convolution in time: the 3 x 3 stencil becomes a 3 x 3 x 3 block, reaching over this frame and the two
    before it, never the next."""
    frames = VGroup()
    for f in range(4):
        sq = VGroup(*[Square(cell, stroke_width=0.6, stroke_color=GREY_D, fill_color=PANEL, fill_opacity=1)
                      for _ in range(25)]).arrange_in_grid(5, 5, buff=0)
        frames.add(sq)
    frames.arrange(RIGHT, buff=0.35)
    frames[3].set_opacity(0.3)
    wins = VGroup(*[Square(3 * cell, stroke_color=PATCH, stroke_width=3, fill_color=PATCH, fill_opacity=0.25)
                    .move_to(frames[f][12]) for f in range(3)])
    tie = VGroup(*[DashedLine(wins[f].get_right(), wins[f + 1].get_left(), color=PATCH, stroke_width=2, dash_length=0.05)
                   for f in range(2)])
    names = VGroup(*[MathTex(t, font_size=24, color=PATCH if f < 3 else GREY_C).next_to(frames[f], DOWN, buff=0.1)
                     for f, t in enumerate((r"t-2", r"t-1", r"t", r"t+1"))])
    br = Brace(VGroup(frames[0], frames[2]), UP, buff=0.08, color=PATCH)
    bl = label(r"one $3 \times 3 \times 3$ stencil: \ this frame and two before", font_size=18, color=PATCH).next_to(br, UP, buff=0.06)
    fl = label(r"the future: \\ never seen", font_size=18, color=GREY_C).next_to(frames[3], UP, buff=0.1)
    return VGroup(frames, wins, tie, names, br, bl, fl)


class Video(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.tokens()
        self.causal()
        self.rope3d()

    def card(self):
        card = chapter_card(12, r"Squeezing time", r"How do you make video into tokens?", part=PART)
        with self.voiceover("Chapter twelve. Squeezing time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"Video generation, \ 2024--2026", font_size=36).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(r"Feb 2024", r"Sora \ (OpenAI)", r"a diffusion transformer on spacetime patches, \ trained on "
                         r"videos and images", color=HIST, width=4.4, font_size=26),
            history_card(r"Oct 2024", r"Movie Gen \ (Meta)", r"$30$ billion weights for video, \ $13$ billion for sound",
                         color=HIST, width=4.4, font_size=26),
            history_card(r"Dec 2024 -- Feb 2025", r"HunyuanVideo; \ Wan 2.1", r"open weights: \ $13$ billion; \ $14$ "
                         r"and $1.3$ billion", color=HIST, width=4.4, font_size=26),
            history_card(r"May -- Sep 2025", r"Veo 3; \ Sora 2", r"video and its sound, \ generated together", color=HIST,
                         width=4.4, font_size=26),
            history_card(r"Jul -- Nov 2025", r"Wan 2.2; \ HunyuanVideo 1.5", r"open: \ a mixture of two experts; \ "
                         r"$8.3$ billion weights on one consumer GPU", color=HIST, width=4.4, font_size=26),
            history_card(r"Jan 2026", r"LTX-2 \ (Lightricks)", r"open: \ $14$ billion weights for video, \ $5$ billion "
                         r"for sound, \ in one model", color=HIST, width=4.4, font_size=26),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.22, 0.4), cell_alignment=UP)
        if cards.width > 13.4:
            cards.width = 13.4
        cards.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Video is pictures in time. In February 2024 OpenAI's Sora showed what a diffusion transformer could do "
            "with it: minute-long clips, trained on videos and images alike. <bookmark mark='a'/> Meta's Movie Gen "
            "followed, with thirty billion weights. <bookmark mark='b'/> Then open weights: Tencent's HunyuanVideo and "
            "Alibaba's Wan. <bookmark mark='c'/> In 2025 Google's Veo 3 and OpenAI's Sora 2 generated the sound "
            "with the picture. <bookmark mark='d'/> The open models kept pace, small enough for one consumer GPU, "
            "<bookmark mark='e'/> and in January 2026 Lightricks released LTX-2, sound and picture in one open model. "
            "All of them rest on the same three pieces: squeeze time, position tokens in three dimensions, and "
            "denoise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tokens(self):
        v = load("video")
        rows = v["rows"]
        frames = VGroup(*[Rectangle(width=2.0, height=1.13, stroke_color=GREY_B, stroke_width=1.5, fill_color=PANEL,
                                    fill_opacity=1).shift(RIGHT * 0.22 * i + UP * 0.16 * i) for i in range(8)])
        frames.move_to([-4.0, 0.8, 0])
        clip = np.asarray(load("vae3d")["orig"])[0]
        shots = Group(*[gray_image(clip[i], 1.0).move_to(f_) for i, f_ in zip(range(len(frames)), frames)])
        sheets = Group(*[Group(f_, im) for f_, im in zip(frames, shots)])
        cap0 = label(rf"a clip: \ ${len(frames)}$ frames", font_size=22, color=GREY_A).next_to(frames, DOWN, buff=0.35)
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
                           MathTex(fmt_int(r["tokens"]) + r"\ \text{tokens}", font_size=30, color=PATCH)).arrange(RIGHT, buff=0.4))
        tab.arrange(DOWN, aligned_edge=RIGHT, buff=0.25).move_to([3.6, -1.6, 0])
        t720 = next(r for r in rows if r["res"] == "720p" and r["sec"] == 5)
        tag = note(r"a typical compression, \ for illustration; \ at $16$ frames a second").to_corner(DL, buff=0.3)
        with self.voiceover(
            "First the squeeze. As with pictures, an autoencoder compresses the video, now in time as well as space, "
            "and a token is a little block of both. <bookmark mark='a'/> With a typical squeeze, five seconds of "
            f"720p at sixteen frames a second is about {round(t720['tokens'], -3):,.0f} tokens."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(sh_) for sh_ in sheets], lag_ratio=0.15), FadeIn(cap0), FadeIn(comp), FadeIn(tag),
                      run_time=1.6)
            two = VGroup(*[f_.copy() for f_ in frames[:2]]).move_to(frames)
            s1 = label(r"$4\times$ fewer in time", font_size=22, color=GREY_A).next_to(frames, DOWN, buff=0.35)
            self.play(FadeOut(shots), Transform(frames, two), ReplacementTransform(cap0, s1), run_time=1.0)
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
            self.play(TransformFromCopy(grid, line), FadeIn(cube), FadeIn(cl), run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.2) for r_ in tab], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def causal(self):
        d = load("vae3d")
        orig, rec = np.asarray(d["orig"])[0], np.asarray(d["rec"])[0]
        Cc = int(d["C"])
        lat = [int(x) for x in d["latent_shape"]]  # channels, latent frames, rows, columns
        S = 1.05
        top = Group(*[gray_image(f_, S) for f_ in orig]).arrange(RIGHT, buff=0.12).move_to([0, 2.3, 0])
        bot = Group(*[gray_image(f_, S) for f_ in rec]).arrange(RIGHT, buff=0.12).move_to([0, -1.9, 0])
        tl = label(r"$9$ frames of a letter bouncing \ (a held-out font)", font_size=20, color=GREY_A).next_to(top, UP, buff=0.12)
        bl = label(r"rebuilt from the latent", font_size=20, color=GREY_A).next_to(bot, DOWN, buff=0.12)
        groups = [(0, 0), (1, 4), (5, 8)]
        braces = VGroup(*[Brace(Group(*top[a:b + 1]), DOWN, buff=0.08, color=PATCH) for a, b in groups])

        def stack(cx):
            g = VGroup()
            for c in range(Cc):
                g.add(Square(0.75, stroke_color=PATCH, stroke_width=1.5, fill_color=PANEL, fill_opacity=1)
                      .move_to([cx + 0.1 * c, 0.15 + 0.08 * c, 0]))
            return g

        lats = VGroup(*[stack(b_.get_center()[0] - 0.15) for b_ in braces])
        ll = VGroup(*[MathTex(rf"z_{k}", font_size=26, color=PATCH).next_to(l_, LEFT, buff=0.12) for k, l_ in enumerate(lats)])
        down = VGroup(*[Arrow(l_.get_bottom(), [l_.get_center()[0], -1.25, 0], buff=0.08, stroke_width=2.5, color=GREY_B,
                              max_tip_length_to_length_ratio=0.2) for l_ in lats])
        size = label(rf"each: \ ${lat[0]}$ channels $\times\,{lat[2]} \times {lat[3]}$", font_size=20, color=PATCH)
        size.next_to(lats[2], RIGHT, buff=0.3)
        rule = label(r"latent frame $k$ sees \\ only frames up to $4k$", font_size=20, color=GREY_A).next_to(size, DOWN, buff=0.25).align_to(size, LEFT)
        ratio = int(d["pixels"]) / int(d["numbers"])
        num = label(rf"${fmt_int(d['pixels'])}$ pixels $\to$ ${int(d['numbers'])}$ numbers \ (${ratio:.0f}\times$); \ "
                    rf"rebuild error ${float(d['rmse']):.3f}$; \ a still picture alone: \ ${float(d['still_rmse']):.3f}$",
                    font_size=22, color=PATCH).to_edge(DOWN, buff=0.2)
        cite_ = cite(r"MAGVIT-v2 (2023), \ CogVideoX, \ Wan (2024--25): \ causal 3D autoencoders", corner=UL)
        cc = gloss(r"a convolution in time", r"the sliding stencil becomes a small cube \\ through the frames, "
                   r"looking only backward", causal_conv_picture(), width=6.4, color=PATCH).move_to([0, 0.15, 0])
        with self.voiceover(
            "The squeeze comes from a video autoencoder, whose convolutions run in time as well as space. "
            "<bookmark mark='v'/> The little stencil a convolution slides over a picture becomes a small cube, "
            "sliding through the frames too, and looking only backward. <bookmark mark='a'/> We trained a small one "
            "on clips of a bouncing letter. The first frame is squeezed on its own; <bookmark mark='b'/> after that, "
            "every four frames become one latent frame, which sees only frames up to its own: causal, like a language "
            "model. <bookmark mark='c'/> That pays twice. A clip can be encoded as it streams in, and a still picture "
            "is just a one-frame video, so a video model can train on images too. Images are plentiful and teach "
            "appearance; videos teach motion; most video models train on both. <bookmark mark='d'/> Here "
            f"{int(d['pixels']):,} pixels become {int(d['numbers'])} numbers, {ratio:.0f} times fewer, with a "
            f"rebuild error of {float(d['rmse']):.3f}; a still picture alone comes back at {float(d['still_rmse']):.3f}."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tl), FadeIn(cite_))
            vo.wait_until("v")
            self.play(FadeIn(cc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(cc))
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
        cube = VGroup()
        nf, nh, nw, u = 3, 4, 5, 0.42
        q = (0, 2, 3)
        for f in reversed(range(nf)):  # back frames first, so the front one is drawn on top
            for h in range(nh):
                for w in range(nw):
                    on = (f, h, w) == q
                    sq = Square(u * 0.9, stroke_color=C.BITS if on else PATCH, stroke_width=2.5 if on else 1.2,
                                fill_color=C.BITS if on else PANEL, fill_opacity=0.95)
                    sq.set_stroke(opacity=1.0 if on else 0.9 - 0.25 * f)
                    cube.add(sq.move_to([w * u + f * 0.8, -h * u + f * 0.62, 0]))
        cube.move_to([-3.8, 0.4, 0])
        qi = ((nf - 1 - q[0]) * nh + q[1]) * nw + q[2]
        o = cube.get_corner(DL) + DL * 0.3
        axes_ = VGroup(Arrow(o, o + RIGHT * 1.2, buff=0, stroke_width=2.5, color=C.TRUE_P, max_tip_length_to_length_ratio=0.2),
                       Arrow(o, o + UP * 1.0, buff=0, stroke_width=2.5, color=C.INTERVAL, max_tip_length_to_length_ratio=0.2),
                       Arrow(o, o + np.array([0.7, 0.5, 0]), buff=0, stroke_width=2.5, color=C.SURPRISE,
                             max_tip_length_to_length_ratio=0.2))
        al = VGroup(MathTex(r"w", font_size=24, color=C.TRUE_P).next_to(axes_[0].get_end(), RIGHT, buff=0.05),
                    MathTex(r"h", font_size=24, color=C.INTERVAL).next_to(axes_[1].get_end(), UP, buff=0.05),
                    MathTex(r"f", font_size=24, color=C.SURPRISE).next_to(axes_[2].get_end(), UR, buff=0.02))
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
        cost = label(rf"$5$ s of 720p: \ ${fmt_int(n5)}$ tokens, \ ${n5 * n5 / 1e9:.1f}$ billion pairs; \ "
                     rf"$10$ s: \ ${n10 * n10 / n5 / n5:.1f}\times$ the pairs", font_size=22, color=PATCH).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"J.~Su et al., \textit{RoFormer} (2021), \ extended to three axes in video models", corner=UR)
        with self.voiceover(
            "A token now has three coordinates: which frame, which row, which column. Part 13's rotary positions "
            "extend naturally. <bookmark mark='a'/> Split each head's pairs of numbers three ways: some are turned by "
            "the frame number, some by the row, some by the column, each group with its own frequencies. "
            "<bookmark mark='b'/> Since each group is a rotation, the score between two tokens depends only on how "
            "far apart they are in time, height and width, exactly as in one dimension. <bookmark mark='c'/> What "
            f"doesn't extend gracefully is the cost: {round(n5, -3):,.0f} tokens means {n5 * n5 / 1e9:.1f} billion "
            "pairs for attention, in every layer, at every denoising step. Double the length and the pairs "
            "quadruple. That's why video models lean on every trick from Parts 15 and 16."
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
