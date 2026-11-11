from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, load, module_box, tag_box,
                                   timeline_bar)

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


CHISEL = [
    "class MAC(w: Int) extends Module {",
    "  val io = IO(new Bundle {",
    "    val a = Input(UInt(w.W))",
    "    val b = Input(UInt(w.W))",
    "    val s = Output(UInt((3 * w).W))",
    "  })",
    "  val acc = RegInit(0.U((3 * w).W))",
    "  acc := acc + io.a * io.b",
    "  io.s := acc",
    "}",
]
PEBBLE = [
    "def hash_stage(bits=32):",
    "    c = Circuit(\"stage 2: rolling hash\")",
    "    h = c.input(\"h\", bits)",
    "    code = c.input(\"code\", 5)",
    "    add = prefix_adder(bits, \"kogge-stone\")",
    "    s = c.embed(add, a=h << 5, b=h)  # 33 h",
    "    u = c.embed(add, a=s, b=code)    # + code",
    "    c.output(\"h_next\", u)",
    "    return c",
]
HLS_C = [
    "int dot(const int8_t a[256],",
    "        const int8_t b[256]) {",
    "  int s = 0;",
    "  for (int i = 0; i < 256; i++) {",
    "#pragma HLS pipeline II=1",
    "    s += a[i] * b[i];",
    "  }",
    "  return s;",
    "}",
]


