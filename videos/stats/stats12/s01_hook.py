from __future__ import annotations

import numpy as np

from videos.stats.stats12.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.ceres()
        self.orbit()
        self.priority()
        self.objectives()

    def ceres(self):
        tl = timeline(lit=(1801,)).to_edge(UP, buff=0.35)
        hc = history_card(1801, r"Giuseppe Piazzi, \ Palermo, \ 1 January", r"a moving point of light between Mars and Jupiter: \ the "
                          r"first asteroid, \ Ceres. \ He tracks it for six weeks, \ a small arc of its orbit, \ until it is lost in "
                          r"the Sun's glare", color=DATA, width=9.0, font_size=24).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"where will it be when it comes out from behind the Sun? \ The astronomers' predictions disagreed", font_size=24),
            label(r"Carl Friedrich Gauss, \ aged 24, \ fitted an orbit to the noisy positions", font_size=26, color=OBS),
            label(r"31 December 1801: \ Franz von Zach finds Ceres within half a degree of Gauss's prediction", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the first night of the nineteenth century, the astronomer Giuseppe Piazzi, in "
            "Palermo, saw a faint point of light that moved against the stars between the orbits of Mars and Jupiter. It "
            "was Ceres, the first asteroid ever found. He followed it for six weeks, across only a small arc "
            "of its path, until it disappeared into the glare of the Sun. <bookmark mark='b'/> Where would it reappear? "
            "Astronomers made predictions, and they disagreed. <bookmark mark='c'/> A twenty-four-year-old mathematician "
            "in Brunswick, Carl Friedrich Gauss, took Piazzi's few, noisy positions and fitted an orbit to them. "
            "<bookmark mark='d'/> On the last night of 1801, Franz von Zach found Ceres within half a degree of where Gauss "
            "said it would be. Gauss became famous for his orbit calculation. In 1809 he published a systematic treatment of least squares for astronomical observations; the exact role of least squares in the 1801 recovery is historically disputed."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def orbit(self):
        g = np.random.Generator(np.random.PCG64(1801))
        sun = Dot(ORIGIN, radius=0.16, color=S.ACCENT).shift(LEFT * 1.4)
        earth_orbit = Circle(radius=1.1, color=GREY_D, stroke_width=1.5).move_to(sun)
        a, e = 2.77, 0.08
        ts = np.linspace(0, 2 * np.pi, 300)
        r = a * (1 - e * e) / (1 + e * np.cos(ts))
        pts = [sun.get_center() + np.array([r_ * np.cos(t), 0.72 * r_ * np.sin(t), 0]) for r_, t in zip(r, ts)]
        true_orbit = VMobject(stroke_color=GREY_C, stroke_width=1.5).set_points_smoothly(pts)
        obs_t = np.linspace(0.3, 0.42, 12)
        obs = []
        for t in obs_t:
            r_ = a * (1 - e * e) / (1 + e * np.cos(t))
            obs.append(sun.get_center() + np.array([r_ * np.cos(t), 0.72 * r_ * np.sin(t), 0]) + np.r_[g.normal(0, 0.04, 2), 0])
        dots = VGroup(*[Dot(p_, radius=0.05, color=DATA) for p_ in obs])
        pred_t = 2.7
        r_ = a * (1 - e * e) / (1 + e * np.cos(pred_t))
        pred = Dot(sun.get_center() + np.array([r_ * np.cos(pred_t), 0.72 * r_ * np.sin(pred_t), 0]), radius=0.09, color=OBS)
        sl = label(r"Sun", font_size=20, color=S.ACCENT).next_to(sun, DOWN, buff=0.1)
        rows = fit_rows(VGroup(
            label(r"a few noisy points on a short arc", font_size=24, color=DATA),
            label(r"find the orbit that misses them by the least, \ in total squared error", font_size=24, color=FIT),
            label(r"follow it around to where Ceres will be", font_size=24, color=OBS),
        ), 4.8, 0.3, [4.4, -1.6, 0])
        tag = simulated_tag(r"schematic: \ constructed orbit and noisy points", corner=DR)
        with self.voiceover(
            "A constructed orbital illustration, not a reconstruction of Piazzi's records or Gauss's fit. <bookmark mark='a'/> Piazzi's observations were a handful of noisy points on a "
            "short arc of a long orbit. <bookmark mark='b'/> Many orbits pass near those points. Least squares would choose an orbit minimizing total squared residuals under a specified observation model. The curve shown here is constructed to explain extrapolation. <bookmark mark='c'/> Then he followed it "
            "around the Sun, to where Ceres would be months later. A short arc constrains a long orbit only if you use every "
            "observation as well as possible, and squaring the errors turned out to be the way."
        ) as vo:
            self.play(FadeIn(sun), FadeIn(sl), Create(earth_orbit), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(true_orbit), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(pred, scale=2), FadeIn(rows[2]))
        self.clear_scene()

    def priority(self):
        h1 = history_card(1805, r"Adrien-Marie Legendre, \ Paris", r"\emph{Nouvelles m\'ethodes pour la d\'etermination des orbites des "
                          r"com\`etes}: \ an appendix names and publishes ``la m\'ethode des moindres carr\'es''", color=FIT, width=6.0,
                          font_size=22).move_to([-3.3, 0.8, 0])
        h2 = history_card(1809, r"Carl Friedrich Gauss, \ G\"ottingen", r"\emph{Theoria motus}: \ least squares derived from the normal law of "
                          r"errors, \ and the claim to have used it ``since 1795''", color=FIT, width=6.0, font_size=22).move_to([3.3, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"Legendre was furious; \ the priority dispute was never settled", font_size=24, color=GREY_A),
            label(r"Stigler (1981): \ Gauss's claim is plausible, \ but Legendre's was the method the world learned", font_size=22, color=GREY_A),
        ), 12.6, 0.3, [0, -2.2, 0])
        intro = label('Legendre publishes first; Gauss claims earlier use', font_size=36)
        with self.voiceover(
            "And then came one of the great priority disputes in science. <bookmark mark='a'/> In 1805 Adrien-Marie Legendre, "
            "in an appendix to a book on comet orbits, published the method, named it, the method of least squares, and "
            "showed how to use it. <bookmark mark='b'/> In 1809 Gauss published his own account, derived it from the normal "
            "law of errors, which is how the normal curve got its other name, the Gaussian, and remarked that he had used it "
            "since 1795. <bookmark mark='c'/> Legendre was furious. Historians, including Stephen Stigler, think Gauss's "
            "claim is plausible, but it was Legendre's clear account that the world learned from."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(h1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(h2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 12", font_size=34, color=GREY_B), label(r"Least Squares", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the principle, \ the normal equations, \ and why squares", r"least squares as a projection; \ Gauss--Markov, \ proved",
            r"normal theory: \ $t$, \ $F$ as Pythagoras, \ $R^2$; \ ``controlling for'' (Frisch--Waugh--Lovell); \ omitted variables",
            r"interpreting coefficients; \ confidence and prediction bands; \ collinearity",
            r"diagnostics and influence; \ uneven noise and robust SEs; \ the regression fallacy",
        ], color=OBS, font_size=26)
        prereq = note(r"prerequisites: \ Parts 4 and 11").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.ols}; \ the influence probe").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twelve: least squares. <bookmark mark='b'/> We'll derive the method and ask why "
            "squares; see it as a projection, and prove the Gauss–Markov theorem that makes it optimal; build its normal "
            "theory, tests and R squared; make precise what controlling for a variable means, and what leaving one out "
            "does; interpret coefficients, draw bands, and see what collinearity does; then diagnose influence, fix standard "
            "errors when the noise is uneven, and end with the regression fallacy."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
