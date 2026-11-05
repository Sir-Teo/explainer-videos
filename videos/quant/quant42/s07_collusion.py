from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C,
                                         fit_right, load)


class Collusion(VoiceoverScene):
    def construct(self):
        c = load("collusion")
        self.card(c)
        self.game(c)
        self.learner()
        self.by_delta(c)
        self.scatter(load("sessions"))
        self.impulse(c, load("research"))
        self.markets()
        self.noise(c)
        self.factors()
        self.nfirms()
        self.law()
        self.cases()
        self.question()

    def card(self, c):
        d95 = [x for x in c["by_delta"] if x["delta_disc"] == 0.95][0]
        ch = chapter_card(6, r"Algorithmic collusion", r"Can algorithms that never communicate keep prices high?",
                          part=PART)
        with self.voiceover(
            "Chapter six, and the answer to the pause: no, they do not end up at competitive prices. In the House's "
            f"replication of a well-known experiment, two learning algorithms settle at an average price of "
            f"{d95['price']:.2f}, where competition would give {c['p_nash']:.2f} and a monopoly {c['p_mon']:.2f}: "
            f"{100 * d95['delta']:.0f} percent of the way from one to the other. They never exchange a message."
        ):
            self.play(FadeIn(ch[0], shift=UP * 0.2), FadeIn(ch[1]))
        self.play(FadeOut(ch))

    def game(self, c):
        rows = [cmath(r"q_i", r"=", r"\frac{e^{(a - p_i)/\mu}}{\sum_j e^{(a - p_j)/\mu} + e^{a_0/\mu}}", font_size=38,
                      colors={r"q_i": REAL_C}),
                cmath(r"\pi_i", r"=", r"(p_i - c)\,q_i", font_size=40),
                cmath(r"p^N", r"=", rf"{c['p_nash']:.3f},\quad p^M = {c['p_mon']:.3f}", font_size=40,
                      colors={r"p^N": COMP_C}),
                cmath(r"\text{grid}", r":", r"15\ \text{prices from } p^N - 0.1\Delta p \text{ to } p^M + 0.1\Delta p", font_size=34)]
        whys = [why(r"Calvano, Calzolari, Denicol\`o and Pastorello (2020): two firms, differentiated goods, logit demand "
                    r"($a = 2$, $a_0 = 0$, $\mu = 0.25$)"),
                why(r"each firm's profit, with marginal cost $c = 1$"),
                why(r"the one-shot Nash price, where each firm best-responds, and the price that maximises joint profit"),
                why(r"the learners choose from fifteen prices spanning both, with a margin on each side")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The experiment, from Emilio Calvano, Giacomo Calzolari, Vincenzo Denicolò and Sergio Pastorello. "
            "<bookmark mark='a'/> Two firms sell similar goods against logit demand. <bookmark mark='b'/> Each earns its "
            "margin times its demand. <bookmark mark='c'/> If they meet once, each best-responds and the price is "
            f"{c['p_nash']:.2f}; a monopolist owning both would charge {c['p_mon']:.2f}. <bookmark mark='d'/> The "
            "algorithms choose from fifteen prices spanning both."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def learner(self):
        rows = [cmath(r"s_t", r"=", r"(p_{1,t-1},\ p_{2,t-1})", font_size=40, colors={r"s_t": LEARN_C}),
                cmath(r"Q(s, p)", r"\leftarrow", r"(1 - \alpha)Q + \alpha\bigl[\pi + \delta \max_{p'} Q(s', p')\bigr]",
                      font_size=36),
                cmath(r"\varepsilon_t", r"=", r"e^{-\beta t}", font_size=40),
                cmath(r"\text{sessions}", r":", r"96 \times 1.5\ \text{million periods}", font_size=38)]
        whys = [why(r"each learner sees only last period's two prices: 225 states"),
                why(r"tabular Q-learning (Part 8): learning rate $\alpha = 0.15$, discount factor $\delta$"),
                why(r"explore at random with a probability that decays, $\beta = 4 \times 10^{-6}$"),
                why(r"run in parallel in the House's agents module; the collusion index is $(\pi - \pi^N)/(\pi^M - \pi^N)$")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The learners. <bookmark mark='a'/> Each remembers only last period's two prices. <bookmark mark='b'/> It "
            "keeps a table of how good each price is in each state, and nudges the entry toward the profit it got plus "
            "the discounted value of what comes next: Part eight's Q-learning. <bookmark mark='c'/> It explores at "
            "random, less and less. <bookmark mark='d'/> Ninety-six independent sessions of a million and a half "
            "periods each. The measure: how far profits sit between competition, zero, and monopoly, one."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def by_delta(self, c):
        rows = c["by_delta"]
        d = np.array([x["delta_disc"] for x in rows])
        m = np.array([x["delta"] for x in rows])
        lo = np.array([x["delta_q"][0] for x in rows])
        hi = np.array([x["delta_q"][2] for x in rows])
        g = axes([0, 1], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"discount factor $\delta$",
                 ylabel=r"collusion index", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1], font_size=15
                 ).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        bd = band(ax, d, lo, hi, COLL_C, opacity=0.2)
        ln = curve(ax, d, m, COLL_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.06, color=COLL_C) for a_, b_ in zip(d, m)])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(1, 0), color=COMP_C, stroke_width=1.5)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(1, 1), color=BAD, stroke_width=1.5)
        side = VGroup(label(r"1: monopoly", font_size=17, color=BAD), label(r"0: competition", font_size=17, color=COMP_C),
                      label(r"band: 10th to 90th percentile of 96 sessions", font_size=15, color=GREY_B)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        r0, r95 = rows[0], rows[-1]
        with self.voiceover(
            "The result, by how much the learners value the future. <bookmark mark='a'/> Myopic learners, with a "
            f"discount factor of zero, end at an index of {r0['delta']:.2f}: close to competition, above it only "
            "because learning is imperfect. <bookmark mark='b'/> As the future matters more, prices rise. "
            f"<bookmark mark='c'/> At nought point nine five, the index is {r95['delta']:.2f}. Patience is what makes "
            "collusion possible, exactly as in the theory of repeated games: the research chapter proves it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(zero), FadeIn(one), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(FadeIn(bd), Create(ln), FadeIn(dots[1:]), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(dots[-1], color=BAD, scale_factor=1.8))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, ss):
        rows = ss["rows"]
        g = axes([1.4, 2.0], [1.4, 2.0], x_length=4.6, y_length=4.6, xlabel=r"firm 1's price",
                 ylabel=r"firm 2's price", xticks=[1.5, 1.75, 2.0], yticks=[1.5, 1.75, 2.0], font_size=15
                 ).move_to(LEFT * 2.6 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(x["p1"], x["p2"]), radius=0.06, color=COLL_C, fill_opacity=0.7) for x in rows])
        nash = Dot(ax.c2p(ss["p_nash"], ss["p_nash"]), radius=0.1, color=COMP_C)
        mon = Dot(ax.c2p(ss["p_mon"], ss["p_mon"]), radius=0.1, color=BAD)
        diag = DashedLine(ax.c2p(1.4, 1.4), ax.c2p(2.0, 2.0), color=GREY_D, stroke_width=1)
        pun, sym = 100 * ss["punish"], 100 * ss["symmetric"]
        side = VGroup(label(r"each dot: one session's settled prices", font_size=17, color=COLL_C),
                      label(r"green: Nash; red: monopoly", font_size=17, color=GREY_A),
                      label(rf"{sym:.0f}\% of sessions end at equal prices", font_size=17, color=GREY_A),
                      label(rf"of the {ss['n_fixed']} that settle on one pair, {pun:.0f}\% punish a forced undercut",
                            font_size=17, color=HURDLE)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, RIGHT, buff=0.7)
        fit_right(side)
        n_fixed = ss["n_fixed"]
        with self.voiceover(
            "Session by session, at a discount factor of nought point nine five. <bookmark mark='a'/> Each dot is "
            "where one pair of learners settles. Almost all sit between the competitive point, in green, and the "
            f"monopoly point, in red, and well above the first. <bookmark mark='b'/> Only {sym:.0f} percent end at "
            "equal prices: the learners often split the gains unevenly, or cycle between price pairs. "
            f"<bookmark mark='c'/> And of the {n_fixed} sessions that settle on one pair, {pun:.0f} percent respond "
            "to a forced undercut with a punishment. The average impulse response is not an accident of averaging."
        ) as vo:
            self.play(FadeIn(g), FadeIn(diag), FadeIn(nash), FadeIn(mon))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02), FadeIn(side[:2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def impulse(self, c, r):
        p1 = np.asarray(c["ir1"], float)
        p2 = np.asarray(c["ir2"], float)
        t = np.arange(len(p1)) - 1
        g = axes([-1, len(p1) - 2], [1.4, 2.0], x_length=7.6, y_length=4.2, xlabel=r"period after the deviation",
                 ylabel=r"price", xticks=[0, 5, 10, 15], yticks=[1.5, 1.75, 2.0], font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, t, p1, LEARN_C, stroke_width=3)
        l2 = curve(ax, t, p2, COLL_C, stroke_width=3)
        d1 = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.05, color=LEARN_C) for a_, b_ in zip(t, p1)])
        d2 = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.05, color=COLL_C) for a_, b_ in zip(t, p2)])
        nash = DashedLine(ax.c2p(-1, c["p_nash"]), ax.c2p(len(p1) - 2, c["p_nash"]), color=COMP_C, stroke_width=1.5)
        mon = DashedLine(ax.c2p(-1, c["p_mon"]), ax.c2p(len(p1) - 2, c["p_mon"]), color=BAD, stroke_width=1.5)
        leg = legend([(LEARN_C, r"firm 1, forced to deviate at 0"), (COLL_C, r"firm 2"), (COMP_C, r"Nash"),
                      (BAD, r"monopoly")], font_size=16)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Is it collusion, or just slow learning? The test Calvano and coauthors proposed. Take the learned "
            f"strategies, averaged over the {c['n_ir']} sessions that settle on one price pair. <bookmark mark='a'/> "
            "Force firm one to undercut for a single period, to its best response. <bookmark mark='b'/> The next period, "
            "firm two cuts its own price sharply: a punishment. <bookmark mark='c'/> Then both climb back, within "
            f"about {r['back']} periods, to where they were. A reward for keeping prices high and a punishment for cutting them, "
            "learned without either firm being told to: that is what economists mean by collusion."
        ) as vo:
            self.play(FadeIn(g), FadeIn(nash), FadeIn(mon), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(d1[:3]), FadeIn(d2[:3]))
            vo.wait_until("b")
            self.play(Indicate(d2[2], color=BAD, scale_factor=2))
            vo.wait_until("c")
            self.play(Create(l1), Create(l2), FadeIn(d1[3:]), FadeIn(d2[3:]), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def markets(self):
        cards = VGroup(
            desk_question(r"market makers (Colliard, Foucault and Lovo)", r"Q-learning dealers competing on quotes earn "
                          r"spreads above the competitive level, but less so when adverse selection makes their "
                          r"profits riskier, as they report", width=12.4, font_size=19),
            desk_question(r"informed traders (Dou, Goldstein and Ji)", r"learning speculators trade less "
                          r"aggressively on their information than competition would make them, and prices become less "
                          r"informative, as they report", width=12.4, font_size=19),
            desk_question(r"spreads, not prices", r"for a market maker the price is the spread; a learned "
                          r"punishment is a tighter quote after a rival undercuts", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "In financial markets. <bookmark mark='a'/> Jean-Edouard Colliard, Thierry Foucault and Stefano Lovo put "
            "Q-learning dealers against each other: their spreads sit above the competitive level, but less so when "
            "adverse selection makes profits riskier, as they report. <bookmark mark='b'/> Winston Dou, Itay Goldstein "
            "and Yan Ji gave learning algorithms to informed speculators: they trade less aggressively than competition "
            "would make them, and prices carry less information. <bookmark mark='c'/> For a dealer the price is the "
            "spread, and a punishment is a tighter quote after a rival undercuts."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def noise(self, c):
        rows = c["by_noise"]
        tab = VGroup()
        head = VGroup(label(r"noise in each period's profit (s.d.)", font_size=19, color=QC.IDEA),
                      label(r"collusion index", font_size=19, color=QC.IDEA), label(r"mean price", font_size=19, color=QC.IDEA))
        tab.add(head)
        for x in rows:
            tab.add(VGroup(label(rf"{x['noise']:.2f}", font_size=21), label(rf"{x['delta']:.2f}", font_size=21, color=COLL_C),
                           label(rf"{x['price']:.2f}", font_size=21)))
        xs = [-3.6, 1.2, 4.4]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 2.0 - 0.75 * j, 0])
        note_ = wrapped_label(rf"discount factor 0.95; profits per period are about {c['pi_nash']:.2f} to "
                              rf"{c['pi_mon']:.2f}, so a noise of 0.2 is as large as the profit itself", 11.0, 17,
                              GREY_B).to_edge(DOWN, buff=0.5)
        hi = rows[-1]
        with self.voiceover(
            "The House's version of the market makers' finding. Add a random shock to every period's profit, as "
            "adverse selection does to a dealer's. <bookmark mark='a'/> Small noise changes little. "
            f"<bookmark mark='b'/> Noise as large as the profit itself brings the index down to {hi['delta']:.2f}. "
            "Collusion needs the learners to tell a rival's undercut from bad luck, and noisy profits make that hard."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def factors(self):
        cards = VGroup(
            desk_question(r"what makes collusion easier", r"few sellers, similar ones, frequent interaction, prices "
                          r"seen at once, and stable demand: the classic list (Ivaldi et al. 2003)", width=12.4,
                          font_size=19),
            desk_question(r"what algorithms change", r"they interact millions of times, see rivals' prices instantly and "
                          r"never forget: every item on the list, turned up", width=12.4, font_size=19),
            desk_question(r"and in markets", r"electronic quotes are visible to all in microseconds, and the same few "
                          r"firms meet in every stock, every day: Part 38's market makers", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why this matters more for algorithms than for people. <bookmark mark='a'/> Industrial economists list what "
            "makes tacit collusion easier: few and similar sellers, frequent interaction, prices seen at once, stable "
            "demand. <bookmark mark='b'/> Algorithms turn every item up: they interact millions of times, see rivals' "
            "prices instantly and never forget. <bookmark mark='c'/> And electronic markets are the extreme case: "
            "quotes visible to all in microseconds, and the same few firms meeting in every stock, every day."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def nfirms(self):
        rows = [cmath(r"\pi^c", r"=", r"\Pi^M / n,\quad \pi^d \approx \Pi^M,\quad \pi^n = 0", font_size=40),
                cmath(r"\delta^*", r"=", r"\frac{\Pi^M - \Pi^M/n}{\Pi^M - 0} = 1 - \frac1n", font_size=42,
                      colors={r"\delta^*": COLL_C}),
                cmath(r"n = 2, 3, 5, 10", r"\Rightarrow", r"\delta^* = 0.5,\ 0.67,\ 0.8,\ 0.9", font_size=40)]
        whys = [why(r"identical goods: colluding firms share the monopoly profit; a deviator who undercuts slightly takes "
                    r"all of it; competition drives profit to zero"),
                why(r"the research chapter's threshold, in closed form"),
                why(r"more sellers need more patience; Calvano and coauthors report lower collusion with three and four "
                    r"learners")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And why the number of sellers matters, in one line of algebra. <bookmark mark='a'/> With identical goods, "
            "colluding firms split the monopoly profit, a firm that undercuts slightly takes all of it, and competition "
            "leaves nothing. <bookmark mark='b'/> The research chapter's threshold becomes one minus one over n. "
            "<bookmark mark='c'/> Two sellers need a discount factor of a half; ten need nine tenths. Calvano and "
            "coauthors report less collusion with three and four learners, as the formula suggests."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def law(self):
        cards = VGroup(
            desk_question(r"economics", r"collusion is prices sustained above competition by rewards and punishments; "
                          r"by that test, these learners collude", width=12.4, font_size=19),
            desk_question(r"law", r"competition law mostly prohibits agreements, and tacit coordination without "
                          r"communication is generally lawful; whether learned coordination is an agreement is open "
                          r"(Harrington 2018)", width=12.4, font_size=19),
            desk_question(r"evidence", r"Assad, Clark, Ershov and Xu (2024): after German petrol stations adopted "
                          r"algorithmic pricing, margins rose where both stations in a duopoly adopted it, as they "
                          r"report", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "So, is it collusion? <bookmark mark='a'/> To an economist, yes: prices held above competition by rewards "
            "and punishments. <bookmark mark='b'/> To the law, it is unclear. Competition law mostly prohibits "
            "agreements, and coordination without communication is generally lawful; whether learned coordination "
            "counts is open, as Joseph Harrington has argued. <bookmark mark='c'/> And the evidence is starting to "
            "arrive: Stephanie Assad and coauthors found that when German petrol stations adopted pricing algorithms, "
            "margins rose where both stations in a local duopoly did, as they report."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def cases(self):
        cards = VGroup(
            desk_question(r"a shared vendor", r"in 2024 the US Justice Department sued RealPage, alleging that its "
                          r"rent-pricing software let competing landlords align rents through shared data; the "
                          r"allegations are contested, and are reported here as allegations", width=12.4, font_size=19),
            desk_question(r"the theory of harm", r"not two learners discovering collusion, but one algorithm pricing "
                          r"for many competitors: a hub, like Chapter 7's shared model", width=12.4, font_size=19),
            desk_question(r"why markets should care", r"a quoting model licensed to many dealers is the same structure; "
                          r"the House's audit runs on vendor models too", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "And the cases regulators have brought so far are of a different kind. <bookmark mark='a'/> In twenty "
            "twenty-four the American Justice Department sued RealPage, alleging that its rent-pricing software let "
            "competing landlords align rents through shared data. The allegations are contested, and they are reported "
            "here as allegations. <bookmark mark='b'/> The theory is not two learners discovering collusion on their "
            "own, but one algorithm pricing for many competitors: a hub, like Chapter seven's shared model. "
            "<bookmark mark='c'/> A quoting model licensed to many dealers has the same structure, which is why the "
            "House's audit runs on vendor models too."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a hundred traders each take a fifth of every trade from one shared model's signal, the rest "
                       r"from their own. What share of the market's order-flow variance is common?")
        with self.voiceover(
            "Pause and predict. A hundred traders each take a fifth of every trade from one shared model's signal, and "
            "the rest from their own independent views. What share of the variance of the market's order flow is "
            "common to all of them?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
