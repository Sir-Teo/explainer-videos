from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import MONO, curve, load


class SparseAttention(VoiceoverScene):
    def construct(self):
        self.card()
        self.mass()
        self.choose()
        self.designs()

    def card(self):
        card = chapter_card(4, r"Sparse attention", r"Does every query need every key?", part=13)
        with self.voiceover("Chapter four. Sparse attention."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

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
        head = label(r"Part 11's transformer, \ every head, \ on held-out text", font_size=26).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Attention looks at every earlier token, but how much of that does it use? Take part eleven's "
            "transformer and, for each query, rank its keys by weight. <bookmark mark='a'/> Each line is one head: "
            "how much of the attention its top k keys hold. "
            f"On average, the top sixteen keys out of a few hundred hold {100 * m16:.0f} percent. Most of the "
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
        lo, hi = full - 0.1, max(wn.max(), tk.max()) + 0.1
        ax = Axes(x_range=[lx[0] - 0.3, lx[-1] + 0.3, 1], y_range=[lo, hi, 0.25], x_length=7.4, y_length=4.2, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(np.log2(v), lo), DOWN, buff=0.1) for v in kk])
        xn = label(r"keys each query may use, \ $k$", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
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
            f"take the {kk[i8]} keys it would weight most: {tk[i8]:.2f}. With {kk[-1]}, it's within "
            f"{tk[-1] - full:.3f} bits of using everything."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn), Create(fl), FadeIn(fll))
            vo.wait_until("a")
            self.play(Create(cw[0]), FadeIn(cw[1:]), FadeIn(k1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ct[0]), FadeIn(ct[1:]), FadeIn(k2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def designs(self):
        rows = VGroup(
            VGroup(label(r"NSA \ (DeepSeek, \ 2025)", font_size=28, color=C.BITS),
                   label(r"three branches: \ compressed summaries of blocks, \ the blocks those summaries rate highest, "
                         r"\\ and a sliding window; \ trained that way from the start", font_size=24, color=GREY_A)),
            VGroup(label(r"DSA \ (DeepSeek-V3.2, \ 2025)", font_size=28, color=C.INTERVAL),
                   label(r"a tiny, fast `lightning indexer' scores every past token; \\ each query attends to the top "
                         r"$2{,}048$ only", font_size=24, color=GREY_A)),
        )
        for r_ in rows:
            r_.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP * 0.4)
        catch = label(r"the catch: \ finding the top keys must cost far less than attending to all of them", font_size=26,
                      color=C.BITS).to_edge(DOWN, buff=0.7)
        cite_ = cite(r"J.~Yuan et al., \textit{Native Sparse Attention} (2025); \ DeepSeek-AI, \textit{DeepSeek-V3.2-Exp} (2025)",
                     corner=DR)
        with self.voiceover(
            "Choosing by score is what real models now do. <bookmark mark='a'/> DeepSeek's native sparse attention "
            "keeps compressed summaries of blocks of the past, picks the blocks that look most relevant, and adds a "
            "window of recent tokens. <bookmark mark='b'/> In DeepSeek-V3.2, a tiny, fast indexer scores every past "
            "token, and each query attends to just the top two thousand and forty-eight. <bookmark mark='c'/> The "
            "trick in both is that finding the important keys must be much cheaper than attending to all of them."
        ) as vo:
            self.play(FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(catch))
        self.wait(0.3)
        self.clear_scene()
