from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant38.common import (BAD, GOOD, HURDLE, MAKER_C, PART, SNIPE_C, SPREAD_C, load)


class Research(VoiceoverScene):
    def construct(self):
        b = load("bcs")
        self.card()
        self.setup_()
        self.payoffs()
        self.undercut()
        self.existence()
        self.theorem()
        self.statics()
        self.general(b)
        self.check_sim(b)
        self.check_fba(b)
        self.fba_logic()
        self.fba_theorem()
        self.welfare(b)
        self.arms_formal()
        self.check_general(b)
        self.btc(b)
        self.related()
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The sniping equilibrium", r"Why does competition in speed not narrow the spread, and what "
                          r"would?", part=PART)
        with self.voiceover("For the researcher. Chapter six stated Budish, Cramton and Shim's result: the sniping spread "
                            "does not depend on how many firms race. This chapter proves it as an equilibrium, generalises "
                            "it to any jump distribution, proves that batch auctions remove the prize, and checks both "
                            "by simulation and against Bitcoin."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        rows = [cmath(r"y_t", r":", r"\text{public value, jumps } \pm J \text{ at rate } \lambda_J", font_size=34),
                cmath(r"\text{investors}", r":", r"\text{rate } \lambda_I,\ \text{trade one unit at the best quote}",
                      font_size=32),
                cmath(r"N\ \text{firms}", r":", r"\text{equally fast; serial processing, random order}", font_size=32),
                cmath(r"\text{roles}", r":", r"\text{one provides } y \pm s/2;\ \text{the others may snipe}", font_size=32,
                      colors={r"\text{roles}": MAKER_C})]
        whys = [why(r"the value moves only on public news, seen by all fast firms at once"),
                why(r"investors are uninformed and impatient: they pay the half-spread"),
                why(r"messages sent at the same instant are processed one at a time, each order equally likely"),
                why(r"a liquidity provider quotes around the value; when a jump makes its quote stale, it tries to cancel and "
                    r"the others try to trade against it")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The model. <bookmark mark='a'/> A public value that jumps up or down by J at rate lambda J. "
            "<bookmark mark='b'/> Uninformed investors who arrive at rate lambda I and pay the half-spread. "
            "<bookmark mark='c'/> N fast firms, equally fast, whose simultaneous messages the exchange processes one at a "
            "time in random order. <bookmark mark='d'/> One firm provides liquidity around the value; when a jump makes "
            "its quote stale it tries to cancel, and the others try to trade against it."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        rows = [cmath(r"\pi_L(s)", r"=", r"\lambda_I \tfrac s2 - \lambda_J \tfrac{N - 1}{N}\,(J - \tfrac s2)^+", font_size=36,
                      colors={r"\pi_L(s)": MAKER_C}),
                cmath(r"\pi_S(s)", r"=", r"\lambda_J \tfrac1N\,(J - \tfrac s2)^+", font_size=36, colors={r"\pi_S(s)": SNIPE_C}),
                cmath(r"\pi_L - \pi_S", r"=", r"\lambda_I \tfrac s2 - \lambda_J (J - \tfrac s2)^+", font_size=36,
                      colors={r"\pi_L - \pi_S": HURDLE})]
        whys = [why(r"Lemma 1: the provider earns from every investor and loses to a jump whenever one of the other "
                    r"$N - 1$ messages is processed before its cancel"),
                why(r"each other firm wins a given race with probability $1/N$"),
                why(r"the difference no longer contains $N$: the two $1/N$ terms add to one race lost per jump")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma one, the payoffs. <bookmark mark='a'/> The provider earns from every investor, and loses whenever one "
            "of the other N minus one messages beats its cancel. <bookmark mark='b'/> Each other firm wins a given race "
            "one time in N. <bookmark mark='c'/> And the difference between the two roles does not contain N at all: the "
            "provider's losses and one sniper's gains add up to one whole race per jump."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def undercut(self):
        rows = [cmath(r"s > s^*", r"\Rightarrow", r"\pi_L > \pi_S:\ \text{a rival undercuts}", font_size=36),
                cmath(r"s < s^*", r"\Rightarrow", r"\pi_L < \pi_S:\ \text{the provider withdraws}", font_size=36),
                cmath(r"\Rightarrow", r"\ ", r"\pi_L(s^*) = \pi_S(s^*)", font_size=40, colors={r"\pi_L(s^*) = \pi_S(s^*)": HURDLE})]
        whys = [why(r"Lemma 2: if providing pays more than sniping, another firm posts a slightly narrower spread, takes the "
                    r"investors, and earns more; Bertrand competition in price"),
                why(r"if it pays less, the provider would rather snipe; no one provides at that spread"),
                why(r"so any equilibrium spread makes the two roles equally attractive")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma two, indifference. <bookmark mark='a'/> If providing paid more than sniping, a rival would post a "
            "slightly narrower spread, take the investors, and earn more: competition on price. <bookmark mark='b'/> If "
            "it paid less, the provider would rather snipe, and no one would provide at that spread. "
            "<bookmark mark='c'/> So in any equilibrium the two roles are equally attractive."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def existence(self):
        rows = [cmath(r"D(h)", r"=", r"\lambda_I h - \lambda_J (J - h)^+", font_size=40),
                cmath(r"D(0) < 0,\ \ D(J) > 0", r",", r"D\ \text{strictly increasing}", font_size=34),
                cmath(r"\Rightarrow", r"\ ", r"h^* = \frac{\lambda_J J}{\lambda_I + \lambda_J}\ \text{unique}", font_size=38,
                      colors={r"h^* = \frac{\lambda_J J}{\lambda_I + \lambda_J}\ \text{unique}": HURDLE})]
        whys = [why(r"Lemma 3: the difference as a function of the half-spread $h = s/2$"),
                why(r"negative at zero, positive at the jump size, and strictly increasing in between"),
                why(r"so it has exactly one root, and on $[0, J]$ it is linear: solve for $h$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Lemma three, existence and uniqueness. <bookmark mark='a'/> Write the difference as a function of the "
            "half-spread h. <bookmark mark='b'/> It is negative at zero, positive at the jump size, and strictly "
            "increasing. <bookmark mark='c'/> So it has exactly one root, and between zero and J it is linear: the "
            "half-spread is lambda J times J over lambda I plus lambda J."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def theorem(self):
        st = VGroup(MathTex(r"\frac{s^*}{2} = \frac{\lambda_J J}{\lambda_I + \lambda_J},\qquad \text{independent of } N",
                            font_size=32),
                    MathTex(r"\text{sniping rents} = \lambda_J\,(J - \tfrac{s^*}{2}) = \lambda_I\,\tfrac{s^*}{2}\ "
                            r"\text{per unit time, paid by investors}", font_size=28),
                    wrapped_label(r"more fast firms split the prize more ways but leave it, and the spread, unchanged; any "
                                  r"firm slightly faster wins every race, so all invest in speed and the investment is "
                                  r"wasted in equilibrium", 9.6, 20)).arrange(DOWN, buff=0.35)
        card = theorem_card(r"The sniping equilibrium (Budish, Cramton and Shim 2015)", st, r"this part's proof", width=11.8,
                            font_size=22)
        with self.voiceover(
            "The theorem. <bookmark mark='a'/> The equilibrium half-spread is lambda J J over lambda I plus lambda J, "
            "independent of the number of firms. <bookmark mark='b'/> The sniping rents, per unit of time, equal what "
            "investors pay in the spread: investors bear the whole cost of the races. More firms split the prize more "
            "ways but leave it unchanged, and since any firm slightly faster would win every race, all invest in speed, "
            "and the investment is wasted."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(st[1], color=HURDLE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def statics(self):
        rows = [cmath(r"\frac{\partial h^*}{\partial \lambda_J}", r">", r"0", font_size=40),
                cmath(r"\frac{\partial h^*}{\partial \lambda_I}", r"<", r"0", font_size=40),
                cmath(r"\frac{\partial h^*}{\partial N}", r"=", r"0", font_size=40, colors={r"0": HURDLE})]
        whys = [why(r"more frequent public news, more races, wider spreads: markets with many correlated instruments, such "
                    r"as an ETF and its futures, are sniped most"),
                why(r"more uninformed investors spread the sniping cost over more trades: busier markets are cheaper"),
                why(r"the striking one: adding fast firms changes nothing for investors")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What moves the spread. <bookmark mark='a'/> More frequent public news means more races and wider spreads: "
            "markets tied to many correlated instruments are sniped the most. <bookmark mark='b'/> More uninformed "
            "investors spread the cost over more trades, so busier markets are cheaper. <bookmark mark='c'/> And the "
            "striking one: adding fast firms changes nothing for investors."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def general(self, b):
        rows = [cmath(r"\lambda_I\,h^*", r"=", r"\lambda_J\,\mathbb E\big[(|J| - h^*)^+\big]", font_size=40,
                      colors={r"\lambda_I\,h^*": HURDLE}),
                cmath(r"\text{LHS}\uparrow,\ \text{RHS}\downarrow", r"\Rightarrow", r"\text{a unique root}", font_size=36),
                cmath(r"\text{fat-tailed jumps}", r"\Rightarrow", r"\text{wider spreads}", font_size=36,
                      colors={r"\text{wider spreads}": BAD})]
        whys = [why(r"with random jump sizes, the provider loses only on jumps larger than its half-spread, and then the "
                    r"excess"),
                why(r"the left side rises in $h$, the right side falls: the same argument gives one equilibrium"),
                why(r"for a fixed mean, a more dispersed jump distribution raises $\mathbb E[(|J| - h)^+]$ or leaves it unchanged "
                    r"(it is convex in $J$), so the spread widens or stays: tails, not averages, set the cost of being "
                    r"sniped")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The general case. <bookmark mark='a'/> With random jump sizes, the provider loses only on jumps larger than "
            "its half-spread, and only the excess. <bookmark mark='b'/> The left side rises with h and the right side "
            "falls, so again there is exactly one equilibrium. <bookmark mark='c'/> And since the excess is convex in the "
            "jump, more dispersed jumps with the same mean widen the spread or leave it unchanged: the tails, not the "
            "average, set the cost of being sniped."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check_sim(self, b):
        sims = b["sims"]
        x = np.asarray([s["half"] for s in sims], float)
        d = np.asarray([s["lp"] - s["sniper"] for s in sims], float)
        k = int(np.argmin(np.abs(d)))
        cross = float(np.interp(0, d, x)) if np.all(np.diff(d) > 0) else float(x[k])
        rows = [cmath(r"\text{formula}", r":", rf"s^*/2 = {b['s_star']:.3f}", font_size=38, colors={r"\text{formula}": HURDLE}),
                cmath(r"\text{simulation}", r":", rf"\pi_L = \pi_S\ \text{{at}}\ {cross:.3f}", font_size=38),
                cmath(r"N = 2 \ldots 30", r":", r"\pi_L = \pi_S\ \text{at } s^*\ \text{for every } N", font_size=34,
                      colors={r"N = 2 \ldots 30": GOOD})]
        whys = [why(r"$\lambda_I = 1$, $\lambda_J = 0.1$, $J = 4$"),
                why(r"two hundred thousand units of time; the crossing of the two profit curves, interpolated"),
                why(r"Chapter 6's table: at the formula's spread the two roles earn the same whatever the number of firms")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            f"Check one: simulation. <bookmark mark='a'/> The formula gives {b['s_star']:.3f}. "
            f"<bookmark mark='b'/> The simulated profit curves cross at {cross:.3f}. <bookmark mark='c'/> And at that "
            "spread, with two firms or thirty, the two roles earn the same, as the theorem says."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check_fba(self, b):
        f = b["fba"]
        rows = [cmath(r"\text{continuous}", r":", rf"\pi_S = {b['byN'][2]['sniper']:.3f}", font_size=38,
                      colors={r"\text{continuous}": SNIPE_C}),
                cmath(r"\text{batch}", r":", rf"\pi_S = {f['sniper']:.0f}", font_size=38, colors={r"\text{batch}": GOOD}),
                cmath(r"\text{provider at } s^*", r":", rf"\pi_L = {f['lp']:.3f}\ \text{{(all spread, no losses)}}", font_size=34)]
        whys = [why(r"five firms, at the equilibrium spread of continuous trading"),
                why(r"in a batch auction, quotes are re-set with the current value before each clearing: no stale quote is "
                    r"ever traded"),
                why(r"so the same spread is pure profit; price competition among providers would push it down toward "
                    r"zero, which is the case for batch auctions")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Check two: batch auctions, in the simulation. <bookmark mark='a'/> In continuous trading, each of five "
            f"firms earns {b['byN'][2]['sniper']:.3f} a unit of time by sniping. <bookmark mark='b'/> In batch auctions, "
            "nothing: quotes are re-set with the current value before each clearing, so no stale quote is ever traded. "
            "<bookmark mark='c'/> At the same spread the provider keeps everything, and competition among providers "
            "would drive the spread down toward zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def fba_logic(self):
        rows = [cmath(r"\text{news before the batch closes}", r"\Rightarrow", r"\text{all firms re-price}", font_size=32),
                cmath(r"\text{many providers}", r"\Rightarrow", r"\text{Bertrand on price}", font_size=36),
                cmath(r"s_{\text{batch}}", r"\to", r"\text{inventory and information costs only}", font_size=34,
                      colors={r"s_{\text{batch}}": GOOD})]
        whys = [why(r"in a batch, the order of messages within the interval is irrelevant: a provider that sees news can "
                    r"update its quote before the auction uses it"),
                why(r"so providers compete by undercutting each other's prices, not by racing"),
                why(r"the sniping term vanishes except for news in the last instant of a batch; what remains is the "
                    r"spread a world without races would have")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The logic of the batch result. <bookmark mark='a'/> Within a batch, the order of messages does not matter: a "
            "provider that sees news updates its quote before the auction uses it. <bookmark mark='b'/> So providers "
            "compete by undercutting each other's prices, not by racing. <bookmark mark='c'/> The sniping term vanishes, "
            "except for news in the last instant of a batch, and what remains is the spread a world without races "
            "would have."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def fba_theorem(self):
        rows = [cmath(r"\Pr(\text{sniped})", r"\approx", r"\frac{\delta}{\tau}", font_size=40, colors={r"\Pr(\text{sniped})": SNIPE_C}),
                cmath(r"\frac{s^*_{\text{batch}}}{2}", r"\approx", r"\frac{\lambda_J J\,\delta/\tau}{\lambda_I + \lambda_J\,\delta/\tau}",
                      font_size=38, colors={r"\frac{s^*_{\text{batch}}}{2}": GOOD}),
                cmath(r"\delta = 1\,\mu\text{s},\ \tau = 100\,\text{ms}", r":", r"\frac{\delta}{\tau} = 10^{-5}", font_size=34)]
        whys = [why(r"with latency $\delta$ and batch interval $\tau$, a jump can catch a stale quote only if it arrives in the "
                    r"last $\delta$ of a batch, when the provider has no time to update"),
                why(r"the same indifference argument with the race probability replaced: the spread scales with "
                    r"$\delta/\tau$"),
                why(r"a microsecond against a tenth of a second: the sniping component falls by five orders of magnitude, "
                    r"and speed below the batch interval is worth almost nothing")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Why, in a formula. <bookmark mark='a'/> With latency delta and batch interval tau, a jump catches a stale "
            "quote only if it lands in the last delta of a batch. <bookmark mark='b'/> The same indifference argument "
            "then gives a spread proportional to delta over tau. <bookmark mark='c'/> A microsecond against a tenth of a "
            "second is ten to the minus five: the sniping component falls by five orders of magnitude, and speed below "
            "the batch interval is worth almost nothing."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def welfare(self, b):
        h = b["s_star"]
        rows = [cmath(r"\text{investors' cost}", r"=", r"\lambda_I\,h^*", font_size=40),
                cmath(r"", r"=", rf"{b['lam_i']:.0f} \times {h:.3f} = {b['lam_i'] * h:.3f}\ \text{{per unit time}}",
                      font_size=36, colors={rf"{b['lam_i'] * h:.3f}\ \text{{per unit time}}": HURDLE}),
                cmath(r"\text{batch}", r"\Rightarrow", r"\text{this cost} \to 0;\ \text{speed spending stops}", font_size=34,
                      colors={r"\text{batch}": GOOD})]
        whys = [why(r"what investors pay in the continuous market: exactly the sniping rents"),
                why(r"in the simulation's parameters"),
                why(r"the batch market returns the rent to investors through narrower spreads, and removes the reason to "
                    r"spend on speed: the welfare gain is the sum of both")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The welfare arithmetic. <bookmark mark='a'/> Investors pay lambda I times the half-spread, exactly the "
            f"sniping rents. <bookmark mark='b'/> In the simulation's parameters, {b['lam_i'] * h:.3f} per unit of time. "
            "<bookmark mark='c'/> A batch market returns that to investors through narrower spreads, and also removes "
            "the reason to spend on speed. The gain is both together."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def arms_formal(self):
        rows = [cmath(r"\text{invest } c", r"\Rightarrow", r"\text{win all races}: \lambda_J (J - \tfrac s2)", font_size=34),
                cmath(r"\text{all invest}", r"\Rightarrow", r"\text{back to } 1/N\ \text{each, minus } c", font_size=34),
                cmath(r"c < \lambda_J (J - \tfrac s2)(1 - \tfrac1N)", r"\Rightarrow", r"\text{everyone invests}", font_size=32,
                      colors={r"\text{everyone invests}": BAD})]
        whys = [why(r"a firm that alone pays $c$ per unit time for a tiny edge wins every race against the rest"),
                why(r"if every firm pays, the races are equal again: each still wins one in $N$ and has paid $c$"),
                why(r"investing is dominant whenever its cost is below the gain from winning the races one would otherwise "
                    r"lose: a prisoner's dilemma, whose total cost $N c$ is borne by the market")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The arms race, formally. <bookmark mark='a'/> A firm that alone pays c per unit of time for a tiny speed "
            "edge wins every race. <bookmark mark='b'/> If every firm pays, the races are equal again, one in N each, and "
            "all have paid c. <bookmark mark='c'/> Investing is the dominant choice whenever its cost is below the races "
            "it would otherwise lose: a prisoner's dilemma whose total cost, N times c, the market bears."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def check_general(self, b):
        g = b["btc"]["gsims"]
        x = np.asarray([s["half"] for s in g], float)
        d = np.asarray([s["lp"] - s["sniper"] for s in g], float)
        cross = float(np.interp(0, d, x))
        top = float(np.ceil(np.abs(d).max()))
        ax_ = axes([0.1, 0.6], [-top, top], x_length=6.4, y_length=4.4, xlabel=r"half-spread $h$, ticks",
                   ylabel=r"$\pi_L - \pi_S$, ticks a second", xticks=[0.1, 0.3, 0.5], yticks=[-top, 0, top],
                   yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.6 + DOWN * 0.2)
        ax = ax_.ax
        c_ = VGroup(curve(ax, x, d, MAKER_C, stroke_width=3), *[Dot(ax.c2p(a, y), radius=0.06, color=MAKER_C)
                                                               for a, y in zip(x, d)])
        root = DashedLine(ax.c2p(b["btc"]["general_half"], -top), ax.c2p(b["btc"]["general_half"], top), color=HURDLE,
                          stroke_width=1.8)
        zero = DashedLine(ax.c2p(0.1, 0), ax.c2p(0.6, 0), color=GREY_B, stroke_width=1.2)
        with self.voiceover(
            "Check three: the general condition, with Bitcoin's own jump sizes. Simulate the market with jumps drawn from "
            "every real mid change and the takers' real rate. <bookmark mark='a'/> The difference between the two roles "
            f"crosses zero at {cross:.2f} of a tick, <bookmark mark='b'/> where the condition, solved directly, puts it: "
            f"{b['btc']['general_half']:.2f}."
        ) as vo:
            self.play(FadeIn(ax_), Create(zero))
            vo.wait_until("a")
            self.play(Create(c_))
            vo.wait_until("b")
            self.play(Create(root))
        self.wait(0.4)
        self.clear_scene()

    def btc(self, b):
        bt = b["btc"]
        rows = [cmath(r"\text{all 100-ms moves}", r":", rf"{bt['lam_all']:.2f}\ \text{{a second}},\ \text{{mean}}\ "
                      rf"{bt['mean_move']:.0f}\ \text{{ticks}}", font_size=32),
                cmath(r"h^*", r"\approx", rf"{bt['general_half']:.2f}\ \text{{tick}}", font_size=40, colors={r"h^*": HURDLE}),
                cmath(r"\text{tick-pinned}", r":", r"h = 0.5", font_size=40, colors={r"\text{tick-pinned}": SPREAD_C})]
        whys = [why(r"every change of Bitcoin's mid between snapshots, with its empirical size distribution, as the jumps"),
                why(rf"the general condition solved with $\lambda_I$ = {bt['lam_i']:.0f} trades a second: close to the "
                    rf"two-point calibration's {bt['half']:.2f}"),
                why(r"the model's sniping spread is below the tick; if it were the only cost, the tick, not sniping, would "
                    r"bind, and the excess would be the rent of Chapter 4")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Check four: Bitcoin. <bookmark mark='a'/> Treat every change of the mid between snapshots as a public jump, "
            f"with its real sizes: {bt['lam_all']:.2f} a second, averaging {bt['mean_move']:.0f} ticks. "
            "<bookmark mark='b'/> Solved against the takers' rate, the general condition gives a half-spread of about "
            f"{bt['general_half']:.2f} of a tick. <bookmark mark='c'/> Below the half tick the tick forces. A crude "
            "calibration, since takers are not all uninformed and not every move is public news, but it says the tick, "
            "not sniping, binds the spread on this market, and Chapter two's losses come from elsewhere: from the "
            "information in the flow."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def related(self):
        cards = VGroup(
            desk_question(r"Budish, Cramton and Shim (2015)", r"the continuous-market model with general jumps, the arms "
                          r"race, and frequent batch auctions; evidence from correlated futures and ETFs", width=12.4,
                          font_size=18),
            desk_question(r"Aquilina, Budish and O'Neill (2022)", r"the races measured message by message on the London "
                          r"Stock Exchange", width=12.4, font_size=18),
            desk_question(r"Baldauf and Mollner (2020); Menkveld and Zoican (2017)", r"how faster exchanges and more "
                          r"competition among makers can widen or narrow spreads once information acquisition is endogenous",
                          width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Where this sits. <bookmark mark='a'/> Budish, Cramton and Shim's paper has general jumps, the arms race, and "
            "batch auctions, with evidence from correlated futures and funds. <bookmark mark='b'/> Aquilina, Budish and "
            "O'Neill measured the races on the London Stock Exchange. <bookmark mark='c'/> And Markus Baldauf and Joshua "
            "Mollner, and Menkveld and Marius Zoican, showed that once acquiring information is a choice, faster markets "
            "can widen spreads or narrow them."
        ) as vo:
            for k_, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: informed and sniping costs together", r"an equilibrium spread with private information, "
                          r"public jumps and inventory at once, estimated on message data", width=12.4, font_size=18),
            desk_question(r"open: competing market designs", r"when continuous and batch markets coexist, where does "
                          r"liquidity go, and is the outcome efficient?", width=12.4, font_size=18),
            desk_question(r"open: crypto's many venues", r"sniping across exchanges with different latencies and no "
                          r"consolidated quote; who wins, and what it costs takers", width=12.4, font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> An equilibrium spread with private information, public jumps and "
            "inventory together, estimated from message data. <bookmark mark='b'/> When continuous and batch markets "
            "coexist, where does liquidity go, and is the result efficient? <bookmark mark='c'/> And sniping across "
            "crypto's many venues, with different latencies and no consolidated quote: who wins, and what does it cost "
            "takers?"
        ) as vo:
            for k_, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k_], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"investors arrive at rate 10, jumps of 3 ticks at rate 2. What is the sniping half-spread? And if "
                       r"jumps are 1 or 5 ticks with equal chance (same mean)?")
        with self.voiceover(
            "Pause and predict. Investors arrive at rate ten and jumps of three ticks at rate two. What is the sniping "
            "half-spread? And if the jumps are one or five ticks with equal chance, the same mean?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
