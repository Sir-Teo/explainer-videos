from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, BAD, GOOD, KELLY, OVER, PART, UNDER, VALUE, load

DESK = [
    (r"A coin lands heads 60\% of the time; you may bet any fraction of your wealth at even odds, again and again. "
     r"What fraction?",
     r"Kelly: $f^* = p - q = 20\%$, growing about 2\% a flip; at 40\% you no longer grow. With a cap and a time limit, "
     r"slightly less does as well (in 300 flips with a \$250 cap, 10\% and 20\% both reach it about 94\% of the time)"),
    (r"A strategy has a Sharpe ratio of 1 at 10\% volatility. What leverage does Kelly suggest, and would you use it?",
     r"$f^* = (\mu - r)/\sigma^2 = SR/\sigma = 10$. No: four years of a Sharpe of 1 has a standard error near 0.6 (Part "
     r"6), and the volatility can triple (LTCM); half Kelly or less, recomputed as volatility changes"),
    (r"Kelly maximizes long-run growth. Why might a long-horizon investor still not use it?",
     r"Samuelson: maximizing growth is maximizing $\mathbb{E}\log W$, which is right only for $\gamma = 1$; a more "
     r"risk-averse investor prefers $(\mu - r)/(\gamma\sigma^2)$ at every horizon, though Kelly usually ends richer"),
    (r"With a 1\% cost per dollar traded and $\gamma = 3$, your stock weight has drifted from 62\% to 66\%. Do you "
     r"trade?",
     r"No: 66\% is inside the no-trade band (about 56--68\% here, by dynamic programming). Trade only when the weight "
     r"leaves the band, and then only to its nearest edge"),
]

