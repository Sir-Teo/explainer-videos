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


class Fsm(VoiceoverScene):
    def construct(self):
        self.card()
        self.machine()
        self.run()
        self.mealy()
        self.encodings()

    def card(self):
        card = chapter_card(6, r"Finite-state machines", r"What can a circuit with a few bits of memory do?",
                            lit=(1955, 1956), part=PART)
        with self.voiceover("Chapter six. Finite-state machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

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

    # ------------------------------------------------------------------
    def mealy(self):
        head = label(r"The same detector, \ as a Mealy machine", font_size=36).to_edge(UP, buff=0.35)
        pos = {"S0": (-4.2, -0.4), "S1": (-1.4, 1.0), "S10": (1.4, -0.4), "S101": (4.2, 1.0)}
        edges = [("S0", "S0", "0/0", DOWN), ("S0", "S1", "1/0", 0), ("S1", "S1", "1/0", UP), ("S1", "S10", "0/0", 0),
                 ("S10", "S0", "0/0", -0.5), ("S10", "S101", "1/0", -0.3), ("S101", "S10", "0/0", -0.3),
                 ("S101", "S1", "1/1", 0.5)]
        sd = StateDiagram(pos, edges, radius=0.48, font_size=22, edge_font=20, names=NAMES)
        hl = SurroundingRectangle(sd.edge[-1][1], buff=0.08, color=YES)
        txt = VGroup(
            label(r"edges carry input / output: \ the 1 is produced \textit{on the transition} that completes 1011",
                  font_size=24, color=GREY_A),
            label(r"4 states instead of 5, \ response timing depends on the output interface", font_size=26, color=YES),
            label(r"but it follows the input combinationally, \ glitches and all: \ often a register is added after it",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "George Mealy's style puts the output on the transitions instead of the states. <bookmark mark='a'/> "
            "Each arrow now carries two labels, the input bit that takes it and the output bit it produces. The "
            "detector no longer needs a state meaning the whole pattern has been seen: from one zero one, a one "
            "completes the pattern, and the output is raised on that very transition, as the machine moves back "
            "to the state that remembers a single one. <bookmark mark='b'/> Four states instead of five. With the "
            "output timing drawn here, the combinational Mealy indication can precede the Moore state output; an "
            "inherent one-cycle saving is not guaranteed for every interface. <bookmark mark='c'/> The price is "
            "that a Mealy output depends directly on the input, through logic, within the cycle, so it can "
            "glitch; designers often register it, which gives back the cycle they saved. Every Moore machine has "
            "a Mealy equivalent and vice versa, so the choice is about timing and size, not about what can be "
            "computed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd.nodes))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in sd.edges], lag_ratio=0.12), run_time=3.0)
            self.play(Create(hl), FadeIn(txt[0]))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]))
            vo.wait_until("c")
            self.play(FadeIn(txt[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def encodings(self):
        d = load("fsm")["encodings"]
        head = label(r"Five states, \ three ways to store them", font_size=36).to_edge(UP, buff=0.35)
        cols = ("binary", "Gray", "one-hot")
        hdr = VGroup(label(r"state", font_size=22, color=GREY_B), *[label(c, font_size=24, color=CTRL) for c in cols])
        rows = VGroup(hdr)
        for s in ("S0", "S1", "S10", "S101", "S1011"):
            rows.add(VGroup(MathTex(r"\texttt{" + NAMES[s] + "}", font_size=26, color=GREY_A),
                            *[MathTex(d[c]["codes"][s], font_size=26, color=DATA) for c in cols]))
        for name, key, colr in ((r"flip-flops", "flip_flops", YES), (r"gates", "gates", COST),
                                (r"literals", "literals", GREY_A)):
            rows.add(VGroup(label(name, font_size=22, color=colr),
                            *[MathTex(str(d[c][key]), font_size=28, color=colr) for c in cols]))
        for i, r in enumerate(rows):
            for j, m in enumerate(r):
                m.move_to([-6.0 + 1.55 * j, 2.3 - 0.52 * i, 0])
        notes = VGroup(
            label(r"logic minimized by Quine--McCluskey, \\ unused codes as don't-cares", font_size=22, color=GREY_B),
            label(r"each version simulated on 64 random streams of 400 bits: \ $\checkmark$", font_size=22, color=YES),
            label(r"one-hot: \ more flip-flops, \ simpler logic; \\ FPGAs, rich in flip-flops, \ prefer it", font_size=24,
                  color=HEAD),
            label(r"Gray counters: one-bit increments; \\ arbitrary FSM transitions may change several bits",
                  font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 0.0 + DOWN * 0.3, aligned_edge=LEFT)
        with self.voiceover(
            "To build the machine, give each state a binary code and store the code in flip-flops. <bookmark "
            "mark='a'/> The choice of codes matters. Numbering the states in binary needs three flip-flops. A "
            "Gray code, where consecutive codes differ in one bit, also needs three. One-hot gives each state its "
            "own flip-flop, five in all, with exactly one of them on. <bookmark mark='b'/> For each encoding, the "
            "next-state and output logic was minimized, with the unused codes as don't-cares, built as gates, and "
            "simulated against the specification. Here binary is cheapest, fourteen gates; one-hot pays two extra "
            "flip-flops for logic almost as small; Gray, with this numbering, is worst. <bookmark mark='c'/> "
            "There is no universal winner. One-hot is often useful on FPGAs with plentiful flip-flops. Gray "
            "counters are useful across clock domains when each increment changes only one bit and timing "
            "constraints are respected. Assigning Gray labels to an arbitrary state graph does not make every "
            "transition change one bit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[:6]))
            vo.wait_until("b")
            self.play(FadeIn(rows[6:]), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()
