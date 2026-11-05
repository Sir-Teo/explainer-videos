from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import (
    ARB_C,
    BAD,
    FEE_C,
    GOOD,
    HURDLE,
    PART,
    POOL_C,
    fit_right,
    load,
)

SHOW = {"withdraw": r"withdraw", "wide (x2)": r"wide, $\times 2$", "medium (+-20%)": r"medium, $\pm 20\%$",
        "narrow (+-5%)": r"narrow, $\pm 5\%$"}


class Concentrated(VoiceoverScene):
    def construct(self):
        v = load("v3")
        rl = load("rl")
        self.card(v)
        self.ranges()
        self.holdings(v)
        self.efficiency(v)
        self.out_of_range(v)
        self.lvr_scale(v)
        self.rl_setup(rl)
        self.rl_q(rl)
        self.rl_results(rl)
        self.rl_caveats()
        self.question()

    def card(self, v):
        e5 = [r for r in v["rows"] if abs(r["w"] - 1.05) < 1e-9][0]["eff"]
        c = chapter_card(4, r"Concentrated liquidity", r"What does a provider gain, and risk, by choosing a price range?",
                         part=PART)
        with self.voiceover(
            f"Chapter four, and the answer to the pause: about {e5:.0f} times as much liquidity per dollar, and so about "
            f"{e5:.0f} times the loss to arbitrage per dollar, as long as the price stays inside the range. Concentration "
            "is leverage on the same short-volatility position."
        ):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ranges(self):
        rows = [cmath(r"x", r"=", r"L\Bigl(\tfrac{1}{\sqrt P} - \tfrac{1}{\sqrt{p_b}}\Bigr)", font_size=40,
                      colors={r"x": POOL_C}),
                cmath(r"y", r"=", r"L\bigl(\sqrt P - \sqrt{p_a}\bigr)", font_size=40, colors={r"y": POOL_C}),
                cmath(r"P < p_a", r":", r"\text{all token};\quad P > p_b:\ \text{all dollars}", font_size=36)]
        whys = [why(r"Uniswap v3 (2021): a provider chooses a range $[p_a, p_b]$ and supplies liquidity $L$ only inside "
                    r"it; inside, it behaves like a constant-product pool with a larger, virtual reserve"),
                why(r"the dollar holdings grow from zero at the bottom of the range"),
                why(r"outside the range the position stops trading and earns nothing: below it holds only the token, "
                    r"above only dollars")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Uniswap's third version, in twenty twenty-one. <bookmark mark='a'/> A provider chooses a price range and "
            "supplies liquidity only inside it. Inside, it behaves like a constant-product pool with a larger virtual "
            "reserve, holding x of the token, <bookmark mark='b'/> and y of dollars. <bookmark mark='c'/> Outside the "
            "range it stops trading and earns nothing: below it, it is all token; above it, all dollars."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def holdings(self, v):
        c = v["curve"]
        p = np.asarray(c["p"], float)
        val = np.asarray(c["v3"], float)
        top = float(val.max() * 1.1)
        g = axes([1200, 3000], [0, top], x_length=7.0, y_length=4.0, xlabel=r"ether price, dollars",
                 ylabel=r"position value, dollars", xticks=[1200, 1600, 2000, 2500, 3000], yticks=[], font_size=16)
        g.move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        vc = curve(ax, p, val, POOL_C, stroke_width=3)
        lo = DashedLine(ax.c2p(v["pa"], 0), ax.c2p(v["pa"], top), color=GREY_B)
        hi = DashedLine(ax.c2p(v["pb"], 0), ax.c2p(v["pb"], top), color=GREY_B)
        side = VGroup(label(r"below the range: all ether, value falls with it", font_size=17, color=GREY_A),
                      label(r"inside: concave, short gamma", font_size=17, color=POOL_C),
                      label(r"above: all dollars, flat", font_size=17, color=GREY_A))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 1.8)
        fit_right(side)
        with self.voiceover(
            f"A position on ether between {v['pa']:,.0f} and {v['pb']:,.0f} dollars. <bookmark mark='a'/> Below the range "
            "it holds only ether, so its value falls one for one with ether. <bookmark mark='b'/> Inside, the value "
            "bends: concave, short gamma, the pool's signature. <bookmark mark='c'/> Above, it has sold all its ether "
            "and holds only dollars: the upside is capped. It is a covered call, written continuously."
        ) as vo:
            self.play(FadeIn(g), Create(lo), Create(hi))
            vo.wait_until("a")
            self.play(Create(vc), run_time=2)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def efficiency(self, v):
        rows_ = v["rows"]
        hx = [-3.0, 0.4, 3.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"range around the price", r"liquidity per dollar",
                                                                         r"formula")])
        tab = VGroup(head)
        for r in rows_:
            nm = rf"$\pm{r['pct']:.0f}\%$" if r["w"] < 2 else r"$\times 2$ either way"
            tab.add(VGroup(label(nm, font_size=20), MathTex(rf"{r['eff']:.1f}\times", font_size=28, color=POOL_C),
                           VectorizedPoint()))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.6 - 0.62 * j, 0])
        frm = MathTex(r"\frac{1}{1 - w^{-1/2}}", font_size=40, color=HURDLE).move_to([hx[2], 0.6, 0])
        e1 = rows_[0]["eff"]
        with self.voiceover(
            "How much liquidity a dollar buys. <bookmark mark='a'/> For a range from P over w to P times w, the "
            "multiple over a constant-product position is one over one minus w to the minus one half. "
            f"<bookmark mark='b'/> Plus or minus one percent: about {e1:.0f} times. Plus or minus ten: about "
            f"{rows_[3]['eff']:.0f}. A doubling either way: {rows_[-1]['eff']:.1f}. A provider with a narrow range "
            "earns as much in fees as a full-range one with that many times its capital."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(frm))
            vo.wait_until("a")
            self.play(Indicate(frm, color=HURDLE))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def out_of_range(self, v):
        rows_ = [r for r in v["rows"] if r["w"] <= 1.1]
        hx = [-3.6, 0.0, 3.6]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"range, re-centred each day",
                                                                         r"days the price left it", r"time out of range")])
        tab = VGroup(head)
        for r in rows_:
            tab.add(VGroup(label(rf"$\pm{r['pct']:.0f}\%$", font_size=20),
                           MathTex(rf"{100 * r['days_left']:.0f}\%", font_size=28, color=BAD if r["days_left"] > 0.2 else GREY_A),
                           MathTex(rf"{100 * r['out_share']:.1f}\%", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        r1, r5 = rows_[0], rows_[2]
        with self.voiceover(
            "The price of concentration: leaving the range. Ether in twenty twenty-three, a range centred at each day's "
            f"open. <bookmark mark='a'/> Plus or minus one percent: the price left it on {100 * r1['days_left']:.0f} "
            f"percent of days, and was outside {100 * r1['out_share']:.0f} percent of the time, earning nothing. "
            f"<bookmark mark='b'/> Plus or minus five: {100 * r5['days_left']:.0f} percent of days, "
            f"{100 * r5['out_share']:.1f} percent of the time. Narrow ranges need constant re-centring, and every "
            "re-centring is a trade, with its own cost."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def lvr_scale(self, v):
        rows = [cmath(r"\ell", r"=", r"\tfrac{\sigma^2}{4}\,L\sqrt P", font_size=44, colors={r"\ell": ARB_C}),
                cmath(r"\frac{\ell}{V}", r"\approx", r"\frac{\sigma^2}{8} \times \text{efficiency}", font_size=40),
                cmath(r"\text{fees}/V", r"\approx", r"\text{fee yield} \times \text{efficiency}", font_size=40,
                      colors={r"\text{fees}/V": FEE_C})]
        whys = [why(r"the loss rate per unit of liquidity is the same as in a full-range pool"),
                why(r"so per dollar, near the centre of the range, the loss is multiplied by the efficiency"),
                why(r"and so are the fees: concentration scales the bet, it does not change its sign")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "And the loss scales the same way. <bookmark mark='a'/> Per unit of liquidity, the rate is sigma squared "
            "over four times L root P, as in a full-range pool. <bookmark mark='b'/> So per dollar, near the centre of "
            "the range, the loss is the full-range rate times the efficiency. <bookmark mark='c'/> And so are the fees. "
            "Concentration multiplies the bet; it does not change its sign. If fees beat variance, narrow is better; if "
            "not, narrow loses faster."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def rl_setup(self, rl):
        sig = rl["sig"]
        rows = [cmath(r"\text{world}", r":", rf"\sigma = {100 * sig[0]:.0f}\%\ \text{{or}}\ {100 * sig[1]:.0f}\%,\ "
                      rf"\text{{switching with probability}}\ {rl['switch']:.2f}\ \text{{a day}}", font_size=30),
                cmath(r"\text{action, each day}", r":", r"\text{withdraw, or a range } \times 2,\ \pm 20\%,\ \pm 5\%", font_size=30,
                      colors={r"\text{action, each day}": POOL_C}),
                cmath(r"\text{state}", r":", rf"\text{{yesterday's realised volatility, cut at}}\ {100 * rl['edges'][0]:.0f}\%,\ "
                      rf"{100 * rl['edges'][1]:.0f}\%", font_size=30),
                cmath(r"\text{reward}", r"=", r"\text{fees} - \text{LVR} - \text{re-centring cost}", font_size=32,
                      colors={r"\text{reward}": FEE_C})]
        whys = [why(r"an illustration, not a calibration: two volatility regimes, hidden from the provider"),
                why(r"a position re-centred at each day's open, or none"),
                why(r"what the provider sees: a noisy hint of the regime"),
                why(r"fees from uninformed flow scaled by the range's efficiency (a full-range pool breaks even at 75\% "
                    r"volatility), the exact LVR of the day's path, and 0.1\% to re-centre; the provider hedges its token "
                    r"exposure")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            "Can a provider learn when to concentrate? The plan promised a learned provider, so here it is, in a "
            f"simulated world. <bookmark mark='a'/> Volatility is {100 * sig[0]:.0f} or {100 * sig[1]:.0f} percent, "
            "switching now and then, and the provider cannot see which. <bookmark mark='b'/> Each day it withdraws, or "
            "re-centres a wide, medium or narrow range. <bookmark mark='c'/> It sees only yesterday's realised "
            "volatility. <bookmark mark='d'/> Its reward is fees from uninformed traders, scaled by the range's "
            "efficiency, minus the day's exact loss to arbitrage, minus the cost of re-centring. It hedges its token "
            "exposure, so price direction does not enter."
        ) as vo:
            step(0)
            for k, m_ in enumerate(("a", "b", "c", "d")):
                vo.wait_until(m_)
                if k:
                    step(k)
        self.wait(0.5)
        self.clear_scene()

    def rl_q(self, rl):
        Q = np.asarray(rl["Q"], float)
        N = np.asarray(rl["N"], float)
        names = rl["names"]
        hx = [-4.6, -2.0, 0.5, 3.0, 5.4]
        states = (r"calm", r"between", r"stormy")
        head = VGroup(label(r"yesterday", font_size=16, color=GREY_B),
                      *[label(SHOW[nm], font_size=15, color=GREY_B) for nm in names])
        tab = VGroup(head)
        for s_ in range(Q.shape[0]):
            best = int(np.argmax(Q[s_])) if N[s_].sum() > 0 else -1
            cells = [label(states[s_], font_size=18)]
            for a in range(Q.shape[1]):
                if N[s_, a] == 0:
                    cells.append(label(r"never seen", font_size=14, color=GREY_D))
                else:
                    cells.append(MathTex(rf"{1e4 * Q[s_, a]:+.0f}", font_size=26,
                                         color=GOOD if a == best else GREY_A))
            tab.add(VGroup(*cells))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.9 * j, 0])
        unit = label(r"learned value of each action, basis points of capital a day", font_size=17,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        q_calm = 1e4 * float(Q[0].max())
        with self.voiceover(
            "After four thousand simulated days, what it learned, in basis points of capital a day. <bookmark mark='a'/> "
            f"After a calm day, the narrow range is worth about {q_calm:+.0f}; the wider ones much less. "
            "<bookmark mark='b'/> After a stormy day every range loses, the narrow one most, and withdrawing, worth "
            "zero, is best. The middle state almost never occurs, because the two regimes are far apart."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(unit))
            vo.wait_until("a")
            self.play(FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def rl_results(self, rl):
        ev = rl["eval"]
        order = list(rl["names"]) + ["learned", "oracle"]
        hx = [-3.4, 0.0, 3.4]
        head = VGroup(*[label(t, font_size=16, color=GREY_B) for t in (r"policy, on 2,000 new days", r"bp a day",
                                                                         r"standard deviation")])
        tab = VGroup(head)
        for k in order:
            m = ev[k]["mean_bp"]
            col = GOOD if m > 0.5 else (BAD if m < -0.5 else GREY_A)
            nm = {"learned": r"learned: narrow when calm, out when stormy", "oracle": r"knows the regime"}.get(k, SHOW.get(k, k))
            tab.add(VGroup(label(nm, font_size=17, color=HURDLE if k in ("learned", "oracle") else WHITE),
                           MathTex(f"{m:+.1f}", font_size=26, color=col), MathTex(f"{ev[k]['sd_bp']:.0f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.6 - 0.66 * j, 0])
        narrow = ev["narrow (+-5%)"]["mean_bp"]
        with self.voiceover(
            "Tested on two thousand fresh days. <bookmark mark='a'/> Every fixed range loses on average, the narrow one "
            f"most, {narrow:+.0f} basis points a day, because the stormy days cost more than the "
            "calm days earn. <bookmark mark='b'/> The learned policy, narrow when calm and out when stormy, earns "
            f"{ev['learned']['mean_bp']:+.0f}, close to the {ev['oracle']['mean_bp']:+.0f} of a provider who could see the "
            "regime. Its whole skill is one rule: do not sell volatility when volatility is high."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:5]], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(tab[5]), FadeIn(tab[6]))
        self.wait(0.4)
        self.clear_scene()

    def rl_caveats(self):
        cards = VGroup(
            desk_question(r"the fee level is assumed", r"real fee income depends on uninformed volume, which is lower "
                          r"in calm markets and is shared with every other provider in the range", width=12.4, font_size=19),
            desk_question(r"the world is easy", r"two regimes far apart, and a signal that reveals them; real volatility "
                          r"drifts, and the signal arrives late", width=12.4, font_size=19),
            desk_question(r"the lesson survives", r"providing liquidity is selling volatility, and the value of a learned "
                          r"policy is in timing that sale, the same lesson as Part 11's volatility desk", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What not to conclude. <bookmark mark='a'/> The fee level is assumed: real fee income depends on uninformed "
            "volume, which is shared with every other provider in the range. <bookmark mark='b'/> The world is easy: two "
            "regimes far apart and a signal that reveals them. <bookmark mark='c'/> But the lesson survives: providing "
            "liquidity is selling volatility, and the value of a learned policy is in timing that sale, the lesson of "
            "Part eleven's volatility desk."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a trader buys \$100,000 of ether from the pool of Chapter 2 and accepts up to 1\% slippage. Someone "
                       r"who can order the block's transactions sees the order first. How much can they take?")
        with self.voiceover(
            "Pause and predict. A trader buys a hundred thousand dollars of ether from Chapter two's pool and accepts "
            "up to one percent of slippage. Someone who can order the block's transactions sees the order first. How much "
            "can they take?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
