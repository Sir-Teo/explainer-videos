from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


def _bell(ax, m, v, col, scale=1.0, sw=3):
    xs = np.linspace(-5.2, -1.8, 220)
    return curve(ax, xs, scale * np.exp(-0.5 * (xs - m) ** 2 / v) / np.sqrt(2 * np.pi * v), col, stroke_width=sw)


class Kalman(VoiceoverScene):
    def construct(self):
        k = load("kalman")
        self.card()
        self.bell(k)
        self.derive(k)
        self.lab(k)
        self.sv(k)

    def card(self):
        c = chapter_card(5, r"The Kalman filter and stochastic volatility", r"How do you track what you cannot see?",
                         lit=(1960,), part=PART)
        with self.voiceover("Chapter five. The Kalman filter, and stochastic volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def bell(self, k):
        y, m, mp = np.asarray(k["y"]), np.asarray(k["m"]), np.asarray(k["m_prior"])
        Pp, P, K = np.asarray(k["P_prior"]), np.asarray(k["P"]), np.asarray(k["K"])
        r = k["r"]
        g = axes([-5.2, -1.8], [0, 3.2], x_length=8.0, y_length=3.6, xticks=[-5, -4, -3, -2],
                 xfmt=lambda u: f"{100 * np.exp(u) * np.sqrt(365):.0f}\\%",
                 xlabel=r"Bitcoin's volatility today (log scale, annualised)", yticks=[], font_size=16).to_edge(UP, buff=0.6)
        ax = g.ax
        i0 = 500
        prior = _bell(ax, m[i0 - 1], P[i0 - 1], VOL)
        leg = legend([(VOL, r"belief (prior, then posterior)"), (RET, r"measurement: today's realized vol, with its noise"),
                      (GOOD, r"updated belief")], font_size=18).to_corner(UR, buff=0.3).shift(DOWN * 4.2)
        info = VGroup()
        with self.voiceover(
            "Kalman's filter of 1960 does for a continuous hidden state what Hamilton's jars do for a discrete one. Hold a belief about today's hidden log volatility: a bell curve, its "
            "centre the best guess, its width the uncertainty. <bookmark mark='a'/> Predict: overnight the hidden "
            "level may have drifted, so the bell widens. <bookmark mark='b'/> Observe: today's realized volatility "
            "arrives, a measurement with its own, wider bell of noise. <bookmark mark='c'/> Update: multiply the two "
            "bells. The product is narrower than either, and its centre moves a fraction K of the way toward the "
            "measurement. K is the Kalman gain. <bookmark mark='d'/> Day after day: widen, observe, pull and narrow."
        ) as vo:
            self.play(FadeIn(g), Create(prior), FadeIn(leg[0]))
            vo.wait_until("a")
            wide = _bell(ax, mp[i0], Pp[i0], VOL)
            self.play(Transform(prior, wide))
            vo.wait_until("b")
            meas = _bell(ax, y[i0], r, RET)
            dot = Dot(ax.c2p(y[i0], 0), radius=0.08, color=RET)
            self.play(FadeIn(dot, shift=DOWN * 0.3), Create(meas), FadeIn(leg[1]))
            vo.wait_until("c")
            post = _bell(ax, m[i0], P[i0], GOOD, sw=4)
            arr = Arrow(ax.c2p(mp[i0], 2.9), ax.c2p(m[i0], 2.9), buff=0, color=GOOD, stroke_width=4,
                        max_tip_length_to_length_ratio=0.3)
            kl = MathTex(rf"K(y - m),\ K = {K[i0]:.2f}", font_size=28, color=GOOD).next_to(arr, UP, buff=0.1)
            self.play(TransformFromCopy(VGroup(prior, meas), post), GrowArrow(arr), FadeIn(kl), FadeIn(leg[2]))
            vo.wait_until("d")
            for i in range(i0 + 1, i0 + 6):
                self.play(FadeOut(dot), FadeOut(meas), FadeOut(arr), FadeOut(kl), Transform(prior, _bell(ax, mp[i], Pp[i], VOL)),
                          FadeOut(post), run_time=0.35)
                dot = Dot(ax.c2p(np.clip(y[i], -5.2, -1.8), 0), radius=0.08, color=RET)
                meas = _bell(ax, y[i], r, RET)
                post = _bell(ax, m[i], P[i], GOOD, sw=4)
                arr = Arrow(ax.c2p(mp[i], 2.9), ax.c2p(m[i], 2.9), buff=0, color=GOOD, stroke_width=4,
                            max_tip_length_to_length_ratio=0.3)
                kl = VGroup()
                self.play(FadeIn(dot), Create(meas), run_time=0.35)
                self.play(TransformFromCopy(VGroup(prior, meas), post), GrowArrow(arr), run_time=0.45)
        self.wait(0.3)
        self.clear_scene()

    def derive(self, k):
        rows = [
            cmath(r"x_t = x_{t-1} + w_t,\ \ y_t = x_t + v_t", r":", r"\ N(m, P) \to N(m, P + q)", font_size=34),
            cmath(r"p(x\mid y)", r"\propto", r"e^{-(x - m)^2/2P^-}\,e^{-(y - x)^2/2r}", font_size=34),
            cmath(r"\frac{1}{P^+} = \frac{1}{P^-} + \frac{1}{r}", r",", r"\ m^+ = m + K(y - m),\ \ K = \frac{P^-}{P^- + r}",
                  font_size=34),
            cmath(r"P^- = P^+ + q,\ P^+ = (1 - K)P^-", r"\Rightarrow", r"p^2 - \tfrac{q}{r}p - \tfrac{q}{r} = 0,\ \ K = \frac{p}{1 + p}",
                  font_size=34),
        ]
        whys = [why(r"the hidden level drifts by $w_t$ (variance $q$), the measurement adds $v_t$ (variance $r$): predict"),
                why(r"Bayes: the prior times the likelihood of the measurement"),
                why(r"complete the square: precisions add, and the mean moves by a fraction $K$"),
                why(r"in steady state the widening and the narrowing balance; $p = P^-/r$")]
        step = ladder(self, rows, whys, keep=2, top=3.2, x=-1.6, buff=0.55, edge=6.9)
        g = axes([-3, 2], [0, 1], x_length=5.4, y_length=2.4, log_x=True, xticks=[-3, -2, -1, 0, 1, 2],
                 yticks=[0, 0.5, 1], xlabel=r"signal-to-noise $q/r$", ylabel=r"steady-state gain $K$", font_size=15)
        g.to_corner(DL, buff=0.45)
        qr, gain = np.asarray(k["qr"]), np.asarray(k["gain"])
        line = curve(g.ax, np.log10(qr), gain, VOL, stroke_width=3)
        pt = Dot(g.ax.c2p(np.log10(k["snr"]), k["K_ss"]), radius=0.09, color=BAD)
        pl = label(rf"Bitcoin: $q/r = {k['snr']:.2f}$, $K = {k['K_ss']:.2f}$", font_size=20, color=BAD).next_to(pt, RIGHT, buff=0.15)
        pc = pause_card(r"If the measurement gets noisier ($r$ up), does the belief move more or less toward each dot?",
                        width=5.6, font_size=21).to_corner(DR, buff=0.35)
        with self.voiceover(
            "The derivation. The hidden level drifts with variance q, the measurement adds noise r, and predicting adds q. <bookmark mark='a'/> Bayes multiplies the prior by the likelihood of "
            "the measurement, <bookmark mark='b'/> and completing the square gives the rules: precisions add, and the "
            "mean moves by the gain K, the prior variance over the prior plus the noise. <bookmark mark='c'/> In "
            "steady state, the widening each night and the narrowing each day balance, and the gain depends only on "
            f"the signal-to-noise ratio. Bitcoin's log volatility has a ratio of about {k['snr']:.2f}, so each day "
            f"the belief moves {100 * k['K_ss']:.0f} percent of the way to the new measurement. <bookmark mark='d'/> "
            "Pause and predict: if the measurements get noisier, does the belief move more, or less? Less: r rises, "
            "the ratio falls, and K slides down the curve."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(g), Create(line), FadeIn(pt), FadeIn(pl))
            vo.wait_until("d")
            self.play(FadeIn(pc))
        self.wait(0.3)
        self.clear_scene()

    def lab(self, k):
        card = lab_card(r"the local-level Kalman filter", [
            "def kalman_states(y, q, r):",
            "    m, P = y[0], np.var(y)",
            "    for t in range(len(y)):",
            "        Pm = P + q                  # predict: widen",
            "        K = Pm / (Pm + r)           # the gain",
            "        m = m + K * (y[t] - m)      # pull toward y",
            "        P = (1 - K) * Pm            # narrow",
            "        out['m'][t], out['K'][t] = m, K",
            "    return out",
        ], source="explainer/quant/house/vol.py", width=6.8).to_corner(UL, buff=0.3)
        t, y, m, P = (np.asarray(k[x]) for x in ("t", "y", "m", "P"))
        g = axes([2017.6, 2021], [-5.2, -1.8], x_length=6.0, y_length=3.0, xticks=[2018, 2019, 2020, 2021],
                 xfmt=lambda u: f"{int(u)}", yticks=[-5, -4, -3, -2], font_size=14,
                 ylabel=r"log volatility, Bitcoin", yfmt=lambda u: f"{u:g}").to_corner(DR, buff=0.4)
        tr = ValueTracker(0)
        dots = VGroup(*[Dot(g.ax.c2p(a, np.clip(b, -5.2, -1.8)), radius=0.015, color=RET).set_opacity(0.6) for a, b in zip(t, y)])
        bd = band(g.ax, t, m - 2 * np.sqrt(P), m + 2 * np.sqrt(P), VOL, 0.3)
        line = tracing(g.ax, t, m, tr, VOL, stroke_width=3)
        with self.voiceover(
            "Lab. Here is the House's filter: four lines inside a loop, widen, gain, pull, narrow. The noise variances "
            "q and r are fitted by maximum likelihood, the filter's own forecast errors scoring each guess. <bookmark "
            "mark='a'/> Run it on Bitcoin's daily log volatility, and the river from the start of this part draws "
            "itself, with its band of uncertainty."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"q = {k['q']:.4f}, r = {k['r']:.4f}, q/r = {k['snr']:.2f}",
                                 f"steady-state K = {k['K_ss']:.2f}"], run_time=1.5)
            self.play(FadeIn(g), FadeIn(dots), FadeIn(bd))
            self.add(line)
            self.play(tr.animate.set_value(len(t) - 1), run_time=max(vo.remaining(1.0) - 0.3, 2.5), rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    def sv(self, k):
        sv = k["sv"]
        rows = [
            cmath(r"h_t", r"=", r"\mu + \phi(h_{t-1} - \mu) + \eta_t", font_size=36),
            cmath(r"\ln r_t^2", r"=", r"h_t + \ln z_t^2,\quad \mathbb{E}\ln z^2 = -1.27,\ \operatorname{Var}\ln z^2 = \tfrac{\pi^2}{2}",
                  font_size=36),
        ]
        whys = [why(r"stochastic volatility: the log variance is a hidden autoregression"),
                why(r"the squared return is its noisy measurement; treat $\ln\chi^2_1$ as Gaussian: quasi-likelihood")]
        step = ladder(self, rows, whys, keep=2, top=3.3, x=-2.2, buff=0.5, edge=6.9)
        t = np.asarray(k["us_t"])
        g = axes([1926, 2021], [0, 1.0], x_length=8.4, y_length=3.0, xticks=[1930, 1960, 1990, 2020],
                 xfmt=lambda u: f"{int(u)}", yticks=[0, 0.5, 1.0], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 ylabel=r"US market volatility, annualised", font_size=15).to_corner(DL, buff=0.4)
        lg = curve(g.ax, t, np.clip(k["garch_vol"], 0, 1), FC, stroke_width=2)
        ls = curve(g.ax, t, np.clip(k["sv_vol"], 0, 1), ALT, stroke_width=2)
        leg = legend([(ALT, r"stochastic volatility, smoothed"), (FC, r"GARCH (next chapter)")], font_size=18)
        side = VGroup(leg,
                      MathTex(rf"\phi = {sv['phi']:.3f},\ \sigma_\eta = {sv['sigma_eta']:.3f}", font_size=28, color=ALT),
                      label(rf"half-life {sv['half_life']:.0f} trading days", font_size=20, color=GREY_A),
                      label(rf"correlation with GARCH: {k['corr_sv_garch']:.2f}", font_size=20, color=GREY_A),
                      label(r"Harvey, Ruiz and Shephard (1994); MCMC is the Bayesian route (Part 6)", font_size=17, color=GREY_B))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.35)
        track = ("almost exactly." if k["corr_sv_garch"] > 0.9 else
                 f"closely, with a correlation of {k['corr_sv_garch']:.2f}.")
        with self.voiceover(
            f"The same filter gives a model of volatility. Let the log variance be a hidden autoregression: stochastic "
            f"volatility. <bookmark mark='a'/> The squared return is a very noisy measurement of it. Take logs, and the "
            f"noise has a known mean and variance. Andrew Harvey, Esther Ruiz and Neil Shephard treated it as Gaussian "
            f"in 1994, and the Kalman filter gives the likelihood. <bookmark mark='b'/> On ninety-four years of daily "
            f"returns, phi is {sv['phi']:.3f}: a half-life of about {sv['half_life']:.0f} trading days. The smoothed volatility "
            f"tracks the GARCH model of the next chapter {track} Two very different models, one hidden river."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(g), Create(lg), Create(ls), FadeIn(side), run_time=3)
        self.wait(0.3)
        self.clear_scene()
