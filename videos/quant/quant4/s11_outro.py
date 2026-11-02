from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, INFO, LOSS, MART, P_C, PART, Q_C, load

DESK = [
    (r"A martingale starts at 1 and stops when it first hits 0 or 3. What is the probability it hits 3?",
     r"$1/3$: by optional stopping, $3p + 0(1 - p) = 1$ (the walk is bounded until it stops)"),
    (r"How many tosses of a fair coin do you expect before you see two heads in a row?",
     r"6: let a gambler arrive before each toss and bet on HH at fair odds; the casino's total payout when HH appears "
     r"is $4 + 2 = 6$, and its takings equal the number of tosses"),
    (r"You have \$100 at a European roulette table and need \$200 tonight. How do you bet?",
     r"all on red, once: $18/37 \approx 48.6\%$; one dollar at a time gives under 0.5\%"),
]

PROBLEMS = [
    r"Show that $S_n^2 - n$ is a martingale for a fair $\pm 1$ walk. Use optional stopping to find the expected time for "
    r"the walk to first reach $\pm a$.",
    r"For a game with win probability $p$, show $(q/p)^{X_n}$ is a martingale and derive the ruin probability. Evaluate "
    r"it for European roulette, $a = 10$, $b = 20$.",
    r"Doubling with a bankroll of $2^k - 1$: show each session's expected gain is zero, and find the expected number of "
    r"sessions before ruin.",
    r"For coins $p = 0.5$ and $q = 0.6$, show $\mathbb{E}_P[L_n] = 1$ but $\tfrac{1}{n}\log L_n \to -D(P\,\|\,Q)$. "
    r"Compute $D$ and predict the median of $L_{300}$.",
    r"Prove Ville's inequality from optional stopping at $\min(\tau, n)$. Why does a $t$-test checked every day "
    r"eventually reject a true null with probability one?",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.p = load("peeking")
        self.recap()
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self):
        items = [
            (r"information is a filtration; conditional expectation is a projection, and projections nest", INFO),
            (r"a martingale's forecast of tomorrow is today: Ville named it after a betting system", MART),
            (r"optional stopping: you can't beat a fair game with bounded bets; doubling needs unbounded ones", MART),
            (r"a small edge against you is ruin for timid play; bold play is optimal (Dubins--Savage)", LOSS),
            (r"Barings: a hidden account turned a doubling strategy into the bank's bankroll", LOSS),
            (r"Doob: a price is predictable drift plus a martingale; the variance is the square's predictable part", DRIFT),
            (r"a change of measure reweights worlds; equivalent measures agree on what is impossible", Q_C),
            (rf"stable laws fit the center ($\alpha \approx 1.4$) but variance is finite; checking daily, a $t$-test "
             rf"rejects {100 * self.p['t_reject']:.0f}\%, an e-process {100 * self.p['e_reject']:.0f}\%", P_C),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=c), label(t, font_size=25)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 4 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part four in eight lines. Information is a filtration, and conditional expectation is a projection onto "
            "what you know. A martingale is a process whose forecast of tomorrow is today; Ville named it after a "
            "betting system. Optional stopping says no strategy with bounded bets beats a fair game, and doubling "
            "escapes only by betting without limit. Against a small edge, timid play is ruin and bold play is "
            "optimal. At Barings, a hidden account supplied the unlimited bankroll. Doob splits any price into "
            "predictable drift and a martingale, and the variance is the predictable part of its square. A change of "
            "measure reweights the worlds, and equivalent measures agree on what is impossible. And stable laws fit "
            "the center of returns, but variance is finite; and a test you check every day must be an e-process."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=25) for q, a in DESK]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        with self.voiceover(
            "Three desk questions. A martingale starts at one and stops at zero or three: the chance it hits three is "
            "a third, by optional stopping. <bookmark mark='a'/> The expected number of fair tosses until two heads "
            "in a row is six. The neat proof: let a new gambler arrive before every toss and bet on heads, heads at "
            "fair odds. When the pattern appears, the casino has paid out six and collected one per toss, and a fair "
            "casino breaks even. <bookmark mark='b'/> And with a hundred dollars at a European roulette table and a "
            "need for two hundred tonight, put it all on red, once. Full solutions are in the notes."
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
            "And five problems: the time for a walk to leave a strip, the ruin probability for a biased game, the "
            "doubling system's real record, why likelihood ratios collapse, and a proof of Ville's inequality. "
            "Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"martingales and quadratic variation", [5, 7]),
            (r"change of measure: the risk-neutral world", [9, 10, 23]),
            (r"admissible strategies and no arbitrage", [9]),
            (r"heavy tails and changing volatility", [7, 13, 40]),
            (r"e-processes: testing what you keep looking at", [26, 43]),
        ])
        with self.voiceover(
            "Where this comes back. Martingales and quadratic variation are the foundation of Itô's calculus in Part "
            "five and of volatility models in Part seven. The change of measure becomes the risk-neutral world of "
            "Parts nine and ten, and the stochastic discount factor of twenty-three. Admissible strategies are how "
            "Part nine rules out doubling. Heavy tails return with changing volatility in seven and thirteen, and "
            "with risk measurement in forty. And e-processes are how Part twenty-six, and the finale, decide which "
            "results to believe."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Williams, \textit{Probability with Martingales}, ch.\ 9--12",
             r"Shreve, \textit{Stochastic Calculus for Finance I}, ch.\ 2--3; F\"ollmer and Schied, \textit{Stochastic "
             r"Finance}, ch.\ 1",
             r"Durrett, \textit{Probability: Theory and Examples}, ch.\ 4",
             r"Shafer and Vovk, \textit{Game-Theoretic Foundations for Probability and Finance} (2019)"],
            [r"Ville (1939); Doob (1953); Dubins and Savage, \textit{How to Gamble If You Must} (1965)",
             r"Mandelbrot (1963); Fama (1965); McCulloch (1986); Mantegna and Stanley (1995)",
             r"Ramdas, Gr\"unwald, Vovk and Shafer, ``Game-theoretic statistics and safe anytime-valid inference'' (2023)",
             r"Board of Banking Supervision, report on the collapse of Barings (1995)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. Every number was computed by the "
            "series' own code: Kenneth French's daily market since 1926, Binance's Bitcoin, and the Nikkei from the "
            "St. Louis Fed."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 5, Stochastic Calculus", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House has its monitor. <bookmark mark='a'/> Next, Part five: stochastic calculus. We let the coin "
            "tosses become infinitely fast, and the random walk becomes Brownian motion, with its own calculus, built "
            "on the quadratic variation we met in this part."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
