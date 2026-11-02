from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import ALT, ARB, CALL, FWD, HEDGE, PART, PUT, Q_C, load

DESK = [
    (r"Call 10, put 7, strike 100, spot 103, no rates. Arbitrage?",
     r"no: $C - P = 3 = S - K$. At a put of 6, buy it, sell the call, buy the stock and borrow 99: the package pays 100 "
     r"for sure, a riskless 1; at a put of 8, do the reverse"),
    (r"A box spread on strikes 100 and 110, one year, with rates at 4\%. What should it cost, and what is it?",
     r"$10\,e^{-0.04} \approx 9.61$: it pays 10 in every state, so it is a loan; quoted cheaper, you lend through it, "
     r"dearer, you borrow. With American options it is not riskless (Robinhood, 2019)"),
    (r"Price a digital that pays 1 if $S_T > 100$, given calls at 99.5 and 100.5 priced 6.20 and 5.70.",
     r"a call spread divided by its width: $(6.20 - 5.70)/1 = 0.50$, the slope of the call curve; exact as the "
     r"strikes close in, since $-\partial C/\partial K = e^{-rT} Q(S_T > K)$"),
    (r"A parent company trades below the value of its stake in a listed subsidiary. Is it an arbitrage?",
     r"not a riskless one: the short leg must be borrowed and can be recalled, convergence may take longer than your "
     r"funding, and the link can be severed (Palm and 3Com; Mitchell, Pulvino and Stafford 2002)"),
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
    r"Show that the model-free band for a forward-start call $(S_2/S_1 - 1)^+$ is exactly half the band for the "
    r"forward-start straddle $|S_2/S_1 - 1|$.",
    r"Derive Margrabe's formula for the option to exchange asset 2 for asset 1 by changing numeraire to asset 2.",
]


