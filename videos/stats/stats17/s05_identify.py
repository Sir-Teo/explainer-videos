from __future__ import annotations

import numpy as np

from videos.stats.stats17.common import *  # noqa: F403


def corr_panel(r, band, center, color, title, lags=20, theory=None, width=5.4, height=1.8, pacf=False):
    rr = np.r_[1.0, np.asarray(r)[:lags]] if pacf else np.asarray(r)[: lags + 1]
    A = axes([0, lags + 1], [-1, 1], x_length=width, y_length=height, yticks=[-1, 0, 1], font_size=14, center=list(center))
    cg = Correlogram(A.ax, rr, band=band, theory=theory, color=color, width=0.55)
    t = label(title, font_size=20, color=color).next_to(A, UP, buff=0.05)
    return VGroup(A, cg, t)


class Identify(VoiceoverScene):
    def construct(self):
        self.card()
        self.pacf_def()
        self.signatures()
        self.simulated()
        self.sunspots()
        self.cycle()
        self.differencing()

    def card(self):
        card = chapter_card(4, r"Identification", r"Reading a model's fingerprints", lit=(1970,), part=PART)
        with self.voiceover("Chapter four. Identification."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pacf_def(self):
        rows = [
            cmath(r"\text{best AR}(h)", r":", r"\hat X_t = \phi_{h1} X_{t-1} + \cdots + \phi_{hh} X_{t-h}", font_size=30),
            cmath(r"\alpha(h)", r"=", r"\phi_{hh}", font_size=32),
            cmath(r"\ ", r"=", r"\mathrm{corr}(r_t, r_{t-h})\quad\text{linear residuals after intervening lags}", font_size=30),
            cmath(r"\text{AR}(p)", r":", r"\alpha(h) = 0 \text{ for } h > p", font_size=32),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the linear predictor from $h$ lags"), why(r"its last coefficient: \ the partial autocorrelation"),
                why(r"linear partial correlation; \ conditional correlation under Gaussianity"), why(r"an AR($p$) needs nothing beyond lag $p$")]
        intro = label('Partial autocorrelation removes the intervening linear effects', font_size=36)
        with self.voiceover(
            "The autocorrelation function has a partner. <bookmark mark='a'/> Fit the best linear predictor of the series from "
            "its last h values. <bookmark mark='b'/> Its last coefficient, phi h h, is the partial autocorrelation at lag h. "
            "<bookmark mark='c'/> It's the correlation between the series and its value h steps back, after removing what the "
            "observations in between explain, much as Part 12's partial regression coefficients did. The Durbin–Levinson "
            "recursion computes them all from the autocorrelations. <bookmark mark='d'/> For an AR of order p, once the p "
            "previous values are known, older ones add nothing, so the partial autocorrelation is exactly zero beyond lag p."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def signatures(self):
        tab = table_rows([
            [r"model", r"ACF", r"PACF"],
            [r"AR($p$)", r"tails off", r"cuts off after lag $p$"],
            [r"MA($q$)", r"cuts off after lag $q$", r"tails off"],
            [r"ARMA($p, q$)", r"tails off", r"tails off"],
            [r"white noise", r"zero", r"zero"],
        ], font_size=30, colors=[GREY_B, SERIES, RES, OBS, GREY_A]).move_to([0, 0.6, 0])
        foot = label(r"a duality: \ an AR is an MA($\infty$), \ an invertible MA is an AR($\infty$)", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.9)
        intro = label('Minimal causal and invertible models have distinct signatures', font_size=36).move_to([0, 3.2, 0])
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "For minimal causal, invertible ARMA models with no cancelling factors, this gives theoretical fingerprints. <bookmark mark='a'/> An autoregression of order p: its autocorrelations "
            "tail off gradually, and its partial autocorrelations cut off sharply after lag p. <bookmark mark='b'/> A moving "
            "average of order q: the reverse. Its autocorrelations cut off after lag q, since shocks more than q steps apart "
            "share nothing, and its partial autocorrelations tail off. <bookmark mark='c'/> A mixed model: both tail off. "
            "<bookmark mark='d'/> White noise: both are zero. <bookmark mark='e'/> The symmetry isn't an accident. An "
            "autoregression is an infinite moving average, and an invertible moving average is an infinite autoregression."
        ) as vo:
            self.play(FadeIn(intro))
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def simulated(self):
        d = load("identify")
        b = d["band"]
        p1 = corr_panel(d["acf_ar"], b, [-3.4, 1.7, 0], SERIES, r"AR(2): \ ACF")
        p2 = corr_panel(d["pacf_ar"], b, [3.4, 1.7, 0], SERIES, r"AR(2): \ PACF", pacf=True)
        p3 = corr_panel(d["acf_ma"], b, [-3.4, -1.6, 0], RES, r"MA(2): \ ACF")
        p4 = corr_panel(d["pacf_ma"], b, [3.4, -1.6, 0], RES, r"MA(2): \ PACF", pacf=True)
        tag = simulated_tag(r"300 steps each", corner=DR)

        def show(p):
            return AnimationGroup(FadeIn(p[0]), FadeIn(p[2]), FadeIn(p[1].zero), FadeIn(p[1].bands),
                                  LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p[1].bars], lag_ratio=0.04))

        intro = label('Compare the theoretical signatures with finite samples', font_size=36)
        with self.voiceover(
            "Two simulated series of three hundred, and their four correlograms. <bookmark mark='a'/> An AR two: the "
            "autocorrelations swing and fade, a damped wave, <bookmark mark='b'/> while the partial autocorrelations are large "
            "at lags one and two, point seven nine and minus point six five, then drop inside the bands and stay there. "
            "<bookmark mark='c'/> An MA two: two large autocorrelations, and then nothing beyond the bands, apart from one "
            "bar at lag three that only just crosses, as one in twenty will. <bookmark mark='d'/> Its partial "
            "autocorrelations don't stop cleanly: in theory they decay forever, and here they leave small values of both signs. On real data the cut-offs are rarely this clean, but the signatures "
            "usually narrow the choice to a few candidates."
        ) as vo:
            self.play(FadeIn(intro))
            self.add(tag)
            for m_, p in zip("abcd", (p1, p2, p3, p4)):
                vo.wait_until(m_)
                if m_ == "a":
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(show(p))
        self.clear_scene()

    def sunspots(self):
        d = load("sunspot")
        b = d["band"]
        p1 = corr_panel(d["acf"], b, [-3.4, 0.6, 0], OBS, r"sunspots: \ ACF", lags=25, height=3.0, width=5.8)
        p2 = corr_panel(d["pacf"], b, [3.4, 0.6, 0], OBS, r"sunspots: \ PACF", lags=15, height=3.0, width=5.8, pacf=True)
        rows = fit_rows(VGroup(
            label(r"ACF: \ a damped wave, \ period about 11: \ AR with complex roots", font_size=22),
            label(r"PACF: \ big at lags 1 and 2, \ then small; \ a few bars near the band at 6--8", font_size=22, color=OBS),
            label(r"candidates: \ AR(2), \ or a longer AR to catch the regularity", font_size=22, color=HIT),
        ), 12.4, 0.25, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The sunspots. The autocorrelation function is a damped wave with a period near eleven: the "
            "signature of an autoregression with complex roots. <bookmark mark='b'/> The partial autocorrelations are large at "
            "lags one and two, point eight one and minus point six four, then small, with a few bars near the edge of the "
            "bands around lags six to eight. <bookmark mark='c'/> So the candidates are Yule's AR two, or a longer "
            "autoregression that also catches those later lags, and with them the cycle's regularity. Choosing between them "
            "is the next chapter's job."
        ) as vo:
            self.play(FadeIn(p1[0]), FadeIn(p1[2]), FadeIn(p1[1].zero), FadeIn(p1[1].bands), FadeIn(p2[0]), FadeIn(p2[2]),
                      FadeIn(p2[1].zero), FadeIn(p2[1].bands))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p1[1].bars], lag_ratio=0.03), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p2[1].bars], lag_ratio=0.04), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def cycle(self):
        names = [(r"identify", r"plots, \ ACF, \ PACF", SERIES), (r"estimate", r"likelihood, \ least squares", MODEL),
                 (r"check", r"residuals: \ white noise?", RES), (r"forecast", r"with intervals", OBS)]
        pos = [np.array([-4.5, 0.4, 0]), np.array([-1.5, 0.4, 0]), np.array([1.5, 0.4, 0]), np.array([4.5, 0.4, 0])]
        boxes = VGroup()
        for (t, sub, col), p in zip(names, pos):
            tt = label(t, font_size=28, color=col)
            ss = label(sub, font_size=18, color=GREY_A)
            inner = VGroup(tt, ss).arrange(DOWN, buff=0.12)
            box = RoundedRectangle(width=2.5, height=1.4, corner_radius=0.15, stroke_color=col, stroke_width=2).move_to(p)
            inner.move_to(p)
            boxes.add(VGroup(box, inner))
        arrows = VGroup(*[Arrow(boxes[k].get_right(), boxes[k + 1].get_left(), buff=0.08, color=GREY_B) for k in range(3)])
        back = CurvedArrow(boxes[2].get_bottom() + DOWN * 0.05, boxes[0].get_bottom() + DOWN * 0.05, angle=-TAU / 5, color=RES)
        bl = label(r"if the residuals aren't white noise, \ try again", font_size=20, color=RES).move_to([-1.5, -2.0, 0])
        hist = historical_tag(r"Box \& Jenkins, \ \emph{Time Series Analysis: Forecasting and Control} (1970)", corner=DR)
        head = label(r"the Box--Jenkins cycle", font_size=34).to_edge(UP, buff=0.8)
        with self.voiceover(
            "<bookmark mark='a'/> In 1970 George Box and Gwilym Jenkins turned this into a method, in a book that made ARMA "
            "models standard practice. <bookmark mark='b'/> Identify a few candidate models from plots and correlograms. "
            "<bookmark mark='c'/> Estimate them. <bookmark mark='d'/> Check the residuals: if the model has captured the "
            "dependence, what's left should be white noise. <bookmark mark='e'/> If it isn't, go back and try again. "
            "<bookmark mark='f'/> Only then forecast. It's an iterative, modest method, and it embodies Box's famous remark "
            "that all models are wrong, but some are useful."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hist))
            vo.wait_until("a")
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(boxes[k]), *([GrowArrow(arrows[k - 1])] if k else []))
            vo.wait_until("e")
            self.play(Create(back), FadeIn(bl))
            vo.wait_until("f")
            self.play(GrowArrow(arrows[2]), FadeIn(boxes[3]))
        self.clear_scene()

    def differencing(self):
        rows = [
            cmath(r"\nabla X_t", r"=", r"X_t - X_{t-1}", font_size=34),
            cmath(r"\text{random walk}", r":", r"\nabla X_t = e_t,\ \ \text{white noise}", font_size=32),
            cmath(r"\text{ARIMA}(p, d, q)", r":", r"\nabla^d X_t \text{ is ARMA}(p, q)", font_size=32),
            cmath(r"\text{Yule's series}", r":", r"\text{differences correlate } 0.02", font_size=32),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"the first difference"), why(r"differencing removes a unit root"),
                why(r"Box \& Jenkins's ``integrated'' models"), why(r"the hook, \ revisited")]
        intro = label('Differencing can remove a stochastic trend', font_size=36)
        with self.voiceover(
            "What about series that wander, like the random walk, or trend? Box and Jenkins's answer was to difference them. "
            "<bookmark mark='a'/> The first difference is the change from one period to the next. <bookmark mark='b'/> A "
            "random walk's differences are just its shocks: white noise. <bookmark mark='c'/> If the d-th differences of a "
            "series are a stationary ARMA, the series is called ARIMA, the I for integrated. <bookmark mark='d'/> That's what we "
            "did to Yule's marriages and deaths in the hook: their changes had little contemporaneous linear correlation. Whether a series "
            "really needs differencing is a question for a test, and Part 38 has it."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()
