from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import CLOCK, COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, load, tile_board


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
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        loyd = tile_board(list(range(1, 14)) + [15, 14, 0], 4, cell=0.5, font_size=22, hot=(14, 15))
        jug = MathTex(r"\gcd(3, 5) = 1 \Rightarrow 4", font_size=40, color=YES)
        sier = bitmap(np.asarray(load("pascal")["mod2"]), ["#0E131C", C.CS_HEAD], width=3.4, height=1.75)
        es = MathTex(r"n^2 + 1 \Rightarrow \text{run of } n + 1", font_size=36, color=CTRL)
        der = MathTex(r"D_n / n! \to 1/e", font_size=44, color=COST)
        crt = MathTex(r"x \equiv 2, 3, 2 \ \Rightarrow\ x = 23", font_size=36, color=CLOCK)
        tiles = Group(
            tile(loyd, r"an invariant settles the puzzle", HEAD),
            tile(jug, r"what every move preserves", YES),
            tile(sier, r"Pascal's triangle, mod 2", HEAD),
            tile(es, r"pigeons: \ Erd\H{o}s--Szekeres", CTRL),
            tile(der, r"inclusion--exclusion", COST),
            tile(crt, r"remainders: \ Sunzi, \ Bezout", CLOCK),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        head = label(rf"Part {PART}: \ Proof and Counting", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            "What we built in this part. Logic, the grammar of precise statements, and the ways to prove them: "
            "directly, by contrapositive, by contradiction, by cases, and by induction, on numbers and on structures. "
            "Invariants, which proved Loyd's puzzle impossible and every jug amount a multiple of the gcd. Counting: "
            "choices, Pascal's triangle and its hidden fractal, pigeonholes, inclusion and exclusion, and the Catalan "
            "numbers. And remainders, chance and graphs, the raw materials of cryptography, algorithms and networks."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"invariants and variants", [16, 33, 39, 54]),
            (r"induction on structures", [12, 14]),
            (r"counting and pigeonholes", [16, 17, 20]),
            (r"Bezout, \ congruences, \ the CRT", [29, 30]),
            (r"indicators, \ linearity, \ tail bounds", [16, 17, 20]),
            (r"trees, \ two-colouring, \ graphs", [18, 36]),
        ], font_size=26)
        with self.voiceover(
            "Where this comes back. Invariants and decreasing measures prove algorithms in Part 16, locks in Part 33, "
            "replicated systems in Part 39, and whole programs by machine in Part 54. Structural induction is how Part "
            "12 reasons about grammars and Part 14 about types. Counting and pigeonholes give the lower bounds of Part "
            "16, the hash tables of Part 17 and the randomized algorithms of Part 20. Bézout, congruences and the "
            "Chinese remainder theorem are the arithmetic of Parts 29 and 30. Linearity of expectation and tail "
            "bounds analyse every randomized algorithm. And graphs carry Part 18's algorithms and Part 36's networks."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"assertions and tests", r"an \texttt{assert} is an invariant you check; \ property-based tests try it "
                                      r"on thousands of random inputs"),
            (r"code review", r"``what is true at the top of this loop?'' \ is the question that finds off-by-one bugs"),
            (r"capacity planning", r"counting users, \ requests and bytes, \ and the pigeonholes they must fit into"),
            (r"incidents", r"probability of failure, \ union bounds over many machines, \ and base rates in alerts"),
            (r"interviews", r"counting, \ induction and probability puzzles \ are the first round's staple"),
        ])
        with self.voiceover(
            "In practice, this mathematics is everywhere in engineering, usually without its name. An assertion is an "
            "invariant you check while the program runs, and property-based testing tries it on thousands of random "
            "inputs. The best question in a code review is: what is true at the top of this loop? Capacity planning is "
            "counting. Incident analysis is probability, with base rates that make most alarms false. And these are the "
            "puzzles of the first round of technical interviews."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove by induction that $1 + 3 + 5 + \cdots + (2n - 1) = n^2$, \ and draw the picture that suggests it.",
            r"On the $3 \times 3$ puzzle, \ can you reach the position with only the 1 and the 2 swapped, \ blank in "
            r"its corner? \ Use the invariant; \ then check with breadth-first search.",
            r"Show that among any $5$ points in a unit square, \ two are at distance at most $\sqrt2 / 2$.",
            r"Count the derangements of $5$ items, \ and prove $D_n = (n - 1)(D_{n-1} + D_{n-2})$ \ by a counting "
            r"argument.",
            r"Find $x$ with $x \equiv 1 \pmod 4$, \ $x \equiv 2 \pmod 5$, \ $x \equiv 3 \pmod 7$, \ by the Chinese "
            r"remainder construction.",
            r"\textit{Build.} \ Run the breadth-first search of \texttt{videos/cs/cs2/compute.py} on the $2 \times 4$ "
            r"puzzle: \ how many positions are reachable, \ and how far is the farthest?",
        ], font_size=24)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The last is a build problem: "
            "it asks you to run this part's search on a board we did not show."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 3, \ Logic from Switches", font_size=44).to_edge(UP, buff=0.6)
        sw = VGroup()
        for k, (a, b) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            row = VGroup(MathTex(str(a), font_size=40, color=DATA), MathTex(str(b), font_size=40, color=DATA),
                         MathTex(str(1 - (a & b)), font_size=40, color=YES if not (a & b) else NO)).arrange(RIGHT, buff=0.9)
            sw.add(row)
        hdr = VGroup(MathTex("A", font_size=36, color=GREY_B), MathTex("B", font_size=36, color=GREY_B),
                     MathTex(r"\mathrm{NAND}", font_size=36, color=CTRL)).arrange(RIGHT, buff=0.7)
        tab = VGroup(hdr, *sw).arrange(DOWN, buff=0.3).move_to(DOWN * 0.4)
        q = label(r"one kind of switch, \ wired this way, \ builds every truth table", font_size=30,
                  color=HEAD).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Next time: logic from switches. Chapter one's truth tables were written on paper. Part 3 builds them out "
            "of physical switches, relays first, the way Claude Shannon showed in 1937, then transistors. And it proves "
            "a surprising fact: one kind of gate, NAND, wired together enough times, computes every truth table there "
            "is. That gate is the only part Pebble needs."
        ):
            self.play(FadeIn(nxt), FadeIn(tab, lag_ratio=0.1), FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Lehman, Leighton and Meyer, \textit{Mathematics for Computer Science}",
             r"Rosen, \textit{Discrete Mathematics and Its Applications}",
             r"Graham, Knuth and Patashnik, \textit{Concrete Mathematics}",
             r"Velleman, \textit{How to Prove It}; \ P\'olya, \textit{How to Solve It}",
             r"Aigner and Ziegler, \textit{Proofs from THE BOOK}",
             r"Stanley, \textit{Enumerative Combinatorics}, vol. 1, ch. 1"],
            [r"Johnson and Story, ``Notes on the `15' puzzle'' (1879); \ Euler, the K\"onigsberg bridges (1736)",
             r"Erd\H{o}s and Szekeres (1935); \ Dilworth (1950); \ Vershik and Kerov, \ Logan and Shepp (1977)",
             r"Floyd, ``Assigning meanings to programs'' (1967); \ Hoare, ``An axiomatic basis for computer "
             r"programming'' (1969)",
             r"Calkin and Wilf, ``Recounting the rationals'' (2000); \ \textit{Sunzi Suanjing} (c.\ 400)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(4.0)
        self.clear_scene()
