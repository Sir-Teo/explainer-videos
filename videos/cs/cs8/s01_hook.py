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
        head = label(r"In order: \ when one instruction waits, \ everything behind it waits", font_size=34).to_edge(
            UP, buff=0.3)
        ch = OooChart(d["timeline"], cw=0.098, ch=0.3, label_width=2.4, label_size=14, c0=0, heads_every=10)
        ch.move_to(DOWN * 0.35)
        leg = phase_legend(font_size=17).to_edge(DOWN, buff=0.25)
        lw = ch.rows[4]
        miss = label(r"a cache miss: \ 60 cycles", font_size=22, color=INF).next_to(ch.bars[4], UP, buff=0.04)
        total = label(rf"{d['cycles']} cycles", font_size=26, color=NO).next_to(ch, RIGHT, buff=0.2).shift(DOWN * 1.8)
        with self.voiceover(
            "Here is a short piece of code on a machine that, like Part 7's pipeline, starts its instructions in "
            "program order. Each row is an instruction; time runs to the right, one column a cycle. <bookmark mark='a'/> "
            "The fifth instruction is a load, and its data is not in the cache: memory takes sixty cycles to answer. "
            "<bookmark mark='b'/> The add after it needs the loaded value, so it waits. That is unavoidable. "
            "<bookmark mark='c'/> But look at everything after the add. None of it uses the load. These instructions "
            "could have run at once, yet an in-order machine cannot start them until the add has started, so they all "
            "sit out the miss. <bookmark mark='d'/> Eighty-one cycles, for sixteen instructions."
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
        head = label(r"Out of order: \ start each instruction when its operands are ready", font_size=32).to_edge(
            UP, buff=0.25)
        ch = OooChart(d["timeline"], cw=0.098, ch=0.3, label_width=2.4, label_size=14, c0=0, heads_every=10)
        ch.scale(0.62).to_corner(DR, buff=0.3).shift(UP * 0.2)
        total = label(rf"{d['cycles']} cycles", font_size=24, color=YES).next_to(ch, UP, buff=0.12).align_to(ch, RIGHT)
        keys = VGroup(
            label(r"the independent work runs \textit{during} the miss", font_size=24, color=FUNC),
            label(r"results still enter the registers in program order", font_size=24, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.4)
        with self.voiceover(
            "Now the same code on a machine that does not wait its turn. <bookmark mark='a'/> Every instruction "
            "starts as soon as its operands are ready. The load misses, as before, and the add waits for it, as before. "
            "But the ten instructions after the add have nothing to wait for, so they run in the next few cycles, "
            "underneath the miss. <bookmark mark='b'/> They finish long before the load, then wait, in the blue, for "
            "their turn to commit, because the machine still makes its results official in program order. When the "
            "load's data arrives, the add runs and everything commits in a rush. <bookmark mark='c'/> Seventy cycles "
            "instead of eighty-one, and every cycle of independent work was hidden behind the miss."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch.heads), LaggedStart(*[FadeIn(r) for r in ch.rows], lag_ratio=0.04))
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
        verdict = label(rf"the same instructions, \ the same core: \ {sp:.2f} times fewer cycles", font_size=28,
                        color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Scale that up to the Job. Its first chapter runs eight hundred twenty-seven thousand instructions. "
            "<bookmark mark='a'/> Part 7's pipeline took about a million cycles: an IPC, instructions per cycle, of "
            "zero point eight three. <bookmark mark='b'/> This part's core, forced to start its instructions one at a "
            "time and in program order, does a little worse: its front end is deeper than the pipeline's, so a wrong "
            "guess about a branch costs it more. <bookmark mark='c'/> The same core, allowed to look ahead and start "
            "up to four ready instructions a cycle, takes four hundred thirty-eight thousand cycles. An IPC of almost "
            "one point nine. <bookmark mark='d'/> Nothing about the instructions changed, nor the adders, nor "
            "the memory. Only the order in which work is started."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cyc))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.names[k]), FadeIn(ch.vals[k]), FadeIn(ipc[k]))
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
        stat = label(rf"on average {occ['mean']:.1f} in flight; \ never once full", font_size=28,
                     color=HEAD).to_edge(DOWN, buff=0.3)
        real = label(r"Intel's Golden Cove (2021): \ 512 entries", font_size=24, color=GREY_A).next_to(stat, UP,
                                                                                                    buff=0.2)
        with self.voiceover(
            "The machine that did this can hold a hundred twenty-eight instructions in flight at once, in a "
            "structure called the reorder buffer. <bookmark mark='a'/> Here is how many it actually holds, cycle by "
            "cycle, over six hundred cycles of the Job. <bookmark mark='b'/> It climbs, and then it crashes to zero; "
            "climbs and crashes. On average, about eleven instructions are in flight, and the buffer is never once "
            "full. <bookmark mark='c'/> Real cores keep far more: Intel's Golden Cove core of 2021 has five hundred "
            "twelve entries. Why build such a huge window, and what keeps knocking ours down to zero? Both answers "
            "are in this part, and the second one is the most important fact about modern processors."
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
            label(r"the dataflow limit: \ how fast a program \textit{could} run", font_size=28, color=FUNC),
            label(r"Tomasulo's algorithm, \ renaming, \ and the reorder buffer, \ built and checked", font_size=28,
                  color=YES),
            label(r"speculation: \ running hundreds of instructions on a guess", font_size=28, color=CTRL),
            label(r"Spectre: \ a secret read through a bounds check, \ on our own machine", font_size=28, color=NO),
            label(r"the Job: \ ledger row 2", font_size=28, color=COST),
        ).arrange(DOWN, buff=0.38).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is where this part goes. <bookmark mark='a'/> First, a limit: given a program, how fast could any "
            "machine run it, if only the true dependences between its instructions mattered? <bookmark mark='b'/> "
            "Then the machines that approach that limit: the scoreboard of 1964, Tomasulo's algorithm of 1967, "
            "register renaming, and the reorder buffer, built here and checked against the emulator. <bookmark "
            "mark='c'/> Then speculation, the guess that lets a core run hundreds of instructions ahead of what it "
            "knows. <bookmark mark='d'/> Then the price of guessing: in 2018 it was shown that the guesses leave "
            "traces a program can read, and we will read a secret on our own machine. <bookmark mark='e'/> And the "
            "Job, run on the new core, for the next row of the ledger."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcde", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
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
            "This is Part 8 of Computer Science, Built, the second part of Act Two, Making It Fast. <bookmark "
            "mark='a'/> In this part: the dataflow graph of a program, its critical path, and the limit it sets. True "
            "and false dependences, and register renaming, which removes the false ones. The scoreboard of the CDC "
            "6600 and Tomasulo's algorithm, cycle by cycle. The reorder buffer, which lets a machine execute out of "
            "order yet keep its exceptions precise. Superscalar issue and the wall it hits, speculation, and the "
            "ordering of loads and stores. Then Spectre, the compiler's alternative called VLIW, the old argument "
            "between RISC and CISC, multithreading, and the Job."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
