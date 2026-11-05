from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import (CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, deriv_tree, grid_table, load,
                                   mono, term_tex)


class Types(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.syntax()
        self.rules()
        self.derivation()
        self.evaluation()

    def card(self):
        card = chapter_card(7, r"Simple types", r"Which programs make sense?", lit=(1940,),
                            extra=((1940, r"Church: \ the simple theory of types"),), part=PART)
        with self.voiceover("Chapter seven. Simple types."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def why(self):
        st = load("stlc")["stuck"]
        head = label(r"Programs that get stuck", font_size=36).to_edge(UP, buff=0.3)
        rows = [[s["term"].replace("\\", "λ"), s["stops_at"]] for s in st]
        tab = grid_table([r"program", r"where evaluation stops"], rows, widths=[5.0, 4.4], row_h=0.5, font_size=22,
                         mono_cols=(0, 1)).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"not a value, \ and no rule applies: \ \textbf{stuck}", font_size=23, color=NO),
            label(r"in a real machine: \ a crash, \ or worse, \ a silent wrong answer", font_size=22, color=GREY_A),
            label(r"``Well-typed programs cannot go wrong'' \ --- \ Robin Milner, \ 1978", font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Add booleans and numbers to the calculus, and some programs make no sense. <bookmark mark='a'/> If "
            "zero then true else false. The successor of true. The predecessor of a boolean. True applied to "
            "zero. Is zero of a function. <bookmark mark='b'/> Each one stops somewhere that is not an answer, "
            "with no rule to apply. It is stuck. On a real machine, the same mistake is a crash, or worse, a "
            "silent wrong answer computed from bits that meant something else. <bookmark mark='c'/> Types rule "
            "such programs out before they run. Robin Milner put it in a slogan in 1978: well-typed programs "
            "cannot go wrong. The next two chapters prove it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), *[FadeIn(c) for c in tab.cells[0]],
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pts[:2]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def syntax(self):
        head = label(r"The simply typed $\lambda$-calculus", font_size=36).to_edge(UP, buff=0.3)
        g = VGroup(
            MathTex(r"T \;::=\; \mathsf{Bool} \;\mid\; \mathsf{Nat} \;\mid\; T \to T", font_size=42),
            MathTex(r"t \;::=\; x \;\mid\; \lambda x{:}T.\; t \;\mid\; t\;t \;\mid\; \mathsf{true} \mid \mathsf{false} "
                    r"\mid \mathsf{if}\;t\;t\;t \mid 0 \mid \mathsf{succ}\;t \mid \mathsf{pred}\;t \mid \mathsf{iszero}\;t",
                    font_size=32),
        ).arrange(DOWN, buff=0.4).next_to(head, DOWN, buff=0.6)
        pts = VGroup(
            label(r"every parameter carries a type: \ $\lambda x{:}\mathsf{Nat}.\; \mathsf{succ}\;x$", font_size=23,
                  color=GREY_A),
            label(r"$A \to B$: \ the functions from $A$ to $B$; \ $\mathsf{Nat} \to \mathsf{Nat} \to \mathsf{Nat}$ "
                  r"\ takes two numbers", font_size=23, color=GREY_A),
            label(r"Church, \ 1940: \ types were invented to keep logic consistent", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(g, DOWN, buff=0.6)
        with self.voiceover(
            "The simply typed lambda calculus adds types to the language. <bookmark mark='a'/> A type is bool, or "
            "nat, or a function type A arrow B. <bookmark mark='b'/> Terms are as before, with booleans, "
            "numbers and their operations, except that every lambda states the type of its parameter. <bookmark "
            "mark='c'/> A arrow B is the type of functions from A to B. Arrows group to the right, so nat to nat "
            "to nat is a function of two numbers. <bookmark mark='d'/> Church introduced this system in 1940, not "
            "for programming, but to keep logic consistent: the untyped calculus could express paradoxes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(g[0]))
            vo.wait_until("b")
            self.play(Write(g[1]), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        head = label(r"Typing rules", font_size=36).to_edge(UP, buff=0.3)
        rs = VGroup(
            MathTex(r"\frac{x{:}T \in \Gamma}{\Gamma \vdash x : T}\;\textsc{Var}", font_size=34),
            MathTex(r"\frac{\Gamma,\, x{:}A \vdash t : B}{\Gamma \vdash \lambda x{:}A.\, t \;:\; A \to B}\;\textsc{Abs}",
                    font_size=34),
            MathTex(r"\frac{\Gamma \vdash f : A \to B \qquad \Gamma \vdash a : A}{\Gamma \vdash f\;a : B}\;\textsc{App}",
                    font_size=34),
        ).arrange(RIGHT, buff=0.7).next_to(head, DOWN, buff=0.6)
        if rs.width > 13:
            rs.scale_to_fit_width(13)
        rs2 = VGroup(
            MathTex(r"\frac{\Gamma \vdash t : \mathsf{Nat}}{\Gamma \vdash \mathsf{succ}\;t : \mathsf{Nat}}", font_size=32),
            MathTex(r"\frac{\Gamma \vdash c : \mathsf{Bool} \quad \Gamma \vdash a : T \quad \Gamma \vdash b : T}"
                    r"{\Gamma \vdash \mathsf{if}\;c\;a\;b : T}", font_size=32),
        ).arrange(RIGHT, buff=0.9).next_to(rs, DOWN, buff=0.6)
        pts = VGroup(
            label(r"\textsc{Abs}: \ to type a function, \ assume its parameter has its declared type, \ type the body",
                  font_size=21, color=GREY_A),
            label(r"\textsc{App}: \ a function from $A$ accepts only an $A$", font_size=21, color=GREY_A),
            label(r"\textsc{If}: \ both branches must have the same type", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(rs2, DOWN, buff=0.5)
        with self.voiceover(
            "The type checker applies a handful of rules, written as in Part 13: what must be known above the "
            "line, what follows below. <bookmark mark='a'/> A variable has the type the context gives it. "
            "<bookmark mark='b'/> To type a function, assume its parameter has the declared type, and type the "
            "body; the function's type is the arrow from one to the other. <bookmark mark='c'/> A function from A "
            "to B, applied to an A, gives a B, and only an A will do. <bookmark mark='d'/> The successor of a "
            "number is a number, and an if needs a boolean condition and two branches of the same type. That is "
            "the whole checker."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rs[0]))
            vo.wait_until("b")
            self.play(FadeIn(rs[1]), FadeIn(pts[0]))
            vo.wait_until("c")
            self.play(FadeIn(rs[2]), FadeIn(pts[1]))
            vo.wait_until("d")
            self.play(FadeIn(rs2), FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    def derivation(self):
        d = load("stlc")
        head = label(r"A derivation: \ why the term has its type", font_size=34).to_edge(UP, buff=0.3)
        tree = deriv_tree(d["small_deriv"], font_size=24)
        if tree.width > 13:
            tree.scale_to_fit_width(13)
        tree.next_to(head, DOWN, buff=0.7)
        cap = VGroup(
            label(r"read upward: \ the conclusion at the bottom, \ the rules it rests on above", font_size=21,
                  color=GREY_A),
            label(rf"generated by our checker; \ for \ \texttt{{twice succ 3}} \ the tree has {d['size']} rules",
                  font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Typing a whole term builds a tree of rules, called a derivation. <bookmark mark='a'/> Here our checker "
            "types lambda x of type nat, successor of x, applied to two. At the bottom is the conclusion: the term "
            "has type nat, by the application rule. Above it, its two premises: the function has type nat to nat, "
            "by the abstraction rule, which in turn rests on typing successor of x with x assumed to be a nat. And "
            "the argument two is a nat, as the successor of the successor of zero. <bookmark mark='b'/> Every "
            "well-typed term has such a tree, and the checker's work is exactly to build it. For a term that "
            "applies twice to successor and three, the tree has sixteen rules."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tree.concl), Create(tree.line), FadeIn(tree.rule))
            self.play(FadeIn(tree.prem), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def evaluation(self):
        d = load("stlc")
        head = label(r"And it runs: \ small steps", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup()
        for k, s in enumerate(d["trace"]):
            t = MathTex(term_tex(s["term"]), font_size=28, color=YES if k == len(d["trace"]) - 1 else WHITE)
            r = VGroup(t, label(s["rule"] or "", font_size=18, color=HEAD) if s["rule"] else VGroup())
            rows.add(r)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.6)
        for r in rows:
            if len(r[1]):
                r[1].next_to(r[0], LEFT, buff=0.4)
        rows.set_x(0.6)
        note = label(r"call-by-value: \ \textsc{E-App1} reduces the function, \ \textsc{E-App2} the argument, \ "
                     r"\textsc{E-AppAbs} substitutes a value", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Typed terms run the same way as before, one small step at a time, by call-by-value. <bookmark "
            "mark='a'/> Twice, applied to successor and three. First the function position is reduced, substituting "
            "successor for f. Then the argument three goes in. The inner application must finish before the outer "
            "one can fire, and the answer is five. <bookmark mark='b'/> Each step is justified by a rule, named on "
            "the left, and the next chapter proves something about every such step."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for r in rows:
                self.play(FadeIn(r, shift=DOWN * 0.05), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
