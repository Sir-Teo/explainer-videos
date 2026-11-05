from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, code, grid_table,
                                   load, mono)


class Job(VoiceoverScene):
    def construct(self):
        self.card()
        self.passes()
        self.levels()
        self.core()
        self.ledger()
        self.gcc()

    def card(self):
        card = chapter_card(13, r"The Job, compiled", r"Did the program write it better than we did?",
                            lit=(1957,), part=PART)
        with self.voiceover("Chapter thirteen. The Job, compiled."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def passes(self):
        p = load("passes")
        rows = p["rows"]
        head = label(r"Every pass, \ switched on in turn", font_size=34).to_edge(UP, buff=0.25)
        top = max(r["array"] for r in rows)
        W = 6.2
        x0 = -0.9
        bars = VGroup()
        for k, r in enumerate(rows):
            y = 2.45 - k * 0.6
            name = label(r["label"].replace("-O0: every value in memory", r"\texttt{-O0}: \ every value in memory")
                         .replace("+ ", r"$+$ \ "), font_size=20, color=GREY_A)
            name.move_to([x0 - 0.25 - name.width / 2, y, 0])
            w = W * r["array"] / top
            bar = Rectangle(width=w, height=0.36, stroke_width=0, fill_color=YES if k else NO,
                            fill_opacity=0.85).move_to([x0 + w / 2, y + 0.08, 0])
            wl = W * r["list"] / top
            lbar = Rectangle(width=wl, height=0.12, stroke_width=0, fill_color=FUNC, fill_opacity=0.9).move_to(
                [x0 + wl / 2, y - 0.17, 0])
            val = label(f"{r['array']:,}", font_size=17, color=WHITE).next_to(bar, RIGHT, buff=0.1)
            bars.add(VGroup(name, bar, lbar, val))
        hand_x = x0 + W * p["hand"] / top
        hand = DashedLine([hand_x, 2.75, 0], [hand_x, 2.45 - 8 * 0.6 - 0.3, 0], color=DATA, stroke_width=2)
        hl = label(rf"by hand: \ {p['hand']:,}", font_size=17, color=DATA).next_to(hand, DOWN, buff=0.08)
        key = VGroup(VGroup(Rectangle(width=0.4, height=0.2, stroke_width=0, fill_color=YES, fill_opacity=0.85),
                            label(r"array Job", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.1),
                     VGroup(Rectangle(width=0.4, height=0.08, stroke_width=0, fill_color=FUNC, fill_opacity=0.9),
                            label(r"list Job", font_size=16, color=GREY_A)).arrange(RIGHT, buff=0.1)).arrange(
            RIGHT, buff=0.4).to_edge(DOWN, buff=0.75)
        cap = label(rf"instructions executed on the first chapter \ ({p['bytes']:,} bytes)", font_size=17,
                    color=GREY_B).next_to(key, DOWN, buff=0.12)
        r = rows
        with self.voiceover(
            "Now the whole compiler, measured. We compiled both versions of the Job with one pass after another "
            "switched on, and counted the instructions each executes on the first chapter of Pride and Prejudice. "
            "<bookmark mark='a'/> With no optimization, every variable lives in memory, and the array Job runs four "
            "and a half million instructions. <bookmark mark='b'/> Register allocation alone cuts that by almost "
            "two thirds. <bookmark mark='c'/> Loop inversion takes a little more. Converting to SSA makes things "
            "slightly worse, because the copies it leaves behind are not all coalesced away, and constant "
            "propagation finds almost nothing. <bookmark mark='d'/> Value numbering takes a fifth. Moving invariant "
            "code out of the loop takes a tenth. <bookmark mark='e'/> And strength reduction of the table index "
            "takes over a third, landing below the dashed line: the hand-written program of Part 6. Inlining "
            "helps only the list Job, which calls same in its loop. <bookmark mark='f'/> Notice that the order of "
            "the bars is not the order of importance. Two passes, registers and induction variables, did most of "
            "the work; the others prepared the ground for them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(bars[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars[1]))
            vo.wait_until("c")
            self.play(FadeIn(bars[2]))
            self.play(FadeIn(bars[3]), FadeIn(bars[4]))
            vo.wait_until("d")
            self.play(FadeIn(bars[5]))
            self.play(FadeIn(bars[6]))
            vo.wait_until("e")
            self.play(Create(hand), FadeIn(hl))
            self.play(FadeIn(bars[7]))
            self.play(FadeIn(bars[8]))
            vo.wait_until("f")
            self.play(Indicate(bars[1][1], color=HEAD), Indicate(bars[7][1], color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def levels(self):
        j = load("job")
        e = j["emulator"]
        head = label(r"Optimization levels", font_size=34).to_edge(UP, buff=0.3)
        keys = ["array -O0", "array -O1", "array -O2", "array -O3", "hand-written (Part 6)",
                "hand-written, linked (Part 11)"]
        names = [r"\texttt{-O0}", r"\texttt{-O1}", r"\texttt{-O2}", r"\texttt{-O3}", r"by hand", r"by hand, linked"]
        ch = bar_chart([e[k] / 1e6 for k in keys], names, [NO, CTRL, YES, YES, DATA, DATA], height=3.6, bar_w=0.85,
                       gap=0.6, fmt_=lambda v: f"{v:.2f}M", font_size=18).move_to(LEFT * 2.2 + DOWN * 0.3)
        lv = VGroup(
            label(r"\texttt{-O0}: \ every variable in memory, \ for the debugger", font_size=19, color=GREY_A),
            label(r"\texttt{-O1}: \ registers", font_size=19, color=GREY_A),
            label(r"\texttt{-O2}: \ loop inversion, \ SSA and every pass", font_size=19, color=GREY_A),
            label(r"\texttt{-O3}: \ and inlining", font_size=19, color=GREY_A),
            label(rf"list Job: \ {e['list -O0']:,} \ $\to$ \ {e['list -O3']:,}", font_size=19, color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Like gcc and clang, our compiler groups its passes into levels. <bookmark mark='a'/> Level zero keeps "
            "every variable in memory, so a debugger can always find it, and runs six times as many instructions "
            "as level two. Level one allocates registers. Level two adds loop inversion, SSA and every pass we have "
            "seen. Level three adds inlining, which leaves the array Job unchanged. <bookmark mark='b'/> Against "
            "these, the hand-written program of Part 6, and its linked version from Part 11, which used a library "
            "routine for printing. The compiled program executes fewer instructions than either."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch.bars[:4]), FadeIn(ch.vals[:4]), FadeIn(ch.names[:4]), FadeIn(lv), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(ch.bars[4:]), FadeIn(ch.vals[4:]), FadeIn(ch.names[4:]))
        self.wait(0.3)
        self.clear_scene()

    def core(self):
        j = load("job")
        head = label(r"On Part 8's out-of-order core", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for r in j["core"]:
            rows.append([f"{r['bytes']:,}", f"{r['hand_instr']:,}", f"{r['O2_instr']:,}", f"{r['hand']:,}",
                         f"{r['O2']:,}", f"{100 * (r['O2'] / r['hand'] - 1):+.1f}\\%"])
            cols.append([GREY_A, WHITE, YES, WHITE, WHITE, NO if r["O2"] > r["hand"] else YES])
        tab = grid_table([r"passage", r"instr., \ hand", r"instr., \ \texttt{-O2}", r"cycles, \ hand",
                          r"cycles, \ \texttt{-O2}", r"cycles"], rows, widths=[1.5, 2.0, 2.0, 2.0, 2.0, 1.4],
                         row_h=0.45, font_size=18, colors=cols, mono_cols=()).next_to(head, DOWN, buff=0.45)
        pts = VGroup(
            label(r"11\% fewer instructions, \ the same cycles to within 2\%", font_size=22, color=HEAD),
            label(r"the core overlaps the hand-written program's extra instructions for free", font_size=20,
                  color=GREY_A),
            label(r"both programs wait on the same chain of loads, \ table entry after table entry", font_size=20,
                  color=GREY_A),
            label(rf"and \texttt{{-O0}} would be {j['ratio_o0']:.1f} times slower", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "But instructions are not time. On the out-of-order core of Part 8, on six passages of text: "
            "<bookmark mark='a'/> the compiled program executes eleven percent fewer instructions, and takes about "
            "the same number of cycles, one or two percent more. <bookmark mark='b'/> The core runs several "
            "instructions per cycle, so the hand-written program's extra instructions cost almost nothing: they "
            "run in the shadow of loads. Both programs wait on the same chain of loads, one table entry after "
            "another, and that chain is the same length however the instructions around it are written. <bookmark "
            "mark='c'/> And level zero, by comparison, is four point four times slower. Optimization matters; the "
            "last ten percent of it, on a modern core, often does not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3]))
        self.wait(0.3)
        self.clear_scene()

    def ledger(self):
        j = load("job")
        led = j["ledger"]
        head = label(r"Ledger row 5", font_size=38).to_edge(UP, buff=0.35)
        rows = led + [{"part": p_, "label": t} for p_, t in ((16, r"sort, then count"), (17, r"a hash table"))]
        tab = ledger_table(rows, shown=6, highlight=(5,), font_size=21, row_h=0.42, label_width=4.8).move_to(
            DOWN * 0.3)
        res = VGroup(
            label(rf"compiled from the Pebble language: \ {human_time(led[5]['seconds'])}, \ one core; \ hand-written: "
                  rf"\ {human_time(led[3]['seconds'])}", font_size=23, color=COST),
            label(rf"unoptimized, \ it would have been {human_time(led[5]['o0_seconds'])}", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So the ledger gets its sixth row. <bookmark mark='a'/> The Job compiled from the Pebble language, on "
            "one core of Part 8's machine, would take about fifty-eight seconds on all thirty novels, against "
            "fifty-seven for the hand-written program. Unoptimized, it would take over four minutes. <bookmark "
            "mark='b'/> This row is not about speed. It is FORTRAN's promise, kept: the program now comes from a "
            "readable source, with names, types and loops, and it runs as fast as our best hand-written "
            "assembly. The speed-ups to come, in Parts 16 and 17, will come from changing the algorithm, and the "
            "compiler will carry them to the machine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.axis), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(res))
            vo.wait_until("b")
            self.play(Indicate(tab.rows[5], color=COST))
        self.wait(0.3)
        self.clear_scene()

    def gcc(self):
        g = load("gcc")
        head = label(r"On this machine: \ gcc and the C Job of Part 10", font_size=32).to_edge(UP, buff=0.3)
        ch = bar_chart([r["seconds"] for r in g["rows"]], [rf"\texttt{{{r['level']}}}" for r in g["rows"]],
                       [NO, YES, YES, YES], height=3.4, bar_w=1.0, gap=0.8, fmt_=lambda v: f"{v * 1000:.0f} ms",
                       font_size=19).move_to(LEFT * 2.6 + DOWN * 0.3)
        cap = label(rf"\textit{{Pride and Prejudice}}, \ {g['bytes'] / 1e3:.0f} KB, \ one thread; \ best of 3",
                    font_size=17, color=GREY_B).next_to(ch, DOWN, buff=0.4)
        pts = VGroup(
            label(r"\texttt{-O1} \ halves the time: \ registers, \ mostly", font_size=21, color=YES),
            label(r"\texttt{-O2} and \texttt{-O3} \ add nothing here: \ the scan waits on memory", font_size=21,
                  color=GREY_A),
            label(r"the same shape as our compiler's, \ on a real machine", font_size=21, color=HEAD),
            label(g["gcc"].split(" (")[0] + " " + g["gcc"].split()[-1], font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The same pattern holds on a real machine. <bookmark mark='a'/> Here is the C version of the Job, from "
            "Part 10, compiled by gcc at each level and run on this computer over the whole of Pride and Prejudice. "
            "Level zero takes two hundred and fifteen milliseconds. Level one, a hundred and fifteen: registers, "
            "mostly. <bookmark mark='b'/> Levels two and three add nothing, and are even a little slower. The Job "
            "scans its table, and the scan waits on memory, which no compiler can make shorter. <bookmark "
            "mark='c'/> A real compiler, a real processor, and the same lesson."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(cap))
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()
