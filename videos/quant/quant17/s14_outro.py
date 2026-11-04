from __future__ import annotations

import numpy as np

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
    (r"Your deep hedger makes money on average with no costs. Is it hedging?",
     r"partly it is speculating: under a real-world drift the exponential-utility hedge is delta plus Merton's "
     r"$\mu / \gamma\sigma^2 S$. Compare its holdings with delta on driftless paths, price it on driftless paths, and "
     r"train under a (near-)martingale measure if the drift is not a view you want to hold"),
]

PROBLEMS = [
    r"Show that the entropic risk $\rho(X) = \frac1\gamma \log \mathbb{E} e^{-\gamma X}$ satisfies $\rho(X + c) = "
    r"\rho(X) - c$, and conclude that $\min_\delta \rho(-Z + (\delta\cdot S)_T - C_T)$ is the seller's indifference price.",
    r"Heuristically derive the scaling $(c\,\Gamma^2/\gamma)^{1/3}$ of the no-trade band by balancing the quadratic cost "
    r"of mis-hedging against the linear cost of trading.",
    r"Let $u$ solve the pricing PDE. Use It\^o's formula to show that $Y_t = u(t, X_t)$, $Z_t = \sigma X_t \nabla u$ "
    r"solve the BSDE $dY = f(Y)\,dt + Z\,dW$ with $f(y) = (1 - \delta) Q(y) y + R y$.",
    r"For a linear model $f(x) = w^\top \phi(x)$, write the normal equations of differential regression with weight "
    r"$\lambda$ on the derivative labels.",
    r"Show that the deep stopping objective at date $n$ is maximized by stopping when $g_n \ge \mathbb{E}[G_{n+1} \mid "
    r"X_n]$, and that every stopping rule's expected payoff is a lower bound on the Bermudan price.",
    r"Derive Leland's volatility $\hat\sigma^2 = \sigma^2\big(1 + \sqrt{2/\pi}\,k / (\sigma\sqrt{\Delta t})\big)$ from "
    r"the expected cost of rebalancing a delta hedge every $\Delta t$.",
    r"Show that in a complete market with zero rates the exponential-utility hedge of a claim under drift $\mu$ is "
    r"$\delta^* = \Delta + \mu / (\gamma\sigma^2 S)$.",
    r"Labels with Monte Carlo variance $s^2$: show that a held-out error against them is at least $s$, and explain why "
    r"doubling $s^2$ need not double the network's error against the truth.",    r"(qual) For $dY = RY\,dt + Z\cdot dW$, $Y_0 = y_0$, and $g = e^{RT}u_0 + \int e^{R(T-t)}Z^*\cdot dW$, show "
    r"$\mathbb E|Y_T - g|^2 = e^{2RT}(y_0 - u_0)^2 + \mathbb E\int e^{2R(T-t)}|Z - Z^*|^2dt$ for adapted $Z$.",
    r"(qual) With $Z$ constant on each of $N$ steps, show the loss cannot fall below $\min_{Z \text{ step}}\mathbb E\int "
    r"|Z - Z^*|^2dt$, and that this is $O(1/N)$ when $Z^*$ is $\frac12$-H\"older in mean square.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("hlp"), load("calib"), load("calib_hist"), load("dml"), load("bsde"), load("stopping"),
                   load("hedge"), load("nsde"), load("greeks_act"), load("calib_noise"), load("bsde_seeds"),
                   load("drift"), load("crossgen"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, hl, c, ch, d, b, st, h, n, ga, nz, bs, dr, cg):
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
            (rf"$H$ week by week: at the box's floor, 0.02, in {100 * floor:.0f}\% of weeks; a near tie with Heston", IV),
            (r"derivatives as labels, and a Gaussian process that uses them exactly", GOOD),
            (rf"100 dimensions: the deep BSDE gives {t0['mean']:.2f} $\pm$ {t0['sd']:.2f} against {b['reference']:.1f}", NET),
            (rf"deep stopping: {st['5']['lower']:.2f}, level with Longstaff--Schwartz, below the published bounds", NET),
            (rf"the deep hedger: an indifference price; under drift it holds Merton's extra {devs:.3f} shares", DELTA),
            (rf"it learns where not to trade; at {100 * hi['cost']:g}\% costs it needs {hi['deep']['price']:.2f}, not "
             rf"{hi['delta']['price']:.2f}", DELTA),
            (rf"the same vanillas leave a barrier free between {n['low']['doc']:.3f} and {n['high']['doc']:.3f}", BAD),
            (r"generators invent markets; a hedger is tested across them and on history (Rule 17)", BAD),
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
            "Part seventeen in eleven lines. A network learns a pricing formula from prices, but its Greeks are only "
            "as good as its activation. A network calibrates a rough model in seconds, every week, and its training "
            "box has walls. Derivatives make better labels, and a Gaussian process uses them exactly, at a cost. Deep "
            "networks price in a hundred dimensions and learn when to exercise. The deep hedger's objective is an "
            "indifference price; under a drift it rediscovers Merton and speculates; with costs it learns where not "
            "to trade. Neural models measure model risk. And generators invent markets, on which every hedger must be "
            "tested, alongside history."
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
            "Three desk questions. Why does a hedger with costs have a band? Because straying from delta adds risk "
            "that grows with the square of the gap, while trading back costs in proportion to it: small gaps are "
            "cheaper to keep. <bookmark mark='a'/> How do you know a neural calibration is right? Re-price it with the "
            "slow engine, and check its inputs are inside the region it learned. <bookmark mark='b'/> And why record "
            "the derivatives of simulated payoffs? Because each one is another label, nearly free with adjoints, and "
            "they fix the shape between samples. <bookmark mark='c'/> And if your deep hedger makes money on average "
            "with no costs, is it hedging? Partly it is betting on the drift: compare it with delta on driftless "
            "paths, and train under a martingale measure unless the bet is one you mean to hold. Full solutions are "
            "in the notes."
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
            "And ten problems: the indifference price, the band's scaling, the BSDE behind the deep solver, "
            "differential regression, why deep stopping gives a lower bound, Leland's volatility, Merton's term in the "
            "hedge, and what label noise does to a calibrator. Two are qualifying-exam problems: the loss "
            "decomposition, and its floor. Solutions, in English and Chinese, are in the notes."
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
            "The textbook chapters this part covers, and the papers it draws on, from Leland's costs in 1985 to the "
            "generative option markets of 2026. Ruf and Wang counted well over a hundred papers on networks for "
            "pricing and hedging by 2020; the notes map each one used here to its chapter. Every network here was "
            "trained on one shared CPU, several times over; the production version retrains them at full size."
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
