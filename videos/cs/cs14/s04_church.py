from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs14.common import (CODE, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, bar_chart, church_boxes,
                                   grid_table, load, mono)


class Church(VoiceoverScene):
    def construct(self):
        self.card()
        self.booleans()
        self.numerals()
        self.arithmetic()
        self.pairs_pred()
        self.lists()

    def card(self):
        card = chapter_card(3, r"Programming with nothing", r"Can functions alone be data?", lit=(1936,), part=PART)
        with self.voiceover("Chapter three. Programming with nothing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def booleans(self):
        c = load("church")
        head = label(r"Booleans are choices", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"\mathsf{true} = \lambda t\,f.\; t \qquad \mathsf{false} = \lambda t\,f.\; f", font_size=36),
            MathTex(r"\mathsf{if}\; b\; x\; y \;=\; b\; x\; y", font_size=36),
            MathTex(r"\mathsf{and} = \lambda p\,q.\; p\;q\;p \qquad \mathsf{or} = \lambda p\,q.\; p\;p\;q", font_size=36),
        ).arrange(DOWN, buff=0.3).next_to(head, DOWN, buff=0.45)
        rows = []
        for a in ("true", "false"):
            for b in ("true", "false"):
                r = {x["op"]: x for x in c["bools"] if x["a"] == a and x["b"] == b}
                rows.append([a, b, r["and"]["result"], r["or"]["result"], str(r["and"]["steps"])])
        tab = grid_table([r"$p$", r"$q$", r"$\mathsf{and}\;p\;q$", r"$\mathsf{or}\;p\;q$", r"steps"], rows,
                         widths=[1.4, 1.4, 2.0, 2.0, 1.2], row_h=0.42, font_size=20, mono_cols=(0, 1, 2, 3)).next_to(
            defs, DOWN, buff=0.45)
        cap = label(r"computed by our reducer: \ every answer is \textsf{true} or \textsf{false} itself",
                    font_size=19, color=GREY_B).next_to(tab, DOWN, buff=0.15)
        with self.voiceover("If the language has nothing but functions, then data must be functions too. Church showed how. <bookmark mark='a'/> A boolean is a choice between two things. True takes two arguments and returns the first; false returns the second. <bookmark mark='b'/> Then if b then x else y needs no special rule at all: it is just b applied to x and y. <bookmark mark='c'/> And p and q is p applied to q and p: if p is true it chooses q, and if p is false it chooses p, which is false. Or is the mirror image. <bookmark mark='d'/> Our reducer confirms all four rows of each table, in four steps each, and every answer comes out as the function true or the function false itself.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defs[0]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(defs[1]))
            vo.wait_until('c')
            self.play(FadeIn(defs[2]))
            vo.wait_until('d')
            self.play(FadeIn(tab), FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def numerals(self):
        head = label(r"Numbers are repetitions", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for n in range(4):
            t = MathTex(rf"\underline{{{n}}} = \lambda f\,x.\; " + (r"f\,(" * n) + "x" + (")" * n), font_size=30)
            b = church_boxes(n).scale(0.8)
            r = VGroup(t, b).arrange(RIGHT, buff=0.8)
            rows.add(r)
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        for r in rows:
            r[1].set_x(3.2, direction=LEFT)
        succ = MathTex(r"\mathsf{succ} = \lambda n\,f\,x.\; f\,(n\,f\,x)", font_size=34, color=YES).to_edge(DOWN,
                                                                                                         buff=0.6)
        sl = label(r"one more $f$ on the outside", font_size=21, color=YES).next_to(succ, RIGHT, buff=0.4)
        with self.voiceover(
            "Numbers are repetitions. <bookmark mark='a'/> The numeral n is the function that takes f and x and "
            "applies f to x, n times. Zero applies it no times and returns x. One applies f once. Two wraps x in two "
            "applications of f, and so on: picture each f as a box around the one inside. <bookmark mark='b'/> "
            "Successor takes a numeral n, lets it apply f n times, and then applies f once more, on the outside."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            for r in rows:
                self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(succ), FadeIn(sl))
        self.wait(0.3)
        self.clear_scene()

    def arithmetic(self):
        c = load("church")
        head = label(r"Arithmetic from repetition", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            VGroup(MathTex(r"\mathit{plus}\;m\;n = \lambda f\,x.\; m\,f\,(n\,f\,x)", font_size=32),
                   label(r"$m$ more applications on top of $n$", font_size=20, color=GREY_A)),
            VGroup(MathTex(r"\mathit{times}\;m\;n = \lambda f.\; m\,(n\,f)", font_size=32),
                   label(r"repeat ``apply $f$ $n$ times'', \ $m$ times", font_size=20, color=GREY_A)),
            VGroup(MathTex(r"\mathit{pow}\;m\;n = n\;m", font_size=32),
                   label(r"apply ``times $m$'' $n$ times: \ $m^n$", font_size=20, color=GREY_A)),
        )
        for d in defs:
            d.arrange(RIGHT, buff=0.5)
        defs.arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(head, DOWN, buff=0.5)
        rows = [[o["op"], f"{o['args'][0]}, {o['args'][1]}", str(o["value"]), str(o["steps"])] for o in c["ops"]]
        tab = grid_table([r"operation", r"arguments", r"normal form", r"$\beta$-steps"], rows,
                         widths=[2.2, 2.0, 2.0, 1.8], row_h=0.45, font_size=21, mono_cols=(0, 1, 2)).next_to(
            defs, DOWN, buff=0.6)
        with self.voiceover("With repetition, arithmetic falls out. <bookmark mark='a'/> Plus m n applies f m more times on top of n applications. <bookmark mark='b'/> Times m n takes the function apply f n times, and repeats that m times. <bookmark mark='c'/> And power is the strangest and shortest of all: n applied to m. Apply the function times m, n times over, starting from one. <bookmark mark='d'/> Our reducer computes three plus four, three times four and two to the third, in six, nine and sixteen beta steps, and each normal form is exactly the expected numeral.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            for mk, d in zip('abc', defs):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(d, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            vo.wait_until('d')
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    def pairs_pred(self):
        c = load("church")
        head = label(r"Pairs, \ and going backwards", font_size=36).to_edge(UP, buff=0.3)
        pair = MathTex(r"\mathsf{pair}\;a\;b = \lambda s.\; s\;a\;b \qquad \mathsf{fst}\;p = p\;\mathsf{true} \qquad "
                       r"\mathsf{snd}\;p = p\;\mathsf{false}", font_size=30).next_to(head, DOWN, buff=0.4)
        trick = VGroup(
            label(r"subtracting one is hard: \ a numeral can only apply $f$, \ never undo it", font_size=22,
                  color=GREY_A),
            label(r"Kleene's trick \ (1932): \ step pairs \ $(0,0) \to (0,1) \to (1,2) \to \cdots \to (n{-}1, n)$, "
                  r"\ keep the first", font_size=22, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(pair, DOWN, buff=0.4)
        pr = c["pred"]
        ch = bar_chart([r["steps"] for r in pr], [str(r["n"]) for r in pr], [FUNC] * len(pr), height=2.4, bar_w=0.5,
                       gap=0.25, fmt_=lambda v: f"{v:.0f}", font_size=16).next_to(trick, DOWN, buff=0.5)
        cl = label(r"$\beta$-steps for $\mathsf{pred}\;\underline{n}$: \ linear in $n$", font_size=19,
                   color=GREY_B).next_to(ch, DOWN, buff=0.15)
        with self.voiceover("Pairs encode two values behind a selector. <bookmark mark='a'/> First applies the pair to true; second applies it to false. These are functions selecting one component. <bookmark mark='b'/> For predecessor, counting forward is easier than undoing a function application. Kleene's construction carries two consecutive counts. <bookmark mark='c'/> Start at zero, zero, and update a, b to b, successor b, once per input iteration. For a positive numeral n the first component ends at n minus one. At zero it stays zero, so predecessor saturates rather than producing a negative numeral. <bookmark mark='d'/> Our full normal-order reducer uses nine beta steps for zero, then ten n plus six for the displayed positive numerals. Those counts belong to this encoding and reduction strategy. They count beta contractions, not the cost of copying syntax trees, memory allocation or machine time.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(pair), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(trick[0]))
            vo.wait_until('c')
            self.play(FadeIn(trick[1]))
            vo.wait_until('d')
            self.play(FadeIn(ch), FadeIn(cl))
        self.wait(0.3)
        self.clear_scene()

    def lists(self):
        head = label(r"Lists are folds", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"\mathsf{nil} = \lambda c\,n.\; n \qquad \mathsf{cons}\;h\;t = \lambda c\,n.\; c\;h\;(t\;c\;n)",
                    font_size=32),
            MathTex(r"[1, 2, 3] \;=\; \lambda c\,n.\; c\;1\;(c\;2\;(c\;3\;n))", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(head, DOWN, buff=0.5)
        uses = VGroup(
            label(r"a list \textit{is} its own loop: \ give it $c = +$ and $n = 0$, \ and it sums itself", font_size=22,
                  color=GREY_A),
            label(r"the same idea as the numerals: \ a structure is what you can do with it", font_size=22,
                  color=GREY_A),
            label(r"so booleans, \ numbers, \ pairs, \ lists: \ all from $\lambda$, \ variables and application",
                  font_size=24, color=HEAD),
        ).arrange(DOWN, buff=0.25).next_to(defs, DOWN, buff=0.55)
        with self.voiceover("Lists follow the same pattern. <bookmark mark='a'/> A list is a function of two arguments, c and n. The empty list returns n. A list with head h and tail t applies c to h and to whatever the tail produces. So the list one, two, three is c one, c two, c three, n. <bookmark mark='b'/> A list is its own loop: hand it addition for c and zero for n, and it sums itself. The same idea made the numerals work: a data structure is defined by what you can do with it. <bookmark mark='c'/> Booleans, numbers, pairs and lists, built from lambda, variables and application, and nothing else.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defs), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(uses[:2]))
            vo.wait_until('c')
            self.play(FadeIn(uses[2]))
        self.wait(0.3)
        self.clear_scene()
