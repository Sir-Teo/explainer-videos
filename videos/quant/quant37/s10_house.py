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

    def answer(self):
        rows = [cmath(r"\text{alpha decays in a day}", r"\Rightarrow", r"\text{urgency}", font_size=36),
                cmath(r"\text{IS, front-loaded}", r"\ \text{or}\ ", r"\text{POV at a higher rate}", font_size=34,
                      colors={r"\text{IS, front-loaded}": SCHED_C}),
                cmath(r"\text{benchmark}", r"=", r"\text{arrival price}", font_size=38, colors={r"\text{arrival price}": GOOD})]
        whys = [why(r"a signal that fades makes waiting expensive: delay is an opportunity cost, like risk in "
                    r"Almgren--Chriss"),
                why(r"so trade faster early, accepting more impact; the square root says the extra impact is modest"),
                why(r"and judge the result against the price when the decision was made, not against VWAP")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The answer to the pause. <bookmark mark='a'/> An alpha that decays in a day makes waiting expensive: delay "
            "is an opportunity cost, playing the role of risk in Almgren and Chriss. <bookmark mark='b'/> So ask for an "
            "implementation-shortfall algorithm, front-loaded, or a higher participation rate. The square root says "
            "the extra impact is modest. <bookmark mark='c'/> And judge it against the arrival price, not against "
            "VWAP."
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
        with self.voiceover("Chapter nine. The House's thirty-seventh rule belongs to the execution desk it opens. Every "
                            "order arrives with a cost estimate and a schedule, and leaves with a measured cost to set "
                            "against both."):
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
            "The first sheet. <bookmark mark='a'/> Impact on Bitcoin that is concave in size. A latent book whose impact "
            "turns from linear to a square root. A propagator that decays at about the rate that keeps prices "
            "diffusive. An Almgren and Chriss schedule whose risk dwarfs its cost. Obizhaeva and Wang's blocks. And a "
            "learned executor that does not yet beat TWAP."
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
                why(r"is worth making only while its square-root impact, with $Y = 1$, is smaller"),
                why(rf"on Bitcoin's perpetual, daily volatility {100 * sig:.1f}\% and volume "
                    rf"\${v_day_usd / 1e9:.0f}bn: the House's largest sensible order for that signal")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "How the desk sizes a trade. <bookmark mark='a'/> A signal expected to earn ten basis points. "
            "<bookmark mark='b'/> It is worth trading only while the square-root impact is smaller. "
            f"<bookmark mark='c'/> On Bitcoin's perpetual, with its daily volatility and volume, that caps the order at "
            f"about {cap_m:.0f} million dollars. Bigger, and the signal pays the market."
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
        with self.voiceover(
            "What the desk records, for every order. <bookmark mark='a'/> Before: its share of expected volume, the "
            "square-root estimate with its uncertainty, the signal's half-life, and the schedule. "
            "<bookmark mark='b'/> During: participation, the path against the schedule, and the microprice before each "
            "child order. <bookmark mark='c'/> After: the shortfall against arrival, split into its parts, the "
            "markouts, and the realised cost against the estimate, pooled over many orders until the noise averages "
            "out. That record is what later parts use to measure capacity."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
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
            "The same sizing as a picture. <bookmark mark='a'/> The square-root cost of an order on Bitcoin's perpetual "
            "against its size, from a hundred thousand dollars to a billion. <bookmark mark='b'/> The signal's ten "
            f"basis points cross it at about {cap_m:.0f} million dollars. Left of the dot the trade pays; right of "
            "it the market is paid. Every strategy the House runs has a picture like this, and its size sits well to "
            "the left."
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
        tab = VGroup(*[VGroup(label(a_, font_size=15, color=QC.HOUSE), label(b_, font_size=15, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a_, b_ in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 9.6)
        tab.next_to(chart, DOWN, buff=0.25)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 37: every order reaches the market with a pre-trade cost from the square root, a "
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
            desk_question(r"the impact model with a free lunch", r"ask whether its kernel is positive definite, convex "
                          r"and decreasing; if the optimiser sells in order to buy, the model is wrong (Chapter 4)",
                          width=12.0, font_size=19),
            desk_question(r"the broker who beat VWAP", r"ask for the arrival-price shortfall, the order's share of "
                          r"volume, and the markouts (Chapter 8)", width=12.0, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The rule against three cases. <bookmark mark='a'/> A backtest with no costs: ask for the square-root cost "
            "at its size, and the size at which it eats the alpha. <bookmark mark='b'/> An impact model with a free "
            "lunch: ask whether its kernel is positive definite, convex and decreasing. If the optimiser sells in order "
            "to buy, the model is wrong. <bookmark mark='c'/> A broker who beat VWAP: ask for the arrival-price "
            "shortfall, the order's share of volume, and the markouts."
        ) as vo:
            for k_, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
