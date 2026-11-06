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
            label(r"done in the 1980s for many fields, \ and for all of them \textbf{if} a conjecture about elliptic "
                  r"curves holds \ (Mazur--Rubin, 2010)", font_size=21, color=GREY_A),
            label(r"Koymans and Pagano \ (December 2024): \ \textbf{unconditionally}, \ for every number field", font_size=22,
                  color=HEAD),
            label(r"their tool: \ elliptic curves that gain no rank in a quadratic extension, \ found with additive "
                  r"combinatorics \ (Green--Tao)", font_size=21, color=LAM),
            label(r"independently: \ Alp\"oge, \ Bhargava, \ Ho and Shnidman \ (2025), \ by a different route",
                  font_size=21, color=DATA),
            label(r"so: \ undecidable over every infinite finitely generated ring", font_size=22, color=NO),
        ).arrange(DOWN, buff=0.24).next_to(ex, DOWN, buff=0.4)
        with self.voiceover(
            "Hilbert asked about the integers. What about other number systems? <bookmark mark='a'/> The Gaussian "
            "integers, numbers of the form a plus b root two, and in general the ring of integers of any number "
            "field. Can a machine decide whether an equation with such coefficients has a solution in such numbers? "
            "<bookmark mark='b'/> In 1978 Jan Denef and Leonard Lipshitz proposed the strategy: show that the "
            "ordinary integers form a Diophantine set inside the bigger ring, and Matiyasevich's theorem carries "
            "over. <bookmark mark='c'/> That was done for many fields in the 1980s, and for all of them in 2010, but "
            "only by assuming an unproved conjecture about elliptic curves. <bookmark mark='d'/> In December 2024 "
            "Peter Koymans and Carlo Pagano proved it for every number field, with no assumption. <bookmark "
            "mark='e'/> The key was to find, for each field, elliptic curves whose rank does not grow in a certain "
            "quadratic extension, and they found them with additive combinatorics, the tools of the Green-Tao "
            "theorem on primes in progressions. <bookmark mark='f'/> Levent Alpöge, Manjul Bhargava, Wei Ho and Ari "
            "Shnidman reached the same result independently, by another route. <bookmark mark='g'/> Combined with "
            "earlier work, the problem is now undecidable over every infinite ring that is finitely generated over "
            "the integers."
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
            label(r"yet $\mathbb{Z}$ \textbf{is} definable with quantifiers: \ Poonen \ (2009) \ and Koenigsmann's "
                  r"one-$\forall$ definition \ (2016)", font_size=21, color=DATA),
            label(r"so the full theory of $\mathbb{Q}$ is undecidable, \ but the purely existential part may not "
                  r"be: \ nobody knows", font_size=21, color=YES),
            label(r"the same question for \textbf{one} equation in \textbf{two} unknowns over $\mathbb{Z}$ is open "
                  r"too", font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.27).next_to(eq, DOWN, buff=0.45)
        with self.voiceover(
            "The rationals are different. <bookmark mark='a'/> Over the rationals, an equation like y squared "
            "equals x cubed minus two is a question about rational points on a curve, the subject of arithmetic "
            "geometry, and Fermat knew the point three, five. <bookmark mark='b'/> If the integers formed a "
            "Diophantine set inside the rationals, the problem would be undecidable, just as before. <bookmark "
            "mark='c'/> But Barry Mazur conjectured in 1992 that rational points are never scattered enough for "
            "that, and most experts believe him. <bookmark mark='d'/> With quantifiers, the integers can be defined: "
            "Bjorn Poonen in 2009, and Jochen Koenigsmann in 2016 with a single for-all. <bookmark mark='e'/> So the "
            "full theory of the rationals is undecidable, as chapter thirteen said, but the equations alone might "
            "still be decidable. That is one of the great open problems of logic and number theory. <bookmark "
            "mark='f'/> Even over the integers, whether you can decide equations in just two unknowns is unknown."
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
                [r"universal Turing machines", r"2 states, 3 symbols \ (weakly)", r"--", r"Wolfram's prize "
                 r"machine \ (Smith, 2007)"],
                [r"busy beaver independent of ZFC", r"432 states \ (claimed)", r"5: \ known", r"chapter 12; \ Part 1"],
                [r"matrix mortality", r"$3 \times 3$", r"$2 \times 2$: \ open", r"Paterson \ (1970)"]]
        tab = grid_table([r"problem", r"undecidable at", r"below that", r"by"], rows,
                         widths=[4.2, 2.8, 3.0, 3.4], row_h=0.52, font_size=18, mono_cols=(),
                         colors=[[WHITE, NO, YES, GREY_A]] * len(rows))
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        note_ = label(r"every gap in the third column is a research problem about where computation begins",
                      font_size=22, color=HEAD).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "A recurring frontier question is how small an undecidable problem can be. <bookmark mark='a'/> For "
            "equations over the natural numbers, nine unknowns are enough, by Matiyasevich and James Jones. Over "
            "the integers, Sun Zhi-Wei brought it to eleven in 2021. With one unknown it is easy; with two, over "
            "the integers, nobody knows. <bookmark mark='b'/> Post's dominoes: five is enough, two is decidable, "
            "three and four are open. A Turing machine with two states and three symbols was shown universal, in a "
            "weak sense, by Alex Smith in 2007. The busy beaver leaves set theory somewhere below four hundred and "
            "thirty-two states, and matrix mortality waits at two by two. <bookmark mark='c'/> Every gap in the "
            "third column is a research problem about exactly where computation begins."
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
            label(r"4. \ What is the smallest $n$ for which ZFC cannot determine BB($n$)?", font_size=22, color=WHITE),
            label(r"5. \ Is the Collatz conjecture provable in Peano arithmetic, \ if it is true?", font_size=22,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        star = label(r"$\bigstar$ \ the part's research problem takes the second, \ for three dominoes",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Five open problems from this part. <bookmark mark='a'/> Hilbert's tenth over the rationals. <bookmark "
            "mark='b'/> Post's problem for three or four dominoes. <bookmark mark='c'/> A natural problem of "
            "intermediate degree, which nobody has ever found. <bookmark mark='d'/> The exact point where set theory "
            "loses track of the busy beaver. <bookmark mark='e'/> And whether the Collatz conjecture, if true, can "
            "be proved from the ordinary axioms of arithmetic. <bookmark mark='f'/> This part's research problem "
            "takes the second, for three dominoes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcde", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(star))
        self.wait(0.3)
        self.clear_scene()
