from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant29.common import BAD, COMB, FORMULA, GOOD, GP_C, HURDLE, PART, RAND_C, RL_C, comma, load

DESK = [
    (r"You mined 10{,}000 alphas with average out-of-sample IC 0.01 and average correlation 0.3. The combined IC?",
     r"equal weights give $c\sqrt{N/(1 + (N - 1)\rho)} \to c/\sqrt\rho \approx 0.018$: correlation, not the count, "
     r"sets the ceiling. Ten thousand alphas are worth about three independent ones"),
    (r"A GP run reports a training IC of 0.08 after 25 generations. What do you ask for?",
     r"the number of distinct trees it evaluated, which sets the hurdle; then the IC on a year the run never touched"),
    (r"An LLM agent finds a factor with a Sharpe ratio of 3 on 2015--2022 A-shares. Your first check?",
     r"the language model's training cut-off: it may have read papers and forums about what worked in those years. "
     r"Then count its loops as trials, and re-run on a period after the cut-off"),
    (r"Your top 40 alphas have a training Sharpe ratio of 6 with estimated weights. What do you expect live?",
     r"much less: weights fitted on the same days fit noise in every direction. The research chapter's formula, with "
     r"$K = 40$ and $T$ the training days, gives the scale; equal weights are the honest benchmark"),
    (r"A `market-neutral' small-cap fund is short large-cap index futures. What is it exposed to?",
     r"the spread between small and large caps, which widens exactly when crowded small-cap books are sold at once: "
     r"February 2024"),
    (r"Your library's fiftieth alpha has a Sharpe ratio of 0.3 a year. Add it?",
     r"only if its squared Sharpe ratio clears $S/(TS + 2K)$ and it is not a cousin of what you hold: measure its "
     r"contribution to the combination out of sample, after estimating its weight"),
]

