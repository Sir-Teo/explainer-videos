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
            "Each new kind of verifier has reached a larger class. <bookmark mark='a'/> Reading a proof gives NP. "
            "<bookmark mark='b'/> Questioning one prover with random coins gives PSPACE, chapter six's theorem. "
            "<bookmark mark='c'/> In 1988 Michael Ben-Or, Shafi Goldwasser, Joe Kilian and Avi Wigderson asked: what "
            "if there are two provers, questioned separately, like suspects in different rooms? László Babai, Lance "
            "Fortnow and Carsten Lund showed in 1991 that this reaches nondeterministic exponential time. It was the "
            "seed of the PCP theorem. <bookmark mark='d'/> Then the provers were allowed to share quantum "
            "entanglement. In 2020 Zhengfeng Ji, Anand Natarajan, Thomas Vidick, John Wright and Henry Yuen proved "
            "that the class jumps all the way to RE. <bookmark mark='e'/> A verifier who runs in polynomial time can "
            "be convinced that a program halts, a question no algorithm can decide."
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
            label(r"a 200-page proof from complexity theory settled a 45-year-old problem in pure mathematics",
                  font_size=22, color=YES),
        ).arrange(DOWN, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The result reached far beyond complexity theory. <bookmark mark='a'/> The verifier tests whether the "
            "provers' answers show correlations that only entanglement can produce, the kind of Bell test Part 53 "
            "describes. <bookmark mark='b'/> Entanglement helps honest provers, but it also helps cheaters, which is "
            "what makes these games hard to analyse. <bookmark mark='c'/> The key step compresses verifiers: a game "
            "that checks a larger game, which checks a larger one, so that a finite conversation certifies an "
            "unbounded computation. <bookmark mark='d'/> As a consequence, Tsirelson's problem in physics has a "
            "negative answer: two natural mathematical models of quantum correlations are different. <bookmark "
            "mark='e'/> And Alain Connes's embedding conjecture of 1976, a central question about operator algebras, "
            "is false. <bookmark mark='f'/> A long proof about interactive proofs settled a problem in pure "
            "mathematics."
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
                 (r"commit", r"to polynomials \\ (KZG, \ FRI)", LAM),
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
            label(r"the output: \ a proof of a few hundred bytes, \ checked in milliseconds, \ however long the "
                  r"computation", font_size=21, color=WHITE),
            label(r"Kilian \ (1992), \ Micali \ (1994): \ PCPs plus hashing; \ GKR \ (2008): \ sum-check for "
                  r"delegating computation", font_size=21, color=GREY_A),
            label(r"Groth \ (2016): \ three group elements; \ Zcash \ (2016) \ made them zero-knowledge payments",
                  font_size=21, color=HEAD),
            label(r"\textbf{rollups}: \ thousands of transactions executed off-chain, \ one proof checked on-chain",
                  font_size=21, color=YES),
            label(r"\textbf{zkVMs}: \ proofs that a whole RISC-V program ran correctly \ (Part 6's machine, "
                  r"certified)", font_size=21, color=DATA),
            label(r"the cost: \ the prover is still orders of magnitude slower than running the program", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).next_to(boxes, DOWN, buff=0.45)
        with self.voiceover(
            "Meanwhile, interactive proofs went into production. <bookmark mark='a'/> The recipe: write a "
            "computation as a circuit, turn the circuit into polynomials, check them with sum-check or a PCP, commit "
            "to the polynomials cryptographically, and replace the verifier's random coins with a hash of the "
            "transcript, the trick of Amos Fiat and Adi Shamir. <bookmark mark='b'/> The result is a proof of a few "
            "hundred bytes that anyone can check in milliseconds, however long the computation was. <bookmark "
            "mark='c'/> Joe Kilian and Silvio Micali saw this in the 1990s; Goldwasser, Kalai and Rothblum built "
            "delegation on sum-check in 2008. <bookmark mark='d'/> Jens Groth's 2016 system needs just three group "
            "elements, and Zcash used such proofs the same year for private payments. <bookmark mark='e'/> Rollups "
            "execute thousands of transactions elsewhere and post one proof. <bookmark mark='f'/> Zero-knowledge "
            "virtual machines prove that an entire RISC-V program ran correctly. <bookmark mark='g'/> The catch is "
            "the prover, still orders of magnitude slower than simply running the program; making it fast is an "
            "active race."
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
            label(r"3. \ Are SETH, \ 3SUM and APSP related? \ No reduction between them is known", font_size=22,
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
            "Six open problems. <bookmark mark='a'/> Whether randomness ever helps polynomial-time computation, and "
            "whether that can be shown without first proving circuit lower bounds, which Kabanets and Impagliazzo "
            "showed is nearly unavoidable. <bookmark mark='b'/> Whether the Unique Games Conjecture is true. "
            "<bookmark mark='c'/> How the three fine-grained conjectures relate: no reduction between any two is "
            "known. <bookmark mark='d'/> Valiant's algebraic version of P versus NP: does the permanent need "
            "algebraic circuits of superpolynomial size? <bookmark mark='e'/> Whether cryptography can rest on an "
            "NP-complete problem. <bookmark mark='f'/> And how sound the simplest tests can be: the exact rejection "
            "curve of the linearity test, whose start we measured in chapter eight. <bookmark mark='g'/> This part's "
            "research problem takes a small, computable case of the sixth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
