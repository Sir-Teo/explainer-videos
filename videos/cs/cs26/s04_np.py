from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, mono)


class Np(VoiceoverScene):
    def construct(self):
        self.card()
        self.verifiers()
        self.equivalence()
        self.examples()

    def card(self):
        card = chapter_card(3, r"NP: \ problems with checkable answers", r"What does it mean that an answer is easy to "
                            r"check?", lit=(1971, 2015), extra=((1971, r"Cook"), (2015, r"Babai")), part=PART)
        with self.voiceover("Chapter three. NP: problems with checkable answers."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def verifiers(self):
        head = label(r"A problem is in NP if \textbf{yes}-answers have short, \ checkable proofs", font_size=30).to_edge(
            UP, buff=0.35)
        boxes = VGroup(
            RoundedRectangle(width=2.6, height=1.0, corner_radius=0.1, color=DATA).set_fill(DATA, 0.12),
            RoundedRectangle(width=2.6, height=1.0, corner_radius=0.1, color=HEAD).set_fill(HEAD, 0.12),
            RoundedRectangle(width=2.6, height=1.0, corner_radius=0.1, color=YES).set_fill(YES, 0.12),
        ).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=1.7)
        bl = VGroup(label(r"input $x$", font_size=22, color=DATA).move_to(boxes[0]),
                    label(r"verifier $V$", font_size=22, color=HEAD).move_to(boxes[1]),
                    label(r"accept", font_size=22, color=YES).move_to(boxes[2]))
        cert = VGroup(RoundedRectangle(width=2.6, height=0.8, corner_radius=0.1, color=LAM).set_fill(LAM, 0.12),
                      label(r"certificate $c$", font_size=22, color=LAM))
        cert[1].move_to(cert[0])
        cert.next_to(boxes[1], UP, buff=0.35).shift(LEFT * 2.0)
        arrows = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B),
                        Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.1, color=GREY_B),
                        Arrow(cert.get_right(), boxes[1].get_top() + LEFT * 0.4, buff=0.1, color=LAM))
        defn = VGroup(
            label(r"$x \in L \iff$ \ some certificate $c$ with $|c| \le |x|^k$ makes $V(x, c)$ accept", font_size=23,
                  color=WHITE),
            label(r"and $V$ runs in polynomial time", font_size=23, color=WHITE),
            label(r"3-colouring: \ $c$ = the colours; \ \ SAT: \ $c$ = the assignment; \ \ composite: \ $c$ = a "
                  r"factor", font_size=21, color=DATA),
            label('NP does not require a uniform short-certificate system for no-instances; individual proofs may exist', font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.25).next_to(boxes, DOWN, buff=0.55)
        with self.voiceover(
            "Here is the definition behind finding and checking. <bookmark mark='a'/> A decision language is in NP when each yes-instance has a certificate whose bit length is polynomial in the input length. <bookmark mark='b'/> One deterministic polynomial-time verifier accepts exactly the valid input-certificate pairs, with no accepting certificate for a no-instance. <bookmark mark='c'/> A graph colouring, a satisfying assignment or a Hamiltonian path can supply such a certificate for the corresponding decision problem. <bookmark mark='d'/> NP does not require short certificates for no-instances. That is a statement about the class definition, not a claim that individual no-instances cannot have short proofs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes), FadeIn(bl), FadeIn(cert), LaggedStart(*[GrowArrow(a) for a in arrows],
                                                                            lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(defn[0]), FadeIn(defn[1]))
            vo.wait_until("c")
            self.play(FadeIn(defn[2]))
            vo.wait_until("d")
            self.play(FadeIn(defn[3]))
        self.wait(0.3)
        self.clear_scene()

    def equivalence(self):
        head = label(r"Guessing machines and checkers are the same thing", font_size=32).to_edge(UP, buff=0.35)
        tree = VGroup()
        levels = 4
        pts = {}
        for d in range(levels):
            for i in range(2 ** d):
                x = -5.6 + (i + 0.5) * (5.0 / 2 ** d)
                y = 1.6 - d * 1.0
                pts[(d, i)] = np.array([x, y, 0])
        for (d, i), p in pts.items():
            if d + 1 < levels:
                for c in (2 * i, 2 * i + 1):
                    tree.add(Line(p, pts[(d + 1, c)], stroke_width=1.5, color=GREY_C))
        acc = (levels - 1, 5)
        path = [(d, acc[1] >> (levels - 1 - d)) for d in range(levels)]
        hl = VGroup(*[Line(pts[path[k]], pts[path[k + 1]], stroke_width=4, color=YES) for k in range(levels - 1)])
        leaves = VGroup(*[Dot(pts[(levels - 1, i)], radius=0.09, color=YES if i == acc[1] else NO)
                          for i in range(2 ** (levels - 1))])
        tl = label(r"a nondeterministic machine: \\ every branch a sequence of guesses", font_size=19,
                   color=GREY_A).next_to(tree, DOWN, buff=0.3)
        lines = VGroup(
            label(r"\textbf{NTM $\Rightarrow$ verifier}: \ the certificate is the list of choices on an accepting "
                  r"branch", font_size=21, color=YES),
            label(r"the verifier replays that one branch: \ polynomial time", font_size=21, color=WHITE),
            label(r"\textbf{verifier $\Rightarrow$ NTM}: \ guess the certificate bit by bit, \ then run the verifier",
                  font_size=21, color=HEAD),
            label(r"so NP = ``nondeterministic polynomial time'': \ the name comes from the machine", font_size=21,
                  color=DATA),
            label(r"P $\subseteq$ NP \ (ignore the certificate) \ $\subseteq$ PSPACE \ (try every certificate, "
                  r"reusing space)", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        if lines.width > 7.4:
            lines.width = 7.4
            lines.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The N in NP stands for nondeterministic, and the two views agree. <bookmark mark='a'/> A "
            "nondeterministic machine branches at every choice, and accepts if any branch does. Given such a machine, "
            "the certificate is simply the list of choices along an accepting branch, <bookmark mark='b'/> and a "
            "verifier replays that single branch in polynomial time. <bookmark mark='c'/> Conversely, given a "
            "verifier, a nondeterministic machine guesses the certificate one bit at a time and then runs the "
            "verifier. <bookmark mark='d'/> So NP is exactly nondeterministic polynomial time. <bookmark mark='e'/> "
            "Every problem in P is in NP, since the verifier can ignore the certificate. And NP sits inside "
            "polynomial space, since one machine can try every certificate in turn, reusing the same cells."
        ) as vo:
            self.play(FadeIn(head), Create(tree), FadeIn(leaves), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(hl), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def examples(self):
        head = label('Six decision problems in NP', font_size=34).to_edge(UP, buff=0.35)
        rows = [[r"SAT", r"a Boolean formula", r"an assignment", r"unknown"],
                [r"clique", r"a graph and $k$", r"$k$ vertices", r"unknown"],
                [r"Hamiltonian cycle", r"a graph", r"an ordering of the vertices", r"unknown"],
                [r"subset sum", r"numbers and a target", r"which numbers", r"unknown"],
                [r"graph isomorphism", r"two graphs", r"the matching of vertices", r"quasi-polynomial \ (Babai)"],
                [r"primality", r"a number", r"none needed", r"in P \ (AKS, 2002)"]]
        tab = grid_table([r"problem", r"input", r"certificate", 'known time status'], rows,
                         widths=[2.8, 3.0, 3.6, 3.4], row_h=0.5, font_size=20, mono_cols=(),
                         colors=[[WHITE, GREY_A, YES, NO]] * 4 + [[WHITE, GREY_A, YES, HEAD]] + [[WHITE, GREY_A, YES,
                                                                                              YES]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label('Babai (2015): $\\exp((\\log n)^{O(1)})$ time; polynomial time remains open',
                  font_size=21, color=HEAD),
            label(r"Agrawal, \ Kayal and Saxena \ (2002): \ primality is in P, \ by a deterministic test", font_size=21,
                  color=YES),
            label('unknown = polynomial-time decision is unknown; binary input size and problem-specific bounds matter', font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Consider six decision problems. <bookmark mark='a'/> SAT, clique, Hamiltonian cycle and binary-encoded subset sum have polynomially checkable yes-certificates. For these general problems, polynomial-time algorithms remain unknown. This is not a claim that every best known algorithm has the same exponential bound. <bookmark mark='b'/> Graph isomorphism asks for an adjacency-preserving bijection. Babai's quasipolynomial upper bound is faster than a general exponential bound, while polynomial time remains open. <bookmark mark='c'/> Primality is in P by the AKS theorem, so it needs no extra certificate for polynomial-time decision. <bookmark mark='d'/> A verifier can always exhaust all polynomial-length certificates using exponential time. That is an upper bound, not a proof that exhaustive search is necessary."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:5]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[5])), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[6])), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
