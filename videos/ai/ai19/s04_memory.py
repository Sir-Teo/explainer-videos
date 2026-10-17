from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.compute import load


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.roofline()
        self.flash()
        self.paging()

    def card(self):
        card = chapter_card(3, r"Moving numbers is the cost", r"Where does the time actually go?", part=19)
        with self.voiceover("Chapter three. Moving numbers is the cost."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def roofline(self):
        r = load("roofline")
        I, G = np.log10(np.asarray(r["intensity"])), np.log10(np.asarray(r["gflops"]))
        bw, peak = float(r["bandwidth"]), float(r["peak"])
        x0, x1 = -1.0, 3.0
        y0, y1 = math.floor(min(G.min(), math.log10(bw * 0.1))), math.ceil(math.log10(peak) + 0.3)
        # coordinates shifted so the axes meet at the bottom left: X = log10(intensity) - x0, Y = log10(GFLOP/s) - y0
        ax = Axes(x_range=[0, x1 - x0, 1], y_range=[0, y1 - y0, 1], x_length=7.4, y_length=4.4, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-1.8, -0.5, 0])

        def P(x, y):
            return ax.c2p(x - x0, y - y0)

        xt = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(P(v, y0), DOWN, buff=0.1)
                      for t, v in ((r"0.1", -1), ("1", 0), ("10", 1), ("100", 2), (r"1{,}000", 3))])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(P(x0, v), LEFT, buff=0.1) for v in range(y0, y1 + 1)])
        xn = label(r"arithmetic per byte moved", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"billions of operations a second \ (this computer)", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        xs = np.linspace(x0, x1, 100)
        roof = np.minimum(np.log10(bw) + xs, math.log10(peak))
        rl = VMobject(color=C.BITS, stroke_width=4).set_points_as_corners([P(x, y) for x, y in zip(xs, roof) if y >= y0])
        pts = VGroup(*[Dot(P(a, b), radius=0.07, color=C.TRUE_P) for a, b in zip(I, G)])
        lab = VGroup(*[MathTex(str(n), font_size=18, color=C.TRUE_P).next_to(p, UR, buff=0.04) for n, p in zip(r["sizes"], pts)])
        k1 = label(rf"memory: \ ${bw:.0f}$ GB/s", font_size=24, color=C.BITS).move_to([4.6, 1.2, 0])
        k2 = label(rf"arithmetic: \ ${peak:.0f}$ GFLOP/s", font_size=24, color=C.BITS).next_to(k1, DOWN, buff=0.2).align_to(k1, LEFT)
        k3 = label(r"dots: \ matrix products, \ by size", font_size=22, color=C.TRUE_P).next_to(k2, DOWN, buff=0.4).align_to(k1, LEFT)
        tok_y = min(math.log10(bw), math.log10(peak))  # at one operation per byte
        tok = glow_dot(P(0, tok_y), color=C.SURPRISE, radius=0.09)
        drop = DashedLine(P(0, y0), P(0, tok_y), color=C.SURPRISE, stroke_width=2)
        gap = DoubleArrow(P(0, tok_y), P(0, math.log10(peak)), buff=0.05, stroke_width=3, color=C.SURPRISE,
                          max_tip_length_to_length_ratio=0.15, tip_length=0.15)
        k4 = label(rf"writing one token: \\ $\approx 1$ operation per byte: \\ at most ${bw:.0f}$ of ${peak:.0f}$ GFLOP/s",
                   font_size=22, color=C.SURPRISE).next_to(k3, DOWN, buff=0.4).align_to(k1, LEFT)
        cite_ = cite(r"S.~Williams, A.~Waterman \& D.~Patterson, \textit{Roofline} (2009)", corner=DR)
        with self.voiceover(
            "Every computer has two speeds: how fast it does arithmetic, and how fast it moves numbers from memory. "
            "<bookmark mark='a'/> We measured this one. The roofline: a slope where moving data is the limit, and a "
            "flat roof where arithmetic is. <bookmark mark='b'/> Big matrix products do lots of arithmetic per number "
            "moved, and the fastest of them sets the roof. <bookmark mark='c'/> But writing one token at a time "
            "multiplies each weight once: about one operation per byte, down on the slope, well below the roof. "
            "That's why the tricks of this part all move fewer bytes."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(rl), FadeIn(k1), FadeIn(k2), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.15), FadeIn(lab), FadeIn(k3))
            vo.wait_until("c")
            self.play(Create(drop), FadeIn(tok, scale=0.5))
            self.play(GrowFromCenter(gap), FadeIn(k4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flash(self):
        f = load("flash")
        n = 8
        cell = 0.42
        grid = VGroup(*[Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=C.ATTN, fill_opacity=0.08)
                        for _ in range(n * n)]).arrange_in_grid(rows=n, cols=n, buff=0).move_to([-3.2, 0.0, 0])
        gl = label(r"the $T \times T$ table of scores", font_size=22, color=C.ATTN).next_to(grid, UP, buff=0.15)
        qb = SurroundingRectangle(VGroup(*grid[:n]), color=C.QUERY, buff=0.02, stroke_width=3)
        tile = SurroundingRectangle(grid[0], color=C.KEY, buff=0.0, stroke_width=3)
        colors = {r"m": C.BITS, r"\ell": C.BITS}
        eqs = VGroup(cmath(r"m \leftarrow \max(m, \max_j s_j)", colors=colors, font_size=30),
                     cmath(r"\ell \leftarrow \ell\,e^{m_{\text{old}} - m} + \textstyle\sum_j e^{s_j - m}", colors=colors, font_size=30),
                     cmath(r"o \leftarrow o\,e^{m_{\text{old}} - m} + \textstyle\sum_j e^{s_j - m} v_j", font_size=30))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 1.2, 0])
        el = label(r"an online softmax: \ a running max and a running sum", font_size=22, color=GREY_A).next_to(eqs, UP, buff=0.2)
        chk = label(rf"computed tile by tile on ${int(f['T'])}$ positions: \\ equal to the plain formula within "
                    rf"$10^{{{math.ceil(math.log10(max(float(f['dev']), 1e-17)))}}}$", font_size=22, color=GREY_B).next_to(eqs, DOWN, buff=0.4)
        Ts, plain, tiled = np.asarray(f["Ts"]), np.asarray(f["plain"]), np.asarray(f["tiled"])
        i = list(Ts).index(131072)
        mem = label(rf"at ${Ts[i]:,}$ positions, \ one head: \ ${plain[i] / 2**30:.0f}$ GiB of scores, \ "
                    rf"or ${tiled[i] / 2**20:.0f}$ MiB without them".replace(",", "{,}"), font_size=22, color=C.BITS).to_edge(DOWN, buff=0.5)
        cite_ = cite(r"T.~Dao et al., \textit{FlashAttention} (2022)", corner=UR)
        with self.voiceover(
            "Attention has its own memory problem: the table of scores grows with the square of the length. "
            "FlashAttention never stores it. <bookmark mark='a'/> It takes a block of queries, streams the keys and "
            "values through in tiles, small enough to stay in the chip's fastest memory, <bookmark mark='b'/> and "
            "keeps a running maximum and a running sum: it remembers the biggest score so far, so the exponentials "
            "never blow up, and rescales its partial sum whenever a bigger one arrives. So the softmax comes out "
            "exactly right at the end. We checked "
            "it: the same numbers as the plain formula, to rounding error, without ever holding the table."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(gl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(qb), Create(tile))
            for j in range(1, n):
                self.play(tile.animate.move_to(grid[j]), grid[j - 1].animate.set_fill(opacity=0.5), run_time=0.25)
            self.play(grid[n - 1].animate.set_fill(opacity=0.5), run_time=0.2)
            self.play(VGroup(*grid[:n]).animate.set_fill(opacity=0.08), FadeOut(tile), run_time=0.4)
            for i in range(1, n):  # every block of queries in turn; each row of scores used, then dropped
                row = VGroup(*grid[i * n:(i + 1) * n])
                self.play(qb.animate.move_to(row), row.animate.set_fill(opacity=0.5), run_time=0.22)
                self.play(row.animate.set_fill(opacity=0.08), run_time=0.12)
            vo.wait_until("b")
            self.play(FadeIn(el), Write(eqs), run_time=2.0)
            self.play(FadeIn(chk), FadeIn(mem))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def paging(self):
        p = load("paging")
        lens = np.asarray(p["lens"])[:24]
        M = int(p["max_len"])
        page = int(p["page"])
        rowh, W = 0.2, 5.2
        left = VGroup()
        for i, L in enumerate(lens):
            y = 2.3 - i * rowh
            left.add(Rectangle(width=W, height=rowh * 0.8, stroke_width=0.6, stroke_color=GREY_D, fill_opacity=0).move_to([-3.6, y, 0]))
            left.add(Rectangle(width=W * L / M, height=rowh * 0.8, stroke_width=0, fill_color=C.TRUE_P, fill_opacity=0.8)
                     .move_to([-3.6 - W / 2 + W * L / M / 2, y, 0]))
        right = VGroup()
        x, y = 0.0, 2.3
        pw = W * page / M * 6  # pages drawn larger, to be visible
        colors = [C.TRUE_P, C.BITS, C.INTERVAL, C.SURPRISE, C.NEURAL, C.MODEL_Q]
        for i, L in enumerate(lens):
            for _ in range(int(math.ceil(L / page / 6))):
                if x + pw > W:
                    x, y = 0.0, y - rowh
                right.add(Rectangle(width=pw * 0.9, height=rowh * 0.8, stroke_width=0, fill_color=colors[i % 6], fill_opacity=0.8)
                          .move_to([1.0 + x + pw / 2, y, 0]))
                x += pw
        pool = Rectangle(width=W, height=rowh * len(lens), stroke_color=GREY_C, stroke_width=1.5).move_to([3.6, 2.3 - rowh * (len(lens) - 1) / 2, 0])
        right.shift([pool.get_left()[0] + 0.05 - right.get_left()[0], pool.get_top()[1] - 0.03 - right.get_top()[1], 0])
        free = label(r"free: \ room for more conversations", font_size=22, color=GREY_B)
        free.move_to([pool.get_x(), (right.get_bottom()[1] + pool.get_bottom()[1]) / 2, 0])
        ll = label(rf"one block per request, \ reserved at the maximum (${M:,}$)".replace(",", "{,}"), font_size=22, color=GREY_A)
        ll.move_to([-3.6, 2.85, 0])
        rl = label(r"pages, \ handed out as needed", font_size=22, color=GREY_A).move_to([3.6, 2.85, 0])
        wl = label(rf"wasted: \ ${100 * float(p['waste_reserved']):.0f}\%$", font_size=28, color=C.SURPRISE).move_to([-3.6, -2.9, 0])
        wr = label(rf"wasted: \ ${100 * float(p['waste_paged']):.1f}\%$", font_size=28, color=C.INTERVAL).move_to([3.6, -2.9, 0])
        tag = note(rf"${int(p['n'])}$ requests of random lengths \ ($24$ drawn); \ pages of ${page}$ tokens").to_edge(DOWN, buff=0.15)
        cite_ = cite(r"W.~Kwon et al., \textit{vLLM: PagedAttention} (2023)", corner=UR)
        with self.voiceover(
            "Finally, the cache from part twelve, on a server answering many people at once. <bookmark mark='a'/> "
            "Reserve each conversation one block of memory long enough for the longest possible answer, and most of "
            f"it sits empty: {100 * float(p['waste_reserved']):.0f} percent wasted, for our two hundred random "
            "requests. <bookmark mark='b'/> vLLM borrowed the operating system's trick: hand out memory in small "
            f"pages, as each conversation grows. Waste falls to {100 * float(p['waste_paged']):.1f} percent, so the "
            "same chip serves several times as many people."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(ll), LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(wl))
            vo.wait_until("b")
            self.play(FadeIn(rl), Create(pool), LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.005), run_time=1.5)
            self.play(FadeIn(wr), FadeIn(free))
        self.wait(0.3)
        self.clear_scene()
