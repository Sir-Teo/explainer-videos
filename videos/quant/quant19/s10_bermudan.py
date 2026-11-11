from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import BAD, GOOD, PART, VAS, ZERO, ask, fit_right, house_lab, illustration, load


class Bermudan(VoiceoverScene):
    def construct(self):
        b = load("bermudan")
        self.card()
        self.what(b)
        self.lsm()
        self.result(b)
        self.lattice(load("lattice"))
        self.boundary(b)
        self.callable(load("lattice"))
        self.sweep(b)

    def card(self):
        c = chapter_card(9, r"Bermudan swaptions", r"What is the right to choose the day worth?", lit=(2001,), part=PART)
        with self.voiceover("Chapter nine. Bermudan swaptions: the most traded exotic in rates."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def what(self, b):
        dates = np.asarray(b["dates"])
        line = NumberLine(x_range=[0, 10, 1], length=11, include_numbers=True, font_size=24).shift(UP * 0.6)
        marks = VGroup(*[Triangle(color=GOOD, fill_opacity=1).scale(0.12).rotate(PI).next_to(line.n2p(d), UP, buff=0.1)
                         for d in dates])
        end = Dot(line.n2p(10), color=BAD, radius=0.1)
        lab = VGroup(
            label(rf"a 10-non-call-1 receiver: on any anniversary from year 1 to year 9, enter a swap to year 10, "
                  rf"receiving {100 * b['K']:.2f}\% (today's par rate)", font_size=22),
            wrapped_label(r"who trades it: issuers of callable bonds own it and sell it on to dealers through cancellable "
                          r"swaps; mortgage investors are short the borrower's right to prepay (chapter 12)", 12.0, 20,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "A Bermudan swaption is the right to enter a swap on any one of a schedule of dates. This one, a ten "
            "non-call one, lets its holder start receiving a fixed rate, today's par rate of "
            f"{100 * b['K']:.2f} percent, on any anniversary from year one to year nine, for the rest of the ten "
            "years. <bookmark mark='a'/> Issuers of callable bonds own this option, and often sell it on to dealers; "
            "investors in mortgages are short the same kind of option, granted to every borrower."
        ) as vo:
            self.play(Create(line), FadeIn(marks), FadeIn(end), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(FadeIn(lab[1]))
        self.wait(0.4)
        self.clear_scene()

    def lsm(self):
        rows = [cmath(r"V_{t_i}", r"=", r"\max\big(\text{swap}_{t_i},\ C_{t_i}\big)", font_size=44, colors={r"V_{t_i}": ZERO}),
                cmath(r"C_{t_i}", r"\approx", r"\textstyle\sum_k \beta_k\,x_{t_i}^k,\quad \beta = \text{regress discounted "
                      r"future cash on } x", font_size=36, colors={r"C_{t_i}": VAS}),
                cmath(r"\beta", r"\leftarrow", r"\text{paths A};\quad \text{price} = \text{paths B}", font_size=38,
                      colors={r"\beta": GOOD})]
        whys = [why(r"at each date, exercise if the swap is worth more than keeping the option"),
                why(r"Longstaff and Schwartz (2001), Part 16: estimate the continuation value by regressing what happens "
                    r"next on today's state, on the paths where exercise is possible"),
                why(r"fit the rule on one set of paths and apply it to an independent set: its expected payoff is a lower bound, "
                    r"with no look-ahead")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "How do you price the right to choose? At each date the holder exercises if the swap is worth more than "
            "keeping the option alive. <bookmark mark='a'/> The value of keeping it is unknown, so estimate it the way "
            "Part sixteen did: regress the discounted value of what actually happens next on today's state, across "
            "simulated paths. <bookmark mark='b'/> And fit that rule on one set of Hull and White paths, then apply it "
            "to a fresh set, so the price cannot peek at the future."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def result(self, b):
        eu = np.asarray(b["europeans"]) * 1e4
        dates = np.asarray(b["dates"])
        g = axes([0.5, 9.5], [0, 500], x_length=7.4, y_length=4.4, xlabel=r"exercise date (European: that date only)",
                 ylabel=r"price, bp of notional", xticks=list(range(1, 10)), yticks=[0, 100, 200, 300, 400, 500],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.55, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                  fill_color=VAS, fill_opacity=0.75).move_to([ax.c2p(d, 0)[0],
                                                                             (ax.c2p(0, v)[1] + ax.c2p(0, 0)[1]) / 2, 0])
                        for d, v in zip(dates, eu)])
        bp = b["price"] * 1e4
        berm = DashedLine(ax.c2p(0.5, bp), ax.c2p(9.5, bp), color=GOOD, stroke_width=3)
        side = VGroup(
            MathTex(rf"\text{{Bermudan}} = {bp:.0f} \pm {2e4 * b['se']:.0f}\ \text{{bp}}", font_size=30, color=GOOD),
            MathTex(rf"\text{{best European}} = {eu.max():.0f}\ \text{{bp}}", font_size=28, color=VAS),
            MathTex(rf"\text{{in-sample}} = {1e4 * b['in_sample']:.0f},\ \ \text{{second seed}} = {1e4 * b['seed1']:.0f}",
                    font_size=24),
            wrapped_label(rf"Hull--White fitted to 31 December 2025, $a = {b['a']:.4f}$, $\sigma = {100 * b['sigma']:.2f}\%$; "
                          r"60{,}000 paths to fit, 60{,}000 to price", 4.0, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        fit_right(side)
        with self.voiceover(
            f"The closed-form Europeans use one allowed exercise date each. The most valuable in this schedule is at year {int(dates[int(np.argmax(eu))])}, worth {eu.max():.0f} basis points of notional. <bookmark mark='a'/> The independent-path Bermudan estimate is {bp:.0f} basis points, with the displayed two-standard-error sampling interval. In the exact optimal-stopping problem the Bermudan is worth at least every scheduled European; strict inequality requires useful exercise flexibility. A learned feasible policy has expected payoff no greater than the optimum, but a finite sample estimate can lie above or below that expectation. A small difference between the in-sample and independent-path estimates does not isolate or prove small look-ahead bias, because fitting error and sampling error also contribute."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(r_, DOWN) for r_ in bars], lag_ratio=0.1), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(berm), FadeIn(side[0]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def boundary(self, b):
        bd = b["boundary"]
        t = np.array([x[0] for x in bd])
        r = np.array([x[1] for x in bd]) * 100
        g = axes([0.5, 9.5], [2.5, 5], x_length=7.4, y_length=4.2, xlabel=r"exercise date", ylabel=r"swap rate to year 10, \%",
                 xticks=list(range(1, 10)), yticks=[3, 4, 5], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        Kl = DashedLine(ax.c2p(0.5, 100 * b["K"]), ax.c2p(9.5, 100 * b["K"]), color=WHITE, stroke_width=2)
        lb = VGroup(curve(ax, t, r, GOOD, stroke_width=3.5), *[Dot(ax.c2p(a, c), color=GOOD) for a, c in zip(t, r)])
        region = Polygon(ax.c2p(t[0], 2.5), *[ax.c2p(a, c) for a, c in zip(t, r)], ax.c2p(t[-1], 2.5), stroke_width=0,
                         fill_color=GOOD, fill_opacity=0.15)
        side = VGroup(label(r"line: sampled exercised-rate maximum", font_size=20, color=GOOD),
                      label(rf"dashed: the strike, {100 * b['K']:.2f}\%", font_size=19, color=GREY_A),
                      wrapped_label(r"early on, the rate must fall well below the strike before giving up the option is "
                                    r"worth it; near the end there is little option left to keep, and the boundary rises "
                                    r"toward the strike", 3.8, 18, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "This line is a sample summary of the learned exercise policy: at each date it records the largest swap rate among the simulated paths that exercised. It is not an analytically solved exercise boundary, and a polynomial regression can in principle create disjoint exercise regions. <bookmark mark='a'/> The broad economic pattern is still useful. Earlier exercise sacrifices more remaining optionality, so the receiver often waits for rates to fall further. Near the final exercise date, less continuation value remains. Establishing an actual boundary would require evaluating and checking the continuation and exercise functions on a state grid."
        ) as vo:
            self.play(FadeIn(g), Create(Kl), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(region), Create(lb), FadeIn(side[0]), FadeIn(side[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def lattice(self, L):
        rows = [cmath(r"\frac{V(t_i, x)}{P(t_i, T_N; x)}", r"=", r"\max\Big(\frac{\text{swap}(t_i, x)}{P(t_i, T_N; x)},\ "
                      r"\mathbb{E}^{T_N}\Big[\frac{V(t_{i+1})}{P(t_{i+1}, T_N)}\,\Big|\,x\Big]\Big)", font_size=32,
                      colors={r"\frac{V(t_i, x)}{P(t_i, T_N; x)}": ZERO})]
        whys = [why(r"no simulation: under the measure that pays at the swap's end, the Hull--White state moves "
                    r"between exercise dates as a Gaussian with a known mean and variance, so each expectation is an "
                    r"integral on a grid of 1{,}201 states (the House's \texttt{bermudan\_swaption\_lattice})")]
        step = ladder(self, rows, whys, keep=1, top=2.9, x=-0.6, buff=0.6, edge=6.9)
        eu_l, eu_c = np.asarray(L["europeans_lattice"]), np.asarray(L["europeans_closed"])
        tab = VGroup(
            MathTex(rf"\text{{Europeans: grid vs Jamshidian, worst }} {100 * np.max(np.abs(eu_l / eu_c - 1)):.3f}\%",
                    font_size=28),
            MathTex(rf"\text{{Bermudan: grid }} {1e4 * L['lattice']:.1f}\ \text{{bp}}, \quad \text{{regression }} "
                    rf"{1e4 * L['lsm']:.1f} \pm {2e4 * L['se']:.1f}\ \text{{bp}}", font_size=28, color=GOOD),
            wrapped_label('the feasible policy has expected value below the optimum, but its sample estimate has noise. The grid comparison is numerical; state resolution, quadrature and interpolation require convergence checks. More factors increase grid cost; simulation is one alternative',
                          11.0, 19, GREY_A),
        ).arrange(DOWN, buff=0.35).shift(DOWN * 1.2)
        with self.voiceover(
            f"In one Gaussian factor, a numerical grid provides a second pricing method. Under the terminal-bond measure the transition law between exercise dates is Gaussian, allowing numerical integration and a backward maximum over the exercise schedule. The transitions are exact in distribution; the finite state grid, interpolation and quadrature still introduce numerical error. <bookmark mark='a'/> The displayed comparison checks scheduled European prices against Jamshidian. Agreement on Europeans is valuable, but does not prove convergence of the Bermudan exercise boundary. <bookmark mark='b'/> The grid Bermudan is {1e4 * L['lattice']:.1f} basis points and the independent-path policy estimate is {1e4 * L['lsm']:.1f}. Their difference is small relative to the displayed Monte Carlo uncertainty. For a rigorous lower-bound claim, distinguish the feasible policy's expected payoff from its noisy estimate. More factors raise grid cost; simulation and other numerical methods offer alternatives."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
        self.wait(0.4)
        self.clear_scene()

    def callable(self, L):
        cols = VGroup(
            VGroup(label(r"10-year bullet bond", font_size=24, color=VAS),
                   MathTex(rf"{L['bullet']:.2f}", font_size=40),
                   MathTex(rf"\text{{yield}}\ {100 * L['y_bullet']:.2f}\%", font_size=28)).arrange(DOWN, buff=0.3),
            MathTex(r"-", font_size=60),
            VGroup(label(r"the Bermudan receiver", font_size=24, color=GOOD),
                   MathTex(rf"{100 * L['lattice']:.2f}", font_size=40),
                   label(r"the issuer's right to call", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.3),
            MathTex(r"=", font_size=60),
            VGroup(label(r"callable bond", font_size=24, color=BAD),
                   MathTex(rf"{L['callable']:.2f}", font_size=40),
                   MathTex(rf"\text{{yield}}\ {100 * L['y_callable']:.2f}\%", font_size=28)).arrange(DOWN, buff=0.3),
        ).arrange(RIGHT, buff=0.6).shift(UP * 0.5)
        head = label(rf"A 10-year bond paying {100 * L['K']:.2f}\% a year, callable at par every year from year 1",
                     font_size=24).to_edge(UP, buff=0.6)
        foot = wrapped_label(
            rf"the call costs the investor {L['bullet'] - L['callable']:.2f} points of price, "
            rf"{1e4 * (L['y_callable'] - L['y_bullet']):.0f} bp of yield to final maturity. Agencies such as the Federal Home Loan "
            r"Banks issue callable notes in volume and swap them into floating-rate funding with cancellable swaps, in "
            r"effect selling the call to dealers, who are left long Bermudans to hedge", 12.0, 19,
            GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            f"A ten-year fixed-coupon bond can give its issuer the right to repay at par on the allowed anniversaries. The coupon here is {100 * L['K']:.2f} percent. <bookmark mark='a'/> Under this schedule and single-curve model, the investor owns the bullet bond and has sold the issuer a cancellation right represented by the receiver Bermudan. Coupon timing and exercise conventions must match. <bookmark mark='b'/> The example's callable price is {L['callable']:.2f}, versus {L['bullet']:.2f} for the bullet. Computing yield to final maturity from those prices gives a {1e4 * (L['y_callable'] - L['y_bullet']):.0f}-basis-point difference. That quoted yield assumes the final cash-flow schedule; it is not the holder's guaranteed realized yield if the bond is called. Agencies may swap callable funding with dealers, transferring embedded optionality subject to their actual contract terms."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols[0]))
            vo.wait_until("a")
            self.play(FadeIn(cols[1]), FadeIn(cols[2]))
            vo.wait_until("b")
            self.play(FadeIn(cols[3]), FadeIn(cols[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sweep(self, b):
        sw = b["sweep"]
        a = np.array([x["a"] for x in sw])
        ratio = np.array([x["bermudan"] / x["best_european"] for x in sw])
        g = axes([0, 0.21], [1.2, 1.6], x_length=6.4, y_length=4.0, xlabel=r"mean reversion $a$ ($\sigma$ held)",
                 ylabel=r"Bermudan / best European", xticks=[0, 0.05, 0.1, 0.15, 0.2], yticks=[1.2, 1.4, 1.6],
                 font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        line = VGroup(curve(ax, a, ratio, GOOD, stroke_width=3.5), *[Dot(ax.c2p(x, y), color=GOOD) for x, y in zip(a, ratio)])
        side = wrapped_label('fixed-sigma sweep: changing mean reversion changes both marginal values and cross-date dependence. This is a model-family sensitivity, not an isolated correlation test; the next House example matches one identical European hedge',
                             4.6, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Keep sigma fixed, vary mean reversion, and reprice the whole exercise schedule in this model family. <bookmark mark='a'/> The estimated premium relative to the most valuable scheduled European rises from {100 * (ratio[0] - 1):.0f} to {100 * (ratio[-1] - 1):.0f} percent in this sweep. Mean reversion changes both cross-date dependence and the marginal option values, so this is not a controlled correlation-only experiment or a universal monotonicity theorem. Early-exercise flexibility depends on the joint dynamics across dates. Vanilla prices restrict those dynamics but do not, on their own, settle every exotic's value. The House chapter separately recalibrates each scenario to one identical fixed European before comparing prices."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2)
        q = ask(r"why is a Bermudan always worth at least the most expensive European in its schedule?")
        with self.voiceover("The desk question: why is a Bermudan worth at least the most expensive European in its "
                            "schedule?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
