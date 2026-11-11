from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load
from videos.cs.cs60.common import LogPlot, commas, say_dec, say_int

# NVIDIA Tesla V100 (Volta, 2017), SXM2 datasheet: 32-bit floating point on the ordinary lanes, tensor-core
# throughput (16-bit products, 32-bit sums), and HBM2 bandwidth.
V100_FP32 = 15.7e12
V100_TENSOR = 125e12
V100_BW = 900e9


class Gpu(VoiceoverScene):
    def construct(self):
        self.card()
        self.simt()
        self.tensor()
        self.amortize()
        self.wall()
        self.tiles()

    def card(self):
        card = chapter_card(6, r"GPUs revisited", r"How did a graphics chip become a matrix machine?",
                            lit=(2006, 2017), extra=((2006, r"CUDA"), (2017, r"Volta: \ tensor cores")), part=PART)
        with self.voiceover("Chapter six. GPUs revisited."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def simt(self):
        head = label(r"One instruction, \ thirty-two lanes", font_size=36).to_edge(UP, buff=0.3)
        lanes = VGroup(*[Square(0.55, stroke_color=GREY_B, stroke_width=1.5, fill_color=BG, fill_opacity=1)
                         for _ in range(32)]).arrange_in_grid(4, 8, buff=0.1)
        lanes.move_to([-1.8, -1.0, 0])
        nums = VGroup(*[label(f"{i}", font_size=17, color=GREY_C).move_to(sq) for i, sq in enumerate(lanes)])
        wl = label(r"one warp: \ 32 threads", font_size=20, color=GREY_A).next_to(lanes, DOWN, buff=0.2)
        instrs = [r"load $x[i]$", r"$y \leftarrow a\,x + y$", r"store $y[i]$"]
        ibox = RoundedRectangle(width=3.4, height=0.6, corner_radius=0.1, stroke_color=KERN, stroke_width=2,
                                fill_color=KERN, fill_opacity=0.12).next_to(lanes, UP, buff=1.0)
        itxt = label(instrs[0], font_size=21, color=WHITE).move_to(ibox)
        fl = label(r"fetch, \ decode: \ once", font_size=19, color=KERN).next_to(ibox, LEFT, buff=0.3)
        bcast = VGroup(*[Line(ibox.get_bottom(), lanes[i].get_top(), color=KERN, stroke_width=1, stroke_opacity=0.5)
                         for i in range(0, 8)])
        side = VGroup(
            wrapped_label(r"Part 10: \ single instruction, \ multiple threads", 3.6, font_size=19, color=WHITE),
            wrapped_label(r"chapter 1's overhead, \ shared 32 ways", 3.6, font_size=19, color=YES),
            wrapped_label(r"divergence: \ a branch the lanes disagree on runs both ways, \ half the lanes idle",
                          3.6, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)

        def light(color, which=range(32)):
            return [lanes[i].animate.set_fill(color if i in which else BG, opacity=0.45 if i in which else 1)
                    for i in range(32)]
        with self.voiceover(
            "Part 10 met the graphics processor's bargain: thousands of simple lanes instead of a few clever cores. "
            "<bookmark mark='a'/> Threads run in warps of thirty-two that share one instruction stream. "
            "<bookmark mark='b'/> One instruction is fetched and decoded, and thirty-two lanes each do a "
            "multiply-add: chapter one's overhead, shared thirty-two ways. <bookmark mark='c'/> The price is "
            "divergence. When the lanes disagree at a branch, the warp runs both paths, with some lanes switched off. "
            "<bookmark mark='d'/> A matrix product never diverges: every lane does the same multiply-add on "
            "different numbers. So in 2017 NVIDIA added hardware that does nothing else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lanes), FadeIn(nums), FadeIn(wl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(ibox), FadeIn(itxt), FadeIn(fl), Create(bcast))
            vo.wait_until("b")
            for k, ins in enumerate(instrs):
                if k:
                    self.play(Transform(itxt, label(ins, font_size=21, color=WHITE).move_to(ibox)), run_time=0.4)
                self.play(*light(YES), run_time=0.5)
                self.play(*light(BG, which=()), run_time=0.3)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Transform(itxt, label(r"if $x > 0$: \ \dots", font_size=21, color=WHITE).move_to(ibox)),
                      FadeIn(side[2]))
            odd = [i for i in range(32) if i % 3 == 0]
            even = [i for i in range(32) if i % 3 != 0]
            self.play(*light(HEAD, which=odd), run_time=0.6)
            self.play(*light(LAM, which=even), run_time=0.6)
            self.play(*light(BG, which=()), run_time=0.3)
            vo.wait_until("d")
            self.play(Indicate(side[1], color=YES))
        self.wait(0.4)
        self.clear_scene()

    def tensor(self):
        head = label(r"A tensor core: \ a small matrix multiplier", font_size=36).to_edge(UP, buff=0.3)
        A = [[1, 2, 0, 1], [0, 1, 3, 2], [2, 0, 1, 1], [1, 1, 2, 0]]
        B = [[2, 1, 0, 1], [1, 0, 2, 1], [0, 3, 1, 2], [1, 2, 1, 0]]
        C = [[1, 0, 0, 1], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1]]
        n = 4
        sz, gap = 0.62, 0.1
        cells = VGroup(*[Square(sz, stroke_color=GREY_B, stroke_width=2, fill_color=BG, fill_opacity=1)
                         for _ in range(16)]).arrange_in_grid(4, 4, buff=gap).move_to([-1.2, -1.0, 0])
        acc = [[C[i][j] for j in range(n)] for i in range(n)]

        def vals():
            return VGroup(*[label(f"{acc[i][j]}", font_size=22, color=WHITE).move_to(cells[i * n + j])
                            for i in range(n) for j in range(n)])
        v = vals()
        am = VGroup(*[label(f"{A[i][k]}", font_size=20, color=DATA).move_to(
            cells[i * n].get_center() + LEFT * (sz + gap) * (n - k) + LEFT * 0.25) for i in range(n) for k in range(n)])
        bm = VGroup(*[label(f"{B[k][j]}", font_size=20, color=LAM).move_to(
            cells[j].get_center() + UP * (sz * 0.72) * (n - k) + UP * 0.1) for k in range(n) for j in range(n)])
        al = label(r"$A$", font_size=24, color=DATA).next_to(am, LEFT, buff=0.2)
        bl = label(r"$B$", font_size=24, color=LAM).next_to(bm, LEFT, buff=0.25).align_to(bm, UP)
        dl = label(r"$C$, \ then $D$", font_size=22, color=WHITE).next_to(cells, DOWN, buff=0.2)
        eq = MathTex(r"D", r"=", r"A", r"\,", r"B", r"+", r"C", font_size=40).to_edge(RIGHT, buff=1.5).shift(UP * 1.6)
        eq[2].set_color(DATA)
        eq[4].set_color(LAM)
        side = VGroup(
            label(r"$4 \times 4 \times 4 = 64$ multiply-adds per clock", font_size=20, color=HEAD),
            label(r"products in float16, \ sums in float32", font_size=20, color=YES),
            wrapped_label(r"NVIDIA has not published the wiring inside: \ drawn here as a small grid, \ "
                          r"illustrative numbers", 4.2, font_size=19, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eq, DOWN, buff=0.5)
        side.align_to(eq, LEFT).shift(LEFT * 0.6)
        kl = label(r"$k = 0$", font_size=24, color=HEAD).next_to(cells, RIGHT, buff=0.4)
        with self.voiceover(
            "NVIDIA's Volta GPU of 2017 added tensor cores. <bookmark mark='a'/> Each computes D equals A times B "
            "plus C, on four by four matrices, every clock: four times four times four, sixty-four multiply-adds at "
            "once. <bookmark mark='b'/> Every output adds four products to its starting value, exactly what a cell "
            "of chapter three's grid did over four ticks. <bookmark mark='c'/> The products are taken in sixteen-bit "
            "floating point and the sums kept in thirty-two bits: multiply small, add wide, as in the TPU. "
            "<bookmark mark='d'/> NVIDIA has not published how a tensor core is wired, so this drawing is a sketch, "
            "but the idea is plain: a small matrix-multiply block, placed in every multiprocessor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(v), FadeIn(dl))
            vo.wait_until("a")
            self.play(Write(eq), FadeIn(am), FadeIn(bm), FadeIn(al), FadeIn(bl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(kl))
            for k in range(n):
                acol = VGroup(*[am[i * n + k] for i in range(n)])
                brow = VGroup(*[bm[k * n + j] for j in range(n)])
                for i in range(n):
                    for j in range(n):
                        acc[i][j] += A[i][k] * B[k][j]
                nv = vals()
                self.play(acol.animate.set_color(HEAD), brow.animate.set_color(HEAD),
                          Transform(kl, label(rf"$k = {k}$", font_size=24, color=HEAD).move_to(kl)), run_time=0.4)
                self.play(*[cells[i].animate.set_fill(HEAD, opacity=0.25) for i in range(16)],
                          Transform(v, nv), run_time=0.6)
                self.play(acol.animate.set_color(DATA), brow.animate.set_color(LAM),
                          *[cells[i].animate.set_fill(BG, opacity=1) for i in range(16)], run_time=0.3)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def amortize(self):
        head = label(r"Work per instruction", font_size=36).to_edge(UP, buff=0.3)
        specs = [(r"a scalar core", 1, GREY_B), (r"AVX-512 \ (16 floats)", 16, DATA),
                 (r"a warp's multiply-add", 32, LAM), (r"a warp's $16 \times 16 \times 16$ matrix step", 16 ** 3, YES)]
        lo, hi, width = 0.0, 4.0, 5.6
        x0 = -2.2
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (nm, v, c) in enumerate(specs):
            y = 1.7 - 0.62 * k
            w = max(0.05, width * (math.log10(v) - lo) / (hi - lo))
            b = Rectangle(width=w, height=0.4, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x0 + w / 2, y, 0])
            bars.add(b)
            names.add(label(nm, font_size=19, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.15))
            vals.add(label(commas(v), font_size=19, color=c).next_to(b, RIGHT, buff=0.12))
        ticks = VGroup(Line([x0, -0.4, 0], [x0 + width, -0.4, 0], color=GREY_C, stroke_width=1.5))
        for p in range(0, 5):
            x = x0 + width * (p - lo) / (hi - lo)
            ticks.add(Line([x, -0.45, 0], [x, -0.35, 0], color=GREY_C, stroke_width=1.5),
                      label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).move_to([x, -0.67, 0]))
        tl = label(r"multiply-adds per instruction \ (log scale)", font_size=18, color=GREY_A).next_to(ticks, DOWN,
                                                                                                       buff=0.35)
        rows = VGroup(
            MathTex(r"E_{\text{per multiply-add}}", r"=", r"E_{\text{op}}", r"+", r"\frac{E_{\text{overhead}}}{n}",
                    font_size=36),
            MathTex(r"n", r"=", r"16 \times 16 \times 16", r"=", r"4{,}096", font_size=36),
        ).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.9)
        rows[1][-1].set_color(YES)
        why = label(r"fetch, \ decode and scheduling paid once per instruction, \ spread over $n$ operations",
                    font_size=18, color=GREY_B).next_to(rows, DOWN, buff=0.2)
        src = note(r"CUDA's warp matrix interface \ (2017) \ works on $16 \times 16$ tiles", font_size=16)
        src.next_to(tl, DOWN, buff=0.12)
        with self.voiceover(
            "Count the multiply-adds that one instruction buys. <bookmark mark='a'/> A scalar core: one. A vector "
            "instruction of Part 10, sixteen floats wide: sixteen. A warp's multiply-add: thirty-two. "
            "<bookmark mark='b'/> And one warp-wide matrix step, on sixteen by sixteen tiles: sixteen cubed, four "
            "thousand and ninety-six. <bookmark mark='c'/> So write the energy of one multiply-add as the "
            "operation itself, plus the instruction's overhead shared among n. <bookmark mark='d'/> At four "
            "thousand operations per instruction, the overhead that dominated chapter one all but disappears, and a "
            "GPU running matrix work begins to look like an accelerator."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ticks), FadeIn(tl))
            vo.wait_until("a")
            for k in range(3):
                self.play(FadeIn(names[k]), GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(names[3]), GrowFromEdge(bars[3], LEFT), FadeIn(vals[3]), FadeIn(src), run_time=1.2)
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(why))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            self.play(Indicate(rows[1][-1], color=YES))
        self.wait(0.4)
        self.clear_scene()

    def wall(self):
        m = load("roofline")["machine"]
        pts = load("roofline")["points"]
        P, B = m["peak_gflops"] * 1e9, m["bandwidth_gbs"] * 1e9
        head = label(r"The memory wall, \ again", font_size=36).to_edge(UP, buff=0.3)
        plot = LogPlot(-2, 3, 9, 15, r"operations per byte", r"operations per second", x_length=6.4, y_length=4.4)
        plot.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        ours = plot.roof(P, B, DATA)
        fp32 = plot.roof(V100_FP32, V100_BW, LAM)
        tens = plot.roof(V100_TENSOR, V100_BW, YES)
        ol = label(r"this machine \ (measured on this machine)", font_size=16, color=DATA).next_to(
            plot.c2p(1.6, math.log10(P)), UP, buff=0.08)
        fl = label(r"V100 lanes, \ float32", font_size=16, color=LAM).next_to(plot.c2p(2.2, math.log10(V100_FP32)),
                                                                           DOWN, buff=0.1)
        tl = label(r"V100 tensor cores", font_size=16, color=YES).next_to(plot.c2p(2.2, math.log10(V100_TENSOR)),
                                                                        UP, buff=0.08)
        first = {}
        for p in pts:
            first.setdefault(p["kernel"], p)
        kern = [("axpy", first["axpy"]["intensity"]), ("matrix-vector", first["matrix-vector"]["intensity"])]
        marks = VGroup()
        for nm, i in kern:
            x = math.log10(i)
            marks.add(DashedLine(plot.c2p(x, 9), plot.c2p(x, 14.6), color=GREY_B, stroke_width=1.5),
                      label(nm, font_size=17, color=GREY_B).rotate(PI / 2).next_to(plot.c2p(x, 13.2), LEFT, buff=0.05))
        r32, rt = V100_FP32 / V100_BW, V100_TENSOR / V100_BW
        notes = VGroup(
            wrapped_label(rf"tensor cores: \ the flat roof {V100_TENSOR / V100_FP32:.0f} times higher", 4.6,
                          font_size=19, color=YES),
            wrapped_label(rf"the same memory: \ the ridge moves from {r32:.0f} to {rt:.0f} operations per byte", 4.6,
                          font_size=19, color=KERN),
            wrapped_label(r"the vector kernels of chapter 2 \ (dashed) \ sit on the slope on any of these machines",
                          4.6, font_size=19, color=WHITE),
            wrapped_label(r"faster arithmetic makes more of the work wait for memory", 4.6, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        src = note(r"V100: \ NVIDIA's datasheet, \ 2017 \ (15.7 and 125 TFLOP/s, \ 900 GB/s); \ intensities as "
                   r"counted in chapter 2", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Now the memory wall of Part 9, once more. <bookmark mark='a'/> Here is this machine's measured roof, and "
            "the roof of Volta's V100 from NVIDIA's datasheet: fifteen point seven trillion thirty-two-bit operations "
            "a second on its ordinary lanes, and nine hundred gigabytes a second from stacked memory. "
            "<bookmark mark='b'/> The tensor cores lift the flat roof eightfold, to a hundred and twenty-five "
            f"trillion. But the memory is the same, so the ridge moves from about {say_int(round(r32))} to about "
            f"{say_int(round(rt))} operations per byte. <bookmark mark='c'/> Chapter two's vector kernels sit far to "
            "the left, on the slope, whichever chip runs them. Faster arithmetic only makes more of the work wait "
            "for memory. That is why accelerators since have paired their arithmetic with stacked memory beside the "
            "chip, chapter eight's subject, and why the other remedy, reuse, matters more each generation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plot), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(ours), FadeIn(ol))
            self.play(Create(fp32), FadeIn(fl))
            vo.wait_until("b")
            self.play(Create(tens), FadeIn(tl), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(marks), FadeIn(notes[2]))
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def tiles(self):
        head = label(r"Climbing the slope: \ tiles", font_size=36).to_edge(UP, buff=0.3)
        u = 0.29
        nb = 8                                     # the drawn matrices are 8 x 8 blocks of u
        Cm = VGroup(*[Square(u, stroke_color=GREY_D, stroke_width=1, fill_color=BG, fill_opacity=1)
                      for _ in range(nb * nb)]).arrange_in_grid(nb, nb, buff=0)
        Am = Cm.copy()
        Bm = Cm.copy()
        Cm.move_to([-2.2, -1.55, 0])
        Am.next_to(Cm, LEFT, buff=0.35)
        Bm.next_to(Cm, UP, buff=0.35)
        ti, tj, b = 1, 5, 2                         # the highlighted tile: rows 2-3, columns 10-11 in block units
        for r in range(nb):
            for c in range(nb):
                if ti * b <= r < ti * b + b and tj // b * b <= c < tj // b * b + b:
                    Cm[r * nb + c].set_fill(HEAD, opacity=0.6)
        al = label(r"$A$", font_size=22, color=DATA).next_to(Am, DOWN, buff=0.1)
        bl = label(r"$B$", font_size=22, color=LAM).next_to(Bm, LEFT, buff=0.1)
        cl = label(r"$C$: \ one $b \times b$ tile", font_size=20, color=HEAD).next_to(Cm, DOWN, buff=0.1)
        rows_a = [r for r in range(ti * b, ti * b + b)]
        cols_b = [c for c in range(tj // b * b, tj // b * b + b)]
        rho = V100_TENSOR / V100_BW
        need = 2 * rho
        eqs = VGroup(
            MathTex(r"\text{flops}", r"=", r"2\,b^2 K", font_size=34),
            MathTex(r"\text{bytes}", r"=", r"2\,(bK + Kb)", r"=", r"4\,b K", font_size=34),
            MathTex(r"I", r"=", r"\frac{2\,b^2 K}{4\,b K}", r"=", r"\frac{b}{2}", font_size=34),
            MathTex(r"\frac{b}{2}", r"\ge", rf"{rho:.0f}", r"\;\Rightarrow\;", rf"b \ge {need:.0f}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.6).shift(UP * 0.35)
        eqs[2][-1].set_color(HEAD)
        eqs[3][-1].set_color(NO)
        whys = VGroup(label(r"$b^2$ outputs, \ $K$ multiply-adds each", font_size=17, color=GREY_B),
                      label(r"a strip of $A$ and of $B$, \ 2 bytes a number", font_size=17, color=GREY_B),
                      label(r"reuse grows with the tile", font_size=17, color=GREY_B),
                      label(r"to reach the V100's tensor ridge", font_size=17, color=GREY_B))
        for w, e in zip(whys, eqs):
            w.next_to(e, DOWN, buff=0.06).align_to(e, LEFT)
        foot = wrapped_label(r"real kernels tile at several levels at once: \ registers, \ shared memory, \ the L2 "
                             r"cache \ (Part 9's blocking, \ stacked)", 12.4, font_size=19, color=KERN)
        foot.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "How does any kernel climb that slope? By reuse, the blocking of Part 9. <bookmark mark='a'/> To compute "
            "one tile of the output, b by b, a multiprocessor reads a strip of A and a strip of B through its fast "
            "memory, a chunk at a time. <bookmark mark='b'/> The tile needs two b squared K operations, and the "
            "strips hold two b K numbers, two bytes each. <bookmark mark='c'/> Divide: the intensity is b over two. "
            "Bigger tiles, more reuse. <bookmark mark='d'/> To reach the tensor-core ridge, b must be about "
            f"{say_int(round(need))}. No single level of fast memory does that alone, so real kernels tile at "
            "every level at once, registers, shared memory and the cache: Part 9's lesson, stacked three deep."
        ) as vo:
            self.play(FadeIn(head), FadeIn(Cm), FadeIn(Am), FadeIn(Bm), FadeIn(al), FadeIn(bl), FadeIn(cl))
            vo.wait_until("a")
            for k in range(0, nb, 2):
                hi_a = [Am[r * nb + c] for r in rows_a for c in range(k, k + 2)]
                hi_b = [Bm[r * nb + c] for r in range(k, k + 2) for c in cols_b]
                self.play(*[s.animate.set_fill(DATA, opacity=0.7) for s in hi_a],
                          *[s.animate.set_fill(LAM, opacity=0.7) for s in hi_b], run_time=0.45)
                self.play(*[s.animate.set_fill(DATA, opacity=0.2) for s in hi_a],
                          *[s.animate.set_fill(LAM, opacity=0.2) for s in hi_b], run_time=0.3)
            self.play(Write(eqs[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[3]), FadeIn(whys[3]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD, NO, say_dec)
