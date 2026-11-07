from __future__ import annotations

import numpy as np

from videos.stats.stats17.common import *  # noqa: F403


class Estimate(VoiceoverScene):
    def construct(self):
        self.card()
        self.yule_walker()
        self.least_squares()
        self.aic()
        self.residuals()
        self.ljung_box()
        self.choice()

    def card(self):
        card = chapter_card(5, r"Estimation", r"Fitting, \ choosing, \ and checking", part=PART)
        with self.voiceover("Chapter five. Estimation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def yule_walker(self):
        d = load("sunspot")
        r1, r2 = d["acf"][1], d["acf"][2]
        rows = [
            cmath(r"\rho(1)", r"=", r"\phi_1 + \phi_2 \rho(1),\ \ \rho(2) = \phi_1 \rho(1) + \phi_2", font_size=30),
            cmath(r"\begin{pmatrix} 1 & \rho_1 \\ \rho_1 & 1 \end{pmatrix}\binom{\phi_1}{\phi_2}", r"=", r"\binom{\rho_1}{\rho_2}", font_size=30),
            cmath(r"\hat\rho_1, \hat\rho_2", r"=", rf"{r1:.3f},\ {r2:.3f}", font_size=30),
            cmath(r"\hat\phi_{\text{YW}}", r"=", rf"({d['yw'][0]:.3f},\ {d['yw'][1]:.3f})", font_size=32),
        ]
        rows[3][2].set_color(MODEL)
        whys = [why(r"multiply the model by $X_{t-1}$, \ $X_{t-2}$; \ take expectations"), why(r"the Yule--Walker equations"),
                why(r"the sunspots' sample ACF"), why(r"Yule (1927), \ Walker (1931): \ the method of moments")]
        intro = label('Autocovariances identify autoregressive coefficients', font_size=36)
        with self.voiceover(
            "How did Yule estimate his coefficients? <bookmark mark='a'/> Multiply the AR two by the value one step back and "
            "take expectations, then do the same with the value two steps back. Out come two equations linking the "
            "coefficients to the autocorrelations. <bookmark mark='b'/> In matrix form, the autocorrelation matrix times the "
            "coefficients equals the vector of autocorrelations: the Yule–Walker equations, after Yule and Gilbert Walker, "
            "who used them on air pressure in 1931. <bookmark mark='c'/> Plug in the sample autocorrelations of the "
            "sunspots, point eight one and point four three, <bookmark mark='d'/> and solve: one point three two six and minus "
            "point six four two. It's Part 9's method of moments, for a series."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def least_squares(self):
        d = load("sunspot")
        s = np.asarray(d["s"])
        A = axes([0, 160], [0, 160], x_length=4.6, y_length=4.2, xlabel=r"$x_{t-1}$", ylabel=r"$x_t$", xticks=[0, 50, 100, 150],
                 yticks=[0, 50, 100, 150], center=[-4.0, 0.2, 0], font_size=18)
        dots = scatter(A.ax, s[:-1], s[1:], color=OBS, radius=0.045, opacity=0.7)
        rows = [
            cmath(r"x_t", r"=", r"c + \phi_1 x_{t-1} + \phi_2 x_{t-2} + e_t", font_size=30),
            cmath(r"\hat\phi_{\text{LS}}", r"=", rf"({d['ols'][0]:.3f},\ {d['ols'][1]:.3f})", font_size=30),
            cmath(r"\text{Gaussian MLE}", r"\approx", r"\text{the same, \ for an AR}", font_size=30),
            cmath(r"\text{MA terms}", r":", r"\text{the shocks are unobserved: \ iterate}", font_size=30),
        ]
        rows[1][2].set_color(MODEL)
        whys = [why(r"Part 12, \ with lagged values as regressors"), why(r"close to Yule--Walker"),
                why(r"Part 22's likelihood, \ conditional on the start"), why(r"nonlinear least squares, \ or the Kalman filter")]
        with self.voiceover(
            "<bookmark mark='a'/> The other natural method is Part 12's least squares, with the series' own past as the "
            "regressors. Here's each year's sunspot number against the year before's. <bookmark mark='b'/> Regressing on two "
            "lags gives one point three three six and minus point six five oh, very close to Yule–Walker. "
            "<bookmark mark='c'/> With Gaussian shocks this is the maximum likelihood estimate, conditional on the first two "
            "values, so the asymptotic theory of Part 9 supplies standard errors. <bookmark mark='d'/> Moving-average terms are "
            "harder, because the shocks they depend on aren't observed. They have to be reconstructed as the fit proceeds, "
            "which takes an iterative optimizer or the Kalman filter of Part 38."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(dots))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=1.4, buff=0.7, edge=6.9)
            step(0, transform=False)
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                step(k + 1, transform=False)
        self.clear_scene()

    def aic(self):
        d = load("order")
        aic = np.asarray(d["aic"])
        rel = aic - aic.min()
        A = axes([-0.6, 12.6], [0, 30], x_length=8.6, y_length=4.0, xlabel=r"AR order $p$", ylabel=r"AIC $-$ its minimum",
                 xticks=list(range(0, 13, 2)), yticks=[0, 10, 20, 30], center=[-1.4, 0.3, 0])
        ax = A.ax
        bars = VGroup()
        for p, v in enumerate(rel):
            h = min(v, 29.5)
            col = HIT if p == d["best"] else (OBS if p == 2 else SERIES)
            bars.add(Rectangle(width=ax.c2p(0.6, 0)[0] - ax.c2p(0, 0)[0], height=max(0.02, ax.c2p(0, h)[1] - ax.c2p(0, 0)[1]),
                               stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(ax.c2p(p, 0), aligned_edge=DOWN))
        clip = VGroup(*[MathTex(f"{rel[p]:.0f}", font_size=20, color="#101418").move_to(bars[p].get_top() + DOWN * 0.22) for p in (0, 1)])
        star = VGroup(Dot(ax.c2p(d["best"], 0.6), radius=0.09, color=HIT),
                      MathTex(r"\text{min}", font_size=20, color=HIT).next_to(ax.c2p(d["best"], 0.6), UP, buff=0.12))
        rows = fit_rows(VGroup(
            MathTex(r"\text{AIC} = n_c \log \hat\sigma^2_p + 2(p + 1) + C", font_size=28),
            label(r"Akaike (1973): \ fit, \ penalized by size", font_size=22, color=GREY_A),
            label(rf"best: \ $p = {d['best']}$", font_size=24, color=HIT),
            label(rf"$p = 2$: \ {rel[2]:.1f} higher", font_size=22, color=OBS),
        ), 4.0, 0.4, [4.9, 0.4, 0])
        with self.voiceover(
            "How many lags? <bookmark mark='a'/> Hirotugu Akaike's information criterion, from 1973, balances fit against size: "
            "on a common sample, take its size times the log mean squared residual, plus twice the number of fitted mean parameters. A common constant includes the innovation-variance penalty. Smaller is better. "
            "<bookmark mark='b'/> For the sunspots, over orders zero to twelve: zero and one lag are hopeless. "
            "<bookmark mark='c'/> The minimum is at order eight. <bookmark mark='d'/> Yule's AR two is four point nine units "
            "worse: a real difference, but not a crushing one. Part 28 explains what such differences mean; for now, AIC "
            "prefers the longer memory that chapter three found missing."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), FadeIn(clip))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(star, scale=1.5))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Indicate(bars[2], color=OBS))
        self.clear_scene()

    def residuals(self):
        d = load("order")
        b = d["band"]
        best = d["best"]
        panels = VGroup()
        for k, (key, nm, col) in enumerate(((f"p2", r"AR(2) residuals", OBS), (f"p{best}", rf"AR({best}) residuals", HIT))):
            A = axes([0, 21], [-0.3, 0.3], x_length=5.6, y_length=3.0, xlabel=r"lag", yticks=[-0.2, 0, 0.2], font_size=16,
                     center=[-3.4 + 6.8 * k, 0.6, 0])
            cg = Correlogram(A.ax, d[key]["resid_acf"], band=b, color=col, width=0.55)
            t = label(nm, font_size=22, color=col).next_to(A, UP, buff=0.08)
            panels.add(VGroup(A, cg, t))
        rows = fit_rows(VGroup(
            label(r"if the model is right, \ the residuals are white noise", font_size=24),
            label(r"AR(2): \ a bump at lag 11, \ just outside: \ the cycle it missed", font_size=22, color=OBS),
            label(rf"AR({best}): \ no large linear correlations detected", font_size=22, color=HIT),
        ), 12.4, 0.25, [0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Then check. If the model has captured the dependence, its residuals should be white noise, "
            "with autocorrelations inside the bands. <bookmark mark='b'/> The AR two's residuals are nearly clean, but there's "
            "a bump at lag eleven, just outside the band: the cycle-length memory it couldn't represent. "
            "<bookmark mark='c'/> The AR eight's residuals show nothing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            p = panels[0]
            self.play(FadeIn(p[0]), FadeIn(p[2]), FadeIn(p[1].zero), FadeIn(p[1].bands),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p[1].bars], lag_ratio=0.04), FadeIn(rows[1]))
            vo.wait_until("c")
            p = panels[1]
            self.play(FadeIn(p[0]), FadeIn(p[2]), FadeIn(p[1].zero), FadeIn(p[1].bands),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in p[1].bars], lag_ratio=0.04), FadeIn(rows[2]))
        self.wait(1.0)
        self.clear_scene()

    def ljung_box(self):
        d = load("order")
        best = d["best"]
        rows = [
            cmath(r"Q", r"=", r"n(n + 2)\sum_{k=1}^{h} \frac{\hat r_k^2}{n - k}", font_size=32),
            cmath(r"H_0", r":", r"Q \approx \chi^2_{h - p}", font_size=32),
            cmath(r"\text{AR(2)}", r":", rf"Q(20) = {d['p2']['Q']:.1f},\ \ p = {d['p2']['p']:.2f}", font_size=30),
            cmath(rf"\text{{AR}}({best})", r":", rf"Q(20) = {d[f'p{best}']['Q']:.1f},\ \ p = {d[f'p{best}']['p']:.2f}", font_size=30),
        ]
        rows[3][2].set_color(HIT)
        whys = [why(r"all the residual autocorrelations at once"), why(r"Ljung \& Box (1978); \ lose a d.f. per coefficient"),
                why(r"passes, \ despite the lag-11 bump"), why(r"no rejection; \ not proof of white noise")]
        intro = label('Check several residual autocorrelations together', font_size=36)
        with self.voiceover(
            "One test can summarize a whole correlogram. <bookmark mark='a'/> Greta Ljung and George Box's Q statistic adds "
            "up the squared residual autocorrelations over the first h lags, with weights that improve its small-sample "
            "behaviour. <bookmark mark='b'/> If the residuals are white noise, Q is approximately chi-squared, with one degree "
            "of freedom subtracted for each fitted AR or MA coefficient. For a model chosen after looking at these data, read the p-values as descriptive checks. <bookmark mark='c'/> For the AR two, Q over twenty lags is "
            "twenty-four point one, p equals point one five: it passes, the lag-eleven bump diluted among twenty lags. "
            "<bookmark mark='d'/> For the AR eight, p equals point four eight. Both pass. A portmanteau test like this one is "
            "a coarse net: passing it doesn't make a model right."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
        self.clear_scene()

    def choice(self):
        best = load("order")["best"]
        rows = fit_rows(VGroup(
            label(r"Yule--Walker and least squares approach the same regular AR target", font_size=24),
            label(r"AIC chooses how much memory to keep", font_size=24, color=HIT),
            label(r"residual checks catch what the model missed; \ Ljung--Box is coarse", font_size=24, color=RES),
            label(rf"AR(2): \ 3 parameters, \ the physics; \ AR({best}): \ 9, \ the better fit", font_size=24, color=OBS),
            label(r"the honest referee is prediction: \ next chapter", font_size=26, color=FC),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: under regular stable autoregressive assumptions, Yule–Walker and least squares approach the same target. "
            "<bookmark mark='b'/> AIC chooses how much memory to keep. <bookmark mark='c'/> Residual checks catch what a model "
            "has missed, though summary tests like Ljung–Box are coarse. <bookmark mark='d'/> Yule's AR two has three "
            "parameters and a physical story; the AR eight has nine, and fits better. <bookmark mark='e'/> Which is better in "
            "the sense that matters? The honest referee is prediction of data the model hasn't seen."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
