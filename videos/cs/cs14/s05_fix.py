from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import (CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, grid_table, load,
                                   mono)


class Recursion(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.ycomb()
        self.factorial()
        self.zcomb()

    def card(self):
        card = chapter_card(4, r"Recursion without names", r"How can a nameless function call itself?",
                            lit=(1941,), extra=((1941, r"Church: \ \textit{The Calculi of Lambda-Conversion}"),),
                            part=PART)
        with self.voiceover("Chapter four. Recursion without names."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def problem(self):
        head = label(r"A function that mentions itself", font_size=36).to_edge(UP, buff=0.3)
        want = MathTex(r"\mathit{fact} = \lambda n.\; \mathsf{if}\; (n = 0)\; 1\; (n \times \mathit{fact}\,(n-1))",
                       font_size=34).next_to(head, DOWN, buff=0.5)
        bad = label(r"but $\lambda$-terms have no names: \ \textit{fact} cannot refer to itself", font_size=23,
                    color=NO).next_to(want, DOWN, buff=0.35)
        F = MathTex(r"F = \lambda \mathit{self}.\; \lambda n.\; \mathsf{if}\; (n = 0)\; 1\; (n \times \mathit{self}\,"
                    r"(n-1))", font_size=34, color=YES).next_to(bad, DOWN, buff=0.5)
        fl = label(r"make the recursive call a parameter", font_size=22, color=YES).next_to(F, DOWN, buff=0.2)
        fp = MathTex(r"\mathit{fact} \;=\; F\;\mathit{fact}", font_size=44, color=HEAD).next_to(fl, DOWN, buff=0.5)
        fpl = label(r"\textit{fact} is a \textbf{fixed point} of $F$: \ $F$ leaves it unchanged", font_size=23,
                    color=HEAD).next_to(fp, DOWN, buff=0.25)
        with self.voiceover("How can a function call itself, when functions have no names? <bookmark mark='a'/> We would like to define factorial: one if n is zero, and otherwise n times factorial of n minus one. <bookmark mark='b'/> But in the lambda calculus there is no way to write the name fact inside its own definition. <bookmark mark='c'/> So make the recursive call a parameter. F takes a function, self, and returns a factorial that calls self for the smaller case. F is an ordinary lambda term. <bookmark mark='d'/> What we want is a function fact such that F applied to fact is fact again. In the language of mathematics, fact is a fixed point of F. All we need is a way to find fixed points.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(want), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(bad))
            vo.wait_until('c')
            self.play(Write(F), FadeIn(fl))
            vo.wait_until('d')
            self.play(Write(fp), FadeIn(fpl))
        self.wait(0.3)
        self.clear_scene()

    def ycomb(self):
        f = load("fix")
        head = label(r"The Y combinator", font_size=36).to_edge(UP, buff=0.3)
        y = MathTex(r"Y = \lambda f.\; (\lambda x.\, f\,(x\,x))\;(\lambda x.\, f\,(x\,x))", font_size=40,
                    color=HEAD).next_to(head, DOWN, buff=0.5)
        steps = VGroup(*[mono(s, 18, CODE) for s in f["unfold"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.next_to(y, DOWN, buff=0.6)
        arrows = VGroup(*[MathTex(r"\to_\beta", font_size=26, color=GREY_B).next_to(s, LEFT, buff=0.2)
                          for s in steps[1:]])
        punch = MathTex(r"Y\,g \;\to_\beta\; \cdots \;\to_\beta\; g\,(\,\cdots\,) \;=_\beta\; g\,(Y\,g)",
                        font_size=36, color=YES).next_to(steps, DOWN, buff=0.5)
        note = VGroup(
            label(r"the inner term is the one we started from, \ one step in: \ $Y\,g$ is a fixed point of $g$",
                  font_size=21, color=GREY_A),
            label(r"it is Omega's self-application, \ with $g$ wrapped around each copy", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover("Haskell Curry's Y combinator finds them. <bookmark mark='a'/> Y takes f and applies lambda x, f of x x, to itself. <bookmark mark='b'/> Watch it run on some g. One step substitutes g. <bookmark mark='c'/> The next applies the self-application, and out comes g, applied to the very term we had a moment ago. <bookmark mark='d'/> So Y g reduces to g of something that is itself equal to Y g. Y g is a fixed point of g, for every g. <bookmark mark='e'/> Look closely and it is omega again: the same self-application that looped forever, with g wrapped around each copy, so each turn of the loop hands g one more chance to use itself.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(y), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(steps[0]))
            self.play(FadeIn(steps[1]), FadeIn(arrows[0]))
            vo.wait_until('c')
            self.play(FadeIn(steps[2]), FadeIn(arrows[1]))
            vo.wait_until('d')
            self.play(Write(punch))
            vo.wait_until('e')
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()

    def factorial(self):
        f = load("fix")
        head = label(r"Factorial, \ through Y", font_size=36).to_edge(UP, buff=0.3)
        rows = [[str(r["n"]), str(r["value"]), f"{r['steps']:,}"] for r in f["fact"]]
        tab = grid_table([r"$n$", r"$Y\,F\,\underline{n}$", r"$\beta$-steps, \ normal order"], rows,
                         widths=[1.2, 2.2, 3.4], row_h=0.48, font_size=22, mono_cols=(0, 1, 2)).next_to(
            head, DOWN, buff=0.6).shift(LEFT * 3)
        ch = bar_chart([r["steps"] for r in f["fact"]], [str(r["n"]) for r in f["fact"]], [FUNC] * 5, height=3.2,
                       bar_w=0.7, gap=0.4, log=True, fmt_=lambda v: f"{v:,.0f}", font_size=17).next_to(tab, RIGHT,
                                                                                                    buff=1.2)
        ch.scale_to_fit_width(4.8).to_edge(RIGHT, buff=0.6)
        notes = VGroup(
            label(r"correct: \ $4! = 24$, \ from functions alone", font_size=22, color=YES),
            label(r"logarithmic bar heights; \ each argument copy is reduced again \ (chapter 5)", font_size=21,
                  color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover("Now combine everything so far. <bookmark mark='a'/> With Church numerals, booleans, multiplication and Kleene's predecessor, F is an ordinary term, and Y F is factorial. Our reducer evaluates it for n from zero to four, and the answers are one, one, two, six and twenty-four. <bookmark mark='b'/> Recursion, from functions that have no names. <bookmark mark='c'/> But look at the cost. Four factorial takes over ten thousand steps, and each extra n multiplies the work. Normal order copies arguments before evaluating them, and then evaluates each copy separately. The next chapter is about exactly this.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(tab), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(notes[0]))
            vo.wait_until('c')
            self.play(FadeIn(ch), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def zcomb(self):
        f = load("fix")
        head = label(r"Call-by-value needs two delays", font_size=34).to_edge(UP, buff=0.3)
        y = MathTex(r"Y = \lambda f.\;(\lambda x.\,f(x\,x))\;(\lambda x.\,f(x\,x))",
                    font_size=32, color=NO).next_to(head, DOWN, buff=0.4)
        z = MathTex(r"Z = \lambda f.\;(\lambda x.\,f(\lambda v.\,x\,x\,v))\;"
                    r"(\lambda x.\,f(\lambda v.\,x\,x\,v))", font_size=30,
                    color=YES).next_to(y, DOWN, buff=0.35)
        observed = VGroup(
            label(r"$Y\,F$: fuel limit reached", font_size=20, color=NO),
            label(r"$Z\,F$: closure returned", font_size=20, color=YES),
            label(r"$Z\,F\,0$: eager branches hit fuel limit", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(LEFT * 3.4 + DOWN * 0.5)
        if observed.width > 6: observed.scale_to_fit_width(6)
        delayed = MathTex(r"F_{\mathrm{delay}}", font_size=24, color=YES).move_to(RIGHT * 3.1 + UP * 1.0)
        condition = MathTex(r"\mathsf{iszero}\;n", font_size=29, color=HEAD).move_to(RIGHT * 3.1 + UP * 0.4)
        yes = MathTex(r"\lambda u.\;1", font_size=27, color=YES).move_to(RIGHT * 1.7 + DOWN * 0.65)
        no = MathTex(r"\lambda u.\;n\times\mathit{self}(\mathsf{pred}\;n)", font_size=25,
                     color=FUNC).move_to(RIGHT * 4.3 + DOWN * 0.65)
        if no.width > 3.5: no.scale_to_fit_width(3.5)
        arrows = VGroup(Arrow(condition.get_bottom(), yes.get_top(), buff=0.12, color=YES),
                        Arrow(condition.get_bottom(), no.get_top(), buff=0.12, color=FUNC))
        force = label(r"choose a branch closure, then apply it to unit", font_size=19,
                      color=HEAD).move_to(RIGHT * 3.1 + DOWN * 1.35)
        tab = grid_table([r"$n$", r"$Z\,F_{\mathrm{delay}}\,\underline{n}$", r"CBV $\beta$-steps"],
                         [[str(r['n']),str(r['value']),str(r['beta'])] for r in f['strict_fact']],
                         widths=[0.7,1.8,2.5], row_h=0.35, font_size=18,
                         mono_cols=(0,1,2)).move_to(RIGHT * 3.1 + DOWN * 2.5)
        note = label(r"closure return $\ne$ factorial evaluation; finite fuel is an observation",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover("A fixed-point equation and an evaluation strategy are different questions. <bookmark mark='a'/> With call-by-value, Y F unfolds its self-application before F can use it. This prevents even obtaining the function closure in the displayed example. <bookmark mark='b'/> Z delays that self-application beneath a lambda. Our first comparison tests Y F and Z F only to weak head: constructing Z F returns a closure. Computing a factorial result needs another condition: in a strict language, Church conditionals must delay their branches, or the recursive branch is evaluated even in the zero case. Z alone does not make every recursive program terminate. <bookmark mark='c'/> In the untyped calculus every term has a fixed point up to beta equality. Related computability ideas lead to Kleene's recursion theorem, developed in Part 25. A program that prints its own source is one application, with a specified encoding and output mechanism; it is not the whole theorem.") as vo:
            self.play(FadeIn(head), Write(y), run_time=0.8)
            vo.wait_until('a')
            self.play(FadeIn(observed[0]))
            vo.wait_until('b')
            self.play(Write(z), FadeIn(observed[1:]), FadeIn(delayed), FadeIn(condition), FadeIn(yes), FadeIn(no),
                      Create(arrows), FadeIn(force), FadeIn(tab))
            vo.wait_until('c')
            self.play(FadeIn(note))
        self.wait(0.3)
        self.clear_scene()
