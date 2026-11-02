from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, PART, PUT, Q_C, load

DESK = [
    (r"Call 10, put 7, strike 100, spot 103, no rates. Arbitrage?",
     r"no: $C - P = 3 = S - K$. At a put of 6, buy it, sell the call, buy the stock and borrow 99: the package pays 100 "
     r"for sure, a riskless 1; at a put of 8, do the reverse"),
    (r"A box spread on strikes 100 and 110, one year, with rates at 4\%. What should it cost, and what is it?",
     r"$10\,e^{-0.04} \approx 9.61$: it pays 10 in every state, so it is a loan; quoted cheaper, you lend through it, "
     r"dearer, you borrow"),
    (r"Is a box of American options riskless?",
     r"no: the short leg can be exercised early, and the position then holds stock and needs financing; the "
     r"no-arbitrage argument assumed European exercise (Robinhood, 2019)"),
]

PROBLEMS = [
    r"Prove put--call parity for European options by a no-arbitrage argument, with a borrowing fee $h$ on the stock.",
    r"Prove the one-period fundamental theorem from Stiemke's lemma: either $\psi > 0$ with $D\psi = p$, or $\theta$ with "
    r"$\theta \cdot p \le 0$ and $D^\top \theta \ge 0$, $D^\top\theta \ne 0$, but not both.",
    r"Derive the binomial risk-neutral probability and show that it lies in $(0, 1)$ if and only if "
    r"$d < e^{r\Delta t} < u$.",
    r"Show that a butterfly with strikes $K - h, K, K + h$, scaled by $1/h^2$, tends to $e^{-rT} q(K)$.",
    r"A stock at 100 can be worth 80, 100 or 125 tomorrow, with zero rates. Find the no-arbitrage interval for a call "
    r"struck at 100, by super-replication and by its dual over risk-neutral measures.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("parity"), load("density"), load("mot"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def recap(self, p, d, m):
        a, b = d["expiries"]
        items = [
            (rf"put--call parity on {p['n_pairs']} bitcoin option pairs holds to {p['trade_p50']:.1f} basis points, and "
             r"reveals a 3--5\% interest rate", FWD),
            (r"where shorting is costly, parity prices the cost; a box spread is a loan, if exercise is European", ARB),
            (r"no arbitrage $\iff$ positive state prices: a separating hyperplane (Harrison--Kreps)", Q_C),
            (r"state prices, the discount factor and $Q$ are one object in three units", Q_C),
            (r"two states complete the market; three leave an interval, which super-replication computes", ALT),
            (r"Harrison--Pliska, Delbaen--Schachermayer; any positive asset can be the numeraire", ALT),
            (rf"the Surface's density: a 20\% fall in {b['T'] * 365:.0f} days has a $Q$-probability of "
             rf"{100 * b['p_down20']:.0f}\%; Ross recovery needs an untestable assumption", CALL),
            (rf"vanilla prices bound a forward-start straddle to [{m['lower']:.3f}, {m['upper']:.3f}] with no model", CALL),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=28, color=col), label(t, font_size=24)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        title = label(r"Part 9 in eight lines", font_size=38).to_edge(UP, buff=0.4)
        rows.next_to(title, DOWN, buff=0.45)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        with self.voiceover(
            "Part nine in eight lines. Put-call parity holds on hundreds of Bitcoin option pairs to a few basis "
            "points, and reveals a three to five percent interest rate. Where shorting is costly, parity prices the "
            "cost, and a box spread is a loan, if exercise is European. No arbitrage means positive state prices: a "
            "separating hyperplane. State prices, the discount factor and Q are one object in three units. Two states "
            "make a market complete; three leave an interval, which super-replication computes. The theorem extends "
            "to continuous time, with any positive asset as numeraire. The Surface's density says how much the "
            "market pays for crash states, and Ross's recovery of real probabilities rests on an assumption prices "
            "cannot test. And vanilla prices alone bound exotic ones, with no model at all."
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
            "Three desk questions. The call at ten and the put at seven: no arbitrage, both sides are three. "
            "<bookmark mark='a'/> A box between a hundred and a hundred and ten, one year, rates at four percent, "
            "should cost ten times e to the minus four percent, about nine sixty-one; it is a loan. "
            "<bookmark mark='b'/> And a box of American options is not riskless: the short leg can be exercised "
            "early. Full solutions are in the notes."
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
            "And five problems: parity with a borrowing fee, the fundamental theorem from Stiemke's lemma, the "
            "binomial probability, the butterfly and the density, and a trinomial interval by linear programming "
            "and its dual. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=4))
            self.wait(4)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"replication in continuous time: Black--Scholes--Merton", [10]),
            (r"the risk-neutral density and the volatility surface", [12]),
            (r"model-free bounds and model choice for exotics", [14, 15]),
            (r"forward and annuity measures", [18, 19]),
            (r"the stochastic discount factor", [23]),
            (r"borrow, funding and the limits of arbitrage", [21, 41]),
        ])
        with self.voiceover(
            "Where this comes back. Replication in continuous time is Part ten, Black, Scholes and Merton. The "
            "density from the smile becomes the volatility surface of Part twelve, and model-free bounds frame the "
            "exotic options of Parts fourteen and fifteen. Forward and annuity measures price the rates products of "
            "Parts eighteen and nineteen. The discount factor is the heart of Part twenty-three. And the frictions "
            "that break parity, borrowing and funding, return in Parts twenty-one and forty-one."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Shreve, \textit{Stochastic Calculus for Finance I}; Bj\"ork, \textit{Arbitrage Theory in Continuous Time}, "
             r"ch.\ 1--3, 10, 26",
             r"Duffie, \textit{Dynamic Asset Pricing Theory}, ch.\ 1--2, 6; Delbaen and Schachermayer, \textit{The "
             r"Mathematics of Arbitrage}",
             r"Henry-Labord\`ere, \textit{Model-Free Hedging}"],
            [r"Arrow (1964); Debreu (1959); Stoll (1969); Ross (1978); Breeden and Litzenberger (1978)",
             r"Cox, Ross and Rubinstein (1979); Harrison and Kreps (1979); Harrison and Pliska (1981)",
             r"Dalang, Morton and Willinger (1990); Delbaen and Schachermayer (1994); Geman, El Karoui and Rochet (1995)",
             r"Hobson (1998); Ofek, Richardson and Whitelaw (2004); Beiglb\"ock, Henry-Labord\`ere and Penkner (2013)",
             r"Ross (2015); Borovi\v{c}ka, Hansen and Scheinkman (2016)"])
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on. The data are the Surface's trades, "
            "a day of Bitcoin options on Deribit, and every bound and recovery was computed by the House's "
            "arbitrage checker."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("data",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 10, Black--Scholes--Merton", font_size=32, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House can now tell a price from an arbitrage. <bookmark mark='a'/> Next, Part ten: Black, Scholes "
            "and Merton. Let the tree's steps shrink to nothing, and the fundamental theorem becomes the most famous "
            "formula in finance, and the volatility desk opens."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
