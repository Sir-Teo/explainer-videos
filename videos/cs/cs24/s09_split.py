from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs24.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, big, load, mono, words)


class Splitting(VoiceoverScene):
    def construct(self):
        self.card()
        self.mitm()
        self.roots()

    def card(self):
        card = chapter_card(8, r"Meet in the middle and square roots", r"What do you gain by cutting a problem in "
                            r"two unequal ways?", lit=(1974,), extra=((1974, r"Horowitz--Sahni"),), part=PART)
        with self.voiceover("Chapter eight. Meet in the middle, and square roots."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def mitm(self):
        d = load("split")
        head = label(r"Meet in the middle", font_size=34).to_edge(UP, buff=0.3)
        L = Rectangle(width=4.6, height=1.5, stroke_color=DATA, stroke_width=2).set_fill(DATA, 0.15)
        R = Rectangle(width=4.6, height=1.5, stroke_color=LAM, stroke_width=2).set_fill(LAM, 0.15)
        VGroup(L, R).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.6)
        lt = label(r"first half: \ all $2^{n/2}$ subset sums", font_size=21, color=DATA).move_to(L)
        rt = label(r"second half: \ all $2^{n/2}$ sums, \ \textbf{sorted}", font_size=21, color=LAM).move_to(R)
        arrow = Arrow(L.get_right(), R.get_left(), buff=0.1, color=YES)
        al = label(r"for each $s$: \ binary-search $t - s$", font_size=19, color=YES).next_to(arrow, UP, buff=0.12)
        notes = VGroup(
            label(r"\textbf{subset sum}: \ does some subset of $n$ numbers add up to $t$? \ NP-complete \ (Part 26)",
                  font_size=22, color=WHITE),
            label(r"try every subset: \ $2^n$; \ meet in the middle \ (Horowitz and Sahni, 1974): \ "
                  r"$O(2^{n/2} \cdot n)$", font_size=22, color=YES),
            label(rf"$n = {d['n']}$: \ {words(d['brute_sums'])} sums by brute force \ ({d['brute_s'] * 1000:.0f} ms), \ "
                  rf"{words(d['mitm_work'])} steps in the middle \ ({d['mitm_s'] * 1000:.1f} ms); \ both find it",
                  font_size=22, color=HEAD),
            label(rf"$n = 40$: \ {big(d['n40_brute'])} subsets, \ against {big(d['n40_mitm'])} sums: \ the square root "
                  r"of an exponential", font_size=22, color=YES),
            label(r"the same idea: \ baby-step giant-step \ (Part 30), \ double encryption \ (Part 29), \ bidirectional search",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(VGroup(L, R), DOWN, buff=0.5)
        with self.voiceover(
            "Some exponential problems can be made exponentially smaller. <bookmark mark='a'/> Subset sum asks "
            "whether some of n numbers add up to a target. It is NP-complete, as Part 26 will prove, and trying every "
            "subset costs two to the n. <bookmark mark='b'/> Split the numbers into two halves. List every subset "
            "sum of the first half, and every subset sum of the second half, sorted. For each sum s on the left, "
            "binary-search the right for the target minus s. Ellis Horowitz and Sartaj Sahni did this in 1974: two "
            "to the n over two, times n. <bookmark mark='c'/> On twenty numbers, brute force generated a million sums "
            "in seventy milliseconds; the middle found the same answer in a fraction of a millisecond. <bookmark "
            "mark='d'/> At forty numbers it is a trillion subsets against two million sums. Still exponential, but "
            "the square root of it. <bookmark mark='e'/> The same move computes discrete logarithms in Part 30, "
            "breaks double encryption in Part 29, and runs a shortest-path search from both ends."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Indicate(notes[0], color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(L), FadeIn(R), FadeIn(lt), FadeIn(rt), GrowArrow(arrow), FadeIn(al), FadeIn(notes[1]))
            for mk, n_ in zip("cde", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def roots(self):
        d = load("split")
        head = label(r"Square-root decomposition, \ and Mo's order", font_size=32).to_edge(UP, buff=0.35)
        B = 8
        n = 64
        bw = 0.17
        cells = VGroup(*[Rectangle(width=bw, height=0.4, stroke_color=GREY_D, stroke_width=0.6) for _ in range(n)])
        cells.arrange(RIGHT, buff=0).move_to(UP * 1.7)
        blocks = VGroup(*[Rectangle(width=B * bw, height=0.62, stroke_color=HEAD, stroke_width=2).move_to(
            VGroup(*cells[b * B:(b + 1) * B])) for b in range(n // B)])
        l, r = 11, 52
        used = VGroup()
        for i in range(l, r + 1):
            if i // B == l // B or i // B == r // B:
                used.add(cells[i].copy().set_fill(DATA, 0.6))
        for b in range(l // B + 1, r // B):
            used.add(blocks[b].copy().set_fill(HEAD, 0.35))
        notes = VGroup(
            label(r"cut the array into $\sqrt n$ blocks of $\sqrt n$, \ and keep each block's total", font_size=22,
                  color=HEAD),
            label(rf"a range: \ whole blocks in the middle, \ single elements at the ends: \ $O(\sqrt n)$ \ (here "
                  rf"{d['sqrt_touched']} steps for a range of {8641 - 137 + 1:,} in {d['sqrt_B']}-blocks)", font_size=22,
                  color=DATA),
            label(r"crude, \ but it handles operations no tree handles neatly", font_size=22, color=GREY_A),
            label(r"\textbf{Mo's order}: \ answer offline queries sorted by $(\lfloor l/\sqrt n \rfloor, r)$, \ moving "
                  r"two pointers", font_size=22, color=LAM),
            label(rf"distinct values in {words(d['mo_q'])} ranges of {words(d['mo_n'])}: \ {words(d['mo_moves'])} "
                  rf"pointer moves \ against {words(d['mo_naive'])} elements scanned one range at a time",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.24).next_to(blocks, DOWN, buff=0.5)
        with self.voiceover(
            "The square root is the other way to split. <bookmark mark='a'/> Cut the array into about root n blocks "
            "of root n elements each, and keep every block's total. <bookmark mark='b'/> A range query adds up the "
            "whole blocks in its middle and the single elements at its two ends: about root n steps. A range of eight "
            "and a half thousand elements in blocks of a hundred took a hundred and eighty-nine steps. <bookmark "
            "mark='c'/> It is cruder than a tree, and more flexible: almost any operation can be kept per block. "
            "<bookmark mark='d'/> Mo's algorithm uses the same idea on time. Given all the queries in advance, sort "
            "them by the block of their left end, then by their right end, and answer them in that order, moving two "
            "pointers and keeping a running answer. <bookmark mark='e'/> For the number of distinct values in twenty "
            "thousand ranges, that took two million pointer moves, against eighty-four million elements if each range "
            "were scanned on its own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(blocks), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(used), FadeIn(notes[1]))
            for mk, n_ in zip("cde", notes[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
