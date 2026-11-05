from __future__ import annotations

import numpy as np

from explainer.stats.kit import ts as T
from videos.stats.stats17.common import *  # noqa: F403


class Cycles(VoiceoverScene):
    def construct(self):
        self.card()
        self.complex_roots()
        self.ar2_path()
        self.slutsky()
        self.sunspots()
        self.acf_compare()
        self.lesson()

    def card(self):
        card = chapter_card(3, r"Pseudo-cycles", r"Rhythm without a clock", part=PART)
        with self.voiceover("Chapter three. Pseudo-cycles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def complex_roots(self):
        p = T.ar2_period(1.3, -0.6)
        rows = [
            cmath(r"X_t", r"=", r"\phi_1 X_{t-1} + \phi_2 X_{t-2} + e_t,\ \ \phi_1^2 + 4\phi_2 < 0", font_size=30),
            cmath(r"\rho(h)", r"=", r"A\, r^h \cos(\omega h + \delta),\ \ r = \sqrt{-\phi_2}", font_size=30),
            cmath(r"\cos\omega", r"=", r"\frac{\phi_1}{2\sqrt{-\phi_2}},\ \ \text{period } 2\pi/\omega", font_size=30),
            cmath(r"(1.3,\ -0.6)", r":", rf"r = {np.sqrt(0.6):.3f},\ \ \text{{period}} = {p:.1f}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"complex roots"), why(r"a damped cosine: \ the pendulum's swing"),
                why(r"the frequency from the roots' angle"), why(r"each cycle 22\% smaller, \ about 11 steps long")]
        with self.voiceover(
            "<bookmark mark='a'/> Take an AR two whose polynomial has complex roots. <bookmark mark='b'/> Its autocorrelation "
            "function is a damped cosine: correlations that swing positive and negative while shrinking by a factor r each "
            "step, where r is the square root of minus phi two. It's the free swing of Yule's pendulum. <bookmark mark='c'/> "
            "The frequency comes from the angle of the roots: cos omega equals phi one over twice the square root of minus "
            "phi two. <bookmark mark='d'/> For phi one equal to one point three and phi two minus point six, r is point seven "
            "seven five and the period is ten point nine steps."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ar2_path(self):
        d = load("slutsky")
        x = np.asarray(d["ar2"])
        A = axes([0, 300], [x.min(), x.max()], x_length=11.0, y_length=2.4, xlabel=r"time", center=[0, 1.7, 0])
        ln = series_line(A.ax, np.arange(300), x, SERIES, 1.8)
        B = axes([0, 31], [-1, 1], x_length=7.0, y_length=2.2, xlabel=r"lag", yticks=[-1, 0, 1], center=[-1.6, -1.8, 0], font_size=18)
        cg = Correlogram(B.ax, d["acf_ar2"], band=2 / np.sqrt(300), theory=T.arma_acf([1.3, -0.6], [], 30), color=S.CTRL,
                        hot=S.CTRL)
        rows = fit_rows(VGroup(
            label(r"swells of uneven height and length", font_size=22),
            label(r"the ACF: \ a damped cosine; \ dots: \ the theory", font_size=22, color=S.TRUTH),
            MathTex(rf"\text{{period}} \approx {d['period_ar2']:.1f}", font_size=28, color=OBS),
        ), 4.2, 0.36, [4.6, -1.8, 0])
        tag = simulated_tag(r"AR(2), \ $(1.3, -0.6)$", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Here's three hundred steps of it. There's an unmistakable rhythm: rises and falls, about eleven "
            "steps apart. <bookmark mark='b'/> But no two cycles are alike. Heights vary, lengths vary, and every so often the "
            "rhythm almost disappears before a run of shocks revives it. <bookmark mark='c'/> The sample autocorrelations trace "
            "the damped cosine, close to the theory. <bookmark mark='d'/> These are pseudo-cycles: regular enough to see, "
            "irregular enough that no clock is driving them. A pendulum and some peas are all it takes."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(B), FadeIn(cg.zero), FadeIn(cg.bands), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cg.bars], lag_ratio=0.04),
                      FadeIn(cg.theory), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def slutsky(self):
        d = load("slutsky")
        e, ms = np.asarray(d["e"]), np.asarray(d["msum"])
        A = axes([0, 300], [-3.5, 3.5], x_length=11.0, y_length=1.8, center=[0, 2.0, 0])
        B = axes([0, 300], [ms.min(), ms.max()], x_length=11.0, y_length=2.4, xlabel=r"time", center=[0, -0.9, 0])
        l1 = series_line(A.ax, np.arange(300), e, GREY_B, 1.4)
        l2 = series_line(B.ax, np.arange(300), ms, RES, 2.2)
        ta = label(r"white noise: \ independent shocks", font_size=22, color=GREY_B).next_to(A, UP, buff=0.05).align_to(A, LEFT)
        tb = label(r"the sum of the last 10 shocks", font_size=22, color=RES).next_to(B, UP, buff=0.05).align_to(B, LEFT)
        foot = fit_rows(VGroup(
            label(r"Slutsky (1927): \ ``The summation of random causes as the source of cyclic processes''", font_size=22),
            label(r"smoothing independent noise manufactures waves: \ beware of cycles in averaged data", font_size=22, color=OBS),
        ), 12.4, 0.2, [0, -3.1, 0])
        tag = simulated_tag(r"Slutsky's experiment", corner=UR)
        with self.voiceover(
            "The same year, in Moscow, Eugen Slutsky made a related discovery. <bookmark mark='a'/> Start with pure white "
            "noise: independent shocks, no rhythm at all. <bookmark mark='b'/> Replace each value by the sum of the last ten. "
            "Waves appear: smooth rises and falls with something like a period, which Slutsky compared with the English "
            "business cycle of the nineteenth century, and found an uncomfortable resemblance. <bookmark mark='c'/> His paper "
            "was called The summation of random causes as the source of cyclic processes. <bookmark mark='d'/> The lesson cuts "
            "both ways. Random shocks passed through any averaging mechanism produce cycles, so a cycle in the data doesn't "
            "prove a periodic cause; and smoothing a series yourself can manufacture waves that weren't there."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(ta), Create(l1), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(tb), Create(l2), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def sunspots(self):
        d = load("sunspot")
        yrs, s = np.asarray(d["years"]), np.asarray(d["s"])
        A = axes([1745, 1928], [0, 160], x_length=11.4, y_length=3.4, xlabel=r"year", ylabel=r"yearly sunspot number",
                 xticks=[1750, 1800, 1850, 1900], yticks=[0, 50, 100, 150], center=[0, 0.9, 0])
        ln = series_line(A.ax, yrs, s, OBS, 2.2)
        rows = fit_rows(VGroup(
            label(r"176 years, \ 1749--1924: \ Yule's data", font_size=22),
            MathTex(rf"\hat\phi = ({d['ols'][0]:.3f},\ {d['ols'][1]:.3f}),\ \ \text{{SE}}\ {d['ols_se'][0]:.3f}", font_size=28, color=MODEL),
            MathTex(rf"\text{{period}} = {d['period']:.1f}\ \text{{years}},\ \ r = {np.sqrt(-d['ols'][1]):.2f}", font_size=28, color=OBS),
            label(r"Yule (1927): \ $1.34$ and $-0.65$", font_size=20, color=GREY_A),
        ), 12.0, 0.25, [0, -2.25, 0])
        tag = historical_tag(r"yearly sunspot numbers, \ as statsmodels ships them", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> Now Yule's data: the yearly sunspot numbers from 1749 to 1924, a hundred and seventy-six "
            "years. The famous cycle is there, about eleven years from peak to peak, with peaks of very different heights. "
            "<bookmark mark='b'/> Fitting an AR two by least squares gives coefficients one point three three six and minus "
            "point six five oh, with standard errors near point oh six. <bookmark mark='c'/> The implied period is ten point "
            "six years, and the damping factor point eight one a year. <bookmark mark='d'/> Yule's own estimates were one "
            "point three four and minus point six five: the same answer from the same data, ninety-nine years apart."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(rows[0]), run_time=3.0)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def acf_compare(self):
        d = load("sunspot")
        A = axes([0, 31], [-0.6, 1], x_length=8.4, y_length=4.0, xlabel=r"lag, \ years", ylabel=r"autocorrelation",
                 xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[-0.5, 0, 0.5, 1], center=[-1.6, 0.3, 0])
        cg = Correlogram(A.ax, d["acf"], band=d["band"], theory=T.arma_acf(d["ols"], [], 30), color=S.CTRL, hot=S.CTRL)
        rows = fit_rows(VGroup(
            label(r"bars: \ the sunspots' sample ACF", font_size=22, color=S.CTRL),
            label(r"dots: \ what the AR(2) implies", font_size=22, color=S.TRUTH),
            label(r"the first cycle matches", font_size=22, color=HIT),
            label(r"the data stay correlated at lag 10--11: \ 0.5 vs 0.1", font_size=22, color=RES),
            label(r"the real cycle is more regular than an AR(2) allows", font_size=22, color=RES),
        ), 4.2, 0.36, [4.8, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> How good is the pendulum? Compare the sunspots' sample autocorrelations with those the fitted "
            "AR two implies. <bookmark mark='b'/> The dots are the model. <bookmark mark='c'/> Over the first cycle they agree "
            "closely: the fall to negative correlation around lag five, the return. <bookmark mark='d'/> But the data stay "
            "correlated at about point five a full cycle later, at lags ten and eleven, where the model has almost forgotten: "
            "point one. <bookmark mark='e'/> The real sunspot cycle is more regular than an AR two allows; its pendulum is "
            "damped too quickly. Chapter five will let the data choose a longer memory."
        ) as vo:
            self.play(FadeIn(A), FadeIn(cg.zero), FadeIn(cg.bands))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in cg.bars], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(cg.theory), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"complex roots $\Rightarrow$ damped oscillation in the ACF", font_size=24),
            label(r"random shocks keep it going: \ cycles of varying height and length", font_size=24, color=SERIES),
            label(r"a cycle in the data is not proof of a clock", font_size=24, color=OBS),
            label(r"averaging noise makes waves: \ Slutsky's warning", font_size=24, color=RES),
            label(r"business cycles, \ predator--prey counts, \ sunspots: \ the same picture", font_size=24, color=GREY_A),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: complex roots give a damped oscillation in the autocorrelations, <bookmark mark='b'/> and "
            "random shocks keep it alive, so the cycles vary in height and length. <bookmark mark='c'/> A cycle in the data "
            "doesn't prove a periodic cause, <bookmark mark='d'/> and averaging noise can make one. <bookmark mark='e'/> Yule "
            "and Slutsky's picture, random shocks driving a resonant system, became the standard model of business cycles in "
            "economics, and it fits lynx and hare counts, river flows and sunspots alike."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
