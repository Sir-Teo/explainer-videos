from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import A_C, B_C, BYTEC, C_C, FLOPC, GPUC, L1C, PART, load, matrix_grid
from videos.ai.ai17.specs import GPUS, TPU1


class Systolic(VoiceoverScene):
    def construct(self):
        self.card()
        self.kung()
        self.wavefront()
        self.count()
        self.tpu()
        self.tensor_cores()

    def card(self):
        card = chapter_card(8, r"Tensor cores and systolic arrays", r"What does a chip built for $C = AB$ look like?",
                            lit=(1978, 2016, 2017), part=PART)
        with self.voiceover("Chapter eight. Tensor cores and systolic arrays."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def kung(self):
        hc = history_card(1978, r"H.~T.~Kung \& Charles Leiserson, \ Carnegie Mellon",
                          r"\textit{systolic arrays}: \ a grid of simple cells; \ data pulses through it like blood "
                          r"through the heart, \ each number used by every cell it passes", width=6.6, color=FLOPC)
        hc.move_to([-3.2, 1.3, 0])
        cells = VGroup(*[Square(0.55, stroke_color=FLOPC, stroke_width=1.5, fill_color=FLOPC, fill_opacity=0.1)
                         for _ in range(25)]).arrange_in_grid(rows=5, cols=5, buff=0.15).move_to([3.6, 0.4, 0])
        mem = Rectangle(width=3.6, height=0.5, stroke_color=BYTEC, fill_color=BYTEC, fill_opacity=0.3)
        mem.next_to(cells, DOWN, buff=0.6)
        ml = label(r"memory: \ read each number once", font_size=20, color=BYTEC).next_to(mem, DOWN, buff=0.1)
        arrows = VGroup(*[Arrow(mem.get_top(), cells[20 + k].get_bottom(), buff=0.05, stroke_width=2, color=BYTEC,
                                max_tip_length_to_length_ratio=0.2) for k in (0, 2, 4)])
        why_ = hc.copy()
        why_ = history_card(1982, r"H.~T.~Kung, \ \textit{Why systolic architectures?}",
                            r"for problems like matrix products, \ the number of operations per memory access can grow "
                            r"without needing more memory bandwidth", width=6.6, color=FLOPC).move_to([-3.2, -1.6, 0])
        with self.voiceover(
            "There's an older idea that suits matrix products even better than a GPU's lanes. <bookmark mark='a'/> "
            "In 1978 H. T. Kung and Charles Leiserson at Carnegie Mellon proposed systolic arrays: a grid of simple "
            "cells, each connected only to its neighbours, with data pulsing through in rhythm, like blood through "
            "the heart. <bookmark mark='b'/> A number read from memory enters at the edge and is used by every cell "
            "it passes, so the memory is read once while the arithmetic happens many times. <bookmark mark='c'/> In "
            "1982 Kung explained why it matters: for problems like matrix products, the operations per memory access "
            "can grow without asking for more bandwidth. The roofline's intensity, built into the wiring."
        ) as vo:
            self.play(FadeIn(cells, lag_ratio=0.02))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(mem), FadeIn(ml), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
            self.play(LaggedStart(*[c_.animate.set_fill(opacity=0.6) for c_ in cells], lag_ratio=0.04),
                      run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(why_, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene(run_time=0.6)

    # ------------------------------------------------------------------
    def wavefront(self):
        s = load("systolic")
        n = int(s["n"])
        A, B, Cr = np.asarray(s["A"]), np.asarray(s["B"]), np.asarray(s["C"])
        acc = np.asarray(s["acc"])
        T = int(s["cycles"])
        size, pitch = 0.85, 1.05
        origin = np.array([0.6, 0.95, 0])  # centre of PE (0, 0)

        def pe_pos(i, j):
            return origin + np.array([j * pitch, -i * pitch, 0])

        pes = VGroup(*[RoundedRectangle(width=size, height=size, corner_radius=0.1, stroke_color=GREY_B,
                                        stroke_width=1.5, fill_color=FLOPC, fill_opacity=0.05).move_to(pe_pos(i, j))
                       for i in range(n) for j in range(n)])
        accs = [[Integer(0, font_size=24, color=C_C).move_to(pe_pos(i, j) + np.array([0.15, -0.18, 0]))
                 for j in range(n)] for i in range(n)]
        acc_g = VGroup(*[a for row in accs for a in row])

        def tok(v, col):
            sq = RoundedRectangle(width=0.36, height=0.32, corner_radius=0.05, stroke_width=0, fill_color=col,
                                  fill_opacity=0.85)
            return VGroup(sq, Integer(int(v), font_size=18, color=BLACK).move_to(sq))

        a_tok = {(i, k): tok(A[i, k], A_C) for i in range(n) for k in range(n)}
        b_tok = {(k, j): tok(B[k, j], B_C) for k in range(n) for j in range(n)}

        def a_pos(i, k, t):
            c = t - i - k
            return pe_pos(i, 0) + np.array([c * pitch - 0.2, 0.15, 0])

        def b_pos(k, j, t):
            r = t - j - k
            return pe_pos(0, j) + np.array([0.2, -r * pitch + 0.26, 0])

        def visible(c):
            return -2 <= c <= n - 1

        left_edge = pe_pos(0, 0)[0] - size / 2 - 0.05
        top_edge = pe_pos(0, 0)[1] + size / 2 + 0.05
        mA = matrix_grid(n, n, 0.36, A_C, fill=0.15).move_to([-5.4, 1.6, 0])
        mB = matrix_grid(n, n, 0.36, B_C, fill=0.15).next_to(mA, DOWN, buff=0.6)
        for i in range(n):
            for k in range(n):
                mA.add(Integer(int(A[i, k]), font_size=16, color=WHITE).move_to(mA.cell(i, k)))
                mB.add(Integer(int(B[i, k]), font_size=16, color=WHITE).move_to(mB.cell(i, k)))
        la, lb = MathTex("A", color=A_C, font_size=30).next_to(mA, LEFT, buff=0.15), \
            MathTex("B", color=B_C, font_size=30).next_to(mB, LEFT, buff=0.15)
        clock = ValueTracker(0)
        ctext = always_redraw(lambda: label(rf"cycle ${int(clock.get_value())}$ of ${T}$", font_size=26,
                                            color=GREY_A).move_to([5.6, 2.6, 0]))
        tag = note(r"computed: \ the array simulated cycle by cycle; \ the result equals numpy's $AB$").to_corner(
            DR, buff=0.2)
        ok = bool(np.array_equal(acc[-1], A @ B))
        done = label(r"$C = AB$ \ \checkmark", font_size=30, color=C_C).move_to([-4.9, -2.6, 0])
        end = ("The result matches the product computed by numpy, exactly." if ok else
               "The result is checked against numpy's product.")

        def positions(t):
            anims = []
            for (i, k), m in a_tok.items():
                c = t - i - k
                if visible(c):
                    anims.append(m.animate.move_to(a_pos(i, k, t)).set_opacity(1))
                else:
                    anims.append(m.animate.move_to(a_pos(i, k, t)).set_opacity(0))
            for (k, j), m in b_tok.items():
                r = t - j - k
                if visible(r):
                    anims.append(m.animate.move_to(b_pos(k, j, t)).set_opacity(1))
                else:
                    anims.append(m.animate.move_to(b_pos(k, j, t)).set_opacity(0))
            return anims

        for (i, k), m in a_tok.items():
            m.move_to(a_pos(i, k, -1)).set_opacity(1 if visible(-1 - i - k) else 0)
        for (k, j), m in b_tok.items():
            m.move_to(b_pos(k, j, -1)).set_opacity(1 if visible(-1 - j - k) else 0)
        with self.voiceover(
            "Here's one computing a product, cycle by cycle, simulated. <bookmark mark='a'/> A four by four grid "
            "of cells, each holding a running sum. The rows of A come in from the left, the columns of B from the "
            "top, each one staggered a cycle behind the last. <bookmark mark='b'/> Every cycle, each cell "
            "multiplies the two numbers passing through it, adds the product to its sum, and hands the A number to "
            "the right and the B number down. <bookmark mark='c'/> Watch the active cells: a diagonal front sweeps "
            f"across the grid. <bookmark mark='d'/> After {T} cycles every cell holds one entry of C. " + end
        ) as vo:
            self.play(FadeIn(pes), FadeIn(acc_g), FadeIn(mA), FadeIn(mB), FadeIn(la), FadeIn(lb), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(m) for m in list(a_tok.values()) + list(b_tok.values())], FadeIn(ctext))
            vo.wait_until("b")
            for t in range(T):
                clock.set_value(t + 1)
                active = [(i, j) for i in range(n) for j in range(n) if 0 <= t - i - j < n]
                anims = positions(t)
                anims += [pes[i * n + j].animate.set_fill(FLOPC, opacity=0.45 if (i, j) in active else 0.05)
                          for i in range(n) for j in range(n)]
                self.play(*anims, run_time=0.8)
                new = [Integer(int(acc[t, i, j]), font_size=24, color=C_C).move_to(accs[i][j]) for i in range(n)
                       for j in range(n)]
                self.play(*[Transform(accs[i][j], new[i * n + j]) for i in range(n) for j in range(n)
                            if acc[t, i, j] != (acc[t - 1, i, j] if t else 0)], run_time=0.35)
                if t == 3:
                    vo.wait_until("c")
            self.play(*positions(T), *[p_.animate.set_fill(C_C, opacity=0.15) for p_ in pes], run_time=0.6)
            vo.wait_until("d")
            self.play(FadeIn(done, scale=1.2))
        ctext.clear_updaters()
        self.wait(0.3)
        self.clear_scene(run_time=0.6)

    # ------------------------------------------------------------------
    def count(self):
        colors = {r"t": FLOPC, r"K": A_C, r"n": GPUC}
        rows = [
            cmath(r"t", r"=", r"i + j + k", colors=colors, font_size=40),
            cmath(r"t_{\text{last}}", r"=", r"(n-1) + (n-1) + (K-1)", colors=colors, font_size=40),
            cmath(r"\text{cycles}", r"=", r"K + 2n - 2", colors=colors, font_size=40),
            cmath(r"\text{reads per operation}", r"=", r"\frac{2nK}{n^2 K}", r"=", r"\frac{2}{n}", colors=colors,
                  font_size=38),
        ]
        whys = [why(r"cell $(i, j)$ meets $a_{ik}$ and $b_{kj}$ at cycle $t$: \ the skew"),
                why(r"the last cell, \ the last term"), why(r"$= 10$ for our $4 \times 4$ example"),
                why(r"each number read once, \ used by $n$ cells")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.45, edge=6.8)
        # the skew, cell by cell: the cycle at which each cell of a 4 x 4 array receives its first term
        cells = VGroup()
        for i in range(4):
            for j in range(4):
                sq = Square(0.5, stroke_color=GREY_B, stroke_width=1.5, fill_color=FLOPC,
                            fill_opacity=0.12 + 0.1 * (i + j)).move_to([-5.2 + 0.58 * j, -1.45 - 0.58 * i, 0])
                cells.add(VGroup(sq, MathTex(str(i + j), font_size=26, color=WHITE).move_to(sq)))
        cap = label(r"cell $(i, j)$ gets its first term at cycle $i + j$: \ the diagonals are the wavefront",
                    font_size=22, color=GREY_A).next_to(cells, RIGHT, buff=0.5).align_to(cells, UP)
        cap2 = label(r"the far corner's last term: \ cycle $6 + (K - 1) = 9$, \ so $10$ cycles in all", font_size=22,
                     color=FLOPC).next_to(cap, DOWN, aligned_edge=LEFT, buff=0.3)
        ring = SurroundingRectangle(cells[-1], color=FLOPC, buff=0.04, stroke_width=3)
        with self.voiceover(
            "Why does it work? <bookmark mark='a'/> Because of the stagger, cell i, j meets a i k and b k j at cycle "
            "i plus j plus k: exactly the terms of its entry, each once. <bookmark mark='b'/> The last term reaches "
            "the far corner at cycle two n minus two plus K minus one, <bookmark mark='c'/> so the product takes K "
            "plus two n minus two cycles: ten for our example. <bookmark mark='d'/> And each number is read from "
            "memory once and used by n cells, so the memory traffic per operation falls like one over n. A bigger "
            "array is a bigger tile, with no cache needed: the reuse is in the wires."
        ) as vo:
            step(0)
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.05), FadeIn(cap), run_time=1.5)
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                step(k + 1)
                if mk == "b":
                    self.play(Create(ring), FadeIn(cap2))
        self.wait(0.3)
        self.clear_scene(run_time=0.6)

    # ------------------------------------------------------------------
    def tpu(self):
        s = load("systolic")
        d, util = np.asarray(s["d"]), np.asarray(s["util"])
        tops = TPU1["macs"] * 2 * TPU1["mhz"] * 1e6
        hc = history_card(2016, r"Google's Tensor Processing Unit \ (Jouppi et al.)",
                          rf"a $256 \times 256$ systolic array of $8$-bit multiply-adds at ${TPU1['mhz']}$ MHz: \ "
                          rf"$65{{,}}536 \times 2 \times 0.7 \times 10^9 \approx {tops / 1e12:.0f}$ trillion operations a "
                          r"second; \ in Google's data centres since 2015", width=6.4, color=GPUC, font_size=20)
        hc.move_to([-3.4, 1.6, 0])
        facts = VGroup(label(r"ran AlphaGo against Lee Sedol, March 2016", font_size=22, color=GREY_A),
                       label(r"$15$--$30\times$ faster than the GPU and CPU beside it", font_size=22, color=GREY_A),
                       label(r"$30$--$80\times$ more operations per watt", font_size=22, color=GREY_A))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(hc, DOWN, buff=0.35).align_to(hc, LEFT)
        g = axes([0, 1024], [0, 1.05], x_length=5.2, y_length=3.0, xlabel=r"layer size $d$ \ ($d \times d$ weights)",
                 ylabel=r"cells doing useful work", xticks=[0, 256, 512, 768, 1024], yticks=[0, 0.5, 1],
                 yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.6, 0.3, 0])
        cv = curve(g.ax, d, util, GPUC, 3)
        k257 = int(np.argmin(np.abs(d - 257)))
        dot = glow_dot(g.ax.c2p(257, util[k257]), color=C.SURPRISE)
        dl = label(rf"$d = 257$: \ ${100 * util[k257]:.0f}\%$", font_size=20, color=C.SURPRISE).next_to(dot, UP, buff=0.15)
        tag = note(r"computed: \ weights padded to whole $256 \times 256$ tiles").to_corner(DR, buff=0.2)
        cite_ = cite(r"N.~Jouppi et al., \ ISCA (2017); \ Google blog (May 2016)", corner=DL)
        # the chip's heart, drawn small: a 256 x 256 grid of multiply-adders (16 x 16 here, each standing for 16 x 16)
        arr = VGroup(*[Square(0.17, stroke_width=0.6, stroke_color=GPUC, fill_color=GPUC, fill_opacity=0.35)
                       for _ in range(256)]).arrange_in_grid(rows=16, cols=16, buff=0.03).move_to([3.6, 0.5, 0])
        feed = VGroup(Arrow(arr.get_left() + LEFT * 0.9, arr.get_left(), buff=0.05, color=A_C, stroke_width=3),
                      Arrow(arr.get_top() + UP * 0.7, arr.get_top(), buff=0.05, color=B_C, stroke_width=3))
        arl = VGroup(label(r"$256 \times 256$ multiply-adders, \ $8$-bit", font_size=22, color=GPUC),
                     label(rf"$700$ MHz: \ $\approx {tops / 1e12:.0f}$ trillion operations a second", font_size=22,
                           color=FLOPC)).arrange(DOWN, buff=0.12).next_to(arr, DOWN, buff=0.3)
        atag = schematic_tag(corner=UR)
        with self.voiceover(
            "In 2013 Google projected that if people used voice search for three minutes a day, the speech "
            "recognition networks alone would need twice its data centres. It built a chip instead, in fifteen "
            "months. <bookmark mark='a'/> The "
            "Tensor Processing Unit is a systolic array of 256 by 256 eight-bit multiply-adders, running at 700 "
            f"megahertz: about {tops / 1e12:.0f} trillion operations a second. It was in Google's data centres from "
            "2015, and it ran AlphaGo in its match against Lee Sedol. <bookmark mark='b'/> On Google's own "
            "workloads it was fifteen to thirty times faster than the CPU and GPU next to it, and thirty to eighty "
            "times better per watt. <bookmark mark='c'/> The price of a big fixed grid: work comes in whole tiles. "
            "A layer of 257 by 257 weights fills four tiles and uses a quarter of the cells. Shapes that are "
            "multiples of the array's size are the ones that run at full speed, on TPUs and GPUs alike."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(cite_), FadeIn(arr, lag_ratio=0.002), FadeIn(atag),
                      run_time=0.8)
            vo.wait_until("a")
            self.play(GrowArrow(feed[0]), GrowArrow(feed[1]), FadeIn(arl[0]))
            self.play(FadeIn(arl[1]), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f_) for f_ in facts[1:]], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(arr, feed, arl, atag)))
            self.play(FadeIn(g))
            self.play(Create(cv), FadeIn(tag), run_time=2.0)
            self.play(FadeIn(dot), FadeIn(dl))
        self.wait(0.3)
        self.clear_scene(run_time=0.6)

    # ------------------------------------------------------------------
    def tensor_cores(self):
        V = GPUS["V100"]
        mA = matrix_grid(4, 4, 0.34, A_C, fill=0.4).move_to([-5.0, 0.8, 0])
        mB = matrix_grid(4, 4, 0.34, B_C, fill=0.4).move_to([-3.0, 0.8, 0])
        mC = matrix_grid(4, 4, 0.34, C_C, fill=0.4).move_to([-1.0, 0.8, 0])
        mD = matrix_grid(4, 4, 0.34, C_C, fill=0.8).move_to([1.4, 0.8, 0])
        ops = VGroup(MathTex(r"\times", font_size=36).move_to([-4.0, 0.8, 0]),
                     MathTex(r"+", font_size=36).move_to([-2.0, 0.8, 0]),
                     MathTex(r"=", font_size=36).move_to([0.2, 0.8, 0]))
        names = VGroup(MathTex("A", color=A_C, font_size=28).next_to(mA, DOWN, buff=0.15),
                       MathTex("B", color=B_C, font_size=28).next_to(mB, DOWN, buff=0.15),
                       MathTex("C", color=C_C, font_size=28).next_to(mC, DOWN, buff=0.15),
                       MathTex("D", color=C_C, font_size=28).next_to(mD, DOWN, buff=0.15))
        one = label(r"one tensor core, \ one clock: \ $4 \times 4 \times 4 = 64$ multiply-adds", font_size=26,
                    color=FLOPC).move_to([-1.8, 2.5, 0])
        peak = label(rf"V100 (2017): \ $640$ tensor cores $\times$ $64$ $\times$ $2$ $\times$ $1.53$ GHz $\approx "
                     rf"{640 * 64 * 2 * 1.53e9 / 1e12:.0f}$ TFLOP/s", font_size=24, color=GPUC).move_to([0, -1.0, 0])
        gens = VGroup(
            label(r"A100 (2020): \ TF32, \ BF16, \ 2:4 sparsity", font_size=22, color=GREY_A),
            label(r"H100 (2022): \ FP8, \ a warp group feeds one big multiply", font_size=22, color=GREY_A),
            label(r"Blackwell (2024): \ FP4 \ and two dies as one GPU", font_size=22, color=GREY_A),
            label(r"Rubin (2026): \ NVFP4 at $35$ PFLOP/s per GPU \ (dense)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.0, -2.6, 0])
        cite_ = cite(r"NVIDIA Volta whitepaper (2017); \ datasheets", corner=DL)
        with self.voiceover(
            "GPUs took the hint in 2017. <bookmark mark='a'/> NVIDIA's Volta added tensor cores: units that take "
            "two four by four matrices and add their product to a third, all in one clock. Sixty-four multiply-adds "
            "per instruction, instead of one. <bookmark mark='b'/> A V100 has 640 of them, which gives "
            f"its {V['tensor'] / 1e12:.0f} trillion operations a second in half precision, eight times its ordinary "
            "lanes. <bookmark mark='c'/> Every generation since has made the tensor cores bigger and their numbers "
            "smaller: TF32 and bfloat16 in the A100, eight-bit floats in the H100, four-bit in Blackwell and in "
            "Rubin. The GPU is still a GPU, but most of its arithmetic now happens in small systolic engines inside "
            "it."
        ) as vo:
            self.play(FadeIn(mA), FadeIn(mB), FadeIn(mC), FadeIn(ops), FadeIn(names), FadeIn(cite_), run_time=0.7)
            vo.wait_until("a")
            self.play(TransformFromCopy(VGroup(mA, mB, mC), mD), FadeIn(one))
            vo.wait_until("b")
            self.play(FadeIn(peak, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.1) for g_ in gens], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene(run_time=0.6)
