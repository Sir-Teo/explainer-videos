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
        tl = label("active-set count proxy: roughly proportional on this family; $m$ counts AST nodes", font_size=19,
                   color=GREY_B).next_to(t, DOWN, buff=0.15)
        pts = VGroup(
            label("word-parallel / Four-Russians methods improve logs under model and preprocessing assumptions",
                  font_size=20, color=GREY_A),
            label("Backurs--Indyk: specified pattern families have conditional hardness under SETH", font_size=20, color=NO),
            label("SETH: for each $\\varepsilon>0$, some $k$ forbids $k$-SAT in $2^{(1-\\varepsilon)N}\\operatorname{poly}(N)$",
                  font_size=20, color=GREY_B),
            label("Bringmann--Gr\\o nlund--Larsen (2017): bounded-depth homogeneous membership types classified", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover("For ordinary regular expressions, Thompson simulation gives an O m n upper bound, with pattern size m and text length n. <bookmark mark='a'/> This grid sums active-state counts after input steps on one pattern family: a work proxy, rather than a count of every internal operation. Here doubling either dimension roughly doubles the count; it is not a proof of a universal lower bound. <bookmark mark='b'/> Four-Russians and word-parallel algorithms improve logarithmic factors under their computational-model and preprocessing assumptions. The important question is whether a polynomial improvement is possible. <bookmark mark='c'/> Backurs and Indyk proved conditional hardness for specified pattern types and matching problems. In balanced hard instances, a truly subquadratic algorithm would refute the strong exponential time hypothesis. Easy pattern families still have much faster algorithms. <bookmark mark='d'/> SETH says that for every positive epsilon, some fixed clause width k rules out a k-SAT algorithm taking two to the one-minus-epsilon times the variable count, up to polynomial factors. It remains a conjecture. <bookmark mark='e'/> Bringmann, Gronlund and Larsen later completed a classification for bounded-depth homogeneous membership types, including an intermediate Word Break case. Distinguish that precise result from a blanket classification of all practical regex features.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(t), FadeIn(tl), run_time=0.6)
            vo.wait_until('a')
            for mk, p in zip('bcde', pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def parsing(self):
        fr = load("frontier")
        cy = fr["cyk"]
        head = label("Context-free recognition via Boolean matrix products", font_size=34).to_edge(UP, buff=0.3)
        xs = [math.log10(r["n"]) for r in cy]
        ys = [math.log10(1000 * r["s"]) for r in cy]
        xmin, xmax = math.floor(min(xs)*10)/10 - .1, math.ceil(max(xs)*10)/10 + .1
        ymin, ymax = math.floor(min(ys)), math.ceil(max(ys))
        ax = Axes(x_range=[0, xmax - xmin + .1, 1], y_range=[0, ymax - ymin + .15, 1],
                  x_length=4.0, y_length=2.1, tips=False,
                  axis_config={"color": GREY_C}).move_to(LEFT * 3.3 + UP * 1.25)
        pts_ = [ax.c2p(x - xmin, y - ymin) for x, y in zip(xs, ys)]
        line = VMobject(color=CTRL, stroke_width=4).set_points_as_corners(pts_)
        dots = VGroup(*[Dot(p, radius=.055, color=CTRL) for p in pts_])
        lab = VGroup(
            *[label(f"{10**x:g}", font_size=14, color=GREY_B).next_to(ax.c2p(x - xmin, 0), DOWN, buff=.1)
              for x in range(math.ceil(xmin), math.floor(xmax) + 1)],
            *[label(f"{10**y:g}", font_size=14, color=GREY_B).next_to(ax.c2p(0, y - ymin), LEFT, buff=.12)
              for y in range(ymin, ymax + 1)],
            label(r"tokens $n$ (log scale)", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=.4),
            label(r"milliseconds (log scale)", font_size=17, color=GREY_B).next_to(ax, UP, buff=.1))
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        slope = sum((x-mx)*(y-my) for x,y in zip(xs,ys)) / sum((x-mx)**2 for x in xs)
        al = VGroup(
            label(r"our CYK: measured on this host", font_size=20, color=CTRL),
            *[label(rf"$n={r['n']}$: {1000*r['s']:.3f} ms", font_size=18, color=GREY_A) for r in cy],
            label(rf"fitted slope: {slope:.2f}; finite sample, not a proof", font_size=17, color=GREY_B)
        ).arrange(DOWN, aligned_edge=LEFT, buff=.12).move_to(RIGHT * 2.5 + UP * 1.25)
        pts = VGroup(
            label("Valiant: fixed-grammar recognition via Boolean matrix multiplication; algebraic exponent bound",
                  font_size=20, color=GREY_A),
            label("$\\omega<2.372$: a loose upper bound, not the current record; asymptotic does not mean practical", font_size=20,
                  color=YES),
            label("Lee: $O(g n^{3-\\varepsilon})$ retrieval-efficient parser $\\Rightarrow$ subcubic Boolean matrix product",
                  font_size=20, color=GREY_A),
            label("Abboud--Backurs--Williams: conditional clique barriers; combinatorial and algebraic models differ", font_size=20, color=NO),
            label("restricted grammars can be fast; general practical performance and model assumptions matter", font_size=21,
                  color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        if pts.width > 13.2:
            pts.scale_to_fit_width(13.2)
        with self.voiceover("For a fixed grammar, standard CYK has a cubic worst-case upper bound in input length. <bookmark mark='a'/> These are timings from our implementation. The labeled log-log plot describes this finite measurement range; its fitted slope is an observation, not a complexity proof. <bookmark mark='b'/> Valiant related general context-free recognition to Boolean matrix multiplication. For a fixed grammar, the algebraic approach gives an upper bound governed by the matrix multiplication exponent, with the usual exponent convention. <bookmark mark='c'/> Known bounds put that exponent below two point three seven two; that is a convenient loose bound, not a claim to today's exact record. Asymptotic improvement also need not make an implementation practical. <bookmark mark='d'/> Lee's converse reduction includes grammar size and a retrieval-efficient parsing model. A suitable O g times n to the three-minus-epsilon parser would yield a subcubic Boolean matrix multiplication algorithm; it is not an unrestricted equivalence of every parsing task. <bookmark mark='e'/> Abboud, Backurs and Williams give further conditional evidence, even for constant-size grammars, by reductions from clique problems. Combinatorial is a model distinction here, not a synonym for simple. <bookmark mark='f'/> These results explain tradeoffs and conditional barriers. They do not prove that every grammar needs cubic time, or rule out useful algorithms for restricted grammars.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Create(ax), Create(line), FadeIn(dots), FadeIn(lab), FadeIn(al), run_time=0.6)
            vo.wait_until('a')
            for mk, p in zip('bcdef', pts):
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
            label("distinct residual languages form the minimal DFA; raw expressions need normalization / equivalence",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.35)
        rows = [[d["regex"], str(d["derivatives"]), str(d["minimal"])] for d in fr["derivatives"]]
        t = grid_table([r"expression", r"derivatives", r"minimal DFA"], rows, [4.6, 2.2, 2.4], row_h=0.38,
                       font_size=17, colors=[[CODE, CTRL, YES]] * len(rows), mono_cols=(0,)).next_to(defn, DOWN,
                                                                                                buff=0.3)
        pts = VGroup(
            label(r"Owens, \ Reppy and Turon \ (2009): \ derivatives make small, \ fast lexers; \ Might et al. \ "
                  r"(2011): \ \textit{parsing} with derivatives", font_size=19, color=GREY_A),
            label(".NET NonBacktracking: linear input time for supported fixed patterns; excludes backreferences and lookarounds", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover("A derivative asks what can follow a character already read. <bookmark mark='a'/> Brzozowski defined this operation in 1964. For the expression any string of a's and b's followed by a b b, deriving by a leaves two possibilities: that a belonged to the arbitrary prefix, or it began the final a b b. The displayed union captures both. <bookmark mark='b'/> A regular language has finitely many distinct left quotients. These residual languages form its minimal DFA. Raw expression syntax can produce redundant forms, so a derivative implementation needs normalization or equivalence reasoning; counting expressions is not automatically counting minimal states. Our examples agree with independently minimized machines. <bookmark mark='c'/> Derivative-based lexers and parsers renewed the idea's practical use. Microsoft's nonbacktracking engine uses this family of methods and guarantees linear processing in input length for a supported fixed pattern. It excludes features such as backreferences and lookarounds; the pattern and initialization costs still matter.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(defn[0]), FadeIn(defn[1]), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(defn[2]), FadeIn(t))
            vo.wait_until('c')
            self.play(FadeIn(pts))
        self.wait(0.3)
        self.clear_scene()
