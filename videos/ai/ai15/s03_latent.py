from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.squeeze()
        self.space()
        self.diffuse()

    def card(self):
        card = chapter_card(2, r"A smaller space", r"Why denoise every pixel?", part=15)
        with self.voiceover("Chapter two. A smaller space."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def squeeze(self):
        d = load("latent")
        Z, n = int(d["Z"]), np.asarray(d["orig"]).shape[-1]
        orig, rec = np.asarray(d["orig"]), np.asarray(d["rec"])
        enc = Polygon([-1.2, 1.0, 0], [1.2, 0.4, 0], [1.2, -0.4, 0], [-1.2, -1.0, 0], stroke_color=PATCH, stroke_width=2.5,
                      fill_color=PATCH, fill_opacity=0.12).move_to([-1.6, 0.6, 0])
        dec = Polygon([-1.2, 0.4, 0], [1.2, 1.0, 0], [1.2, -1.0, 0], [-1.2, -0.4, 0], stroke_color=PATCH, stroke_width=2.5,
                      fill_color=PATCH, fill_opacity=0.12).move_to([2.6, 0.6, 0])
        el = label(r"encoder", font_size=22, color=PATCH).move_to(enc)
        dl = label(r"decoder", font_size=22, color=PATCH).move_to(dec)
        zc = VGroup(*[Square(0.18, stroke_width=0.6, stroke_color=GREY_D, fill_color=C.EMBED, fill_opacity=0.7) for _ in range(Z)])
        zc.arrange(DOWN, buff=0).scale_to_fit_height(1.6).move_to([0.5, 0.6, 0])
        zl = label(rf"${Z}$ numbers", font_size=22, color=C.EMBED).next_to(zc, DOWN, buff=0.15)
        a_in = gray_image(orig[0], 1.6).move_to([-4.6, 0.6, 0])
        a_out = gray_image(rec[0], 1.6).move_to([5.4, 0.6, 0])
        il = label(rf"${n * n}$ pixels", font_size=22, color=GREY_A).next_to(a_in, DOWN, buff=0.15)
        ol = label(r"rebuilt", font_size=22, color=GREY_A).next_to(a_out, DOWN, buff=0.15)
        pairs = Group(*[Group(gray_image(o, 0.6), gray_image(r, 0.6)).arrange(DOWN, buff=0.05) for o, r in zip(orig[:10], rec[:10])])
        pairs.arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.5)
        pl = label(r"top: \ the pictures; \ bottom: \ rebuilt from $16$ numbers", font_size=20, color=GREY_A).next_to(pairs, UP, buff=0.1)
        cite_ = cite(r"R.~Rombach et al., \textit{Latent Diffusion Models} (2022)", corner=UR)
        with self.voiceover(
            f"Real pictures have millions of pixels, and most of that detail is predictable. So first, train an "
            f"autoencoder: an encoder squeezes each picture into a few numbers, here {Z} instead of {n * n}, and a "
            "decoder rebuilds the picture from them. <bookmark mark='a'/> The rebuilt letters are close to the "
            f"originals: {n * n // Z} times fewer numbers, little lost."
        ) as vo:
            self.play(FadeIn(a_in), FadeIn(il), FadeIn(enc), FadeIn(el), FadeIn(zc), FadeIn(zl), FadeIn(dec), FadeIn(dl),
                      FadeIn(a_out), FadeIn(ol), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.1), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def space(self):
        d = load("latent")
        Q, N = np.asarray(d["nn_query"]), np.asarray(d["nn_imgs"])
        ql, nl = [int(x) for x in d["nn_qlabels"]], np.asarray(d["nn_labels"])
        same, chance = float(d["nn_same"]), float(d["nn_chance"])
        S = 0.8
        rows = Group()
        for q, ns, lq, lns in zip(Q, N, ql, nl):
            qi = gray_image(q, S)
            box = SurroundingRectangle(qi, color=C.BITS, buff=0.03, stroke_width=2.5)
            arrow = MathTex(r"\rightarrow", font_size=36, color=GREY_B)
            nbrs = Group(*[Group(gray_image(n_, S), SurroundingRectangle(gray_image(n_, S), buff=0.03, stroke_width=2,
                                                                         color=C.INTERVAL if int(l_) == lq else C.SURPRISE))
                           for n_, l_ in zip(ns, lns)]).arrange(RIGHT, buff=0.12)
            rows.add(Group(Group(qi, box), arrow, nbrs).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-1.0, -0.4, 0])
        head = label(r"each picture, \ and the $6$ pictures nearest to it in the $16$ numbers", font_size=24, color=GREY_A)
        head.to_edge(UP, buff=0.4)
        key = VGroup(label(r"green: \ the same letter", font_size=22, color=C.INTERVAL),
                     label(r"red: \ a different one", font_size=22, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.move_to([5.2, 1.2, 0])
        res = label(rf"over all the pictures: \\ ${100 * same:.0f}\%$ of neighbours \\ are the same letter \\ "
                    rf"(by chance: \ ${100 * chance:.0f}\%$)", font_size=24, color=C.INTERVAL).next_to(key, DOWN, buff=0.5)
        res.align_to(key, LEFT)
        good = same > 5 * chance
        with self.voiceover(
            "And the space of those few numbers has structure. <bookmark mark='a'/> Take a picture, and find the "
            "pictures whose sixteen numbers are closest to its own. "
            + (f"<bookmark mark='b'/> Mostly, they're the same letter, in other fonts: {100 * same:.0f} percent of the "
               f"time, against {100 * chance:.0f} by chance. "
               if good else
               f"<bookmark mark='b'/> Often they're the same letter, {100 * same:.0f} percent of the time against "
               f"{100 * chance:.0f} by chance, but just as often only something of a similar shape. ")
            + "Denoising in this space is cheaper, and each step is about shapes, not pixels."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[1]), LaggedStart(*[FadeIn(n_, shift=RIGHT * 0.1) for n_ in r_[2]],
                                                                              lag_ratio=0.1)) for r_ in rows], lag_ratio=0.25),
                      FadeIn(key), run_time=2.5)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diffuse(self):
        d = load("latent")
        S = np.asarray(d["samples"])
        grid = Group(*[gray_image(im, 0.7) for im in S[:24]]).arrange_in_grid(rows=3, cols=8, buff=0.08).move_to(DOWN * 0.3)
        head = label(r"Part 14's flow matching, \ run on the $16$ numbers, \ then decoded", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.5)
        foot = label(r"Stable Diffusion, \ Flux, \ and every video model work this way", font_size=26, color=PATCH).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Now run part fourteen's flow matching on those {int(d['Z'])} numbers instead of the pixels, and decode the "
            f"result. <bookmark mark='a'/> Letters again, with {int(d['ratio'])} times fewer numbers to "
            "denoise. That's latent diffusion, and it's how Stable Diffusion, Flux and every video model work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in grid], lag_ratio=0.04), FadeIn(foot), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
