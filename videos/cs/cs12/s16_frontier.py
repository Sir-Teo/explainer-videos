from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs12.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.regex()
        self.parsing()
        self.derivatives()

    def card(self):
        card = chapter_card(15, r"Frontier: \ how fast can we parse?", r"Is $O(mn)$ the best possible?",
                            lit=(1975, 2016), extra=((1975, r"Valiant: \ parsing as matrix product"),
                                                     (2016, r"Backurs and Indyk")), part=PART)
        with self.voiceover("Chapter fifteen. The frontier."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def regex(self):
        fr = load("frontier")
        head = label(r"Is $m \times n$ the best possible for regular expressions?", font_size=32).to_edge(UP, buff=0.3)
        g = fr["thompson"]
        ms = sorted({r["m"] for r in g})
        ns = sorted({r["n"] for r in g})
        body = [[str(m)] + [f"{next(r['work'] for r in g if r['m'] == m and r['n'] == n):,}" for n in ns] for m in ms]
        t = grid_table([r"pattern size $m$"] + [rf"$n = {n:,}$" for n in ns], body, [2.6, 2.0, 2.0, 2.0], row_h=0.45,
                       font_size=19, colors=[[HEAD, GREY_A, GREY_A, GREY_A]] * len(body), mono_cols=()).next_to(
            head, DOWN, buff=0.35)
        tl = label(r"our NFA simulation's work: \ double either, \ double the work", font_size=19,
                   color=GREY_B).next_to(t, DOWN, buff=0.15)
        pts = VGroup(
            label(r"Myers \ (1992): \ $O(mn / \log n)$; \ since then, \ only small logarithmic factors shaved off",
                  font_size=20, color=GREY_A),
            label(r"Backurs and Indyk \ (2016): \ for many pattern types, \ an $O((mn)^{1-\varepsilon})$ algorithm "
                  r"would refute SETH", font_size=20, color=NO),
            label(r"SETH: \ satisfiability needs about $2^n$ time \ (Part 26) \ --- \ unproved, \ widely believed",
                  font_size=20, color=GREY_B),
            label(r"open: \ exactly which patterns can be matched in near-linear time", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Thompson's method takes time proportional to the pattern's size times the text's length. Can anyone "
            "do fundamentally better? <bookmark mark='a'/> Our simulation behaves exactly that way: double the "
            "pattern or double the text, and the work doubles. <bookmark mark='b'/> In 1992 Gene Myers shaved off "
            "a logarithmic factor, and later work has shaved off only a little more. <bookmark mark='c'/> In 2016 "
            "Arturs Backurs "
            "and Piotr Indyk explained why. For many kinds of pattern, an algorithm substantially faster than m "
            "times n would refute the strong exponential time hypothesis: <bookmark mark='d'/> the conjecture that "
            "Boolean satisfiability cannot be solved much faster than trying all two to the n assignments, which "
            "we meet in Part 26. <bookmark mark='e'/> Their work classifies many patterns as easy or hard, but not "
            "all, and finishing the classification is open."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t), FadeIn(tl))
            for mk, p in zip("bcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def parsing(self):
        fr = load("frontier")
        cy = fr["cyk"]
        head = label(r"Parsing is matrix multiplication", font_size=34).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1.0, 2.3, 0.3], y_range=[0, 3.0, 1], x_length=4.2, y_length=2.3, tips=False,
                  axis_config={"color": GREY_C}).next_to(head, DOWN, buff=0.5).shift(LEFT * 2.5)
        pts_ = [ax.c2p(math.log10(r["n"]), math.log10(r["s"]) + 4.2) for r in cy]
        line = VMobject(color=CTRL, stroke_width=4).set_points_as_corners(pts_)
        dots = VGroup(*[Dot(p, radius=0.05, color=CTRL) for p in pts_])
        lab = VGroup(*[label(rf"$n = {r['n']}$: \ {1000 * r['s']:.1f} ms", font_size=16, color=GREY_A).next_to(
            p, RIGHT, buff=0.15) for r, p in zip(cy, pts_)])
        al = label(r"our CYK, \ log--log: \ slope close to 3", font_size=18, color=CTRL).next_to(ax, RIGHT,
                                                                                                  buff=2.2)
        pts = VGroup(
            label(r"Valiant \ (1975): \ CYK's table can be filled with Boolean matrix products: \ time $O(n^\omega)$",
                  font_size=20, color=GREY_A),
            label(r"$\omega < 2.372$ \ today: \ asymptotically faster than $n^3$ \ --- \ in theory", font_size=20,
                  color=YES),
            label(r"Lee \ (2002): \ any fast parser gives fast matrix multiplication: \ the two problems are tied",
                  font_size=20, color=GREY_A),
            label(r"Abboud, \ Backurs and Williams \ (2015): \ no \textit{combinatorial} parser beats $n^{3}$ by a "
                  r"power, \ unless $k$-clique is easier than believed", font_size=20, color=NO),
            label(r"open: \ a practical parser, \ for every grammar, \ that is truly subcubic", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        if pts.width > 13.2:
            pts.scale_to_fit_width(13.2)
        with self.voiceover(
            "For context-free grammars the general methods are cubic. <bookmark mark='a'/> Our CYK confirms it: "
            "on a log-log plot its times climb with a slope close to three. <bookmark mark='b'/> In 1975 Leslie "
            "Valiant showed that the CYK table can be filled using Boolean matrix multiplication, so parsing is no "
            "harder than multiplying matrices, <bookmark mark='c'/> which can be done, in theory, in less than n to "
            "the two point three seven two. <bookmark mark='d'/> In 2002 Lillian Lee proved the converse: a "
            "substantially faster parser would give a faster way to multiply matrices. <bookmark mark='e'/> And in "
            "2015 Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams showed that no simple, "
            "combinatorial parser can beat n cubed by a polynomial factor unless a long-standing conjecture about "
            "finding cliques in graphs is false. <bookmark mark='f'/> A practical general parser that is truly "
            "faster than cubic remains out of reach."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), Create(line), FadeIn(dots), FadeIn(lab), FadeIn(al))
            for mk, p in zip("bcdef", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def derivatives(self):
        fr = load("frontier")
        head = label(r"Derivatives: \ an old idea, \ newly at work", font_size=34).to_edge(UP, buff=0.3)
        defn = VGroup(
            label(r"Brzozowski \ (1964): \ the derivative $\partial_c\, r$ \ is the expression for ``what is left "
                  r"after reading $c$''", font_size=20, color=GREY_A),
            MathTex(r"\partial_a\,\big((a|b)^*abb\big) = \big((a|b)^*a \mid \varepsilon\big)\,bb", font_size=32,
                    color=HEAD),
            label(r"the distinct derivatives of $r$ are the states of a DFA for it, \ built with no NFA at all",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.35)
        rows = [[d["regex"], str(d["derivatives"]), str(d["minimal"])] for d in fr["derivatives"]]
        t = grid_table([r"expression", r"derivatives", r"minimal DFA"], rows, [4.6, 2.2, 2.4], row_h=0.38,
                       font_size=17, colors=[[CODE, CTRL, YES]] * len(rows), mono_cols=(0,)).next_to(defn, DOWN,
                                                                                                buff=0.3)
        pts = VGroup(
            label(r"Owens, \ Reppy and Turon \ (2009): \ derivatives make small, \ fast lexers; \ Might et al. \ "
                  r"(2011): \ \textit{parsing} with derivatives", font_size=19, color=GREY_A),
            label(r".NET's non-backtracking regex engine \ (2022) \ is built on derivatives, \ with linear-time "
                  r"guarantees", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "And an old idea has come back. <bookmark mark='a'/> In 1964 Janusz Brzozowski defined the derivative "
            "of a regular expression with respect to a character: another regular expression, for whatever must "
            "follow that character. Derive a b star a b b by a, and you get, roughly, a b star a, or nothing, then "
            "b b. <bookmark mark='b'/> Keep deriving, and only finitely many different expressions ever appear. "
            "They are the states of a deterministic automaton, built directly, with no NFA at all. On our "
            "examples, the derivatives give exactly the minimal machine every time. <bookmark mark='c'/> Derivatives "
            "came back into use around 2009 for lexer generators, were extended to whole grammars in 2011, and "
            "now drive the linear-time regular expression engine in Microsoft's .NET. A sixty-year-old idea, at the "
            "frontier of practice."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defn[0]), FadeIn(defn[1]))
            vo.wait_until("b")
            self.play(FadeIn(defn[2]), FadeIn(t))
            vo.wait_until("c")
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