PROBLEMS = [
    r"With 6 fields, 5 unary operators, 7 time-series operators and \texttt{corr} over 4 windows, and 4 binary "
    r"operators, verify that there are 492 trees of depth at most 2.",
    r"Daily IC has a standard deviation of 0.10 over 500 training days. Roughly what is the best mean IC among 10{,}000 "
    r"pure-noise formulas?",
    r"A signal has an IC of 0.02 every day across 100 coins. Using $IR \approx IC\sqrt N$, its daily and annual Sharpe "
    r"ratio?",
    r"$N$ standardised signals each have IC $c$ and pairwise correlation $\rho$. Show the equal-weight IC is "
    r"$c\sqrt{N/(1 + (N - 1)\rho)}$, and evaluate it for $N = 10{,}000$, $c = 0.01$, $\rho = 0.3$.",
    r"GP's parsimony penalty is 0.0005 IC per node. How much IC must ten extra nodes add to survive selection?",
    r"An agent tests 500 hypotheses, each over 4 windows. How many trials, and how far does $\sqrt{2\ln N}$ move "
    r"compared with 500?",
    r"Show that subtracting a constant baseline $b$ from the reward leaves the REINFORCE gradient unbiased: "
    r"$\mathbb E[\nabla\log\pi(a)\,b] = 0$.",
    r"Long small caps, short CSI 300 futures, equal notional. Small caps fall 20\%, the CSI 300 5\%. The loss per unit "
    r"of gross long?",
    r"An alpha's IC halves every two years as others find it. From 0.03, when does it fall below 0.01?",
    r"Twenty independent alphas, each with daily Sharpe ratio 0.02, and 365 days of data: $SR_*$, and the formula's "
    r"out-of-sample Sharpe ratio, daily and annual.",
    r"(qual) $r_t \sim N(\mu, \Sigma)$ in $\mathbb R^K$, $\Sigma$ known, $\hat w = \Sigma^{-1}\hat\mu$ from $T$ "
    r"observations. Show $SR(\hat w) = z^\top\theta/\|z\|$ with $z = \theta + \varepsilon/\sqrt T$, deduce the limit "
    r"$SR_*/\sqrt{1 + \gamma/SR_*^2}$ for $K/T \to \gamma$, and the bar $s^2 > S/(TS + 2K)$ for one more alpha.",
    r"(qual) Standardised signals $s$ with correlation matrix $C$ and ICs $c = \operatorname{Corr}(s, r)$. Show the "
    r"best linear combination's IC is $\sqrt{c^\top C^{-1}c}$, and that for equicorrelated signals with equal ICs it "
    r"equals the equal-weight IC of Problem 4.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("classic"), load("space"), load("random"), load("gp"), load("rl"), load("combine"),
                   load("decay"), load("envelope"), load("theory"))
        self.desk()
        self.problems()
        self.payoffs()
        self.references()
        self.house()

    def _rows(self, items, title):
        rows = VGroup()
        for j, (t, col) in items:
            rows.add(VGroup(MathTex(str(j), font_size=24, color=col), label(t, font_size=21)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(title, font_size=36).to_edge(UP, buff=0.3)
        rows.next_to(head, DOWN, buff=0.35)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        if rows.height > 6.4:
            rows.scale_to_fit_height(6.4)
        return head, rows

    def recap(self, cl, sp, r, g, rl, c, dc, env, th):
        best = r["best_by_n"][-1]
        gp_last = [run[-1] for run in g["runs"]]
        gp_tr = sum(x["train"] for x in gp_last) / len(gp_last)
        gp_va = sum(x["valid"] for x in gp_last) / len(gp_last)
        h = env["row"]["holdout"]
        n_eff = c["n_eff"]
        items = [
            (r"formulaic alphas: Kakushadze's 101, short-horizon, 15.9\% average correlation; two of three, on coins, "
             r"changed sign in 2020", FORMULA),
            (r"the space: six fields and a few operators give $10^{13}$ formulas of depth four; no search is exhaustive",
             FORMULA),
            (rf"random search: 10{{,}}000 formulas, 2018--19 against 2020 IC correlation {r['corr']:.2f}; the best "
             rf"{best['train']:.3f}, then {best['valid']:+.3f}: a few real patterns, restated", RAND_C),
            (rf"genetic programming: selection, crossover, mutation, bloat; train {gp_tr:.3f}, 2020 {gp_va:+.3f}", GP_C),
            (rf"RL: a generator rewarded for what each formula adds to the pool; {rl['train']['ic']:.3f} to "
             rf"{rl['valid']['ic']:+.3f}", RL_C),
            (r"LLM agents: hypotheses in words, code, backtest, critique; the authors' numbers, not yet sealed", GREY_A),
            (rf"combining: the top 40 alphas average correlation {c['rho']:.2f}; equal weights against estimated", COMB),
        ]
        items2 = [
            (r"the counter: every formula, generation and agent loop is a trial; the hurdle grows like "
             r"$\sqrt{2\ln N}$", HURDLE),
            (r"decay: short horizons, crowding, and the alpha factory that must keep producing", BAD),
            (r"China: index enhancement, a crowded small-cap tilt, and February 2024", BAD),
            (r"High-Flyer: an alpha factory that became a language-model lab", GREY_A),
            (r"humans: the prior, the data and the judgement; a prior is a smaller $N$", GOOD),
            (rf"the mined combination on 2021--25: {h['sharpe']:.2f} $\pm$ {h['sharpe_se']:.2f} gross, "
             rf"{h['sharpe_net']:.2f} net; the counter {comma(env['trials'])}", QC.HOUSE),
            (r"research: an estimated combination earns $SR_*/\sqrt{1 + K/(T SR_*^2)}$; past a point, more alphas hurt",
             COMB),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 29 in fourteen lines")
        with self.voiceover(
            "Part twenty-nine in fourteen lines. A formulaic alpha is a short formula over prices and volumes; the "
            "published hundred and one are fast and only loosely correlated, and two of three, on coins, changed sign "
            "in the year after we measured them. A handful of fields and operators make a space far beyond exhaustive "
            "search. Ten thousand random formulas on coins were not mostly noise: they restated a few real patterns, "
            "above all that calm coins beat wild ones. Genetic programming breeds formulas and bloats them; a learned "
            "generator writes them token by token, rewarded for what they add, and both found the same patterns. "
            "Language-model agents now run the whole loop, on their authors' numbers. And the best alphas turn out to "
            f"be cousins: forty of them, about {n_eff:.0f} bets."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=20))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 8)), r"Part 29 in fourteen lines")
        with self.voiceover(
            "Every formula, generation and agent loop is a trial, and the hurdle grows with the logarithm of their "
            "number. Fast signals decay, and crowding makes many firms' libraries one bet: China's quant industry "
            "learned that in February 2024. One alpha factory became a language-model lab. What remains for people is "
            "the prior, the data and the judgement, and a prior is worth exactly the search it saves. The mined "
            "combination, opened on the sealed years, held up before costs and thinned after them. And the research "
            "chapter showed why estimated weights on many weak alphas can do worse than fewer."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q, a_, width=12.4, font_size=20) for q, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. Ten thousand alphas with an out-of-sample IC of one percent and a correlation of "
            "point three combine to an IC under two percent: correlation sets the ceiling, and ten thousand alphas are "
            "worth about three independent ones. <bookmark mark='a'/> A genetic program's training IC means nothing "
            "without the number of trees it evaluated, and a year it never saw. <bookmark mark='b'/> And an agent's "
            "factor must be tested after its language model's training cut-off."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "Forty alphas with weights fitted on the same days will disappoint; equal weights are the benchmark. "
            "<bookmark mark='a'/> A market-neutral small-cap book hedged with large-cap futures is a bet on the spread "
            "between them. <bookmark mark='b'/> And the fiftieth alpha joins the library only if it clears the research "
            "chapter's bar and is not a cousin of what is already there. Full solutions are in the notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: counting the grammar's small trees; the best of ten thousand noise ICs; from IC to "
            "Sharpe ratio; the IC of an equal-weight combination; the price of bloat; counting an agent's trials; the "
            "baseline in REINFORCE; the February 2024 hedge; an alpha's half-life; and the research chapter's formula by "
            "hand. Then two qualifying-exam problems: the out-of-sample Sharpe ratio of an estimated combination, and "
            "the best combination's IC. Solutions, in English and Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"estimation error in the optimizer; shrinkage and $1/N$", [30]),
            (r"the fundamental law, derived; combining alphas under costs, capacity and crowding", [31]),
            (r"the quant quake of 2007: crowded statistical arbitrage", [33]),
            (r"the finale: the mined combination's row, deflated by the full count", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part thirty takes the research chapter's estimation error into the portfolio "
            "optimizer, with shrinkage and the humble one over N. Part thirty-one derives the fundamental law and "
            "combines alphas under trading costs, capacity and crowding. Part thirty-three replays the quant quake of 2007, "
            "when crowded statistical arbitrage books unwound together. And the finale "
            "deflates the mined combination's row with everything else."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Kakushadze and Serur, \textit{151 Trading Strategies} (2018); Isichenko, \textit{Quantitative Portfolio "
             r"Management} (2021), chapters 2--3; Koza, \textit{Genetic Programming} (1992); Sutton and Barto, "
             r"\textit{Reinforcement Learning} (2018)"],
            [r"Brown (1976); Williams (1992); Allen and Karjalainen (1999); Kan and Zhou (2007); Kakushadze (2016); "
             r"Harvey and Liu (2015); Yu, Xue, Ao, Pan, He, Tu and He (2023); Wang et al.\ (2023), Alpha-GPT; "
             r"Tang et al.\ (2025), AlphaAgent; Li et al.\ (2025), R\&D-Agent-Quant",
             r"China, February 2024: as reported by Reuters, Bloomberg and Caixin; High-Flyer and DeepSeek: company "
             r"statements and press reports. Data: Binance public daily candles"])
        with self.voiceover(
            "The textbooks this part follows, and the papers it draws on, from Brown's estimation risk in 1976 to the "
            "research agents of 2025. Every number on screen was computed by the House's code from public exchange "
            "data, with simulations labelled as such, and every firm is described from the public record."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research",))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 30, Portfolio Construction", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House now has an alpha factory: a grammar of formulas, three ways to search it, a way to combine what "
            "it finds, and a counter that records every try. <bookmark mark='a'/> Next, Part thirty: portfolio "
            "construction. Why the optimizer loves the asset with the most estimation error, and what to do about it."
        ) as vo:
            self.play(FadeIn(chart))
            vo.wait_until("a")
            self.play(FadeOut(chart), FadeIn(smap), FadeIn(nxt))
        self.wait(1.0)
        self.clear_scene()
