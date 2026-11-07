from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.compute import load as load10
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, tag_box

TRENDS = [("transistors", r"transistors \ (thousands)", DATA), ("specint", r"single-thread performance", YES),
          ("frequency", r"clock \ (MHz)", NO)]


def tile(title, body, col, chapter, w=6.3, h=2.45):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=26, color=col)
    b = wrapped_label(body, w - 0.5, font_size=21, color=GREY_A)
    c = label(chapter, font_size=18, color=GREY_B)
    VGroup(t, b, c).arrange(DOWN, buff=0.18).move_to(frame)
    return VGroup(frame, t, b, c)


class Scaling(VoiceoverScene):
    def construct(self):
        self.card()
        self.trends()
        self.instruction()
        self.amortize()
        self.golden()
        self.amdahl()

    def card(self):
        card = chapter_card(1, r"The end of general-purpose scaling", r"Where did the free speedups go?",
                            lit=(1974, 2018), extra=((1974, r"Dennard scaling"),
                                                     (2018, r"Hennessy and Patterson: \ a new golden age")),
                            part=PART)
        with self.voiceover("Chapter one. The end of general-purpose scaling."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def trends(self):
        tr = load10("trends")
        head = label(r"Transistors kept coming; \ speed did not", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1970, 2022, 10], y_range=[0, 7.4, 1], x_length=10.4, y_length=4.3, tips=False,
                  axis_config={"color": GREY_C}).shift(DOWN * 0.45)
        xt = VGroup(*[label(str(y), font_size=16, color=GREY_B).next_to(ax.c2p(y, 0), DOWN, buff=0.12)
                      for y in range(1970, 2021, 10)])
        yt = VGroup(*[label(rf"$10^{{{k}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(1970, k), LEFT, buff=0.12)
                      for k in range(0, 8)])
        dots = {k: VGroup(*[Dot(ax.c2p(x, np.log10(max(y, 1))), radius=0.035, color=c, fill_opacity=0.85)
                            for x, y in tr["series"][k]]) for k, _, c in TRENDS}
        legend = VGroup(*[VGroup(Dot(radius=0.06, color=c), label(t, font_size=18, color=c)).arrange(RIGHT, buff=0.1)
                          for _, t, c in TRENDS]).arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.2)
        x05 = ax.c2p(2005, 0)[0]
        mark = DashedLine([x05, ax.c2p(0, 0)[1], 0], [x05, ax.c2p(0, 7.1)[1], 0], color=HEAD, stroke_width=2)
        g = tr["clock_growth"]
        rate = label(rf"clock: \ {100 * g['1985-2004']:+.0f}\% a year, \ 1985--2004; \ "
                     rf"{100 * g['2006-2021']:+.1f}\% a year, \ 2006--2021", font_size=20, color=NO)
        rate.move_to(ax.c2p(1990, 6.7))
        src = note(r"data: \ Karl Rupp's compilation \ (CC BY 4.0), \ as in Part 10; \ growth rates fitted there",
                   font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Part 10 opened with this picture: fifty years of microprocessors, on a logarithmic scale. "
            "<bookmark mark='a'/> The transistors kept coming, doubling about every two years. <bookmark mark='b'/> "
            "For three decades a single thread got faster with them, <bookmark mark='c'/> and so did the clock, by "
            "about a third every year. <bookmark mark='d'/> Then, around 2005, the voltage stopped falling, Dennard "
            "scaling ended, and the clock stopped: since then it has not grown at all. But there is a second way to spend transistors. Instead of "
            "more copies of a general machine, build a machine that does one kind of work, and does it with far less "
            "waste. To see where the waste is, we count energy."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(src))
            for mk, (k, _, _) in zip("abc", TRENDS):
                vo.wait_until(mk)
                self.play(FadeIn(legend[[s[0] for s in TRENDS].index(k)]),
                          LaggedStart(*[FadeIn(d) for d in dots[k]], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(mark), FadeIn(rate))
        self.wait(0.4)
        self.clear_scene()

    def instruction(self):
        E = {r["op"]: r["pj"] for r in load("energy")["horowitz"]["table"]}
        fetch, add = E["8 KB SRAM read (64 bits)"], E["int32 add"]
        head = label(r"The energy of an instruction, \ and of its operation", font_size=36).to_edge(UP, buff=0.3)
        names = [r"fetch", r"decode", r"read registers", r"execute", r"write back"]
        cols = [KERN, GREY_B, GREY_B, YES, GREY_B]
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=0.75, corner_radius=0.1, stroke_color=c,
                                                 stroke_width=2, fill_color=BG, fill_opacity=1),
                                label(n, font_size=20, color=c)) for n, c in zip(names, cols)])
        for b in boxes:
            b[1].move_to(b[0])
        boxes.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.55)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.03, stroke_width=2,
                                color=GREY_C, max_tip_length_to_length_ratio=0.35) for i in range(4)])
        costs = VGroup(
            label(rf"$\ge {fetch:g}$ pJ", font_size=20, color=KERN).next_to(boxes[0], DOWN, buff=0.15),
            label(r"more", font_size=18, color=GREY_B).next_to(boxes[1], DOWN, buff=0.15),
            label(r"more", font_size=18, color=GREY_B).next_to(boxes[2], DOWN, buff=0.15),
            label(rf"${add:g}$ pJ", font_size=20, color=YES).next_to(boxes[3], DOWN, buff=0.15),
            label(r"more", font_size=18, color=GREY_B).next_to(boxes[4], DOWN, buff=0.15),
        )
        cl = VGroup(wrapped_label(r"read 64 bits from an 8 KB SRAM, \ the size of a small instruction cache", 2.6,
                                  font_size=18, color=KERN).next_to(costs[0], DOWN, buff=0.12),
                    wrapped_label(r"a 32-bit integer add", 2.4, font_size=18, color=YES).next_to(costs[3], DOWN,
                                                                                               buff=0.12))
        rows = VGroup(
            MathTex(r"\text{useful share}", r"=", r"\frac{E_{\text{op}}}{E_{\text{fetch}} + E_{\text{decode}} + "
                    r"E_{\text{regs}} + E_{\text{op}}}", font_size=36),
            MathTex(r"\text{useful share}", r"\le", r"\frac{E_{\text{op}}}{E_{\text{fetch}} + E_{\text{op}}}",
                    font_size=36),
            MathTex(r"\text{useful share}", r"\le", rf"\frac{{{add:g}}}{{{fetch:g} + {add:g}}}", r"\approx",
                    rf"{100 * add / (fetch + add):.0f}\%", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(cl, DOWN, buff=0.45).set_x(0)
        rows[2][-1].set_color(NO)
        why = VGroup(label(r"drop every overhead but the fetch: \ the share can only grow", font_size=18, color=GREY_B),
                     label(r"Horowitz's figures", font_size=18, color=GREY_B))
        why[0].next_to(rows[1], RIGHT, buff=0.4)
        why[1].next_to(rows[2], RIGHT, buff=0.4)
        src = note(r"energies: \ Horowitz, \ ISSCC 2014, \ 45 nm, \ approximate", font_size=16).to_edge(DOWN,
                                                                                                    buff=0.2)
        with self.voiceover(
            "Every instruction a general-purpose processor runs goes through the stages of Part 7's pipeline. "
            "<bookmark mark='a'/> It is fetched from the instruction cache, decoded, its registers are read, "
            "it is executed, and its result is written back. <bookmark mark='b'/> Only one of those stages is the "
            "work we asked for. By Mark Horowitz's figures for a forty-five nanometre chip, a thirty-two-bit add "
            "costs a tenth of a picojoule, and just reading sixty-four bits from a small eight-kilobyte memory, the "
            "size of an instruction cache, costs ten. <bookmark mark='c'/> So write the useful share of the energy "
            "as the operation over the whole. <bookmark mark='d'/> Throw away every overhead except the fetch: "
            "the share can only grow. <bookmark mark='e'/> Put in the numbers: at most about one percent. "
            "Ninety-nine parts in a hundred go on organizing the work, not doing it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.25), Create(arrows), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(costs), FadeIn(cl), FadeIn(src))
            vo.wait_until("c")
            self.play(Write(rows[0]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(why[0]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(why[1]))
            self.play(Indicate(rows[2][-1], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def amortize(self):
        en = load("energy")
        E = {r["op"]: r["pj"] for r in en["horowitz"]["table"]}
        fetch, add, mac = E["8 KB SRAM read (64 bits)"], E["int32 add"], E["int8 multiply"] + E["int32 add"]
        macs = en["tpu"]["macs"]
        head = label(r"One instruction, \ many operations", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\text{useful share}", r"\le", r"\frac{E_{\text{op}}}{E_{\text{fetch}} + E_{\text{op}}}",
                    font_size=38),
            MathTex(r"\text{useful share}", r"\le", r"\frac{k\,E_{\text{op}}}{E_{\text{fetch}} + k\,E_{\text{op}}}",
                    r"\xrightarrow{\;k \to \infty\;}", r"1", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)

        def share(k, e):
            return k * e / (fetch + k * e)
        cases = [(r"1 add \ (a scalar processor)", 1, add, NO),
                 (r"16 adds \ (one 512-bit vector instruction)", 16, add, HEAD),
                 (rf"{macs:,} 8-bit multiply-adds \ (a $256 \times 256$ grid)".replace(",", "{,}"), macs, mac, YES)]
        bar_w = 5.6
        lines = VGroup()
        for name, k, e, col in cases:
            s = share(k, e)
            frame = Rectangle(width=bar_w, height=0.4, stroke_color=GREY_C, stroke_width=1.2)
            fill = Rectangle(width=max(bar_w * s, 0.03), height=0.4, stroke_width=0, fill_color=col, fill_opacity=0.85)
            fill.align_to(frame, LEFT)
            pct = rf"{100 * s:.1f}\%" if s > 0.99 else rf"{100 * s:.0f}\%"
            t = label(pct, font_size=21, color=col).next_to(frame, RIGHT, buff=0.15)
            n = label(rf"$k$ = {name}", font_size=19, color=GREY_A)
            lines.add(VGroup(n, VGroup(frame, fill, t)).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
        grid = VGroup(*[Square(0.16, stroke_width=0.8, stroke_color=YES, fill_color=YES, fill_opacity=0.35)
                        for _ in range(256)]).arrange_in_grid(16, 16, buff=0.04)
        instr = tag_box(r"one instruction", color=KERN, size=18)
        VGroup(instr, grid).arrange(DOWN, buff=0.35).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.3)
        arrow = Arrow(instr.get_bottom(), grid.get_top(), buff=0.05, color=KERN, stroke_width=2,
                      max_tip_length_to_length_ratio=0.3)
        gnote = note(r"schematic: \ 256 of the cells", font_size=16).next_to(grid, DOWN, buff=0.15)
        src = note(rf"overhead counted as one fetch \ ({fetch:g} pJ, \ a lower bound); \ add {add:g} pJ, \ 8-bit "
                   rf"multiply-add {mac:g} pJ \ (Horowitz 2014); \ $k$: \ illustrative", font_size=16).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "The way out is not to make the fetch cheaper. It is to make one instruction do more. "
            "<bookmark mark='a'/> If one fetch drives k operations, the overhead is shared k ways, and the useful "
            "share climbs towards one. <bookmark mark='b'/> With one add per instruction it is one percent. "
            "<bookmark mark='c'/> A vector instruction, Part 10's SIMD, does sixteen adds at once: about fourteen "
            "percent. <bookmark mark='d'/> Now imagine an instruction that starts sixty-five thousand five hundred "
            "and thirty-six eight-bit multiply-adds, on a grid of two hundred and fifty-six by two hundred and "
            "fifty-six cells. The overhead all but disappears. That grid is not imaginary: it is Google's TPU, and "
            "this part builds a small one. Moving the data costs energy too: that is the next chapter."
        ) as vo:
            self.play(FadeIn(head), Write(rows[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(instr), FadeIn(src))
            for mk, ln in zip("bcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln[0]), FadeIn(ln[1][0]), GrowFromEdge(ln[1][1], LEFT), FadeIn(ln[1][2]))
            self.play(GrowArrow(arrow), LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.004), FadeIn(gnote),
                      run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def golden(self):
        head = label(r"Hennessy and Patterson: \ a new golden age", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"parallelism the domain allows", r"a grid of cells working in lockstep, \ not threads that must "
                 r"coordinate", DATA, r"chapters 3 and 4"),
            tile(r"memories the program controls", r"buffers placed and filled on purpose, \ rather than caches "
                 r"that guess", KERN, r"chapters 5 and 8"),
            tile(r"less precision, \ when it is enough", r"8-bit integers where 32-bit floats were the habit",
                 HEAD, r"chapter 5"),
            tile(r"a domain-specific language", r"programs written so the parallelism is visible, \ such as "
                 r"TensorFlow's graphs", LAM, r"chapter 10, \ for hardware: \ Chisel"),
        ).arrange_in_grid(2, 2, buff=(0.35, 0.35)).next_to(head, DOWN, buff=0.4)
        src = note(r"Turing lecture, \ June 2018; \ \textit{Communications of the ACM}, \ February 2019", font_size=16)
        src.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "In June 2018 John Hennessy and David Patterson gave their Turing Award lecture, later published as A New "
            "Golden Age for Computer Architecture. Their argument was that with Dennard scaling gone and Moore's law "
            "slowing, the remaining road to large gains is domain-specific architecture, for four reasons."
            " <bookmark mark='a'/> First, it can use the kind of parallelism the domain really has: a grid "
            "of cells in lockstep, with nothing to coordinate. <bookmark mark='b'/> Second, it can manage its own "
            "memories, filling buffers on purpose instead of hoping a cache guesses right. <bookmark mark='c'/> "
            "Third, it can use no more precision than the work needs. <bookmark mark='d'/> And fourth, its programs "
            "come from domain-specific languages that make the parallelism plain. Each of these is a chapter of "
            "this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mk, t in zip("abcd", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()

    def amdahl(self):
        f, s = 0.9, 50
        head = label(r"The price: \ Amdahl again", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"T'", r"=", r"(1-f)\,T", r"+", r"\frac{f\,T}{s}", font_size=38),
            MathTex(r"\frac{T}{T'}", r"=", r"\frac{1}{(1-f) + f/s}", font_size=38),
            MathTex(r"\frac{T}{T'}", r"\xrightarrow{\;s \to \infty\;}", r"\frac{1}{1-f}", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.8).set_y(0.2)
        w = 6.0
        y0 = 1.0
        before = VGroup(Rectangle(width=w * (1 - f), height=0.5, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8),
                        Rectangle(width=w * f, height=0.5, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
                        ).arrange(RIGHT, buff=0).move_to([3.4, y0, 0])
        bl = VGroup(label(r"$1-f$", font_size=19, color=GREY_B).next_to(before[0], UP, buff=0.1),
                    label(r"$f$: \ the part an accelerator can take", font_size=19, color=DATA).next_to(before[1], UP,
                                                                                                  buff=0.1))
        after = VGroup(before[0].copy(), Rectangle(width=w * f / s, height=0.5, stroke_width=0, fill_color=YES,
                                                    fill_opacity=0.9)).arrange(RIGHT, buff=0)
        after.next_to(before, DOWN, buff=0.9).align_to(before, LEFT)
        al = label(rf"$s = {s}$: \ {1 / ((1 - f) + f / s):.1f} times faster", font_size=20, color=YES).next_to(
            after, RIGHT, buff=0.3)
        cap = label(rf"$f = {f}$: \ never more than {1 / (1 - f):.0f} times", font_size=24, color=NO)
        cap.next_to(after, DOWN, buff=0.8).align_to(before, LEFT)
        ill = note(r"$f$, \ $s$: \ illustrative", font_size=16).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Specialization has a price, and Part 10 already named it. <bookmark mark='a'/> An accelerator speeds up "
            "only the fraction of the work it was built for, say f, by some factor s; the rest runs as before. "
            "<bookmark mark='b'/> So the speedup is one over one minus f, plus f over s. <bookmark mark='c'/> If "
            "nine tenths of a program suits the accelerator and it is fifty times faster there, the whole runs about "
            "eight times faster. <bookmark mark='d'/> And no accelerator, however fast, gets past ten. A chip that "
            "does one thing pays only if that thing is most of the work. In 2013 Google projected that speech recognition by neural network alone could double "
            "the computing its data centres needed, and what a neural network does most is multiply matrices."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(before), FadeIn(bl))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("c")
            self.play(TransformFromCopy(before, after), run_time=1.2)
            self.play(FadeIn(al))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

