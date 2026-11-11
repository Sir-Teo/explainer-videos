from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, OooChart, bar_chart,
                                  fmt, load, phase_legend)


class Hook(VoiceoverScene):
    def construct(self):
        self.waiting()
        self.overtake()
        self.numbers()
        self.window()
        self.preview()
        self.plan()

    # ------------------------------------------------------------------
    def waiting(self):
        d = load("hook")["miss"]["in order"]
        head = label("One-entry issue queue: \\ a blocked head delays later dispatch", font_size=34).to_edge(
            UP, buff=0.3)
        ch = OooChart(d["timeline"], cw=0.098, ch=0.3, label_width=2.4, label_size=14, c0=0, heads_every=10)
        ch.move_to(DOWN * 0.35)
        leg = phase_legend(font_size=17).to_edge(DOWN, buff=0.25)
        lw = ch.rows[4]
        miss = label(r"a cache miss: \ 60 cycles", font_size=22, color=INF).next_to(ch.bars[4], UP, buff=0.04)
        total = label(rf"{d['cycles']} cycles", font_size=26, color=NO).next_to(ch, RIGHT, buff=0.2).shift(DOWN * 1.8)
        with self.voiceover(
            "Start with a short program on this part's functional core, constrained to a one-entry issue queue. "
            "That forces instructions to start in program order. Rows are instructions; time runs to the right. "
            "<bookmark mark='a'/> The fifth instruction loads from a cold cache line. We assign a sixty-cycle miss "
            "latency in this model. <bookmark mark='b'/> The next add needs that value and must wait. <bookmark "
            "mark='c'/> Several later instructions do not depend on the missing value. They still have their own "
            "dependencies and resource requirements, but this in-order configuration cannot pass the waiting add. "
            "Their useful work is delayed behind it. <bookmark mark='d'/> This recorded run takes eighty-one cycles "
            "for sixteen instructions, including setup and halt. It illustrates head-of-line blocking under the "
            "model's chosen resources and timing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.heads), LaggedStart(*[FadeIn(r) for r in ch.rows], lag_ratio=0.05))
            self.play(FadeIn(leg), LaggedStart(*[FadeIn(VGroup(ch.bars[i], ch.commits[i])) for i in range(4)],
                                               lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.bars[4], ch.commits[4])), Indicate(lw, color=INF), FadeIn(miss))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(ch.bars[5], ch.commits[5])))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(ch.bars[i], ch.commits[i])) for i in range(6, ch.n)],
                                  lag_ratio=0.15), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(total))
        self.wait(0.3)
        self.inorder = VGroup(ch, miss, total)
        self.play(FadeOut(head), FadeOut(leg), self.inorder.animate.scale(0.62).to_corner(UL, buff=0.3).shift(DOWN * 0.5))

    # ------------------------------------------------------------------
    def overtake(self):
        d = load("hook")["miss"]["out of order"]
        head = label("Out of order: \\ ready work competes for finite resources", font_size=32).to_edge(
            UP, buff=0.25)
        ch = OooChart(d["timeline"], cw=0.098, ch=0.3, label_width=2.4, label_size=14, c0=0, heads_every=10)
        ch.scale(0.62).to_corner(DR, buff=0.3).shift(UP * 0.2)
        total = label(rf"{d['cycles']} cycles", font_size=24, color=YES).next_to(ch, UP, buff=0.12).align_to(ch, RIGHT)
        keys = VGroup(
            label(r"the independent work runs \textit{during} the miss", font_size=24, color=FUNC),
            label("architectural results retire in program order", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.4)
        with self.voiceover(
            "Now use the normal issue queue and ready-instruction selection on the same functional core. <bookmark "
            "mark='a'/> An instruction can start when its operands, execution resources and ordering rules allow. "
            "The load still misses, and its dependent add still waits. Later independent work can overlap the miss, "
            "while dependencies among those later instructions remain. <bookmark mark='b'/> Completed results wait "
            "for in-order architectural retirement, shown in blue. When the load finishes, the waiting add executes "
            "and the core retires the completed work in order. <bookmark mark='c'/> This run takes seventy cycles "
            "instead of eighty-one. The comparison changes queue capacity and scheduling freedom; it does not make "
            "every later instruction immediately ready or reproduce every feature of a physical processor."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(ch.heads), LaggedStart(*[FadeIn(r) for r in ch.rows], lag_ratio=0.04))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in ch.bars], lag_ratio=0.08), run_time=2.0)
            self.play(FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in ch.commits], lag_ratio=0.08), FadeIn(keys[1]))
            vo.wait_until("c")
            self.play(FadeIn(total))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        h = load("hook")
        head = label(r"The Job's first chapter: \ 827,576 instructions", font_size=36).to_edge(UP, buff=0.35)
        vals = [h["pipeline"]["cycles"] / 1e3, h["in_order"]["cycles"] / 1e3, h["ooo"]["cycles"] / 1e3]
        names = [r"Part 7's pipeline", r"our core, \ in order", r"our core, \ out of order"]
        ch = bar_chart(vals, names, [GREY_B, NO, YES], height=3.6, bar_w=1.4, gap=1.4, font_size=22,
                       fmt_=lambda v: f"{v:.0f}K").move_to(DOWN * 0.2)
        cyc = note(r"thousands of cycles", font_size=20).next_to(ch, LEFT, buff=0.3).shift(UP * 1.2)
        ipc = VGroup(*[label(rf"IPC {x:.2f}", font_size=22, color=c).next_to(b, DOWN, buff=0.6)
                       for x, c, b in zip((h["pipeline"]["ipc"], h["in_order"]["ipc"], h["ooo"]["ipc"]),
                                          (GREY_B, NO, YES), ch.bars)])
        sp = h["in_order"]["cycles"] / h["ooo"]["cycles"]
        verdict = label(rf"issue queue 1 $\to$ 64: \ {sp:.2f} times fewer cycles; capacity and scheduling change", font_size=28,
                        color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Job's first chapter retires eight hundred twenty-seven thousand five hundred seventy-six "
            "instructions in each configuration. <bookmark mark='a'/> Part 7's functional pipeline used about a "
            "million cycles, or zero point eight three retired instructions per cycle. <bookmark mark='b'/> This "
            "part's core with a one-entry issue queue takes about one point zero six million cycles. Its front end "
            "and recovery rules differ from that pipeline. <bookmark mark='c'/> The normal sixty-four-entry queue "
            "permits ready work to pass blocked instructions. It finishes in four hundred thirty-seven thousand "
            "five hundred eighty cycles, about one point eight nine retired instructions per cycle. <bookmark "
            "mark='d'/> The program and execution-unit configuration are shared between these last two runs. Queue "
            "capacity and the resulting scheduling opportunities change together. These are model cycle counts; a "
            "silicon frequency and hardware speedup have not been measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cyc))
            for k, mk in enumerate("abc"):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.names[k]), FadeIn(ch.vals[k]), FadeIn(ipc[k]))
                if mk == "a":
                    vo.wait_until(mk)
            self.add(ch[0])
            vo.wait_until("d")
            self.play(FadeIn(verdict))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def window(self):
        h = load("hook")
        occ = h["occupancy"]
        head = label(r"Instructions in flight, \ cycle by cycle", font_size=36).to_edge(UP, buff=0.35)
        s = occ["sample"]
        ax = Axes(x_range=[0, len(s), 100], y_range=[0, 130, 32], x_length=11.0, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(DOWN * 0.3)
        ax.y_axis.add_numbers([0, 32, 64, 96, 128], font_size=18, num_decimal_places=0)
        line = VMobject(color=DATA, stroke_width=2).set_points_as_corners([ax.c2p(i, v) for i, v in enumerate(s)])
        cap = DashedLine(ax.c2p(0, 128), ax.c2p(len(s), 128), color=NO, stroke_width=2)
        capl = label(r"the reorder buffer holds 128", font_size=20, color=NO).next_to(cap, UP, buff=0.06).align_to(
            cap, RIGHT)
        xl = note(r"600 cycles of the Job", font_size=20).next_to(ax, DOWN, buff=0.15)
        stat = label(rf"whole-run mean: {occ['mean']:.1f} in flight; \ zero full-capacity cycles", font_size=28,
                     color=HEAD).to_edge(DOWN, buff=0.3)
        real = label("Golden Cove (2021): \\ 512 ROB entries; \\ operation units vary", font_size=24, color=GREY_A).next_to(stat, UP,
                                                                                                    buff=0.2)
        with self.voiceover(
            "The reorder buffer can hold a hundred twenty-eight in-flight instructions. <bookmark mark='a'/> This "
            "plot shows one six-hundred-cycle sample from the Job run. <bookmark mark='b'/> Occupancy rises and "
            "falls as instructions arrive, retire or are squashed. Separately, the histogram over the whole run "
            "gives a mean of ten point seven entries and no cycle at the full capacity. The plotted sample and "
            "whole-run statistics have different scopes. <bookmark mark='c'/> Real implementations can hold much "
            "more: Intel's 2021 Golden Cove disclosure gives a five-hundred-twelve-entry reorder buffer. Its "
            "entries count implementation operations, so they are not automatically equivalent to our model's "
            "architectural instructions. We will investigate why larger windows can help some workloads and why "
            "this particular run uses so little of its buffer."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(cap), FadeIn(capl))
            vo.wait_until("b")
            self.play(Create(line), run_time=3.0)
            self.play(FadeIn(stat))
            vo.wait_until("c")
            self.play(FadeIn(real))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def preview(self):
        head = label(r"By the end of this part", font_size=40).to_edge(UP, buff=0.4)
        facts = VGroup(
            label("dataflow limits under stated oracle assumptions", font_size=28, color=FUNC),
            label(r"Tomasulo's algorithm, \ renaming, \ and the reorder buffer, \ built and checked", font_size=28,
                  color=YES),
            label(r"speculation: \ running hundreds of instructions on a guess", font_size=28, color=CTRL),
            label("Spectre: \\ bounds-check bypass in a simulated cache/core", font_size=28, color=NO),
            label("the Job: \\ fitted corpus projection, \\ ledger row 2", font_size=28, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the route through this part. <bookmark mark='a'/> First, a dataflow model: how quickly a known "
            "execution trace can be scheduled under explicit latency and resource assumptions. <bookmark mark='b'/> "
            "Then historical scheduling mechanisms: the scoreboard, Tomasulo's algorithm, renaming and precise "
            "retirement, illustrated with functional models and finite emulator comparisons. <bookmark mark='c'/> "
            "Then branch speculation, which lets ready work run before earlier control decisions are resolved. "
            "<bookmark mark='d'/> A modeled Spectre bounds-check-bypass experiment will show how wrong-path loads "
            "can influence a simulated cache. It reads data in the model's shared memory, not host hardware "
            "secrets. <bookmark mark='e'/> Finally, measured model cycles on passages support the next fitted "
            "full-corpus projection in the Job ledger."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Out of Order", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"the dataflow graph, \ its critical path, \ and the limit it sets",
            r"true and false dependences; \ register renaming",
            r"the CDC 6600's scoreboard \ and Tomasulo's algorithm, \ cycle by cycle",
            r"the reorder buffer: \ out-of-order execution, \ precise exceptions",
            r"superscalar issue, \ the ILP wall, \ speculation, \ memory ordering",
            r"Spectre; \ VLIW; \ RISC and CISC; \ multithreading; \ the Job, \ ledger row 2",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 8 of Computer Science, Built, in Act Two, Making It Fast. <bookmark mark='a'/> We will "
            "connect a program's dataflow graph and weighted critical path to carefully scoped scheduling limits. "
            "We will separate true register dependencies from name hazards, then follow the scoreboard, Tomasulo's "
            "algorithm, renaming and the reorder buffer. We will distinguish execution from architectural "
            "retirement, and examine finite resources, prediction and memory ordering. The later chapters cover a "
            "simulated Spectre experiment, VLIW scheduling, RISC and CISC, an oracle multithreading study and the "
            "Job's projected corpus runtime."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
