from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, KIND_COLOR, NO, PART, YES, box,
                                  fmt, load, mono)

KINDS = ["branch", "load", "branch", "alu", "alu", "jump"]


def bundle_grid(starts, ops, width, cycles, cw=2.4, ch=0.55, trips=1, ii=None, font_size=15):
    """VLIW bundles: one column per cycle (a long instruction word), one row per slot; ``trips`` copies of the loop
    body, each started ``ii`` cycles after the last (software pipelining)."""
    g = VGroup()
    g.cells = VGroup()
    frame = VGroup()
    for c in range(cycles):
        for w in range(width):
            frame.add(Rectangle(width=cw, height=ch, stroke_color=GREY_D, stroke_width=1).move_to([c * cw, -w * ch, 0]))
    g.add(frame)
    g.frame = frame
    used: dict[int, int] = {}
    trip_cols = [YES, DATA, CTRL, INF]
    for k in range(trips):
        off = (ii or 0) * k
        for i, t in enumerate(starts):
            c = t + off
            if c >= cycles:
                continue
            slot = used.get(c, 0)
            used[c] = slot + 1
            col = KIND_COLOR[KINDS[i]] if trips == 1 else trip_cols[k % 4]
            r = Rectangle(width=cw * 0.94, height=ch * 0.84, stroke_width=0, fill_color=col, fill_opacity=0.45)
            txt = Text(ops[i], font="DejaVu Sans Mono", font_size=font_size, color=WHITE)
            if txt.width > cw * 0.9:
                txt.width = cw * 0.9
            cell = VGroup(r, txt.move_to(r)).move_to([c * cw, -slot * ch, 0])
            g.cells.add(cell)
    g.nops = VGroup()
    for c in range(cycles):
        for w in range(used.get(c, 0), width):
            t = Text("nop", font="DejaVu Sans Mono", font_size=font_size, color=GREY_D).move_to([c * cw, -w * ch, 0])
            g.nops.add(t)
    g.add(g.cells, g.nops)
    return g


