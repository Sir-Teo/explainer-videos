from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, SystolicView, grid_table, load,
                                   module_box)


def int_matrix(M, color=WHITE, font_size=34, h_buff=1.0):
    m = IntegerMatrix(M, element_to_mobject_config={"color": color}, h_buff=h_buff, v_buff=0.65)
    m.scale(font_size / 48)
    return m


class Systolic(VoiceoverScene):
    def construct(self):
        self.card()
        self.product()
        self.cell()
        self.timing()
        self.wave()
        self.verify()

    def card(self):
        card = chapter_card(3, r"A systolic array", r"Can a grid of simple cells multiply matrices with no program?",
                            lit=(1978, 1982), extra=((1978, r"Kung and Leiserson: \ systolic arrays"),
                                                     (1982, r"Kung: \ why systolic architectures?")), part=PART)
        with self.voiceover("Chapter three. A systolic array."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def product(self):
        w = load("wave")["os"]
        A, B, C, n = w["A"], w["B"], w["C"], w["n"]
        head = label(r"One entry of a matrix product", font_size=36).to_edge(UP, buff=0.3)
        ma, mb, mc = int_matrix(A, DATA), int_matrix(B, LAM), int_matrix(C, WHITE, h_buff=1.45)
        eq = VGroup(ma, MathTex(r"\times", font_size=36), mb, MathTex(r"=", font_size=36), mc).arrange(
            RIGHT, buff=0.3).next_to(head, DOWN, buff=0.4)
        names = VGroup(label(r"$A$", font_size=24, color=DATA).next_to(ma, DOWN, buff=0.1),
                       label(r"$B$", font_size=24, color=LAM).next_to(mb, DOWN, buff=0.1),
                       label(r"$C$", font_size=24).next_to(mc, DOWN, buff=0.1))
        rowbox = SurroundingRectangle(VGroup(*ma.get_rows()[0]), color=HEAD, buff=0.08)
        colbox = SurroundingRectangle(VGroup(*mb.get_columns()[0]), color=HEAD, buff=0.08)
        cbox = SurroundingRectangle(mc.get_entries()[0], color=HEAD, buff=0.08)
        terms = [f"{A[0][k]} \\cdot {B[k][0]}" for k in range(n)]
        prods = [f"{A[0][k] * B[k][0]}" for k in range(n)]
        rows = VGroup(
            MathTex(r"C_{ij}", r"=", r"\sum_{k} A_{ik}\, B_{kj}", font_size=36),
            MathTex(r"C_{00}", r"=", " + ".join(terms), font_size=36),
            MathTex(r"C_{00}", r"=", " + ".join(prods), r"=", f"{C[0][0]}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(names, DOWN, buff=0.4)
        rows.set_x(0)
        rows[2][-1].set_color(HEAD)
        count = label(rf"{n} multiply-adds per entry, \ {n * n} entries: \ $N^3$ = {n ** 3} in all", font_size=23,
                      color=GREY_A).next_to(rows, DOWN, buff=0.35)
        with self.voiceover(
            "Start with what we want to compute. <bookmark mark='a'/> Two four by four matrices, A and B, "
            "and their product C. <bookmark mark='b'/> Each entry of C is a row "
            "of A times a column of B: <bookmark mark='c'/> multiply the pairs, <bookmark mark='d'/> and add them "
            f"up. {', plus '.join(say_gates(int(p)) for p in prods)}: {say_gates(C[0][0])}. "
            "<bookmark mark='e'/> That is four multiply-adds for each entry, and sixteen entries: N cubed, "
            "sixty-four in all. In 1978 H. T. Kung and Charles Leiserson proposed giving every entry its own cell, "
            "and having the numbers flow past it rhythmically, like blood pumped by a heart. They called it a "
            "systolic array, after the heartbeat."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(names))
            vo.wait_until("b")
            self.play(Create(rowbox), Create(colbox), Create(cbox), Write(rows[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(count))
        self.wait(0.4)
        self.clear_scene()

    def cell(self):
        c = load("cells")
        tr, ar = c["kinds"]["tree"], c["kinds"]["array"]
        head = label(r"One cell: \ a multiplier, \ an adder, \ a register", font_size=36).to_edge(UP, buff=0.3)
        frame = RoundedRectangle(width=4.6, height=4.4, corner_radius=0.2, stroke_color=GREY_B, stroke_width=2)
        frame.move_to([-4.1, -0.55, 0])
        cx, cy = frame.get_center()[:2]
        mul = module_box(rf"$\times$ \ ({c['width']}-bit)", HEAD, w=1.5, h=0.8, font=20).move_to([cx - 1.1, cy + 0.6, 0])
        add = module_box(rf"$+$ \ ({c['acc_width']}-bit)", YES, w=1.5, h=0.8, font=20).move_to([cx + 0.9, cy + 0.6, 0])
        reg = module_box(r"$s$ \ (sum)", KERN, w=1.5, h=0.6, font=20).move_to([cx + 0.9, cy - 1.0, 0])
        ra = module_box(r"$a$", DATA, w=0.7, h=0.5, font=20).move_to([cx + 1.6, cy + 1.75, 0])
        rb = module_box(r"$b$", LAM, w=0.7, h=0.5, font=20).move_to([cx - 1.1, cy - 1.75, 0])
        a_in = frame.get_left()[0] - 0.45
        wires = VGroup(
            Arrow([a_in, cy + 0.6, 0], mul.get_left(), buff=0, color=DATA, stroke_width=3),
            Line([cx - 2.05, cy + 0.6, 0], [cx - 2.05, cy + 1.75, 0], color=DATA, stroke_width=3),
            Arrow([cx - 2.05, cy + 1.75, 0], ra.get_left(), buff=0, color=DATA, stroke_width=3),
            Arrow(ra.get_right(), [frame.get_right()[0] + 0.55, cy + 1.75, 0], buff=0, color=DATA, stroke_width=3),
            Arrow([cx - 1.1, frame.get_top()[1] + 0.6, 0], mul.get_top(), buff=0, color=LAM, stroke_width=3),
            Arrow(mul.get_bottom(), rb.get_top(), buff=0, color=LAM, stroke_width=3),
            Arrow(rb.get_bottom(), [cx - 1.1, frame.get_bottom()[1] - 0.5, 0], buff=0, color=LAM, stroke_width=3),
            Arrow(mul.get_right(), add.get_left(), buff=0, color=HEAD, stroke_width=3),
            Arrow(add.get_bottom(), reg.get_top(), buff=0, color=YES, stroke_width=3),
            VMobject(color=KERN, stroke_width=3).set_points_as_corners(
                [reg.get_right(), [cx + 1.95, cy - 1.0, 0], [cx + 1.95, cy + 0.6, 0], add.get_right()]),
        )
        tags = VGroup(label(r"$a$ in", font_size=18, color=DATA).next_to(wires[0], UP, buff=0.08),
                      label(r"$b$ in", font_size=18, color=LAM).next_to(wires[4], LEFT, buff=0.08),
                      label(r"to the right", font_size=18, color=DATA).next_to(wires[3], DOWN, buff=0.08),
                      label(r"down", font_size=18, color=LAM).next_to(wires[6], RIGHT, buff=0.08))
        rows = [[r"multiplier", r"Dadda tree", r"array"], [r"adder", r"Kogge--Stone", r"ripple-carry"],
                [r"gates", f"{tr['gates']}", f"{ar['gates']}"],
                [r"as NAND gates", f"{tr['nand_gates']:,}".replace(",", "{,}"),
                 f"{ar['nand_gates']:,}".replace(",", "{,}")],
                [r"depth \ (gate delays)", f"{tr['depth']}", f"{ar['depth']}"]]
        tab = grid_table([r"", r"tree", r"array"], rows, widths=[2.4, 2.3, 2.1], row_h=0.5, font_size=21,
                         mono_cols=(), colors=[[GREY_A, YES, LAM]] * 5)
        tab.move_to([3.3, 1.0, 0])
        ok = c["check"]["correct"]
        facts = VGroup(
            label(rf"{c['flip_flops']['output_stationary']} flip-flops: \ $a$, \ $b$ \ ({c['width']} bits each), \ "
                  rf"$s$ \ ({c['acc_width']})", font_size=19, color=KERN),
            label(rf"both checked against $s + ab$ on {c['check']['samples']:,} random inputs".replace(",", "{,}"),
                  font_size=19, color=YES if all(ok.values()) else NO),
            label(r"the tree: \ more gates, \ half the depth: \ a faster clock", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tab, DOWN, buff=0.45).align_to(tab, LEFT)
        with self.voiceover(
            "Here is one cell. <bookmark mark='a'/> A multiplier from Part 4 takes "
            "an eight-bit number a arriving from the left and an eight-bit number b arriving from above. An adder "
            "adds the product to the cell's running sum, a twenty-four-bit register from Part 5."
            " Two more registers hold a and b for one clock tick and pass them on, a to the right and "
            "b downwards. <bookmark mark='b'/> With Dadda's tree "
            f"multiplier and the Kogge-Stone adder, the cell has {say_gates(tr['gates'])} gates and a depth of "
            f"{say_gates(tr['depth'])}. With the plain array multiplier and a ripple-carry adder it is smaller, "
            f"{say_gates(ar['gates'])} gates, but its depth is {say_gates(ar['depth'])}. <bookmark mark='c'/> Depth "
            "sets the clock, as Part 7 showed, so we use the tree. Both were checked gate by gate on four "
            "thousand and ninety-six random inputs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(frame), FadeIn(mul), FadeIn(add), FadeIn(reg), FadeIn(ra), FadeIn(rb))
            self.play(LaggedStart(*[Create(x) for x in wires], lag_ratio=0.15), FadeIn(tags), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def timing(self):
        n = load("wave")["os"]["n"]
        head = label(r"When do the numbers meet?", font_size=36).to_edge(UP, buff=0.3)
        cols = [DATA, LAM, YES, HEAD, KERN, NO, GREY_B]
        sq = VGroup(*[Square(0.72, stroke_color=GREY_B, stroke_width=1.5, fill_color=cols[(i + j) % 7],
                             fill_opacity=0.3) for i in range(n) for j in range(n)]).arrange_in_grid(n, n, buff=0.08)
        nums = VGroup(*[label(rf"{i + j}", font_size=22).move_to(sq[i * n + j]) for i in range(n) for j in range(n)])
        grid = VGroup(sq, nums).to_edge(LEFT, buff=0.5).set_y(-0.4)
        gl = label(r"$i + j$ \ in cell $(i, j)$", font_size=20, color=GREY_A).next_to(grid, UP, buff=0.2)
        rows = VGroup(
            MathTex(r"A_{ik}:", r"\ \text{enters row } i \text{ at cycle } i + k,", r"\ \text{reaches column } j "
                    r"\text{ at }", r"i + j + k", font_size=32),
            MathTex(r"B_{kj}:", r"\ \text{enters column } j \text{ at cycle } j + k,", r"\ \text{reaches row } i "
                    r"\text{ at }", r"i + j + k", font_size=32),
            MathTex(r"\text{last product:}\ ", r"i = j = k = N - 1", r"\ \Rightarrow\ ", r"t = 3N - 3", font_size=32),
            MathTex(r"\text{cycles}", r"=", r"3N - 2", r"=", rf"{3 * n - 2}", r"\quad (N = {n})".replace(
                "{n}", str(n)), font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        room = 6.7 - grid.get_right()[0] - 0.5
        if rows.width > room:
            rows.width = room
        rows.next_to(grid, RIGHT, buff=0.5).shift(UP * 0.2)
        rows[0][0].set_color(DATA)
        rows[1][0].set_color(LAM)
        for r in rows[:2]:
            r[-1].set_color(HEAD)
        rows[3][-2].set_color(YES)
        why = label(r"the work at cycle $t$ lies on the cells with $i + j \le t$: \ a diagonal wavefront", font_size=20,
                    color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The trick is in the timing. <bookmark mark='a'/> Row i of A enters the grid's left edge i cycles late, "
            "so the number A i k enters at cycle i plus k, and after j more cycles it reaches column j. "
            "<bookmark mark='b'/> Column j of B enters the top j cycles late, so B k j enters at j plus k, and "
            "reaches row i at i plus j plus k. <bookmark mark='c'/> The same cycle: the two numbers "
            "that must be multiplied always meet, in the right cell, at the right moment. <bookmark mark='d'/> The last product has all three indices at N minus one, at cycle "
            "three N minus three, so a product takes three N minus two cycles: ten for our four by four grid. "
            "<bookmark mark='e'/> And since a cell starts work at cycle i plus j, the busy cells form diagonals that "
            "sweep from the top left corner to the bottom right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sq), FadeIn(gl))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(rows[0][-1], color=HEAD), Indicate(rows[1][-1], color=HEAD))
            vo.wait_until("d")
            self.play(Write(rows[2]))
            self.play(Write(rows[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(x) for x in nums], lag_ratio=0.08), FadeIn(why), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def wave(self):
        w = load("wave")["os"]
        A, B = w["A"], w["B"]
        head = label(r"The wave, \ cycle by cycle", font_size=36).to_edge(UP, buff=0.3)
        view = SystolicView(w, size=0.86, gap=0.14, font_size=22)
        view.shift(RIGHT * 2.3 + DOWN * 0.75 - view.boxes.get_center())
        clock = label(r"cycle 0", font_size=28, color=HEAD).to_corner(UL, buff=0.5).shift(DOWN * 0.8)
        corner = SurroundingRectangle(view.box(0, 0), color=YES, buff=0.04, stroke_width=3)
        sums = [w["trace"][t]["acc"][0][0] for t in range(w["n"])]
        track = VGroup(*[label(rf"{s}", font_size=22, color=YES) for s in sums]).arrange(RIGHT, buff=0.3)
        tl = label(r"cell $(0, 0)$: ", font_size=22, color=YES)
        VGroup(tl, track).arrange(RIGHT, buff=0.2).next_to(clock, DOWN, buff=0.4, aligned_edge=LEFT)
        ok = label(rf"after {w['cycles']} cycles the grid holds $C$; \ "
                   + (r"it matches the integer product" if w["correct"] else r"it does not match"), font_size=22,
                   color=YES if w["correct"] else NO).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now watch it run, one clock tick at a time. Each cell shows its running sum, with the blue number from "
            "A and the purple number from B that it is multiplying. <bookmark mark='a'/> In the first cycle only the "
            f"corner cell has a pair: {say_gates(A[0][0])} times {say_gates(B[0][0])}. In the second, its two "
            f"neighbours start, and the corner adds {say_gates(A[0][1])} times {say_gates(B[1][0])}. Watch the "
            f"corner: <bookmark mark='b'/> {', '.join(say_gates(x) for x in sums)}, and it is finished, while the far "
            "corner has not yet begun. The wave of work crosses the grid diagonally, the lit cells always on one anti-diagonal band. "
            "<bookmark mark='c'/> Each number is fetched from outside the grid once, and then used four times, by "
            "four cells in turn. That reuse is the arithmetic intensity of chapter two, built into wires."
        ) as vo:
            self.play(FadeIn(head), FadeIn(view.boxes), FadeIn(view.acc), FadeIn(view.qa), FadeIn(view.qb),
                      FadeIn(clock))
            self.play(Create(corner), FadeIn(tl))
            vo.wait_until("a")
            for t in range(w["cycles"]):
                new_clock = label(rf"cycle {t + 1}", font_size=28, color=HEAD).move_to(clock, aligned_edge=LEFT)
                extra = [FadeIn(track[t])] if t < w["n"] else []
                self.play(*view.step(t), Transform(clock, new_clock), *extra, run_time=1.6 if t < 4 else 1.1)
                if t == 1:
                    vo.wait_until("b")
            vo.wait_until("c")
            self.play(FadeIn(ok))
        self.wait(0.4)
        self.clear_scene()

    def verify(self):
        rows_ = [r for r in load("gates")["rows"] if r["dataflow"] == "output-stationary"]
        cell = load("cells")["kinds"]["tree"]["gates"]
        head = label(r"Simulated gate by gate, \ and checked", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"{r['n']} $\times$ {r['n']}", f"{r['cycles']}", f"{3 * r['n'] - 2}", f"{r['macs']}",
                 f"{r['gates']:,}".replace(",", "{,}"), f"{r['flip_flops']:,}".replace(",", "{,}"), f"{r['trials']}",
                 r"yes" if r["correct"] else r"no"] for r in rows_]
        cols = [[WHITE, WHITE, GREY_A, WHITE, WHITE, WHITE, WHITE, YES if r["correct"] else NO] for r in rows_]
        tab = grid_table([r"grid", r"cycles", r"$3N-2$", r"multiply-adds", r"gates", r"flip-flops",
                          r"random products", r"all exact"], rows, widths=[1.4, 1.2, 1.2, 1.9, 1.5, 1.5, 2.3, 1.4],
                         row_h=0.62, font_size=23, colors=cols, mono_cols=())
        tab.next_to(head, DOWN, buff=0.8).set_x(0)
        per = all(r["gates"] == r["n"] ** 2 * cell for r in rows_)
        notes = VGroup(
            label(rf"gates $= N^2 \times {cell}$: \ the cells are all there is" if per else
                  r"gates: \ the cells plus wiring", font_size=23, color=HEAD),
            label(r"operands 8 bits, \ sums 24 bits: \ products compared with NumPy's exact integers", font_size=23,
                  color=GREY_A),
            label(r"a $256 \times 256$ grid, \ as in the TPU, \ would have 65{,}536 cells", font_size=23,
                  color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(tab, DOWN, buff=0.8).set_x(0)
        big = rows_[-1]
        with self.voiceover(
            "Now the evidence. <bookmark mark='a'/> We built grids of two, "
            "four and eight cells a side out of Part 4's gates and Part 5's registers, fed each sixteen random pairs "
            "of eight-bit matrices, and clocked the simulator cycle by cycle. <bookmark mark='b'/> Each finished in "
            "exactly three N minus two cycles, and every one of the products matched NumPy's exact integer answer. "
            f"<bookmark mark='c'/> The eight by eight grid has {say_gates(big['gates'])} gates, and that is exactly "
            "sixty-four cells' worth: there is nothing else, no control, no program counter. "
            "<bookmark mark='d'/> The TPU's grid has two hundred and fifty-six cells a side, sixty-five thousand five "
            "hundred and thirty-six of them. But first, a choice this design made without telling us: it keeps the "
            "outputs still and moves both inputs. That is not the only way."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in tab.cells[0]], FadeIn(tab.rule))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[i])) for i in range(1, len(rows) + 1)], lag_ratio=0.4),
                      run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


def say_gates(n: int) -> str:
    """A gate count as a speaker says it."""
    ones = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
           "seventeen eighteen nineteen".split()
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()

    def w(k):
        if k < 20:
            return ones[k]
        if k < 100:
            return tens[k // 10] + ("" if k % 10 == 0 else "-" + ones[k % 10])
        if k < 1000:
            r = k % 100
            return ones[k // 100] + " hundred" + ("" if r == 0 else " and " + w(r))
        r = k % 1000
        return w(k // 1000) + " thousand" + ("" if r == 0 else (" and " if r < 100 else " ") + w(r))
    return w(n)


_ = (BG,)
