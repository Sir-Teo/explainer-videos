from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import quoting as Q
from videos.quant.quant11.common import (ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, illustration, load, pause)

SHOW = [0, 10_000, 40_000, 160_000, 800_000]


def skew_color(v, lim=2.75):
    x = float(np.clip(v / lim, -1, 1))
    return interpolate_color(ManimColor(GREY_D), ManimColor(QC.GAIN if x > 0 else QC.LOSS), abs(x))


class Inventory(VoiceoverScene):
    def construct(self):
        m = load("mm_learn")
        self.card()
        self.toy(load("mm"))
        self.derive(m)
        self.lab()
        self.replay(m)
        self.live(m)

    def card(self):
        c = chapter_card(9, r"Inventory, and a market maker that learns", r"How far should a quote lean?", part=PART)
        with self.voiceover("Chapter nine. Inventory: the optimal quote, and a market maker that learns."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def toy(self, m):
        a, b = m["no skew"], m["skewed"]
        ia, ib = np.asarray(a["inventory"]), np.asarray(b["inventory"])
        x = np.arange(len(ia)) * 5
        lim = max(np.abs(ia).max(), np.abs(ib).max()) + 2
        g = axes([0, x[-1]], [-lim, lim], x_length=7.2, y_length=4.2, xlabel=r"client requests",
                 ylabel=r"inventory, in units of vega", xticks=[0, 500, 1000, 1500, 2000], yticks=[-40, -20, 0, 20, 40],
                 font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        tr = ValueTracker(0.0)
        la = tracing(ax, x, ia, tr, THETA, stroke_width=2.5)
        lb = tracing(ax, x, ib, tr, GAMMA, stroke_width=3)
        leg = legend([(THETA, r"quotes fixed around fair value"), (GAMMA, r"quotes skewed against inventory")],
                     font_size=19).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            MathTex(r"\text{mid} = \sigma_{\text{fair}} - k \cdot \text{vega inventory}", font_size=30, color=VEGA),
            MathTex(rf"\text{{largest inventory: }} {a['max_abs']:.0f} \to {b['max_abs']:.0f}", font_size=30, color=GAMMA),
            MathTex(rf"\text{{spread earned: }} {a['spread_pnl']:.1f} \to {b['spread_pnl']:.1f}", font_size=30),
            wrapped_label(r"a little income given up for a book that stays small", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = illustration(r"a toy: 2{,}000 random client requests, the same for both books")
        with self.voiceover(
            "An options market maker quotes volatility to clients who arrive at random, some to buy and some to sell. "
            "A desk that quotes fixed around fair value lets its inventory wander, here as far as "
            f"{a['max_abs']:.0f} units of vega. <bookmark mark='a'/> Lean the quotes against the inventory, lower when "
            "long and higher when short, and the same clients leave a book that stays within "
            f"{b['max_abs']:.0f}, for a small loss of spread income. How far should the quotes lean? That is a control "
            "problem, and it has an exact answer."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg))
            self.add(la, lb)
            self.play(tr.animate.set_value(len(x) - 1), FadeIn(side[0]), run_time=vo.until("a"), rate_func=linear)
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side[1:]], lag_ratio=0.4, run_time=2.5))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self, m):
        rows = [
            cmath(r"\lambda^{\pm}(\delta)", r"=", r"A e^{-k\delta},\qquad \max\ \mathbb{E}\Big[X_T + q_T S_T - "
                  r"\phi\int_0^T q_t^2\,dt\Big]", font_size=32),
            cmath(r"0", r"=", r"\partial_t\theta + \max_{\delta^{\pm}} \sum_{\pm} \lambda^{\pm}(\delta^{\pm})\big[\delta^{\pm} "
                  r"+ \theta(q \mp 1) - \theta(q)\big] - \phi q^2", font_size=30),
            cmath(r"\delta^{\pm *}", r"=", r"\tfrac1k + \theta(q) - \theta(q \mp 1)", font_size=34),
            VGroup(
                MathTex(r"\delta^b\approx\tfrac1k+(q+\tfrac12)c,\quad\delta^a\approx\tfrac1k-(q-\tfrac12)c", font_size=30),
                MathTex(r"c=\sqrt{\phi e/(Ak)}", font_size=26),
            ).arrange(DOWN, buff=0.12),
        ]
        whys = [why(r"fills fall exponentially in the distance from fair value; profit, minus a running penalty on "
                    r"inventory (Avellaneda and Stoikov 2008; Cartea and Jaimungal's form)"),
                why(r"the Hamilton--Jacobi--Bellman equation, with the ansatz value $= x + qs + \theta(t, q)$"),
                why(r"differentiate $A e^{-k\delta}(\delta + \Delta\theta)$ in $\delta$ and set it to zero"),
                why(r"Gu\'eant, Lehalle and Fernandez-Tapia (2013), in the limit of a long horizon: long inventory moves "
                    r"both quotes down, in proportion to $q$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-0.4, buff=0.5, edge=6.9)  # ends high: the foot fits below
        foot = wrapped_label(r"in an options book $q$ is vega and $\phi$ carries the volatility of implied volatility "
                             r"(Stoikov and Sa\u{g}lam 2009); a hundred options reduce to a few risk factors (Baldacci, "
                             r"Bergault and Gu\'eant 2021); demand that market makers cannot hedge moves prices "
                             r"(G\^arleanu, Pedersen and Poteshman 2009)", 12.4, 19, ALT).to_edge(DOWN, buff=0.35)
        pc = pause(r"You are long 20 vega. Raise both quotes, or lower them?", width=4.6, font_size=21, corner=UR)
        with self.voiceover(
            "Write it down. Clients hit a quote with an intensity that falls exponentially in its distance from fair "
            "value. The market maker maximizes its profit minus a running penalty on inventory, Marco Avellaneda "
            "and Sasha Stoikov's problem, in the form Álvaro Cartea and Sebastian Jaimungal use. <bookmark mark='a'/> "
            "Dynamic programming gives a Hamilton-Jacobi-Bellman equation for the value of holding q. "
            "<bookmark mark='b'/> Its first-order condition: each quote sits one over k from fair value, plus the "
            "change in that value from one more unit of inventory. <bookmark mark='c'/> Olivier Guéant, "
            "Charles-Albert Lehalle and Joaquin Fernandez-Tapia derived a long-horizon approximation: long inventory moves both "
            "quotes down, in proportion to q. <bookmark mark='d'/> For options, q is vega, and Sasha Stoikov and "
            "Mehmet Sağlam did exactly this in 2009. And because market makers cannot hedge perfectly, client demand "
            "itself moves option prices, as Gârleanu, Pedersen and Poteshman showed. Pause and "
            "predict: long twenty vega, raise your quotes or lower them? Lower: you want to sell."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            # the top row's place goes to the question; the last two rows, the answer's ingredients, stay
            self.play(FadeOut(rows[1]), FadeOut(whys[1]), FadeIn(foot), FadeIn(pc))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lab(self):
        card = lab_card(r"a quote that leans against inventory", [
            "def quote(fair_vol, inventory_vega, half_spread=0.01,",
            "          skew_per_vega=0.002, vega_limit=None) -> dict:",
            "    mid = fair_vol - skew_per_vega * inventory_vega",
            "    bid, ask = mid - half_spread, mid + half_spread",
            "    if vega_limit is not None and inventory_vega >= vega_limit:",
            "        bid = np.nan",
            "    if vega_limit is not None and inventory_vega <= -vega_limit:",
            "        ask = np.nan",
            "    return {\"bid\": bid, \"ask\": ask, \"mid\": mid}",
        ], source="explainer/quant/house/quoting.py", width=7.6).to_edge(UP, buff=0.4)
        outs = []
        for inv in (-20, 0, 20):
            q = Q.quote(0.60, inv, half_spread=0.01, skew_per_vega=0.002, vega_limit=None)
            outs.append(f"inventory {inv:+3d}:  bid {100 * q['bid']:.1f}%   ask {100 * q['ask']:.1f}%")
        with self.voiceover(
            "In the House, the quoting rule is a few lines: the mid moves against the vega inventory, and beyond a "
            "limit the desk quotes one side only. <bookmark mark='a'/> Run it at sixty percent fair volatility. Short "
            "twenty vega, it quotes four points higher, to buy back; long twenty, four points lower, to sell."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, ["quote(0.60, inv, half_spread=0.01, skew_per_vega=0.002)"] + outs)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def replay(self, m):
        ck = np.asarray(m["checkpoints"], float)
        vals = np.clip(np.asarray(m["values"]) / m["V_dp"] * 100, -50, 105)
        qs = np.asarray(m["q"])
        dp = np.asarray(m["dp_skew"])
        sk0 = m["skews"]["0"]

        def strip(sk, title, col):
            cells = VGroup()
            for i, q in enumerate(qs):
                cells.add(Rectangle(width=0.5, height=0.17, stroke_width=0.5, stroke_color=GREY_D,
                                    fill_color=skew_color(sk[i]), fill_opacity=1).move_to([0, (q) * 0.18, 0]))
            return VGroup(cells, label(title, font_size=17, color=col).next_to(cells, UP, buff=0.1))

        def frame(i):
            c = SHOW[i]
            a = strip(sk0[str(c)], r"learned", GAMMA)
            b = strip(dp, r"exact (DP)", WHITE).next_to(a, RIGHT, buff=0.25)
            ql = VGroup(label(r"long 10", font_size=15, color=GREY_B).next_to(a[0][-1], LEFT, buff=0.1),
                        label(r"short 10", font_size=15, color=GREY_B).next_to(a[0][0], LEFT, buff=0.1))
            return VGroup(a, b, ql)
        rp = TrainingReplay(ck, vals, frame, SHOW, ylabel=r"greedy policy's value, \% of the optimum",
                            xlabel=r"simulated clients", color=GAMMA, left=LEFT * 4.2 + DOWN * 0.3,
                            right=RIGHT * 2.2 + DOWN * 0.2, x_length=6.0, y_length=3.6)
        ax = rp.ax
        glft = 100 * m["glft_value"] / m["V_dp"]
        sym = max(100 * m["sym_best"] / m["V_dp"], -50)
        base = VGroup(DashedLine(ax.c2p(0, 100), ax.c2p(ck[-1], 100), color=WHITE, stroke_width=2),
                      DashedLine(ax.c2p(0, glft), ax.c2p(ck[-1], glft), color=VEGA, stroke_width=2),
                      DashedLine(ax.c2p(0, sym), ax.c2p(ck[-1], sym), color=THETA, stroke_width=2))
        bl = VGroup(label(r"exact optimum", font_size=15, color=WHITE).next_to(base[0], UP, buff=0.04).align_to(base[0], RIGHT),
                    label(rf"GLFT formula: {glft:.0f}\%", font_size=15, color=VEGA).next_to(base[1], DOWN, buff=0.04).align_to(base[1], RIGHT),
                    label(r"best symmetric quote", font_size=15, color=THETA).next_to(base[2], UP, buff=0.04).align_to(base[2], RIGHT))
        key = VGroup(label(r"colour: skew = bid offset $-$ ask offset", font_size=17, color=GREY_A),
                     legend([(QC.GAIN, r"quotes shaded down (sell)"), (QC.LOSS, r"shaded up (buy)")], font_size=15)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        pct = 100 * np.asarray(m["pct_final"])
        src = illustration(rf"a 21-state inventory game; 5 seeds of tabular Q-learning, {int(ck[-1]):,} steps each; the "
                           r"band spans the seeds".replace(",", "{,}"))
        msay = (f"After eight hundred thousand simulated clients the five seeds reach between {pct.min():.0f} and "
                f"{pct.max():.0f} percent of the optimum.")
        with self.voiceover(
            "Now let a machine find the answer without being told the model. The game: twenty-one inventory levels, "
            "seven quote offsets a side, clients arriving at random. Dynamic programming solves it exactly: the white "
            "column, a staircase that shades the quotes down when long and up when short. <bookmark mark='a'/> The "
            "learner is tabular Q-learning, the simplest method that can find this: it only sees clients arrive and "
            "trade, and keeps a table of how good each quote is at each inventory. Five seeds; the band is their "
            "spread. <bookmark mark='b'/> Watch its column, seed zero, sharpen from noise into the staircase, and its "
            f"value climb. {msay} The closed-form formula, snapped to the same grid, gets {glft:.0f} percent; quoting "
            "symmetrically, whatever the width, loses money once inventory is charged for. <bookmark mark='c'/> The "
            "learner is noisiest at inventories it rarely visits. That is the honest lesson of learned market makers: "
            "they learn where they have data."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(key), FadeIn(src), Create(base), FadeIn(bl))
            vo.wait_until("a")
            vo.wait_until("b")
            rp.play(self, run_time=max(vo.until("c") - 0.3, 4.0))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def live(self, m):
        L, Sy = m["live"]["learned"], m["live"]["symmetric"]
        ia, ib = np.asarray(L["inventory"]), np.asarray(Sy["inventory"])
        x = np.arange(len(ia))
        g = axes([0, len(ia)], [-10, 10], x_length=8.0, y_length=3.6, xlabel=r"clients",
                 ylabel=r"inventory (vega units)", xticks=[0, 500, 1000, 1500, 2000], yticks=[-10, -5, 0, 5, 10],
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        tr = ValueTracker(0.0)
        la = tracing(g.ax, x[::4], ia[::4], tr, GAMMA, stroke_width=2.5)
        lb = tracing(g.ax, x[::4], ib[::4], tr, THETA, stroke_width=2.5)
        leg = legend([(GAMMA, rf"the learned quoter: score {L['score']:+.0f}"),
                      (THETA, rf"best symmetric quote ({m['sym_best_offset']:.1f} points wide a side): "
                              rf"{Sy['score']:+.0f}")], font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = wrapped_label(r"the symmetric quoter's best choice is to quote so wide that it barely trades: it keeps "
                             r"its inventory small by giving up the business", 4.0, 20, GREY_A).to_edge(RIGHT, buff=0.4)
        better = L["score"] > Sy["score"]
        lsay = ("The learned quoter trades all day and keeps its inventory within a few units by leaning, scoring "
                f"{L['score']:.0f}; the symmetric one, to keep its inventory small, quotes so wide it barely trades, "
                f"and scores {Sy['score']:.0f}." if better else
                f"Here the symmetric quoter scores {Sy['score']:.0f} against the learner's {L['score']:.0f}.")
        with self.voiceover(
            "Put the trained quoter to work on two thousand new clients, next to the best symmetric quote, on exactly "
            f"the same arrivals. <bookmark mark='a'/> {lsay} Leaning is how a market maker stays in business and stays "
            "small. Chapter ten hedges what is left."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.add(la, lb)
            self.play(tr.animate.set_value(len(x[::4]) - 1), run_time=max(vo.until("a") + 4, 4.0), rate_func=linear)
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
