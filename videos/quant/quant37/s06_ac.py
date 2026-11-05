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
        with self.voiceover("Chapter five, and the answer to the pause: fast at first, then slower. A seller who fears "
                            "the price's moves front-loads the sale, paying more impact to carry less risk. Robert "
                            "Almgren and Neil Chriss made that trade-off exact in two thousand."):
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
            "The model. <bookmark mark='a'/> The price diffuses, and each sale moves it down permanently in proportion. "
            "<bookmark mark='b'/> The price actually received is lower still, by a temporary impact proportional to the "
            "rate of trading. <bookmark mark='c'/> And the holdings run down from X to zero over N intervals."
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
            "The objective. <bookmark mark='a'/> The expected shortfall: the permanent part, which no schedule can "
            "change, and the temporary part, which punishes trading fast. <bookmark mark='b'/> Its variance: every unit "
            "still held is exposed to the price, which punishes trading slowly. <bookmark mark='c'/> Minimise the mean "
            "plus lambda times the variance."
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
        rows = [cmath(r"x_{k+1} - 2x_k + x_{k-1}", r"=", r"\kappa^2\tau^2\,x_k", font_size=36),
                cmath(r"x(t)", r"=", r"X\,\frac{\sinh\kappa(T - t)}{\sinh\kappa T}", font_size=42,
                      colors={r"x(t)": SCHED_C}),
                cmath(r"\kappa", r"\approx", r"\sqrt{\lambda\sigma^2/\eta}", font_size=42, colors={r"\kappa": HURDLE})]
        whys = [why(r"the first-order condition in each $x_k$: a linear second-difference equation"),
                why(r"its solution with $x_0 = X$, $x_N = 0$: a hyperbolic sine, exactly $\cosh\kappa\tau = 1 + "
                    r"\lambda\sigma^2\tau^2/(2\tilde\eta)$ on the grid"),
                why(r"the urgency: $1/\kappa$ is the order's half-life; $\lambda = 0$ gives a straight line, TWAP; large "
                    r"$\lambda$ sells almost at once")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The solution. <bookmark mark='a'/> The first-order condition in each holding is a linear second-difference "
            "equation. <bookmark mark='b'/> With the holdings pinned at X at the start and zero at the end, the "
            "solution is a hyperbolic sine. <bookmark mark='c'/> The constant kappa, the root of lambda sigma squared "
            "over eta, is the urgency: one over kappa is the order's half-life. With no risk aversion it is a straight "
            "line, TWAP; with a lot, the sale is nearly immediate."
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
            "A Bitcoin-sized example: sell five thousand bitcoin, about a hundred and thirty-five million dollars, over "
            "an hour, minute by minute, with the volatility and a temporary impact estimated from the minutes of "
            "Chapter one. <bookmark mark='a'/> With no risk aversion, a straight line. <bookmark mark='b'/> As lambda "
            "grows, the curves bow toward the start: more is sold early, and the last minutes carry little."
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
            "The efficient frontier. <bookmark mark='a'/> Each schedule is a point: its expected shortfall against its "
            "standard deviation. TWAP is the cheapest on average and the riskiest. <bookmark mark='b'/> Moving along "
            "the curve buys certainty with impact, and the first steps are cheap: near TWAP, the frontier is flat, so "
            "any risk-averse trader should front-load at least a little."
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
                cmath(r"\text{half-life}", r"=", rf"1/\kappa \approx "
                      rf"{1 / math.sqrt(1e-6 * a['sigma'] ** 2 / a['eta']):.0f}\ \text{{min}}", font_size=34)]
        whys = [why(rf"selling {comma(a['X'])} BTC, \${notional / 1e6:.0f} million, evenly over the hour: the impact "
                    r"is small next to the risk of holding for an hour"),
                why(r"a moderate risk aversion pays more impact to cut the uncertainty by a third"),
                why(r"the order's half-life at that risk aversion, in Almgren and Chriss's sense: about two-thirds is "
                    r"sold in the first twenty minutes")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        hl = 1 / math.sqrt(1e-6 * a["sigma"] ** 2 / a["eta"])
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> Selling evenly costs about "
            f"{tw['cost'] / 1000:.0f} thousand dollars of temporary impact, {bp_tw:.1f} basis points, against a standard "
            f"deviation of {tw['sd'] / 1000:.0f} thousand: risk dwarfs cost. <bookmark mark='b'/> A moderate risk aversion "
            f"pays {mid['cost'] / 1000:.0f} thousand to bring the uncertainty down to {mid['sd'] / 1000:.0f} thousand. "
            f"<bookmark mark='c'/> Its half-life is about {hl:.0f} minutes: two-thirds of the order goes in the first "
            "twenty."
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
                cmath(r"\text{the gap}", r":", r"\text{impact that accumulates}", font_size=36)]
        whys = [why(r"temporary impact fitted to one-minute flows, paid minute by minute and forgotten"),
                why(rf"the order is {100 * frac:.1f}\% of a day's volume, with a daily volatility of "
                    rf"{100 * sig_d:.1f}\%"),
                why(r"the linear model forgets each minute's impact at once; real impact persists and builds over the "
                    r"order's life (the propagator), which is what the square root measures")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "But compare the square-root law. <bookmark mark='a'/> Almgren and Chriss with a linear temporary cost "
            f"fitted to single minutes says {bp_tw:.1f} basis points. <bookmark mark='b'/> The square-root law, for an "
            f"order of {100 * frac:.1f} percent of a day's volume, says about {bp_sq:.0f}. <bookmark mark='c'/> The gap "
            "is impact that accumulates. The linear model forgets each minute's impact at once; real impact persists "
            "and builds over the order's life. The schedule's shape is still useful, but its cost must come from the "
            "square root, or from a propagator."
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
        whys = [why(r"the pre-trade estimate a desk quotes: half the spread on every share, the square root for the "
                    r"order, and the fees"),
                why(r"Almgren, Thum, Hauptmann and Li (2005) fitted temporary impact as the rate to the power 0.6 on "
                    r"Citigroup's orders, with permanent impact linear"),
                why(r"in practice: shape the schedule with the optimal-control answer, and price it with the empirical "
                    r"law")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What desks actually use. <bookmark mark='a'/> A pre-trade estimate: half the spread on every share, the "
            "square root for the order, and the fees. <bookmark mark='b'/> Almgren and colleagues fitted temporary "
            "impact on Citigroup's own orders as the trading rate to the power three-fifths, with permanent impact "
            "linear. <bookmark mark='c'/> So the practice is a hybrid: shape the schedule with the optimal-control "
            "answer, and price it with the empirical law."
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
        with self.voiceover(
            "Three extensions. <bookmark mark='a'/> With impact a power of the rate, Almgren showed the curve changes "
            "shape but still front-loads for risk. <bookmark mark='b'/> Bertsimas and Lo, earlier, minimised expected "
            "cost alone with a predictable drift: without one, the answer is TWAP. <bookmark mark='c'/> And the "
            "mean-variance schedule is static. Almgren and Julian Lorenz showed that re-optimising as prices move, "
            "selling faster after gains, does better, at the price of time-consistency."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
        with self.voiceover(
            "Beyond variance. <bookmark mark='a'/> Alexander Schied and Torsten Schöneborn showed that with exponential "
            "utility the static schedule is optimal, and with other utilities the schedule adapts to wealth. "
            "<bookmark mark='b'/> Minimising a tail measure of the shortfall front-loads more when prices can jump. "
            "<bookmark mark='c'/> And in practice desks do not choose a lambda: they set an urgency, a half-life or a "
            "participation rate, from the signal's decay and the order's size."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"impact decays exponentially, and the book recovers between trades. A risk-neutral buyer has an "
                       r"hour. Is TWAP still optimal, or should some of the order be traded in blocks?")
        with self.voiceover(
            "Pause and predict. Now impact decays: the book recovers between trades. A risk-neutral buyer has an hour. "
            "Is trading steadily still optimal, or should part of the order go in blocks?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
