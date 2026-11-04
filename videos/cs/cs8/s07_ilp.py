from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt, load,
                                  mono)


class Ilp(VoiceoverScene):
    def construct(self):
        self.card()
        self.wall()
        self.curves()
        self.core()
        self.verdict()

    def card(self):
        card = chapter_card(6, r"Wider, \ and the ILP wall", r"How much parallelism is in a real program?",
                            lit=(1972, 1991), extra=((1972, r"Riseman and Foster"), (1991, r"Wall's limits of ILP")),
                            part=PART)
        with self.voiceover("Chapter six. Wider, and the wall."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wall(self):
        d = load("limits")
        head = label(r"A limit study: \ an oracle, \ handicapped one way at a time", font_size=32).to_edge(UP, buff=0.3)
        names = [r"the oracle", r"no renaming", r"memory: \\ wait for \\ every store", r"branches: \\ a real \\ "
                 r"predictor", r"branches: \\ no \\ speculation"]
        vals = [e["ipc"] for e in d["each"]]
        cols = [YES, CTRL, INF, NO, NO]
        lo, hi = -0.5, 3.5
        H = 4.2
        bars = VGroup()
        for k, (v, nm, c) in enumerate(zip(vals, names, cols)):
            h = H * (np.log10(v) - lo) / (hi - lo)
            b = Rectangle(width=1.3, height=h, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([k * 2.3, h / 2, 0], aligned_edge=ORIGIN)
            b.move_to([k * 2.3, h / 2, 0])
            t = label(f"{v:,.0f}" if v >= 10 else f"{v:.2f}", font_size=24, color=c).next_to(b, UP, buff=0.08)
            n = label(nm, font_size=18, color=GREY_A).next_to([k * 2.3, 0, 0], DOWN, buff=0.15)
            bars.add(VGroup(b, t, n))
        axis = VGroup()
        for e in (0, 1, 2, 3):
            y = H * (e - lo) / (hi - lo)
            axis.add(DashedLine([-1.0, y, 0], [4 * 2.3 + 0.8, y, 0], color=GREY_D, stroke_width=1, dash_length=0.08))
            axis.add(label(f"{10 ** e:,}", font_size=16, color=GREY_B).move_to([-1.4, y, 0]))
        fig = VGroup(axis, bars).move_to(DOWN * 0.35)
        yl = note(r"instructions per cycle \ (log scale), \ the Job's first chapter", font_size=20).next_to(
            fig, UP, buff=0.15).align_to(fig, LEFT)
        with self.voiceover(
            "In 1991 David Wall, at Digital's research lab, asked how much parallelism real programs contain. Earlier "
            "studies had found less than two instructions per cycle inside a basic block, but dozens, by Riseman and "
            "Foster's count in 1972, if a machine could see through every branch. Wall's method was the oracle we "
            "met in chapter two: record a program's run, schedule every instruction as early as its dependences "
            "allow, then take the oracle's powers away one at a time. We repeat it on the Job. <bookmark mark='a'/> "
            "With every power: two thousand four hundred instructions a cycle. <bookmark mark='b'/> Without "
            "renaming: three point seven. <bookmark mark='c'/> With renaming, but making every load wait until every "
            "earlier store's address is known: sixty-two. Memory ordering costs a lot, but not everything. <bookmark "
            "mark='d'/> And now keep renaming and perfect memory, but replace the oracle's knowledge of branches with "
            "Part 7's tournament predictor, so that each wrong guess blocks everything after it until it is resolved: "
            "three point four. <bookmark mark='e'/> With no guessing at all, stopping at every branch: under one half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(yl))
            for mk, b in zip("abcde", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[1]), FadeIn(b[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("limits")
        head = label(r"Width and window: \ the oracle with real branches", font_size=34).to_edge(UP, buff=0.3)
        ws = d["widths"]
        ax = Axes(x_range=[0, 6, 1], y_range=[0, 32, 8], x_length=8.0, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 1.3 + DOWN * 0.3)
        ax.y_axis.add_numbers([0, 8, 16, 24, 32], font_size=18, num_decimal_places=0)
        xt = VGroup(*[label(str(w), font_size=18, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k, w in enumerate(ws)])
        xl = note(r"width: \ instructions started per cycle", font_size=20).next_to(xt, DOWN, buff=0.1)
        yl = note(r"instructions per cycle", font_size=20).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)

        def curve(vals, color, width=4):
            return VMobject(color=color, stroke_width=width).set_points_as_corners(
                [ax.c2p(k, v) for k, v in enumerate(vals)])

        real = VGroup(*[curve(d["curves"][k], NO, 3) for k in ("32", "128", "512", "2048", "inf")])
        pb128 = curve(d["perfect_branches"]["128"], DATA)
        pb2048 = curve(d["perfect_branches"]["2048"], YES)
        lr = label(r"real branch prediction: \ any window, \ 32 to $\infty$", font_size=20, color=NO).next_to(
            ax.c2p(6, d["curves"]["inf"][-1]), UP, buff=0.15).shift(LEFT * 1.2)
        l128 = label(r"perfect branches, \ window 128", font_size=20, color=DATA).next_to(
            ax.c2p(6, d["perfect_branches"]["128"][-1]), UP, buff=0.1).shift(LEFT * 1.0)
        l2048 = label(r"perfect branches, \ window 2048", font_size=20, color=YES).next_to(
            ax.c2p(6, d["perfect_branches"]["2048"][-1]), LEFT, buff=0.15).shift(DOWN * 0.3)
        side = VGroup(
            label(r"the window: \ how far ahead \\ the machine may look", font_size=22, color=GREY_A),
            label(r"with real branches \\ it hardly matters", font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        with self.voiceover(
            "Now give the oracle real limits: a width, and a window, the number of instructions ahead of the oldest "
            "unfinished one that it may look at. A reorder buffer is exactly such a window. <bookmark mark='a'/> With "
            "the real predictor, here is instructions per cycle against width, for windows from thirty-two "
            "instructions to infinity. The curves lie on top of each other. They climb to about three point three at "
            "eight wide and stop. A bigger window is useless, because the machine never gets far ahead before a wrong "
            "guess knocks it back. <bookmark mark='b'/> Now make the branches perfect. With a window of one hundred "
            "twenty-eight, the curve keeps climbing, to eight. <bookmark mark='c'/> With a window of two thousand and "
            "forty-eight, to thirty. The parallelism is there; it is the branches that hide it."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xl), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in real], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(lr), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(pb128), FadeIn(l128), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(pb2048), FadeIn(l2048), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def core(self):
        d = load("sweep")
        head = label(r"Our core: \ width against reorder-buffer size", font_size=34).to_edge(UP, buff=0.3)
        runs = d["runs"]
        robs = [16, 32, 64, 128, 256, 512]
        widths = [1, 2, 4, 8]
        cw, chh = 1.3, 0.62
        grid = VGroup()
        for r, w in enumerate(widths):
            for c, rb in enumerate(robs):
                v = [x["ipc"] for x in runs if x["width"] == w and x["rob"] == rb][0]
                cell = Rectangle(width=cw * 0.95, height=chh * 0.9, stroke_width=0, fill_color=FUNC,
                                 fill_opacity=0.15 + 0.4 * v / 2.0)
                cell.move_to([c * cw, -r * chh, 0])
                grid.add(VGroup(cell, label(f"{v:.2f}", font_size=20, color=WHITE).move_to(cell)))
        rl = VGroup(*[label(rf"{w} wide", font_size=20, color=GREY_A).move_to([-1.1, -r * chh, 0])
                      for r, w in enumerate(widths)])
        cl = VGroup(*[label(str(rb), font_size=20, color=GREY_A).move_to([c * cw, 0.6, 0]) for c, rb in enumerate(robs)])
        ct = note(r"reorder-buffer entries", font_size=20).move_to([2.5 * cw, 1.05, 0])
        tab = VGroup(grid, rl, cl, ct).move_to(UP * 0.4)
        pp = d["perfect_512"]
        perf = label(rf"with perfect prediction \ (512 entries): \ {pp[0]:.2f}, \ {pp[1]:.2f}, \ {pp[2]:.2f}, \ "
                     rf"{pp[3]:.2f}", font_size=24, color=YES).next_to(tab, DOWN, buff=0.5)
        why = label(r"the rest of the gap: \ one taken branch fetched per cycle, \ two memory ports", font_size=22,
                    color=GREY_B).next_to(perf, DOWN, buff=0.2)
        with self.voiceover(
            "Our real core tells the same story. <bookmark mark='a'/> Each cell is the Job's instructions per cycle, "
            "for a width and a reorder-buffer size. Going from one to two to four wide helps a lot: zero point eight "
            "six, one point two four, one point eight nine. Eight wide adds almost nothing. <bookmark mark='b'/> And "
            "across each row, the buffer size changes nothing at all beyond thirty-two entries. Remember the hook: the "
            "buffer held about eleven instructions on average. <bookmark mark='c'/> With perfect prediction the same "
            "core reaches three point one six at four wide and three point five at eight. What stops it there is the "
            "front end and the memory ports: it fetches past at most one taken branch a cycle, and the scan loop "
            "takes a jump every six instructions."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rl), FadeIn(cl), FadeIn(ct))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.03), run_time=2.0)
            vo.wait_until("b")
            self.play(*[Indicate(grid[2 * 6 + c], color=HEAD, scale_factor=1.05) for c in range(6)])
            vo.wait_until("c")
            self.play(FadeIn(perf))
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def verdict(self):
        head = label(r"The ILP wall", font_size=40).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"the parallelism is real: \ thousands of instructions could overlap", font_size=26, color=YES),
            label(r"but a machine finds it only as far ahead as it can \textit{predict}", font_size=26, color=NO),
            label(r"and each extra instruction of width costs more wires, \ ports and power than the last",
                  font_size=26, color=COST),
            label(r"so cores stopped near 4 to 8 wide, \ and turned to many cores \ (Part 10)", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "This is the instruction-level parallelism wall. <bookmark mark='a'/> The parallelism is real: in the "
            "Job, thousands of instructions could run at once. <bookmark mark='b'/> But a machine can only exploit "
            "what lies within the stretch of program it can predict correctly, and with real branch prediction that "
            "stretch is short. <bookmark mark='c'/> Meanwhile each extra unit of width costs more than the last: "
            "every new instruction must compare its sources with every other instruction renamed in the same cycle, "
            "and every result must be broadcast to every waiting station. <bookmark mark='d'/> So, in the 2000s, "
            "designers stopped near four to eight wide and spent their transistors on more cores instead. That is "
            "Part 10. But first, the prediction itself: how a machine runs a hundred instructions ahead on a guess."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
