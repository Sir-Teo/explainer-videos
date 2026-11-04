from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load


class Dram(VoiceoverScene):
    def construct(self):
        self.card()
        self.cell()
        self.leak()
        self.rows()

    def card(self):
        card = chapter_card(11, r"Dynamic memory", r"How do you store a bit in one transistor?", lit=(1966, 1970),
                            part=PART)
        with self.voiceover("Chapter eleven. Dynamic memory."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cell(self):
        head = label(r"One transistor, \ one capacitor", font_size=38).to_edge(UP, buff=0.35)
        bl = Line([-3.0, 2.2, 0], [-3.0, -2.2, 0], color=DATA, stroke_width=3)
        wl = Line([-4.2, 1.2, 0], [0.6, 1.2, 0], color=HEAD, stroke_width=3)
        tr = Square(0.5, color=HEAD, stroke_width=2.5).move_to([-1.6, 0.4, 0])
        links = VGroup(Line([-3.0, 0.4, 0], tr.get_left(), color=WIRE, stroke_width=2.5),
                       Line(tr.get_top(), [-1.6, 1.2, 0], color=HEAD, stroke_width=2.5),
                       Line(tr.get_right(), [-0.4, 0.4, 0], color=WIRE, stroke_width=2.5),
                       Line([-0.4, 0.4, 0], [-0.4, -0.3, 0], color=WIRE, stroke_width=2.5))
        cap = VGroup(Line([-0.9, -0.3, 0], [0.1, -0.3, 0], color=YES, stroke_width=5),
                     Line([-0.9, -0.55, 0], [0.1, -0.55, 0], color=YES, stroke_width=5),
                     Line([-0.4, -0.55, 0], [-0.4, -1.1, 0], color=WIRE, stroke_width=2.5))
        gnd = VGroup(*[Line([-0.4 - w, -1.1 - 0.1 * k, 0], [-0.4 + w, -1.1 - 0.1 * k, 0], color=WIRE, stroke_width=2)
                       for k, w in enumerate((0.3, 0.2, 0.1))])
        labs = VGroup(MathTex(r"\text{bit line}", font_size=22, color=DATA).next_to(bl, DOWN, buff=0.1),
                      MathTex(r"\text{word line}", font_size=22, color=HEAD).next_to(wl, LEFT, buff=0.1),
                      MathTex(r"C_s", font_size=26, color=YES).next_to(cap, LEFT, buff=0.15).shift(DOWN * 0.1),
                      MathTex(r"C_b", font_size=26, color=DATA).next_to(bl, LEFT, buff=0.15).shift(DOWN * 1.2))
        charge = VGroup(*[MathTex("+", font_size=34, color=YES).move_to([-0.8 + 0.16 * k, -0.12, 0]) for k in range(7)])
        spread = [[-3.0 + (0.18 if k % 2 else -0.18), 1.7 - 0.6 * k, 0] for k in range(7)]
        formula = MathTex(r"\Delta V = \frac{V_{dd}}{2}\cdot\frac{C_s}{C_s + C_b}", r"\approx 0.6\,\text{V}\times"
                          r"\frac{10\ \text{fF}}{110\ \text{fF}}", r"\approx 55\ \text{mV}", font_size=32,
                          color=HEAD).to_edge(DOWN, buff=0.45).shift(RIGHT * 1.2)
        notes = VGroup(
            label(r"the bit is charge on a tiny capacitor \\ (about 10 femtofarads)", font_size=22, color=YES),
            label(r"reading connects it to the much larger bit line: \\ the voltage moves by a small fraction of a "
                  r"volt, \\ and the charge is gone", font_size=22, color=NO),
            label(r"so every read is destructive: \\ the sense amplifier writes the value back", font_size=22,
                  color=HEAD),
            label(r"Robert Dennard, \ IBM, \ 1966; \\ the Intel 1103, \ the first commercial DRAM, \ 1970", font_size=20,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 1.4 + UP * 0.4, aligned_edge=LEFT)
        with self.voiceover(
            "In 1966 Robert Dennard at IBM found a much smaller way to store a bit. <bookmark mark='a'/> One "
            "transistor, used as a switch, and one capacitor. The bit is the charge on the capacitor: charged is one, "
            "empty is zero. <bookmark mark='b'/> To read it, raise the word line and connect the capacitor to the bit "
            "line. But the bit line is far larger than the cell, so the charge spreads out and moves its voltage by "
            "only a small fraction of a volt. A sense amplifier detects that. <bookmark mark='c'/> And the cell's charge "
            "is now gone: reading destroys the value, so the sense amplifier writes it straight back. This is dynamic "
            "RAM. Intel's 1103, the first commercial DRAM chip, appeared in 1970 and quickly replaced the magnetic "
            "memories of chapter fourteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(bl), Create(wl), FadeIn(tr), Create(links), FadeIn(cap), FadeIn(gnd), FadeIn(labs),
                      FadeIn(notes[0]))
            self.play(LaggedStart(*[FadeIn(c, scale=1.5) for c in charge], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(wl.animate.set_stroke(width=6), tr.animate.set_fill(HEAD, 0.5))
            self.play(*[c.animate.move_to(p).set_opacity(0.7) for c, p in zip(charge, spread)], FadeIn(notes[1]),
                      run_time=1.6)
            self.play(Write(formula[0]))
            self.play(FadeIn(formula[1:]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(*[c.animate.move_to([-0.8 + 0.16 * k, -0.12, 0]).set_opacity(1) for k, c in enumerate(charge)],
                      run_time=1.2)
            self.play(wl.animate.set_stroke(width=3), tr.animate.set_fill(BG, 0), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def leak(self):
        d = load("dram")
        t = np.array(d["t"]) * 1000
        head = label(r"The charge leaks away", font_size=38).to_edge(UP, buff=0.35)
        ax = Axes(x_range=[0, 256, 64], y_range=[0, 1.05, 0.5], x_length=8.4, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18, "include_numbers": True}).move_to(LEFT * 1.6 + DOWN * 0.3)
        xl = note(r"milliseconds", font_size=20).next_to(ax, DOWN, buff=0.35)
        yl = note(r"charge \ (fraction of full)", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        thr = DashedLine(ax.c2p(0, d["threshold"]), ax.c2p(256, d["threshold"]), color=NO, stroke_width=2)
        tl = label(r"read as 0 below here", font_size=22, color=NO).next_to(ax.c2p(256, d["threshold"]), RIGHT, buff=0.1)
        no = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners([ax.c2p(a, b) for a, b in zip(t, d["v_no"])])
        ref = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(a, b) for a, b in zip(t, d["v_ref"])])
        nl = label(r"left alone", font_size=22, color=GREY_B).next_to(ax.c2p(200, float(np.exp(-0.2 / d['tau']))),
                                                                    DOWN, buff=0.1)
        rl = label(r"refreshed every 64 ms", font_size=24, color=YES).next_to(ax.c2p(150, 1.0), UP, buff=0.1)
        side = VGroup(label(r"refresh: \ read every row \\ and write it back", font_size=24, color=GREY_A),
                      label(r"a few percent of the memory's time \\ and power, \ forever", font_size=24,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.5)
        with self.voiceover(
            "There is a second problem. <bookmark mark='a'/> A capacitor that small is not perfectly isolated, and its "
            "charge leaks away, in a fraction of a second for the weakest cells. Left alone, a one would slowly turn "
            "into a zero. <bookmark mark='b'/> So the memory refreshes itself: the controller reads every row and "
            "writes it back, on a fixed schedule, the standard being every sixty-four milliseconds, and the charge is "
            "topped up long before it falls below the threshold. That is why it is called dynamic: the bits survive "
            "only because they are constantly rewritten, at a cost of a few percent of the memory's time and power."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), Create(thr), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(no), FadeIn(nl), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ref), FadeIn(rl), run_time=2.5)
            self.play(FadeIn(side))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rows(self):
        head = label(r"Dense, \ and slow", font_size=38).to_edge(UP, buff=0.35)
        # cell areas to scale: about 140 F^2 against 6 F^2
        side_s = 1.5
        sq_s = Square(side_s, stroke_color=YES, stroke_width=2.5, fill_color=YES, fill_opacity=0.25)
        sq_d = Square(side_s * np.sqrt(6 / 140), stroke_color=DATA, stroke_width=2.5, fill_color=DATA, fill_opacity=0.5)
        cells = VGroup(sq_s, sq_d).arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(LEFT * 4.5 + UP * 1.3)
        cl = VGroup(label(r"SRAM \\ 6 transistors, \ $\approx 140\,F^2$ \\ about 1 ns", font_size=22, color=YES)
                    .next_to(sq_s, DOWN, buff=0.2),
                    label(r"DRAM \\ 1T $+$ 1C, \ $6\,F^2$ \\ tens of ns", font_size=22, color=DATA)
                    .next_to(sq_d, DOWN, buff=0.2))
        cl[1].align_to(cl[0], UP)
        cap = note(r"cell areas to scale", font_size=20).next_to(cells, UP, buff=0.2)
        # a bank, its row buffer and its column multiplexer
        nr, nc = 8, 16
        bank = VGroup(*[Square(0.22, stroke_color=GREY_D, stroke_width=0.8, fill_color=DATA, fill_opacity=0.25)
                        for _ in range(nr * nc)]).arrange_in_grid(nr, nc, buff=0.04).move_to(RIGHT * 2.6 + UP * 1.35)
        buf = VGroup(*[Square(0.22, stroke_color=HEAD, stroke_width=0.8, fill_color=BG, fill_opacity=1)
                       for _ in range(nc)]).arrange(RIGHT, buff=0.04).next_to(bank, DOWN, buff=0.35)
        bufbox = SurroundingRectangle(buf, buff=0.06, color=HEAD, stroke_width=2)
        bl_ = label(r"row buffer \ (sense amplifiers)", font_size=20, color=HEAD).next_to(bufbox, LEFT, buff=0.15)
        bkl = label(r"one bank", font_size=20, color=DATA).next_to(bank, LEFT, buff=0.15)
        mux = Arrow(bufbox.get_bottom(), bufbox.get_bottom() + DOWN * 0.45, buff=0.02, color=YES, stroke_width=3)
        timing = VGroup(label(r"row hit: \ column read only, \ $t_{CL} \approx 14$ ns", font_size=22, color=YES),
                        label(r"row conflict: \ $t_{RP} + t_{RCD} + t_{CL} \approx 42$ ns \ (DDR4)", font_size=22,
                              color=NO)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cl, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        steps = VGroup(
            label(r"activate: \ open a whole row, \ thousands of bits, \ into the row buffer", font_size=24,
                  color=HEAD),
            label(r"read: \ take columns from the open row \ (fast while it stays open)", font_size=24, color=GREY_A),
            label(r"precharge: \ close the row, \ writing it back, \ before opening another", font_size=24,
                  color=GREY_A),
            label(r"so memory is fast for neighbouring addresses \ and slow for scattered ones: \ Part 9's caches "
                  r"exploit exactly this", font_size=23, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)

        def activate(r):
            src = VGroup(*bank[r * nc:(r + 1) * nc])
            copies = src.copy().set_fill(HEAD, 0.8)
            return src, copies

        with self.voiceover(
            "That trade, a cell twenty times smaller than static RAM's in exchange for complexity, is why main memory "
            "is DRAM. <bookmark mark='a'/> A static cell answers in about a nanosecond; DRAM takes tens. "
            "<bookmark mark='b'/> A DRAM access opens an entire row of thousands of bits into a row buffer of sense "
            "amplifiers, reads the columns it wants from that buffer, and later closes the row, writing it back. "
            "Reading more of an open row is quick; reaching a different row means closing and opening, which is slow. "
            "So a processor that reads memory in order runs fast, and one that jumps around waits. Real chips split "
            "their rows into independent banks, each with its own open row, and memory controllers reorder waiting "
            "requests so that as many as possible hit a row that is already open; a DDR module streams data in bursts "
            "of eight words per request for the same reason. Part 9 builds the cache hierarchy that hides as much of "
            "this as possible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), GrowFromCenter(sq_s), GrowFromCenter(sq_d))
            vo.wait_until("a")
            self.play(FadeIn(cl, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(bank, lag_ratio=0.002), FadeIn(bkl), Create(bufbox), FadeIn(buf), FadeIn(bl_))
            src, copies = activate(2)
            self.play(src.animate.set_fill(HEAD, 0.6), FadeIn(steps[0]))
            self.play(*[c.animate.move_to(b) for c, b in zip(copies, buf)], run_time=1.0)
            self.play(GrowArrow(mux), FadeIn(steps[1]))
            for col in (3, 4, 5):
                self.play(Indicate(copies[col], color=YES, scale_factor=1.4), run_time=0.45)
            self.play(FadeIn(timing[0]))
            self.play(*[c.animate.move_to(b) for c, b in zip(copies, src)], FadeIn(steps[2]), run_time=0.9)
            self.play(FadeOut(copies), src.animate.set_fill(DATA, 0.25), run_time=0.4)
            src2, copies2 = activate(6)
            self.play(src2.animate.set_fill(NO, 0.6), run_time=0.4)
            self.play(*[c.animate.move_to(b).set_fill(NO, 0.8) for c, b in zip(copies2, buf)], FadeIn(timing[1]),
                      run_time=1.0)
            self.play(FadeIn(steps[3]))
        self.wait(0.3)
        self.clear_scene()
