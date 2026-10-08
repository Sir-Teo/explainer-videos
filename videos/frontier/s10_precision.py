from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Mono, Plot, bar_rows, calc, label, load, note, num_table, source

FORMATS = [  # name, sign, exponent, mantissa
    (r"FP32", 1, 8, 23),
    (r"BF16", 1, 8, 7),
    (r"FP8 (E4M3)", 1, 4, 3),
    (r"FP4 (E2M1)", 1, 2, 1),
]


def bit_row(name, s, e, m, cell=0.26):
    cells = VGroup()
    for k, (n, col) in enumerate([(s, C.SIGN_BIT), (e, C.EXP_BIT), (m, C.MAN_BIT)]):
        for _ in range(n):
            cells.add(Square(cell, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.55))
    cells.arrange(RIGHT, buff=0.03)
    lab = label(name, font_size=28).next_to(cells, LEFT, buff=0.3)
    nb = MathTex(str(s + e + m), font_size=28, color=GREY_A).next_to(cells, RIGHT, buff=0.25)
    g = VGroup(lab, cells, nb)
    g.cells, g.lab, g.n = cells, lab, nb
    return g


def heat_image(X: np.ndarray, width: float, height: float, vmax: float = 3.5) -> ImageMobject:
    """|x| on a log scale: black (0) -> blue -> white (the outliers)."""
    a = np.abs(np.asarray(X, float))
    v = np.clip((np.log10(a + 1e-4) + 1.5) / (vmax + 1.5), 0, 1)
    v = np.where(a == 0, 0.0, v)
    # black (zero) -> deep blue -> teal (typical, |x| ~ 1) -> yellow -> white (the outliers)
    stops = np.array([0.0, 0.25, 0.45, 0.75, 1.0])
    cols = np.array([[0.02, 0.03, 0.06], [0.08, 0.16, 0.38], [0.16, 0.55, 0.62], [0.95, 0.80, 0.25], [1.0, 1.0, 1.0]])
    rgb = np.stack([np.interp(v, stops, cols[:, c]) for c in range(3)], -1)
    img = ImageMobject((np.clip(rgb, 0, 1) * 255).astype(np.uint8))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    img.stretch_to_fit_width(width).stretch_to_fit_height(height)
    return img


