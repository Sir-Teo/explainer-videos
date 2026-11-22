from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs5.common import fsm_block, tick_tokens, BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, WIRE, YES, load

POS = {"S0": (-5.0, -0.5), "S1": (-2.5, 1.1), "S10": (0.0, -0.5), "S101": (2.5, 1.1), "S1011": (5.0, -0.5)}
NAMES = {"S0": "-", "S1": "1", "S10": "10", "S101": "101", "S1011": "1011"}


def detector():
    edges = [
        ("S0", "S0", "0", DOWN), ("S0", "S1", "1", 0), ("S1", "S1", "1", UP), ("S1", "S10", "0", 0),
        ("S10", "S0", "0", -0.5), ("S10", "S101", "1", -0.3), ("S101", "S10", "0", -0.3), ("S101", "S1011", "1", 0),
        ("S1011", "S10", "0", -0.5), ("S1011", "S1", "1", 0.45),
    ]
    return StateDiagram(POS, edges, radius=0.48, font_size=22, edge_font=20, accept=("S1011",), names=NAMES)


class Fsm(WatchScene):
    def construct(self):
        self.card()
        self.machine()
        self.run()

    def card(self):
        self.chapter(6, r"Finite-state machines", r"What can a circuit with a few bits of memory do?", lit=(1955, 1956), part=PART, said="Chapter six. Finite-state machines.")

    # ------------------------------------------------------------------
    def machine(self):
        head = label(r"A detector for the pattern 1011", font_size=38).to_edge(UP, buff=0.35)
        sd = detector()
        cap = label(r"each state remembers how much of the pattern has just been seen", font_size=26,
                    color=GREY_A).to_edge(DOWN, buff=1.0)
        mm = label(r"Moore: \ the output depends on the state \ (1 only in \texttt{1011}); \quad Mealy: \ on the state "
                   r"and the input", font_size=24, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A register and some logic make a finite-state machine: a circuit with a few bits of memory that "
            "reacts to a stream of inputs, one per clock cycle. <bookmark mark='a'/> Here is one that watches a "
            "stream of bits and raises its output whenever the last four were one, zero, one, one. Each state "
            "stands for how much of the pattern has just been seen: nothing, a one, one zero, one zero one, or "
            "the whole pattern. <bookmark mark='b'/> The arrows say where each input bit leads. A wrong bit does "
            "not always start from scratch: after one zero one, a zero leaves one zero, which is still the start "
            "of a match. <bookmark mark='c'/> Its output depends only on the state, which makes it a Moore "
            "machine, after Edward Moore's 1956 paper; George Mealy's machines of 1955 let the output depend on "
            "the input too, so the response can occur within the cycle."
        ) as vo:
            blk = fsm_block(0.95).move_to(UP * 0.3)
            self.play(FadeIn(head), FadeIn(blk))
            tick_tokens(self, blk, ticks=3, run_time=1.0)
            vo.wait_until("a")
            self.play(FadeOut(blk))
            self.play(FadeIn(sd.nodes, lag_ratio=0.2), FadeIn(cap))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(e) for e in sd.edges], lag_ratio=0.12), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(mm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run(self):
        self.ask(r"The machine watches for 1011 in \\ 1011011101011. \\ How many times does it fire?", [r"2", r"3", r"4"], 1,
                 say="The machine watches for one zero one one, overlaps included. How many times does it fire on this input?",
                 reveal="Three times.")
        d = load("fsm")
        tr = d["trace"]
        head = label(r"Running it", font_size=38).to_edge(UP, buff=0.35)
        sd = detector().shift(UP * 0.6)
        self.add_foreground_mobject(sd.glow)
        cells = VGroup()
        for i, t in enumerate(tr[:-1]):
            cells.add(VGroup(MathTex(str(t["x"]), font_size=32, color=DATA),
                             MathTex(str(tr[i + 1]["y"]), font_size=28, color=YES if tr[i + 1]["y"] else GREY_C)).arrange(
                DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.32).to_edge(DOWN, buff=0.8)
        rl = VGroup(label(r"input", font_size=22, color=DATA).next_to(cells[0][0], LEFT, buff=0.4),
                    label(r"output", font_size=22, color=YES).next_to(cells[0][1], LEFT, buff=0.4))
        with self.voiceover(
            "Feed it the input one zero one one zero one one one zero one zero one one. <bookmark mark='a'/> The "
            "highlighted state walks through the diagram one clock cycle per bit, and the output rises exactly three "
            "times, each just after a complete one zero one one, including the two that overlap. Thirteen bits of "
            "history, and the machine never needed more than five states to keep track of what matters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd), FadeIn(rl))
            self.play(sd.light("S0"))
            vo.wait_until("a")
            for i, t in enumerate(tr[:-1]):
                self.play(FadeIn(cells[i][0]), run_time=0.25)
                self.play(sd.light(tr[i + 1]["state"]), FadeIn(cells[i][1]), run_time=0.45)
        self.wait(0.5)
        self.clear_scene()


