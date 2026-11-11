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
            label("explicit issue groups; \\ hardware still enforces its ISA rules", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Dynamic scheduling spends hardware on dependency checking, wakeup and selection. <bookmark mark='a'/> "
            "A straightforward W-wide rename stage compares destinations and sources within the incoming group, "
            "giving a quadratic family of comparisons. Implementations can organize that logic differently. "
            "<bookmark mark='b'/> Waiting instructions must learn when their operands become available, and ready "
            "operations must compete for resources. <bookmark mark='c'/> Very Long Instruction Word designs move "
            "more scheduling decisions into the compiler, which places operations into explicit issue groups. "
            "<bookmark mark='d'/> The hardware still decodes, executes and handles the ISA's timing, memory and "
            "exception rules. Some designs retain interlocks, caches and variable-latency operations. Static "
            "scheduling changes where decisions are made; it does not eliminate every hardware scheduling or "
            "correctness mechanism."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", costs):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(c, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
            vo.wait_until("d")
            self.play(FadeIn(alt))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bundles(self):
        d = load("vliw")
        head = label("Fixed-path scheduling illustration: \\ four start slots", font_size=32).to_edge(UP, buff=0.3)
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
            "Use the six-operation mismatched-length path as a scheduling illustration with four start slots. This "
            "is not an executable VLIW translation of the whole search. <bookmark mark='a'/> Under the chart's "
            "same-bundle read-before-write convention, the load and table-end test read old register versions while "
            "the increments produce later versions. That convention must be part of a real target's semantics. "
            "<bookmark mark='b'/> With a two-cycle load and these fixed data dependencies, the comparison cannot "
            "start in the next cycle, leaving an empty bundle in this candidate schedule. <bookmark mark='c'/> The "
            "displayed operations occupy three cycles and six of twelve slots. Actual exits, multiple control "
            "operations in a bundle, safe early loads and side effects need a complete control and guard policy "
            "before this could replace the original program."
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
            "Software pipelining overlaps operations from successive loop trips. The colors distinguish trips in "
            "this fixed-path scheduling illustration. <bookmark mark='a'/> Address increments permit some work for "
            "the next trip to begin before the previous trip's load-dependent comparison finishes. Here the modulo "
            "placement satisfies the displayed data and start-slot constraints. <bookmark mark='b'/> Six operations "
            "and four slots give a resource initiation-interval lower bound of two cycles; the one-cycle address "
            "recurrence gives another lower bound of one. Their maximum is two. A complete loop implementation must "
            "also preserve live versions, define control within bundles, handle startup and drain, guard "
            "speculative loads, and recover on exits. The picture does not verify those full-program requirements "
            "or establish an achieved hardware throughput."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(heads))
            self.play(LaggedStart(*[FadeIn(c) for c in g.cells], lag_ratio=0.06), FadeIn(leg), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(g.nops))
            vo.wait_until("b")
            self.play(Write(bound))
        self.wait(1.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        h = load("hook")["miss"]
        head = label("Where static scheduling trades off", font_size=36).to_edge(UP, buff=0.35)
        items = VGroup(
            label("variable latency: \\ interlocks, stalls and other mechanisms depend on the ISA",
                  font_size=23, color=NO),
            label("data-dependent control: \\ branches, predicates or guarded speculation", font_size=23,
                  color=NO),
            label("compatibility can preserve meaning; \\ retuning may improve performance",
                  font_size=23, color=NO),
            label("Itanium (2001, EPIC): \\ predication, advanced loads and wider trade-offs",
                  font_size=23, color=HIST),
            label("used in some DSPs and accelerators; \\ workload and implementation matter",
                  font_size=23, color=YES),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(DOWN * 0.1)
        with self.voiceover(
            "Static and dynamic scheduling make different trade-offs. <bookmark mark='a'/> Cache misses and "
            "variable execution times can invalidate a compiler's preferred timing. Depending on the ISA, "
            "interlocks or other mechanisms preserve correctness, sometimes by stalling. <bookmark mark='b'/> "
            "Data-dependent branches require control flow, predication, speculation or guarded schedules; a "
            "compiler need not know every runtime outcome in advance. <bookmark mark='c'/> A schedule tuned for one "
            "implementation can perform poorly on another. Compatible hardware can preserve the program's meaning "
            "without recompilation; a changed width does not automatically make old code wrong. <bookmark "
            "mark='d'/> Itanium's EPIC approach included features such as predication and advanced loads and faced "
            "several commercial and technical challenges. One simple bundle chart cannot explain its whole history. "
            "<bookmark mark='e'/> VLIW remains useful in some DSPs and accelerators, where workload knowledge and "
            "implementation choices can make static scheduling attractive, even when real systems still contain "
            "caches or variable-latency events."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcde", items):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
                if mk == "a":
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()
