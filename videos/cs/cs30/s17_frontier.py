from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs30.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.breaks()
        self.lattice_doubt()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ post-quantum and beyond", r"What is still unknown about public keys?",
                            lit=(2022, 2024, 2025), extra=((2022, r"SIKE and Rainbow broken"),
                                                           (2024, r"a quantum LWE claim, \ withdrawn"),
                                                           (2025, r"HQC chosen")), part=PART)
        with self.voiceover("Chapter sixteen. The frontier: post-quantum, and beyond."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def breaks(self):
        head = label(r"New assumptions, \ new breaks", font_size=34).to_edge(UP, buff=0.3)
        tab = grid_table([r"family", r"example", r"status"], [
            [r"lattices", r"ML-KEM, \ ML-DSA", r"standardised, \ 2024"],
            [r"hash functions", r"SLH-DSA", r"standardised, \ 2024"],
            [r"codes \ (Part 28)", r"HQC, \ Classic McEliece", r"HQC chosen as a backup, \ 2025"],
            [r"multivariate", r"Rainbow", r"broken \ (Beullens, 2022): \ a weekend on a laptop"],
            [r"isogenies", r"SIKE", r"broken \ (Castryck and Decru, 2022): \ an hour on one core"],
        ], widths=[2.6, 3.4, 5.6], row_h=0.55, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for r in (4, 5):
            tab.cells[r][2].set_color(NO)
        for r in (1, 2, 3):
            tab.cells[r][2].set_color(YES)
        lines = VGroup(
            label(r"SIKE had just entered the fourth round of NIST's process; \ it fell to a 1997 theorem about curves",
                  font_size=21, color=WHITE),
            label(r"the lesson: \ assumptions earn trust only by surviving years of attack; \ so deploy "
                  r"\textbf{hybrids}, \ and keep a diverse backup", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Post-quantum cryptography rests on younger assumptions, and some have not survived. <bookmark mark='a'/> "
            "Lattices and hash functions became standards in 2024. In 2025 a code-based scheme, HQC, built on Part 28's "
            "mathematics, was chosen as a backup with a different foundation. <bookmark mark='b'/> But in 2022 two "
            "leading candidates fell. Ward Beullens broke the Rainbow signature scheme with a weekend on a laptop. Wouter "
            "Castryck and Thomas Decru broke SIKE, based on maps between elliptic curves, in about an hour on one core, "
            "using a theorem from 1997 that nobody had connected to it. <bookmark mark='c'/> The lesson is old: an "
            "assumption earns trust only by surviving years of attack. That is why new systems combine a classical "
            "and a post-quantum algorithm, and why the standards keep backups built on different mathematics."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1], *tab.cells[2], *tab.cells[3])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[4], *tab.cells[5])), FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def lattice_doubt(self):
        head = label(r"How hard are lattices, \ really?", font_size=34).to_edge(UP, buff=0.3)
        lines = VGroup(
            label(r"security levels come from \textbf{estimates}: \ the best lattice-reduction attacks \ (BKZ, \ sieving) "
                  r"\ extrapolated to large dimension", font_size=22, color=WHITE),
            label(r"the estimates have moved: \ better sieves shaved bits in the 2010s and 2020s", font_size=22,
                  color=HEAD),
            label(r"April 2024: \ a preprint claimed a quantum polynomial-time algorithm for LWE", font_size=22,
                  color=NO),
            label(r"within ten days, \ a bug was found, \ and the claim withdrawn: \ the field held its breath", font_size=22,
                  color=YES),
            label(r"no proof says lattice problems resist quantum computers; \ only that nobody has found the way",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Even lattices carry uncertainty. <bookmark mark='a'/> Their security levels are estimates: the best known "
            "reduction attacks, extrapolated to hundreds of dimensions. <bookmark mark='b'/> Those estimates have moved, "
            "as better sieving algorithms took bits off the security of every scheme. <bookmark mark='c'/> In April 2024 "
            "a preprint claimed a quantum algorithm solving learning with errors in polynomial time, which would have "
            "broken the new standards before they were published. <bookmark mark='d'/> Within ten days, readers found "
            "a bug, and the claim was withdrawn. <bookmark mark='e'/> Nothing proves that lattice problems resist "
            "quantum computers. As with factoring before Shor, we know only that nobody has found a way."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ Can factoring or discrete logarithms be solved in classical polynomial time?", font_size=22,
                  color=WHITE),
            label(r"2. \ Public-key encryption from one-way functions alone? \ (black-box methods cannot do it)",
                  font_size=22, color=WHITE),
            label(r"3. \ Is there a quantum algorithm for the lattice problems under ML-KEM?", font_size=22,
                  color=WHITE),
            label(r"4. \ Are there attacks on prime-order elliptic curves better than rho?", font_size=22,
                  color=WHITE),
            label(r"5. \ How fast does the concrete hardness of LWE grow with dimension?", font_size=22, color=WHITE),
            label(r"6. \ Can computing on encrypted data become nearly as cheap as computing in the clear?",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes a small case of the fifth", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Six open problems. <bookmark mark='a'/> Whether factoring or discrete logarithms can be solved in "
            "polynomial time by an ordinary computer. <bookmark mark='b'/> Whether public-key encryption can be built "
            "from any one-way function, as everything in Part 29 was; Impagliazzo and Rudich showed in 1989 that the "
            "standard black-box techniques cannot. <bookmark mark='c'/> Whether a quantum algorithm breaks the lattice "
            "problems under the new standards. <bookmark mark='d'/> Whether well-chosen elliptic curves have any attack "
            "better than the generic square root. <bookmark mark='e'/> How quickly the concrete difficulty of learning "
            "with errors grows as the dimension does, which is what sets every post-quantum key size. <bookmark "
            "mark='f'/> And whether computing on encrypted data can ever be nearly as cheap as computing in the clear. "
            "<bookmark mark='g'/> This part's research problem takes a small, computable case of the fifth."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcdef", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("g")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
