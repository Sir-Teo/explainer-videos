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
        card = chapter_card(11, r"Counting distinct things: \ HyperLogLog", r"How many different words, \ in 3 KB?",
                            lit=(1985, 2007), extra=((1985, r"Flajolet--Martin"), (2007, r"HyperLogLog")), part=PART)
        with self.voiceover("Chapter eleven. Counting distinct things: HyperLogLog."):
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
            label(r"a run of $\rho - 1$ leading zeros has probability $2^{-\rho}$: \ to see one, \ you need about "
                  r"$2^\rho$ distinct items", font_size=21, color=WHITE),
            label(r"remember only the largest rank seen: \ $\log_2 \log_2 n$ bits \ (Flajolet and Martin, 1985)",
                  font_size=21, color=YES),
            label(r"but one record is noisy: \ off by a factor of 2 or 4 is common", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How many different words are in the novels? Counting them exactly means remembering them all. "
            "<bookmark mark='a'/> Philippe Flajolet and Nigel Martin had a better idea in 1985. Hash each word to "
            "a string of random-looking bits, and look at how many zeros it starts with. A repeated word hashes "
            "the same way every time, so repeats change nothing. <bookmark mark='b'/> A hash that starts with "
            "rho minus one zeros and then a one has probability two to the minus rho. Seeing one is like "
            "flipping that many heads in a row: you need about two to the rho different items before it "
            "happens. <bookmark mark='c'/> So remember only the largest rank you have seen. That takes about log "
            "log n bits, five bits for any number of words you will ever meet. <bookmark mark='d'/> But a single "
            "record is noisy. One lucky hash, and the estimate doubles."
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
            MathTex(r"\text{relative error} \approx \frac{1.04}{\sqrt{m}}", font_size=34, color=HEAD),
            label(r"Flajolet, \ Fusy, \ Gandouet and Meunier, \ 2007", font_size=18, color=GREY_B),
            label(r"few items: \ count the empty registers instead \ (linear counting)", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.28)
        if side.width > 5.4:
            side.width = 5.4
        side.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        with self.voiceover(
            "The cure is to average many records. <bookmark mark='a'/> Use the first few bits of each hash to "
            "choose one of m registers, and keep in each register the largest rank of the hashes sent to it. "
            "Here are sixty-four registers after the whole vocabulary of the novels. <bookmark mark='b'/> "
            "Philippe Flajolet and his colleagues combined them, in 2007, with a harmonic mean, which isn't fooled "
            "by a few lucky registers, times a constant that corrects the bias. <bookmark mark='c'/> The relative "
            "error is about one point zero four over the square root of m. <bookmark mark='d'/> When there are "
            "few items and many registers are still empty, it counts the empty ones instead."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(cap))
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
        rows = [[str(r["m"]), (f"{r['bytes']:.0f} B" if r["bytes"] < 1024 else f"{r['bytes'] / 1024:.0f} KB"),
                 f"{r['rmse'] * 100:.1f}\\%", f"{r['theory'] * 100:.1f}\\%"] for r in d["rows"]]
        tab = grid_table([r"registers $m$", r"memory", r"measured error", r"$1.04/\sqrt{m}$"], rows,
                         widths=[2.4, 2.0, 2.8, 2.4], row_h=0.42, font_size=20, mono_cols=(),
                         colors=[[LAM, GREY_A, YES, HEAD]] * len(rows)).next_to(head, DOWN, buff=0.4)
        big_ = VGroup(
            label(rf"the whole corpus, \ {words(d['words'])} words, \ $m = 4096$ \ (3 KB): \ estimate "
                  rf"{words(round(d['est_corpus']))}", font_size=21, color=YES),
            label(rf"every five-word phrase: \ {words(d['true_shingles'])} distinct, \ estimate "
                  rf"{words(round(d['est_shingles']))}, \ the same 3 KB", font_size=21, color=YES),
            label(r"in practice: \ Redis's \texttt{PFCOUNT}, \ BigQuery's \texttt{APPROX\_COUNT\_DISTINCT}, \ "
                  r"Presto, \ Druid", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "We ran HyperLogLog on the novels' vocabulary with thirty different hash functions for each number of "
            "registers. <bookmark mark='a'/> The measured error follows one point zero four over root m down the "
            "table: sixteen registers, a quarter off; four thousand, one and a half percent, in three "
            "kilobytes. <bookmark mark='b'/> On the whole stream of four point six million words, the estimate was "
            f"{words(round(d['est_corpus']))} against the true {words(d['distinct'])}. <bookmark mark='c'/> And on "
            "every five-word phrase in the novels, four and a half million distinct ones, the same three kilobytes "
            "were off by half a percent. An exact count would need a table of tens of megabytes. <bookmark "
            "mark='d'/> This is why databases and analytics engines answer count distinct queries approximately, "
            "with HyperLogLog behind them."
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
