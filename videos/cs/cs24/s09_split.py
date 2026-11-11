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
        al = label(r"for each $s$: \ binary-search $t - s$", font_size=19, color=YES).next_to(VGroup(L, R), UP, buff=0.1)
        notes = VGroup(
            label(r"\textbf{subset sum}: \ does some subset of $n$ numbers add up to $t$? \ NP-complete \ (Part 26)",
                  font_size=22, color=WHITE),
            label(r"try every subset: \ $2^n$; \ meet in the middle \ (Horowitz and Sahni, 1974): \ "
                  r"$O(2^{n/2} \cdot n)$", font_size=22, color=YES),
            label(rf"$n = {d['n']}$: \ {words(d['brute_sums'])} sums by brute force \ ({d['brute_s'] * 1000:.0f} ms), \ "
                  rf"{words(d['mitm_work'])} generated sums + search calls \ ({d['mitm_s'] * 1000:.1f} ms) \\ excludes sorting/comparison/bit-operation counts; \ both find it",
                  font_size=22, color=HEAD),
            label(rf"$n = 40$: \ {big(d['n40_brute'])} subsets, \ against {big(d['n40_mitm'])} sums: \ the square root "
                  r"of an exponential", font_size=22, color=YES),
            label(r"the same idea: \ baby-step giant-step \ (Part 30), \ double encryption \ (Part 29), \ bidirectional search",
                  font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.24).next_to(VGroup(L, R), DOWN, buff=0.5)
        with self.voiceover(
            "Meet in the middle reduces the exponent of some exhaustive searches. <bookmark mark='a'/> Subset "
            'sum asks whether selected numbers total a target. The brute-force routine here enumerates all '
            "subsets. <bookmark mark='b'/> Generate the sums of each half, sort one list, then search it for the "
            'complement of each sum in the other. The sorting and searches contribute additional factors; the '
            'displayed work counter counts generated sums and search calls, not every comparison or bit '
            "operation. <bookmark mark='c'/> The twenty-item example agrees with brute force; both have three "
            "retained timing trials. <bookmark mark='d'/> At forty items, two million generated sums replace a "
            'trillion full subsets, but sorting, exponential storage and the bit lengths of sums still matter. '
            "<bookmark mark='e'/> Bidirectional search uses a related meet-in-the-middle idea, with its own "
            'graph and stopping conditions.'
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
            label(rf"{words(d['mo_q'])} distinct-count queries on an array of {words(d['mo_n'])} elements \\ "
                  rf"{words(d['mo_moves'])} pointer moves; \ {words(d['mo_naive'])} elements scanned range by range",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.24).next_to(blocks, DOWN, buff=0.5)
        with self.voiceover(
            "Square-root decomposition divides work another way. <bookmark mark='a'/> Store totals for blocks of "
            "about square root n elements. <bookmark mark='b'/> A query scans boundary fragments and uses "
            'whole-block totals in the middle; the displayed example counts every touched element or block. '
            "<bookmark mark='c'/> Its update and query costs depend on the stored summary; not every operation "
            "admits an equally cheap merge. <bookmark mark='d'/> Mo's algorithm instead reorders offline queries "
            'by endpoint blocks and maintains a moving answer. It needs efficient add and remove operations for '
            "that statistic. <bookmark mark='e'/> For all twenty thousand distinct-count queries, we retain the "
            'deterministic input specification and output hash, and check every answer with an independent '
            'last-occurrence sweep using a sum tree. Pointer moves are an abstract work count, separate from '
            'Python wall time.'
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
