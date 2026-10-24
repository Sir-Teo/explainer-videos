from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (CFG_C, HIST, PART, PATCH, fmt_int, glyph_sheet, gray_image, load, mean_band, patch_grid,
                                   take_away)

UNET_C, DIT_C = CFG_C["unet"], CFG_C["zero"]


def unet_picture() -> VGroup:
    """A U-Net: the picture shrinks through convolutions (left), grows back (right); skips carry detail across."""
    sizes = [(1.5, 20, 24), (1.0, 10, 48), (0.6, 5, 64)]
    down, up_ = VGroup(), VGroup()
    for k, (h, px, ch) in enumerate(sizes):
        w = 0.25 + 0.12 * k
        down.add(Rectangle(width=w, height=h, stroke_color=UNET_C, stroke_width=2, fill_color=UNET_C, fill_opacity=0.2)
                 .move_to([-2.2 + 0.9 * k, 1.0 - 1.0 * k, 0]))
        if k < 2:
            up_.add(Rectangle(width=w, height=h, stroke_color=UNET_C, stroke_width=2, fill_color=UNET_C, fill_opacity=0.2)
                    .move_to([2.2 - 0.9 * k, 1.0 - 1.0 * k, 0]))
    mid = down[2]
    arrows = VGroup(
        Arrow(down[0].get_bottom(), down[1].get_top(), buff=0.06, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.2),
        Arrow(down[1].get_bottom(), mid.get_left() + UP * 0.1, buff=0.06, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.2),
        Arrow(mid.get_right() + UP * 0.1, up_[1].get_bottom(), buff=0.06, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.2),
        Arrow(up_[1].get_top(), up_[0].get_bottom(), buff=0.06, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.2))
    skips = VGroup(*[DashedLine(down[k].get_right() + RIGHT * 0.1, up_[k].get_left() + LEFT * 0.1, color=PATCH,
                                stroke_width=2.5, dash_length=0.08).add_tip(tip_length=0.15) for k in range(2)])
    names = VGroup(*[MathTex(rf"{px}\!\times\!{px}", font_size=20, color=GREY_A).next_to(down[k], LEFT, buff=0.12)
                     for k, (_, px, _) in enumerate(sizes)])
    sk = label(r"skips: \ fine detail \ carried across", font_size=18, color=PATCH).next_to(skips[0], UP, buff=0.08)
    at = label(r"attention \ at $5 \times 5$", font_size=18, color=C.ATTN).next_to(mid, DOWN, buff=0.12)
    return VGroup(down, up_, arrows, skips, names, sk, at)


