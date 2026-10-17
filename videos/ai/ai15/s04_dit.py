from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load


class DiT(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.alphabet()
        self.mmdit()

    def card(self):
        card = chapter_card(3, r"Transformers as denoisers", r"What should do the denoising?", part=15)
        with self.voiceover("Chapter three. Transformers as denoisers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def design(self):
        d = load("dit")
        toks = VGroup(*[Square(0.34, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.18) for _ in range(10)])
        toks.arrange(RIGHT, buff=0.08).move_to([-1.5, -1.6, 0])
        tl = label(r"noisy patches, \ as tokens", font_size=22, color=PATCH).next_to(toks, DOWN, buff=0.15)
        blocks = VGroup(*[RoundedRectangle(width=4.4, height=0.5, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2)
                          for _ in range(int(d["L"]))]).arrange(UP, buff=0.18).next_to(toks, UP, buff=0.5)
        bl = VGroup(*[label(r"attention $+$ MLP", font_size=20, color=GREY_A).move_to(b) for b in blocks])
        cond = VGroup(label(r"noise level $t$", font_size=22, color=C.SURPRISE), label(r"the letter wanted", font_size=22, color=C.BITS))
        cond.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.2, -0.6, 0])
        ada = VGroup(*[Arrow(cond.get_left(), b.get_right(), buff=0.1, color=C.SURPRISE, stroke_width=2, max_tip_length_to_length_ratio=0.08)
                       for b in blocks])
        colors = {r"\gamma(c)": C.SURPRISE, r"\beta(c)": C.SURPRISE}
        f = cmath(r"\mathrm{adaLN}(h)", "=", r"\gamma(c)", r"\odot", r"\mathrm{LN}(h)", "+", r"\beta(c)", colors=colors,
                  font_size=34).to_edge(UP, buff=0.4).shift(RIGHT * 2.5)
        fl = label(r"the condition sets each layer's scale and shift", font_size=22, color=GREY_A).next_to(f, DOWN, buff=0.12)
        out = label(r"out: \ the velocity, \ patch by patch", font_size=22, color=GREY_A).next_to(blocks, UP, buff=0.2)
        cite_ = cite(r"W.~Peebles \& S.~Xie, \textit{Scalable Diffusion Models with Transformers} (2023)", corner=DR)
        with self.voiceover(
            "Who does the denoising? Early diffusion models used convolutional networks. In 2023, Peebles and Xie "
            "showed a plain transformer does it better, and scales like a language model. <bookmark mark='a'/> The "
            "noisy picture is cut into patch tokens, part eleven's blocks process them, and out come velocities, "
            "patch by patch. <bookmark mark='b'/> The noise level and the request come in through every layer's "
            "normalization: they set its scale and shift. We trained one, with "
            f"{int(d['n_params']) / 1e6:.1f} million numbers, on our letters, told which letter to draw."
        ) as vo:
            self.play(FadeIn(cite_), LaggedStart(*[FadeIn(t_) for t_ in toks], lag_ratio=0.05), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), FadeIn(bl), FadeIn(out))
            vo.wait_until("b")
            self.play(FadeIn(cond), LaggedStart(*[GrowArrow(a_) for a_ in ada], lag_ratio=0.15), Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alphabet(self):
        d = load("dit")
        A = np.asarray(d["alphabet"])
        grid = Group(*[gray_image(im, 0.85) for im in A[:26]]).arrange_in_grid(rows=2, cols=13, buff=0.08).move_to(UP * 0.6)
        asked = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=20, color=C.BITS).next_to(grid[i], UP, buff=0.06)
                         for i, c in enumerate(LETTERS)])
        second = Group(*[gray_image(im, 0.62) for im in A[26:52]]).arrange_in_grid(rows=2, cols=13, buff=0.06).to_edge(DOWN, buff=0.5)
        sl = label(r"asked again, \ from different noise: \ different fonts", font_size=22, color=GREY_A).next_to(second, UP, buff=0.12)
        with self.voiceover(
            "Here it is, asked for each letter of the alphabet, with part fourteen's guidance. <bookmark mark='a'/> "
            "Asked again from different noise, it draws the same letters in different styles: the request fixes "
            "what, the noise picks how."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.05), FadeIn(asked), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g_) for g_ in second], lag_ratio=0.03), FadeIn(sl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mmdit(self):
        txt = VGroup(*[Square(0.34, stroke_color=C.TRUE_P, stroke_width=1.5, fill_color=C.TRUE_P, fill_opacity=0.2) for _ in range(6)])
        img = VGroup(*[Square(0.34, stroke_color=PATCH, stroke_width=1.5, fill_color=PATCH, fill_opacity=0.2) for _ in range(10)])
        seq = VGroup(txt, img).arrange(RIGHT, buff=0.25)
        for g_ in (txt, img):
            g_.arrange(RIGHT, buff=0.06)
        seq.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.4)
        tl = label(r"the prompt's tokens", font_size=22, color=C.TRUE_P).next_to(txt, DOWN, buff=0.2)
        il = label(r"the picture's patches", font_size=22, color=PATCH).next_to(img, DOWN, buff=0.2)
        arcs = VGroup(*[ArcBetweenPoints(a.get_top() + UP * 0.05, b.get_top() + UP * 0.05, angle=-PI / 3, color=C.ATTN,
                                         stroke_width=1.5).set_stroke(opacity=0.6)
                        for a in (txt[1], txt[4], img[2], img[7]) for b in (txt[2], img[0], img[5], img[9]) if a is not b])
        head = label(r"MM-DiT: \ one sequence, \ attention across both, \ separate weights for each kind", font_size=26)
        head.to_edge(UP, buff=0.5)
        sizes = label(r"Stable Diffusion 3: \ $2$ and $8$ billion parameters; \ FLUX.1: \ $12$ billion \ (as published)",
                      font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        cite_ = cite(r"P.~Esser et al., \textit{Scaling Rectified Flow Transformers} (2024)", corner=DR)
        with self.voiceover(
            "For a text prompt, Stable Diffusion 3 put the prompt's tokens and the picture's patches into one "
            "sequence. <bookmark mark='a'/> Attention runs across both, so every patch can look at every word and "
            "every word at every patch, while each kind keeps its own weights. Scaled up, that's Stable Diffusion 3, "
            "and FLUX, with twelve billion parameters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(seq), FadeIn(tl), FadeIn(il), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in arcs], lag_ratio=0.05), run_time=2.0)
            self.play(FadeIn(sizes))
        self.wait(0.3)
        self.clear_scene()
