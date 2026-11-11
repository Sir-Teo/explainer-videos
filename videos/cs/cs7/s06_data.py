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
            label('\\texttt{sub} waits in ID; \\\\ model policy: write-back before decode in each cycle', font_size=22, color=NO),
            label(rf"{d['retired']} instructions, \ {d['cycles']} cycles: \ shown adjacent ALU pairs cost two bubbles",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Instructions often use a recent result. <bookmark mark='a'/> In this example, the subtract reads register "
            "a one in decode before the preceding add has written it back. That is a read-after-write hazard. "
            "<bookmark mark='b'/> Without forwarding, hold the subtract until the value is in the register file. Our "
            "simulator writes back before decoding in each cycle, allowing a write and a dependent read in that cycle. "
            "This ordering is a model policy, not a physical half-cycle timing proof. <bookmark mark='c'/> The shown "
            "adjacent ALU dependencies each need two bubbles. Other distances, operations and memory latencies can "
            "require different waits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
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
            label('EX/MEM before MEM/WB; ignore $x0$; \\\\ do not forward an unavailable load result', font_size=20, color=GREY_A),
            label(rf"{d['retired']} instructions, \ {d['cycles']} cycles: \\ no bubbles at all", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.3 + DOWN * 1.6)
        with self.voiceover(
            "The consumer needs the value, not necessarily a register-file read. An ALU result already exists before "
            "write-back. <bookmark mark='a'/> Forward it from EX/MEM or MEM/WB to the next instruction's execute "
            "inputs. <bookmark mark='b'/> Compare source and destination numbers, ignore writes to register zero, and "
            "prefer the newest matching producer in EX/MEM over an older MEM/WB result. An EX/MEM load holds an "
            "address, not its loaded data, so that value cannot be forwarded as the answer. <bookmark mark='c'/> For "
            "this ALU chain, all the dependency bubbles disappear. The arrows show the bypass paths. The next example "
            "explains why forwarding cannot eliminate every data stall."
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
            "A load reveals forwarding's limit. <bookmark mark='a'/> The following instruction needs the loaded value "
            "at the start of its execute stage, but the load produces it only at the end of memory access. Those "
            "events fall in the same cycle, at different instants: forwarding cannot send a value backward in time. "
            "<bookmark mark='b'/> Hold fetch and decode for one cycle and insert a bubble into execute. <bookmark "
            "mark='c'/> One cycle later the value is available from MEM/WB and the dependent operation can proceed. "
            "This one-bubble result assumes our one-cycle memory and the shown consumer timing; other machines or "
            "consumers can differ."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pc.heads), FadeIn(VGroup(*pc.rows.values())))
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
