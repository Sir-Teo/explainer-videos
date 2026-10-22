from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (A_C, B_C, BYTEC, C_C, CPUC, FLOPC, L1C, L2C, PART, box_label, gflops, load,
                                   matrix_grid)
from videos.ai.ai17.specs import GPT3_CFG, GPT3_FLOP


class Matmul(VoiceoverScene):
    def construct(self):
        self.card()
        self.where()
        self.flops()
        self.traffic()
        self.tiling()
        self.measured()

    def card(self):
        card = chapter_card(5, r"Matrix multiply is the workload", r"Where does a model's arithmetic go?",
                            lit=(2017, 2020), part=PART)
        with self.voiceover("Chapter five. Matrix multiply is the workload."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def where(self):
        d, L, T, N = GPT3_CFG["d"], GPT3_CFG["layers"], GPT3_CFG["ctx"], GPT3_CFG["params"]
        w = 2 * N  # forward FLOPs per token in the weight matrices (Kaplan et al. 2020)
        att = 2 * L * T * d  # attention's own products, q.k and the weighted sum of values
        other = L * (4 * d * 8 + 5 * T * (d // 128))  # layer norms, GELU, softmax: a generous count
        tot = w + att + other
        parts = [(w / tot, A_C, r"weight matrices"), (att / tot, B_C, r"attention's products"),
                 (other / tot, GREY_B, r"everything else")]
        bar_w = 11.0
        x = -bar_w / 2
        segs = VGroup()
        for frac, col, _ in parts:
            wd = max(bar_w * frac, 0.03)
            segs.add(Rectangle(width=wd, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.9)
                     .move_to([x + wd / 2, 0.6, 0]))
            x += wd
        labs = VGroup(
            label(rf"weight matrices: \ ${100 * parts[0][0]:.1f}\%$", font_size=26, color=A_C).next_to(segs[0], DOWN,
                                                                                                    buff=0.3),
            label(rf"attention: \ ${100 * parts[1][0]:.1f}\%$", font_size=24, color=B_C)
            .next_to(segs[1], UP, buff=0.3).shift(LEFT * 1.0),
            label(rf"everything else: \ ${100 * parts[2][0]:.2f}\%$", font_size=22, color=GREY_B)
            .next_to(segs[2], DOWN, buff=1.0).shift(LEFT * 1.2),
        )
        head = label(r"GPT-3, \ forward pass, \ arithmetic per token", font_size=30).to_edge(UP, buff=0.6)
        outline = Rectangle(width=bar_w, height=0.8, stroke_color=GREY_C, stroke_width=1.5).move_to([0, 0.6, 0])
        nw = label(r"$175$ billion weights, \ $96$ layers, \ width $12{,}288$", font_size=24, color=GREY_A)
        nw.next_to(outline, UP, buff=0.5)
        rule = cmath(r"\text{training} \approx 6\,N\,D", r"=", r"6 \times 175 \times 10^9 \times 300 \times 10^9",
                     r"\approx", rf"{6 * N * 300e9 / 1e23:.2f} \times 10^{{23}}", font_size=32)
        rule.to_edge(DOWN, buff=0.9)
        pub = label(rf"published: \ ${GPT3_FLOP / 1e23:.2f} \times 10^{{23}}$ FLOP", font_size=22, color=GREY_B)
        pub.next_to(rule, DOWN, buff=0.15)
        cite_ = cite(r"Brown et al.\ (2020); \ Kaplan et al.\ (2020)", corner=DR)
        tag = note(r"computed from GPT-3's published shape").to_corner(DL, buff=0.2)
        with self.voiceover(
            "Why are GPUs so good for neural networks in particular? Because almost all of a network's arithmetic "
            "is one operation. <bookmark mark='a'/> Take GPT-3. For every token, each of its 175 billion weights is "
            "used in one multiply and one add: two operations per weight, all of them in matrix products. "
            f"<bookmark mark='b'/> Attention's own products, queries against keys, add {100 * parts[1][0]:.1f} "
            "percent. <bookmark mark='c'/> Everything else, the normalizations, the activations, the softmax, is a "
            "rounding error, even counted generously. <bookmark mark='d'/> Training does the forward pass and a "
            "backward pass twice as expensive: six operations per weight per token. Six times 175 billion "
            "parameters times 300 billion tokens gives GPT-3's published compute, to within a fraction of a "
            "percent. To make AI faster, make matrix multiplication faster."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cite_), FadeIn(tag), Create(outline), FadeIn(nw))
            vo.wait_until("a")
            self.play(GrowFromEdge(segs[0], LEFT), FadeIn(labs[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(segs[1], LEFT), FadeIn(labs[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(segs[2], LEFT), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(Write(rule), FadeIn(pub))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layout(self, n=6, cell=0.36, center=(0, 0, 0)):
        A = matrix_grid(n, n, cell, A_C, fill=0.1)
        B = matrix_grid(n, n, cell, B_C, fill=0.1)
        Cm = matrix_grid(n, n, cell, C_C, fill=0.08)
        Cm.move_to(center)
        A.next_to(Cm, LEFT, buff=0.3)
        B.next_to(Cm, UP, buff=0.3)
        return A, B, Cm

    def flops(self):
        A, B, Cm = self.layout(n=6, cell=0.36, center=(-2.6, -1.2, 0))
        names = VGroup(MathTex("A", color=A_C, font_size=36).next_to(A, LEFT, buff=0.2),
                       MathTex("B", color=B_C, font_size=36).next_to(B, LEFT, buff=0.2),
                       MathTex("C", color=C_C, font_size=36).next_to(Cm, DOWN, buff=0.2))
        i, j = 2, 4
        row = SurroundingRectangle(VGroup(*[A.cell(i, k) for k in range(6)]), color=A_C, buff=0.02, stroke_width=3)
        col = SurroundingRectangle(VGroup(*[B.cell(k, j) for k in range(6)]), color=B_C, buff=0.02, stroke_width=3)
        cij = Cm.cell(i, j).copy().set_fill(C_C, opacity=0.9)
        colors = {r"C_{ij}": C_C, r"A_{ik}": A_C, r"B_{kj}": B_C, r"A": A_C, r"B": B_C, r"C": C_C}
        rows = [
            cmath(r"C_{ij}", r"=", r"\sum_{k=1}^{K}", r"A_{ik}", r"B_{kj}", colors=colors, font_size=40),
            cmath(r"\text{per entry}", r"=", r"K \text{ multiplies} + (K - 1) \text{ adds}", font_size=32),
            cmath(r"\text{FLOPs}(C = AB)", r"=", r"M N \cdot 2K", r"=", r"2MNK", font_size=36),
        ]
        whys = [why(r"row $i$ of $A$ against column $j$ of $B$"), why(r"$\approx 2K$ operations"),
                why(r"$MN$ entries, \ $A$ is $M \times K$, \ $B$ is $K \times N$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=2.6, buff=0.5, edge=6.9)
        with self.voiceover(
            "So let's count. <bookmark mark='a'/> Each entry of C is a row of A dotted with a column of B. "
            "<bookmark mark='b'/> With K terms, that's K multiplies and K minus one adds: about 2K operations. "
            "<bookmark mark='c'/> There are M times N entries, so the whole product costs 2MNK floating-point "
            "operations. For square matrices of size n: 2 n cubed. Double the size, eight times the work."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(Cm), FadeIn(names))
            step(0)
            vo.wait_until("a")
            self.play(Create(row), Create(col))
            self.play(TransformFromCopy(VGroup(row, col), cij))
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(LaggedStart(*[Cm.cells[q].animate.set_fill(C_C, opacity=0.6) for q in range(36)],
                                  lag_ratio=0.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def traffic(self):
        colors = {r"I": FLOPC}
        rows = [
            cmath(r"I", r"=", r"\frac{\text{FLOPs}}{\text{bytes moved}}", colors=colors, font_size=40),
            cmath(r"I_{\text{naive}}", r"=", r"\frac{2}{2 \times 4}", r"=", r"\tfrac14", font_size=38),
            cmath(r"I_{\text{best}}", r"=", r"\frac{2n^3}{3n^2 \times 4}", r"=", r"\frac{n}{6}", font_size=38),
        ]
        rows[1][0].set_color(FLOPC)
        rows[2][0].set_color(FLOPC)
        whys = [why(r"arithmetic intensity"),
                why(r"each multiply-add fetches $A_{ik}$ and $B_{kj}$: \ two $4$-byte numbers"),
                why(r"read $A$ and $B$ once, \ write $C$ once")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.5, buff=0.55, edge=6.8)
        n = 1024
        ex = label(rf"$n = {n:,}$: \ ${n / 6:.0f}$ FLOPs per byte, \ every number used ${n:,}$ times".replace(",", "{,}"),
                   font_size=28, color=FLOPC).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "The arithmetic is only half the cost. The numbers have to come from memory. <bookmark mark='a'/> The "
            "ratio of operations to bytes moved is called the arithmetic intensity. <bookmark mark='b'/> Done "
            "naively, every multiply-add fetches its two numbers, four bytes each in single precision: two "
            "operations for eight bytes, a quarter of an operation per byte. <bookmark mark='c'/> But the whole "
            "product only needs A and B read once and C written once: three n squared numbers for 2 n cubed "
            "operations. The intensity grows like n over six. <bookmark mark='d'/> For n of a thousand and "
            "twenty-four, that's about 170 operations per byte. Each number is used a thousand times. The whole "
            "game is to use it a thousand times while it's close by, instead of fetching it a thousand times."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1, transform=False)
            vo.wait_until("c")
            step(2, transform=False)
            vo.wait_until("d")
            self.play(FadeIn(ex, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tiling(self):
        n, b = 12, 4
        A, B, Cm = self.layout(n=n, cell=0.22, center=(0.5, -1.5, 0))
        names = VGroup(MathTex("A", color=A_C, font_size=32).next_to(A, LEFT, buff=0.15),
                       MathTex("B", color=B_C, font_size=32).next_to(B, LEFT, buff=0.15),
                       MathTex("C", color=C_C, font_size=32).next_to(Cm, DOWN, buff=0.15))
        fast = RoundedRectangle(width=3.2, height=4.4, corner_radius=0.15, stroke_color=L1C, stroke_width=2)
        fast.move_to([5.0, 0.2, 0])
        fl = label(r"fast memory", font_size=24, color=L1C).next_to(fast, UP, buff=0.12)
        slots = [fast.get_top() + DOWN * (0.85 + 1.35 * k) for k in range(3)]

        def tile(M, ti, tj, col, op=0.55):
            return VGroup(*[M.cell(ti * b + u, tj * b + v).copy().set_fill(col, opacity=op)
                            for u in range(b) for v in range(b)])

        colors = {r"b": FLOPC, r"I": FLOPC, r"M": L1C}
        rows = [
            cmath(r"I_{\text{tile}}", r"=", r"\frac{2b^3}{2b^2 \times 4}", r"=", r"\frac{b}{4}", colors=colors,
                  font_size=34),
            cmath(r"3b^2", r"\le", r"M", colors=colors, font_size=34),
        ]
        rows[0][0].set_color(FLOPC)
        whys = [why(r"$b^3$ multiply-adds per pair of tiles", font_size=22), why(r"three tiles must fit", font_size=22)]
        blocks = VGroup(*[VGroup(r_, w_).arrange(DOWN, aligned_edge=LEFT, buff=0.12) for r_, w_ in zip(rows, whys)])
        blocks.arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_corner(UL, buff=0.45)
        hk = history_card(1981, r"Hong Jia-Wei \& H.~T.~Kung", r"no order of operations can move fewer than about "
                          r"$n^3/\sqrt{M}$ numbers", width=5.0, color=L1C, font_size=20)
        hk.to_corner(UL, buff=0.3)
        with self.voiceover(
            "That's what tiling does. <bookmark mark='a'/> Cut C into b by b tiles. To compute one tile, walk along "
            "a strip of A and a strip of B, one b by b tile of each at a time. <bookmark mark='b'/> Bring the two "
            "tiles into fast memory, multiply them, add into the tile of C, and move on. <bookmark mark='c'/> Every "
            "number brought in is used b times, so the intensity is b over four bytes. <bookmark mark='d'/> The "
            "limit is the fast memory: three tiles have to fit. Bigger fast memory, bigger tiles, more reuse. "
            "<bookmark mark='e'/> In 1981 Hong Jia-Wei and H. T. Kung proved that no schedule can do much better: "
            "any way of computing the product moves at least on the order of n cubed over the square root of the "
            "fast memory's size."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(Cm), FadeIn(names), Create(fast), FadeIn(fl))
            vo.wait_until("a")
            ctile = tile(Cm, 0, 0, C_C, 0.6)
            self.play(FadeIn(ctile))
            vo.wait_until("b")
            for kk in range(3):
                ta, tb = tile(A, 0, kk, A_C), tile(B, kk, 0, B_C)
                self.play(FadeIn(ta), FadeIn(tb), run_time=0.4)
                ca, cb = ta.copy(), tb.copy()
                self.play(ca.animate.scale(1.3).move_to(slots[0]), cb.animate.scale(1.3).move_to(slots[1]),
                          run_time=0.7)
                if kk == 0:
                    cc = ctile.copy()
                    self.play(cc.animate.scale(1.3).move_to(slots[2]), run_time=0.5)
                self.play(Indicate(cc, color=C_C, scale_factor=1.05), Indicate(ctile, color=C_C), run_time=0.5)
                self.play(FadeOut(ca), FadeOut(cb), FadeOut(ta), FadeOut(tb), run_time=0.3)
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(Write(rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(hk, shift=DOWN * 0.1), *[FadeOut(r_) for r_ in rows], *[FadeOut(w_) for w_ in whys])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        r = load("blocking")
        m = load("machine")
        tiles = np.asarray(r["tiles"])
        blk = np.asarray(r["blocked"])
        kb = int(np.argmax(blk))
        best_b = int(tiles[kb])
        vals = [r["naive"], r["ikj"], blk[kb], r["blas"]]
        names = [r"textbook loop", r"loops reordered", rf"tiled, $b = {best_b}$", r"BLAS library"]
        cols = [C.SURPRISE, B_C, FLOPC, CPUC]
        lo, hi = -1.0, math.log10(max(vals) / 1e9) + 0.4
        ax = axes([0, 4], [lo, hi], x_length=6.0, y_length=4.0, ylabel=r"GFLOP/s \ (log scale)",
                  yticks=list(range(int(math.ceil(lo)), int(math.floor(hi)) + 1)),
                  yfmt=lambda v: {-1: "0.1", 0: "1", 1: "10", 2: "100", 3: r"1{,}000"}.get(int(v), f"10^{{{int(v)}}}"),
                  center=[-3.2, 0.0, 0])
        bars = VGroup()
        for k, (v, c_) in enumerate(zip(vals, cols)):
            y = math.log10(v / 1e9)
            p0, p1 = ax.ax.c2p(k + 0.5, lo), ax.ax.c2p(k + 0.5, y)
            bars.add(Rectangle(width=0.9, height=p1[1] - p0[1], stroke_width=0, fill_color=c_, fill_opacity=0.9)
                     .move_to((p0 + p1) / 2))
        vl = VGroup(*[label(rf"${gflops(v)}$", font_size=22, color=c_).next_to(b_, UP, buff=0.08)
                      for v, b_, c_ in zip(vals, bars, cols)])
        nl = VGroup(*[label(t, font_size=18, color=c_).rotate(0.0).next_to(ax.ax.c2p(k + 0.5, lo), DOWN, buff=0.15)
                      for k, (t, c_) in enumerate(zip(names, cols))])
        for k, t in enumerate(nl):
            if t.width > 1.45:
                t.width = 1.45
        # the tile sweep
        g = axes([math.log2(tiles[0]) - 0.3, math.log2(tiles[-1]) + 0.3], [0, max(blk) / 1e9 * 1.25], x_length=5.2,
                 y_length=3.4, xlabel=r"tile size $b$", ylabel=r"GFLOP/s, \ tiled", xticks=[math.log2(t) for t in tiles],
                 xfmt=lambda v: f"{int(round(2 ** v))}", yticks=[0, 10 * math.floor(max(blk) / 1e10)],
                 center=[3.6, -0.4, 0])
        pts = [g.ax.c2p(math.log2(t), v / 1e9) for t, v in zip(tiles, blk)]
        cv = VMobject(color=FLOPC, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.06, color=FLOPC) for p in pts])
        l2 = m["caches"].get("L2", {}).get("kib", 0) * 1024
        l1 = m["caches"].get("L1", {}).get("kib", 0) * 1024
        ws = 3 * best_b * best_b * 4
        marks = VGroup()
        for size, nm, col in ((l1, "L1", L1C), (l2, "L2", L2C)):
            if size:
                bb = math.sqrt(size / 12)  # the tile whose three copies fill this cache
                x = g.ax.c2p(math.log2(bb), 0)[0]
                ln = DashedLine([x, g.ax.c2p(0, 0)[1], 0], [x, g.ax.c2p(0, max(blk) / 1e9 * 1.2)[1], 0], color=col,
                                dash_length=0.08)
                marks.add(VGroup(ln, label(rf"3 tiles fill {nm}", font_size=16, color=col).next_to(ln, UP, buff=0.05)))
        tag = note(rf"computed: \ $n = {int(r['n'])}$, \ one core, \ {r['lang']}").to_corner(DR, buff=0.2)
        speed_tile = blk[kb] / r["naive"]
        speed_blas = r["blas"] / r["naive"]
        where = (f"three {best_b} by {best_b} tiles take {ws / 1024:.0f} kilobytes, which fits in the "
                 f"{l2 / 1024:.0f}-kilobyte second-level cache" if l2 and ws <= l2 else
                 f"three {best_b} by {best_b} tiles take {ws / 1024:.0f} kilobytes")
        past = (". Past that, the tiles spill out and the speed falls." if kb < len(tiles) - 1 else
                ", the largest we tried.")
        how = ("in C." if r["lang"] == "C" else
               "in Python, with numpy doing the innermost loop: this computer has no C compiler.")
        with self.voiceover(
            "We measured this on one core of this computer, multiplying two matrices of size 1,024 " + how + " "
            f"<bookmark mark='a'/> The textbook triple loop: {gflops(r['naive'])} billion operations a second. It "
            "walks down the columns of B, one cache line per number. <bookmark mark='b'/> The same arithmetic with "
            f"the loops reordered, so every inner loop walks along rows: {gflops(r['ikj'])}. "
            f"<bookmark mark='c'/> Tiled: {gflops(blk[kb])}, {speed_tile:.0f} times the textbook loop. "
            f"<bookmark mark='d'/> The best tile size was {best_b}: " + where + past + " "
            "<bookmark mark='e'/> And the BLAS library numpy calls, tuned by experts, with "
            f"tiles inside tiles and hand-written vector code: {gflops(r['blas'])}, {speed_blas:.0f} times the "
            "textbook loop, for exactly the same arithmetic."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(g))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(bars[k], DOWN), FadeIn(vl[k]), FadeIn(nl[k]))
                if k == 2:
                    self.play(Create(cv), FadeIn(dots), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(marks), Indicate(dots[kb], scale_factor=2.0))
            vo.wait_until("e")
            self.play(GrowFromEdge(bars[3], DOWN), FadeIn(vl[3]), FadeIn(nl[3]))
        self.wait(0.3)
        self.clear_scene()
