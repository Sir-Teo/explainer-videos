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
            "The Nisan–Wigderson construction links circuit hardness with pseudorandomness. <bookmark mark='a'/> Apply a hard Boolean function to overlapping subsets of a random seed. The subset system must satisfy quantitative design bounds. <bookmark mark='b'/> The picture is schematic: small overlaps alone do not prove that arbitrary output bits are independent. The theorem controls distinguishability by circuits of a specified size. <bookmark mark='c'/> A hybrid argument converts a successful distinguisher into a circuit predicting the hard function; suitable hardness amplification supplies the needed average-case hardness. <bookmark mark='d'/> Under sufficiently strong, efficiently evaluable hardness assumptions, the seed can be logarithmic in the simulated input length. Enumerating all seeds then yields deterministic polynomial-time simulation."
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
        head = label('General circuit PIT; a known identity as an example', font_size=34).to_edge(UP, buff=0.3)
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
            label('general arithmetic-circuit PIT: randomized; deterministic polynomial time remains open', font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.2).next_to(tl, DOWN, buff=0.3)
        with self.voiceover(
            "General arithmetic-circuit identity testing remains a central derandomization problem. The Vandermonde formula is a known identity used to illustrate the randomized test. <bookmark mark='a'/> Evaluating a determinant and its product expression at a point avoids explicitly expanding all factorially many permutation terms. The recorded timings measure this implementation on this host. <bookmark mark='b'/> Over a prime field, a nonzero polynomial of total degree d has at most d divided by the field size probability of vanishing at uniformly independent coordinates. The field and formal-polynomial assumptions matter. <bookmark mark='c'/> We retain every sampled point and compare both true and deliberately false expressions with an independent native computation. Zero observed false passes is a finite sample result. <bookmark mark='d'/> The open problem concerns general circuit representations with suitable degree and field access, not this specific identity, which has a deterministic proof."
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
            label('precise conditional links connect derandomization and circuit lower bounds',
                  font_size=22, color=DATA),
            label(r"the poster child: \ primality, \ randomized since the 1970s, \ deterministic since 2002 \ (AKS)",
                  font_size=22, color=LAM),
            label(r"in practice we keep the coins: \ Miller--Rabin is far faster than AKS", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Hardness and derandomization have precise conditional connections. <bookmark mark='a'/> Impagliazzo and Wigderson showed that if some language in E, deterministic time two to a constant times n, requires exponential-size Boolean circuits, then P equals BPP. <bookmark mark='b'/> This is a circuit-hardness assumption with a particular quantitative strength, rather than a consequence of P differing from NP alone. <bookmark mark='c'/> Kabanets and Impagliazzo connected suitable deterministic identity testing over integer arithmetic circuits to a disjunction of new Boolean or arithmetic circuit lower bounds. <bookmark mark='d'/> These implications connect different problems; they do not establish an unrestricted equivalence between all lower bounds and all derandomization. <bookmark mark='e'/> Primality provides a concrete success: the AKS algorithm places it in deterministic polynomial time. <bookmark mark='f'/> Efficient probabilistic tests remain useful in practice; this engineering comparison depends on the algorithms and input sizes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, ln in zip("abcdef", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
