from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, DELTA, GOOD, IV, NET, OPT, PART, load

DESK = [
    (r"Why does a small-cost hedge have a band?",
     r"in the reflected-gap approximation, risk costs $A h^2$ per unit time and turnover costs $B c/h$; minimizing their sum gives $h\propto c^{1/3}$, under the asymptotic assumptions"),
    (r"How do you check a neural calibration?",
     r"use independent simulation with error bars, verify the training domain, and separate surrogate, Monte Carlo, optimization and model errors; small fit error is not identification"),
    (r"Why record payoff derivatives?",
     r"valid pathwise derivatives add correlated slope labels at modest adjoint cost; justify differentiation under expectation, especially at discontinuous payoffs"),
    (r"Does average hedge profit prove better replication?",
     r"no: drift and the risk objective can introduce investment demand; compare exposures and risk under stated measures, with the appropriate no-claim baseline"),
]

PROBLEMS = [
    r"For finite entropic risk, prove cash invariance and derive the seller's premium as the optimized short-claim risk minus the optimized no-claim risk. When is the second term zero?",
    r"For a reflected hedge gap with variance rate $a^2$, derive total turnover $a^2/(2h)$ and minimize $\gamma\sigma^2S^2h^2/6+cS a^2/(2h)$. State the small-cost assumptions.",
    r"Use It\^o's formula and the pricing PDE to obtain $dY=f(Y)dt+Z\cdot dW$, with $Y=u(t,X)$ and $Z_i=\sigma X_i\partial_i u$; distinguish $Z$ from share holdings.",
    r"Write the normal equations for linear differential regression with price-feature matrix $\Phi$, derivative-feature matrices $D_j$, and derivative weight $\lambda$.",
    r"Derive the date-$n$ stopping decision from the conditional continuation value. Why is a fixed rule's expected discounted payoff a lower bound, but its simulated sample mean need not be?",
    r"Derive Leland's volatility correction using one-way proportional cost $c$; express it also using round-trip cost $k=2c$ and state the approximation.",
    r"In the continuous-time complete constant-volatility market with zero rates and exponential utility, derive the investment overlay $\mu/(\gamma\sigma^2 S)$ for a replicable claim.",
    r"For conditionally unbiased validation labels with independent noise of variance $s^2$, derive the population MSE decomposition. Does the realized finite-sample RMSE have to exceed $s$?",
    r"(qual) For the continuous linear BSDE, prove $L_{\rm pop}=e^{2RT}(y_0-u_0)^2+\mathbb E\int_0^T e^{2R(T-t)}|Z-Z^*|^2dt$, under square-integrability assumptions.",
    r"(qual) For predictable left-endpoint step controls, derive an $O(h)$ upper bound on the continuous population control-error floor under mean-square half-H\"older regularity. Does this prove an exact $1/N$ floor or certify Euler batch loss?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("hlp"), load("calib"), load("calib_hist"), load("dml"), load("bsde"), load("stopping"),
                   load("hedge"), load("nsde"), load("greeks_act"), load("calib_noise"), load("bsde_seeds"),
                   load("drift"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, hl, c, ch, d, b, st, h, n, ga, nz, bs, dr):
        trace = load("nsde_trace")
        n = dict(n, low=trace["low"], high=trace["high"])
        floor = sum(r["H"] < 0.021 for r in ch["rows"]) / len(ch["rows"])
        hi = h["band"]["rows"][-1]
        gr = float(np.mean([ga["runs"][f"ReLU_{s}"]["gamma_rmse"] for s in (0, 1)]) /
                   np.mean([ga["runs"][f"SiLU_{s}"]["gamma_rmse"] for s in (0, 1)]))
        t0 = bs["tail0"]
        devs = float(np.mean([r["dev"] for r in dr["rows"]]))
        items = [
            (r"a network learns Black--Scholes from prices, and hedges with it (HLP 1994)", NET),
            (rf"its Greeks depend on the activation: ReLU's gamma error is {gr:.0f} times SiLU's", NET),
            (rf"the neural calibrator: {nz['net_fresh']['rmse']:.2f} vol points from fresh simulation; the Surface in "
             rf"{c['surface']['seconds']:.0f} s", IV),
            (rf"$H$ week by week: near the box's floor ($H<0.021$) in {100 * floor:.0f}\% of weeks; descriptive constrained fits, not identification", IV),
            (r"derivative labels and a Gaussian working model with finite features", GOOD),
            (rf"100 dimensions: the deep BSDE gives {t0['mean']:.2f} $\pm$ {t0['sd']:.2f} against {b['reference']:.1f}", NET),
            (rf"deep stopping: {st['5']['lower']:.2f}, a simulated policy mean; published results have different budgets", NET),
            (rf"finite-sample hedger risk; under drift, average extra holdings {devs:.3f} shares", DELTA),
            (rf"it learns where not to trade; at {100 * hi['cost']:g}\% costs it needs {hi['deep']['price']:.2f}, not "
             rf"{hi['delta']['price']:.2f}", DELTA),
            (rf"penalized barrier candidates, not bounds: {n['low']['doc']:.3f} and {n['high']['doc']:.3f}", BAD),
            (r"Gaussian reverse illustration; cross-generator history validation remains a plan", BAD),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        title = label(r"Part 17 in eleven lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.6:
            rows.scale_to_fit_height(6.6)
        with self.voiceover(
            'The main results are conditional numerical demonstrations. Networks approximate prices, but smoothness does not enforce correct Greeks or convexity. Calibration has label noise, domain limits and optimizer error. Differential labels add correlated information; a Gaussian process adds chosen statistical assumptions. High-dimensional BSDE and stopping solvers still have discretization, training and simulation error. Hedger entries are empirical risk objectives; an indifference premium requires its no-claim baseline. Band priors constrain the policy class. Penalized neural-SDE candidates illustrate sensitivity without certified robust bounds. Finally, the Gaussian reverse illustration is analytical, while the disjoint-history cross-generator test remains a validation plan.'
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=22))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Four desk questions. The cube-root band balances a quadratic risk cost against turnover proportional to the inverse width, not a static quadratic-versus-linear comparison. <bookmark mark='a'/> Check a neural calibration with independent simulation and uncertainty, domain checks, and a decomposition of errors. <bookmark mark='b'/> Derivative labels help when their unbiasedness and computational cost are justified; discontinuous payoffs require special care. <bookmark mark='c'/> Average profit does not prove better replication. Separate investment demand from hedging, and include the optimized no-claim baseline when deriving an indifference premium. The bilingual notes give the details."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[3], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19)
        with self.voiceover(
            "The ten exercises cover cash baselines, reflected-band turnover, the BSDE hedge units, differential regression, stopping bounds, Leland's cost convention, Merton's investment term and validation-label noise. The two qualifying problems distinguish continuous population loss from Euler training loss, and an order-h upper bound from an exact rate. Complete English and Chinese solutions are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
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
            [r"Dixon, Halperin and Bilokon, \textit{Machine Learning in Finance} (ch.\ 1, 3--5, 8, 10, 12); Kelly and "
             r"Xiu, \textit{Financial Machine Learning}", r"Savine, \textit{Modern Computational Finance}; Jentzen, "
             r"Kuckuck and von Wurstemberger, \textit{Mathematical Introduction to Deep Learning}"],
            [r"Leland (1985); Hodges and Neuberger (1989); Cybenko (1989); Pardoux and Peng (1990); Davis, Panas and "
             r"Zariphopoulou (1993); Hutchinson, Lo and Poggio (1994); Whalley and Wilmott (1997); Rockafellar and "
             r"Uryasev (2000)",
             r"Hernandez (2016); E, Han and Jentzen (2017); Han, Jentzen and E (2018); Sirignano and Spiliopoulos (2018); "
             r"Bayer and Stemper (2018); Becker, Cheridito and Jentzen (2019); Buehler, Gonon, Teichmann and Wood (2019)",
             r"Huge and Savine (2020); Ruf and Wang (2020); Wiese et al.\ (2020); Buehler, Horvath, Lyons, Perez Arribas "
             r"and Wood (2020); Ho, Jain and Abbeel (2020); Cuchiero, Khosrawi and Teichmann (2020)",
             r"Horvath, Muguruza and Tomas (2021); Imaki et al.\ (2021); Kidger et al.\ (2021); Ni et al.\ (2021); "
             r"Gierjatowicz et al.\ (2022); Chevyrev and Oberhauser (2022); Fran\c{c}ois et al.\ (2024)",
             r"Buehler et al.: SANOS, DYSANOS, GROMM (2026); Arzel and Lehdili (2026); SR 11-7 (2011); SR 26-2 (2026); "
             r"PRA SS1/23"])
        with self.voiceover(
            'The notes link the primary methods and distinguish paper results from this small CPU implementation. Fixed-seed cached runs support the numerical demonstrations reviewed here. The three legacy BTC-through-2025 jobs were deliberately not restored. Source review and sampled audio checks do not replace continuous listening to a production master.'
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
