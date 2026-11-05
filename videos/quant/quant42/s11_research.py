from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
        with self.voiceover("For the researcher. Chapter six watched learning algorithms keep prices high and punish a "
                            "rival that cut them. This chapter proves when such behaviour can be an equilibrium at all, "
                            "computes the threshold for Chapter six's game, and compares it with what the learners "
                            "actually did, which is not the same thing."):
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
        card = theorem_card(r"The one-shot deviation principle (Blackwell; Abreu)", st, r"used, not proved here",
                            width=11.8, font_size=22, kind=r"Lemma")
        with self.voiceover(
            "The tool. <bookmark mark='a'/> A strategy profile is subgame perfect if and only if no player can gain by "
            "deviating at a single history and then going back to the strategy. <bookmark mark='b'/> In discounted games "
            "with bounded payoffs, any profitable deviation can be cut short to a profitable one-shot deviation, because "
            "the far future counts for little. So it is enough to check one period at a time."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
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
                why(r"take the shortest such deviation: at its last deviating history, deviating once and then returning "
                    r"to $\sigma$ must already pay, or a shorter one would")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "For the researcher who wants the lemma proved too, the sketch. <bookmark mark='a'/> Suppose some deviation "
            "gains epsilon at some history. <bookmark mark='b'/> Truncate it: follow it for T periods, then return to "
            "the strategy. Payoffs are bounded, so what happens after T is worth at most two M delta to the T over one "
            "minus delta. <bookmark mark='c'/> For T large enough the truncated deviation still gains. "
            "<bookmark mark='d'/> Take the shortest profitable one. At its last deviating history, deviating once and "
            "then returning must already pay, or a shorter deviation would. So a profitable one-shot deviation exists."
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
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
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
        whys = [why(r"a forgiving punishment, like the learners' in Chapter 6"),
                why(r"by the lemma: the gain from deviating today against the profit lost during the $T$ periods of "
                    r"punishment"),
                why(r"shorter punishments need more patience; the grim threshold is the limit")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "A corollary, for forgiving punishments like the learners'. <bookmark mark='a'/> Punish with the Nash price "
            "for T periods, then return to colluding. <bookmark mark='b'/> By the same lemma, this deters a deviation "
            "when today's gain is no larger than the profit lost during the punishment. <bookmark mark='c'/> Shorter "
            "punishments need more patience, and as T grows the threshold falls to the grim one."
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
            "For Chapter six's logit game. <bookmark mark='a'/> At the monopoly price, the three profits are these. "
            f"<bookmark mark='b'/> Grim trigger sustains monopoly pricing for any delta above {m['grim']:.2f}. "
            f"<bookmark mark='c'/> A one-period punishment needs {T['1']:.2f}; a five-period one, {T['5']:.2f}, almost "
            "the grim threshold. <bookmark mark='d'/> And less ambitious collusion needs less patience: the lower the "
            "collusive price, the smaller the temptation to cut it."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                self.play(FadeIn(lines[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def abreu(self, r):
        m = r["mono"]
        rows = [cmath(r"\underline\pi", r"=", r"\min_{p_2}\max_{p_1} \pi_1(p_1, p_2)", font_size=40, colors={r"\underline\pi": BAD}),
                cmath(r"\delta \ge", r"", r"\frac{\pi^d - \pi^c}{\pi^d - \underline\pi}", font_size=42),
                cmath(r"\text{here}", r":", rf"\underline\pi = {m['minmax']:.3f},\ \ \delta \ge {m['abreu']:.2f}\ \ "
                      rf"(\text{{against }} {m['grim']:.2f})", font_size=36, colors={r"\text{here}": HURDLE})]
        whys = [why(r"the minmax profit: the least a rival can hold you to, if it tries; no equilibrium punishment is "
                    r"harsher"),
                why(r"Abreu (1988): optimal penal codes, sticks and carrots, can approach this bound, which no "
                    r"punishment can beat"),
                why(r"on Chapter 6's grid; the learners, at 0.95, are far above either bound")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        mm, ab, gr = m["minmax"], m["abreu"], m["grim"]
        with self.voiceover(
            "How low can the threshold go? <bookmark mark='a'/> No punishment can hold a firm below its minmax profit: "
            "the least a rival can force on it. <bookmark mark='b'/> So no scheme sustains collusion below this "
            "threshold, and Dilip Abreu's optimal penal codes, a short sharp stick followed by a carrot, can approach "
            f"it. <bookmark mark='c'/> On Chapter six's grid the minmax profit is {mm:.3f}, and the bound is "
            f"{ab:.2f}, against {gr:.2f} for grim trigger. The learners, at nought point nine five, are far above both."
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
        side = VGroup(label(r"shaded: monopoly is an equilibrium", font_size=16, color=COLL_C),
                      label(r"dots: what 96 learners found", font_size=16, color=LEARN_C)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.25)
        side.next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        d5 = [x for x in rows if x["delta_disc"] == 0.5][0]
        with self.voiceover(
            "The check, against the learners. <bookmark mark='a'/> To the right of the threshold, monopoly pricing can "
            "be sustained. <bookmark mark='b'/> The learners do not find it there at first: at a discount factor of a "
            f"half, already above the threshold, their index is only {d5['delta']:.2f}. Only with delta of nought point "
            "nine and above do they get most of the way. <bookmark mark='c'/> So the theorem is the right necessary "
            "condition, and learning needs far more patience than equilibrium does. A plausible reason: while the "
            "learners explore, a rival's punishment is hard to tell from noise, so it must be worth a great deal to "
            "learn."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(shade), FadeIn(vl), FadeIn(vl_l))
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
                cmath(r"\Rightarrow", r"", r"\text{a finite, forgiving punishment is enough}", font_size=38, colors={r"\Rightarrow": GOOD})]
        whys = [why(r"Chapter 6's impulse response: the rival cuts below Nash, then both return"),
                why(r"by the corollary, a five-period punishment deters deviation at any $\delta$ above this"),
                why(r"the learners need not find grim trigger; any punishment long enough satisfies the corollary at "
                    r"their discount factor, and forgiveness avoids price wars that never end")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the learned punishments. <bookmark mark='a'/> Chapter six's impulse response: a deep cut, then a "
            f"return within about {r['back']} periods. <bookmark mark='b'/> By the corollary, a five-period punishment "
            f"deters deviation for any delta above {T['5']:.2f}, far below the learners' nought point nine five. "
            "<bookmark mark='c'/> So they need not discover grim trigger. Any punishment long enough will do, and "
            "forgiving ones avoid price wars that never end."
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
            "Where the theory goes. <bookmark mark='a'/> The folk theorem of Drew Fudenberg and Eric Maskin: with enough "
            "patience, almost any outcome better than the punishment can be an equilibrium, which is why the theorem is "
            "necessary but says little about which one learners reach. <bookmark mark='b'/> Edward Green and Robert "
            "Porter: when rivals' prices are seen only through noise, collusion needs occasional price wars, as Chapter "
            "six's noisy profits suggested. <bookmark mark='c'/> And Zach Brown and Alexander MacKay: algorithms that "
            "update faster than rivals raise prices even without collusion, by acting as commitment."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
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
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"with $\delta = 0$ the theorem allows no collusion, yet the myopic learners ended above Nash. "
                       r"Give two reasons.")
        with self.voiceover(
            "Pause and predict. With a discount factor of zero, the theorem allows no collusion, yet the myopic "
            "learners ended above the Nash profit. Give two reasons."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