class Precision(VoiceoverScene):
    def construct(self):
        self.p = load("precision")
        self.throughput()
        self.layouts()
        self.number_lines()
        self.decode()
        self.real_tensor()
        self.block_math()
        self.at_scale()

    # ------------------------------------------------------------------
    def throughput(self):
        bars = [  # (chip, format, dense PFLOP/s)  -- vendor datasheets, dense (no sparsity)
            (r"H100", r"BF16", 0.989),
            (r"H100", r"FP8", 1.979),
            (r"B300", r"FP8", 5.0),
            (r"B300", r"NVFP4", 15.0),
        ]
        rows = bar_rows([(chip + r"\; " + fmt, pf, C.COMPUTE, rf"{pf:g} PFLOP/s") for chip, fmt, pf in bars], 7.5 / 15.0,
                        font_size=30, bar_h=0.5, buff=0.45, name_color=WHITE, value_color=GREY_A, opacity=0.8)
        rows.move_to(DOWN * 0.2)
        title = label(r"Fewer bits per number $\Rightarrow$ more arithmetic per second", font_size=38).to_edge(UP, buff=0.6)
        src = source(r"NVIDIA H100 and Blackwell Ultra datasheets (dense throughput)")

        def bitrow(n):
            sq = VGroup(*[Square(0.3, stroke_width=1, stroke_color=BLACK, fill_color=C.COMPUTE, fill_opacity=0.85)
                          for _ in range(n)]).arrange(RIGHT, buff=0.04)
            sq.move_to(UP * 0.4)
            t = label(rf"{n} bits: {n // 8 if n >= 8 else 0.5:g} byte{'s' if n > 8 else ''} per number", font_size=30)
            return VGroup(sq, t.next_to(sq, DOWN, buff=0.35))
        rowb = bitrow(32)
        half = label(r"half the bits: $\approx 2\times$ the multiplications per second, half the memory to move",
                     font_size=26, color=GREY_A).to_edge(DOWN, buff=1.2)
        with self.voiceover(
            "Every number in a training run is stored in a fixed number of bits, and that choice is one of the "
            "biggest levers on speed. <bookmark mark='u'/> Use half as many bits, and a chip can do roughly twice as "
            "many multiplications per second, while moving half as much memory. <bookmark mark='h'/> An H100 does "
            "about a thousand trillion operations per second in sixteen-bit bfloat, and twice that in eight-bit. "
            "<bookmark mark='b'/> A Blackwell Ultra chip does fifteen thousand trillion in four-bit."
        ) as vo:
            self.play(FadeIn(title), FadeIn(rowb))
            vo.wait_until("u")
            for n in (16, 8, 4):
                self.play(Transform(rowb, bitrow(n)), FadeIn(half) if n == 16 else Wait(0.01), run_time=0.9)
                self.wait(0.3)
            vo.wait_until("h")
            self.play(FadeOut(rowb), FadeOut(half), run_time=0.5)
            for r in rows[:2]:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.8)
            self.play(FadeIn(src))
            vo.wait_until("b")
            for r in rows[2:]:
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]), run_time=0.8)
        self.clear_scene()

    # ------------------------------------------------------------------
    def layouts(self):
        rows = VGroup(*[bit_row(*f) for f in FORMATS]).arrange(DOWN, buff=0.45)
        for r in rows[1:]:
            r.cells.align_to(rows[0].cells, LEFT)
            r.lab.next_to(r.cells, LEFT, buff=0.3)
            r.n.next_to(r.cells, RIGHT, buff=0.25)
        rows.move_to(DOWN * 0.3)
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.7),
                                 label(t, font_size=26)).arrange(RIGHT, buff=0.15)
                          for c, t in [(C.SIGN_BIT, r"sign"), (C.EXP_BIT, r"exponent: the scale"),
                                       (C.MAN_BIT, r"mantissa: the precision")]]).arrange(RIGHT, buff=0.6)
        legend.to_edge(UP, buff=0.5)
        formula = MathTex(r"x = \pm\, 2^{\,\text{exponent}} \times 1.\text{mantissa}", font_size=36)
        formula.next_to(legend, DOWN, buff=0.3)

        with self.voiceover(
            "A floating-point number has three parts: a sign, an exponent that sets its scale, and a mantissa that "
            "sets its precision within that scale. <bookmark mark='a'/> Ordinary thirty-two-bit floats have eight "
            "exponent bits and twenty-three mantissa bits. <bookmark mark='b'/> Bfloat16 keeps all eight exponent "
            "bits but only seven of mantissa: the same range, less precision. It's the workhorse of training "
            "today. <bookmark mark='c'/> The eight-bit format called E4M3 has four exponent bits and three of "
            "mantissa, <bookmark mark='d'/> and four-bit E2M1 has just two exponent bits and one mantissa bit."
        ) as vo:
            self.play(FadeIn(legend), FadeIn(formula))
            for i, k in enumerate("abcd"):
                vo.wait_until(k)
                self.play(FadeIn(rows[i].lab), LaggedStart(*[FadeIn(c) for c in rows[i].cells], lag_ratio=0.02),
                          FadeIn(rows[i].n), run_time=1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def number_lines(self):
        e4, e2 = self.p["e4m3"], self.p["e2m1"]
        assert len(e4) == 127 and e4[-1] == 448 and list(e2) == [0, 0.5, 1, 1.5, 2, 3, 4, 6]
        lo, hi = 1e-3, 1e3
        L = 12.0
        x0 = -L / 2

        def xpos(v):
            return x0 + L * (np.log10(v) - np.log10(lo)) / (np.log10(hi) - np.log10(lo))

        axis = Line([x0, 0, 0], [x0 + L, 0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup()
        for e in range(-3, 4):
            ticks.add(Line([xpos(10.0**e), -0.08, 0], [xpos(10.0**e), 0.08, 0], color=GREY_C, stroke_width=2))
            ticks.add(MathTex(rf"10^{{{e}}}", font_size=24, color=GREY_A).move_to([xpos(10.0**e), -0.4, 0]))
        base = VGroup(axis, ticks).move_to(DOWN * 2.2)
        y8, y4 = 0.9, -0.6
        f8 = VGroup(*[Line([xpos(v), y8 - 0.28, 0], [xpos(v), y8 + 0.28, 0], color=C.EXP_BIT, stroke_width=2)
                      for v in e4[1:]])
        f4 = VGroup(*[Line([xpos(v), y4 - 0.28, 0], [xpos(v), y4 + 0.28, 0], color=C.MAN_BIT, stroke_width=4)
                      for v in e2[1:]])
        l8 = label(r"FP8 E4M3: 126 positive values, $2^{-9}$ to 448", font_size=28, color=C.EXP_BIT)
        l8.move_to([0, y8 + 0.7, 0])
        l4 = label(r"FP4 E2M1: 7 positive values, 0.5 to 6", font_size=28, color=C.MAN_BIT).move_to([0, y4 + 0.7, 0])
        vals = VGroup(*[MathTex(f"{v:g}", font_size=22, color=C.MAN_BIT).move_to([xpos(v), y4 - 0.5, 0])
                        for v in e2[1:]])
        head = label(r"Every number each format can store (log scale)", font_size=36).to_edge(UP, buff=0.5)

        with self.voiceover(
            "Here is every positive number each format can represent, on a log scale. <bookmark mark='a'/> FP8 has "
            "a hundred and twenty-six of them, from about two thousandths up to 448. <bookmark mark='b'/> FP4 has "
            "seven: one half, one, one and a half, two, three, four and six. That's all."
        ) as vo:
            self.play(FadeIn(head), Create(base))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(t) for t in f8], lag_ratio=0.01), FadeIn(l8), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in f4], lag_ratio=0.1), FadeIn(l4), FadeIn(vals), run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def decode(self):
        nv = load("math")["nvfp4"]
        assert nv["sb"] == 1.375 and nv["sb_bits"] == [0, 7, 3]

        def bits(sign, exp, man, ne):
            cells = VGroup()
            for b, col in [(sign, C.SIGN_BIT)] + [(x, C.EXP_BIT) for x in exp] + [(x, C.MAN_BIT) for x in man]:
                sq = Square(0.5, stroke_width=1.5, stroke_color=col, fill_color=col, fill_opacity=0.35)
                cells.add(VGroup(sq, Mono(str(b), font_size=26).move_to(sq)))
            cells.arrange(RIGHT, buff=0.06)
            cells[1:1 + ne].shift(RIGHT * 0.12)
            cells[1 + ne:].shift(RIGHT * 0.24)
            return cells
        e4 = MathTex(r"\text{E4M3:}\quad x = (-1)^{s} \times 2^{\,e-7} \times \left(1 + \tfrac{m}{8}\right)", font_size=36)
        e4.to_edge(UP, buff=0.5)
        r1 = bits(0, "0111", "011", 4)
        c1 = calc(r"e = 0111_2 = 7,\ m = 011_2 = 3:\quad x &= 2^{0} \times \left(1 + \tfrac38\right) = 1.375", font_size=32)
        r2 = bits(0, "1111", "110", 4)
        c2 = calc(r"e = 15,\ m = 6:\quad x &= 2^{8} \times \left(1 + \tfrac68\right) = 448\ \ \text{(the largest)}", font_size=32)
        e2 = MathTex(r"\text{E2M1 (FP4):}\quad x = 2^{\,e-1} \times \left(1 + \tfrac{m}{2}\right)", font_size=36)
        r3 = bits(0, "11", "1", 2)
        c3 = calc(r"e = 3,\ m = 1:\quad x &= 2^{2} \times 1.5 = 6\ \ \text{(the largest)}", font_size=32)
        lines = VGroup(VGroup(r1, c1).arrange(RIGHT, buff=0.5), VGroup(r2, c2).arrange(RIGHT, buff=0.5), e2,
                       VGroup(r3, c3).arrange(RIGHT, buff=0.5)).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        if lines.width > 13.0:
            lines.scale_to_fit_width(13.0)
        lines.next_to(e4, DOWN, buff=0.55).set_x(0)
        tag = label(r"$1.375$ is a real number from later in this chapter: the scale of one NVFP4 block", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Decoding one is simple arithmetic. In E4M3, the value is two to the exponent minus seven, times one plus "
            "the mantissa over eight. <bookmark mark='a'/> Take the bits 0, 0111, 011: the exponent is seven, so two "
            "to the zero; the mantissa is three, so the value is 1.375. <bookmark mark='b'/> The largest pattern, "
            "0, 1111, 110, is two to the eighth times 1.75: 448. <bookmark mark='c'/> FP4 works the same way with "
            "a bias of one: its largest value, 0, 11, 1, is four times 1.5, which is six."
        ) as vo:
            self.play(Write(e4))
            vo.wait_until("a")
            self.play(FadeIn(r1), run_time=0.6)
            self.play(Write(c1), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(r2), run_time=0.6)
            self.play(Write(c2))
            vo.wait_until("c")
            self.play(Write(e2), FadeIn(r3))
            self.play(Write(c3))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_tensor(self):
        p = self.p
        X = p["X"]
        T, Cn = X.shape
        toks = p["tokens"]
        i_paris = toks.index(" Paris")
        ch = p["outlier_channels"][0]
        assert ch == 447 and p["amax"] > 2500 and abs(p["median_abs"] - 1.2) < 0.2
        W, H = 11.0, 3.3
        img = heat_image(X, W, H).move_to(DOWN * 0.35)
        frame = SurroundingRectangle(img, buff=0.02, color=GREY_B, stroke_width=1.5)
        head = label(r"A real tensor: GPT-2's residual stream after 6 blocks", font_size=34).to_edge(UP, buff=0.45)
        dims = label(rf"{T} tokens $\times$ {Cn} channels; brightness $=|x|$, log scale", font_size=24,
                     color=GREY_A).next_to(head, DOWN, buff=0.15)
        ylab = label(r"tokens", font_size=22, color=GREY_A).rotate(PI / 2).next_to(frame, LEFT, buff=0.15)
        xlab = label(r"channels", font_size=22, color=GREY_A).next_to(frame, DOWN, buff=0.12)

        def cell_center(r, c):
            return img.get_corner(UL) + RIGHT * (c + 0.5) * W / Cn + DOWN * (r + 0.5) * H / T

        ring = Circle(radius=0.18, color=YELLOW, stroke_width=3).move_to(cell_center(0, ch))
        ol = label(rf"channel {ch}, first token: $x = {p['amax']:,.0f}$".replace(",", "{,}"), font_size=26,
                   color=YELLOW).next_to(frame, UP, buff=0.1).align_to(frame, RIGHT)
        typical = label(rf"a typical entry: $|x|\approx {p['median_abs']:.1f}$", font_size=26, color=GREY_A)
        typical.next_to(frame, UP, buff=0.1).align_to(frame, LEFT)

        with self.voiceover(
            "Because the range is so small, low-precision numbers are stored with a scale factor: divide by the "
            "scale, round, and multiply back. The question is how many numbers share one scale. "
            "<bookmark mark='t'/> Here is a real tensor: the residual stream of GPT-2 after six blocks, for one "
            "sentence. Forty-five tokens by 768 channels. <bookmark mark='ty'/> A typical entry is about one. "
            "<bookmark mark='o'/> But a few channels are enormous: this one reaches almost 2,900 at the first "
            "token. Such massive activations show up in many transformers."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(head), FadeIn(dims), FadeIn(img), Create(frame), FadeIn(ylab), FadeIn(xlab))
            vo.wait_until("ty")
            self.play(FadeIn(typical))
            vo.wait_until("o")
            self.play(Create(ring), FadeIn(ol))

        err = p["errors"]
        assert err["fp4_tensor"]["flushed"] > 0.999 and 0.08 < err["nvfp4"]["rel_rmse_typical"] < 0.15
        assert err["fp8_tensor"]["rel_rmse_typical"] < 0.03
        q4 = heat_image(p["q_fp4_tensor"], W, H).move_to(img)
        qn = heat_image(p["q_nvfp4"], W, H).move_to(img)
        tag4 = label(r"FP4, one scale for the whole tensor", font_size=28, color=C.REMOVED).next_to(frame, DOWN, buff=0.45)
        res4 = label(rf"{100 * err['fp4_tensor']['flushed']:.2f}\% of the values round to zero", font_size=28,
                     color=C.REMOVED).next_to(tag4, DOWN, buff=0.12)
        tagn = label(r"NVFP4: FP4 with one scale per block of 16 values", font_size=28, color=C.KEPT)
        tagn.move_to(tag4)
        resn = label(rf"error on ordinary channels: {100 * err['nvfp4']['rel_rmse_typical']:.0f}\%", font_size=28,
                     color=C.KEPT).next_to(tagn, DOWN, buff=0.12)

        with self.voiceover(
            "Now store it in FP4 with a single scale for the whole tensor. The outlier sets the scale, "
            "<bookmark mark='z'/> and every ordinary value rounds to zero: 99.99 percent of the tensor simply "
            "vanishes. <bookmark mark='n'/> Give every block of sixteen numbers its own scale, as NVIDIA's NVFP4 "
            "format does, and the picture comes back. Each value is still rounded coarsely, here with about twelve "
            "percent error, but the information survives."
        ) as vo:
            self.play(FadeIn(tag4), FadeOut(xlab))
            vo.wait_until("z")
            self.play(FadeOut(img), FadeIn(q4), run_time=1.2)
            self.play(FadeIn(res4))
            vo.wait_until("n")
            self.play(FadeOut(q4), FadeIn(qn), FadeOut(tag4), FadeOut(res4), FadeIn(tagn), run_time=1.2)
            self.play(FadeIn(resn))
        self.wait(0.5)

        # one token's vector, block by block
        x = X[i_paris, :64]
        qx = p["q_nvfp4"][i_paris, :64]
        bw = 0.15
        vmax = np.abs(x).max()
        hs = 2.6
        orig = VGroup(*[Rectangle(width=bw * 0.85, height=max(0.01, hs * abs(v) / vmax), stroke_color=GREY_A, stroke_width=1.5,
                                  fill_opacity=0).move_to([k * bw, 0.5 * hs * np.sign(v) * abs(v) / vmax, 0])
                        for k, v in enumerate(x)])
        quant = VGroup(*[Rectangle(width=bw * 0.5, height=max(0.01, hs * abs(v) / vmax), stroke_width=0,
                                   fill_color=C.KEPT, fill_opacity=0.95).move_to([k * bw, 0.5 * hs * np.sign(v) * abs(v) / vmax, 0])
                         for k, v in enumerate(qx)])
        bars = VGroup(orig, quant).move_to(DOWN * 0.6)
        braces = VGroup(*[BraceBetweenPoints(orig[16 * b].get_corner(DL) + DOWN * 1.2,
                                             orig[16 * b + 15].get_corner(DR) + DOWN * 1.2, DOWN, color=C.EXP_BIT)
                          for b in range(4)])
        for b, br in enumerate(braces):
            br.set_y(bars.get_bottom()[1] - 0.25)
        scales = VGroup(*[MathTex(rf"s_{b + 1}", font_size=28, color=C.EXP_BIT).next_to(br, DOWN, buff=0.08)
                          for b, br in enumerate(braces)])
        head2 = label(r"The token ``\,Paris'', first 64 of 768 channels", font_size=32).to_edge(UP, buff=0.5)
        key = VGroup(VGroup(Square(0.2, stroke_color=GREY_A, stroke_width=1.5, fill_opacity=0), label(r"original", font_size=24)).arrange(RIGHT, buff=0.12),
                     VGroup(Square(0.2, stroke_width=0, fill_color=C.KEPT, fill_opacity=0.9), label(r"NVFP4", font_size=24)).arrange(RIGHT, buff=0.12)
                     ).arrange(RIGHT, buff=0.5).next_to(head2, DOWN, buff=0.25)

        with self.voiceover(
            "Zooming in on one token, the word Paris: each block of sixteen values gets its own scale, stored "
            "in eight bits, <bookmark mark='b'/> so a large value only coarsens its own block, not the whole tensor."
        ) as vo:
            self.play(*[FadeOut(m) for m in [qn, frame, tagn, resn, ring, ol, typical, ylab, head, dims]], run_time=0.8)
            self.play(FadeIn(head2), FadeIn(key), FadeIn(orig, lag_ratio=0.02), run_time=1.2)
            self.play(FadeIn(quant, lag_ratio=0.02), run_time=1.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(b) for b in braces], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(s) for s in scales], lag_ratio=0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def block_math(self):
        nv = load("math")["nvfp4"]
        x, sc, q, dq = (np.array(nv[k]) for k in ("x", "scaled", "q", "deq"))
        st, sb = nv["st"], nv["sb"]
        assert round(nv["tensor_amax"]) == 2883 and round(st, 3) == 1.072 and round(nv["block_amax"], 2) == 8.84
        assert round(nv["sb_raw"], 3) == 1.374 and q[7] == 6.0 and q[1] == 3.0 and round(100 * nv["rel_err"], 1) == 9.6
        head = label(r"One NVFP4 block, step by step: 16 real values of `` Paris''", font_size=32).to_edge(UP, buff=0.35)
        steps = calc(r"s_{\rm tensor} &= \frac{\max|X|}{448 \times 6} = \frac{2883}{2688} = 1.072",
                     rf"\\ s_{{\rm block}} &= \operatorname{{round}}_{{\rm FP8}}\!\left(\frac{{8.84}}{{6 \times 1.072}}\right)"
                     rf" = \operatorname{{round}}_{{\rm FP8}}(1.374) = 1.375",
                     r"\\ \hat x &= \operatorname{round}_{\rm FP4}\!\left(\frac{x}{1.375 \times 1.072}\right) \times 1.375 \times 1.072",
                     font_size=30)
        steps.next_to(head, DOWN, buff=0.35).set_x(0)
        f2 = lambda v: f"{v + 0.0:.2f}" if abs(v) >= 0.005 else "0"  # noqa: E731  (no "-0.00")
        rows = [[r"x"] + [f2(v) for v in x], [r"x/s"] + [f2(v) for v in sc],
                [r"\text{FP4}"] + [f"{abs(v) if v == 0 else v:g}" for v in q], [r"\hat x"] + [f2(v) for v in dq]]
        tab = num_table([r""] + [""] * 16, rows, font_size=21, h_buff=0.16, v_buff=0.2,
                        col_colors=[GREY_A] + [WHITE] * 16)
        tab.header.set_opacity(0)
        tab.rule.set_opacity(0)
        for c, col in zip(tab.rows, [WHITE, GREY_A, C.MAN_BIT, C.KEPT]):
            c[1:].set_color(col)
        tab.next_to(steps, DOWN, buff=0.45).set_x(0)
        if tab.width > 13.4:
            tab.scale_to_fit_width(13.4)
        mark = VGroup(SurroundingRectangle(VGroup(*[r[8] for r in tab.rows]), buff=0.05, color=C.KEPT, stroke_width=2),
                      SurroundingRectangle(VGroup(*[r[2] for r in tab.rows]), buff=0.05, color=C.EDU, stroke_width=2))
        err = label(rf"block error: {100 * nv['rel_err']:.1f}\%", font_size=28, color=C.KEPT).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "Here's one block, step by step: sixteen real values from the Paris token. First, one scale for the "
            "whole tensor, so its largest value fits: 2,883, over 448 times 6, is 1.072. <bookmark mark='b'/> Then "
            "the block's own scale: its largest value is 8.84; divided by 6 and by 1.072 that's 1.374, rounded to "
            "the nearest FP8 number, the 1.375 we just decoded. <bookmark mark='q'/> Divide every value by the "
            "combined scale, round to the nearest FP4 value, and multiply back. <bookmark mark='r'/> The block's "
            "largest value, 8.84, becomes exactly 6 and comes back almost perfectly; 5.11 lands at 3.47, rounds to 3, "
            "and comes back as 4.42. <bookmark mark='e'/> Over the block, the error is 9.6 percent."
        ) as vo:
            self.play(FadeIn(head), Write(steps[0]))
            vo.wait_until("b")
            self.play(Write(steps[1]))
            vo.wait_until("q")
            self.play(Write(steps[2]))
            for r in tab.rows:
                self.play(FadeIn(r, shift=DOWN * 0.05), run_time=0.6)
            vo.wait_until("r")
            self.play(Create(mark[0]))
            self.play(Create(mark[1]))
            vo.wait_until("e")
            self.play(FadeIn(err))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def at_scale(self):
        err = self.p["errors"]
        fp8 = 100 * err["fp8_tensor"]["rel_rmse_typical"]
        assert fp8 < 3
        items = VGroup(
            label(r"\textbf{FP8} has 4 exponent bits: forgiving", font_size=32, color=C.EXP_BIT),
            label(rf"on this tensor, one scale for everything: {fp8:.1f}\% error", font_size=28, color=GREY_A),
            label(r"\textbf{DeepSeek-V3} (Dec 2024): FP8 training, a scale per $1\times128$ tile,", font_size=30),
            label(r"FP32 accumulation every 128 products; loss within 0.25\% of BF16", font_size=30, color=GREY_A),
            label(r"\textbf{Nemotron 3 Ultra} (Jun 2026): 550B parameters, 20T tokens, pretrained in \textbf{NVFP4}",
                  font_size=30),
            label(r"sensitive layers kept in higher precision; random Hadamard rotations, stochastic rounding",
                  font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for k in (1, 3, 5):
            items[k].shift(RIGHT * 0.4)
        items[2].shift(DOWN * 0.25)
        items[3].shift(DOWN * 0.25)
        items[4].shift(DOWN * 0.5)
        items[5].shift(DOWN * 0.5)
        items.move_to(ORIGIN)
        src = source(r"DeepSeek-V3 report (arXiv 2412.19437); NVIDIA, arXiv 2509.25149 and 2606.15007")

        with self.voiceover(
            "FP8, with its four exponent bits, is more forgiving: on this same tensor, even a single scale gives "
            "under three percent error. <bookmark mark='d'/> Labs still scale finely, for safety. DeepSeek-V3 was "
            "trained in FP8 with a separate scale for every 128 values, adding up partial sums in full precision "
            "every 128 products, and in tests against sixteen-bit training its loss stayed within a quarter of a "
            "percent. <bookmark mark='n'/> And in 2026, NVIDIA pretrained Nemotron 3 Ultra, a 550-billion-parameter "
            "model, on twenty trillion tokens in NVFP4, keeping the most sensitive layers in higher precision and "
            "using tricks like random rotations and stochastic rounding to tame the outliers."
        ) as vo:
            self.play(FadeIn(items[0]), FadeIn(items[1]))
            vo.wait_until("d")
            self.play(FadeIn(items[2]), FadeIn(items[3]), FadeIn(src))
            vo.wait_until("n")
            self.play(FadeIn(items[4]), FadeIn(items[5]))
        self.wait(0.6)
        self.clear_scene()
