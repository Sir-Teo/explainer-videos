from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data, predict


class Arma(VoiceoverScene):
    def construct(self):
        a = load("acf_arma")
        self.card()
        self.spring()
        self.derive()
        self.identify()
        self.lab(a)

    def card(self):
        c = chapter_card(1, r"Stationarity, ARMA and Box--Jenkins", r"What does a series remember?", lit=(1927,),
                         part=PART)
        with self.voiceover("Chapter one. Stationarity, ARMA models, and the Box-Jenkins method."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def spring(self):
        n = 240
        eps = np.random.default_rng(4).standard_normal(n)
        phi = ValueTracker(0.0)

        def path(p):
            x = np.zeros(n)
            x[0] = eps[0] / np.sqrt(1 - p ** 2)
            for t in range(1, n):
                x[t] = p * x[t - 1] + eps[t]
            return x

        extent = max(np.max(np.abs(path(p))) for p in np.linspace(0, 0.99, 300)) * 1.05
        g = axes([0, n], [-extent, extent], x_length=7.4, y_length=3.4, xticks=[], yticks=[-10, 0, 10],
                 ylabel=r"$x_t = \phi\,x_{t-1} + \varepsilon_t$ (simulated, the same shocks)", font_size=16)
        g.to_edge(LEFT, buff=0.5).shift(UP * 0.9)
        ga = axes([0, 21], [0, 1], x_length=4.4, y_length=2.4, xticks=[1, 10, 20], yticks=[0, 0.5, 1],
                  xlabel=r"lag $k$", ylabel=r"autocorrelation $\rho_k = \phi^k$", font_size=16)
        ga.to_edge(RIGHT, buff=0.5).align_to(g, UP)
        line = always_redraw(lambda: curve(g.ax, np.arange(n), path(phi.get_value()), VOL,
                                           stroke_width=2))
        bars = always_redraw(lambda: VGroup(*[Line(ga.ax.c2p(k, 0), ga.ax.c2p(k, phi.get_value() ** k), stroke_width=6,
                                                   color=VOL) for k in range(1, 21)]))
        ro = VGroup(readout(r"\phi =", lambda: phi.get_value(), digits=2, font_size=34, color=VOL),
                    readout(r"\operatorname{Var} x_t = \frac{\sigma^2}{1-\phi^2} =",
                            lambda: 1 / (1 - phi.get_value() ** 2), digits=1, font_size=30),
                    readout(r"\text{half-life (steps)} = \frac{\ln\tfrac12}{\ln\phi} =",
                            lambda: np.log(0.5) / np.log(max(phi.get_value(), 1e-3)) if phi.get_value() > 0.01 else 0.0,
                            digits=1, font_size=30))
        ro.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ga, DOWN, buff=0.45).align_to(ga, LEFT)
        defn = definition_card(r"Weak stationarity",
                               r"the mean is constant, the variance is finite, and the covariance of $x_t$ and "
                               r"$x_{t-k}$ depends only on the lag $k$, not on $t$", width=7.4, font_size=22)
        defn.next_to(g, DOWN, buff=0.35).align_to(g, LEFT)
        with self.voiceover(
            "The simplest series that remembers: keep a fraction phi of yesterday's value, add a fresh shock. At "
            "phi zero, pure noise. <bookmark mark='a'/> Turn phi up to a half: the "
            "path smooths, and its autocorrelation decays geometrically, phi to the power of the lag. <bookmark "
            "mark='b'/> At zero point nine the series wanders in long swings, and its variance has grown five-fold. "
            "<bookmark mark='c'/> At zero point nine nine, a shock takes almost seventy steps to lose half its effect. "
            "It is a ball on a spring, kicked by shocks. For absolute phi below one, with a stationary start and independent unit-variance shocks, the series is stationary: its "
            "mean and variance stay put, and its correlations depend only on the lag."
        ) as vo:
            self.play(FadeIn(g), FadeIn(ga), FadeIn(ro))
            self.add(line, bars)
            vo.wait_until("a")
            self.play(phi.animate.set_value(0.5), run_time=2)
            vo.wait_until("b")
            self.play(phi.animate.set_value(0.9), run_time=2)
            vo.wait_until("c")
            self.play(phi.animate.set_value(0.99), run_time=2)
            self.play(FadeIn(defn, shift=UP * 0.1))
        self.wait(0.3)
        line.clear_updaters()
        bars.clear_updaters()
        self.clear_scene()

    def derive(self):
        C = {r"\phi": VOL}
        rows = [
            cmath(r"x_t", r"=", r"\phi x_{t-1} + \varepsilon_t = \sum_{k\ge 0}\phi^k\varepsilon_{t-k}", font_size=38),
            cmath(r"\operatorname{Var} x_t", r"=", r"\sigma^2\sum_{k\ge0}\phi^{2k} = \frac{\sigma^2}{1-\phi^2}",
                  font_size=38),
            cmath(r"\gamma_k", r"=", r"\mathbb{E}[x_t x_{t-k}] = \phi^k\gamma_0,\qquad \rho_k = \phi^k", font_size=38),
            cmath(r"\mathbb{E}_t x_{t+h}", r"=", r"\phi^h x_t,\qquad h_{1/2} = \ln\tfrac12 / \ln\phi", font_size=38),
            cmath(r"Q", r"=", r"T(T+2)\sum_{k=1}^{m}\frac{\hat\rho_k^2}{T-k}\ \overset{a}{\sim}\ \chi^2_m", font_size=38),
        ]
        whys = [why(r"substitute the recursion into itself; the sum converges when $|\phi| < 1$"),
                why(r"the shocks are independent: variances add; a geometric series"),
                why(r"multiply by $x_{t-k}$ and take expectations: the shock $\varepsilon_t$ is new"),
                why(r"iterate forward; the half-life shown requires $0<\phi<1$"),
                why(r"Ljung--Box: asymptotic under suitable white-noise assumptions; fitted ARMA residuals use $m-p-q$ df")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-2.6, buff=0.5, edge=6.9)
        wold = wrapped_label('Wold (1938): a centered, purely nondeterministic covariance-stationary series has $x_t=\\sum_k\\psi_k\\varepsilon_{t-k}$. ARMA uses $\\phi(L)x_t=\\theta(L)\\varepsilon_t$.', 12.4, 22, ALT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why those numbers. Substitute the recursion into itself, and the series is a weighted sum of all past "
            "shocks, with weights phi to the k. <bookmark mark='a'/> Shocks are independent, so their variances add: "
            "a geometric series, sigma squared over one minus phi squared. <bookmark mark='b'/> Multiply by the value "
            "k steps back and take expectations: the autocorrelation is phi to the k. <bookmark mark='c'/> Iterate "
            "forward, and the forecast decays toward the mean at the same rate, which gives the half-life. <bookmark "
            "mark='d'/> To test whether anything is left, Greta Ljung and George Box summed the squared "
            "autocorrelations of the residuals: asymptotically chi-squared under suitable white-noise assumptions; adjust the degrees of freedom for fitted ARMA residuals. <bookmark mark='e'/> And Herman Wold "
            "proved in 1938 that every centered, purely nondeterministic covariance-stationary series is a moving average of its past surprises; ARMA writes those "
            "weights compactly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            vo.wait_until("e")
            self.play(FadeIn(wold))
        self.wait(0.3)
        self.clear_scene()

    def identify(self):
        def panel(title, vals, col):
            g = axes([0, 9], [-0.6, 1], x_length=2.8, y_length=1.8, xticks=[], yticks=[0, 1], ylabel=title, font_size=14)
            b = VGroup(*[Line(g.ax.c2p(k, 0), g.ax.c2p(k, v), stroke_width=6, color=col) for k, v in enumerate(vals, 1)])
            return VGroup(g, b)

        th, ph = 0.7, 0.7
        acf_ma = [th / (1 + th ** 2)] + [0.0] * 7
        pacf_ma = [-(-th) ** k * (1 - th ** 2) / (1 - th ** (2 * (k + 1))) for k in range(1, 9)]
        acf_ar = [ph ** k for k in range(1, 9)]
        pacf_ar = [ph] + [0.0] * 7
        grid = VGroup(panel(r"AR(1): ACF", acf_ar, VOL), panel(r"AR(1): PACF", pacf_ar, VOL),
                      panel(r"MA(1): ACF", acf_ma, ALT), panel(r"MA(1): PACF", pacf_ma, ALT))
        grid.arrange_in_grid(rows=2, cols=2, buff=(0.6, 0.6)).to_edge(LEFT, buff=0.6)
        nodes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=0.8, corner_radius=0.15, stroke_color=c,
                                                 fill_color=c, fill_opacity=0.15),
                                label(t, font_size=24, color=c)) for t, c in
                         ((r"identify", VOL), (r"estimate", FC), (r"check", GOOD))])
        for nd in nodes:
            nd[1].move_to(nd[0])
        nodes[0].move_to(RIGHT * 3.6 + UP * 1.9)
        nodes[1].move_to(RIGHT * 5.4 + DOWN * 0.3)
        nodes[2].move_to(RIGHT * 1.8 + DOWN * 0.3)
        arrows = VGroup(*[CurvedArrow(nodes[i].get_center() + 0.5 * (nodes[(i + 1) % 3].get_center() - nodes[i].get_center()) / 2,
                                      nodes[(i + 1) % 3].get_center() - 0.5 * (nodes[(i + 1) % 3].get_center() - nodes[i].get_center()) / 2,
                                      angle=-0.6, color=GREY_B, stroke_width=3) for i in range(3)])
        cap = wrapped_label(r"Box and Jenkins (1970): read the shape of the ACF and PACF, fit by least squares, test "
                            r"the residuals; loop while checking the remaining dependence", 5.6, 20, GREY_A)
        cap.next_to(VGroup(nodes, arrows), DOWN, buff=0.5)
        with self.voiceover(
            "How do you tell which model you have? By the fingerprints. An autoregression's autocorrelations decay "
            "slowly, but its partial autocorrelations, the correlation left after accounting for shorter lags, stop "
            "dead after lag p. A moving average is the mirror image: its autocorrelations stop after lag q. <bookmark "
            "mark='a'/> Box and Jenkins turned that into a loop. Identify a candidate from the fingerprints, estimate "
            "it, check the residuals with the Ljung-Box test, and look for remaining dependence; passing one test does not prove independence. The spectrum "
            "carries the same information in frequency; this part stays in time."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p_) for p_ in grid], lag_ratio=0.3, run_time=3))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(nd) for nd in nodes], lag_ratio=0.3),
                      LaggedStart(*[Create(a_) for a_ in arrows], lag_ratio=0.3), FadeIn(cap), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    def lab(self, a):
        card = lab_card(r"an autoregression by least squares", [
            "def ar_fit(x, p=1):",
            "    X = np.column_stack([np.ones(len(x) - p)] +",
            "        [x[p-k-1:len(x)-k-1] for k in range(p)])",
            "    y = x[p:]",
            "    beta, *_ = np.linalg.lstsq(X, y, rcond=None)",
            "    resid = y - X @ beta",
            "    return {'beta': beta, 'resid': resid}",
        ], source="explainer/quant/house/vol.py", width=6.4).to_corner(UL, buff=0.35)
        self.play(FadeIn(card))
        best = a["best"]
        with self.voiceover(
            "Lab. The House's autoregression: lagged values and least squares. Run it on the "
            f"logarithm of the VIX, {a['n_vix']:,} trading days from 1990 to 2020. <bookmark mark='a'/> Phi comes out "
            f"at {a['ar1_phi']:.3f}: fear decays with a half-life of about {a['ar1_half_life']:.0f} trading days."
        ) as vo:
            vo.wait_until("a")
            lab_run(self, card, [">>> c, phi = ar_fit(np.log(vix), 1)['beta']",
                                 f"phi = {a['ar1_phi']:.3f}",
                                 f"half-life = log(0.5) / log(phi) = {a['ar1_half_life']:.0f} days"])
        rows = sorted(a["table"], key=lambda r_: r_["aic"])[:5]
        tab = VGroup(*[VGroup(MathTex(rf"\text{{ARMA}}({r_['p']},{r_['q']})", font_size=26,
                                      color=GOOD if (r_["p"], r_["q"]) == (best["p"], best["q"]) else WHITE),
                              MathTex(f"{r_['aic']:,.1f}".replace(",", "{,}"), font_size=26, color=GREY_A))
                       for r_ in rows])
        for r_ in tab:
            r_.arrange(RIGHT, buff=0.6)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        head = label(r"conditional-Gaussian AIC on log VIX (candidate set)", font_size=20, color=GREY_A)
        lb = a["lb"]
        side = VGroup(head, tab,
                      label(rf"best: ARMA({best['p']},{best['q']}); Ljung--Box on its residuals: "
                            rf"$Q_{{20}} = {a['best_lb']['Q']:.0f}$", font_size=20, color=GREY_A),
                      label(r"US daily returns, Ljung--Box, 20 lags:", font_size=20, color=GREY_A),
                      MathTex(rf"r_t:\ Q = {lb['r']['Q']:.0f} \qquad r_t^2:\ Q = {lb['sq']['Q']:,.0f}".replace(",", "{,}"),
                              font_size=30, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        side.to_edge(RIGHT, buff=0.4).shift(UP * 0.2)
        if side.width > 6.4:
            side.scale_to_fit_width(6.4)
        pc = predict(r"As $\phi \to 1$, what happens to the variance and the half-life?", width=6.2, font_size=22)
        pc.to_corner(DL, buff=0.35)
        ratio = lb["sq"]["Q"] / lb["r"]["Q"]
        with self.voiceover(
            "Let the Akaike criterion choose among candidates. "
            f"ARMA({best['p']},{best['q']}) wins, but its residuals still fail the Ljung-Box test: serial dependence remains in this limited candidate set; that alone does not establish long memory. <bookmark mark='a'/> "
            "Last, Ljung-Box on ninety-four years of daily returns: "
            f"Q is {lb['r']['Q']:.0f}, a raw Ljung--Box statistic whose usual calibration needs stronger assumptions than zero correlation under changing volatility. On squared "
            f"returns, Q is {lb['sq']['Q']:,.0f}, about {ratio:.0f} times larger. The level barely remembers; the "
            "size remembers enormously. <bookmark mark='b'/> Pause and predict: as phi goes to one, what happens to "
            "the variance and the half-life? Both go to infinity, and that is the next chapter."
        ) as vo:
            self.play(FadeIn(side[0]), LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(pc))
        self.wait(0.3)
        self.clear_scene()
