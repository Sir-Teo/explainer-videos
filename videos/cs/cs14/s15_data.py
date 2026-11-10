from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, load, mono


class Data(VoiceoverScene):
    def construct(self):
        self.card()
        self.adts()
        self.subtyping()
        self.unsound()
        self.gradual()

    def card(self):
        card = chapter_card(14, r"Data, subtyping and gradual types", r"How do real languages bend the rules?",
                            lit=(2006,), extra=((2006, r"EC2 and S3; \ gradual typing"),), part=PART)
        with self.voiceover("Chapter fourteen. Data, subtyping and gradual types."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def adts(self):
        head = label(r"Algebraic data types", font_size=36).to_edge(UP, buff=0.3)
        src = code(["type shape =", "  | Circle of float", "  | Rect of float * float", "",
                    "let area s = match s with", "  | Circle r -> 3.14159 *. r *. r", "  | Rect (w, h) -> w *. h",
                    "", "type 'a option = None | Some of 'a"], size=18, color=CODE).to_edge(LEFT, buff=0.8).shift(
            DOWN * 0.2)
        pts = VGroup(
            label(r"a \textbf{sum} of \textbf{products}: \ one of several shapes, \ each with its fields", font_size=21,
                  color=GREY_A),
            label(r"Curry--Howard again: \ sums are $\lor$, \ products are $\land$", font_size=21, color=GREY_A),
            label("exhaustiveness checking may warn; wildcard branches can hide newly added cases", font_size=19, color=YES),
            label(r"\texttt{option} instead of \texttt{null}: \ ``my billion-dollar mistake'' \ (Hoare, \ 2009)",
                  font_size=21, color=HEAD),
            label(r"make illegal states unrepresentable", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(src, RIGHT, buff=0.8)
        with self.voiceover(
            (
            "Algebraic data types describe alternatives and their fields. <bookmark mark='a'/> A shape can be a "
            "circle with a radius or a rectangle with width and height: a sum of products. <bookmark mark='b'/> "
            "The propositions-as-types dictionary interprets these constructors as choices and pairs, with the "
            "logical assumptions stated earlier. <bookmark mark='c'/> Pattern matching inspects the constructor. "
            "Exhaustiveness checking can report missing cases, but language settings, wildcards and guards affect "
            "the guarantee. Adding a triangle does not force every match to change if a wildcard already handles "
            "it. Nested patterns need more analysis than counting constructor names. <bookmark mark='d'/> An "
            "option type makes absence an explicit alternative. It can rule out an unhandled null dereference "
            "when programs respect its interface; extracting a value can still require handling the empty case. "
            "<bookmark mark='e'/> Make illegal states unrepresentable is a useful design goal. A type can encode "
            "a chosen invariant, not automatically every property the application needs."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src[:3]))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[1]))
            vo.wait_until("c")
            self.play(FadeIn(src[3:7]), FadeIn(pts[2]))
            vo.wait_until("d")
            self.play(FadeIn(src[7:]), FadeIn(pts[3]))
            vo.wait_until("e")
            self.play(FadeIn(pts[4]))
        self.wait(0.3)
        self.clear_scene()

    def subtyping(self):
        head = label(r"Subtyping, \ and which way the arrows point", font_size=34).to_edge(UP, buff=0.3)
        sub = MathTex(r"\frac{\Gamma \vdash t : S \qquad S <: T}{\Gamma \vdash t : T}", font_size=38).next_to(
            head, DOWN, buff=0.5)
        sl = label(r"a \texttt{Dog} can go wherever an \texttt{Animal} is expected", font_size=22,
                   color=GREY_A).next_to(sub, DOWN, buff=0.2)
        fn = MathTex(r"\frac{A' <: A \qquad B <: B'}{A \to B \;<:\; A' \to B'}", font_size=40, color=YES).next_to(
            sl, DOWN, buff=0.5)
        pts = VGroup(
            label(r"results: \ \textbf{covariant} \ (a function returning a \texttt{Dog} returns an \texttt{Animal})",
                  font_size=21, color=GREY_A),
            label(r"arguments: \ \textbf{contravariant} \ (a function that accepts any \texttt{Animal} accepts a "
                  r"\texttt{Dog})", font_size=21, color=GREY_A),
            label("unrestricted mutable arrays need invariant element types, or another safety mechanism", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(fn, DOWN, buff=0.4)
        with self.voiceover("Subtyping specifies which replacements preserve an interface's guarantees. <bookmark mark='a'/> A value of subtype S can be used where a T is expected under the language's subtype rules. A Dog can supply an Animal interface. <bookmark mark='b'/> For ordinary function subtyping, the replacement accepts at least the promised inputs and returns a sufficiently specific result. A function that can handle every Animal can serve a caller that supplies only Dogs. <bookmark mark='c'/> Results are covariant; arguments are contravariant. The arrows in the rule point in opposite directions for that reason. <bookmark mark='d'/> An unchecked mutable array both produces and consumes elements. Allowing Dog arrays to be used as writable Animal arrays would let a caller insert a Cat. Invariance prevents that substitution. Read-only views or runtime store checks permit other designs, with different contracts and costs.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(sub), FadeIn(sl), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Write(fn))
            vo.wait_until('c')
            self.play(FadeIn(pts[:2]))
            vo.wait_until('d')
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def unsound(self):
        g = load("gradual")
        c = g["covariant"]
        head = label(r"A deliberate hole, \ measured", font_size=34).to_edge(UP, buff=0.3)
        src = code(c["source"], size=16, color=CODE).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        res = VGroup(
            label(rf"\texttt{{tsc --strict}}: \ {'no errors' if not c['tsc_errors'] else 'errors'}", font_size=22,
                  color=YES if not c["tsc_errors"] else NO),
            label(r"\texttt{node}:", font_size=22, color=GREY_A),
            mono(c["runtime_error"] or "", 17, NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(src, DOWN, buff=0.45).align_to(src, LEFT)
        pts = VGroup(
            label(r"TypeScript makes arrays covariant on purpose: \ convenience over soundness", font_size=21,
                  color=GREY_A),
            label(r"Java did the same in 1995, \ and checks every array store at run time \ "
                  r"(\texttt{ArrayStoreException})", font_size=21, color=GREY_A),
            label(r"a type system can be useful without being sound: \ but then it promises less", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover("This recorded TypeScript example shows an intentional soundness tradeoff. <bookmark mark='a'/> The Dog array is assigned to an Animal-array variable. A Cat is pushed through that alias, and the original Dog-array expression later calls bark on the new element. <bookmark mark='b'/> The recorded compiler accepts it with exactly the displayed strict flag. Strict is a bundle of checks, not every possible checking option; additional indexed-access checks can report other concerns. <bookmark mark='c'/> Running the emitted JavaScript with the recorded Node version raises a TypeError because bark is not a function. The types were erased and supplied no runtime store barrier. <bookmark mark='d'/> Java's covariant reference arrays use a different contract: a runtime component-type check can reject an incompatible store. Compare the static rules and runtime checks together. Useful typing tools can deliberately offer less than the no-stuck-state theorem of a sound calculus.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(src), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(res[0]))
            vo.wait_until('c')
            self.play(FadeIn(res[1:]))
            vo.wait_until('d')
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def gradual(self):
        g = load("gradual")
        a = g["any"]
        head = label(r"Gradual typing", font_size=34).to_edge(UP, buff=0.3)
        src = code(a["source"], size=17, color=CODE).next_to(head, DOWN, buff=0.4)
        out = label(rf"\texttt{{tsc --strict}}: \ no errors; \ \texttt{{node}} prints \texttt{{{a['stdout']}}}",
                    font_size=22, color=NO).next_to(src, DOWN, buff=0.3)
        pts = VGroup(
            label("TypeScript \\texttt{any} disables checks; sound gradual models insert dynamic checks",
                  font_size=21, color=GREY_A),
            label(r"add types to an untyped program one function at a time: \ TypeScript, \ Python's hints, \ "
                  r"Hack", font_size=21, color=GREY_A),
            label(r"\textit{unsound} gradual typing \ (TypeScript): \ the types are erased; \ \texttt{any} switches "
                  r"checking off", font_size=21, color=NO),
            label(r"\textit{sound} gradual typing \ (Typed Racket): \ checks at every boundary, \ and they cost",
                  font_size=21, color=YES),
            label("2016 Typed Racket study: some tested configurations exceeded 100$\\times$ overhead",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(out, DOWN, buff=0.5)
        with self.voiceover(
            (
            "Gradual typing studies how precise and imprecise type information can coexist. <bookmark mark='a'/> "
            "A gradual unknown type is related to other types by a consistency relation, with checks determined "
            "by the chosen semantics. TypeScript's any, its unknown type and Python's optional type hints make "
            "different choices; these mechanisms should not all be treated as one sound cast calculus. <bookmark "
            "mark='b'/> In the displayed TypeScript program, any allows forty-two to pass to a string-typed "
            "parameter. Erasure leaves ordinary JavaScript execution, and the result printed here is NaN. No "
            "runtime string contract was inserted. <bookmark mark='c'/> Sound gradual systems can insert boundary "
            "checks and higher-order wrappers. A 2016 Typed Racket study measured very large slowdowns for some "
            "partially typed configurations. That is a historical workload result, not a bound for every current "
            "implementation. Coercion composition and other techniques improve particular costs. The research "
            "exercise asks for a stated semantics and baseline before discussing guarantees."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("b")
            self.play(FadeIn(out), FadeIn(pts[2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[3:]))
        self.wait(0.3)
        self.clear_scene()