class UNet(VoiceoverScene):
    def construct(self):
        self.card()
        self.unet()
        self.dit()
        self.experiment()

    def card(self):
        card = chapter_card(5, r"U-Net or transformer", r"What should do the denoising?", lit=(2015,), part=PART)
        with self.voiceover("Chapter five. U-Net or transformer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def unet(self):
        pic = unet_picture().scale(1.15).move_to([-2.6, 0.6, 0])
        cards = VGroup(
            history_card(2015, r"Ronneberger, Fischer \& Brox", r"the U-Net, \ for outlining cells in microscope images",
                         color=HIST, width=5.2, font_size=20),
            history_card(2021, r"Dhariwal \& Nichol \ (ADM)", r"a bigger U-Net with attention, \ the time fed through "
                         r"its normalizations: \ diffusion beats GANs", color=HIST, width=5.2, font_size=20),
            history_card(2022, r"Stable Diffusion", r"a U-Net in the latent space, \ text through cross-attention",
                         color=HIST, width=5.2, font_size=20),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.0, 0.2, 0])
        with self.voiceover(
            "Who does the denoising? For the first diffusion models, a U-Net. Olaf Ronneberger and colleagues "
            "designed it in 2015 to outline cells in microscope pictures. <bookmark mark='a'/> Convolutions shrink "
            "the picture step by step, so each unit sees more of it; <bookmark mark='b'/> then the network grows it "
            "back, <bookmark mark='c'/> and skip connections carry the fine detail straight across the U, so it "
            "needn't survive the bottleneck. <bookmark mark='d'/> DDPM used one; in 2021 Prafulla Dhariwal and Alex "
            "Nichol enlarged it, with attention at low resolution and the noise level fed through every "
            "normalization, and diffusion beat GANs. Stable Diffusion's denoiser was a U-Net too."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(pic[0][0]), FadeIn(pic[4][0]))
            vo.wait_until("a")
            self.play(GrowArrow(pic[2][0]), FadeIn(pic[0][1]), FadeIn(pic[4][1]), GrowArrow(pic[2][1]), FadeIn(pic[0][2]),
                      FadeIn(pic[4][2]), FadeIn(pic[6]))
            vo.wait_until("b")
            self.play(GrowArrow(pic[2][2]), FadeIn(pic[1][1]), GrowArrow(pic[2][3]), FadeIn(pic[1][0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(s_) for s_ in pic[3]], lag_ratio=0.3), FadeIn(pic[5]))
            vo.wait_until("d")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dit(self):
        d = load("denoisers")
        path = np.asarray(load("showcase")["alphabet_path"])
        half = path[len(path) // 2][0]
        k = 4
        noisy = gray_image(half, 1.7).move_to([-5.4, -1.5, 0])
        ngrid = patch_grid(noisy, half.shape[0] // k, stroke_width=1)
        toks = Group(*[Group(gray_image(half[r * k:(r + 1) * k, c * k:(c + 1) * k], 0.34), Square(0.34, stroke_color=PATCH,
                                                                                                   stroke_width=1.2))
                       for r in range(5) for c in range(5)][:10]).arrange(RIGHT, buff=0.08).move_to([-1.4, -1.5, 0])
        more = MathTex(r"\cdots", font_size=28, color=PATCH).next_to(toks, RIGHT, buff=0.12)
        feed = Arrow(noisy.get_right(), toks.get_left(), buff=0.15, color=PATCH, stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
        blocks = VGroup(*[RoundedRectangle(width=4.4, height=0.48, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2)
                          for _ in range(int(d["L"]))]).arrange(UP, buff=0.16).next_to(toks, UP, buff=0.45)
        bl = VGroup(*[label(r"attention $+$ MLP", font_size=20, color=GREY_A).move_to(b) for b in blocks])
        out = label(r"out: \ the velocity, \ patch by patch", font_size=20, color=GREY_A).next_to(blocks, UP, buff=0.15)
        cond = VGroup(label(r"noise level $t$", font_size=22, color=C.SURPRISE), label(r"the letter wanted", font_size=22,
                                                                                      color=PATCH))
        cond.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 0.0, 0])
        ada = VGroup(*[Arrow(cond.get_left(), b.get_right(), buff=0.1, color=C.SURPRISE, stroke_width=2,
                             max_tip_length_to_length_ratio=0.08) for b in blocks])
        res = label(r"DiT-XL/2: \ FID $2.27$ on ImageNet $256^2$, \ the best of its time; \\ more arithmetic per picture "
                    r"$\to$ better pictures", font_size=20, color=DIT_C).to_corner(UR, buff=0.4)
        cite_ = cite(r"W.~Peebles \& S.~Xie, \textit{Scalable Diffusion Models with Transformers} (2023)", corner=DR)
        dcard = history_card(2023, r"DiT \ (Peebles \& Xie)", r"a plain transformer as the denoiser", color=HIST,
                             width=4.4, font_size=24).move_to([4.3, 1.9, 0])
        with self.voiceover(
            "In 2023 William Peebles and Saining Xie replaced the U-Net with a plain transformer, the diffusion "
            "transformer, DiT. <bookmark mark='a'/> The noisy picture is cut into patch tokens, as in chapter 1. "
            "<bookmark mark='b'/> Transformer blocks process them, and out comes the velocity, patch by patch. "
            "<bookmark mark='c'/> The noise level and the request come in through every block; how exactly is the "
            "next chapter. <bookmark mark='d'/> Its quality tracked its arithmetic: bigger models, or smaller "
            "patches, gave better pictures, and their largest set a record on ImageNet. It scales like a language "
            "model, and the image and video models since have nearly all been transformers."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(noisy), Create(ngrid), FadeIn(dcard, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(GrowArrow(feed), LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.1) for t_ in toks], lag_ratio=0.08),
                      FadeIn(more))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), FadeIn(bl), FadeIn(out))
            vo.wait_until("c")
            self.play(FadeIn(cond), LaggedStart(*[GrowArrow(a_) for a_ in ada], lag_ratio=0.15))
            vo.wait_until("d")
            self.play(FadeOut(dcard), FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("denoisers")
        ev = np.asarray(d["eval_at"], float)
        ua, za = np.asarray(d["unet_acc"]), np.asarray(d["zero_acc"])
        uf, zf = np.asarray(d["unet_fd"]), np.asarray(d["zero_fd"])
        top_fd = float(max(uf.max(), zf.max())) * 1.08
        ax1 = axes([0, ev[-1]], [0, 1], x_length=4.0, y_length=2.4, xlabel=r"training step",
                   ylabel=r"read as the letter requested", xticks=[0, ev[-1]], yticks=[0, 0.5, 1], center=[-4.4, 0.6, 0],
                   font_size=17, xfmt=lambda x: fmt_int(x))
        ax2 = axes([0, ev[-1]], [0, top_fd], x_length=4.0, y_length=2.4, xlabel=r"training step",
                   ylabel=r"distance from real letters (FD)", xticks=[0, ev[-1]], yticks=[0, round(top_fd / 2)],
                   center=[0.4, 0.6, 0], font_size=17, xfmt=lambda x: fmt_int(x))
        l1 = VGroup(mean_band(ax1.ax, ev, ua, UNET_C), mean_band(ax1.ax, ev, za, DIT_C))
        l2 = VGroup(mean_band(ax2.ax, ev, uf, UNET_C), mean_band(ax2.ax, ev, zf, DIT_C))
        sU = Group(label(r"U-Net", font_size=20, color=UNET_C), glyph_sheet(np.asarray(d["unet_final"]), 2, 5, size=0.5,
                                                                          gap=0.04)).arrange(DOWN, buff=0.1)
        sD = Group(label(r"DiT", font_size=20, color=DIT_C), glyph_sheet(np.asarray(d["zero_final"]), 2, 5, size=0.5,
                                                                       gap=0.04)).arrange(DOWN, buff=0.1)
        Group(sU, sD).arrange(DOWN, buff=0.3).move_to([5.0, 0.6, 0])
        pu, pz = int(d["unet_params"]), int(d["zero_params"])
        mu, mz = int(d["unet_macs"]), int(d["zero_macs"])
        tab = label(rf"U-Net: \ ${fmt_int(pu)}$ weights, \ ${mu / 1e6:.1f}$ million multiply-adds a picture; \ "
                    rf"DiT: \ ${fmt_int(pz)}$ weights, \ ${mz / 1e6:.1f}$ million", font_size=20, color=GREY_A)
        tab.to_edge(DOWN, buff=1.0)
        hd = note(r"same steps, \ batches, \ data order \ and seeds \ (three; \ bands: \ min to max)").next_to(tab, DOWN, buff=0.15)
        u_end, z_end = float(uf[:, -1].mean()), float(zf[:, -1].mean())
        ua_end, za_end = float(ua[:, -1].mean()), float(za[:, -1].mean())
        if u_end < 0.9 * z_end:
            verdict = (f"With similar weights and the same steps, the U-Net wins here: its letters end at a distance of {u_end:.0f} "
                       f"against the transformer's {z_end:.0f}, and {100 * ua_end:.0f} percent are read as requested "
                       f"against {100 * za_end:.0f}. But it bought that with {mu / mz:.0f} times the arithmetic per "
                       "picture, and on letters this small its convolutions' assumptions fit perfectly.")
        elif z_end < 0.9 * u_end:
            verdict = (f"With similar weights and the same steps, the transformer wins: its letters end at a distance of {z_end:.0f} "
                       f"against the U-Net's {u_end:.0f}, though the U-Net spent {mu / mz:.0f} times the arithmetic "
                       "per picture.")
        else:
            verdict = (f"With similar weights and the same steps they end close: a distance of {u_end:.0f} for the U-Net and "
                       f"{z_end:.0f} for the transformer, though the U-Net spent {mu / mz:.0f} times the arithmetic "
                       "per picture.")
        tk = take_away(r"what the transformer brings is not a better small denoiser: \ it's a denoiser that keeps "
                       r"improving with scale", font_size=24)
        with self.voiceover(
            "So which is better? We trained a small U-Net and a small diffusion transformer with about the same "
            "number of weights, on the same letters, with the same steps, batches and seeds. <bookmark mark='a'/> "
            + verdict + " <bookmark mark='b'/> The transformer's case was never that it wins small. It's that it "
            "keeps improving as it grows, with one simple recipe, the same as language models."
        ) as vo:
            self.play(Create(ax1), Create(ax2), FadeIn(tab), FadeIn(hd))
            self.play(FadeIn(sU), FadeIn(sD))
            vo.wait_until("a")
            self.play(*[FadeIn(l_[0]) for l_ in (*l1, *l2)], *[Create(l_[1]) for l_ in (*l1, *l2)], run_time=2.5)
            vo.wait_until("b")
            self.play(FadeOut(hd), FadeOut(tab), FadeIn(tk, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
