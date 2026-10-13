from __future__ import annotations

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis5.common import interval_band, load, plain_axes, polyline, step_graph


class SigmaAlgebras(VoiceoverScene):
    def construct(self):
        self.card()
        self.sigma()
        self.functions()
        self.simple()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"$\sigma$-algebras and measurable functions",
                            r"Which sets get a length, \ and which functions can we integrate?", lit=(), part=5)
        with self.voiceover("Chapter three: the sets that get a length, and the functions we will integrate."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sigma(self):
        dfn = VGroup(label(r"\textbf{Rudin, RCA 1.2} \ a $\sigma$-algebra $\mathfrak M$ on $X$:", font_size=28),
                     label(r"contains $X$; \ closed under complements; \ closed under countable unions", font_size=28,
                           color=C.EPS)).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.25)
        names = [(r"open sets", C.OPEN_SET), (r"closed sets, \ countable unions of them ($\mathbb Q$)", C.CLOSED_SET),
                 (r"Borel sets: \ the smallest $\sigma$-algebra with the open sets", C.SEQ),
                 (r"Lebesgue measurable sets \ (Borel, plus subsets of null sets)", C.MEASURE),
                 (r"all subsets of $\R$", GREY_B)]
        boxes = VGroup()
        for k in range(5):
            w, h = 3.6 + 2.0 * k, 0.9 + 0.7 * k
            boxes.add(RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=names[k][1], stroke_width=2.5,
                                       fill_color=names[k][1], fill_opacity=0.06).move_to([0, -1.85 + h / 2, 0]))
        labs = VGroup()
        for k in range(5):
            t = label(names[k][0], font_size=22, color=names[k][1])
            t.move_to(boxes[k].get_top() + DOWN * 0.28)
            labs.add(t)
        vit = VGroup(Dot([5.45, 1.5, 0], radius=0.08, color=C.PATHOLOGY),
                     label(r"Vitali's set", font_size=22, color=C.PATHOLOGY).next_to([5.45, 1.5, 0], LEFT, buff=0.12))
        cant = VGroup(Dot([-1.0, -0.75, 0], radius=0.06, color=C.CLOSED_SET),
                      label(r"Cantor set", font_size=20, color=C.CLOSED_SET).next_to([-1.0, -0.75, 0], RIGHT, buff=0.1))
        with self.voiceover(
            "<bookmark mark='a'/> The sets that get a length form a sigma-algebra: a family that contains the whole "
            "space and is closed under complements and countable unions, so countable intersections too. "
            "<bookmark mark='b'/> Start from the open sets. Their complements are the closed sets, and countable "
            "unions of closed sets include the rationals, a union of single points. <bookmark mark='c'/> Keep going "
            "and you reach the Borel sets, the smallest sigma-algebra containing the open sets. <bookmark mark='d'/> "
            "Lebesgue's sigma-algebra is a little larger still, and <bookmark mark='e'/> Vitali's set lies outside "
            "it, among the sets no length can handle."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn))
            vo.wait_until("b")
            self.play(Create(boxes[0]), FadeIn(labs[0]))
            self.play(Create(boxes[1]), FadeIn(labs[1]), FadeIn(cant))
            vo.wait_until("c")
            self.play(Create(boxes[2]), FadeIn(labs[2]))
            vo.wait_until("d")
            self.play(Create(boxes[3]), FadeIn(labs[3]))
            vo.wait_until("e")
            self.play(Create(boxes[4]), FadeIn(labs[4]), FadeIn(vit, scale=1.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def functions(self):
        ax = plain_axes([0, 1, 0.25], [0, 1.1, 0.5], 6.0, 3.6).move_to([-3.4, -0.4, 0])
        x = np.linspace(0, 1, 1601)
        f = 0.55 + 0.35 * np.sin(9 * x) * np.cos(2 * x)
        fg = polyline(ax, x, f, color=C.FUNC, stroke_width=3)
        lo, hi = 0.62, 0.8
        Vbar = Line(ax.c2p(0, lo), ax.c2p(0, hi), color=C.OPEN_SET, stroke_width=10)
        band = Rectangle(width=6.0, height=ax.c2p(0, hi)[1] - ax.c2p(0, lo)[1], stroke_width=0, fill_color=C.OPEN_SET,
                         fill_opacity=0.12).move_to(ax.c2p(0.5, (lo + hi) / 2))
        on = (f > lo) & (f < hi)
        runs_, start = [], None
        for i in range(len(x) + 1):
            o = i < len(x) and on[i]
            if o and start is None:
                start = i
            elif not o and start is not None:
                runs_.append((x[start], x[i - 1]))
                start = None
        pre = interval_band(ax, runs_, ax.c2p(0, 0)[1] - 0.3, C.OPEN_SET, height=0.14)
        Vl = MathTex("V", font_size=30, color=C.OPEN_SET).next_to(Vbar, LEFT, buff=0.1)
        pl = MathTex(r"f^{-1}(V)", font_size=28, color=C.OPEN_SET).next_to(pre, DOWN, buff=0.12)
        card = dictionary_card(
            r"continuous (Part 2)", r"measurable (RCA 1.12)",
            [(r"$f^{-1}(V)$ open for open $V$", r"$f^{-1}(V)$ measurable for open $V$"),
             (r"limits can break it (Part 3)", r"$\sup, \inf, \limsup, \lim$ keep it (1.14)"),
             (r"Dirichlet's function: \ no", r"Dirichlet's function: \ yes")],
            font_size=24, width=7.4).move_to([3.3, -0.5, 0])
        head = label(r"Measurable functions: \ the same template as continuity", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Which functions can we integrate? Part 2 characterized continuity by preimages: "
            "the preimage of every open set is open. <bookmark mark='b'/> A function is measurable if the preimage "
            "of every open set is measurable. Same template, weaker demand. <bookmark mark='c'/> And here is the "
            "point: limits are free. The supremum, infimum, upper limit and limit of measurable functions are "
            "measurable, so Dirichlet's function, a double limit of continuous ones, is measurable, though it is "
            "nowhere continuous."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(fg))
            vo.wait_until("a")
            self.play(Create(Vbar), FadeIn(band), FadeIn(Vl))
            self.play(FadeIn(pre), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(card.titles), FadeIn(card.rows[0]), FadeIn(card.arrows[0]))
            vo.wait_until("c")
            self.play(FadeIn(card.rows[1]), FadeIn(card.arrows[1]))
            self.play(FadeIn(card.rows[2]), FadeIn(card.arrows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simple(self):
        d = load("simple")
        x, f, S, errs = d["x"], d["f"], d["S"], d["errs"]
        ax = plain_axes([0, 2, 0.5], [0, 6.5, 1], 7.4, 4.6).move_to([-2.6, -0.75, 0])
        fg = polyline(ax, x, f, color=WHITE, stroke_width=3)
        cols = [interpolate_color(ManimColor(C.SEQ), ManimColor(C.MEASURE), k / 7) for k in range(8)]

        def sgraph(k):
            s = S[k]
            # draw the simple function as many short horizontal pieces (it is constant on each level set)
            idx = np.nonzero(np.diff(s) != 0)[0]
            cuts = np.concatenate([[0], idx + 1, [len(x)]])
            return VGroup(*[Line(ax.c2p(x[a], s[a]), ax.c2p(x[b - 1], s[a]), color=cols[k], stroke_width=3)
                            for a, b in zip(cuts[:-1], cuts[1:])])

        shown = [0, 1, 2, 3, 5, 7]
        sg = [sgraph(k) for k in shown]
        labs = [MathTex(rf"s_{{{k + 1}}}: \ \text{{levels }} j/2^{{{k + 1}}}, \quad \sup_{{f < {k + 1}}} |s_{{{k + 1}}} - f| "
                        rf"= {errs[k]:.4f} \le 2^{{-{k + 1}}}", font_size=26, color=cols[k]).next_to(ax, DOWN, buff=0.15)
                for k in shown]
        head = VGroup(label(r"\textbf{Rudin, RCA 1.17} \ simple functions climb to any measurable $f \ge 0$",
                            font_size=30),
                      MathTex(r"s_n = \frac{j}{2^n} \text{ on } \Big\{\frac{j}{2^n} \le f < \frac{j + 1}{2^n}\Big\}, "
                              r"\quad s_n = n \text{ where } f \ge n", font_size=30)).arrange(DOWN, buff=0.12)
        head.to_edge(UP, buff=0.25)
        side = VGroup(label(r"slice the \emph{range} into", font_size=26),
                      label(r"dyadic layers: \ each level set", font_size=26),
                      label(r"$\{j 2^{-n} \le f < (j + 1) 2^{-n}\}$", font_size=26),
                      label(r"is measurable", font_size=26),
                      label(r"$s_1 \le s_2 \le \dots \to f$", font_size=28, color=C.EPS),
                      label(r"the honest version of", font_size=24, color=GREY_A),
                      label(r"Lebesgue's coins", font_size=24, color=GREY_A),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -0.5, 0])
        assert all(errs[k] <= 2.0 ** -(k + 1) for k in range(len(errs)))
        with self.voiceover(
            "<bookmark mark='a'/> Every non-negative measurable function is the limit of an increasing sequence of "
            "simple functions, functions with finitely many values. <bookmark mark='b'/> The recipe slices the range: "
            "at stage n, round f down to the nearest multiple of one over two to the n. Each layer's preimage is a "
            "measurable set, so each stage is a finite combination of indicator functions. <bookmark mark='c'/> Each "
            "stage refines the last, so the sequence increases, and where f is below n, the error is at most one over "
            "two to the n. This is the honest version of Lebesgue's coins."
        ) as vo:
            self.play(FadeIn(head[0]), Create(ax), Create(fg))
            vo.wait_until("a")
            self.play(FadeIn(head[1]))
            vo.wait_until("b")
            self.play(Create(sg[0]), FadeIn(labs[0]), FadeIn(side[:4]))
            cur, cl = sg[0], labs[0]
            for k in range(1, 3):
                self.play(cur.animate.set_stroke(opacity=0.25), Create(sg[k]), FadeTransform(cl, labs[k]), run_time=1.2)
                cur, cl = sg[k], labs[k]
            vo.wait_until("c")
            for k in range(3, len(shown)):
                self.play(cur.animate.set_stroke(opacity=0.25), Create(sg[k]), FadeTransform(cl, labs[k]), run_time=1.0)
                cur, cl = sg[k], labs[k]
            self.play(FadeIn(side[4:]))
        self.wait(0.4)
        self.clear_scene()
