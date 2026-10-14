from __future__ import annotations

import math

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
        head = label(r"$\sigma$-algebras: \ the sets that get a length", font_size=34).to_edge(UP, buff=0.3)
        dfn = VGroup(label(r"\textbf{RCA 1.3} \ a $\sigma$-algebra $\mathfrak M$ on $X$:", font_size=26),
                     Tex(r"contains $X$; \ ", r"closed under complements; \ ", r"closed under countable unions",
                         font_size=26, color=C.EPS)).arrange(DOWN, buff=0.1).next_to(head, DOWN, buff=0.2)
        names = [(r"open sets", C.OPEN_SET), (r"closed sets, \ countable unions of them ($\mathbb Q$)", C.CLOSED_SET),
                 (r"Borel sets: \ the smallest $\sigma$-algebra with the open sets", C.DELTA),
                 (r"Lebesgue measurable sets \ (Borel, plus subsets of null sets)", C.MEASURE),
                 (r"all subsets of $\R$", GREY_B)]
        # nested families drawn concentric (not stacked on one baseline); each label sits in the band between its box
        # and the next one inside.  Closed sets get a dashed edge: their orange is close to the measure's orange.
        boxes = VGroup()
        cy, ring = -1.0, 0.5
        for k in range(5):
            w, h = 3.6 + 2.0 * k, 1.0 + 2 * ring * k
            rr = RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=names[k][1], stroke_width=2.5,
                                  fill_color=names[k][1], fill_opacity=0.06).move_to([0, cy, 0])
            if k == 1:
                rr = VGroup(rr.copy().set_stroke(width=0),
                            DashedVMobject(rr.copy().set_fill(opacity=0), num_dashes=70))
            boxes.add(rr)
        labs = VGroup()
        for k in range(5):
            t = label(names[k][0], font_size=22, color=names[k][1])
            t.move_to(boxes[k].get_top() + DOWN * ring / 2)
            assert t.width < boxes[k].width - 0.5
            labs.add(t)
        vy = boxes[4].get_top()[1] - ring / 2  # the band between the Lebesgue box and "all subsets"
        vit = VGroup(Dot([4.75, vy, 0], radius=0.08, color=C.PATHOLOGY),
                     label(r"Vitali's set", font_size=22, color=C.PATHOLOGY).next_to([4.75, vy, 0], LEFT, buff=0.12))
        cy0 = boxes[1].get_bottom()[1] + ring / 2  # the band between the open and the closed box: closed, not open
        cant = VGroup(Dot([-1.0, cy0, 0], radius=0.06, color=C.CLOSED_SET),
                      label(r"Cantor set", font_size=22, color=C.CLOSED_SET).next_to([-1.0, cy0, 0], RIGHT, buff=0.1))
        assert boxes[4].get_bottom()[1] > -3.6 and boxes[4].get_top()[1] < dfn.get_bottom()[1] - 0.25
        with self.voiceover(
            "<bookmark mark='a'/> The sets that get a length form a sigma-algebra: a family that <bookmark mark='a1'/> "
            "contains the whole space and is <bookmark mark='a2'/> closed under complements and <bookmark mark='a3'/> "
            "countable unions, so countable intersections too. "
            "<bookmark mark='b'/> Start from the open sets. Their complements are the closed sets, and countable "
            "unions of closed sets include the rationals, a union of single points. <bookmark mark='c'/> Keep going "
            "and you reach the Borel sets, the smallest sigma-algebra containing the open sets. <bookmark mark='d'/> "
            "Lebesgue's sigma-algebra is a little larger still, and <bookmark mark='e'/> Vitali's set lies outside "
            "it, among the sets no length can handle."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(dfn), Create(boxes[0]), FadeIn(labs[0]))
            for i, mk in enumerate(("a1", "a2", "a3")):
                vo.wait_until(mk)
                self.play(Indicate(dfn[1][i], color=C.EPS, scale_factor=1.08))
            vo.wait_until("b")
            self.play(Indicate(VGroup(boxes[0], labs[0]), color=C.OPEN_SET, scale_factor=1.04))
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
            r"continuous (Part 2)", r"measurable (RCA 1.3)",
            [(r"$f^{-1}(\text{open})$ open", r"$f^{-1}(\text{open})$ measurable"),
             (r"limits can break it", r"$\sup, \lim$ keep it (1.14)"),
             (r"Dirichlet: \ no", r"Dirichlet: \ yes")],
            font_size=24, width=7.4).move_to([3.3, -0.5, 0])
        head = label(r"Measurable functions: \ the same template as continuity", font_size=34).to_edge(UP, buff=0.3)
        # Dirichlet's function as a double limit of continuous functions: cos(m! pi x)^(2n) -> 1 on {k/m!} as n -> oo
        xx = np.linspace(0, 1, 24001)
        # the approximants in APPROX (as in the opening), D itself in PATHOLOGY; the late stages take a high power so
        # the spikes stay thin, and the sequence stops at m = 4 (on this 6-unit plot m = 5 prints 121 spikes 7 px
        # apart, which reads as one solid slab, i.e. "D = 1")
        seq = [(2, 1), (2, 6), (2, 60), (3, 60), (3, 400), (4, 400)]

        def dl(m, n):
            return polyline(ax, xx, np.cos(math.factorial(m) * np.pi * xx) ** (2 * n), color=C.APPROX,
                            stroke_width=2.2 if n < 100 else 1.2)

        dls = [dl(m, n) for m, n in seq]
        dlab = [MathTex(rf"m = {m}, \ n = {n}", font_size=28, color=C.APPROX).next_to(ax, DOWN, buff=0.2)
                for m, n in seq]
        dform = MathTex(r"D(x) = \lim_{m \to \infty} \lim_{n \to \infty} \cos(m!\,\pi x)^{2n}", font_size=30,
                        color=C.PATHOLOGY).next_to(ax, UP, buff=0.1)
        for m, n in seq[2:]:
            k_ = np.arange(math.factorial(m) + 1) / math.factorial(m)
            assert np.allclose(np.cos(math.factorial(m) * np.pi * k_) ** (2 * n), 1)
        assert np.cos(math.factorial(2) * np.pi * 0.3) ** 120 < 1e-10  # off the grid the bumps have died
        # at the last stage the spikes are thin: below half height 1e-3 away from each k/24, 24 spikes 0.25 units apart
        assert np.cos(24 * np.pi * 1e-3) ** 800 < 0.5
        assert dform.get_top()[1] < head.get_bottom()[1] - 0.1
        with self.voiceover(
            "<bookmark mark='a'/> Which functions can we integrate? Part 2 characterized continuity by preimages: "
            "the preimage of every open set is open. <bookmark mark='b'/> A function is measurable if the preimage "
            "of every open set is measurable. Same template, weaker demand. <bookmark mark='c'/> And here is the "
            "point: limits are free. The supremum, infimum, upper limit and limit of measurable functions are "
            "measurable, <bookmark mark='d'/> so Dirichlet's function, a double limit of continuous ones, is "
            "measurable, though it is nowhere continuous: raise cosine of m factorial pi x to a high power and it "
            "becomes spikes at the fractions with denominator m factorial; then let m grow."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(fg))
            vo.wait_until("a")
            self.play(Create(Vbar), FadeIn(band), FadeIn(Vl))
            self.play(FadeIn(pre), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(card.titles), FadeIn(card.rows[0]), FadeIn(card.arrows[0]))
            vo.wait_until("c")
            self.play(FadeIn(card.rows[1]), FadeIn(card.arrows[1]))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(fg, Vbar, band, Vl, pre, pl)), FadeIn(dform), Create(dls[0]), FadeIn(dlab[0]))
            for k in range(1, len(seq)):
                self.play(ReplacementTransform(dls[k - 1], dls[k]), FadeTransform(dlab[k - 1], dlab[k]), run_time=1.1)
            self.play(FadeIn(card.rows[2]), FadeIn(card.arrows[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simple(self):
        d = load("simple")
        x, f, S, errs = d["x"], d["f"], d["S"], d["errs"]
        ax = plain_axes([0, 2, 0.5], [0, 6.5, 1], 7.4, 4.3).move_to([-2.6, -0.6, 0])
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
        head = VGroup(label(r"Simple functions climb to any measurable $f \ge 0$", font_size=34),
                      MathTex(r"s_n = \frac{j}{2^n} \text{ on } \Big\{\frac{j}{2^n} \le f < \frac{j + 1}{2^n}\Big\}, "
                              r"\quad s_n = n \text{ where } f \ge n", r"\quad \text{\small (RCA 1.17)}", font_size=30)
                      ).arrange(DOWN, buff=0.12)
        head[1][1].set_color(GREY_B)
        head.to_edge(UP, buff=0.3)
        side = VGroup(label(r"slice the \emph{range} into", font_size=26),
                      label(r"dyadic layers: \ each level set", font_size=26),
                      label(r"$\{j 2^{-n} \le f < (j + 1) 2^{-n}\}$", font_size=26),
                      label(r"is measurable", font_size=26),
                      label(r"$s_1 \le s_2 \le \dots \to f$", font_size=28, color=C.EPS),
                      label(r"the honest version of", font_size=24, color=GREY_A),
                      label(r"Lebesgue's coins", font_size=24, color=GREY_A),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.6, -0.5, 0])
        assert all(errs[k] <= 2.0 ** -(k + 1) for k in range(len(errs)))
        assert min(l_.get_bottom()[1] for l_ in labs) > -3.6 and ax.get_top()[1] < head.get_bottom()[1] - 0.15
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
