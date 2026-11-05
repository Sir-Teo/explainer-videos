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
            label(r"\texttt{match} must cover every case: \ the compiler checks", font_size=21, color=YES),
            label(r"\texttt{option} instead of \texttt{null}: \ ``my billion-dollar mistake'' \ (Hoare, \ 2009)",
                  font_size=21, color=HEAD),
            label(r"make illegal states unrepresentable", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(src, RIGHT, buff=0.8)
        with self.voiceover(
            "Real functional languages organise data as algebraic data types. <bookmark mark='a'/> A shape is "
            "either a circle with a radius, or a rectangle with a width and a height: a sum of products. <bookmark "
            "mark='b'/> These are Curry and Howard's or and and again, now as data. <bookmark mark='c'/> A match "
            "takes a shape apart, case by case, and the compiler checks that every case is covered, so adding a "
            "triangle later points you at every function that must change. <bookmark mark='d'/> An option type, "
            "either nothing or something, replaces the null pointer, which its inventor, Tony Hoare, called his "
            "billion-dollar mistake. <bookmark mark='e'/> The slogan: make illegal states unrepresentable."
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
            label(r"a mutable array is read \textit{and} written: \ it must be \textbf{invariant}", font_size=22,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(fn, DOWN, buff=0.4)
        with self.voiceover(
            "Object-oriented languages add subtyping. <bookmark mark='a'/> If S is a subtype of T, a term of type S "
            "may be used wherever a T is expected: a dog wherever an animal is. <bookmark mark='b'/> For functions "
            "the rule is subtle. A function from A to B can stand in for a function from A prime to B prime when "
            "its result is more specific, and its argument more general. <bookmark mark='c'/> Results vary in the "
            "same direction, covariantly. Arguments vary the opposite way, contravariantly. <bookmark mark='d'/> "
            "And a mutable array is both read, like a result, and written, like an argument. So it must be "
            "invariant: an array of dogs is not an array of animals."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(sub), FadeIn(sl))
            vo.wait_until("b")
            self.play(Write(fn))
            vo.wait_until("c")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("d")
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
        with self.voiceover(
            "Not every language follows the rule. <bookmark mark='a'/> Here is a short TypeScript program. An "
            "array of dogs is assigned to a variable of type array of animals, a cat is pushed onto it, and then "
            "the second element of the dog array is asked to bark. <bookmark mark='b'/> TypeScript's checker, in "
            "its strictest mode, accepts it. <bookmark mark='c'/> And node, running the result on this machine, "
            "fails: bark is not a function. <bookmark mark='d'/> TypeScript makes arrays covariant on purpose, "
            "trading soundness for convenience. Java made the same choice for arrays in 1995, and pays for it by "
            "checking every array store at run time. A type system can be useful without being sound, but then "
            "it promises less."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(FadeIn(res[1:]))
            vo.wait_until("d")
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
            label(r"a type \texttt{any} \ (or $?$) \ that is compatible with everything \ (Siek and Taha, \ 2006)",
                  font_size=21, color=GREY_A),
            label(r"add types to an untyped program one function at a time: \ TypeScript, \ Python's hints, \ "
                  r"Hack", font_size=21, color=GREY_A),
            label(r"\textit{unsound} gradual typing \ (TypeScript): \ the types are erased; \ \texttt{any} switches "
                  r"checking off", font_size=21, color=NO),
            label(r"\textit{sound} gradual typing \ (Typed Racket): \ checks at every boundary, \ and they cost",
                  font_size=21, color=YES),
            label(r"some mixtures ran over 100 times slower \ (Takikawa et al., \ 2016): \ an open problem",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(out, DOWN, buff=0.5)
        with self.voiceover(
            "Finally, a compromise most working programmers now use. <bookmark mark='a'/> Gradual typing, "
            "introduced by Jeremy Siek and Walid Taha in 2006, adds a type, written any or question mark, that is "
            "compatible with everything, so that a program can be typed one function at a time. TypeScript, "
            "Python's type hints and Hack work this way. <bookmark mark='b'/> In TypeScript the types are simply "
            "erased, and any switches checking off: passing forty-two to a function that expects a string passes "
            "the checker, and prints not a number. <bookmark mark='c'/> Sound gradual typing, as in Typed Racket, "
            "inserts checks wherever typed and untyped code meet, and those checks cost: a 2016 study found some "
            "mixtures over a hundred times slower. Making sound gradual typing cheap is still a research question."
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
