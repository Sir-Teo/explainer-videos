from __future__ import annotations

import math

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (HURDLE, IMPACT_C, PART, SCHED_C, TWAP_C, comma, fit_right, load)


class AC(VoiceoverScene):
    def construct(self):
        a = load("ac")
        self.card()
        self.model()
        self.objective()
        self.solution()
        self.continuous()
        self.trajectories(a)
        self.frontier(a)
        self.numbers(a)
        self.lam_meaning(a)
        self.versus(a)
        self.practitioner()
        self.extensions()
        self.beyond_var()
        self.question()

    def card(self):
        c = chapter_card(5, r"Almgren and Chriss", r"How fast should a risk-averse trader sell?", part=PART)
        with self.voiceover("Chapter five. A deterministic mean-variance execution model trades expected temporary cost against price risk. Its risk-averse seller front-loads relative to TWAP under the stated positive effective-cost coefficient. Robert Almgren and Neil Chriss made this trade-off explicit; the answer depends on the model's clock, risk preference and calibration."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self):
        rows = [cmath(r"S_k", r"=", r"S_{k-1} + \sigma\sqrt\tau\,\xi_k - \gamma\,n_k", font_size=38),
                cmath(r"\tilde S_k", r"=", r"S_{k-1} - \eta\,\frac{n_k}{\tau}", font_size=38,
                      colors={r"\tilde S_k": IMPACT_C}),
                cmath(r"x_k", r"=", r"X - \textstyle\sum_{j \le k} n_j,\quad x_N = 0", font_size=36)]
        whys = [why(r"the price diffuses with volatility $\sigma$, and each sale of $n_k$ moves it down permanently by "
                    r"$\gamma n_k$"),
                why(r"the price actually received is lower by a temporary impact proportional to the trading rate"),
                why(r"holdings, sold down from $X$ to zero over $N$ intervals of length $\tau$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The discrete model. <bookmark mark='a'/> Unaffected price innovations are independent, zero mean and unit variance, with sigma in price per square root of the chosen time unit. Sales add linear permanent displacement. <bookmark mark='b'/> Execution has linear temporary rate cost, and a specified interval convention for when noise is borne. <bookmark mark='c'/> Deterministic holdings fall from X to zero. The displayed mean-variance formulas match that convention; they are not identities for arbitrary adaptive execution or jump processes."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def objective(self):
        rows = [cmath(r"\mathbb E[\text{IS}]", r"=", r"\tfrac12\gamma X^2 + \frac{\tilde\eta}{\tau}\textstyle\sum_k n_k^2",
                      font_size=36),
                cmath(r"\text{Var}[\text{IS}]", r"=", r"\sigma^2\tau \textstyle\sum_k x_k^2", font_size=38),
                cmath(r"\min_x", r"\ ", r"\mathbb E + \lambda\,\text{Var}", font_size=42, colors={r"\min_x": SCHED_C})]
        whys = [why(r"expected shortfall: the permanent part, fixed whatever the schedule (Chapter 4), and the temporary "
                    r"part, which punishes fast trading"),
                why(r"its variance: every unit still held is exposed to the price's moves, which punishes slow trading"),
                why(r"a risk aversion $\lambda$ sets the exchange rate between the two")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The objective. <bookmark mark='a'/> Expected shortfall has permanent term one half gamma X squared and temporary term eta-tilde over tau times squared trades, where eta-tilde equals eta minus gamma tau over two. Require eta-tilde positive for this strictly convex discrete problem. <bookmark mark='b'/> The variance uses post-trade holdings under the implemented noise convention, sigma squared tau times their squared sum. <bookmark mark='c'/> Minimize expected dollars plus lambda times squared-dollar variance, with nonnegative lambda. Lambda therefore has units inverse dollars."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def solution(self):
        rows = [cmath(r"x_{k+1} - 2x_k + x_{k-1}", r"=", r"(\lambda\sigma^2/\tilde\eta)\tau^2 x_k", font_size=36),
                cmath(r"x(t)", r"=", r"X\,\frac{\sinh\kappa(T - t)}{\sinh\kappa T}", font_size=42,
                      colors={r"x(t)": SCHED_C}),
                cmath(r"\kappa", r"\approx", r"\sqrt{\lambda\sigma^2/\eta}", font_size=42, colors={r"\kappa": HURDLE})]
        whys = [why(r"the first-order condition in each $x_k$: a linear second-difference equation"),
                why(r"its solution with $x_0 = X$, $x_N = 0$: a hyperbolic sine, exactly $\cosh\kappa\tau = 1 + "
                    r"\lambda\sigma^2\tau^2/(2\tilde\eta)$ on the grid"),
                why('urgency: $1/\\kappa$ is an e-folding time; long-horizon half-life is $\\log 2/\\kappa$; finite paths use the sinh equation')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The solution. <bookmark mark='a'/> Differentiation gives the displayed second-difference equation with coefficient lambda sigma squared over eta-tilde. <bookmark mark='b'/> Its exact grid solution is a hyperbolic sine with cosh kappa tau equal to one plus lambda sigma squared tau squared over twice eta-tilde. <bookmark mark='c'/> The continuous small-step approximation is kappa equal to root lambda sigma squared over eta. One over kappa is an e-folding time, not an exact half-life. In a long-horizon exponential approximation the half-life is log two over kappa; for a finite sinh path it must be solved from the path itself."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def continuous(self):
        rows = [cmath(r"\min_x", r"\ ", r"\int_0^T \big(\eta\,\dot x^2 + \lambda\sigma^2 x^2\big)\,dt", font_size=40),
                cmath(r"\eta\,\ddot x", r"=", r"\lambda\sigma^2\,x", font_size=42),
                cmath(r"x(0) = X,\ x(T) = 0", r"\Rightarrow", r"x = X\frac{\sinh\kappa(T - t)}{\sinh\kappa T}", font_size=34,
                      colors={r"x = X\frac{\sinh\kappa(T - t)}{\sinh\kappa T}": SCHED_C})]
        whys = [why(r"in continuous time: the cost of speed, $\eta\dot x^2$, against the risk of holding, "
                    r"$\lambda\sigma^2 x^2$, a Lagrangian of classical mechanics"),
                why(r"its Euler--Lagrange equation: a particle pulled toward zero by a spring of stiffness "
                    r"$\lambda\sigma^2/\eta$"),
                why(r"the boundary conditions give the hyperbolic sine; Part 8's calculus of variations, applied to "
                    r"trading")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The same answer in continuous time, by Part eight's calculus of variations. <bookmark mark='a'/> Minimise "
            "the integral of the cost of speed, eta times the rate squared, plus the cost of risk, lambda sigma squared "
            "times the holding squared. <bookmark mark='b'/> The Euler-Lagrange equation is a particle pulled toward "
            "zero by a spring. <bookmark mark='c'/> With the order full at the start and empty at the end, the solution "
            "is the hyperbolic sine."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def trajectories(self, a):
        X, T = a["X"], a["T"]
        g = axes([0, T], [0, X], x_length=6.4, y_length=4.4, xlabel=r"minutes", ylabel=r"BTC still held",
                 xticks=[0, 20, 40, 60], yticks=[0, X / 2, X], yfmt=lambda v: f"{v:,.0f}".replace(",", "{,}"),
                 font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        cols = [TWAP_C, GREY_A, SCHED_C, IMPACT_C]
        names = list(a["show"].keys())
        t = np.linspace(0, T, a["n"] + 1)
        curves = [curve(ax, t, a["show"][k]["x"], c, stroke_width=3) for k, c in zip(names, cols)]
        lam_tex = {"0": r"$\lambda = 0$ (TWAP)", "1e-07": r"$\lambda = 10^{-7}$", "1e-06": r"$\lambda = 10^{-6}$",
                   "1e-05": r"$\lambda = 10^{-5}$"}
        leg = legend([(c, lam_tex[k]) for k, c in zip(names, cols)], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "An illustrative sell of five thousand bitcoin over sixty one-minute intervals. Volatility is obtained from minute price changes in the recorded trade spans. Temporary eta is inferred from a contemporaneous signed-volume bin by a half-move heuristic, not causally estimated execution cost. <bookmark mark='a'/> With zero risk aversion the model gives TWAP. <bookmark mark='b'/> Increasing lambda front-loads the displayed schedules. The shapes illustrate this assumed model; they are not validated forecasts of market-order costs."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(curves[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves[1:]], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def frontier(self, a):
        c = np.asarray(a["cost"], float) / 1000
        s = np.asarray(a["sd"], float) / 1000
        g = axes([0, float(np.ceil(s.max() / 50) * 50)], [0, float(np.ceil(min(c.max(), 400) / 50) * 50)], x_length=6.4,
                 y_length=4.4, xlabel=r"standard deviation of the shortfall, \$ thousands",
                 ylabel=r"expected shortfall, \$ thousands", xticks=[0, 100, 200], yticks=[0, 100, 200, 300],
                 yfmt=lambda v: f"{v:.0f}", xfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        ok = c <= 400
        cur = curve(ax, s[ok], c[ok], SCHED_C, stroke_width=3)
        tw = Dot(ax.c2p(s[0], c[0]), radius=0.09, color=TWAP_C)
        twl = label(r"TWAP", font_size=18, color=TWAP_C).next_to(tw, UP, buff=0.12)
        with self.voiceover(
            "The model's efficient frontier. <bookmark mark='a'/> Each point is a deterministic schedule's expected temporary cost against its shortfall standard deviation. The plotted family begins at a very small positive lambda, not exact zero; exact TWAP is the lambda-zero reference. <bookmark mark='b'/> Front-loading exchanges higher modeled mean cost for lower modeled variance. Near the minimum-cost schedule the first cost change is second order, while risk can fall at first order. The conclusion holds within the stated deterministic mean-variance setting."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(tw), FadeIn(twl))
            vo.wait_until("b")
            self.play(Create(cur), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def numbers(self, a):
        sh = a["show"]
        notional = a["X"] * a["price"]
        tw = sh["0"]
        mid = sh["1e-06"]
        bp_tw = 1e4 * tw["cost"] / notional
        rows = [cmath(r"\text{TWAP}", r":", rf"\${tw['cost'] / 1000:.0f}\text{{k}}\ ({bp_tw:.1f}\ \text{{bp}}),\ "
                      rf"\text{{sd}}\ \${tw['sd'] / 1000:.0f}\text{{k}}", font_size=34, colors={r"\text{TWAP}": TWAP_C}),
                cmath(r"\lambda = 10^{-6}", r":", rf"\${mid['cost'] / 1000:.0f}\text{{k}},\ \text{{sd}}\ "
                      rf"\${mid['sd'] / 1000:.0f}\text{{k}}", font_size=34, colors={r"\lambda = 10^{-6}": SCHED_C}),
                cmath(r"\text{e-folding time}", r"\approx", rf"1/\kappa = "
                      rf"{1 / math.sqrt(1e-6 * a['sigma'] ** 2 / a['eta']):.0f}\ \text{{min}}", font_size=34)]
        whys = [why(rf"selling {comma(a['X'])} BTC, \${notional / 1e6:.0f} million, evenly over the hour: the impact "
                    r"is small next to the risk of holding for an hour"),
                why('the specified lambda increases model cost and lowers model variance'),
                why('continuous e-folding time; the finite-horizon half-life is computed from the actual holdings path')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        hl = 1 / math.sqrt(1e-6 * a["sigma"] ** 2 / a["eta"])
        with self.voiceover(
            f"""The model numbers. <bookmark mark='a'/> Equal slices cost {tw['cost']/1000:.0f} thousand dollars, {bp_tw:.1f} basis points, with standard deviation {tw['sd']/1000:.0f} thousand. <bookmark mark='b'/> At lambda ten to minus six, modeled cost is {mid['cost']/1000:.0f} thousand and standard deviation {mid['sd']/1000:.0f} thousand. <bookmark mark='c'/> The continuous urgency approximation has e-folding time {hl:.0f} minutes. This is not the exact finite-horizon half-life; the exact path must be used to compute a fraction sold by any particular minute. All figures inherit the descriptive eta calibration and minute clock."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def lam_meaning(self, a):
        sd = a["show"]["1e-06"]["sd"]
        pen = 1e-6 * sd ** 2
        rows = [cmath(r"\lambda", r"=", r"10^{-6}\ \text{per dollar}", font_size=38),
                cmath(r"\lambda\,\text{Var}", r"=", rf"10^{{-6}} \times ({sd / 1000:.0f}\text{{k}})^2 \approx "
                      rf"\${pen / 1000:.0f}\text{{k}}", font_size=36, colors={r"\lambda\,\text{Var}": HURDLE}),
                cmath(r"\text{read as}", r":", r"\text{the dollars paid to remove the risk}", font_size=34)]
        whys = [why(r"risk aversion has units: dollars of expected cost per squared dollar of uncertainty"),
                why(r"at that schedule's standard deviation, the risk term is worth about this much"),
                why(r"a certainty equivalent: the desk would pay that much, in expected impact, to remove the "
                    r"uncertainty entirely")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What lambda means. <bookmark mark='a'/> It has units: dollars of expected cost per squared dollar of "
            "uncertainty. <bookmark mark='b'/> At ten to the minus six, the schedule's risk term is worth about "
            f"{pen / 1000:.0f} thousand dollars. <bookmark mark='c'/> Read it as a certainty equivalent: what the desk "
            "would pay, in expected impact, to remove the uncertainty. Choosing lambda is choosing that price."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def versus(self, a):
        notional = a["X"] * a["price"]
        frac = a["X"] / a["v_day"]
        sig_d = a["sigma_day"] / a["price"]
        sq = sig_d * math.sqrt(frac)
        bp_sq = 1e4 * sq
        bp_tw = 1e4 * a["show"]["0"]["cost"] / notional
        rows = [cmath(r"\text{Almgren--Chriss, linear}", r":", rf"{bp_tw:.1f}\ \text{{bp}}", font_size=36),
                cmath(r"\text{square root},\ Y = 1", r":", rf"\sigma_{{\text{{day}}}}\sqrt{{Q/V}} = {bp_sq:.0f}\ "
                      r"\text{bp}", font_size=36, colors={r"\text{square root},\ Y = 1": IMPACT_C}),
                cmath(r"\text{the gap}", r":", '\\text{different observables and calibrations}', font_size=36)]
        whys = [why(r"temporary impact fitted to one-minute flows, paid minute by minute and forgotten"),
                why(rf"the order is {100 * frac:.1f}\% of a day's volume, with a daily volatility of "
                    rf"{100 * sig_d:.1f}\%"),
                why(r"average temporary cost and terminal displacement use different conventions and calibrations; the gap is not an identified persistence effect")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""Compare two different quantities. <bookmark mark='a'/> The linear temporary-cost illustration gives average shortfall {bp_tw:.1f} basis points. <bookmark mark='b'/> A Y-equals-one square-root extrapolation gives terminal displacement {bp_sq:.0f} basis points for {100*frac:.1f} percent of mean recorded volume. <bookmark mark='c'/> These use different calibration and measurement conventions. Under an ideal path c root q, average impact is two-thirds of terminal displacement, before spread and fees. Persistence, rate dependence and identification also differ. The numerical gap alone cannot attribute missing costs to persistence or validate either estimate."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def practitioner(self):
        rows = [cmath(r"\text{cost}", r"\approx", r"\tfrac12\,\text{spread} + Y\sigma\sqrt{Q/V} + \text{fees}", font_size=36,
                      colors={r"\text{cost}": IMPACT_C}),
                cmath(r"h(v)", r"\propto", r"v^{3/5}", font_size=40),
                cmath(r"\text{schedule}", r":", r"\text{Almgren--Chriss shape, square-root price}", font_size=34,
                      colors={r"\text{schedule}": SCHED_C})]
        whys = [why('average-cost template: half-spread, an average-impact calibrated coefficient, and fees'),
                why(r"Almgren, Thum, Hauptmann and Li (2005) fitted temporary impact as the rate to the power 0.6 on "
                    r"Citigroup's orders, with permanent impact linear"),
                why(r"in practice: shape the schedule with the optimal-control answer, and price it with the empirical "
                    r"law")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A practical model template. <bookmark mark='a'/> An average-cost estimate may add half-spread, an average-impact coefficient times sigma root Q over V, and fees. Calibrate that coefficient for average shortfall; do not silently reuse a terminal-impact coefficient. <bookmark mark='b'/> Almgren and colleagues fitted rate-dependent temporary impact with exponent around three fifths under their data and conventions. <bookmark mark='c'/> A schedule and an empirical cost model can be combined, but their clocks, units, measurement targets and uncertainty must agree. The continuous shape is not automatically optimal for the empirical square-root surface."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def extensions(self):
        cards = VGroup(
            desk_question(r"nonlinear temporary impact", r"Almgren (2003): a power of the rate changes the curve's shape "
                          r"but keeps front-loading for risk", width=12.4, font_size=19),
            desk_question(r"risk-neutral with drift", r"Bertsimas and Lo (1998): with linear impact and a predictable "
                          r"drift, dynamic programming trades on the signal; without it, TWAP", width=12.4, font_size=19),
            desk_question(r"time-consistency", r"mean--variance schedules are re-optimised as prices move; adaptive "
                          r"versions (Almgren and Lorenz) sell faster after gains, and are not time-consistent in the "
                          r"static sense", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Three extensions. <bookmark mark='a'/> With impact a power of the rate, Almgren showed the curve changes "
            "shape but still front-loads for risk. <bookmark mark='b'/> Bertsimas and Lo, earlier, minimised expected "
            "cost alone with a predictable drift: without one, the answer is TWAP. <bookmark mark='c'/> And the "
            "mean-variance schedule is static. Almgren and Julian Lorenz showed that re-optimising as prices move, "
            "selling faster after gains, does better, at the price of time-consistency."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def beyond_var(self):
        cards = VGroup(
            desk_question(r"utility, not variance", r"Schied and Schöneborn (2009): with exponential utility the static "
                          r"schedule is optimal; with other utilities the best schedule depends on wealth and adapts",
                          width=12.4, font_size=19),
            desk_question(r"tail risk", r"minimising a conditional value at risk of the shortfall front-loads more than "
                          r"variance when price jumps are possible", width=12.4, font_size=19),
            desk_question(r"the risk aversion in practice", r"desks set urgency, not $\lambda$: a target half-life or a "
                          r"participation rate, chosen from the signal's decay and the order's share of volume",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Beyond variance. <bookmark mark='a'/> Alexander Schied and Torsten Schöneborn showed that with exponential "
            "utility the static schedule is optimal, and with other utilities the schedule adapts to wealth. "
            "<bookmark mark='b'/> Minimising a tail measure of the shortfall front-loads more when prices can jump. "
            "<bookmark mark='c'/> And in practice desks do not choose a lambda: they set an urgency, a half-life or a "
            "participation rate, from the signal's decay and the order's size."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('5. Finite-horizon urgency', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('Continuous AC: $T=60$ min, $\\lambda\\sigma^2/\\eta=0.01$ per min$^2$.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Find $\\kappa$, $x(20)/X$, and the exact finite-horizon half-life.', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause five. In continuous Almgren-Chriss, horizon sixty minutes and lambda sigma squared over eta equals point zero one per minute squared. Find kappa, the fraction held at twenty minutes, and the exact half-life using the sinh path.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
