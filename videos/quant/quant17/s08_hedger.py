from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from explainer.quant.house import deep as D
from videos.quant.quant17.common import (BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, house_lab, illustration, load,
                                         step_xy)


class Hedger(VoiceoverScene):
    def construct(self):
        h = load("hedge")
        r = load("hedge_replay")
        self.card()
        self.framework(h)
        self.derive(h)
        self.replay(h, r)
        self.live(r)
        self.lab(h)

    def card(self):
        c = chapter_card(11, r"The deep hedger", r"What if the hedge is learned, not derived?", lit=(2019,), part=PART)
        with self.voiceover("Chapter eleven. The deep hedger, part one: the objective."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def framework(self, h):
        rows = [cmath(r"\delta_k", r"=", r"\text{network}\big(\log S_k/K,\ \tau_k,\ \delta_{k-1}\big)", font_size=38,
                      colors={r"\delta_k": NET}),
                cmath(r"X", r"=", r"-(S_T - K)^+ + \sum_k \delta_k\,(S_{k+1} - S_k) - c\sum_k |\delta_k - \delta_{k-1}|\,S_k",
                      font_size=32, colors={r"X": OPT}),
                cmath(r"\min_\theta", r"\ ", r"\rho(X) = \tfrac{1}{\gamma}\log \mathbb{E}\,e^{-\gamma X}", font_size=38,
                      colors={r"\min_\theta": GOOD})]
        whys = [why(r"Buehler, Gonon, Teichmann and Wood (2019): at each rebalancing date a network chooses the holding from "
                    r"the price, the time left and the holding it already has; nothing about Greeks or formulas"),
                why(r"the seller's profit and loss on a short call: the payoff paid, the hedge's gains, and a proportional cost "
                    r"$c$ on every initial/subsequent trade; zero rates, zero initial stock, no terminal unwind charge"),
                why(r"minimize a risk measure of that profit and loss over simulated paths. Here the entropic one, "
                    r"exponential utility's certainty equivalent; with CVaR the method is the same. The minimum is the "
                    r"with-claim cash requirement only when the relevant population risk is finite; indifference also subtracts the no-claim optimum")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-0.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "A semi-recurrent MLP chooses holdings from current price, remaining time and previous holding. This unrestricted architecture is not supplied delta; the band architecture later is delta-centred. <bookmark mark='a'/> The saved profit and loss starts with zero cash and stock, charges initial and later trades, and includes no separate terminal unwind fee. <bookmark mark='b'/> The formal entropic objective requires a finite exponential loss moment. Finite-path log-sum-exp estimates do not prove that condition. In particular, a discretely underhedged call with lognormal terminal tails can have infinite population entropic risk despite a finite simulation estimate. Read the recorded numbers as empirical objectives; an indifference price additionally requires optimizing and subtracting the no-claim baseline under the same assumptions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def derive(self, h):
        n = h["nocost"]
        bsp, sd = n["bs_price"], n["bs_eval"]["sd_pnl"]
        approx = bsp + 0.5 * sd ** 2
        lo_, hi_ = sorted([n["eval"]["price"], n["bs_eval"]["price"]])
        rows = [cmath(r"\rho(X + c)", r"=", r"\tfrac1\gamma \log \mathbb{E}\,e^{-\gamma X} e^{-\gamma c} = \rho(X) - c",
                      font_size=38, colors={r"\rho(X + c)": GOOD}),
                cmath(r"p", r"=", r"\inf_\delta \rho\big(-Z + (\delta\cdot S)_T - C_T(\delta)\big) - \inf_\delta "
                      r"\rho\big((\delta\cdot S)_T - C_T(\delta)\big)", font_size=34, colors={r"p": OPT}),
                cmath(r"\rho(X)", r"\approx", r"-\mathbb{E}X + \tfrac{\gamma}{2}\operatorname{Var} X", font_size=38,
                      colors={r"\rho(X)": GOOD}),
                cmath(r"\text{moment proxy}", r"=", rf"{bsp:.3f} + \tfrac12 \times {sd:.3f}^2 = {approx:.3f}", font_size=38,
                      colors={r"p": OPT})]
        whys = [why(r"cash invariance: pull $e^{-\gamma c}$ out of the expectation. Adding cash $c$ to a position lowers "
                    r"its risk by exactly $c$; the measure is also monotone and convex"),
                why(r"so the risk with the option, minus the risk without it, is the cash that makes the seller "
                    r"indifferent: Hodges and Neuberger's (1989) indifference price. With a martingale stock and no "
                    r"option the best trade is none, and the second term is 0"),
                why(r"only with suitable exponential moments near zero does a small-$\gamma$ cumulant expansion justify the "
                    r"expected loss plus variance correction; finite ordinary moments alone do not suffice"),
                why(rf"no costs, zero drift: the expected loss of a delta-hedged short call is the Black--Scholes price, and "
                    rf"its variance is the error of hedging once a day (sd {sd:.3f}). Empirical objectives, network and delta: {lo_:.3f} to "
                    rf"{hi_:.3f}")]
        step = ladder(self, rows, whys, keep=3, top=3.1, x=-0.6, buff=0.45, edge=6.9)
        with self.voiceover(
            f"For a finite entropic risk, adding sure cash lowers risk by that cash amount. <bookmark mark='a'/> A seller's indifference premium subtracts the optimized no-claim risk from the optimized with-claim risk. Under martingale prices, integrable gains, nonnegative costs and an admissible zero policy, the no-claim optimum is zero. Under drift it generally is not. <bookmark mark='b'/> A small-risk-aversion cumulant expansion also requires exponential-moment control; it is not justified by finite variance alone. <bookmark mark='c'/> The displayed value {approx:.3f} inserts the Black–Scholes mean and the recorded delta-hedge variance with risk aversion one. It is a second-moment proxy, not a bound or a verified approximation to population exponential risk. The two reported empirical objectives are {lo_:.3f} and {hi_:.3f}; neither proves global optimization or a universal daily-rebalancing premium."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, h, r):
        S = np.asarray(r["S"])
        bsd = np.asarray(r["bs_delta"])
        ck = r["ck_nocost"]
        runs = np.array([r[f"nocost_{s}"]["curve"] for s in range(3)])
        steps = np.arange(runs.shape[1], dtype=float)
        snaps = r["nocost_0"]["snaps"]
        show = [0, 10, 30, 60, 100, 200, 400, 800]
        yr = data_range(bsd, *[snaps[str(i)] for i in show])

        def frame(i):
            g = axes([S[0], S[-1]], yr, x_length=5.0, y_length=3.6, xlabel=r"price, 15 days to expiry",
                     ylabel=r"shares held", xticks=[90, 100, 110], yticks=[0, 0.5, 1], font_size=13)
            y = np.asarray(snaps[str(show[i])])
            dev = float(np.max(np.abs(np.asarray(snaps[str(show[i])]) - bsd)))
            return VGroup(g, DashedVMobject(curve(g.ax, S, bsd, REF, stroke_width=2.5), num_dashes=36),
                          curve(g.ax, S, y, NET, stroke_width=4),
                          label(rf"step {show[i]}: largest gap {dev:.2f} shares", font_size=17,
                                color=NET).next_to(g, DOWN, buff=0.12))
        rp = TrainingReplay(steps, runs, frame, checkpoints=show,
                            ylabel=r"empirical exponential-loss objective")
        bs_price = h["nocost"]["bs_eval"]["price"]
        line = DashedLine(rp.ax.c2p(0, bs_price), rp.ax.c2p(steps[-1], bs_price), stroke_color=REF, stroke_width=2) \
            if rp.lo < bs_price < rp.hi else VGroup()
        ev = [r[f"nocost_{s}"]["eval"]["price"] for s in range(3)]
        leg = legend([(REF, r"Black--Scholes delta (left), delta hedge's empirical objective (right)"),
                      (NET, r"seed 0 holding; three-seed min--max, not a confidence band")], font_size=16).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.35)
        src = illustration(r"no costs; 800 steps of 2{,}048 fresh paths each; a 30-day at-the-money call, 20\% volatility")
        with self.voiceover(
            f"The no-cost replay uses an unrestricted MLP. Black–Scholes delta is a continuous-time replication reference, not a theorem of optimality for a daily empirical exponential objective. The left panel retains every saved holding, including values outside zero to one. The right retains the full batch-loss range from three seeds. <bookmark mark='a'/> These runs approach the delta reference and finish with empirical evaluation objectives from {min(ev):.3f} to {max(ev):.3f}. The seed range is descriptive, and the batch loss is not a confidence band for population risk. Similar holdings in this experiment do not certify the optimizer or the unobserved tails."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(line), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 5))
        self.wait(0.4)
        self.clear_scene()

    def live(self, r):
        L = r["live"]
        Sx = np.asarray(L["S"])
        hn, hd = np.asarray(L["net"]), np.asarray(L["delta"])
        n = len(hn)
        t = np.arange(n + 1)
        top = axes([0, n], [Sx.min() - 1, Sx.max() + 1], x_length=7.2, y_length=1.7, ylabel=r"price", xticks=[],
                   yticks=[round(Sx.min()), round(Sx.max())], font_size=13)
        bot = axes([0, n], data_range(hn, hd, [0, 1]), x_length=7.2, y_length=3.4, xlabel=r"trading day", ylabel=r"shares held",
                   xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1], font_size=13)
        VGroup(top, bot).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(LEFT, buff=0.7)
        tr = ValueTracker(1)

        def stepl(hh, col, w):
            def f():
                k = int(tr.get_value())
                xs, ys = step_xy(t[:k + 1], hh[:k])
                return VMobject(stroke_color=col, stroke_width=w).set_points_as_corners(
                    [bot.ax.c2p(a, b) for a, b in zip(xs, ys)])
            return f
        price = always_redraw(lambda: curve(top.ax, t[:int(tr.get_value()) + 1], Sx[:int(tr.get_value()) + 1], REF,
                                            stroke_width=2.5))
        a = always_redraw(stepl(hd, DELTA, 6))
        b = always_redraw(stepl(hn, NET, 2.5))
        gap = float(np.max(np.abs(hn - hd)))
        side = VGroup(legend([(DELTA, r"Black--Scholes delta"), (NET, r"the trained network")], font_size=17),
                      wrapped_label(rf"one fresh path, 30 rebalances: the two holdings never differ by more than "
                                    rf"{gap:.3f} shares", 4.2, 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35
                                                                                    ).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "And on a single fresh path, rebalance by rebalance: the delta in yellow, the network in purple, drawn on "
            "top. <bookmark mark='a'/> They move together, day after day, up when the price rises, down when it falls. "
            f"The largest gap on this path is {gap:.3f} shares."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(side[0]))
            self.add(price, a, b)
            vo.wait_until("a")
            self.play(tr.animate.set_value(n), run_time=6, rate_func=linear)
            for m in (price, a, b):
                m.clear_updaters()
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def lab(self, h):
        card = house_lab(r"the profit and loss of any hedge", D.hedge_pnl, "for k in range(steps):", 9)
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.6)
        n = h["nocost"]
        ev, bsd = n["eval"], n["bs_eval"]
        outs = [f"network: empirical rho {ev['price']:.3f}   CVaR50 {ev['cvar50']:.3f}   sd {ev['sd_pnl']:.3f}",
                f"delta:   empirical rho {bsd['price']:.3f}   CVaR50 {bsd['cvar50']:.3f}   sd {bsd['sd_pnl']:.3f}"]
        with self.voiceover(
            "Everything rests on one House function: the profit and loss of a short option under any policy, a "
            "network, a formula or a band. Ask for a holding, pay the trade's cost, collect the stock's gain, pay the "
            "payoff. <bookmark mark='a'/> The trained network and the delta, on two hundred thousand fresh paths."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs)
        q = ask(r"which continuous replication component is risk-aversion independent, and what can change on a daily grid?")
        with self.voiceover(
            'Before the next chapter: distinguish the continuous complete-market replication component from a discretely optimized hedge. The replication component does not depend on risk aversion; a daily-grid utility optimum can, because residual risk remains. A drift can also introduce an investment overlay and a nonzero no-claim baseline.'
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
