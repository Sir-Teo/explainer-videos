from __future__ import annotations

import numpy as np

from videos.stats.stats38.common import *  # noqa: F403


class Kalman(VoiceoverScene):
    def construct(self):
        self.card()
        self.conditioning()
        self.ellipses()
        self.equations()
        self.steady()
        self.nile()
        self.drop()

    def card(self):
        card = chapter_card(7, r"State space and the Kalman filter", r"Tracking what cannot be seen", lit=(1960,), part=PART)
        with self.voiceover("Chapter seven. The state space, and the Kalman filter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def conditioning(self):
        rows = [
            cmath(r"x_t", r"=", r"F x_{t-1} + w_t, \quad w_t \sim N(0, Q)", font_size=32),
            cmath(r"y_t", r"=", r"H x_t + v_t, \quad v_t \sim N(0, R)", font_size=32),
            cmath(r"\binom{x}{y}", r"\sim", r"N\!\left(\binom{m}{Hm}, \begin{pmatrix} P & PH^\top \\ HP & HPH^\top + R \end{pmatrix}\right)", font_size=28),
            cmath(r"x \mid y", r"\sim", r"N\big(m + K(y - Hm),\ (I - KH)P\big), \ K = PH^\top(HPH^\top + R)^{-1}", font_size=26),
        ]
        rows[3][-1].set_color(STATEC)
        whys = [why(r"the hidden state evolves"), why(r"we see it through noise"), why(r"jointly Gaussian"),
                why(r"Part 5's conditional normal")]
        with self.voiceover(
            "<bookmark mark='a'/> A state-space model has two equations. The state, which we cannot see, evolves linearly "
            "with Gaussian noise: a position and velocity, a river's underlying level, an economy's trend. <bookmark "
            "mark='b'/> We observe a linear function of it, plus noise. <bookmark mark='c'/> Before each observation, our "
            "belief about the state and the observation we expect are jointly Gaussian, assuming a Gaussian initial state and independent process and measurement noises. <bookmark mark='d'/> So after "
            "observing, the state's conditional distribution is Gaussian too, by the conditional-normal formula of Part "
            "five. The mean moves toward the observation by the gain K times the surprise, and the variance shrinks. That "
            "is the whole of the Kalman filter."
        ) as vo:
            intro=label('Linear Gaussian conditioning updates a hidden-state distribution',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def ellipses(self):
        d = load("kalman")["track"]
        mp, Pp, mf, Pf = (np.asarray(d[k], float) for k in ("mp", "Pp", "mf", "Pf"))
        ys, xs = np.asarray(d["y"], float), np.asarray(d["x"], float)
        A = axes([-3, 10], [-2, 3.5], x_length=9.0, y_length=4.4, xlabel=r"position", ylabel=r"velocity",
                 xticks=[-2, 0, 4, 8], yticks=[-1, 0, 1, 2, 3], center=[-1.2, 0.3, 0])
        K = KalmanEllipses(A.ax, k=2.0)
        side = fit_rows(VGroup(
            label(r"purple: \ predicted", font_size=22, color=SPECC),
            label(r"grey band: \ what the measured position says", font_size=22, color=GREY_A),
            label(r"blue: \ updated", font_size=22, color=STATEC),
            label(r"gold: \ the true state", font_size=22, color=TRUEC),
        ), 3.0, 0.42, [5.4, 0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Watch it as ellipses. A target moves with nearly constant velocity; we measure only its "
            "position, with noise. The state is two-dimensional: position across, velocity up. <bookmark mark='b'/> Each "
            "step, the prediction carries the last ellipse forward. Position moves by the velocity, so the ellipse shears "
            "and grows. <bookmark mark='c'/> The measurement says only where the position is, a vertical band; it says "
            "nothing directly about velocity. <bookmark mark='d'/> The update is the intersection, in the Gaussian sense: an "
            "ellipse narrower in position, and, because the predicted position and velocity were correlated, narrower in "
            "velocity too. Velocity is learned without ever being measured. <bookmark mark='e'/> Step after step, the "
            "ellipses settle into a steady size, tracking the true state in gold."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A), FadeIn(side))
            prev = None
            for t in range(len(ys)):
                pe, ob, up = K.ellipse(mp[t], Pp[t], SPECC), K.observation(ys[t], 1.0, 0, GREY_A), K.ellipse(mf[t], Pf[t], STATEC)
                tr = K.dot(xs[t], TRUEC, 0.07)
                if t == 0:
                    vo.wait_until("b")
                    self.play(FadeIn(pe))
                    vo.wait_until("c")
                    self.play(FadeIn(ob))
                    vo.wait_until("d")
                    self.play(FadeIn(up), FadeIn(tr))
                    vo.wait_until("e")
                else:
                    self.play(FadeIn(pe), FadeIn(ob), run_time=0.6)
                    self.play(FadeIn(up), FadeIn(tr), FadeOut(pe), FadeOut(ob), run_time=0.6)
                if prev is not None:
                    self.play(prev.animate.set_fill(opacity=0.04).set_stroke(opacity=0.3), run_time=0.3)
                if t == 0:
                    self.play(FadeOut(pe), FadeOut(ob), run_time=0.4)
                prev = up
        self.clear_scene()

    def equations(self):
        rows = [
            cmath(r"\text{predict}", r":", r"m_{t|t-1} = F m_{t-1}, \quad P_{t|t-1} = F P_{t-1} F^\top + Q", font_size=28),
            cmath(r"\text{innovation}", r":", r"v_t = y_t - H m_{t|t-1}, \quad S_t = H P_{t|t-1} H^\top + R", font_size=28),
            cmath(r"\text{update}", r":", r"m_t = m_{t|t-1} + K_t v_t, \quad P_t = (I - K_t H) P_{t|t-1}", font_size=28),
            cmath(r"\text{missing } y_t", r":", r"\text{skip the update: \ predict again}", font_size=28),
        ]
        rows[2][-1].set_color(STATEC)
        whys = [why(r"carry the ellipse forward"), why(r"the surprise and its variance"), why(r"Kalman (1960)"),
                why(r"ignorable missingness: skip measurement update")]
        with self.voiceover(
            "<bookmark mark='a'/> In equations: predict the mean and covariance forward through the dynamics. "
            "<bookmark mark='b'/> Compare the observation with its prediction: the innovation, with its variance. "
            "<bookmark mark='c'/> Update by the gain. Rudolf Kálmán published the recursion in 1960; it needs only "
            "the last mean and covariance, not the whole history, which made it practical on the computers of the "
            "day. <bookmark mark='d'/> And an ignorable missing observation needs no measurement update: predict "
            "again, with greater uncertainty. Informative missingness requires modelling the observation process."
        ) as vo:
            intro=label('Predict through dynamics, then update with the measurement',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nile(self):
        d = load("kalman")
        yrs, y = np.asarray(d["years"], float), np.asarray(d["y"], float)
        f, fs = np.asarray(d["filt"], float), np.asarray(d["filt_sd"], float)
        A = axes([1870, 1971], [400, 1450], x_length=8.4, y_length=4.2, xlabel=r"year", ylabel=r"flow ($10^8$ m$^3$)",
                 xticks=[1880, 1900, 1920, 1940, 1960], yticks=[500, 1000], xfmt=lambda v: f"{v:.0f}", center=[-1.4, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=OBSC) for a, b in zip(yrs, y)])
        b = band(ax, yrs[1:], (f - 1.645 * fs)[1:], (f + 1.645 * fs)[1:], STATEC, 0.2)
        c = polyline(ax, yrs[1:], f[1:], STATEC, 3)
        side = fit_rows(VGroup(
            label(r"the local level: \ $x_t = x_{t-1} + w_t$, \ $y_t = x_t + v_t$", font_size=22),
            label(rf"MLE: \ $\hat\sigma^2_w$ = {d['q']:,.0f}, \ $\hat\sigma^2_v$ = {d['r']:,.0f}", font_size=22, color=STATEC),
            label(r"Durbin \& Koopman: \ 1,469.1 and 15,099", font_size=22, color=GREY_A),
            label(rf"signal-to-noise {d['signal_noise']:.3f}: \ the level moves slowly", font_size=22, color=TAUC),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The Nile again, now its annual flow at Aswan from 1871 to 1970, the standard "
            "example of James Durbin and Siem Jan Koopman's textbook. The simplest state-space model, the local "
            "level, says the river has an underlying level that drifts as a random walk, and each year's flow is that"
            " level plus noise. <bookmark mark='b'/> Maximizing the likelihood gives a level variance of about "
            "fifteen hundred and a noise variance of about fifteen thousand: <bookmark mark='c'/> approximately the "
            "values in Durbin and Koopman's book, with a finite diffuse-prior approximation. <bookmark mark='d'/> The"
            " filtered level, in blue with its ninety percent band, follows the flows only slowly, discounting each "
            "year's surprise by the gain."
        ) as vo:
            self.add(nile_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(side[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                if m_ == "d":
                    self.play(FadeIn(b), Create(c))
                self.play(FadeIn(side[k + 1]))
        self.clear_scene()

    def drop(self):
        d = load("kalman")
        yrs, y = np.asarray(d["years"], float), np.asarray(d["y"], float)
        s, ss = np.asarray(d["smooth"], float), np.asarray(d["smooth_sd"], float)
        A = axes([1870, 1971], [400, 1450], x_length=8.4, y_length=4.2, xlabel=r"year", ylabel=r"flow ($10^8$ m$^3$)",
                 xticks=[1880, 1900, 1920, 1940, 1960], yticks=[500, 1000], xfmt=lambda v: f"{v:.0f}", center=[-1.4, 0.3, 0])
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=OBSC) for a, b in zip(yrs, y)])
        b = band(ax, yrs, s - 1.645 * ss, s + 1.645 * ss, BANDC, 0.2)
        c = polyline(ax, yrs, s, BANDC, 3)
        line = DashedLine(ax.c2p(1899, 400), ax.c2p(1899, 1450), color=MISSC, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"green: \ the smoothed level \ (chapter 8)", font_size=22, color=BANDC),
            label(rf"its largest one-year fall: \ into {d['biggest_drop_year']}", font_size=22, color=MISSC),
            label(rf"a level shift in 1899: \ {d['shift']:.0f}, \ $2\Delta\log L$ = {d['lr_shift']:.1f}, \ variances fixed", font_size=22, color=TAUC),
            label(r"the first Aswan dam begun in 1898; \ a drier climate", font_size=22, color=GREY_A),
        ), 3.8, 0.42, [4.9, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Using all the data, past and future, gives the smoothed level, in green, the "
            "subject of chapter eight. <bookmark mark='b'/> Its biggest one-year fall comes into 1899. <bookmark "
            "mark='c'/> Adding a permanent shift at 1899 to the model, the likelihood picks a fall of about three "
            "hundred, and the likelihood improvement statistic of " + say(d["lr_shift"], 1) + " is descriptive. The variances are held at their no-shift estimates, and the date was inspected in this "
            "same record, so this is not a calibrated likelihood-ratio test. <bookmark mark='d'/> Work on the first "
            "dam at Aswan began in 1898, and the climate of the basin became drier around the same time. This is "
            "evidence to investigate a level change, not causal attribution to the dam or a proof that the process "
            "broke."
        ) as vo:
            self.add(nile_tag())
            self.play(FadeIn(A), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(b), Create(c), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def steady(self):
        d = load("kalman")
        q, r = d["q"], d["r"]
        P = (q + (q * q + 4 * q * r) ** 0.5) / 2
        K = P / (P + r)
        rows = [
            cmath(r"\text{local level}", r":", r"K_t = P_{t|t-1} / (P_{t|t-1} + r)", font_size=30),
            cmath(r"\text{steady state}", r":", r"P = (q + \sqrt{q^2 + 4qr})/2, \quad K = P/(P + r)", font_size=30),
            cmath(r"m_t", r"=", r"m_{t-1} + K (y_t - m_{t-1}) = K y_t + (1 - K) m_{t-1}", font_size=30),
            cmath(r"\text{the Nile}", r":", rf"q/r = {q / r:.3f} \ \Rightarrow \ K = {K:.2f}", font_size=30),
        ]
        rows[2][-1].set_color(STATEC)
        whys = [why(r"the gain for a random-walk level"), why(r"the gain settles quickly"),
                why(r"Part 17's exponential smoothing! \ (Muth 1960)"), why(r"$\alpha = K$: \ chosen by the likelihood")]
        with self.voiceover(
            "<bookmark mark='a'/> For the local level the gain is the predicted variance over the predicted variance "
            "plus the noise variance. <bookmark mark='b'/> After a few steps it settles to a steady state, a fixed "
            "number determined by the ratio of the two variances. <bookmark mark='c'/> And then the "
            "filter's update is a weighted average of the new observation and the old level: Part seventeen's simple "
            "exponential smoothing, exactly. John Muth noticed this in 1960. <bookmark mark='d'/> For the Nile the "
            "signal-to-noise ratio of " + say(q / r, 3)
            + " gives a gain of " + say(K, 2) + ". The state space explains why exponential smoothing works, and lets the "
            "likelihood choose its smoothing constant."
        ) as vo:
            intro=label('The local-level steady-state gain yields exponential smoothing',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
