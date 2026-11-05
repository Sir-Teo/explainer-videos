from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, load, mono, region


class Normalization(VoiceoverScene):
    def construct(self):
        self.card()
        self.omega()
        self.theorem()
        self.measured()
        self.price()

    def card(self):
        card = chapter_card(9, r"Every typed program stops", r"What do types cost?", lit=(1967,),
                            extra=((1967, r"Tait: \ strong normalization"),), part=PART)
        with self.voiceover("Chapter nine. Every typed program stops."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def omega(self):
        n = load("normal")
        head = label(r"Can $\Omega$ be typed?", font_size=36).to_edge(UP, buff=0.3)
        t = MathTex(r"\lambda x.\; x\;x", font_size=48).next_to(head, DOWN, buff=0.5)
        steps = VGroup(
            label(r"$x$ is applied, \ so $x : A \to B$ for some $A, B$", font_size=24, color=GREY_A),
            label(r"$x$ is also the argument, \ so $x : A$", font_size=24, color=GREY_A),
            MathTex(r"A \;=\; A \to B \;=\; (A \to B) \to B \;=\; \cdots", font_size=36, color=NO),
            label(r"no finite type solves it", font_size=24, color=NO),
            label(rf"our inference engine: \ \texttt{{{n['omega_error']}}}", font_size=20, color=GREY_B),
        ).arrange(DOWN, buff=0.25).next_to(t, DOWN, buff=0.5)
        with self.voiceover(
            "Try to give a type to the heart of omega, lambda x, x x. <bookmark mark='a'/> x is applied to "
            "something, so it must be a function, of some type A to B. <bookmark mark='b'/> But x is also what it is "
            "applied to, so x must have type A. <bookmark mark='c'/> Then A equals A to B, which equals A to B, to "
            "B, and so on forever. <bookmark mark='d'/> No finite type is a solution. <bookmark mark='e'/> Our "
            "inference engine, the one from the hook, gives up with exactly this complaint: an infinite type. Omega "
            "has no type, and neither does the Y combinator."
        ) as vo:
            self.play(FadeIn(head), Write(t))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.3)
        self.clear_scene()

    def theorem(self):
        head = label(r"Strong normalization \ (Tait, \ 1967)", font_size=34).to_edge(UP, buff=0.3)
        thm = label(r"every well-typed term of the simply typed calculus reaches a normal form, \ by \textit{every} "
                    r"reduction order", font_size=24, color=HEAD).next_to(head, DOWN, buff=0.5)
        why = VGroup(
            label(r"the obvious induction fails: \ a step can make a term \textit{bigger}", font_size=22, color=NO),
            label(r"Tait's idea: \ a stronger property, \ defined by induction on the \textit{type}", font_size=22,
                  color=GREY_A),
            MathTex(r"\mathrm{R}_{\mathsf{Nat}} = \{\, t \text{ that terminate} \,\}", font_size=32),
            MathTex(r"\mathrm{R}_{A \to B} = \{\, f \;:\; f\,a \in \mathrm{R}_B \text{ for every } a \in "
                    r"\mathrm{R}_A \,\}", font_size=32),
            label(r"show every typed term is in $\mathrm{R}$; \ everything in $\mathrm{R}$ terminates", font_size=22,
                  color=YES),
            label(r"the method of \textbf{logical relations}: \ the workhorse of type theory since", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, buff=0.22).next_to(thm, DOWN, buff=0.5)
        with self.voiceover(
            "In fact no typed term runs forever. <bookmark mark='a'/> William Tait proved in 1967 that every "
            "well-typed term of the simply typed calculus reaches a normal form, whichever order of reduction you "
            "choose. <bookmark mark='b'/> The obvious proof by induction on the size of the term fails, because a "
            "beta step can make a term bigger, by copying its argument. <bookmark mark='c'/> Tait's idea was to "
            "prove something stronger, defined by induction on the type. A number is good if it terminates. A "
            "function is good if it sends every good argument to a good result. <bookmark mark='d'/> Then show that "
            "every typed term is good, and every good term terminates. This method, now called logical relations, "
            "has been the workhorse of type theory ever since."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(why[0]))
            vo.wait_until("c")
            self.play(FadeIn(why[1:4]))
            vo.wait_until("d")
            self.play(FadeIn(why[4:]))
        self.wait(0.3)
        self.clear_scene()

    def measured(self):
        n = load("normal")
        s = load("safety")
        head = label(r"Typed and untyped, \ measured", font_size=34).to_edge(UP, buff=0.3)
        un = n["untyped_terms"]
        bars = bar_chart([100 * n["untyped_no_stop"] / un, 0.0], [r"untyped", r"typed"], [NO, YES], height=3.0,
                         bar_w=1.4, gap=1.4, fmt_=lambda v: f"{v:.1f}\\%", font_size=20).move_to(LEFT * 3 + DOWN * 0.4)
        yl = label(r"random terms still running after 400 steps", font_size=18, color=GREY_B).next_to(bars, UP,
                                                                                                  buff=0.3)
        side = VGroup(
            label(rf"untyped: \ {un:,} random closed terms, \ {n['untyped_no_stop']} never finished", font_size=21,
                  color=NO),
            label(rf"typed: \ {s['terms']:,} terms, \ all finished, \ the longest in {s['max_steps']} steps",
                  font_size=21, color=YES),
            label(r"no finite test proves termination; \ for the typed ones, \ the theorem does", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        with self.voiceover(
            "The difference shows up in a simple experiment. <bookmark mark='a'/> We generated two thousand random "
            "untyped terms and ran each for up to four hundred steps of normal order: one hundred and thirty-six "
            "were still running. <bookmark mark='b'/> Of the five thousand typed terms from the last chapter, not "
            "one ran long. For those, the theorem tells us what no amount of testing could: every one of them "
            "would have stopped."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(bars.bars[0]), FadeIn(bars.vals[0]), FadeIn(bars.names[0]), FadeIn(yl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bars.bars[1]), FadeIn(bars.vals[1]), FadeIn(bars.names[1]), FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    def price(self):
        head = label(r"The price: \ not every program can be written", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label(r"every typed program stops, \ so the calculus cannot express a program that does not", font_size=22,
                  color=GREY_A),
            label(r"so it cannot be Turing complete: \ it cannot even interpret itself \ (diagonalization, \ "
                  r"Part 25)", font_size=22, color=NO),
            label(r"languages add general recursion back:", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.5)
        fix = MathTex(r"\frac{\Gamma \vdash f : T \to T}{\Gamma \vdash \mathsf{fix}\;f : T}\;\textsc{Fix}", font_size=36,
                      color=YES).next_to(pts, DOWN, buff=0.4)
        two = VGroup(
            VGroup(region(4.4, 0.6, r"ML, \ Haskell, \ OCaml", DATA, font_size=20),
                   label(r"\textsf{fix}: \ any recursion; \ programs may loop", font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.12),
            VGroup(region(4.4, 0.6, r"Agda, \ Coq/Rocq, \ Lean", HEAD, font_size=20),
                   label(r"only recursion that provably ends: \ a type is a theorem \ (ch. 12)", font_size=19,
                         color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=0.8).next_to(fix, DOWN, buff=0.5)
        with self.voiceover(
            "Termination has a price. <bookmark mark='a'/> If every typed program stops, then the calculus cannot "
            "express a program that runs forever, and so it is not Turing complete. It cannot even contain an "
            "interpreter for itself, by the diagonal argument of Part 25. <bookmark mark='b'/> Programming "
            "languages buy general recursion back with a fixed-point operator, fix, whose rule says that fix of a "
            "function from T to T has type T. <bookmark mark='c'/> ML, Haskell and OCaml include it, and their "
            "programs may loop. Proof assistants like Agda, Rocq and Lean refuse it, and accept only recursion that "
            "provably terminates, for a reason chapter twelve will make clear: in those languages a type is a "
            "theorem, and a looping program would prove anything."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]), Write(fix))
            vo.wait_until("c")
            self.play(FadeIn(two))
        self.wait(0.3)
        self.clear_scene()
