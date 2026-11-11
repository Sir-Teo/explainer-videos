from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
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
            f"""Chapter six. In this fixed-budget pricing experiment, the high-discount learners' mean price is {d95['price']:.2f}, compared with continuous-action Nash {c['p_nash']:.2f} and joint-monopoly {c['p_mon']:.2f}. Their profit interpolation index is {100*d95['delta']:.0f} percent of the gap between those benchmark profits. That percentage is not a fraction of the price gap. The algorithms exchange no explicit messages, but observe each other's previous prices."""
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
            f"""Results across the tested discount factors. <bookmark mark='a'/> Myopic learners have mean profit index {r0['delta']:.2f}. Grid effects and finite learning can put this above continuous-action Nash. <bookmark mark='b'/> The high-discount runs have larger average indices, but the tested sequence is not monotone: it first dips at discount point two five. <bookmark mark='c'/> At discount nought point nine five the index is {r95['delta']:.2f}. These finite runs show supra-competitive outcomes; they do not prove convergence or that patience is necessary for every form of algorithmic price elevation."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(zero), FadeIn(one), FadeIn(side), FadeIn(dots[0]))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
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
            f"""At discount nought point nine five, each dot summarises one frozen pair's post-training prices. <bookmark mark='a'/> The continuous Nash and monopoly points are references, not the complete equilibria of the fifteen-price game. <bookmark mark='b'/> Equal prices occur in {sym:.0f} percent of sessions. The remaining policies may cycle or be asymmetric. The recurrence search is capped at two hundred steps, below the two hundred twenty-five possible states. <bookmark mark='c'/> Among the {n_fixed} sessions classified as fixed points, {pun:.0f} percent meet this forced-undercut punishment criterion. This conditional percentage is not a rate across all sessions or proof of subgame perfection."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(diag), FadeIn(nash), FadeIn(mon), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.02), FadeIn(side[:2]), run_time=2)
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
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
            f"""A forced-deviation diagnostic, conditional on {c['n_ir']} sessions classified as fixed points. <bookmark mark='a'/> Firm one is forced to its best response for one period, after which both frozen policies resume. <bookmark mark='b'/> The mean rival price falls. <bookmark mark='c'/> The average response returns near its starting level after about {r['back']} periods. A return in the mean does not imply every session returns. This reward-and-punishment pattern is evidence of possible coordination, not a proof of equilibrium, intent or a legal agreement."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(nash), FadeIn(mon), FadeIn(side), FadeIn(d1[:3]), FadeIn(d2[:3]))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
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
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
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
            f"""A separate payoff-noise experiment. Independent zero-mean noise is added to period profits; it is not an adverse-selection model. <bookmark mark='a'/> The plotted outcomes depend on the tested noise levels and finite learning budget. <bookmark mark='b'/> At the largest level the mean profit index is {hi['delta']:.2f}. Noise can disrupt learned reward signals, but this experiment does not identify the effect of informed traders, who change conditional payoffs and incentives."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def factors(self):
        cards = VGroup(
            desk_question(r"what makes collusion easier", r"few sellers, similar ones, frequent interaction, prices "
                          r"seen at once, and stable demand: the classic list (Ivaldi et al. 2003)", width=12.4,
                          font_size=19),
            desk_question(r"what algorithms change", 'automation can increase interaction speed and history retention; information and decision constraints still vary', width=12.4, font_size=19),
            desk_question(r"and in markets", 'rapid repeated interaction and concentration can matter; hidden liquidity, entry and adverse selection complicate coordination', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Some conditions can facilitate coordination. <bookmark mark='a'/> Few sellers, repeated interaction, observable prices and stable demand appear in the industrial-organisation literature. <bookmark mark='b'/> Algorithms can interact frequently and retain histories, but their information, constraints and learning rules vary. <bookmark mark='c'/> Electronic markets can combine rapid interaction with concentrated participation. Hidden liquidity, asynchronous decisions, entry and adverse selection complicate the analogy; automation alone does not imply collusion."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
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
            desk_question(r"economics", 'supra-competitive prices and retaliation are coordination diagnostics; equilibrium and legal conclusions require additional evidence', width=12.4, font_size=19),
            desk_question(r"law", 'legal treatment depends on jurisdiction, agreement, information exchange and conduct; this simulation establishes no legal conclusion', width=12.4, font_size=19),
            desk_question(r"evidence", r"Assad, Clark, Ershov and Xu (2024): after German petrol stations adopted "
                          r"algorithmic pricing, margins rose where both stations in a duopoly adopted it, as they "
                          r"report", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Economic and legal questions differ. <bookmark mark='a'/> High prices plus a retaliatory response are coordination diagnostics, but frozen policies require further deviation checks before equilibrium claims. <bookmark mark='b'/> Legal treatment depends on jurisdiction, agreement, information exchange and conduct. A simulation cannot establish a violation or a general safe harbour. <bookmark mark='c'/> Assad and coauthors report evidence from German petrol pricing that margins rose where both stations in local duopolies adopted algorithms. That empirical setting is distinct from this simulator."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
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
            desk_question(r"why markets should care", 'vendor systems warrant review of shared information and feedback; common licensing alone does not establish unlawful coordination', width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label('A dated enforcement example: the 2024 complaint', font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "A dated example of enforcement allegations. <bookmark mark='a'/> In August twenty twenty-four the US Justice Department sued RealPage over alleged coordination through rent-pricing software and shared information. This describes that complaint, not the case's current status or a finding of liability. <bookmark mark='b'/> A shared pricing intermediary is structurally different from two independent learners in our experiment. <bookmark mark='c'/> Vendor models deserve scrutiny for shared information, constraints and feedback, without assuming that licensing one model itself establishes unlawful coordination."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('$N=100$, $x_i=0.2s+0.8e_i$; independent unit-variance signal components. What fraction of aggregate flow variance is common?')
        with self.voiceover(
            'Pause and predict. A hundred traders use orders x i equal to point two times a common signal plus point eight times a private signal. All signal components are independent, mean zero and unit variance. What fraction of the variance of their summed order flow comes from the common signal?'
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
