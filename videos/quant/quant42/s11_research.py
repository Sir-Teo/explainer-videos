from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import ladder
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C,
                                         fit_right, load)


class Research(VoiceoverScene):
    def construct(self):
        r = load("research")
        c = load("collusion")
        self.card()
        self.setup_game()
        self.one_shot()
        self.osd_proof()
        self.theorem(r)
        self.proof()
        self.finite()
        self.numbers(r)
        self.abreu(r)
        self.check(r, c)
        self.punish(r)
        self.learning()
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"When can collusion last?", r"How patient must two firms be for high prices to survive "
                          r"without an agreement?", part=PART)
        with self.voiceover("For the researcher. We derive a grim-trigger incentive condition in an infinitely repeated, perfectly monitored game with common action domains and a credible static-Nash punishment. We then compare that continuous-game benchmark with finite-grid learning outcomes. The comparison does not certify the learners' equilibrium. A separate grid-restricted punishment calculation will be labelled as illustrative algebra rather than a general bound."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_game(self):
        rows = [cmath(r"\pi^c", r":", r"\text{each firm's profit when both charge } p^c", font_size=38, colors={r"\pi^c": COLL_C}),
                cmath(r"\pi^d", r":", r"\text{the best one-period profit from undercutting } p^c", font_size=36,
                      colors={r"\pi^d": BAD}),
                cmath(r"\pi^n", r":", r"\text{the one-shot Nash profit}", font_size=38, colors={r"\pi^n": COMP_C}),
                cmath(r"\pi^d > \pi^c > \pi^n", r",", r"\ V = \textstyle\sum_t \delta^t \pi_t", font_size=40)]
        whys = [why(r"a collusive price, above the competitive one"),
                why(r"against a rival who keeps $p^c$, a firm earns more this period by cutting to its best response"),
                why(r"the price each firm sets when the game is played once"),
                why(r"the stage game repeated forever, payoffs discounted by $\delta$ per period")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "Three numbers from the one-period game. <bookmark mark='a'/> Pi c, each firm's profit when both charge a "
            "collusive price. <bookmark mark='b'/> Pi d, the most a firm can earn in one period by undercutting a "
            "rival who keeps that price. <bookmark mark='c'/> And pi n, the one-shot Nash profit. "
            "<bookmark mark='d'/> Undercutting pays today, colluding pays more than competing, and the game repeats "
            "forever with payoffs discounted by delta."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def one_shot(self):
        st = VGroup(MathTex(r"\sigma \text{ is subgame perfect} \iff \text{no player gains by deviating at one history "
                            r"and then returning to } \sigma", font_size=30),
                    wrapped_label(r"the one-shot deviation principle, for discounted games with bounded payoffs: a "
                                  r"profitable deviation, if any, can be truncated to a profitable deviation at a single "
                                  r"history, because payoffs far in the future count for little", 9.8, 20)
                    ).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The one-shot deviation principle (Blackwell; Abreu)", st, 'bounded discounted payoffs; proof sketch follows',
                            width=11.8, font_size=22, kind=r"Lemma")
        with self.voiceover(
            "The tool. <bookmark mark='a'/> A strategy profile is subgame perfect if and only if no player can gain by "
            "deviating at a single history and then going back to the strategy. <bookmark mark='b'/> In discounted games "
            "with bounded payoffs, any profitable deviation can be cut short to a profitable one-shot deviation, because "
            "the far future counts for little. So it is enough to check one period at a time."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def osd_proof(self):
        rows = [cmath(r"\text{suppose}", r":", r"\text{a deviation } \sigma' \text{ gains } \varepsilon > 0 \text{ at some history}",
                      font_size=34, colors={r"\text{suppose}": BAD}),
                cmath(r"\text{truncate}", r":", r"\text{follow } \sigma' \text{ for } T \text{ periods, then } \sigma;\ \text{loss} \le \frac{2M\delta^T}{1-\delta}",
                      font_size=32),
                cmath(r"T \text{ large}", r"\Rightarrow", r"\text{a deviation of finite length still gains}", font_size=36),
                cmath(r"\text{its last step}", r"\Rightarrow", r"\text{a profitable one-shot deviation}", font_size=36,
                      colors={r"\text{its last step}": GOOD})]
        whys = [why(r"if $\sigma$ is not subgame perfect, some player has a better continuation strategy somewhere"),
                why(r"payoffs are bounded by $M$, so what happens after period $T$ is worth at most this"),
                why(r"choose $T$ with $2M\delta^T/(1 - \delta) < \varepsilon$"),
                why('if no one-shot deviation pays at any history, remove the last deviating date without loss and repeat backwards')]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof sketch. <bookmark mark='a'/> Suppose a deviation improves continuation payoff by epsilon at some history. <bookmark mark='b'/> With absolute stage payoffs bounded by M, truncation after T periods changes payoff by at most two M delta to the T over one minus delta. <bookmark mark='c'/> Choose T large enough to preserve a gain. <bookmark mark='d'/> If no one-shot deviation is profitable at any history, remove the last deviating date without lowering payoff, then work backwards through every earlier date. That contradicts the profitable finite deviation. This uses discounted bounded payoffs and the standard perfect-monitoring strategy framework."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self, r):
        st = VGroup(MathTex(r"\text{grim trigger sustains } (p^c, p^c) \iff \delta \ \ge\ \delta^* = "
                            r"\frac{\pi^d - \pi^c}{\pi^d - \pi^n}", font_size=32),
                    wrapped_label(r"grim trigger: charge $p^c$ while both always have; after any deviation, charge the "
                                  r"Nash price forever", 9.8, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"Collusion by grim trigger (Friedman 1971)", st, r"this part's proof", width=11.8, font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The grim-trigger strategy, charge the collusive price as long as both "
            "always have, and the Nash price forever after any deviation, is a subgame-perfect equilibrium exactly when "
            "delta is at least pi d minus pi c, over pi d minus pi n. <bookmark mark='b'/> Patience must exceed the "
            "temptation to deviate, measured against the cost of the punishment."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(Indicate(st[0], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"\text{after a deviation}", r":", r"\text{Nash forever is a Nash equilibrium of every stage}", font_size=34,
                      colors={r"\text{after a deviation}": COMP_C}),
                cmath(r"\text{on the path}", r":", r"\frac{\pi^c}{1 - \delta}\ \ge\ \pi^d + \frac{\delta\,\pi^n}{1 - \delta}",
                      font_size=36, colors={r"\text{on the path}": COLL_C}),
                cmath(r"\iff", r"", r"\pi^c \ge (1 - \delta)\pi^d + \delta\pi^n", font_size=40),
                cmath(r"\iff", r"", r"\delta \ge \frac{\pi^d - \pi^c}{\pi^d - \pi^n}", font_size=42, colors={r"\iff": GOOD})]
        whys = [why(r"off the path, repeating the static equilibrium is subgame perfect: no one-shot deviation pays "
                    r"against a rival who ignores it"),
                why(r"on the path, by the lemma, compare colluding forever with deviating once and then facing Nash "
                    r"forever"),
                why(r"multiply by $1 - \delta$"),
                why(r"rearrange; since $\pi^d > \pi^c > \pi^n$ the threshold lies strictly between 0 and 1")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The proof, by the lemma. <bookmark mark='a'/> Off the path, after a deviation, both charge the Nash price "
            "forever. That is subgame perfect: against a rival who will charge Nash whatever you do, no one-shot "
            "deviation pays. <bookmark mark='b'/> On the path, compare colluding forever with deviating once, earning "
            "pi d, and then Nash forever. <bookmark mark='c'/> Multiply through by one minus delta. "
            "<bookmark mark='d'/> And rearrange. Because pi d exceeds pi c, which exceeds pi n, the threshold lies "
            "strictly between zero and one."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def finite(self):
        rows = [cmath(r"\text{punish for } T", r":", r"\text{Nash for } T \text{ periods, then back to } p^c", font_size=38,
                      colors={r"\text{punish for } T": BAD}),
                cmath(r"\pi^d - \pi^c", r"\le", r"(\pi^c - \pi^n)\,(\delta + \delta^2 + \cdots + \delta^T)", font_size=38),
                cmath(r"\delta^*_T", r"\downarrow", r"\delta^* \text{ as } T \to \infty", font_size=40, colors={r"\delta^*_T": HURDLE})]
        whys = [why('specified strategy: Nash for $T$ periods, restart the clock after any further deviation, then return'),
                why(r"by the lemma: the gain from deviating today against the profit lost during the $T$ periods of "
                    r"punishment"),
                why('a threshold below 1 requires $T(\\pi^c-\\pi^n)>\\pi^d-\\pi^c$; feasible thresholds approach grim trigger')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A finite-punishment strategy needs its off-path rule specified. <bookmark mark='a'/> After deviation, play static Nash for T periods; any deviation during punishment restarts the clock. Then return to collusion. <bookmark mark='b'/> On the cooperation path, deterrence requires today's gain to be no larger than the discounted loss during T punishment periods. During punishment, Nash best response prevents a current gain and restarting delays the better continuation. <bookmark mark='c'/> A finite threshold below one exists only when T times the per-period punishment loss exceeds the deviation gain. Longer feasible punishments approach grim trigger."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def numbers(self, r):
        m = r["mono"]
        T = m["T"]
        lines = VGroup(
            label(rf"at the monopoly price: $\pi^c = {m['pi_c']:.3f}$, $\pi^d = {m['pi_d']:.3f}$, $\pi^n = {m['pi_n']:.3f}$",
                  font_size=22, color=GREY_A),
            label(rf"grim trigger: $\delta^* = {m['grim']:.2f}$", font_size=26, color=COLL_C),
            label(rf"punish for 1, 2, 3, 5 periods: $\delta^* = {T['1']:.2f}$, ${T['2']:.2f}$, ${T['3']:.2f}$, ${T['5']:.2f}$",
                  font_size=22, color=BAD),
            label(r"lower collusive prices: " + ", ".join(rf"${x['price']:.2f} \to {x['grim']:.2f}$" for x in r["rows"]),
                  font_size=20, color=HURDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(ORIGIN)
        with self.voiceover(
            f"""Continuous-action logit benchmarks. <bookmark mark='a'/> These are the collusive, best-deviation and Nash profits for the stated action domain. <bookmark mark='b'/> The grim-trigger threshold is {m['grim']:.2f}. <bookmark mark='c'/> A one-period Nash punishment requires {T['1']:.2f}; a five-period one requires {T['5']:.2f}, using the specified restart rule. <bookmark mark='d'/> The selected lower collusive prices give the displayed thresholds. The learners use fifteen prices, so their exact incentive constraints must be computed in that discrete game before claiming equilibrium."""
        ) as vo:
            self.play(FadeIn(lines[0], shift=RIGHT * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c', 'd')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(lines[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def abreu(self, r):
        m = r["mono"]
        rows = [cmath(r"\underline\pi", r"=", '\\min_{p_2\\in G}\\max_{p_1\\in G}\\pi_1(p_1,p_2)', font_size=40, colors={r"\underline\pi": BAD}),
                cmath(r"\text{illustrative ratio}", r"=", r"\frac{\pi^d - \pi^c}{\pi^d - \underline\pi}", font_size=42),
                cmath(r"\text{here}", r":", rf"\underline\pi_G = {m['minmax']:.3f},\ \ R = {m['abreu']:.2f}\ \ "
                      rf"(\text{{against }} {m['grim']:.2f})", font_size=36, colors={r"\text{here}": HURDLE})]
        whys = [why('pure grid min-best-response value; mixed-action minmax and credible continuation payoffs require separate analysis'),
                why('mixed action domains: grid punishment value with continuous collusion/deviation profits; this ratio is illustrative only'),
                why('do not interpret this mixed-domain ratio as a universal equilibrium bound or an attainable penal code')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        mm, ab, gr = m["minmax"], m["abreu"], m["grim"]
        with self.voiceover(
            f"""An important domain warning. <bookmark mark='a'/> The displayed minimisation takes a pure opponent price on the fifteen-point grid and a best response on that grid. It yields {mm:.3f}; this is not a mixed-action minmax calculation. <bookmark mark='b'/> Inserting that value alongside continuous-action monopoly and deviation profits gives the illustrative ratio {ab:.2f}. Because the action domains differ, it is not a universal lower bound or an established optimal penal code. <bookmark mark='c'/> The continuous grim reference is {gr:.2f}. Abreu's theory concerns credible continuation punishments under explicit game assumptions; this computation does not establish attainability of its illustrative ratio."""
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def check(self, r, c):
        rows = c["by_delta"]
        d = np.array([x["delta_disc"] for x in rows])
        mm = np.array([x["delta"] for x in rows])
        g = axes([0, 1], [0, 1], x_length=7.4, y_length=4.2, xlabel=r"discount factor $\delta$",
                 ylabel=r"collusion index of the learners", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        thr = r["mono"]["grim"]
        shade = Rectangle(width=ax.c2p(1, 0)[0] - ax.c2p(thr, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1],
                          stroke_width=0, fill_color=COLL_C, fill_opacity=0.12)
        shade.move_to([(ax.c2p(1, 0)[0] + ax.c2p(thr, 0)[0]) / 2, (ax.c2p(0, 1)[1] + ax.c2p(0, 0)[1]) / 2, 0])
        vl = DashedLine(ax.c2p(thr, 0), ax.c2p(thr, 1), color=COLL_C, stroke_width=2)
        vl_l = label(rf"$\delta^* = {thr:.2f}$", font_size=17, color=COLL_C).next_to(ax.c2p(thr, 1), UP, buff=0.08)
        ln = curve(ax, d, mm, LEARN_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.06, color=LEARN_C) for a_, b_ in zip(d, mm)])
        side = VGroup(label('shaded: continuous-game grim benchmark', font_size=16, color=COLL_C),
                      label(r"dots: what 96 learners found", font_size=16, color=LEARN_C)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.25)
        side.next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        d5 = [x for x in rows if x["delta_disc"] == 0.5][0]
        with self.voiceover(
            f"""Comparing a theoretical reference with finite learning. <bookmark mark='a'/> The shaded region permits continuous-action monopoly under the specified grim strategy. <bookmark mark='b'/> At discount one half the learners' finite-run profit index is {d5['delta']:.2f}; higher tested discounts have larger averages. <bookmark mark='c'/> The grim threshold characterises that strategy, not every collusive equilibrium, and the learning game is discrete. These sessions do not prove a necessary patience threshold for learning. Exploration and coupled estimates are possible mechanisms, not identified causes from this chart alone."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(side), FadeIn(shade), FadeIn(vl), FadeIn(vl_l))
            vo.wait_until("a")
            pass  # first substantive content already entered before the bookmark
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(dots), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(dots[2], color=BAD, scale_factor=1.8))
        self.wait(0.4)
        self.clear_scene()

    def punish(self, r):
        T = r["mono"]["T"]
        rows = [cmath(r"\text{learned punishment}", r":", rf"\text{{deep, then back within about }} {r['back']} \text{{ periods}}",
                      font_size=36, colors={r"\text{learned punishment}": LEARN_C}),
                cmath(r"\delta^*_{5}", r"=", rf"{T['5']:.2f}\ \ \le\ \ 0.95", font_size=40, colors={r"\delta^*_{5}": HURDLE}),
                cmath(r"\Rightarrow", r"", '\\text{duration alone does not verify learned incentives}', font_size=38, colors={r"\Rightarrow": GOOD})]
        whys = [why('selected fixed-point subset: the mean rival price falls and the average response returns near baseline'),
                why(r"by the corollary, a five-period punishment deters deviation at any $\delta$ above this"),
                why('the learned response is not the theoretical Nash punishment; equilibrium requires incentive checks at every relevant history')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            f"""The mean learned impulse response returns near baseline after about {r['back']} periods in the selected fixed-point subset. <bookmark mark='a'/> It is not a deterministic five-period Nash punishment. <bookmark mark='b'/> The theoretical five-period strategy has continuous-game threshold {T['5']:.2f}, below the learners' discount point nine five. <bookmark mark='c'/> Similar duration does not establish the learned policies' incentives at every history. Further deviations, individual responses and discrete action constraints need checking before an equilibrium claim."""
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def learning(self):
        cards = VGroup(
            desk_question(r"why learners find it", r"not by reasoning about equilibria: Q-learning's estimates of a "
                          r"price's value depend on the rival's play, so the two learners' errors become correlated",
                          width=12.4, font_size=19),
            desk_question(r"Banchio and Mantegazza (2023)", r"call this spontaneous coupling, and show that it can "
                          r"sustain high prices even without memory or patience", width=12.4, font_size=19),
            desk_question(r"Fish, Gonczarowski and Shorrer (2024)", r"report that pricing agents built on large "
                          r"language models also reach supra-competitive prices in such games", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why learners find collusion at all. <bookmark mark='a'/> Not by reasoning about equilibria. A Q-learner's "
            "estimate of a price's value depends on what its rival is doing, so the two learners' errors move together. "
            "<bookmark mark='b'/> Martino Banchio and Giacomo Mantegazza call this spontaneous coupling, and show it can "
            "hold prices up even without memory or patience. <bookmark mark='c'/> And Sara Fish, Yannai Gonczarowski "
            "and Ran Shorrer report that pricing agents built on language models reach high prices in such games too."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"the folk theorem", r"Fudenberg and Maskin (1986): with enough patience, any feasible, "
                          r"individually rational payoff can be an equilibrium of the repeated game", width=12.4,
                          font_size=19),
            desk_question(r"imperfect monitoring", r"Green and Porter (1984): when prices are observed with noise, "
                          r"collusion needs price wars on bad news, as Chapter 6's noisy profits suggested", width=12.4,
                          font_size=19),
            desk_question(r"algorithms and commitment", r"Brown and MacKay (2023): faster-updating pricing algorithms "
                          r"raise prices even without collusion, by acting as commitment", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Related theory, with its assumptions kept visible. <bookmark mark='a'/> Folk theorems describe broad sets of feasible individually rational payoffs for sufficiently patient players under appropriate monitoring and game conditions; they do not select the outcome a learner reaches. <bookmark mark='b'/> Green and Porter show how imperfect monitoring can generate equilibrium price wars. Independent additive payoff noise here is only a loose analogy. <bookmark mark='c'/> Brown and MacKay analyse price algorithms and commitment through differing revision frequencies. High prices need not have the same mechanism in every algorithmic market."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"a theory of learning", r"which equilibria Q-learning and gradient learners reach, how fast, "
                          r"and how that depends on exploration and memory", width=12.4, font_size=19),
            desk_question(r"detection", r"tests that tell learned collusion from competition in market data, without "
                          r"access to the algorithms", width=12.4, font_size=19),
            desk_question(r"design", r"market rules, such as price-update frequencies or batch auctions, that make "
                          r"learned collusion unprofitable", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three open problems. <bookmark mark='a'/> A theory of learning: which equilibria learners reach, how fast, "
            "and how that depends on exploration and memory. <bookmark mark='b'/> Detection: tests that distinguish "
            "learned collusion from competition in market data, without seeing the algorithms. <bookmark mark='c'/> "
            "And design: market rules that make learned collusion unprofitable."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            for k, m_ in enumerate(('a', 'b', 'c')):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card('at zero discount, profitable current deviations defeat grim trigger. Why can finite-grid learners still exceed the continuous Nash reference?')
        with self.voiceover(
            'Pause and predict. With zero discounting, the grim-trigger mechanism cannot sustain a price with a profitable current deviation. Yet these finite-grid myopic learners can score above the continuous Nash reference. Give two possible explanations, and say why that does not prove a repeated-game equilibrium.'
        ):
            self.play(FadeIn(q))
        self.wait(6.0)
        self.clear_scene()
