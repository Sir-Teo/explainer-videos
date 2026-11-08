from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, SystolicView, load


class Hook(VoiceoverScene):
    def construct(self):
        self.energy()
        self.wave()
        self.plan()

    def energy(self):
        e = load("energy")
        rows = {r["op"]: r["pj"] for r in e["horowitz"]["table"]}
        specs = [(r"8-bit integer add", rows["int8 add"], YES), (r"32-bit integer add", rows["int32 add"], YES),
                 (r"8-bit integer multiply", rows["int8 multiply"], YES),
                 (r"32-bit float multiply", rows["fp32 multiply"], HEAD),
                 (r"read 64 bits from an 8 KB SRAM", rows["8 KB SRAM read (64 bits)"], DATA),
                 (r"read 64 bits from a 1 MB SRAM", rows["1 MB SRAM read (64 bits)"], DATA),
                 (r"read 64 bits from DRAM", rows["DRAM read (64 bits), high"], NO)]
        head = label(r"Arithmetic is cheap; \ moving data is not", font_size=36).to_edge(UP, buff=0.3)
        lo, hi, width = -2.0, 3.6, 7.2          # log10 picojoules across the bar area
        x0 = -1.6
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (name, pj, col) in enumerate(specs):
            y = 2.0 - 0.68 * k
            w = width * (math.log10(pj) - lo) / (hi - lo)
            b = Rectangle(width=max(w, 0.04), height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([x0 + w / 2, y, 0])
            bars.add(b)
            names.add(label(name, font_size=19, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.2))
            vals.add(label(rf"{pj:g} pJ" if pj < 1000 else rf"{pj:,.0f} pJ", font_size=19, color=col).next_to(
                b, RIGHT, buff=0.15))
        ticks = VGroup()
        for p in range(-2, 4):
            x = x0 + width * (p - lo) / (hi - lo)
            ticks.add(Line([x, -2.55, 0], [x, -2.45, 0], color=GREY_C, stroke_width=1.5),
                      label(rf"$10^{{{p}}}$", font_size=16, color=GREY_B).move_to([x, -2.8, 0]))
        axis = VGroup(Line([x0, -2.5, 0], [x0 + width, -2.5, 0], color=GREY_C, stroke_width=1.5), ticks)
        src = note(r"energy per operation, \ 45 nm \ (Horowitz, \ ISSCC 2014; \ approximate); \ log scale", font_size=16)
        src.to_edge(DOWN, buff=0.3)
        ratio = rows["DRAM read (64 bits), high"] / rows["int8 add"]
        with self.voiceover(
            "Here is what things cost on a chip, in energy. <bookmark mark='a'/> Adding two eight-bit integers costs "
            "about three hundredths of a picojoule. A thirty-two-bit add, a tenth. An eight-bit multiply, a fifth. A "
            "thirty-two-bit floating-point multiply, nearly four. <bookmark mark='b'/> Now fetch the numbers. Reading "
            "sixty-four bits from a small memory on the chip costs ten picojoules, more than any of those operations. "
            "From a megabyte of on-chip memory, a hundred. <bookmark mark='c'/> And from DRAM, off the chip, thirteen "
            f"hundred to twenty-six hundred: as much as {round(ratio, -4):,.0f} eight-bit additions, for one read. "
            "<bookmark mark='d'/> A general-purpose processor spends most of its energy on neither: it goes on "
            "fetching, decoding and scheduling instructions, and on moving data between them. When Rehan Hameed and "
            "colleagues measured a video encoder in 2010, a chip built for that one job used about five hundred times "
            "less energy than general-purpose cores running it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(src))
            vo.wait_until("a")
            for k in range(4):
                self.play(FadeIn(names[k]), GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.7)
            vo.wait_until("b")
            for k in (4, 5):
                self.play(FadeIn(names[k]), GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.9)
            vo.wait_until("c")
            self.play(FadeIn(names[6]), GrowFromEdge(bars[6], LEFT), FadeIn(vals[6]), run_time=1.4)
            vo.wait_until("d")
            self.play(Indicate(VGroup(names[6], bars[6], vals[6]), color=NO))
        self.wait(0.4)
        self.clear_scene()

    def wave(self):
        w = load("wave")["os"]
        head = label(r"Sixteen cells, \ passing numbers to their neighbours", font_size=36).to_edge(UP, buff=0.3)
        view = SystolicView(w, size=0.9, gap=0.14, font_size=22)
        view.shift(RIGHT * 1.9 + DOWN * 0.6 - view.boxes.get_center())     # place by the grid, not its queues
        clock = label(r"cycle 0", font_size=26, color=HEAD).to_corner(UL, buff=0.5).shift(DOWN * 0.9)
        side = VGroup(label(r"each cell: \ $s \leftarrow s + a \cdot b$", font_size=22, color=WHITE),
                      label(r"$a$ moves right, \ $b$ moves down", font_size=20, color=GREY_A),
                      label(r"$C = AB$, \ one diagonal wave", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).next_to(clock, DOWN, buff=0.4, aligned_edge=LEFT)
        ok = label(rf"{w['cycles']} cycles: \ $C$ matches the integer product" if w["correct"] else r"mismatch",
                   font_size=22, color=YES if w["correct"] else NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This part's machine is very different from Pebble. <bookmark mark='a'/> It is a grid of sixteen cells, "
            "and each cell holds only a multiplier and an adder from Part 4, and a running sum. "
            "<bookmark mark='b'/> On every clock tick, each cell multiplies the two numbers it has just received, "
            "adds the product to its sum, and passes the numbers on: the blue ones from the left to the right, the "
            "purple ones from the top downwards. The rows of one matrix enter from the left, the columns of another "
            "from the top, each a step later than the one before, so the work sweeps across the grid as a diagonal "
            "wave. <bookmark mark='c'/> There is no program, no instruction fetched, no register file. After ten "
            "cycles the grid holds the product of two matrices, simulated gate by gate and checked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(view.boxes), FadeIn(view.acc), FadeIn(view.qa), FadeIn(view.qb))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(clock))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            for t in range(w["cycles"]):
                new_clock = label(rf"cycle {t + 1}", font_size=24, color=HEAD).move_to(clock)
                self.play(*view.step(t), Transform(clock, new_clock), run_time=0.85)
            vo.wait_until("c")
            self.play(FadeIn(ok))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        job = load("job")
        row = job["row"]
        title = label(rf"Part {PART}: \ Domain-Specific Hardware", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"why general-purpose speedups ended, \ in energy",
            r"the roofline of this machine, \ measured",
            r"a systolic array built from Part 4's multipliers",
            r"the TPU, \ and why eight bits are enough",
            r"GPUs, \ spatial machines, \ memory, \ sparsity",
            r"the Job as a circuit: \ ledger row 21",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 60 of Computer Science, Built. <bookmark mark='a'/> We will see why the free speedups of "
            "Act II ended, and why the answer was specialization; measure this machine's roofline; build a systolic "
            "array out of Part 4's multipliers and simulate it gate by gate; read the numbers in Google's TPU paper; "
            "revisit GPUs, spatial machines, computing near memory and sparsity; and finally turn the Job itself "
            f"into a circuit, which counts the thirty novels in about {1000 * row['seconds']:.0f} milliseconds."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, KERN, LAM)
