from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load

DESK = [
    (r"What is $\mathbb{E}[W_t^4]$?", r"$3t^2$: $W_t \sim N(0, t)$ and a Gaussian's fourth moment is $3\sigma^4$; or by "
                                       r"It\^o, $d(W^4) = 4W^3\,dW + 6W^2\,dt$, so $\tfrac{d}{dt}\mathbb{E}[W^4] = 6t$"),
    (r"What is the probability that Brownian motion hits $+1$ before $-2$?",
     r"$2/3$: $W$ is a martingale, so $1 \cdot p - 2(1 - p) = 0$"),
    (r"Price a digital call (pays 1 if $S_T > K$) in Black--Scholes, using Girsanov.",
     r"$e^{-rT} Q(S_T > K) = e^{-rT} N(d_2)$: under $Q$, $\log S_T$ is normal with mean "
     r"$\log S_0 + (r - \tfrac12\sigma^2)T$"),
]

PROBLEMS = [
    r"Show that $\sum |\Delta W|$ over a grid of $n$ steps on $[0, 1]$ has mean $\sqrt{2n/\pi}$, and $\sum (\Delta W)^2$ has "
    r"mean 1 and variance $2/n$.",
    r"Compute $\int_0^T W\,dW$ as a limit of left-point sums, and then of midpoint sums. Which one is a martingale in $T$?",
    r"Derive Milstein's correction for $dX = a\,dt + b(X)\,dW$ from It\^o's lemma applied to $b(X)$ over one step.",
    r"For Vasicek, show that $r_T$ is Gaussian and find its mean and variance. What is the long-run probability of a "
    r"negative rate with the fitted $\kappa = 0.099$, $\theta = 4.1\%$, $\sigma = 1.4\%$?",
    r"A Hawkes process has $\mu = 0.1$, $\alpha = 0.8$, $\beta = 2$ (per day). What is its long-run rate? What fraction of "
    r"events are triggered by earlier ones?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.s = load("signature")
        self.j = load("jumps")
        self.h = load("hawkes")
        self.r = load("rough")
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        items = [
            (r"Brownian motion is the universal limit; its quadratic variation is time: $(dW)^2 = dt$", BM),
            (rf"on Bitcoin, sampling every minute measures {100 * self.s['vol_annual'][0]:.0f}\% volatility, every day "
             rf"{100 * self.s['vol_annual'][-1]:.0f}\%: microstructure noise", BM),
            (r"It\^o evaluates before the move, so gains are martingales; Milstein's term doubles the order", ITO),
            (r"mean reversion fits Treasury bills, but the fitted model mispriced 2020's curve", DRIFT),
            (r"Girsanov: drift is a change of measure, volatility is not; importance sampling cut variance 52$\times$", STRAT),
            (r"local time: the free stop-loss hedge loses the option's whole time value", JUMP),
            (rf"jumps: {self.j['n_jumps']} Bitcoin hours beyond 5 sd carry {100 * self.j['share_of_variance']:.0f}\% of "
             rf"variance; large moves self-excite, branching {self.h['fit']['branching']:.2f}", JUMP),
            (rf"volatility is rough: $H \approx {self.r['hurst']['H']:.2f}$; signatures read a path's order", ITO),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=c), label(t, font_size=25)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 5 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part five in eight lines. Brownian motion is the universal limit of random walks, and its quadratic "
            "variation is time. On Bitcoin, the variance you measure depends on how often you look, because of "
            "microstructure noise. Itô's integral evaluates before the move, so trading gains are martingales, and "
            "Milstein's extra term doubles a scheme's accuracy. Mean reversion fits Treasury bills, yet the fitted "
            "model mispriced the 2020 curve. Girsanov turns drift into a change of measure, which makes rare events "
            "cheap to simulate. Local time is why the free hedge costs the option's price. Jumps carry a quarter of "
            "Bitcoin's variance, and large moves excite more of them. And volatility is rough."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions, all classics. The expected fourth power of Brownian motion at time t is three t "
            "squared. <bookmark mark='a'/> The chance that Brownian motion hits plus one before minus two is two "
            "thirds, by optional stopping, exactly as for the walk in Part four. <bookmark mark='b'/> And a digital "
            "call in Black and Scholes is worth the discounted risk-neutral probability of finishing in the money: "
            "N of d two. Full solutions are in the notes."
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
            "And five problems: the variations of Brownian motion, the two integrals of W against itself, Milstein's "
            "correction, the Vasicek distribution, and a Hawkes process's long-run rate. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"Girsanov and the risk-neutral measure", [9, 10]),
            (r"local time and hedging near the strike", [10, 11]),
            (r"mean reversion and term-structure models", [18, 19]),
            (r"jumps, Hawkes and rough volatility", [13, 14, 36]),
            (r"the simulation library and signatures", [16, 17, 42]),
        ])
        with self.voiceover(
            "Where this comes back. Girsanov is the step from the real world to the pricing world in Parts nine and "
            "ten, and local time explains the hedging error near the strike in ten and eleven. Mean reversion "
            "returns in the rates parts, eighteen and nineteen. Jumps, Hawkes processes and rough volatility return "
            "in thirteen, fourteen and thirty-six. And the simulation library and signatures power the computing "
            "parts, sixteen and seventeen, and the machines of forty-two."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Shreve, \textit{Stochastic Calculus for Finance II}, ch.\ 3--11",
             r"\O ksendal, \textit{Stochastic Differential Equations}; Karatzas and Shreve, \textit{Brownian Motion and "
             r"Stochastic Calculus}",
             r"Cont and Tankov, \textit{Financial Modelling with Jump Processes}, ch.\ 2--8; Bj\"ork, \textit{Arbitrage "
             r"Theory in Continuous Time}, ch.\ 4--5",
             r"Kloeden and Platen, \textit{Numerical Solution of Stochastic Differential Equations}; Glasserman, "
             r"\textit{Monte Carlo Methods in Financial Engineering}"],
            [r"Donsker (1951); Vasicek (1977); Cox, Ingersoll and Ross (1985); Carr and Jarrow (1990)",
             r"Merton (1976); Hawkes (1971); Ogata (1981); Barndorff-Nielsen and Shephard (2004)",
             r"Andersen, Bollerslev, Diebold and Labys (2000); Zhang, Mykland and A\"it-Sahalia (2005)",
             r"Mandelbrot and Van Ness (1968); Gatheral, Jaisson and Rosenbaum (2018); Chen (1957); Lyons (1998)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code: Bitcoin by the minute and by the hour from Binance, and Treasury bill and bond yields "
            "from the St. Louis Fed."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 6, Financial Econometrics", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now simulate almost anything. <bookmark mark='a'/> Next, Part six: financial econometrics. "
            "How to estimate the parameters of these models from data that is short, noisy and overlapping, and how "
            "not to fool yourself while doing it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
