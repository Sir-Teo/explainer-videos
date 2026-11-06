from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, words)


class Numbers(VoiceoverScene):
    def construct(self):
        self.card()
        self.pseudo()
        self.strong()

    def card(self):
        card = chapter_card(8, r"Strong and weak hardness", r"When is a hard problem only hard because of big "
                            r"numbers?", lit=(1975, 1978), extra=((1975, r"Ibarra--Kim"), (1978, r"Garey--Johnson")),
                            part=PART)
        with self.voiceover("Chapter eight. Strong and weak hardness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def pseudo(self):
        k = load("knapsack")
        head = label(r"Subset sum: \ NP-complete, \ yet the DP is fast?", font_size=32).to_edge(UP, buff=0.35)
        rows = [[str(r["digits"]), words(r["W"]), f"{r['dp_s'] * 1000:.2f} ms"] for r in k["rows"]]
        tab = grid_table([r"digits per number", r"target $W$", r"DP time"], rows, widths=[2.8, 2.6, 2.2],
                         row_h=0.42, font_size=20, mono_cols=(), colors=[[WHITE, DATA, NO]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        tl = label(rf"{k['n']} numbers; \ the DP marks every reachable sum up to $W$ \ (Part 19)", font_size=19,
                   color=GREY_A).next_to(tab, DOWN, buff=0.15).align_to(tab, LEFT)
        notes = VGroup(
            label(r"time $O(nW)$: \ polynomial in the \textbf{value} $W$", font_size=21, color=WHITE),
            label(r"but the input has only $\log_{10} W$ digits: \\ each extra digit multiplies the time by 10",
                  font_size=21, color=NO),
            label(r"\textbf{pseudo-polynomial}: \ fast while the numbers are small", font_size=21, color=YES),
            label(rf"with {k['mitm_digits']}-digit numbers the DP is hopeless; \\ meet in the middle \ (Part 24) "
                  rf"takes {k['mitm_s'] * 1000:.0f} ms, \\ whatever the digits, \ but $2^{{n/2}}$ in $n$",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        if notes.get_right()[0] > 6.9:
            notes.width = 6.9 - notes.get_left()[0]
            notes.next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        with self.voiceover(
            "Subset sum is NP-complete, yet Part 19 solved it with dynamic programming. Is that a contradiction? "
            "<bookmark mark='a'/> The dynamic program marks every reachable sum up to the target W, so it takes "
            "time proportional to n times W. <bookmark mark='b'/> But W is a number, and the input only contains "
            "its digits. Every extra digit multiplies W, and the running time, by ten: thirty numbers of six digits "
            "take a hundred times longer than thirty numbers of four. <bookmark mark='c'/> Such an algorithm is "
            "called pseudo-polynomial. It is polynomial in the size of the numbers, not in the length of the input. "
            "<bookmark mark='d'/> With twelve-digit numbers the table would have a trillion entries. Meet in the "
            "middle, from Part 24, does not care about the digits and takes fifty milliseconds here, but it is "
            "exponential in the number of items."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), FadeIn(tl),
                      FadeIn(notes[0]))
            for mk, n_ in zip("bcd", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def strong(self):
        head = label(r"Weakly against strongly NP-hard", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"\textbf{weakly} NP-hard: \ hard only when the numbers are huge; \ knapsack, \ subset sum, \ "
                  r"partition", font_size=22, color=DATA),
            label(r"\textbf{strongly} NP-hard: \ hard even with numbers written in unary; \ 3-partition, \ bin packing, "
                  r"\ TSP", font_size=22, color=NO),
            label(r"Garey and Johnson \ (1978) \ drew the line; \ the reductions of chapter 6 use small numbers or "
                  r"none", font_size=22, color=WHITE),
            label(r"weak hardness has an escape: \ \textbf{round the numbers}", font_size=22, color=YES),
            label(r"knapsack within $(1 - \varepsilon)$ of optimal in time polynomial in $n$ and $1/\varepsilon$ "
                  r"\ (Ibarra and Kim, 1975)", font_size=22, color=YES),
            label(r"a strongly NP-hard problem has no such scheme unless P = NP", font_size=22, color=NO),
            label(r"so ``NP-hard'' is the start of the analysis, \ not the end", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.28).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This splits NP-hard problems in two. <bookmark mark='a'/> Some are weakly NP-hard: hard only because "
            "the numbers can be astronomically large. Knapsack, subset sum and partition. <bookmark mark='b'/> "
            "Others are strongly NP-hard: hard even if every number is small, written in unary. Three-partition, "
            "bin packing, the travelling salesman. <bookmark mark='c'/> Michael Garey and David Johnson drew this "
            "line in 1978. <bookmark mark='d'/> Weak hardness has an escape: round the numbers down to fewer "
            "digits. <bookmark mark='e'/> Oscar Ibarra and Chul Kim did that for knapsack in 1975: a solution within "
            "a factor one minus epsilon of the best, in time polynomial in n and one over epsilon. <bookmark "
            "mark='f'/> A strongly NP-hard problem cannot have such a scheme unless P equals NP. <bookmark "
            "mark='g'/> So learning that a problem is NP-hard is the beginning of the analysis: which kind, how "
            "close can we get, and how big are the real inputs?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
