from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, DELTA, GOOD, NET, OPT, PART, REF, ask, illustration, load


def _avg(rm, risk, key):
    return float(np.mean([rm["runs"][f"{risk}_{s}"][key] for s in (0, 1, 2)]))


class Drift(VoiceoverScene):
    def construct(self):
        rm = load("risk_measures")
        d = load("drift")
        self.card()
        self.cvar_derive()
        self.cvar(rm)
        self.merton(d)
        self.replay(d)
        self.twist(d)
        self.cards()

    def card(self):
        c = chapter_card(12, r"Risk measures and the drift trap", r"What does the hedger optimize, and under which "
                         r"probabilities?", part=PART)
        with self.voiceover("Chapter twelve. The deep hedger, part two: risk measures, and the drift trap."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def cvar_derive(self):
        rows = [cmath(r"\mathrm{CVaR}_\alpha(L)", r"=", r"\min_w \Big\{ w + \tfrac1\alpha\,\mathbb{E}(L - w)^+ \Big\}",
                      font_size=40, colors={r"\mathrm{CVaR}_\alpha(L)": BAD}),
                cmath(r"0\in\partial_w", r":\ ", r"\mathbb P(L>w)\le\alpha\le\mathbb P(L\ge w),\quad 0<\alpha<1",
                      font_size=38, colors={r"\partial_w": GOOD})]
        whys = [why(r"Rockafellar and Uryasev (2000): the expected loss in the worst $\alpha$ of outcomes is a minimum "
                    r"over a threshold $w$, for integrable loss and tail fraction $0<\alpha<1$; a threshold atom is allocated fractionally"),
                why(r"the subgradient condition handles atoms; with a continuous loss law this reduces to upper-tail probability $\alpha$, the "
                    r"$(1-\alpha)$ quantile. Joint finite-sample optimization need not reach this optimum")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "Here alpha denotes the upper-tail fraction, not a confidence level. For an integrable loss and alpha strictly between zero and one, the Rockafellar–Uryasev representation minimizes over a threshold w. It handles an atom at that threshold by assigning only the required fraction of its mass. <bookmark mark='a'/> The subgradient condition places alpha between strict and weak exceedance probabilities. For a continuous loss law it reduces to the usual upper quantile condition. Jointly training the threshold and the hedge is possible, but a finite optimizer need not attain the population optimum."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def cvar(self, rm):
        bins = np.asarray(rm["bins"])
        mid = (bins[:-1] + bins[1:]) / 2
        e0, c0 = rm["runs"]["entropic_0"], rm["runs"]["cvar_ru_0"]
        he, hc = np.asarray(e0["hist"], float), np.asarray(c0["hist"], float)
        top = max((he / he.sum()).max(), (hc / hc.sum()).max()) * 1.15
        g = axes([bins[0], bins[-1]], [0, top], x_length=7.4, y_length=4.2, xlabel=r"profit and loss of the hedged short "
                 r"call (premium excluded; capped histogram)", ylabel=r"share of paths", xticks=[-8, -4, 0], yticks=[], font_size=14
                 ).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax

        def hist(hh, col):
            pts = [ax.c2p(bins[0], 0)]
            for i, v in enumerate(hh / hh.sum()):
                pts += [ax.c2p(bins[i], v), ax.c2p(bins[i + 1], v)]
            pts.append(ax.c2p(bins[-1], 0))
            return VMobject(stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=0.15).set_points_as_corners(pts)
        H1, H2 = hist(he, NET), hist(hc, BAD)
        wt = ValueTracker(-c0["var50"] - 2.5)
        wline = always_redraw(lambda: DashedLine(ax.c2p(wt.get_value(), 0), ax.c2p(wt.get_value(), top), stroke_color=GOOD,
                                                 stroke_width=2.5))
        wlab = always_redraw(lambda: MathTex(r"-w", font_size=28, color=GOOD).next_to(ax.c2p(wt.get_value(), top), UP,
                                                                                    buff=0.05))
        rows = VGroup(
            label(r"averages over three seeds, 0.5\% costs, band network", font_size=18, color=GREY_A),
            MathTex(rf"\text{{entropic: CVaR}}_{{50}}\ {_avg(rm, 'entropic', 'cvar50'):.3f},\ "
                    rf"\text{{CVaR}}_{{5}}\ {_avg(rm, 'entropic', 'cvar05'):.3f}", font_size=26, color=NET),
            MathTex(rf"\text{{CVaR-trained: CVaR}}_{{50}}\ {_avg(rm, 'cvar_ru', 'cvar50'):.3f},\ "
                    rf"\text{{CVaR}}_{{5}}\ {_avg(rm, 'cvar_ru', 'cvar05'):.3f}", font_size=26, color=BAD),
            label(rf"learned $w$ {c0['w']:.3f}; the empirical VaR$_{{50}}$ of its losses {c0['var50']:.3f}",
                  font_size=19, color=GOOD),
            label(rf"bands at the money: [{e0['band_atm'][0]:.2f}, {e0['band_atm'][1]:.2f}] entropic, "
                  rf"[{c0['band_atm'][0]:.2f}, {c0['band_atm'][1]:.2f}] CVaR", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"The histograms select seed zero. They retain all two hundred thousand evaluation paths, but the saved histograms cap values below minus nine or above three into the edge bins. The summary risk measures use uncapped outcomes. <bookmark mark='a'/> The learned threshold is {c0['w']:.3f}; the evaluation loss median is {c0['var50']:.3f}. Finite training and a separate sample need not make them equal. <bookmark mark='b'/> The side panel averages three training seeds, all evaluated with the same fixed test draws. The empirical worst-half and worst-five-percent losses are different targets. <bookmark mark='c'/> Neither optimization success nor a far-tail ranking is guaranteed by choosing a risk measure. In particular, the finite-path exponential objective does not establish a finite population exponential moment."
        ) as vo:
            self.play(FadeIn(g), Create(H1), FadeIn(rows[0]), FadeIn(rows[1]))
            self.play(Create(H2), FadeIn(rows[2]))
            vo.wait_until("a")
            self.add(wline, wlab)
            self.play(wt.animate.set_value(-c0["w"]), run_time=2.5)
            self.play(FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]))
            vo.wait_until("c")
        wline.clear_updaters()
        wlab.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def merton(self, d):
        m = d["merton_atm"]
        rows = [cmath(r"\max\ \mathbb{E}\big[-e^{-\gamma W_T}\big]", r",\ ", r"W_T = x - Z + (\delta\cdot S)_T", font_size=38,
                      colors={r"\max\ \mathbb{E}\big[-e^{-\gamma W_T}\big]": GOOD}),
                cmath(r"\delta^*_t", r"=", r"\Delta_t + \frac{\mu}{\gamma\,\sigma^2\,S_t}", font_size=44,
                      colors={r"\delta^*_t": NET}),
                cmath(r"\frac{0.3}{1 \times 0.2^2 \times 100}", r"=", rf"{m:.3f}\ \text{{shares}}", font_size=40,
                      colors={r"=": WHITE})]
        whys = [why(r"exponential utility of terminal wealth, which is what minimizing entropic risk means, now with the "
                    r"stock with excess drift $\mu$; continuous trading, complete market, zero rates/costs, suitable admissibility and finite-utility assumptions"),
                why(r"by the martingale method: the claim can be replicated, so hedge it away with delta; what remains is "
                    r"the problem with no claim, whose solution under exponential utility holds a fixed dollar amount "
                    r"$\mu / \gamma\sigma^2$ in the stock (Merton 1969)"),
                why(r"at the money, $\mu = 30\%$, risk aversion 1, volatility 20\%: the hedger should hold this many extra "
                    r"shares, a bet on the drift layered on top of the hedge")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            f"Use a continuous-trading, complete-market ideal with zero rates and costs, and admissible strategies with well-defined utility. <bookmark mark='a'/> Replicating the claim separates it from the no-claim investment problem. Exponential utility then adds a fixed-dollar Merton position, mu over gamma sigma squared, to the replication delta. Here mu is excess drift. <bookmark mark='c'/> At price one hundred, drift thirty percent and volatility twenty percent, the overlay is {m:.3f} shares. It is an investment component and may be intended by the mandate. This ideal formula is a benchmark; it does not assert the exact optimizer of the saved daily-grid empirical objective."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def replay(self, d):
        S = np.asarray(d["S"])
        bsd, mer = np.asarray(d["bs_delta"]), np.asarray(d["merton"])
        runs = np.array([d["runs"][str(s)]["curve"] for s in (0, 1, 2)])
        steps = np.arange(runs.shape[1], dtype=float)
        sn = d["runs"]["0"]["snaps"]
        ck = d["ck"]
        yr = data_range(bsd, mer, *[sn[str(c)] for c in ck])

        def frame(i):
            g = axes([S[0], S[-1]], yr, x_length=5.0, y_length=3.6, xlabel=r"price, 15 days to expiry",
                     ylabel=r"shares held", xticks=[90, 100, 110], yticks=[0, 0.5, 1], font_size=13)
            return VGroup(g, DashedVMobject(curve(g.ax, S, bsd, REF, stroke_width=2.2), num_dashes=36),
                          DashedVMobject(curve(g.ax, S, mer, GOOD, stroke_width=2.5), num_dashes=36),
                          curve(g.ax, S, np.asarray(sn[str(ck[i])]), NET, stroke_width=4),
                          label(rf"step {ck[i]}", font_size=17, color=NET).next_to(g, DOWN, buff=0.1))
        rp = TrainingReplay(steps, runs, frame, checkpoints=ck,
                            ylabel=r"empirical exponential objective, drifting paths")
        devs = [row["dev"] for row in d["rows"]]
        leg = legend([(REF, r"Black--Scholes delta"), (GOOD, r"delta $+\ \mu / \gamma\sigma^2 S$ (Merton)"),
                      (NET, r"the network trained on paths drifting at 30\% a year")], font_size=16).arrange(
            RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"These three no-cost training runs use thirty-percent drifting paths. The full holdings and batch-objective ranges are retained. <bookmark mark='a'/> Across prices ninety to one hundred ten, the mean holding deviations from delta range from {min(devs):.3f} to {max(devs):.3f} shares across seeds. The continuous-time Merton benchmark gives {d['merton_atm']:.3f} at the money. This qualitative agreement is a finite-model observation. A daily-grid optimizer, finite samples and unverified exponential tails prevent treating it as exact recovery of the continuous-time solution."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(leg))
            vo.wait_until("a")
            rp.play(self, run_time=max(vo.remaining(0.5), 5))
        self.wait(0.4)
        self.clear_scene()

    def twist(self, d):
        rows = d["rows"]
        f = lambda key: float(np.mean([r[key]["price"] for r in rows]))  # noqa: E731
        dP, dQ, pP, pQ = f("drifted_on_P"), f("drifted_on_Q"), f("plain_on_P"), f("plain_on_Q")
        tab = VGroup(
            VGroup(label(r"", font_size=20), label(r"empirical $\rho$ on drifting paths", font_size=21, color=GREY_A),
                   label(r"empirical $\rho$ on driftless paths", font_size=21, color=GREY_A)),
            VGroup(label(r"hedger trained with drift", font_size=22, color=NET), MathTex(f"{dP:.3f}", font_size=34, color=NET),
                   MathTex(f"{dQ:.3f}", font_size=34, color=NET)),
            VGroup(label(r"hedger trained without drift", font_size=22, color=REF), MathTex(f"{pP:.3f}", font_size=34),
                   MathTex(f"{pQ:.3f}", font_size=34)))
        xs = [-4.0, 0.6, 4.2]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 1.8 - 0.9 * i, 0])
        ttl = wrapped_label(r"Empirical short-call risk; no no-claim baseline subtracted", 12.8, 26).to_edge(UP, buff=0.6)
        foot = wrapped_label(r"Under drift the no-claim optimum generally is nonzero. These finite-sample values do not subtract it, so they are not indifference premiums. Changing the training measure changes the objective and requires separate validation.", 12.2, 20, GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"On drifting paths the two empirical short-call risks are {dP:.3f} and {pP:.3f}; on driftless paths, {dQ:.3f} and {pQ:.3f}, averaged over three trained policies. <bookmark mark='a'/> The code does not optimize and subtract a no-claim baseline under drift. These entries therefore are not indifference premiums. In the continuous complete-market ideal, properly subtracting the investment baseline gives a replication price independent of physical drift. <bookmark mark='b'/> An investment overlay may fit one mandate and violate another. Training under a martingale or near-martingale measure can target hedging rather than a drift view, but changing measure does not automatically validate a model, handle market incompleteness or solve finite-sample tail problems."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tab[0]), FadeIn(tab[2]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def cards(self):
        cs = VGroup(
            firm_card(r"QLBS", r"Halperin (2020): Q-learning in a discrete Black--Scholes world: price and hedge from "
                      r"data, one rebalancing at a time", source=r"Dixon, Halperin and Bilokon, ch.\ 10", width=4.1,
                      font_size=17, kind=r"Method"),
            firm_card(r"RL hedging", r"Kolm and Ritter (2019); Cao, Chen, Hull and Poulos (2021): reinforcement learning "
                      r"agents that trade off cost against variance", source=r"\textit{J.\ Financial Data Science}",
                      width=4.1, font_size=17, kind=r"Method"),
            firm_card(r"Deep Bellman hedging", r"Buehler, Murray and Wood (2022): a value function over whole portfolios, "
                      r"amortizing portfolio decisions within a specified training domain; generalization requires checks", source=r"arXiv 2207.00932", width=4.1, font_size=17, kind=r"Method"),
        ).arrange(RIGHT, buff=0.22).shift(UP * 0.4)
        for c_ in cs:
            c_[0].set_stroke(GREY_C)
        with self.voiceover(
            "The same objective, seen as reinforcement learning: Igor Halperin's QLBS, the agents of Kolm and Ritter "
            "and of Cao, Chen, Hull and Poulos, and Buehler's deep Bellman hedging. Whatever the algorithm, the two "
            "questions remain: which risk, and under which probabilities."
        ):
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.2) for c_ in cs], lag_ratio=0.5, run_time=4))
        q = ask(r"your deep hedger makes money on average with no costs. Is it hedging?")
        with self.voiceover("Which gives us a desk question: your deep hedger makes money on average with no costs. "
                            "Is it hedging?"
                            " Not entirely. Its delta part hedges; the extra holding is Merton's bet on the drift. Test it on paths without drift before you call it a hedge. Next: what trading costs do to the hedge."):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
