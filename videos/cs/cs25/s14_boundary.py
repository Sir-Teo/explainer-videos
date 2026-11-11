from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (fit_right, CTRL, DATA, HEAD, LAM, NO, PART, YES, grid_table, load, mono, words)

PRIMEGAME = ["17/91", "78/85", "19/51", "23/38", "29/33", "77/29", "95/23", "77/19", "1/17", "11/13", "13/11", "15/2",
             "1/7", "55/1"]


class Boundary(VoiceoverScene):
    def construct(self):
        self.card()
        self.theories()
        self.algebra()
        self.fractran()
        self.collatz()

    def card(self):
        card = chapter_card(13, r"Where decidability ends", r"How little does it take to be undecidable?",
                            lit=(1929, 1972), extra=((1929, r"Presburger"), (1955, r"Novikov"), (1972, r"Conway")),
                            part=PART)
        with self.voiceover("Chapter thirteen. Where decidability ends."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theories(self):
        head = label(r"Which theories can a machine decide?", font_size=32).to_edge(UP, buff=0.35)
        rows = [[r"whole numbers with $+$", r"\textbf{decidable}", 'Presburger (1929); Fischer--Rabin: doubly exponential WORST CASE in formula length'],
                [r"real numbers with $+, \times, <$", r"\textbf{decidable}", r"Tarski \ (1948): \ so is Euclid's "
                 r"geometry; \ Collins \ (1975)"],
                [r"whole numbers with $+, \times$", r"undecidable", r"G\"odel, \ Church, \ Turing \ (1931--36)"],
                [r"rational numbers with $+, \times$", r"undecidable", r"Julia Robinson \ (1949): \ $\mathbb{Z}$ is "
                 r"definable inside $\mathbb{Q}$"],
                [r"just the \textbf{equations} over $\mathbb{Q}$", r"\textbf{open}", r"the frontier \ (chapter 15)"]]
        tab = grid_table([r"first-order truths about", r"status", r"by"], rows, widths=[4.6, 2.2, 6.2], row_h=0.58,
                         font_size=20, mono_cols=(), colors=[[WHITE, YES, GREY_A], [WHITE, YES, GREY_A],
                                                              [WHITE, NO, GREY_A], [WHITE, NO, GREY_A],
                                                              [WHITE, HEAD, GREY_A]])
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        notes = VGroup(
            label(r"multiplication is the dangerous ingredient: \ with it, \ numbers can encode computations",
                  font_size=22, color=DATA),
            label(r"the reals escape because they cannot single out the whole numbers", font_size=22, color=LAM),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Decidability depends on the theory's exact language. <bookmark mark='a'/> Presburger arithmetic, with addition on natural numbers, is decidable; the doubly exponential lower bound is WORST CASE as formula length grows. <bookmark mark='b'/> Tarski decides first-order polynomial formulas over real closed fields, covering the corresponding algebraic geometry. Arbitrary real functions are outside that statement. <bookmark mark='c'/> Adding multiplication on natural numbers makes the full first-order theory undecidable. <bookmark mark='d'/> The full first-order theory of the rationals is also undecidable, via definitions of the integers. <bookmark mark='e'/> Its purely existential polynomial-equation problem is the separate open Hilbert-tenth question. <bookmark mark='f'/> In the ordered real field, integers are not first-order definable; this prevents that particular arithmetic encoding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abcde", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("f")
            self.play(FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    def algebra(self):
        head = label(r"Undecidable algebra", font_size=34).to_edge(UP, buff=0.35)
        gp = VGroup(
            label(r"\textbf{the word problem}", font_size=24, color=HEAD),
            MathTex(r"\langle\, a, b \;\mid\; aba^{-1}b^{-1} = 1,\ \ldots \,\rangle", font_size=32, color=WHITE),
            label(r"given finitely many generators and relations, \\ does a word equal 1?", font_size=20,
                  color=GREY_A),
            label(r"undecidable for groups \\ (Novikov 1955; \ Boone 1958)", font_size=20, color=NO),
            label(r"Dehn \ (1911) \ asked it, \\ for the groups of surfaces", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.22).shift(LEFT * 3.4 + DOWN * 0.2)
        mm = VGroup(
            label(r"\textbf{matrix mortality}", font_size=24, color=HEAD),
            MathTex(r"M_{i_1} M_{i_2} \cdots M_{i_k} \;=\; 0\ ?", font_size=32, color=WHITE),
            label(r"given a few $3 \times 3$ integer matrices, \\ does some product vanish?", font_size=20,
                  color=GREY_A),
            label(r"undecidable \ (Paterson 1970, \\ by encoding Post's dominoes)", font_size=20, color=NO),
            label('$2\\times2$: open in cited Neary (2015) discussion; dated status', font_size=18, color=YES),
        ).arrange(DOWN, buff=0.22).shift(RIGHT * 3.4 + DOWN * 0.2)
        div = DashedLine(UP * 2.4, DOWN * 2.8, color=GREY_D)
        with self.voiceover(
            "Undecidability also hides in pure algebra. <bookmark mark='a'/> Max Dehn asked in 1911: given a group by finitely many generators and relations, can you decide whether a word in the generators equals the identity? Pyotr Novikov in 1955 and William Boone in 1958 found groups where no algorithm can. <bookmark mark='b'/> Or take a handful of three-by-three integer matrices. Does some product of them, in some order, with repetition, give the zero matrix? Michael Paterson proved in 1970 that this is undecidable, by turning Post's dominoes into matrices. <bookmark mark='c'/> The cited Neary 2015 paper records unrestricted two-by-two integer mortality as open. This is a dated literature status, not a claimed new 2026 survey."
        ) as vo:
            self.play(FadeIn(head), Create(div))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in gp], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in mm[:4]], lag_ratio=0.3), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(mm[4]))
        self.wait(0.3)
        self.clear_scene()

    def fractran(self):
        f = load("fractran")
        head = label(r"Conway's PRIMEGAME \ (1987)", font_size=34).to_edge(UP, buff=0.3)
        fr = VGroup(*[MathTex(rf"\tfrac{{{a.split('/')[0]}}}{{{a.split('/')[1]}}}", font_size=40, color=HEAD)
                      for a in PRIMEGAME]).arrange(RIGHT, buff=0.32).next_to(head, DOWN, buff=0.4)
        rule = label(r"start with $n = 2$. \ Repeatedly: \ multiply $n$ by the \textbf{first} fraction that gives a "
                     r"whole number", font_size=21, color=WHITE).next_to(fr, DOWN, buff=0.3)
        ps, st = f["primes"][:12], f["steps"][:12]
        rows = [[rf"$2^{{{p}}}$", words(s)] for p, s in zip(ps, st)]
        tab = grid_table([r"power of 2 reached", r"after step"], rows, widths=[2.8, 2.2], row_h=0.34, font_size=19,
                         mono_cols=(), colors=[[YES, DATA]] * len(rows))
        tab.next_to(rule, DOWN, buff=0.35).to_edge(LEFT, buff=1.0)
        notes = VGroup(
            label('after POSITIVE steps, powers of 2 \\\\ have prime exponents, in order; initial $2^1$ excluded', font_size=21,
                  color=YES),
            label(rf"our run: \ every prime up to {f['primes'][-1]} \\ in {words(f['steps'][-1])} steps", font_size=21,
                  color=GREY_A),
            label(r"\textbf{FRACTRAN} is universal: \\ exponents of primes are registers, \\ fractions are rules", font_size=21,
                  color=HEAD),
            label(r"so ``does this list of fractions \\ ever stop?'' \ is undecidable", font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.7).align_to(tab, UP)
        fit_right(notes)
        with self.voiceover(
            "John Conway invented the strangest programming language of all. <bookmark mark='a'/> A program is a list of fractions. Start with a POSITIVE INTEGER; repeatedly multiply it by the first fraction in the list that gives a whole number; stop when none does. <bookmark mark='b'/> This list, PRIMEGAME, starts from two. Record powers of two reached AFTER positive steps, excluding the initial two to the first power. After nineteen steps, four, which is two squared. After sixty-nine, eight. Then thirty-two, a hundred and twenty-eight, two to the eleven. <bookmark mark='c'/> The exponents are exactly the primes, in order. Our run reached every prime up to a hundred and twenty-seven in under three million steps. <bookmark mark='d'/> Why does this work? The exponents of the primes in n act as registers, and each fraction is an instruction that decrements some registers and increments others. That is Part 1's counter machine, and it is universal. <bookmark mark='e'/> So whether a list of fractions ever stops is undecidable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in fr], lag_ratio=0.08), FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2), run_time=3.0)
            for mk, n_ in zip("cde", [VGroup(notes[0], notes[1]), notes[2], notes[3]]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def collatz(self):
        c = load("collatz")
        head = label(r"Collatz, \ on the boundary", font_size=34).to_edge(UP, buff=0.3)
        tr = c["traj27"]
        ax = Axes(x_range=[0, len(tr), 20], y_range=[0, 4.0, 1], x_length=6.2, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).next_to(head, DOWN, buff=0.5).to_edge(
            LEFT, buff=0.9)
        pts = [ax.c2p(i, np.log10(v)) for i, v in enumerate(tr)]
        path = VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners(pts)
        yt = VGroup(*[label(rf"$10^{k}$", font_size=15, color=GREY_A).next_to(ax.c2p(0, k), LEFT, buff=0.1)
                      for k in range(1, 4)])
        xl = label(rf"the {len(tr) - 1} steps from 27 to 1 \ (peak {max(tr):,})", font_size=18,
                   color=GREY_A).next_to(ax, DOWN, buff=0.15)
        rule = MathTex(r"n \mapsto \begin{cases} n/2 & n \text{ even} \\ 3n + 1 & n \text{ odd} \end{cases}",
                       font_size=32, color=WHITE)
        notes = VGroup(
            label(rf"below a million, \ {c['longest_n']:,} takes longest: \\ {c['longest']} steps", font_size=20,
                  color=DATA),
            label(rf"{c['peak_n']:,} climbs to \\ {c['peak']:,}", font_size=20, color=DATA),
            label('this run: all positive starts below $10^6$ \\\\ complete lengths and peaks independently replayed', font_size=20, color=GREY_A),
            label(r"Conway \ (1972): \ rules of the same shape, \\ ``$n \bmod m$ picks $a n + b$'', \\ can be "
                  r"\textbf{undecidable}", font_size=20, color=NO),
            label('ordinary Collatz: true and provable, independent, or false? \\\\ no independence result is proved here',
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        right = VGroup(rule, notes).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(ax, RIGHT, buff=0.5).align_to(
            ax, UP)
        fit_right(right)
        with self.voiceover(
            "The ordinary Collatz question remains distinct from its universal generalizations. <bookmark mark='a'/> For positive integers, halve an even value and triple an odd value then add one. Twenty-seven takes one hundred and eleven steps to reach one. <bookmark mark='b'/> We retain stopping lengths and full trajectory peaks for EVERY positive start below a million, independently checked by an overflow-guarded native implementation. The longest takes five hundred and twenty-four steps from eight hundred and thirty-seven thousand, seven hundred and ninety-nine. <bookmark mark='c'/> These finite checks prove only this finite prefix; larger published verification ranges are dated claims, not executions of this run. <bookmark mark='d'/> Conway's generalized residue-dependent iterations can encode universal computation and have an undecidable halting problem. <bookmark mark='e'/> That does not prove ordinary Collatz undecidable or independent. It could be true with a proof, true but independent of a specified theory, or false. No independence result is established here."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yt), FadeIn(rule))
            vo.wait_until("a")
            self.play(Create(path), FadeIn(xl), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()