PROBLEMS = [
    r"For a bet that pays $b$ per unit with probability $p$, derive $f^* = p - q/b$ and show that, for a small edge, "
    r"growth is zero again at about $2f^*$.",
    r"Write the HJB equation for Merton's problem and show that $V = e^{a(T - t)}\,w^{1-\gamma}/(1 - \gamma)$ solves "
    r"it with $\pi^* = (\mu - r)/(\gamma\sigma^2)$; find $a$.",
    r"Show that betting $c$ times the Kelly fraction gives $(2c - c^2)$ of Kelly's excess growth with $c$ times its "
    r"volatility.",
    r"Show that the secretary rule's success probability tends to $-x\log x$ with $x = k/n$, maximized at $x = 1/e$.",
    r"In Peters' coin (+50\%, $-40\%$), what fraction of wealth should you stake each flip, and at what growth rate?",
    r"For the perpetual American put, show that maximizing $(K - b)\,b^{\beta}$ over $b$ gives $b^* = \beta K/(1 + "
    r"\beta)$, and that this is equivalent to smooth fit $V'(b^*) = -1$.",
    r"For $N$ symmetric traders with $\phi = 0$, solve $2\eta Q'' + \kappa\frac{N-1}{N}Q' = 0$, $Q(0) = 1$, "
    r"$Q(T) = 0$, and find the share sold by $T/5$ when $\kappa T/(2\eta) = 2$ and $N \to \infty$.",    r"(qual) With $\hat\mu \sim N(\mu, \sigma^2/T)$ and $\sigma$ known, show that the expected certainty equivalent of "
    r"$c\,\hat\mu/(\gamma\sigma^2)$ is $[c\theta^2 - c^2(\theta^2 + 1/T)/2]/\gamma$, that the plug-in loses in expectation "
    r"when $T < 1/\theta^2$, and that $c^* = T\theta^2/(T\theta^2 + 1)$.",
    r"(qual) Now estimate $\sigma^2$ by $s^2$ from $n$ iid normal returns. Using $\mathbb E[\sigma^2/s^2] = (n - 1)/(n - 3)$ "
    r"and $\mathbb E[\sigma^4/s^4] = (n - 1)^2/((n - 3)(n - 5))$, find the plug-in's expected certainty equivalent, and "
    r"show it is negative for $\theta = 0.4$, $T = 5$ years of monthly data.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("coin"), load("merton_us"), load("kelly_us"), load("davis_norman"), load("mfg_crowd"),
                   load("ppo_seeds"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, c, m, k, d, mf, ps):
        items = [
            (r"a 60\% coin at even odds: bet 20\%; at 100\%, most players go bust", OVER),
            (r"utility turns a gamble into a certainty equivalent; the premium is $\frac12\gamma\sigma^2$", VALUE),
            (r"Bellman solves backwards; the HJB is its continuous form; verification proves the guess", VALUE),
            (r"kinks need viscosity solutions, and grids need monotone schemes", VALUE),
            (rf"Merton: {100 * m['fraction'][2]:.0f}\% in US stocks at $\gamma = 3$, with wide error bands; spend a "
             r"constant share", KELLY),
            (rf"costs open a no-trade band, {100 * d['rows'][2]['lo']:.0f}--{100 * d['rows'][2]['hi']:.0f}\% at 1\%, "
             r"growing like $\varepsilon^{1/3}$", KELLY),
            (r"Kelly wins eventually (Breiman), slowly; overestimate the edge twofold and it earns nothing", KELLY),
            (r"Samuelson: growth is not utility; stopping is a rope over pegs, and smooth fit finds the boundary", ALT),
            (rf"a liquidating crowd sells {100 * mf['runs']['inf']['share_fifth']:.0f}\% in the first fifth; PPO finds "
             r"Merton, and struggles with costs", GOOD),
            (r"in practice: fractional Kelly, risk budgets, drawdown floors, volatility targeting", QC.FIRM),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title = label(r"Part 8 in ten lines", font_size=38).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part eight in ten lines. Bet twenty percent on the sixty percent coin. The premium for risk is half gamma times "
            "the variance. Bellman solves backwards, the HJB is its continuous form, and verification proves the guess. "
            "Kinks need viscosity solutions and monotone grids. Merton holds "
            f"{100 * m['fraction'][2]:.0f} percent in stocks at gamma three, with wide error bars, and spends a constant "
            "share. Costs open a band growing like the cube root of the cost. Kelly wins eventually, slowly, and earns "
            "nothing on an edge overestimated twofold. Growth is not utility; stopping is a rope over pegs. A crowd sells "
            "in a rush, and a learner finds Merton. And funds bet fractions inside risk budgets."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=14))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.6, font_size=22) for q, a in DESK]).arrange(DOWN, buff=0.22)
        if cards.height > 7.5:
            cards.scale_to_fit_height(7.5)
        with self.voiceover(
            "Four desk questions. The sixty percent coin: bet twenty percent, which grows your wealth about two "
            "percent a flip; at forty percent you stop growing. <bookmark mark='a'/> A strategy with a Sharpe ratio "
            "of one at ten percent volatility: Kelly says ten times leverage. Don't: four years of a Sharpe of one "
            "is barely evidence, and volatility can triple. <bookmark mark='b'/> Why might a patient investor "
            "refuse Kelly? Because maximizing growth is maximizing the expected log, which is right only for one "
            "particular risk aversion. <bookmark mark='c'/> And with a one percent cost, your stock weight drifted "
            "from sixty-two to sixty-six percent: do nothing, you are still inside the band. Full solutions are in "
            "the notes."
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
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And nine problems: Kelly's formula for any odds, Merton's value function, fractional Kelly, the "
            "secretary's one over e, how much to stake on Peters' coin, smooth fit for the perpetual put, and the "
            "liquidating crowd. Two are qualifying-exam problems: the exact cost of an estimated edge, and the "
            "correction when the variance is estimated too. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"optimal stopping and the American option", [10, 16]),
            (r"BSDEs, nonlinear pricing and funding costs", [17, 21]),
            (r"Kelly, Merton and position sizing in portfolios", [30, 31]),
            (r"mean-field games: order books and execution", [36, 37]),
            (r"reinforcement learning in hedging, execution and markets", [17, 37, 42]),
            (r"leverage, funding and LTCM in full", [41]),
        ])
        with self.voiceover(
            "Where this comes back. Optimal stopping prices the American option in Parts ten and sixteen. Backward "
            "equations return in deep hedging, and in Part twenty-one, where funding at different rates is exactly "
            "the nonlinearity we priced. Kelly and Merton size the portfolios of Parts thirty and thirty-one. "
            "Mean-field games model order books and execution. Reinforcement learning hedges, executes and trades "
            "in later parts. And Part forty-one tells LTCM's story in full."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Pham, \textit{Continuous-time Stochastic Control and Optimization with Financial Applications}, ch.\ 1--7",
             r"Touzi, \textit{Optimal Stochastic Control, Stochastic Target Problems, and Backward SDE}; Karatzas and "
             r"Shreve, \textit{Methods of Mathematical Finance}, ch.\ 3, 6; Bj\"ork, \textit{Arbitrage Theory in "
             r"Continuous Time}; \O{}ksendal, ch.\ 10--11",
             r"Merton, \textit{Continuous-Time Finance}, ch.\ 4--5; Back, \textit{Asset Pricing and Portfolio Choice "
             r"Theory}, ch.\ 1--2, 14; Bertsekas, vol.\ I; Sutton and Barto; Carmona and Delarue, vol.\ I"],
            [r"Bernoulli (1738); von Neumann and Morgenstern (1944); Allais (1953); Pratt (1964); Arrow (1965); Rabin (2000)",
             r"Bellman (1957); Merton (1969, 1971); Crandall and Lions (1983); Barles and Souganidis (1991); "
             r"Karatzas, Lehoczky and Shreve (1987); Cox and Huang (1989)",
             r"Magill and Constantinides (1976); Davis and Norman (1990); Shreve and Soner (1994); Janecek and Shreve "
             r"(2004); Rogers (2004)",
             r"Kelly (1956); Breiman (1961); Samuelson (1979); Thorp (2006); Benter (1994); Peters (2019); Toda (2023)",
             r"Snell (1952); Dynkin (1963); McKean (1965); Kahneman and Tversky (1979); Benartzi and Thaler (1995); "
             r"Maenhout (2004)",
             r"Pardoux and Peng (1990); El Karoui, Peng and Quenez (1997); Lasry and Lions (2007); Huang, Malham\'e "
             r"and Caines (2006); Schulman et al.\ (2017); Jia and Zhou (2023); Grossman and Zhou (1993)"], font_size=19)
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on; the full list, with the frontier "
            "papers, is in the notes. Every number was computed by the series' own code: Kenneth French's market "
            "returns for the history, and seeded simulations, labelled on screen, for the rest."
        ):
            self.play(FadeIn(card))
            self.wait(4)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 9, No Arbitrage", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now forecast risk and size its bets. That completes the toolkit. <bookmark mark='a'/> "
            "Next, Part nine, and the start of the derivatives act: no arbitrage. Why there is one price for a "
            "replicable payoff, the fundamental theorem of asset pricing, and the risk-neutral measure, built "
            "from the martingales of Part four."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
