from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load


class DiT(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.zero()
        self.alphabet()

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
    def zero(self):
        d = load("dit")
        colors = {r"\gamma": C.SURPRISE, r"\beta": C.SURPRISE, r"\alpha": C.BITS, r"c": C.SURPRISE}
        f1 = cmath(r"h \leftarrow h +", r"\alpha", r"_1(", r"c", r") \odot \operatorname{Attn}\big((1 +", r"\gamma", r"_1(", r"c",
                   r")) \odot \operatorname{LN}(h) +", r"\beta", r"_1(", r"c", r")\big)", colors=colors, font_size=32)
        f2 = cmath(r"h \leftarrow h +", r"\alpha", r"_2(", r"c", r") \odot \operatorname{MLP}\big((1 +", r"\gamma", r"_2(", r"c",
                   r")) \odot \operatorname{LN}(h) +", r"\beta", r"_2(", r"c", r")\big)", colors=colors, font_size=32)
        f3 = cmath(r"(", r"\gamma", r"_1,", r"\beta", r"_1,", r"\alpha", r"_1,", r"\gamma", r"_2,", r"\beta", r"_2,", r"\alpha",
                   r"_2) = W", r"c", r"+ b, \qquad W = 0,\ b = 0 \text{ at the start}", colors=colors, font_size=32)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        n1 = label(r"$c$: \ the noise level and the letter, \ as one vector", font_size=22, color=C.SURPRISE)
        n2 = label(r"$\alpha = 0$: \ every block starts as the identity", font_size=22, color=C.BITS)
        VGroup(n1, n2).arrange(RIGHT, buff=1.2).next_to(fs, DOWN, buff=0.6)
        cite_ = cite(r"W.~Peebles \& S.~Xie (2023): \ adaLN-Zero", corner=DR)
        with self.voiceover(
            "Here is that block exactly; Peebles and Xie call it adaLN-Zero. <bookmark mark='a'/> The condition, c, "
            "sets a scale gamma and a shift beta for each normalization, and also a gate, alpha, on each block's "
            "output. <bookmark mark='b'/> All six come from one linear map of c, and that map starts at zero. "
            "<bookmark mark='c'/> So at the start of training, every gate is closed and every block passes its input "
            "straight through: a deep network that begins as the identity, and opens up only as it learns. Of the "
            f"ways they tried to feed in the condition, this one trained best. Ours has {int(d['L'])} such blocks."
        ) as vo:
            self.play(FadeIn(cite_), Write(f1), Write(f2), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(n1))
            vo.wait_until("b")
            self.play(Write(f3))
            vo.wait_until("c")
            self.play(FadeIn(n2), *[Indicate(m_, color=C.BITS) for m_ in (f1[1], f2[1])])
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
