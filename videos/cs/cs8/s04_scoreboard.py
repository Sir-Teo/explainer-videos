from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  grid_table, load, mono)

STAGE_NAMES = [r"issue", r"read operands", r"execute done", r"write result"]


class Scoreboard(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.stages()
        self.table()
        self.limits()

    def card(self):
        card = chapter_card(3, r"The scoreboard", "How does dynamic scheduling keep track?", lit=(1964,),
                            extra=((1964, r"CDC 6600: \ Thornton and Cray"),), part=PART)
        with self.voiceover("Chapter three. The scoreboard."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"Control Data 6600, \ 1964", font_size=40).to_edge(UP, buff=0.35)
        units = ["add", "multiply", "multiply", "divide", "long add", "shift", "boolean", "branch", "increment",
                 "increment"]
        boxes = VGroup(*[box(1.35, 0.6, rf"\text{{{u}}}", FUNC if i < 5 else DATA, 18) for i, u in enumerate(units)])
        boxes.arrange_in_grid(rows=2, cols=5, buff=(0.18, 0.25)).move_to(UP * 0.9)
        sb = box(5.0, 0.7, r"\text{the scoreboard}", HEAD, 26).next_to(boxes, DOWN, buff=0.5)
        lines = VGroup(*[Line(sb.get_top(), b.get_bottom(), color=GREY_D, stroke_width=1.5) for b in boxes])
        facts = VGroup(
            label("ten functional units; \\ 100 ns clock; \\ overlap subject to constraints", font_size=24,
                  color=GREY_A),
            label(r"designed by Seymour Cray, \ with James Thornton, \ in a lab in Chippewa Falls", font_size=24,
                  color=GREY_A),
            label("a landmark in dynamic instruction scheduling", font_size=24, color=HIST),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Control Data 6600, delivered in 1964, is a landmark in dynamic instruction scheduling, associated "
            "with Seymour Cray and James Thornton. <bookmark mark='a'/> Its ten functional units could overlap "
            "different operations, subject to dependencies and shared resources. <bookmark mark='b'/> The "
            "scoreboard tracked functional-unit availability, pending register writers and operand readiness. That "
            "bookkeeping let instructions execute out of order while protecting their register dependencies. "
            "<bookmark mark='c'/> The machine used a hundred-nanosecond clock. Historical peak floating-point rates "
            "and application throughput are different measures, so we will focus on its scheduling mechanism rather "
            "than a universal performance ranking. The important question is how several units cooperate without "
            "changing the program's results."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.08))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(sb), Create(lines))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def stages(self):
        head = label(r"Four steps, \ and a hazard checked at each", font_size=36).to_edge(UP, buff=0.35)
        steps = VGroup(*[box(2.6, 0.9, rf"\text{{{t}}}", c, 24) for t, c in zip(
            ("issue", "read operands", "execute", "write result"), (CTRL, DATA, FUNC, YES))]).arrange(RIGHT, buff=0.45)
        steps.move_to(UP * 1.2)
        arrows = VGroup(*[Arrow(steps[k].get_right(), steps[k + 1].get_left(), buff=0.05, color=GREY_C,
                                stroke_width=3) for k in range(3)])
        checks = VGroup(
            label(r"in order: \ a free unit, \ and no one else \\ about to write my destination \ (WAW)",
                  font_size=20, color=CTRL),
            label(r"wait until every source \\ has been written \ (RAW)", font_size=20, color=DATA),
            label(r"the unit works \\ for its latency", font_size=20, color=FUNC),
            label(r"wait until no earlier instruction \\ still has to read the old value \ (WAR)", font_size=20,
                  color=YES),
        )
        for c, s in zip(checks, steps):
            c.next_to(s, DOWN, buff=0.35)
        note_ = label(r"operands are read from the registers: \ a result reaches its user by being written",
                      font_size=24, color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Each instruction passes through four steps, and the scoreboard checks one kind of hazard at each. "
            "<bookmark mark='a'/> Issue happens in program order. An instruction issues when its kind of unit is "
            "free, and when no instruction already in flight is going to write the same register; that is the write "
            "after write hazard, and the 6600 simply refuses to have two writers of one name. <bookmark mark='b'/> "
            "Next, read operands. The instruction waits at its unit until every register it reads has been written "
            "by whoever was producing it: the true dependence. <bookmark mark='c'/> Then it executes, taking as many "
            "cycles as its unit needs. <bookmark mark='d'/> Last, write result. Before overwriting its destination, it "
            "waits until every earlier instruction that still needs the old value has read it: the write after read "
            "hazard. <bookmark mark='e'/> Notice that values travel only through the registers. Every hazard is a "
            "wait; nothing is renamed."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.2), Create(arrows))
            for mk, c in zip("abcd", checks):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("scoreboard")
        lat = d["latency"]
        head = label(r"The textbook example, \ cycle by cycle", font_size=34).to_edge(UP, buff=0.3)
        sub = note(rf"latencies: \ load {lat['lw']}, \ add {lat['add']}, \ multiply {lat['mul']}, \ divide "
                   rf"{lat['div']} \quad (Hennessy and Patterson's)", font_size=20).next_to(head, DOWN, buff=0.12)
        sb = d["scoreboard"]
        rows = [[p, "", "", "", ""] for p in d["program"]]
        t = grid_table([r"instruction", *STAGE_NAMES], rows, [3.4, 1.4, 2.2, 2.2, 2.2], row_h=0.55, font_size=22)
        t.move_to(DOWN * 0.15)
        keys = ("issue", "read", "exec", "write")
        events = []
        for i, s in enumerate(sb):
            for k, key in enumerate(keys):
                events.append((s[key], i, k))
        events.sort()
        nums = {}
        for c, i, k in events:
            cell = t.cells[i + 1][k + 1]
            m = label(str(c), font_size=24, color=WHITE).move_to(cell)
            nums[(i, k)] = m
        clock = label(r"cycle 0", font_size=26, color=HEAD).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        notes = VGroup(
            label(r"the second load waits for the one integer unit", font_size=22, color=INF),
            label(r"the divide waits at its unit until the multiply writes \ (RAW)", font_size=22, color=DATA),
            label(r"the add is done at 16, \ but may not write \texttt{a1} until the divide has read it \ (WAR)",
                  font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.25)

        def cyc(n):
            return label(rf"cycle {n}", font_size=26, color=HEAD).move_to(clock)

        with self.voiceover(
            "Here is the standard example from Hennessy and Patterson's textbook, written in Pebble's registers, "
            "with their latencies: a load takes one cycle, an add two, a multiply ten, a divide forty. <bookmark "
            "mark='a'/> Watch the scoreboard fill in the cycle at which each instruction completes each step. The "
            "first load issues in cycle one, reads in two, executes in three, writes in four. <bookmark mark='b'/> "
            "The second load cannot even issue until cycle five: there is only one integer unit, and the first load "
            "holds it until its result is written. <bookmark mark='c'/> The multiply and the subtract both wait for "
            "the second load, then read their operands together in cycle nine. The divide needs the multiply's "
            "result, so it waits at its unit until cycle twenty-one. <bookmark mark='d'/> And the last add. It issues "
            "in thirteen, when the adder is free, and its result is ready by sixteen. But it writes a1, and the "
            "divide, an earlier instruction, has not yet read the old a1. So the add sits on its finished result "
            "until cycle twenty-two. <bookmark mark='e'/> The whole thing takes sixty-two cycles."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(t), FadeIn(clock))
            done = set()
            vo.wait_until("a")
            for c, i, k in events:
                if c > 4 and "b" not in done:
                    vo.wait_until("b")
                    done.add("b")
                    self.play(FadeIn(notes[0]))
                if c > 9 and "c" not in done:
                    vo.wait_until("c")
                    done.add("c")
                    self.play(FadeIn(notes[1]))
                if c > 12 and "d" not in done:
                    vo.wait_until("d")
                    done.add("d")
                if c == 22:
                    self.play(FadeIn(notes[2]))
                self.play(FadeIn(nums[(i, k)], scale=1.3), Transform(clock, cyc(c)), run_time=0.3)
            vo.wait_until("e")
            self.play(Indicate(nums[(5, 3)], color=NO), Indicate(nums[(4, 1)], color=NO))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        head = label(r"What the scoreboard cannot do", font_size=36).to_edge(UP, buff=0.4)
        items = VGroup(
            label(r"a false dependence is a wait: \ WAW stops issue, \ WAR stops the write", font_size=26, color=NO),
            label(r"values pass through the registers: \ a cycle to write, \ a cycle to read", font_size=26,
                  color=CTRL),
            label(r"one instruction stuck at issue \ blocks every one behind it", font_size=26, color=INF),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.3)
        nxt = label("tags and broadcast help; \\ traditional dispatch remains in order", font_size=30, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This scoreboard handles several hazards by waiting. <bookmark mark='a'/> A pending writer blocks "
            "another writer of the same register, and an earlier reader can delay a later writeback. <bookmark "
            "mark='b'/> In this model, results reach their users through register writes and subsequent operand "
            "reads. <bookmark mark='c'/> Dispatch is in program order: if the next instruction cannot reserve its "
            "required unit, later instructions cannot dispatch past it. <bookmark mark='d'/> Tomasulo's algorithm "
            "adds reservation stations, producer tags and direct result broadcast. Those remove register-name "
            "hazards and decouple dispatch from immediate unit availability. Traditional Tomasulo still dispatches "
            "in order, and still stalls when the needed station is full. It does not remove every limit listed "
            "here."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.wait(0.3)
        self.clear_scene()
