from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, grid_table, load, module_box

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def say_int(n: int) -> str:
    """An integer below a million as a speaker says it (British: 'one hundred and five')."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])
    if n < 1000:
        rest = n % 100
        return _ONES[n // 100] + " hundred" + ("" if rest == 0 else " and " + say_int(rest))
    rest = n % 1000
    return say_int(n // 1000) + " thousand" + ("" if rest == 0 else (" and " if rest < 100 else " ") + say_int(rest))


def say(x: float) -> str:
    """x to two significant figures, spoken: 83, 55, 'one point five'."""
    if x >= 10:
        return say_int(int(round(x)))
    v = round(x, 1)
    whole, tenth = int(v), int(round(10 * (v - int(v))))
    return say_int(whole) + ("" if tenth == 0 else " point " + _ONES[tenth])


def sig(x: float) -> str:
    """Two significant figures, for the screen."""
    if x >= 10:
        return f"{x:.0f}"
    if x >= 1:
        return f"{x:.1f}"
    return f"{x:.2g}"


class Roofline(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.intensity()
        self.measure()
        self.plot()
        self.reading()

    def card(self):
        card = chapter_card(2, r"The roofline model", r"How fast could this kernel possibly run here?",
                            lit=(1995, 2009), extra=((1995, r"McCalpin: \ STREAM"),
                                                     (2009, r"Williams, \ Waterman and Patterson: \ the roofline")),
                            part=PART)
        with self.voiceover("Chapter two. The roofline model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def derive(self):
        head = label(r"Two limits on every kernel", font_size=36).to_edge(UP, buff=0.3)
        mem = module_box(r"memory", KERN, w=2.2, h=1.0, font=22)
        cpu = module_box(r"processor", DATA, w=2.2, h=1.0, font=22)
        VGroup(mem, cpu).arrange(RIGHT, buff=3.0).next_to(head, DOWN, buff=0.7)
        pipe = DoubleArrow(mem.get_right(), cpu.get_left(), buff=0.08, color=GREY_B, stroke_width=3)
        beta = label(r"$\beta$ \ bytes per second", font_size=20, color=KERN).next_to(pipe, UP, buff=0.12)
        peak = label(r"$P$ \ flops per second", font_size=20, color=DATA).next_to(cpu, DOWN, buff=0.15)
        work = label(r"a kernel: \ $F$ flops, \ $Q$ bytes moved", font_size=20, color=GREY_A).next_to(mem, DOWN,
                                                                                                  buff=0.15)
        colors = {r"P": DATA, r"\beta": KERN, r"I": HEAD}
        rows = VGroup(
            MathTex(r"T", r"\ge", r"\frac{F}{P}", r"\quad\text{and}\quad", r"T", r"\ge", r"\frac{Q}{\beta}",
                    font_size=38),
            MathTex(r"\frac{F}{T}", r"\le", r"\min\!\left(P,\; \frac{F}{Q}\,\beta\right)", font_size=38),
            MathTex(r"\frac{F}{T}", r"\le", r"\min\!\left(P,\; I\,\beta\right)", r",\qquad", r"I = \frac{F}{Q}",
                    font_size=38),
        ).arrange(DOWN, buff=0.45).next_to(VGroup(peak, work), DOWN, buff=0.7)
        for r in rows:
            for part in r:
                for key, col in colors.items():
                    if part.get_tex_string() in (key, rf"\frac{{Q}}{{{key}}}", rf"\frac{{F}}{{{key}}}"):
                        part.set_color(col)
        rows[2][4].set_color(HEAD)
        whys = VGroup(label(r"the work cannot finish faster than the processor computes, \ nor than memory delivers",
                            font_size=20, color=GREY_B),
                      label(r"divide the work by the time", font_size=20, color=GREY_B),
                      label(r"arithmetic intensity: \ flops per byte", font_size=20, color=HEAD))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.06)
        whys[0].next_to(rows[0], RIGHT, buff=0.3)
        whys[1].next_to(rows[1], RIGHT, buff=0.3)
        whys[2].next_to(rows[2], RIGHT, buff=0.3)
        allg = VGroup(rows, whys)
        if allg.width > 13.2:
            allg.width = 13.2
        allg.set_x(0)
        with self.voiceover(
            "Part 9 ended by naming the roofline model; now we derive it, as Samuel Williams, Andrew Waterman and David "
            "Patterson did in 2009. <bookmark mark='a'/> A kernel does F floating-point operations and moves Q bytes "
            "between memory and the processor. The processor can do at most P operations a second; memory can "
            "deliver at most beta bytes a second. <bookmark mark='b'/> So the time is at least F over P, and at "
            "least Q over beta. <bookmark mark='c'/> Divide the work by the time: the speed is at most the smaller "
            "of P, and F over Q times beta. <bookmark mark='d'/> F over Q "
            "is called the arithmetic intensity, I, the operations done for each byte moved. The bound is the "
            "minimum of P and I times beta: a sloped roof for low intensity, a flat one for high."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mem), FadeIn(cpu), GrowArrow(pipe), FadeIn(beta), FadeIn(peak), FadeIn(work))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
        self.wait(0.4)
        self.clear_scene()

    def intensity(self):
        pts = load("roofline")["points"]
        first = {}
        for p in pts:
            first.setdefault(p["kernel"], p)
        mm = [p for p in pts if p["kernel"] == "matrix-matrix"]
        big = mm[-1]
        head = label(r"Counting flops and bytes", font_size=36).to_edge(UP, buff=0.3)
        axpy = VGroup(
            MathTex(r"y_i \leftarrow a\,x_i + y_i", font_size=36),
            label(r"2 flops: \ one multiply, \ one add", font_size=20, color=DATA),
            label(r"24 bytes: \ read $x_i$, \ read $y_i$, \ write $y_i$ \ (8 each)", font_size=20, color=KERN),
            MathTex(r"I", r"=", r"\frac{2}{24}", r"=", rf"{first['axpy']['intensity']:.3f}", font_size=36),
        ).arrange(DOWN, buff=0.25)
        gemm = VGroup(
            MathTex(r"C \leftarrow A\,B \quad (n \times n)", font_size=36),
            label(r"$2n^3$ flops: \ $n$ multiply-adds per entry", font_size=20, color=DATA),
            label(r"$24n^2$ bytes: \ read $A$, \ read $B$, \ write $C$", font_size=20, color=KERN),
            MathTex(r"I", r"=", r"\frac{2n^3}{24n^2}", r"=", r"\frac{n}{12}", font_size=36),
        ).arrange(DOWN, buff=0.25)
        tag_a = label(r"axpy", font_size=24, color=HEAD)
        tag_g = label(r"matrix product", font_size=24, color=HEAD)
        VGroup(VGroup(tag_a, axpy).arrange(DOWN, buff=0.3), VGroup(tag_g, gemm).arrange(DOWN, buff=0.3)).arrange(
            RIGHT, buff=1.6, aligned_edge=UP).next_to(head, DOWN, buff=0.45)
        for g in (axpy, gemm):
            g[3][0].set_color(HEAD)
        rows = [[r"axpy", f"{first['axpy']['intensity']:.3f}"], [r"dot product", f"{first['dot']['intensity']:.3f}"],
                [r"matrix-vector", f"{first['matrix-vector']['intensity']:.2f}"],
                [r"5-point stencil", f"{first['5-point stencil']['intensity']:.2f}"],
                [rf"matrix product, \ $n$ = {big['size']:,}".replace(",", "{,}"), f"{big['intensity']:.0f}"]]
        tab = grid_table([r"kernel", r"flops per byte"], rows, widths=[3.8, 2.2], row_h=0.36, font_size=19,
                         mono_cols=())
        tab.to_edge(DOWN, buff=0.3).set_x(0)
        ill = note(r"bytes: \ compulsory traffic, \ 8-byte floats, \ each array touched once", font_size=16)
        ill.next_to(tab, UP, buff=0.15)
        with self.voiceover(
            "Intensity is a matter of counting. <bookmark mark='a'/> Axpy, Part 52's simplest kernel, sets y to a x "
            "plus y. Each element costs two operations, a multiply and an add, and twenty-four bytes: x and y read, "
            "y written, eight bytes each. The intensity is one twelfth."
            " <bookmark mark='b'/> A matrix product of size n does two n cubed operations, but needs to "
            "read only two matrices and write one: twenty-four n squared bytes. The "
            "intensity is n over twelve, and it grows with n. <bookmark mark='c'/> Here are the kernels we will "
            f"measure. The vector kernels sit below one, and the largest matrix product at about "
            f"{say(big['intensity'])}. Getting close to that ideal is exactly what the blocking of Part 9 is for."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tag_a), LaggedStart(*[FadeIn(m) for m in axpy], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(tag_g), LaggedStart(*[FadeIn(m) for m in gemm[:3]], lag_ratio=0.5), run_time=2)
            self.play(FadeIn(gemm[3]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    def measure(self):
        m = load("roofline")["machine"]
        bw = m["bandwidth"]
        head = label(r"Measuring this machine's two roofs", font_size=36).to_edge(UP, buff=0.3)
        peaks = [s["gflops"] for s in m["peak"]["sizes"]]
        pnames = [rf"$n$ = {s['n']:,}".replace(",", "{,}") for s in m["peak"]["sizes"]]
        best_p = max(range(len(peaks)), key=lambda i: peaks[i])
        left = bar_chart(peaks, pnames, [YES if i == best_p else GREY_B for i in range(len(peaks))], height=2.8,
                         bar_w=0.75, gap=0.45, fmt_=lambda v: f"{v:.0f}", font_size=19)
        kinds = [("copy", "copy_gbs"), ("add", "add_gbs"), ("axpy", "daxpy_gbs"), ("dot", "dot_gbs")]
        bvals = [bw[k] for _, k in kinds]
        best_b = max(range(4), key=lambda i: bvals[i])
        right = bar_chart(bvals, [n for n, _ in kinds], [KERN if i == best_b else GREY_B for i in range(4)],
                          height=2.8, bar_w=0.75, gap=0.45, fmt_=lambda v: f"{v:.0f}", font_size=19)
        lt = label(r"peak: \ matrix products, \ GFLOP/s", font_size=21, color=YES)
        rt = label(rf"bandwidth: \ {bw['array_mb']:.0f} MB arrays, \ GB/s", font_size=21, color=KERN)
        lg, rg = VGroup(lt, left).arrange(DOWN, buff=0.35), VGroup(rt, right).arrange(DOWN, buff=0.35)
        VGroup(lg, rg).arrange(RIGHT, buff=1.6, aligned_edge=DOWN).next_to(head, DOWN, buff=0.45)
        P, B, R = m["peak_gflops"], m["bandwidth_gbs"], m["ridge_flops_per_byte"]
        ridge = MathTex(r"\text{ridge} = \frac{P}{\beta}", r"=", rf"\frac{{{P:.0f}}}{{{B:.0f}}}", r"\approx",
                        rf"{R:.1f}\ \text{{flops per byte}}", font_size=34, color=WHITE)
        ridge[-1].set_color(HEAD)
        ridge.next_to(VGroup(lg, rg), DOWN, buff=0.45)
        src = note(rf"measured on this machine: \ one core of a {m['cores']}-core Xeon, \ load average "
                   rf"{m['load_average']:.1f} when measured; \ best of several runs each", font_size=16)
        src.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Now the two roofs of the computer making this video. <bookmark mark='a'/> For the flat roof, time "
            "matrix products of four sizes through NumPy's BLAS, on one core, and keep the best: about "
            f"{say(P)} billion operations a second. <bookmark mark='b'/> For the sloped roof, stream arrays of "
            f"{say_int(int(bw['array_mb']))} megabytes, as John McCalpin's STREAM benchmark does, too large for the "
            f"caches. The four kernels disagree, by more than a factor of three; the roof is the best of them, about "
            f"{say(B)} gigabytes a second, and the others remind us it is an optimistic one. <bookmark mark='c'/> "
            f"Divide one by the other: the ridge sits at about {say(R)} operations per byte. A kernel needs at least "
            "that intensity before the processor, rather than memory, is what limits it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(lt), FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(rt), FadeIn(right))
            vo.wait_until("c")
            self.play(Write(ridge))
        self.wait(0.4)
        self.clear_scene()

    def _roof(self):
        """The log-log roofline of this machine, its points numbered, and a key."""
        d = load("roofline")
        m, pts = d["machine"], d["points"]
        P, B = m["peak_gflops"], m["bandwidth_gbs"]
        x0, x1, y0, y1 = -1.5, 2.5, -1.0, 2.0
        # Axes in shifted log units, so the axis lines run along the bottom and the left of the plot
        ax0 = Axes(x_range=[0, x1 - x0, 1], y_range=[0, y1 - y0, 1], x_length=6.6, y_length=4.5, tips=False,
                   axis_config={"color": GREY_D, "include_ticks": False})
        ax0.to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)

        class _Log:
            def c2p(self, u, v):
                return ax0.c2p(u - x0, v - y0)
        ax = _Log()
        lx = VGroup(*[label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(p, y0), DOWN, buff=0.12)
                      for p in range(-1, 3)])
        ly = VGroup(*[label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(x0, p), LEFT, buff=0.12)
                      for p in range(-1, 3)])
        xl = label(r"arithmetic intensity \ (flops per byte)", font_size=18, color=GREY_A).next_to(lx, DOWN,
                                                                                                    buff=0.12)
        yl = label(r"GFLOP/s", font_size=18, color=GREY_A).next_to(ax0, UP, buff=0.12).align_to(ax0, LEFT)
        lr = math.log10(P / B)
        roof = VMobject(color=KERN, stroke_width=4).set_points_as_corners(
            [ax.c2p(x0, x0 + math.log10(B)), ax.c2p(lr, math.log10(P)), ax.c2p(x1, math.log10(P))])
        rl = label(rf"ridge {P / B:.1f}", font_size=17, color=KERN).next_to(ax.c2p(lr, math.log10(P)), UP, buff=0.1)
        tag = label(r"measured on this machine", font_size=19, color=HEAD)
        tag.next_to(ax.c2p(x1, y0), UL, buff=0.2)

        def fam(k):
            if k == "matrix-matrix":
                return YES
            if k.startswith("Part 52"):
                return LAM
            if k.startswith("the Job"):
                return NO
            return DATA
        dots, nums, rows, cols = VGroup(), VGroup(), [], []
        # where each number goes beside its dot, so none collide
        place = [UR, UP, UR, DR, DOWN, DOWN, DOWN, DOWN, DR, UR, LEFT, RIGHT]
        for i, p in enumerate(pts):
            c = fam(p["kernel"])
            pos = ax.c2p(math.log10(p["intensity"]), math.log10(p["gflops"]))
            dot = Dot(pos, radius=0.07, color=c) if not p["kernel"].startswith("Part 52") else \
                Circle(radius=0.08, color=c, stroke_width=2.5).move_to(pos)
            dots.add(dot)
            nums.add(label(f"{i + 1}", font_size=16, color=c).next_to(dot, place[i % len(place)], buff=0.05))
            name = p["kernel"].replace("the Job (Python)", r"the Job, \ Python \ (est.)")
            if p["kernel"] in ("matrix-matrix", "Part 52 axpy", "Part 52 gemv", "Part 52 gemm"):
                name += rf", \ {p['size']:,}".replace(",", "{,}", 1) if p["kernel"] == "matrix-matrix" else ""
            rows.append([f"{i + 1}", name, sig(p["intensity"]), sig(p["gflops"]),
                         rf"{100 * p['fraction_of_roof']:.{1 if p['fraction_of_roof'] < 0.01 else 0}f}\%"])
            cols.append([c, c, WHITE, WHITE, YES if p["fraction_of_roof"] > 0.75 else
                         (HEAD if p["fraction_of_roof"] > 0.25 else NO)])
        key = grid_table([r"", r"kernel", r"flop/B", r"GFLOP/s", r"of roof"], rows, widths=[0.45, 2.9, 0.95, 1.05, 0.9],
                         row_h=0.32, font_size=17, colors=cols, mono_cols=())
        key.to_edge(RIGHT, buff=0.3).set_y(-0.1)
        return VGroup(ax0, lx, ly, xl, yl), roof, rl, tag, dots, nums, key, pts, ax

    def plot(self):
        frame, roof, rl, tag, dots, nums, key, pts, _ax = self._roof()
        head = label(r"The roofline of this machine", font_size=36).to_edge(UP, buff=0.3)
        mem = [i for i, p in enumerate(pts) if p["kernel"] in ("axpy", "dot", "matrix-vector", "5-point stencil")]
        mm = [i for i, p in enumerate(pts) if p["kernel"] == "matrix-matrix"]
        rest = [i for i in range(len(pts)) if i not in mem + mm]
        src = note(r"Part 52's kernels: \ open circles; \ the Job's operations are estimated, \ four per byte",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Here is the result, on logarithmic axes. <bookmark mark='a'/> The orange line is the roof: rising "
            "with intensity, at the bandwidth we measured, until it meets the flat peak at the ridge. "
            "<bookmark mark='b'/> The vector kernels, axpy, the dot product, matrix times vector and the stencil, "
            "sit far to the left, on or under the sloped roof: memory decides their speed. <bookmark mark='c'/> The "
            "matrix products sit to the right of the ridge, close under the flat roof: the processor decides theirs. "
            "<bookmark mark='d'/> The open circles are Part 52's timings of the same three levels of linear algebra, "
            "and the red dot is the Job itself, counting words in Python, with its operations estimated at four per "
            "byte."
        ) as vo:
            self.play(FadeIn(head), Create(frame[0]), FadeIn(frame[1:]))
            vo.wait_until("a")
            self.play(Create(roof), FadeIn(rl), FadeIn(tag), FadeIn(key.rule),
                      *[FadeIn(c) for c in key.cells[0]])
            for mk, group in zip("bcd", (mem, mm, rest)):
                vo.wait_until(mk)
                self.play(*[FadeIn(dots[i], scale=1.5) for i in group], *[FadeIn(nums[i]) for i in group],
                          *[FadeIn(c) for i in group for c in key.cells[i + 1]])
            self.play(FadeIn(src))
        self.wait(0.4)
        self.clear_scene()

    def reading(self):
        frame, roof, rl, tag, dots, nums, key, pts, ax = self._roof()
        en = load("energy")
        head = label(r"Reading the roofline", font_size=36).to_edge(UP, buff=0.3)
        job = next(i for i, p in enumerate(pts) if p["kernel"].startswith("the Job"))
        sten = next(i for i, p in enumerate(pts) if p["kernel"] == "5-point stencil")
        axpy = next(i for i, p in enumerate(pts) if p["kernel"] == "axpy")
        mmx = [i for i, p in enumerate(pts) if p["kernel"] == "matrix-matrix"]
        frac = [pts[i]["fraction_of_roof"] for i in mmx]
        js = pts[job]
        jroof = ax.c2p(math.log10(js["intensity"]), math.log10(js["roof_gflops"]))
        gap = DashedLine(dots[job].get_top(), jroof, color=NO, stroke_width=2.5)
        gl = label(rf"$\approx\times${round(js['roof_gflops'] / js['gflops'], -2):.0f}", font_size=18, color=NO).next_to(gap, LEFT,
                                                                                                   buff=0.1)
        ridge_tpu = en["tpu_ridge_ops_per_byte"]
        notes = VGroup(
            wrapped_label(rf"axpy: \ {100 * pts[axpy]['fraction_of_roof']:.0f}\% of its roof; \ the stencil only "
                          rf"{100 * pts[sten]['fraction_of_roof']:.0f}\%: \ NumPy builds a temporary array for each "
                          r"addition, \ moving far more bytes than we counted", 6.0, font_size=19, color=DATA),
            wrapped_label(rf"matrix products: \ {100 * min(frac):.0f}--{100 * max(frac):.0f}\% of the peak", 6.0,
                          font_size=19, color=YES),
            wrapped_label(r"the Job in Python: \ far under its roof; \ the interpreter's instructions are the cost, "
                          r"\ chapter one's overhead", 6.0, font_size=19, color=NO),
            wrapped_label(rf"TPU v1's ridge: \ about {round(ridge_tpu, -2):,.0f} operations per byte of DRAM".replace(",", "{,}")
                          + r" \ (92 TOPS over 34 GB/s, \ Jouppi et al. 2017): \ chapter five", 6.0, font_size=19,
                          color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.2)
        with self.voiceover(
            "What does the picture tell us? <bookmark mark='a'/> Axpy runs at "
            f"{say_int(round(100 * pts[axpy]['fraction_of_roof']))} percent of its sloped roof: nothing will make it "
            f"much faster on this machine. The stencil manages only {say_int(round(100 * pts[sten]['fraction_of_roof']))}"
            " percent, because NumPy builds a temporary array for every addition and so moves far more bytes than "
            "the count we made. <bookmark mark='b'/> The matrix products run within sight of the peak, as a kernel "
            "with high intensity should. <bookmark mark='c'/> And the Job sits "
            f"about {say_int(int(round(js['roof_gflops'] / js['gflops'], -2)))} times below its roof. Neither memory nor arithmetic "
            "holds it back; the interpreter's own instructions do, the overhead of chapter one. <bookmark mark='d'/> "
            "An accelerator raises the flat roof, and pushes the ridge far to the right. Google's "
            "first TPU, with ninety-two trillion operations a second and thirty-four gigabytes a second of memory, "
            f"has its ridge near {say_int(int(round(ridge_tpu, -2)))} operations per byte. Only work like "
            "the matrix product can feed it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(roof), FadeIn(rl), FadeIn(tag), FadeIn(dots), FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), Indicate(dots[axpy], scale_factor=2), Indicate(dots[sten], scale_factor=2))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), *[Indicate(dots[i], scale_factor=1.8, color=YES) for i in mmx])
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), Create(gap), FadeIn(gl))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
