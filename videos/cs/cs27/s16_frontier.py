from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.ladder()
        self.mipstar()
        self.practice()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ MIP* = RE \ and proofs in practice",
                            r"What can a verifier check, \ and how cheaply?", lit=(1988, 2020),
                            extra=((1991, r"MIP = NEXP"), (2016, r"Groth16"), (2020, r"MIP* = RE")), part=PART)
        with self.voiceover("Chapter fifteen. The frontier: MIP star equals RE, and proofs in practice."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ladder(self):
        head = label(r"More provers, \ more power", font_size=34).to_edge(UP, buff=0.3)
        rungs = [
            (r"NP", r"read a proof", r"Part 26", DATA),
            (r"IP = PSPACE", r"question one prover, \ with coins", r"Shamir, 1990", YES),
            (r"MIP = NEXP", r"question \textbf{two} provers \\ who cannot talk to each other", r"Babai, \ Fortnow, \ "
             r"Lund, 1991", HEAD),
            (r"MIP* = RE", r"two provers who share \\ \textbf{quantum entanglement}", r"Ji, \ Natarajan, \ Vidick, \\ "
             r"Wright, \ Yuen, 2020", NO),
        ]
        rows = VGroup()
        for i, (cls, how, who, col) in enumerate(rungs):
            box = RoundedRectangle(width=3.2, height=0.8, corner_radius=0.12, stroke_color=col, stroke_width=2.5,
                                   fill_color=col, fill_opacity=0.12)
            c = label(cls, font_size=24, color=col).move_to(box)
            h = label(how, font_size=19, color=WHITE)
            w = label(who, font_size=17, color=GREY_A)
            row = VGroup(VGroup(box, c), h, w)
            h.next_to(box, RIGHT, buff=0.5)
            w.next_to(box, RIGHT, buff=5.0)
            rows.add(row)
        rows.arrange(UP, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        for r in rows:
            r[1].next_to(r[0], RIGHT, buff=0.5)
            r[2].next_to(r[0], RIGHT, buff=5.2)
        arrows = VGroup(*[Arrow(rows[i][0].get_top(), rows[i + 1][0].get_bottom(), buff=0.05, color=GREY_B,
                                stroke_width=2.5, max_tip_length_to_length_ratio=0.3) for i in range(3)])
        note = label(r"RE: \ everything a program can \textbf{confirm}, \ including ``this program halts'' "
                     r"\ (Part 25)", font_size=21, color=NO).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "These proof models give a chain of class inclusions; not every adjacent inclusion is known to be strict. <bookmark mark='a'/> Ordinary polynomial-time witness verification gives NP. <bookmark mark='b'/> Polynomial-round randomized interaction with one unbounded prover gives IP, equal to PSPACE. <bookmark mark='c'/> Multiple classical provers who cannot communicate during the protocol give MIP, equal to NEXP. Their strategies can be agreed beforehand. <bookmark mark='d'/> Entangled provers change the class dramatically. The MIP-star theorem, first announced in 2020, gives equality with the recursively enumerable languages. <bookmark mark='e'/> A classical polynomial-time verifier can check an appropriate interaction encoding halting, while the provers may need unbounded finite-dimensional resources. This does not give a uniform algorithm deciding halting; the theorem’s completeness and soundness quantifiers remain essential."
        ) as vo:
            self.play(FadeIn(head))
            for i, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(rows[i], shift=UP * 0.1)]
                if i:
                    anims.append(GrowArrow(arrows[i - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def mipstar(self):
        head = label(r"Why MIP* = RE matters beyond computer science", font_size=32).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"the verifier checks the provers' answers for \textbf{non-local} correlations, \ like a Bell "
                  r"test \ (Part 53)", font_size=22, color=WHITE),
            label(r"entanglement lets honest provers win games no classical pair can: \ and lets cheaters too",
                  font_size=22, color=GREY_A),
            label(r"the proof \textbf{compresses} the verifier: \ games recursively checking larger games, \ a "
                  r"computation of unbounded length", font_size=22, color=HEAD),
            label(r"consequence: \ \textbf{Tsirelson's problem} has a negative answer: \ two models of quantum "
                  r"correlations differ", font_size=22, color=DATA),
            label(r"and \textbf{Connes' embedding conjecture} \ (1976), \ a question about operator algebras, \ is "
                  r"false", font_size=22, color=NO),
            label('MIP* = RE: cited theorem and consequences; full proof not reproduced here',
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The result has consequences for mathematical models of quantum correlations. <bookmark mark='a'/> The verifier asks separated provers questions and tests their answer correlations. The permitted entanglement helps honest strategies but also enlarges the cheating strategies covered by soundness. <bookmark mark='b'/> The tensor-product model allows finite-dimensional entangled resources without a computable uniform dimension bound sufficient for all instances. <bookmark mark='c'/> Recursive compression links games checking games to computations of unbounded duration. We describe this architecture without reproducing the full proof. <bookmark mark='d'/> The theorem separates the closure of finite-dimensional tensor-product correlations from the commuting-operator correlation model, yielding a negative answer to the relevant Tsirelson problem. <bookmark mark='e'/> Through known equivalences it also refutes Connes’ embedding conjecture. <bookmark mark='f'/> Our source reading includes the abstract and stated consequences of the October 2026 arXiv revision. The theorem is cited from that literature, not established by this episode’s small classical simulations."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def practice(self):
        head = label(r"Proofs in practice: \ succinct arguments", font_size=32).to_edge(UP, buff=0.3)
        steps = [(r"computation", r"a program, \\ a circuit", DATA),
                 (r"arithmetize", r"polynomials \\ over a field", HEAD),
                 (r"sum-check / PCP", r"chapters 6 and 8", YES),
                 (r"commit", 'PCS / oracle commitments', LAM),
                 (r"Fiat--Shamir", r"hash replaces \\ the verifier's coins", CTRL)]
        boxes = VGroup()
        for t, s, c in steps:
            b = RoundedRectangle(width=2.2, height=1.3, corner_radius=0.12, stroke_color=c, stroke_width=2.5)
            boxes.add(VGroup(b, label(t, font_size=19, color=c).move_to(b.get_center() + UP * 0.28),
                             label(s, font_size=15, color=GREY_A).move_to(b.get_center() + DOWN * 0.25)))
        boxes.arrange(RIGHT, buff=0.38).next_to(head, DOWN, buff=0.5)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.04, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.35) for i in range(4)])
        lines = VGroup(
            label('proof size, verifier work and setup depend on the system, security parameters and public input', font_size=21, color=WHITE),
            label(r"Kilian \ (1992), \ Micali \ (1994): \ PCPs plus hashing; \ GKR \ (2008): \ sum-check for "
                  r"delegating computation", font_size=21, color=GREY_A),
            label(r"Groth \ (2016): \ three group elements; \ Zcash \ (2016) \ made them zero-knowledge payments",
                  font_size=21, color=HEAD),
            label('validity rollups: aggregate argument; optimistic rollups use dispute mechanisms',
                  font_size=21, color=YES),
            label(r"\textbf{zkVMs}: \ proofs that a whole RISC-V program ran correctly \ (Part 6's machine, "
                  r"certified)", font_size=21, color=DATA),
            label(r"the cost: \ the prover is still orders of magnitude slower than running the program", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).next_to(boxes, DOWN, buff=0.45)
        with self.voiceover(
            "Practical proof systems combine several ingredients with distinct security assumptions. <bookmark mark='a'/> Arithmetize a specified bounded computation into field constraints. Some systems use sum-check or related interactive oracle proofs to reduce verification work. <bookmark mark='b'/> Commitments bind the prover to the relevant polynomials or oracles; the commitment scheme determines important assumptions and costs. <bookmark mark='c'/> Fiat–Shamir removes interaction only for suitable protocols under an appropriate analysis, often in a random-oracle model. A fixed real hash is an instantiation rather than an unconditional theorem. <bookmark mark='d'/> Groth16 has constant-size proofs in group elements under its algebraic assumptions and structured setup. Transparent systems use different assumptions and typically different proof-size trade-offs. <bookmark mark='e'/> Validity rollups can aggregate transaction verification into such arguments; optimistic rollups follow a different dispute-based mechanism. <bookmark mark='f'/> A zkVM proves a bounded execution according to an encoded machine and constraints. Zero knowledge is an additional property and must not be inferred from succinctness alone. <bookmark mark='g'/> Proof size and verifier work depend on the system, security parameters and public input. Prover overhead can be substantial. None of our small teaching protocols is presented as a deployed secure proof system."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.4),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.4), run_time=5.0)
            for mk, ln in zip("bcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ Is P = BPP? \ Can it be proved without proving circuit lower bounds?", font_size=22,
                  color=WHITE),
            label(r"2. \ Is the Unique Games Conjecture true?", font_size=22, color=WHITE),
            label('3. How do specified SETH, 3SUM and APSP variants relate through reductions?', font_size=22,
                  color=WHITE),
            label(r"4. \ VP vs VNP: \ does the permanent need superpolynomial \textbf{algebraic} circuits?",
                  font_size=22, color=WHITE),
            label(r"5. \ Can one-way functions be built from the hardness of an NP-complete problem?",
                  font_size=22, color=WHITE),
            label(r"6. \ How sound can the simplest tests be? \ The exact rejection curve of linearity testing",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the sixth", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here are the broader questions behind the examples. <bookmark mark='a'/> Does randomness increase the power of polynomial-time computation, and what new hardness results would derandomization imply? <bookmark mark='b'/> What is the status of the precise near-satisfiable Unique Games promise? <bookmark mark='c'/> How do the stated variants of SETH, 3SUM and APSP relate through fine-grained reductions? We do not assert an equivalence between them. <bookmark mark='d'/> Over a suitable field, such as characteristic zero, does the permanent require superpolynomial arithmetic circuits? Characteristic two is different because signs vanish and permanent equals determinant. <bookmark mark='e'/> Can useful average-case cryptographic hardness be derived from standard worst-case assumptions through suitable reductions? The reduction model matters. <bookmark mark='f'/> How do exact local-test soundness bounds behave as the dimension grows? Our exhaustive four-bit BLR computation settles only that finite domain. <bookmark mark='g'/> The research exercise starts with complete finite witnesses, then asks which general patterns can actually be proved."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
