from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs19.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load,
                                   mono, words)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.omega()
        self.seth()
        self.lower()
        self.open_()

    def card(self):
        card = chapter_card(16, r"Frontier: \ how fast can we multiply?", r"Are these algorithms the last word?",
                            lit=(2024,), extra=((2015, r"edit distance and SETH"), (2019, r"$n \log n$ multiplication"),
                                                (2024, r"$\omega < 2.3714$")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: how fast can we multiply?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def omega(self):
        head = label(r"Is $\omega = 2$?", font_size=36).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"every bound since 1987 comes from Strassen's \textbf{laser method}, \ applied to one small "
                  r"tensor", font_size=21, color=GREY_A),
            label(r"Ambainis, \ Filmus and Le Gall \ (2015): \ that route cannot go below 2.3078", font_size=21,
                  color=NO),
            label(r"Alman and Vassilevska Williams \ (2018): \ limits for a much wider family of methods",
                  font_size=21, color=NO),
            label(r"other routes: \ Cohn and Umans's groups \ (2003); \ \textit{asymmetric} hashing, \ which gave "
                  r"the 2023--24 gains", font_size=21, color=HEAD),
            label(r"if $\omega = 2$: \ linear algebra, \ graph problems \ (triangles, \ transitive closure) \ and "
                  r"parsing all get faster in theory", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The first open question: is omega two? <bookmark mark='a'/> Every improvement since 1987 has applied "
            "Strassen's laser method to powers of one small tensor, Coppersmith and Winograd's. <bookmark "
            "mark='b'/> In 2015 Andris Ambainis, Yuval Filmus and François Le Gall proved that this route cannot "
            "reach below two point three zero seven eight, however far it is pushed. <bookmark mark='c'/> Josh "
            "Alman and Virginia Vassilevska Williams then showed similar limits for a much broader family of "
            "methods. <bookmark mark='d'/> So reaching two needs a new idea: perhaps Henry Cohn and Chris Umans's "
            "approach through group theory, or refinements like the asymmetric hashing behind the most recent "
            "gains. <bookmark mark='e'/> The stakes are wide: matrix multiplication sits inside linear algebra, "
            "finding triangles in graphs, transitive closure and context-free parsing."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def seth(self):
        head = label(r"Why edit distance seems quadratic", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"\textbf{SETH} \ (Impagliazzo and Paturi, \ 2001): \ $k$-SAT needs nearly $2^n$ time as $k$ "
                  r"grows", font_size=21, color=GREY_A),
            label(r"Backurs and Indyk \ (2015): \ edit distance in $O(n^{2 - \varepsilon})$ \ $\Rightarrow$ \ SETH "
                  r"is false", font_size=22, color=NO),
            label(r"the same for LCS and dynamic time warping \ (Abboud, \ Backurs, \ Vassilevska Williams; \ "
                  r"Bringmann and K\"unnemann, \ 2015)", font_size=21, color=NO),
            label(r"a conditional lower bound: \ the best we have, \ since unconditional ones are far out of reach",
                  font_size=21, color=HEAD),
            label(r"but approximately: \ a constant factor in almost linear time \ (Andoni and Nosatzki, \ 2020)",
                  font_size=21, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "The second: can edit distance beat chapter ten's quadratic table? <bookmark mark='a'/> The strong "
            "exponential time hypothesis, of Russell Impagliazzo and Ramamohan Paturi, says that satisfiability "
            "with long clauses needs nearly two to the n time. <bookmark mark='b'/> In 2015 Arturs Backurs and Piotr "
            "Indyk proved that a truly subquadratic algorithm for edit distance would refute it. <bookmark "
            "mark='c'/> The same was soon shown for the longest common subsequence and for dynamic time warping. "
            "<bookmark mark='d'/> These are conditional lower bounds: the best kind available, because proving "
            "unconditional ones for such problems is far beyond current techniques. This is fine-grained "
            "complexity, which Part 27 develops. <bookmark mark='e'/> Approximation escapes the barrier: in 2020 "
            "Alexandr Andoni and Negev Shekel Nosatzki computed edit distance to within a constant factor in "
            "almost linear time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def lower(self):
        head = label(r"Is $n \log n$ the end?", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"the FFT: \ $\frac{n}{2} \lg n$ butterflies; \ no algorithm with $o(n \log n)$ operations is "
                  r"known", font_size=21, color=GREY_A),
            label(r"Morgenstern \ (1973): \ $\Omega(n \log n)$, \ but only for circuits whose constants are bounded",
                  font_size=21, color=HEAD),
            label(r"integer multiplication: \ $\Omega(n \log n)$ \ if the network coding conjecture holds \ "
                  r"(Afshani, \ Freksen, \ Kamma and Larsen, \ 2019)", font_size=21, color=HEAD),
            label(r"unconditionally: \ nothing better than linear is proved for either", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.7)
        with self.voiceover(
            "The third: is n log n the end for the FFT and for multiplication? <bookmark mark='a'/> Nobody knows an "
            "FFT with fewer than order n log n operations. <bookmark mark='b'/> Jacques Morgenstern proved in 1973 "
            "that n log n is necessary, but only for circuits whose constants are bounded, which leaves room for "
            "cleverness with large constants. <bookmark mark='c'/> For integer multiplication, Peyman Afshani, "
            "Casper Freksen, Lior Kamma and Kasper Green Larsen showed in 2019 that n log n is optimal, if a "
            "conjecture about information flow in networks is true. <bookmark mark='d'/> Unconditionally, no lower "
            "bound better than linear is known for either. The algorithms in this part may be optimal; nobody can "
            "prove it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, p in zip("abcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.35)
        qs = VGroup(
            label(r"is $\omega = 2$? \ is there even a practical method below Strassen's 2.807?", font_size=24,
                  color=GREY_A),
            label(r"edit distance in $O(n^{2-\varepsilon})$, \ or a proof of hardness without SETH?", font_size=24,
                  color=GREY_A),
            label(r"does every linear algorithm for the DFT need $\Omega(n \log n)$ operations?", font_size=24,
                  color=GREY_A),
            label(r"which problems have greedy algorithms? \ matroids are not the whole answer", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        star = label(r"$\bigstar$ \ the part's research problem takes the third", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is where things stand. <bookmark mark='a'/> Is omega two, and is there any practical algorithm "
            "faster than Strassen's? <bookmark mark='b'/> Can edit distance be computed in truly subquadratic time, "
            "or can its hardness be proved without assuming SETH? <bookmark mark='c'/> Does every linear algorithm "
            "for the discrete Fourier transform need n log n operations? <bookmark mark='d'/> And which problems "
            "admit greedy algorithms? Matroids explain many, but not all: greedoids and other generalizations "
            "cover more. <bookmark mark='e'/> This part's research problem takes the third."
        ) as vo:
            self.play(FadeIn(head))
            for mk, q in zip("abcd", qs):
                vo.wait_until(mk)
                self.play(FadeIn(q))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
