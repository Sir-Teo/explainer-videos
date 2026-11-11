from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Distinct(VoiceoverScene):
    def construct(self):
        self.card()
        self.zeros()
        self.registers()
        self.measured()

    def card(self):
        card = chapter_card(11, r"Counting distinct things: \ HyperLogLog", r"How many different words, \ with small registers?",
                            lit=(1985, 2007), extra=((1985, r"Flajolet--Martin"), (2007, r"HyperLogLog")), part=PART)
        with self.voiceover((
            'Chapter eleven. Counting distinct things: HyperLogLog.'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def zeros(self):
        head = label(r"A coin-flip record", font_size=34).to_edge(UP, buff=0.35)
        ex = [("whale", "0001011010110"), ("the", "1011100101001"), ("ishmael", "0100111010010"),
              ("harpoon", "0000001101011"), ("sea", "0010110100111")]
        rows = VGroup()
        for w, bits in ex:
            z = len(bits) - len(bits.lstrip("0"))
            b = VGroup(*[mono(c, 20, NO if i < z else (YES if i == z else GREY_B)) for i, c in enumerate(bits)]
                       ).arrange(RIGHT, buff=0.06)
            rows.add(VGroup(label(rf"\texttt{{{w}}}", font_size=22, color=DATA), b,
                            label(rf"rank {z + 1}", font_size=20, color=HEAD)))
        for r in rows:
            r[0].move_to([-4.4, 0, 0])
            r[1].move_to([0.0, 0, 0])
            r[2].move_to([3.6, 0, 0])
        rows.arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[0].set_x(-4.4)
            r[1].set_x(0.0)
            r[2].set_x(3.6)
        facts = VGroup(
            label(r"hash each item to random-looking bits; \ \textbf{repeats hash the same}, \ so they change nothing",
                  font_size=21, color=WHITE),
            label(r"$\rho - 1$ zeros followed by 1 has probability $2^{-\rho}$ in the ideal model; \ scale: "
                  r"$2^\rho$ distinct items", font_size=21, color=WHITE),
            label(r"finite hashes: \ store the maximum rank; \ collisions and saturation limit the range",
                  font_size=21, color=YES),
            label(r"but one record is noisy: \ off by a factor of 2 or 4 is common", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            (
            'How many different words are in the novels? An exact general-purpose set can grow with the distinct '
            "items. <bookmark mark='a'/> Flajolet and Martin proposed a much smaller randomized summary in 1985: "
            'hash each item to random-looking bits and examine its leading zeros. Repeated items reuse their hash '
            "and do not change the maximum. <bookmark mark='b'/> In an ideal independent-bit model, a rank of rho, "
            'meaning rho minus one zeros followed by a one, has probability two to the minus rho. The largest '
            "observed rank therefore gives a noisy scale for cardinality. <bookmark mark='c'/> Remember the largest "
            'rank. Its storage is logarithmic in the hash bit width; finite hashes eventually saturate and collide. '
            "Five bits do not cover every possible stream. <bookmark mark='d'/> A single extreme hash makes the "
            'estimate unstable, so we use many registers.'
        )
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25))
            for mk, f in zip("abcd", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f))
        self.wait(0.3)
        self.clear_scene()

    def registers(self):
        d = load("hll")
        reg = d["registers64"]
        head = label(r"HyperLogLog: \ many registers, \ one harmonic mean", font_size=34).to_edge(UP, buff=0.35)
        bars = VGroup()
        for i, v in enumerate(reg):
            b = Rectangle(width=0.09, height=v * 0.12, stroke_width=0, fill_color=LAM, fill_opacity=0.85)
            b.move_to([-6.3 + i * 0.118, -0.8 + b.height / 2, 0])
            bars.add(b)
        cap = label(r"64 registers on the novels' vocabulary: \\ the first 6 bits choose a register, \\ the rest give "
                    r"the rank", font_size=19, color=GREY_A).next_to(bars, DOWN, buff=0.2)
        side = VGroup(
            MathTex(r"E = \alpha_m\, m^2 \Big(\sum_{j=1}^{m} 2^{-M_j}\Big)^{-1}", font_size=36, color=YES),
            label(r"the harmonic mean tames the lucky registers", font_size=20, color=GREY_A),
            MathTex(r"\text{relative standard error} \approx \frac{1.04}{\sqrt{m}}", font_size=34, color=HEAD),
            label(r"Flajolet, \ Fusy, \ Gandouet and Meunier, \ 2007", font_size=18, color=GREY_B),
            label(r"few items: \ count the empty registers instead \ (linear counting)", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.28)
        if side.width > 5.4:
            side.width = 5.4
        side.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        with self.voiceover(
            (
            "The cure uses many registers. <bookmark mark='a'/> The leading hash bits choose one of m registers. "
            'Store the largest rank of the remaining suffix in that register. Here are sixty-four registers after '
            "hashing the novel vocabulary. <bookmark mark='b'/> HyperLogLog, from Flajolet and colleagues in 2007, "
            "combines powers of those ranks through a bias-corrected harmonic estimate. <bookmark mark='c'/> The "
            'familiar one point zero four over root m is a leading relative standard-error scale under the hashing '
            "model, not a guaranteed relative-error interval. <bookmark mark='d'/> When many registers are zero, our"
            ' implementation switches to the small-range empty-register correction. The actual register vector is '
            'checked against an independent scalar implementation.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(cap))
            vo.wait_until("a")
            self.play(Indicate(bars, color=LAM))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        d = load("hll")
        head = label(rf"Measured: \ {words(d['distinct'])} distinct words, \ 30 hash functions", font_size=32
                     ).to_edge(UP, buff=0.35)
        rows = [[str(r["m"]), (f"{r['bytes']:.0f} B" if r["bytes"] < 1024 else f"{r['bytes'] / 1024:.0f} KiB"),
                 f"{r['rmse'] * 100:.1f}\\%", f"{r['theory'] * 100:.1f}\\%"] for r in d["rows"]]
        tab = grid_table([r"registers $m$", r"packed model", r"30-seed RMSE", r"$1.04/\sqrt{m}$"], rows,
                         widths=[2.4, 2.0, 2.8, 2.4], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[LAM, GREY_A, YES, HEAD]] * len(rows)).next_to(head, DOWN, buff=0.4)
        big_ = VGroup(
            label(rf"the whole corpus, \ {words(d['words'])} words, \ $m = 4096$ \ (3 KiB packed model): \ estimate "
                  rf"{words(round(d['est_corpus']))}", font_size=21, color=YES),
            label(rf"every five-word phrase: \ {words(d['true_shingles'])} distinct, \ estimate "
                  rf"{words(round(d['est_shingles']))}, \ same modeled registers", font_size=21, color=YES),
            label(r"actual NumPy registers: \ 32 KiB at $m=4096$; \ excludes input, hashes and interpreter", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            f"We ran thirty fixed hash seeds per register count on the novel vocabulary. <bookmark mark='a'/> The "
            f'table compares empirical root-mean-square error with the leading standard-error formula. Three '
            f'kibibytes for 4096 registers means a modeled six-bit packed representation. The actual NumPy array uses'
            f" thirty-two kibibytes, eight bytes per register, excluding the input and hashes. <bookmark mark='b'/> "
            f'On the complete word stream, the estimate was '
            f"{words(round(d['est_corpus']))}"
            f' against '
            f"{words(d['distinct'])}"
            f" distinct words. <bookmark mark='c'/> The five-word-shingle run uses the same modeled register storage;"
            f' its error and exact reference are shown separately. Neither this result nor thirty seeds certifies a '
            f"confidence guarantee. <bookmark mark='d'/> Database engines use carefully engineered variants to trade "
            f'precision for storage in approximate count-distinct queries.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25))
            vo.wait_until("a")
            self.play(*[Indicate(tab.cells[r][2], color=YES) for r in range(1, len(rows) + 1)])
            vo.wait_until("b")
            self.play(FadeIn(big_[0]))
            vo.wait_until("c")
            self.play(FadeIn(big_[1]))
            vo.wait_until("d")
            self.play(FadeIn(big_[2]))
        self.wait(0.3)
        self.clear_scene()
