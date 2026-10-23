from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (F, GRADS, PART, PREC, PREC_NAME, PREC_SPOKEN, format_band, load, log2_axis,
                                   take_away)


class Precision(VoiceoverScene):
    def construct(self):
        self.card()
        self.ranges()
        self.scaling()
        self.runs()
        self.accumulate()
        self.fp8()
        self.fp4()

    def card(self):
        card = chapter_card(14, r"Fewer bits", r"How few bits can a training run use?", lit=(1985,), part=PART)
        with self.voiceover("Chapter fourteen. Fewer bits."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def _axis_and_hist(self, y_axis=-2.2):
        H = load("precision")["hist"]
        ax = log2_axis(-40, 18, width=12.4).move_to([0.3, y_axis, 0])
        edges = np.asarray(H["edges"])
        h = np.asarray(H["hist"])
        bars = VGroup()
        top = h.max()
        for e0, v in zip(edges[:-1], h):
            if v <= 0:
                continue
            x0, x1 = ax.x(e0), ax.x(e0 + 1)
            r = Rectangle(width=(x1 - x0) * 0.92, height=1.6 * v / top, stroke_width=0, fill_color=GRADS,
                          fill_opacity=0.85)
            r.move_to([(x0 + x1) / 2, ax.line.get_y() + 0.8 * v / top + 0.02, 0])
            bars.add(r)
        return ax, bars, H

    # ------------------------------------------------------------------
    def ranges(self):
        ax, bars, H = self._axis_and_hist()
        Fm = F.FORMATS
        bands = VGroup(
            format_band(ax, -126, 18, PREC["fp32"], 2.6, r"FP32"),
            format_band(ax, -126, 18, PREC["bf16"], 2.1, r"BF16"),
            format_band(ax, -14, math.log2(65504), PREC["fp16"], 1.6, r"FP16", sub_e=-24),
            format_band(ax, -6, math.log2(448), PREC["fp8_tile"], 1.1, r"FP8 E4M3", sub_e=-9),
            format_band(ax, -14, math.log2(57344), PREC["fp8_tensor"], 0.6, r"FP8 E5M2", sub_e=-16),
        )
        for b in bands:
            if b.get_left()[0] < -6.9:
                b.name.set_x(-6.9 + b.name.width / 2)
        clip = note(r"FP32 and BF16 reach $2^{-126}$: \ off the left edge", font_size=18).move_to([-3.0, 3.3, 0])
        bits = VGroup(
            label(r"BF16: \ FP32's $8$ exponent bits, \ $7$ of its $23$ mantissa bits", font_size=20, color=PREC["bf16"]),
            label(r"FP16: \ $5$ exponent bits, \ $10$ mantissa bits", font_size=20, color=PREC["fp16"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.6, 3.15, 0])
        hl = label(rf"$|\partial L / \partial y|$ \ at the outputs of our model's matrix products \ (step "
                   rf"$60$, \ ${H['n']:,}$ values)".replace(",", "{,}"), font_size=20, color=GRADS)
        hl.next_to(bars, UP, buff=0.12).set_x(ax.x(-20))
        under = label(rf"${100 * H['below_normal']:.0f}\%$ below FP16's smallest normal number; \ "
                      rf"${100 * H['below_sub']:.0f}\%$ round to zero", font_size=22, color=PREC["fp16"])
        under.next_to(ax, DOWN, buff=0.55)
        floor = DashedLine([ax.x(-24), ax.line.get_y() - 0.1, 0], [ax.x(-24), 3.0, 0], color=PREC["fp16"],
                           dash_length=0.06)
        src = cite(r"IEEE 754 (1985); \ Micikevicius et al.\ (2018, 2022); \ computed here", corner=DR, font_size=16)
        with self.voiceover(
            "Every number in a training run takes memory and bandwidth, and narrower numbers multiply faster: Part "
            "17's tensor cores do twice the work in eight bits as in sixteen. So how few bits can training use? "
            "<bookmark mark='a'/> Here are the formats, on a scale of powers of two, as far as each reaches before "
            "its numbers become too small or too large. <bookmark mark='b'/> FP32 and bfloat16 share an eight-bit "
            "exponent, so the same enormous range; bfloat16 just keeps fewer digits. Half precision, FP16, has five "
            "exponent bits: nothing below about six times ten to the minus eight, and a fainter zone of "
            "low-precision subnormals below two to the minus fourteen. <bookmark mark='c'/> Now the numbers that "
            "matter: the gradients flowing back through our model's matrix products, measured after sixty steps. "
            f"<bookmark mark='d'/> {100 * H['below_normal']:.0f} percent of them are below FP16's smallest normal "
            f"number, and {100 * H['below_sub']:.0f} percent are so small that FP16 rounds them to zero."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bands], lag_ratio=0.3), FadeIn(clip),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(bits))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(hl), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(floor), FadeIn(under))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scaling(self):
        ax, bars, H = self._axis_and_hist(y_axis=-1.4)
        colors = {r"S": PREC["fp16_scaled"], r"L": C.LOSS}
        rows = [
            cmath(r"\frac{\partial (S\,L)}{\partial y}", r"=", r"S\,\frac{\partial L}{\partial y}", colors=colors,
                  font_size=30),
            cmath(r"g_W", r"=", r"\frac{1}{S}\,\frac{\partial (S\,L)}{\partial W}", colors=colors, font_size=30),
        ]
        whys = [why(r"the chain rule is linear: \ every gradient scales by $S$", font_size=20),
                why(r"divide by $S$ before the update", font_size=20)]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-2.8, buff=0.4, edge=6.9)
        shift = ax.x(16) - ax.x(0)
        floor = DashedLine([ax.x(-24), ax.line.get_y() - 0.1, 0], [ax.x(-24), 1.0, 0], color=PREC["fp16"],
                           dash_length=0.06)
        top_ = DashedLine([ax.x(math.log2(65504)), ax.line.get_y() - 0.1, 0], [ax.x(math.log2(65504)), 1.0, 0],
                          color=PREC["fp16"], dash_length=0.06)
        dyn = label(r"dynamic: \ on an overflow, \ skip the step and halve $S$; \ after a run of good steps, \ "
                    r"double it", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        sl = label(r"$\times\, S = 2^{16}$", font_size=26, color=PREC["fp16_scaled"]).move_to([ax.x(-5), 0.9, 0])
        src = cite(r"Micikevicius et al., \textit{Mixed Precision Training} (ICLR 2018)", corner=DR, font_size=17)
        with self.voiceover(
            "The fix, from Micikevicius and colleagues at NVIDIA and Baidu in 2018, is loss scaling. "
            "<bookmark mark='a'/> Multiply the loss by a large number S before the backward pass. The chain rule is "
            "linear, so every gradient comes out S times larger. <bookmark mark='b'/> On the scale of powers of two, "
            "the whole distribution slides to the right by sixteen places for S of two to the sixteen, into FP16's "
            "range. <bookmark mark='c'/> Then divide the weights' gradients by S before the update, which happens in "
            "thirty-two bits. <bookmark mark='d'/> Too large an S makes the biggest gradients overflow, so in "
            "practice S is dynamic: halve it and skip the step when an overflow appears, double it after a run of "
            "good steps. BFloat16, with FP32's range, needs none of this, which is why it took over."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(bars), FadeIn(floor), FadeIn(top_), FadeIn(src))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            self.play(bars.animate.shift(RIGHT * shift), FadeIn(sl), run_time=2.0)
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            self.play(FadeIn(dyn))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def _panel(self, runs, keys, center, title, x_len=5.6, y_len=3.4, lo=None, hi=None):
        evs = {k: np.asarray(runs[k]["evals"]) for k in keys}
        allv = np.concatenate([e[:, 2] for e in evs.values()])
        lo = lo if lo is not None else math.floor(allv.min() * 4) / 4
        hi = hi if hi is not None else lo + 2.5
        steps = max(e[-1, 0] for e in evs.values())
        g = axes([0, steps], [lo, hi], x_length=x_len, y_length=y_len, xlabel=r"step",
                 ylabel=title, xticks=[0, steps], yticks=[lo, hi], yfmt=lambda v: f"{v:.2f}", center=center,
                 font_size=18)
        return g, evs, lo, hi

    def runs(self):
        Pc = load("precision")
        runs, seeds = Pc["runs"], Pc["seeds"]
        fin = Pc["final"]
        g, evs, lo, hi = self._panel(runs, [f"{v}_{s}" for v in Pc["precisions"] for s in seeds], [-2.9, -0.3, 0],
                                     r"held-out loss (nats)")
        lines = VGroup()
        for v in Pc["precisions"]:
            for s in seeds:
                e = evs[f"{v}_{s}"]
                sel = e[:, 2] <= hi
                lines.add(curve(g.ax, e[sel, 0], e[sel, 2], PREC[v], 2.5).set_stroke(opacity=0.85))
        names = VGroup()
        for i, v in enumerate(Pc["precisions"]):
            a, b = fin[v]
            names.add(VGroup(Line(ORIGIN, RIGHT * 0.4, color=PREC[v], stroke_width=5),
                             label(rf"{PREC_NAME[v]}: \ ${min(a, b):.3f}$--${max(a, b):.3f}$", font_size=19,
                                   color=PREC[v])).arrange(RIGHT, buff=0.12))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.7, 0.2, 0])
        nh = label(r"final held-out loss, \ two seeds", font_size=20, color=GREY_A).next_to(names, UP, buff=0.25)
        U = runs[f"fp16_{seeds[0]}"]["underflow"]
        zero = float(np.mean([u[1] for u in U]))
        f32 = np.mean(fin["fp32"])
        spread = max(abs(fin[v][0] - fin[v][1]) for v in fin)
        worst_v = max(fin, key=lambda v: np.mean(fin[v]))
        gap = np.mean(fin[worst_v]) - f32
        tag = note(rf"computed: \ every matrix product's inputs rounded to the format, \ sums in FP32; \ "
                   rf"${Pc['steps']}$ steps", font_size=18).to_corner(DR, buff=0.2)
        if gap < max(spread, 0.01):
            verdict = (f"All six end within {gap:.3f} nats of each other, inside the {spread:.3f} that separates two "
                       f"seeds. Even FP16 without loss scaling, which flushed {100 * zero:.1f} percent of the "
                       "gradient values to zero, trained just as well.")
        else:
            worst_name = PREC_SPOKEN[worst_v]
            verdict = (f"The worst, {worst_name}, ends "
                       f"{gap:.3f} nats above FP32, more than the {spread:.3f} between seeds; FP16 without loss scaling "
                       f"flushed {100 * zero:.1f} percent of the gradient values to zero.")
        with self.voiceover(
            "Does it matter in practice? We trained the same small model six times over, with every matrix "
            "product's inputs rounded to a format, going forward and backward, and the sums kept in FP32, which is "
            "what the hardware does. Two seeds each. <bookmark mark='a'/> FP32, bfloat16, FP16 without and with "
            "loss scaling, and two kinds of eight-bit training we'll meet in a moment. <bookmark mark='b'/> "
            + verdict
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), FadeIn(nh))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(n_) for n_ in names], lag_ratio=0.3), run_time=4.0)
            vo.wait_until("b")
            self.play(Indicate(names[2], scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def accumulate(self):
        Pc, A = load("precision"), load("precision_acc")
        seeds = A["seeds"]
        runs = {**{f"ref_{s}": Pc["runs"][f"fp32_{s}"] for s in seeds}, **A["runs"]}
        g, evs, lo, hi = self._panel(runs, list(runs), [-2.9, -0.3, 0], r"held-out loss (nats)", hi=None)
        cols = {"ref": PREC["fp32"], "fp16": PREC["fp16"], "fp16_scaled": PREC["fp16_scaled"]}
        lines = VGroup()
        for k, e in evs.items():
            v = k.rsplit("_", 1)[0]
            sel = e[:, 2] <= hi
            lines.add(curve(g.ax, e[sel, 0], e[sel, 2], cols[v], 2.5))
        fin = A["final"]
        f32 = Pc["final"]["fp32"]
        U = A["runs"][f"fp16_{seeds[0]}"]["underflow"]
        zero = float(np.mean([u[1] for u in U]))
        leg = VGroup(
            label(rf"FP32: \ ${np.mean(f32):.3f}$", font_size=20, color=PREC["fp32"]),
            label(rf"FP16, \ no loss scaling: \ ${np.mean(fin['fp16']):.3f}$", font_size=20, color=PREC["fp16"]),
            label(rf"FP16, \ loss scaling: \ ${np.mean(fin['fp16_scaled']):.3f}$", font_size=20,
                  color=PREC["fp16_scaled"]),
            label(rf"gradient values flushed to zero without scaling: \ ${100 * zero:.0f}\%$", font_size=20,
                  color=PREC["fp16"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, 0.3, 0])
        head = label(rf"the same runs, \ each step's gradient accumulated over ${A['accum']}$ micro-batches",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.4)
        d_noscale = np.mean(fin["fp16"]) - np.mean(f32)
        d_scaled = np.mean(fin["fp16_scaled"]) - np.mean(f32)
        if d_noscale > 0.05 and d_scaled < d_noscale / 2:
            verdict = (f"Now the gradients are {A['accum']} times smaller while they are rounded, and FP16 without "
                       f"loss scaling flushes {100 * zero:.0f} percent of them to zero: it ends {d_noscale:.2f} nats "
                       f"behind FP32. With loss scaling, {abs(d_scaled):.3f} from it. That is the failure loss "
                       "scaling exists to prevent.")
        elif d_noscale > 0.05:
            verdict = (f"Now FP16 without loss scaling flushes {100 * zero:.0f} percent of the gradients to zero and "
                       f"ends {d_noscale:.2f} nats behind FP32; loss scaling recovers part of the gap.")
        else:
            verdict = (f"Even now, with {100 * zero:.0f} percent of the gradient values flushed to zero, FP16 without "
                       f"loss scaling ends only {d_noscale:.3f} nats from FP32: our model is too small to show the "
                       "failure clearly.")
        with self.voiceover(
            "Why, then, did loss scaling matter? Because our gradients are averages over only two thousand tokens. "
            "A frontier run averages each step's gradient over millions, accumulated piece by piece, and every piece "
            f"is that much smaller. <bookmark mark='a'/> So we repeated the FP16 runs with each step split into "
            f"{A['accum']} micro-batches, as gradient accumulation does. <bookmark mark='b'/> " + verdict
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x_) for x_ in leg], lag_ratio=0.3), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fp8(self):
        Pc, D = load("precision"), F.DSV3
        q = Pc["qerr"]
        sample = np.asarray(q["act_sample"])
        bars = VGroup()
        mx = np.abs(sample).max()
        big = []
        for i, v in enumerate(sample):
            h = 1.6 * abs(v) / mx
            bars.add(Rectangle(width=0.035, height=max(h, 0.01), stroke_width=0,
                               fill_color=PREC["fp8_tensor"] if abs(v) > 0.5 * mx else GREY_B, fill_opacity=0.9)
                     .move_to([-6.0 + 0.045 * i, 1.6 + h / 2, 0]))
            if abs(v) > 0.5 * mx:
                big.append(bars[-1])
        bl = label(r"$128$ inputs of a matrix product in the series' model: \ a few large values", font_size=20,
                   color=GREY_A).next_to(bars, UP, buff=0.15).align_to(bars, LEFT)
        rows = VGroup(
            label(rf"one scale per tensor: \ ${100 * q['act_tensor']:.1f}\%$ error \ (activations), \ "
                  rf"${100 * q['w_tensor']:.1f}\%$ \ (weights)", font_size=22, color=PREC["fp8_tensor"]),
            label(rf"one scale per $1 \times 128$ tile, \ $128 \times 128$ block: \ ${100 * q['act_tile']:.1f}\%$, \ "
                  rf"${100 * q['w_block']:.1f}\%$", font_size=22, color=PREC["fp8_tile"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.2, 2.0, 0])
        rl = note(r"relative RMS error of E4M3, \ computed on the series' trained model", font_size=18)
        rl.next_to(rows, DOWN, buff=0.12).align_to(rows, LEFT)
        ds = VGroup(
            label(r"DeepSeek-V3's FP8 recipe (2024):", font_size=24, color=PREC["fp8_tile"]),
            label(rf"E4M3 for every tensor; \ one scale per $1 \times {D['tile_act']}$ tile of activations and per "
                  rf"${D['block_w']} \times {D['block_w']}$ block of weights", font_size=21, color=GREY_A),
            label(rf"tensor cores keep about ${D['accum_bits']}$ bits while summing: \ up to ${D['accum_err']:.0f}\%$ error "
                  rf"over $4{{,}}096$ terms, \ so partial sums move to FP32 every ${D['nc']}$", font_size=21,
                  color=GREY_A),
            label(r"embedding, output head, router, norms and attention kept in higher precision", font_size=21,
                  color=GREY_A),
            label(rf"loss within ${D['loss_err']}\%$ of BF16, \ on $671$B parameters and $14.8$T tokens", font_size=22,
                  color=PREC["fp8_tile"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).move_to([0.0, -1.5, 0])
        src = cite(r"DeepSeek-AI (2024), Sec.\ 3.3", corner=DR, font_size=17)
        with self.voiceover(
            "Eight bits is harder. E4M3, the eight-bit format with four exponent bits, spans only about eighteen "
            "powers of two, so every tensor needs a scale that moves its values into range. One scale per tensor, as the "
            "first FP8 recipes used, is set by the largest value. <bookmark mark='a'/> And real activations have a "
            "few large values. Here are 128 inputs to one matrix product of the series' model. "
            f"<bookmark mark='b'/> With one scale for the whole tensor, rounding to E4M3 costs "
            f"{100 * q['act_tensor']:.1f} percent; with one scale per tile of 128 values, "
            f"{100 * q['act_tile']:.1f}. <bookmark mark='c'/> DeepSeek-V3 trained its 671 billion parameters this way: "
            "a scale for every 128 values of an activation and every 128 by 128 block of a weight. It also found "
            "that the tensor cores keep only about fourteen bits while summing, so it moved the partial sums to FP32 "
            "every 128 terms, and kept the sensitive parts in higher precision. Its loss stayed within a quarter of "
            "a percent of a sixteen-bit run."
        ) as vo:
            self.play(FadeIn(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.005), run_time=2.0)
            vo.wait_until("a")
            self.play(*[Indicate(b, color=YELLOW) for b in big])
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rl))
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x_, shift=UP * 0.1) for x_ in ds], lag_ratio=0.3), FadeIn(src), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fp4(self):
        M, N, NS, K3 = F.MXFP8, F.NVFP4, F.NEMOTRON3, F.KIMIK3
        cells = VGroup(*[Square(0.3, stroke_width=0.8, stroke_color=BLACK, fill_color=PREC["fp8_tile"],
                                fill_opacity=0.7) for _ in range(16)]).arrange(RIGHT, buff=0.02)
        sc = Square(0.3, stroke_width=0.8, stroke_color=BLACK, fill_color=C.EDU, fill_opacity=0.9)
        sc.next_to(cells, LEFT, buff=0.15)
        blk = VGroup(sc, cells).move_to([-3.4, 2.2, 0])
        bt = VGroup(label(r"NVFP4: \ $16$ values of $4$ bits (E2M1)", font_size=20, color=PREC["fp8_tile"]),
                    label(r"share one $8$-bit scale (E4M3), \ plus one FP32 scale per tensor", font_size=20,
                          color=C.EDU)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(blk, DOWN, buff=0.2)
        bt.align_to(blk, LEFT)
        items = VGroup(
            label(rf"MXFP8, \ blocks of ${M['block']}$ (Blackwell): \ an ${M['params'] / 1e9:.0f}$B model on "
                  rf"${M['tokens'] / 1e12:.0f}$T tokens matches BF16 \ (NVIDIA, 2025)", font_size=21, color=GREY_A),
            label(rf"NVFP4: \ a ${N['params'] / 1e9:.0f}$B model on ${N['tokens'] / 1e12:.0f}$T tokens; \ MMLU-Pro "
                  rf"${N['mmlu_pro'][0]}\%$ against FP8's ${N['mmlu_pro'][1]}\%$", font_size=21, color=GREY_A),
            label(rf"\ \ with random Hadamard transforms, \ stochastic rounding, \ ${N['bf16_share']}\%$ of layers "
                  r"left in BF16", font_size=19, color=GREY_B),
            label(rf"Nemotron 3 Super (March 2026): \ pretrained in NVFP4, \ ${NS['tokens'] / 1e12:.0f}$T tokens",
                  font_size=21, color=PREC["fp8_tile"]),
            label(r"Kimi K3, DeepSeek-V4 (2026): \ four-bit weights learned in quantization-aware training", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0.2, -1.2, 0])
        tw = take_away(r"FP32 $\to$ BF16 $\to$ FP8 $\to$ FP4: \ each halving, \ a new scaling trick", font_size=24)
        src = cite(r"Mishra et al.\ (2025); \ NVIDIA (2025, 2026); \ Moonshot AI (2026); \ DeepSeek-AI (2026)",
                   corner=UR, font_size=16)
        with self.voiceover(
            "The newest chips go further, with scales in the hardware itself. NVIDIA's Blackwell multiplies "
            "microscaled formats: blocks of 32 numbers sharing one scale, MXFP8, and NVIDIA reported in 2025 that "
            "an eight-billion-parameter model trained in it on fifteen trillion tokens matched bfloat16. "
            "<bookmark mark='a'/> Then four bits: NVFP4 packs sixteen four-bit values with one eight-bit scale. "
            "<bookmark mark='b'/> NVIDIA pretrained a twelve-billion-parameter model on ten trillion tokens in it, "
            "with random rotations to spread out the outliers and stochastic rounding for the gradients, and kept "
            "sixteen percent of the layers in bfloat16; it matched the FP8 model's MMLU-Pro score to within a "
            "twentieth of a point. <bookmark mark='c'/> In March 2026, NVIDIA's Nemotron 3 Super was pretrained in "
            "NVFP4 on 25 trillion tokens. And Kimi K3 ships four-bit weights, and DeepSeek-V4 four-bit experts, both "
            "learned in quantization-aware training. <bookmark mark='d'/> Each halving of the bits came with a new way of "
            "scaling."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(blk), FadeIn(bt))
            vo.wait_until("b")
            self.play(FadeIn(items[1]), FadeIn(items[2]))
            vo.wait_until("c")
            self.play(FadeIn(items[3]), FadeIn(items[4]))
            vo.wait_until("d")
            self.play(FadeIn(tw, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
