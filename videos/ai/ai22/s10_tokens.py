from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import (GEN_C, GEN_NAME, HIST, PANEL, PART, PATCH, glyph_sheet, gray_image, load,
                                   spread_bars)

RAS_C, MG_C = GEN_C["raster"], GEN_C["maskgit"]


class Tokens(VoiceoverScene):
    def construct(self):
        self.card()
        self.vq()
        self.raster()
        self.maskgit()
        self.compare()

    def card(self):
        card = chapter_card(9, r"Pictures as tokens", r"Can a picture be written like a sentence?", part=PART)
        with self.voiceover("Chapter nine. Pictures as tokens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def vq(self):
        d = load("tokens")
        orig, rec = np.asarray(d["orig"]), np.asarray(d["single_rec"])
        a_in = gray_image(orig[0], 2.0).move_to([-5.0, 0.9, 0])
        rng = np.random.default_rng(3)  # illustrative indices for the picture of a token grid
        idx = VGroup(*[VGroup(Square(0.42, stroke_color=PATCH, stroke_width=1.5, fill_color=PANEL, fill_opacity=1),
                              MathTex(str(int(k)), font_size=18, color=PATCH)) for k in rng.integers(0, int(d["K"]), 25)])
        for s_ in idx:
            s_[1].move_to(s_[0])
        idx.arrange_in_grid(5, 5, buff=0).move_to([-1.4, 0.9, 0])
        a_out = gray_image(rec[0], 2.0).move_to([2.2, 0.9, 0])
        arr = VGroup(Arrow(a_in.get_right(), idx.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5),
                     Arrow(idx.get_right(), a_out.get_left(), buff=0.15, color=GREY_B, stroke_width=2.5))
        labs = VGroup(label(r"encode, \ snap to \\ the nearest code", font_size=18, color=GREY_A).next_to(arr[0], UP, buff=0.1),
                      label(r"decode", font_size=18, color=GREY_A).next_to(arr[1], UP, buff=0.1),
                      label(rf"$25$ tokens, \ each one of ${int(d['K'])}$ codes \ (schematic numbers)", font_size=18,
                            color=PATCH).next_to(idx, DOWN, buff=0.15),
                      label(rf"rebuilt: \ error ${float(d['single_rmse']):.3f}$", font_size=18, color=GREY_A).next_to(a_out, DOWN, buff=0.15))
        hc = history_card(r"Dec 2020", r"VQGAN \ (Esser, Rombach \& Ommer)", r"a codebook autoencoder trained with a "
                          r"perceptual loss and a GAN's judge, \ so a $16 \times 16$ grid of tokens rebuilds a sharp "
                          r"picture; \ then a transformer writes the tokens", color=HIST, width=5.6, font_size=19)
        hc.move_to([4.0, -2.0, 0])
        recs = Group(glyph_sheet(orig[:4], 1, 4, size=0.55), glyph_sheet(rec[:4], 1, 4, size=0.55)).arrange(DOWN, buff=0.1)
        recs.move_to([-3.6, -2.2, 0])
        rl = label(r"held-out letters, \ and rebuilt from $25$ tokens", font_size=18, color=GREY_A).next_to(recs, UP, buff=0.1)
        with self.voiceover(
            "Diffusion isn't the only way to draw. Language models write one token at a time; to do that with "
            "pictures, first turn a picture into tokens. <bookmark mark='a'/> Part 20's VQ-VAE and Part 23's codebooks "
            "do it: encode the picture into a small grid, and snap each cell to the nearest entry of a learned "
            "codebook. The entry's number is the token. <bookmark mark='b'/> In December 2020 Patrick Esser, Robin "
            "Rombach and Bjorn Ommer trained such a tokenizer with a perceptual loss and a GAN's judge, so a sixteen "
            "by sixteen grid of tokens rebuilt a sharp picture: VQGAN. <bookmark mark='c'/> Ours squeezes a letter "
            f"into twenty-five tokens, each one of {int(d['K'])} codes, and rebuilds held-out letters with an error "
            f"of {float(d['single_rmse']):.3f}."
        ) as vo:
            self.play(FadeIn(a_in))
            vo.wait_until("a")
            self.play(GrowArrow(arr[0]), FadeIn(labs[0]), FadeIn(idx, lag_ratio=0.02), FadeIn(labs[2]), run_time=1.5)
            self.play(GrowArrow(arr[1]), FadeIn(labs[1]), FadeIn(a_out), FadeIn(labs[3]))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(recs), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def raster(self):
        d = load("tokens")
        x = np.asarray(d["raster_samples"])[0]
        n = 5
        S = 3.6
        img = gray_image(x, S).move_to([-3.0, -0.2, 0])
        px = S / n
        ul = img.get_corner(UL)
        cover = VGroup(*[Square(px * 1.02, stroke_width=0, fill_color=PANEL, fill_opacity=1)
                         .move_to(ul + RIGHT * px * (c + 0.5) + DOWN * px * (r + 0.5)) for r in range(n) for c in range(n)])
        order = VGroup(*[MathTex(str(k + 1), font_size=22, color=RAS_C).move_to(cover[k]) for k in range(n * n)])
        canvas = SurroundingRectangle(img, buff=0, color=GREY_C, stroke_width=1.5)
        cap = label(r"raster order: \ token $k$ from tokens $1, \dots, k-1$; \ $25$ passes", font_size=22, color=RAS_C)
        cap.next_to(img, DOWN, buff=0.3)
        f = MathTex(r"p(x) = \prod_{k=1}^{25} p(x_k \mid x_1, \dots, x_{k-1}, \text{letter})", font_size=32).move_to([3.4, 1.0, 0])
        side = label(r"DALL$\cdot$E: \ $1{,}024$ tokens, \ $1{,}024$ passes; \\ the top rows are fixed \\ before anything "
                     r"below exists", font_size=22, color=GREY_A).move_to([3.4, -1.0, 0])
        with self.voiceover(
            "Then write the tokens the way a language model writes words: left to right, top to bottom, each one "
            "predicted from the ones before. <bookmark mark='a'/> For us that's twenty-five passes through the "
            "network. <bookmark mark='b'/> It works: DALL-E and Parti did exactly this. But a thousand tokens take a "
            "thousand passes, and it's an odd order for a picture: the top rows are decided before anything below "
            "them exists."
        ) as vo:
            self.add(img, cover)
            self.play(Create(canvas), Write(f))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(order[k], scale=0.6), FadeOut(cover[k])) for k in range(n * n)],
                                  lag_ratio=0.25), FadeIn(cap), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def maskgit(self):
        d = load("tokens")
        tr = np.asarray(d["maskgit_trace"])  # (steps, 4, 20, 20)
        tm = np.asarray(d["maskgit_trace_mask"])  # (steps, 4, 25)
        T = tr.shape[0]
        S = 0.95
        cols = Group()
        for k in range(T):
            col = Group()
            for i in range(tr.shape[1]):
                im = gray_image(tr[k, i], S)
                cells = VGroup(*[Square(S / 5, stroke_width=0, fill_color=PANEL, fill_opacity=0.0 if tm[k, i, j] else 0.72)
                                 .move_to(im.get_corner(UL) + RIGHT * S / 5 * (j % 5 + 0.5) + DOWN * S / 5 * (j // 5 + 0.5))
                                 for j in range(25)])
                col.add(Group(im, cells))
            col.arrange(DOWN, buff=0.12)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.18).move_to([0, -0.5, 0])
        if cols.width > 12.8:
            cols.width = 12.8
        steps_l = VGroup(*[MathTex(str(k + 1), font_size=20, color=MG_C).next_to(c_, UP, buff=0.1) for k, c_ in enumerate(cols)])
        hl = label(r"MaskGIT drawing four letters in $8$ passes: \ dark cells still masked; \ the rest of each picture is "
                   r"its current best guess", font_size=20, color=GREY_A).to_edge(UP, buff=0.3)
        sched = MathTex(r"\text{still masked after pass } k:\ \ \big\lfloor 25 \cos\!\big(\tfrac{\pi}{2}\tfrac{k}{8}\big)\big\rfloor",
                        font_size=26, color=MG_C).to_edge(DOWN, buff=0.3)
        cite_ = cite(r"H.~Chang et al., \textit{MaskGIT} (2022): \ $8$ passes instead of $256$; \ FID $6.18$ against "
                     r"$18.65$ \ (ImageNet $256^2$, as published)", corner=UL)
        cite_.next_to(hl, DOWN, buff=0.1)
        with self.voiceover(
            "In February 2022 Huiwen Chang and colleagues at Google trained a transformer like BERT instead: hide "
            "a random share of the tokens and predict them all at once, seeing every other token. MaskGIT. "
            "<bookmark mark='a'/> To draw, start fully masked. Predict every token; keep the ones it's surest of; "
            "mask the rest again, and repeat. A cosine schedule says how many to keep: few at first, then faster. "
            "<bookmark mark='b'/> Here is ours drawing four letters in eight passes. Each pass fixes tokens all over "
            "the picture at once, a few at first, then more. The paper drew ImageNet pictures in eight passes "
            "instead of two hundred and fifty-six, and better."
        ) as vo:
            self.play(FadeIn(hl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), FadeIn(steps_l[0]), FadeIn(sched))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c_), FadeIn(s_)) for c_, s_ in zip(cols[1:], steps_l[1:])],
                                  lag_ratio=0.4), run_time=4.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("tokens")
        kinds = ["raster", "maskgit"]
        fd = [np.asarray(d[f"{k}_fd"], float) for k in kinds]
        acc = [np.asarray(d[f"{k}_acc"], float) for k in kinds]
        cols = [GEN_C[k] for k in kinds]
        b1 = spread_bars([fd], cols, None, height=2.6, bar_w=0.8, gap=0.4, fmt=lambda v: f"{v:.0f}", font_size=20).move_to([-3.6, 0.0, 0])
        b2 = spread_bars([acc], cols, None, height=2.6, bar_w=0.8, gap=0.4, vmax=1.0, fmt=lambda v: rf"{100 * v:.0f}\%",
                         font_size=20).move_to([0.6, 0.0, 0])
        t1 = label(r"distance from real letters (FD)", font_size=20, color=GREY_A).next_to(b1, UP, buff=0.3)
        t2 = label(r"read as requested", font_size=20, color=GREY_A).next_to(b2, UP, buff=0.3)
        passes = VGroup(*[label(rf"{GEN_NAME[k]}: \ ${int(d[f'{k}_passes'])}$ passes", font_size=24, color=GEN_C[k])
                          for k in kinds]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.3, 0])
        hd = note(rf"same tokens, \ same transformer size \ (${int(d['raster_params']) // 1000}$ thousand weights), \ "
                  rf"${int(d['ng']):,}$ steps, \ guidance ${float(d['guide']):g}$; \ three seeds".replace(",", "{,}")).to_edge(DOWN, buff=0.35)
        m_r, m_m = float(fd[0].mean()), float(fd[1].mean())
        a_r, a_m = float(acc[0].mean()), float(acc[1].mean())
        if m_m < m_r:
            verdict = (f"MaskGIT's letters are closer to real ones, {m_m:.0f} against {m_r:.0f}, in about a third of "
                       "the passes.")
        else:
            verdict = (f"Raster order's letters are closer to real ones here, {m_r:.0f} against MaskGIT's {m_m:.0f}: "
                       "parallel decoding guesses several tokens without seeing each other's choices. MaskGIT does it "
                       "in about a third of the passes.")
        with self.voiceover(
            "We trained both on the same tokens, with the same size of transformer and the same steps, three seeds "
            f"each. <bookmark mark='a'/> {verdict} <bookmark mark='b'/> The judge reads {100 * a_r:.0f} percent of "
            f"raster order's letters as requested, and {100 * a_m:.0f} percent of MaskGIT's."
        ) as vo:
            self.play(FadeIn(t1), FadeIn(t2), FadeIn(b1.base), FadeIn(b2.base), FadeIn(hd), FadeIn(passes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in b1.bars[0]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in b2.bars[0]], lag_ratio=0.3), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
