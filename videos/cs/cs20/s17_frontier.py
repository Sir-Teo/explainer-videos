from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.derandomized()
        self.hardness()
        self.pit()
        self.sketches()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ does randomness help?", r"Is every coin flip removable?",
                            lit=(1997, 2002, 2016), extra=((1997, r"hardness against randomness"),
                                                           (2002, r"PRIMES is in P"),
                                                           (2016, r"matching in quasi-NC")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: does randomness help?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def derandomized(self):
        head = label(r"Coins that were removed", font_size=34).to_edge(UP, buff=0.35)
        rows = [
            [r"primality", r"Miller--Rabin \ (1976--80)", r"AKS \ (2002)"],
            [r"undirected connectivity in log space", r"a random walk", r"Reingold \ (2005)"],
            [r"minimum cut, \ near-linear time", r"Karger \ (2000)", r"Kawarabayashi--Thorup \ (2015); \ "
                                                                    r"Henzinger, \ Li, \ Rao, \ Wang \ (2024)"],
            [r"bipartite matching, \ in parallel", r"Tutte matrix \ (1979--87)", r"quasi-NC: \ Fenner, \ Gurjar, \ "
                                                                                r"Thierauf \ (2016)"],
        ]
        tab = grid_table([r"problem", r"with coins", r"without"], rows, widths=[4.4, 3.4, 5.2], row_h=0.62,
                         font_size=19, mono_cols=(), colors=[[WHITE, LAM, YES]] * len(rows)).next_to(head, DOWN,
                                                                                                buff=0.5)
        tab.set_x(0)
        note_ = label(r"each took decades, \ and none was a general method", font_size=22, color=HEAD
                      ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Many of this part's coins have since been removed, one problem at a time. <bookmark mark='a'/> "
            "Primality got a deterministic polynomial test in 2002; logarithmic-space connectivity lost its random "
            "walk in 2005; near-linear minimum cuts became deterministic in 2015 and, for weighted graphs, in 2024; "
            "and in 2016 Fenner, Gurjar and Thierauf nearly removed the coins from parallel bipartite matching. "
            "<bookmark mark='b'/> Each took years and its own idea. Is there a general reason this keeps working?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.7), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def hardness(self):
        head = label(r"Hardness against randomness", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"BPP: \ problems a polynomial-time algorithm with coins solves, \ wrong with probability "
                  r"$\le \tfrac13$", font_size=21, color=GREY_A),
            label(r"a pseudorandom generator stretches $O(\log n)$ truly random bits into $n$ that fool every "
                  r"small circuit", font_size=21, color=WHITE),
            label(r"then try all $2^{O(\log n)} = n^{O(1)}$ seeds, \ and take the majority: \ no coins", font_size=21,
                  color=LAM),
            label(r"Nisan and Wigderson (1994); \ Impagliazzo and Wigderson (1997):", font_size=21, color=WHITE),
            label(r"if some problem in $\mathsf{E}$ needs circuits of size $2^{\Omega(n)}$, \ then $\mathsf{P} = "
                  r"\mathsf{BPP}$", font_size=24, color=YES),
            label(r"hard functions make good coins: \ most researchers believe $\mathsf{P} = \mathsf{BPP}$ \ "
                  r"(Part 27)", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "There is, conditionally. <bookmark mark='a'/> Call BPP the problems that a polynomial-time algorithm "
            "with coins solves with error at most a third. <bookmark mark='b'/> Suppose we had a pseudorandom "
            "generator that stretched a logarithmic number of truly random bits into n bits that no small circuit "
            "can tell from coins. <bookmark mark='c'/> Then we could try every seed, only polynomially many, and "
            "take the majority answer. No coins at all. <bookmark mark='d'/> Noam Nisan and Avi Wigderson, and "
            "then Russell Impagliazzo and Wigderson, showed how to build such a generator from any sufficiently "
            "hard function. <bookmark mark='e'/> If some problem solvable in exponential time needs exponentially "
            "large circuits, then P equals BPP: every randomized algorithm can be derandomized with polynomial "
            "slowdown. <bookmark mark='f'/> Hard functions make good coins. Most complexity theorists believe P "
            "equals BPP, and Part 27 follows the argument further."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def pit(self):
        head = label(r"The test we can't derandomize", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"polynomial identity testing: \ is this arithmetic circuit the zero polynomial?", font_size=22,
                  color=WHITE),
            label(r"with coins: \ Schwartz--Zippel, \ chapter 3, \ one evaluation", font_size=21, color=YES),
            label(r"without: \ no polynomial-time algorithm is known", font_size=21, color=NO),
            label(r"Kabanets and Impagliazzo (2004): \ a deterministic PIT would prove circuit lower bounds \ "
                  r"($\mathsf{NEXP} \not\subseteq \mathsf{P/poly}$, \ or the permanent needs large arithmetic "
                  r"circuits)", font_size=20, color=HEAD),
            label(r"so derandomizing it is \textbf{as hard as} proving lower bounds we have sought for 50 years",
                  font_size=21, color=LAM),
            label(r"solved special cases: \ sparse polynomials, \ read-once branching programs (quasi-polynomial), "
                  r"\ depth-3 circuits with few gates", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "And the converse holds too, which is why the question is so hard. <bookmark mark='a'/> Polynomial "
            "identity testing asks whether an arithmetic circuit computes the zero polynomial. <bookmark "
            "mark='b'/> With coins it is easy: evaluate at one random point, chapter three. <bookmark mark='c'/> "
            "Without coins, no polynomial-time algorithm is known. <bookmark mark='d'/> Valentine Kabanets and "
            "Russell Impagliazzo proved in 2004 that a deterministic algorithm would itself prove a circuit lower "
            "bound of a kind complexity theory has sought for fifty years. <bookmark mark='e'/> So removing this "
            "one coin is as hard as the great open problems of lower bounds. <bookmark mark='f'/> Special cases "
            "are solved, such as sparse polynomials and some restricted kinds of circuit, and the matching result "
            "of 2016 came from this line of work."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def sketches(self):
        head = label(r"How small can a sketch be?", font_size=34).to_edge(UP, buff=0.35)
        rows = [
            [r"distinct items, \ $1 \pm \varepsilon$", r"$O(\varepsilon^{-2} + \log n)$ bits",
             r"optimal \ (Kane, Nelson, Woodruff, 2010)"],
            [r"$F_2$, \ $1 \pm \varepsilon$", r"$O(\varepsilon^{-2} \log n)$", r"AMS is optimal up to the log"],
            [r"$F_p$, \ $p > 2$", r"$n^{1 - 2/p}$", r"necessary \ (Bar-Yossef et al., 2002)"],
            [r"point queries, \ $\pm \varepsilon N$", r"$O(\varepsilon^{-1} \log \tfrac1\delta)$ counters",
             r"Count-Min is near optimal"],
            [r"the exact top $k$", r"$\Omega(\text{distinct items})$", r"impossible in small space"],
        ]
        tab = grid_table([r"question", r"space", r"status"], rows, widths=[3.8, 3.6, 5.2], row_h=0.5,
                         font_size=19, mono_cols=(), colors=[[WHITE, YES, GREY_A]] * len(rows)).next_to(head, DOWN,
                                                                                                    buff=0.45)
        tab.set_x(0)
        how = label(r"the lower bounds come from communication complexity: \ a small sketch would let two "
                    r"people solve a problem \\ that provably needs a long conversation \ (Part 27)", font_size=20,
                    color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "For sketches, the theory is unusually complete. <bookmark mark='a'/> Counting distinct items to "
            "within one plus or minus epsilon needs about one over epsilon squared bits, plus log n, and in 2010 "
            "Daniel Kane, Jelani Nelson and David Woodruff matched that exactly. The second moment is similar. "
            "For higher moments, a polynomial amount of space is provably necessary. Count-Min is close to optimal "
            "for estimating single counts, and finding the exact top words in small space is impossible: the "
            "Job's sketch must sometimes be wrong. <bookmark mark='b'/> The lower bounds come from communication "
            "complexity. If a small sketch existed, two people could pass it between them and solve a problem "
            "that provably needs a long conversation. Part 27 proves those."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.6), run_time=7.0)
            vo.wait_until("b")
            self.play(FadeIn(how))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"is $\mathsf{P} = \mathsf{BPP}$? \ can it be proved without proving circuit lower bounds?",
                  font_size=23, color=GREY_A),
            label(r"a deterministic polynomial-time test for polynomial identities", font_size=23, color=GREY_A),
            label(r"an explicit colouring of $K_n$ as good as a random one: \ no one-colour clique of size "
                  r"$2 \log_2 n$", font_size=23, color=GREY_A),
            label(r"perfect matching in NC, \ deterministically, \ for every graph", font_size=23, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the second", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is where things stand. <bookmark mark='a'/> Does P equal BPP, and can that be proved without "
            "first proving circuit lower bounds? <bookmark mark='b'/> Is there a deterministic polynomial-time "
            "test for polynomial identities? <bookmark mark='c'/> Can anyone write down a colouring of a complete "
            "graph that is as good as a random one? Explicit constructions improved dramatically after 2016, with "
            "two-source extractors, but still fall short. <bookmark mark='d'/> And can perfect matchings be found "
            "fast in parallel without coins, for every graph? <bookmark mark='e'/> This part's research problem "
            "takes the second."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
