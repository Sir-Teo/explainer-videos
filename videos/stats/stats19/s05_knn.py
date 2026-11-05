from __future__ import annotations

import numpy as np

from explainer.stats.kit import learn as L
from videos.stats.stats19.common import *  # noqa: F403


class Neighbours(VoiceoverScene):
    def construct(self):
        self.card()
        self.regions()
        self.curse_cube()
        self.distances()
        self.irrelevant()
        self.cover_hart()
        self.lessons()

    def card(self):
        card = chapter_card(4, r"$k$-nearest neighbours", r"Predict like your neighbours, \ if you have any", part=PART)
        with self.voiceover("Chapter four. Nearest neighbours."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def region_map(self, ax, X, v, k, nx=36, ny=26):
        xs = np.linspace(0.6, 2.6, nx)
        ys = np.linspace(18, 95, ny)
        G = np.array([[a, b] for b in ys for a in xs])
        sc = np.array([1.0, 1 / 35.0])  # put log income and age on comparable scales
        pr = L.knn_predict(X * sc, v, G * sc, k)
        cw = ax.c2p(xs[1], 0)[0] - ax.c2p(xs[0], 0)[0]
        ch = ax.c2p(0, ys[1])[1] - ax.c2p(0, ys[0])[1]
        cells = VGroup()
        for (a, b), p in zip(G, pr):
            cells.add(Rectangle(width=cw, height=ch, stroke_width=0, fill_color=BLUE if p > 0.5 else RED, fill_opacity=0.18 + 0.3 * abs(p - 0.5))
                      .move_to(ax.c2p(a, b)))
        return cells

    def regions(self):
        d = load("tree")
        X, v = np.asarray(d["sample_x"]), np.asarray(d["sample_v"])
        panels = VGroup()
        for j, k in enumerate((1, 51)):
            A = axes([0.6, 2.6], [18, 95], x_length=5.4, y_length=3.8, xlabel=r"income, \ thousands \ (log scale)", ylabel=r"age",
                     xticks=[1, 1.5, 2, 2.5], yticks=[20, 40, 60, 80], center=[-3.4 + 6.8 * j, 0.4, 0], font_size=16,
                     xfmt=lambda u: f"{10 ** u:.0f}")
            ax = A.ax
            cells = self.region_map(ax, X, v, k)
            dots = VGroup(*[Dot(ax.c2p(min(max(a, 0.62), 2.58), b), radius=0.035, color=BLUE if c else RED) for (a, b), c in zip(X, v)])
            t = label(rf"$k = {k}$", font_size=24, color=GREY_A).next_to(A, UP, buff=0.1)
            panels.add(VGroup(A, cells, dots, t))
        rows = fit_rows(VGroup(
            label(r"600 adults from the World: \ income, \ age, \ and the vote", font_size=22),
            label(r"$k = 1$: \ a patchwork that copies every point", font_size=22, color=RES),
            label(r"$k = 51$: \ smooth regions: \ richer adults lean Blue", font_size=22, color=HIT),
        ), 12.4, 0.25, [0, -2.6, 0])
        tag = simulated_tag(r"the World's survey block", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> Nearest neighbours classify too. Here are six hundred adults from the World, by income and age, "
            "coloured by their vote. Shade each spot of the plane by the vote of its nearest neighbours. "
            "<bookmark mark='b'/> With one neighbour, the map is a patchwork: every point claims a little territory, noise "
            "included. That's a rule with no bias and enormous variance. <bookmark mark='c'/> With fifty-one neighbours, the map "
            "is smooth, and shows the real pattern: Blue's support grows with income. The vote is hard to predict from income "
            "and age alone, and the smoother map is honest about that."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(panels[0][0]), FadeIn(panels[0][2]), FadeIn(panels[1][0]), FadeIn(panels[1][2]))
            vo.wait_until("b")
            self.play(FadeIn(panels[0][1]), FadeIn(panels[0][3]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(panels[1][1]), FadeIn(panels[1][3]), FadeIn(rows[2]))
        self.clear_scene()

    def curse_cube(self):
        d = load("curse")
        tab = table_rows([
            [r"dimensions $p$", *[str(p) for p in d["dims"]]],
            [r"edge of a cube holding 10\%", *[f"{s:.2f}" for s in d["side"]]],
        ], font_size=26, colors=[GREY_B, OBS]).move_to([0, 1.2, 0])
        rows = fit_rows(VGroup(
            MathTex(r"\text{edge} = 0.1^{1/p}", font_size=32),
            label(r"in 10 dimensions, \ a ``neighbourhood'' with 10\% of the data spans 79\% of every axis", font_size=24, color=RES),
            label(r"local is no longer local", font_size=26, color=OBS),
            label(r"Bellman (1961): \ the curse of dimensionality", font_size=22, color=GREY_A),
        ), 12.4, 0.35, [0, -1.4, 0])
        with self.voiceover(
            "Nearest neighbours rely on there being near neighbours, and in many dimensions there aren't. "
            "<bookmark mark='a'/> Spread data uniformly in a unit cube, and ask how big a sub-cube must be to hold ten percent "
            "of it. Its edge is point one to the power one over p. <bookmark mark='b'/> In one dimension, a tenth of the axis. "
            "In ten dimensions, seventy-nine percent of every axis. In a hundred, ninety-eight. <bookmark mark='c'/> A "
            "neighbourhood that holds enough points to average is no longer local at all. <bookmark mark='d'/> Richard Bellman "
            "called this the curse of dimensionality, in 1961."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def distances(self):
        d = load("curse")
        dims = np.log10(np.asarray(d["dims"], float))
        A = axes([-0.1, 2.1], [0, 1], x_length=7.6, y_length=4.0, xlabel=r"dimensions $p$",
                 ylabel=r"nearest distance / average distance", xticks=[0, 1, 2], yticks=[0, 0.5, 1], center=[-1.8, 0.3, 0],
                 xfmt=lambda u: f"{10 ** u:.0f}")
        ax = A.ax
        c = polyline(ax, dims, d["nn_ratio"], RES, 3.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=RES) for a, b in zip(dims, d["nn_ratio"])])
        rows = fit_rows(VGroup(
            label(r"500 random points in the unit cube", font_size=22),
            label(r"how near is the nearest, \ compared with the average?", font_size=22),
            MathTex(rf"p = 1:\ {d['nn_ratio'][0]:.3f};\ \ p = 100:\ {d['nn_ratio'][-1]:.2f}", font_size=26, color=RES),
            label(r"in high dimensions, \ everyone is about equally far away", font_size=22, color=OBS),
        ), 4.4, 0.4, [4.8, 0.3, 0])
        tag = simulated_tag(r"uniform points", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Another way to see it: scatter five hundred random points in a cube, and compare one point's "
            "nearest neighbour with its average distance to the others. <bookmark mark='b'/> In one dimension the nearest point "
            "is three thousandths as far as the average. <bookmark mark='c'/> In a hundred dimensions it's eighty-one percent as "
            "far. <bookmark mark='d'/> Everyone is about equally distant, so the nearest neighbour is barely nearer than a "
            "random point, and averaging neighbours is little better than averaging everyone."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(dots))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def irrelevant(self):
        d = load("curse")
        dims = np.log10(np.asarray(d["dims"], float))
        A = axes([-0.1, 2.1], [0, 0.5], x_length=7.6, y_length=4.0, xlabel=r"dimensions: \ 1 relevant, \ the rest noise",
                 ylabel=r"10-NN test error", xticks=[0, 1, 2], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], center=[-1.8, 0.3, 0],
                 xfmt=lambda u: f"{10 ** u:.0f}")
        ax = A.ax
        c = polyline(ax, dims, d["err"], OBS, 3.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=OBS) for a, b in zip(dims, d["err"])])
        nz = DashedLine(ax.c2p(-0.1, 0.09), ax.c2p(2.1, 0.09), color=GREY_B, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"chapter one's curve in $x_1$; \ $x_2, \ldots, x_p$ irrelevant", font_size=22),
            MathTex(rf"p = 1:\ {d['err'][0]:.3f}\ \ \to\ \ p = 100:\ {d['err'][-1]:.2f}", font_size=26, color=OBS),
            label(r"the noise dimensions drown the signal in the distances", font_size=22, color=RES),
            label(r"remedies: \ choose variables, \ or methods with structure", font_size=22, color=HIT),
        ), 4.4, 0.4, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And irrelevant variables do real damage. Predict chapter one's curve, which depends on one "
            "variable, from that variable plus p minus one that are pure noise. <bookmark mark='b'/> With the relevant variable "
            "alone, ten nearest neighbours have a test error of point oh eight six, close to the noise. With ninety-nine "
            "irrelevant ones added, point four three, barely better than the point four five of simply predicting the average. <bookmark mark='c'/> The noise "
            "dimensions dominate the distances, so the neighbours aren't really neighbours in the dimension that matters. "
            "<bookmark mark='d'/> The remedies are to choose variables, or to use methods with more structure, like the "
            "linear models, trees and penalties that follow."
        ) as vo:
            self.play(FadeIn(A), Create(nz))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(dots), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def cover_hart(self):
        d = load("coverhart")
        ns = np.log10(np.asarray(d["ns"], float))
        A = axes([0.9, 3.6], [0.15, 0.4], x_length=8.0, y_length=4.4, xlabel=r"training points $n$ \ (log scale)",
                 ylabel=r"error on 12,000 new points", xticks=[1, 2, 3], yticks=[0.15, 0.2, 0.25, 0.3, 0.35, 0.4],
                 center=[-1.6, 0.3, 0], xfmt=lambda v: f"{10 ** v:,.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        bayes = DashedLine(ax.c2p(0.9, d["bayes"]), ax.c2p(3.6, d["bayes"]), color=HIT, stroke_width=2.5)
        bound = DashedLine(ax.c2p(0.9, d["bound"]), ax.c2p(3.6, d["bound"]), color=RES, stroke_width=2, dash_length=0.08)
        limit = DashedLine(ax.c2p(0.9, d["nn_limit"]), ax.c2p(3.6, d["nn_limit"]), color=BLUE, stroke_width=1.5, dash_length=0.05)
        c1 = polyline(ax, ns, d["err1"], BLUE, 3.5)
        d1 = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=BLUE) for a, b in zip(ns, d["err1"])])
        ck = polyline(ax, ns, d["errk"], OBS, 3.5)
        dk = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=OBS) for a, b in zip(ns, d["errk"])])
        rows = fit_rows(VGroup(
            label(r"two normal classes, \ means 0 and 1.5, \ SD 1", font_size=22),
            label(rf"green: \ the Bayes rule, \ {100 * d['bayes']:.1f}\%", font_size=22, color=HIT),
            label(rf"blue: \ 1-NN, \ toward {100 * d['nn_limit']:.1f}\%", font_size=22, color=BLUE),
            label(rf"red: \ $2R^*(1 - R^*) = {100 * d['bound']:.1f}\%$, \ the bound", font_size=22, color=RES),
            label(rf"gold: \ $\sqrt n$-NN, \ down to {100 * d['errk'][-1]:.1f}\%", font_size=22, color=OBS),
            label(r"Cover \& Hart (1967); \ Stone (1977)", font_size=20, color=GREY_B),
        ), 3.45, 0.38, [5.1, 0.3, 0])
        tag = simulated_tag(r"simulated: \ 20 training sets per $n$")
        with self.voiceover(
            "Nearest neighbours have one beautiful guarantee, in low dimensions. <bookmark mark='a'/> Take two classes, normal "
            "with means zero and one and a half, and the same spread. <bookmark mark='b'/> The best possible rule, the Bayes "
            "rule, knows the distributions and cuts halfway between the means. Its error is twenty-two point seven percent, and "
            "no rule can do better. <bookmark mark='c'/> One nearest neighbour knows nothing about normal distributions, yet as "
            "the data grows its error settles at thirty-one percent. <bookmark mark='d'/> Thomas Cover and Peter Hart proved in "
            "1967 that this limit is never more than twice the Bayes error: two R star times one minus R star, here thirty-five "
            "percent. Half the information in the data, they put it, is in the nearest neighbour. <bookmark mark='e'/> And let "
            "k grow with n, here the square root of n, and the error falls toward the Bayes rate itself, twenty-two point six "
            "percent at three thousand points. Charles Stone showed in 1977 that this holds for every distribution, which is "
            "what makes nearest neighbours a universally consistent rule, as long as the dimension doesn't ruin the "
            "neighbourhoods first."
        ) as vo:
            self.add(tag)
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(bayes), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(d1), Create(limit), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(bound), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Create(ck), FadeIn(dk), FadeIn(rows[4]), FadeIn(rows[5]), run_time=2.0)
        self.wait(1.0)
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"$k$-NN: \ no model, \ just local averaging", font_size=24),
            label(r"excellent in low dimensions with plenty of data", font_size=24, color=HIT),
            label(r"in high dimensions, \ neighbourhoods stop being local", font_size=24, color=RES),
            label(r"structure beats proximity: \ assumptions buy back what dimensions take away", font_size=24, color=OBS),
            label(r"Parts 29, \ 51 and 52: \ smoothing and high-dimensional statistics", font_size=22, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So nearest neighbours make no model at all: they just average locally. <bookmark mark='b'/> In "
            "low dimensions with plenty of data, that works remarkably well. <bookmark mark='c'/> In high dimensions, "
            "neighbourhoods stop being local. <bookmark mark='d'/> There, structure beats proximity: assumptions about the form of "
            "the rule, such as linearity or sparsity, buy back what the dimensions take away. <bookmark mark='e'/> Parts 29, 51 "
            "and 52 take this further."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
