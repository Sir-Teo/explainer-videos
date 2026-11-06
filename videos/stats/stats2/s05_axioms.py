from __future__ import annotations

from itertools import permutations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

A_COL, B_COL = PA, PB


class Axioms(VoiceoverScene):
    def construct(self):
        self.card()
        self.kolmogorov()
        self.consequences()
        self.mere_again()
        self.hats()
        self.series()
        self.continuity()

    def card(self):
        card = chapter_card(4, r"Kolmogorov's axioms", r"Three rules from which everything else follows",
                            lit={1933: "Kolmogorov's axioms"}, part=PART)
        with self.voiceover("Chapter four. Kolmogorov's axioms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def kolmogorov(self):
        hc = history_card(1933, r"Andrey Kolmogorov, aged 30: \ \emph{Grundbegriffe der "
                          r"Wahrscheinlichkeitsrechnung}", r"Hilbert's sixth problem (1900) had asked for axioms of "
                          r"probability; \ Kolmogorov built them on measure theory", color=S.MUSEUM, width=6.0,
                          font_size=22).to_corner(UL, buff=0.35)
        sq = Square(side_length=3.6, stroke_color=GREY_A, stroke_width=2.5, fill_color=CELL, fill_opacity=1)
        sq.move_to([-3.4, -1.2, 0])
        om = MathTex(r"\Omega", font_size=40, color=GREY_A).next_to(sq, UP, buff=0.12).align_to(sq, LEFT)
        ev = Ellipse(width=1.9, height=1.3, stroke_color=EVENT, stroke_width=2, fill_color=EVENT,
                     fill_opacity=0.4).move_to(sq.get_center() + np.array([-0.4, 0.4, 0]))
        evl = MathTex(r"A", font_size=34, color=EVENT).move_to(ev)
        area = label(r"$P(A)$: \ its area, \ when $\Omega$ has area $1$", font_size=24, color=EVENT)
        area.next_to(sq, DOWN, buff=0.25)
        dfn = definition_card(r"Probability space $(\Omega, \mathcal F, P)$",
                              r"$\Omega$: the outcomes. \ $\mathcal F$: the events, closed under complements and "
                              r"countable unions. \ $P$: a number for each event, with", color=EXACT, width=6.4,
                              font_size=23).move_to([3.6, 1.1, 0])
        axs = VGroup(
            MathTex(r"\text{1.}\ \ P(A) \ge 0", font_size=32),
            MathTex(r"\text{2.}\ \ P(\Omega) = 1", font_size=32),
            MathTex(r"\text{3.}\ \ P\Big(\bigcup_{i} A_i\Big) = \sum_i P(A_i)", r"\ \ \text{for disjoint } A_1, A_2, \dots",
                    font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(dfn, DOWN, buff=0.35)
        axs[2][1].set_color(GREY_B).scale(0.8)
        foot = note(r"why not every subset? \ some sets cannot be sized consistently (Vitali 1905): \ Part 43")
        if foot.width > 7.0:
            foot.width = 7.0
        foot.move_to([3.3, -3.55, 0])
        with self.voiceover(
            "Bertrand's paradox showed that at random has to be defined. In 1933 Andrey Kolmogorov, thirty years "
            "old, defined it. <bookmark mark='a'/> In 1900 David Hilbert had listed the axioms of probability among "
            "the great open problems. Kolmogorov's answer was to treat probability like area. <bookmark mark='b'/> "
            "Take a square of area one: that's omega, the set of all outcomes. An event is a region in it, "
            "<bookmark mark='c'/> and its probability is its area. <bookmark mark='d'/> Formally, a probability "
            "space has three parts: the outcomes; a collection of events, which must include complements and "
            "countable unions of events; and the probability itself, which obeys three rules. <bookmark mark='e'/> "
            "Probabilities are never negative. <bookmark mark='f'/> The whole space has probability one. "
            "<bookmark mark='g'/> And for events that don't overlap, the probability of their union is the sum of "
            "their probabilities, even for infinitely many of them. <bookmark mark='h'/> Why not let every set of "
            "outcomes be an event? Because on a continuum some sets can't be given a size at all without "
            "contradiction. That's a story for Part 43. Everything in this part uses only the three rules."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(sq), FadeIn(om))
            vo.wait_until("c")
            self.play(FadeIn(ev), FadeIn(evl), FadeIn(area))
            vo.wait_until("d")
            self.play(FadeIn(dfn, shift=LEFT * 0.2))
            for k, m in zip(range(3), "efg"):
                vo.wait_until(m)
                self.play(FadeIn(axs[k], shift=RIGHT * 0.2))
            vo.wait_until("h")
            self.play(FadeIn(foot))
        self.clear_scene()

    def consequences(self):
        sq = Square(side_length=3.8, stroke_color=GREY_A, stroke_width=2.5, fill_color=CELL, fill_opacity=1)
        sq.move_to([-4.0, -0.4, 0])
        ca = Circle(radius=1.05, stroke_color=A_COL, stroke_width=2.5).move_to(sq.get_center() + LEFT * 0.55)
        cb = Circle(radius=1.05, stroke_color=B_COL, stroke_width=2.5).move_to(sq.get_center() + RIGHT * 0.55)
        fa = ca.copy().set_fill(A_COL, opacity=0.35).set_stroke(width=0)
        fb = cb.copy().set_fill(B_COL, opacity=0.35).set_stroke(width=0)
        la = MathTex(r"A", font_size=32, color=A_COL).move_to(ca.get_center() + LEFT * 0.5)
        lb = MathTex(r"B", font_size=32, color=B_COL).move_to(cb.get_center() + RIGHT * 0.5)
        complement = Difference(sq, ca, stroke_width=0, fill_color=B_COL, fill_opacity=0.3)
        ac_label = MathTex(r"A^c", font_size=30, color=B_COL).move_to(sq.get_center() + DR * 1.35)
        inside = Circle(radius=0.72, stroke_color=A_COL, stroke_width=2.5,
                        fill_color=A_COL, fill_opacity=0.35).move_to(sq.get_center() + LEFT * 0.3)
        outside = Circle(radius=1.5, stroke_color=B_COL, stroke_width=2.5,
                         fill_color=B_COL, fill_opacity=0.2).move_to(sq)
        nested = VGroup(outside, inside,
                        MathTex("A", font_size=32, color=A_COL).move_to(inside),
                        MathTex("B", font_size=32, color=B_COL).move_to(sq.get_center() + RIGHT * 1.1))
        lens = Intersection(ca, cb, stroke_width=0, fill_color=WHITE, fill_opacity=0.55)
        twice = label(r"counted twice", font_size=22, color=WHITE).next_to(sq, DOWN, buff=0.2)
        rows = [
            cmath(r"P(A^c)", r"=", r"1 - P(A)", font_size=36),
            cmath(r"A \subseteq B", r"\Rightarrow", r"P(A) \le P(B)", font_size=36),
            cmath(r"P(A \cup B)", r"=", r"P(A) + P(B) - P(A \cap B)", font_size=36),
            cmath(r"P\Big(\bigcup_i A_i\Big)", r"\le", r"\sum_i P(A_i)", font_size=36),
        ]
        whys = [why(r"$A$, $A^c$ disjoint; \ union is $\Omega$"), why(r"$P(B) = P(A) + P(B \setminus A)$"),
                why(r"the overlap is counted twice"), why(r"the union bound: \ overlaps only help")]
        with self.voiceover(
            "From three rules, everything else follows. <bookmark mark='a'/> An event and its complement don't "
            "overlap and together make up everything, so their probabilities add to one: the chance that A doesn't "
            "happen is one minus the chance that it does. <bookmark mark='b'/> If A is inside B, then B is A plus "
            "the part of B outside A, so B is at least as probable. <bookmark mark='c'/> For two events that do "
            "overlap, add their probabilities, and the overlap has been counted twice, <bookmark mark='d'/> so "
            "subtract it once: <bookmark mark='e'/> the probability of A or B is P of A plus P of B minus P of A and "
            "B. <bookmark mark='f'/> Drop the subtraction and you get an inequality that holds for any events at "
            "all: the probability that at least one happens is at most the sum of their probabilities. It's called "
            "the union bound, it's crude, and it will hold up a surprising amount of this series, from multiple "
            "testing to learning theory."
        ) as vo:
            self.play(FadeIn(sq))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=1.9, buff=0.75)
            vo.wait_until("a")
            self.play(FadeIn(complement), FadeIn(fa), Create(ca), FadeIn(la), FadeIn(ac_label))
            step(0, transform=False)
            vo.wait_until("b")
            self.play(FadeOut(VGroup(complement, fa, ca, la, ac_label)), FadeIn(nested))
            step(1, transform=False)
            vo.wait_until("c")
            self.play(FadeOut(nested))
            self.play(Create(ca), Create(cb), FadeIn(la), FadeIn(lb))
            self.play(FadeIn(fa), FadeIn(fb))
            vo.wait_until("d")
            self.play(FadeIn(lens), FadeIn(twice))
            vo.wait_until("e")
            step(2, transform=False)
            self.play(FadeOut(lens), FadeOut(twice))
            vo.wait_until("f")
            step(3, transform=False)
        self.clear_scene()

    def mere_again(self):
        d = load("axioms")
        terms = [fval(t) for t in d["ie_terms"]]
        partial = np.cumsum([terms[0], -terms[1], terms[2], -terms[3]])
        exact = fval(d["ie"])
        eq = MathTex(r"P\Big(\bigcup_{i=1}^4 A_i\Big)", r"=", r"4 \cdot \tfrac16", r"-", r"6 \cdot \tfrac1{36}", r"+",
                     r"4 \cdot \tfrac1{216}", r"-", r"\tfrac1{1296}", r"=", r"\tfrac{671}{1296}", font_size=34)
        eq.to_edge(UP, buff=0.6)
        eq[-1].set_color(EXACT)
        sub = label(r"$A_i$: \ throw $i$ shows a six", font_size=24, color=GREY_B).next_to(eq, DOWN, buff=0.2)
        A = axes([0.5, 4.5], [0.45, 0.7], x_length=7.0, y_length=3.6, xlabel=r"terms kept", ylabel=r"partial sum",
                 xticks=[1, 2, 3, 4], yticks=[0.5, 0.6, 0.7], center=[-1.3, -1.6, 0])
        ax = A.ax
        gold = DashedLine(ax.c2p(0.5, exact), ax.c2p(4.5, exact), color=EXACT, stroke_width=2.5)
        dots = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.08, color=SIM) for k, v in enumerate(partial)])
        zig = VMobject(color=SIM, stroke_width=2).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(partial)])
        vals = VGroup(*[MathTex(f"{v:.4f}", font_size=22, color=SIM).next_to(dt, DOWN if k % 2 else UP, buff=0.12)
                        for k, (dt, v) in enumerate(zip(dots, partial))])
        ub = label(r"one term: \ the union bound, \ $\tfrac23$", font_size=24, color=GREY_A).move_to([4.6, 0.2, 0])
        bon = VGroup(label(r"partial sums alternate above and below:", font_size=24, color=GREY_A),
                     label(r"Bonferroni's inequalities", font_size=24, color=S.ACCENT)).arrange(DOWN, buff=0.15)
        bon.move_to([4.6, -1.2, 0])
        intro = label('Inclusion--exclusion', font_size=36)
        with self.voiceover(
            "Inclusion–exclusion extends to any number of events, and it gives us de Méré's first bet a second "
            "way. <bookmark mark='a'/> Let A i be the event that throw i is a six. At least one six is the union of "
            "four events. Add their probabilities, four sixths; subtract the six pairwise overlaps, each one "
            "thirty-sixth; add back the four triple overlaps; subtract the one quadruple. <bookmark mark='b'/> Six "
            "hundred and seventy-one over twelve hundred and ninety-six, the same as before. <bookmark mark='c'/> "
            "Watch the partial sums. The first term alone is the union bound, two thirds, too big. Two terms, too "
            "small. Three, too big again, by a little. Each truncation alternates around the truth, narrowing as it "
            "goes: these are Bonferroni's inequalities, and they turn inclusion–exclusion into a source of upper and "
            "lower bounds."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(eq[:9]), FadeIn(sub), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(eq[9:]))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(gold))
            for k in range(4):
                self.play(FadeIn(dots[k], scale=1.4), FadeIn(vals[k]),
                          *([Create(Line(ax.c2p(k, partial[k - 1]), ax.c2p(k + 1, partial[k]), color=SIM,
                                         stroke_width=2))] if k else []), run_time=0.8)
                if k == 0:
                    self.play(FadeIn(ub))
            self.play(FadeIn(bon))
        _ = zig
        self.clear_scene()

    def hats(self):
        d = load("axioms")
        cols = [PA, PB, S.LIK, S.PRIOR]
        perms = list(permutations(range(4)))
        tiles = VGroup()
        for p in perms:
            row = VGroup()
            for i, v in enumerate(p):
                sq = Square(side_length=0.3, stroke_width=0, fill_color=cols[v], fill_opacity=0.9)
                if v == i:
                    sq.set_stroke(WHITE, width=2.5)
                row.add(sq)
            row.arrange(RIGHT, buff=0.04)
            row.der = all(v != i for i, v in enumerate(p))
            tiles.add(row)
        tiles.arrange_in_grid(6, 4, buff=(0.45, 0.3)).move_to([-3.6, -0.6, 0])
        owners = VGroup(*[Square(side_length=0.3, stroke_width=0, fill_color=c, fill_opacity=0.9) for c in cols])
        owners.arrange(RIGHT, buff=0.04)
        own_l = label(r"owners: ", font_size=24, color=GREY_A)
        head = VGroup(own_l, owners).arrange(RIGHT, buff=0.2).next_to(tiles, UP, buff=0.4)
        hc = history_card(1708, r"Pierre R\'emond de Montmort, \ \emph{le probl\`eme des rencontres}",
                          r"hats returned at random: \ what is the chance that nobody gets their own?",
                          color=S.MUSEUM, width=5.6, font_size=22).move_to([3.5, 2.0, 0])
        cnt = MathTex(rf"{d['d4']} \text{{ of }} {d['n4']}", r"=", r"\tfrac{3}{8}", font_size=38).move_to([3.5, 0.0, 0])
        cnt[2].set_color(EXACT)
        rows = [
            cmath(r"P(\text{some match})", r"=", r"\sum_{k=1}^n (-1)^{k+1} \binom{n}{k} \frac{(n-k)!}{n!}",
                  font_size=32),
            cmath(r"P(\text{no match})", r"=", r"\sum_{k=0}^n \frac{(-1)^k}{k!}", r"\longrightarrow", r"e^{-1}",
                  font_size=34),
        ]
        rows[1][4].set_color(EXACT)
        whys = [why(r"inclusion--exclusion: \ $k$ fixed hats, the rest in any order"), why(r"the series for $e^x$ at $x=-1$")]
        with self.voiceover(
            "Inclusion–exclusion's most famous answer is a puzzle from 1708, Montmort's problem of matches. "
            "<bookmark mark='a'/> People check their hats at a theatre, and the attendant hands them back at random. "
            "What's the chance that nobody gets their own hat back? <bookmark mark='b'/> With four people there are "
            "twenty-four ways to return the hats. A white outline marks someone who got their own. "
            "<bookmark mark='c'/> In nine of the twenty-four, nobody did: three eighths. <bookmark mark='d'/> For n "
            "people, let A i be the event that person i gets their own hat. Any k particular people get their own "
            "hats in n minus k factorial of the n factorial orders, and there are n choose k ways to pick the k. "
            "Inclusion–exclusion adds and subtracts these, and the binomials cancel the factorials, "
            "<bookmark mark='e'/> leaving the chance of no match as the sum of minus one to the k over k factorial. "
            "That's the series for e to the x at minus one."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in tiles], lag_ratio=0.04),
                      run_time=2.5)
            vo.wait_until("c")
            self.play(*[t.animate.set_opacity(0.18) for t in tiles if not t.der],
                      *[Indicate(t, color=EVENT, scale_factor=1.15) for t in tiles if t.der])
            self.play(Write(cnt))
            vo.wait_until("d")
            self.play(FadeOut(hc), cnt.animate.scale(0.8).move_to([3.5, 2.8, 0]))
            step = ladder(self, rows, whys, keep=2, top=1.8, x=3.0, buff=1.0, edge=6.9)
            step(0, transform=False)
            vo.wait_until("e")
            step(1, transform=False)
        self.clear_scene()

    def series(self):
        d = load("axioms")
        ser = np.asarray(d["series"])
        A = axes([0.5, 12.5], [0, 0.55], x_length=8.4, y_length=4.6, xlabel=r"number of people, $n$",
                 ylabel=r"P(nobody gets their own hat)", xticks=list(range(1, 13)), yticks=[0, 0.25, 0.5],
                 center=[-1.6, -0.3, 0])
        ax = A.ax
        e1 = DashedLine(ax.c2p(0.5, d["e_inv"]), ax.c2p(12.5, d["e_inv"]), color=EXACT, stroke_width=2.5)
        el = MathTex(r"1/e = 0.3679", font_size=26, color=EXACT).next_to(e1, RIGHT, buff=0.15)
        dots = VGroup(*[Dot(ax.c2p(n, v), radius=0.07, color=EXACT) for n, v in zip(range(1, 13), ser)])
        eng = VGroup(*[MathTex(frac(fr), font_size=22, color=EXACT).next_to(dots[k], UP if k % 2 else DOWN, buff=0.15)
                       for k, fr in enumerate(d["exact"][1:6], start=1)])
        sim = exact_sim(r"\textstyle\sum_{k\le 10} \tfrac{(-1)^k}{k!}", ser[9], d["sim_p"], d["sim_n"],
                        font_size=26).move_to([4.2, 2.6, 0])
        note_ = label(r"exact for $n \le 8$ by enumerating every order \ (the engine)", font_size=22,
                      color=GREY_B).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here's that answer for one to twelve people. <bookmark mark='a'/> For one person it's zero, for two a "
            "half, for three a third, for four three eighths, and then it locks onto one over e, zero point three "
            "six eight, almost at once. <bookmark mark='b'/> The engine confirms the first eight exactly, by "
            "listing every possible order; for eight people that's forty thousand three hundred and twenty orders. "
            "<bookmark mark='c'/> And ten thousand simulated shuffles of ten hats give the same answer to two "
            "decimals. A theatre of ten people or ten thousand: the chance that nobody gets their own hat is about "
            "thirty-seven percent, almost independent of the size of the crowd."
        ) as vo:
            self.play(FadeIn(A), Create(e1), FadeIn(el))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt, scale=1.4) for dt in dots], lag_ratio=0.2), run_time=3.0)
            self.play(FadeIn(eng))
            vo.wait_until("b")
            self.play(FadeIn(note_))
            vo.wait_until("c")
            self.play(FadeIn(sim, shift=LEFT * 0.2))
        self.clear_scene()

    def continuity(self):
        th = theorem_card(r"continuity of probability", r"if $A_1 \subseteq A_2 \subseteq \cdots$, \ then "
                          r"$P\big(\bigcup_n A_n\big) = \lim_{n} P(A_n)$", who=r"a consequence of axiom 3", color=EXACT,
                          width=7.4, font_size=26).move_to([0, 1.6, 0])
        ex = MathTex(r"P(\text{a head, eventually})", r"=", r"\lim_{n\to\infty}\big(1 - 2^{-n}\big)", r"=", r"1",
                     font_size=36).move_to([0, -0.6, 0])
        ex[4].set_color(EXACT)
        take = label(r"the axioms say how probabilities must fit together, \ not what they \emph{mean}: \ chapter 14",
                     font_size=28, color=S.ACCENT).to_edge(DOWN, buff=0.6)
        intro = label('Continuity of probability', font_size=36)
        with self.voiceover(
            "The third axiom's infinite sums buy one more property, continuity. <bookmark mark='a'/> If events grow, "
            "each containing the last, the probability of their union is the limit of their probabilities. "
            "<bookmark mark='b'/> Toss a coin until a head appears. The chance of a head within n tosses is one "
            "minus two to the minus n, so the chance of a head eventually is the limit, one. Infinite processes like "
            "this one are everywhere in statistics, and continuity is what lets us reason about them. "
            "<bookmark mark='c'/> Notice what the axioms don't say. They say how probabilities must fit together; "
            "they say nothing about what a probability is: a frequency, a degree of belief, a betting price. We'll "
            "come back to that question at the end of the part. First, the most useful operation in all of "
            "probability: learning something, and updating."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(th, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Write(ex))
            vo.wait_until("c")
            self.play(FadeIn(take, shift=UP * 0.2))
        self.clear_scene()
