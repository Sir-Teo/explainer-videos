from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs3.common import COST, CTRL, DATA, HEAD, NO, ONE, PART, WIRE, YES, ZERO, load
from videos.cs.cs3.s08_mux import mux_symbol


def byte_row(bits, cell=0.5, color=DATA):
    g = VGroup()
    for i, b in enumerate(bits):
        sq = Square(cell, stroke_color=GREY_C, stroke_width=1.5, fill_color=YES if b else "#121722",
                    fill_opacity=0.55 if b else 1)
        g.add(VGroup(sq, MathTex(str(b), font_size=24, color=WHITE if b else GREY_D)).move_to([i * cell, 0, 0]))
    return g


class Blocks(VoiceoverScene):
    def construct(self):
        self.card()
        self.comparator()
        self.priority()
        self.shifter()
        self.table()

    def card(self):
        card = chapter_card(11, r"The blocks Pebble needs", r"What does a processor build from gates?", part=PART)
        with self.voiceover("Chapter eleven. The blocks Pebble needs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def comparator(self):
        head = label(r"A comparator: \ is $a < b$?", font_size=38).to_edge(UP, buff=0.35)
        a = [1, 0, 1, 1]
        b = [1, 0, 0, 1]
        A = byte_row(a).move_to(LEFT * 2.6 + UP * 1.0)
        B = byte_row(b).next_to(A, DOWN, buff=0.25)
        la = MathTex(r"a = 11", font_size=30, color=DATA).next_to(A, LEFT, buff=0.4)
        lb = MathTex(r"b = 9", font_size=30, color=DATA).next_to(B, LEFT, buff=0.4)
        steps = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"scan from the top bit: \ while the bits agree, \ keep going", GREY_A),
            (r"at the first difference, \ the number with the 0 is smaller", HEAD),
            (r"$\mathit{lt} = \bar a_3 b_3 + e_3\, \bar a_2 b_2 + e_3 e_2\, \bar a_1 b_1 + \dots$, \ \ $e_i = "
             r"\overline{a_i \oplus b_i}$", CTRL),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(B, DOWN, buff=0.6).shift(RIGHT * 2.2)
        res = label(r"$a > b$: \ \ $\mathit{lt} = 0$, \ $\mathit{eq} = 0$", font_size=30, color=YES).move_to(
            RIGHT * 3.4 + UP * 0.8)
        with self.voiceover(
            "With the tools of this part we can now build the parts a processor needs. Pebble will compare numbers, "
            "for instructions like branch if less than. <bookmark mark='a'/> Is a less than b? Scan from the most "
            "significant bit. While the bits agree, the answer depends on what comes later. <bookmark mark='b'/> At "
            "the first place they differ, the number with the zero there is smaller. Here a has a one where b has a "
            "zero, so a is bigger. <bookmark mark='c'/> As a formula: an equal signal for each bit, an exclusive-nor, "
            "and a sum of terms, one per position, each requiring all the higher bits to be equal. Built and checked on "
            "every pair of inputs, the four-bit version takes twenty-one gates."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(la), FadeIn(lb))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]))
            for i in range(3):
                self.play(Indicate(VGroup(A[i], B[i]), color=HEAD if a[i] != b[i] else GREY_A), run_time=0.6)
                if a[i] != b[i]:
                    break
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def priority(self):
        head = label(r"A priority encoder: \ where is the highest 1?", font_size=36).to_edge(UP, buff=0.35)
        x = [0, 0, 1, 0, 1, 1, 0, 0]  # bit 7 first
        row = byte_row(x).move_to(LEFT * 2.4 + UP * 0.8)
        idx = VGroup(*[MathTex(str(7 - i), font_size=22, color=GREY_B).next_to(row[i], UP, buff=0.1) for i in range(8)])
        out = MathTex(r"y = 101_2 = 5, \quad \mathit{valid} = 1", font_size=36, color=YES).next_to(row, DOWN, buff=0.6)
        uses = VGroup(label(r"which interrupt to serve first \ (Part 31)", font_size=26, color=GREY_A),
                      label(r"normalizing a floating-point number: \\ count the leading zeros \ (Part 52)", font_size=26,
                            color=GREY_A),
                      label(r"one-hot of the highest 1, \ then OR into binary", font_size=26, color=CTRL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.6 + DOWN * 0.6)
        with self.voiceover(
            "Next, a priority encoder. <bookmark mark='a'/> Given eight wires, report the position of the highest one "
            "that is on. Here, bits five, three and two are on; the answer is five, and a valid flag says that some bit "
            "was on at all. <bookmark mark='b'/> The circuit first keeps only the highest one, by and-ing each bit with "
            "not of everything above it, and then turns that single hot wire back into a number. Processors use it to "
            "decide which interrupt to serve first, and to normalize floating-point numbers by counting leading zeros."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(idx))
            vo.wait_until("a")
            self.play(Indicate(row[2], color=HEAD, scale_factor=1.3), FadeIn(out))
            vo.wait_until("b")
            self.play(FadeIn(uses, lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shifter(self):
        head = label(r"A barrel shifter: \ shift by any amount, \ in $\log_2 n$ stages", font_size=34).to_edge(UP, buff=0.3)
        x = [0, 0, 0, 1, 0, 1, 1, 1]  # bit 7 first: 00010111 = 23
        stages = []
        cur = list(x)
        rows = VGroup()
        r0 = byte_row(cur).move_to(LEFT * 2.0 + UP * 1.6)
        rows.add(r0)
        labels = VGroup(MathTex(r"x = 23", font_size=28, color=DATA).next_to(r0, LEFT, buff=0.4))
        shift = 5
        for st, d in enumerate((1, 2, 4)):
            on = (shift >> st) & 1
            if on:
                cur = cur[d:] + [0] * d
            r = byte_row(cur).move_to(LEFT * 2.0 + UP * (1.6 - 1.15 * (st + 1)))
            rows.add(r)
            labels.add(label(rf"stage {st + 1}: \ shift by {d}? \ $s_{st} = {on}$", font_size=24,
                             color=YES if on else GREY_B).next_to(r, RIGHT, buff=0.5))
        res = MathTex(r"23 \ll 5 = 736 \bmod 256 = 224 = 11100000_2", font_size=32, color=HEAD).to_edge(DOWN, buff=0.9)
        cost = note(r"each stage: \ a row of 2-to-1 multiplexers; \ 3 stages, \ 24 muxes, \ depth 3 muxes \ "
                    r"(any shift, \ same time)", font_size=22).to_edge(DOWN, buff=0.4)
        arrows = VGroup(*[Arrow(rows[k].get_bottom(), rows[k + 1].get_top(), buff=0.05, stroke_width=2.5,
                                color=CTRL, max_tip_length_to_length_ratio=0.25) for k in range(3)])
        with self.voiceover(
            "Shifting a number left by k places multiplies it by two to the k, and Pebble has instructions that shift "
            "by any amount from zero to thirty-one. Doing it one place at a time would take thirty-one steps. "
            "<bookmark mark='a'/> A barrel shifter does it in log n stages instead. Write the shift amount in binary. "
            "The first stage shifts by one, or not, according to the lowest bit; the second by two, or not; the third "
            "by four. <bookmark mark='b'/> To shift twenty-three by five, which is four plus one: shift by one, skip "
            "the two, shift by four. <bookmark mark='c'/> Each stage is a row of multiplexers, so any shift takes the "
            "same time: three multiplexers deep for eight bits, five for thirty-two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(labels[0]))
            vo.wait_until("b")
            for k in range(1, 4):
                self.play(GrowArrow(arrows[k - 1]), FadeIn(rows[k], shift=DOWN * 0.2), FadeIn(labels[k]), run_time=0.8)
            self.play(Write(res))
            vo.wait_until("c")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("blocks")
        head = label(r"Built, \ verified on every input, \ and counted", font_size=36).to_edge(UP, buff=0.35)
        hdr = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"block", r"gates", r"depth", r"as NANDs",
                                                                         r"NAND depth", r"inputs checked")])
        xs = [-6.4, -1.6, -0.2, 1.3, 2.9, 4.6]
        for h_, x in zip(hdr, xs):
            h_.move_to([x, 2.3, 0], aligned_edge=LEFT)
        rows = VGroup()
        for i, r in enumerate(d["rows"]):
            vals = [label(r["name"], font_size=24, color=CTRL), MathTex(str(r["gates"]), font_size=28),
                    MathTex(str(r["depth"]), font_size=28, color=COST), MathTex(str(r["nands"]), font_size=28),
                    MathTex(str(r["nand_depth"]), font_size=28, color=COST),
                    MathTex(f"{r['vectors']:,}".replace(",", "{,}"), font_size=26, color=YES)]
            for v, x in zip(vals, xs):
                v.move_to([x, 1.7 - 0.52 * i, 0], aligned_edge=LEFT)
            rows.add(VGroup(*vals))
        tag = note(r"every block is a netlist in \texttt{explainer/cs/pebble/hdl.py}; \ ``as NANDs'' is the same "
                   r"circuit with every gate replaced by NANDs", font_size=21).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is everything this chapter built, plus the decoder and multiplexer from chapter seven, with their "
            "costs. <bookmark mark='a'/> Each one is a netlist in this series' hardware library, simulated on every "
            "possible input and compared with its specification: for the eight-bit comparator, all sixty-five "
            "thousand pairs. <bookmark mark='b'/> The last columns rebuild each block from NAND gates only, as chapter "
            "five promised was possible: roughly twice the gates, and twice the depth. Pebble will be built from these "
            "blocks, and nothing else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:3], r[5])) for r in rows], lag_ratio=0.15), run_time=2.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(r[3], r[4])) for r in rows], lag_ratio=0.15), FadeIn(tag), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
