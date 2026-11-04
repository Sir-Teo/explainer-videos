from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, CARRY, GOOD, OIL, PART, load

PRICE, INV, SPR = OIL, QC.SPOT, QC.IMPLIED


class Research(VoiceoverScene):
    def construct(self):
        t = load("storage_theory")
        self.card()
        self.equilibrium()
        self.solution(t)
        self.working(t)
        self.data(t)
        self.puzzle(t)
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The competitive storage model", r"Can rational storers explain spikes, backwardation and the "
                          r"Working curve?", part=PART)
        with self.voiceover("For the researcher: Chapter 7 drew Holbrook Working's curve by hand: the futures spread "
                            "against inventories, flat in plenty, plunging in scarcity. Here is the equilibrium model "
                            "that produces it, solved exactly, checked against forty years of crude oil, and the famous "
                            "fact it cannot explain."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def equilibrium(self):
        rows = [cmath(r"x_t", r"=", r"I_{t-1} + z_t,\qquad p_t = P(x_t - I_t)", font_size=32, colors={r"x_t": INV}),
                cmath(r"P(x_t - I_t) + k", r"\ge", r"\beta\,\mathbb E_t\big[p_{t+1}\big],\ \ \text{with equality if } I_t > 0",
                      font_size=30, colors={r"P(x_t - I_t) + k": PRICE}),
                cmath(r"f(x)", r"=", r"\max\Big\{P(x),\ \beta\,\mathbb E\big[f(I^*(x) + z')\big] - k\Big\}", font_size=30,
                      colors={r"f(x)": PRICE}),
                cmath(r"F_t - p_t", r"=", r"\begin{cases} k + (\beta^{-1} - 1)\,p_t\ \text{(full carry)} & I_t > 0 \\ "
                      r"\text{negative (backwardation)} & I_t = 0 \end{cases}", font_size=28, colors={r"F_t - p_t": SPR})]
        whys = [why(r"availability is what was stored plus the new harvest (or production); what is not stored is consumed, "
                    r"and inverse demand $P$ sets the price"),
                why(r"competitive storers buy today, pay the cost $k$, and sell next period: in equilibrium the "
                    r"discounted expected price cannot exceed today's plus the cost, and equals it whenever anyone stores"),
                why(r"so the price is a function of availability alone, the fixed point of this equation (Gustafson 1958; "
                    r"Williams and Wright 1991; Deaton and Laroque 1992)"),
                why(r"with risk-neutral storers the future is the expected price: at full carry when stocks are positive, and "
                    r"below spot when they run out. Inventories cannot be negative, and that one constraint does "
                    r"everything")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-0.3, buff=0.44, edge=6.9)
        with self.voiceover(
            "The model has one constraint. <bookmark mark='a'/> What is available is what was stored plus the new "
            "harvest; what is not stored is consumed, and demand sets the price. <bookmark mark='b'/> Competitive "
            "storers buy today, pay a storage cost, and sell next period. So the discounted expected price can never "
            "exceed today's plus the cost, and equals it whenever anyone stores. <bookmark mark='c'/> The price is then "
            "a function of availability alone, the fixed point of this equation. <bookmark mark='d'/> And with "
            "risk-neutral storers the future price is the expected price: at full carry whenever stocks are positive, "
            "and below spot when they run out. Inventories cannot go negative. That one inequality does everything."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def solution(self, t):
        m = t["model"]
        x = np.asarray(m["x"])
        f = np.asarray(m["f"])
        I = np.asarray(m["I"])
        g = axes([0.5, 3.0], [0, 3.4], x_length=7.8, y_length=4.2, xlabel=r"availability $x$ (mean harvest 1)",
                 ylabel=r"price $f(x)$, and inventory carried $I(x)$", xticks=[0.5, 1, 1.5, 2, 2.5, 3],
                 yticks=[0, 1, 2, 3], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        pd_ = curve(ax, x, np.minimum(np.maximum(x, 0.55) ** -2.0, 3.4), GREY_B, stroke_width=2)
        pf = curve(ax, x, np.minimum(f, 3.4), PRICE, stroke_width=3.5)
        iv = curve(ax, x, I, INV, stroke_width=3)
        kink = x[np.argmax(I > 1e-6)]
        kl = DashedLine(ax.c2p(kink, 0), ax.c2p(kink, 3.4), color=GREY_C, stroke_width=1.5)
        kt = label(r"storage begins", font_size=14, color=GREY_B).next_to(ax.c2p(kink, 3.4), DOWN, buff=0.08)
        leg = legend([(GREY_B, r"consume everything: $P(x)$"), (PRICE, r"equilibrium price $f(x)$"),
                      (INV, r"inventory carried $I(x)$")], font_size=16).to_edge(RIGHT, buff=0.3).shift(UP * 1.4)
        fit_right(leg)
        p = t["params"]
        side = wrapped_label(rf"demand elasticity {p['elasticity']}, harvests with standard deviation {p['harvest_sd']}, "
                             rf"interest 1\% and storage cost {100 * p['k']:.1f}\% of the mean price per period; time iteration "
                             rf"converged in {m['iterations']} steps", 3.3, 14, GREY_A).next_to(leg, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Solve it by time iteration: guess a price function, compute what storers would carry, and repeat until "
            "nothing changes. <bookmark mark='a'/> Without storage, the price would simply be demand at whatever is "
            "available. <bookmark mark='b'/> With it, plenty is smoothed: storers buy when availability is high and "
            "the price is flattened. <bookmark mark='c'/> But below the kink, nobody stores, and the price follows the "
            "steep demand curve: storage can carry a surplus forward, never a shortage backward."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(pd_), FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Create(pf), Create(iv), FadeIn(leg[1]), FadeIn(leg[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(kl), FadeIn(kt))
        self.wait(0.4)
        self.clear_scene()

    def working(self, t):
        m = t["model"]
        I = np.asarray(m["I"])
        sp = 100 * np.asarray(m["spread"])
        o = np.argsort(I)
        g = axes([-0.05, 1.6], [-30, 4], x_length=7.8, y_length=4.2, xlabel=r"inventory carried $I$",
                 ylabel=r"one-period spread $(F - p)/p$, \%", xticks=[0, 0.5, 1.0, 1.5], yticks=[-30, -20, -10, 0],
                 font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(-0.05, 0), ax.c2p(1.6, 0), color=GREY_C, stroke_width=1.2)
        pos = I > 1e-6
        line = curve(ax, I[pos], sp[pos], SPR, stroke_width=3.5)
        stock = VGroup(*[Dot(ax.c2p(0, max(v, -30)), radius=0.04, color=BAD) for v in sp[~pos][::12]])
        stats = VGroup(MathTex(rf"\text{{stock-outs}}:\ {100 * m['stockout_share']:.0f}\%\ \text{{of periods}}", font_size=24),
                       MathTex(rf"\text{{price skewness}}:\ {m['price_skew']:.1f}", font_size=24),
                       MathTex(rf"\text{{price autocorrelation}}:\ {m['price_ac1']:.2f}", font_size=24)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        fit_right(stats)
        side = wrapped_label(r"red: the stock-out states, all at zero inventory, with spreads down to $-66\%$; the "
                             r"statistics from 200{,}000 simulated periods", 3.3, 14, GREY_A).next_to(stats, DOWN, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "And the futures spread. <bookmark mark='a'/> Whenever anything is stored, the spread sits at full carry, "
            "interest plus storage, a flat line: Working's contango. <bookmark mark='b'/> At zero inventory it falls off "
            "a cliff, and the deeper the shortage the steeper the backwardation. Working's curve, derived rather than "
            f"drawn. <bookmark mark='c'/> Simulated, the model stocks out {100 * m['stockout_share']:.0f} percent of the "
            f"time, and those episodes give the price a skewness of {m['price_skew']:.1f}: rare, violent spikes, as "
            "commodity prices have."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side))
            vo.wait_until("a")
            self.play(Create(line), run_time=1.3)
            vo.wait_until("b")
            self.play(FadeIn(stock))
            vo.wait_until("c")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
        self.wait(0.4)
        self.clear_scene()

    def data(self, t):
        d = t["data"]
        dev = 100 * np.asarray(d["dev"])
        sp = 100 * np.asarray(d["spread"])
        g = axes([-25, 45], [-12, 8], x_length=7.8, y_length=4.2, xlabel=r"US commercial crude stocks, \% above their "
                 r"5-year seasonal norm", ylabel=r"second WTI future over the first, \% (monthly average)",
                 xticks=[-20, 0, 20, 40], yticks=[-10, -5, 0, 5], font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(-25, 0), ax.c2p(45, 0), color=GREY_C, stroke_width=1.2)
        ok = (dev > -25) & (dev < 45) & (sp > -12) & (sp < 8)
        dots = VGroup(*[Dot(ax.c2p(a_, b_), radius=0.03, color=OIL, fill_opacity=0.5) for a_, b_ in zip(dev[ok], sp[ok])])
        bins = d["bins"]
        bl = VGroup(curve(ax, [100 * b_["dev"] for b_ in bins], [100 * b_["spread"] for b_ in bins], WHITE, stroke_width=3.5),
                    *[Dot(ax.c2p(100 * b_["dev"], 100 * b_["spread"]), radius=0.07, color=WHITE) for b_ in bins])
        side = wrapped_label(rf"EIA: NYMEX WTI contracts 1 and 2, daily, and weekly stocks excluding the SPR; {d['n']} "
                             rf"months, 1990--2020; white: the means by decile of the inventory deviation; correlation "
                             rf"{d['corr']:.2f}; {100 * d['share_backwardation']:.0f}\% of months in backwardation", 3.3, 14,
                             GREY_A).to_edge(RIGHT, buff=0.3).shift(UP * 0.8)
        fit_right(side)
        lo, hi = bins[0], bins[-1]
        with self.voiceover(
            "Now crude oil. Thirty-one years of months: the spread between the second and first WTI futures, against "
            "US commercial stocks relative to their seasonal norm. <bookmark mark='a'/> The cloud is noisy, but the "
            f"decile means trace Working's curve: in the scarcest tenth the spread averages {100 * lo['spread']:.1f} "
            f"percent a month, backwardation; in the most plentiful, {100 * hi['spread']:+.1f}, near full carry. "
            "<bookmark mark='b'/> And the far right is where storage fills up: April 2020, when the curve's contango "
            "outran the cost of carry and the front contract went negative, Chapter 10's story."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(bl), run_time=1.3)
            vo.wait_until("b")
            self.wait(0.1)
        self.wait(0.4)
        self.clear_scene()

    def puzzle(self, t):
        m, a = t["model"], t["data_ac"]
        rows = [(r"model: price autocorrelation, one period", rf"{m['price_ac1']:.2f}"),
                (r"WTI: monthly log price autocorrelation, one month", rf"{a['monthly_log_price_ac1']:.2f}"),
                (r"WTI: twelve months", rf"{a['monthly_log_price_ac12']:.2f}")]
        tab = VGroup()
        for j, (a_, v) in enumerate(rows):
            r_ = VGroup(label(a_, font_size=20, color=GREY_A), MathTex(v, font_size=30, color=BAD if j else PRICE))
            r_[0].move_to([-1.6, 1.6 - 0.8 * j, 0]).align_to(np.array([-6.0, 0, 0]), LEFT)
            r_[1].move_to([5.0, 1.6 - 0.8 * j, 0])
            tab.add(r_)
        note_ = why(r"Deaton and Laroque (1992, 1996) found the same for thirteen commodities: the storage model gets "
                    r"the skewness and the spikes right and the persistence badly wrong. Cafiero, Bobenrieth, Bobenrieth "
                    r"and Wright (2011) argue a finer numerical solution and different demand narrow the gap; "
                    r"serially correlated supply and demand shocks close more of it").to_edge(DOWN, buff=0.5)
        if note_.width > 12.4:
            note_.scale_to_fit_width(12.4)
        with self.voiceover(
            "But one fact it cannot match. <bookmark mark='a'/> In the model, prices forget quickly: an "
            f"autocorrelation of {m['price_ac1']:.2f} per period. Oil's monthly price has an autocorrelation of "
            f"{a['monthly_log_price_ac1']:.2f}, and {a['monthly_log_price_ac12']:.2f} even a year apart. "
            "<bookmark mark='b'/> Angus Deaton and Guy Laroque found this in 1992 for thirteen commodities: the model "
            "gets the spikes and the skewness right, and the persistence badly wrong. Later work argues that finer "
            "numerical solutions and different demand curves narrow the gap, and persistent shocks to supply and demand "
            "close more of it."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: persistence", r"how much of commodity price persistence is storage and how much is "
                          r"persistent shocks to supply, demand or storage capacity is still argued", width=12.4,
                          font_size=18),
            desk_question(r"open: risk premia in the curve", r"with risk-averse storers and hedgers (Keynes's normal "
                          r"backwardation) the spread is no longer the expected price change; separating the two in data "
                          r"is unsettled", width=12.4, font_size=18),
            desk_question(r"open: capacity limits", r"storage tanks fill: an upper bound on inventory (April 2020) adds a "
                          r"second kink, and models with both bounds and financial traders are young", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> How much of commodity price persistence is storage, and how much "
            "is persistent shocks to supply, demand or storage capacity, is still argued. <bookmark mark='b'/> With "
            "risk-averse storers and hedgers, Keynes's normal backwardation, the spread is no longer the expected price "
            "change, and separating the two in data is unsettled. <bookmark mark='c'/> And tanks fill up: an upper bound "
            "on inventory, April 2020's lesson, adds a second kink, and models with both bounds and financial traders "
            "are young."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"spot oil is \$70, the one-month rate 0.4\%, and storage costs \$0.30 a barrel a month. What is the "
                       r"most the one-month future can trade above spot? Below it, how far can it go?")
        with self.voiceover(
            "Pause and predict. Spot oil at seventy dollars, a one-month rate of point four percent, and storage at "
            "thirty cents a barrel a month. What is the most the one-month future can trade above spot? And below it, "
            "how far can it go?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
