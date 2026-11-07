from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, module_box
from videos.cs.cs60.common import commas, say_int

# The reduction of the pim section (illustrative): 2^28 four-byte numbers, spread over 16 banks.
N_ITEMS, ITEM_BYTES, BANKS, PARTIAL_BYTES = 2 ** 28, 4, 16, 8


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.byte()
        self.wires()
        self.stacked()
        self.pim()
        self.crossbar()

    def card(self):
        card = chapter_card(8, r"Computing near memory", r"If moving data costs most, \ why not move the work?",
                            lit=(2013, 2014, 2021), extra=((2013, r"HBM standardized"),
                                                           (2014, r"Horowitz: \ the cost of moving data"),
                                                           (2021, r"Samsung: \ HBM-PIM")), part=PART)
        with self.voiceover("Chapter eight. Computing near memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def byte(self):
        E = {r["op"]: r["pj"] for r in load("energy")["horowitz"]["table"]}
        head = label(r"The energy of one byte", font_size=36).to_edge(UP, buff=0.3)
        lo_d, hi_d = E["DRAM read (64 bits), low"] / 8, E["DRAM read (64 bits), high"] / 8
        specs = [(r"add two bytes \ (8-bit add)", E["int8 add"], YES),
                 (r"one byte from an 8 KB SRAM", E["8 KB SRAM read (64 bits)"] / 8, DATA),
                 (r"one byte from a 32 KB SRAM", E["32 KB SRAM read (64 bits)"] / 8, DATA),
                 (r"one byte from a 1 MB SRAM", E["1 MB SRAM read (64 bits)"] / 8, HEAD),
                 (r"one byte from DRAM", hi_d, NO)]
        lo, hi, width = -2.0, 3.0, 6.0
        x0 = -0.9
        bars, names, vals = VGroup(), VGroup(), VGroup()
        for k, (nm, v, c) in enumerate(specs):
            y = 2.15 - 0.6 * k
            w = width * (math.log10(v) - lo) / (hi - lo)
            b = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.85).move_to([x0 + w / 2,
                                                                                                         y, 0])
            if k == 4:
                wl = width * (math.log10(lo_d) - lo) / (hi - lo)
                b = VGroup(Rectangle(width=wl, height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.85)
                           .move_to([x0 + wl / 2, y, 0]),
                           Rectangle(width=w - wl, height=0.38, stroke_width=0, fill_color=c, fill_opacity=0.4)
                           .move_to([x0 + wl + (w - wl) / 2, y, 0]))
            bars.add(b)
            names.add(label(nm, font_size=19, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.15))
            txt = rf"{lo_d:.0f}--{hi_d:.0f} pJ" if k == 4 else rf"{v:g} pJ"
            vals.add(label(txt, font_size=19, color=c).next_to(b, RIGHT, buff=0.12))
        ticks = VGroup(Line([x0, -0.75, 0], [x0 + width, -0.75, 0], color=GREY_C, stroke_width=1.5))
        for p in range(-2, 4):
            x = x0 + width * (p - lo) / (hi - lo)
            ticks.add(Line([x, -0.8, 0], [x, -0.7, 0], color=GREY_C, stroke_width=1.5),
                      label(rf"$10^{{{p}}}$ pJ", font_size=16, color=GREY_B).move_to([x, -1.02, 0]))
        rows = VGroup(
            MathTex(r"\text{one byte from DRAM}", r"=", r"\frac{%g \text{ to } %g\ \text{pJ}}{8}" % (
                E["DRAM read (64 bits), low"], E["DRAM read (64 bits), high"]), r"\approx",
                    rf"{lo_d:.0f} \text{{ to }} {hi_d:.0f}\ \text{{pJ}}", font_size=32),
            MathTex(r"\frac{\text{one byte from DRAM}}{\text{one 8-bit add}}", r"\approx",
                    rf"\frac{{{lo_d:.0f} \text{{ to }} {hi_d:.0f}}}{{{E['int8 add']:g}}}", r"\approx",
                    rf"{commas(int(round(lo_d / E['int8 add'], -2)))} \text{{ to }} "
                    rf"{commas(int(round(hi_d / E['int8 add'], -2)))}", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ticks, DOWN, buff=0.45).set_x(0)
        rows[1][-1].set_color(NO)
        src = note(r"Horowitz, \ ISSCC 2014, \ 45 nm, \ approximate; \ per-byte figures are his 64-bit reads "
                   r"divided by 8", font_size=16).to_edge(DOWN, buff=0.15)
        ratio_lo, ratio_hi = round(lo_d / E["int8 add"], -3), round(hi_d / E["int8 add"], -3)
        with self.voiceover(
            "Chapter one began with Mark Horowitz's table. Put it in terms of a single byte. <bookmark mark='a'/> "
            "Adding two bytes costs three hundredths of a picojoule. Fetching one byte from a small memory beside "
            "the arithmetic costs about forty times that; from a megabyte of on-chip memory, four hundred times. "
            "<bookmark mark='b'/> And from DRAM, off the chip: a sixty-four-bit read costs thirteen hundred to "
            "twenty-six hundred picojoules, so one byte costs between about a hundred and sixty and three hundred "
            f"and twenty-five. <bookmark mark='c'/> That is the energy of {say_int(int(ratio_lo))} to "
            f"{say_int(int(ratio_hi))} eight-bit additions, spent to bring in one byte. For most programs, the "
            "arithmetic is a rounding error; the bill is for transport."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ticks), FadeIn(src))
            vo.wait_until("a")
            for k in range(4):
                self.play(FadeIn(names[k]), GrowFromEdge(bars[k], LEFT), FadeIn(vals[k]), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(names[4]), GrowFromEdge(bars[4], LEFT), FadeIn(vals[4]), run_time=1.2)
            self.play(Write(rows[0]))
            vo.wait_until("c")
            self.play(Write(rows[1]))
            self.play(Indicate(rows[1][-1], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def wires(self):
        head = label(r"Why distance costs energy", font_size=36).to_edge(UP, buff=0.3)
        chip = RoundedRectangle(width=5.6, height=3.2, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2)
        chip.move_to([-3.4, -0.6, 0])
        cl = label(r"the chip", font_size=18, color=GREY_B).next_to(chip, UP, buff=0.1).align_to(chip, LEFT)
        alu = module_box(r"ALU", YES, w=1.0, h=0.6, font=20).move_to(chip.get_center() + LEFT * 1.9)
        reg = module_box(r"registers", YES, w=1.3, h=0.5, font=17).move_to(chip.get_center() + LEFT * 1.9 + UP * 1.0)
        sram = module_box(r"SRAM", DATA, w=1.1, h=0.9, font=19).move_to(chip.get_center() + RIGHT * 1.9)
        dram = module_box(r"DRAM chip", NO, w=1.6, h=1.6, font=19).move_to([3.0, -0.6, 0])
        w_reg = Line(alu.get_top(), reg.get_bottom(), color=YES, stroke_width=3)
        w_sram = Line(alu.get_right(), sram.get_left(), color=DATA, stroke_width=3)
        pin = chip.get_right()
        w_dram = VMobject(color=NO, stroke_width=3).set_points_as_corners(
            [alu.get_bottom(), alu.get_bottom() + DOWN * 1.0, [pin[0], alu.get_bottom()[1] - 1.0, 0],
             [dram.get_left()[0], alu.get_bottom()[1] - 1.0, 0], dram.get_left() + DOWN * 0.6])
        wl = VGroup(label(r"$\mu$m", font_size=18, color=YES).next_to(w_reg, RIGHT, buff=0.08),
                    label(r"mm", font_size=18, color=DATA).next_to(w_sram, UP, buff=0.08),
                    label(r"cm: \ pins, \ package, \ board", font_size=18, color=NO).next_to(w_dram, DOWN, buff=0.1)
                    .shift(RIGHT * 1.2))
        rows = VGroup(
            MathTex(r"E_{\text{bit}}", r"\approx", r"\tfrac12", r"\,C\,", r"V^2", font_size=36),
            MathTex(r"C", r"\approx", r"c\,L", font_size=36),
            MathTex(r"E_{\text{bit}}", r"\approx", r"\tfrac12", r"\,c\,L\,", r"V^2", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
        rows[2][3].set_color(NO)
        whys = VGroup(label(r"charge a wire: \ Part 10's $\alpha C V^2 f$", font_size=17, color=GREY_B),
                      label(r"capacitance grows with length", font_size=17, color=GREY_B),
                      label(r"so energy grows with distance", font_size=17, color=NO))
        for w, r in zip(whys, rows):
            w.next_to(r, LEFT, buff=0.3)
        rowg = VGroup(rows, whys)
        rowg.to_edge(RIGHT, buff=0.4)
        foot = wrapped_label(r"and DRAM opens a whole row of cells \ (Part 5) \ to deliver a few of them", 12.4,
                             font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)

        def pulse(path, color, rt):
            d = Dot(path.get_start(), radius=0.08, color=color)
            return d, MoveAlongPath(d, path, run_time=rt)
        with self.voiceover(
            "Why should distance cost energy? <bookmark mark='a'/> Sending a bit along a wire means charging the "
            "wire, and Part 10 gave the energy: about a half of C V squared for each change. "
            "<bookmark mark='b'/> A wire's capacitance grows with its length. <bookmark mark='c'/> So the energy "
            "of a bit grows with the distance it travels. A register is micrometres from the arithmetic, an on-chip "
            "memory millimetres, and DRAM centimetres away, through the pins, the package and the board, wires with "
            "far more capacitance. <bookmark mark='d'/> And a DRAM chip must open a whole row of its cells, "
            "thousands of them, to deliver the few that were asked for."
        ) as vo:
            self.play(FadeIn(head), Create(chip), FadeIn(cl), FadeIn(alu), FadeIn(reg), FadeIn(sram), FadeIn(dram),
                      Create(w_reg), Create(w_sram), Create(w_dram))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(FadeIn(wl))
            for path, col, rt in ((w_reg, YES, 0.4), (w_sram, DATA, 0.8), (w_dram, NO, 1.8)):
                d, a = pulse(path, col, rt)
                self.play(a)
                self.remove(d)
            vo.wait_until("d")
            self.play(FadeIn(foot), Indicate(dram, color=NO))
        self.wait(0.4)
        self.clear_scene()

    def stacked(self):
        head = label(r"Near memory: \ stack it beside the processor", font_size=36).to_edge(UP, buff=0.3)
        # left: a DDR channel across a board; right: HBM on an interposer (side view, schematic)
        board = Rectangle(width=5.8, height=0.3, stroke_width=0, fill_color=GREY_D, fill_opacity=1)
        board.move_to([-3.55, -1.4, 0])
        cpu_l = Rectangle(width=1.6, height=0.9, stroke_color=YES, stroke_width=2, fill_color=YES,
                          fill_opacity=0.2).next_to(board, UP, buff=0).align_to(board, LEFT).shift(RIGHT * 0.3)
        dimm = Rectangle(width=0.3, height=2.6, stroke_color=NO, stroke_width=2, fill_color=NO,
                         fill_opacity=0.2).next_to(board, UP, buff=0).align_to(board, RIGHT).shift(LEFT * 0.6)
        y0 = board.get_top()[1]
        ddr_bus = VGroup(*[Line([cpu_l.get_right()[0], y0 + 0.12 + 0.16 * k, 0], [dimm.get_left()[0],
                                                                                 y0 + 0.12 + 0.16 * k, 0],
                                color=NO, stroke_width=2) for k in range(4)])
        ddr_l = VGroup(label(r"processor", font_size=18, color=YES).next_to(cpu_l, UP, buff=0.1),
                       label(r"DRAM module", font_size=18, color=NO).next_to(dimm, UP, buff=0.1),
                       label(r"a DDR channel: \ 64 data wires, \ centimetres", font_size=19, color=NO)
                       .next_to(board, DOWN, buff=0.25))
        sub = Rectangle(width=5.8, height=0.3, stroke_width=0, fill_color=GREY_D, fill_opacity=1).move_to(
            [3.45, -1.4, 0])
        inter = Rectangle(width=5.0, height=0.3, stroke_color=GREY_B, stroke_width=1.5, fill_color=GREY_C,
                          fill_opacity=0.4).next_to(sub, UP, buff=0)
        proc = Rectangle(width=2.0, height=0.9, stroke_color=YES, stroke_width=2, fill_color=YES,
                         fill_opacity=0.2).next_to(inter, UP, buff=0).align_to(inter, LEFT).shift(RIGHT * 0.3)
        stack = VGroup(Rectangle(width=1.7, height=0.3, stroke_color=KERN, stroke_width=1.5, fill_color=KERN,
                                 fill_opacity=0.3))
        for _ in range(4):
            stack.add(Rectangle(width=1.7, height=0.3, stroke_color=DATA, stroke_width=1.5, fill_color=DATA,
                                fill_opacity=0.3))
        stack.arrange(UP, buff=0.05).next_to(inter, UP, buff=0).align_to(inter, RIGHT).shift(LEFT * 0.4)
        tsv = VGroup(*[Line(stack.get_bottom() + RIGHT * x, stack.get_top() + RIGHT * x, color=GREY_A,
                            stroke_width=1.2) for x in (-0.6, -0.3, 0.0, 0.3, 0.6)])
        hbus = VGroup(*[Line([proc.get_right()[0], inter.get_y() + 0.1 - 0.0286 * k, 0],
                             [stack.get_left()[0], inter.get_y() + 0.1 - 0.0286 * k, 0], color=DATA,
                             stroke_width=1.2) for k in range(8)])
        hbm_l = VGroup(label(r"processor", font_size=18, color=YES).next_to(proc, UP, buff=0.1),
                       label(r"stacked DRAM dies, \\ joined by through-silicon vias", font_size=18, color=DATA)
                       .next_to(stack, UP, buff=0.1),
                       label(r"HBM, \ on a silicon interposer: \ 1{,}024 data wires per stack, \ millimetres",
                             font_size=19, color=DATA).next_to(sub, DOWN, buff=0.25))
        hbm_l[1].shift(LEFT * max(0, hbm_l[1].get_right()[0] - 6.7))
        tsv_l = VGroup()
        tops = VGroup(label(r"far and narrow", font_size=24, color=NO).move_to([-3.6, 1.8, 0]),
                      label(r"close and wide", font_size=24, color=DATA).move_to([3.4, 1.8, 0]))
        foot = wrapped_label(r"HBM: \ a JEDEC standard since 2013; \ the V100's 900 GB/s of chapter 6 and later "
                             r"TPUs' bandwidth come from it", 12.4, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        ill = note(r"schematic side views, \ not to scale", font_size=16).next_to(foot, UP, buff=0.2)

        def bits(lines, color, n):
            ds = VGroup(*[Dot(lines[k % len(lines)].get_start(), radius=0.04, color=color) for k in range(n)])
            return ds, [MoveAlongPath(d, lines[k % len(lines)]) for k, d in enumerate(ds)]
        with self.voiceover(
            "The first answer is to bring memory closer. <bookmark mark='a'/> A conventional DRAM module sits "
            "centimetres from the processor, across the board, on a channel sixty-four data wires wide. "
            "<bookmark mark='b'/> High Bandwidth Memory, standardized in 2013, stacks several DRAM dies on top of "
            "one another, joins them with vertical wires through the silicon, and sets the stack beside the "
            "processor on a slab of silicon, with one thousand and twenty-four data wires per stack, millimetres "
            "long. <bookmark mark='c'/> Shorter wires cost less energy per bit, and many more of them run at once. "
            "Chapter six's GPU gets its nine hundred gigabytes a second this way, and so do later TPUs. But the "
            "data still has to make the trip."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tops), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(board), FadeIn(cpu_l), FadeIn(dimm), Create(ddr_bus), FadeIn(ddr_l))
            ds, an = bits(ddr_bus, NO, 4)
            self.play(*an, run_time=1.2)
            self.remove(*ds)
            vo.wait_until("b")
            self.play(FadeIn(sub), FadeIn(inter), FadeIn(proc), LaggedStart(*[FadeIn(s, shift=DOWN * 0.1)
                                                                              for s in stack], lag_ratio=0.2),
                      run_time=1.5)
            self.play(Create(tsv), FadeIn(tsv_l), Create(hbus), FadeIn(hbm_l))
            vo.wait_until("c")
            for _ in range(2):
                ds, an = bits(ddr_bus, NO, 4)
                hs, hn = bits(hbus, DATA, 4)
                self.play(*an, *hn, run_time=0.5)
                self.remove(*ds, *hs)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def pim(self):
        head = label(r"In memory: \ move the work, \ not the data", font_size=36).to_edge(UP, buff=0.3)
        banks = VGroup(*[RoundedRectangle(width=0.95, height=0.6, corner_radius=0.06, stroke_color=DATA,
                                          stroke_width=1.8, fill_color=DATA, fill_opacity=0.12) for _ in range(BANKS)])
        banks.arrange_in_grid(4, 4, buff=0.15).move_to([-3.6, -0.5, 0])
        mem = SurroundingRectangle(banks, color=GREY_B, buff=0.2, corner_radius=0.1)
        ml = label(r"DRAM: \ 16 banks", font_size=19, color=GREY_A).next_to(mem, UP, buff=0.12)
        cpu = module_box(r"processor", YES, w=1.8, h=1.0, font=20).move_to([4.6, -0.5, 0])
        chan = Line(mem.get_right(), cpu.get_left(), color=GREY_B, stroke_width=3)
        chl = label(r"the channel", font_size=18, color=GREY_B).next_to(chan, UP, buff=0.1)
        units = VGroup(*[Square(0.2, stroke_color=HEAD, stroke_width=1.5, fill_color=HEAD, fill_opacity=0.5)
                         .move_to(b.get_corner(DR) + UL * 0.15) for b in banks])
        moved = N_ITEMS * ITEM_BYTES
        pim_bytes = BANKS * PARTIAL_BYTES
        counter_a = label(r"bytes over the channel: \ 0", font_size=21, color=NO)
        counter_a.next_to(chan, DOWN, buff=1.1).align_to([-0.8, 0, 0], LEFT)
        task = label(rf"sum $2^{{28}}$ four-byte numbers", font_size=21, color=WHITE).next_to(chan, UP, buff=0.9)
        final_a = label(rf"bytes over the channel: \ {commas(moved)}", font_size=21, color=NO).move_to(
            counter_a, aligned_edge=LEFT)
        final_b = label(rf"in memory: \ {pim_bytes} bytes \ (16 partial sums of 8 bytes)", font_size=21,
                        color=YES).next_to(final_a, DOWN, buff=0.3).align_to(counter_a, LEFT)
        ratio = moved // pim_bytes
        notes = VGroup(
            wrapped_label(r"the banks are still read; \ what is saved is the trip across the pins, \ the channel "
                          r"and the caches", 12.4, font_size=19, color=GREY_A),
            wrapped_label(r"UPMEM sells DRAM modules with a small processor beside each bank; \ Samsung announced "
                          r"HBM with arithmetic inside the stack in 2021", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.25)
        ill = note(r"illustrative workload", font_size=16).next_to(mem, DOWN, buff=0.12)

        def stream(n, color, src_list, rt):
            path_end = cpu.get_left()
            dots = VGroup(*[Square(0.1, stroke_width=0, fill_color=color, fill_opacity=1).move_to(s.get_center())
                            for s in src_list[:n]])
            anims = [Succession(Wait(0.03 * k), d.animate(run_time=rt).move_to(path_end)) for k, d in
                     enumerate(dots)]
            return dots, anims
        with self.voiceover(
            "The second answer is bolder: do the arithmetic where the data already is. <bookmark mark='a'/> Take a "
            "simple job, summing a quarter of a billion numbers, a gigabyte, spread over sixteen banks of DRAM. "
            "<bookmark mark='b'/> A processor must pull every byte across the channel, more than a billion of them. "
            "<bookmark mark='c'/> Put a small adder beside each bank instead. Each sums its own share, and only "
            "sixteen partial sums of eight bytes cross the channel, a hundred and twenty-eight bytes in all, "
            f"about {say_int(round(ratio / 1e6))} million times less. <bookmark mark='d'/> The banks are still "
            "read, so the saving is the trip, not the whole bill. This suits work with little reuse: scans, "
            "filters, sums, the left of the roofline. UPMEM sells such memory, and Samsung announced stacked "
            "memory with arithmetic inside in 2021."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mem), FadeIn(banks), FadeIn(ml), FadeIn(cpu), Create(chan), FadeIn(chl),
                      FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(task), FadeIn(counter_a))
            vo.wait_until("b")
            for rep in range(3):
                dots, anims = stream(16, NO, list(banks), 0.7)
                self.add(dots)
                self.play(*anims, run_time=1.2)
                self.remove(*dots)
            self.play(Transform(counter_a, final_a))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(u, scale=1.5) for u in units], lag_ratio=0.05), run_time=1)
            self.play(*[Indicate(u, color=HEAD) for u in units], run_time=0.8)
            dots, anims = stream(16, YES, list(units), 0.9)
            self.add(dots)
            self.play(*anims, run_time=1.4)
            self.remove(*dots)
            self.play(FadeIn(final_b))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def crossbar(self):
        head = label(r"In memory, \ in analog: \ a crossbar", font_size=36).to_edge(UP, buff=0.3)
        n = 4
        G = [[3, 1, 0, 2], [1, 2, 1, 0], [0, 1, 3, 1], [2, 0, 1, 2]]
        V = [1, 2, 0, 1]
        Ij = [sum(G[i][j] * V[i] for i in range(n)) for j in range(n)]
        gap = 0.9
        org = np.array([-4.2, 1.2, 0])
        rows_l = VGroup(*[Line(org + DOWN * gap * i + LEFT * 0.4, org + DOWN * gap * i + RIGHT * gap * (n - 0.4),
                               color=DATA, stroke_width=3) for i in range(n)])
        cols_l = VGroup(*[Line(org + RIGHT * gap * j + UP * 0.4, org + RIGHT * gap * j + DOWN * gap * (n - 0.4),
                               color=LAM, stroke_width=3) for j in range(n)])
        cells = VGroup()
        for i in range(n):
            for j in range(n):
                c = Circle(radius=0.17, color=HEAD, stroke_width=2, fill_color=HEAD,
                           fill_opacity=0.15 + 0.25 * G[i][j]).move_to(org + RIGHT * gap * j + DOWN * gap * i)
                cells.add(VGroup(c, label(f"{G[i][j]}", font_size=16, color=WHITE).move_to(c)))
        vlab = VGroup(*[label(rf"$V_{i + 1} = {V[i]}$", font_size=19, color=DATA).next_to(rows_l[i], LEFT, buff=0.15)
                        for i in range(n)])
        ilab = VGroup(*[label(rf"$I_{j + 1} = {Ij[j]}$", font_size=19, color=LAM).next_to(cols_l[j], DOWN, buff=0.15)
                        for j in range(n)])
        for k in range(1, n, 2):
            ilab[k].shift(DOWN * 0.35)
        gl = label(r"each cell: \ a conductance $G_{ij}$, \ the stored weight", font_size=18, color=HEAD).next_to(
            VGroup(rows_l, cols_l), UP, buff=0.25)
        eqs = VGroup(
            MathTex(r"I", r"=", r"G", r"\,", r"V", font_size=36),
            MathTex(r"I_j", r"=", r"\sum_i", r"G_{ij}", r"\,", r"V_i", font_size=36),
            MathTex(r"\mathbf{I}", r"=", r"G^{\mathsf T}", r"\,", r"\mathbf{V}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        eqs.next_to([0.4, 1.2, 0], RIGHT, buff=0)
        whys = VGroup(label(r"Ohm's law, \ one cell", font_size=18, color=GREY_B),
                      label(r"Kirchhoff: \ currents on a wire add", font_size=18, color=GREY_B),
                      label(r"a matrix-vector product, \ in one step", font_size=18, color=YES))
        for w, e in zip(whys, eqs):
            w.next_to(e, RIGHT, buff=0.35)
        cav = wrapped_label(r"the catch: \ analog values drift and are noisy, \ a few bits of precision; \ "
                            r"converters at the edges cost energy and area; \ research chips use phase-change "
                            r"or resistive memory", 6.2, font_size=19, color=NO)
        cav.next_to(eqs, DOWN, buff=0.6).align_to(eqs, LEFT)
        ill = note(r"illustrative values, \ arbitrary units", font_size=16).to_edge(DOWN, buff=0.2).shift(LEFT * 3.6)
        with self.voiceover(
            "The boldest answer stops moving the weights at all. <bookmark mark='a'/> Store each weight as the "
            "conductance of a cell where a row wire crosses a column wire. <bookmark mark='b'/> Put the inputs on "
            "the rows as voltages. By Ohm's law, each cell passes a current equal to its conductance times its "
            "voltage. <bookmark mark='c'/> And by Kirchhoff's law, the currents meeting on a column wire add up. "
            "<bookmark mark='d'/> So the column currents are a matrix-vector product, computed in one step, by "
            "physics, where the weights are stored. <bookmark mark='e'/> The catch is that this is analog. Values "
            "drift and are noisy, worth only a few bits, and the converters at the edges cost energy of their own. "
            "Research chips built from phase-change or resistive memory are still working on that."
        ) as vo:
            self.play(FadeIn(head), Create(rows_l), Create(cols_l), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=1.4) for c in cells], lag_ratio=0.05), FadeIn(gl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(vlab), Write(eqs[0]), FadeIn(whys[0]))
            pulses = VGroup(*[Dot(rows_l[i].get_start(), radius=0.07, color=DATA) for i in range(n) if V[i]])
            self.play(*[MoveAlongPath(p, rows_l[i]) for p, i in zip(pulses, [i for i in range(n) if V[i]])],
                      run_time=1.2)
            self.remove(*pulses)
            vo.wait_until("c")
            self.play(TransformMatchingTex(eqs[0].copy(), eqs[1]), FadeIn(whys[1]))
            down = VGroup(*[Dot(cols_l[j].get_start(), radius=0.07, color=LAM) for j in range(n)])
            self.play(*[MoveAlongPath(d, cols_l[j]) for j, d in enumerate(down)], run_time=1.2)
            self.remove(*down)
            self.play(FadeIn(ilab))
            vo.wait_until("d")
            self.play(TransformMatchingTex(eqs[1].copy(), eqs[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(cav))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, PART)
