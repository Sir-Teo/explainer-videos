from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant42.common import (BAD, COLL_C, COMP_C, GOOD, HURDLE, LEARN_C, PART, REAL_C, SHARE_C, SIM_C,
                                         fit_right, load)


class Learning(VoiceoverScene):
    def construct(self):
        m = load("maker")
        self.card(m)
        self.uses()
        self.mdp()
        self.session(m)
        self.fixed(m)
        self.learned(m)
        self.learn_curve(m)
        self.model_based()
        self.policy(m)
        self.cross(m)
        self.replay(m)
        self.offline()
        self.deep()
        self.question()

    def card(self, m):
        cx = m["cross"]
        best = max(m["fixed"]["0.3"], key=lambda x: x["mean"])
        e30, h30, b30 = cx["0.05"]["0.3"]["mean"], cx["0.3"]["0.3"]["mean"], best["mean"]
        c = chapter_card(4, r"Learning to trade", r"What does a learning agent learn, and from which world?", part=PART)
        with self.voiceover(
            "Chapter four, and the answer to the pause: it still makes money, and in this market the world it trained in "
            f"barely matters. Trained where five percent are informed, it earns {e30:.0f} per "
            f"session where thirty percent are; one trained there earns {h30:.0f}. What both lack "
            f"is experience: the best of eight fixed rules earns {b30:.0f}."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def uses(self):
        cards = VGroup(
            desk_question(r"hedging", r"Part 17's deep hedging: a network learns the hedge that minimises a risk measure "
                          r"of the P\&L, with costs, in simulated paths", width=12.4, font_size=19),
            desk_question(r"execution", r"Part 37's queue executor (after Nevmyvaka, Feng and Kearns 2006): where to "
                          r"place an order, step by step", width=12.4, font_size=19),
            desk_question(r"market making and allocation", r"quotes as actions and inventory as state (Spooner et al. "
                          r"2018), or portfolio weights as actions; Hambly, Xu and Yang (2023) survey them", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Reinforcement learning in finance, so far in this series. <bookmark mark='a'/> Hedging: Part seventeen's "
            "deep hedging, learned on simulated paths. <bookmark mark='b'/> Execution: Part thirty-seven's queue "
            "executor. <bookmark mark='c'/> And market making and allocation: quotes or weights as actions, inventory or "
            "holdings as the state. Ben Hambly, Renyuan Xu and Huining Yang survey all four. Each needs an environment "
            "to learn in, and every environment is a simulator."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def mdp(self):
        rows = [cmath(r"\text{state}", r":", r"(\text{inventory},\ \text{last trade's side})", font_size=38,
                      colors={r"\text{state}": LEARN_C}),
                cmath(r"\text{action}", r":", r"(h, s) \in \{1, 2, 3, 4\} \times \{0, 1\}", font_size=40,
                      colors={r"\text{action}": LEARN_C}),
                cmath(r"\text{reward}", r":", r"\text{spread earned} + \text{inventory} \times \Delta v - \gamma\,\text{inventory}^2",
                      font_size=34),
                cmath(r"\text{learning}", r":", r"\text{Q-learning, 24{,}000 sessions of 400 steps}", font_size=36)]
        whys = [why(r"thirty-nine states: inventory from $-6$ to $+6$, and whether the last trader bought, sold or did not "
                    r"trade"),
                why(r"a half-spread in ticks, and whether to skew both quotes against the inventory"),
                why(r"the spread earned against the true value, the inventory marked to it, and a charge for risk"),
                why(r"Part 8's tabular update; then each learned policy is scored on fresh sessions it never saw")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The market maker as a learning problem, in Chapter three's dealer market. <bookmark mark='a'/> It sees its "
            "inventory and the side of the last trade. <bookmark mark='b'/> It chooses a half-spread and whether to skew "
            "its quotes against its inventory. <bookmark mark='c'/> It is paid the spread it earns against the true "
            "value, plus its inventory's change in value, less a charge for risk. <bookmark mark='d'/> And it learns by "
            "Q-learning over twenty-four thousand sessions, then is scored on fresh ones."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def session(self, m):
        p = m["path"]
        v = np.asarray(p["v"], float)
        mid = np.asarray(p["mid"], float)
        inv = np.asarray(p["inv"], float)
        side = np.asarray(p["side"], int)
        t = np.arange(len(v))
        lo, hi = float(min(v.min(), mid.min()) - 2), float(max(v.max(), mid.max()) + 2)
        g1 = axes([0, len(v)], [lo, hi], x_length=11.6, y_length=2.6, xlabel=r"", ylabel=r"ticks: value and the maker's mid",
                  xticks=[], yticks=[], font_size=14).move_to(UP * 1.4)
        g2 = axes([0, len(v)], [-6.5, 6.5], x_length=11.6, y_length=2.0, xlabel=r"one 400-step session, half-spread 3, skewed",
                  ylabel=r"inventory", xticks=[], yticks=[-6, 0, 6], font_size=14).move_to(DOWN * 1.8)
        lv = curve(g1.ax, t, v, REAL_C, stroke_width=2.5)
        lm = curve(g1.ax, t, mid, LEARN_C, stroke_width=2)
        li = curve(g2.ax, t, inv, HURDLE, stroke_width=2)
        n_tr = int(np.sum(side != 0))
        leg = legend([(REAL_C, r"value, seen by the informed"), (LEARN_C, r"the maker's mid")], font_size=15).to_corner(UR, buff=0.35)
        with self.voiceover(
            "One session, under the best fixed rule. <bookmark mark='a'/> The value wanders a tick at a time; the "
            "maker never sees it, only the trades. <bookmark mark='b'/> Its mid follows the flow, lagging the value, "
            "and every gap between them is an opportunity for the informed. <bookmark mark='c'/> Its inventory "
            f"swings, and the skew pulls it back toward zero. {n_tr} trades in four hundred steps."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lv), run_time=2)
            vo.wait_until("b")
            self.play(Create(lm), run_time=2)
            vo.wait_until("c")
            self.play(Create(li), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def fixed(self, m):
        rows = m["fixed"]["0.15"]
        g = axes([0.5, 4.5], [-30, 200], x_length=7.4, y_length=4.2, xlabel=r"half-spread, ticks",
                 ylabel=r"mean P\&L per session, 15\% informed", xticks=[1, 2, 3, 4], yticks=[0, 100, 200],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for x in rows:
            off = -0.17 if x["skew"] == 0 else 0.17
            col = GREY_B if x["skew"] == 0 else COMP_C
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, x["mean"])[1]
            b = Rectangle(width=0.3 * ax.x_length / 4, height=max(abs(y1 - y0), 0.02), stroke_width=0, fill_color=col,
                          fill_opacity=0.85)
            b.move_to([ax.c2p(x["half"] + off, 0)[0], (y0 + y1) / 2, 0])
            bars.add(b)
        leg = legend([(GREY_B, r"no skew"), (COMP_C, r"skewed against inventory")], font_size=17)
        side = VGroup(leg).next_to(g, RIGHT, buff=0.4)
        fit_right(side)
        best = max(rows, key=lambda x: x["mean"])
        with self.voiceover(
            "First, every fixed rule, where fifteen percent of traders are informed. <bookmark mark='a'/> A one-tick "
            "half-spread barely pays: the informed pick it off. Four ticks drives the noise traders away. "
            f"<bookmark mark='b'/> The best is {best['half']} ticks, skewed, at {best['mean']:.0f} per session. And "
            "skewing against inventory roughly doubles the profit of every width: unloading risk matters as much as the "
            "spread."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bars], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(bars[[i for i, x in enumerate(rows) if x is best][0]], color=GOOD))
        self.wait(0.4)
        self.clear_scene()

    def learned(self, m):
        heads = [r"", r"5\% informed", r"15\%", r"30\%"]
        best = {pi: max(m["fixed"][pi], key=lambda x: x["mean"]) for pi in ("0.05", "0.15", "0.3")}
        body = [[r"best fixed rule"] + [rf"{best[p]['mean']:.0f}" for p in ("0.05", "0.15", "0.3")],
                [r"learner trained at 5\%"] + [rf"{m['cross']['0.05'][p]['mean']:.0f}" for p in ("0.05", "0.15", "0.3")],
                [r"learner trained at 30\%"] + [rf"{m['cross']['0.3'][p]['mean']:.0f}" for p in ("0.05", "0.15", "0.3")]]
        cols = [COMP_C, LEARN_C, SIM_C]
        tab = VGroup(VGroup(*[label(h_, font_size=20, color=QC.IDEA) for h_ in heads]))
        for i, row in enumerate(body):
            tab.add(VGroup(*[label(c_, font_size=21, color=cols[i] if j == 0 else WHITE) for j, c_ in enumerate(row)]))
        xs = [-3.8, 0.6, 2.8, 5.0]
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([xs[i], 1.6 - 0.85 * j, 0])
            if len(row[0].get_all_points()):  # an empty header cell has no points to align
                row[0].align_to(np.array([-6.3, 0, 0]), LEFT)
        note_ = label(r"mean P\&L per 400-step session, scored on fresh sessions", font_size=16, color=GREY_B
                      ).to_edge(DOWN, buff=0.6)
        g5 = m["cross"]["0.05"]["0.05"]["mean"]
        b05 = best["0.05"]["mean"]
        share = 100 * g5 / b05
        h30, e30 = m["cross"]["0.3"]["0.3"]["mean"], m["cross"]["0.05"]["0.3"]["mean"]
        with self.voiceover(
            "Now the learners. <bookmark mark='a'/> The best fixed rule, found by trying all eight, in each market. "
            "<bookmark mark='b'/> The learner trained where five percent are informed: in its own market it earns "
            f"{g5:.0f}, about {share:.0f} percent of the best rule's {b05:.0f}. Nine and a half million "
            "steps of trial and error get close to, but not past, a search over eight simple rules. "
            "<bookmark mark='c'/> And the learner trained in the hard market. Compare down the last column: "
            f"{h30:.0f} against {e30:.0f}, the same within noise. Training in the right world did not help, and, as the "
            "next chart shows, neither does simply training for longer."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_))
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def learn_curve(self, m):
        cv = m["curve"]
        ep = np.array([x["episodes"] for x in cv], float)
        mu = np.array([x["mean"] for x in cv], float)
        se = np.array([x["se"] for x in cv], float)
        best = max(x["mean"] for x in m["fixed"]["0.05"])
        lx = np.log10(ep)
        g = axes([2.6, 4.5], [min(0.0, float(mu.min()) - 10), best * 1.15], x_length=7.4, y_length=4.2,
                 xlabel=r"sessions of training (log scale)", ylabel=r"P\&L per fresh session, 5\% informed",
                 xticks=[3, 4], yticks=[0, 100, 200], xfmt=lambda u: {3: r"1{,}000", 4: r"10{,}000"}[int(u)],
                 font_size=15).move_to(LEFT * 1.3 + DOWN * 0.2)
        ax = g.ax
        bd = band(ax, lx, mu - 2 * se, mu + 2 * se, LEARN_C, opacity=0.2)
        ln = curve(ax, lx, mu, LEARN_C, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.06, color=LEARN_C) for a_, b_ in zip(lx, mu)])
        bl = DashedLine(ax.c2p(2.6, best), ax.c2p(4.5, best), color=COMP_C, stroke_width=2)
        bl_l = label(rf"best fixed rule, {best:.0f}", font_size=16, color=COMP_C).next_to(ax.c2p(2.7, best), UP, buff=0.08,
                                                                                   aligned_edge=LEFT)
        first, last = mu[0], mu[-1]
        i_lo = int(np.argmin(mu))
        low, ep_low = mu[i_lo], ep[i_lo]
        with self.voiceover(
            "How the learning goes, scoring the greedy policy on fresh sessions as training proceeds. "
            f"<bookmark mark='a'/> After only five hundred sessions it already earns {first:.0f}: the spread and the "
            f"skew are learned early. <bookmark mark='b'/> Then it does not settle. As rarely visited states are revised, "
            f"its earnings swing, down to {low:.0f} after {ep_low:,.0f} sessions, <bookmark mark='c'/> and back to "
            f"{last:.0f} at the end, never reaching the best fixed rule's {best:.0f}. Tabular learning with a constant "
            "step size, in a market this noisy, wanders rather than converges: one more reason the House scores a "
            "learner on fresh data, at the moment it would be deployed."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bl), FadeIn(bl_l))
            vo.wait_until("a")
            self.play(FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(FadeIn(bd), Create(ln), FadeIn(dots[1:]), run_time=2)
            vo.wait_until("c")
            self.play(Indicate(dots[-1], color=HURDLE, scale_factor=1.8))
        self.wait(0.4)
        self.clear_scene()

    def model_based(self):
        rows = [cmath(r"\delta^*", r"\approx", r"\frac1k + \text{adverse selection} + \text{inventory}", font_size=40,
                      colors={r"\delta^*": COMP_C}),
                cmath(r"k = 0.5", r"\Rightarrow", r"\tfrac1k = 2 \text{ ticks, before the informed}", font_size=38),
                cmath(r"\text{model-free}", r":", r"\text{the same answer, from millions of trades}", font_size=38,
                      colors={r"\text{model-free}": LEARN_C})]
        whys = [why(r"Part 38's Avellaneda--Stoikov and GLFT quotes: with an exponential fill law, the spread that "
                    r"maximises income is $1/k$, widened for adverse selection and inventory risk"),
                why(r"this market's noise traders; the informed push the best fixed rule out to three"),
                why(r"a learner that is told nothing must discover all of this from experience: model-based methods are "
                    r"far more efficient when the model is right, and learning earns its keep when it is not")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Why a fixed rule can beat a learner. <bookmark mark='a'/> Part thirty-eight derived the optimal quotes: "
            "with an exponential fill law, the spread that maximises income is one over k, widened for adverse "
            "selection and inventory. <bookmark mark='b'/> Here that is two ticks before the informed, and their "
            "presence pushes the best rule to three. <bookmark mark='c'/> A learner told nothing must discover all of "
            "this from millions of trades. Model-based methods win when the model is right; learning earns its keep "
            "only when it is not."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def policy(self, m):
        grid = m["grid"]
        inv = np.array([x["inv"] for x in grid])
        half = np.array([x["half"] for x in grid])
        skew = np.array([x["skew"] for x in grid])
        g = axes([-6.5, 6.5], [0, 4.5], x_length=8.4, y_length=3.8, xlabel=r"inventory",
                 ylabel=r"half-spread chosen, ticks", xticks=[-6, -3, 0, 3, 6], yticks=[1, 2, 3, 4], font_size=15
                 ).move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i_, h_, s_ in zip(inv, half, skew):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, h_)[1]
            b = Rectangle(width=0.45, height=y1 - y0, stroke_width=0, fill_color=COMP_C if s_ else GREY_B, fill_opacity=0.85)
            b.move_to([ax.c2p(i_, 0)[0], (y0 + y1) / 2, 0])
            bars.add(b)
        leg = legend([(COMP_C, r"skewed"), (GREY_B, r"not skewed")], font_size=16).to_corner(UR, buff=0.5)
        with self.voiceover(
            "What the learner trained in the easy market chose, by inventory, after a quiet step. "
            "<bookmark mark='a'/> Near flat, it quotes two to four ticks. <bookmark mark='b'/> Carrying inventory either "
            "way, it mostly skews and narrows, quoting tight on the side that unloads its risk. But neighbouring cells "
            "disagree: states visited too rarely to learn well, which is the price of learning from experience in a "
            "noisy market, and why it trails the best fixed rule."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.08), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(VGroup(bars[0], bars[-1]), color=HURDLE))
        self.wait(0.4)
        self.clear_scene()

    def cross(self, m):
        cx = m["cross"]
        rows = [cmath(r"\text{trained at } 5\%", r"\to", rf"{cx['0.05']['0.3']['mean']:.0f}\ \text{{at }} 30\%,\ "
                      rf"\text{{half-spread }} {cx['0.05']['0.3']['half']:.2f}", font_size=36,
                      colors={r"\text{trained at } 5\%": LEARN_C}),
                cmath(r"\text{trained at } 30\%", r"\to", rf"{cx['0.3']['0.3']['mean']:.0f}\ \text{{at }} 30\%,\ "
                      rf"\text{{half-spread }} {cx['0.3']['0.3']['half']:.2f}", font_size=36,
                      colors={r"\text{trained at } 30\%": SIM_C}),
                cmath(r"\Rightarrow", r"", r"\text{here, experience mattered more than the regime}", font_size=36)]
        whys = [why(r"its quotes, set in the easy market, average about three ticks"),
                why(r"trained among more informed traders, it quotes tighter on average, not wider: noise in learning, "
                    r"not a lesson about the market"),
                why(r"a regime change is a new environment, and nothing in a policy says which one it was built for; "
                    r"but a learner that has not converged cannot be told apart from one that learned the wrong world")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "The regime change, in detail. <bookmark mark='a'/> The easy-market learner quotes about three ticks on "
            "average. <bookmark mark='b'/> The hard-market learner quotes tighter, not wider, which no theory of the "
            "market would advise: that is noise in learning. <bookmark mark='c'/> So the honest conclusion is narrower "
            "than the usual story. A regime change is a new environment, but a learner that has not converged cannot be "
            "told apart from one that learned the wrong world."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def replay(self, m):
        rp = m["replay"]
        vals = [(r"half-spread 2, live", rp["live2"], COMP_C), (r"half-spread 4, replayed on 2's tape", rp["naive4"], BAD),
                (r"half-spread 4, live", rp["live4"], LEARN_C)]
        mx = max(v for _, v, _ in vals) * 1.1
        bars = VGroup()
        for i, (nm, v, col) in enumerate(vals):
            w = 8.0 * v / mx
            b = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-4.0 + w / 2, 1.2 - 1.2 * i, 0])
            t = label(nm, font_size=19, color=GREY_A).next_to(b, UP, buff=0.08).align_to(b, LEFT)
            n = label(rf"{v:.0f}", font_size=20).next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(b, t, n))
        with self.voiceover(
            "And why a backtest is not an environment. Record a session of the two-tick rule: who traded, and when. "
            f"<bookmark mark='a'/> Live, it earns {rp['live2']:.0f}. <bookmark mark='b'/> Now evaluate a four-tick rule "
            "on that tape, the usual way: same trades, two ticks better each. It looks worth "
            f"{rp['naive4']:.0f}. <bookmark mark='c'/> Run it live and it earns {rp['live4']:.0f}, less than the "
            "two-tick rule, because wider quotes drive the noise traders away. The tape recorded who traded with the "
            "old quotes, not who would have traded with the new ones."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(bars[k], shift=RIGHT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def offline(self):
        rows = [cmath(r"\text{the data}", r":", r"\text{actions the old policy took, and what followed}", font_size=36,
                      colors={r"\text{the data}": REAL_C}),
                cmath(r"\text{the question}", r":", r"\text{what would a new policy have earned?}", font_size=38,
                      colors={r"\text{the question}": LEARN_C}),
                cmath(r"\hat V(\pi)", r"=", r"\textstyle\frac1n\sum_t \frac{\pi(a_t \mid s_t)}{\pi_0(a_t \mid s_t)}\, r_t", font_size=38),
                cmath(r"\pi_0(a \mid s) = 0", r"\Rightarrow", r"\text{no estimate at all}", font_size=38, colors={r"\Rightarrow": BAD})]
        whys = [why(r"offline reinforcement learning (Levine et al. 2020): learning from a fixed log, with no new experiments"),
                why(r"off-policy evaluation"),
                why(r"importance weighting corrects for the change of policy, if the old one sometimes took each action"),
                why(r"a market maker that always quoted two ticks says nothing about four: the replay above invented the "
                    r"answer")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The general problem has a name: offline reinforcement learning. <bookmark mark='a'/> The data are the "
            "actions an old policy took and what followed. <bookmark mark='b'/> The question is what a new policy would "
            "have earned. <bookmark mark='c'/> Importance weighting answers it, reweighting each step by how much more "
            "or less likely the new policy was to act that way. <bookmark mark='d'/> But only if the old policy ever "
            "took the new action. A market maker that always quoted two ticks says nothing about four; the replay simply "
            "invented the answer."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def deep(self):
        cards = VGroup(
            desk_question(r"deep reinforcement learning", r"replace the table by a network (DQN) or learn the policy "
                          r"directly (policy gradients, PPO): states too many to list, such as a whole order book",
                          width=12.4, font_size=19),
            desk_question(r"what it does not fix", r"sample efficiency, the simulator's assumptions and the "
                          r"counterfactual; a network can also overfit the simulator's quirks more thoroughly", width=12.4,
                          font_size=19),
            desk_question(r"why a table here", r"thirty-nine states can be printed and read, so the House can see what "
                          r"was learned, not only how much it earned", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Why a table, when the field uses deep networks? <bookmark mark='a'/> Deep reinforcement learning replaces "
            "the table by a network, or learns the policy directly, so that states too numerous to list, like a whole "
            "order book, can be handled. <bookmark mark='b'/> It does not fix the sample efficiency, the simulator's "
            "assumptions or the missing counterfactual, and a network can overfit a simulator's quirks more thoroughly. "
            "<bookmark mark='c'/> Thirty-nine states can be printed and read, so the House can see what was learned, "
            "not only what it earned."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"language models read news and write trading plans. What is the hardest problem in testing one on "
                       r"historical data?")
        with self.voiceover(
            "Pause and predict. Language models read the news and write trading plans. What is the hardest problem in "
            "testing one on historical data?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
