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
        with self.voiceover((
            'Chapter sixteen. Frontier: does randomness help?'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def derandomized(self):
        head = label(r"Coins that were removed", font_size=34).to_edge(UP, buff=0.35)
        rows = [
            [r"primality", r"Miller--Rabin \ (1976--80)", r"AKS \ (2002)"],
            [r"undirected connectivity in log space", r"a random walk", r"Reingold \ (2005)"],
            [r"minimum cut, \ near-linear time", r"Karger \ (2000)", r"Kawarabayashi--Thorup \ (2015); \ "
                                                                    r"Henzinger, \ Li, \ Rao, \ Wang \ (2024)"],
            [r"bipartite matching, \ in parallel", r"Tutte matrix \ (1979--87)", r"quasi-NC squared: \ Fenner, \ Gurjar, \ "
                                                                                r"Thierauf \ (2016)"],
        ]
        tab = grid_table([r"problem", r"with coins", r"without"], rows, widths=[4.4, 3.4, 5.2], row_h=0.62,
                         font_size=19, mono_cols=(), colors=[[WHITE, LAM, YES]] * len(rows)).next_to(head, DOWN,
                                                                                                buff=0.5)
        tab.set_x(0)
        note_ = label(r"each took decades, \ and none was a general method", font_size=22, color=HEAD
                      ).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            (
            "Several problems now have deterministic alternatives. <bookmark mark='a'/> AKS gave polynomial-time "
            'primality in 2002. Reingold gave logarithmic-space undirected connectivity in 2005. Kawarabayashi and '
            'Thorup gave a deterministic near-linear minimum-cut result for simple graphs in 2015; Henzinger, Li, '
            "Rao and Wang reported the weighted-graph extension in 2024. Fenner, Gurjar and Thierauf's 2016 "
            'bipartite perfect-matching result is quasi-NC squared: quasi-polynomial size and polylogarithmic depth,'
            " not an NC algorithm. <bookmark mark='b'/> These are different models and individual achievements. Is "
            'there a general route for bounded-error decision algorithms?'
        )
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
            label(r"BPP: \ polynomial-time decision, \ error $\le1/3$ on every input", font_size=21, color=GREY_A),
            label(r"efficient PRG: \ logarithmic seed; \ fools all circuits of the required polynomial size",
                  font_size=20, color=WHITE),
            label(r"enumerate polynomially many seeds; \ acceptance majority preserves the decision gap",
                  font_size=20, color=LAM),
            label(r"Nisan--Wigderson (1994); \ Impagliazzo--Wigderson (1997)", font_size=20, color=WHITE),
            MathTex(r"\mathsf E=\mathrm{DTIME}(2^{O(n)}),\quad"
                    r"\exists f\in\mathsf E:\mathrm{CircuitSize}(f_n)\ge2^{\Omega(n)}\ \Longrightarrow\ \mathsf P=\mathsf{BPP}",
                    font_size=29, color=YES),
            label(r"conditional decision simulation; \ arbitrary sampling and search need separate guarantees",
                  font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.23).next_to(head, DOWN, buff=0.3)
        boxes = VGroup()
        for title,subtitle,color in [(r"seed $s$",r"$O(\log n)$ bits",DATA),(r"generator $G$",r"poly$(n)$ random bits",LAM),
                                    (r"decision circuit",r"fixed input $x$",CTRL),(r"majority",r"over every seed",YES)]:
            frame = RoundedRectangle(width=2.6,height=0.95,corner_radius=0.12,stroke_color=color,fill_color=color,fill_opacity=0.10)
            content = VGroup(label(title,font_size=22,color=color),label(subtitle,font_size=17,color=GREY_A)).arrange(DOWN,buff=0.1).move_to(frame)
            boxes.add(VGroup(frame,content))
        boxes.arrange(RIGHT,buff=0.48).to_edge(DOWN,buff=0.65)
        arrows = VGroup(*[Arrow(a.get_right(),b.get_left(),buff=0.07,color=GREY_B,stroke_width=2,
                                max_tip_length_to_length_ratio=0.18) for a,b in zip(boxes,boxes[1:])])
        with self.voiceover(
            (
            "There is a conditional route. <bookmark mark='a'/> BPP consists of decision problems solvable in "
            "polynomial time with error at most one third on every input. <bookmark mark='b'/> For an input length, "
            'imagine an efficiently computable generator with logarithmic seed length that fools every circuit of '
            'the required polynomial size to sufficiently small additive advantage. Its output supplies the '
            "algorithm's polynomially many random bits. <bookmark mark='c'/> Enumerate all seeds and take the "
            'majority of acceptance decisions. The seed count is polynomial, and fooling preserves the acceptance '
            'gap. This is a decision simulation, not a promise to reproduce arbitrary sampling or search tasks. '
            "<bookmark mark='d'/> Nisan–Wigderson and Impagliazzo–Wigderson connect such generators to circuit "
            "hardness. <bookmark mark='e'/> The 1997 sufficient premise is a language in E, deterministic time two "
            'to order n, requiring exponential-size Boolean circuits. Under that premise, P equals BPP. Arbitrary '
            "exponential-time hardness is not the same stated premise. <bookmark mark='f'/> Hard functions can "
            'produce pseudorandom bits for bounded computations. The unconditional equality P equals BPP remains '
            'open.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(arrows))
            for mk, p in zip("abcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
                if mk == "c":
                    self.play(Indicate(boxes[-1], color=YES))
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
            label(r"integer PIT derandomization implies one of these lower bounds; \ a specific implication",
                  font_size=21, color=LAM),
            label(r"solved special cases: \ sparse polynomials, \ read-once branching programs (quasi-polynomial), "
                  r"\ depth-3 circuits with few gates", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            (
            "Derandomization also implies hardness in important settings. <bookmark mark='a'/> Polynomial identity "
            "testing asks whether an arithmetic circuit computes the zero formal polynomial. <bookmark mark='b'/> "
            'Random evaluation gives a bounded-error test when the field, degree and evaluation set satisfy the '
            "required conditions. <bookmark mark='c'/> General deterministic polynomial-time identity testing "
            "remains open. <bookmark mark='d'/> Kabanets and Impagliazzo showed in 2004 that deterministic "
            'polynomial-time identity testing over the integers implies a major lower bound: either NEXP lacks '
            'polynomial-size Boolean circuits, or the permanent lacks polynomial-size arithmetic circuits. <bookmark'
            " mark='e'/> This is a specific implication, not an unconditional equivalence between every form of "
            "hardness and derandomization. <bookmark mark='f'/> Restricted circuit classes admit progress. The 2016 "
            'bipartite matching quasi-NC result uses related isolation ideas, with quasi-polynomial size still '
            'present.'
        )
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
            [r"distinct, \ insertion-only $[n]$", r"$O(\varepsilon^{-2}+\log n)$ bits", r"constant success, e.g. $2/3$; \ KNW 2010"],
            [r"$F_2$, \ relative approximation", r"AMS counters + confidence groups", r"space depends on bits and success target"],
            [r"higher moments, \ $p>2$", r"polynomial dependence on universe", r"model and approximation must be fixed"],
            [r"fixed-item Count-Min query", r"$O(\varepsilon^{-1}\log(1/\delta))$ counters", r"insertion-only; \ independent row hashes"],
            [r"exact unrestricted top items", r"can require growing space", r"our fixed candidate heap is empirical"],
        ]
        tab = grid_table([r"question", r"space", r"status"], rows, widths=[3.8, 3.6, 5.2], row_h=0.5,
                         font_size=19, mono_cols=(), colors=[[WHITE, YES, GREY_A]] * len(rows)).next_to(head, DOWN,
                                                                                                    buff=0.45)
        tab.set_x(0)
        how = label(r"the lower bounds come from communication complexity: \ a small sketch would let two "
                    r"people solve a problem \\ that provably needs a long conversation \ (Part 27)", font_size=20,
                    color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            (
            "Streaming space bounds require a model. <bookmark mark='a'/> For insertion-only distinct counting over "
            "a universe of size n, Kane, Nelson and Woodruff's 2010 result uses order epsilon to the minus two plus "
            'log n bits, with a fixed constant success probability such as two thirds. Raising confidence has '
            'additional cost. Bounds for other moments and point queries depend on the moment, update model, '
            'approximation and failure probability. Exact unrestricted top-item recovery can require space growing '
            "with the input universe; no theorem here makes our candidate heap exact. <bookmark mark='b'/> "
            'Communication reductions explain many lower bounds: if a tiny sketch solved the streaming problem, two '
            'parties could exchange it to solve a communication problem with a proved larger cost. Part 27 develops '
            'this argument.'
        )
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
            (
            "Here is where things stand. <bookmark mark='a'/> Does P equal BPP, and can that be proved without first"
            " proving circuit lower bounds? <bookmark mark='b'/> Is there a deterministic polynomial-time test for "
            "polynomial identities? <bookmark mark='c'/> Can anyone write down a colouring of a complete graph that "
            'is as good as a random one? Explicit constructions improved dramatically after 2016, with two-source '
            "extractors, but still fall short. <bookmark mark='d'/> And can perfect matchings be found fast in "
            "parallel without coins, for every graph? <bookmark mark='e'/> This part's research problem takes the "
            'second.'
        )
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
