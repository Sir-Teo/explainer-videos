from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, LogPlot, commas, grid_table, load,
                                   module_box, say_dec, say_int)

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


class Tpu(VoiceoverScene):
    def construct(self):
        self.card()
        self.chip()
        self.peak()
        self.roofs()
        self.quantize()
        self.accumulate()
        self.errors()

    def card(self):
        card = chapter_card(5, r"The TPU, \ and fewer bits", r"What do the numbers in Google's TPU paper mean?",
                            lit=(2015, 2017), extra=((2015, r"the TPU in Google's data centres"),
                                                     (2017, r"Jouppi et al.: \ the TPU paper")), part=PART)
        with self.voiceover("Chapter five. The TPU, and fewer bits."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def chip(self):
        t = load("energy")["tpu"]
        head = label(r"Inside the first TPU", font_size=36).to_edge(UP, buff=0.3)
        mxu = VGroup(Square(2.3, stroke_color=HEAD, stroke_width=3, fill_color=HEAD, fill_opacity=0.08))
        for k in range(1, 8):
            f = k / 8
            mxu.add(Line(mxu[0].get_corner(UL) + RIGHT * 2.3 * f, mxu[0].get_corner(DL) + RIGHT * 2.3 * f,
                         color=HEAD, stroke_width=0.8, stroke_opacity=0.4),
                    Line(mxu[0].get_corner(UL) + DOWN * 2.3 * f, mxu[0].get_corner(UR) + DOWN * 2.3 * f,
                         color=HEAD, stroke_width=0.8, stroke_opacity=0.4))
        mxl = label(rf"matrix unit \\ ${t['grid']} \times {t['grid']}$ cells", font_size=20, color=WHITE)
        mxl.move_to(mxu)
        bg = BackgroundRectangle(mxl, color=BG, fill_opacity=0.85, buff=0.08)
        mx = VGroup(mxu, bg, mxl).move_to([0.2, -0.3, 0])
        ub = module_box(rf"unified buffer \\ {t['unified_buffer_mib']} MiB \ (activations)", DATA, w=2.6, h=1.3,
                        font=19).move_to([-3.6, -0.3, 0])
        host = module_box(r"host CPU, \ over PCIe", GREY_B, w=2.6, h=0.6, font=18).move_to([-3.6, 1.55, 0])
        fifo = module_box(r"weight queue", LAM, w=2.3, h=0.5, font=18).next_to(mx, UP, buff=0.45)
        dram = module_box(rf"weight DRAM \\ 8 GiB, \ {t['dram_gb_per_s']} GB/s", KERN, w=2.6, h=0.95,
                          font=19).move_to([4.4, fifo.get_y(), 0])
        acc = module_box(rf"accumulators \ ({t['accumulator_bits']}-bit), \ 4 MiB", YES, w=2.9, h=0.55,
                         font=18).next_to(mx, DOWN, buff=0.4)
        act = module_box(r"activation unit", YES, w=2.6, h=0.55, font=18).move_to([-3.6, acc.get_y(), 0])
        boxes = VGroup(ub, host, fifo, dram, acc, act)
        paths = [
            Line(ub.get_right(), mx.get_left(), color=DATA),
            Line(dram.get_left(), fifo.get_right(), color=KERN),
            Line(fifo.get_bottom(), mx.get_top(), color=LAM),
            Line(mx.get_bottom(), acc.get_top(), color=YES),
            Line(acc.get_left(), act.get_right(), color=YES),
            Line(act.get_top(), ub.get_bottom(), color=YES),
            Line(host.get_bottom(), ub.get_top(), color=GREY_B),
        ]
        arrows = VGroup(*[Arrow(p.get_start(), p.get_end(), buff=0.05, stroke_width=3, color=p.get_color(),
                                max_tip_length_to_length_ratio=0.25) for p in paths])
        side = VGroup(
            label(rf"each cell: \ {t['operand_bits']}-bit multiply, \ add", font_size=19, color=HEAD),
            label(r"weights stay \ (chapter 4)", font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.6, -0.4, 0])
        src = note(rf"schematic, \ after Jouppi et al., \ ISCA 2017; \ {t['process_nm']} nm, \ "
                   rf"{t['clock_mhz']} MHz; \ not to scale", font_size=16).to_edge(DOWN, buff=0.2)

        def flow(k, color):
            d = Dot(paths[k].get_start(), radius=0.07, color=color)
            return d
        with self.voiceover(
            "Google put its Tensor Processing Unit into its data centres in 2015, and Norman Jouppi and colleagues "
            "described it in 2017. <bookmark mark='a'/> It is a coprocessor on the PCI Express bus: the host sends "
            "it instructions. "
            "<bookmark mark='b'/> At its centre is the matrix unit, a grid of two hundred and fifty-six by two "
            "hundred and fifty-six cells, each an eight-bit multiplier and an adder. <bookmark mark='c'/> Weights "
            "come from eight gibibytes of off-chip DRAM, through a queue, and are loaded into the grid from the top, "
            "where they stay. Activations stream in from the left, out of a twenty-four mebibyte buffer. "
            "<bookmark mark='d'/> Thirty-two-bit sums leave from the bottom, pass through the nonlinearity, and "
            "return to the buffer as the next layer's input."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(host), FadeIn(ub), GrowArrow(arrows[6]))
            vo.wait_until("b")
            self.play(FadeIn(mx), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(dram), FadeIn(fifo), GrowArrow(arrows[1]), GrowArrow(arrows[2]), FadeIn(side[1]),
                      GrowArrow(arrows[0]))
            dots = [flow(1, KERN), flow(2, LAM), flow(0, DATA)]
            self.play(MoveAlongPath(dots[0], paths[1]), run_time=0.8)
            self.play(FadeOut(dots[0]), MoveAlongPath(dots[1], paths[2]), MoveAlongPath(dots[2], paths[0]),
                      run_time=0.8)
            self.play(FadeOut(dots[1]), FadeOut(dots[2]), run_time=0.3)
            vo.wait_until("d")
            self.play(FadeIn(acc), FadeIn(act), *[GrowArrow(arrows[k]) for k in (3, 4, 5)])
            for _ in range(2):
                ds = [flow(k, c) for k, c in ((0, DATA), (2, LAM))]
                self.play(*[MoveAlongPath(d, paths[k]) for d, k in zip(ds, (0, 2))], run_time=0.6)
                self.play(*[FadeOut(d) for d in ds], run_time=0.2)
                for k in (3, 4, 5):
                    d = flow(k, YES)
                    self.play(MoveAlongPath(d, paths[k]), run_time=0.45)
                    self.remove(d)
        _ = boxes
        self.wait(0.4)
        self.clear_scene()

    def peak(self):
        e = load("energy")
        t = e["tpu"]
        peak, ridge = e["tpu_peak_ops_computed"], e["tpu_ridge_ops_per_byte"]
        head = label(r"Where 92 TOPS comes from", font_size=36).to_edge(UP, buff=0.3)
        grid = VGroup(*[Square(0.19, stroke_color=HEAD, stroke_width=1, fill_color=HEAD, fill_opacity=0.15)
                        for _ in range(256)]).arrange_in_grid(16, 16, buff=0.02)
        grid.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        gl = label(r"each square: \ $16 \times 16$ cells", font_size=18, color=GREY_A).next_to(grid, DOWN, buff=0.2)
        gt = label(rf"${t['grid']}^2 = {commas(t['macs'])}$ cells", font_size=22, color=HEAD).next_to(grid, UP,
                                                                                                    buff=0.2)
        p_e = f"{peak / 1e13:.2f}"
        r_e = f"{t['dram_gb_per_s'] / 10:.1f}"
        rows = VGroup(
            MathTex(r"\text{peak}", r"=", r"\text{cells}", r"\times", r"\text{ops per cell}", r"\times",
                    r"\text{clock}", font_size=34),
            MathTex(r"\text{peak}", r"=", commas(t["macs"]), r"\times", r"2", r"\times",
                    rf"{t['clock_mhz']}\times 10^{{6}}\,/\text{{s}}", font_size=34),
            MathTex(r"\text{peak}", r"=", rf"{p_e} \times 10^{{13}}", r"\ \text{ops/s}", r"\approx",
                    rf"{t['peak_tops_reported']}\ \text{{TOPS}}", font_size=34),
            MathTex(r"\text{ridge}", r"=", r"\frac{\text{peak}}{\text{DRAM bandwidth}}", r"=",
                    rf"\frac{{{p_e} \times 10^{{13}}}}{{{r_e} \times 10^{{10}}}}", r"\approx",
                    rf"{commas(int(round(ridge, -2)))}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        rows.next_to(grid, RIGHT, buff=0.6).shift(UP * 0.1)
        rows[2][-1].set_color(HEAD)
        rows[3][-1].set_color(KERN)
        whys = VGroup(label(r"a multiply and an add count as two", font_size=18, color=GREY_B),
                      label(r"the paper's figure, \ rounded", font_size=18, color=GREY_B),
                      label(r"operations per byte of weights fetched", font_size=18, color=KERN))
        for w, r in zip(whys, rows[1:]):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        src = note(r"cells and clock from Jouppi et al. 2017; \ the product computed here", font_size=16)
        src.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Where does the paper's famous figure come from? <bookmark mark='a'/> Sixty-five thousand five hundred "
            "and thirty-six cells. <bookmark mark='b'/> Each does a multiply and an add on every tick, counted as two "
            f"operations, at seven hundred million ticks a second. <bookmark mark='c'/> Multiply: {say_dec(peak / 1e12)} trillion operations a "
            "second: the paper's ninety-two tera-operations. <bookmark mark='d'/> Divide by the thirty-four "
            f"gigabytes a second of weight memory: the ridge of chapter two, about {say_int(int(round(ridge, -2)))} "
            "operations for every byte fetched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.004), FadeIn(gt), FadeIn(gl), run_time=1.6)
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(Write(rows[3]), FadeIn(whys[2]))
            self.play(Indicate(rows[3][-1], color=KERN))
        self.wait(0.4)
        self.clear_scene()

    def roofs(self):
        e = load("energy")
        m = load("roofline")["machine"]
        t = e["tpu"]
        P, B = m["peak_gflops"] * 1e9, m["bandwidth_gbs"] * 1e9
        TP, TB = e["tpu_peak_ops_computed"], t["dram_gb_per_s"] * 1e9
        head = label(r"Two roofs, \ one plot", font_size=36).to_edge(UP, buff=0.3)
        plot = LogPlot(-1, 4, 8, 14, r"operations per byte from DRAM", r"operations per second", x_length=6.4,
                       y_length=4.4)
        plot.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        ours = plot.roof(P, B, DATA)
        tpu = plot.roof(TP, TB, KERN)
        ol = label(r"this machine: \ measured on this machine", font_size=17, color=DATA).next_to(
            plot.c2p(2.4, math.log10(P)), DOWN, buff=0.12)
        tl = label(r"TPU v1: \ published figures", font_size=17, color=KERN).move_to(plot.c2p(0.9, 13.4))
        rd = [Dot(plot.c2p(math.log10(P / B), math.log10(P)), radius=0.06, color=DATA),
              Dot(plot.c2p(math.log10(TP / TB), math.log10(TP)), radius=0.06, color=KERN)]
        ratio_p, ratio_b = TP / P, TB / B
        notes = VGroup(
            wrapped_label(rf"flat roof: \ about {round(ratio_p, -2):,.0f} times higher".replace(",", "{,}"), 5.0,
                          font_size=19, color=HEAD),
            wrapped_label(rf"bandwidth: \ only {ratio_b:.1f} times higher, \ so the ridge moves from "
                          rf"{P / B:.1f} to about {round(TP / TB, -2):,.0f}".replace(",", "{,}"), 5.0, font_size=19,
                          color=KERN),
            wrapped_label(r"the paper's roofline: \ its multilayer perceptrons and LSTMs were limited by memory "
                          r"bandwidth, \ only its convolutional networks by arithmetic", 5.0, font_size=19,
                          color=WHITE),
            wrapped_label(r"against a 2015 Haswell server CPU and an NVIDIA K80 GPU, \ on inference: \ about "
                          r"15--30 times faster, \ 30--80 times the operations per watt", 5.0, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.15)
        src = note(r"TPU: \ Jouppi et al. 2017 \ (8-bit integer operations); \ this machine: \ 64-bit floating "
                   r"point", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Put the TPU's roof beside this machine's. <bookmark mark='a'/> Ours, measured, in blue. "
            "<bookmark mark='b'/> The TPU's, in orange: a flat roof more than a thousand times higher, but a sloped roof "
            "that hardly moves, because its weights came from ordinary DRAM. The ridge slides far to the right. "
            "<bookmark mark='c'/> The paper drew this picture for Google's own networks, and most of them sat under "
            "the slope, limited by memory, not by the grid. <bookmark mark='d'/> Its headline, fifteen to thirty "
            "times the speed of a contemporary CPU and GPU, is real, but it is a claim about inference, in eight "
            "bits, on those networks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ours), FadeIn(ol), FadeIn(rd[0]))
            vo.wait_until("b")
            self.play(Create(tpu), FadeIn(tl), FadeIn(rd[1]), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]), Indicate(rd[1], color=KERN, scale_factor=2))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def quantize(self):
        head = label(r"Eight bits: \ scale, \ then round", font_size=36).to_edge(UP, buff=0.3)
        xs = [0.82, -1.95, 0.31, 1.40]
        s = max(abs(v) for v in xs) / 127
        qs = [round(v / s) for v in xs]
        rows = VGroup(
            MathTex(r"x", r"\approx", r"s", r"\,", r"q", font_size=38),
            MathTex(r"s", r"=", r"\frac{\max_k |x_k|}{127}", font_size=38),
            MathTex(r"q", r"=", r"\operatorname{round}(x / s)", r"\in \{-127, \dots, 127\}", font_size=38),
            MathTex(r"|x - s\,q|", r"\le", r"\frac{s}{2}", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(LEFT, buff=0.8).shift(DOWN * 0.1)
        for r in rows:
            for p in r:
                if p.get_tex_string() == "q":
                    p.set_color(HEAD)
                if p.get_tex_string() == "s":
                    p.set_color(KERN)
        whys = VGroup(label(r"a real number as a scale times a small integer", font_size=18, color=GREY_B),
                      label(r"the largest value maps to 127", font_size=18, color=GREY_B),
                      label(r"the nearest of 255 levels", font_size=18, color=GREY_B),
                      label(r"the error is at most half a step", font_size=18, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        for k in range(1, 4):
            rows[k].shift(DOWN * 0.3 * k)
            whys[k].shift(DOWN * 0.3 * k)
        tab_rows = [[f"{v:.2f}", f"{v / s:.2f}", f"{q}", f"{s * q:.4f}", f"{abs(v - s * q):.4f}"]
                    for v, q in zip(xs, qs)]
        tab = grid_table([r"$x$", r"$x/s$", r"$q$", r"$s\,q$", r"error"], tab_rows, widths=[1.0, 1.15, 0.9, 1.2, 1.1],
                         row_h=0.5, font_size=21, mono_cols=())
        for r in range(1, len(tab_rows) + 1):
            tab.cells[r][2].set_color(HEAD)
            tab.cells[r][4].set_color(YES)
        tab.to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        sl = label(rf"$s = {max(abs(v) for v in xs):.2f} / 127 = {s:.5f}$; \ half a step: \ {s / 2:.4f}",
                   font_size=20, color=KERN).next_to(tab, DOWN, buff=0.35)
        ill = note(r"illustrative vector; \ symmetric, \ one scale per tensor", font_size=16).next_to(sl, DOWN,
                                                                                                   buff=0.2)

        def col(c):
            return VGroup(*[tab.cells[r][c] for r in range(1, len(tab_rows) + 1)])
        with self.voiceover(
            "The grid multiplies eight-bit integers, but weights are real numbers, so they are quantized. "
            "<bookmark mark='a'/> Write each number as a scale, s, times a small integer, q. "
            "<bookmark mark='b'/> Choose the scale so that the largest magnitude in the tensor becomes one hundred "
            "and twenty-seven. <bookmark mark='c'/> Then divide by the scale and round to the nearest integer: one of "
            "two hundred and fifty-five levels. <bookmark mark='d'/> For this vector, one point nine five sets the "
            "scale; divided by it, the numbers land between levels, and rounding moves each a little. "
            "<bookmark mark='e'/> Never more than half a step: Part 4's rounding argument, with one exponent "
            "shared by the whole tensor."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=DOWN * 0.2), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2], shift=DOWN * 0.2), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in tab.cells[0]], FadeIn(tab.rule), FadeIn(col(0)), FadeIn(ill))
            self.play(FadeIn(sl))
            for c in (1, 2, 3):
                self.play(TransformFromCopy(col(c - 1), col(c)), run_time=0.9)
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=DOWN * 0.2), FadeIn(whys[3]), TransformFromCopy(col(3), col(4)))
        self.wait(0.4)
        self.clear_scene()

    def accumulate(self):
        q = load("quant")["matmul"]
        head = label(r"Multiply small, \ add wide", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\sum_k x_k w_k", r"\approx", r"\sum_k", r"(s_x q_k)", r"(s_w r_k)", font_size=40),
            MathTex(r"\sum_k x_k w_k", r"\approx", r"s_x s_w", r"\sum_k", r"q_k r_k", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(head, DOWN, buff=0.5).shift(LEFT * 2.2)
        rows[1][4].set_color(HEAD)
        rows[1][2].set_color(KERN)
        why = VGroup(label(r"one scale per tensor: \ it comes out of the sum", font_size=19, color=GREY_B),
                     label(r"one rescale per output, \ not per term", font_size=19, color=KERN))
        why[0].next_to(rows[1], RIGHT, buff=0.4)
        why[1].next_to(why[0], DOWN, buff=0.12).align_to(why[0], LEFT)
        bound = VGroup(
            MathTex(r"|q_k r_k|", r"\le", r"127^2 = 16{,}129", r"< 2^{14}", font_size=34),
            MathTex(r"\Bigl|\sum_{k=1}^{256} q_k r_k\Bigr|", r"\le", r"256 \times 16{,}129 = 4{,}129{,}024",
                    r"< 2^{22}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(rows, DOWN, buff=0.55).align_to(rows, LEFT)
        bw = VGroup(label(r"each product fits in 16 bits", font_size=19, color=GREY_B),
                    label(r"so 32-bit sums cannot overflow", font_size=19, color=YES))
        for b, r in zip(bw, bound):
            b.next_to(r, RIGHT, buff=0.35)
        meas = wrapped_label(
            rf"measured: \ a ${q['n']} \times {q['n']}$ Gaussian product through int8, \ largest accumulator "
            rf"{commas(q['max_abs_int32_acc'])}, \ {q['int32_headroom_bits']:.0f} bits of headroom left; \ a "
            rf"${q['systolic_n']} \times {q['systolic_n']}$ slice through chapter 4's weight-stationary model: \ "
            + (r"exact" if q["systolic_int8_exact"] else r"mismatch") + rf" \ ({q['systolic_cycles']} cycles)",
            12.4, font_size=20, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now a dot product, the work of one column. <bookmark mark='a'/> Replace each input and weight by its "
            "scale times its integer. <bookmark mark='b'/> The scales come out of the sum: the grid adds products of "
            "small integers, and one multiplication per output restores the units. <bookmark mark='c'/> How wide "
            "must the sum be? Each product is at most sixteen thousand one hundred and twenty-nine, sixteen bits; "
            "two hundred and fifty-six of them fit in twenty-three. Thirty-two-bit accumulators cannot overflow. "
            "<bookmark mark='d'/> We checked: through int8, the "
            f"largest sum in a two hundred and fifty-six by two hundred and fifty-six product was "
            f"{say_int(q['max_abs_int32_acc'])}, and a slice run through chapter four's model of the grid gave "
            "exactly the integer answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(why[0]))
            self.play(FadeIn(why[1]))
            vo.wait_until("c")
            self.play(FadeIn(bound[0]), FadeIn(bw[0]))
            self.play(FadeIn(bound[1]), FadeIn(bw[1]))
            vo.wait_until("d")
            self.play(FadeIn(meas))
        self.wait(0.4)
        self.clear_scene()

    def errors(self):
        q = load("quant")
        mm, cl = q["matmul"], q["classifier"]
        e = load("energy")
        E = {r["op"]: r["pj"] for r in e["horowitz"]["table"]}
        g = e["our_multipliers"]
        head = label(r"What eight bits cost, \ and what they save", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"float32", mm["float32_rel_error"], YES), (r"float16 inputs", mm["float16_inputs_rel_error"], HEAD),
                 (r"int8, \ int32 sums", mm["int8_rel_error"], NO)]
        lo, hi, width = -8.0, 0.0, 5.2
        x0 = -4.2
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (nm, v, c) in enumerate(specs):
            y = 1.55 - 0.72 * k
            w = width * (math.log10(v) - lo) / (hi - lo)
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([x0 + w / 2, y, 0])
            bars.add(b)
            names.add(label(nm, font_size=19, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.15))
            ex = int(math.floor(math.log10(v)))
            vals.add(label(rf"${v / 10 ** ex:.1f} \times 10^{{{ex}}}$", font_size=19, color=c).next_to(b, RIGHT,
                                                                                                     buff=0.12))
        ticks = VGroup(Line([x0, -0.65, 0], [x0 + width, -0.65, 0], color=GREY_C, stroke_width=1.5))
        for p in range(-8, 1, 2):
            x = x0 + width * (p - lo) / (hi - lo)
            ticks.add(Line([x, -0.7, 0], [x, -0.6, 0], color=GREY_C, stroke_width=1.5),
                      label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).move_to([x, -0.92, 0]))
        ct = label(rf"relative error of a ${mm['n']} \times {mm['n']}$ product, \ against float64", font_size=20,
                   color=WHITE).next_to(VGroup(names, bars), UP, buff=0.3).align_to(names, LEFT)
        left = VGroup(ct, bars, names, vals, ticks)
        cls = VGroup(
            label(rf"a {cl['classes']}-class linear classifier, \ {commas(cl['test'])} test points", font_size=20,
                  color=WHITE),
            label(rf"float32: \ {100 * cl['float32_accuracy']:.2f}\% correct", font_size=21, color=YES),
            label(rf"int8: \ {100 * cl['int8_accuracy']:.2f}\% correct", font_size=21, color=NO),
            label(rf"same answer on {100 * cl['agreement']:.1f}\% of points", font_size=23, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).match_y(left)
        cost_rows = [[r"multiply energy \ (Horowitz)", rf"{E['int8 multiply']:g} pJ", rf"{E['fp16 multiply']:g} pJ",
                      rf"{E['fp32 multiply']:g} pJ"],
                     [r"our multiplier \ (gates)", commas(g["8"]["gates"]), commas(g["11"]["gates"]),
                      commas(g["24"]["gates"])]]
        cost = grid_table([r"", r"8-bit integer", r"float16 \ (11-bit mantissa)", r"float32 \ (24-bit)"], cost_rows,
                          widths=[3.6, 2.2, 3.4, 2.4], row_h=0.45, font_size=20, mono_cols=(),
                          colors=[[GREY_A, YES, HEAD, NO]] * 2)
        cost.to_edge(DOWN, buff=0.55).set_x(0)
        src = note(r"Horowitz, \ ISSCC 2014, \ 45 nm, \ approximate; \ gates: \ Part 4's tree multiplier, \ "
                   r"mantissa width only", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Is eight bits enough? <bookmark mark='a'/> We multiplied two random matrices three ways against "
            "sixty-four-bit floating point. Float32 is off by parts in ten million; sixteen-bit inputs, parts in ten "
            "thousand; eight bits, about one and a half percent. <bookmark mark='b'/> That sounds bad, until you ask "
            "what a network needs. A small classifier in float32 and in int8 gives the same answer on "
            f"{say_dec(100 * cl['agreement'])} percent of five thousand test points, and its accuracy changes in "
            "the fourth digit. <bookmark mark='c'/> And the saving: by Horowitz's figures an eight-bit multiply "
            f"takes about {FRACTION.get(int(e['ratios']['fp32_mult_over_int8_mult_energy']), 'a small fraction')} of "
            "the energy of a float32 one, and in our own circuits from Part 4 it is "
            f"about {FRACTION.get(round(g['24']['gates'] / g['8']['gates']), 'a small fraction')} of the gates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ct), FadeIn(ticks), FadeIn(names))
            vo.wait_until("a")
            for k in range(3):
                self.play(GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.8)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cls], lag_ratio=0.4), run_time=2)
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in cost.cells[0]], FadeIn(cost.rule), FadeIn(src))
            self.play(FadeIn(VGroup(*cost.cells[1])), FadeIn(VGroup(*cost.cells[2])))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, YES, NO, DATA)
