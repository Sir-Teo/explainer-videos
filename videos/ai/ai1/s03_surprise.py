from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import (ALPHA27, letter_row, load, plain_axes, polyline, surprise_color,
                                  surprise_legend, wrap_words)


class Surprise(VoiceoverScene):
    def construct(self):
        self.card()
        self.intuition()
        self.rules()
        self.derive()
        self.curve()
        self.halvings()
        self.skyline()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"How surprised to be",
                            r"If something had probability $p$, how much did seeing it tell you?", lit=(1948,), part=1)
        with self.voiceover("Chapter two. How surprised should you be?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def intuition(self):
        lt = load("letters")
        bg = load("bigram")
        p = lt["p"]
        pe, pz = float(p[ALPHA27.index("e")]), float(p[ALPHA27.index("z")])
        pu = float(bg["q_u"])
        line = NumberLine(x_range=[0, 1, 0.1], length=12, color=GREY_C, include_numbers=False).shift(DOWN * 0.6)
        ends = VGroup(MathTex("0", font_size=30, color=GREY_B).next_to(line.n2p(0), DOWN, buff=0.25),
                      MathTex("1", font_size=30, color=GREY_B).next_to(line.n2p(1), DOWN, buff=0.25))
        head = label(r"how likely it was \ $\longrightarrow$ \ how much it tells you", font_size=34).to_edge(UP, buff=0.5)
        events = [
            (pu, r"\texttt{u} after \texttt{q}", r"no news", 1),
            (0.5, r"a coin lands heads", r"a little", 1),
            (pe, r"the next letter is \texttt{e}", r"some", -1),
            (pz, r"the next letter is \texttt{z}", r"a lot", 1),
        ]
        marks = VGroup()
        for v, name, how, side in events:
            d = Dot(line.n2p(v), radius=0.08, color=C.SURPRISE)
            t = label(name, font_size=24, color=WHITE)
            h = label(how, font_size=22, color=C.SURPRISE)
            g = VGroup(t, h).arrange(DOWN, buff=0.08)
            g.next_to(d, UP if side > 0 else DOWN, buff=0.35 if side > 0 else 0.6)
            stem = Line(d.get_center(), g.get_bottom() if side > 0 else g.get_top(), color=GREY_D, stroke_width=1.5)
            marks.add(VGroup(d, stem, g))
        # keep the two labels near p = 0 apart
        marks[3][2].shift(RIGHT * 0.6)
        marks[2][2].shift(RIGHT * 0.5)
        with self.voiceover(
            "If you were sure something would happen, seeing it happen tells you nothing. <bookmark mark='a'/> u "
            "after q: no news. <bookmark mark='b'/> A coin landing heads tells you a little. <bookmark mark='c'/> "
            "A letter e, a bit more. <bookmark mark='d'/> And a z, which turns up about once in two thousand "
            "symbols, tells you a lot. The less likely something was, the more you learn when it happens."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ends))
            for k, mark in enumerate("abcd"):
                vo.wait_until(mark)
                self.play(FadeIn(marks[k], shift=UP * 0.1), run_time=0.7)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        head = label(r"What should the surprise $s(p)$ of an event with probability $p$ be?", font_size=34)
        head.to_edge(UP, buff=0.45)
        items = [
            (r"1.\ \ it depends only on $p$", WHITE),
            (r"2.\ \ the less likely, the more surprising: \ $s$ decreases, \ $s(1) = 0$", WHITE),
            (r"3.\ \ for independent events, surprises add: \ $s(pq) = s(p) + s(q)$", C.BITS),
            (r"4.\ \ small changes in $p$ make small changes in $s$: \ $s$ is continuous", WHITE),
        ]
        rows = VGroup(*[label(t, font_size=30, color=c) for t, c in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        rows.next_to(head, DOWN, buff=0.55)
        # independent events: a coin and a die
        coin = VGroup(Circle(radius=0.38, color=C.TRUE_P, stroke_width=3), MathTex(r"H", font_size=30, color=C.TRUE_P))
        die = VGroup(RoundedRectangle(width=0.78, height=0.78, corner_radius=0.1, color=C.TRUE_P, stroke_width=3))
        for dx, dy in ((-0.2, 0.2), (0.2, -0.2), (0, 0), (-0.2, -0.2), (0.2, 0.2)):
            die.add(Dot([dx, dy, 0], radius=0.055, color=C.TRUE_P))
        pair = VGroup(coin, MathTex(r"\text{and}", font_size=28, color=GREY_B), die).arrange(RIGHT, buff=0.35)
        eq = mtex(r"P = \tfrac12 \times \tfrac16 = \tfrac1{12} \qquad s\!\left(\tfrac1{12}\right) = "
                  r"s\!\left(\tfrac12\right) + s\!\left(\tfrac16\right)", font_size=34, color=C.BITS)
        VGroup(pair, eq).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Let's turn that into mathematics. Call the surprise of an event with probability p, s of p. What "
            "should s be? <bookmark mark='a'/> Shannon asked for a few modest things. It should depend only on p. "
            "<bookmark mark='b'/> It should go down as p goes up, and a certain event should be no surprise at all. "
            "<bookmark mark='c'/> For independent events, surprises should add: <bookmark mark='d'/> a coin landing "
            "heads and a die showing five, together, should be exactly as surprising as each one, added up. "
            "<bookmark mark='e'/> And small changes in p should make small changes in s."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark in enumerate("abc"):
                vo.wait_until(mark)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(pair), Write(eq))
            vo.wait_until("e")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        head = label(r"Only one function does all that", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            mtex([r"g(x)", r"=", r"s\!\left(2^{-x}\right)"]),
            mtex([r"g(x + y)", r"=", r"g(x) + g(y)"]),
            mtex([r"g(n)", r"=", r"n\, g(1)"]),
            mtex([r"g\!\left(\tfrac{m}{n}\right)", r"=", r"\tfrac{m}{n}\, g(1)"]),
            mtex([r"g(x)", r"=", r"x\, g(1)"]),
            mtex([r"s(p)", r"=", r"g(1)\, \log_2 \tfrac{1}{p}"], font_size=44),
        ]
        whys = [why(r"measure $p$ in halvings: \ $p = 2^{-x}$"),
                why(r"rule 3, with $p = 2^{-x}$, $q = 2^{-y}$"),
                why(r"add $1$ to itself $n$ times"),
                why(r"$n\, g(\tfrac mn) = g(m) = m\, g(1)$"),
                why(r"for every real $x \ge 0$: \ rule 4 (continuity)"),
                why(r"put $x = \log_2 \tfrac1p$ back")]
        step = ladder(self, rows, whys, keep=6, top=2.55, buff=0.36)
        with self.voiceover(
            "Remarkably, those rules leave only one choice. Measure probabilities in halvings: <bookmark mark='a'/> "
            "write p as two to the minus x, and let g of x be the surprise of that event. <bookmark mark='b'/> Rule "
            "three says g turns sums into sums. <bookmark mark='c'/> So g of n is n times g of one, for every whole "
            "number n, <bookmark mark='d'/> and the same holds for every fraction. <bookmark mark='e'/> Continuity "
            "fills in the numbers between the fractions, so g of x is x times g of one, for every x."
        ) as vo:
            self.play(FadeIn(head))
            for k, mark in enumerate("abcde"):
                vo.wait_until(mark)
                step(k)
        unit = mtex(r"s(p) = \log_2 \frac{1}{p} \ \text{bits}", font_size=50, color=C.SURPRISE)
        box = SurroundingRectangle(unit, color=C.SURPRISE, buff=0.25, corner_radius=0.1)
        res = VGroup(unit, box).move_to(DOWN * 1.2)
        cap = label(r"one bit $=$ the surprise of a fair coin: \ $s(\tfrac12) = 1$", font_size=26, color=GREY_A)
        cap.next_to(res, UP, buff=0.3)
        with self.voiceover(
            "Put the probability back in, and the surprise must be a constant times the log of one over p. "
            "<bookmark mark='a'/> The constant just picks a unit. Choose it so that a fair coin flip carries "
            "exactly one unit, and call that unit a bit. The surprise of an event with probability p is log, base "
            "two, of one over p, bits."
        ) as vo:
            step(5)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(*rows[:5], *whys[:5])), VGroup(rows[5], whys[5]).animate.move_to(UP * 1.4))
            self.play(FadeIn(cap), Write(unit), Create(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        lt = load("letters")
        bg = load("bigram")
        p = lt["p"]
        ax = plain_axes([0, 1, 0.25], [0, 12, 2], 9.0, 5.2).shift(DOWN * 0.3 + LEFT * 0.4)
        xl = VGroup(*[MathTex(t, font_size=26, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.15)
                      for t, v in (("0", 0), ("0.5", 0.5), ("1", 1))])
        yl = VGroup(*[MathTex(str(v), font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                      for v in (0, 4, 8, 12)])
        axl = VGroup(MathTex("p", font_size=32, color=GREY_A).next_to(ax.c2p(1, 0), RIGHT, buff=0.2),
                     label(r"$s(p)$, bits", font_size=26, color=GREY_A).next_to(ax.c2p(0, 12), UP, buff=0.15))
        xs = np.concatenate([np.geomspace(2 ** -12, 0.05, 200), np.linspace(0.05, 1, 200)])
        curve = polyline(ax, xs, -np.log2(xs), color=C.SURPRISE, stroke_width=4)
        pts = [
            (0.5, r"coin: \ $1$ bit", 1.0),
            (1 / 6, r"a die: \ $2.58$", 2.585),
            (float(p[ALPHA27.index("e")]), r"\texttt{e}: \ $3.32$", None),
            (float(p[ALPHA27.index("z")]), r"\texttt{z}: \ $10.9$", None),
            (float(bg["q_u"]), r"\texttt{u} after \texttt{q}: \ $0.002$", None),
        ]
        assert abs(-math.log2(pts[2][0]) - 3.32) < 0.01 and abs(-math.log2(pts[3][0]) - 10.9) < 0.05
        assert -math.log2(pts[4][0]) < 0.0025
        dots = VGroup()
        for v, t, _ in pts:
            d = Dot(ax.c2p(v, -math.log2(v)), radius=0.07, color=WHITE)
            lab = label(t, font_size=24).next_to(d, UR, buff=0.08)
            dots.add(VGroup(d, lab))
        dots[4][1].next_to(dots[4][0], UP, buff=0.25).shift(LEFT * 0.5)
        dots[3][1].next_to(dots[3][0], RIGHT, buff=0.2)
        with self.voiceover(
            "Here's that function. <bookmark mark='a'/> A coin: one bit. A face of a die: 2.58 bits. "
            "<bookmark mark='b'/> The letter e: 3.32 bits. The letter z: almost eleven. <bookmark mark='c'/> And u, "
            "right after q, carries two thousandths of a bit: almost nothing. <bookmark mark='d'/> As p heads to "
            "zero, the surprise grows without limit."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl))
            self.play(Create(curve), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(dots[0]), FadeIn(dots[1]))
            vo.wait_until("b")
            self.play(FadeIn(dots[2]), FadeIn(dots[3]))
            vo.wait_until("c")
            self.play(FadeIn(dots[4]))
            vo.wait_until("d")
            self.play(Indicate(curve, color=C.BITS), run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def halvings(self):
        head = label(r"A bit is a halving", font_size=38).to_edge(UP, buff=0.4)
        W = 12.0
        frame = Rectangle(width=W, height=0.5, stroke_width=1.5, stroke_color=GREY_C).move_to(UP * 1.6)
        bar = Rectangle(width=W, height=0.5, stroke_width=0, fill_color=C.BITS, fill_opacity=0.95).move_to(UP * 1.6)
        lo, w = 0.0, 1.0
        rng = np.random.default_rng(11)
        choices = rng.integers(0, 2, 10)
        y = 1.6
        segs = VGroup()
        for k, c in enumerate(choices):
            w /= 2
            lo += w * c
            seg = Rectangle(width=max(W * w, 0.006), height=0.5, stroke_width=0, fill_color=C.BITS, fill_opacity=0.95)
            seg.move_to([-W / 2 + (lo + w / 2) * W, y, 0])
            segs.add(seg)
        bits = VGroup(*[MathTex(str(int(c)), font_size=34, color=C.BIT1 if c else C.BIT0) for c in choices])
        bits.arrange(RIGHT, buff=0.3).move_to(DOWN * 0.3)
        count = MathTex(r"10 \text{ halvings}: \ p = 2^{-10} = \tfrac{1}{1024} \ \Longrightarrow \ s = 10 \text{ bits}",
                        font_size=36).move_to(DOWN * 1.6)
        cap = label(r"each yes-or-no answer that halves the possibilities is one bit", font_size=26, color=GREY_A)
        cap.to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Bits have a concrete meaning. Take the whole range of possibilities, and halve it: <bookmark mark='a'/> "
            "left or right, zero or one. Halve what's left, and again, ten times. <bookmark mark='b'/> You've "
            "narrowed things down to one part in 1024, an event of probability two to the minus ten, and the "
            "surprise of seeing it is ten bits. Each yes-or-no answer that halves the possibilities is one bit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bar), Create(frame))
            vo.wait_until("a")
            for k in range(10):
                self.play(Transform(bar, segs[k]), FadeIn(bits[k]), run_time=0.45)
            arrow = Arrow(segs[-1].get_center() + DOWN * 1.0 + RIGHT * 0.6, segs[-1].get_bottom(), buff=0.05,
                          color=C.BITS, stroke_width=3, max_tip_length_to_length_ratio=0.25)
            what = label(r"$\tfrac{1}{1024}$ of the bar", font_size=24, color=C.BITS).next_to(arrow.get_start(), DOWN,
                                                                                         buff=0.08)
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(what))
            self.play(Write(count))
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def skyline(self):
        g = load("game")
        sent, bits = g["sentence"], np.asarray(g["sentence_bits"])
        total = float(bits.sum())
        k = int(g["sentence_order"])
        assert abs(total - 182.2) < 0.1 and len(sent) == 101 and k == 5
        lines = wrap_words(sent, 36)
        rows = VGroup(*[letter_row(ln, font_size=27) for ln in lines]).arrange(DOWN, aligned_edge=LEFT, buff=1.5)
        rows.move_to(DOWN * 0.95)
        bars, i = VGroup(), 0
        for t, ln in zip(rows, lines):
            top = t.get_top()[1] + 0.08
            for j in range(len(ln)):
                b = float(bits[i])
                h = max(0.02, 0.115 * b)
                bars.add(Rectangle(width=0.2, height=h, stroke_width=0, fill_color=surprise_color(b), fill_opacity=1)
                         .move_to([t[j].get_x(), top + h / 2, 0]))
                i += 1
        letters = [m for t in rows for m in t]
        rule = mtex(r"\log_2 \frac{1}{P(x_1 \dots x_n)} = \sum_i \log_2 \frac{1}{P(x_i \mid x_{<i})}", font_size=38)
        rule.to_edge(UP, buff=0.35)
        tot = label(rf"total: \ ${total:.0f}$ bits for ${len(sent)}$ symbols \ $=$ \ ${total / len(sent):.2f}$ bits "
                    r"per symbol", font_size=30, color=C.BITS).to_edge(DOWN, buff=0.35)
        leg = surprise_legend(width=3.0).to_corner(DR, buff=0.4).shift(UP * 0.5)
        src = note(rf"each letter's surprise given the previous {k} letters, under a counting model of the $30$ books "
                   r"(Chapter 7); \ computed").next_to(rule, DOWN, buff=0.2)
        with self.voiceover(
            "And because logs turn products into sums, the chain rule turns into something lovely. "
            "<bookmark mark='a'/> The surprise of a whole text is the sum of the surprises of its symbols, each "
            "given everything before it. <bookmark mark='b'/> Here is Shannon's sentence again, with each letter's "
            "surprise drawn as a bar, as judged by a model that knows only the previous five letters."
        ) as vo:
            self.play(Write(rule))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in letters], lag_ratio=0.02), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02), FadeIn(leg), run_time=3)
        starts = np.array([i == 0 or sent[i - 1] == " " for i in range(len(sent))])
        assert bits[starts].mean() > 2 * bits[~starts].mean()  # the surprise is at the starts of words
        with self.voiceover(
            "The tall bars are where the text surprised the model: the starts of words, and words it didn't "
            "expect. <bookmark mark='a'/> Altogether, 182 bits for 101 symbols: 1.8 bits per symbol, under half of "
            "what the letter frequencies alone would give. Remember that number; it's how we'll keep score."
        ) as vo:
            self.play(*[Indicate(bars[j], color=WHITE, scale_factor=1.3) for j in range(len(sent)) if bits[j] > 4.4],
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(tot, shift=UP * 0.1))
        self.wait(0.5)
        self.clear_scene()
