from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C, load)

DESK = [
    (r"Two algorithms that never communicate end up quoting wide spreads. Is that collusion?",
     'wide spreads alone do not prove collusion; examine individual deviation incentives, coordination evidence and applicable law'),
    (r"Why is a backtest not an environment for a market maker?",
     r"its quotes change who trades with it; replaying another rule's fills at new prices overstates a wider quote "
     r"more than threefold here"),
    (r"Your agent was trained in a simulator. What would you check before trusting it?",
     r"that the simulator reproduces responses to orders, not just stylised facts; and how the agent does in regimes "
     r"and against rivals it never saw"),
    (r"How does herding produce volatility clustering?",
     r"the share of trend-followers moves slowly, because each agent's switch depends on the others', and volatility "
     r"rises with that share"),
    (r"A fifth of every trader's order comes from one shared model. Why does that matter?",
     'independent unit-variance signals and common coefficient 0.2 give about 86\\% of aggregate flow variance at $N=100$'),
    (r"When can grim trigger sustain the monopoly price?",
     r"when $\delta \ge (\pi^d - \pi^c)/(\pi^d - \pi^n)$; 0.39 in this part's logit game"),
]

PROBLEMS = [
    '$r_t=\\sigma_t\\varepsilon_t$: centred IID innovations independent of a stationary Gaussian log-volatility AR(1) with $0<\\rho<1$. Derive return and absolute-return covariances.',
    r"Kirman's chain with $N = 50$, $\varepsilon = 0.01$, $\delta = 0.02$: $\alpha$, and whether the crowd herds.",
    r"Show that the beta-binomial$(N, \alpha, \alpha)$ law satisfies detailed balance for the ant chain.",
    r"A noise trader trades with probability $\lambda e^{-k d}$ at distance $d$: the half-spread that maximises "
    r"expected spread income, with no informed traders.",
    r"A replayed tape has $n$ fills at half-spread 2. Why is $R + 2n$ a biased estimate for half-spread 4, and in which "
    r"direction?",
    r"Logit demand with $a = 2$, $\mu = 0.25$, $c = 1$: verify that $p^N \approx 1.473$ solves the first-order condition.",
    r"Two firms, $\pi^c = 3$, $\pi^d = 4$, $\pi^n = 2$: the grim-trigger threshold, and the threshold for a one-period "
    r"punishment.",
    r"$N$ traders with weight $w$ on a shared signal: the weight at which half the flow variance is common, for "
    r"$N = 100$.",
    'For independent unit-variance signal components and linear impact $\\kappa/\\sqrt N$, add $e$ to the common signal. Derive the added return in $w=0$ volatility units.',
    r"Why can a collusion index above zero arise with $\delta = 0$ on a discrete price grid?",
    r"(qual) State and prove the one-shot deviation principle for discounted repeated games with bounded payoffs; use it "
    r"to prove the grim-trigger threshold and the $T$-period corollary.",
    '(qual) Derive the stationary law; holding $\\alpha>0$ fixed by scaling $\\varepsilon$, prove the Beta limit and the $N^{-\\alpha}$ unanimity asymptotic.',
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap(load("facts"), load("kirman"), load("maker"), load("collusion"), load("crowd"), load("research"))
        self.lessons()
        self.formulas()
        self.connections()
        self.desk()
        self.answers(load("research"))
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

    def recap(self, f, k, m, c, cr, r):
        d95 = [x for x in c["by_delta"] if x["delta_disc"] == 0.95][0]
        w2 = [x for x in cr["rows"] if x["share"] == 0.2][0]
        cx = m["cross"]
        rp = m["replay"]
        best30 = max(x["mean"] for x in m["fixed"]["0.3"])
        items = [
            (r"the Santa Fe market: adaptive agents produce bubbles, crashes and clustering on their own", SIM_C),
            (rf"herding between rules gives fat tails and slow volatility memory (lag-20 $|r|$ autocorrelation "
             rf"{f['sim']['acf_abs'][4]:.2f}; the market's {f['real']['acf_abs'][4]:.2f})", SIM_C),
            (rf"Kirman's crowd is exactly beta-binomial; with copying, unanimous {100 * k['bi']['p_edges']:.0f}\% of the "
             r"time", SHARE_C),
            (r"simulators match facts more easily than responses; the counterfactual is assumed, not measured", HURDLE),
            (rf"a learned maker earns {cx['0.3']['0.3']['mean']:.0f} in one hard-market run; the best tested "
             rf"fixed rule, {best30:.0f}", LEARN_C),
            (rf"replay is not live: {rp['naive4']:.0f} predicted, {rp['live4']:.0f} earned", BAD),
        ]
        items2 = [
            (r"language models need a clean cut-off, a registry, costs and a baseline; none was run here", HURDLE),
            (rf"finite pricing runs: profit index {d95['delta']:.2f}, with conditional retaliation", COLL_C),
            ('these finite runs show sensitivity to payoff noise and discounting', COLL_C),
            (rf"common coefficient 0.2: {100 * w2['common']:.0f}\% of aggregate flow variance under the stated assumptions", SHARE_C),
            ('2024 reports discuss correlation, concentration, cyber and model risks', BAD),
            (rf"research: grim trigger needs $\delta \ge {r['mono']['grim']:.2f}$ in the continuous game; finite-grid learners differ", GOOD),
            (r"Rule 42: test the agent against the market it creates", QC.HOUSE),
        ]
        head, rows = self._rows(list(enumerate(items, 1)), r"Part 42 in thirteen lines")
        with self.voiceover(
            "Part forty-two in thirteen lines. Selected adaptive-agent models generate tails and clustered volatility; they do not identify a unique market mechanism. Kirman's chain has an exact beta-binomial stationary law. Matching historical moments does not validate intervention responses. In one partially observed dealer experiment, finite-trained learners trail the best tested fixed rule. And reusing fixed fills does not reproduce a new policy's interactive execution."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=18))
        self.wait(0.5)
        self.clear_scene()
        head, rows = self._rows(list(enumerate(items2, 7)), r"Part 42 in thirteen lines")
        with self.voiceover(
            'No language-model trader was run here. Finite pricing experiments show supra-competitive profits and conditional retaliation, without certifying equilibrium or legal agreement. Common signals can dominate aggregate flow variance under explicit assumptions. Dated supervisory reports highlight concentration and correlation risks. The research chapter proves a specified grim-trigger condition and distinguishes it from mixed-domain illustrative calculations. Rule forty-two proposes testing agents against alternative markets and populations.'
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows], lag_ratio=0.6,
                                                run_time=16))
        self.wait(0.5)
        self.clear_scene()

    def lessons(self):
        cards = VGroup(
            desk_question(r"the market is the agents", r"its statistics, its liquidity and its crashes are what its "
                          r"traders do together; change them and the market changes", width=12.4, font_size=19),
            desk_question(r"learning finds what pays", r"including collusion, simulator artefacts and other traders' "
                          r"mistakes; what it learns depends on the world it learned in", width=12.4, font_size=19),
            desk_question('diversity can reduce shared exposure', 'common exposure can amplify shocks; diversity benefits depend on incentives, constraints and liquidity', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three lessons. <bookmark mark='a'/> Market behaviour depends on agents, institutions and their interaction; matching a pattern is not unique causal identification. <bookmark mark='b'/> Learning can exploit reward definitions and simulator artefacts, so performance needs independent checks. <bookmark mark='c'/> Shared exposures can amplify shocks, while diversity may reduce alignment under suitable conditions. Neither learning nor diversity guarantees stability."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for kk, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if kk:
                    self.play(FadeIn(cards[kk], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def formulas(self):
        rows = VGroup(
            MathTex(r"p_{t+1} - p_t = \mu\bigl[n_f(\phi(p^* - p_t) + \sigma_f\varepsilon_f) + n_c(\chi\Delta p_t + "
                    r"\sigma_c\varepsilon_c)\bigr]", font_size=30, color=SIM_C),
            MathTex(r"\pi(k) \propto \binom Nk B(k + \alpha, N - k + \alpha),\quad \alpha = \frac{\varepsilon(N - 1)}{1 - \delta}",
                    font_size=30, color=SHARE_C),
            MathTex(r"Q(s, a) \leftarrow (1 - \alpha)Q(s, a) + \alpha\bigl[\pi + \delta\max_{a'}Q(s', a')\bigr]", font_size=30,
                    color=LEARN_C),
            MathTex(r"\delta^* = \frac{\pi^d - \pi^c}{\pi^d - \pi^n},\qquad \pi^d - \pi^c \le (\pi^c - \pi^n)\sum_{j=1}^T \delta^j",
                    font_size=30, color=COLL_C),
            MathTex(r"\text{common share} = \frac{Nw^2}{Nw^2 + (1 - w)^2}", font_size=32, color=BAD),
        ).arrange(DOWN, buff=0.38)
        head = label(r"The part on one card", font_size=34).to_edge(UP, buff=0.4)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "The part on one card. The fundamentalist and chartist market. Kirman's exact law. The Q-learning update. "
            "The collusion thresholds, grim and finite. And the common share of a crowd's flow."
        ):
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.4, run_time=5))
            self.wait(2)
        self.clear_scene()

    def connections(self):
        cards = VGroup(
            desk_question(r"backwards", r"Part 7's volatility models, Part 8's Q-learning, Part 26's trial counter, Part "
                          r"28's look-ahead, Parts 35 to 38's market makers and Part 41's herding all return here",
                          width=12.4, font_size=19),
            desk_question(r"sideways", r"collusion is Part 38's spread competition with memory; monoculture is Part 41's "
                          r"common holdings, made of models", width=12.4, font_size=19),
            desk_question(r"forwards", r"Part 43 asks whether, in a market of such agents, anyone earns more than the "
                          r"market itself", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How this part connects. <bookmark mark='a'/> Backwards: volatility models, Q-learning, the trial counter, "
            "look-ahead, the market makers of Parts thirty-five to thirty-eight, and Part forty-one's herding. "
            "<bookmark mark='b'/> Sideways: collusion is spread competition with memory, and monoculture is common "
            "holdings made of models. <bookmark mark='c'/> Forwards: Part forty-three asks whether, in a market of such "
            "agents, anyone beats the market."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for kk, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if kk:
                    self.play(FadeIn(cards[kk], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk(self):
        def page(qs):
            cards = VGroup(*[desk_question(q_, a_, width=12.4, font_size=20) for q_, a_ in qs]).arrange(DOWN, buff=0.22)
            if cards.height > 7.4:
                cards.scale_to_fit_height(7.4)
            return cards
        cards = page(DESK[:3])
        with self.voiceover(
            "Six desk questions. The hook asks whether wide spreads prove collusion. They do not. Retaliation is a diagnostic; equilibrium and legal conclusions require more evidence. <bookmark mark='a'/> Why is a tape not an interactive environment? New quotes change who fills them. <bookmark mark='b'/> What should simulator evaluation check? Responses to interventions, unfamiliar regimes, alternative opponents and assumptions behind the mapping to real trading."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2), FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
        cards = page(DESK[3:])
        with self.voiceover(
            "How does herding cluster volatility? Through a slowly moving share of trend-followers. <bookmark mark='a'/> "
            "Why does a shared model matter? Its parts add coherently. <bookmark mark='b'/> And when can grim trigger "
            "hold the monopoly price? Above the threshold proved in the research chapter. Full solutions are in the "
            "notes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2), FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    def answers(self, r):
        ne = r["grid_ne"]
        my = r["myopic"]
        hi_ne = max(x["delta"] for x in ne)
        cards = VGroup(
            desk_question(r"Research: one reason is the grid", rf"the one-shot game on fifteen prices has its own "
                          rf"equilibria, at indices of {ne[0]['delta']:.2f} and {hi_ne:.2f}, so a myopic learner can "
                          r"settle above the continuous Nash price", width=12.4, font_size=20),
            desk_question(r"the other is learning itself", rf"{100 * my['above_grid_ne']:.0f}\% of myopic sessions end "
                          r"above even the higher grid equilibrium: finite learning need not reach equilibrium "
                          r"(Banchio and Mantegazza)", width=12.4, font_size=20),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            f"""The research pause, answered. <bookmark mark='a'/> Discretisation changes the one-period game. Its listed equilibrium indices are {ne[0]['delta']:.2f} and {hi_ne:.2f}, relative to continuous-action benchmarks. <bookmark mark='b'/> Finite learning need not reach either equilibrium: {100*my['above_grid_ne']:.0f} percent of myopic sessions have reported indices above the higher listed grid equilibrium. Coupled learning estimates are one literature mechanism, but this statistic alone does not identify the cause or prove a repeated-game equilibrium."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=18)
        with self.voiceover(
            "And twelve problems: why size is predictable when returns are not; Kirman's alpha; its detailed balance; "
            "the best spread against elastic noise traders; the replay bias; the logit Nash price; collusion thresholds; "
            "the common share; a shared model's error; and collusion on a grid. Then two qualifying-exam problems: the "
            "one-shot deviation principle with its consequences, and Kirman's law in full. Solutions, in English and "
            "Chinese, are in the notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_) for r_ in ps.rows], lag_ratio=0.3, run_time=5))
            self.wait(3)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"whether, in a market of adaptive agents, anyone beats the market", [43]),
            (r"luck, skill and adaptive markets: Lo's hypothesis, after this part's agents", [43]),
        ])
        with self.voiceover(
            "Where this comes back. Part forty-three, the last, asks whether anyone beats a market made of agents like "
            "these, and why Andrew Lo called markets adaptive."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_) for r_ in card.rows], lag_ratio=0.4, run_time=4))
        self.wait(0.4)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"LeBaron, ``Agent-based computational finance'' (2006); Sutton and Barto, \textit{Reinforcement Learning} "
             r"(2018); Fudenberg and Tirole, \textit{Game Theory}, ch.~5 (1991); Hambly, Xu and Yang, ``Recent advances "
             r"in reinforcement learning in finance'' (2023)"],
            [r"Friedman (1971); Green and Porter (1984); Fudenberg and Maskin (1986); Kirman (1993); Gode and Sunder "
             r"(1993); Arthur et al.\ (1997); Lux and Marchesi (1999); Alfarano, Lux and Wagner (2005); Farmer, Patelli "
             r"and Zovko (2005); Franke and Westerhoff (2012); Kirilenko and Lo (2013)",
             r"Byrd, Hybinette and Balch (2020); Vyetrenko et al.\ (2020); Calvano et al.\ (2020); Gensler and Bailey "
             r"(2020); Danielsson, Macrae and Uthemann (2022); Brown and MacKay (2023); Banchio and Mantegazza (2023); "
             r"Assad et al.\ (2024); IMF and FSB (2024). Data: Kenneth French's library, to 2020"])
        with self.voiceover(
            "The references separate reported historical episodes, published theoretical and simulation results, and this part's fixed-seed calculations. The only downloaded market series used here is Kenneth French's daily research-window data through twenty twenty. Source citations and the limits of the experiments are in the bilingual notes."
        ):
            self.play(FadeIn(card))
            self.wait(3)
        self.clear_scene()

    def house(self):
        chart = house_chart(PART, lit=("research", "mm", "compliance"))
        smap = series_map(current=PART + 1, done=PART)
        nxt = label(r"Next: Part 43, Can You Beat the Market?", font_size=30, color=QC.IDEA).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The House's proposed rule is to test agents against markets and opponents their deployment could create. <bookmark mark='a'/> Next, Part forty-three asks whether anyone can beat the market: Sharpe's arithmetic, luck versus skill and the evidence required for a performance claim. This continuation makes no promise to open sealed strategy outcomes."
        ) as vo:
            self.play(FadeIn(chart), FadeOut(chart), FadeIn(smap), FadeIn(nxt))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
        self.wait(1.0)
        self.clear_scene()
