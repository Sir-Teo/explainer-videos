from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, mono)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.rings()
        self.rationals()
        self.unknowns()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ Hilbert's tenth over other rings", r"Which number systems can a machine "
                            r"solve equations in?", lit=(1978, 2025),
                            extra=((1978, r"Denef--Lipshitz"), (2024, r"Koymans--Pagano")), part=PART)
        with self.voiceover("Chapter fifteen, the frontier. Hilbert's tenth problem over other rings."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rings(self):
        head = label(r"Settled in 2024--25: \ every ring of integers", font_size=32).to_edge(UP, buff=0.35)
        ex = VGroup(
            MathTex(r"\mathbb{Z}[i] = \{a + bi\}", font_size=32, color=DATA),
            MathTex(r"\mathbb{Z}[\sqrt 2] = \{a + b\sqrt 2\}", font_size=32, color=DATA),
            MathTex(r"\mathbb{Z}[\sqrt[3]{2}],\ \mathbb{Z}[\zeta_7],\ \ldots", font_size=32, color=DATA),
        ).arrange(RIGHT, buff=0.7).next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            label(r"the question: \ do polynomial equations with coefficients in $\mathcal{O}_K$ have solutions in "
                  r"$\mathcal{O}_K$?", font_size=21, color=WHITE),
            label(r"the strategy \ (Denef and Lipshitz, \ 1978): \ show $\mathbb{Z}$ is \textbf{Diophantine} inside "
                  r"$\mathcal{O}_K$, \ then use Matiyasevich", font_size=21, color=GREY_A),
            label('earlier all-field result conditional on Shafarevich-group finiteness (Mazur--Rubin, 2010)', font_size=21, color=GREY_A),
            label(r"Koymans and Pagano \ (December 2024): \ \textbf{unconditionally}, \ for every number field", font_size=22,
                  color=HEAD),
            label(r"their tool: \ elliptic curves that gain no rank in a quadratic extension, \ found with additive "
                  r"combinatorics \ (Green--Tao)", font_size=21, color=LAM),
            label(r"independently: \ Alp\"oge, \ Bhargava, \ Ho and Shnidman \ (2025), \ by a different route",
                  font_size=21, color=DATA),
            label('infinite commutative unital rings finitely generated as $\\mathbb Z$-algebras; effective presentations', font_size=22, color=NO),
        ).arrange(DOWN, buff=0.24).next_to(ex, DOWN, buff=0.4)
        with self.voiceover(
            "Hilbert's tenth extends to effectively presented rings of integers. <bookmark mark='a'/> For a number field K, ask for solutions in its ring of integers, with coefficients in that ring. <bookmark mark='b'/> A Diophantine definition of the ordinary integers transfers undecidability. <bookmark mark='c'/> Earlier all-field conditional results used conjectural finiteness of Shafarevich groups, not merely an unspecified elliptic-curve claim. <bookmark mark='d'/> Koymans and Pagano's December 2024 work gives an unconditional result for every number field. <bookmark mark='e'/> Their tools include elliptic rank stability and additive combinatorics. <bookmark mark='f'/> Independently, Alpoge, Bhargava, Ho and Shnidman's 2025 work uses positive-rank abelian varieties stable in quadratic extensions. The two routes should not be conflated. <bookmark mark='g'/> Combined with earlier reductions, Hilbert's tenth is undecidable over every infinite commutative unital ring finitely generated as a Z algebra, with an effective presentation."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.3))
            for mk, ln in zip("abcdefg", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def rationals(self):
        head = label(r"Still open: \ the rational numbers", font_size=32).to_edge(UP, buff=0.35)
        eq = MathTex(r"y^2 = x^3 - 2 \quad\text{over } \mathbb{Q}:\ \ (3, 5),\ \left(\tfrac{129}{100}, "
                     r"\tfrac{383}{1000}\right),\ \ldots", font_size=34, color=HEAD).next_to(head, DOWN, buff=0.45)
        lines = VGroup(
            label(r"over $\mathbb{Q}$ every equation in many unknowns is a question about rational points: \ "
                  r"\textbf{arithmetic geometry}", font_size=21, color=WHITE),
            label(r"if $\mathbb{Z}$ were Diophantine in $\mathbb{Q}$, \ the problem would be undecidable, \ as "
                  r"before", font_size=21, color=GREY_A),
            label(r"Mazur's conjecture \ (1992) \ would forbid that: \ rational points can't be that scattered",
                  font_size=21, color=LAM),
            label('Koenigsmann: universal definition; DIFFERENT $\\forall\\exists$ definition with one universal variable', font_size=21, color=DATA),
            label(r"so the full theory of $\mathbb{Q}$ is undecidable, \ but the purely existential part may not "
                  r"be: \ nobody knows", font_size=21, color=YES),
            label(r"the same question for \textbf{one} equation in \textbf{two} unknowns over $\mathbb{Z}$ is open "
                  r"too", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.27).next_to(eq, DOWN, buff=0.45)
        with self.voiceover(
            "Hilbert's tenth over the rationals remains a separate question. <bookmark mark='a'/> The displayed rational points satisfy y squared equals x cubed minus two; their exact fraction identities can be checked directly. <bookmark mark='b'/> A Diophantine definition of integers in rationals would transfer integer undecidability. <bookmark mark='c'/> Mazur's topological conjecture would obstruct such a definition; it does not itself give a decision algorithm. <bookmark mark='d'/> Integers ARE first-order definable in rationals. Koenigsmann gives a universal definition, and a DIFFERENT forall-exists definition with only one universally quantified variable. These are distinct quantifier claims. <bookmark mark='e'/> Thus the full first-order theory is undecidable, while the purely existential polynomial-equation fragment remains open. <bookmark mark='f'/> General integer equations restricted to two unknowns present another unresolved decision question in the cited literature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def unknowns(self):
        head = label(r"How small can an undecidable problem be?", font_size=32).to_edge(UP, buff=0.35)
        rows = [[r"Diophantine equations over $\mathbb{N}$", r"9 unknowns", r"1 unknown: \ decidable",
                 r"Matiyasevich; \ Jones \ (1982)"],
                [r"Diophantine equations over $\mathbb{Z}$", r"11 unknowns", r"2 unknowns: \ open", r"Sun \ (2021)"],
                [r"Post's dominoes", r"5 dominoes", r"2: \ decidable; \ 3, 4: \ open", r"Neary \ (2015)"],
                [r"universal Turing machines", '2 states, 3 symbols; nonstandard background', r"--", r"Wolfram's prize "
                 r"machine \ (Smith, 2007)"],
                [r"busy beaver independent of ZFC", r"432 states \ (claimed)", r"5: \ known", r"chapter 12; \ Part 1"],
                [r"matrix mortality", r"$3 \times 3$", '$2\\times2$: open in cited 2015 account', r"Paterson \ (1970)"]]
        tab = grid_table([r"problem", 'sufficient bound / model', r"below that", r"by"], rows,
                         widths=[4.2, 2.8, 3.0, 3.4], row_h=0.52, font_size=18, mono_cols=(),
                         colors=[[WHITE, NO, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        note_ = label('compare constructions, decision results and verification status under their stated models',
                      font_size=22, color=HEAD).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Small universality claims require model labels. <bookmark mark='a'/> The cited constructions give undecidability bounds of nine natural-number unknowns and eleven integer unknowns. These are sufficient bounds, not proved minimal counts. <bookmark mark='b'/> Neary's published theorem uses five dominoes. Smith's two-state three-symbol 2007 machine uses a nonstandard infinite-background convention; it is not ordinary blank-background universality. The smaller ZFC busy-beaver encoding is explicitly conditional on verification, and the matrix row records the cited mortality literature's scope. <bookmark mark='c'/> Gaps between sufficient constructions and decision results motivate research, but the models and evidence must remain visible."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[3:]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    def open_(self):
        head = label(r"Open problems", font_size=34).to_edge(UP, buff=0.35)
        items = VGroup(
            label(r"1. \ Is Hilbert's tenth problem decidable over $\mathbb{Q}$?", font_size=22, color=WHITE),
            label(r"2. \ Is Post's correspondence problem decidable for 3 dominoes? \ For 4?", font_size=22,
                  color=WHITE),
            label(r"3. \ Is there a \textit{natural} recognizable problem strictly between decidable and halting?",
                  font_size=22, color=WHITE),
            label('4. What is the least $n$ whose step busy beaver $S(n)$ ZFC cannot determine?', font_size=22, color=WHITE),
            label(r"5. \ Is the Collatz conjecture provable in Peano arithmetic, \ if it is true?", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes the second, \ for three dominoes",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Five open problems from this part. <bookmark mark='a'/> Hilbert's tenth over the rationals. <bookmark mark='b'/> Post's problem for three or four dominoes. <bookmark mark='c'/> Convincing natural intermediate computably enumerable degrees, with naturalness understood informally. <bookmark mark='d'/> The exact point where set theory loses track of the busy beaver. <bookmark mark='e'/> And whether the Collatz conjecture, if true, can be proved from the ordinary axioms of arithmetic. <bookmark mark='f'/> This part's research problem takes the second, for three dominoes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcde", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
