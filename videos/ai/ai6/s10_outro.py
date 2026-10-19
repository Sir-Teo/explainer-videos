from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, load


def mix(v):
    return interpolate_color(ManimColor(AUSTEN), ManimColor(DICKENS), float(v))


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        out = []
        g = np.random.default_rng(5)
        # 1. least squares: a line and its squares
        P = np.array([[-1.1, -0.5], [0.0, 0.6], [1.1, 0.1]])
        sq = VGroup(Line([-1.4, -0.45, 0], [1.4, 0.55, 0], color=C.MODEL_Q, stroke_width=3))
        for x, yv in P:
            fy = -0.45 + (x + 1.4) / 2.8
            r = yv - fy
            sq.add(Square(abs(r), stroke_color=C.SURPRISE, stroke_width=1.5, fill_color=C.SURPRISE, fill_opacity=0.3)
                   .move_to([x + abs(r) / 2, (yv + fy) / 2, 0]), Dot([x, yv, 0], radius=0.06, color=C.TRUE_P))
        out.append((sq, r"least squares", C.MODEL_Q))
        # 2. the sigmoid sheet, as a curve
        zs = np.linspace(-3, 3, 60)
        sg = VMobject(stroke_width=4).set_points_smoothly([np.array([z * 0.45, 1.2 / (1 + math.exp(-2 * z)) - 0.6, 0])
                                                          for z in zs])
        sg.set_color([AUSTEN, DICKENS])
        out.append((sg, r"logistic regression", C.MODEL_Q))
        # 3. lasso's diamond and a contour
        dia = VGroup(Polygon([0.8, 0, 0], [0, 0.8, 0], [-0.8, 0, 0], [0, -0.8, 0], color=C.BITS, fill_opacity=0.15),
                     Ellipse(width=2.2, height=1.1, color=GREY_B).rotate(0.3).move_to([1.6, 0.25, 0]),
                     Dot([0.8, 0, 0], radius=0.07, color=C.BITS))
        out.append((dia, r"lasso picks words", C.BITS))
        # 4. Fisher's piles
        xs = np.linspace(-3, 3, 60)
        piles = VGroup(*[VMobject(color=c, stroke_width=3).set_points_smoothly(
            [np.array([x * 0.5, 1.1 * math.exp(-0.5 * ((x - m) / 0.7) ** 2) - 0.5, 0]) for x in xs])
            for m, c in ((-0.9, AUSTEN), (0.9, DICKENS))])
        out.append((piles, r"Fisher's direction", C.BITS))
        # 5. nearest neighbours: a patchwork
        pts = g.uniform(-1, 1, (26, 2))
        lab = (pts[:, 0] + 0.4 * pts[:, 1] + 0.3 * g.normal(size=26)) > 0
        cells = VGroup()
        for i in range(14):
            for j in range(10):
                c = np.array([-1 + (i + 0.5) / 7, -1 + (j + 0.5) / 5])
                nn = np.argmin(((pts - c) ** 2).sum(1))
                cells.add(Rectangle(width=1.5 / 7 + 0.005, height=0.95 * 2 / 10 + 0.005, stroke_width=0,
                                    fill_color=mix(lab[nn]), fill_opacity=0.4)
                          .move_to([c[0] * 1.5, c[1] * 0.95, 0]))
        cells.add(*[Dot([p[0] * 1.5, p[1] * 0.95, 0], radius=0.04, color=mix(l_)) for p, l_ in zip(pts, lab)])
        out.append((cells, r"nearest neighbours", GREY_A))
        # 6. the widest street
        st = VGroup(Polygon([-1.4, -0.9, 0], [0.4, 0.9, 0], [1.4, 0.9, 0], [-0.4, -0.9, 0], stroke_width=0,
                            fill_color=C.BITS, fill_opacity=0.15),
                    Line([-0.9, -0.9, 0], [0.9, 0.9, 0], color=C.BITS, stroke_width=3))
        for k in range(7):
            st.add(Dot([-1.3 + 0.18 * k - 0.4, 0.5 - 0.2 * k + 0.3, 0], radius=0.05, color=AUSTEN),
                   Dot([0.9 + 0.18 * k - 0.2, -0.3 - 0.15 * k + 0.2, 0], radius=0.05, color=DICKENS))
        out.append((st, r"support vectors", C.BITS))
        # 7. a tree's boxes
        t = load("trees")
        rects = VGroup()
        box = t["box"]
        for x0, x1, y0, y1, v in t["rects3"]:
            p0 = np.array([(x0 - box[0]) / (box[1] - box[0]) * 3 - 1.5, (y0 - box[2]) / (box[3] - box[2]) * 2 - 1, 0])
            p1 = np.array([(x1 - box[0]) / (box[1] - box[0]) * 3 - 1.5, (y1 - box[2]) / (box[3] - box[2]) * 2 - 1, 0])
            rects.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_color=WHITE, stroke_width=1,
                                fill_color=mix(v), fill_opacity=0.5).move_to((p0 + p1) / 2))
        out.append((rects, r"trees ask questions", C.INTERVAL))
        # 8. a forest
        forest = VGroup()
        for k in range(15):
            tri = Triangle(color=C.INTERVAL, fill_color=C.INTERVAL, fill_opacity=0.25 + 0.5 * g.random(), stroke_width=1)
            forest.add(tri.scale(0.25).move_to([-1.2 + 0.6 * (k % 5), 0.6 - 0.6 * (k // 5), 0]))
        out.append((forest, r"forests and boosting", C.INTERVAL))
        tiles = Group()
        for pic, cap, col in out:
            box_, c = frame(cap, col)
            pic.move_to(box_.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box_, pic, c))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 6, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Least squares fits a line by minimizing squared misses, and its answer is a "
            "perpendicular projection. Logistic regression turns a line into probabilities and fits them by "
            "cross-entropy. The lasso keeps weights in a diamond, and picks out the words that matter. Fisher found "
            "the direction that separates two groups best. Nearest neighbours just ask around. Support vector "
            "machines find the widest street, and kernels bend it. Trees ask questions, and forests and boosting "
            "turn many weak trees into a strong committee."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15, scale=0.95) for t in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"projection, least squares", [7, 12]),
            (r"logistic regression: \ every network's last layer", [9, 13]),
            (r"penalties on weights: \ weight decay", [8, 11]),
            (r"kernels: \ attention as a smoother", [13]),
            (r"nearest neighbours: \ retrieval", [15, 29]),
            (r"memorizing vs generalizing", [8]),
        ], font_size=26)
        with self.voiceover(
            "These ideas don't go away. Projections return with principal components in part seven and with scaling "
            "laws in part twelve. The last layer of every network is a logistic regression. The ridge penalty is "
            "weight decay. Attention, in part thirteen, is a kernel smoother. Nearest neighbours become retrieval. And "
            "the gap between training pages and new pages is all of part eight."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 7, \ Statistical ML", font_size=40).to_edge(UP, buff=0.35)
        g = np.random.default_rng(1977)  # Dempster, Laird & Rubin's EM, 1977
        centers = np.array([[-2.5, 0.6], [0.4, -1.2], [2.8, 0.9]])
        pts = np.vstack([g.normal(c, 0.55, (40, 2)) for c in centers])
        dots = VGroup(*[Dot([p[0], p[1] - 0.3, 0], radius=0.05, color=GREY_B) for p in pts])
        cols = [C.TRUE_P, C.MODEL_Q, C.INTERVAL]
        ells = VGroup(*[Ellipse(width=2.4, height=1.4, color=c, stroke_width=3).move_to([0.0, -0.3, 0])
                        for c in cols])
        targets = [Ellipse(width=2.3, height=2.1, color=c, stroke_width=3).move_to([cc[0], cc[1] - 0.3, 0])
                   for c, cc in zip(cols, centers)]
        tag = label(r"a mixture of bells, fitted by EM \ (illustrative)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Next time: statistical machine learning. Models with hidden parts: principal components, mixtures fitted "
            "by expectation-maximization, hidden Markov models, Gaussian processes, variational inference. "
            "<bookmark mark='a'/> And part one's scoreboard gets a new row, from the best smoothing method of the "
            "counting era."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005), FadeIn(tag), run_time=1.5)
            self.play(FadeIn(ells))
            self.play(*[Transform(e, t_) for e, t_ in zip(ells, targets)], run_time=2.5)
            vo.wait_until("a")
            self.play(*[d.animate.set_color(cols[int(np.argmin(((centers - p) ** 2).sum(1)))]) for d, p in zip(dots, pts)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"T.~Hastie, R.~Tibshirani \& J.~Friedman, \textit{The Elements of Statistical Learning}, 2nd ed.\ (2009)",
            r"C.~M.~Bishop, \textit{Pattern Recognition and Machine Learning} (2006), chapters 3, 4, 6, 7, 14",
            r"K.~P.~Murphy, \textit{Probabilistic Machine Learning: An Introduction} (2022)",
        ]
        papers = [
            r"F.~Mosteller \& D.~L.~Wallace, \textit{Inference in an Authorship Problem} (1963)",
            r"R.~A.~Fisher, \textit{The Use of Multiple Measurements in Taxonomic Problems} (1936)",
            r"A.~E.~Hoerl \& R.~W.~Kennard, \textit{Ridge Regression} (1970); \ R.~Tibshirani, \textit{The Lasso} (1996)",
            r"T.~Cover \& P.~Hart, \textit{Nearest Neighbor Pattern Classification} (1967)",
            r"C.~Cortes \& V.~Vapnik, \textit{Support-Vector Networks} (1995)",
            r"L.~Breiman, \textit{Random Forests} (2001); \ J.~H.~Friedman, \textit{Gradient Boosting} (2001)",
            r"L.~Grinsztajn, E.~Oyallon \& G.~Varoquaux, \textit{Why Do Tree-Based Models Still Outperform Deep "
            r"Learning on Tabular Data?} (2022)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Project Gutenberg (Austen and Dickens, from Part 1's novels). \ Every method is written out "
                    r"in numpy; \ every number on screen is computed and checked.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Hastie, Tibshirani and Friedman's Elements of Statistical Learning covers every method here, and much "
            "more. Thanks for watching, and see you in part seven."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
