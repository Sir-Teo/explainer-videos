from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, IV, NET, OPT, PART, load

DESK = [
    (r"Your hedger has costs. Why does the optimal hedge have a band?",
     r"straying from delta by $\epsilon$ adds hedging risk of order $\epsilon^2$; trading back costs of order $\epsilon$. "
     r"Small deviations are cheaper to keep than to fix, so the hedger waits until the risk pays for the trade: a band of "
     r"half-width about $(3 c S \Gamma^2 / 2\gamma)^{1/3}$ (Whalley and Wilmott), widest where gamma is large"),
    (r"A neural calibrator fits the surface beautifully. How do you know it is right?",
     r"re-price the calibrated parameters by the slow engine (fresh Monte Carlo) and compare; check every input lies "
     r"inside the training ranges; know its held-out error and the noise of its own labels. A network extrapolates "
     r"silently, so the check is not optional"),
    (r"You have a thousand simulated payoffs. Why also record their derivatives?",
     r"each sample then carries one label per input, at the cost of about one extra pricing by adjoint differentiation; "
     r"the slopes pin down the function's shape between samples, so the price and, above all, the Greeks need far fewer "
     r"samples (Huge and Savine 2020)"),
]

PROBLEMS = [
    r"Show that the entropic risk $\rho(X) = \frac1\gamma \log \mathbb{E} e^{-\gamma X}$ satisfies $\rho(X + c) = "
    r"\rho(X) - c$, and conclude that $\min_\delta \rho(-Z + (\delta\cdot S)_T - C_T)$ is the seller's indifference price.",
    r"Heuristically derive the scaling $(c\,\Gamma^2/\gamma)^{1/3}$ of the no-trade band by balancing the quadratic cost "
    r"of mis-hedging against the linear cost of trading.",
    r"Let $u$ solve the pricing PDE. Use It\^o's formula to show that $Y_t = u(t, X_t)$, $Z_t = \sigma X_t \nabla u$ "
    r"solve the BSDE $dY = -f\,dt + Z\,dW$.",
    r"For a linear model $f(x) = w^\top \phi(x)$, write the normal equations of differential regression with weight "
    r"$\lambda$ on the derivative labels.",
    r"Show that the deep stopping objective at date $n$ is maximized by stopping when $g_n \ge \mathbb{E}[G_{n+1} \mid "
    r"X_n]$, and that every stopping rule's expected payoff is a lower bound on the Bermudan price.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("hlp"), load("calib"), load("calib_hist"), load("dml"), load("bsde"), load("stopping"),
                   load("hedge"), load("nsde"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, hl, c, ch, d, b, st, h, n):
        r0 = {(r["n"], r["differential"]): r for r in d["rows"]}
        n0 = min(r["n"] for r in d["rows"])
        dg = r0[(n0, False)]["delta_rmse"] / r0[(n0, True)]["delta_rmse"]
        hi = h["band"]["rows"][-1]
        floor = sum(r["H"] < 0.021 for r in ch["rows"]) / len(ch["rows"])
        items = [
            (r"a network learns Black--Scholes from prices, and hedges with it (HLP 1994)", NET),
            (rf"rough Bergomi calibrated in {c['surface']['seconds']:.0f} s through a network; checked by Monte Carlo", IV),
            (rf"$H$ week by week: rougher than 0.02 in {100 * floor:.0f}\% of weeks; over two years, a near tie with Heston", IV),
            (rf"derivatives as labels: {dg:.0f} times better deltas from {n0} samples", GOOD),
            (rf"100 dimensions: the deep BSDE prices within {100 * b['rel_error']:.1f}\% of the reference", NET),
            (rf"deep stopping: {st['5']['lower']:.2f} for the five-asset max-call", NET),
            (rf"the deep hedger rediscovers the no-trade band; at {100 * hi['cost']:g}\% costs it needs "
             rf"{hi['deep']['price']:.2f}, not {hi['delta']['price']:.2f}", DELTA),
            (rf"the same vanillas leave a barrier free between {n['low']['doc']:.3f} and {n['high']['doc']:.3f}", BAD),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 17 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part seventeen in eight lines. A network can learn a pricing formula from prices. It can learn a model's "
            "smile and calibrate it in seconds, every week, which shows that one good day is not a model. Derivatives make better labels than prices alone. Deep "
            "networks price in a hundred dimensions and learn when to exercise. The deep hedger finds the no-trade "
            "band, and with costs it is far cheaper than hedging to delta every day. And neural models measure how "
            "much the vanillas leave an exotic's price undecided."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. Why does a hedger with costs have a band? Because straying from delta adds risk "
            "that grows with the square of the gap, while trading back costs in proportion to it: small gaps are "
            "cheaper to keep. <bookmark mark='a'/> How do you know a neural calibration is right? Re-price it with the "
            "slow engine, and check its inputs are inside the region it learned. <bookmark mark='b'/> And why record "
            "the derivatives of simulated payoffs? Because each one is another label, nearly free with adjoints, and "
            "they fix the shape between samples. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "And five problems: the indifference price, the band's scaling, the BSDE behind the deep solver, "
            "differential regression, and why deep stopping gives a lower bound. Solutions, in English and Chinese, "
            "are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"exposures for XVA learned by differential regression", [21]),
            (r"generators that make backtests honest, and overfitting they can hide", [26]),
            (r"machine learning for returns, with the same validation discipline", [27]),
            (r"the finale's stress test, run on the market generator", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part twenty-one learns exposures for valuation adjustments by differential "
            "regression. Part twenty-six uses generators to test backtests, and Part twenty-seven turns machine "
            "learning on returns, under the same discipline. And the finale stress-tests the whole House with the "
            "market generator."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Dixon, Halperin and Bilokon, \textit{Machine Learning in Finance}; Kelly and Xiu, \textit{Financial "
             r"Machine Learning}", r"Savine, \textit{Modern Computational Finance: AAD and Parallel Simulations}"],
            [r"Hodges and Neuberger (1989); Hutchinson, Lo and Poggio (1994); Whalley and Wilmott (1997)",
             r"Han, Jentzen and E (2018); Becker, Cheridito and Jentzen (2019); Buehler, Gonon, Teichmann and Wood (2019)",
             r"Huge and Savine (2020); Wiese et al.\ (2020); Buehler, Horvath, Lyons, Perez Arribas and Wood (2020)",
             r"Horvath, Muguruza and Tomas (2021); Imaki et al.\ (2021); Ni et al.\ (2021); Gierjatowicz et al.\ (2022)",
             r"Federal Reserve and OCC, SR 11-7 (2011)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every network here was trained on one "
            "CPU; the production version retrains them at full size."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("vol", "research"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 18, Money, Bonds and the Curve", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "That closes the House's volatility desk: from Black–Scholes to networks that learn to hedge. "
            "<bookmark mark='a'/> Next, Part eighteen: money, bonds and the curve. The rates desk opens, and the price "
            "of time itself becomes the thing that moves."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
