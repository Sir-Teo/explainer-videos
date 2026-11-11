from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant39.common import prediction_card
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

SHOW = {"withdraw": r"withdraw", "wide (x2)": r"wide, $\times 2$", "medium (+-20%)": 'medium, $w=1.2$',
        "narrow (+-5%)": 'narrow, $w=1.05$'}


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
                why('outside the range the position earns no modeled swap fees; its token or numeraire holdings still have value')]
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
            nm = rf"$w={r['w']:g}$" if r["w"] < 2 else r"$\times 2$ either way"
            tab.add(VGroup(label(nm, font_size=20), MathTex(rf"{r['eff']:.1f}\times", font_size=28, color=POOL_C),
                           VectorizedPoint()))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 2.6 - 0.62 * j, 0])
        frm = MathTex(r"\frac{1}{1 - w^{-1/2}}", font_size=40, color=HURDLE).move_to([hx[2], 0.6, 0])
        e1 = rows_[0]["eff"]
        with self.voiceover(
            f"How much liquidity a dollar buys at the geometric centre. <bookmark mark='a'/> A range from P over w to P times w has efficiency one over one minus w to the minus one half relative to full range at the same price. <bookmark mark='b'/> For w equal to one point zero one, about {e1:.0f} times; for one point one, {rows_[3]['eff']:.0f}; for two, {rows_[-1]['eff']:.1f}. The lower bound is a reciprocal, not a symmetric percentage discount. At equal active liquidity and identical fee allocation, local fee exposure scales too. Real income also depends on volume, competition, time in range and execution costs."
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
            tab.add(VGroup(label(rf"$w={r['w']:g}$", font_size=20),
                           MathTex(rf"{100 * r['days_left']:.0f}\%", font_size=28, color=BAD if r["days_left"] > 0.2 else GREY_A),
                           MathTex(rf"{100 * r['out_share']:.1f}\%", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        r1, r5 = rows_[0], rows_[2]
        with self.voiceover(
            f"Leaving a range changes the position. Each sample day resets its centre to the first observed ether price. <bookmark mark='a'/> For bounds P divided by one point zero one and P times one point zero one, at least one sampled minute lies outside on {100 * r1['days_left']:.0f} percent of days; {100 * r1['out_share']:.0f} percent of sampled observations are outside on average. <bookmark mark='b'/> With w equal to one point zero five, these become {100 * r5['days_left']:.0f} percent of days and {100 * r5['out_share']:.1f} percent of sampled time. A daily-mean share gives each day equal weight. Unobserved intraminute exits are missed; these are not continuous barrier-hit probabilities. Re-centering involves trades and costs."
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
                why('local fee scaling also requires comparable volume and active-liquidity allocation; pathwise performance differs')]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.6, edge=6.9)
        with self.voiceover(
            "Concentration changes local curvature. <bookmark mark='a'/> In range, the continuous fee-free loss rate is sigma squared times liquidity times square root of price, divided by four. It vanishes outside the active range in this model. <bookmark mark='b'/> At the geometric centre, divide by the concentrated position's smaller capital value to get the efficiency multiple of the full-range local loss rate. <bookmark mark='c'/> Fee income has the same local multiple only under comparable active-liquidity allocation and volume. Over a path, price location, range exits, competing liquidity and re-centering costs change the result. A local scaling argument does not prove narrow ranges are globally better."
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
                cmath(r"\text{action, each day}", r":", '\\text{withdraw, or }w\\in\\{2,1.2,1.05\\},\\ [P/w,Pw]', font_size=30,
                      colors={r"\text{action, each day}": POOL_C}),
                cmath(r"\text{state}", r":", rf"\text{{yesterday's realised volatility, cut at}}\ {100 * rl['edges'][0]:.0f}\%,\ "
                      rf"{100 * rl['edges'][1]:.0f}\%", font_size=30),
                cmath(r"\text{reward}", r"=", r"\text{fees} - \text{LVR} - \text{re-centring cost}", font_size=32,
                      colors={r"\text{reward}": FEE_C})]
        whys = [why(r"an illustration, not a calibration: two volatility regimes, hidden from the provider"),
                why(r"a position re-centred at each day's open, or none"),
                why(r"what the provider sees: a noisy hint of the regime"),
                why('chosen external fee yield times centre efficiency and in-range share, less normalized simulated LVR and a 0.1\\% reset charge; benchmark-relative reward')]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.45, edge=6.9)
        with self.voiceover(
            f"A contextual-bandit illustration in a chosen simulated world. <bookmark mark='a'/> Annual volatility is {100 * sig[0]:.0f} or {100 * sig[1]:.0f} percent with a persistent latent regime. <bookmark mark='b'/> Each day chooses withdrawal or a freshly centred multiplicative range; current action does not control tomorrow's regime or observation. <bookmark mark='c'/> The state is a bucket of yesterday's noisy realized-volatility estimate. <bookmark mark='d'/> Reward is an assumed exogenous daily fee yield times centre efficiency and in-range share, less simulated loss-versus-rebalancing divided by initial daily capital and a reset charge. It is a stylized benchmark-relative reward, not a total executable LP return. The model omits hedge financing, fee competition and realistic transaction costs."
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
        unit = label('estimated one-step benchmark-relative reward, bp of daily initial capital', font_size=17,
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
            f"Evaluation uses two thousand fresh simulated days and common daily random seeds across actions. <bookmark mark='a'/> In this chosen run the narrow fixed action averages {narrow:+.0f} basis points of benchmark-relative reward a day. Other fixed actions and withdrawal provide the displayed baselines. <bookmark mark='b'/> The learned policy averages {ev['learned']['mean_bp']:+.0f}, versus {ev['oracle']['mean_bp']:+.0f} for a regime-informed action selected using extra Monte Carlo samples. These are one training and evaluation design, with serially dependent regimes, not evidence of live skill or a confidence interval. The oracle has more information and a separate selection budget; it is not an equally informed competitor."
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
            desk_question('a conditional simulation result', 'one seeded contextual-bandit run does not establish a general timing rule or executable net LP return', width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        self.add(cards[0])
        with self.voiceover(
            "What this experiment supports. <bookmark mark='a'/> Fee yield is chosen externally and scales by a simple efficiency factor, rather than arising from traders competing across ranges. <bookmark mark='b'/> Two well-separated regimes and a lagged volatility bucket make the prediction problem easier than a real market; one seeded training run does not quantify training uncertainty. <bookmark mark='c'/> The learner estimates conditional one-step action values, with sample-mean updates and no continuation-value term. This is a contextual bandit, not a general long-horizon liquidity-management policy. Its positive benchmark-relative reward depends on its assumed world and does not establish an investment return."
        ) as vo:
            for k, m_ in enumerate(("a", "b", "c")):
                vo.wait_until(m_)
                if k:
                    self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = prediction_card(r"a trader buys \$100,000 of ether from the pool of Chapter 2 and accepts up to 1\% slippage. Someone "
                       r"who can order the block's transactions sees the order first. How much can they take?")
        with self.voiceover(
            "Pause and predict. A trader buys a hundred thousand dollars of ether from Chapter two's pool and accepts "
            "up to one percent of slippage. Someone who can order the block's transactions sees the order first. How much "
            "can they take?"
        ):
            self.play(FadeIn(q))
        self.wait(6)
        self.clear_scene()
