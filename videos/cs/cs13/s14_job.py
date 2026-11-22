from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs13.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart, code, grid_table,
                                   load, mono)


class Job(WatchScene):
    def construct(self):
        self.card()
        self.passes()
        self.core()
        self.ledger()

    def card(self):
        self.chapter(13, r"The Job, compiled", r"Did the program write it better than we did?", lit=(1957,), part=PART, said="Chapter thirteen. The Job, compiled.")

    def passes(self):
        self.ask(r"The Job compiled with optimizations, \\ against without. Instructions executed?",
                 [r"about the same", r"far fewer"], 1,
                 say="Compile the Job with optimizations, and without. How many fewer instructions run?",
                 reveal="Far fewer: values stay in registers, and repeated work disappears.")
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

