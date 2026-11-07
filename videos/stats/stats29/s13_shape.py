from __future__ import annotations

import numpy as np

from videos.stats.stats29.common import *  # noqa: F403


class Shape(VoiceoverScene):
    def construct(self):
        self.card()
        self.isotonic()
        self.pava_picture()
        self.grenander_idea()
        self.grenander_picture()
        self.rate()
        self.more()

    def card(self):
        card = chapter_card(12, r"Shape constraints", r"Only monotone: \ no bandwidth at all", lit=(1956,), part=PART)
        with self.voiceover("Chapter twelve. Shape constraints."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def isotonic(self):
        rows = [
            cmath(r"\min_{m_1 \le \dots \le m_n}", r"\ ", r"\textstyle\sum_i (y_i - m_i)^2", font_size=32),
            cmath(r"\text{PAVA}", r":", r"\text{pool adjacent blocks using count-weighted means}", font_size=30),
            cmath(r"\text{no tuning}", r":", r"\text{the constraint does the smoothing}", font_size=30),
            cmath(r"\text{solution}", r":", r"\text{the slopes of the greatest convex minorant of the cumulative sums}", font_size=26),
        ]
        rows[1][2].set_color(SPLC)
        whys = [why(r"isotonic regression"), why(r"Ayer et al.\ (1955); \ Part 21's PAVA"), why(r"a step function, \ data-driven steps"),
                why(r"Barlow, \ Bartholomew, \ Bremner \& Brunk (1972)")]
        with self.voiceover(
            "<bookmark mark='a'/> Sometimes all we know is the shape: a dose-response curve rises, a hazard falls. "
            "Then fit the best monotone sequence: isotonic regression. <bookmark mark='b'/> Part 21's "
            "pool-adjacent-violators algorithm solves it exactly: whenever adjacent fitted blocks violate the order, "
            "pool them using their sample-count weighted average. <bookmark mark='c'/> There is no bandwidth and no "
            "lambda: the constraint alone does the smoothing. <bookmark mark='d'/> Geometrically, the solution is the"
            " slope of the greatest convex minorant of the cumulative sums, the picture behind its theory."
        ) as vo:
            intro=label('An order constraint pools adjacent incompatible fitted blocks',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pava_picture(self):
        d = load("shape")
        x, mu, y, iso = (np.asarray(d[k]) for k in ("x", "mu", "y", "iso"))
        A = axes([0, 1], [-0.4, 1.4], x_length=7.4, y_length=4.4, xlabel=r"dose", ylabel=r"response", xticks=[0, 0.5, 1],
                 yticks=[0, 0.5, 1], center=[-2.0, 0.3, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.05, color=WHITE, fill_opacity=0.8) for a, b in zip(x, y)])
        truth = curve(ax, x, mu, TRUE, 3)
        st = VMobject(stroke_color=SPLC, stroke_width=4)
        pp = []
        for i in range(len(x)):
            x0 = x[i] - (x[1] - x[0]) / 2 if i else x[0]
            x1 = x[i] + (x[1] - x[0]) / 2 if i < len(x) - 1 else x[-1]
            pp += [ax.c2p(x0, iso[i]), ax.c2p(x1, iso[i])]
        st.set_points_as_corners(pp)
        rows = fit_rows(VGroup(
            label(r"60 noisy readings of a rising curve", font_size=22),
            label(r"gold: \ the truth", font_size=22, color=TRUE),
            label(rf"green: \ isotonic fit, \ {d['n_blocks']} steps", font_size=22, color=SPLC),
            label(r"flat where the data dither, \ steep where they climb", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Sixty noisy readings of a rising curve. <bookmark mark='b'/> The truth in gold. "
            "<bookmark mark='c'/> The isotonic fit is a staircase of eighteen steps, <bookmark mark='d'/> flat where the data "
            "dither and steep where they climb. Its steps are chosen by the data, as wavelets chose their coefficients."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(pts))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(st), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def grenander_idea(self):
        rows = [
            cmath(r"f", r":", r"\text{non-increasing on } [0, \infty)", font_size=30),
            cmath(r"\hat f_n", r"=", r"\text{the left slope of the least concave majorant of } F_n", font_size=28),
            cmath(r"\text{also}", r":", r"\text{the maximum likelihood estimate over decreasing densities}", font_size=28),
            cmath(r"n^{1/3}(\hat f_n(x) - f(x))", r"\Rightarrow", r"|\tfrac12 f(x) f'(x)|^{1/3} \cdot 2\,\mathbb Z", font_size=28),
        ]
        rows[3][2].set_color(SPLC)
        whys = [why(r"waiting times, \ survival, \ sizes"), why(r"Grenander (1956)"), why(r"no bandwidth: \ the constraint regularizes"),
                why(r"interior $x$, $f(x)>0$, $f'(x)<0$; \ Chernoff limit")]
        with self.voiceover(
            "<bookmark mark='a'/> For densities: suppose only that f is non-increasing, as for many waiting times. "
            "<bookmark mark='b'/> Ulf Grenander's estimator of 1956 is the slope of the least concave majorant of the"
            " empirical distribution function: the tightest concave curve lying above it. <bookmark mark='c'/> It is "
            "also the maximum likelihood estimate among all decreasing densities, and needs no bandwidth. <bookmark "
            "mark='d'/> At a positive interior density with strictly negative derivative and suitable regularity, its"
            " error has cube-root rate and a limit found by B. L. S. Prakasa Rao: a scaled Chernoff distribution, the"
            " location of the maximum of Brownian motion minus a parabola."
        ) as vo:
            intro=label('A concave CDF majorant yields the decreasing-density likelihood fit',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def grenander_picture(self):
        d = load("shape")
        t, g, z = np.asarray(d["gren_t"]), np.asarray(d["gren"]), np.asarray(d["z"])
        A = axes([0, 4], [0, 1.6], x_length=7.4, y_length=4.4, xlabel=r"$x$", ylabel=r"density", xticks=[0, 1, 2, 3, 4],
                 yticks=[0, 0.5, 1, 1.5], center=[-2.0, 0.3, 0])
        ax = A.ax
        truth = curve(ax, t, np.exp(-t), TRUE, 3)
        knots=np.asarray(d["gren_knots"]); heights=np.asarray(d["gren_density"])
        gs=clip_curve(ax,np.repeat(knots,2)[1:-1],np.repeat(heights,2),SPLC,3.5)
        rows = fit_rows(VGroup(
            label(r"200 draws from an exponential", font_size=22),
            label(r"gold: \ $e^{-x}$", font_size=22, color=TRUE),
            label(r"green: \ Grenander estimate; view cropped above 1.6", font_size=22, color=SPLC),
            label(r"a decreasing staircase; \ too high at 0", font_size=22, color=GREY_A),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two hundred exponential waiting times. <bookmark mark='b'/> The true density in gold. "
            "<bookmark mark='c'/> Grenander's estimate, a decreasing staircase that follows it closely in the middle. "
            "<bookmark mark='d'/> At zero it overshoots, a known inconsistency at the boundary, where the majorant's first "
            "slope can be enormous."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(rug(ax, z[z < 4])))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(gs), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def rate(self):
        d = load("shape")
        r = d["rates"]
        hdr = [r"\textbf{$n$}", r"\textbf{Grenander SD at $x = 1$}", r"\textbf{$\times\, n^{1/3}$}", r"\textbf{kernel SD}", r"\textbf{$\times\, n^{2/5}$}"]
        body = [[f"{int(k):,}", f"{v['gren_sd']:.4f}", f"{v['gren_scaled']:.3f}", f"{v['kde_sd']:.4f}", f"{v['kde_scaled']:.3f}"]
                for k, v in r.items()]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.8, row_buff=0.32, colors=[GREY_A] + [None] * 3)
        for row in tb[1:]:
            row[2].set_color(SPLC)
            row[4].set_color(KDEC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"Chernoff's limit for the Grenander column: \ {d['chernoff_sd']:.2f}", font_size=22, color=SPLC),
            label(r"monotonicity alone buys the cube-root rate; \ two derivatives buy $n^{-2/5}$", font_size=22, color=PATH),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The rates, by simulation at x equals one. The Grenander estimate's standard deviation, "
            "multiplied by n to the one third, settles near point four, close to the Chernoff limit of point four two. "
            "<bookmark mark='b'/> A kernel estimate's, multiplied by n to the two fifths, settles too, near point two eight. "
            "Monotonicity alone buys the cube-root rate, the same as one derivative would; assuming two derivatives buys n to "
            "the minus two fifths. Each assumption about shape or smoothness has an exchange rate in sample size."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(VGroup(*x[:3])) for x in tb[1:]], lag_ratio=0.3), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*x[3:])) for x in tb[1:]], lag_ratio=0.3), FadeIn(foot[1]))
        self.wait(1.0)
        self.clear_scene()

    def more(self):
        rows = fit_rows(VGroup(
            label(r"log-concave densities: \ an MLE with no tuning \ (Walther 2002; \ Cule, Samworth \& Stewart 2010)", font_size=24, color=SPLC),
            label(r"convex regression; \ unimodal densities", font_size=24, color=KDEC),
            label(r"monotone hazards in survival \ (Part 40)", font_size=24, color=PATH),
            label(r"constraints adapt: \ near-parametric rates when the truth is simple", font_size=24, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The idea has grown: Log-concave densities include normals and gamma laws with shape"
            " at least one. Their MLE exists under a full-dimensional convex-hull condition, with sample size "
            "sufficient for the dimension. <bookmark mark='b'/> Convex regression and unimodal density estimation are"
            " other shape problems, but constraints do not by themselves guarantee that an unrestricted likelihood "
            "maximizer exists. <bookmark mark='c'/> Monotone hazards return in survival analysis, Part 40. <bookmark "
            "mark='d'/> And shape-constrained estimators adapt: some procedures attain near-parametric risk bounds "
            "for suitable simple piecewise truths, with the dimension, loss and model class specified."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
