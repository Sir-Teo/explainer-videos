from __future__ import annotations

import numpy as np
from scipy import stats as sst

from explainer.quant import *  # noqa: F403
from videos.quant.quant6.common import ALT, BAD, DATA_C, EST, GOOD, PART, ellipse_curve, load, predict, show_card


class SNR(VoiceoverScene):
    def construct(self):
        s = load("snr")
        ep = load("ellipse_path")
        b = load("bootstrap")
        self.card()
        self.derive(b)
        self.ellipse(ep)
        self.years(s)

    def card(self):
        c = chapter_card(16, r"How many years until you know?", r"How long before a good strategy proves itself?",
                         part=PART)
        with self.voiceover("Chapter sixteen. How many years until you know?"):
            show_card(self, c)
        self.play(FadeOut(c))

    def derive(self, b):
        C_ = {r"T_{yrs}": EST, r"\widehat{SR}": ALT}
        rows = [cmath(r"t = \frac{\hat\mu}{\hat\sigma / \sqrt T}", r"=", r"\widehat{SR}_{ann}\sqrt{T_{yrs}}"
                      r"\ \Rightarrow\ T_{yrs} = (t / SR)^2", font_size=36, colors=C_),
                cmath(r"\mathrm{Var}(\widehat{SR})", r"\approx", r"\frac{1 + \tfrac12 SR^2}{T}\ \Big(+\frac{\kappa - 3}{4}"
                      r"SR^2 - \gamma_3\,SR\Big)", font_size=36, colors=C_),
                cmath(r"\mathrm{Var}(\hat\alpha) = \frac{\sigma_\varepsilon^2}{T}\Big(1 + \frac{\mu_m^2}{\sigma_m^2}\Big)",
                      r",", r"\ \mathrm{Var}(\hat\beta) = \frac{\sigma_\varepsilon^2}{T \sigma_m^2}", font_size=36,
                      colors=C_)]
        whys = [why(r"annualise: the $t$-statistic of a mean return is the Sharpe ratio times the root of the years"),
                why(r"the delta method (Lo 2002); with skewness $\gamma_3$ and kurtosis $\kappa$ (Mertens 2002)"),
                why(r"chapter one's formula for the regression on the market: $\alpha$ is a mean, $\beta$ a co-movement")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.4, buff=1.0, edge=6.8)
        with self.voiceover(
            "The deepest problem in quantitative finance: small signal, large noise. A mean return's t-statistic is "
            "the mean over its standard error, the volatility over the root of T. Annualise both, and t is the Sharpe "
            "ratio times the root of the years. So a t of two needs two over the Sharpe ratio, squared, years. "
            "<bookmark mark='a'/> The Sharpe ratio's own standard error, by the delta method, adds the noise of the "
            "mean, one over T, to the noise of the volatility, half the Sharpe ratio squared over T: Andrew Lo, 2002. "
            "Christoph Mertens added skewness and fat tails. For the market, "
            f"{b['se_iid']:.3f} and {b['se_mertens']:.3f}, and chapter eleven's bootstrap was wider still. "
            "<bookmark mark='b'/> And on the market, chapter one's formula splits into two speeds. Beta's variance is "
            "the residual variance over T times the market's variance: a co-movement, measured every month. Alpha's has "
            "a one plus the market's squared Sharpe ratio in it: it is a mean, and means take decades."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def ellipse(self, ep):
        P = ep["path"]
        g = axes([-0.4, 0.45], [0.0, 1.6], x_length=6.6, y_length=4.8, xlabel=r"$\alpha$, annual", ylabel=r"$\beta$",
                 xticks=[-0.3, 0, 0.3], xfmt=lambda u: f"{100 * u:.0f}\\%", yticks=[0.4, 0.8, 1.2, 1.6], font_size=16)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        k = ValueTracker(0)
        clip = ((-0.4, 0.45), (0.0, 1.6))

        def shape():
            i = int(min(k.get_value(), len(P) - 1))
            p = P[i]
            e = ellipse_curve(ax, (p["alpha"], p["beta"]), p["V"], EST, clip=clip)
            d = Dot(ax.c2p(np.clip(p["alpha"], -0.4, 0.45), np.clip(p["beta"], 0, 1.6)), radius=0.06, color=EST)
            V = np.asarray(p["V"])
            ro = VGroup(
                MathTex(rf"{p['date'] // 100}:\ {p['months'] / 12:.0f}\ \text{{{'year' if round(p['months'] / 12) == 1 else 'years'}}}",
                        font_size=30, color=WHITE),
                MathTex(rf"\alpha = {100 * p['alpha']:+.1f}\% \pm {196 * np.sqrt(V[0, 0]):.1f}\%", font_size=28,
                        color=ALT),
                MathTex(rf"\beta = {p['beta']:.2f} \pm {1.96 * np.sqrt(V[1, 1]):.2f}", font_size=28, color=GOOD),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.6).shift(UP * 0.6)
            return VGroup(e, d, ro)
        sm = always_redraw(shape)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 1.6), color=GREY_B, stroke_width=2)
        notes = VGroup(label(r"$\beta$ axis: a co-movement, pinned down in months", font_size=21, color=GOOD),
                       label(r"$\alpha$ axis: a mean, it creeps", font_size=21, color=ALT),
                       label(r"tobacco on the market, refitted every quarter from 1961", font_size=19, color=GREY_B)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.8)
        last = P[-1]
        with self.voiceover(
            "Watch it happen. Regress tobacco on the market from 1961 with one year of data, refitting every quarter "
            "as the data arrive; the ellipse is the ninety-five percent region for alpha and beta. "
            "<bookmark mark='a'/> In the first years it is enormous. Within a few years the beta axis collapses to a "
            "sliver. The alpha axis creeps, and creeps, and creeps. <bookmark mark='b'/> After sixty years, tobacco's "
            f"alpha is {100 * last['alpha']:.1f} percent a year, give or take "
            f"{196 * np.sqrt(np.asarray(last['V'])[0, 0]):.1f}. Its beta has been known to within a tenth for half a "
            "century."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(notes[2]))
            self.add(sm)
            vo.wait_until("a")
            self.play(k.animate.set_value(len(P) * 0.15), run_time=3, rate_func=linear)
            self.play(FadeIn(notes[0]))
            self.play(k.animate.set_value(len(P) - 1), run_time=max(vo.until("b") - 0.5, 2.0), rate_func=linear)
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
        sm.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def years(self, s):
        sr, yrs = np.asarray(s["sr"]), np.asarray(s["years"])
        g = axes([0.2, 2.0], [0, 100], x_length=5.6, y_length=4.0, xlabel=r"true Sharpe ratio, annual",
                 ylabel=r"years for an expected $t$ of 2", xticks=[0.5, 1.0, 1.5, 2.0], yticks=[0, 16, 50, 100],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, sr, np.minimum(yrs, 100), EST, stroke_width=3.5)
        dots = VGroup(Dot(ax.c2p(0.5, s["y05"]), radius=0.08, color=BAD), Dot(ax.c2p(1.0, s["y1"]), radius=0.08,
                                                                              color=GOOD))
        T = np.asarray(s["T"])
        g2 = axes([0, 30], [0, 0.5], x_length=4.8, y_length=2.6, xlabel=r"years of data", ylabel=r"chance it looks "
                  r"worse than zero", xticks=[0, 10, 20, 30], yticks=[0, 0.25, 0.5], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=14).to_corner(UR, buff=0.45)
        a2 = g2.ax
        cols = {"0.25": BAD, "0.5": ALT, "1.0": GOOD}
        pl = VGroup(*[curve(a2, T, np.asarray(s["p_neg"][k]), c, stroke_width=3) for k, c in cols.items()])
        leg = legend([(BAD, r"SR 0.25"), (ALT, r"SR 0.5"), (GOOD, r"SR 1")], font_size=17).next_to(g2, DOWN, buff=0.25)
        p5 = float(sst.norm.cdf(-0.5 * np.sqrt(5)))
        desk = desk_question(r"A strategy has a Sharpe ratio of 1 over 4 years. What is the standard error?",
                             rf"$\sqrt{{(1 + SR^2/2)/T}} = \sqrt{{1.5/4}} \approx {s['se_desk']:.2f}$: the 95\% "
                             r"interval runs from below zero to above two", width=6.2, font_size=21)
        desk.next_to(leg, DOWN, buff=0.3).to_edge(RIGHT, buff=0.4)
        q = predict(r"To halve the standard error of $\alpha$, how many more years?", width=5.0).to_corner(DR, buff=0.3)
        q.to_edge(LEFT, buff=0.5)
        with self.voiceover(
            "Put numbers on it. A strategy with a true Sharpe ratio of a half, a good strategy, needs "
            f"{s['y05']:.0f} years of data before its t-statistic is expected to reach two. A Sharpe ratio of one "
            f"needs {s['y1']:.0f}. <bookmark mark='a'/> Over shorter spans good strategies often look bad. After five "
            f"years, a Sharpe-of-a-half strategy has about a {100 * p5:.0f} percent chance of having lost money. Funds "
            "are closed and strategies abandoned on evidence like that, and bad ones are kept for the same reason. "
            "<bookmark mark='b'/> A desk question: a Sharpe ratio of one over four years. The standard error is "
            f"about {s['se_desk']:.2f}, so the true value could be anywhere from below zero to above two. "
            "<bookmark mark='c'/> Pause and predict: to halve the standard error of alpha, how many more years? "
            "Four times as many. This is why the House seals its hold-out data in an envelope, and counts every "
            "trial: Part twenty-six."
            " Next: how research desks guard against all of this."
        ) as vo:
            self.play(FadeIn(g), Create(line))
            self.play(FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(g2), LaggedStart(*[Create(p) for p in pl], lag_ratio=0.3), FadeIn(leg))
            vo.wait_until("b")
            self.play(FadeIn(desk))
            vo.wait_until("c")
            self.play(FadeOut(desk), FadeIn(q))  # the desk question is answered; the next one takes its corner
        self.wait(0.4)
        self.clear_scene()
