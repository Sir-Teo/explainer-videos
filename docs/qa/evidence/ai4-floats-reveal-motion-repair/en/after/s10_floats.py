from __future__ import annotations

import inspect
import math
import textwrap

import numpy as np

from explainer.ai import *  # noqa: F403
from explainer.ai.autodiff import log_softmax
from videos.ai.ai4.common import GRAD, HIST, MONO, PART, VALUE, bits_bar, load, log_axes

FMT_COL = {"fp32": WHITE, "bf16": C.TRUE_P, "fp16": C.BITS, "e5m2": C.SURPRISE, "e4m3": GRAD}
FMT_NAME = {"fp64": r"float64", "fp32": r"float32", "bf16": r"bfloat16", "fp16": r"float16", "e5m2": r"FP8 E5M2",
            "e4m3": r"FP8 E4M3FN"}


def big(x: float) -> str:
    """A format's largest number, for the screen: 65504, or 3.4 x 10^38."""
    return f"{x:,.0f}".replace(",", "{,}") if x < 1e6 else sci(x, 1)


class Floats(VoiceoverScene):
    def construct(self):
        self.card()
        self.layout()
        self.ulp()
        self.rounding()
        self.lse()

    def card(self):
        card = chapter_card(9, r"Numbers in a computer", r"What does a computer do with $0.1$?", lit=(1985,), part=PART)
        with self.voiceover("Chapter nine. Numbers in a computer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layout(self):
        d = load("floats")
        info = d["info"]
        hist = history_card(1985, r"IEEE 754, \ designed largely by William Kahan",
                            r"specified basic operations, formats and rounding modes; \ operation order still matters", width=5.6,
                            font_size=19, color=HIST).to_corner(UL, buff=0.3)
        form = MathTex(r"x = (-1)^{\,s} \times 1.m_1 m_2 \dots \times 2^{\,e - \text{bias}}", font_size=34)
        form.next_to(hist, RIGHT, buff=0.5).align_to(hist, UP).shift(DOWN * 0.2)
        normal = label(r"normal, finite numbers", font_size=20, color=GREY_B).next_to(form, DOWN, buff=0.12)
        keys = VGroup(label(r"sign", font_size=20, color=C.SIGN_BIT), label(r"exponent: \ range", font_size=20, color=C.EXP_BIT),
                      label(r"mantissa: \ precision", font_size=20, color=C.MAN_BIT)).arrange(RIGHT, buff=0.4)
        keys.next_to(normal, DOWN, buff=0.18)
        rows = VGroup()
        for k in ("fp32", "bf16", "fp16", "e5m2", "e4m3"):
            i = info[k]
            bar = bits_bar(1, i["exp"], i["man"], unit=0.17, height=0.36)
            nm = label(FMT_NAME[k], font_size=22, color=FMT_COL[k])
            stats = label(rf"${i['exp']}$ exponent, ${i['man']}$ mantissa bits \\ largest ${big(i['max'])}$; \ "
                          rf"$\approx {i['digits']:.1f}$ normal digits", font_size=19, color=GREY_A)
            rows.add(VGroup(nm, bar, stats))
        for r in rows:
            r[0].move_to([-5.4, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-3.4, 0, 0], aligned_edge=LEFT)
            r[2].move_to([2.6, 0, 0], aligned_edge=LEFT)
        rows.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        for r in rows:
            r[0].set_x(-6.6 + r[0].width / 2)
            r[1].set_x(-4.4 + r[1].width / 2)
            r[2].set_x(1.5 + r[2].width / 2)
        rows.to_edge(DOWN, buff=0.7)
        special = label(r"E4M3FN: \ finite values and NaN, \ no infinities", font_size=18, color=GREY_B)
        special.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Every number in this series so far has been a float. In 1985 one standard, IEEE 754, designed largely by "
            "William Kahan, specified basic operations and rounding. The same format, operation and rounding "
            "mode agree; changing the order or fusing operations can change a program's answer. "
            "<bookmark mark='a'/> A normal finite float has a sign, an exponent and a mantissa: one point the mantissa, "
            "times two to the exponent. Exponent bits buy range; mantissa bits buy precision. <bookmark mark='b'/> "
            "Float32 has eight and twenty-three. Bfloat16 keeps float32's eight exponent bits and only seven for the "
            "mantissa; float16 has five and ten; and the eight-bit formats of 2022 have four and three, or five and "
            "two. The E4M3 finite variant shown here reserves NaN but has no infinities."
        ) as vo:
            self.play(FadeIn(hist, shift=UP * 0.2), Write(form))
            vo.wait_until("a")
            self.play(FadeIn(normal), FadeIn(keys), Indicate(form, color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows], lag_ratio=0.35), run_time=2.5)
            self.play(FadeIn(special))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ulp(self):
        d = load("floats")
        info = d["info"]
        xs = np.asarray(d["xs"])
        format_keys = ("fp32", "bf16", "fp16", "e5m2", "e4m3")
        finite_logs = np.concatenate([np.log10(np.asarray(d[f"ulp_{k}"])[
            np.isfinite(d[f"ulp_{k}"]) & (np.asarray(d[f"ulp_{k}"]) > 0)]) for k in format_keys])
        ylo = min(-14, math.floor(float(finite_logs.min())))
        yhi = max(4, math.ceil(float(finite_logs.max())))
        g = log_axes((-8, 6), (ylo, yhi), x_length=7.4, y_length=5.0, xlabel=r"the number $x$",
                     ylabel=r"the gap to the next float, \ $\mathrm{ulp}(x)$", center=[-2.4, -0.3, 0], xstep=2, ystep=3)
        ax = g.ax
        lines = VGroup()
        for k in ("fp32", "bf16", "fp16", "e5m2", "e4m3"):
            u = np.asarray(d[f"ulp_{k}"])
            ok = np.isfinite(u) & (u > 0)
            yy = np.log10(u[ok])
            lines.add(curve(ax, np.log10(xs[ok]), yy, FMT_COL[k], 3))
        leg = legend([(FMT_COL[k], FMT_NAME[k]) for k in ("fp32", "bf16", "fp16", "e5m2", "e4m3")], font_size=20)
        leg.move_to([4.9, 1.6, 0])
        dc = definition_card(r"ulp: \ unit in the last place",
                             r"the gap to the next float. \\ "
                             r"Round to nearest; normal finite range, \\ "
                             r"without overflow: \\ "
                             r"relative error $\le 2^{-(m+1)}$ ($m$ mantissa bits). \\ "
                             r"Subnormals: fixed absolute spacing; \\ "
                             r"absolute rounding error $\le \tfrac12$ that spacing.",
                             width=5.0, font_size=20).move_to([4.25, -1.5, 0])
        min_normal = float(info["fp16"]["min_normal"])
        sub_gap = float(info["fp16"]["min_sub"])
        boundary = DashedLine(ax.c2p(math.log10(min_normal), ylo),
                              ax.c2p(math.log10(min_normal), math.log10(sub_gap) + 1), color=C.BITS, stroke_width=1.5)
        sub = label(r"float16: \ subnormal gap $2^{-24}$; \ normal from $2^{-14}$", font_size=18, color=C.BITS)
        sub.next_to(g, DOWN, buff=0.12).align_to(g, LEFT)
        semantics = label(r"enumerated format spacing; \ device arithmetic may flush subnormals to zero; \ "
                          r"undefined end-of-format gaps omitted", font_size=16, color=GREY_B).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "The gap between neighbouring floats, the unit in the last place, grows with the number itself: a "
            "staircase, one step per power of two in the normal range. Normal relative precision is about "
            f"{info['fp32']['digits']:.1f} decimal digits in float32, {info['bf16']['digits']:.1f} in bfloat16. "
            "Below the smallest normal number, subnormals instead have a fixed absolute gap: two to the minus "
            "twenty-four for float16. Relative error can then grow to one on underflow. The plot enumerates format "
            "values; some device arithmetic flushes subnormals to zero. "
            f"<bookmark mark='a'/> Each format also ends somewhere. Float16 stops at {info['fp16']['max']:,.0f}, the "
            f"four-bit-exponent FP8 at {info['e4m3']['max']:,.0f}, while bfloat16 keeps float32's exponent range. That is why bfloat16, Google's format for its "
            "TPUs, usually avoids the loss scaling often needed with float16. Part 17 covers the hardware, and Part 19 how "
            "models are squeezed into fewer bits still."
        ) as vo:
            self.play(FadeIn(g))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(leg), run_time=3.0)
            self.play(Create(boundary), FadeIn(sub), FadeIn(semantics))
            vo.wait_until("a")
            self.play(FadeIn(dc, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rounding(self):
        d = load("floats")
        r = d["rounding"]
        steps, inc = int(d["acc_steps"]), float(d["acc_inc"])
        exs = VGroup(
            label(rf"bfloat16: \ $1 + \tfrac{{1}}{{256}} \to {r['bf16_1p']:g}$, \ $257 \to {r['bf16_257']:g}$, \ "
                  rf"$\pi \to {r['bf16_pi']}$", font_size=22, color=C.TRUE_P),
            label(rf"float16: \ $2049 \to {r['fp16_2049']:g}$; \quad FP8 E4M3: \ $\pi \to {r['e4m3_pi']}$", font_size=22,
                  color=C.BITS),
            label(rf"float32: \ $0.1 \to {r['fp32_tenth']:.17f}$", font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(UL, buff=0.35)
        g = axes([0, steps, 2500], [0, 110, 25], x_length=7.6, y_length=3.5, xlabel=r"additions of $0.01$",
                 ylabel=r"the running sum", xticks=[0, 5000, 10000], yticks=[0, 50, 100], center=[-1.6, -1.25, 0])
        ax = g.ax
        ts = np.arange(1, steps // 100 + 1) * 100
        cols = {"fp32": WHITE, "fp16": C.BITS, "bf16": C.TRUE_P, "bf16_fp32acc": GRAD}
        names = {"fp32": r"float32", "fp16": r"float16", "bf16": r"bfloat16",
                 "bf16_fp32acc": r"bfloat16 numbers, float32 sum"}
        cs = {k: curve(ax, ts, np.asarray(d[f"acc_{k}"]), cols[k], 3) for k in cols}
        ends = {k: float(np.asarray(d[f"acc_{k}"])[-1]) for k in cols}
        leg = VGroup(*[label(rf"{names[k]}: \ ${ends[k]:.4g}$", font_size=21, color=cols[k]) for k in cols])
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([4.6, -1.3, 0])
        tenth = ends["bf16_fp32acc"] / steps
        with self.voiceover(
            "Rounding has consequences. In bfloat16, one plus one two-hundred-and-fifty-sixth is one, and 257 is "
            "256. Even 0.1 is not 0.1 in float32. <bookmark mark='a'/> Add 0.01 ten thousand times; the answer "
            f"should be 100. <bookmark mark='b'/> Float32 gets {ends['fp32']:.3f}. <bookmark mark='c'/> Float16 "
            f"stalls at {ends['fp16']:g}, and bfloat16 at {ends['bf16']:g}: once the sum is big enough, the gap "
            "between floats is more than twice 0.01, and every addition rounds back to where it was. "
            "<bookmark mark='d'/> In this experiment, keep each input in bfloat16 and accumulate sequentially in "
            f"float32: {ends['bf16_fp32acc']:.2f}, because 0.01 itself was rounded to {tenth:.6f}. "
            "Mixed-precision matrix units use the same wider-accumulation idea; their reduction order can differ."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(e) for e in exs], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(g))
            for k, mk in zip(cols, "bccd"):
                vo.wait_until(mk)
                self.play(Create(cs[k]), FadeIn(leg[list(cols).index(k)]), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lse(self):
        d = load("floats")
        ov = d["overflow_at"]
        p = np.asarray(d["lse_p"])
        rows = [
            cmath(r"\log \textstyle\sum_i e^{z_i}", r"=", r"\log\big(e^{m}\textstyle\sum_i e^{z_i - m}\big)", font_size=36),
            cmath(r"\log \textstyle\sum_i e^{z_i}", r"=", r"m + \log \textstyle\sum_i e^{z_i - m}", font_size=36),
            cmath(r"z_i - m \le 0", r"\;\Rightarrow\;", r"\text{no overflow; \ one term is } e^0 = 1", font_size=34),
        ]
        whys = [why(r"finite scores; \ $m = \max_i z_i$", font_size=22), why(r"the log of a product", font_size=22),
                why(r"so the sum is at least $1$", font_size=22)]
        step = ladder(self, rows, whys, keep=3, top=1.2, x=-2.6, buff=0.45, edge=6.9)
        z = [int(v) for v in d["lse_z"]]
        naive = VGroup(label(rf"scores ${z[0]}, {z[1]}, {z[2]}$ in float32:", font_size=24, color=GREY_A),
                       label(r"$e^{z} = \infty, \infty, \infty$; \ probabilities $\mathrm{NaN}$ \ (not a number)",
                             font_size=24, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        assert all(s_ == "inf" for s_ in d["lse_naive_e"]) and all(s_ == "nan" for s_ in d["lse_naive_p"])
        naive.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.5)
        over = label(rf"$e^{{z}}$ overflows above $z = {ov['fp32']:.1f}$ in float32, \ ${ov['fp16']:.1f}$ in float16",
                     font_size=22, color=GREY_B).next_to(naive, DOWN, buff=0.2).align_to(naive, LEFT)
        fixed = label(r"shifted: \ " + ", ".join(f"${v:.4f}$" for v in p), font_size=26, color=GRAD)
        src = [ln.split("  #")[0].rstrip() for ln in textwrap.dedent(inspect.getsource(log_softmax)).rstrip().split("\n")]
        code = code_block(src, font_size=17, font=MONO)
        code.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.6)
        fixed.next_to(code, RIGHT, buff=0.6).align_to(code, UP)
        if fixed.get_right()[0] > 6.8:
            fixed.next_to(code, UP, buff=0.5).to_edge(RIGHT, buff=0.4)
        cap = label(r"our library, \ \texttt{explainer/ai/autodiff.py}", font_size=20, color=GREY_B).next_to(code, UP, buff=0.12)
        cap.align_to(code, LEFT)
        hl = SurroundingRectangle(code[1], color=GRAD, buff=0.06)
        with self.voiceover(
            "Range has consequences too. The softmax exponentiates its scores, and e to the power "
            f"{math.ceil(ov['fp32'])} is already too big for float32; in float16, e to the {ov['fp16']:.1f} is. "
            "<bookmark mark='a'/> So scores of a thousand, nine hundred "
            "and ninety-nine and nine hundred and ninety-eight become infinities, and the probabilities become not a "
            "number. <bookmark mark='b'/> The fix is to subtract the largest score first. The log of a sum of "
            "exponentials is the maximum, <bookmark mark='c'/> plus the log of a sum in which every exponent is at "
            "most zero. <bookmark mark='d'/> For finite scores, no shifted exponential overflows, and the largest "
            "term is exactly one, so the sum can't vanish either. Very small terms may underflow harmlessly to zero. "
            "<bookmark mark='e'/> The same three scores now give clean probabilities, and our "
            "library's log-softmax does exactly this, in its first line."
        ) as vo:
            self.play(FadeIn(naive[0]))
            vo.wait_until("a")
            self.play(FadeIn(naive[1]), FadeIn(over))
            vo.wait_until("b")
            step(0)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2, transform=False)
            vo.wait_until("e")
            self.play(FadeIn(code), FadeIn(cap), FadeIn(fixed))
            self.play(Create(hl))
        self.wait(0.3)
        self.clear_scene()
