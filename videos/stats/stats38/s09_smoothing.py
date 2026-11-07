from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Smoothing(VoiceoverScene):
    def construct(self):
        self.card()
        self.rts_()
        self.missing()
        self.likelihood()
        self.em()
        self.structural()
        self.apollo()

    def card(self):
        card = chapter_card(8, r"Smoothing and learning", r"Using the future, \ and estimating the noise", lit=(1965, 1982), part=PART)
        with self.voiceover("Chapter eight. Smoothing, and learning the model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def rts_(self):
        rows = [
            cmath(r"\text{filter}", r":", r"p(x_t \mid y_{1:t}) \ \text{(forward)}", font_size=30),
            cmath(r"\text{smoother}", r":", r"p(x_t \mid y_{1:n}) \ \text{(then backward)}", font_size=30),
            cmath(r"m_t^s", r"=", r"m_t + J_t (m_{t+1}^s - m_{t+1|t}), \quad J_t = P_t F^\top P_{t+1|t}^{-1}", font_size=28),
            cmath(r"P_t^s", r"=", r"P_t + J_t (P_{t+1}^s - P_{t+1|t}) J_t^\top", font_size=28),
        ]
        rows[2][-1].set_color(BANDC)
        whys = [why(r"what is known by time $t$"), why(r"what is known in the end"), why(r"Rauch, \ Tung \& Striebel (1965)"),
                why(r"never wider than the filter")]
        with self.voiceover(
            "<bookmark mark='a'/> The filter answers a real-time question: given everything up to now, where is the state? "
            "<bookmark mark='b'/> Afterwards we can ask a better one: given all the data, where was it? <bookmark mark='c'/> "
            "Herbert Rauch, Frank Tung and Charlotte Striebel's smoother of 1965 runs the filter forward, then a second pass "
            "backward, correcting each filtered mean by what the next smoothed value turned out to be. <bookmark mark='d'/> "
            "The smoothed variances are never larger than the filtered ones, because more data never hurts a Gaussian."
        ) as vo:
            intro=label('Smoothing conditions on the full observation record',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def missing(self):
        d = load("kalman")
        yrs, ym = np.asarray(d["years"], float), np.asarray(d["miss_y"], float)
        y = np.asarray(d["y"], float)
        s, ss = np.asarray(d["miss_smooth"], float), np.asarray(d["miss_sd"], float)
        A = axes([1870, 1971], [400, 1450], x_length=8.4, y_length=4.2, xlabel=r"year", ylabel=r"flow ($10^8$ m$^3$)",
                 xticks=[1880, 1900, 1920, 1940, 1960], yticks=[500, 1000], xfmt=lambda v: f"{v:.0f}", center=[-1.4, 0.3, 0])
        ax = A.ax
        ok = np.isfinite(ym)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=OBSC) for a, b in zip(yrs[ok], ym[ok])])
        hidden = VGroup(*[Dot(ax.c2p(a, b), radius=0.04, color=GREY_D) for a, b in zip(yrs[~ok], y[~ok])])
        b = band(ax, yrs, s - 1.645 * ss, s + 1.645 * ss, BANDC, 0.2)
        c = polyline(ax, yrs, s, BANDC, 3)
        side = fit_rows(VGroup(
            label(r"hide 1891--1910 and 1931--1950; variances fitted to full record", font_size=22, color=GREY_A),
            label(r"the smoother interpolates the level across the gaps", font_size=22, color=BANDC),
            label(r"and its band widens in the middle of each gap", font_size=22, color=TAUC),
            label(r"grey: \ the deleted flows", font_size=22, color=GREY_D),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Durbin and Koopman's demonstration: hide two twenty-year stretches of the Nile's "
            "record. This illustration holds the noise variances at estimates from the complete record, so it is not "
            "an honest missing-data forecasting benchmark. <bookmark mark='b'/> The filter simply predicts through "
            "them, and the smoother then interpolates the level across each gap, using the years on both sides. "
            "<bookmark mark='c'/> Its band widens towards the middle of each gap, where the nearest data are furthest"
            " away, and narrows again at the edges. <bookmark mark='d'/> The deleted flows, in grey, scatter around "
            "the interpolated level as the noise variance says they should."
        ) as vo:
            self.add(nile_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), Create(c), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(hidden), FadeIn(side[3]))
        self.clear_scene()

    def likelihood(self):
        rows = [
            cmath(r"p(y_{1:n})", r"=", r"\textstyle\prod_t p(y_t \mid y_{1:t-1}) = \prod_t N(v_t;\, 0,\, S_t)", font_size=30),
            cmath(r"\log L(\theta)", r"=", r"-\tfrac12 \textstyle\sum_t \left(\log|2\pi S_t| + v_t^\top S_t^{-1} v_t\right)", font_size=30),
            cmath(r"\text{maximize}", r":", r"\text{over } Q, R \text{ (and } F, H\text{): \ one filter pass per evaluation}", font_size=28),
            cmath(r"\text{or EM}", r":", r"\text{E: smooth; \ M: the variances in closed form}", font_size=30),
        ]
        rows[1][-1].set_color(STATEC)
        whys = [why(r"the prediction-error decomposition"), why(r"Schweppe (1965)"), why(r"Part 22's likelihood"),
                why(r"Shumway \& Stoffer (1982)")]
        with self.voiceover(
            "<bookmark mark='a'/> Where did the two variances come from? Any joint density factors into one-step-ahead "
            "conditional densities, and for a Gaussian state space each is the density of an innovation. <bookmark "
            "mark='b'/> So the filter computes the likelihood as a by-product, the prediction-error decomposition of Fred "
            "Schweppe in 1965. <bookmark mark='c'/> Maximizing it takes one filter pass per evaluation, the method of Part "
            "twenty-two. <bookmark mark='d'/> Or, as Robert Shumway and David Stoffer showed in 1982, treat the states as "
            "missing data and use the EM algorithm: smooth, then update the variances in closed form."
        ) as vo:
            intro=label('One-step innovations factor the state-space likelihood',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def em(self):
        d = load("em")
        ll = np.asarray(d["ll_path"], float)
        it = np.arange(len(ll))
        A = axes([0, len(ll)], [float(ll.min()) - 0.5, float(ll.max()) + 0.5], x_length=7.6, y_length=4.0, xlabel=r"EM iteration",
                 ylabel=r"log-likelihood", xticks=[0, 100, 200, 300], yticks=[round(float(ll.min())), round(float(ll.max()))],
                 center=[-1.8, 0.2, 0])
        c = polyline(A.ax, it, ll, STATEC, 3)
        top = DashedLine(A.ax.c2p(0, d["ll_mle"]), A.ax.c2p(len(ll), d["ll_mle"]), color=TRUEC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"start: \ $\sigma^2_w$ = 1,000, \ $\sigma^2_v$ = 10,000", font_size=22, color=GREY_A),
            label(r"every iteration raises the likelihood", font_size=22, color=STATEC),
            label(rf"after 300: \ {d['q']:,.0f} and {d['r']:,.0f}", font_size=22, color=BANDC),
            label(rf"the direct MLE: \ {d['q_mle']:,.0f} and {d['r_mle']:,.0f} \ (gold)", font_size=22, color=TRUEC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> EM on the Nile, from a poor start. <bookmark mark='b'/> The likelihood rises with "
            "every iteration, as Part twenty-two proved it must: quickly at first, then slowly, EM's usual pace. "
            "<bookmark mark='c'/> After three hundred iterations it has reached the same variances as direct "
            "maximization. <bookmark mark='d'/> This run approaches the direct solution; EM in general can converge "
            "slowly or reach a local stationary point. It extends naturally to models with many parameters, where a "
            "direct search would struggle."
        ) as vo:
            self.add(nile_tag())
            self.play(FadeIn(A), Create(top), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def apollo(self):
        rows = fit_rows(VGroup(
            label(r"1960: \ K\'alm\'an visits Stanley Schmidt at NASA's Ames Research Center", font_size=26, color=TAUC),
            label(r"Schmidt's team linearizes the filter around the trajectory: \ the extended Kalman filter", font_size=26),
            label(r"Apollo's guidance computer navigated to the Moon with it", font_size=26, color=STATEC),
            label(r"today: \ GPS, \ phones, \ aircraft, \ weather forecasting \ (ensemble filters)", font_size=26, color=BANDC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The filter's first great application came within a year of its publication. Kálmán visited "
            "Stanley Schmidt at NASA's Ames Research Center, which was studying navigation for a voyage to the Moon. "
            "<bookmark mark='b'/> Schmidt's group linearized the equations of motion around the current estimate of the "
            "trajectory, creating the extended Kalman filter of the next chapter. <bookmark mark='c'/> Apollo's onboard "
            "navigation used it. <bookmark mark='d'/> Today descendants of Kálmán's filter run in satellite navigation, every "
            "phone, aircraft, and, as ensemble filters with millions of states, in weather forecasting."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def structural(self):
        rows = fit_rows(VGroup(
            label(r"the state can hold many components: \ level, \ slope, \ seasonal, \ regression effects", font_size=26, color=TAUC),
            label(r"Harvey (1989): \ structural time-series models, \ each component a small random walk", font_size=26, color=STATEC),
            label(r"one filter estimates them all, \ handles gaps, \ and gives the likelihood", font_size=26, color=BANDC),
            label(r"ARIMA models are state space models too: \ one framework for chapters 1 to 9", font_size=26, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The state can hold many components at once: a level, a slope, a seasonal pattern, the "
            "effects of regressors or interventions. <bookmark mark='b'/> Andrew Harvey's structural time-series models of "
            "1989 make each a small random walk, so that trends and seasons can evolve. <bookmark mark='c'/> One Kalman filter "
            "estimates them all together, handles missing observations, and delivers the likelihood. <bookmark mark='d'/> "
            "Every ARIMA model of Part seventeen can be written in state-space form too, so the state space is one framework "
            "for almost everything in this part."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
