from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, cells_row, load, mono)


class PrefixSums(VoiceoverScene):
    def construct(self):
        self.card()
        self.sums()
        self.diffs()
        self.image()
        self.scan()

    def card(self):
        card = chapter_card(1, r"Prefix sums", r"How do you answer a range question with one subtraction?",
                            lit=(1984, 2001), extra=((1984, r"Crow's summed-area tables"), (2001, r"Viola--Jones")),
                            part=PART)
        with self.voiceover("Chapter one. Prefix sums."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def sums(self):
        d = load("prefix")
        a, S = d["a"], d["S"]
        l, r = d["query"]
        head = label(r"One pass now, \ one subtraction per question", font_size=32).to_edge(UP, buff=0.35)
        row = cells_row(a, w=0.62, h=0.55, font=22).move_to(UP * 1.4)
        al = label(r"$a$", font_size=24, color=GREY_A).next_to(row, LEFT, buff=0.25)
        prow = cells_row(S, w=0.62, h=0.55, font=20, color=HEAD, labels=True).next_to(row, DOWN, buff=0.75)
        prow.shift(LEFT * 0.31)
        pl = label(r"$S$", font_size=24, color=HEAD).next_to(prow, LEFT, buff=0.25)
        sel = SurroundingRectangle(VGroup(*row.boxes[l:r + 1]), color=YES, buff=0.04, stroke_width=3)
        s_hi = SurroundingRectangle(prow.boxes[r + 1], color=YES, buff=0.03, stroke_width=3)
        s_lo = SurroundingRectangle(prow.boxes[l], color=NO, buff=0.03, stroke_width=3)
        lines = VGroup(
            MathTex(r"S_0 = 0, \qquad S_{i+1} = S_i + a_i", font_size=34, color=HEAD),
            MathTex(rf"a_{l} + \dots + a_{{{r}}} \;=\; S_{{{r + 1}}} - S_{l} \;=\; {S[r + 1]} - {S[l]} \;=\; "
                    rf"{d['query_sum']}", font_size=34, color=YES),
            label(r"$O(n)$ once, \ then $O(1)$ per range: \ the trade every index makes", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(prow, DOWN, buff=0.55)
        with self.voiceover(
            "The simplest precomputation in the business. <bookmark mark='a'/> Here are sixteen numbers, and we will be "
            "asked, over and over, for the sum of some stretch of them. <bookmark mark='b'/> Walk the array once and "
            "write down the running totals: S of i is the sum of everything before position i. <bookmark mark='c'/> "
            "Now any range sum is one subtraction. Positions three to ten: the total up to eleven, minus the total up "
            "to three, forty-four minus eight, thirty-six. <bookmark mark='d'/> Linear work once, then constant work "
            "per question. Nearly every index in this part makes some version of that trade."
        ) as vo:
            self.play(FadeIn(head), FadeIn(row), FadeIn(al))
            vo.wait_until("a")
            self.play(Indicate(row.boxes, color=DATA, scale_factor=1.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(prow.boxes[i], prow.vals[i], prow.idx[i])) for i in range(len(S))],
                                  lag_ratio=0.12), FadeIn(pl), FadeIn(lines[0]), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(sel), Create(s_hi), Create(s_lo), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def diffs(self):
        d = load("prefix")
        head = label(r"Difference arrays: \ the same trick, \ backwards", font_size=32).to_edge(UP, buff=0.35)
        ups = d["updates"]
        D = d["diff"]
        after = d["after"]
        ul = VGroup(*[label(rf"add {v} to positions {l}--{r}", font_size=22, color=c)
                      for (l, r, v), c in zip(ups, (DATA, LAM, HEAD))]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ul.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.8)
        drow = cells_row(D, w=0.62, h=0.55, font=20, color=LAM).move_to(UP * 0.1)
        dl = label(r"$D$", font_size=24, color=LAM).next_to(drow, LEFT, buff=0.25)
        arow = cells_row(after, w=0.62, h=0.55, font=20, color=YES, labels=False).next_to(drow, DOWN, buff=0.7)
        alab = label(r"prefix sum of $D$", font_size=20, color=YES).next_to(arow, LEFT, buff=0.25)
        notes = VGroup(
            label(r"each update touches two cells: \ $D_l \mathrel{+}= v$, \ $D_{r+1} \mathrel{-}= v$", font_size=22,
                  color=LAM),
            label(r"one prefix sum at the end rebuilds the array: \ $k$ updates in $O(k + n)$, \ not $O(kn)$",
                  font_size=22, color=YES),
            label(r"in two dimensions: \ four corners per rectangle \ (box filters, \ painting rectangles offline)",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(arow, DOWN, buff=0.45)
        with self.voiceover(
            "Run the idea backwards and it handles updates. <bookmark mark='a'/> Suppose we must add three to "
            "positions two to nine, two to positions five to twelve, and one to positions zero to four. Doing it "
            "directly touches every position in every range. <bookmark mark='b'/> Instead keep a difference array: "
            "for each update, add the amount where its range starts and subtract it just after the range ends. Two "
            "cells per update, however long the range. <bookmark mark='c'/> One prefix sum at the end rebuilds "
            "the array: the running total switches each update on at its start and off after its end. <bookmark "
            "mark='d'/> In two dimensions the same trick costs four corners per rectangle."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(u) for u in ul], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(Indicate(ul, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(drow), FadeIn(dl), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(arow.boxes[i], arow.vals[i])) for i in range(len(after))],
                                  lag_ratio=0.1), FadeIn(alab), FadeIn(notes[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def image(self):
        d = load("prefix")
        img, I = d["img"], d["I"]
        r0, c0, r1, c1 = d["box"]
        head = label(r"The integral image", font_size=34).to_edge(UP, buff=0.3)
        cw = 0.52

        def grid(M, color, origin, shade=None):
            g = VGroup()
            for r, rowv in enumerate(M):
                for c, v in enumerate(rowv):
                    sq = Square(side_length=cw, stroke_color=GREY_B, stroke_width=1.0).move_to(
                        origin + np.array([c * cw, -r * cw, 0]))
                    if shade and shade(r, c):
                        sq.set_fill(color, 0.35)
                    g.add(VGroup(sq, mono(str(v), 15 if v < 100 else 12, WHITE).move_to(sq)))
            return g
        o1 = np.array([-6.3, 1.6, 0])
        G = grid(img, YES, o1, shade=lambda r, c: r0 <= r <= r1 and c0 <= c <= c1)
        gl = label(r"pixels", font_size=20, color=GREY_A).next_to(G, UP, buff=0.12)
        o2 = np.array([-1.4, 1.85, 0])
        H = grid(I, HEAD, o2)
        hl = label(r"$I_{r,c}$ = sum above and to the left", font_size=20, color=HEAD).next_to(H, UP, buff=0.12)
        corners = [(r1 + 1, c1 + 1, YES), (r0, c1 + 1, NO), (r1 + 1, c0, NO), (r0, c0, YES)]
        rings = VGroup(*[Circle(radius=cw * 0.45, color=col, stroke_width=3).move_to(o2 + np.array([c * cw, -r * cw, 0]))
                         for r, c, col in corners])
        eq = MathTex(rf"{I[r1 + 1][c1 + 1]} - {I[r0][c1 + 1]} - {I[r1 + 1][c0]} + {I[r0][c0]} = {d['box_sum']}",
                     font_size=32, color=YES).next_to(VGroup(G, H), DOWN, buff=0.45)
        notes = VGroup(
            label(rf"any rectangle in four lookups \ (here rows {r0}--{r1}, \ columns {c0}--{c1}: \ {d['box_brute']}, "
                  r"\ checked)", font_size=21, color=WHITE),
            label(r"Viola and Jones (2001): \ thousands of box features per window, \ face detection in real time \ "
                  r"(\textit{AI, Built} Part 6)", font_size=21, color=LAM),
            label(r"Crow (1984): \ summed-area tables for texture filtering in graphics", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(eq, DOWN, buff=0.35)
        with self.voiceover(
            "Prefix sums work in two dimensions. <bookmark mark='a'/> Here is a small image. <bookmark mark='b'/> Its "
            "integral image stores, at each position, the sum of every pixel above and to the left. One pass builds "
            "it. <bookmark mark='c'/> Then the sum over any rectangle is four lookups: the corner below and to the "
            "right, minus the two strips we do not want, plus the corner we subtracted twice. <bookmark mark='d'/> "
            "Paul Viola and Michael Jones built real-time face detection on this in 2001: thousands of rectangle "
            "features per window, each in constant time, as the AI series showed. Frank Crow had used the same "
            "tables in 1984 to blur textures in computer graphics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(G), FadeIn(gl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in H], lag_ratio=0.01), FadeIn(hl), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(rings), FadeIn(eq), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def scan(self):
        head = label(r"Prefix sums in parallel", font_size=34).to_edge(UP, buff=0.35)
        a = [3, 1, 4, 1, 5, 9, 2, 6]
        rows = [a]
        k = 1
        while k < len(a):
            prev = rows[-1]
            rows.append([prev[i] + (prev[i - k] if i >= k else 0) for i in range(len(a))])
            k *= 2
        cw, dy = 0.8, 1.15
        grid = VGroup()
        for r, vals in enumerate(rows):
            g = VGroup(*[VGroup(Rectangle(width=cw, height=0.55, stroke_color=GREY_B, stroke_width=1.2).set_fill(
                YES if r == len(rows) - 1 else DATA, 0.12 + 0.12 * r), mono(str(v), 20, WHITE)) for v in vals])
            for c in g:
                c[1].move_to(c[0])
            g.arrange(RIGHT, buff=0.15).move_to([-1.6, 2.0 - r * dy, 0])
            grid.add(g)
        arrows = VGroup()
        k = 1
        for r in range(1, len(rows)):
            for i in range(k, len(a)):
                arrows.add(Arrow(grid[r - 1][i - k].get_bottom(), grid[r][i].get_top(), buff=0.05, stroke_width=1.6,
                                 color=GREY_C, max_tip_length_to_length_ratio=0.12))
            k *= 2
        steps = VGroup(*[label(rf"step {r}: \ add the value $2^{{{r - 1}}}$ to the left", font_size=18, color=GREY_A)
                         .next_to(grid[r], RIGHT, buff=0.35) for r in range(1, len(rows))])
        notes = VGroup(
            label(r"$\log_2 n$ rounds, \ every element in parallel \ (Hillis and Steele, 1986); \ Blelloch's "
                  r"work-efficient scan does $O(n)$ additions", font_size=21, color=WHITE),
            label(r"GPUs use scans for stream compaction, \ radix sort \ (chapter 11) and sparse matrices", font_size=21,
                  color=LAM),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One more property makes prefix sums a workhorse: they parallelize, although each total seems to depend "
            "on the one before. <bookmark mark='a'/> In the first round, every element adds its left neighbour. "
            "<bookmark mark='b'/> In the second, every element adds the value two places to its left; in the third, "
            "four places. <bookmark mark='c'/> After log n rounds every position holds its prefix sum, and each round "
            "is done by all elements at once. Daniel Hillis and Guy Steele ran this on the Connection Machine, and "
            "Guy Blelloch made it work-efficient. <bookmark mark='d'/> Graphics cards use scans to compact streams, "
            "to sort, and to handle sparse matrices."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid[0]))
            vo.wait_until("a")
            n1 = len(a) - 1
            self.play(FadeIn(arrows[:n1]), FadeIn(grid[1]), FadeIn(steps[0]))
            vo.wait_until("b")
            n2 = n1 + len(a) - 2
            self.play(FadeIn(arrows[n1:n2]), FadeIn(grid[2]), FadeIn(steps[1]))
            self.play(FadeIn(arrows[n2:]), FadeIn(grid[3]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()
