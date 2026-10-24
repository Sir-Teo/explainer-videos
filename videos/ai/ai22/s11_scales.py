from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import GEN_C, GEN_NAME, HIST, PANEL, PART, PATCH, gray_image, load, signed_image, spread_bars

VAR_C = GEN_C["var"]


def block_mask(sizes=(1, 2, 3, 4, 5), cell=0.075) -> VGroup:
    """VAR's attention mask: a token sees every token of its own scale and of the coarser ones."""
    n = sum(s * s for s in sizes)
    lev = np.concatenate([np.full(s * s, k) for k, s in enumerate(sizes)])
    g = VGroup()
    for i in range(n):
        for j in range(n):
            if lev[j] <= lev[i]:
                g.add(Square(cell, stroke_width=0, fill_color=VAR_C, fill_opacity=0.35 + 0.1 * lev[j]).move_to([j * cell, -i * cell, 0]))
    frame = Square(n * cell, stroke_color=GREY_C, stroke_width=1.5).move_to([(n - 1) * cell / 2, -(n - 1) * cell / 2, 0])
    return VGroup(frame, g)


class Scales(VoiceoverScene):
    def construct(self):
        self.card()
        self.residual()
        self.mask()
        self.compare()
        self.frontier()

    def card(self):
        card = chapter_card(10, r"Coarse to fine", r"In what order should a picture be written?", part=PART)
        with self.voiceover("Chapter ten. Coarse to fine."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def residual(self):
        d = load("tokens")
        sizes = [int(s) for s in d["scales"]]
        imgs = np.asarray(d["scale_imgs"])[:, 0]  # (scales, 20, 20): the picture so far, after each scale
        errs = np.asarray(d["scale_errs"], float)
        S = 1.3
        so_far, adds = Group(), Group()
        prev = np.zeros_like(imgs[0])
        top = max(float(np.abs(np.diff(np.concatenate([prev[None], imgs]), axis=0)).max()), 1e-6)
        for k in range(len(sizes)):
            so_far.add(gray_image(imgs[k], S))
            adds.add(signed_image(imgs[k] - prev, S, top))
            prev = imgs[k]
        so_far.arrange(RIGHT, buff=0.55).move_to([0.6, 1.6, 0])
        for a_, s_ in zip(adds, so_far):
            a_.next_to(s_, DOWN, buff=0.5)
        sl = VGroup(*[MathTex(rf"{s}\times{s}", font_size=22, color=VAR_C).next_to(im, UP, buff=0.1) for s, im in zip(sizes, so_far)])
        el = VGroup(*[MathTex(f"{e:.3f}", font_size=20, color=GREY_B).next_to(im, DOWN, buff=0.08) for e, im in zip(errs, adds)])
        rowl = VGroup(label(r"the picture \\ so far", font_size=18, color=GREY_A).next_to(so_far, LEFT, buff=0.3),
                      label(r"what this \\ scale adds", font_size=18, color=GREY_A).next_to(adds, LEFT, buff=0.3),
                      label(r"error \ (held-out)", font_size=16, color=GREY_B).next_to(el, LEFT, buff=0.3))
        colors = {r"r_k": VAR_C, r"\hat f": GREY_A}
        eq = cmath(r"r_k", r"= Q\big(\operatorname{down}_{s_k}(f -", r"\hat f", r"_{k-1})\big), \qquad", r"\hat f", r"_k =",
                   r"\hat f", r"_{k-1} + \operatorname{up}(", r"r_k", r")", colors=colors, font_size=30).to_edge(DOWN, buff=0.4)
        cite_ = cite(r"K.~Tian, Y.~Jiang, Z.~Yuan, B.~Peng \& L.~Wang, \textit{Visual Autoregressive Modeling} (2024)", corner=UL)
        with self.voiceover(
            "There's a more natural order for a picture: coarse to fine. In April 2024 Keyu Tian, Liwei Wang and "
            "colleagues at Peking University and ByteDance built a tokenizer with five scales. <bookmark mark='a'/> "
            "The first scale is one token, for the whole picture's rough average; <bookmark mark='b'/> each next scale "
            "codes, on a finer grid, only what the coarser ones missed: a residual. <bookmark mark='c'/> Here is ours, "
            f"on a held-out letter: the error falls from {errs[0]:.3f} after one token to {errs[-1]:.3f} after all "
            f"{sum(s * s for s in sizes)}. <bookmark mark='d'/> In symbols: quantize what's left, averaged down to "
            "this scale; add it back, smoothed up."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(rowl[0]), FadeIn(rowl[1]))
            vo.wait_until("a")
            self.play(FadeIn(so_far[0]), FadeIn(adds[0]), FadeIn(sl[0]), FadeIn(el[0]), FadeIn(rowl[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(so_far[k]), FadeIn(adds[k]), FadeIn(sl[k])) for k in range(1, len(sizes))],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(e_) for e_ in el[1:]], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(Write(eq))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mask(self):
        d = load("tokens")
        tr = np.asarray(d["var_trace"])  # (scales, 4, 20, 20)
        bm = block_mask().move_to([-4.2, 0.2, 0])
        bml = label(r"who sees whom: \ $55$ tokens, \ by scale", font_size=20, color=VAR_C).next_to(bm, DOWN, buff=0.2)
        f = MathTex(r"p(r_1, \ldots, r_5) = \prod_{k=1}^{5} p\big(r_k \mid r_1, \ldots, r_{k-1}, \text{letter}\big)", font_size=30)
        f.move_to([2.2, 2.4, 0])
        rows = Group(*[Group(*[gray_image(tr[k, i], 0.8) for k in range(tr.shape[0])]).arrange(RIGHT, buff=0.15)
                       for i in range(tr.shape[1])]).arrange(DOWN, buff=0.15).move_to([2.2, -0.6, 0])
        hdr = VGroup(*[MathTex(rf"{s}\!\times\!{s}", font_size=20, color=VAR_C).next_to(rows[0][k], UP, buff=0.1)
                       for k, s in enumerate(d["scales"])])
        cap = label(r"our VAR drawing four letters: \ one pass per scale", font_size=20, color=GREY_A).next_to(rows, DOWN, buff=0.2)
        with self.voiceover(
            "Then train a transformer to predict each whole scale at once, from all the coarser ones: next-scale "
            "prediction, VAR. <bookmark mark='a'/> The attention mask is block-causal: every token sees its own scale "
            "and the coarser ones, never the finer. <bookmark mark='b'/> So a picture takes one pass per scale. Here "
            "is ours drawing four letters, in five passes: first a blur, then the shape, then the strokes."
        ) as vo:
            self.play(Write(f))
            vo.wait_until("a")
            self.play(FadeIn(bm[0]), FadeIn(bm[1], lag_ratio=0.002), FadeIn(bml), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hdr), FadeIn(cap))
            for k in range(tr.shape[0]):
                self.play(*[FadeIn(r_[k], shift=RIGHT * 0.05) for r_ in rows], run_time=0.7)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("tokens")
        kinds = ["raster", "maskgit", "var"]
        fd = [np.asarray(d[f"{k}_fd"], float) for k in kinds]
        acc = [np.asarray(d[f"{k}_acc"], float) for k in kinds]
        cols = [GEN_C[k] for k in kinds]
        b1 = spread_bars([fd], cols, None, height=2.6, bar_w=0.7, gap=0.3, fmt=lambda v: f"{v:.0f}", font_size=20).move_to([-4.0, 0.2, 0])
        b2 = spread_bars([acc], cols, None, height=2.6, bar_w=0.7, gap=0.3, vmax=1.0, fmt=lambda v: rf"{100 * v:.0f}\%",
                         font_size=20).move_to([0.4, 0.2, 0])
        t1 = label(r"distance from real letters (FD)", font_size=20, color=GREY_A).next_to(b1, UP, buff=0.3)
        t2 = label(r"read as requested", font_size=20, color=GREY_A).next_to(b2, UP, buff=0.3)
        passes = VGroup(*[label(rf"{GEN_NAME[k]}: \ ${int(d[f'{k}_passes'])}$ passes", font_size=24, color=GEN_C[k])
                          for k in kinds]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.9, 0.4, 0])
        hd = note(r"same transformer size, \ steps and guidance; \ three seeds: \ dots, \ bars min to max").to_edge(DOWN, buff=0.35)
        m = {k: float(f.mean()) for k, f in zip(kinds, fd)}
        best = min(kinds, key=lambda k: m[k])
        names = {"raster": "raster order", "maskgit": "MaskGIT", "var": "VAR"}
        if best == "var":
            verdict = (f"VAR comes out best here, at a distance of {m['var']:.0f}, against {m['maskgit']:.0f} for "
                       f"MaskGIT and {m['raster']:.0f} for raster order, in the fewest passes.")
        else:
            verdict = (f"Here {names[best]} comes out best, at a distance of {m[best]:.0f}; VAR reaches {m['var']:.0f} "
                       f"in five passes. With only twenty-five tokens, our letters leave little room for the order to "
                       "matter much; VAR's case is made at a thousand tokens and more.")
        with self.voiceover(
            "All three, side by side: the same transformer size, steps and guidance, three seeds each. "
            "<bookmark mark='a'/> " + verdict
        ) as vo:
            self.play(FadeIn(t1), FadeIn(t2), FadeIn(b1.base), FadeIn(b2.base), FadeIn(hd), FadeIn(passes))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in b1.bars[0]], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(b_, shift=UP * 0.15) for b_ in b2.bars[0]], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"Tokens that keep up with diffusion", font_size=36).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(r"Apr 2024", r"VAR", r"ImageNet $256^2$: \ FID $1.73$, \ against $18.65$ for its raster-order "
                         r"baseline; \ about $20\times$ faster; \ NeurIPS 2024 best paper", color=HIST, width=4.2, font_size=19),
            history_card(r"Jun 2024", r"MAR \ (Li, Tian, Li, Deng \& He)", r"no codebook: \ continuous tokens, \ each "
                         r"drawn by a tiny diffusion head", color=HIST, width=4.2, font_size=19),
            history_card(r"Dec 2024", r"Infinity \ (Han et al.)", r"each token a string of up to $64$ bits, \ predicted bit by bit: "
                         r"\ a vocabulary of $2^{64}$; \ a $1024^2$ picture in $0.8$ s", color=HIST, width=4.2, font_size=19),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        if cards.width > 13.2:
            cards.width = 13.2
        foot = label(r"the token route stays alive: \ it is how a language model can draw \ (chapter 11)", font_size=24,
                     color=PATCH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "On ImageNet, VAR's own raster-order baseline scored a distance of eighteen point six five; VAR scored one "
            "point seven three, beat the diffusion transformer, and drew about twenty times faster. It won the best "
            "paper award at NeurIPS 2024. <bookmark mark='a'/> Others dropped the codebook: MAR, from Kaiming He's "
            "group, makes continuous tokens, each drawn by a tiny diffusion model. <bookmark mark='b'/> And Infinity "
            "made each token a string of up to sixty-four bits, predicted bit by bit: a vocabulary of up to two to the "
            "sixty-four. <bookmark mark='c'/> Tokens matter for another reason: they are how a language model can "
            "draw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
