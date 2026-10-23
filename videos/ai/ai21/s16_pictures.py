from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import FM_C, HIST, PART, glyph_sheet, gray_image, load


class Pictures(VoiceoverScene):
    def construct(self):
        self.card()
        self.pixels()
        self.replay()
        self.samples()
        self.systems()

    def card(self):
        card = chapter_card(15, r"From points to pictures", r"What is an image, to a diffusion model?", part=PART)
        with self.voiceover("Chapter fifteen. From points to pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def pixels(self):
        g = load("glyphs")
        tr = np.asarray(g["train"])
        n = int(tr.shape[-1])
        grid = glyph_sheet(tr[:32], 4, 8, size=0.62, gap=0.06).move_to([-3.4, -0.3, 0])
        tl = label(rf"training pictures: \ ${int(g['n_train']):,}$ capital letters \\ from ${int(g['n_fonts'])}$ fonts, \ "
                   rf"${n}\times{n}$ pixels".replace(",", "{,}"), font_size=24, color=GREY_A).next_to(grid, UP, buff=0.25)
        pt = label(rf"one picture $=$ a point in ${n * n}$ dimensions", font_size=30, color=FM_C).move_to([3.6, 2.6, 0])
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
            "Points in a plane were a warm-up. A picture is also a point: here, capital letters from many fonts, "
            f"{n} by {n} pixels. <bookmark mark='a'/> Each picture is a list of {n * n} numbers, one point in a space "
            f"of {n * n} dimensions. <bookmark mark='b'/> The model is the flow matching we trained on the letters "
            "A and I, with more numbers in and out."
        ) as vo:
            self.play(FadeIn(tl), FadeIn(grid), run_time=1.5)
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
    def replay(self):
        g = load("glyphs")
        snaps = np.asarray(g["snaps"])
        checks = [int(c) for c in g["checks"]]
        L = np.asarray(g["curve"])
        sheets = [glyph_sheet(s_, 2, 8, size=0.66, gap=0.06).move_to([-2.4, 1.3, 0]) for s_ in snaps]
        cl = [label(rf"after ${c:,}$ training steps".replace(",", "{,}"), font_size=24, color=FM_C).next_to(sheets[0], UP, buff=0.15)
              for c in checks]
        top = float(np.percentile(L[:, 1], 99)) * 1.05
        ax = axes([0, checks[-1]], [0, top], x_length=4.0, y_length=2.0, xlabel=r"training step", ylabel=r"the loss",
                  xticks=[0, checks[-1]], yticks=[0, round(top, 2)], center=[4.6, 1.2, 0], font_size=18)
        J = np.asarray(g["journey"])
        steps = Group(*[gray_image(im, 0.95) for im in J]).arrange(RIGHT, buff=0.1).move_to([0, -2.2, 0])
        sl = label(rf"one sample, \ from noise to a letter: \ every $5$ steps of $50$", font_size=22, color=GREY_A).next_to(steps, UP, buff=0.15)
        with self.voiceover(
            "Here it is learning: sixteen pictures from the same noise at each checkpoint. <bookmark mark='a'/> At "
            "first, static. <bookmark mark='b'/> Then grey blobs where letters tend to be, <bookmark mark='c'/> then "
            "shapes, and finally letters. <bookmark mark='d'/> And here is one picture being born: static, then a "
            "blur, then a shape, then a letter."
        ) as vo:
            self.play(FadeIn(sheets[0]), FadeIn(cl[0]), FadeIn(ax))
            vo.wait_until("a")
            marks = {1: "b", 3: "c"}
            for k in range(1, len(sheets)):
                if k in marks:
                    vo.wait_until(marks[k])
                seg = [ax.ax.c2p(a, b) for a, b in L if checks[k - 1] <= a <= checks[k]]
                an = [FadeOut(sheets[k - 1]), FadeIn(sheets[k]), ReplacementTransform(cl[k - 1], cl[k])]
                if len(seg) > 1:
                    an.append(Create(VMobject(color=FM_C, stroke_width=3).set_points_as_corners(seg)))
                self.play(*an, run_time=0.9)
            vo.wait_until("d")
            self.play(FadeIn(sl), LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.3), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def samples(self):
        g = load("glyphs")
        S = np.asarray(g["samples"])
        near = np.asarray(g["nearest"])
        tn = float(g["train_nearest"])
        grid = glyph_sheet(S[:32], 4, 8, size=0.6, gap=0.06).move_to([-2.4, -0.2, 0])
        gl = label(r"$32$ samples", font_size=22, color=FM_C).next_to(grid, UP, buff=0.15)
        far = near.mean() > 1.3 * tn
        nn = VGroup(label(rf"each sample's distance to its nearest training picture: \ ${near.mean():.2f}$ on average",
                          font_size=20, color=GREY_A),
                    label(rf"a training picture's distance to its nearest other: \ ${tn:.2f}$", font_size=20, color=GREY_A),
                    label(r"(root mean square, \ pixels from $0$ to $1$)", font_size=18, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -0.3, 0])
        if nn.width > 6.0:
            nn.width = 6.0
        verdict = ("further from the training set than the training pictures are from each other: these are new "
                   "pictures, not copies." if far else
                   "about as close to the training set as the training pictures are to each other: some may be near "
                   "copies.")
        with self.voiceover(
            "A batch of samples: rough, speckled, mostly recognizable capitals in a mix of styles. "
            "<bookmark mark='a'/> Are they copies? Each sample is, on average, "
            f"{near.mean():.2f} from its nearest training picture; a training picture is {tn:.2f} from its nearest "
            f"neighbour. So the samples are {verdict}"
        ) as vo:
            self.play(FadeIn(grid), FadeIn(gl))
            vo.wait_until("a")
            self.play(FadeIn(nn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def systems(self):
        enc = VGroup(
            label(r"$512 \times 512 \times 3$ pixels", font_size=22, color=GREY_A),
            MathTex(r"\xrightarrow{\ \text{encoder}\ }", font_size=30, color=GREY_B),
            label(r"$64 \times 64 \times 4$ latents", font_size=22, color=FM_C),
            MathTex(r"\xrightarrow{\ \text{diffusion here}\ }", font_size=30, color=FM_C),
            label(r"decoder \ $\to$ \ picture", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.5)
        if enc.width > 13.2:
            enc.width = 13.2
        ratio = 512 * 512 * 3 // (64 * 64 * 4)
        el = label(rf"${ratio}$ times fewer numbers; \ text steers it through cross-attention \ (Rombach et al., 2022)",
                   font_size=20, color=GREY_A).next_to(enc, DOWN, buff=0.15)
        cards = VGroup(
            history_card(2022, r"DALL$\cdot$E 2; \ Imagen; \ Stable Diffusion", r"text to image: \ CLIP latents, \ cascades "
                         r"in pixels, \ latent diffusion with open weights", color=HIST, width=6.4, font_size=18),
            history_card(2023, r"Peebles \& Xie: \ DiT; \ SDXL", r"a transformer as the denoiser; \ bigger latent models",
                         color=HIST, width=6.4, font_size=18),
            history_card(2024, r"Sora; \ SD3; \ FLUX.1; \ Movie Gen", r"diffusion transformers on spacetime patches; \ "
                         r"flow-matching transformers at $12$ to $30$ billion parameters", color=HIST, width=6.4, font_size=18),
            history_card(2025, r"Veo 3; \ Wan 2.1", r"latent diffusion over video and sound together; \ open video "
                         r"weights", color=HIST, width=6.4, font_size=18),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.25)).next_to(el, DOWN, buff=0.35)
        if cards.width > 13.2:
            cards.width = 13.2
        nxt = label(r"the encoders, \ the transformers, \ video: \ Part 22", font_size=24, color=C.BITS).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Real images have millions of numbers, and denoising every one of them is expensive. In 2022 Robin "
            "Rombach, Patrick Esser, Bjorn Ommer and colleagues ran diffusion in a compressed space instead: an "
            "autoencoder turns a picture into a small grid of latents, the diffusion model works there, and a "
            f"decoder turns the result back into pixels, {ratio} times fewer numbers, with text steering through "
            "cross-attention. <bookmark mark='a'/> Released with open weights that August, it became Stable "
            "Diffusion, the same year as OpenAI's DALL-E 2 and Google's Imagen. <bookmark mark='b'/> Then William "
            "Peebles and Saining Xie replaced the denoiser's convolutions with a transformer, <bookmark mark='c'/> "
            "and by 2024 diffusion and flow transformers were drawing video, OpenAI's Sora, and pictures at twelve "
            "billion parameters. <bookmark mark='d'/> By 2025 Google's Veo 3 generated video and its sound together, "
            "by latent diffusion. <bookmark mark='e'/> The encoders, the transformers and the video models are "
            "the next part."
        ) as vo:
            self.play(FadeIn(enc), FadeIn(el))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cards[3], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
