from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (A_C, B_C, BYTEC, C_C, COMMC, CPUC, FLOPC, GPUC, PART, POWERC, box_label, load,
                                   ring_devices)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []

        def small_axes(xr, yr):
            return Axes(x_range=[*xr, (xr[1] - xr[0]) / 2], y_range=[*yr, (yr[1] - yr[0]) / 2], x_length=TW * 0.9,
                        y_length=TH * 0.85, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})

        t = load("trends")
        ax = small_axes((1970, 2022), (-0.5, 4))
        ft, fy = np.asarray(t["frequency_t"]), np.asarray(t["frequency_y"])
        out.append((VGroup(ax, *[Dot(ax.c2p(a, math.log10(b)), radius=0.025, color=FLOPC) for a, b in zip(ft, fy)]),
                    r"the power wall", POWERC))
        w = load("warps")
        ax = small_axes((0, 1), (0, 1.05))
        out.append((VGroup(ax, curve(ax, w["qs"], w["eff_rand"], C.SURPRISE, 3), curve(ax, w["qs"], w["eff_sort"], GPUC,
                                                                                         3)), r"divergence", GPUC))
        b = load("blocking")
        vals = [b["naive"], b["ikj"], float(np.max(b["blocked"])), b["blas"]]
        ax = small_axes((0, 4), (-1, math.log10(max(vals) / 1e9) + 0.3))
        bars = VGroup(*[Rectangle(width=0.45, height=max(ax.c2p(0, math.log10(v / 1e9))[1] - ax.c2p(0, -1)[1], 0.02),
                                  stroke_width=0, fill_color=c_, fill_opacity=0.9)
                        .move_to([ax.c2p(k + 0.5, 0)[0], (ax.c2p(0, math.log10(v / 1e9))[1] + ax.c2p(0, -1)[1]) / 2, 0])
                        for k, (v, c_) in enumerate(zip(vals, [C.SURPRISE, B_C, FLOPC, CPUC]))])
        out.append((VGroup(ax, bars), r"tiling: \ reuse", FLOPC))
        h = load("hierarchy")
        x, bw = np.log2(np.asarray(h["sizes"]) / 1024), np.asarray(h["bandwidth"]) / 1e9
        ax = small_axes((x[0], x[-1]), (0, bw.max() * 1.1))
        out.append((VGroup(ax, curve(ax, x, bw, BYTEC, 3)), r"the memory hierarchy", BYTEC))
        mm = load("matmul")
        P = max(r_[1] for r_ in mm["np_float32"]) / 1e9
        B = float(h["stream"].get("triad", mm["np_copy"][0])) / 1e9
        ax = small_axes((-2, 3), (-1, 2.5))
        xs = np.linspace(-2, 3, 50)
        roof = curve(ax, xs, np.minimum(math.log10(P), math.log10(B) + xs), WHITE, 3)
        dots = VGroup(*[Dot(ax.c2p(math.log10(n / 6), math.log10(v / 1e9)), radius=0.04, color=B_C)
                        for n, v, _ in mm["np_float32"]])
        out.append((VGroup(ax, roof, dots), r"the roofline", WHITE))
        s = load("systolic")
        n = int(s["n"])
        grid = VGroup(*[Square(0.36, stroke_color=FLOPC, stroke_width=1, fill_color=FLOPC,
                               fill_opacity=0.15 + 0.6 * ((i + j) % n) / n) for i in range(n) for j in range(n)])
        grid.arrange_in_grid(rows=n, cols=n, buff=0.06)
        out.append((grid, r"a systolic wavefront", FLOPC))
        f = load("formats")
        names = ["FP32", "BF16", "FP16", "E4M3", "E5M2", "E2M1"]
        errs = [f["rows"][k]["gauss"] for k in names]
        ax = small_axes((0, 6), (-8.5, 0))
        bars2 = VGroup(*[Rectangle(width=0.32, height=ax.c2p(0, math.log10(e_))[1] - ax.c2p(0, -8.5)[1], stroke_width=0,
                                   fill_color=C.MAN_BIT, fill_opacity=0.9)
                         .move_to([ax.c2p(k + 0.5, 0)[0], (ax.c2p(0, math.log10(e_))[1] + ax.c2p(0, -8.5)[1]) / 2, 0])
                         for k, e_ in enumerate(errs)])
        out.append((VGroup(ax, bars2), r"fewer bits, more error", C.MAN_BIT))
        devs = ring_devices(4, radius=0.75, size=0.35, names=["", "", "", ""])
        arcs = VGroup(*[CurvedArrow(devs[k][0].get_center(), devs[(k + 1) % 4][0].get_center(), angle=-0.5,
                                    color=COMMC, stroke_width=2, tip_length=0.1) for k in range(4)])
        out.append((VGroup(devs, arcs), r"ring all-reduce", COMMC))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. When the voltage stopped falling, clocks stopped rising, and the only way to use more "
            "transistors was in parallel. GPUs run thousands of threads in warps, and pay for divergence. Matrix "
            "multiplication is nearly all of a network's arithmetic, and tiling lets each number fetched be used many "
            "times. Memory is a hierarchy, small and close to large and far, and the roofline says whether a "
            "program is bound by arithmetic or by bytes. Systolic arrays build reuse into the wiring. Fewer bits buy "
            "throughput at a measured cost in error. And when one chip isn't enough, a ring all-reduce shares the "
            "work at nearly the bandwidth limit."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"the $\alpha$--$\beta$ model, \ ring all-reduce, \ FP8 training", [18]),
            (r"the roofline: \ prefill against decode; \ FlashAttention; \ MXFP4, NVFP4", [19]),
            (r"memory capacity and bandwidth: \ the KV cache, \ hardware-aware scans", [15]),
            (r"all-to-all inside an NVLink domain; \ 2:4 sparsity", [16]),
        ], font_size=26)
        with self.voiceover(
            "All of this comes back. Part 18 trains a model across many GPUs, with the alpha-beta model, the ring "
            "all-reduce and eight-bit arithmetic. Part 19 puts inference on the roofline: reading a prompt is "
            "arithmetic-bound, writing an answer is memory-bound, and FlashAttention and four-bit formats follow. "
            "Part 15's memory methods are sized to high-bandwidth memory and written to use the tensor cores, and "
            "Part 16's experts trade tokens across an NVLink domain, while the tensor cores' two-in-four sparsity "
            "doubles their arithmetic."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For $C = AB$ with $A$ of size $m \times k$ and $B$ of size $k \times n$, in $s$-byte numbers, each moved "
            r"once, show that $I = 2mnk / \big(s(mk + kn + mn)\big)$. \ What happens when $m = 1$?",
            r"Tile an $n \times n$ product with $b \times b$ tiles in a fast memory of $M$ numbers ($3b^2 \le M$). "
            r"\ Show that it moves about $2n^3/b$ numbers, \ about $2\sqrt3\, n^3/\sqrt{M}$.",
            r"An H100 does $989$ TFLOP/s in BF16 and reads $3.35$ TB/s. \ Which square BF16 products can reach "
            r"the roof? \ Repeat for a Rubin GPU in NVFP4: $35$ PFLOP/s, $19.2$ TB/s, half a byte per number.",
            r"Derive $T_{\text{ring}} = 2(p-1)\alpha + 2\frac{p-1}{p}\frac{n}{\beta}$ and "
            r"$T_{\text{tree}} = 2\log_2 p\,(\alpha + n/\beta)$. \ For $p = 8$, where do they cross?",
            r"Show that rounding to nearest with $M$ mantissa bits has relative error at most $2^{-(M+1)}$, \ and "
            r"find the largest finite FP16, E4M3 and E5M2 numbers.",
            r"Memory $3.35$ TB/s away by $\approx 273$ ns, \ $132$ SMs, \ $128$-byte loads: \ how many loads must "
            r"each SM keep in flight? \ Can $64$ warps, one load each, do it?",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from arithmetic intensity to the latency a GPU has to hide. Pause here, "
            "and work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 18, \ Pretraining at Scale", font_size=40).to_edge(UP, buff=0.5)
        steps = VGroup(*[box_label(t, c, font_size=28) for t, c in (
            (r"clean, deduplicated data", GREY_B), (r"data, tensor, pipeline and expert parallelism", GPUC),
            (r"ZeRO and FSDP", BYTEC), (r"FP8 training", C.MAN_BIT), (r"a stable run on thousands of GPUs", FLOPC))])
        steps.arrange(DOWN, buff=0.62).move_to(DOWN * 0.45)
        if steps.height > 5.9:
            steps.height = 5.9
        arrs = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B, stroke_width=2.5,
                              max_tip_length_to_length_ratio=0.35) for a, b in zip(steps, steps[1:])])
        with self.voiceover(
            "Next time: pretraining at scale. Where the trillions of tokens come from and how they're cleaned; how "
            "one model is cut across thousands of GPUs, by data, by tensor, by pipeline stage and by expert, with "
            "this part's all-reduce at the centre; how training in eight bits stays stable; and what goes wrong on "
            "a run of sixteen thousand GPUs."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *([GrowArrow(arrs[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps)], lag_ratio=0.5), run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"J.~L.~Hennessy \& D.~A.~Patterson, \textit{Computer Architecture: A Quantitative Approach}, 6th ed.\ (2017)",
             r"D.~B.~Kirk, W.~W.~Hwu \& I.~El Hajj, \textit{Programming Massively Parallel Processors}, 4th ed.\ (2022)",
             r"V.~Sze, Y.-H.~Chen, T.-J.~Yang \& J.~S.~Emer, \textit{Efficient Processing of Deep Neural Networks} (2020)"],
            [r"Moore (1965); \ Dennard et al.\ (1974); \ Amdahl (1967); \ Little (1961); \ Sutter (2005); \ "
             r"Esmaeilzadeh et al.\ (2011)",
             r"Kung \& Leiserson (1978); \ Kung (1982); \ Hong \& Kung (1981); \ Jouppi et al.\ (2017, 2020, 2023)",
             r"Buck et al.\ (2004); \ Oh \& Jung (2004); \ Lindholm et al.\ (2008); \ Raina, Madhavan \& Ng (2009); "
             r"\ Krizhevsky et al.\ (2012)",
             r"Williams, Waterman \& Patterson (2009); \ Volkov (2010); \ Tillet, Kung \& Cox (2019); \ Dao et al.\ (2022)",
             r"Micikevicius et al.\ (2022); \ Rouhani et al.\ (2023); \ Horowitz (2014); \ Han et al.\ (2016)",
             r"Hockney (1994); \ Thakur et al.\ (2005); \ Patarasuk \& Yuan (2009); \ Leiserson (1985)",
             r"Amodei \& Hernandez (2018); \ Hooker (2020); \ Hobbhahn et al.\ (2023); \ Gholami et al.\ (2024); \ "
             r"Luo et al.\ (2024)",
             r"NVIDIA, Google, AWS, Cerebras datasheets; \ IEA (2025); \ Epoch AI; \ K.~Rupp's trend data"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Hennessy and Patterson's book is the place to go deeper on all of this, and Kirk and Hwu's on GPU "
            "programming. Thanks for watching, and see you in Part 18."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
