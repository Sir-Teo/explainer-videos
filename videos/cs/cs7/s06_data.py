from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, STAGE_COLOR, STAGES,
                                  YES, PipeChart, PipeFigure, box, fmt, load, mono)


def reveal(scene, pc, rt=0.22):
    for c in range(pc.ncycles):
        if c in pc.columns:
            scene.play(FadeIn(pc.columns[c]), run_time=rt)


class Data(VoiceoverScene):
    def construct(self):
        self.card()
        self.raw()
        self.forwarding()
        self.loaduse()
        self.measured()

    def card(self):
        card = chapter_card(5, r"Data hazards and forwarding", r"What if an instruction needs a result still on its "
                            r"way?", part=PART)
        with self.voiceover("Chapter five. Data hazards and forwarding."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def raw(self):
        d = load("charts")["noforward"]
        head = label(r"Read after write, \ without help", font_size=36).to_edge(UP, buff=0.3)
        pc = PipeChart(d, cw=0.42, ch=0.48, font_size=13, label_size=16).move_to(UP * 0.3)
        notes = VGroup(
            label(r"\texttt{sub} reads \texttt{a1} in ID, \ but \texttt{add} writes it only in WB, \ three cycles later",
                  font_size=22, color=GREY_A),
            label(r"so \texttt{sub} waits in ID \ (the register file writes in the first half of a cycle, \ reads in "
                  r"the second)", font_size=22, color=NO),
            label(rf"{d['retired']} instructions, \ {d['cycles']} cycles: \ every dependent pair costs two bubbles",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Programs are full of instructions that use the result of the one just before. <bookmark mark='a'/> Here "
            "each instruction reads the register its predecessor wrote. The subtract reads a one in the decode stage, "
            "but the add writes a one only in write-back, three stages later. This is a read-after-write hazard. "
            "<bookmark mark='b'/> Without help, the only safe thing is to wait. The subtract sits in decode until the "
            "add has written its result. Part 5's register file is written in the first half of a cycle and read in "
            "the second, so the wait is two cycles rather than three. <bookmark mark='c'/> Every dependent pair costs "
            "two bubbles, and in real code most instructions depend on a recent one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
            vo.wait_until("a")
            reveal(self, pc)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]), LaggedStart(*[Indicate(b, color=NO) for b in pc.bubbles],
                                                                     lag_ratio=0.1))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def forwarding(self):
        d = load("charts")["forward"]
        head = label(r"Forwarding: \ take the result from where it is", font_size=34).to_edge(UP, buff=0.3)
        pc = PipeChart(d, cw=0.42, ch=0.48, font_size=13, label_size=16).move_to(UP * 1.2 + LEFT * 1.4)
        fig = PipeFigure(width=8.0, stage_w=1.1, h=0.8).scale(0.9).move_to(DOWN * 1.7 + LEFT * 2.0)
        arcs = fig.forward_arcs()
        notes = VGroup(
            label(r"the value exists \ at the end of EX: \\ send it straight back \\ to the next instruction's ALU input",
                  font_size=20, color=HEAD),
            label(r"two paths: \ from EX/MEM \ and from MEM/WB; \\ a comparator on register numbers \\ drives each "
                  r"multiplexer", font_size=20, color=GREY_A),
            label(rf"{d['retired']} instructions, \ {d['cycles']} cycles: \\ no bubbles at all", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.3 + DOWN * 1.6)
        with self.voiceover(
            "But the subtract does not really need a one from the register file. It needs the number, and the number "
            "exists as soon as the add leaves the ALU, a whole stage before it is written back. <bookmark mark='a'/> So "
            "send it back directly. Two new paths carry results from the EX/MEM and MEM/WB pipeline registers to the "
            "ALU's inputs, with a multiplexer on each input. <bookmark mark='b'/> A little logic compares register "
            "numbers: if the instruction entering EX reads a register that the instruction one or two ahead is about "
            "to write, it takes the forwarded value instead of the stale one it read in decode. "
            "<bookmark mark='c'/> On the same program, every bubble disappears. The arrows on the chart are the "
            "forwarded values, each going from the end of one instruction's ALU cycle to the start of the next one's."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())), FadeIn(fig))
            vo.wait_until("a")
            self.play(Create(arcs), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            reveal(self, pc, 0.25)
            self.play(LaggedStart(*[Create(a) for a in pc.arrows], lag_ratio=0.2), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loaduse(self):
        d = load("charts")["loaduse"]
        head = label(r"The one forwarding cannot fix: \ load, \ then use", font_size=34).to_edge(UP, buff=0.3)
        pc = PipeChart(d, cw=0.46, ch=0.5, font_size=13, label_size=16).move_to(UP * 0.5)
        notes = VGroup(
            label(r"a loaded word exists only at the end of MEM, \ but the \texttt{add} needs it at the start of EX:"
                  r" \ one cycle too late", font_size=22, color=GREY_A),
            label(r"the hazard unit in ID detects it \ (a load in EX whose $rd$ is a source here) \ and stalls once",
                  font_size=22, color=NO),
            label(r"compilers hide it by moving an independent instruction between the load and its use \ (Part 13)",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One case is beyond forwarding. <bookmark mark='a'/> A load's value does not exist until the end of the "
            "memory stage, but an instruction right behind it needs the value at the start of execute, which is the same "
            "moment. No wire can send a value back in time. <bookmark mark='b'/> So the pipeline needs a hazard unit in "
            "the decode stage: if the instruction in execute is a load, and it writes a register this instruction reads, "
            "hold this instruction for one cycle and send a bubble down. After that one cycle, forwarding from MEM/WB "
            "does the rest. <bookmark mark='c'/> Compilers fight back by scheduling: moving some independent instruction "
            "into the slot between a load and its use, so the bubble does useful work. Part 13's compiler does this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
            vo.wait_until("a")
            reveal(self, pc, 0.3)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), *[Indicate(b, color=NO, scale_factor=1.3) for b in pc.bubbles])
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        hz = load("hazards")["benchmarks"]
        head = label(r"What forwarding buys, \ measured", font_size=36).to_edge(UP, buff=0.35)
        names = list(hz)
        a, b = "no forwarding, no prediction", "forwarding"
        maxc = max(max(hz[n][a]["cpi"], hz[n][b]["cpi"]) for n in names)
        scale = 5.0 / maxc
        rows = VGroup()
        for k, n in enumerate(names):
            y = 2.0 - 0.62 * k
            nl = label(n, font_size=20, color=GREY_A).move_to([-2.6, y, 0], aligned_edge=RIGHT)
            r1 = Rectangle(width=hz[n][a]["cpi"] * scale, height=0.22, stroke_width=0, fill_color=NO,
                           fill_opacity=0.6).move_to([-2.4 + hz[n][a]["cpi"] * scale / 2, y + 0.12, 0])
            r2 = Rectangle(width=hz[n][b]["cpi"] * scale, height=0.22, stroke_width=0, fill_color=YES,
                           fill_opacity=0.7).move_to([-2.4 + hz[n][b]["cpi"] * scale / 2, y - 0.12, 0])
            v = label(rf"{hz[n][a]['cpi']:.2f} $\to$ {hz[n][b]['cpi']:.2f}", font_size=18, color=GREY_A).next_to(
                r1, RIGHT, buff=0.15)
            rows.add(VGroup(nl, r1, r2, v))
        one = DashedLine([-2.4 + scale, 2.4, 0], [-2.4 + scale, -2.2, 0], color=GREY_C, stroke_width=1.5)
        ol = label(r"CPI 1", font_size=18, color=GREY_C).next_to(one, DOWN, buff=0.05)
        key = VGroup(label(r"no forwarding", font_size=20, color=NO), label(r"forwarding", font_size=20, color=YES)
                     ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is what forwarding is worth on real programs, measured on the simulated pipeline. Branches are still "
            "handled crudely here; the next chapters fix them. <bookmark mark='a'/> Without forwarding, CPIs run from "
            "about one and a half to more than two: a third to a half of all cycles are spent waiting for results. "
            "<bookmark mark='b'/> With forwarding, every benchmark improves, the sieve's CPI falling from two point "
            "three to one point four five. What remains is mostly load-use stalls and branches, and branches are "
            "where most of the remaining time goes."
        ) as vo:
            self.play(FadeIn(head), Create(one), FadeIn(ol), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in rows],
                                  lag_ratio=0.15), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(r[2], LEFT), FadeIn(r[3])) for r in rows],
                                  lag_ratio=0.15), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
