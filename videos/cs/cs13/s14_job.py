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
            f"This experiment enables transformations cumulatively on both Job versions and counts instructions on the same first-chapter input. <bookmark mark='a'/> The unoptimized array configuration executes {r[0]['array']:,} instructions. <bookmark mark='b'/> Register allocation brings it to {r[1]['array']:,}. <bookmark mark='c'/> The next bars add inversion, SSA and constant propagation. Their changes reflect the actual combination, including copies left after SSA destruction. <bookmark mark='d'/> Value numbering changes the preceding array count by {100 * (r[5]['array'] / r[4]['array'] - 1):+.1f} percent, and the repaired invariant-code pass changes it by {100 * (r[6]['array'] / r[5]['array'] - 1):+.1f} percent. <bookmark mark='e'/> Strength reduction then changes it by {100 * (r[7]['array'] / r[6]['array'] - 1):+.1f} percent. The final array count is {r[-1]['array']:,}, beside the dashed hand-written baseline of {p['hand']:,}. Inlining changes the list version here while leaving the array count unchanged. <bookmark mark='f'/> This order is an experiment, not a universal ranking of passes. Legality, register pressure, code shape and earlier transformations interact. A correct compiler may miss an optimization; an unsafe shortcut does not count as a valid speed improvement."
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
        with self.voiceover("Our compiler groups transformations into named levels. <bookmark mark='a'/> In this implementation, level zero gives source variables stack storage; level one allocates registers; level two adds loop inversion, SSA and the optimization pipeline; level three also inlines selected functions. The array Job's final bars coincide in this run. GCC and Clang use their own version-dependent sets of transformations, so matching level names do not imply matching pipelines. Stack storage alone also does not provide a complete source debugger. <bookmark mark='b'/> Compare these bars with the hand-written Part 6 program and its linked Part 11 variant. They report executed instructions on one input, including the implementations' actual overhead. The cycle comparison is a separate experiment.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ch.bars[:4]), FadeIn(ch.vals[:4]), FadeIn(ch.names[:4]), FadeIn(lv), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
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
            cols.append([GREY_A, WHITE, NO if r["O2_instr"] > r["hand_instr"] else YES,
                         WHITE, WHITE, NO if r["O2"] > r["hand"] else YES])
        tab = grid_table([r"passage", r"instr., \ hand", r"instr., \ \texttt{-O2}", r"cycles, \ hand",
                          r"cycles, \ \texttt{-O2}", r"cycles"], rows, widths=[1.5, 2.0, 2.0, 2.0, 2.0, 1.4],
                         row_h=0.45, font_size=18, colors=cols, mono_cols=()).next_to(head, DOWN, buff=0.45)
        pts = VGroup(
            label("six sampled passages: compare instruction totals and simulated cycles", font_size=22, color=HEAD),
            label("overlap can hide some instruction work; dependency chains remain", font_size=20,
                  color=GREY_A),
            label("these totals suggest dependencies; they do not isolate every causal bottleneck", font_size=20,
                  color=GREY_A),
            label(rf"unoptimized aggregate cycle cost: {j['ratio_o0']:.1f} times hand-written", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            (
            "Instruction count is not elapsed time. This table uses Part 8's simulated out-of-order core and six text passages. <bookmark mark='a'/> The table records both instruction totals and cycles for each implementation; compare their actual differences on every passage. Compare each row and the aggregate ratio rather than assuming one fixed percentage for every input. <bookmark mark='b'/> Overlap and dependency chains help explain why eliminating instructions may save few cycles. The observations are consistent with important load dependencies; these totals alone are not a full causal performance-counter study. <bookmark mark='c'/> The unoptimized comparison has a much larger aggregate cycle cost. Optimization matters on this workload, but neither the last few percent nor the same bottleneck must generalize to another program, machine or input distribution."
        )
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
            f"The sixth ledger row is a projection from the recorded model. <bookmark mark='a'/> We multiply the earlier hand-written row's corpus estimate by the ratio of total compiled to hand-written cycles across six sampled passages. This gives {led[5]['seconds']:.1f} seconds for compiled code, versus {led[3]['seconds']:.1f} seconds for the hand-written baseline; the unoptimized projection is {led[5]['o0_seconds']:.1f} seconds. These are extrapolated times under the earlier clock and cost assumptions, not a full-corpus hardware timing. <bookmark mark='b'/> The practical achievement is a readable source program that approaches this hand-written implementation on the selected machine model. Later algorithm changes can alter the amount of work much more substantially. New inputs or machines require new measurements."
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
            label("compare the recorded best-of-three host times", font_size=21, color=YES),
            label("level ordering can vary with host, compiler version and workload", font_size=21,
                  color=GREY_A),
            label("elapsed time is distinct from instruction counts and simulated cycles", font_size=21, color=HEAD),
            label(g["gcc"].split(" (")[0] + " " + g["gcc"].split()[-1], font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        if pts.width > 5.2:
            pts.scale_to_fit_width(5.2)
        pts.to_edge(RIGHT, buff=0.5)
        with self.voiceover(f"The host experiment uses the C Job from Part 10 and the recorded GCC version. <bookmark mark='a'/> Each bar is the best of three one-thread runs on the same input. Level zero records {g['rows'][0]['seconds'] * 1000:.1f} milliseconds; level one records {g['rows'][1]['seconds'] * 1000:.1f}. <bookmark mark='b'/> Levels two and three record {g['rows'][2]['seconds'] * 1000:.1f} and {g['rows'][3]['seconds'] * 1000:.1f} milliseconds. Read this run's ordering from the bars; it can change across hosts and repetitions. Optimization levels change several decisions, so these timings alone do not isolate register allocation or prove a particular memory bottleneck. <bookmark mark='c'/> They do show why choosing a level should include measurement of the real workload. Instruction counts, simulated cycles and host elapsed time are related evidence with different boundaries.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(ch), FadeIn(cap), run_time=0.6)
            vo.wait_until('a')
            self.play(FadeIn(pts[0]))
            vo.wait_until('b')
            self.play(FadeIn(pts[1]))
            vo.wait_until('c')
            self.play(FadeIn(pts[2:]))
        self.wait(0.3)
        self.clear_scene()
