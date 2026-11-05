from __future__ import annotations

import numpy as np

from videos.stats.stats25.common import *  # noqa: F403


class Growth(VoiceoverScene):
    def construct(self):
        self.card()
        self.spaghetti()
        self.model()
        self.fits()
        self.blups()
        self.covariance()

    def card(self):
        card = chapter_card(7, r"Longitudinal data", r"Each child its own line", lit=(1982,), part=PART)
        with self.voiceover("Chapter seven. Longitudinal data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def axes_(self):
        return axes([3, 13], [70, 160], x_length=7.4, y_length=4.6, xlabel=r"age", ylabel=r"height, \ cm",
                    xticks=[4, 6, 8, 10, 12], yticks=[80, 100, 120, 140], center=[-2.0, 0.3, 0])

    def spaghetti(self):
        d = load("growth")
        age, y, grp = np.asarray(d["age"]), np.asarray(d["y"]), np.asarray(d["groups"])
        A = self.axes_()
        ax = A.ax
        lines = VGroup(*[polyline(ax, age[grp == k], y[grp == k], GREY_B, 1.5, 0.7) for k in range(60)])
        rows = fit_rows(VGroup(
            label(r"60 children, \ measured at 4, 6, 8, 10, 12", font_size=22),
            label(r"each line: \ one child", font_size=22, color=GREY_B),
            label(r"different starts, \ different speeds", font_size=22, color=GREY_A),
            label(r"a seeded simulation", font_size=20, color=GREY_B),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Repeated measurements of the same people over time are clusters too. Sixty children, "
            "each measured at ages four, six, eight, ten and twelve. <bookmark mark='b'/> Each line is one child. "
            "<bookmark mark='c'/> They start at different heights and grow at different speeds, and the five measurements "
            "of one child are far from independent. <bookmark mark='d'/> These children are a seeded "
            "simulation, so we know the truth the model should recover."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.03), FadeIn(rows[1]), run_time=2.5)
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def model(self):
        rows = [
            cmath(r"y_{it}", r"=", r"(\beta_0 + b_{0i}) + (\beta_1 + b_{1i})(t - 8) + \varepsilon_{it}", font_size=30),
            cmath(r"(b_{0i}, b_{1i})", r"\sim", r"N(0, G), \ \ G = \begin{pmatrix} \tau_0^2 & \tau_{01} \\ \tau_{01} & \tau_1^2 \end{pmatrix}", font_size=28),
            cmath(r"\mathrm{Var}\,y_{it}", r"=", r"\tau_0^2 + 2\tau_{01}(t - 8) + \tau_1^2 (t - 8)^2 + \sigma^2", font_size=28),
            cmath(r"\text{centring}", r":", r"\text{age 8 makes } \tau_{01} \text{ the correlation at the middle}", font_size=28),
        ]
        rows[0][2].set_color(SHRUNK)
        whys = [why(r"random intercepts and slopes: \ Laird \& Ware"), why(r"intercepts and slopes may correlate"),
                why(r"the spread grows away from the centre"), why(r"choose the origin with care")]
        with self.voiceover(
            "<bookmark mark='a'/> The natural model gives each child a random intercept and a random slope: their own height "
            "at age eight, and their own growth rate. <bookmark mark='b'/> The two random effects have a covariance matrix "
            "G, which allows tall children to grow faster or slower. <bookmark mark='c'/> The implied variance of a height "
            "changes with age, smallest near the centre and growing away from it, a fan of lines. <bookmark mark='d'/> "
            "Centring age at eight makes the intercept the height at eight; with age uncentred, the intercept would be a "
            "height at birth, far outside the data, and its correlation with the slope would be an artefact."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def fits(self):
        d = load("growth")
        ri, rs, t = d["ri"], d["rs"], d["truth"]
        hdr = [r"\textbf{model}", r"\textbf{growth, cm/yr}", r"\textbf{SE}", r"\textbf{SD intercepts}", r"\textbf{SD slopes}", r"\textbf{log lik}"]
        body = [[r"random intercept", f"{ri['beta'][1]:.2f}", f"{ri['se'][1]:.3f}", f"{np.sqrt(ri['G'][0][0]):.1f}", r"---", f"{ri['ll']:.1f}"],
                [r"+ random slope", f"{rs['beta'][1]:.2f}", f"{rs['se'][1]:.3f}", f"{np.sqrt(rs['G'][0][0]):.1f}", f"{np.sqrt(rs['G'][1][1]):.2f}", f"{rs['ll']:.1f}"],
                [r"the simulation's truth", f"{t['slope']:.2f}", r"", f"{t['int_sd']:.1f}", f"{t['slope_sd']:.2f}", r""]]
        tb = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.3, colors=[GREY_A, RAW, SHRUNK, TRUE])
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(rf"LR $= {d['lr']:.0f}$: \ slopes do vary \ (on the boundary again: \ a mixture of $\chi^2_1$ and $\chi^2_2$)", font_size=22),
            label(r"with random slopes, \ the growth rate's SE nearly doubles", font_size=22, color=RES),
        ), 12.0, 0.25, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two fits. <bookmark mark='b'/> With only random intercepts, children grow five point six "
            "seven centimetres a year with a standard error of point oh four five. <bookmark mark='c'/> Adding random slopes "
            "leaves the estimate the same but nearly doubles the standard error to point oh eight: the intercept-only model "
            "treated sixty children's slopes as if they were all the same, and claimed precision it didn't have. "
            "<bookmark mark='d'/> The likelihood ratio, a hundred and forty-nine, leaves no doubt that slopes vary, and the "
            "estimated spreads match the simulation's five and a half centimetres and point six centimetres a year."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tb[0]))
            vo.wait_until("b")
            self.play(FadeIn(tb[1]))
            vo.wait_until("c")
            self.play(FadeIn(tb[2]), FadeIn(foot[1]))
            vo.wait_until("d")
            self.play(FadeIn(tb[3]), FadeIn(foot[0]))
        self.clear_scene()

    def blups(self):
        d = load("growth")
        age, y, grp = np.asarray(d["age"]), np.asarray(d["y"]), np.asarray(d["groups"])
        b = np.asarray(d["rs"]["beta"])
        bl = np.asarray(d["rs"]["blup"])
        A = self.axes_()
        ax = A.ax
        pick = [0, 7, 21, 33, 48]
        cols = [BLUE, RED, TEAL, PATH, SHRUNK]
        dots = VGroup()
        own = VGroup()
        blup = VGroup()
        for k, c in zip(pick, cols):
            m = grp == k
            dots.add(VGroup(*[Dot(ax.c2p(a, v), radius=0.06, color=c) for a, v in zip(age[m], y[m])]))
            co = np.polyfit(age[m] - 8, y[m], 1)
            own.add(DashedLine(ax.c2p(3.5, co[1] + co[0] * (-4.5)), ax.c2p(12.5, co[1] + co[0] * 4.5), color=c, stroke_width=2))
            i0, s0 = b[0] + bl[k][0], b[1] + bl[k][1]
            blup.add(Line(ax.c2p(3.5, i0 + s0 * (-4.5)), ax.c2p(12.5, i0 + s0 * 4.5), color=c, stroke_width=3.5))
        mean = Line(ax.c2p(3.5, b[0] - 4.5 * b[1]), ax.c2p(12.5, b[0] + 4.5 * b[1]), color=WHITE, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"five children", font_size=22),
            label(r"dashed: \ each child's own line", font_size=22, color=GREY_A),
            label(r"solid: \ the BLUP line", font_size=22),
            label(r"white: \ the average child", font_size=22),
            label(r"five points each: \ little shrinkage", font_size=22, color=GREY_A),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> For individual children, the model's predictions are BLUP lines. Five children: "
            "<bookmark mark='b'/> dashed, each child's own least squares line, <bookmark mark='c'/> solid, their BLUP lines, "
            "<bookmark mark='d'/> and in white the average child. <bookmark mark='e'/> With five accurate measurements per "
            "child the BLUPs barely differ from each child's own fit. With two noisy measurements per child, as in many real "
            "studies, the BLUP lines would be pulled much more towards the average, and their slopes far more trustworthy "
            "than a two-point line."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.2), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(o) for o in own], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(o) for o in blup], lag_ratio=0.2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(mean), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def covariance(self):
        rows = [
            cmath(r"\text{compound symmetry}", r":", r"\text{one correlation for any two times}", font_size=30),
            cmath(r"\text{AR(1)}", r":", r"\rho^{|t - s|}: \ \text{closer in time, \ more alike}", font_size=30),
            cmath(r"\text{unstructured}", r":", r"\text{every variance and covariance free}", font_size=30),
            cmath(r"\text{missing visits}", r":", r"\text{fine if MAR: \ the likelihood uses what is there}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"the random intercept's implied pattern"), why(r"Part 17's autoregression, \ within a person"),
                why(r"$T(T + 1)/2$ parameters"), why(r"Part 41; \ unlike complete-case analysis")]
        with self.voiceover(
            "<bookmark mark='a'/> Random effects are one way to model the covariance of repeated measures. A random intercept "
            "alone implies compound symmetry, one correlation between any two times. <bookmark mark='b'/> An autoregressive "
            "structure, Part 17's, makes nearby times more alike than distant ones. <bookmark mark='c'/> An unstructured "
            "covariance lets every variance and covariance be free, which is feasible when there are few time points. "
            "<bookmark mark='d'/> And a great practical virtue: children who miss a visit still contribute everything they "
            "have, and the likelihood is valid if the missingness depends only on what was observed, Part 41's missing at "
            "random."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
