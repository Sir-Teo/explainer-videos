from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import BAD, COLL_C, HURDLE, LEARN_C, PART, SHARE_C, SIM_C, era_strip, load


class Hook(VoiceoverScene):
    def construct(self):
        self.title_card()
        self.claims(load("collusion"), load("maker"), load("crowd"), load("kirman"))
        self.desk_q()
        self.stakes()
        self.not_this()
        self.act()
        self.history()
        self.objectives()
        self.house()
        self.question()

    def title_card(self):
        card = part_title(PART, r"Machines in the Market")
        disc = note(DISCLAIMER, font_size=18, color=GREY_C).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part forty-two. Machines in the market: what happens when the traders are programs that learn, and the "
            "market is made of them. Artificial markets, herding, simulators, learning market makers, algorithms that "
            "collude without speaking, and crowds that share one model."
        ):
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(disc))
        self.play(FadeOut(card), FadeOut(disc))

    def claims(self, c, m, cr, k):
        d95 = [x for x in c["by_delta"] if x["delta_disc"] == 0.95][0]
        w2 = [x for x in cr["rows"] if x["share"] == 0.2][0]
        rp = m["replay"]
        cards = VGroup(
            desk_question('supra-competitive learning outcomes', rf"two Q-learning pricing algorithms that never communicate settle "
                          rf"{100 * d95['delta']:.0f}\% of the way from competitive to monopoly profits, and punish "
                          r"a rival who undercuts", width=12.4, font_size=19),
            desk_question(r"a backtest is not an environment", rf"replayed on another quote rule's tape, a wider quote "
                          rf"looks worth {rp['naive4']:.0f}; trading live in the same market it earns {rp['live4']:.0f}",
                          width=12.4, font_size=19),
            desk_question(r"a shared model dominates", rf"for 100 traders with independent unit-variance signal components and common coefficient 0.2, "
                          rf"{100 * w2['common']:.0f}\% of aggregate flow variance is common", width=12.4,
                          font_size=19),
            desk_question(r"herding has a law", rf"Kirman's crowd is exactly beta-binomial; when copying dominates it "
                          rf"is unanimous {100 * k['bi']['p_edges']:.0f}\% of the time", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            f"""Four findings, with their scope. <bookmark mark='a'/> Pricing learners reach a profit index of {100*d95['delta']:.0f} percent between continuous Nash and monopoly benchmarks; a selected fixed-point subset retaliates after forced undercuts. <bookmark mark='b'/> Reusing another rule's fills gives a wider quote score of {rp['naive4']:.0f}, against {rp['live4']:.0f} in interactive simulated trading. <bookmark mark='c'/> With independent unit-variance signal components, common weight point two explains {100*w2['common']:.0f} percent of a hundred traders' aggregate flow variance. <bookmark mark='d'/> Kirman's specified imitation chain has an exact stationary law. These are model results, not universal market estimates."""
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for kk, mk_ in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(mk_)
                if kk:
                    self.play(FadeIn(cards[kk], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def desk_q(self):
        rows = VGroup(label(r"two algorithms that never communicate", font_size=26),
                      label(r"end up quoting wide spreads", font_size=26, color=GREY_A),
                      label(r"is that collusion?", font_size=26, color=HURDLE))
        rows.arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        with self.voiceover(
            "The desk question for this part, answered in Chapter six. <bookmark mark='a'/> Two algorithms that never "
            "communicate <bookmark mark='b'/> end up quoting wide spreads. <bookmark mark='c'/> Is that collusion? Hold "
            "your answer; the economist's and the lawyer's differ."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def stakes(self):
        cards = VGroup(
            desk_question('automation and learning differ', 'automated trading matters in many markets; adaptive-learning shares depend on venue, date and definition', width=12.4,
                          font_size=19),
            desk_question(r"their interactions are new", r"a single algorithm can be tested; a market of them can "
                          r"behave in ways none was designed to: collusion, herding, flash crashes", width=12.4,
                          font_size=19),
            desk_question(r"why the House cares", r"its agents trade against others like them, and may one day be "
                          r"copied: it must test them in the market they create", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why it matters. <bookmark mark='a'/> Automated trading is important in many markets, but automation and adaptive learning are different categories; their shares depend on venue, period and definition. <bookmark mark='b'/> Interacting algorithms can produce collective behaviour that an isolated test misses. <bookmark mark='c'/> The House's proposed research standard therefore includes alternative opponents and copies of a successful policy. Such scenarios test mechanisms without claiming they predict deployment outcomes."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for kk, mk_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(mk_)
                if kk:
                    self.play(FadeIn(cards[kk], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def not_this(self):
        cards = VGroup(
            desk_question(r"not a product", r"no agent here is a trading recommendation, and none was run with real "
                          r"money", width=12.4, font_size=19),
            desk_question(r"not a language model", r"the House runs no language model as a trader in this part; "
                          r"Chapter 5 says why and what a fair test would need", width=12.4, font_size=19),
            desk_question(r"simulations, labelled", r"every learned result is from the House's own simulators, with "
                          r"fixed seeds; the papers it reproduces are cited as reported", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And what this part is not. <bookmark mark='a'/> No agent here is a recommendation, and none traded real "
            "money. <bookmark mark='b'/> The House runs no language model as a trader; Chapter five says why, and what "
            "a fair test would need. <bookmark mark='c'/> Every learned result comes from the House's own simulators, "
            "with fixed seeds."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for kk, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if kk:
                    self.play(FadeIn(cards[kk], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def act(self):
        smap = series_map(current=PART, done=PART - 1)
        with self.voiceover(
            "Where this sits. Act seven, the system. Part forty measured risk and Part forty-one followed it into "
            "crises. This part puts machines into the market and watches what they do to it, and to each other. Part "
            "forty-three, the last, asks whether anyone beats the market at all."
        ):
            self.play(FadeIn(smap))
            self.wait(1.0)
        self.clear_scene()

    def history(self):
        I = QC.IDEA
        R = BAD
        entries = [(1993, r"Kirman's ants", I), (1994, r"zero intelligence", I), (1997, r"the Santa Fe market", I),
                   (1999, r"Lux--Marchesi", I), (2006, r"RL execution", I), (2010, r"the flash crash", R),
                   (2012, r"Knight Capital", R), (2013, r"Moore vs Murphy", I), (2020, r"Calvano; ABIDES", I),
                   (2022, r"AI and systemic risk", I), (2024, r"IMF, FSB reports", I)]
        strip = era_strip(entries, y0=1990, y1=2026, font_size=12, step=10).move_to(DOWN * 0.3)
        head = label(r"Thirty years of machines in markets", font_size=34).to_edge(UP, buff=0.6)
        groups = [(0, 4), (4, 8), (8, 11)]
        with self.voiceover(
            "Thirty years. Alan Kirman's ants; zero-intelligence traders; the Santa Fe artificial market; Lux and "
            "Marchesi. <bookmark mark='a'/> Reinforcement learning for execution; the flash crash; Knight Capital; "
            "Moore's law against Murphy's. <bookmark mark='b'/> Then Calvano's colluding learners and the ABIDES "
            "simulator, the first papers on AI and systemic risk, and the supervisors' reports of twenty twenty-four."
        ) as vo:
            self.play(FadeIn(head), Create(strip[0]), FadeIn(strip[1]))
            for (a, b), mk_ in zip(groups, [None, "a", "b"]):
                if mk_:
                    vo.wait_until(mk_)
                self.play(LaggedStart(*[FadeIn(strip.items[i], shift=UP * 0.1) for i in range(a, b)], lag_ratio=0.3),
                          run_time=1.6)
        self.wait(0.4)
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Artificial markets: the Santa Fe market and structural stochastic volatility",
            r"Herding: Kirman's ant model and its exact law",
            r"Simulators, realism, and the gap to real markets",
            r"A learning market maker, and why a backtest is not an environment",
            r"Language models as traders, and what a fair test needs",
            r"Algorithmic collusion, reproduced; monoculture; AI and stability",
            r"For the researcher: when collusion can last, proved and checked",
        ], color=QC.IDEA)
        with self.voiceover(
            "The plan: artificial markets and herding; simulators; a learning market maker; language models as traders; "
            "algorithmic collusion, reproduced; crowds that share a model; what supervisors worry about; and the theorem "
            "that says when collusion can last."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows],
                                                     lag_ratio=0.5, run_time=12))
        self.play(FadeOut(card))

    def house(self):
        chart = house_chart(PART, lit=("research", "mm", "compliance"))
        with self.voiceover(
            "In the House, the research desk and the market makers bring their learning agents to compliance, which "
            "asks a question none of them was trained to answer: what happens to the market when they succeed?"
        ):
            self.play(FadeIn(chart))
        self.wait(0.3)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a market of traders following simple rules: some expect prices to revert, some chase trends. "
                       r"Can it produce the real market's fat tails and clustered volatility? What would it need?")
        with self.voiceover(
            "Pause and predict. A market of traders following simple rules: some expect prices to revert to value, some "
            "chase trends. Can it produce the real market's fat tails and clustered volatility? And if so, what "
            "ingredient would it need?"
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
