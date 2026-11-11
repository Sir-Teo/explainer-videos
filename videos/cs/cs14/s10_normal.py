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
        card = chapter_card(9, "Why the typed core terminates", r"What do types cost?", lit=(1967,),
                            extra=((1967, r"Tait: \ strong normalization"),), part=PART)
        with self.voiceover((
            "Chapter nine. Why the typed core terminates."
        )):
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
            (
            "Try typing lambda x, x x with finite simple types. <bookmark mark='a'/> In its function position, x "
            "must have some arrow type A to B. <bookmark mark='b'/> The same x is also its own argument, which "
            "must have type A. Simple typing gives that binder one monomorphic type. <bookmark mark='c'/> "
            "Unification therefore demands A equals A to B, with A occurring inside its own proposed definition. "
            "<bookmark mark='d'/> No finite simple type solves this equation. Recursive-type systems or richer "
            "polymorphic rules are different systems and require their own reasoning. <bookmark mark='e'/> Our "
            "Hindley Milner engine rejects this application with its occurs check. Omega and Y are untypable in "
            "the recursion-free simply typed calculus. Their rejection is a fact about this typing discipline; it "
            "is not a claim that every language with static types rejects all self-application or recursion."
        )
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
        with self.voiceover("In fact no typed term runs forever. <bookmark mark='a'/> William Tait proved in 1967 that every well-typed term of the simply typed calculus reaches a normal form, whichever order of reduction you choose. <bookmark mark='b'/> The obvious proof by induction on the size of the term fails, because a beta step can make a term bigger, by copying its argument. <bookmark mark='c'/> Tait's idea was to prove something stronger, defined by induction on the type. A number is good if it terminates. A function is good if it sends every good argument to a good result. <bookmark mark='d'/> Then show that every typed term is good, and every good term terminates. This method, now called logical relations, has been the workhorse of type theory ever since.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(thm), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(why[0]))
            vo.wait_until('c')
            self.play(FadeIn(why[1:4]))
            vo.wait_until('d')
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
            label(rf"untyped: \ {un:,} random closed terms, \ {n['untyped_no_stop']} reached the limit", font_size=21,
                  color=NO),
            label(rf"typed: \ {s['terms']:,} terms, \ all finished, \ the longest in {s['max_steps']} steps",
                  font_size=21, color=YES),
            label(r"no finite test proves termination; \ for the typed ones, \ the theorem does", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        with self.voiceover("The experiment compares two generated populations. <bookmark mark='a'/> Of two thousand random closed untyped terms, one hundred and thirty-six do not finish within four hundred normal-order steps. That means the budget was exhausted; it does not independently prove that each of those terms diverges. The sampling grammar and seed define this population. <bookmark mark='b'/> All five thousand terms in the separate well-typed sample finish within the evaluator's limits. No finite experiment establishes universal termination. For the recursion-free simply typed calculus, strong normalization supplies the general theorem. The bar chart reports the samples; the proof explains the model's guarantee.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(bars.bars[0]), FadeIn(bars.vals[0]), FadeIn(bars.names[0]), FadeIn(yl), FadeIn(side[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(bars.bars[1]), FadeIn(bars.vals[1]), FadeIn(bars.names[1]), FadeIn(side[1:]))
        self.wait(0.3)
        self.clear_scene()

    def price(self):
        head = label(r"The price: \ not every program can be written", font_size=34).to_edge(UP, buff=0.3)
        pts = VGroup(
            label("the simply typed core without general recursion is strongly normalizing", font_size=22,
                  color=GREY_A),
            label("no uniform-code self-evaluator satisfying the diagonalization assumptions", font_size=22, color=NO),
            label(r"languages add general recursion back:", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(head, DOWN, buff=0.5)
        fix = MathTex(r"\frac{\Gamma \vdash f : T \to T}{\Gamma \vdash \mathsf{fix}\;f : T}\;\textsc{Fix}", font_size=36,
                      color=YES).next_to(pts, DOWN, buff=0.4)
        two = VGroup(
            VGroup(region(4.4, 0.6, r"ML, \ Haskell, \ OCaml", DATA, font_size=20),
                   label(r"\textsf{fix}: \ any recursion; \ programs may loop", font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.12),
            VGroup(region(4.4, 0.6, r"Agda, \ Coq/Rocq, \ Lean", HEAD, font_size=20),
                   label("total logical core; partial, unsafe and noncomputable facilities have separate rules", font_size=19,
                         color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=0.8).next_to(fix, DOWN, buff=0.5)
        with self.voiceover("Strong normalization has a precise boundary. <bookmark mark='a'/> The simply typed calculus without general recursion cannot express a divergent computation, so it is not Turing complete. Diagonal arguments also restrict universal evaluation with a common type of program codes. Encoding assumptions matter: differently typed notions of self-interpretation need separate treatment. <bookmark mark='b'/> A general fixed-point operator changes the calculus. Given a function from T to T, fix produces a T, and its unfolding can continue forever. Safety can survive this extension even though termination does not. <bookmark mark='c'/> ML, Haskell and OCaml support general recursion. Proof assistants keep their trusted logical core consistent by restricting recursive definitions or requiring termination arguments. Their executable facilities can also include partial, unsafe or noncomputable features with carefully separated trust rules. The theorem concerns the specified core, not every command a proof-assistant installation can execute.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pts[:2]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[2]), Write(fix))
            vo.wait_until('c')
            self.play(FadeIn(two))
        self.wait(0.3)
        self.clear_scene()
