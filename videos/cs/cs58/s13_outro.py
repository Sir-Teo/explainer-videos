from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs58.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Semantics", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"e \to e'", font_size=60, color=HEAD), r"steps", HEAD),
            tile(MathTex(r"\mathrm{fix}\,F = \bigsqcup_k F^k(\bot)", font_size=42, color=YES), r"least fixed points",
                 YES),
            tile(label(r"same traces, \ not bisimilar", font_size=30, color=DATA), r"equivalence", DATA),
            tile(MathTex(r"\mathit{map}\,f \circ r = r \circ \mathit{map}\,f", font_size=40, color=KERN),
                 r"theorems for free", KERN),
            tile(MathTex(r"M\,a \to (a \to M\,b) \to M\,b", font_size=40, color=LAM), r"monads", LAM),
            tile(MathTex(r"\Pi\,x{:}A.\ B(x)", font_size=50, color=NO), r"dependent types", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Three operational semantics for one language, small-step, big-step and the "
            "CEK machine, agreeing on every program we tried. A denotational semantics, where recursion is a least "
            "fixed point reached by Kleene's chain. Adequacy and full abstraction, and the parallel-or that PCF cannot "
            "define. Equivalence by bisimulation and logical relations, and the normalization proof they give. "
            "Parametricity's free theorems; Hoare logic proved sound; effects as monads; dependent types; and "
            "processes that communicate. One idea runs through it: meaning is compositional, the meaning of a whole is "
            "built from the meanings of its parts."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"the theory of distributed processes", [59]),
            (r"hardware described as programs", [60]),
            (r"proof as research", [61]),
            (r"formal methods in practice", [54]),
            (r"trusting compilers", [55]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 59's distributed algorithms are processes like chapter ten's. Part 60 "
            "describes hardware as programs whose meaning must match a specification. Part 61 treats proof as a "
            "research method. And looking back, Part 54's verification and Part 55's trusted compilers both rest on "
            "the semantics of this part."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"specify", r"write a language's rules down before its implementation"),
            (r"test", r"two interpreters that must agree are a strong oracle"),
            (r"refactor", r"justify a change by an equivalence, \ not by hope"),
            (r"design", r"effects in the types: \ async, \ errors and state, \ explicit"),
            (r"prove", r"mechanize the semantics when the stakes justify it"),
        ])
        with self.voiceover(
            "In practice. Write a language's rules down before implementing it. Use two interpreters that must agree "
            "as a test oracle for each other. Justify a refactoring by an equivalence, not by hope. Put effects in "
            "the types, so that errors, state and asynchrony are explicit. And when the stakes justify it, "
            "mechanize the semantics."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that small-step evaluation is deterministic for our language.",
            r"Show that the factorial functional is continuous, \ and that its least fixed point is factorial.",
            r"Show that $a.(b + c)$ and $a.b + a.c$ have the same traces but are not bisimilar, \ with a "
            r"distinguishing formula.",
            r"Derive the free theorem for $r : \forall a.\, [a] \to [a]$.",
            r"\textit{Build.} \ Add exceptions to our interpreters, \ and check the three still agree on random "
            r"programs.",
            r"$\bigstar$ \textit{Research.} \ A relaxed-memory semantics for C without out-of-thin-air values.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add exceptions to all three of our interpreters and check that they still agree. The last, "
            "marked with a star, is a research problem: a memory model for C that forbids values from thin air and "
            "still lets compilers optimize."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 59, \ Distributed Computing Theory", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"colouring a ring in $O(\log^* n)$ rounds", HEAD),
            (r"why three generals cannot survive one traitor", YES),
            (r"randomized consensus", DATA),
            (r"topology: \ why k-set agreement is impossible", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 59: the theory of distributed computing. What can n processes compute when each sees "
            "only its neighbours, or some crash, or some lie? Some answers are lower bounds as sharp as log star of "
            "n, and one of them came from algebraic topology."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Winskel, \ \textit{The Formal Semantics of Programming Languages}; \ Harper, \ \textit{Practical "
             r"Foundations for Programming Languages}",
             r"Pierce et al., \ \textit{Software Foundations}; \ Milner, \ \textit{Communicating and Mobile "
             r"Systems}"],
            [r"Scott \ (1970); \ Plotkin \ (1977); \ Reynolds \ (1983); \ Wadler \ (1989)",
             r"Moggi \ (1991); \ Felleisen and Friedman \ (1986); \ Tait \ (1967)",
             r"Leroy \ (2009); \ Kumar et al. \ (2014); \ Haas et al. \ (2017)",
             r"The HoTT Book \ (2013); \ Martin-L\"of \ (1984)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
