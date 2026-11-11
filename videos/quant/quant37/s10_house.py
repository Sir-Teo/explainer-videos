from __future__ import annotations


from explainer.quant import *  # noqa: F403
from explainer.quant.house import execution as E
from videos.quant.quant37.common import (GOOD, HURDLE, IMPACT_C, KERNEL_C, PART, RL_C, SCHED_C, fit_right,
                                         house_lab, load)


class House(VoiceoverScene):
    def construct(self):
        self.answer()
        self.card()
        self.sheet(load("aggregate"), load("propagator"), load("latent"), load("ac"), load("ow"), load("rl"))
        self.sizing(load("ac"))
        self.report()
        self.capacity_chart(load("ac"))
        self.lab()
        self.lab2()
        self.lab3()
        self.lab4()
        self.lab5()
        self.module()
        self.test()
        self.question()

    def answer(self):
        rows = [cmath(r"\text{alpha decays in a day}", r"\Rightarrow", r"\text{urgency}", font_size=36),
                cmath(r"\text{IS, front-loaded}", r"\ \text{or}\ ", r"\text{POV at a higher rate}", font_size=34,
                      colors={r"\text{IS, front-loaded}": SCHED_C}),
                cmath(r"\text{benchmark}", r"=", r"\text{arrival price}", font_size=38, colors={r"\text{arrival price}": GOOD})]
        whys = [why(r"a signal that fades makes waiting expensive: delay is an opportunity cost, like risk in "
                    r"Almgren--Chriss"),
                why('compare urgency and rate-dependent costs; a size-only formula cannot decide the schedule'),
                why(r"and judge the result against the price when the decision was made, not against VWAP")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "An execution-choice example. <bookmark mark='a'/> A fading signal can make delay costly, separately from price variance. <bookmark mark='b'/> Compare an urgency-based shortfall schedule or a higher participation target with the incremental rate-dependent costs. A size-only square-root formula cannot settle that choice. <bookmark mark='c'/> Fix a decision or arrival benchmark independently of the executor, and judge all costs and uncertainties against the same convention."
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

    def card(self):
        c = chapter_card(9, r"Rule 37: price the trade before you make it", r"What must every order carry before it "
                         r"reaches the market?", part=PART)
        with self.voiceover('Chapter nine. Rule thirty-seven is a proposed execution research protocol. An order should carry a cost estimate, uncertainty, a schedule and a fixed benchmark, followed by an honest record of execution. This lesson does not deploy a trading system or approve a signal, capacity limit or broker.'):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sheet(self, ag, p, lt, ac, ow, rl):
        r = rl["res"]
        rows = [(r"Bitcoin: price move per minute against signed volume, log-log slope", rf"{ag['slope']:.2f}", IMPACT_C),
                (r"latent book: impact exponent, small and large orders",
                 rf"{lt['slope_small']:.2f},\ {lt['slope_large']:.2f}", IMPACT_C),
                (r"propagator: peak, and decay exponent against $(1 - \gamma)/2$",
                 rf"{p['G_peak']:.2f};\ {p['beta']:.2f}\ \text{{vs}}\ {p['beta_theory']:.2f}", KERNEL_C),
                (r"Almgren--Chriss, 5{,}000 BTC in an hour: TWAP cost and sd, \$k",
                 rf"{ac['show']['0']['cost'] / 1000:.0f},\ {ac['show']['0']['sd'] / 1000:.0f}", SCHED_C),
                (r"Obizhaeva--Wang, $\rho T = 10$: each block, as a share of the order",
                 rf"{100 * ow['closed']['block']:.1f}\%", SCHED_C),
                (r"simulator: TWAP, Q-learning and dump, half-ticks",
                 rf"{r['TWAP']['mean']:.1f},\ {r['Q-learning']['mean']:.1f},\ {r['dump at once']['mean']:.1f}", RL_C)]
        hx = [-2.2, 4.8]
        tab = VGroup()
        for j, (txt, val, col) in enumerate(rows):
            y = 2.3 - 0.7 * j
            tab.add(VGroup(label(txt, font_size=16, color=col).move_to([hx[0], y, 0]),
                           MathTex(val, font_size=24).move_to([hx[1], y, 0])))
        title = label(r"The execution desk's first sheet", font_size=28).to_edge(UP, buff=0.25)
        foot = wrapped_label(r"computed in this part from Binance's public trade tape and best quotes for the BTCUSDT "
                             r"perpetual (16--25 May 2023), one-minute bars for 2023, and simulation; none is advice", 12.0,
                             15, GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The illustrative research sheet. <bookmark mark='a'/> A same-window aggregate-flow slope, finite-grid latent-book exponents, a descriptive propagator fit, assumed Almgren-Chriss costs, exponential-kernel blocks, and simulator-policy averages. They answer different questions with different clocks and uncertainties. Reading them together does not identify a causal cost model or validate an executable strategy."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def sizing(self, ac):
        sig = ac["sigma_day"] / ac["price"]
        v_day_usd = ac["v_day"] * ac["price"]
        cap = (0.0010 / sig) ** 2 * v_day_usd
        cap_m = cap / 1e6
        rows = [cmath(r"\text{alpha}", r"=", r"10\ \text{bp}", font_size=38),
                cmath(r"Y\sigma\sqrt{Q/V}", r"<", r"10\ \text{bp}", font_size=38, colors={r"Y\sigma\sqrt{Q/V}": IMPACT_C}),
                cmath(r"Q", r"<", rf"\left(\frac{{0.001}}{{{sig:.3f}}}\right)^2 V \approx \${cap / 1e6:.0f}\text{{m}}",
                      font_size=36, colors={r"Q": HURDLE})]
        whys = [why(r"a trade expected to earn ten basis points before costs"),
                why('simplified one-leg average-impact break-even condition, omitting other costs'),
                why(rf"on Bitcoin's perpetual, daily volatility {100 * sig:.1f}\% and volume "
                    rf"\${v_day_usd / 1e9:.0f}bn: illustrative one-leg threshold, before other costs and uncertainty")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"""A simplified break-even illustration. <bookmark mark='a'/> Assume ten basis points of expected alpha for one trading leg, before costs. <bookmark mark='b'/> Set an average-cost square-root coefficient to one, and omit spread, fees, other legs and uncertainty. <bookmark mark='c'/> The resulting threshold is about {cap_m:.0f} million dollars under this recorded-volume and volatility calibration. It is not an optimal position size or an approved capacity limit; round-trip costs and a margin for error would lower the allowable scale."""
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

    def report(self):
        cards = VGroup(
            desk_question(r"before", r"every parent order carries its size as a share of expected volume, the "
                          r"square-root estimate with its uncertainty, the signal's half-life, and the chosen schedule",
                          width=12.0, font_size=19),
            desk_question(r"during", r"the desk watches participation, the realised path against the schedule, and the "
                          r"microprice of Part 36 before each child order", width=12.0, font_size=19),
            desk_question(r"after", r"the shortfall against arrival, split as in Chapter 1, the markouts, and the "
                          r"realised against the estimated cost, pooled over orders until the noise averages out",
                          width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "A proposed order record. <bookmark mark='a'/> Before: expected volume, a convention-specific average-cost estimate with uncertainty, signal decay and schedule. <bookmark mark='b'/> During: participation and actual fills against plan; book features need separate predictive validation before use as alpha. <bookmark mark='c'/> After: fixed-benchmark signed shortfall, fees, unfilled-share marks and subsequent markouts. Pool appropriate samples with dependence and selection controls. This is a research protocol, not evidence that a live system currently records or trades this way."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def capacity_chart(self, ac):
        import numpy as np
        sig = ac["sigma_day"] / ac["price"]
        v_usd = ac["v_day"] * ac["price"]
        sizes = np.logspace(5, 9, 60)
        cost = 1e4 * sig * np.sqrt(sizes / v_usd)
        x = np.log10(sizes)
        g = axes([5, 9], [0, 60], x_length=6.4, y_length=4.4, xlabel=r"order size, dollars",
                 ylabel=r"square-root cost, bp", xticks=[5, 6, 7, 8, 9], xfmt=lambda v: f"10^{{{v:.0f}}}",
                 yticks=[0, 10, 20, 40, 60], yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = g.ax
        c_ = curve(ax, x, cost, IMPACT_C, stroke_width=3)
        alpha = DashedLine(ax.c2p(5, 10), ax.c2p(9, 10), color=GOOD, stroke_width=2)
        cap = (0.0010 / sig) ** 2 * v_usd
        cap_m = cap / 1e6
        mark = Dot(ax.c2p(np.log10(cap), 10), radius=0.09, color=HURDLE)
        leg = legend([(IMPACT_C, r"impact, $Y = 1$"), (GOOD, r"a 10-bp signal")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            f"""The same illustrative one-leg break-even curve. <bookmark mark='a'/> Average impact under the assumed Y-equals-one convention rises with dollar order size. <bookmark mark='b'/> The ten-basis-point line crosses near {cap_m:.0f} million dollars. This is a model threshold with fixed inputs, not a forecast that trades left of the dot profit or that any deployed portfolio has such a size. Net profitability also depends on all other costs, alpha estimation, exits and uncertainty."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(c_))
            vo.wait_until("b")
            self.play(Create(alpha), FadeIn(mark))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The latent order book", E.latent_book, "for n in range(n_tot):", 10, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter two's latent book. Each step, the density diffuses by a discrete Laplacian; while the order runs, "
            "a source at the price removes offers; and the price is wherever the density crosses zero. Ten lines, and "
            "the square root comes out."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab2(self):
        card = house_lab(r"Almgren and Chriss", E.almgren_chriss, "tau = T / n", 12, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapter five's schedule: the urgency kappa from the hyperbolic cosine, the holdings as a hyperbolic sine, "
            "and the expected cost and variance of the shortfall."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab3(self):
        card = house_lab(r"Optimal trading under a decay kernel", E.kernel_optimal, "n = len(G)", 4,
                         extra=((E.ow_closed_form, "a = X / (2 + rho * T)", 2),), width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "Chapters four and six. Build the matrix of the kernel at every pair of dates, solve it against a vector of "
            "ones, and scale to the order's size: the discrete Fredholm condition. And the closed form it converges to "
            "for an exponential kernel, two lines."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab4(self):
        card = house_lab(r"Fitting the propagator", E.propagator_fit, "c = np.array", 4, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter three's fit: the sign autocorrelation and the cross-correlation of price changes with past "
            "signs, a Toeplitz system solved, and a cumulative sum. The propagator is what remains of a trade's impact."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def lab5(self):
        card = house_lab(r"A market sell in the simulator", E.QueueExec._sell, "while k > 0:", 9, width=10.6)
        card.move_to(ORIGIN)
        with self.voiceover(
            "And Chapter seven's market order. While units remain, take what the best bid holds, at half a tick below "
            "the mid; when the queue is emptied the mid falls half a tick and new queues are drawn. Impact, in nine "
            "lines."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def module(self):
        chart = house_chart(PART, lit=("execution",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{response\_function}, \texttt{propagator\_fit}, \texttt{aggregate\_impact}", r"measurement"),
            (r"\texttt{latent\_book}", r"the square root"),
            (r"\texttt{almgren\_chriss}, \texttt{kernel\_cost}, \texttt{kernel\_optimal}, \texttt{ow\_closed\_form}",
             r"schedules"),
            (r"\texttt{QueueExec}, \texttt{q\_learn}, \texttt{run\_policy}", r"learning"),
        ]
        tab = VGroup(*[VGroup(label(a_, font_size=20, color=QC.HOUSE), label(b_, font_size=20, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.35)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Proposed Rule 37: every order should reach the market with a pre-trade cost from the square root, a "
                             r"schedule matched to its signal's urgency, and a benchmark at its arrival price; every "
                             r"impact model the desk uses is checked for no dynamic arbitrage; and every learned executor "
                             r"is judged first against TWAP.", 12.4, 17, QC.HOUSE).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The tools this part adds. <bookmark mark='a'/> Measurement; the latent book; the schedules; and the "
            "learning environment. <bookmark mark='b'/> And the thirty-seventh rule. Every order reaches the market "
            "with a pre-trade cost from the square root, a schedule matched to its signal's urgency, and a benchmark at "
            "its arrival price. Every impact model is checked for no dynamic arbitrage. And every learned executor is "
            "judged first against TWAP."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def test(self):
        cards = VGroup(
            desk_question(r"the backtest with no costs", r"ask for the square-root cost at the strategy's size, and the "
                          r"size at which it eats the alpha (Chapter 9's sizing)", width=12.0, font_size=19),
            desk_question(r"the impact model with a free lunch", 'ask whether its kernel is positive definite, convex and decreasing; distinguish negative round trips from intermediate sales; use a no-sales constraint if required',
                          width=12.0, font_size=19),
            desk_question(r"the broker who beat VWAP", r"ask for the arrival-price shortfall, the order's share of "
                          r"volume, and the markouts (Chapter 8)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Apply the protocol to three cases. <bookmark mark='a'/> A backtest without costs needs a calibrated cost convention, all trading legs and capacity uncertainty. <bookmark mark='b'/> An impact optimizer needs separate checks for positive costs, numerical conditioning, existence and intermediate sales. Sales in a purchase program do not by themselves prove negative round-trip costs. <bookmark mark='c'/> A broker reporting a VWAP win should also supply the independently fixed arrival benchmark, order participation, fill details, fees and markouts."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k_:
                    self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label(r"10. A simplified one-leg break-even size", font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label(r"$\alpha=10$ bp, $\sigma_{day}=2\%$, $V_{day}=\$10$bn, average-impact $Y=1$.", 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label(r"Solve $Y\sigma\sqrt{Q/V}<\alpha$. Which missing costs and uncertainties limit the threshold?", 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        with self.voiceover("Quantitative pause ten. Alpha is ten basis points, daily return volatility two percent and dollar volume ten billion. Choose an average-impact coefficient of one. Solve the one-leg impact-less-than-alpha inequality, and identify the omitted costs and uncertainties. This threshold is neither an optimal position nor approved capacity."):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task))
        self.wait(6)
        self.clear_scene()
