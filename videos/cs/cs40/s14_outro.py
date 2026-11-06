from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES)


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Software Engineering", font_size=38).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(label(r"one module, \\ one secret", font_size=40, color=YES), r"Parnas' KWIC, \ 3 against 1", YES),
            tile(MathTex(r"I = \frac{C_e}{C_a + C_e}", font_size=44, color=HEAD), r"coupling, \ measured here",
                 HEAD),
            tile(MathTex(r"\text{Square} \not<: \text{Rectangle}", font_size=40, color=NO), r"behavioural subtyping",
                 NO),
            tile(label(r"62\% \ of mutants killed", font_size=36, color=KERN), r"tests, \ tested", KERN),
            tile(MathTex(r"\tfrac{n(n-1)}{2}", font_size=60, color=LAM), r"Brooks and Conway", LAM),
            tile(MathTex(r"L = \lambda W", font_size=56, color=DATA), r"limit work in progress", DATA),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Parnas' index, built two ways, and changes that cost three modules or one. "
            "Abstract types, contracts, and a square that is not a rectangle. This repository measured: its layers, "
            "its two upward imports, its five cycles, and the stability of its core. SOLID, patterns and the "
            "expression problem. Flaky tests found and bisected, a fuzzer that crashed our assembler twenty-four ways, "
            "and a mutation score that coverage hid. Code shown to be more predictable than prose. Debt as a "
            "model, and evidence that much folklore lacks. Little's law for work in progress, Conway's law, Brooks' "
            "law with its condition, and estimates with their tails."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"version control, \ builds and dependency graphs", [41]),
            (r"interfaces between services; \ one team per service", [43]),
            (r"continuous delivery, \ deployment and its metrics", [44]),
            (r"incidents, \ post-mortems and blameless review", [50]),
            (r"static analysis, \ types and proofs of programs", [54]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 41 builds version control and build systems, which are this part's "
            "dependency graphs made into machines. Part 43 designs the interfaces between services and the teams "
            "behind them. Part 44 delivers software continuously and measures it. Part 50 handles incidents, and "
            "Part 54 replaces tests with proofs where proofs are affordable."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"design docs", r"write the problem, \ the options and the decision before the code; \ review the "
                             r"design, \ not just the diff"),
            (r"modules", r"name the secret each module hides; \ keep interfaces small and deep"),
            (r"tests", r"fast unit tests, \ few end-to-end ones; \ quarantine and fix flaky tests, \ never just "
                       r"retry"),
            (r"review", r"small changes, \ reviewed quickly; \ let machines check style"),
            (r"estimates", r"ranges and percentiles; \ cut scope, \ not quality"),
        ])
        with self.voiceover(
            "In practice. Before large changes, write a design document: the problem, the options considered, and "
            "the decision, and review that before the code. Name the secret each module hides, and keep its "
            "interface small. Write many fast tests and few slow ones, and fix flaky tests instead of retrying them. "
            "Keep changes small so that review is quick, and let machines check the style. And estimate in ranges, "
            "cutting scope rather than quality when time runs out."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"For Parnas' second decomposition, \ list the design decision each module hides, \ and predict which "
            r"modules each of the four changes touches before running them.",
            r"State Liskov and Wing's rules for pre- and postconditions, \ and show that a subtype with a "
            r"\textit{stronger} precondition can break a client that is correct for the supertype.",
            r"Prove Little's law $L = \lambda W$ for a system that starts and ends empty, \ by counting the area "
            r"under the number-in-system curve two ways.",
            r"With $k$ independent parallel streams, \ show that $P(\text{on time}) = \prod_i P(\text{stream } i "
            r"\text{ on time})$, \ and explain the table's four-stream result.",
            r"\textit{Build.} \ Write tests that kill the ten surviving mutants on lines our tests already run, \ "
            r"and report the new mutation score.",
            r"$\bigstar$ \textit{Research.} \ Design a test-adequacy score that predicts whether a patch the tests "
            r"accept is correct; \ validate it on our assembler's mutants and on real patches.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: write the tests that kill the ten survivors on lines our tests already run, and measure the "
            "new score. The last, marked with a star, is a research problem: a score for test suites that predicts "
            "whether a patch they accept is really correct."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 41, \ Version Control, \ Builds and Dependencies", font_size=38).to_edge(
            UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"Git as a content-addressed Merkle graph", HEAD),
            (r"three-way merge, \ and why merges conflict", NO),
            (r"build systems as incremental computation", YES),
            (r"dependency resolution is NP-complete", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 41: version control, builds and dependencies. Git turns out to be a Merkle graph of "
            "content-addressed objects; merging is a three-way comparison with a common ancestor; a build system "
            "is an incremental computation over a graph; and choosing versions of dependencies is NP-complete."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Brooks, \textit{The Mythical Man-Month}; \ Ousterhout, \textit{A Philosophy of Software Design}",
             r"Winters, Manshreck and Wright, \textit{Software Engineering at Google}; \ Forsgren, Humble and Kim, "
             r"\textit{Accelerate}",
             r"Fowler, \textit{Refactoring}; \ Feathers, \textit{Working Effectively with Legacy Code}; \ Gamma et "
             r"al., \textit{Design Patterns}"],
            [r"Naur and Randell \ (1969); \ Parnas \ (1972); \ Liskov and Zilles \ (1974); \ Liskov and Wing \ "
             r"(1994); \ Conway \ (1968)",
             r"DeMillo, Lipton and Sayward \ (1978); \ Luo et al. \ (2014); \ Petrovi\'c and Ivankovi\'c \ (2018)",
             r"Bacchelli and Bird \ (2013); \ Nagappan, Murphy and Basili \ (2008); \ Menzies et al. \ (2016)",
             r"Hindle et al. \ (2012); \ Chen et al. \ (2021); \ Jimenez et al. \ (2024)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES)
