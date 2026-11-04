from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CODE, COST, CTRL, DATA, FUNC, HEAD, LIMIT, PART, YES, fmt, load, spacetime_mob
from videos.cs.cs1.s02_algorithms import ramp
from videos.cs.cs1.s14_beavers import density_rgb


def tile(content, caption, color, TW=3.6, TH=2.3):
    box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D, stroke_width=1.5,
                           fill_color="#121722", fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(box.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.3)
    return Group(box, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        e = load("euclid")
        heat = bitmap(ramp(np.asarray(e["grid"], float).T / e["max_steps"])[::-1], width=2.2, height=2.2)
        pal = load("palindrome")
        zig = spacetime_mob(np.asarray(pal["st_long"]), width=1.2, height=2.2)
        u = load("universal")
        utab = VGroup(*[label(rf"${r['m_steps']}$ \ $\to$ \ ${fmt(r['u_steps'])}$", font_size=30, color=CODE)
                        for r in u["rows"]]).arrange(DOWN, buff=0.18)
        lam_ = VGroup(MathTex(r"\mathrm{PLUS}\ 2\ 3", font_size=40, color=FUNC),
                      MathTex(r"\to_\beta^{6}\ \lambda f\,x.\, f^5 x", font_size=36, color=FUNC)).arrange(DOWN)
        r110 = bitmap(np.asarray(load("rule110")["grid"])[:150, -200:], [BACKGROUND, HEAD], width=3.2, height=2.2)
        bb = bitmap(density_rgb(np.asarray(load("beavers")["st5"])), width=3.4, height=2.2, smooth=True)
        tiles = Group(
            tile(heat, r"Euclid: \ Lam\'e's worst cases", DATA),
            tile(zig, r"one tape: \ $n^2/2$ steps", COST),
            tile(utab, r"$U$ runs any machine", CODE),
            tile(lam_, r"functions alone compute", FUNC),
            tile(r110, r"Rule 110 is universal", HEAD),
            tile(bb, r"BB(5): \ $47{,}176{,}870$ steps", LIMIT),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ What Is a Computation?", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we found in this part. Euclid's rule, followed without understanding, and Lamé's bound on its worst "
            "cases. Turing's machine, which settles palindromes in n squared steps on one tape and three n on two. A "
            "universal machine, running any other from its description, for a price. Functions alone, bowls of "
            "pebbles, and a row of cells, all computing the same things. And beyond them all, the halting problem, and "
            "a five-state machine whose forty-seven million steps took the world until 2024 to understand."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the universal machine, \ programs as data", [6, 15, 32]),
            (r"invariants, \ and quantities that shrink", [2, 54]),
            (r"finite-state control", [5, 12]),
            (r"the $\lambda$-calculus", [14]),
            (r"diagonalization, \ reductions", [25, 26, 27]),
            (r"polynomial slowdown, \ the extended thesis", [16, 26, 53]),
        ], font_size=26)
        with self.voiceover(
            "Where this comes back. The universal machine becomes the stored-program computer of Part 6, the "
            "interpreters of Part 15 and the hypervisors of Part 32. Invariants and shrinking quantities are the proofs "
            "of Part 2 and Part 54. The finite control of a Turing machine is the finite automaton of Parts 5 and 12. "
            "The lambda calculus becomes the type theory of Part 14. Diagonalization and reductions drive Parts 25 to "
            "27. And the extended thesis is the foundation of complexity theory, and the claim quantum computers test."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Design a Turing machine that adds one to a number written in binary (the head starts on the leftmost "
            r"digit). \ How many steps does it take on the input $1^n$?",
            r"Show that the set of finite binary strings is countable, \ and that the set of all subsets of "
            r"$\mathbb{N}$ is not.",
            r"Prove that ``does $M$ ever write a $1$, \ started on a blank tape?'' is undecidable, \ by reducing the "
            r"blank-tape halting problem to it.",
            r"Prove that $S(n + 1) > S(n)$ for every $n \ge 1$.",
            r"Reduce $\mathrm{TIMES}\ 2\ 2$ to normal form by hand, \ with $\mathrm{TIMES} = \lambda m\,n\,f.\ m\,(n\,f)$. "
            r"\ How many $\beta$-steps does normal order take?",
            r"\textit{Build.} \ Run our universal machine (\texttt{videos/cs/cs1/machines.py}) on the 4-state champion "
            r"and measure its steps per simulated step. \ Reorder the rules of $\langle M \rangle$ so the most used "
            r"come first: \ how much faster is it?",
        ], font_size=24)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The last one is a build "
            "problem: it asks you to run and change the universal machine this part used."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 2, \ Proof and Counting", font_size=44).to_edge(UP, buff=0.6)
        puzzle = VGroup()
        nums = list(range(1, 14)) + [15, 14, 0]
        for i, n in enumerate(nums):
            r, c = divmod(i, 4)
            sq = RoundedRectangle(width=0.8, height=0.8, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2,
                                  fill_color="#1B2130" if n else BACKGROUND, fill_opacity=1)
            sq.move_to([(c - 1.5) * 0.86, (1.5 - r) * 0.86, 0])
            g = VGroup(sq)
            if n:
                g.add(label(str(n), font_size=30, color=HEAD if n in (14, 15) else WHITE).move_to(sq))
            puzzle.add(g)
        puzzle.move_to(DOWN * 0.6)
        q = label(r"swap the 14 and the 15: \ is it solvable?", font_size=30, color=HEAD).next_to(puzzle, DOWN,
                                                                                               buff=0.35)
        with self.voiceover(
            "Next time: proof and counting. This part used proofs without saying what a proof is. Part 2 fixes that: "
            "logic, induction, invariants, and the counting that every later bound needs. It opens with a puzzle that "
            "sold millions of copies in 1880: slide the tiles to swap the fourteen and the fifteen. Can it be done? An "
            "invariant answers, in one line."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(t) for t in puzzle], lag_ratio=0.04), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Sipser, \textit{Introduction to the Theory of Computation}, ch. 3--5",
             r"Petzold, \textit{The Annotated Turing}",
             r"Moore and Mertens, \textit{The Nature of Computation}, ch. 7",
             r"Minsky, \textit{Computation: Finite and Infinite Machines}",
             r"Boolos, Burgess and Jeffrey, \textit{Computability and Logic}",
             r"Davis, \textit{The Universal Computer: The Road from Leibniz to Turing}"],
            [r"Lovelace, Notes on Menabrea's \textit{Sketch of the Analytical Engine} (1843); \ Hilbert and Ackermann, "
             r"\textit{Grundz\"uge der theoretischen Logik} (1928); \ G\"odel (1931)",
             r"Church, ``An unsolvable problem of elementary number theory'' (1936); \ Turing, ``On computable numbers, "
             r"with an application to the \textit{Entscheidungsproblem}'' (1936)",
             r"Rice (1953); \ Minsky (1961); \ Rad\'o, ``On non-computable functions'' (1962); \ Hennie (1965); \ "
             r"Lin and Rad\'o (1965); \ Brady (1983); \ Cohen (1987)",
             r"Marxen and Buntrock (1990); \ Cook, ``Universality in elementary cellular automata'' (2004); \ "
             r"Yedidia and Aaronson (2016); \ the bbchallenge collaboration, ``Determination of the fifth busy beaver "
             r"value'' (2025)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
