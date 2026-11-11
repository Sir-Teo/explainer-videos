from __future__ import annotations

from explainer.cs import *  # noqa: F403
from explainer.cs.lam import parse
from videos.cs.cs14.common import APP, CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, lam_tree, load, mono


class Terms(VoiceoverScene):
    def construct(self):
        self.card()
        self.grammar()
        self.free()
        self.capture()

    def card(self):
        card = chapter_card(1, r"Terms, variables and substitution", r"What is a function, written down?",
                            lit=(1936,), part=PART)
        with self.voiceover("Chapter one. Terms, variables and substitution."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def grammar(self):
        head = label(r"Three kinds of term", font_size=36).to_edge(UP, buff=0.3)
        g = MathTex(r"t \;::=\; x \;\mid\; \lambda x.\, t \;\mid\; t\;t", font_size=48).next_to(head, DOWN, buff=0.4)
        kinds = VGroup(
            VGroup(label(r"a variable", font_size=24, color=CODE), MathTex(r"x", font_size=36)),
            VGroup(label(r"an abstraction: \ a function of $x$", font_size=24, color=LAM),
                   MathTex(r"\lambda x.\, t", font_size=36)),
            VGroup(label(r"an application: \ $f$ applied to $a$", font_size=24, color=APP),
                   MathTex(r"f\;a", font_size=36)),
        )
        for k in kinds:
            k.arrange(DOWN, buff=0.15)
        kinds.arrange(RIGHT, buff=1.2).next_to(g, DOWN, buff=0.6)
        ex = parse(r"(\x. x x) ((\y. y) z)")
        tr = lam_tree(ex, dx=0.75, dy=0.62, font_size=20).to_edge(DOWN, buff=0.4).to_edge(RIGHT, buff=1.2)
        exl = VGroup(mono(r"(λx. x x) ((λy. y) z)", 20, CODE),
                     label(r"its syntax tree: \ @ for application", font_size=19, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(tr, LEFT, buff=0.8).shift(UP * 0.4)
        conv = label(r"conventions: \ $f\,a\,b$ means $(f\,a)\,b$; \ $\lambda x.$ reaches as far right as it can",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        with self.voiceover(
            (
            "The untyped lambda calculus has three term constructors. <bookmark mark='a'/> A variable; an "
            "abstraction, lambda x dot t, binding x in its body; and an application, one term applied to another. "
            "<bookmark mark='b'/> Read the example's parentheses carefully. The left function is lambda x, x x. "
            "Its single argument is the whole application of lambda y, y to z. The syntax tree makes that "
            "grouping explicit, with at signs for applications. <bookmark mark='c'/> Application normally "
            "associates to the left: f a b means the result of f a applied to b. A lambda body extends rightward "
            "until a closing delimiter. Parentheses override those conventions. The tree, rather than an "
            "ambiguous spoken string, determines what substitution will copy."
        )
        ) as vo:
            self.play(FadeIn(head), Write(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.1) for k in kinds], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(exl), FadeIn(tr))
            vo.wait_until("c")
            self.play(FadeIn(conv))
        self.wait(0.3)
        self.clear_scene()

    def free(self):
        s = load("subst")
        head = label(r"Free and bound", font_size=36).to_edge(UP, buff=0.3)
        t = MathTex(r"\lambda", r"x", r".\;", r"f", r"\;", r"x", r"\;", r"y", font_size=60).next_to(head, DOWN,
                                                                                                  buff=0.6)
        t[1].set_color(LAM)
        t[5].set_color(LAM)
        t[3].set_color(NO)
        t[7].set_color(NO)
        notes = VGroup(
            label(r"$x$ is \textbf{bound}: \ it refers to the $\lambda$ that introduces it", font_size=24,
                  color=LAM),
            label(rf"$f$ and $y$ are \textbf{{free}}: \ they come from outside \ (free variables: \ "
                  rf"$\{{{', '.join(s['free'])}\}}$)", font_size=24, color=NO),
            label(r"renaming a bound variable changes nothing: \ $\lambda x.\, x \;\equiv_\alpha\; \lambda y.\, y$",
                  font_size=24, color=GREY_A),
            label(r"$\alpha$-equivalent terms are the same function, \ like $\int f(x)\,dx$ and $\int f(t)\,dt$",
                  font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).next_to(t, DOWN, buff=0.6)
        arc = CurvedArrow(t[5].get_top() + UP * 0.12, t[1].get_top() + UP * 0.12, angle=1.1, color=LAM,
                          stroke_width=2, tip_length=0.12)
        with self.voiceover(
            "Variables come in two kinds. <bookmark mark='a'/> In lambda x, f x y, the x is bound: it refers to the "
            "lambda that introduced it, like a function's parameter. <bookmark mark='b'/> f and y are free. They "
            "refer to something outside the term, and the term's meaning depends on what they turn out to be. "
            "<bookmark mark='c'/> A bound variable's name does not matter. Lambda x, x and lambda y, y are the "
            "same function, the identity, and terms that differ only in bound names are called alpha equivalent, "
            "just as the integral of f of x d x is the integral of f of t d t."
        ) as vo:
            self.play(FadeIn(head), Write(t))
            vo.wait_until("a")
            self.play(Create(arc), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(VGroup(t[3], t[7]), color=NO))
            vo.wait_until("c")
            self.play(FadeIn(notes[2:]))
        self.wait(0.3)
        self.clear_scene()

    def capture(self):
        s = load("subst")
        head = label(r"Substitution, \ and the capture trap", font_size=36).to_edge(UP, buff=0.3)
        q = MathTex(r"(\lambda x.\, \lambda y.\, x)\; y", font_size=44).next_to(head, DOWN, buff=0.5)
        ql = label(r"``the function that ignores its second argument'', \ applied to a free $y$", font_size=21,
                   color=GREY_A).next_to(q, DOWN, buff=0.2)
        bad = VGroup(MathTex(r"\to\; \lambda y.\, y", font_size=40, color=NO),
                     label(r"wrong: \ the free $y$ was \textit{captured}; \ now it is the identity", font_size=21,
                           color=NO)).arrange(RIGHT, buff=0.5)
        good = VGroup(MathTex(r"\to\; \lambda y'.\, y", font_size=40, color=YES),
                      label(r"right: \ rename the bound $y$ first; \ still ignores its argument", font_size=21,
                            color=YES)).arrange(RIGHT, buff=0.5)
        VGroup(bad, good).arrange(DOWN, buff=0.4, aligned_edge=LEFT).next_to(ql, DOWN, buff=0.5)
        rules = VGroup(
            MathTex(r"x[x := s] = s \qquad y[x := s] = y", font_size=30),
            MathTex(r"(t_1\, t_2)[x := s] = t_1[x := s]\;\, t_2[x := s]", font_size=30),
            MathTex(r"(\lambda y.\, t)[x := s] = \lambda y.\, t[x := s] \quad \text{if } y \ne x,\; y \notin "
                    r"\mathrm{FV}(s)", font_size=30),
            label(r"otherwise rename $y$ to something fresh first", font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover("Computation in the lambda calculus is substitution: to apply a function, replace its parameter by the argument. That is subtler than it looks. <bookmark mark='a'/> Take lambda x, lambda y, x: a function that takes two arguments and returns the first. Apply it to a free variable y. <bookmark mark='b'/> Replacing x by y naively gives lambda y, y: the identity function. The free y has been captured by the inner lambda, and the meaning has changed. <bookmark mark='c'/> The correct answer renames the bound y first, to y prime, and gives lambda y prime, y: still a function that ignores its argument and returns y. <bookmark mark='d'/> Capture-avoiding substitution is defined by these rules, and the last one carries the condition. Getting this right is the first bug every implementer of a programming language meets, and the reason closures exist, as Part 15 will show.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(q), FadeIn(ql), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(bad))
            vo.wait_until('c')
            self.play(FadeIn(good))
            vo.wait_until('d')
            self.play(LaggedStart(*[FadeIn(r) for r in rules], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
