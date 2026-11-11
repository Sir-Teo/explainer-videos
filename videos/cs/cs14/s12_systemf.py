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
        with self.voiceover("A type can imply an equation when the language supplies parametricity. Work first in a pure, total setting. <bookmark mark='a'/> A closed function of type for all alpha, alpha to alpha must return its argument: it has no other alpha to manufacture. <bookmark mark='b'/> At for all alpha, alpha to alpha to alpha, it must consistently choose one of its two arguments, giving a Church boolean. <bookmark mark='c'/> For a function from lists of alpha to lists of alpha, behavior can depend on list shape while elements can only be rearranged, dropped or copied. It cannot inspect an arbitrary alpha. <bookmark mark='d'/> The square commutes: map f after g equals g after map f, for total f and finite lists in this model. Reynolds's parametricity supports the proof; Wadler popularized such free theorems. With divergence, effects, runtime type inspection or primitives such as Haskell's seq, the assumptions and resulting theorem need adjustment.") as vo:
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

    def checked(self):
        s = load("systemf")
        head = label(r"Map commutation: tests and a boundary", font_size=34).to_edge(UP, buff=0.3)
        rows, colors = [], []
        for r in s['rows']:
            rows.append([r['g'].split(' (')[0], r['type'], f"{r['held']} / {r['trials']}"])
            colors.append([WHITE,WHITE,YES if r['held']==r['trials'] else NO])
        tab = grid_table([r"$g$", r"printed inferred type", r"commutation checks"], rows,
                         widths=[3.7,4.2,2.7], row_h=0.48, font_size=20,
                         colors=colors, mono_cols=(0,1)).next_to(head, DOWN, buff=0.4)
        cap = label(r"first four: 200 finite lists and integer affine maps each", font_size=19,
                    color=GREY_B).next_to(tab, DOWN, buff=0.15)
        pts = VGroup(
            label(r"shape-only implementations: sampled agreement", font_size=21, color=YES),
            label(r"the toy core's unrestricted equality is outside pure System F parametricity",
                  font_size=20, color=NO),
        ).arrange(DOWN, buff=0.18).next_to(cap, DOWN, buff=0.3)
        w = s['equality_counterexample']
        values = VGroup(mono('l = ' + str(w['input']), 25, CODE),
                        mono('g l = []',25, CODE), mono('map f l = [0, 0]',25,CODE),
                        VGroup(mono('map f (g l) = []',24,NO), mono('g (map f l) = [0]',24,NO)).arrange(DOWN,buff=0.2))
        for m, pos in zip(values, [LEFT*3.6+UP*1.5,RIGHT*3.1+UP*1.5,
                                   LEFT*3.6+DOWN*0.7,RIGHT*3.1+DOWN*0.7]): m.move_to(pos)
        arrows = VGroup(Arrow(values[0].get_right(),values[1].get_left(),buff=0.2,color=FUNC),
                        Arrow(values[0].get_bottom(),values[2].get_top(),buff=0.2,color=DATA),
                        Arrow(values[1].get_bottom(),values[3].get_top(),buff=0.2,color=DATA),
                        Arrow(values[2].get_right(),values[3].get_left(),buff=0.2,color=FUNC))
        ops = VGroup(mono('g',21,FUNC).next_to(arrows[0],UP,buff=0.1),
                     mono('map (fun x -> 0)',17,DATA).next_to(arrows[1],LEFT,buff=0.12),
                     mono('map f',19,DATA).next_to(arrows[2],RIGHT,buff=0.12),
                     mono('g',21,FUNC).next_to(arrows[3],DOWN,buff=0.1))
        program = mono('g [h; j; ...] = if h = j then [h] else []',20,CODE).move_to(DOWN*2.1)
        boundary = label(r"the map merges unequal elements: the square does not commute",font_size=23,
                         color=NO).next_to(program,DOWN,buff=0.35)
        with self.voiceover("The lambda-core experiment needs one more boundary. <bookmark mark='a'/> Four shape-based functions reverse, take three, select every other element and duplicate elements. Each passes two hundred sampled comparisons using finite lists and integer affine maps. <bookmark mark='b'/> These results exercise those implementations; they do not prove a universal equation for every function with that printed type. <bookmark mark='c'/> The monomorphic add-one witness fails. More subtly, our toy core has unrestricted polymorphic equality. A function that compares its first two elements still receives the printed type tick a list to tick a list, yet a constant map can merge unequal elements and break the equation. That primitive is outside pure System F parametricity. Real ML equality constraints also need more modeling than this toy type printer supplies. <bookmark mark='d'/> Follow both routes through the diagram, and check the counterexample. Compiler fusion needs a valid equation under the actual language semantics and rule conditions; type compatibility alone is insufficient.") as vo:
            self.play(FadeIn(head),run_time=0.5)
            self.play(FadeIn(tab.rule),*[FadeIn(c) for c in tab.cells[0]],
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:5]],lag_ratio=0.25),FadeIn(cap),run_time=1.3)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[0]))
            vo.wait_until('c')
            self.play(FadeIn(VGroup(*tab.cells[5])),FadeIn(VGroup(*tab.cells[6])),FadeIn(pts[1]))
            vo.wait_until('d')
            self.play(FadeOut(tab),FadeOut(cap),FadeOut(pts))
            self.play(FadeIn(values),Create(arrows),FadeIn(ops),FadeIn(program),FadeIn(boundary))
        self.wait(0.3)
        self.clear_scene()
