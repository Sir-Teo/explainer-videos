from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, grid_table, load, mono


class SystemF(WatchScene):
    def construct(self):
        self.card()
        self.system()
        self.church()
        self.parametric()

    def card(self):
        self.chapter(11, r"Polymorphism and free theorems", r"What can a type tell you about a program?", lit=(1972,), extra=((1972, r"Karp's 21; \ Girard's System F"),), part=PART, said="Chapter eleven. Polymorphism and free theorems.")

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
            label("explicit Church-style checking is decidable; unrestricted Curry-style inference is not", font_size=21, color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover("System F makes polymorphism explicit and allows quantifiers inside function types. <bookmark mark='a'/> Types gain for all alpha. Terms gain type abstraction, capital lambda alpha, and explicit type application. Girard introduced the system in 1972 and Reynolds independently in 1974. <bookmark mark='b'/> The identity first receives a type and then a value of that type. <bookmark mark='c'/> A function can now receive a polymorphic identity and instantiate it at both int and bool. The displayed pair uses the corresponding product extension. Ordinary Hindley Milner does not allow this higher-rank parameter without an extension. <bookmark mark='d'/> Distinguish two tasks. Checking fully annotated Church-style System F is decidable. Finding omitted type abstractions and applications in the unrestricted Curry-style typability problem is undecidable. Annotations or restricted inference systems make useful intermediate choices.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(g[0]), Write(g[1]), FadeIn(pts[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(Write(g[2]))
            vo.wait_until('c')
            self.play(Write(g[3]), FadeIn(pts[1]))
            vo.wait_until('d')
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
            label("closed pure normal inhabitants encode booleans, numerals and lists", font_size=22,
                  color=GREY_A),
            label("pure System F strongly normalizes; recursion and effects change the assumptions", font_size=22, color=YES),
        ).arrange(DOWN, buff=0.2).next_to(rows, DOWN, buff=0.6)
        with self.voiceover("Church encodings receive explicit polymorphic types here. <bookmark mark='a'/> A boolean chooses between two arguments of one arbitrary type. A numeral iterates a function, and a list provides a fold over its element type. The quantifiers let callers choose the result type. <bookmark mark='b'/> For closed terms in the pure total system, normalization and parametricity give these encodings their expected behavior. System F is strongly normalizing, yet represents a large class of total numerical functions related to second-order arithmetic's provably total functions. That is a precise proof-theoretic connection, not a claim that every mathematical function is computable or expressible. General recursion, effects and additional primitives require a fresh analysis of these properties.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[Write(r) for r in rows], lag_ratio=0.5), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()

    def parametric(self):
        self.ask(r"A function of type $\forall \alpha.\ \textsf{List}\,\alpha \to \textsf{List}\,\alpha$. \\ Could it add 1 to "
                 r"every element?", [r"yes", r"no"], 1,
                 say="A function that works on lists of every type alpha. Could it add one to each element?",
                 reveal="No. It knows nothing about alpha, so it can only rearrange, drop or copy elements.")
        head = label(r"Parametricity: \ the type limits the program", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(MathTex(r"\forall \alpha.\; \alpha \to \alpha", font_size=34),
                   label("in pure total System F: identity", font_size=22, color=GREY_A)),
            VGroup(MathTex(r"\forall \alpha.\; \alpha \to \alpha \to \alpha", font_size=34),
                   label("in that model: choose first or second", font_size=22, color=GREY_A)),
            VGroup(MathTex(r"g : \forall \alpha.\; \alpha\;\mathsf{list} \to \alpha\;\mathsf{list}", font_size=34),
                   label("parametric implementations act uniformly on element types", font_size=22,
                         color=GREY_A)),
        )
        for r in rows:
            r.arrange(RIGHT, buff=0.6)
        rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6)
        free = MathTex(r"\mathit{map}\;f\;(g\;l) \;=\; g\;(\mathit{map}\;f\;l)", font_size=42, color=YES).next_to(
            rows, DOWN, buff=0.6)
        fl = label("for total maps in the pure parametric model (Reynolds; Wadler)",
                   font_size=22, color=HEAD).next_to(free, DOWN, buff=0.25)
        with self.voiceover("A type can imply an equation when the language supplies parametricity. Work first in a pure, total setting. <bookmark mark='a'/> A closed function of type for all alpha, alpha to alpha must return its argument: it has no other alpha to manufacture. <bookmark mark='b'/> At for all alpha, alpha to alpha to alpha, it must consistently choose one of its two arguments, giving a Church boolean. <bookmark mark='c'/> For a function from lists of alpha to lists of alpha, behavior can depend on list shape while elements can only be rearranged, dropped or copied. It cannot inspect an arbitrary alpha. <bookmark mark='d'/> The square commutes: map f after g equals g after map f, for total f and finite lists. Reynolds's parametricity supports the proof; Wadler popularized such free theorems. With divergence, effects, runtime type inspection or primitives such as Haskell's seq, the assumptions and resulting theorem need adjustment.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, r in zip('abc', rows):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('d')
            self.play(Write(free), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

