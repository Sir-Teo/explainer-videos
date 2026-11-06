from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, grid_table, load, mono,
                                   words)


class Derandom(VoiceoverScene):
    def construct(self):
        self.card()
        self.generator()
        self.identity()
        self.tradeoff()

    def card(self):
        card = chapter_card(2, r"Hardness against randomness", r"Could every coin be replaced by a hard function?",
                            lit=(1988, 1997), extra=((1988, r"Nisan--Wigderson"), (1997, r"Impagliazzo--Wigderson")),
                            part=PART)
        with self.voiceover("Chapter two. Hardness against randomness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def generator(self):
        head = label(r"The Nisan--Wigderson generator", font_size=34).to_edge(UP, buff=0.3)
        seed = VGroup(*[Square(side_length=0.36, stroke_color=GREY_B, stroke_width=1.2,
                               fill_color=DATA if b else BG, fill_opacity=0.8)
                        for b in (1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0)]).arrange(RIGHT, buff=0.04)
        seed.next_to(head, DOWN, buff=0.6).to_edge(LEFT, buff=1.0)
        sl = label(r"a short truly random seed \ ($O(\log n)$ bits)", font_size=19, color=DATA).next_to(seed, DOWN,
                                                                                                buff=0.12)
        sets = [(0, 1, 2, 3), (2, 4, 6, 8), (1, 5, 7, 10), (3, 6, 9, 11), (0, 5, 8, 11), (4, 7, 9, 10)]
        cols = [HEAD, YES, LAM, NO, CTRL, DATA]
        brackets = VGroup()
        outs = VGroup()
        for k, (S, col) in enumerate(zip(sets, cols)):
            marks = VGroup(*[Dot(seed[i].get_center() + DOWN * (0.75 + 0.4 * k), radius=0.05, color=col)
                             for i in S])
            box_ = RoundedRectangle(width=0.7, height=0.3, corner_radius=0.06, color=col).move_to(
                [seed.get_right()[0] + 0.7, marks[0].get_y(), 0])
            line = Line(marks[0].get_center(), box_.get_left(), stroke_width=1.2, color=col)
            fl = MathTex(r"f", font_size=22, color=col).move_to(box_)
            brackets.add(VGroup(line, marks, box_, fl))
            outs.add(Square(side_length=0.3, stroke_color=col, fill_color=col, fill_opacity=0.5))
        outs.arrange(RIGHT, buff=0.06).next_to(brackets, DOWN, buff=0.4).align_to(seed, LEFT)
        ol = label(r"many output bits \ (one per subset)", font_size=19, color=GREY_A).next_to(outs, DOWN, buff=0.12)
        lines = VGroup(
            label(r"apply a \textbf{hard} function $f$ to many overlapping subsets of the seed", font_size=21,
                  color=WHITE),
            label(r"the subsets share few bits \ (a combinatorial \textbf{design})", font_size=21, color=GREY_A),
            label(r"if a small circuit could tell the output from coins, \\ it could be turned into a small circuit "
                  r"\textbf{computing} $f$", font_size=21, color=NO),
            label(r"so: \ hard functions make good generators; \\ try all $\mathrm{poly}(n)$ seeds and take the "
                  r"majority", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(seed, RIGHT, buff=1.6).align_to(seed, UP)
        fit_right(lines)
        with self.voiceover(
            "Part 20's frontier previewed the idea; here is how it works. <bookmark mark='a'/> Start with a short "
            "truly random seed, only logarithmically many bits. Choose many subsets of its positions that overlap "
            "very little, a combinatorial design, and apply a hard function f to each subset. Each application "
            "gives one output bit. <bookmark mark='b'/> Noam Nisan and Avi Wigderson showed in 1988 that the small "
            "overlaps keep the outputs nearly independent. <bookmark mark='c'/> If some small circuit could tell this "
            "output from real coins, a hybrid argument would turn it into a small circuit that computes f, "
            "contradicting f's hardness. <bookmark mark='d'/> So the output fools every small circuit, and a "
            "randomized algorithm is one. With a logarithmic seed there are only polynomially many seeds: try them "
            "all and take the majority. No coins at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(seed), FadeIn(sl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in brackets], lag_ratio=0.2), FadeIn(outs), FadeIn(ol),
                      FadeIn(lines[0]), run_time=3.0)
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def identity(self):
        d = load("pit")
        head = label(r"The problem nobody can derandomize", font_size=34).to_edge(UP, buff=0.3)
        eq = MathTex(r"\det \begin{pmatrix} 1 & x_1 & x_1^2 & \cdots \\ 1 & x_2 & x_2^2 & \cdots \\ \vdots & & & "
                     r"\ddots \end{pmatrix} \;\overset{?}{=}\; \prod_{i < j} (x_j - x_i)", font_size=34, color=WHITE)
        eq.next_to(head, DOWN, buff=0.35)
        rows = [[words(r["p"]), f"{r['true_pass'] * 100:.0f}\\%",
                 f"{r['false_pass'] * 100:.2f}\\%", f"{r['bound'] * 100:.2f}\\%"] for r in d["rows"]]
        tab = grid_table([r"field size $p$", r"true identity passes", r"false identity passes",
                          r"bound $d/p$"], rows, widths=[2.4, 3.4, 3.4, 2.4], row_h=0.42, font_size=20,
                         mono_cols=(), colors=[[WHITE, YES, NO, GREY_A]] * len(rows))
        tab.next_to(eq, DOWN, buff=0.35).set_x(0)
        tl = label(rf"$n = {d['n']}$ variables, \ {words(d['trials'])} random points per row; \ the false identity "
                   r"has $(x_2 + x_1)$ in place of $(x_2 - x_1)$", font_size=18, color=GREY_A).next_to(
            tab, DOWN, buff=0.22)
        lines = VGroup(
            label(rf"expanding the determinant: \ {words(d['terms'])} terms; \ one random test: "
                  rf"{d['rows'][-1]['seconds'] * 1e6:.0f} $\mu$s", font_size=21, color=WHITE),
            label(r"\textbf{Schwartz--Zippel}: \ a nonzero polynomial of degree $d$ vanishes at a random point with "
                  r"probability $\le d/p$", font_size=21, color=HEAD),
            label(r"identity testing is in coRP; \ no deterministic polynomial algorithm is known", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).next_to(tl, DOWN, buff=0.3)
        with self.voiceover(
            "Here is the problem at the centre of derandomization. <bookmark mark='a'/> Is this determinant, the "
            "Vandermonde determinant, equal to the product of all the differences? Expanding it for ten variables "
            "would produce over three and a half million terms. <bookmark mark='b'/> Instead, pick random values "
            "modulo a prime and compare the two sides: about a tenth of a millisecond. Richard DeMillo and Richard "
            "Lipton, Jacob Schwartz and Richard Zippel proved that a nonzero polynomial of degree d vanishes at a "
            "random point with probability at most d over p. <bookmark mark='c'/> The true identity passed every "
            "test. A false one, with a single sign changed, slipped through a little less often than the bound allows when "
            "the field is tiny, and never once in five thousand tries over a field of a million. <bookmark "
            "mark='d'/> So identity testing has a fast randomized algorithm. Nobody knows a deterministic "
            "polynomial one."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(tl), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def tradeoff(self):
        head = label(r"Either hardness or randomness", font_size=34).to_edge(UP, buff=0.35)
        lines = VGroup(
            label(r"Impagliazzo and Wigderson \ (1997): \ if some problem in $\mathrm{E} = \mathrm{TIME}(2^{O(n)})$ "
                  r"needs circuits of size $2^{\Omega(n)}$, \ then \textbf{P = BPP}", font_size=22, color=HEAD),
            label(r"most researchers believe the hypothesis, \ so most believe randomness adds \textbf{no} power to "
                  r"polynomial time", font_size=22, color=YES),
            label(r"the converse also holds, \ in part: \ derandomizing identity testing would itself prove circuit "
                  r"lower bounds \ (Kabanets and Impagliazzo, 2004)", font_size=22, color=NO),
            label(r"so derandomization and lower bounds are \textbf{the same problem}, \ seen from two sides",
                  font_size=22, color=DATA),
            label(r"the poster child: \ primality, \ randomized since the 1970s, \ deterministic since 2002 \ (AKS)",
                  font_size=22, color=LAM),
            label(r"in practice we keep the coins: \ Miller--Rabin is far faster than AKS", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "This turns into a striking trade-off. <bookmark mark='a'/> Russell Impagliazzo and Avi Wigderson "
            "proved in 1997: if some problem solvable in exponential time requires exponential-size circuits, then "
            "P equals BPP. <bookmark mark='b'/> Almost everyone believes that hypothesis, so almost everyone "
            "believes randomness gives no extra power to polynomial-time algorithms. <bookmark mark='c'/> The "
            "converse holds too, in part: Valentine Kabanets and Impagliazzo showed that removing the coins from "
            "polynomial identity testing would itself prove new circuit lower bounds. <bookmark mark='d'/> So "
            "derandomization and lower bounds are the same problem seen from two sides. <bookmark mark='e'/> "
            "Primality is the poster child: randomized tests since the 1970s, a deterministic polynomial one since "
            "2002. <bookmark mark='f'/> In practice nobody uses the deterministic test: Miller-Rabin is far faster."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
