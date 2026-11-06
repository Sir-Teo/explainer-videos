from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant4.common import DRIFT, INFO, LOSS, MART, P_C, PART, Q_C, load

DESK = [
    (r"A martingale starts at 1 and stops when it first hits 0 or 3. What is the probability it hits 3?",
     r"$1/3$: by optional stopping, $3p + 0(1 - p) = 1$ (the walk is bounded until it stops)"),
    (r"How many tosses of a fair coin do you expect before you see two heads in a row?",
     r"6: let a gambler arrive before each toss and bet on HH at fair odds; the casino's total payout when HH appears "
     r"is $4 + 2 = 6$, and its takings equal the number of tosses"),
    (r"In the classic target-before-ruin model, compare \$100 aiming for \$200: one all-in bet or one-unit bets?",
     r"all on red, once: $18/37 \approx 48.6\%$; one dollar at a time gives under 0.5\%"),
    (r"Penney's game: you pick HHT, I pick THH. Who wins, and how often?",
     r"THH, with probability $3/4$: unless the first two tosses are HH, any HHT must be preceded by THH"),
    (r"A fair $\pm 1$ walk is stopped the first time it is up 1. What is $\mathbb{E}\tau$?",
     r"Infinite: if it were finite, Wald's identity would give $1 = \mathbb{E}S_\tau = 0 \cdot \mathbb{E}\tau = 0$"),
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
    r"Prove Ville's inequality from optional stopping at $\min(\tau, n)$. Why does a fixed $z$ cutoff checked every day "
    r"eventually reject a true null with probability one?",
    r"P\'olya's urn from one red and one blue ball: show $P(R_n = k) = 1/(n + 1)$ for $k = 1, \dots, n + 1$, so the "
    r"limit of the red fraction is Uniform$(0, 1)$.",
    r"Prove Wald's identity $\mathbb{E}S_\tau = \mu\,\mathbb{E}\tau$ when $\mathbb{E}\tau < \infty$, from the "
    r"martingale $S_n - n\mu$ and optional stopping.",
    r"(qual) For iid $N(0, 1)$ steps, prove $\limsup S_t/\sqrt{2t\log\log t} \le 1$ a.s. by Doob's maximal "
    r"inequality on geometric blocks and Borel--Cantelli.",
    r"(qual) Derive Robbins's mixture $M_t$ and show $\Pr\big(\exists t: |S_t| \ge \sqrt{(t + \rho)\log\frac{t + \rho}"
    r"{\rho\alpha^2}}\big) \le \alpha$.",
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
            (r"a $\sigma$-algebra is what you can answer; conditional expectation is a projection, and projections nest", INFO),
            (r"a martingale's forecast of tomorrow is today (Ville, Doob); convex functions of it rise", MART),
            (r"the martingale transform: no predictable stake beats a fair game; roulette taxes every system 1/37", MART),
            (r"stopping times; optional stopping proved; the walk that always wins has $\mathbb{E}\tau = \infty$", MART),
            (r"doubling needs unbounded credit: admissibility forbids it; Barings found it in account 88888", LOSS),
            (r"ruin $a/b$ and duration $a(b - a)$; bold play optimizes the classic subfair target-before-ruin model", LOSS),
            (r"bounded martingales converge: upcrossings, P\'olya's urn, L\'evy's learning", INFO),
            (r"Doob: drift plus martingale, and the drift depends on the filtration (Ivey)", DRIFT),
            (r"change of measure moves weight, not paths; Esscher's $Q$ fattens the crash tail", Q_C),
            (r"Radon--Nikodym by martingales; Kakutani: infinite coins are equivalent or singular", Q_C),
            (r"stable fits disagree and sample kurtosis changes with horizon: evidence, not a moment-existence proof", P_C),
            (rf"Ville: repeated fixed-$z$ checks reject {100 * self.p['t_reject']:.0f}\%, an e-process "
             rf"{100 * self.p['e_reject']:.0f}\%; bettors learn, e-BH survives peeking", MART),
        ]
        rows = VGroup()
        for i, (t, c) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=c), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        title = label(r"Part 4 in twelve lines", font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(title, DOWN, buff=0.3)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
            rows.next_to(title, DOWN, buff=0.3)
        with self.voiceover(
            "Part four in twelve lines. A sigma-algebra is the set of questions you can answer, and conditional "
            "expectation is a projection onto it. A martingale's forecast of tomorrow is today. No predictable stake "
            "turns a fair game favourable, and roulette taxes every system the same. Optional stopping holds with "
            "its stopping-time and integrability conditions; bounded bets alone do not suffice. Doubling needs "
            "unbounded credit, which finance forbids and Barings found in a hidden account. Ruin is a over b, and "
            "bold play solves the classic subfair target-before-ruin model. Martingales that stay bounded converge. Doob splits a process into drift "
            "and martingale, and the drift depends on what you know. A change of measure moves weight, not paths, "
            "and martingales build the Radon-Nikodym derivative. The stable-fit diagnostics are evidence, not "
            "proof of finite population moments. Properly calibrated e-processes allow learned stakes and repeated looks."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK[:3]]).arrange(DOWN, buff=0.3)
        if cards.height > 7.4:
            cards.scale_to_fit_height(7.4)
        more = VGroup(*[desk_question(q, a, width=12.4, font_size=24) for q, a in DESK[3:]]).arrange(DOWN, buff=0.4)
        with self.voiceover(
            "Five desk questions. A martingale starts at one and stops at zero or three: the chance it hits three is "
            "a third, by optional stopping. <bookmark mark='a'/> The expected number of fair tosses until two heads "
            "in a row is six, by the casino of gamblers. <bookmark mark='b'/> With a hundred dollars at a European "
            "roulette table in the classic target-before-ruin model, one all-in red bet has higher success "
            "probability than one-unit bets. <bookmark mark='c'/> In "
            "Penney's game, if you choose heads, heads, tails, I choose tails, heads, heads and win three times in "
            "four. <bookmark mark='d'/> And a fair walk stopped the first time it is up one takes, on average, "
            "forever. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(cards), FadeIn(more[0], shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(more[1], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And nine problems: the time for a walk to leave a strip, the ruin probability for a biased game, the "
            "doubling system's real record, why likelihood ratios collapse, a proof of Ville's inequality, the limit "
            "of Pólya's urn, Wald's identity, and two at the level of a qualifying exam: the upper half of the law of the "
            "iterated logarithm, and Robbins's always-valid boundary. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"martingales and quadratic variation", [5, 7]),
            (r"change of measure: the risk-neutral world", [9, 10, 23]),
            (r"admissible strategies and no arbitrage", [9]),
            (r"convex functions of martingales: calendar spreads", [12]),
            (r"the Kelly (numeraire) portfolio", [8]),
            (r"heavy tails and changing volatility", [7, 13, 40]),
            (r"e-processes and e-BH: testing what you keep looking at", [26, 43]),
        ])
        with self.voiceover(
            "Where this comes back: quadratic variation in Parts five and seven; the risk-neutral world in nine, ten "
            "and twenty-three; admissibility in nine; calendar spreads in twelve; the numéraire portfolio in eight; "
            "heavy tails in seven, thirteen and forty; and e-processes in twenty-six and the finale."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r) for r in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Williams, \textit{Probability with Martingales}, ch.\ 0, 4, 9--14, 16--18",
             r"Shreve, \textit{Stochastic Calculus for Finance} I, ch.\ 2, 3, 5; II, ch.\ 1--2",
             r"F\"ollmer and Schied, \textit{Stochastic Finance}, \S 1.2 and App.\ A.2; Durrett, ch.\ 4",
             r"Shafer and Vovk (2001, 2019); Ramdas and Wang, \textit{Hypothesis Testing with E-values} (2025)"],
            [r"Kolmogorov (1933); Ville (1939); Wald (1945); Kakutani (1948); Doob (1953); Dubins and Savage (1965); "
             r"Azuma (1967)",
             r"Esscher (1932); Li (1980); Harrison and Pliska (1981); Dybvig and Huang (1988); Gerber and Shiu (1994)",
             r"Mandelbrot (1963); Fama (1965); Koutrouvelis (1980); McCulloch (1986); Mantegna and Stanley (1995)",
             r"Ramdas, Gr\"unwald, Vovk and Shafer (2023); Wang and Ramdas (2022); Waudby-Smith and Ramdas (2024)",
             r"Augenblick and Rabin (2021); Kaunitz, Zhong and Kreiner (2017); Board of Banking Supervision (1995)"],
            font_size=19)
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on; the notes map every textbook section "
            "to its chapter. Every number was computed by the series' own code: Kenneth French's daily market since "
            "1926, Binance's Bitcoin, and the Nikkei from the St. Louis Fed."
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
