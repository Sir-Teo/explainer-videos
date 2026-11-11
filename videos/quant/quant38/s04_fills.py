from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, GOOD, HURDLE, INV_C, MAKER_C, PART, SPREAD_C, fit_right, load)


class Fills(VoiceoverScene):
    def construct(self):
        f = load("fills")
        g = load("glft")
        d = load("deep")
        self.card(g)
        self.method()
        self.curve_(f)
        self.by_day(f)
        self.misfit(f)
        self.quotes(g)
        self.deep_test(d)
        self.per_hour(d)
        self.why_far(d)
        self.assumption()
        self.alpha_quotes()
        self.question()

    def card(self, g):
        half = g["rows"][0]["half_spread"]
        c = chapter_card(3, r"Fill rates and optimal quotes", r"How far from the mid should a market maker quote?",
                         part=PART)
        with self.voiceover(f'Chapter three. At the lowest chosen risk aversion, the GLFT approximation gives {half:.0f} ticks from the mid. Its inputs include a reach-probability proxy rather than observed resting fills. We will compare it with a separate gross mark calculation, without claiming an optimized or profitable live strategy.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def method(self):
        rows = [cmath(r"\text{each second}", r":", r"\text{quotes at } M_0 \pm \delta", font_size=36),
                cmath(r"P(\delta)", r"=", r"\tfrac12(P_{\rm ask}(\delta)+P_{\rm bid}(\delta))", font_size=30),
                cmath(r"\lambda(\delta)", r"=", r"-\log(1 - P(\delta)) / 1\,\text{s}", font_size=36, colors={r"\lambda(\delta)": SPREAD_C}),
                cmath(r"\log\lambda", r"\approx", r"\log A - k\,\delta", font_size=38)]
        whys = [why(r"imagine quotes at each distance from the mid at the start of every second, two days of the tape"),
                why(r"the share of seconds in which a taker's trade reaches that price, buys for the ask and sells for the "
                    r"bid"),
                why(r"the homogeneous-Poisson-equivalent event rate; this does not validate Poisson arrivals or resting queue fills"),
                why(r"Avellaneda and Stoikov's exponential: a straight line on a log scale; its slope is $-k$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Measure reach first. <bookmark mark='a'/> At each second's start, take the mid from the hundred-millisecond quote grid. <bookmark mark='b'/> Count separately whether buy trades reach an ask-distance threshold and sell trades reach a bid-distance threshold, then average the two probabilities. <bookmark mark='c'/> Minus log one minus probability divided by one second is the equivalent rate for a homogeneous Poisson event. This transformation does not establish Poisson arrivals or queue fills. <bookmark mark='d'/> Fit log rate against distance: its slope is minus k. The pooled fit averages daily probabilities before taking the logarithm, not daily intensities."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def curve_(self, f):
        dl = np.asarray(f["deltas"], float)
        lam = np.asarray(f["lam"], float)
        y = np.log10(lam)
        g = axes([0, 50], [-1.5, 0], x_length=6.4, y_length=4.4, xlabel=r"distance from the mid $\delta$, ticks",
                 ylabel=r"Poisson-equivalent reach rate, per second", xticks=[0, 10, 20, 30, 40, 50], yticks=[-1.5, -1, -0.5, 0],
                 yfmt=lambda v: f"10^{{{v:g}}}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.07, color=SPREAD_C) for a, b in zip(dl, y)])
        xs = np.linspace(0, 50, 60)
        fit = curve(ax, xs, np.log10(f["A"]) - f["k"] * xs / np.log(10), HURDLE, stroke_width=2.5)
        st = VGroup(label(rf"$A = {f['A']:.2f}$ per second", font_size=18, color=HURDLE),
                    label(rf"$k = {f['k']:.3f}$ per tick", font_size=18, color=HURDLE),
                    label(rf"$1/k \approx {1 / f['k']:.0f}$ ticks", font_size=18, color=GREY_A))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
        fit_right(st)
        half_d = float(np.log(2) / f["k"])
        with self.voiceover(
            f"The two-day reach fit. <bookmark mark='a'/> A half-tick threshold is reached on about a third of the averaged side-windows; a forty-five-tick threshold on about one in twenty. These are side reach events, not actual fill counts. <bookmark mark='b'/> The fitted k is {f['k']:.3f} per tick, so the equivalent rate halves over about {half_d:.0f} ticks. The near point lies above the fitted line. Large threshold reaches can accompany trading and price moves; the grid does not identify a message-level sweep mechanism."
        ) as vo:
            self.play(FadeIn(g), FadeIn(st))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(Create(fit))
        self.wait(0.4)
        self.clear_scene()

    def by_day(self, f):
        days = list(f["days"].keys())
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"day", r"$A$, per second", r"$k$, per tick")])
        tab = VGroup(head)
        for d in days:
            r = f["days"][d]
            tab.add(VGroup(label(d[5:], font_size=18), MathTex(f"{r['A']:.3f}", font_size=26),
                           MathTex(f"{r['k']:.4f}", font_size=26, color=SPREAD_C)))
        tab.add(VGroup(label(r"pooled", font_size=18, color=HURDLE), MathTex(f"{f['A']:.3f}", font_size=26, color=HURDLE),
                       MathTex(f"{f['k']:.4f}", font_size=26, color=HURDLE)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        k0, k1 = f["days"][days[0]]["k"], f["days"][days[1]]["k"]
        with self.voiceover(
            f"Across the two days, fitted k is {k0:.3f} and {k1:.3f}. <bookmark mark='a'/> These descriptive differences accompany different flow and volatility. They do not prove a sweep mechanism or parameter stability. Pooled probabilities are averaged with equal day weights before conversion to an equivalent rate. A live estimator would need a specified past-only window and out-of-sample validation."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def misfit(self, f):
        d = np.asarray(f["deltas"], float)
        lam = np.asarray(f["lam"], float)
        fit = f["A"] * np.exp(-f["k"] * d)
        pick = [0, 1, 4, 7, 8, 9]
        hx = [-4.2, -1.6, 1.0, 3.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"distance, ticks", r"reach-equivalent rate",
                                                                         r"fitted $Ae^{-k\delta}$", r"measured / fitted")])
        tab = VGroup(head)
        for i in pick:
            ratio = lam[i] / fit[i]
            tab.add(VGroup(MathTex(f"{d[i]:g}", font_size=26), MathTex(f"{lam[i]:.3f}", font_size=26, color=SPREAD_C),
                           MathTex(f"{fit[i]:.3f}", font_size=26),
                           MathTex(f"{ratio:.2f}", font_size=26, color=BAD if abs(ratio - 1) > 0.1 else GREY_A)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.3 - 0.72 * j, 0])
        touch = 100 * (lam[0] / fit[0] - 1)
        mid_err = 100 * float(np.mean(np.abs(lam[1:9] / fit[1:9] - 1)))
        tail = 100 * (lam[9] / fit[9] - 1)
        foot = wrapped_label(r"descriptive threshold-reach residuals; an equivalent rate is not a queue fill or a structural identification of "
                             r"a sweep", 11.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Compare the equivalent reach rates with the fitted exponential. <bookmark mark='a'/> The half-tick rate is {touch:.0f} percent above the fit. <bookmark mark='b'/> From one through thirty ticks, the mean absolute relative deviation over these chosen points is {mid_err:.0f} percent. That is a descriptive in-sample residual, without a confidence interval. <bookmark mark='c'/> At forty-five ticks the deviation is {tail:.0f} percent. <bookmark mark='d'/> Near and far thresholds need not share one constant exponential law. Neither the residual pattern nor a log-linear fit tests independent arrivals, actual queue fills or an optimal quoting policy."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:6]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(tab[6]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def quotes(self, g):
        hx = [-3.8, -0.8, 2.0, 4.8]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"risk aversion $\gamma$", r"half-spread at $q = 0$",
                                                                         r"skew per unit", r"base term")])
        tab = VGroup(head)
        for r in g["rows"]:
            tab.add(VGroup(MathTex(f"{r['gamma']:g}", font_size=26), MathTex(f"{r['half_spread']:.1f}", font_size=26,
                                                                               color=MAKER_C),
                           MathTex(f"{r['skew']:.1f}", font_size=26, color=INV_C), MathTex(f"{r['static']:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.85 * j, 0])
        foot = wrapped_label(rf"GLFT with Bitcoin's fitted $A$ and $k$ and a volatility of {g['sigma']:.0f} ticks per "
                             r"square root of a second; distances in ticks", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        r0 = g["rows"][0]
        r2 = g["rows"][2]
        with self.voiceover(
            f"Feed the proxies into the GLFT approximation. Sigma is the standard deviation of one-second mid increments, about {g['sigma']:.0f} ticks per square root of a second, without a claim that the price is Brownian. <bookmark mark='a'/> At gamma equal to one ten-thousandth per tick-unit, half-spread is {r0['half_spread']:.0f} ticks. At one hundredth it is {r2['half_spread']:.0f}, with inventory skew {r2['skew']:.0f} ticks per unit. Unit size, risk preference, arrival assumptions and interior approximation matter. This is a model output, not a verified optimal quote."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def deep_test(self, d):
        rows = d["rows"]
        x = np.asarray([r["delta"] for r in rows], float)
        y = np.asarray([r["pnl60"] for r in rows], float)
        lo = float(np.floor(y.min() / 5) * 5)
        hi = float(np.ceil(y.max() / 5) * 5)
        g = axes([0, 50], [lo, hi], x_length=6.4, y_length=4.4, xlabel=r"quote distance $\delta$, ticks",
                 ylabel=r"gross mark at quote-start + 60 s, ticks", xticks=[0, 10, 20, 30, 40, 50], yticks=[lo, 0, hi],
                 yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(50, 0), color=GREY_B, stroke_width=1.5)
        c_ = VGroup(curve(ax, x, y, MAKER_C, stroke_width=3), *[Dot(ax.c2p(a, b), radius=0.07, color=MAKER_C)
                                                                for a, b in zip(x, y)])
        r30 = [r for r in rows if r["delta"] == 30][0]
        r45 = [r for r in rows if r["delta"] == 45][0]
        r5 = [r for r in rows if r["delta"] == 5][0]
        with self.voiceover(
            f"A separate reach experiment. At each second's starting mid, set two distance thresholds. Count at most one reach per side per window, and mark it at the mid sixty seconds after the window started, not sixty seconds after an exact fill time. No queue, tick rounding, fees or endogenous inventory are modeled. <bookmark mark='a'/> The gross mean at five ticks is {r5['pnl60']:.0f} ticks. <bookmark mark='b'/> It is {r30['pnl60']:+.0f} at thirty and {r45['pnl60']:+.0f} at forty-five. Agreement in distance does not validate the control model or establish executable profit."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(c_), run_time=2.5)
            vo.wait_until("b")
            self.wait(0.2)
        self.wait(0.4)
        self.clear_scene()

    def per_hour(self, d):
        r45 = [r for r in d["rows"] if r["delta"] == 45][0]
        r30 = [r for r in d["rows"] if r["delta"] == 30][0]
        r2 = [r for r in d["rows"] if r["delta"] == 2][0]
        rows = [cmath(r"\delta = 2", r":", rf"{r2['per_hour60']:,.0f}\ \text{{tick-units per elapsed hour}}".replace(",", "{,}"),
                      font_size=36, colors={r"\delta = 2": BAD}),
                cmath(r"\delta = 30", r":", rf"{r30['per_hour60']:+,.0f}\ \text{{tick-units per elapsed hour}}".replace(",", "{,}"),
                      font_size=36),
                cmath(r"\delta = 45", r":", rf"{r45['per_hour60']:+,.0f}\ \text{{tick-units per elapsed hour}}".replace(",", "{,}"),
                      font_size=36, colors={r"\delta = 45": GOOD})]
        whys = [why(r"many fills, each losing: the touch's business is volume times a negative edge"),
                why(r"near breakeven: fewer fills, edges close to zero"),
                why(r"rarer fills with large edges: per unit of size, about \$700 an hour in this optimistic test; a real "
                    r"maker would share these levels with others, pay fees, and hold the inventory")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"Aggregate the reach marks per elapsed hour, counting one hypothetical unit per reached side-window. <bookmark mark='a'/> At two ticks, the loss is about {abs(r2['per_hour60']):,.0f} tick-units per hour. <bookmark mark='b'/> At thirty it is {r30['per_hour60']:+,.0f}. <bookmark mark='c'/> At forty-five it is {r45['per_hour60']:+,.0f}, about seven hundred dollars if a unit is one bitcoin. Windows overlap, final windows are excluded while full elapsed time is used, and inventories are unconstrained. These sums are gross marks, not returns on a specified capital base."
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

    def why_far(self, d):
        r45 = [r for r in d["rows"] if r["delta"] == 45][0]
        cards = VGroup(
            desk_question(r"the far end of a sweep", r"a taker who walks the book pays prices beyond where the mid "
                          r"settles; a quote out there is filled by the overshoot, and the mid comes back toward it",
                          width=12.4, font_size=19),
            desk_question(r"few fills", rf"at 45 ticks a quote is filled only {r45['fills_per_hour']:.0f} times an hour "
                          r"against thousands at the touch: a business of rare, large edges", width=12.4, font_size=19),
            desk_question(r"an optimistic reach experiment", r"queues, tick feasibility, overlapping exposure and fees are omitted; real deep levels have "
                          r"queues too, and the best of them belong to whoever got there first", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            f"Interpreting the positive far-distance marks. <bookmark mark='a'/> A threshold reached during a large trade can lie beyond the later mid, consistent with an overshoot story; the calculation does not identify its cause. <bookmark mark='b'/> At forty-five ticks there are about {r45['fills_per_hour']:.0f} reached side-windows per hour. <bookmark mark='c'/> Optimistic fill treatment is not a mathematical upper bound on every feasible strategy. Queue priority, tick feasibility, overlapping positions and subsequent liquidation are missing."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def assumption(self):
        rows = [cmath(r"\text{AS assumes}", r":", r"\text{arrival drivers} \perp \text{price noise}", font_size=38),
                cmath(r"\text{data}", r":", r"\text{fills at the touch} \Rightarrow \text{moves against}", font_size=36,
                      colors={r"\text{data}": BAD}),
                cmath(r"\text{fix}", r":", r"\text{fill rates conditional on the state, and an alpha term}", font_size=32,
                      colors={r"\text{fix}": GOOD})]
        whys = [why(r"the baseline specifies independent noise drivers; state-adaptive controls need not make observed fills independent of price paths"),
                why(r"near the touch, being filled is news (Part 36's markouts), which the formula ignores; it is "
                    r"not validated by a similar-looking distance"),
                why(r"Cartea, Jaimungal and Ricci (2014) add short-term alpha and adverse selection to the market maker's "
                    r"problem; state-conditioned means are candidate features requiring past-only execution and cost validation")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What the comparison tests. <bookmark mark='a'/> In the baseline model, arrival drivers are independent of the Brownian price noise, while controls can adapt to the current state. <bookmark mark='b'/> Conditional tape marks reveal dependence that a constant-rate independent-driver model omits. Similarity of a suggested distance and a gross-mark crossing is not validation. <bookmark mark='c'/> State-dependent arrivals and adverse-selection models are possible extensions. Their forecasts must be validated at actual decision times, with fills and costs."
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

    def alpha_quotes(self):
        rows = [cmath(r"\text{centre}", r":", r"M \to M + \hat\alpha", font_size=40, colors={r"\text{centre}": MAKER_C}),
                cmath(r"\hat\alpha", r"=", r"\text{the expected move over the quote's life}", font_size=34),
                cmath(r"\text{e.g.}", r":", r"\text{Part 36's per-horizon table of mean moves}", font_size=34,
                      colors={r"\text{e.g.}": GOOD})]
        whys = [why(r"a schematic price-unit center shift inspired by short-term-alpha models; the full control solution is more than "
                    r"mid plus expected drift, with inventory, adverse-selection and arrival terms solved consistently"),
                why(r"the forecast that matters is over the time a quote is likely to rest"),
                why(r"a state-conditioned table is a candidate feature requiring past-only validation; the microprice, "
                    r"also needs calibration; neither is approved for live quoting")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A schematic way to add a forecast. <bookmark mark='a'/> Shift a quote center by an expected price move with matching price units, while solving the chosen model's inventory and arrival problem. This is not the full Cartea, Jaimungal and Ricci solution. <bookmark mark='b'/> The horizon must match the quote decision and possible fill time. <bookmark mark='c'/> Part thirty-six supplies descriptive state-conditioned means as candidate features, not validated executable alpha or proof that one estimator is always preferable."
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

    def question(self):
        q = VGroup(label(r"Pause and predict", font_size=32, color=QC.IDEA),
                   wrapped_label("Bitcoin's perpetual has a one-tick spread almost all the time. If the tick were ten times smaller, would the quoted spread shrink ten times? Who would gain, and who would lose?", 11.8, 30)).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        with self.voiceover(
            "Pause and predict. Bitcoin's perpetual sits at a one-tick spread almost all the time. If the tick were ten "
            "times smaller, would the spread shrink ten times? Who would gain, and who would lose?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
