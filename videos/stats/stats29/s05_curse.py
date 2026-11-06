from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Curse(VoiceoverScene):
    def construct(self):
        self.card()
        self.rate()
        self.table()
        self.corners()
        self.neighbours()
        self.shell()
        self.escape()

    def card(self):
        card = chapter_card(4, r"The curse of dimensionality", r"Why smoothing fails in many dimensions", lit=(1961,), part=PART)
        with self.voiceover("Chapter four. The curse of dimensionality."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rate(self):
        rows = [
            cmath(r"\text{bias}^2", r"\propto", r"h^4, \ \ \text{as before}", font_size=30),
            cmath(r"\text{variance}", r"\propto", r"\dfrac{1}{n h^d}: \ \text{a box of volume } h^d", font_size=30),
            cmath(r"h^*", r"\propto", r"n^{-1/(4 + d)}", font_size=32),
            cmath(r"\text{MISE}", r"\propto", r"n^{-4/(4 + d)}", font_size=34),
        ]
        rows[3][2].set_color(RES)
        whys = [why(r"curvature in each direction"), why(r"the local sample shrinks like $h^d$"), why(r"balance them"),
                why(r"$d = 1$: \ $n^{-0.8}$; \ $d = 10$: \ $n^{-0.29}$")]
        with self.voiceover(
            "<bookmark mark='a'/> In d dimensions, the bias of a kernel estimate is still of order h squared. "
            "<bookmark mark='b'/> But the number of observations in a window of width h is now n times h to the d, so the "
            "variance is one over n h to the d. <bookmark mark='c'/> Balancing gives a bandwidth shrinking like n to the "
            "minus one over four plus d, <bookmark mark='d'/> and an error falling like n to the minus four over four plus "
            "d. In one dimension, minus point eight. In ten, minus point two nine. Richard Bellman named the problem the curse "
            "of dimensionality in 1961."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("curse")["table"]
        dims = list(range(1, 11))
        A = axes([0.5, 10.5], [0, 6.3], x_length=7.4, y_length=4.4, xlabel=r"dimension $d$", ylabel=r"sample size needed (log scale)",
                 xticks=dims, yticks=[0, 2, 4, 6], yfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.0, 0.3, 0])
        ax = A.ax
        w = ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0]
        bars = VGroup(*[Rectangle(width=w, height=ax.c2p(0, np.log10(d[str(k)]))[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=RES if k >= 6 else KDEC, fill_opacity=0.8).move_to(ax.c2p(k, np.log10(d[str(k)]) / 2))
                        for k in dims])
        nums = VGroup(*[label(f"{d[str(k)]:,}", font_size=16, color=GREY_A).next_to(bars[k - 1], UP, buff=0.06) for k in dims])
        rows = fit_rows(VGroup(
            label(r"estimate a standard normal density at its centre", font_size=22),
            label(r"to relative MSE 0.1, \ best bandwidth, \ exact error", font_size=22),
            label(rf"$d = 1$: \ {d['1']} points; \ $d = 2$: \ {d['2']}", font_size=22, color=KDEC),
            label(rf"$d = 5$: \ {d['5']:,}", font_size=22, color=KDEC),
            label(rf"$d = 10$: \ {d['10']:,}", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Silverman's table makes it concrete. Estimate a standard normal density at its centre, "
            "where it is easiest, <bookmark mark='b'/> to within ten percent relative mean squared error, at the best "
            "bandwidth, computing the error exactly. <bookmark mark='c'/> In one dimension, four observations suffice; in "
            "two, nineteen. <bookmark mark='d'/> In five, seven hundred and sixty-eight. <bookmark mark='e'/> In ten, eight "
            "hundred and forty-two thousand. These are statkit's numbers; they reproduce Silverman's 1986 table."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[0], DOWN), GrowFromEdge(bars[1], DOWN), FadeIn(nums[:2]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[2:5]], lag_ratio=0.3), FadeIn(nums[2:5]), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[5:]], lag_ratio=0.3), FadeIn(nums[5:]), FadeIn(rows[4]))
        self.clear_scene()

    def corners(self):
        d = load("curse")["ball"]
        dims = list(range(1, 21))
        A = axes([0.5, 20.5], [0, 1.05], x_length=7.4, y_length=4.2, xlabel=r"dimension $d$", ylabel=r"share of the cube",
                 xticks=[1, 5, 10, 15, 20], yticks=[0, 0.5, 1], center=[-2.0, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(k, d[str(k)]), radius=0.07, color=KDEC) for k in dims])
        line = polyline(ax, dims, [d[str(k)] for k in dims], KDEC, 2.5)
        sq = VGroup(Square(side_length=1.6, color=GREY_B), Circle(radius=0.8, color=KDEC, fill_opacity=0.25)).move_to([4.4, 1.6, 0])
        rows = fit_rows(VGroup(
            label(r"the ball inside the unit cube", font_size=22),
            label(rf"$d = 2$: \ {100 * d['2']:.1f}\%; \ \ $d = 3$: \ {100 * d['3']:.1f}\%", font_size=22, color=KDEC),
            label(rf"$d = 10$: \ {100 * d['10']:.2f}\%", font_size=22, color=RES),
            label(r"almost everything is in the corners", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, -0.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Geometry explains it. Inscribe a ball in a cube. <bookmark mark='b'/> In two dimensions "
            "the disc fills seventy-nine percent of the square; in three, the ball fills fifty-two percent of the cube. "
            "<bookmark mark='c'/> In ten dimensions, a quarter of one percent. <bookmark mark='d'/> Almost all of a "
            "high-dimensional cube is corners, far from its centre, so any neighbourhood small enough to be local contains "
            "almost none of the data."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(sq), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.05), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def neighbours(self):
        d = load("curse")["nn"]
        hdr = [r"\textbf{dimension}", r"\textbf{nearest of 999 neighbours}", r"\textbf{nearest / farthest}"]
        body = [[f"{k}", f"{v['nearest']:.3g}", f"{v['ratio']:.2g}"] for k, v in d.items()]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.3, colors=[GREY_A] + [None] * 6)
        for r in tb[1:]:
            r[1].set_color(KDEC)
            r[2].set_color(RES)
        tb.move_to([0, 0.7, 0])
        foot = fit_rows(VGroup(
            label(r"1,000 points uniform in the unit cube; \ medians over 200 of them", font_size=22),
            label(r"in high dimension every point is far from every other, \ and about equally far", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -2.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Or measure it. Scatter a thousand points uniformly in a cube and find each point's nearest "
            "neighbour. <bookmark mark='b'/> In one dimension it is a few ten-thousandths away. In ten dimensions, half the "
            "cube's side. In fifty, more than twice the side. And the nearest neighbour is nearly as far as the farthest: "
            "the ratio climbs towards one. Kevin Beyer and colleagues asked in 1999 when 'nearest neighbour' is meaningful "
            "at all."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tb[1:]], lag_ratio=0.4), FadeIn(foot[1]), run_time=4.0)
        self.wait(1.0)
        self.clear_scene()

    def escape(self):
        rows = fit_rows(VGroup(
            label(r"assume structure: \ additive models \ (chapter ten)", font_size=24, color=SPLC),
            label(r"single and multiple index models: \ $f(x) = g(\beta^\top x)$", font_size=24, color=KDEC),
            label(r"sparsity: \ only a few variables matter \ (Part 32)", font_size=24, color=WAVC),
            label(r"smoothness: \ more derivatives, \ faster rates \ (Part 50)", font_size=24, color=PATH),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The escapes all assume structure. Additive models, chapter ten, estimate a sum of "
            "one-dimensional curves, each at the one-dimensional rate. <bookmark mark='b'/> Index models smooth along a few "
            "estimated directions. <bookmark mark='c'/> Sparsity assumes only a few variables matter, Part 32. "
            "<bookmark mark='d'/> And smoother truths permit faster rates: with s derivatives the rate is n to the minus two "
            "s over two s plus d, Charles Stone's result, which Part 50 proves optimal."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def shell(self):
        rows = [
            cmath(r"X \sim N(0, I_d)", r":", r"\|X\|^2 = \textstyle\sum_j X_j^2 \sim \chi^2_d", font_size=30),
            cmath(r"E\|X\|^2", r"=", r"d, \ \ \mathrm{SD}\,\|X\|^2 = \sqrt{2d}", font_size=30),
            cmath(r"\|X\|", r"\approx", r"\sqrt d \pm 0.7", font_size=34),
            cmath(r"\text{density at the centre}", r":", r"\text{highest, \ yet almost no data there}", font_size=28),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"a standard normal cloud"), why(r"Part 6's chi-squared"), why(r"a thin shell of radius $\sqrt d$"),
                why(r"Silverman's table estimated $f(0)$")]
        with self.voiceover(
            "<bookmark mark='a'/> Even a normal cloud is mostly far from its centre. The squared distance of a standard "
            "normal point from the origin is chi-squared with d degrees of freedom. <bookmark mark='b'/> Its mean is d, its "
            "standard deviation root two d. <bookmark mark='c'/> So the distance itself is about root d, give or take "
            "point seven, whatever d is: in high dimensions the points live in a thin shell. <bookmark mark='d'/> The "
            "density is highest at the centre, where Silverman's table estimated it, and yet almost no observations fall "
            "anywhere near it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
