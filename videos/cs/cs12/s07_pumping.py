from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load, region)


class Pumping(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.anbn()
        self.consequence()

    def card(self):
        card = chapter_card(6, r"What regular languages cannot do", r"Can a finite machine count?", lit=(1961,),
                            extra=((1961, r"Bar-Hillel, \ Perles, \ Shamir"),), part=PART)
        with self.voiceover("Chapter six. What regular languages cannot do."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lemma(self):
        head = label(r"The pumping lemma", font_size=36).to_edge(UP, buff=0.3)
        n = 7
        xs = np.linspace(-5.5, 5.5, n)
        circ = VGroup(*[Circle(radius=0.28, stroke_color=CTRL, stroke_width=2, fill_color=CTRL, fill_opacity=0.12)
                        .move_to([x, 0.3, 0]) for x in xs])
        arrows = VGroup(*[Arrow(circ[k].get_right(), circ[k + 1].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2) for k in range(n - 1)])
        loop_from, loop_to = 2, 5
        same = label(r"the same state, \ twice", font_size=19, color=NO).next_to(
            VGroup(circ[loop_from], circ[loop_to]), DOWN, buff=0.9)
        link = DashedLine(circ[loop_from].get_bottom(), circ[loop_to].get_bottom(), color=NO).shift(DOWN * 0.15)
        bx = VGroup(Brace(VGroup(circ[0], circ[loop_from]), UP, color=DATA),
                    Brace(VGroup(circ[loop_from], circ[loop_to]), UP, color=HEAD),
                    Brace(VGroup(circ[loop_to], circ[-1]), UP, color=YES))
        bl = VGroup(*[label(t, font_size=24, color=c).next_to(b, UP, buff=0.08)
                      for t, c, b in ((r"$x$", DATA, bx[0]), (r"$y$", HEAD, bx[1]), (r"$z$", YES, bx[2]))])
        stmt = VGroup(
            label(r"a DFA with $p$ states reads a string of length $\ge p$: \ it visits $p + 1$ states, \ so one "
                  r"repeats \ (pigeonhole)", font_size=20, color=GREY_A),
            label(r"the part read between the two visits, \ $y$, \ is a loop: \ go round it any number of times",
                  font_size=20, color=GREY_A),
            label("if $L$ is regular: $\\exists p\\,\\forall s\\in L,\\ |s|\\ge p:\\ \\exists x,y,z,\\ s=xyz,\\ |xy|\\le p,\\ |y|>0,\\ \\forall i\\ge0:\\ xy^iz\\in L$", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover("Is every language regular? No, and the proof is a counting argument. <bookmark mark='a'/> Suppose a deterministic machine with p states reads a string of length p or more. After p symbols it has visited p plus one states, so by the pigeonhole principle it has been in some state twice. <bookmark mark='b'/> Call the part of the string read before the first visit x, the part between the two visits y, and the rest z. Reading y takes the machine round a loop, back to where it was. <bookmark mark='c'/> So it cannot tell the difference if we go round that loop twice, or ten times, or not at all: x y y z, and x z, end in the same state as x y z. <bookmark mark='d'/> That is the pumping lemma, from Yehoshua Bar-Hillel, Micha Perles and Eli Shamir in 1961: in a regular language, every long enough string has a short, non-empty piece near its start that can be pumped.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in circ], lag_ratio=0.15), FadeIn(arrows), FadeIn(stmt[0]), run_time=0.6)
            vo.wait_until('a')
            self.play(Create(link), FadeIn(same), Indicate(circ[loop_from], color=NO), Indicate(circ[loop_to], color=NO))
            vo.wait_until('b')
            self.play(FadeIn(bx), FadeIn(bl), FadeIn(stmt[1]))
            vo.wait_until('c')
            self.play(Indicate(bl[1], color=HEAD, scale_factor=1.6))
            vo.wait_until('d')
            self.play(FadeIn(stmt[2]))
        self.wait(0.3)
        self.clear_scene()

    def anbn(self):
        pu = load("pumping")
        p = pu["p"]
        head = label(r"$a^n b^n$ is not regular", font_size=36).to_edge(UP, buff=0.3)
        s = pu["s"]
        sl = label(rf"if it were regular with $p$ states, \ take $s = a^p b^p$ \ (here $p = {p}$)", font_size=21,
                   color=GREY_A).next_to(head, DOWN, buff=0.3)
        letters = VGroup(*[Text(c, font="DejaVu Sans Mono", font_size=34, color=DATA if c == "a" else CTRL)
                           for c in s]).arrange(RIGHT, buff=0.12).next_to(sl, DOWN, buff=0.3)
        bp = Brace(letters[:p], DOWN, color=HEAD)
        bpl = label(r"$|xy| \le p$: \ $y$ lies inside the $a$'s", font_size=19, color=HEAD).next_to(bp, DOWN,
                                                                                                  buff=0.08)
        grid = VGroup()
        for row in pu["splits"]:
            x, y, z, w = row["x"], row["y"], row["z"], row["pumped"]
            t = Text(f"{x}[{y}{y}]{z}", font="DejaVu Sans Mono", font_size=15, color=GREY_A)
            mark = label(r"$\notin L$" if not row["in"] else r"$\in L$", font_size=17, color=NO if not row["in"]
                         else YES)
            grid.add(VGroup(t, mark).arrange(RIGHT, buff=0.15))
        grid.arrange_in_grid(5, 3, buff=(0.6, 0.18), col_alignments="lll").next_to(letters, DOWN, buff=0.95)
        gl = label(rf"all {len(pu['splits'])} legal splits, \ $y$ doubled: \ more $a$'s than $b$'s, \ every time",
                   font_size=20, color=NO).next_to(grid, DOWN, buff=0.25)
        concl = label(r"no split can be pumped \ $\Rightarrow$ \ no finite automaton recognizes $a^n b^n$", font_size=23,
                      color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover("Now use the lemma to rule out a language. <bookmark mark='a'/> Suppose a DFA with p states recognizes a to the n followed by b to the n. Choose p a's followed by p b's; the picture illustrates p equals five. <bookmark mark='b'/> Every allowed split has x y of length at most p and a nonempty y, so y contains only a's. <bookmark mark='c'/> Pumping y twice adds at least one a and no b. All fifteen splits in this picture fail, and the same argument works for every p, without enumerating its splits. <bookmark mark='d'/> The assumed DFA would accept a string outside the language. That contradiction rules out every finite number of states; the finite picture illustrates the general proof.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(letters), FadeIn(sl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(GrowFromCenter(bp), FadeIn(bpl))
            vo.wait_until('c')
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.12), run_time=4)
            self.play(FadeIn(gl))
            vo.wait_until('d')
            self.play(FadeIn(concl))
        self.wait(0.3)
        self.clear_scene()

    def consequence(self):
        head = label("Unbounded nesting exceeds finite memory", font_size=36).to_edge(UP, buff=0.3)
        pts = VGroup(
            label("balanced parentheses $\\cap\\ \\mathtt{(}^*\\mathtt{)}^* = \\{\\mathtt{(}^n\\mathtt{)}^n:n\\ge0\\}$", font_size=22,
                  color=GREY_A),
            label("closure under intersection transfers the contradiction; bounded depth is a different language", font_size=22, color=GREY_A),
            label(r"the Myhill--Nerode view: \ $a$, $aa$, $aaa$, \dots \ are pairwise distinguishable \ "
                  r"($a^i b^i \in L$, \ $a^j b^i \notin L$): \ infinitely many states needed", font_size=21,
                  color=DATA),
            label("finite automata handle token forms; unbounded nesting needs more memory", font_size=24,
                  color=HEAD),
            label(r"the fix: \ give the machine a stack \ (chapter 10)", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            (
            "The distinction matters when reading programs. <bookmark mark='a'/> If balanced parentheses were "
            "regular, intersecting them with the regular pattern opening-brackets-star then closing-brackets-star "
            "would leave equal numbers of opens and closes, a language the same pumping argument rules out. "
            "<bookmark mark='b'/> Ordinary finite automata therefore cannot validate arbitrary nesting. A fixed "
            "depth limit changes the language, and engines with recursion or other extensions go beyond "
            "mathematical regular expressions. <bookmark mark='c'/> Myhill and Nerode give another proof for a to "
            "the n b to the n: different counts of initial a's require different states, since a suitable suffix "
            "of b's distinguishes each pair. <bookmark mark='d'/> Regular expressions are useful for this "
            "language's token forms; recognizing its unbounded nested syntax needs more memory. <bookmark "
            "mark='e'/> A stack supplies that memory in chapter ten."
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
