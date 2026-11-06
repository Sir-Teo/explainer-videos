from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs28.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


def step(state, bit):
    s = ((state << 1) | bit) & 0b111
    out = (bin(s & 0b111).count("1") & 1, bin(s & 0b101).count("1") & 1)
    return s & 0b11, out


class Viterbi(VoiceoverScene):
    def construct(self):
        self.card()
        self.trellis()
        self.measured()

    def card(self):
        card = chapter_card(10, r"Convolutional codes and Viterbi", r"Can a code be decoded as it streams?",
                            lit=(1955, 1967), extra=((1955, r"Elias"), (1966, r"Forney: \ concatenation"),
                                                     (1967, r"Viterbi")), part=PART)
        with self.voiceover("Chapter ten. Convolutional codes and the Viterbi algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def trellis(self):
        v = load("viterbi")
        head = label(r"A code with memory, \ and its trellis", font_size=34).to_edge(UP, buff=0.3)
        bits = v["sample"]
        T = len(bits)
        x0, dx = -5.6, 1.45
        ys = {0: 1.2, 1: 0.3, 2: -0.6, 3: -1.5}
        nodes = VGroup(*[Dot([x0 + dx * t, ys[s], 0], radius=0.07, color=GREY_B) for t in range(T + 1) for s in range(4)])
        edges = VGroup()
        for t in range(T):
            for s in range(4):
                for b in (0, 1):
                    ns, _ = step(s, b)
                    edges.add(Line([x0 + dx * t, ys[s], 0], [x0 + dx * (t + 1), ys[ns], 0], stroke_width=1.2,
                                   color=GREY_D if b == 0 else GREY_C))
        slabels = VGroup(*[mono(f"{s >> 1}{s & 1}", 16, GREY_A).next_to([x0, ys[s], 0], LEFT, buff=0.25)
                           for s in range(4)])
        path = VGroup()
        outs = VGroup()
        s = 0
        for t, b in enumerate(bits):
            ns, o = step(s, b)
            path.add(Line([x0 + dx * t, ys[s], 0], [x0 + dx * (t + 1), ys[ns], 0], stroke_width=5, color=YES))
            outs.add(mono(f"{o[0]}{o[1]}", 18, HEAD).move_to([x0 + dx * (t + 0.5), 2.0, 0]))
            outs.add(mono(str(b), 18, DATA).move_to([x0 + dx * (t + 0.5), 2.45, 0]))
            s = ns
        il = label(r"in", font_size=16, color=DATA).move_to([x0 - 0.7, 2.45, 0])
        ol = label(r"out", font_size=16, color=HEAD).move_to([x0 - 0.7, 2.0, 0])
        lines = VGroup(
            label(r"each input bit is shifted into a 3-bit register; \ two parity bits come out \ (rate $\tfrac12$, "
                  r"generators 111 and 101)", font_size=20, color=WHITE),
            label(r"the \textbf{trellis}: \ the 4 possible register states at each time; \ every message is a path",
                  font_size=20, color=GREY_A),
            label(r"\textbf{Viterbi} \ (1967): \ for each state keep only the best path so far, \ by Hamming "
                  r"distance to what arrived", font_size=20, color=YES),
            label(r"dynamic programming \ (Part 19): \ $4 \times 2$ comparisons per bit, \ whatever the message length",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Hamming and Reed-Solomon codes work on fixed blocks. Peter Elias's convolutional codes of 1955 work on "
            "streams. <bookmark mark='a'/> Each input bit is shifted into a small register, and two parity bits of "
            "the register come out: rate one half. This message, one zero one one zero zero, produces these pairs. "
            "<bookmark mark='b'/> The register has four states, and drawing them over time gives a trellis: every "
            "possible message is a path through it. <bookmark mark='c'/> Decoding means finding the path whose "
            "outputs are closest to what arrived. Andrew Viterbi saw in 1967 that at each step you need to keep only "
            "the best path into each state; any path through a state that loses there can never win later. "
            "<bookmark mark='d'/> It is dynamic programming, Part 19's idea: eight comparisons per bit, however long "
            "the message."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(slabels))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(il), FadeIn(ol), FadeIn(outs))
            vo.wait_until("b")
            self.play(Create(edges), FadeIn(lines[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(path), FadeIn(lines[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        v = load("viterbi")
        head = label(r"Viterbi, \ measured", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1.5, 0.5], y_range=[0, 5, 1], x_length=5.8, y_length=4.2,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.55).to_edge(
            LEFT, buff=1.0)
        lg = math.log10
        xt = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(ax.c2p(lg(x) + 2.4, 0), DOWN, buff=0.08)
                      for x, t in ((0.005, "0.005"), (0.01, "0.01"), (0.03, "0.03"), (0.1, "0.1"))])
        yt = VGroup(*[label(rf"$10^{{{y}}}$", font_size=15, color=GREY_A).next_to(ax.c2p(0, y + 5), LEFT, buff=0.08)
                      for y in (-4, -3, -2, -1)])
        xl = label(r"channel flip probability", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.35)
        rows = [r for r in v["rows"] if r["coded"] > 0]
        raw = VMobject(color=GREY_B, stroke_width=3).set_points_as_corners(
            [ax.c2p(lg(r["p"]) + 2.4, lg(r["raw"]) + 5) for r in v["rows"]])
        cod = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(lg(r["p"]) + 2.4, lg(r["coded"]) + 5)
                                                                         for r in rows])
        cdots = VGroup(*[Dot(ax.c2p(lg(r["p"]) + 2.4, lg(r["coded"]) + 5), radius=0.06, color=YES) for r in rows])
        keys = VGroup(label(r"no code", font_size=18, color=GREY_B), label(r"(7,5) code + Viterbi", font_size=18,
                                                                            color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.c2p(0.4, 4.4))
        r2 = next(r for r in v["rows"] if r["p"] == 0.02)
        z = next(r for r in v["rows"] if r["p"] == 0.005)
        notes = VGroup(
            label(r"20{,}000 random bits per point", font_size=20, color=GREY_A),
            label(rf"at 2\% flips: \ {r2['coded'] * 1e4:.1f} errors per 10{{,}}000 \\ instead of 200", font_size=20,
                  color=YES),
            label(rf"at 0.5\%: \ {int(z['coded'] * 20000)} errors in 20{{,}}000", font_size=20, color=YES),
            label(r"real systems use 64 states and \textbf{soft} decisions: \\ the receiver's confidence in each "
                  r"bit", font_size=20, color=WHITE),
            label(r"Forney \ (1966): \ \textbf{concatenate}: \ an inner \\ convolutional code, \ an outer "
                  r"Reed--Solomon code \\ to mop up its bursts of errors", font_size=20, color=HEAD),
            label(r"Voyager, \ GSM, \ Wi-Fi until the 2000s, \ and \\ your phone's 4G control channel", font_size=20,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "We sent twenty thousand random bits through the code at each noise level. <bookmark mark='a'/> With two "
            "percent of the channel bits flipped, Viterbi's decoder leaves about six and a half errors per ten "
            "thousand data bits, instead of two hundred. At half a percent, none at all. <bookmark mark='b'/> Real "
            "systems use registers with sixty-four states, and soft decisions: the receiver passes on how confident "
            "it is in each bit, not just a zero or a one. <bookmark mark='c'/> David Forney showed in 1966 how to "
            "combine codes: an inner convolutional code, and an outer Reed-Solomon code to clean up the short bursts "
            "of errors a Viterbi decoder leaves behind. <bookmark mark='d'/> That pairing flew on Voyager, and "
            "convolutional codes ran GSM, early Wi-Fi and 4G's control channel."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(notes[0]))
            self.play(Create(raw), FadeIn(keys[0]))
            vo.wait_until("a")
            self.play(Create(cod), FadeIn(cdots), FadeIn(keys[1]), FadeIn(notes[1]), FadeIn(notes[2]))
            for mk, n_ in zip("bcd", notes[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
