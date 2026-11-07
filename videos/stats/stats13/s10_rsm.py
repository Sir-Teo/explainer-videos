from __future__ import annotations

import numpy as np

from videos.stats.stats13.common import *  # noqa: F403
from videos.stats.stats13.s08_factorial import bakery_map


class Surface(VoiceoverScene):
    def construct(self):
        self.card()
        self.box_wilson()
        self.first_order()
        self.ascent()
        self.ccd()
        self.quadratic()
        self.result()

    def card(self):
        card = chapter_card(9, r"Response surfaces", r"Climbing a hill you cannot see", part=PART)
        with self.voiceover("Chapter nine. Response surfaces."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def box_wilson(self):
        hc = history_card(1951, r"George Box \ and \ K. B. Wilson, \ Imperial Chemical Industries",
                          r"``On the experimental attainment of optimum conditions'': \ a chemical yield depends on temperature, \ "
                          r"pressure, \ time and concentrations; \ find the best settings in as few runs as possible", color=S.POST,
                          width=10.6, font_size=22).move_to([0, 1.3, 0])
        rows = fit_rows(VGroup(
            label(r"in a factory, \ runs can be quicker than field trials: \ experiment sequentially", font_size=24),
            label(r"far from the top, \ the surface looks like a plane: \ fit one, \ and climb", font_size=24, color=S.POST),
            label(r"near the top, \ it looks like a quadratic: \ fit one, \ and find its peak", font_size=24, color=OBS),
        ), 12.4, 0.3, [0, -1.7, 0])
        intro = label('Sequential experiments fit a local response surface', font_size=36)
        with self.voiceover(
            "Agriculture gets one harvest a year. Industry can run an experiment every afternoon. <bookmark mark='a'/> In "
            "1951 George Box, a chemist turned statistician, and K. B. Wilson, both at Imperial Chemical Industries, "
            "published a strategy for finding the best operating conditions of a chemical process. <bookmark mark='b'/> "
            "Experiment in stages, each designed from what the last one found. <bookmark mark='c'/> Far from the optimum, "
            "a small piece of any smooth surface looks like a tilted plane: fit a plane, and walk uphill. <bookmark mark='d'/> "
            "Near the top, the surface looks like a quadratic bowl, upside down: fit a quadratic, and find its peak. Let's give "
            "the island's baker the method."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def first_order(self):
        d = load("rsm")
        A, ax, cells = bakery_map([-2.8, -0.1, 0])
        cells.set_opacity(0.0)
        pts = np.asarray(d["pts"])
        y = np.asarray(d["y"])
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=WHITE) for p in pts[:5]])
        box = Polygon(*[ax.c2p(*pts[i]) for i in (0, 1, 3, 2)], color=GREY_A, stroke_width=2)
        b = d["coef1"]
        rows = fit_rows(VGroup(
            label(r"stage 1: \ a $2^2$ factorial + 3 centre bakes", font_size=24),
            label(r"coded: \ $x_1 = (T - 185)/8$, \ $x_2 = (t - 22)/3$", font_size=22, color=GREY_A),
            MathTex(rf"\hat y = {b[0]:.1f} + {b[1]:.1f}\,x_1 + {b[2]:.1f}\,x_2", font_size=30, color=S.POST),
            MathTex(rf"\bar y_{{\text{{corners}}}} - \bar y_{{\text{{centre}}}} = {d['curv']:.1f}", font_size=28),
            label(r"a little curvature; \ the slope dominates", font_size=24, color=OBS),
            label(r"the centre bakes also measure the noise", font_size=22, color=GREY_A),
        ), 5.2, 0.34, [4.0, 0.1, 0])
        vals = VGroup(*[label(rf"{v:.0f}", font_size=20, color=WHITE).next_to(dd, UR, buff=0.04) for v, dd in zip(y[:5], dots)])
        tag = simulated_tag(r"the island bakery, \ noise SD 1.5", corner=DR)
        with self.voiceover(
            "Now the surface is hidden, as it is for the baker. <bookmark mark='a'/> Start at his current recipe, one eighty-five "
            "degrees and twenty-two minutes. Bake at the four corners of a small square around it, and three times at the "
            "centre: seven bakes. <bookmark mark='b'/> Work in coded units, so each factor runs from minus one to plus one. "
            "<bookmark mark='c'/> Fit a plane by least squares: quality forty-four, plus twelve point six per unit of "
            "temperature, plus fifteen point six per unit of time. <bookmark mark='d'/> Is a plane good enough? Compare the "
            "corners' average with the centre's. If the surface curved strongly, they'd differ. They differ by about four "
            "points, small beside the slopes. <bookmark mark='e'/> So the plane is a fair local description, and its gradient "
            "points uphill. <bookmark mark='f'/> The repeated centre bakes also measure the noise, which is how the method "
            "knows a difference from an accident."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(box), LaggedStart(*[FadeIn(d_, scale=2) for d_ in dots], lag_ratio=0.15), FadeIn(vals), FadeIn(rows[0]))
            for k, m_ in enumerate("bcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def ascent(self):
        d = load("rsm")
        A, ax, cells = bakery_map([-3.6, 0.6, 0], width=5.2, height=3.6)
        cells.set_opacity(0.0)
        path = np.asarray(d["path"])
        yp = np.asarray(d["ypath"])
        start = Dot(ax.c2p(*path[0]), radius=0.09, color=WHITE)
        arrow = Arrow(ax.c2p(*path[0]), ax.c2p(*path[2]), buff=0, color=S.POST, stroke_width=5)
        pdots = VGroup(*[Dot(ax.c2p(*p), radius=0.08, color=S.POST) for p in path[1:]])
        B = axes([0, 8.5], [30, 95], x_length=5.0, y_length=3.4, xlabel=r"steps along the path", ylabel=r"quality",
                 xticks=[0, 2, 4, 6, 8], yticks=[40, 60, 80], center=[3.6, 0.6, 0])
        bx = B.ax
        qd = VGroup(*[Dot(bx.c2p(k, v), radius=0.08, color=S.POST) for k, v in enumerate(yp)])
        ql = VMobject(stroke_color=S.POST, stroke_width=3).set_points_as_corners([bx.c2p(k, v) for k, v in enumerate(yp)])
        kb = d["kbest"]
        best = Circle(radius=0.2, color=OBS, stroke_width=4).move_to(bx.c2p(kb, yp[kb]))
        rows = fit_rows(VGroup(
            label(r"stage 2: \ the path of steepest ascent, \ along the fitted gradient $(12.6, \ 15.6)$", font_size=22),
            label(r"bake one recipe per step; \ quality rises, \ peaks, \ then falls", font_size=22, color=S.POST),
            label(rf"best at step {kb}: \ {d['c1'][0]:.0f}$^\circ$C, \ {d['c1'][1]:.1f} min, \ quality {yp[kb]:.1f}", font_size=24, color=OBS),
            label(r"the plane's prediction fails here: \ we are near the top", font_size=22, color=GREY_A),
        ), 12.6, 0.24, [0, -2.55, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Stage two: walk uphill. The path of steepest ascent leaves the centre along the fitted "
            "gradient, twelve point six units of temperature for every fifteen point six of time, in coded units. "
            "<bookmark mark='b'/> Bake one recipe at each step along it. Quality climbs fast: forty-five, sixty-two, "
            "seventy-six, then eighty-five, twice. Then it falls. <bookmark mark='c'/> The best is at step four, two oh five degrees and "
            "thirty-one minutes, quality eighty-five. <bookmark mark='d'/> The plane predicted endless improvement; the "
            "fall means we've reached the curved region near the top, where a plane is no longer good enough."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(start))
            vo.wait_until("a")
            self.play(GrowArrow(arrow), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(qd[0]))
            for k in range(1, len(path)):
                self.play(FadeIn(pdots[k - 1], scale=2), FadeIn(qd[k], scale=2), run_time=0.45)
            self.play(Create(ql), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(best), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ccd(self):
        d = load("rsm")
        A, ax, cells = bakery_map([-2.8, -0.1, 0])
        cells.set_opacity(0.0)
        pts2 = np.asarray(d["pts2"])
        fac = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=WHITE) for p in pts2[:4]])
        axial = VGroup(*[Dot(ax.c2p(*p), radius=0.09, color=S.ALT) for p in pts2[4:8]])
        ctr = Dot(ax.c2p(*pts2[8]), radius=0.11, color=OBS)
        sq = Polygon(*[ax.c2p(*pts2[i]) for i in (0, 1, 3, 2)], color=GREY_A, stroke_width=2)
        circ = Ellipse(width=abs(ax.c2p(pts2[5][0], 0)[0] - ax.c2p(pts2[4][0], 0)[0]),
                       height=abs(ax.c2p(0, pts2[7][1])[1] - ax.c2p(0, pts2[6][1])[1]), color=GREY_C, stroke_width=1.5).move_to(ctr)
        rows = fit_rows(VGroup(
            label(r"stage 3: \ a central composite design", font_size=24),
            label(r"4 factorial corners", font_size=24),
            label(r"4 axial points at $\pm\sqrt2$: \ a circle", font_size=24, color=S.ALT),
            label(r"5 centre bakes", font_size=24, color=OBS),
            label(r"13 bakes: \ a full quadratic", font_size=24, color=OBS),
            label(r"rotatable: \ equal precision all round", font_size=22, color=GREY_A),
        ), 5.0, 0.34, [4.1, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Stage three: Box and Wilson's central composite design, centred on the best point found. "
            "<bookmark mark='b'/> A small factorial square, <bookmark mark='c'/> plus four axial points, out along each axis at "
            "plus or minus root two in coded units, so all eight lie on a circle. <bookmark mark='d'/> Plus five bakes at the "
            "centre. <bookmark mark='e'/> Thirteen bakes, with five distinct levels of each factor: enough to fit a full "
            "quadratic, with its curvatures and its interaction. <bookmark mark='f'/> Putting the axial points at root two "
            "makes the design rotatable: under independent equal-variance errors, fitted-mean prediction variance depends only on the distance from the centre in coded units."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sq), FadeIn(fac, scale=2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(circ), FadeIn(axial, scale=2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(ctr, scale=2), FadeIn(rows[3]))
            for k, m_ in enumerate("ef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 4]))
        self.clear_scene()

    def quadratic(self):
        d = load("rsm")
        b0, b1, b2, b11, b22, b12 = d["coef2"]
        e1, e2 = d["eig"]
        rows = [
            cmath(r"\hat y", r"=", rf"{b0:.1f} {b1:+.2f}\,x_1 {b2:+.2f}\,x_2 {b11:+.2f}\,x_1^2 {b22:+.2f}\,x_2^2 {b12:+.2f}\,x_1x_2", font_size=30),
            cmath(r"\hat y", r"=", r"b_0 + x^\top b + x^\top B x", font_size=32),
            cmath(r"x_s", r"=", r"-\tfrac12 B^{-1} b", font_size=34),
            cmath(r"\text{eig}(B)", r"=", rf"({e1:.2f},\ {e2:.2f})", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"least squares on the 13 bakes"), why(r"$B$ holds the curvatures, \ half the interaction off the diagonal"),
                why(r"the stationary point: \ gradient zero"), why(r"both negative: \ a maximum; \ the small one is the ridge")]
        with self.voiceover(
            "<bookmark mark='a'/> Fit the quadratic by least squares: an intercept, two slopes, two curvatures and an "
            "interaction. <bookmark mark='b'/> In matrix form, b zero, plus x transpose b, plus x transpose B x, with the "
            "curvatures on B's diagonal and half the interaction off it. <bookmark mark='c'/> Set the gradient to zero: the "
            "stationary point is minus a half B inverse b. <bookmark mark='d'/> Is it a peak, a valley or a saddle? B's "
            "eigenvalues tell. Both are negative, so it's a maximum. One is three times the other: the surface falls steeply "
            "in one direction and gently in the other, along the ridge, where temperature and time can trade off. Box called "
            "this canonical analysis."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-2.4, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def result(self):
        d = load("rsm")
        A, ax, cells = bakery_map([-2.8, -0.1, 0])
        pts = np.asarray(d["pts"])[:5]
        path = np.asarray(d["path"])
        pts2 = np.asarray(d["pts2"])
        s1 = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=WHITE) for p in pts])
        s2 = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=S.POST) for p in path[1:]])
        s3 = VGroup(*[Dot(ax.c2p(*p), radius=0.06, color=S.ALT) for p in pts2[:9]])
        st = Star(n=5, outer_radius=0.18, color=OBS, fill_opacity=1).move_to(ax.c2p(*d["stationary"]))
        tr = Star(n=5, outer_radius=0.14, color=EXACT, fill_opacity=0.6).move_to(ax.c2p(205, 31))
        rows = fit_rows(VGroup(
            MathTex(rf"x_s:\ {d['stationary'][0]:.1f}^\circ\text{{C}},\ \ {d['stationary'][1]:.1f}\ \text{{min}}", font_size=30, color=OBS),
            MathTex(rf"\text{{predicted}}\ {d['pred_max']:.1f};\quad\text{{true quality there}}\ {d['truth_at']:.1f}", font_size=28),
            label(r"the true optimum: \ 205$^\circ$C, \ 31 min, \ 85", font_size=22, color=EXACT),
            label(rf"{d['runs']} bakes in all, \ in three stages", font_size=24, color=OBS),
            label(r"each stage designed from the last", font_size=22),
            label(r"``all models are wrong, \ but some are useful'' \ (Box)", font_size=22, color=GREY_A),
        ), 4.8, 0.32, [4.3, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The fitted peak is at two oh three degrees and thirty-one point seven minutes. "
            "<bookmark mark='b'/> The quadratic predicts a quality of eighty-five point two there; the hidden truth at that "
            "recipe is eighty-four point nine. <bookmark mark='c'/> Now reveal the surface: the true optimum, two oh five and "
            "thirty-one, is right beside it. <bookmark mark='d'/> Twenty-nine bakes in all, in three stages. "
            "<bookmark mark='e'/> The plane was wrong, and the quadratic is wrong too: the true surface isn't a quadratic far "
            "from the top. But each was useful exactly where it was used. <bookmark mark='f'/> That's George Box's famous line: "
            "all models are wrong, but some are useful."
        ) as vo:
            cells.set_fill(opacity=0)
            self.add(cells)
            self.play(FadeIn(A), FadeIn(s1), FadeIn(s2), FadeIn(s3))
            vo.wait_until("a")
            self.play(FadeIn(st, scale=2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(cells.animate.set_fill(opacity=1), FadeIn(tr, scale=2), FadeIn(rows[2]), run_time=1.5)
            for k, m_ in enumerate("def"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 3]))
        self.clear_scene()
