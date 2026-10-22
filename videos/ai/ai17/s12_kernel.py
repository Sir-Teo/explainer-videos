from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (A_C, B_C, BYTEC, C_C, FLOPC, GPUC, L1C, PART, REGC, WARPC, code_lines, load,
                                   matrix_grid)
from videos.ai.ai17.specs import CC90, GPUS


class Kernel(VoiceoverScene):
    def construct(self):
        self.card()
        self.tiled()
        self.occupancy()
        self.triton()
        self.flash()

    def card(self):
        card = chapter_card(11, r"Writing a kernel", r"What does fast GPU code look like?", lit=(2007,), part=PART)
        with self.voiceover("Chapter eleven. Writing a kernel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def tiled(self):
        code = code_lines([
            "__global__ void matmul(const float *A, const float *B,",
            "                       float *C, int n) {",
            "    __shared__ float As[T][T], Bs[T][T];",
            "    int tx = threadIdx.x, ty = threadIdx.y;",
            "    int row = blockIdx.y * T + ty, col = blockIdx.x * T + tx;",
            "    float acc = 0.0f;",
            "    for (int t = 0; t < n / T; t++) {",
            "        As[ty][tx] = A[row * n + t * T + tx];",
            "        Bs[ty][tx] = B[(t * T + ty) * n + col];",
            "        __syncthreads();",
            "        for (int k = 0; k < T; k++) acc += As[ty][k] * Bs[k][tx];",
            "        __syncthreads();",
            "    }",
            "    C[row * n + col] = acc;",
            "}",
        ], font_size=15, buff=0.1)
        code.to_corner(UL, buff=0.35)
        if code.get_right()[0] > 0.4:
            code.scale((0.4 - code.get_left()[0]) / code.width, about_edge=UL)
        hl_smem = SurroundingRectangle(code[2], color=L1C, buff=0.04, stroke_width=2)
        hl_load = SurroundingRectangle(VGroup(code[7], code[8]), color=BYTEC, buff=0.04, stroke_width=2)
        hl_math = SurroundingRectangle(code[10], color=FLOPC, buff=0.04, stroke_width=2)
        hl_sync = VGroup(SurroundingRectangle(code[9], color=WARPC, buff=0.03, stroke_width=2),
                         SurroundingRectangle(code[11], color=WARPC, buff=0.03, stroke_width=2))
        n = 8
        Cm = matrix_grid(n, n, 0.26, C_C, fill=0.06).move_to([4.3, -1.45, 0])
        Am = matrix_grid(n, n, 0.26, A_C, fill=0.06).next_to(Cm, LEFT, buff=0.25)
        Bm = matrix_grid(n, n, 0.26, B_C, fill=0.06).next_to(Cm, UP, buff=0.25)
        blk = VGroup(*[Cm.cell(i, j) for i in range(2, 4) for j in range(4, 6)])
        blk_box = SurroundingRectangle(blk, color=C_C, buff=0.0, stroke_width=3)
        bl = label(r"one thread block: \ one $T \times T$ tile of $C$, \\ one thread per entry", font_size=20,
                   color=C_C).next_to(Cm, DOWN, buff=0.2)
        colors = {r"T": FLOPC}
        inten = cmath(r"I", r"=", r"\frac{2T^3}{2T^2 \times 4}", r"=", r"\frac{T}{4}", colors=colors, font_size=30)
        inten.move_to([-4.6, -1.65, 0])
        H = GPUS["H100"]
        il = label(rf"$T = 32$: \ $8$ FLOP/byte, \ below an H100's FP32 ridge of ${H['fp32'] / H['bw']:.0f}$",
                   font_size=20, color=GREY_A).next_to(inten, DOWN, buff=0.3).align_to(inten, LEFT)
        with self.voiceover(
            "Here is chapter five's tiling, written for a GPU, the way textbooks teach it. <bookmark mark='a'/> "
            "Each block of threads computes one T by T tile of C, one thread per entry. <bookmark mark='b'/> The "
            "block declares two tiles of shared memory, the programmer-managed SRAM of chapter six. "
            "<bookmark mark='c'/> In each round, every thread copies one number of A and one of B from global "
            "memory into the shared tiles: neighbouring threads, neighbouring addresses, coalesced. "
            "<bookmark mark='d'/> The threads wait for each other, then each does T multiply-adds out of shared "
            "memory, and waits again before the tiles are overwritten. <bookmark mark='e'/> Every number fetched "
            "from global memory is used T times: the intensity is T over four. With tiles of thirty-two, that's "
            "eight operations per byte, still below an H100's ridge. Real kernels go further: each thread keeps a "
            "small tile of its own in registers, and the multiply-adds go to the tensor cores."
        ) as vo:
            self.play(FadeIn(code), FadeIn(Am), FadeIn(Bm), FadeIn(Cm))
            vo.wait_until("a")
            self.play(Create(blk_box), *[c_.animate.set_fill(C_C, opacity=0.5) for c_ in blk], FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(hl_smem))
            vo.wait_until("c")
            self.play(Create(hl_load))
            for t in range(4):
                ta = VGroup(*[Am.cell(i, 2 * t + u).copy().set_fill(A_C, opacity=0.7) for i in (2, 3) for u in (0, 1)])
                tb = VGroup(*[Bm.cell(2 * t + u, j).copy().set_fill(B_C, opacity=0.7) for u in (0, 1) for j in (4, 5)])
                self.play(FadeIn(ta), FadeIn(tb), run_time=0.35)
                self.play(Indicate(blk_box, color=C_C, scale_factor=1.06), FadeOut(ta), FadeOut(tb), run_time=0.45)
            vo.wait_until("d")
            self.play(Create(hl_sync), Create(hl_math))
            vo.wait_until("e")
            self.play(Write(inten), FadeIn(il))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def occupancy(self):
        w = load("warps")
        regs, occ = np.asarray(w["regs"]), np.asarray(w["occ_regs"])
        g = axes([16, 256], [0, 1.05], x_length=6.2, y_length=3.6, xlabel=r"registers per thread",
                 ylabel=r"occupancy: \ warps resident, \ of $64$", xticks=[32, 64, 128, 192, 255],
                 yticks=[0, 0.25, 0.5, 1], yfmt=lambda v: rf"{int(100 * v)}\%", center=[-2.6, -0.3, 0])
        pts = []
        for r_, o_ in zip(regs, occ):
            pts += [g.ax.c2p(r_, o_), g.ax.c2p(min(r_ + 8, 256), o_)]
        st = VMobject(color=WARPC, stroke_width=3).set_points_as_corners(pts)
        colors = {r"R": REGC, r"W": WARPC}
        law = cmath(r"\text{warps}", r"\le", r"\Big\lfloor \frac{65{,}536}{32\,R} \Big\rfloor", colors=colors,
                    font_size=32).move_to([3.9, 2.1, 0])
        ll = label(r"$R$ registers per thread; \ also capped by shared memory \\ and by $64$ warps per SM",
                   font_size=20, color=GREY_A).next_to(law, DOWN, buff=0.2)
        ex1, ex2 = float(w["ex_occ"]), float(w["ex2_occ"])
        exs = VGroup(label(rf"the tile kernel: \ $32$ registers, \ $8$ KB shared: \ ${100 * ex1:.0f}\%$", font_size=20,
                           color=C_C),
                     label(rf"a big-tile kernel: \ $128$ registers, \ $64$ KB shared: \ ${100 * ex2:.0f}\%$",
                           font_size=20, color=FLOPC)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        exs.next_to(ll, DOWN, buff=0.45)
        vh = history_card(2010, r"Vasily Volkov, \ \textit{Better performance at lower occupancy}",
                          r"fewer threads, each doing more with its registers, can win", width=5.4, color=WARPC,
                          font_size=19).to_corner(DR, buff=0.3)
        tag = note(r"computed: \ NVIDIA's limits for the H100 (Hopper tuning guide)").to_corner(DL, buff=0.2)
        res = VGroup(label(r"one H100 multiprocessor holds:", font_size=24, color=WHITE),
                     label(rf"${CC90['regs']:,}$ registers \ (${CC90['regs'] * 4 // 1024}$ KB)".replace(",", "{,}"),
                           font_size=22, color=REGC),
                     label(rf"up to ${CC90['smem'] // 1024}$ KB of shared memory", font_size=22, color=L1C),
                     label(rf"at most ${CC90['warps']}$ warps \ (${CC90['warps'] * 32:,}$ threads)".replace(",", "{,}"),
                           font_size=22, color=WARPC))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.9, 1.6, 0])
        with self.voiceover(
            "How many threads can share a multiprocessor? Chapter three said: as many as it takes to hide memory's "
            "latency. But they share its registers and its shared memory. <bookmark mark='a'/> An H100's "
            "multiprocessor has 65,536 registers. A kernel whose threads each need R registers can keep at most "
            "65,536 over thirty-two R warps resident, and never more than sixty-four. The fraction is called "
            "occupancy. <bookmark mark='b'/> It falls in steps as each thread grows. <bookmark mark='c'/> Our tile "
            f"kernel, small and simple, runs at {100 * ex1:.0f} percent. A kernel with big register tiles, "
            f"the kind that feeds tensor cores, at {100 * ex2:.0f}. <bookmark mark='d'/> And that can be faster: in "
            "2010 Vasily Volkov showed that fewer threads, each doing more work from its registers, often beat "
            "full occupancy. It's chapter three's trade again: hide latency with threads, or with more arithmetic "
            "per load."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), LaggedStart(*[FadeIn(r_) for r_ in res], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeOut(res))
            self.play(Write(law), FadeIn(ll))
            vo.wait_until("b")
            self.play(Create(st), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(exs[0]))
            self.play(FadeIn(exs[1]))
            vo.wait_until("d")
            self.play(FadeIn(vh, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def triton(self):
        code = code_lines([
            "@triton.jit",
            "def matmul(a, b, c, M, N, K, BM: tl.constexpr, BN: tl.constexpr, BK: tl.constexpr):",
            "    rm = tl.program_id(0) * BM + tl.arange(0, BM)",
            "    rn = tl.program_id(1) * BN + tl.arange(0, BN)",
            "    rk = tl.arange(0, BK)",
            "    acc = tl.zeros((BM, BN), dtype=tl.float32)",
            "    for k in range(0, K, BK):",
            "        x = tl.load(a + rm[:, None] * K + (k + rk)[None, :])",
            "        y = tl.load(b + (k + rk)[:, None] * N + rn[None, :])",
            "        acc += tl.dot(x, y)",
            "    tl.store(c + rm[:, None] * N + rn[None, :], acc)",
        ], font_size=16, buff=0.12)
        code.to_corner(UL, buff=0.4)
        hl = SurroundingRectangle(code[9], color=FLOPC, buff=0.04, stroke_width=2)
        simp = note(r"simplified: \ no bounds checks").next_to(code, DOWN, buff=0.2).align_to(code, LEFT)
        hc = history_card(2019, r"Philippe Tillet, H.~T.~Kung \& David Cox, \ \textit{Triton}",
                          r"program a block, not a thread: \ the compiler handles shared memory, coalescing and the "
                          r"tensor cores; \ released by OpenAI in 2021", width=6.2, color=FLOPC, font_size=20)
        hc.to_corner(DR, buff=0.3).shift(UP * 0.6)
        others = label(r"also: \ CUTLASS (NVIDIA, C$++$), \ Pallas (JAX), \ \texttt{torch.compile} writes Triton",
                       font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Writing kernels like that by hand is hard, and getting the last factor of two is harder. "
            "<bookmark mark='a'/> In 2019 Philippe Tillet, a graduate student at Harvard, published Triton with "
            "H. T. Kung, the Kung of the systolic arrays, and David Cox. You write Python, and you program a block of "
            "the output, not a thread. <bookmark mark='b'/> Load a tile of A, a tile of B, multiply them with one dot, accumulate, "
            "move on: the tiling of chapter five, in eleven lines. The compiler decides how the threads share the "
            "work, stages the tiles through shared memory, coalesces the loads and uses the tensor cores. "
            "<bookmark mark='c'/> OpenAI released it in 2021, and PyTorch's compiler now writes Triton kernels "
            "itself. NVIDIA's CUTLASS library and JAX's Pallas play the same role in C plus plus and in JAX."
        ) as vo:
            self.play(FadeIn(code), FadeIn(simp))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Create(hl))
            vo.wait_until("c")
            self.play(FadeIn(others))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def flash(self):
        n = 8
        S = VGroup(*[Square(0.34, stroke_width=0.8, stroke_color=GREY_D, fill_color=C.ATTN, fill_opacity=0.1)
                     for _ in range(n * n)]).arrange_in_grid(rows=n, cols=n, buff=0).move_to([-3.6, -0.2, 0])
        sl = label(r"the $T \times T$ attention scores", font_size=22, color=C.ATTN).next_to(S, UP, buff=0.15)
        hbm = RoundedRectangle(width=3.4, height=1.1, corner_radius=0.12, stroke_color=BYTEC, fill_color=BYTEC,
                               fill_opacity=0.15).move_to([3.4, -2.2, 0])
        hl_ = label(r"HBM: \ large, \ far", font_size=22, color=BYTEC).move_to(hbm)
        sram = RoundedRectangle(width=3.4, height=1.6, corner_radius=0.12, stroke_color=L1C, fill_color=L1C,
                                fill_opacity=0.15).move_to([3.4, 1.75, 0])
        sr_ = label(r"SRAM: \ small, \ close", font_size=22, color=L1C).move_to(sram.get_top() + DOWN * 0.3)
        slot = sram.get_center() + DOWN * 0.25
        plain = Arrow(S.get_right(), hbm.get_left(), buff=0.2, color=C.SURPRISE, stroke_width=3)
        cross = Cross(plain, stroke_color=C.SURPRISE, stroke_width=5).scale(0.4)
        tiles = [VGroup(*[S[(2 * i + u) * n + 2 * j + v] for u in (0, 1) for v in (0, 1)]) for i in range(4)
                 for j in range(4)]
        colors = {r"T": C.ATTN, r"d": WHITE, r"M": L1C}
        io = VGroup(cmath(r"\text{standard}", r":", r"\Theta(Td + T^2)", colors=colors, font_size=30),
                    cmath(r"\text{FlashAttention}", r":", r"\Theta\big(T^2 d^2 / M\big)", colors=colors, font_size=30))
        io.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.4, 0])
        iol = label(r"bytes read and written to HBM", font_size=20, color=GREY_A).next_to(io, UP, buff=0.15)
        hc = note(r"T.~Dao, D.~Fu, S.~Ermon, A.~Rudra \& C.~R\'e (2022); \ FlashAttention-2 (2023), -3 (2024)")
        hc.to_corner(DL, buff=0.2)
        with self.voiceover(
            "The model example of thinking this way is FlashAttention. <bookmark mark='a'/> Attention computes a "
            "score for every pair of positions: a T by T table. The standard implementation writes that table out to "
            "high-bandwidth memory, then reads it back for the softmax, then again to weight the values. For long "
            "inputs that traffic dominates, while the tensor cores wait. <bookmark mark='b'/> In 2022 Tri Dao and "
            "colleagues at Stanford computed attention tile by tile instead, keeping each tile in on-chip SRAM, "
            "with a running maximum and sum so the softmax comes out exact. <bookmark mark='c'/> The table is never "
            "written out at all. They proved its memory traffic is T squared d squared over M, M the SRAM size: "
            "less than the standard version's whenever d squared is smaller than M, as it is in practice. The same "
            "arithmetic, faster, because it moves fewer bytes. Part 19 derives it."
        ) as vo:
            self.play(FadeIn(S), FadeIn(sl), FadeIn(hbm), FadeIn(hl_), FadeIn(sram), FadeIn(sr_), FadeIn(hc))
            vo.wait_until("a")
            self.play(GrowArrow(plain))
            vo.wait_until("b")
            self.play(Create(cross))
            for k, t_ in enumerate(tiles[:8]):
                cp = t_.copy().set_fill(C.ATTN, opacity=0.8)
                self.play(t_.animate.set_fill(C.ATTN, opacity=0.6), cp.animate.scale(0.8).move_to(slot),
                          run_time=0.3)
                self.play(FadeOut(cp), run_time=0.2)
            vo.wait_until("c")
            self.play(FadeIn(iol), Write(io))
            self.play(*[t_.animate.set_fill(C.ATTN, opacity=0.6) for t_ in tiles[8:]], run_time=1.0)
        self.wait(0.3)
        self.clear_scene()
