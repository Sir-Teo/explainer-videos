from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (ATTNC, BYTEC, F, KEYC, PART, QUERYC, load, loglog)

COLORS = {r"m": C.BITS, r"\ell": C.BITS, r"o": C.ATTN, r"s_j": QUERYC, r"v_j": C.VALUE, r"M": BYTEC, r"d": GREY_A,
          r"T": GREY_A}


class Flash(VoiceoverScene):
    def construct(self):
        self.card()
        self.standard()
        self.online()
        self.tiles()
        self.io()

    def card(self):
        card = chapter_card(14, r"FlashAttention", r"Can attention be computed without ever writing down its table?",
                            part=PART)
        with self.voiceover("Chapter fourteen. FlashAttention."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def standard(self):
        hbm = RoundedRectangle(width=4.2, height=4.4, corner_radius=0.15, stroke_color=BYTEC, stroke_width=2.5)
        hbm.move_to([-4.2, -0.3, 0])
        hl = label(r"HBM: \ large, \ slow", font_size=22, color=BYTEC).next_to(hbm, UP, buff=0.15)
        sram = RoundedRectangle(width=2.6, height=2.0, corner_radius=0.15, stroke_color=C.CACHE_L1, stroke_width=2.5)
        sram.move_to([3.8, 0.6, 0])
        sl = label(r"SRAM: \ small, \ fast", font_size=22, color=C.CACHE_L1).next_to(sram, UP, buff=0.15)
        mats = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in ((r"$Q, K, V$", GREY_A), (r"$S = QK^\top$", ATTNC),
                                                                       (r"$P = \mathrm{softmax}(S)$", ATTNC),
                                                                       (r"$O = PV$", C.VALUE))])
        mats.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(hbm)
        steps = [(0, 1, r"read $Q, K$; \ write $S$"), (1, 2, r"read $S$; \ write $P$"), (2, 3, r"read $P, V$; \ write $O$")]
        arrows = VGroup()
        texts = VGroup()
        for k, (a, b, t) in enumerate(steps):
            y = mats[a].get_y() - 0.25
            ar1 = Arrow([hbm.get_right()[0], y, 0], [sram.get_left()[0], sram.get_y() + 0.3 - 0.3 * k, 0], buff=0.1,
                        color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.06)
            arrows.add(ar1)
            texts.add(label(t, font_size=18, color=GREY_A).next_to(sram, DOWN, buff=0.3 + 0.4 * k))
        f = load("flash")
        T = 131072
        tbl = 2.0 * T * T
        cost = label(rf"the table, \ one head, \ $T = 128$k, \ $16$ bits: \ ${tbl / 2**30:.0f}$ GiB", font_size=22,
                     color=ATTNC).to_corner(DL, buff=0.4)
        hc = history_card(2022, r"Tri Dao, Daniel Fu, Stefano Ermon, Atri Rudra \& Christopher R\'e",
                          rf"FlashAttention: \ exact, \ IO-aware; \ GPT-2 ${F.FLASH1['gpt2']:.0f}\times$ faster",
                          width=5.0, font_size=16, color=ATTNC).move_to([4.2, -2.75, 0])
        with self.voiceover(
            "Part 17 ended with FlashAttention, and promised its derivation. Here it is. <bookmark mark='a'/> A GPU "
            "has a large, slow memory, HBM, and a small, fast one on the chip, SRAM. The standard way to compute "
            "attention writes out the T by T table of scores, <bookmark mark='b'/> reads it back for the softmax "
            "and writes the probabilities, <bookmark mark='c'/> then reads those again to weight the values. "
            "<bookmark mark='d'/> For long inputs the table is enormous: at 128 thousand tokens, "
            f"{tbl / 2**30:.0f} gibibytes for a single head, and all that traffic leaves the arithmetic waiting. In "
            "2022 Tri Dao and colleagues at Stanford showed how never to write it at all."
        ) as vo:
            self.play(Create(hbm), FadeIn(hl), Create(sram), FadeIn(sl), FadeIn(mats[0]))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(texts[0]), FadeIn(mats[1]))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(texts[1]), FadeIn(mats[2]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), FadeIn(texts[2]), FadeIn(mats[3]))
            vo.wait_until("d")
            self.play(FadeIn(cost), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def online(self):
        f = load("flash")
        s = np.asarray(f["scores"])
        tr = np.asarray(f["trace"])
        rows = [
            cmath(r"\mathrm{softmax}(s)_j", r"=", r"\frac{e^{s_j - m}}{\ell},", r"\quad m = \max_j s_j,",
                  r"\quad \ell = \sum_j e^{s_j - m}", colors=COLORS, font_size=32),
            cmath(r"m'", r"=", r"\max\big(m, \max_{j \in \text{tile}} s_j\big)", colors=COLORS, font_size=32),
            cmath(r"\ell'", r"=", r"\ell\, e^{m - m'} + \sum_{j \in \text{tile}} e^{s_j - m'}", colors=COLORS, font_size=32),
            cmath(r"o'", r"=", r"o\, e^{m - m'} + \sum_{j \in \text{tile}} e^{s_j - m'}\, v_j", colors=COLORS,
                  font_size=32),
        ]
        whys = [why(r"subtract the max: \ no overflow"), why(r"a bigger score may arrive"),
                why(r"rescale the old sum to the new max"), why(r"the output, \ the same way; \ divide by $\ell$ at the end")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.6, buff=0.32, edge=6.8)
        # the scores of one real query, in tiles of 32, and the running max and sum
        n = len(s)
        W = 10.4
        lo, hi = float(s.min()), float(s.max())
        x0, y0, Hh = -5.2, -2.7, 1.3
        bars = VGroup(*[Rectangle(width=W / n * 0.8, height=max(Hh * (v - lo) / (hi - lo), 0.01), stroke_width=0,
                                  fill_color=QUERYC, fill_opacity=0.7)
                        .move_to([x0 + W * (i + 0.5) / n, y0 + Hh * (v - lo) / (hi - lo) / 2, 0]) for i, v in enumerate(s)])
        tiles = VGroup(*[DashedLine([x0 + W * j / n, y0 - 0.05, 0], [x0 + W * j / n, y0 + Hh + 0.1, 0], color=GREY_C,
                                    dash_length=0.05, stroke_width=1) for j in range(0, n, 32)])
        cap = label(rf"one query of Part 13's transformer \ (position ${int(f['row'])}$): \ its ${n}$ scores, \ tiles "
                    r"of $32$", font_size=18, color=GREY_A).next_to([0, y0 + Hh + 0.12, 0], UP, buff=0.05)
        rd = VGroup(MathTex(r"m =", font_size=26, color=C.BITS), DecimalNumber(tr[0, 0], num_decimal_places=2,
                                                                               font_size=26, color=C.BITS),
                    MathTex(r"\quad \ell =", font_size=26, color=C.BITS),
                    DecimalNumber(tr[0, 1], num_decimal_places=2, font_size=26, color=C.BITS)).arrange(RIGHT, buff=0.1)
        rd.move_to([4.4, -0.75, 0])
        cur = Rectangle(width=W * 32 / n, height=Hh + 0.2, stroke_color=C.BITS, stroke_width=2.5)
        cur.move_to([x0 + W * 16 / n, y0 + Hh / 2, 0])
        dev = float(f["softmax_dev"])
        res = label(rf"at the end: \ the softmax, \ equal to the direct one within ${sci(max(dev, 1e-17), 0)}$",
                    font_size=20, color=C.BITS).move_to([0, -3.3, 0])
        hc = history_card(2018, r"Maxim Milakov \& Natalia Gimelshein, \ NVIDIA", r"the online softmax: \ one pass, \ a "
                          r"running max and sum", width=4.2, font_size=16, color=C.BITS).move_to([4.4, -2.6, 0])
        with self.voiceover(
            "The key is the softmax. <bookmark mark='a'/> To compute it safely you subtract the largest score, so "
            "no exponential overflows, and divide by the sum: so it seems you need the whole row first. "
            "<bookmark mark='b'/> But you can go tile by tile, keeping a running maximum m. <bookmark mark='c'/> "
            "When a bigger score arrives, rescale the sum so far by e to the old max minus the new one, and add "
            "the new tile's terms. <bookmark mark='d'/> The output is kept the same way, unnormalized, and divided "
            "by the sum at the very end. Maxim Milakov and Natalia Gimelshein at NVIDIA published this online "
            "softmax in 2018. <bookmark mark='e'/> Here it runs on one real query of Part 13's transformer, tile by "
            "tile: watch the maximum jump, and the sum shrink to make room for it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(FadeIn(hc))
            vo.wait_until("e")
            self.play(FadeOut(hc), VGroup(*rows, *[w for w in whys if w is not None]).animate.scale(0.72).to_edge(UP,
                                                                                                        buff=0.2))
            self.play(FadeIn(cap), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.003),
                      FadeIn(tiles), run_time=1.5)
            self.play(Create(cur), FadeIn(rd))
            for j in range(1, len(tr)):
                self.play(cur.animate.shift(RIGHT * W * 32 / n), rd[1].animate.set_value(tr[j, 0]),
                          rd[3].animate.set_value(tr[j, 1]), run_time=0.6)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tiles(self):
        f = load("flash")
        n = 8
        cell = 0.42
        grid = VGroup(*[Square(cell, stroke_width=0.8, stroke_color=GREY_D, fill_color=ATTNC, fill_opacity=0.08)
                        for _ in range(n * n)]).arrange_in_grid(rows=n, cols=n, buff=0).move_to([-3.2, 0.0, 0])
        gl = label(r"the $T \times T$ table of scores: \ never stored", font_size=22, color=ATTNC).next_to(grid, UP, buff=0.15)
        qb = SurroundingRectangle(VGroup(*grid[:n]), color=QUERYC, buff=0.02, stroke_width=3)
        tile = SurroundingRectangle(grid[0], color=KEYC, buff=0.0, stroke_width=3)
        k1 = label(r"a block of queries \ stays in SRAM", font_size=22, color=QUERYC)
        k2 = label(r"keys and values \ stream through, \ tile by tile", font_size=22, color=KEYC)
        k3 = label(r"each tile's scores: \ used, \ then dropped", font_size=22, color=ATTNC)
        keys = VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.3, 0])
        dev, d32 = float(f["dev"]), float(f["tf32_dev"])
        chk = VGroup(label(rf"Part 13's real queries, keys and values \ (${int(f['T'])}$ positions):", font_size=20,
                           color=GREY_A),
                     label(rf"tiled against plain: \ ${sci(dev, 0)}$ \ ($64$-bit numbers)", font_size=20,
                           color=C.BITS),
                     label(rf"${sci(d32, 0)}$ in $32$-bit numbers: \ rounding, \ nothing more", font_size=20,
                           color=C.BITS))
        chk.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.4, -1.6, 0])
        ring = sorted(range(n * n), key=lambda q: max(q // n, q % n))
        with self.voiceover(
            "With that, the table is never needed. <bookmark mark='a'/> Take a block of queries and keep it in fast "
            "memory. <bookmark mark='b'/> Stream the keys and values through, tile by tile, small enough to fit "
            "beside it; compute each tile's scores, update the running max, sum and output, and drop the tile. "
            "<bookmark mark='c'/> Then the next block of queries. <bookmark mark='d'/> We checked it on the real "
            "attention of Part 13's transformer: the tiled result equals the plain formula to within rounding, in "
            "64-bit and in 32-bit numbers."
        ) as vo:
            for c_ in grid:
                c_.set_fill(opacity=0.55)
            self.play(FadeIn(gl), LaggedStart(*[FadeIn(grid[q], scale=0.6) for q in ring], lag_ratio=0.02), run_time=2.0)
            self.play(grid.animate.set_fill(opacity=0.08), run_time=0.5)
            vo.wait_until("a")
            self.play(Create(qb), FadeIn(k1))
            vo.wait_until("b")
            self.play(Create(tile), FadeIn(k2))
            for j in range(1, n):
                self.play(tile.animate.move_to(grid[j]), grid[j - 1].animate.set_fill(opacity=0.5), run_time=0.25)
            self.play(grid[n - 1].animate.set_fill(opacity=0.5), run_time=0.2)
            self.play(VGroup(*grid[:n]).animate.set_fill(opacity=0.08), FadeOut(tile), FadeIn(k3), run_time=0.4)
            vo.wait_until("c")
            for i in range(1, n):
                row = VGroup(*grid[i * n:(i + 1) * n])
                self.play(qb.animate.move_to(row), row.animate.set_fill(opacity=0.5), run_time=0.22)
                self.play(row.animate.set_fill(opacity=0.08), run_time=0.12)
            vo.wait_until("d")
            self.play(FadeIn(chk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def io(self):
        f = load("flash")
        Ns = np.asarray(f["Ns"], float)
        M = int(f["M"])
        rows = [
            cmath(r"B_c", r"=", r"\Big\lceil \frac{M}{4d} \Big\rceil", colors=COLORS, font_size=32),
            cmath(r"\text{reads of } K, V", r"=", r"2Td", colors=COLORS, font_size=32),
            cmath(r"\text{reads of } Q, O", r"=", r"\frac{T}{B_c} \cdot T \cdot 3d", r"\;\approx\;",
                  r"\frac{12\,T^2 d^2}{M}", colors=COLORS, font_size=32),
            cmath(r"\Theta\Big(\frac{T^2 d^2}{M}\Big)", r"\;\text{vs}\;", r"\Theta(T^2 + Td)", colors=COLORS,
                  font_size=32),
        ]
        whys = [why(r"a tile of keys and values fills SRAM"), why(r"each loaded once"),
                why(r"once per outer block"), why(r"tiled \ vs \ standard: \ smaller when $d^2 < M$")]
        step = ladder(self, rows, whys, keep=4, top=3.25, x=-3.2, buff=0.3, edge=6.9)
        g = loglog((math.log10(400), math.log10(2e5)), (5, 11.5), x_length=5.4, y_length=3.0,
                   xlabel=r"sequence length $T$", ylabel=r"numbers moved, \ one head", center=[-2.9, -2.25, 0],
                   font_size=17, xfmt=lambda v: {3: r"10^3", 4: r"10^4", 5: r"10^5"}.get(int(v), ""), ystep=2)
        ax = g.ax
        cols = [("io_std_128", ATTNC, r"standard"), ("io_flash_128", C.BITS, r"FlashAttention, \ $d = 128$"),
                ("io_flash_64", KEYC, r"FlashAttention, \ $d = 64$")]
        lines = VGroup(*[curve(ax, np.log10(Ns), np.log10(np.asarray(f[k], float)), c_, 3) for k, c_, _ in cols])
        leg = legend([(c_, t) for _, c_, t in cols], font_size=17).move_to([3.0, -1.7, 0])
        r128 = f["io_std_128"][-1] / f["io_flash_128"][-1]
        r64 = f["io_std_64"][-1] / f["io_flash_64"][-1]
        ok = f["io_count_128"] == f["io_flash_128"][:len(f["io_count_128"])]
        rl = VGroup(label(rf"H100: \ $M = {M:,}$ numbers of SRAM per multiprocessor".replace(",", "{,}"), font_size=18,
                          color=BYTEC),
                    label(rf"$d = 128$: \ ${r128:.1f}\times$ fewer; \ $d = 64$: \ ${r64:.1f}\times$ fewer", font_size=18,
                          color=C.BITS),
                    label(r"the formula and the counted loops agree exactly" if ok else r"formula and count differ",
                          font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rl.move_to([3.6, -2.75, 0])
        hist = VGroup(
            history_card(2023, r"Tri Dao, \ FlashAttention-2", rf"loops swapped, \ less non-matmul work: \ "
                         rf"${F.FLASH2['util'][0]}$--${F.FLASH2['util'][1]}\%$ of an A100's peak", width=3.4, font_size=14,
                         color=ATTNC),
            history_card(2024, r"Jay Shah et al., \ FlashAttention-3", rf"Hopper's asynchrony, \ FP8: \ "
                         rf"${F.FLASH3['bf16'] / 1e12:.0f}$ TFLOP/s, \ ${F.FLASH3['util']}\%$ of an H100", width=3.4,
                         font_size=14, color=ATTNC)).arrange(DOWN, buff=0.15).to_corner(UR, buff=0.15)
        with self.voiceover(
            "How much traffic does that save? <bookmark mark='a'/> With M numbers of fast memory and heads of size "
            "d, a tile of keys and values holds M over 4 d of them. <bookmark mark='b'/> Keys and values are each "
            "read once. <bookmark mark='c'/> The queries and the running outputs are read and written once per "
            "tile of keys: T over B c times, about twelve T squared d squared over M numbers in all. "
            "<bookmark mark='d'/> Against the standard method's T squared plus T d, that's smaller whenever d "
            "squared is smaller than M, and Dao and colleagues proved no exact method can do better for every M. "
            "<bookmark mark='e'/> With an H100's shared memory, we counted the numbers moved, running the "
            f"algorithm's loops: {r128:.1f} times fewer with heads of 128, {r64:.1f} times fewer with heads of 64. "
            "<bookmark mark='f'/> FlashAttention-2 in 2023 swapped the loops and trimmed the work between "
            "matrix products; FlashAttention-3, in 2024, overlapped data movement with arithmetic on Hopper GPUs, "
            "reaching 75 percent of the chip's peak."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            self.play(FadeIn(g), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(leg), FadeIn(rl),
                      run_time=2.5)
            vo.wait_until("f")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()
