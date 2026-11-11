from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant37.common import (IMPACT_C, PART, RL_C, TWAP_C, comma, load)


class RL(VoiceoverScene):
    def construct(self):
        r = load("rl")
        self.card(r)
        self.literature()
        self.env(r)
        self.learner(r)
        self.curve_(r)
        self.table(r)
        self.policy(r)
        self.why_not(r)
        self.better()
        self.features()
        self.question()

    def card(self, r):
        c = chapter_card(7, r"A learned executor", r"Can reinforcement learning find a better schedule?", part=PART)
        q, tw = r["res"]["Q-learning"]["mean"], r["res"]["TWAP"]["mean"]
        with self.voiceover(f"""Chapter seven. A fitted queue simulator provides a separate numerical illustration. After sixty thousand training episodes, its learner costs {q:.1f} total half-ticks against {tw:.1f} for TWAP on another simulator random stream. This is a comparison within one model and training seed, with no proof of optimality and no real-market test."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def literature(self):
        cards = VGroup(
            desk_question(r"Nevmyvaka, Feng and Kearns (2006)", r"tabular reinforcement learning on Nasdaq order books, "
                          r"with the time left, the inventory left and book features as the state; it improved on "
                          r"submit-and-leave strategies", width=12.4, font_size=18),
            desk_question(r"deep versions", r"Ning, Lin and Jaimungal (2021), double deep Q-learning; others with policy "
                          r"gradients; gains over TWAP and Almgren--Chriss reported in simulation and backtests",
                          width=12.4, font_size=18),
            desk_question(r"the catch", r"a learner is only as good as the market it practises in: replayed history does "
                          r"not react, and a simulator that misses facts teaches the wrong lesson (Part 36)", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        self.add(cards[0])
        with self.voiceover(
            "The literature. <bookmark mark='a'/> Yuriy Nevmyvaka, Yi Feng and Michael Kearns applied tabular "
            "reinforcement learning to Nasdaq order books in two thousand and six, and improved on simple strategies. "
            "<bookmark mark='b'/> Deep versions followed, such as Brian Ning, Franco Lin and Jaimungal's double deep "
            "Q-learning, with gains over TWAP and Almgren and Chriss reported. <bookmark mark='c'/> The catch: a learner "
            "is only as good as the market it practises in."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def env(self, r):
        rows = [cmath(r"\text{market}", r":", r"\text{Part 36's queue-reactive book}", font_size=36),
                cmath(r"\text{task}", r":", rf"\text{{sell }} {r['inv']}\ \text{{units in }} {r['steps']}\ \text{{steps}}",
                      font_size=36),
                cmath(r"\text{a sale}", r":", r"\text{eats the bid queue; emptied} \Rightarrow \text{mid} - \tfrac12\text{tick}",
                      font_size=30),
                cmath(r"\text{cost}", r"=", r"\textstyle\sum (\text{arrival mid} - \text{price received})", font_size=34,
                      colors={r"\text{cost}": IMPACT_C})]
        whys = [why(r"the House's simulator, fitted to 17 May: queues that grow and shrink at fitted rates"),
                why(rf"each step lets {r['sub']} simulator steps pass; whatever is left at the end is dumped"),
                why(r"a market sell takes the best bid; when that queue is emptied the price falls half a tick, new queues "
                    r"are drawn, and the rest of the order walks on: impact"),
                why(r"implementation shortfall in half-ticks, summed over the parent order")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.5, edge=6.9)
        with self.voiceover(
            "The environment. <bookmark mark='a'/> The market is Part thirty-six's queue-reactive book, fitted to the "
            f"seventeenth of May. <bookmark mark='b'/> The task: sell {r['inv']} units in {r['steps']} steps, with the "
            "rest dumped at the end. <bookmark mark='c'/> A sale eats the bid queue; each time a queue is emptied the "
            "price falls half a tick and the order walks on. That is the impact. <bookmark mark='d'/> The cost is the "
            "implementation shortfall, in half-ticks."
        ) as vo:
            step(0)
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def learner(self, r):
        rows = [cmath(r"s", r"=", r"(\text{step},\ \text{inventory},\ \text{imbalance bucket})", font_size=34),
                cmath(r"a", r"\in", r"\{0, 1, 2, 4\}\ \text{units now}", font_size=36),
                cmath(r"Q(s, a)", r"\leftarrow", r"Q + \alpha\,[r + \max_{a'} Q(s', a') - Q]", font_size=34,
                      colors={r"Q(s, a)": RL_C})]
        whys = [why(r"what the learner sees: how much time and inventory are left, and Part 36's queue imbalance"),
                why(r"what it can do each step"),
                why(rf"Part 8's Q-learning, with exploration that decays over {comma(r['episodes'])} episodes; the "
                    r"reward is minus the cost")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "The learner. <bookmark mark='a'/> It sees the step, the inventory left, and the queue imbalance in three "
            "buckets. <bookmark mark='b'/> Each step it sells nothing, one, two or four units. <bookmark mark='c'/> And "
            "it learns by Part eight's Q-learning, exploring less and less over sixty thousand episodes."
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

    def curve_(self, r):
        c = np.asarray(r["curve"], float)
        ep = (np.arange(len(c)) + 1) * 500 / 1000
        tw = r["res"]["TWAP"]["mean"]
        lo = float(np.floor(min(c.min(), tw) - 2))
        hi = float(np.ceil(c.max() + 2))
        g = axes([0, float(ep[-1])], [lo, hi], x_length=8.4, y_length=4.2, xlabel=r"episodes, thousands",
                 ylabel=r"mean cost, half-ticks", xticks=[0, 20, 40, 60], yticks=[lo, hi], yfmt=lambda v: f"{v:.0f}",
                 font_size=15).move_to(DOWN * 0.2)
        ax = g.ax
        cv = curve(ax, ep, c, RL_C, stroke_width=2.5)
        twl = DashedLine(ax.c2p(0, tw), ax.c2p(ep[-1], tw), color=TWAP_C, stroke_width=2)
        lab = label(r"TWAP", font_size=18, color=TWAP_C).next_to(ax.c2p(ep[-1], tw), UP, buff=0.1).shift(LEFT * 0.4)
        with self.voiceover(
            "The training curve. <bookmark mark='a'/> Each point averages five hundred exploration episodes of the same fitted queue simulator. <bookmark mark='b'/> Costs are noisy and the curve approaches the TWAP reference. Training noise, finite learning and restricted state and actions can all matter. This curve alone does not show that there is nothing useful to learn, certify convergence to an optimum, or compare real-market execution quality."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(cv), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(twl), FadeIn(lab))
        self.wait(0.4)
        self.clear_scene()

    def table(self, r):
        names = ["TWAP", "Q-learning", "front-loaded", "sell when the bid is thin", "dump at once"]
        cols = {"TWAP": TWAP_C, "Q-learning": RL_C}
        hx = [-3.4, 1.0, 3.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"policy", r"mean cost", r"standard deviation")])
        tab = VGroup(head)
        for n in names:
            x = r["res"][n]
            tab.add(VGroup(label(n, font_size=19, color=cols.get(n, GREY_A)),
                           MathTex(f"{x['mean']:.1f} \\pm {x['se']:.1f}", font_size=26, color=cols.get(n, WHITE)),
                           MathTex(f"{x['sd']:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.0 - 0.75 * j, 0])
        foot = wrapped_label('same fitted model, new seed; individual Monte Carlo errors only; total half-ticks including final forced dump',
                             11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        res = r["res"]
        with self.voiceover(
            f"""Evaluation on five thousand episodes per policy, with a new simulator seed but the same fitted model. <bookmark mark='a'/> TWAP costs {res['TWAP']['mean']:.1f}, Q-learning {res['Q-learning']['mean']:.1f}, front-loading {res['front-loaded']['mean']:.1f}, thin-bid selling {res['sell when the bid is thin']['mean']:.1f}, and immediate dumping {res['dump at once']['mean']:.1f} total half-ticks. The plus-minus values are individual Monte Carlo standard errors, not uncertainty in calibration, learning seeds or real-market performance. Reusing one starting seed does not align paths after different state-dependent actions consume different random draws; a paired-difference error is not available here."""
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def policy(self, r):
        s = np.asarray(r["sold"], float)
        n = len(s)
        g = axes([-0.5, n - 0.5], [0, float(np.ceil(s.max() + 0.5))], x_length=8.4, y_length=4.0, xlabel=r"step",
                 ylabel='chosen units per decision; excludes final forced dump', xticks=[0, 5, 10, 15, 19], yticks=[0, 1, 2], font_size=15)
        g.move_to(DOWN * 0.3)
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.3, height=max(1e-3, abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])), fill_color=RL_C,
                                  fill_opacity=0.85, stroke_width=0).move_to(ax.c2p(i, v / 2)) for i, v in enumerate(s)])
        twl = DashedLine(ax.c2p(-0.5, 1), ax.c2p(n - 0.5, 1), color=TWAP_C, stroke_width=1.8)
        with self.voiceover(
            "What the profile records. <bookmark mark='a'/> Bars average the learner's chosen sales at each decision, capped by remaining inventory. The collection code does not add any forced final dump to these bars, although final liquidation is included in evaluation cost. The bar sum can therefore be below the twenty-unit parent order. The plot describes this trained policy's decisions; it does not prove that waiting is costless or the fitted market is conditionally driftless in every state."
        ) as vo:
            self.play(FadeIn(g), Create(twl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in bars], lag_ratio=0.05))
        self.wait(0.4)
        self.clear_scene()

    def why_not(self, r):
        cards = VGroup(
            desk_question('restricted state and finite learning', 'queue resets simplify the model, but imbalance can predict moves; this comparison does not prove TWAP optimal', width=12.4,
                          font_size=19),
            desk_question(r"noise", r"a single episode's cost varies far more than the differences between good "
                          r"policies; tabular learning needs many more episodes, or variance reduction", width=12.4,
                          font_size=19),
            desk_question(r"where learning can help", r"books with memory, signals and resilience (Chapters 3 and 6), "
                          r"where the optimum is not a formula; but only in a simulator that passes Part 36's "
                          r"scorecard", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Interpreting the result. <bookmark mark='a'/> This learner did not beat TWAP in this particular simulator run. A state-dependent queue model may have conditional imbalance drift even when an overall symmetric distribution has zero average drift; queue resets do not establish that no exploitable structure remains. <bookmark mark='b'/> Finite learning, coarse observations, restricted actions and noise are possible explanations; the result does not isolate their causes or prove TWAP near-optimal. <bookmark mark='c'/> Improving state, impact dynamics and evaluation is a research direction requiring fresh authorization for new experiments, not a new market trial performed here."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def better(self):
        cards = VGroup(
            desk_question(r"common random numbers", 'couple common exogenous innovations by time and source; quantify paired differences, since state-dependent draw counts can break seed matching', width=12.4,
                          font_size=19),
            desk_question(r"structure first", r"learn the residual around TWAP or Almgren--Chriss instead of the "
                          r"whole schedule; the learner then needs to find only the deviations that pay", width=12.4,
                          font_size=19),
            desk_question(r"a market that reacts", r"train in a simulator with memory, sweeps and resilience, scored "
                          r"against data, and evaluate out of sample on replayed history with an impact model",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Possible evaluation improvements. <bookmark mark='a'/> Common random numbers require deliberately coupled exogenous innovations, not merely setting the same seed before policies that consume different numbers of draws. Measure the variance of paired differences rather than assuming cancellation. <bookmark mark='b'/> A learner may search residual decisions around a strong analytic baseline. <bookmark mark='c'/> Richer impact dynamics need empirical validation and genuine future-market tests. These are proposals; the current evidence comes only from the unchanged original simulator computation."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def features(self):
        cards = VGroup(
            desk_question(r"what a richer state would add", r"the spread, the recent order-flow imbalance, the microprice's "
                          r"lean and short-term volatility: Part 36's measurements, as inputs", width=12.4, font_size=19),
            desk_question(r"what the reward should be", r"the shortfall against arrival, plus a penalty for risk, so "
                          r"that the learner faces Almgren--Chriss's trade-off rather than a risk-neutral one",
                          width=12.4, font_size=19),
            desk_question(r"what it must be compared with", r"TWAP, the Almgren--Chriss schedule at the same risk, and a "
                          r"simple imbalance rule, on the same random paths", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "Designing a better experiment. <bookmark mark='a'/> A richer state: the spread, the recent imbalance, the "
            "microprice's lean, and short-term volatility. <bookmark mark='b'/> A reward with a risk penalty, so the "
            "learner faces Almgren and Chriss's trade-off. <bookmark mark='c'/> And comparisons on the same random paths "
            "with TWAP, with Almgren and Chriss at the same risk, and with a simple imbalance rule."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        head = label('8. A VWAP hour', font_size=30, color=QC.IDEA).to_edge(UP, buff=0.45)
        given = wrapped_label('Expected hourly volume share $7.5\\%$; parent quantity $1{,}000$ BTC.', 12.0, 29).move_to(UP * 0.65)
        task = wrapped_label('Compute the planned hourly quantity. Is realized participation guaranteed constant?', 12.0, 27, QC.IDEA).move_to(DOWN * 1.3)
        foot = note("Pause: work the units and assumptions; full solution in the notes.", font_size=18, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover('Quantitative pause eight. A VWAP plan allocates a thousand bitcoin according to an expected volume curve. One hour has seven point five percent expected share. Find the planned quantity and explain why forecast errors can change realized participation.'):
            self.play(FadeIn(head), FadeIn(given), FadeIn(task), FadeIn(foot))
        self.wait(6)
        self.clear_scene()
