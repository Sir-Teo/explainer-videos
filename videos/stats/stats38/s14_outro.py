from __future__ import annotations

from videos.stats.stats38.common import *  # noqa: F403

PROBLEMS = [
    r"For Gaussian white noise, \ show that periodogram ordinates at distinct Fourier frequencies are independent $\sigma^2 \cdot$ Exp(1).",
    r"For $\Delta x_t = \gamma x_{t-1} + \varepsilon_t$ with $\gamma = 0$, \ show $\frac{1}{T}\sum x_{t-1}\varepsilon_t = \frac{\sigma^2}{2}(x_T^2/(\sigma^2 T) - \hat\sigma^2/\sigma^2)$ approximately.",
    r"For GARCH(1,1), \ show $E\sigma_t^2 = \omega/(1-\alpha-\beta)$ and that $\varepsilon_t^2$ follows an ARMA(1,1).",
    r"For ARFIMA$(0,d,0)$, \ show $\rho_1 = d/(1-d)$.",
    r"Local level: \ show the gain is $K = P/(P + R)$, \ and find the steady-state $P$ in terms of $q/r$.",
    r"For an AR(1), \ show $n\,\text{Var}(\bar X_n) \to \sigma_X^2 (1+\phi)/(1-\phi)$.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.upgrade()
        self.payoffs()
        self.problems()
        self.references()
        self.transcript()

    def recap(self):
        items = [
            (r"Hurst: \ the Nile's range grows like $n^{0.85}$", LMC), (r"Wold, \ and four ways to leave Part 17", GREY_A),
            (r"spectra: \ smooth the periodogram; \ 11 years", SPECC), (r"unit roots: \ Dickey--Fuller, \ not the normal", MISSC),
            (r"spurious regression; \ cointegration", MISSC), (r"GARCH: \ the variance remembers", VOLC),
            (r"long memory: \ $d$, \ $H$, \ an uncertain mean", LMC), (r"Kalman: \ Gaussian conditioning, \ one step at a time", STATEC),
            (r"smoothing, \ likelihood, \ EM; \ Apollo", STATEC), (r"EKF, \ UKF, \ particles; \ Hamilton's regimes", STATEC),
            (r"VARs, \ Granger, \ impulse responses", TAUC), (r"block bootstraps; \ honest forecasting", BANDC),
        ]
        rows = VGroup(*[label(rf"{i}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:6]).arrange(DOWN, aligned_edge=LEFT, buff=0.45),
                      VGroup(*rows[6:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 38, \ in twelve lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part thirty-eight in twelve lines. <bookmark mark='a'/> Hurst found the Nile's range growing faster than "
            "independence allows. Wold's theorem frames four ways to leave Part seventeen's world. The spectrum spreads a "
            "series' variance over frequencies, and its estimate must be smoothed; the sunspots cycle every eleven years. A "
            "unit root's test statistic is not normal, and Dickey and Fuller's tables replace the t table. Regressions of "
            "one random walk on another lie, unless the walks are cointegrated. GARCH lets the variance remember its past. "
            "Long memory makes the mean far less certain than it looks. Kalman's filter tracks a hidden state by Gaussian "
            "conditioning, step by step; the smoother uses the future, and the likelihood or EM learns the noise. Extended, "
            "unscented and particle filters handle nonlinearity, and Hamilton's filter finds recessions. Vector "
            "autoregressions forecast several series together, with causal claims only under identifying assumptions. And "
            "block bootstraps and honest evaluation keep the inference and the forecasts truthful."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=40.0)
        self.clear_scene()

    def upgrade(self):
        card = upgrade_card(38, r"dependence in time: \ spectra, \ unit roots, \ volatility, \ hidden states",
                            r"one dimension of dependence, \ ordered, \ in one direction",
                            r"Part 39: \ dependence in space, \ in every direction: \ variograms, \ kriging, \ point patterns")
        with self.voiceover(
            "<bookmark mark='a'/> A promise for later. This part handled dependence in time. <bookmark mark='b'/> Time has "
            "one dimension and one direction, the past, which is what makes filtering possible. <bookmark mark='c'/> Part "
            "thirty-nine moves to space, where dependence runs in every direction at once: variograms, kriging, which is "
            "the Kalman smoother's cousin, and point patterns."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card[0]), FadeIn(card[1][0]), FadeIn(card[1][1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1][1]))
            vo.wait_until("c")
            self.play(FadeIn(card[1][1][2]))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"dependence in space: \ kriging", [39]), (r"EM and missing data", [41]), (r"Brownian motion and Donsker", [44]),
            (r"nonstandard limits", [47]), (r"Gaussian processes", [53]), (r"sequential, \ anytime-valid inference", [58]),
            (r"nonstationarity as distribution shift", [60]), (r"pretrained forecasters, \ honestly", [64]),
        ], font_size=22)
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> Part thirty-nine takes dependence into space. Part forty-one uses EM "
            "for missing data. Part forty-four proves the functional central limit theorem behind Dickey and Fuller. Part "
            "forty-seven studies non-standard limits. Part fifty-three uses Gaussian processes, the continuous cousins of "
            "state space models. Part fifty-eight makes sequential inference valid at every time. Part sixty treats "
            "nonstationarity as distribution shift. And Part sixty-four returns to large pretrained models."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=20)
        with self.voiceover(
            "Six problems, with full solutions in the README. <bookmark mark='a'/> The periodogram of white noise; the "
            "Dickey-Fuller numerator; GARCH's stationary variance and its ARMA form; the first autocorrelation of "
            "fractional noise; the Kalman gain for a local level and its steady state; and the long-run variance of an "
            "autoregressive mean. Pause here if you want to try them."
        ) as vo:
            self.play(FadeIn(ps.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in ps.rows], lag_ratio=0.3), run_time=4.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"R. Shumway \& D. Stoffer, \emph{Time Series Analysis and Its Applications} (4th ed. 2017)",
             r"J. Hamilton, \emph{Time Series Analysis} (1994); \ P. Brockwell \& R. Davis, \emph{Time Series: Theory and Methods} (1991)",
             r"J. Durbin \& S. J. Koopman, \emph{Time Series Analysis by State Space Methods} (2nd ed. 2012)",
             r"J. Beran, \emph{Statistics for Long-Memory Processes} (1994); \ R. Hyndman \& G. Athanasopoulos, \emph{FPP} (3rd ed.)"],
            [r"H. Hurst (1951); \ R. Kalman (1960); \ H. Rauch, F. Tung \& C. Striebel (1965); \ P. Welch (1967); \ C. Granger (1969)",
             r"D. Dickey \& W. Fuller (1979); \ C. Sims (1980); \ C. Granger \& R. Joyeux (1980); \ R. Engle (1982); \ D. Thomson (1982)",
             r"T. Bollerslev (1986); \ R. Engle \& C. Granger (1987); \ S. Johansen (1988); \ J. Hamilton (1989); \ H. K\"unsch (1989)",
             r"D. Kwiatkowski et al. (1992); \ N. Gordon et al. (1993); \ D. Politis \& J. Romano (1994); \ S. Julier \& J. Uhlmann (1997)"])
        with self.voiceover(
            "The books this part follows: Shumway and Stoffer; Hamilton's Time Series Analysis and Brockwell and Davis; "
            "Durbin and Koopman on state space methods; Beran on long memory, and Hyndman and Athanasopoulos on forecasting; "
            "with the papers from Hurst to Julier and Uhlmann."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=38, current=None)
        nxt = VGroup(label(r"Part 39", font_size=30, color=GREY_B), label(r"Space", font_size=48),
                     label(r"variograms, \ kriging, \ point patterns, \ and disease maps", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Thirty-eight parts of sixty-five. <bookmark mark='a'/> A series remembers its past, sometimes for centuries, and "
            "the thing we care about is often hidden beneath it. <bookmark mark='b'/> Next, dependence in every direction: "
            "Part thirty-nine, space."
        ) as vo:
            self.play(FadeIn(tr))
            vo.wait_until("a")
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(38)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
