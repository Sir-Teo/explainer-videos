from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
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
                cmath(r"\partial_w", r":\ ", r"1 - \tfrac1\alpha\,\mathbb{P}(L > w) = 0\ \Rightarrow\ w^* = \mathrm{VaR}_\alpha(L)",
                      font_size=38, colors={r"\partial_w": GOOD})]
        whys = [why(r"Rockafellar and Uryasev (2000): the expected loss in the worst $\alpha$ of outcomes is a minimum "
                    r"over one number $w$, so it can be trained by gradient descent like everything else"),
                why(r"differentiate in $w$: the minimum sits where exactly a fraction $\alpha$ of losses exceed $w$, the "
                    r"value at risk. So $w$ joins the network's weights as one more trainable number")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "The entropic measure is one choice. Desks often prefer conditional value at risk: the average loss in "
            "the worst fraction alpha of outcomes. It looks hard to train, because it is defined by sorting. Tyrrell "
            "Rockafellar and Stanislav Uryasev showed it is a minimum over a single threshold w: w, plus the expected "
            "excess of the loss over w, scaled up by one over alpha. <bookmark mark='a'/> Differentiate in w: the "
            "minimum sits where exactly a fraction alpha of losses lie above it, the value at risk. So w becomes one "
            "more trainable number, learned alongside the network."
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
        top = max(he.max(), hc.max()) / he.sum() * 1.15
        g = axes([bins[0], bins[-1]], [0, top], x_length=7.4, y_length=4.2, xlabel=r"profit and loss of the hedged short "
                 r"call (premium not included)", ylabel=r"share of paths", xticks=[-8, -4, 0], yticks=[], font_size=14
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
        ce, cc = _avg(rm, "cvar_ru", "cvar50"), _avg(rm, "entropic", "cvar50")
        t5e, t5c = _avg(rm, "entropic", "cvar05"), _avg(rm, "cvar_ru", "cvar05")
        if ce < cc:
            first = "The CVaR-trained hedger has the lower CVaR at fifty percent, as it should: it optimized exactly that."
        else:
            first = "Even on its own objective the CVaR-trained hedger is no better here, a sign of how flat the problem is."
        if t5e < t5c:
            second = "But in the far tail, the worst five percent, the entropic hedger is better: its exponential " \
                     "punishes the very worst paths hardest."
        else:
            second = "And it is better in the far tail too, the worst five percent."
        with self.voiceover(
            "Train the band network both ways, at half a percent costs: once on the entropic measure, once on CVaR at "
            "fifty percent, three seeds each. Here are the profit-and-loss distributions of the two hedgers on fresh "
            "paths. <bookmark mark='a'/> The dashed line is the CVaR hedger's learned threshold, sliding to where it "
            f"settled, which is the median loss, as the derivation says: {c0['w']:.3f}, against an empirical "
            f"{c0['var50']:.3f}. <bookmark mark='b'/> {first} <bookmark mark='c'/> {second} The choice of risk measure is a choice of which "
            "losses you fear most, and the network will shape its hedge accordingly."
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
                    r"stock drifting at $\mu$ a year under the real-world measure; complete market, zero rates"),
                why(r"by the martingale method: the claim can be replicated, so hedge it away with delta; what remains is "
                    r"the problem with no claim, whose solution under exponential utility holds a fixed dollar amount "
                    r"$\mu / \gamma\sigma^2$ in the stock (Merton 1969)"),
                why(r"at the money, $\mu = 30\%$, risk aversion 1, volatility 20\%: the hedger should hold this many extra "
                    r"shares, a bet on the drift layered on top of the hedge")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Now the trap. Every path so far had no drift; paths that look like history do. Minimizing entropic risk "
            "is maximizing exponential utility: what is the best holding when the stock drifts at mu? "
            "<bookmark mark='a'/> In a complete market the answer "
            "splits in two. The claim can be replicated, so the delta hedge removes it. What is left is the problem "
            "with no claim at all, and Robert Merton solved that in 1969: under exponential utility, hold a fixed "
            "dollar amount, the drift over risk aversion times variance. <bookmark mark='c'/> At the money, with a "
            f"thirty percent drift, that is {m:.3f} extra shares. Not a hedge: a bet."
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

        def frame(i):
            g = axes([S[0], S[-1]], [0, 1.1], x_length=5.0, y_length=3.6, xlabel=r"price, 15 days to expiry",
                     ylabel=r"shares held", xticks=[90, 100, 110], yticks=[0, 0.5, 1], font_size=13)
            return VGroup(g, DashedVMobject(curve(g.ax, S, bsd, REF, stroke_width=2.2), num_dashes=36),
                          DashedVMobject(curve(g.ax, S, np.clip(mer, 0, 1.1), GOOD, stroke_width=2.5), num_dashes=36),
                          curve(g.ax, S, np.clip(np.asarray(sn[str(ck[i])]), 0, 1.1), NET, stroke_width=4),
                          label(rf"step {ck[i]}", font_size=17, color=NET).next_to(g, DOWN, buff=0.1))
        rp = TrainingReplay(steps, np.clip(runs, None, np.percentile(runs, 99)), frame, checkpoints=ck,
                            ylabel=r"entropic risk, drifting paths")
        devs = [row["dev"] for row in d["rows"]]
        leg = legend([(REF, r"Black--Scholes delta"), (GOOD, r"delta $+\ \mu / \gamma\sigma^2 S$ (Merton)"),
                      (NET, r"the network trained on paths drifting at 30\% a year")], font_size=16).arrange(
            RIGHT, buff=0.35).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Train the same no-cost hedger on paths drifting at thirty percent a year, three seeds, and watch its "
            "holding against the price. <bookmark mark='a'/> It does not settle on the delta. It settles above it, by a "
            "nearly constant amount, right along Merton's line. Averaged over prices from ninety to a hundred and ten, "
            f"the three seeds hold {min(devs):.3f} to {max(devs):.3f} shares more than delta; Merton's formula says "
            f"{d['merton_atm']:.3f} at the money. Nobody told it about Merton. It rediscovered a portfolio problem "
            "from 1969, inside an option hedge."
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
        eD = dP + float(np.mean([r["drifted_on_P"]["mean"] for r in rows]))
        eP = pP + float(np.mean([r["plain_on_P"]["mean"] for r in rows]))
        if eD > eP:
            profit = "A hedger that expects a profit is not only hedging."
        else:
            profit = "So the drift buys it little expected profit here."
        tab = VGroup(
            VGroup(label(r"", font_size=20), label(r"priced on drifting paths", font_size=21, color=GREY_A),
                   label(r"priced on driftless paths", font_size=21, color=GREY_A)),
            VGroup(label(r"hedger trained with drift", font_size=22, color=NET), MathTex(f"{dP:.3f}", font_size=34, color=NET),
                   MathTex(f"{dQ:.3f}", font_size=34, color=NET)),
            VGroup(label(r"hedger trained without drift", font_size=22, color=REF), MathTex(f"{pP:.3f}", font_size=34),
                   MathTex(f"{pQ:.3f}", font_size=34)))
        xs = [-4.0, 0.6, 4.2]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 1.8 - 0.9 * i, 0])
        ttl = label(r"Indifference prices, no costs, mean of three seeds", font_size=28).to_edge(UP, buff=0.6)
        if dQ > pQ and dP < pP:
            verdict = "On drifting paths it asks a lower price, because it counts on the drift; on driftless paths " \
                      "it needs more than the plain hedger. Part of what it learned was speculation."
        else:
            verdict = "Here the difference is small in both directions; the overlay is a bet that barely moves the price."
        foot = wrapped_label(r"the gap between a deep hedge and the replicating hedge can be a bet on the drift: a "
                             r"speculative overlay, unless the risk measure weighs bad outcomes enough (Fran\c{c}ois, "
                             r"Gauthier, Godin and P\'erez Mendoza 2024). The remedy of Buehler, Murray, Pakkanen and Wood "
                             r"(2021): first remove the drift, training under a near-martingale measure", 12.2, 19,
                             GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"Is that bad? Price both hedgers on both kinds of paths. <bookmark mark='a'/> {verdict} Sold at its "
            f"own price, the drift-trained hedger expects to keep {eD:.3f} per option on drifting paths, the plain "
            f"one {eP:.3f}. {profit} <bookmark mark='b'/> Pascal François and coauthors showed in 2024 "
            "that the gap between deep hedging and delta hedging can be exactly such a speculative overlay, unless the "
            "risk measure puts enough weight on bad outcomes. Buehler's team proposed the cure: before training, "
            "remove the drift from the simulator, learning a nearby measure under which prices are martingales."
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
                      r"so one training hedges any starting book", source=r"arXiv 2207.00932", width=4.1, font_size=17, kind=r"Method"),
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