class Design(VoiceoverScene):
    def construct(self):
        self.card()
        self.flow()
        self.hls()
        self.agile()
        self.explore()
        self.widths()
        self.codesign()

    def card(self):
        card = chapter_card(10, r"How hardware is designed", r"How does an idea become a circuit, \ and which "
                            r"circuit?", lit=(2012, 2016, 2019),
                            extra=((2012, r"Bachrach et al.: \ Chisel"),
                                   (2016, r"Lee et al.: \ agile RISC-V chips"),
                                   (2019, r"Hennessy and Patterson: \ a new golden age")), part=PART)
        with self.voiceover("Chapter ten. How hardware is designed."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def flow(self):
        head = label(r"Programs that build circuits", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"register-transfer \\ description", DATA), (r"synthesis", KERN), (r"netlist \\ of gates", HEAD),
                 (r"place and \\ route", KERN), (r"layout: \\ tape-out", YES)]
        boxes = VGroup(*[module_box(t, c, w=2.1, h=0.85, font=18) for t, c in steps]).arrange(RIGHT, buff=0.42)
        boxes.next_to(head, DOWN, buff=0.45)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, stroke_width=3, color=GREY_B,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(boxes, boxes[1:])])
        langs = label(r"Verilog, \ VHDL \ (1980s)", font_size=18, color=GREY_A).next_to(boxes[0], DOWN, buff=0.12)
        ours = label(r"Pebble's HDL \ (Part 3)", font_size=18, color=HEAD).next_to(boxes[2], DOWN, buff=0.12)
        ch = code_block(CHISEL, size=16)
        py = code_block(PEBBLE, size=16)
        fr = []
        for blk, col in ((ch, LAM), (py, HEAD)):
            f = SurroundingRectangle(blk, color=col, buff=0.2, corner_radius=0.1, stroke_width=1.6)
            fr.append(VGroup(f, blk))
        panels = VGroup(*fr).arrange(RIGHT, buff=0.5, aligned_edge=UP).next_to(boxes, DOWN, buff=0.95)
        tl = VGroup(label(r"Chisel \ (Scala): \ a cell for any width $w$", font_size=18,
                          color=LAM).next_to(panels[0], UP, buff=0.12).align_to(panels[0], LEFT),
                    label(r"our Python: \ the Job unit's hash stage \ (simplified)", font_size=18, color=HEAD)
                    .next_to(panels[1], UP, buff=0.12).align_to(panels[1], LEFT))
        foot = wrapped_label(r"the program runs, \ and its output is a circuit: \ parameters, \ loops and functions "
                             r"generate hardware", 12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Chips are not drawn gate by gate. <bookmark mark='a'/> A designer writes a register-transfer "
            "description, in Verilog or VHDL, languages of the 1980s, which says what each register holds on the "
            "next tick. <bookmark mark='b'/> Synthesis turns it into gates, and place and route lays them out on "
            "silicon. <bookmark mark='c'/> In 2012 Jonathan Bachrach and colleagues at Berkeley released Chisel, "
            "hardware embedded in Scala: <bookmark mark='d'/> a class that, run with a width, produces a "
            "multiply-accumulate cell of that width. <bookmark mark='e'/> This series has worked that way since "
            "Part 3. Our hardware description is Python, and chapter eleven's hash stage is a function that "
            "returns a circuit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]), FadeIn(langs))
            vo.wait_until("b")
            for k in range(4):
                self.play(GrowArrow(arrows[k]), FadeIn(boxes[k + 1]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(panels[0][0]), FadeIn(tl[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(x) for x in ch], lag_ratio=0.12), run_time=2)
            vo.wait_until("e")
            self.play(FadeIn(panels[1][0]), FadeIn(tl[1]), FadeIn(ours))
            self.play(LaggedStart(*[FadeIn(x) for x in py], lag_ratio=0.12), run_time=2)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def hls(self):
        head = label(r"High-level synthesis: \ from a loop to a pipeline", font_size=36).to_edge(UP, buff=0.3)
        c = code_block(HLS_C, size=16)
        cf = VGroup(SurroundingRectangle(c, color=DATA, buff=0.2, corner_radius=0.1, stroke_width=1.6), c)
        cf.to_edge(LEFT, buff=0.5).shift(UP * 0.6)
        pragma = c[4]
        stages = [(r"load", DATA), (r"multiply", HEAD), (r"add", YES)]
        iters, cyc = 6, 8
        cw, rh = 0.7, 0.5
        org = [-0.1, 1.6, 0]
        grid = VGroup()
        for i in range(iters):
            row = VGroup()
            for s, (nm, col) in enumerate(stages):
                r = Rectangle(width=cw - 0.06, height=rh - 0.08, stroke_width=0, fill_color=col, fill_opacity=0.8)
                r.move_to([org[0] + (i + s + 0.5) * cw, org[1] - i * rh, 0])
                row.add(VGroup(r, label(nm[0].upper(), font_size=16, color=BLACK).move_to(r)))
            grid.add(row)
        ctop = VGroup(*[label(f"{t}", font_size=16, color=GREY_B).move_to([org[0] + (t + 0.5) * cw, org[1] + 0.45, 0])
                        for t in range(cyc)])
        cl = label(r"cycle", font_size=17, color=GREY_B).next_to(ctop, LEFT, buff=0.25)
        il = VGroup(*[label(rf"$i={i}$", font_size=16, color=GREY_B).next_to(grid[i][0], LEFT, buff=0.15)
                      for i in range(iters)])
        key = VGroup(*[label(rf"{nm[0].upper()}: \ {nm}", font_size=17, color=col) for nm, col in stages]).arrange(
            RIGHT, buff=0.4).next_to(grid, DOWN, buff=0.35).align_to(cl, LEFT)
        n_it, depth = 256, len(stages)
        rows = VGroup(
            MathTex(r"\text{cycles}", r"=", r"\text{depth}", r"+", r"(N - 1)\cdot \text{II}", font_size=32),
            MathTex(r"\text{cycles}", r"=", rf"{depth}", r"+", rf"{n_it - 1} \cdot 1", r"=",
                    rf"{depth + n_it - 1}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(key, DOWN, buff=0.4).align_to(cl, LEFT)
        rows[1][-1].set_color(YES)
        loop = label(r"the sum feeds back: \ one add must fit in one cycle", font_size=18, color=NO)
        loop.next_to(rows, DOWN, buff=0.25).align_to(rows, LEFT)
        tools = wrapped_label(r"the tool chooses the units, \ the memory ports and the registers; \ commercial: \ "
                              r"AMD's Vitis HLS, \ Siemens's Catapult; \ open: \ LegUp, \ Bambu", 5.6, font_size=18,
                              color=GREY_A).next_to(cf, DOWN, buff=0.35).align_to(cf, LEFT)
        ill = note(r"illustrative schedule", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "High-level synthesis starts from ordinary C. <bookmark mark='a'/> Here is a dot product, with one "
            "extra line asking for a pipelined loop. <bookmark mark='b'/> The tool splits each iteration into a "
            "load, a multiply and an add, and overlaps them like Part 7's pipeline, starting a new iteration "
            "every cycle. <bookmark mark='c'/> Two hundred and fifty-six iterations take two hundred and fifty-"
            "eight cycles. <bookmark mark='d'/> One thing cannot overlap: each add needs the previous sum, so the"
            " adder must finish within a cycle. <bookmark mark='e'/> This is how many software people program "
            "chapter seven's FPGAs, though the result depends heavily on how the C is written."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(cf))
            self.play(Indicate(pragma, color=HEAD))
            vo.wait_until("b")
            self.play(FadeIn(ctop), FadeIn(cl), FadeIn(key))
            for i in range(iters):
                self.play(FadeIn(il[i]), LaggedStart(*[FadeIn(x) for x in grid[i]], lag_ratio=0.3), run_time=0.55)
            vo.wait_until("c")
            self.play(Write(rows[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("d")
            adds = VGroup(*[grid[i][2] for i in range(iters)])
            self.play(Indicate(adds, color=NO), FadeIn(loop))
            vo.wait_until("e")
            self.play(FadeIn(tools))
        self.wait(0.4)
        self.clear_scene()

    def agile(self):
        head = label(r"Agile hardware", font_size=36).to_edge(UP, buff=0.3)
        sc = 0.28                                  # scene units per month
        x_off = -4.4
        months = 36

        def bar(a, b, y, col, txt=None):
            return timeline_bar(a, b, y, col, h=0.5, scale=sc, label_text=txt, size=17).shift(RIGHT * x_off)
        wy, ay = 1.3, -0.9
        water = VGroup(bar(0, 4, wy, LAM, r"spec"), bar(4, 14, wy, DATA, r"write RTL"),
                       bar(14, 26, wy, KERN, r"verify"), bar(26, 30, wy, HEAD, r"layout"),
                       bar(30, 34, wy, GREY_C, r"fab"))
        first = Star(n=5, outer_radius=0.17, color=YES, fill_opacity=1).move_to([x_off + 34 * sc, wy + 0.5, 0])
        fl = label(r"first silicon", font_size=17, color=YES).next_to(first, UP, buff=0.06)
        sprints = VGroup()
        ticks = VGroup()
        for k in range(12):
            a = 3 * k
            sprints.add(VGroup(bar(a, a + 1.6, ay, DATA), bar(a + 1.6, a + 2.8, ay, KERN)))
            ticks.add(Dot([x_off + (a + 2.9) * sc, ay + 0.38, 0], radius=0.06, color=HEAD))
        tapes = VGroup(*[Star(n=5, outer_radius=0.15, color=YES, fill_opacity=1).move_to([x_off + m * sc, ay - 0.5, 0])
                         for m in (12, 24, 36)])
        names = VGroup(label(r"waterfall", font_size=22, color=WHITE).next_to([x_off, wy, 0], LEFT, buff=0.2),
                       label(r"agile", font_size=22, color=WHITE).next_to([x_off, ay, 0], LEFT, buff=0.2))
        axis = VGroup(Line([x_off, -2.1, 0], [x_off + months * sc, -2.1, 0], color=GREY_C, stroke_width=1.5))
        for m in range(0, months + 1, 6):
            axis.add(Line([x_off + m * sc, -2.15, 0], [x_off + m * sc, -2.05, 0], color=GREY_C, stroke_width=1.5),
                     label(f"{m}", font_size=16, color=GREY_B).move_to([x_off + m * sc, -2.35, 0]))
        axis.add(label(r"months", font_size=17, color=GREY_B).move_to([x_off + months * sc / 2, -2.65, 0]))
        keys = VGroup(label(r"every few weeks: \ a working design, \ run in simulation or on an FPGA", font_size=17,
                            color=HEAD).next_to(sprints, UP, buff=0.32).align_to(sprints, LEFT),
                      label(r"small test chips along the way", font_size=17, color=YES).next_to(tapes[0], DOWN,
                                                                                                buff=0.12))
        foot = wrapped_label(r"Lee, \ Waterman, \ Asanovi\'c and colleagues \ (IEEE Micro, \ 2016): \ RISC-V chips "
                             r"built from generators such as Rocket Chip, \ in small iterations", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.3)
        ill = note(r"illustrative schedules", font_size=16).to_corner(UR, buff=0.3).shift(DOWN * 0.5)
        with self.voiceover(
            "Generators also changed how chips are planned. <bookmark mark='a'/> The traditional flow is a "
            "waterfall: specify, design, spend a year verifying, lay out, and only years in does anything run on "
            "silicon, so a mistake in the specification is found last. <bookmark mark='b'/> In 2016 Yunsup Lee, "
            "Andrew Waterman, Krste Asanovic and colleagues at Berkeley described the agile alternative behind "
            "their RISC-V chips: keep a working design at all times, change it in small steps, and run every "
            "version, in simulation or on an FPGA. <bookmark mark='c'/> Tape out small test chips along the way. "
            "With a generator, a new configuration is a change of parameters, not a rewrite."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            for b in water:
                self.play(GrowFromEdge(b, LEFT), run_time=0.6)
            self.play(FadeIn(first, scale=1.6), FadeIn(fl))
            vo.wait_until("b")
            self.play(FadeIn(keys[0]))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(s, LEFT), FadeIn(t)) for s, t in zip(sprints, ticks)],
                                  lag_ratio=0.3), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t, scale=1.6) for t in tapes], lag_ratio=0.3), FadeIn(keys[1]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def explore(self):
        c = load("cells")
        tm = load("accel")["timing"]
        tr, ar = c["kinds"]["tree"], c["kinds"]["array"]
        gps, ffps = tm["gate_ps"], tm["ff_ps"]
        head = label(r"Design-space exploration: \ two cells", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 800, 200], y_range=[0, 70, 10], x_length=5.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 20})
        ax.to_edge(LEFT, buff=0.9).shift(DOWN * 0.35)
        xl = label(r"gates \ (area)", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"depth \ (gate delays)", font_size=19, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        pt = Dot(ax.c2p(tr["gates"], tr["depth"]), radius=0.1, color=YES)
        pa = Dot(ax.c2p(ar["gates"], ar["depth"]), radius=0.1, color=LAM)
        lt = label(r"tree \ (Dadda $+$ Kogge--Stone)", font_size=18, color=YES).next_to(pt, DOWN, buff=0.15)
        la = label(r"array \ $+$ ripple carry", font_size=18, color=LAM).next_to(pa, UP, buff=0.15)
        better = Arrow(ax.c2p(260, 42), ax.c2p(90, 14), buff=0, color=GREY_B, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.15)
        bl = label(r"better", font_size=17, color=GREY_B).next_to(better.get_end(), RIGHT, buff=0.1)
        rows = VGroup(
            MathTex(r"T", r"=", r"d \cdot", rf"{gps:.0f}", r"\text{ ps}", r"+", rf"{ffps:.0f}", r"\text{ ps}",
                    font_size=32),
            MathTex(r"T_{\text{tree}}", r"=", rf"{tr['depth'] * gps + ffps:.0f}", r"\text{ ps}", r",\quad",
                    r"T_{\text{array}}", r"=", rf"{ar['depth'] * gps + ffps:.0f}", r"\text{ ps}", font_size=32),
            MathTex(r"G \cdot T", r":\quad", rf"{tr['gates'] * (tr['depth'] * gps + ffps):,.0f}".replace(",", "{,}"),
                    r"\ \text{vs}\ ", rf"{ar['gates'] * (ar['depth'] * gps + ffps):,.0f}".replace(",", "{,}"),
                    font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.6).shift(UP * 0.9)
        rows[2][2].set_color(YES)
        rows[2][4].set_color(LAM)
        whys = VGroup(label(r"the clock: \ depth times a gate delay, \ plus the register", font_size=18,
                            color=GREY_B),
                      label(r"the tree clocks almost twice as fast", font_size=18, color=GREY_B),
                      label(r"area $\times$ time per result: \ lower is better", font_size=18, color=GREY_B))
        for w, r in zip(whys, rows):
            w.next_to(r, DOWN, buff=0.1).align_to(r, LEFT)
        ratio = (ar['gates'] * (ar['depth'] * gps + ffps)) / (tr['gates'] * (tr['depth'] * gps + ffps))
        verdict = wrapped_label(rf"neither dominates: \ the array is smaller, \ the tree faster; \ per gate, \ the "
                                rf"tree does {ratio:.1f} times the work", 4.6, font_size=20, color=HEAD)
        verdict.next_to(whys[2], DOWN, buff=0.4).align_to(rows, LEFT)
        src = note(r"both cells built and checked gate by gate in chapter 3; \ the series' gate delay and register "
                   r"overhead", font_size=16).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Choosing among designs is design-space exploration. <bookmark mark='a'/> Chapter three built two "
            "multiply-accumulate cells. Plot each by its gates, a proxy for area, and its depth. The tree has "
            f"{say_int(tr['gates'])} gates and a depth of {say_int(tr['depth'])}; <bookmark mark='b'/> the array, "
            f"{say_int(ar['gates'])} gates and a depth of {say_int(ar['depth'])}. Neither wins on both. "
            "<bookmark mark='c'/> Turn depth into a clock: ten picoseconds a gate, plus seventy for the register."
            f" <bookmark mark='d'/> The tree's period is {say_int(int(tr['depth']*gps+ffps))} picoseconds, the "
            f"array's {say_int(int(ar['depth']*gps+ffps))}. <bookmark mark='e'/> Multiply area by time per result,"
            " and the tree wins, by about a fifth. Real tools sweep thousands of such points."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(pt, scale=1.6), FadeIn(lt))
            vo.wait_until("b")
            self.play(FadeIn(pa, scale=1.6), FadeIn(la))
            self.play(GrowArrow(better), FadeIn(bl))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1], shift=DOWN * 0.2), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2], shift=DOWN * 0.2), FadeIn(whys[2]))
            self.play(FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    def widths(self):
        g = load("energy")["our_multipliers"]
        ws = sorted(int(k) for k in g)
        head = label(r"The biggest knob: \ how many bits", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 28, 4], y_range=[0, 4500, 1000], x_length=5.8, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 20})
        ax.to_edge(LEFT, buff=1.1).shift(DOWN * 0.35)
        xl = label(r"operand width $n$ \ (bits)", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"gates in our tree multiplier", font_size=19, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(
            ax, LEFT)
        k = sum(g[str(n)]["gates"] / n ** 2 for n in ws) / len(ws)
        curve = ax.plot(lambda x: k * x * x, x_range=[0, 26], color=GREY_B, stroke_width=2.5)
        cl = label(rf"${k:.1f}\,n^2$", font_size=20, color=GREY_B).next_to(ax.c2p(26, k * 26 * 26), LEFT, buff=0.15)
        cols = {8: YES, 11: HEAD, 24: NO}
        names = {8: r"int8", 11: r"float16 mantissa", 24: r"float32 mantissa"}
        dots = VGroup(*[Dot(ax.c2p(n, g[str(n)]["gates"]), radius=0.09, color=cols[n]) for n in ws])
        dl = VGroup(*[label(rf"{names[n]}: \ {g[str(n)]['gates']:,}".replace(",", "{,}"), font_size=17,
                            color=cols[n]).next_to(d, {8: DR, 11: UL, 24: LEFT}[n], buff=0.1)
                    for n, d in zip(ws, dots)])
        rows = VGroup(
            MathTex(r"n \times n", r"\text{ partial products}", r"\Rightarrow", r"G(n) \propto n^2", font_size=32),
            MathTex(r"\frac{G}{n^2}", r":\quad", *[rf"\tfrac{{{g[str(n)]['gates']}}}{{{n * n}}} = "
                                                    rf"{g[str(n)]['gates'] / n ** 2:.1f}" + (r",\ " if i < 2 else "")
                                                    for i, n in enumerate(ws)], font_size=30),
            MathTex(r"\frac{G(24)}{G(8)}", r"=", rf"{g['24']['gates'] / g['8']['gates']:.2f}", r"\approx",
                    r"\left(\tfrac{24}{8}\right)^2", r"=", r"9", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.45).shift(UP * 0.8)
        rows[2][2].set_color(NO)
        depth = label(rf"depth grows slowly: \ {g['8']['depth']}, \ {g['11']['depth']}, \ {g['24']['depth']} "
                      r"gate delays", font_size=19, color=GREY_A).next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
        lesson = wrapped_label(r"so a format with a third of the bits needs about a ninth of the multiplier: \ "
                               r"chapter 5's choice, \ seen as a design space", 6.0, font_size=19, color=HEAD)
        lesson.next_to(depth, DOWN, buff=0.3).align_to(rows, LEFT)
        src = note(r"gate counts: \ Part 4's multipliers at each width, \ built by our instruments", font_size=16)
        src.to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "One knob moves a design further than any other: the number of bits. <bookmark mark='a'/> We built "
            "the same tree multiplier at eight bits, for int8; at eleven, the significand of a sixteen-bit float;"
            " and at twenty-four, that of a thirty-two-bit float. <bookmark mark='b'/> An n by n multiplier forms"
            " n squared partial products, so it should grow as n squared. <bookmark mark='c'/> Divide each count "
            "by n squared: about six and a half, every time. <bookmark mark='d'/> Three times the width costs "
            f"{say_int(round(g['24']['gates']/g['8']['gates']))} times the gates, while the depth grows only slowly. "
            "That is chapter five's case for eight bits, as a point in the design space."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            for d, t in zip(dots, dl):
                self.play(FadeIn(d, scale=1.6), FadeIn(t), run_time=0.6)
            vo.wait_until("b")
            self.play(Write(rows[0]))
            self.play(Create(curve), FadeIn(cl))
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=DOWN * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[2], shift=DOWN * 0.2))
            self.play(FadeIn(depth))
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def codesign(self):
        tm = load("accel")["timing"]
        hs = tm["stages"]["hash"]
        head = label(r"Co-design: \ bend the algorithm to the hardware", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"h", r"\leftarrow", r"33\,h", r"+", r"c", font_size=36),
            MathTex(r"h", r"\leftarrow", r"(32 + 1)\,h", r"+", r"c", font_size=36),
            MathTex(r"h", r"\leftarrow", r"(h \ll 5)", r"+", r"h", r"+", r"c", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.8).shift(UP * 1.3)
        rows[2][2].set_color(KERN)
        whys = VGroup(label(r"the Job unit's word hash \ (Bernstein's)", font_size=18, color=GREY_B),
                      label(r"33 is a power of two plus one", font_size=18, color=GREY_B),
                      label(r"a shift is only wires: \ no gates", font_size=18, color=KERN))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.35)
        cost = label(rf"so the hash stage is two adders: \ {commas_(hs['gates'])} gates, \ depth {hs['depth']}",
                     font_size=20, color=YES).next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        pairs = [(r"weights quantized to 8 bits", r"an 8-bit grid", r"ch.\ 5"),
                 (r"pruned two in every four", r"selectors in the tensor core", r"ch.\ 9"),
                 (r"bfloat16: \ float32's range, \ fewer bits", r"smaller multipliers", r"Google, \ TPUs"),
                 (r"attention computed in tiles", r"tiles that fit on-chip memory", r"Dao et al.\ 2022")]
        pr = VGroup()
        for a, h, ref in pairs:
            la = tag_box_tex(a, DATA)
            lh = tag_box_tex(h, KERN)
            arr = DoubleArrow(LEFT * 0.35, RIGHT * 0.35, buff=0, color=GREY_B, stroke_width=2.5,
                              max_tip_length_to_length_ratio=0.25)
            rl = label(ref, font_size=16, color=GREY_B)
            pr.add(VGroup(la, arr, lh, rl))
        wa = max(p[0].width for p in pr)
        wh = max(p[2].width for p in pr)
        for p in pr:
            p[0].move_to([-wa / 2, 0, 0])
            p[1].move_to([0.45, 0, 0])
            p[2].move_to([0.9 + wh / 2, 0, 0])
            p[3].next_to([0.9 + wh, 0, 0], RIGHT, buff=0.2)
        pr.arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(cost, DOWN, buff=0.6).set_x(0.3)
        hdr = VGroup(label(r"algorithm", font_size=20, color=DATA).next_to(pr[0][0], UP, buff=0.15),
                     label(r"hardware", font_size=20, color=KERN).next_to(pr[0][2], UP, buff=0.15))
        with self.voiceover(
            "Co-design chooses the algorithm and the hardware together, and our own unit is an example. "
            "<bookmark mark='a'/> Its word hash, Daniel Bernstein's, multiplies by thirty-three. "
            "<bookmark mark='b'/> Thirty-three is thirty-two plus one, <bookmark mark='c'/> and multiplying by "
            "thirty-two is a shift, which in hardware is only rewiring. So the hash stage is two adders, "
            f"{say_int(hs['gates'])} gates. <bookmark mark='d'/> The same move runs through this part: networks "
            "quantized for an eight-bit grid; pruned two in four for tensor cores; bfloat16, Google's format with"
            " float32's range in fewer bits; and Tri Dao's FlashAttention of 2022, which reorders a model's "
            "arithmetic into tiles that fit in on-chip memory, Part 9's blocking again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(cost))
            vo.wait_until("d")
            self.play(FadeIn(hdr))
            for p in pr:
                self.play(FadeIn(p[0], shift=RIGHT * 0.2), GrowFromCenter(p[1]), FadeIn(p[2], shift=LEFT * 0.2),
                          FadeIn(p[3]), run_time=0.7)
        self.wait(0.4)
        self.clear_scene()


def commas_(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def tag_box_tex(text: str, color, size=18, h=0.5):
    """A rounded box around a line of Tex (``tag_box`` is for monospace tokens)."""
    t = label(text, font_size=size, color=WHITE)
    box = RoundedRectangle(width=t.width + 0.35, height=h, corner_radius=0.08, stroke_color=color, stroke_width=1.6,
                           fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, tag_box)
