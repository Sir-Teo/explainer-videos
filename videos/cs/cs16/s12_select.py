from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs16.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono,
                                   words)


class Select(VoiceoverScene):
    def construct(self):
        self.card()
        self.quickselect()
        self.mom()
        self.five()

    def card(self):
        card = chapter_card(11, r"Selection and the median of medians", r"Can we find the median without sorting?",
                            lit=(1973,), extra=((1973, r"Blum, Floyd, Pratt, Rivest and Tarjan"),), part=PART)
        with self.voiceover("Chapter eleven. Selection and the median of medians."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def quickselect(self):
        d = load("select")
        head = label(r"Quickselect: \ recurse on one side only", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"to find the $k$-th smallest: \ partition, \ then continue only where $k$ lies", font_size=22,
                  color=GREY_A),
            MathTex(r"\mathbb{E}[C] \le n + \tfrac34 n + (\tfrac34)^2 n + \cdots = 4n \quad\text{(a crude bound)}",
                    font_size=30),
            label(r"exactly, \ for the median: \ $(2 + 2\ln 2)\,n \approx 3.39\,n$ \ (Knuth, \ 1971)", font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.5)
        rows = [[words(r["n"]), words(round(r["quick"])), f"{r['quick'] / r['n']:.2f}", words(round(r["sort"]))]
                for r in d["rows"]]
        tab = grid_table([r"$n$", r"quickselect, \ mean", r"per element", r"sorting: \ $n \lg n$"], rows,
                         widths=[2.0, 3.2, 2.2, 3.0], row_h=0.44, font_size=19,
                         colors=[[WHITE, YES, YES, GREY_B]] * len(rows)).next_to(pts, DOWN, buff=0.4)
        with self.voiceover(
            "Sorting finds every element's rank. Often we need only one: the median, or the ninety-ninth "
            "percentile. <bookmark mark='a'/> Hoare's quickselect partitions like quicksort, then recurses only into "
            "the side that contains the rank we want. <bookmark mark='b'/> A crude argument: a random pivot usually "
            "throws away at least a quarter, so the work is at most n plus three quarters of n plus nine sixteenths "
            "of n, and so on: four n. <bookmark mark='c'/> The exact expected cost for the median is two plus two "
            "log two, times n, about three point three nine n. Measured, the counts hover right there: linear, and "
            "far below sorting."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(Write(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def five(self):
        head = label(r"Why groups of five?", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(label(r"groups of 3", font_size=22, color=NO),
                   MathTex(r"T(n) \le T(n/3) + T(2n/3) + O(n) \;\Rightarrow\; \Theta(n \log n)", font_size=28,
                           color=NO),
                   label(r"$\tfrac13 + \tfrac23 = 1$: \ every level costs the same", font_size=19,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(label(r"groups of 5", font_size=22, color=YES),
                   MathTex(r"T(n) \le T(n/5) + T(7n/10) + O(n) \;\Rightarrow\; \Theta(n)", font_size=28, color=YES),
                   label(r"$\tfrac15 + \tfrac{7}{10} = \tfrac{9}{10}$: \ the levels shrink", font_size=19,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
            VGroup(label(r"groups of 7", font_size=22, color=DATA),
                   MathTex(r"T(n) \le T(n/7) + T(5n/7) + O(n) \;\Rightarrow\; \Theta(n)", font_size=28, color=DATA),
                   label(r"$\tfrac17 + \tfrac57 = \tfrac67$: \ also linear, \ larger constant per group", font_size=19,
                         color=GREY_B)).arrange(DOWN, buff=0.1),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.5)
        note = label(r"the recursion tree again: \ linear exactly when the pieces add up to less than the whole",
                     font_size=21, color=HEAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why five? The recursion tree answers it. <bookmark mark='a'/> With groups of three, the median of "
            "medians guarantees only a third on each side, so the two recursive calls have sizes a third and two "
            "thirds. They add up to the whole, every level costs n, and the total is n log n: no better than "
            "sorting. <bookmark mark='b'/> With five, a fifth plus seven tenths is nine tenths. The levels shrink "
            "geometrically and the total is linear. <bookmark mark='c'/> Seven works too, with a larger cost per "
            "group. <bookmark mark='d'/> The rule is the one from the master theorem's geometry: divide and conquer "
            "is linear exactly when the subproblems add up to strictly less than the problem."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def mom(self):
        d = load("select")
        head = label(r"Linear in the worst case \ (Blum, Floyd, Pratt, Rivest, Tarjan, \ 1973)", font_size=30).to_edge(
            UP, buff=0.3)
        steps = VGroup(
            label(r"1. \ split into groups of five; \ find each group's median", font_size=22, color=GREY_A),
            label(r"2. \ find the median of those $n/5$ medians, \ recursively: \ the pivot", font_size=22,
                  color=GREY_A),
            label(r"3. \ at least $3n/10$ elements are smaller than it, \ and $3n/10$ larger", font_size=22,
                  color=YES),
            MathTex(r"T(n) \le T(n/5) + T(7n/10) + O(n)", font_size=34, color=HEAD),
            label(r"$\tfrac15 + \tfrac{7}{10} = \tfrac{9}{10} < 1$: \ the levels shrink geometrically, \ so $T(n) = O(n)$",
                  font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(head, DOWN, buff=0.45)
        r = d["rows"][-1]
        meas = label(rf"measured: \ {r['mom'] / r['n']:.1f} comparisons per element, \ against quickselect's "
                     rf"{r['quick'] / r['n']:.1f}: \ a guarantee, \ at a price", font_size=21,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Quickselect is linear on average. Can it be linear in the worst case? In 1973, five authors, four of "
            "them Turing award winners, showed it can. <bookmark mark='a'/> Split the elements into groups of "
            "five and find each group's median. <bookmark mark='b'/> Then find the median of those medians, "
            "recursively, and use it as the pivot. <bookmark mark='c'/> It is guaranteed to be a good one: at least "
            "three tenths of the elements are smaller, and three tenths larger. <bookmark mark='d'/> So the time "
            "satisfies T of n at most T of n over five, plus T of seven n over ten, plus linear work. <bookmark "
            "mark='e'/> One fifth plus seven tenths is nine tenths, less than one, so in the recursion tree each "
            "level does at most nine tenths of the work of the level above: a geometric series, linear in total. "
            "Our implementation makes about eight comparisons per element, more than twice quickselect's average. A "
            "guarantee, bought with a constant."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()