class Vliw(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.bundles()
        self.pipelined()
        self.why()

    def card(self):
        card = chapter_card(10, r"The compiler's alternative: \ VLIW", r"What if the compiler did the scheduling?",
                            lit=(1981, 2001), extra=((1981, r"Fisher: \ trace scheduling"), (2001, r"Itanium")),
                            part=PART)
        with self.voiceover("Chapter ten. The compiler's alternative."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        head = label(r"Scheduling in hardware is expensive", font_size=36).to_edge(UP, buff=0.4)
        costs = VGroup(
            label(r"rename $W$ instructions a cycle: \ compare each with all the others \ $\sim W^2$", font_size=24,
                  color=CTRL),
            label(r"wake up: \ every result's tag compared with every waiting operand", font_size=24, color=FUNC),
            label(r"select: \ pick the oldest ready, \ every cycle, \ in a fraction of a nanosecond", font_size=24,
                  color=INF),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 0.5)
        alt = VGroup(
            label(r"Very Long Instruction Word: \ the compiler packs independent operations into a bundle,", font_size=26,
                  color=HEAD),
            label(r"one per unit; \ the hardware just runs bundle after bundle, \ in order", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Everything we have built so far finds parallelism at run time, in hardware, and that hardware is costly. "
            "<bookmark mark='a'/> Renaming W instructions in one cycle means comparing each one's sources with the "
            "destinations of all the others renamed alongside it: work that grows as the square of the width. "
            "<bookmark mark='b'/> Every result's tag must be compared with every operand waiting in the issue queue. "
            "<bookmark mark='c'/> And every cycle, the oldest ready instructions must be picked out of dozens, in a "
            "fraction of a nanosecond. <bookmark mark='d'/> So from the early 1980s, Joseph Fisher at Yale and others "
            "argued for the opposite design. Let the compiler, which can study the whole program at leisure, find the "
            "independent operations and pack them into one very long instruction word, a bundle with one slot for "
            "each unit. The hardware then needs no scheduling at all."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", costs):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(alt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bundles(self):
        d = load("vliw")
        head = label(r"The scan loop, \ scheduled by a compiler, \ four slots wide", font_size=32).to_edge(UP, buff=0.3)
        ops = [o.split("#")[0].strip() for o in d["ops"]]
        g = bundle_grid(d["start"], ops, d["width"], d["block_cycles"], cw=3.0, ch=0.6, font_size=17).move_to(UP * 0.5)
        heads = VGroup(*[label(rf"bundle {c}", font_size=20, color=GREY_B).next_to(g.frame[c * d['width']], UP,
                                                                                   buff=0.15)
                         for c in range(d["block_cycles"])])
        facts = VGroup(
            label(rf"{d['block_cycles']} cycles a trip \ (the pipeline: 7); \ {d['nops']} of {d['slots']} slots are "
                  r"\texttt{nop}", font_size=24, color=HEAD),
            label(r"bundle 1 is empty: \ the load needs two cycles, \ and nothing else is ready", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Here is the Job's scan loop, compiled for a four-wide VLIW machine. <bookmark mark='a'/> The first "
            "bundle holds four operations that need nothing from each other: the end-of-table test, the load of the "
            "entry's length, and the two increments, which may share a bundle with the instructions reading the old "
            "values. <bookmark mark='b'/> The second bundle is empty. The compiler knows a load takes two cycles, "
            "and nothing else in this trip is ready, so it must fill the slots with no-ops. <bookmark mark='c'/> The "
            "third holds the length test and the jump back. Three cycles a trip, against the pipeline's seven, with "
            "no scheduling hardware at all. But half the slots are wasted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(heads))
            vo.wait_until("a")
            first = [c for c in g.cells if abs(c.get_x() - g.frame[0].get_x()) < 0.1]
            self.play(LaggedStart(*[FadeIn(c) for c in first], lag_ratio=0.2))
            vo.wait_until("b")
            mid = [n for n in g.nops if abs(n.get_x() - g.frame[d["width"]].get_x()) < 0.1]
            self.play(FadeIn(VGroup(*mid)))
            vo.wait_until("c")
            rest = [c for c in g.cells if c not in first]
            self.play(LaggedStart(*[FadeIn(c) for c in rest], lag_ratio=0.2), FadeIn(VGroup(*[n for n in g.nops
                                                                                               if n not in mid])))
            self.play(FadeIn(facts))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pipelined(self):
        d = load("vliw")
        head = label(r"Software pipelining: \ start the next trip before this one ends", font_size=32).to_edge(
            UP, buff=0.3)
        ops = [o.split("#")[0].strip().split()[0] for o in d["ops"]]
        ii = d["ii"]
        g = bundle_grid(d["mstart"], ops, d["width"], 9, cw=1.3, ch=0.55, trips=4, ii=ii, font_size=15).move_to(
            UP * 0.4)
        heads = VGroup(*[label(str(c), font_size=18, color=GREY_B).next_to(g.frame[c * d['width']], UP, buff=0.12)
                         for c in range(9)])
        leg = VGroup(*[label(rf"trip {k + 1}", font_size=20, color=c) for k, c in enumerate((YES, DATA, CTRL, INF))]
                     ).arrange(RIGHT, buff=0.5).next_to(g, DOWN, buff=0.35)
        bound = MathTex(r"\text{II} \ge \max\!\Big(\Big\lceil \tfrac{6 \text{ ops}}{4 \text{ slots}} \Big\rceil, "
                        r"\ \underbrace{1}_{\texttt{t0} \,\to\, \texttt{t0}}\Big) = 2", font_size=34,
                        color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A compiler can do better, by overlapping trips: software pipelining, worked out by Bob Rau and others "
            "around 1981, and by Monica Lam in 1988. <bookmark mark='a'/> Start a new trip every two cycles. Trip "
            "two begins while trip one is still finishing, in the slots trip one leaves free, and so on: in the "
            "steady state each bundle mixes the start of one trip with the end of the one before. <bookmark mark='b'/> Two cycles is as fast "
            "as this loop can go on four slots. The interval between trips is bounded by the resources, six "
            "operations into four slots, and by the loop-carried chain, the add to t0, which needs one cycle. The "
            "larger bound wins: two. That is three instructions a cycle on the loop's common path, with none of the "
            "out-of-order hardware. Part 13's compiler will do this kind of scheduling."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(heads))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in g.cells], lag_ratio=0.06), FadeIn(leg), run_time=3.0)
            self.play(FadeIn(g.nops))
            vo.wait_until("b")
            self.play(Write(bound))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        h = load("hook")["miss"]
        head = label(r"Why VLIW lost the desktop", font_size=36).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"the compiler cannot know which loads will miss: \ one miss stalls every slot of every bundle",
                  font_size=23, color=NO),
            label(r"the bne in our loop: \ taken or not depends on the data; \ the schedule must assume", font_size=23,
                  color=NO),
            label(r"code is tied to one width and one set of latencies: \ new chips need recompiled programs",
                  font_size=23, color=NO),
            label(r"Intel and HP's Itanium (2001, \ EPIC): \ late, \ and x86-64 (AMD, 2003) ran the old code fast",
                  font_size=23, color=HIST),
            label(r"VLIW thrives where code is known and latencies fixed: \ signal processors, \ some AI chips",
                  font_size=23, color=YES),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Then why does your laptop not work this way? <bookmark mark='a'/> Because the compiler must plan for "
            "latencies it cannot know. It assumed a load takes two cycles. When a load misses the cache and takes "
            "sixty, a VLIW machine, marching in lockstep, stalls every slot of every bundle behind it, which is "
            "exactly the in-order problem of the hook. The out-of-order core simply finds other work. <bookmark "
            "mark='b'/> It also cannot know branches that depend on data, like our length test, so it must guess at "
            "compile time, or execute both sides under predicates and throw one away. <bookmark mark='c'/> And code "
            "scheduled for one width and one set of latencies is wrong for the next generation of chips. <bookmark "
            "mark='d'/> Intel and Hewlett-Packard bet heavily on this design, as EPIC, in the Itanium of 2001, with "
            "features to soften each problem. It arrived late, and in 2003 AMD's sixty-four-bit x86 ran existing "
            "software fast; the last Itaniums shipped in 2021. <bookmark mark='e'/> VLIW lives on where programs "
            "are known and latencies fixed: in digital signal processors, and in some machine-learning accelerators."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcde", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
