from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import (BYTEC, CPUC, EXPC, FLOPC, GPUC, MANC, PART, SIGNC, bit_strip, gflops, load)
from videos.ai.ai17.specs import GPUS

SHOWN = ["FP32", "TF32", "BF16", "FP16", "E4M3", "E5M2", "E2M1"]
NAMES = {"FP32": "FP32", "TF32": "TF32", "BF16": "BF16", "FP16": "FP16", "E4M3": r"FP8 E4M3", "E5M2": r"FP8 E5M2",
         "E2M1": r"FP4 E2M1", "E3M2": r"FP6 E3M2", "E2M3": r"FP6 E2M3"}


class Formats(VoiceoverScene):
    def construct(self):
        self.card()
        self.layouts()
        self.derive()
        self.measured()
        self.blocks()
        self.why_small()

    def card(self):
        card = chapter_card(9, r"Number formats in hardware", r"How few bits can a number have?", part=PART)
        with self.voiceover("Chapter nine. Number formats in hardware."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layouts(self):
        f = load("formats")
        pi = f["pi"]
        rows = VGroup()
        for name in SHOWN:
            b = pi[name]
            strip = bit_strip([(str(b["sign"]), SIGNC), (b["exp"], EXPC), (b["man"], MANC)], cell=0.27, font_size=15)
            nm = label(NAMES[name], font_size=22, color=WHITE)
            val = label(rf"${b['value']:.7g}$", font_size=22, color=GREY_A)
            rows.add(VGroup(nm, strip, val))
        for r_ in rows:
            r_[0].move_to([-5.6, 0, 0], aligned_edge=LEFT)
            r_[1].move_to([-3.75, 0, 0], aligned_edge=LEFT)
            r_[2].next_to(r_[1], RIGHT, buff=0.3)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0.1, -0.5, 0])
        for r_ in rows:
            r_[0].set_x(-6.0 + r_[0].width / 2)
        formula = cmath(r"x", r"=", r"(-1)^{s}", r"\times", r"2^{\,e - \text{bias}}", r"\times", r"1.m",
                        font_size=40).to_edge(UP, buff=0.45)
        formula[2].set_color(SIGNC)
        formula[4].set_color(EXPC)
        formula[6].set_color(MANC)
        key = VGroup(label(r"sign", font_size=20, color=SIGNC), label(r"exponent: \ range", font_size=20, color=EXPC),
                     label(r"mantissa: \ precision", font_size=20, color=MANC)).arrange(RIGHT, buff=0.5)
        key.next_to(formula, DOWN, buff=0.25)
        tag = note(r"computed: \ $\pi$ rounded to nearest in each format").to_corner(DR, buff=0.2)
        with self.voiceover(
            "A floating-point number is a sign, an exponent and a mantissa: scientific notation in base two. "
            "<bookmark mark='a'/> Here is pi, rounded into each format the hardware of this part supports. "
            "<bookmark mark='b'/> FP32, the IEEE standard of 1985: eight exponent bits, twenty-three mantissa bits, "
            "about seven decimal digits. <bookmark mark='c'/> TF32 and bfloat16 keep FP32's eight-bit exponent, so "
            "the same range, but cut the mantissa to ten bits and to seven. FP16 trades the other way: five exponent "
            "bits, ten of mantissa. <bookmark mark='d'/> Then eight bits in two flavours, four exponent bits and "
            "three of mantissa, or five and two. <bookmark mark='e'/> And four bits: two of exponent, one of "
            "mantissa. Pi becomes three."
        ) as vo:
            self.play(Write(formula), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(Indicate(rows[0][1], scale_factor=1.03))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:4]], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[4:6]], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(rows[6], shift=RIGHT * 0.2))
            self.play(Indicate(rows[6][2], color=C.SURPRISE))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        f = load("formats")
        r = f["rows"]
        colors = {r"M": MANC, r"e": EXPC, r"u": MANC}
        rows = [
            cmath(r"\text{spacing in } [2^e, 2^{e+1})", r"=", r"2^{\,e - M}", colors=colors, font_size=36),
            cmath(r"\frac{|\mathrm{fl}(x) - x|}{|x|}", r"\le", r"\tfrac12 \cdot 2^{-M}", r"=", r"u", colors=colors,
                  font_size=36),
            cmath(r"x_{\max}", r"=", r"(2 - 2^{-M}) \cdot 2^{\,e_{\max}}", colors=colors, font_size=36),
            cmath(r"x_{\max}(\text{E4M3})", r"=", r"1.75 \times 2^{8}", r"=", rf"{r['E4M3']['max']:g}", font_size=36),
        ]
        whys = [why(r"$2^M$ evenly spaced values per power of two"), why(r"round to nearest: \ half a step"),
                why(r"the exponent sets the range"), why(r"E4M3 keeps one pattern for NaN: \ no $1.875$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.45, edge=6.8)
        tab = VGroup()
        for name in ("FP32", "BF16", "FP16", "E4M3", "E5M2", "E2M1"):
            v = r[name]
            big = (rf"{v['max']:,.0f}".replace(",", "{,}") if v["max"] < 1e6 else
                   rf"\approx {v['max'] / 10 ** math.floor(math.log10(v['max'])):.1f} \times 10^{{{math.floor(math.log10(v['max']))}}}")
            tab.add(label(rf"{NAMES[name]}: \ $u = 2^{{-{v['m'] + 1}}}$, \ largest ${big}$", font_size=20,
                          color=GREY_A))
        tab.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.2)).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Two numbers describe a format. <bookmark mark='a'/> With M mantissa bits, each power of two is cut into "
            "two to the M equal steps. <bookmark mark='b'/> Rounding to the nearest value is off by at most half a "
            "step, so the relative error is at most two to the minus M plus one, the unit roundoff. That's "
            "precision. <bookmark mark='c'/> The exponent bits set the range: the largest number is just under two "
            "times two to the largest exponent. <bookmark mark='d'/> For E4M3 that's 448, because one bit pattern "
            "is kept to mean not-a-number. FP16 tops out at 65,504, which is why training in FP16 needs care, and "
            "bfloat16, with FP32's exponent, doesn't."
        ) as vo:
            step(0)
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                step(k + 1)
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tab], lag_ratio=0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        f = load("formats")
        r = f["rows"]
        names = ["FP32", "TF32", "BF16", "FP16", "E4M3", "E5M2", "E2M1"]
        err = [r[n]["gauss"] for n in names]
        pred = [r[n]["predict"] for n in names]
        lo, hi = -8.5, 0
        ax = axes([0, len(names)], [lo, hi], x_length=8.4, y_length=4.4,
                  ylabel=r"relative rounding error \ (RMS, log scale)", yticks=[-8, -6, -4, -2, 0],
                  yfmt=lambda v: rf"10^{{{int(v)}}}" if v else "1", center=[-1.2, -0.2, 0])
        bars, dots, labs = VGroup(), VGroup(), VGroup()
        cols = [GPUC, GPUC, GPUC, GPUC, FLOPC, FLOPC, C.SURPRISE]
        for k, (e_, p_, c_) in enumerate(zip(err, pred, cols)):
            y = math.log10(max(e_, 1e-12))
            p0, p1 = ax.ax.c2p(k + 0.5, lo), ax.ax.c2p(k + 0.5, y)
            bars.add(Rectangle(width=0.7, height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=c_,
                               fill_opacity=0.85).move_to((p0 + p1) / 2))
            dots.add(Dot(ax.ax.c2p(k + 0.5, math.log10(p_)), radius=0.07, color=WHITE))
            labs.add(label(NAMES[names[k]].replace("FP8 ", "").replace("FP4 ", ""), font_size=18, color=c_)
                     .next_to(ax.ax.c2p(k + 0.5, lo), DOWN, buff=0.15))
        key = VGroup(VGroup(Dot(radius=0.07, color=WHITE), label(r"predicted: \ $2^{-M} \sqrt{\ln 2 / 18}$",
                                                                  font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.15),
                     label(r"bars: \ measured on $10^6$ Gaussian samples", font_size=20, color=GREY_A))
        key.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, 2.2, 0])
        tag = note(r"computed: \ 8 bits and fewer scaled so the largest sample fits").to_corner(DR, buff=0.2)
        worst = max(abs(math.log2(e_ / p_)) for e_, p_ in zip(err[:6], pred[:6]))
        agree = ("and the measurements land on it" if worst < 0.5 else
                 "and the measurements land close to it")
        e4 = r["E2M1"]["gauss"]
        with self.voiceover(
            "Let's measure it. Round a million Gaussian samples into each format and compare. <bookmark mark='a'/> "
            "Each step down in mantissa bits multiplies the error. FP32 is off by a few parts in a hundred million, "
            f"bfloat16 by about {100 * r['BF16']['gauss']:.2f} percent, eight-bit E4M3 by about "
            f"{100 * r['E4M3']['gauss']:.1f} percent, and four bits by {100 * e4:.0f} percent. "
            "<bookmark mark='b'/> The white dots are the prediction: if the rounding error is spread evenly over a "
            "step, and values are spread evenly in the logarithm, the root-mean-square relative error is two to the "
            "minus M times a constant, the square root of log two over eighteen, about a fifth. The prediction "
            "ignores the very small and very large numbers, " + agree + ". Four bits miss it most: there, many "
            "samples fall below the smallest step."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.25), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(key), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blocks(self):
        f = load("formats")
        b = f["blocks"]
        src = f["weights_source"]
        key = "weights" if src else "gauss"
        what = {"novels": "the weights of this series' own small language model",
                "narrator": "a weight matrix of the voice model narrating this video"}.get(src, "Gaussian samples")
        what_tex = {"novels": r"the weights of this series' own model",
                    "narrator": r"a weight matrix of the narrator's voice model"}.get(src, r"Gaussian samples")
        rows_ = [("FP8 (one scale)", r"FP8, \ one scale per tensor", FLOPC), ("MXFP8", r"MXFP8: \ a shared exponent "
                 r"per $32$", FLOPC), ("FP4 (one scale)", r"FP4, \ one scale per tensor", C.SURPRISE),
                 ("MXFP4", r"MXFP4: \ a shared exponent per $32$", C.SURPRISE),
                 ("NVFP4", r"NVFP4: \ an FP8 scale per $16$", C.SURPRISE)]
        vals = [b[k][key] for k, _, _ in rows_]
        mx = max(vals)
        bars, labs, nums = VGroup(), VGroup(), VGroup()
        for k, ((_, t, c_), v) in enumerate(zip(rows_, vals)):
            w = 6.0 * v / mx
            y = 1.3 - 0.75 * k
            bars.add(Rectangle(width=w, height=0.45, stroke_width=0, fill_color=c_, fill_opacity=0.85)
                     .move_to([-0.6 + w / 2, y, 0]))
            labs.add(label(t, font_size=20, color=c_).next_to([-0.8, y, 0], LEFT, buff=0.1))
            nums.add(label(rf"${100 * v:.1f}\%$", font_size=22).next_to(bars[-1], RIGHT, buff=0.15))
        head = label(rf"relative rounding error on {what_tex}", font_size=26).to_edge(UP, buff=0.5)
        # a block of 32 numbers sharing one exponent
        cells = VGroup(*[Square(0.2, stroke_width=0.8, stroke_color=MANC, fill_color=MANC, fill_opacity=0.35)
                         for _ in range(32)]).arrange(RIGHT, buff=0.03)
        sc = Square(0.3, stroke_width=1.2, stroke_color=EXPC, fill_color=EXPC, fill_opacity=0.6)
        blk = VGroup(sc, cells).arrange(RIGHT, buff=0.15).to_edge(DOWN, buff=0.9)
        bl = label(r"$32$ four-bit numbers \ $+$ \ one shared $8$-bit exponent \ $= 4.25$ bits each", font_size=22,
                   color=GREY_A).next_to(blk, DOWN, buff=0.15)
        nv, mx4, t4 = b["NVFP4"][key], b["MXFP4"][key], b["FP4 (one scale)"][key]
        verdict = (f"Sharing a scale per block of thirty-two cuts the four-bit error from {100 * t4:.0f} to "
                   f"{100 * mx4:.0f} percent, and NVIDIA's finer blocks, with an eight-bit scale, to {100 * nv:.0f}."
                   if nv < mx4 < t4 else
                   f"Here the block scales give {100 * mx4:.0f} and {100 * nv:.0f} percent, against {100 * t4:.0f} "
                   "with one scale for the whole tensor.")
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Four bits have so little range that one scale for a whole matrix doesn't work: a few large values "
            "push everything else into the bottom step. <bookmark mark='a'/> The fix, standardized in 2023 by the "
            "Open Compute Project, is microscaling: give each block of thirty-two numbers its own shared exponent. "
            "<bookmark mark='b'/> We rounded " + what + " each way. " + verdict + " <bookmark mark='c'/> Part 19 "
            "uses these formats to run a real model in four bits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.play(*[AnimationGroup(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]), FadeIn(nums[k])) for k in (0, 2)])
            vo.wait_until("a")
            self.play(FadeIn(blk), FadeIn(bl))
            self.play(Indicate(sc, color=EXPC, scale_factor=1.5))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[k], LEFT), FadeIn(labs[k]), FadeIn(nums[k]))
                                    for k in (1, 3, 4)], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why_small(self):
        mm = load("matmul")
        H = GPUS["H100"]
        tf = {r[0]: r[1] for r in mm["torch_float32"]}
        tb = {r[0]: r[1] for r in mm["torch_bfloat16"]}
        n = max(set(tf) & set(tb))
        chips = [("H100", GPUS["H100"]), ("GB200", GPUS["GB200"]), ("Rubin", GPUS["Rubin"])]
        fmts = [("tensor", r"BF16", GPUC), ("fp8", r"FP8", FLOPC), ("fp4", r"FP4", C.SURPRISE)]
        g = axes([0, 3], [14, 16.8], x_length=6.4, y_length=3.4, ylabel=r"dense FLOP/s per GPU \ (log scale)",
                 xticks=[0.5, 1.5, 2.5], xfmt=lambda v: chips[int(v)][0], yticks=[14, 15, 16],
                 yfmt=lambda v: rf"10^{{{int(v)}}}", center=[-2.4, 1.0, 0])
        bars = VGroup()
        for k, (nm, spec) in enumerate(chips):
            grp = VGroup()
            for j, (key, fl, col) in enumerate(fmts):
                if key not in spec:
                    continue
                x = k + 0.22 + 0.28 * j
                y = math.log10(spec[key])
                p0, p1 = g.ax.c2p(x, 14), g.ax.c2p(x, y)
                grp.add(Rectangle(width=0.24, height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                  fill_opacity=0.9).move_to((p0 + p1) / 2))
            bars.add(grp)
        lg = legend([(col, fl) for _, fl, col in fmts], font_size=20).next_to(g.ax, RIGHT, buff=0.3).shift(UP * 0.6)
        cpu = label(rf"this CPU, \ no bfloat16 units: \\ FP32 ${gflops(tf[n])}$, \ BF16 ${gflops(tb[n])}$ GFLOP/s",
                    font_size=24, color=CPUC).move_to([4.3, -0.3, 0])
        src = cite(r"NVIDIA datasheets and product pages", corner=UL)
        hist = VGroup(*[history_card(y, w, t, width=4.2, color=c, font_size=18) for y, w, t, c in (
            (1985, r"IEEE 754", r"William Kahan's standard: \ FP32, FP64", GREY_B),
            (2017, r"bfloat16", r"Google Brain's format, \ in the TPU v2: \ FP32's range in 16 bits", GPUC),
            (2022, r"FP8", r"NVIDIA, Arm \& Intel: \ E4M3 and E5M2", FLOPC),
            (2023, r"Microscaling (MX)", r"the Open Compute Project: \ blocks of 32 share an exponent", C.SURPRISE),
        )]).arrange_in_grid(rows=1, cols=4, buff=0.15).to_edge(DOWN, buff=0.35)
        if hist.width > 13.4:
            hist.width = 13.4
        tag = note(rf"computed: \ PyTorch, $n = {int(n)}$, \ one thread").to_corner(UR, buff=0.2)
        slow = tf[n] / tb[n]
        with self.voiceover(
            "Why go small at all? Because the multiplier's size grows roughly with the square of the mantissa's "
            "width, and every bit not moved is bandwidth saved. <bookmark mark='a'/> Halve the bits and the tensor "
            f"cores do twice the work: an H100 does {H['tensor'] / 1e12:.0f} trillion operations a second in "
            f"bfloat16 and {H['fp8'] / 1e12:,.0f} in FP8; a Blackwell GPU doubles again in four bits. "
            "<bookmark mark='b'/> But only on hardware built for it. This computer's processor has no bfloat16 "
            f"units, and PyTorch's bfloat16 product runs {slow:.1f} times slower than its FP32. "
            "<bookmark mark='c'/> The history: Kahan's IEEE standard in 1985; bfloat16 from Google Brain for the "
            "TPU; eight-bit floats proposed by NVIDIA, Arm and Intel in 2022; microscaling in 2023. Part 18 trains "
            "in eight bits; Part 19 serves in four."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(lg))
            vo.wait_until("a")
            self.play(LaggedStart(*[LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in grp], lag_ratio=0.3)
                                    for grp in bars], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(cpu), FadeIn(tag))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(h_, shift=UP * 0.15) for h_ in hist], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()
