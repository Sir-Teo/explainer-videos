from __future__ import annotations

import math

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403


def stars_bars(counts, star_color=EVENT, size=0.34) -> VGroup:
    """Stars and bars for counts over 6 faces: each face's stars, then a bar (5 bars in all)."""
    g = VGroup()
    for f, c in enumerate(counts):
        for _ in range(c):
            g.add(Star(n=5, outer_radius=size / 2, inner_radius=size / 4.6, stroke_width=0, fill_color=star_color,
                       fill_opacity=1))
        if f < len(counts) - 1:
            g.add(Line(UP * size * 0.75, DOWN * size * 0.75, color=GREY_A, stroke_width=4))
    return g.arrange(RIGHT, buff=0.16)


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.multiply()
        self.permutations()
        self.combinations()
        self.triangle()
        self.stars()

    def card(self):
        card = chapter_card(2, r"Counting", r"How many equally likely cases are there?", lit=(1654,), part=PART)
        with self.voiceover("Chapter two. Counting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def multiply(self):
        one = dice_row(range(1, 7), size=0.46, buff=0.1).move_to([-4.6, 1.8, 0])
        l1 = MathTex(r"6", font_size=40, color=EXACT).next_to(one, DOWN, buff=0.3)
        two = outcome_grid(size=0.42, buff=0.04, dice_size=0.15).move_to([-4.6, -1.2, 0])
        l2 = MathTex(r"6 \times 6 = 36", font_size=36, color=EXACT).next_to(two, DOWN, buff=0.25)
        slabs = VGroup()
        for k in range(6):
            s = VGroup(*[Square(side_length=0.17, stroke_color=GREY_D, stroke_width=0.8, fill_color=CELL,
                                fill_opacity=1) for _ in range(36)]).arrange_in_grid(6, 6, buff=0.02)
            s.add(die_face(k + 1, 0.3).next_to(s, UP, buff=0.12))
            slabs.add(s)
        slabs.arrange_in_grid(2, 3, buff=(0.35, 0.35)).move_to([2.6, 0.6, 0])
        l3 = MathTex(r"6 \times 6 \times 6 = 216", font_size=36, color=EXACT).next_to(slabs, DOWN, buff=0.35)
        rule = theorem_card(r"the multiplication principle", r"a choice made in $m$ ways, then another in $n$ ways "
                            r"whatever the first was, \ can be made in $m \times n$ ways", color=EXACT, width=6.6,
                            font_size=23, kind=r"Rule").to_edge(DOWN, buff=0.25).shift(RIGHT * 2.6)
        with self.voiceover(
            "Classical probability turns every question into a count, so we need to count well. "
            "<bookmark mark='a'/> The first rule is multiplication. One die: six outcomes. <bookmark mark='b'/> Two "
            "dice: for each of the first die's six faces, six for the second, thirty-six pairs, a six by six grid. "
            "<bookmark mark='c'/> Three dice: six of those grids, one for each face of the third die, two hundred "
            "and sixteen. <bookmark mark='d'/> In general, if one choice can be made in m ways and then another in n "
            "ways, whatever the first was, the pair can be made in m times n ways."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, scale=0.7) for f in one], lag_ratio=0.15), FadeIn(l1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in two], lag_ratio=0.01), run_time=1.6)
            self.play(FadeIn(l2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in slabs], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(l3))
            vo.wait_until("d")
            self.play(FadeIn(rule, shift=UP * 0.2))
        self.clear_scene()

    def permutations(self):
        d = load("counting")
        cols = [PA, PB, S.LIK, S.PRIOR, S.ACCENT]
        balls = VGroup(*[Circle(radius=0.34, stroke_width=0, fill_color=c, fill_opacity=0.95) for c in cols])
        balls.arrange(RIGHT, buff=0.3).move_to([0, 2.2, 0])
        slots = VGroup(*[Line(LEFT * 0.38, RIGHT * 0.38, color=GREY_B, stroke_width=3) for _ in range(5)])
        slots.arrange(RIGHT, buff=0.3).move_to([0, 0.6, 0])
        counts = VGroup(*[MathTex(str(5 - k), font_size=34, color=EXACT).next_to(slots[k], DOWN, buff=0.25)
                          for k in range(5)])
        times = MathTex(r"5 \times 4 \times 3 \times 2 \times 1", r"=", r"5!", r"=", r"120", font_size=40)
        times.move_to([0, -1.0, 0])
        times[4].set_color(EXACT)
        digits = d["perm_52"]
        big = MathTex(r"52! = " + r"\," .join([digits[i:i + 3] for i in range(0, len(digits), 3)]), font_size=26,
                      color=EXACT).move_to([0, -2.4, 0])
        if big.width > 13.4:
            big.width = 13.4
        cap = label(rf"a {d['perm_52_digits']}-digit number: \ a well-shuffled deck is almost surely in an order "
                    r"no deck has ever been in", font_size=24, color=GREY_A).next_to(big, DOWN, buff=0.3)
        with self.voiceover(
            "Arrangements next. <bookmark mark='a'/> In how many orders can five different balls be put in a row? "
            "<bookmark mark='b'/> Five choices for the first place; whichever we chose, four left for the second; "
            "then three, two, one. <bookmark mark='c'/> Five times four times three times two times one: five "
            "factorial, a hundred and twenty. <bookmark mark='d'/> Factorials grow ferociously. A deck of "
            f"fifty-two cards can be ordered in fifty-two factorial ways, a number with {d['perm_52_digits']} "
            "digits. If every person who has ever lived had shuffled a deck every second since the universe began, "
            "they would not have made a dent in it. A well-shuffled deck is almost surely in an order no deck has "
            "ever been in."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(balls), FadeIn(slots))
            vo.wait_until("b")
            order = [2, 0, 4, 1, 3]
            for k, i in enumerate(order):
                self.play(balls[i].animate.move_to(slots[k].get_center() + UP * 0.42), FadeIn(counts[k]), run_time=0.7)
            vo.wait_until("c")
            self.play(Write(times))
            vo.wait_until("d")
            self.play(FadeIn(big, shift=UP * 0.2))
            self.play(FadeIn(cap))
        self.clear_scene()

    def combinations(self):
        d = load("counting")
        rows = [
            cmath(r"\text{ordered: }", r"n(n-1)\cdots(n-k+1)", r"=", r"\frac{n!}{(n-k)!}", font_size=38),
            cmath(r"\binom{n}{k}", r"=", r"\frac{n!}{(n-k)!\,k!}", font_size=42),
            cmath(r"\binom{49}{6}", r"=", rf"{fmt_int(d['c_49_6'])}", font_size=42),
        ]
        rows[2][2].set_color(EXACT)
        whys = [why(r"multiplication: \ $n$, then $n-1$, \dots"), why(r"each set of $k$ appears in $k!$ orders"),
                why(r"a lottery: \ choose $6$ of $49$")]
        title = label(r"Choosing $k$ of $n$, \ order ignored", font_size=36).to_edge(UP, buff=0.4)
        sets = VGroup()
        for word in ("ABC", "ACB", "BAC", "BCA", "CAB", "CBA"):
            sets.add(VGroup(*[label(ch, font_size=30, color={"A": PA, "B": PB, "C": S.LIK}[ch]) for ch in word])
                     .arrange(RIGHT, buff=0.12))
        sets.arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.75)
        br = Brace(sets, UP, color=GREY_B)
        brl = label(r"$3! = 6$ orders, \ one set $\{A, B, C\}$", font_size=26, color=GREY_A).next_to(sets, DOWN, buff=0.3)
        with self.voiceover(
            "Often order doesn't matter: a hand of cards, a committee, a lottery ticket. <bookmark mark='a'/> To "
            "choose k things from n in order, there are n choices, then n minus one, down to n minus k plus one: n "
            "factorial over n minus k factorial. <bookmark mark='b'/> But every set of k things has been counted "
            "once for each of its orders, and there are k factorial of those. <bookmark mark='c'/> Divide them out: "
            "n choose k, n factorial over n minus k factorial times k factorial. <bookmark mark='d'/> Choose six "
            f"numbers from forty-nine and there are {money(d['c_49_6'])} tickets: one chance in nearly fourteen "
            "million."
        ) as vo:
            self.play(FadeIn(title))
            step = ladder(self, rows, whys, keep=3, top=2.5, x=0.6, buff=0.42)
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.1) for s in sets], lag_ratio=0.15), FadeIn(brl))
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
        self.clear_scene()

    def triangle(self):
        d = load("counting")
        tri = d["triangle"]
        rows = VGroup()
        for n, row in enumerate(tri):
            r = VGroup(*[MathTex(str(v), font_size=24 if v < 100 else 21, color=WHITE) for v in row])
            for k, m in enumerate(r):
                m.move_to([(k - n / 2) * 0.68, 2.9 - n * 0.5, 0])
            rows.add(r)
        rows.shift(LEFT * 2.6)
        rule = cmath(r"\binom{n}{k}", r"=", r"\binom{n-1}{k-1}", r"+", r"\binom{n-1}{k}", font_size=34)
        rule.move_to([4.0, 2.7, 0])
        rw = label(r"sets with item $n$, \ and sets without it", font_size=22, color=GREY_B).next_to(rule, DOWN,
                                                                                                buff=0.2)
        pts = MathTex(r"P(\text{A wins})", r"=", r"\sum_{k \ge a} \binom{a+b-1}{k}\, 2^{-(a+b-1)}", font_size=32)
        pts.move_to([4.0, 1.15, 0])
        pts[0].set_color(PA)
        pw = label(r"A needs $a$, B needs $b$: \ play all $a + b - 1$ rounds", font_size=22, color=GREY_B)
        pw.next_to(pts, DOWN, buff=0.2)
        # the heat map: P(A wins) by points needed
        grid = load("points")["grid"]
        hm = VGroup()
        for i in range(5):
            for j in range(5):
                v = grid[i][j]
                sq = Square(side_length=0.56, stroke_width=0.8, stroke_color=GREY_D,
                            fill_color=interpolate_color(ManimColor(PB), ManimColor(PA), v), fill_opacity=0.85)
                sq.move_to([2.9 + j * 0.58, -1.05 - i * 0.58, 0])
                hm.add(VGroup(sq, MathTex(f"{v:.2f}", font_size=16, color=BLACK).move_to(sq)))
        hm_x = label(r"B needs $1, \dots, 5$", font_size=20, color=PB).next_to(hm, UP, buff=0.12)
        hm_y = label(r"A needs $1, \dots, 5$", font_size=20, color=PA).rotate(PI / 2).next_to(hm, LEFT, buff=0.12)
        with self.voiceover(
            "Arrange the counts n choose k in rows, and you get the triangle that bears Pascal's name, though it was "
            "known centuries earlier in China, India and Persia. <bookmark mark='a'/> Each entry is the sum of the "
            "two above it. <bookmark mark='b'/> Why? Fix one of the n items. The sets of k either contain it, and "
            "then choose k minus one of the rest, or don't, and choose all k from the rest. <bookmark mark='c'/> "
            "Pascal used the triangle to solve the problem of points in general. If A needs a more points and B "
            "needs b, imagine all a plus b minus one remaining rounds played, as Fermat did. A wins the match exactly "
            "when A wins at least a of them, so the answer is a sum along one row of the triangle, divided by two to "
            "that power. <bookmark mark='d'/> Our game, A needing one and B two, is row two: three of four. "
            "<bookmark mark='e'/> And here's the whole family: the chance that A wins, for every pair of points "
            "still needed, from one to five each. It's one half down the diagonal, of course, and it falls off as A "
            "needs more."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("a")
            for (n, k) in ((4, 2), (6, 3), (8, 4)):
                self.play(Indicate(rows[n - 1][k - 1], color=S.ACCENT), Indicate(rows[n - 1][k], color=S.ACCENT),
                          Indicate(rows[n][k], color=EXACT, scale_factor=1.4), run_time=0.9)
            vo.wait_until("b")
            self.play(Write(rule), FadeIn(rw))
            vo.wait_until("c")
            self.play(Write(pts), FadeIn(pw))
            vo.wait_until("d")
            self.play(rows[2][1].animate.set_color(PA), rows[2][2].animate.set_color(PA),
                      rows[2][0].animate.set_color(PB))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in hm], lag_ratio=0.03), FadeIn(hm_x), FadeIn(hm_y),
                      run_time=2.0)
        self.clear_scene()

    def stars(self):
        d = load("counting")
        examples = [((1, 1, 1, 0, 0, 0), (1, 2, 3)), ((0, 0, 2, 0, 0, 1), (3, 3, 6)), ((0, 0, 0, 0, 3, 0), (5, 5, 5))]
        title = label(r"Three dice, \ order ignored: \ how many different rolls?", font_size=34).to_edge(UP, buff=0.4)
        sb = stars_bars(examples[0][0]).move_to([-2.4, 1.4, 0])
        dice = dice_row(examples[0][1], size=0.5).next_to(sb, RIGHT, buff=1.0)
        faces_ = VGroup(*[MathTex(str(f), font_size=22, color=GREY_B) for f in range(1, 7)])
        formula = MathTex(r"\binom{3 + 6 - 1}{3}", r"=", r"\binom{8}{3}", r"=", r"56", font_size=40).move_to([0, 0.0, 0])
        formula[4].set_color(EXACT)
        fw = label(r"$3$ stars and $5$ bars in $8$ places: \ choose where the stars go", font_size=24,
                   color=GREY_B).next_to(formula, DOWN, buff=0.25)
        probs = VGroup(
            VGroup(dice_row((5, 5, 5), size=0.4), MathTex(r"\tfrac{1}{216}", font_size=32, color=EXACT)),
            VGroup(dice_row((3, 3, 6), size=0.4), MathTex(r"\tfrac{3}{216}", font_size=32, color=EXACT)),
            VGroup(dice_row((1, 2, 3), size=0.4), MathTex(r"\tfrac{6}{216}", font_size=32, color=EXACT)),
        )
        for p in probs:
            p.arrange(RIGHT, buff=0.3)
        probs.arrange(RIGHT, buff=1.0).move_to([0, -2.0, 0])
        warn = label(r"$56$ rolls, \ but \emph{not} equally likely", font_size=30, color=S.RESID).next_to(probs, DOWN,
                                                                                                         buff=0.35)
        bose = label(r"for photons they are: \ Bose and Einstein, 1924", font_size=22, color=GREY_B)
        bose.to_corner(DR, buff=0.3)
        with self.voiceover(
            "One more counting trick, and one more trap. <bookmark mark='a'/> If we ignore the order of three dice, "
            "how many different rolls are there? <bookmark mark='b'/> Write a roll as stars and bars: a star for "
            "each die, sorted into six bins by face, with five bars between the bins. One, two, three is a star in "
            "each of the first three bins. <bookmark mark='c'/> Three, three, six: two stars in bin three, one in "
            "bin six. <bookmark mark='d'/> Five, five, five: three stars in bin five. Every roll is an arrangement "
            "of three stars and five bars in eight places, so there are eight choose three of them: fifty-six. "
            "<bookmark mark='e'/> And here's the trap Galileo avoided. Fifty-six rolls, but they are not equally "
            "likely. Five, five, five happens one way in two hundred and sixteen; three, three, six three ways; one, "
            "two, three six ways. Divide by fifty-six and you get the wrong answer for real dice. <bookmark mark='f'/> "
            "Strangely, nature uses both kinds of counting. For photons, the unordered states really are equally "
            "likely: that's Bose–Einstein statistics, and lasers depend on it. Which cases are equally likely is a "
            "fact about the world, not about counting."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("b")
            self.play(FadeIn(sb), FadeIn(dice))
            for counts, roll, mark in ((examples[1][0], examples[1][1], "c"), (examples[2][0], examples[2][1], "d")):
                vo.wait_until(mark)
                self.play(Transform(sb, stars_bars(counts).move_to(sb)), Transform(dice, dice_row(roll, size=0.5)
                                                                                  .move_to(dice)))
            self.play(Write(formula), FadeIn(fw))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in probs], lag_ratio=0.3))
            self.play(FadeIn(warn))
            vo.wait_until("f")
            self.play(FadeIn(bose))
        _ = faces_
        self.clear_scene()
