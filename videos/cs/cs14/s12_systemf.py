from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


class SystemF(VoiceoverScene):
    def construct(self):
        self.card()
        self.system()
        self.church()
        self.parametric()
        self.checked()

    def card(self):
        card = chapter_card(11, r"Polymorphism and free theorems", r"What can a type tell you about a program?",
                            lit=(1972,), extra=((1972, r"Karp's 21; \ Girard's System F"),), part=PART)
        with self.voiceover("Chapter eleven. Polymorphism and free theorems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def system(self):
        head = label(r"System F: \ $\forall$ anywhere", font_size=36).to_edge(UP, buff=0.3)
        g = VGroup(
            MathTex(r"T \;::=\; \alpha \;\mid\; T \to T \;\mid\; \forall \alpha.\, T", font_size=40),
            MathTex(r"t \;::=\; \cdots \;\mid\; \Lambda \alpha.\; t \;\mid\; t\,[T]", font_size=40),
            MathTex(r"\mathit{id} \;=\; \Lambda \alpha.\; \lambda x{:}\alpha.\; x \;\;:\;\; \forall \alpha.\; \alpha \to \alpha",
                    font_size=36, color=YES),
            MathTex(r"\lambda \mathit{id}{:}(\forall \alpha.\, \alpha \to \alpha).\;\; (\mathit{id}\,[\mathsf{int}]\;1,\;\; "
                    r"\mathit{id}\,[\mathsf{bool}]\;\mathsf{true})", font_size=32, color=HEAD),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"functions that take types as arguments \ (Girard, \ 1972; \ Reynolds, \ 1974)", font_size=21,
                  color=GREY_A),
            label(r"the program ML could not type, \ chapter 10, \ is fine here", font_size=21, color=HEAD),
            label(r"but its types must be written: \ inference is undecidable", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "ML allows for all only at the outside of a type. System F allows it anywhere. <bookmark mark='a'/> "
            "Types gain a quantifier, for all alpha, and terms gain functions of types: capital lambda alpha, and "
            "application to a type. Jean-Yves Girard found the system in 1972, for logic, and John Reynolds "
            "independently in 1974, for programming. <bookmark mark='b'/> The identity takes a type alpha, then a "
            "value of that type. <bookmark mark='c'/> And now a function can take the polymorphic identity as an "
            "argument and use it at two types, which ML could not type. <bookmark mark='d'/> The price is that the "
            "types must be written: inference is undecidable."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(g[0]), Write(g[1]), FadeIn(pts[0]))
            vo.wait_until("b")
            self.play(Write(g[2]))
            vo.wait_until("c")
            self.play(Write(g[3]), FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def church(self):
        head = label(r"Church's encodings, \ typed", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\mathsf{Bool} \;=\; \forall \alpha.\; \alpha \to \alpha \to \alpha", font_size=38),
            MathTex(r"\mathsf{Nat} \;=\; \forall \alpha.\; (\alpha \to \alpha) \to \alpha \to \alpha", font_size=38),
            MathTex(r"\mathsf{List}\;\tau \;=\; \forall \alpha.\; (\tau \to \alpha \to \alpha) \to \alpha \to \alpha",
                    font_size=38),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"chapter 3's booleans, numerals and lists are exactly the terms of these types", font_size=22,
                  color=GREY_A),
            label(r"System F still always terminates \ (Girard), \ yet expresses every function provably total in "
                  r"second-order arithmetic", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(rows, DOWN, buff=0.6)
        with self.voiceover(
            "System F gives chapter three's encodings honest types. <bookmark mark='a'/> A boolean takes two "
            "things of any one type and returns one of them. A numeral takes a function from some type to itself, "
            "and a starting value, and returns a value of that type. A list of taus is its own fold. <bookmark "
            "mark='b'/> Every term of these types behaves like a boolean, a number or a list. And System F, like "
            "the simply typed calculus, always terminates, as Girard proved, yet it can express every function "
            "that second-order arithmetic can prove total: almost everything a mathematician would call a function."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[Write(r) for r in rows], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def parametric(self):
        head = label(r"Parametricity: \ the type limits the program", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(MathTex(r"\forall \alpha.\; \alpha \to \alpha", font_size=34),
                   label(r"must be the identity: \ it has nothing else to return", font_size=22, color=GREY_A)),
            VGroup(MathTex(r"\forall \alpha.\; \alpha \to \alpha \to \alpha", font_size=34),
                   label(r"returns its first or its second argument: \ a boolean", font_size=22, color=GREY_A)),
            VGroup(MathTex(r"g : \forall \alpha.\; \alpha\;\mathsf{list} \to \alpha\;\mathsf{list}", font_size=34),
                   label(r"cannot look inside the elements: \ only rearrange, \ drop or copy them", font_size=22,
                         color=GREY_A)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.6)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6)
        free = MathTex(r"\mathit{map}\;f\;(g\;l) \;=\; g\;(\mathit{map}\;f\;l)", font_size=42, color=YES).next_to(
            rows, DOWN, buff=0.6)
        fl = label(r"for every $f$ and every list $l$: \ a \textbf{theorem for free} \ (Reynolds 1983; \ Wadler 1989)",
                   font_size=22, color=HEAD).next_to(free, DOWN, buff=0.25)
        with self.voiceover(
            "A polymorphic type constrains a program more than you might expect. <bookmark mark='a'/> A function of "
            "type for all alpha, alpha to alpha, knows nothing about its argument, so it has nothing to return but "
            "the argument itself: it must be the identity, or never return. <bookmark mark='b'/> For all alpha, "
            "alpha to alpha to alpha, must return one of its two arguments: it is a Church boolean. <bookmark "
            "mark='c'/> And a function from lists of alpha to lists of alpha cannot look inside the elements. All "
            "it can do is rearrange them, drop some, or copy some, based on the shape of the list alone. <bookmark "
            "mark='d'/> So it commutes with map: changing the elements first, or after, gives the same result. "
            "Reynolds called this parametricity, and Philip Wadler's 1989 paper named such results theorems for "
            "free: you read them off the type, without looking at the program."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(Write(free), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    def checked(self):
        s = load("systemf")
        head = label(r"A free theorem, \ tested", font_size=34).to_edge(UP, buff=0.3)
        rows, cols = [], []
        for r in s["rows"]:
            rows.append([r["g"].split(" (")[0], r["type"], f"{r['held']} / {r['trials']}"])
            ok = r["held"] == r["trials"]
            cols.append([WHITE, WHITE, YES if ok else NO])
        tab = grid_table([r"$g$", r"inferred type", r"$\mathit{map}\,f \circ g = g \circ \mathit{map}\,f$"], rows,
                         widths=[4.4, 3.8, 3.4], row_h=0.55, font_size=20, colors=cols, mono_cols=(0, 1)).next_to(
            head, DOWN, buff=0.5)
        cap = label(r"random lists and random $f(x) = ax + b$, \ run in the $\lambda$-core", font_size=19,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        pts = VGroup(
            label(r"the four polymorphic functions never fail", font_size=22, color=YES),
            label(r"a function that \textit{does} look at the elements \ (add one: \ \texttt{int list -> int list}) "
                  r"\ breaks it at once", font_size=21, color=NO),
            label(r"compilers use such laws to fuse loops: \ \texttt{map f (map g l)} into one pass \ (GHC)",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.18).next_to(cap, DOWN, buff=0.4)
        with self.voiceover(
            "We can test the free theorem in the lambda core. <bookmark mark='a'/> For four functions whose "
            "inferred type is lists of tick a to lists of tick a: reverse, take three, every other element, and "
            "duplicate each element, we compared map f after g with g after map f, on two hundred random lists and "
            "random linear functions f. <bookmark mark='b'/> They agree every time. <bookmark mark='c'/> A function "
            "of the less general type int list to int list, which adds one to each element, breaks the law at the "
            "first try. Only the type made the promise. <bookmark mark='d'/> Compilers use laws like this. GHC, the "
            "Haskell compiler, rewrites map f of map g into a single loop, safely, because the types guarantee it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]],
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:5]], lag_ratio=0.3), FadeIn(cap),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[5])), FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()