class Outro(VoiceoverScene):
    def construct(self):
        env = load("envelope")
        self.checker(env)
        self.recap(load("parity"), load("futures_basis"), load("density_specs"), load("mot_grid"), load("neural_mot"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def checker(self, env):
        chart = house_chart(PART, lit=("data",)).scale(0.62).to_edge(UP, buff=0.2)
        rows = [
            (r"\texttt{parity\_gap}, \texttt{implied\_forward}", r"parity with rates and borrow; the forward from raw trades"),
            (r"\texttt{ftap}, \texttt{simplex}", r"state prices or an arbitrage, by linear programming"),
            (r"\texttt{superhedge}, \texttt{superhedge\_tree}", r"the no-arbitrage interval, in one period and through time"),
            (r"\texttt{static\_checks}, \texttt{calendar\_check}", r"calls decreasing, convex and bounded; variance "
                                                                  r"rising with maturity"),
            (r"\texttt{mot\_bounds}, \texttt{mot\_dual}, \texttt{entropic\_mot}", r"model-free bounds and their hedges"),
            (r"\texttt{power\_iteration}, \texttt{ross\_recovery}", r"Perron--Frobenius on state prices, with its caveat"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=19, color=QC.HOUSE), label(b, font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.4) for a, b in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        for r_ in tab:
            r_[1].align_to(tab, LEFT).shift(RIGHT * 6.2)
        tab.next_to(chart, DOWN, buff=0.3)
        if tab.width > 13.0:
            tab.scale_to_fit_width(13.0)
        rule = wrapped_label(r"Rule 10: no model is fitted to a surface that fails the arbitrage checker; it is repaired "
                             r"or rejected first, and a model whose prices fail it is rejected too.  "
                             rf"The trial counter still reads {env['trials']}: this part tested no strategy.", 12.4, 22,
                             QC.HOUSE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The House's arbitrage checker now holds this part's tools. <bookmark mark='a'/> Parity, and the forward "
            "read from raw trades. The fundamental theorem as a linear program, with the teaching simplex. "
            "Super-replication in one period and through time. The static and calendar checks. Model-free bounds, "
            "their hedges, and the entropic solver. And Ross recovery, with its warning label. "
            "<bookmark mark='b'/> The tenth rule: no model is fitted to a surface that fails these checks; the "
            "surface is repaired or rejected first, and a model whose own prices fail them is rejected too. This part "
            f"tested no strategy, so the trial counter still reads {env['trials']}."
        ) as vo:
            self.play(FadeIn(chart))
            self.play(Indicate(chart.desk["data"], color=QC.HOUSE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.4, run_time=5))
            vo.wait_until("b")
            self.play(FadeIn(rule))
        self.wait(0.4)
        self.clear_scene()

    def recap(self, p, fb, sp, gr, nm):
        fine = [r for r in gr["rows"] if "upper" in r][-1]
        items = [
            (rf"parity holds on {p['n_pairs']} bitcoin option pairs to {p['trade_p50']:.1f} bp, and its forward matches "
             rf"the futures to {fb['gap_p50']:.1f} bp", FWD),
            (r"where shorting is costly, parity prices the cost (Palm, GameStop); a box is a loan, if European", ARB),
            (r"no arbitrage $\iff$ strictly positive state prices: a separating plane, proved and found by a simplex", Q_C),
            (r"state prices, the discount factor and $Q$ are one object in three units; $Q$ is $P$ reweighted", Q_C),
            (r"two states replicate (the tree); three leave an interval, a linear program and its dual", HEDGE),
            (r"options complete the market; without them, super-replication is Black--Scholes at the widest volatility",
             HEDGE),
            (r"continuous time needs admissibility and NFLVR; strict local martingales are bubbles", ALT),
            (r"any positive asset can be the numeraire: $N(d_1)$, Margrabe, bitcoin as the unit", ALT),
            (rf"butterflies build the density; its tails depend on the fit (a 30\% fall: "
             rf"{100 * sp['down30_spread']:.1f} points of spread)", CALL),
            (rf"Ross recovery needs an untestable assumption; vanilla prices bound exotics with no model: "
             rf"[{fine['lower']:.3f}, {fine['upper']:.3f}] on the finest grid", CALL),
        ]
        rows = VGroup()
        for i, (t, col) in enumerate(items, 1):
            rows.add(VGroup(MathTex(str(i), font_size=26, color=col), label(t, font_size=22)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        title = label(r"Part 9 in ten lines", font_size=36).to_edge(UP, buff=0.35)
        rows.next_to(title, DOWN, buff=0.35)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        with self.voiceover(
            "Part nine in ten lines. Parity holds on Bitcoin options to a few basis points, and its forward matches "
            "the futures market. Where shorting is costly, parity prices the cost, and a box spread is a loan, if "
            "exercise is European. No arbitrage means strictly positive state prices: a separating plane, which a "
            "simplex finds. State prices, the discount factor and Q are one object in three units. Two states make "
            "a tree that replicates; three leave an interval, a linear program and its dual. Options complete the "
            "market, and without them the super-hedger prices at the widest volatility. Continuous time needs "
            "admissible strategies and no free lunch with vanishing risk, and it allows bubbles. Any positive asset "
            "can be the unit of account. Butterflies build the density, whose tails depend on the fit. And Ross "
            "recovery rests on an assumption prices cannot test, while vanilla prices bound exotic ones with no model "
            "at all."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                 run_time=20))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        cards = VGroup(*[desk_question(q, a, width=12.6, font_size=22) for q, a in DESK]).arrange(DOWN, buff=0.22)
        if cards.height > 7.6:
            cards.scale_to_fit_height(7.6)
        with self.voiceover(
            "Four desk questions. The call at ten and the put at seven: no arbitrage, both sides are three. "
            "<bookmark mark='a'/> A box between a hundred and a hundred and ten, one year, rates at four percent, "
            "should cost about nine sixty-one; it is a loan, and with American options it is not riskless. "
            "<bookmark mark='b'/> A digital from two calls: the call spread divided by its width, the slope of the "
            "call curve. <bookmark mark='c'/> And a negative stub is not a riskless arbitrage: the short leg can be "
            "recalled, and convergence can outlast your funding. Full solutions are in the notes."
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
        ps = problem_set(PROBLEMS, font_size=21)
        with self.voiceover(
            "And seven problems: parity with a borrowing fee, the fundamental theorem from Stiemke's lemma, the "
            "binomial probability, the butterfly and the density, the trinomial interval and its dual, the "
            "forward-start call's band, and Margrabe by change of numeraire. Solutions, in English and Chinese, are "
            "in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
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
            (r"ETF arbitrage and market making", [38]),
        ])
        with self.voiceover(
            "Where this comes back. Replication in continuous time is Part ten, Black, Scholes and Merton. The "
            "density from the smile becomes the volatility surface of Part twelve, and model-free bounds frame the "
            "exotic options of Parts fourteen and fifteen. Forward and annuity measures price the rates products of "
            "Parts eighteen and nineteen. The discount factor is the heart of Part twenty-three. The frictions that "
            "break parity, borrowing and funding, return in Parts twenty-one and forty-one, and ETF arbitrage in "
            "Part thirty-eight."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Shreve, \textit{Stochastic Calculus for Finance} I (ch.\ 1, 3, 4) and II (ch.\ 5, 9); Bj\"ork, "
             r"\textit{Arbitrage Theory in Continuous Time}, 4th ed., ch.\ 2--3, 9--12, 15",
             r"Duffie, \textit{Dynamic Asset Pricing Theory}, ch.\ 1--2, 6; Delbaen and Schachermayer, \textit{The "
             r"Mathematics of Arbitrage}; F\"ollmer and Schied, \textit{Stochastic Finance}, ch.\ 1, 5, 7",
             r"Henry-Labord\`ere, \textit{Model-Free Hedging}"],
            [r"Farkas (1902); Stiemke (1915); Arrow (1964); Stoll (1969); Ross (1976, 1978); Breeden and Litzenberger "
             r"(1978); Margrabe (1978); Cox, Ross and Rubinstein (1979); Harrison and Kreps (1979)",
             r"Harrison and Pliska (1981); Kreps (1981); Jamshidian (1989); Dalang, Morton and Willinger (1990); "
             r"Delbaen and Schachermayer (1994, 1998); Geman, El Karoui and Rochet (1995); Avellaneda, Levy and Par\'as "
             r"(1995); Lyons (1995); Kramkov (1996); Shleifer and Vishny (1997); Hobson (1998)",
             r"Jackwerth (2000); Mitchell, Pulvino and Stafford (2002); Lamont and Thaler (2003); Ofek, Richardson and "
             r"Whitelaw (2004); Cox and Hobson (2005); Beiglb\"ock, Henry-Labord\`ere and Penkner (2013); Galichon, "
             r"Henry-Labord\`ere and Touzi (2014); Ross (2015); Borovi\v{c}ka, Hansen and Scheinkman (2016)",
             r"Martin and Ross (2019); Jensen, Lando and Pedersen (2019); Jackwerth and Menner (2020); Haddad, "
             r"Moreira and Muir (2021); van Binsbergen, Diamond and Grotteria (2022); Neufeld and Sester (2023); "
             r"Neufeld, Papapantoleon and Xiang (2023); Heston, Jacobs and Kim (2023); Guyon (2024); Horvath (2025); "
             r"Bartl, Beiglb\"ock and Pammer (2026); Shikhman et al.\ (2026)"])
        if card.height > 7.6:
            card.scale_to_fit_height(7.6)
        with self.voiceover(
            "The textbook chapters this part covers, and the papers it draws on, classic and new. The data are the "
            "Surface's trades, a day of Bitcoin options and futures on Deribit, and every bound, density and "
            "recovery was computed by the House's arbitrage checker."
        ):
            self.play(FadeIn(card))
            self.wait(4)
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
