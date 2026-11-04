from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  grid_table, load, mono)

GROUPS = (("Load", 3, INF, r"load unit"), ("Add", 3, FUNC, r"adder"), ("Mult", 2, CTRL, r"multiply / divide"))
REGS = ["a0", "a1", "a2", "a3", "a4", "a5"]


class Tomasulo(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.machine()
        self.compare()
        self.catch()

    def card(self):
        card = chapter_card(4, r"Tomasulo's algorithm", r"What if every value had a name of its own?", lit=(1967,),
                            extra=((1967, r"IBM 360/91: \ Tomasulo"),), part=PART)
        with self.voiceover("Chapter four. Tomasulo's algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        head = label(r"IBM System/360 Model 91, \ 1967", font_size=38).to_edge(UP, buff=0.4)
        facts = VGroup(
            label(r"its floating-point unit had only \ \textit{four} registers to name values with", font_size=26,
                  color=GREY_A),
            label(r"Robert Tomasulo's idea: \ name a value by the unit that will produce it", font_size=26,
                  color=HEAD),
            label(r"a waiting instruction holds either a value \ or the \textit{tag} of the station making it",
                  font_size=26, color=YES),
            label(r"when a result is ready, \ its tag and value are broadcast to everyone at once", font_size=26,
                  color=DATA),
        ).arrange(DOWN, buff=0.4).move_to(DOWN * 0.1)
        with self.voiceover(
            "In 1967 IBM shipped the System/360 Model 91, a machine built for scientific computing. <bookmark "
            "mark='a'/> Its floating-point unit had a problem far worse than Pebble's: only four floating-point "
            "registers in the instruction set, so the same few names were reused constantly, and a scoreboard would "
            "have stalled on false dependences all the time. <bookmark mark='b'/> Robert Tomasulo's answer was to "
            "stop naming values by registers at all. A value in flight is named by the reservation station, a small "
            "waiting area in front of a functional unit, of the instruction that will produce it. <bookmark "
            "mark='c'/> An instruction waiting in a station holds, for each operand, either the value itself or the "
            "tag of the station that will produce it. <bookmark mark='d'/> And when a unit finishes, it broadcasts "
            "the result and its tag on a common data bus. Every station and the register file listen, and whoever is "
            "waiting for that tag takes the value. This is register renaming, done in 1967 with a handful of tags."
        ) as vo:
            self.play(FadeIn(head))
            for mk, f in zip("abcd", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def build(self, d):
        prog = d["program"]
        queue = VGroup(*[mono(p, 17) for p in prog]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        qtitle = label(r"instructions, \ in order", font_size=18, color=GREY_B).next_to(queue, UP, buff=0.12)
        qbox = SurroundingRectangle(queue, color=GREY_D, buff=0.12)
        qg = VGroup(qtitle, qbox, queue).to_corner(UL, buff=0.3).shift(DOWN * 0.55)
        stations = {}
        cols = VGroup()
        for name, n, c, unit in GROUPS:
            rows = VGroup()
            for k in range(n):
                nm = f"{name}{k + 1}"
                r = Rectangle(width=3.0, height=0.42, stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.08)
                t = Text(nm, font="DejaVu Sans Mono", font_size=14, color=c).move_to(r.get_left() + RIGHT * 0.38)
                rows.add(VGroup(r, t))
                stations[nm] = r
            rows.arrange(DOWN, buff=0.04)
            u = box(2.4, 0.5, rf"\text{{{unit}}}", c, 18).next_to(rows, DOWN, buff=0.35)
            ar = Arrow(rows.get_bottom(), u.get_top(), buff=0.04, color=c, stroke_width=2,
                       max_tip_length_to_length_ratio=0.3)
            cols.add(VGroup(rows, ar, u))
        cols.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to([1.3, 0.75, 0])
        regs = VGroup()
        for r in REGS:
            cell = Rectangle(width=1.1, height=0.38, stroke_color=GREY_C, stroke_width=1.2)
            regs.add(VGroup(Text(r, font="DejaVu Sans Mono", font_size=15, color=CODE), cell).arrange(RIGHT, buff=0.1))
        regs.arrange(DOWN, buff=0.04)
        rtitle = label(r"registers: \ who will write them", font_size=17, color=GREY_B).next_to(regs, UP, buff=0.1)
        rg = VGroup(rtitle, regs).to_corner(DL, buff=0.35).shift(UP * 0.15)
        # the common data bus: under the units, up to the stations and the registers
        y_bus = cols.get_bottom()[1] - 0.35
        bus = VGroup(Line([rg.get_right()[0] + 0.2, y_bus, 0], [cols.get_right()[0] + 0.15, y_bus, 0], color=HEAD,
                          stroke_width=5))
        blabel = label(r"common data bus", font_size=18, color=HEAD).next_to(bus, DOWN, buff=0.08).align_to(bus, RIGHT)
        taps = VGroup()
        for col in cols:
            u = col[2]
            taps.add(Line(u.get_bottom(), [u.get_x(), y_bus, 0], color=HEAD, stroke_width=3))
        up = Line([cols.get_right()[0] + 0.15, y_bus, 0], [cols.get_right()[0] + 0.15, cols.get_top()[1], 0],
                  color=HEAD, stroke_width=3)
        to_regs = Line([rg.get_right()[0] + 0.2, y_bus, 0], [regs.get_right()[0] + 0.05, y_bus, 0], color=HEAD,
                       stroke_width=3)
        busg = VGroup(bus, taps, up, to_regs, blabel)
        return qg, queue, cols, stations, regs, rg, busg, y_bus

    def contents(self, d, snap, stations, regs, queue):
        prog = d["program"]
        g = VGroup()
        for nm, info in snap["stations"].items():
            r = stations[nm]
            i = info["i"]
            op = prog[i].split()[0]
            parts = [Text(op, font="DejaVu Sans Mono", font_size=14, color=WHITE)]
            if op == "lw":
                parts.append(Text(prog[i].split(",")[1].strip(), font="DejaVu Sans Mono", font_size=14, color=YES))
            else:
                for reg, tag in info["waits"].items():
                    parts.append(Text(tag if tag else reg, font="DejaVu Sans Mono", font_size=14,
                                      color=HEAD if tag else YES))
            row = VGroup(*parts).arrange(RIGHT, buff=0.22).move_to(r.get_center() + RIGHT * 0.38)
            if info["running"]:
                row.add(Dot(r.get_right() + LEFT * 0.15, radius=0.06, color=FUNC))
            g.add(row)
        for k, reg in enumerate(REGS):
            tag = snap["regs"].get(reg)
            if tag:
                g.add(Text(tag, font="DejaVu Sans Mono", font_size=14, color=HEAD).move_to(regs[k][1]))
        return g

    def machine(self):
        d = load("scoreboard")
        snaps = d["snaps"]
        tm = d["tomasulo"]
        head = label(r"The same example, \ with tags", font_size=32).to_edge(UP, buff=0.25)
        qg, queue, cols, stations, regs, rg, busg, y_bus = self.build(d)
        clock = label(r"cycle 0", font_size=24, color=HEAD).to_corner(UR, buff=0.3).shift(DOWN * 0.45)
        leg = VGroup(label(r"green: \ a value in hand", font_size=17, color=YES),
                     label(r"yellow: \ a tag, \ still to come", font_size=17, color=HEAD)).arrange(
            RIGHT, buff=0.5).to_edge(DOWN, buff=0.15)
        cur = VGroup()
        self.play(FadeIn(head), FadeIn(qg), FadeIn(cols), FadeIn(rg), FadeIn(busg), FadeIn(clock), FadeIn(leg))

        def show(c, rt=0.45):
            nonlocal cur
            snap = snaps[c - 1]
            new = self.contents(d, snap, stations, regs, queue)
            anims = [FadeOut(cur), FadeIn(new), Transform(clock, label(rf"cycle {c}", font_size=24,
                                                                          color=HEAD).move_to(clock))]
            hl = [queue[i] for i, s in enumerate(tm) if s["issue"] == c]
            self.play(*anims, *[Indicate(h, color=HEAD, scale_factor=1.05) for h in hl], run_time=rt)
            cur = new
            if snap["bus"] is not None:
                src = tm[snap["bus"]]["rs"]
                grp = [k for k, (nm, *_) in enumerate(GROUPS) if src.startswith(nm)][0]
                u = cols[grp][2]
                dot = Dot(u.get_bottom(), radius=0.16, color=HEAD)
                tag = Text(src, font="DejaVu Sans Mono", font_size=14, color=BG).move_to(dot)
                pulse = VGroup(dot, tag)
                path = VMobject().set_points_as_corners([u.get_bottom(), [u.get_x(), y_bus, 0],
                                                         [busg[0].get_left()[0], y_bus, 0]])
                path2 = VMobject().set_points_as_corners([[u.get_x(), y_bus, 0], [busg[2].get_x(), y_bus, 0],
                                                          busg[2].get_end()])
                ghost = pulse.copy()
                self.add(pulse, ghost)
                self.play(MoveAlongPath(pulse, path), MoveAlongPath(ghost, path2), run_time=0.8)
                self.play(FadeOut(pulse), FadeOut(ghost), run_time=0.2)

        with self.voiceover(
            "Here is the machine. On the left, the instructions waiting to issue, in order. In the middle, the "
            "reservation stations: three for loads, three in front of the adder, two in front of the "
            "multiplier and divider. Below them the units, and under everything the common data bus, which runs "
            "back to every station and to the registers. <bookmark mark='a'/> Cycle one: the first load issues into "
            "Load1, and the register a1 now records that its next value will come from Load1. Cycle two: the second "
            "load issues, and a2 points at Load2. <bookmark mark='b'/> Cycle three: the multiply issues. Its operand "
            "a2 is not ready, so the station takes the tag Load2 instead. And the first load broadcasts: tag Load1 "
            "and its value go out on the bus, and a1 takes it. <bookmark mark='c'/> Cycle four: Load2 broadcasts, "
            "and the multiply, which was waiting for that tag, captures the value. The subtract issues with both its "
            "values in hand. <bookmark mark='d'/> Cycle five: the divide issues, waiting on tag Mult1, and holding the "
            "current value of a1. Cycle six: the last add issues. It will write a1, so a1 now points at Add2, but the "
            "divide does not care: it has already copied the old a1. That is the write after read hazard, gone. "
            "<bookmark mark='e'/> The subtract broadcasts in cycle seven, the add starts in the next cycle, and it broadcasts "
            "in cycle ten, while the multiply is still working. <bookmark mark='f'/> The multiply finishes in "
            "fifteen and its broadcast wakes the divide, which takes forty cycles and broadcasts in fifty-six."
        ) as vo:
            vo.wait_until("a")
            show(1)
            show(2)
            vo.wait_until("b")
            show(3)
            vo.wait_until("c")
            show(4)
            vo.wait_until("d")
            show(5)
            show(6)
            vo.wait_until("e")
            for c in range(7, 11):
                show(c, 0.35)
            vo.wait_until("f")
            show(15)
            show(16, 0.3)
            show(56)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("scoreboard")
        head = label(r"Scoreboard against Tomasulo", font_size=36).to_edge(UP, buff=0.35)
        rows = []
        colors = []
        for p, a, b in zip(d["program"], d["scoreboard"], d["tomasulo"]):
            rows.append([p, str(a["write"]), str(b["write"])])
            colors.append([WHITE, GREY_B, YES if b["write"] < a["write"] - 2 else WHITE])
        t = grid_table([r"instruction", r"scoreboard: \ written", r"Tomasulo: \ broadcast"], rows, [3.6, 3.0, 3.0],
                       row_h=0.55, font_size=24, colors=colors).move_to(UP * 0.3)
        total = label(rf"{d['sb_cycles']} cycles \ against \ {d['tm_cycles']}", font_size=30, color=HEAD).next_to(
            t, DOWN, buff=0.4)
        why = VGroup(
            label(r"no WAR wait: \ the divide copied \texttt{a1} at issue", font_size=24, color=YES),
            label(r"no register round trip: \ the bus hands a result straight to its users", font_size=24,
                  color=DATA),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Side by side. <bookmark mark='a'/> Most results arrive a little earlier, because the bus hands a value "
            "straight to the stations waiting for it, with no write and read through the register file. <bookmark "
            "mark='b'/> And the last add finishes twelve cycles sooner: under Tomasulo nobody waits for an earlier "
            "reader, because every reader has already copied what it needs. <bookmark mark='c'/> Fifty-six cycles "
            "instead of sixty-two. The divide's forty cycles dominate both, as they should: that is this example's "
            "critical path."
        ) as vo:
            self.play(FadeIn(head), FadeIn(t))
            vo.wait_until("a")
            self.play(FadeIn(why[1]))
            vo.wait_until("b")
            self.play(Indicate(t.cells[6][2], color=YES), FadeIn(why[0]))
            vo.wait_until("c")
            self.play(FadeIn(total))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def catch(self):
        d = load("scoreboard")["tomasulo"]
        head = label(r"The catch: \ results land out of order", font_size=36).to_edge(UP, buff=0.4)
        line = NumberLine(x_range=[0, 60, 10], length=11, include_numbers=True, font_size=20, color=GREY_C).move_to(
            DOWN * 0.2)
        marks = VGroup()
        prog = load("scoreboard")["program"]
        for i, s in enumerate(d):
            p = line.n2p(s["write"])
            col = NO if i == 4 else (HEAD if i == 5 else GREY_B)
            dot = Dot(p, radius=0.1 if i in (4, 5) else 0.07, color=col)
            if i in (4, 5):
                t = Text(prog[i], font="DejaVu Sans Mono", font_size=18, color=col).next_to(dot, UP, buff=0.35)
                t.add(Line(t.get_bottom() + DOWN * 0.05, dot.get_top(), color=col, stroke_width=1.5))
            else:
                t = VectorizedPoint(p)
            marks.add(VGroup(dot, t))
        others = note(r"(grey: \ the other four)", font_size=18).next_to(line.n2p(4), DOWN, buff=0.55)
        marks[0].add(others)
        q = VGroup(
            label(r"suppose the divide divides by zero, \ in cycle 55", font_size=26, color=NO),
            label(r"by then the add, \ a later instruction, \ has already overwritten \texttt{a1}", font_size=26,
                  color=HEAD),
            label(r"the machine cannot stop \textit{between} two instructions: \ the exception is imprecise",
                  font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a catch, and it is serious. <bookmark mark='a'/> Here is when each instruction's result reached "
            "the registers: the add in cycle ten, the divide in fifty-six. Program order says the divide comes "
            "first. <bookmark mark='b'/> Now suppose the divide divides by zero. The machine discovers this in cycle "
            "fifty-five, and wants to stop with every earlier instruction done and every later one untouched, so the "
            "operating system can report the error, or fix it and resume. <bookmark mark='c'/> But the add, a later "
            "instruction, overwrote a1 forty-five cycles ago. There is no moment between the divide and the add at "
            "which the registers were ever in a consistent state. The exception is imprecise. The Model 91 lived with "
            "this; its manuals warned programmers that a floating-point error could be reported some instructions "
            "late. For general-purpose machines with virtual memory, where any load may fault and must be restarted, "
            "it is not acceptable. The fix took eighteen years."
        ) as vo:
            self.play(FadeIn(head), Create(line))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(q[0]), Indicate(marks[4], color=NO))
            vo.wait_until("c")
            self.play(FadeIn(q[1]), Indicate(marks[5], color=HEAD))
            self.play(FadeIn(q[2]))
        self.wait(0.3)
        self.clear_scene()
