from __future__ import annotations

import numpy as np

from videos.stats.stats31.common import *  # noqa: F403
from videos.stats.stats31.s06_factor import FNAMES, SHORT

GC = [S.CTRL, S.TREAT, S.ALT, S.PRIOR]  # verbal, speed, spatial, memory


def layout(group, center, r=2.55):
    """Nodes on a circle, ordered by factor group so that each group occupies an arc."""
    order = sorted(range(len(group)), key=lambda i: (group[i], i))
    pos = {}
    for k, i in enumerate(order):
        t = np.pi / 2 - 2 * np.pi * k / len(order)
        pos[i] = np.array(center) + r * np.array([np.cos(t), np.sin(t), 0])
    return pos


def graph(pc, pos, color=GREY_B, tol=1e-6):
    g = VGroup()
    p = len(pc)
    for i in range(p):
        for j in range(i + 1, p):
            v = abs(pc[i, j])
            if v > tol:
                g.add(Line(pos[i], pos[j], stroke_width=0.8 + 9 * v, color=color, stroke_opacity=min(1.0, 0.35 + 1.5 * v)))
    return g


class Graphs(VoiceoverScene):
    def construct(self):
        self.card()
        self.partial()
        self.theorem()
        self.full()
        self.objective()
        self.neighbourhood()
        self.path()
        self.reading()

    def card(self):
        card = chapter_card(9, r"Graphical models", r"Who is directly connected to whom", lit=(2008,), part=PART)
        with self.voiceover("Chapter nine. Graphical models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def partial(self):
        rows = [
            cmath(r"\mathrm{corr}(x_i, x_j)", r":", r"\text{direct and indirect association together}", font_size=30),
            cmath(r"\rho_{ij \cdot \text{rest}}", r":", r"\text{the correlation left after regressing both on the rest}", font_size=28),
            cmath(r"\Theta", r"=", r"\Sigma^{-1}, \ \ \rho_{ij \cdot \text{rest}} = -\theta_{ij} / \sqrt{\theta_{ii} \theta_{jj}}", font_size=30),
            cmath(r"\text{the 24 tests}", r":", r"\text{mean correlation } 0.30; \ 60\% \text{ of absolute partials below } 0.1", font_size=28),
        ]
        rows[2][-1].set_color(MAPC)
        whys = [why(r"everything correlates"), why(r"partial correlation, \ Part 12"), why(r"read off the precision matrix"),
                why(r"most links are indirect")]
        with self.voiceover(
            "<bookmark mark='a'/> In the twenty-four tests every pair is correlated, but a correlation mixes direct "
            "and indirect association. <bookmark mark='b'/> Partial correlation measures residual linear association "
            "after adjustment: regress both variables on all the others and correlate what is left. <bookmark "
            "mark='c'/> All of them at once come from the inverse covariance, the precision matrix: minus each entry "
            "over the root of the two diagonal entries. <bookmark mark='d'/> For the tests the average correlation is"
            " point three, but sixty percent of their absolute values are below point one. Word classification and "
            "word meaning correlate point five three; given the other twenty-two tests, their partial correlation is "
            "zero to two decimals."
        ) as vo:
            intro=label('Partial correlation measures linear association after adjustment',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"\theta_{ij} = 0", r"\iff", r"x_i \perp\!\!\!\perp x_j \mid \text{the rest} \ \ \text{(Gaussian)}", font_size=30),
            cmath(r"\text{graph}", r":", r"\text{an edge wherever } \theta_{ij} \ne 0", font_size=30),
            cmath(r"\text{separation}", r"\Rightarrow", r"\text{conditional independence}", font_size=30),
            cmath(r"\text{covariance selection}", r":", r"\text{choose the zeros, \ fit the rest}", font_size=28),
        ]
        rows[0][-1].set_color(MAPC)
        whys = [why(r"zeros of $\Sigma^{-1}$"), why(r"a Gaussian graphical model"), why(r"the global Markov property"),
                why(r"Dempster (1972)")]
        with self.voiceover(
            "<bookmark mark='a'/> For normal data, a zero in the precision matrix means more than a zero partial "
            "correlation: it means the two variables are independent given all the others. <bookmark mark='b'/> Draw an edge "
            "between every pair whose entry is non-zero and you have a Gaussian graphical model. <bookmark mark='c'/> The "
            "graph can be read: if every path from one set of variables to another passes through a third set, the first two "
            "are independent given the third. <bookmark mark='d'/> Arthur Dempster in 1972 called the problem of choosing "
            "the zeros covariance selection."
        ) as vo:
            intro=label('Gaussian precision zeros encode conditional independence',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nodes(self, pos, group, names=False):
        g = VGroup(*[Dot(pos[i], radius=0.11, color=GC[group[i]]) for i in range(len(group))])
        if not names:
            return g, VGroup()
        c = np.mean([pos[i] for i in pos], axis=0)
        lab = VGroup()
        for i in range(len(group)):
            dvec = normalize(pos[i] - c)
            lab.add(label(rf"{i + 1}", font_size=16, color=GC[group[i]]).move_to(pos[i] + dvec * 0.3))
        return g, lab

    def full(self):
        d = load("glasso")
        fa = load("fa")
        group = list(np.argmax(np.abs(np.asarray(fa["loadings"])), 1))
        pos = layout(group, [-2.3, 0.0, 0])
        pf = np.asarray(d["pcor_full"])
        nd, lab = self.nodes(pos, group, names=True)
        e = graph(pf, pos)
        keyrows = VGroup(*[label(FNAMES[j], font_size=22, color=GC[j]) for j in range(4)]).arrange(RIGHT, buff=0.35)
        rows = fit_rows(VGroup(
            keyrows,
            label(r"colour: \ the test's varimax factor", font_size=22, color=GREY_A),
            label(r"every partial correlation: \ 276 edges, \ width $\propto |\rho|$", font_size=22),
            label(r"a hairball: \ estimated partials are never exactly zero", font_size=22, color=RES),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The twenty-four tests as nodes, coloured by the factor each loads on most. "
            "<bookmark mark='b'/> Draw every estimated partial correlation as an edge, thicker for larger values: two"
            " hundred and seventy-six edges. <bookmark mark='c'/> A hairball. Unpenalized estimated partial "
            "correlations are generally not exactly zero, so the plain inverse covariance gives a complete graph that"
            " says nothing."
        ) as vo:
            self.add(harman_tag())
            vo.wait_until("a")
            self.play(FadeIn(nd), FadeIn(lab), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Create(e), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def objective(self):
        rows = [
            cmath(r"\max_{\Theta \succ 0}", r"", r"\log\det\Theta - \mathrm{tr}(S\Theta) - \lambda \textstyle\sum_{i \ne j} |\theta_{ij}|", font_size=30),
            cmath(r"\text{without } \lambda", r":", r"\hat\Theta = S^{-1}", font_size=30),
            cmath(r"\text{each column}", r":", r"\text{a lasso regression on the others}", font_size=30),
            cmath(r"\lambda", r"\uparrow", r"\text{typically sparser; edges need not be nested}", font_size=32),
        ]
        rows[0][-1].set_color(MAPC)
        whys = [why(r"the Gaussian log likelihood, \ penalized"), why(r"Part 22's MLE"),
                why(r"Friedman, \ Hastie \& Tibshirani (2008)"), why(r"sparsity: \ Part 32")]
        with self.voiceover(
            "<bookmark mark='a'/> The graphical lasso adds a penalty on the absolute values of the off-diagonal "
            "entries to the normal log likelihood. <bookmark mark='b'/> Without the penalty the maximizer is S "
            "inverse, the hairball. <bookmark mark='c'/> Jerome Friedman, Trevor Hastie and Robert Tibshirani showed "
            "in 2008 that it can be solved one column at a time, each column a lasso regression of one variable on "
            "the others, by coordinate descent. <bookmark mark='d'/> The absolute-value penalty sets entries exactly "
            "to zero, and larger lambda generally makes a sparser graph, although individual edges need not form a "
            "nested path. Why the absolute value produces exact zeros is the subject of Part 32."
        ) as vo:
            intro=label('Graphical lasso penalizes off-diagonal precision entries',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def path(self):
        d = load("glasso")
        fa = load("fa")
        group = list(np.argmax(np.abs(np.asarray(fa["loadings"])), 1))
        pos = layout(group, [-2.3, 0.0, 0])
        nd, lab = self.nodes(pos, group, names=True)
        gs = {lam: graph(np.asarray(d["path"][lam]["pcor"]), pos, color=MAPC) for lam in ("0.5", "0.4", "0.3")}
        cnt = {lam: d["path"][lam]["edges"] for lam in gs}
        tag = label(rf"$\lambda = 0.5$: \ {cnt['0.5']} edges", font_size=26, color=MAPC).move_to([4.6, 2.4, 0])
        rows = fit_rows(VGroup(
            label(r"edges appear within factor groups first", font_size=22),
            label(r"verbal tests 5--9 form a tight clique", font_size=22, color=GC[0]),
            label(r"reasoning tests (20--24) bridge the groups", font_size=22, color=GREY_A),
        ), 4.2, 0.42, [4.6, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The graphical lasso with a large penalty, lambda point five: sixteen edges. "
            "<bookmark mark='b'/> Lower it to point four: forty-five. <bookmark mark='c'/> And point three: "
            "ninety-seven. <bookmark mark='d'/> The strongest direct links appear within the factor groups, and the "
            "verbal tests form a tight clique. <bookmark mark='e'/> Edges between groups run mostly through the "
            "reasoning tests, like deduction and series completion, which draw on several abilities at once. The "
            "factor model and the graph are two descriptions of the same correlations: one by latent shared "
            "variation, one by conditional links."
        ) as vo:
            self.add(harman_tag())
            self.play(FadeIn(nd), FadeIn(lab))
            vo.wait_until("a")
            self.play(Create(gs["0.5"]), FadeIn(tag))
            vo.wait_until("b")
            self.play(ReplacementTransform(gs["0.5"], gs["0.4"]),
                      Transform(tag, label(rf"$\lambda = 0.4$: \ {cnt['0.4']} edges", font_size=26, color=MAPC).move_to(tag)))
            vo.wait_until("c")
            self.play(ReplacementTransform(gs["0.4"], gs["0.3"]),
                      Transform(tag, label(rf"$\lambda = 0.3$: \ {cnt['0.3']} edges", font_size=26, color=MAPC).move_to(tag)))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def reading(self):
        rows = fit_rows(VGroup(
            label(r"an absent edge: \ conditionally independent, \ if the data are normal", font_size=24),
            label(r"an edge is not a cause: \ the graph is undirected", font_size=24, color=RES),
            label(r"$\lambda$ trades edges for stability: \ choose it by CV, \ BIC, \ or stability selection", font_size=24, color=MAPC),
            label(r"directed graphs: \ Part 36; \ causal discovery: \ Part 62", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Reading such a graph. An absent edge represents conditional independence in the "
            "fitted Gaussian model. Estimation and tuning can miss or add population edges. <bookmark mark='b'/> A "
            "present edge is not a cause: the graph has no arrows. <bookmark mark='c'/> The penalty trades edges "
            "against reliability, and is chosen by cross-validation, BIC, or by keeping only the edges that survive "
            "resampling. <bookmark mark='d'/> Graphs with arrows come in Part 36, and what data alone can say about "
            "causal direction in Part 62."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def neighbourhood(self):
        rows = [
            cmath(r"x_i", r"=", r"\textstyle\sum_{j \ne i} \beta_{ij} x_j + \varepsilon_i", font_size=32),
            cmath(r"\beta_{ij}", r"=", r"-\theta_{ij} / \theta_{ii}", font_size=32),
            cmath(r"\text{lasso each } x_i", r":", r"\text{edge if } \hat\beta_{ij} \ne 0 \text{ (or and/or)}", font_size=30),
            cmath(r"\text{consistent}", r":", r"\text{the right graph with high probability}", font_size=30),
        ]
        rows[1][-1].set_color(MAPC)
        whys = [why(r"regress each on the rest"), why(r"zeros line up with $\Theta$"), why(r"Meinshausen \& B\"uhlmann (2006)"), why(r"under conditions: \ Part 52")]
        with self.voiceover(
            "<bookmark mark='a'/> A simpler route to the same graph. Regress each variable on all the others. "
            "<bookmark mark='b'/> The regression coefficients are proportional to the precision matrix's entries, so a "
            "zero coefficient is a missing edge. <bookmark mark='c'/> Nicolai Meinshausen and Peter Bühlmann ran a "
            "separate lasso for each variable and drew an edge when the coefficient was non-zero, in one regression or "
            "in both. <bookmark mark='d'/> They proved it recovers the right graph with high probability under "
            "conditions that Part 52 makes precise."
        ) as vo:
            intro=label('Nodewise regression links conditional neighborhoods to precision zeros',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
