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
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("coin"), load("merton_us"), load("kelly_us"), load("bsde"), load("ppo"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, c, m, k, b, p):
        items = [
            (r"a 60\% coin at even odds: bet 20\%; about 30\% of trained players went bust", OVER),
            (r"utility turns a gamble into a certainty equivalent; $\gamma$ measures the bend", VALUE),
            (r"Bellman: solve backwards; HJB: the same, in continuous time, solved here on a grid", VALUE),
            (rf"Merton on 94 years of US stocks: {100 * m['fraction'][0]:.0f}\% at $\gamma = 1$, "
             rf"{100 * m['fraction'][2]:.0f}\% at $\gamma = 3$, with wide error bands", KELLY),
            (rf"Kelly measured on history: {100 * k['best']:.0f}\%; half Kelly keeps three quarters of the growth", KELLY),
            (r"Samuelson: Kelly usually ends richer, yet a cautious investor rightly refuses it", ALT),
            (r"LTCM: leverage sized in calm markets is far beyond Kelly in a storm", OVER),
            (rf"frontiers: a BSDE prices with two interest rates; PPO finds Merton's {100 * p['discrete']:.0f}\% unaided",
             GOOD),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 8 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part eight in eight lines. With a sixty percent coin at even odds, bet twenty percent; nearly a third of "
            "trained players went bust instead. Utility turns a gamble into a certainty equivalent, and gamma "
            "measures how much the curve bends. Bellman's principle solves decisions backwards; the HJB equation is "
            "the same idea in continuous time, and we solved it on a grid. Merton's fraction, on ninety-four years "
            f"of American stocks, is {100 * m['fraction'][0]:.0f} percent for log utility and "
            f"{100 * m['fraction'][2]:.0f} for gamma three, with wide error bands. Kelly, measured on history, "
            f"peaks at {100 * k['best']:.0f} percent, and half Kelly keeps three quarters of the growth. Kelly "
            "usually ends richer, yet a cautious investor rightly refuses it. Leverage sized in calm markets is far "
            "beyond Kelly in a storm. And at the frontier, a backward equation prices with two interest rates, and "
            "a reinforcement learner finds Merton's answer by itself."
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
            "Three desk questions. The sixty percent coin: bet twenty percent, which grows your wealth about two "
            "percent a flip; at forty percent you stop growing. <bookmark mark='a'/> A strategy with a Sharpe ratio "
            "of one at ten percent volatility: Kelly says ten times leverage. Don't: four years of a Sharpe of one "
            "is barely evidence, and volatility can triple. <bookmark mark='b'/> And why might a patient investor "
            "refuse Kelly? Because maximizing growth is maximizing the expected log, which is right only for one "
            "particular risk aversion. Full solutions are in the notes."
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
            "And five problems: Kelly's formula for any odds, Merton's value function, fractional Kelly, the "
            "secretary's one over e, and how much to stake on Peters' coin. Solutions, in English and Chinese, are "
            "in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
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
            [r"Pham, \textit{Continuous-time Stochastic Control and Optimization with Financial Applications}, ch.\ 3--6",
             r"Back, \textit{Asset Pricing and Portfolio Choice Theory}, ch.\ 1--2, 14",
             r"Carmona and Delarue, \textit{Probabilistic Theory of Mean Field Games}; Touzi, \textit{Optimal Stochastic "
             r"Control, Stochastic Target Problems, and Backward SDE}"],
            [r"Bernoulli (1738); von Neumann and Morgenstern (1944); Bellman (1957); Arrow (1965); Pratt (1964)",
             r"Kelly (1956); Breiman (1961); Merton (1969, 1971); Samuelson (1969, 1979); Thorp (2006)",
             r"Kahneman and Tversky (1979); Ellsberg (1961); Gilboa and Schmeidler (1989); Maenhout (2004)",
             r"Crandall and Lions (1983); Pardoux and Peng (1990); El Karoui, Peng and Quenez (1997)",
             r"Lasry and Lions (2007); Huang, Malham\'e and Caines (2006); Schulman et al.\ (2017); Peters (2019)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code: Kenneth French's market returns for the history, and seeded simulations, labelled "
            "on screen, for the rest."
        ):
            self.play(FadeIn(card))
            self.wait(3)
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
