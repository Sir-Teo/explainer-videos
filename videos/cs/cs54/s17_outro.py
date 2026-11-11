from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs54.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Proving Programs Correct", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\{P\}\ c\ \{Q\}", font_size=60, color=HEAD), r"Hoare triples", HEAD),
            tile(MathTex(r"\mathit{wp}(x := e, Q) = Q[e/x]", font_size=40, color=YES), r"weakest preconditions", YES),
            tile(MathTex(r"P * Q", font_size=60, color=DATA), r"separation logic", DATA),
            tile(MathTex(r"\mathbf{AG}\,\neg(cs_0 \wedge cs_1)", font_size=42, color=KERN), r"model checking", KERN),
            tile(MathTex(r"[0, +\infty] \to [0, 100]", font_size=44, color=LAM), r"widening, \ narrowing", LAM),
            tile(label(r"a small trusted kernel", font_size=32, color=NO), r"proof assistants", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Floyd–Hoare logic and its rules, with invariants for loops and variants for "
            "termination. Weakest preconditions, turned into formulas and checked by our own SAT solver, which found "
            "the binary search overflow and proved the fix. Separation logic, so that proofs about the heap can be "
            "local. Model checking: explicit, symbolic with BDDs, and bounded with SAT, on Peterson's lock, the "
            "philosophers, two-phase commit and Raft. Abstract interpretation with widening; an LCF kernel; and a "
            "fuzzer that caught a planted bug in our own compiler. One idea runs through it: correctness cannot be "
            "decided in general, but it can be proved in particular."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"trusting compilers and toolchains", [55]),
            (r"the meaning of programs, \ proved", [58]),
            (r"verified distributed protocols", [59]),
            (r"hardware verified against its specification", [60]),
            (r"proof as research", [61]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 55 asks whether a compiler can be trusted at all. Part 58 gives programs the "
            "mathematical meaning these proofs rest on. Part 59 proves the limits of distributed protocols. Part 60 "
            "checks hardware against its specification. And Part 61 treats proof as a research method."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"assert", r"write invariants as assertions; \ they document and test at once"),
            (r"property-test", r"state properties, \ not examples; \ let the tool shrink failures"),
            (r"fuzz", r"in CI, \ with sanitizers; \ keep the corpus"),
            (r"model", r"a TLA$^+$ or similar model of every tricky protocol, \ before code"),
            (r"prove", r"the small critical core: \ parsers, \ crypto, \ kernels"),
        ])
        with self.voiceover(
            "In practice. Write invariants as assertions, so they document and test at the same time. State "
            "properties rather than examples, and let the tool shrink the failures. Fuzz in continuous integration, "
            "with sanitizers, and keep the corpus. Model every tricky protocol before writing it. And prove the "
            "small critical core: parsers, cryptography, kernels."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove $\{n \ge 0\}$ the summation loop $\{s = n(n+1)/2\}$ with an invariant and a variant.",
            r"Compute $\mathit{wp}$ for the swap without a temporary, \ and show it holds for all $w$-bit values.",
            r"Show that in-place list reversal is correct in separation logic.",
            r"Show that interval analysis without widening may not terminate, \ and that widening makes it "
            r"terminate.",
            r"\textit{Build.} \ Plant a different bug in our compiler's optimizer \ and measure how many random "
            r"programs the fuzzer needs.",
            r"$\bigstar$ \textit{Research.} \ Complete, \ practical invariant inference with multiplication.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: plant a bug of your own in the optimizer and count how many random programs it takes the "
            "fuzzer to find it. The last, marked with a star, is a research problem: complete and practical "
            "invariant inference for loops with multiplication."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 55, \ Trusting Trust", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"every layer leaks", HEAD),
            (r"return-oriented programming on Pebble", NO),
            (r"Lowe's attack, \ found by model checking", YES),
            (r"a compiler that hides a backdoor, \ and how to catch it", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 55, the finale of the degree: trusting trust. Security is a property of the whole "
            "tower, and every layer leaks. We build Ken Thompson's backdoored compiler against our own, catch it, and "
            "walk the tower one last time, from a NAND gate to a cluster."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Huth and Ryan, \ \textit{Logic in Computer Science}; \ Baier and Katoen, \ \textit{Principles of "
             r"Model Checking}",
             r"Nipkow and Klein, \ \textit{Concrete Semantics}; \ Pierce et al., \ \textit{Software Foundations}"],
            [r"Floyd \ (1967); \ Hoare \ (1969); \ Dijkstra \ (1975); \ Reynolds \ (2002)",
             r"Clarke and Emerson \ (1981); \ Bryant \ (1986); \ Biere et al. \ (1999); \ Cousot and Cousot "
             r"\ (1977)",
             r"Leroy \ (2009); \ Klein et al. \ (2009); \ Newcombe et al. \ (2015)",
             r"Claessen and Hughes \ (2000); \ Yang et al. \ (2011); \ Bloch \ (2006)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
