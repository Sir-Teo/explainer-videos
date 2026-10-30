from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import FULLC, HISTC, INDEXC, MONO, PART, WINC, load, show


def mask_picture(kind: str, n=16, cell=0.13) -> VGroup:
    """Which keys (columns) each query (row) may read, for a fixed sparse pattern (schematic)."""
    g = VGroup()
    for i in range(n):
        for j in range(n):
            on = j <= i
            if kind == "window":
                on = on and i - j < 4
            elif kind == "strided":
                on = on and (i - j < 4 or (j % 4 == 3))
            elif kind == "global":
                on = on and (i - j < 3 or j < 2)
            elif kind == "random":
                on = on and (i - j < 3 or j < 1 or (i * 7 + j * 3) % 5 == 0)
            g.add(Square(cell, stroke_width=0, fill_color=FULLC if on else GREY_D, fill_opacity=0.9 if on else 0.15)
                  .move_to([j * cell, -i * cell, 0]))
    return g


class Mass(VoiceoverScene):
    def construct(self):
        self.card()
        self.patterns()
        self.mass()
        self.choose()

    def card(self):
        card = chapter_card(12, r"How sparse is attention?", r"Does every query need every key?", lit=(2017,), part=PART)
        with self.voiceover("Chapter twelve. How sparse is attention?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def patterns(self):
        kinds = [("full", r"full \\ (2017)", r"every earlier key"),
                 ("strided", r"strided \\ (Child et al., 2019)", r"a window, \\ and every fourth key"),
                 ("global", r"window $+$ global \\ (Longformer, 2020)", r"a few keys \\ everyone reads"),
                 ("random", r"$+$ random \\ (BigBird, 2020)", r"a few random keys \\ too"),
                 ("window", r"sliding window \\ (Mistral 7B, 2023)", r"only the last few")]
        pics = Group()
        for k, nm, sub in kinds:
            p = mask_picture(k)
            pics.add(VGroup(label(nm, font_size=18, color=FULLC if k == "full" else C.ATTN), p,
                            label(sub, font_size=16, color=GREY_A)).arrange(DOWN, buff=0.15))
        pics.arrange(RIGHT, buff=0.35).move_to([0, 0.2, 0])
        if pics.width > 13.2:
            pics.width = 13.2
        head = label(r"which keys each query may read: \ rows are queries, \ columns keys", font_size=24).to_edge(UP, buff=0.35)
        tag = note(r"schematic", font_size=18).to_corner(DR, buff=0.25)
        foot = label(r"cost of full attention: \ $O(L^2)$ \ $\cdot$ \ a fixed pattern: \ $O(L \sqrt L)$ or $O(L\,w)$ \ "
                     r"$\cdot$ \ but the pattern is chosen in advance", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Attention reads every earlier token, so its cost grows with the square of the length. <bookmark mark='a'/> "
            "The first answers fixed the pattern in advance. OpenAI's Sparse Transformer, in 2019, read a local window "
            "and every k-th key, for a cost that grows like the length to the power one and a half. "
            "<bookmark mark='b'/> In 2020, Longformer added a few global keys that everyone reads, and Google's "
            "BigBird added random ones as well, and proved that such patterns lose no expressive power in "
            "principle. <bookmark mark='c'/> Mistral 7B, in 2023, kept just a sliding window, and stacked layers "
            "let information travel further back. Part 19 measures what windows save at serving time. "
            "<bookmark mark='d'/> But all of these decide in advance which keys a query may read. Does that match "
            "where attention actually goes?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pics[0]))
            vo.wait_until("a")
            self.play(FadeIn(pics[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(pics[2], shift=UP * 0.1), FadeIn(pics[3], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(pics[4], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mass(self):
        t = load("topk")
        ks = [int(v) for v in t["ks"]]
        M = np.asarray(t["mass"])  # layer, head, k
        L, H, _ = M.shape
        lx = np.log2(ks)
        ax = Axes(x_range=[0, lx[-1], 1], y_range=[0, 1, 0.25], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(np.log2(v), 0), DOWN, buff=0.1) for v in ks])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        xn = label(r"the $k$ keys a query weights most \ (of $128$ to $256$)", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"share of its attention they hold", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        cols = [C.TRUE_P, C.INTERVAL, C.BITS, C.SURPRISE]
        lines = VGroup(*[curve(ax, lx, M[l_, h], cols[l_ % 4], 2.5).set_stroke(opacity=0.8) for l_ in range(L) for h in range(H)])
        key = VGroup(*[label(rf"layer {l_ + 1}", font_size=22, color=cols[l_ % 4]) for l_ in range(L)])
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 0.6, 0])
        m16 = float(M[..., ks.index(16)].mean())
        head = label(r"Part 13's transformer, \ every head, \ on held-out text", font_size=26).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Attention looks at every earlier token, but how much of that does it use? Take part thirteen's "
            "transformer and, for each query, rank its keys by weight. <bookmark mark='a'/> Each line is one head: "
            "how much of the attention its top k keys hold. "
            f"On average, the top sixteen keys, out of between a hundred and twenty-eight and two hundred and fifty-six, "
            f"hold {100 * m16:.0f} percent. Most of the "
            "attention goes to a few keys."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.05), FadeIn(key), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choose(self):
        t = load("topk")
        kk = [int(v) for v in t["kk"]]
        tk, wn = np.asarray(t["bits_topk"]), np.asarray(t["bits_window"])
        full = float(t["full"])
        lx = np.log2(kk)
        lo = math.floor((full - 0.05) / 0.25) * 0.25
        hi = math.ceil((max(wn.max(), tk.max()) + 0.05) / 0.25) * 0.25
        ax = Axes(x_range=[lx[0] - 0.3, lx[-1] + 0.3, 1], y_range=[lo, hi, 0.25], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(np.log2(v), lo), DOWN, buff=0.1) for v in kk])
        xn = label(r"keys each query may use, \ $k$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yt = VGroup(*[MathTex(f"{v:.2f}", font_size=22, color=GREY_B).next_to(ax.c2p(lx[0] - 0.3, v), LEFT, buff=0.1)
                      for v in np.arange(lo, hi + 1e-9, 0.25)])
        yn = label(r"bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        fl = DashedLine(ax.c2p(lx[0] - 0.3, full), ax.c2p(lx[-1] + 0.3, full), color=GREY_B, stroke_width=1.5)
        fll = label(rf"all keys: \ ${full:.3f}$", font_size=22, color=GREY_B).next_to(ax.c2p(lx[-1] + 0.3, full), UR, buff=0.05)
        cw = VGroup(curve(ax, lx, wn, C.SURPRISE, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=C.SURPRISE) for a, b in zip(lx, wn)])
        ct = VGroup(curve(ax, lx, tk, C.INTERVAL, 3.5), *[Dot(ax.c2p(a, b), radius=0.06, color=C.INTERVAL) for a, b in zip(lx, tk)])
        k1 = label(r"the last $k$ keys \ (a sliding window)", font_size=24, color=C.SURPRISE).move_to([4.4, 1.6, 0])
        k2 = label(r"the $k$ highest-scoring keys", font_size=24, color=C.INTERVAL).next_to(k1, DOWN, buff=0.3).align_to(k1, LEFT)
        i8 = kk.index(8)
        with self.voiceover(
            "So let each query use only k keys. Which k? <bookmark mark='a'/> The simplest choice is the most recent "
            f"ones, a sliding window: with {kk[i8]} keys, {wn[i8]:.2f} bits a character. <bookmark mark='b'/> Better, "
            f"take the {kk[i8]} keys it would weight most: {tk[i8]:.2f}. With {kk[-1]}, "
            + (f"it's within {tk[-1] - full:.3f} bits of using everything."
               if tk[-1] - full >= 0.0005 else "it's within a thousandth of a bit of using everything.")
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(fl), FadeIn(fll))
            vo.wait_until("a")
            self.play(Create(cw[0]), FadeIn(cw[1:]), FadeIn(k1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ct[0]), FadeIn(ct[1:]), FadeIn(k2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

