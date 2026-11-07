from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, VEGA, illustration, load, real_data, ymd_to_year, axes, data_range, pause_card


class Flows(VoiceoverScene):
    def construct(self):
        v = load("book_vega")
        self.card()
        self.book(v)
        self.derive()
        self.supply()
        self.record()

    def card(self):
        c = chapter_card(15, r"Dealer flows: when the hedges move the market", r"What does a whole book of notes force "
                         r"its issuers to trade?", part=PART)
        with self.voiceover("Chapter fifteen. Dealer flows: when the hedges move the market."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def book(self, v):
        t = ymd_to_year(v["dates"])
        px = np.asarray(v["close"])
        vg = np.asarray(v["vega"])
        gm = np.asarray(v["gamma"])
        live = np.asarray(v["live"])
        n = len(t)
        g1 = axes([2021, 2025], [float(px.min()) * 0.95, float(px.max()) * 1.05], x_length=8.8, y_length=1.9,
                  ylabel=r"CSI 500 ETF", xticks=[], yticks=[], font_size=14)
        g2 = axes([2021, 2025], [min(0.0, float(vg.min())), float(vg.max()) * 1.1], x_length=8.8, y_length=1.7,
                  ylabel=r"book vega", xticks=[], yticks=[0, round(float(vg.max()), 2)], font_size=14)
        g3 = axes([2021, 2025], [0, float(live.max()) + 1], x_length=8.8, y_length=1.5, ylabel=r"notes alive",
                  xticks=[2021, 2022, 2023, 2024, 2025], yticks=[0, int(live.max())], font_size=14)
        G = VGroup(g1, g2, g3).arrange(DOWN, buff=0.25).to_edge(LEFT, buff=0.6).shift(UP * 0.1)
        tr = ValueTracker(0)
        l1 = tracing(g1.ax, t, px, tr, SPOT, stroke_width=2.2)
        l2 = tracing(g2.ax, t, vg, tr, VEGA, stroke_width=2.8)
        l3 = tracing(g3.ax, t, live.astype(float), tr, GREY_A, stroke_width=2.2)
        pk = v["peak"]
        tp = ymd_to_year([pk["date"]])[0]
        mk = Dot(g2.ax.c2p(tp, pk["vega"]), radius=0.09, color=BAD)
        side = wrapped_label(rf"one note of notional 1 issued each month, 2021--2023; each day every live note's issuer "
                             rf"vega is read from chapter 8's table and summed. Peak: {pk['vega']:.3f} per vol point on "
                             rf"{str(pk['date'])[:4]}-{str(pk['date'])[4:6]}-{str(pk['date'])[6:]}, with {pk['live']} "
                             r"notes alive", 3.4, 18, GREY_A).to_edge(RIGHT, buff=0.3)
        src = real_data(r"the index path is real (510500.SS); the book is stylized", corner=DL)
        with self.voiceover(
            f"Now aggregate issuer vega for one hypothetical note issued monthly in 2021 through 2023, each of notional one. This is a retrospective ETF-path reconstruction under fixed model parameters. <bookmark mark='a'/> Each live note is located in an interpolated spot, age and knock-in table; the original calculation clamps relative spot to that table's endpoints. Issuance, aging, early redemption and market moves all affect the aggregate. <bookmark mark='b'/> The peak shown is {pk['vega']:.3f} per volatility point with {pk['live']} live notes. Later knock-ins change the profile, but do not universally eliminate vega. The curve is a model diagnostic, not measured dealer inventory or a backtested hedge return. Its date and height depend on this book and approximation."
        ) as vo:
            self.play(FadeIn(G), FadeIn(src))
            self.add(l1, l2, l3)
            vo.wait_until("a")
            self.play(tr.animate.set_value(n - 1), run_time=9, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(mk, scale=0.5), Flash(mk, color=BAD), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"\mathcal V_t", r"=", r"\sum_i N_i\,\mathcal V\big(S_t / S_{0,i},\ t - t_{0,i},\ KI_{i,t}\big)",
                  font_size=36, colors={r"\mathcal V_t": VEGA}),
            cmath(r"\text{vega sold}", r"\approx", r"\mathcal V_t\ \text{at maturities of 10 months to 2 years}",
                  font_size=34, colors={r"\text{vega sold}": BAD}),
            cmath(r"Q_t", r"\approx", r"-\Gamma_t^{\text{issuer}} S_t\,\Delta S_t,\qquad \text{impact} \propto "
                  r"\sigma\sqrt{Q/V}", font_size=34, colors={r"Q_t": QC.GAMMA}),
        ]
        whys = [why(r"linearity over notes: each priced from one table, by its moneyness, its age and its state"),
                why(r"to stay flat the issuers sell options of about the notes' expected lives (chapter 7: about ten "
                    r"months for a two-year note), bucket by bucket"),
                why(r"the daily futures trade, and the square-root law of Part 37: whether hedging moves prices depends "
                    r"on that trade $Q$ against the market's volume $V$, which the record disputes")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-0.6, buff=0.9, edge=6.9)
        pp = pause_card(r"When is the dealers' aggregate vega largest: after a rally, or just before the barriers break?",
                        width=6.0).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Book vega adds across notes in a common convention, but a single total does not reveal all maturity or smile buckets. <bookmark mark='p'/> When does this book peak? Read the plotted history; it is not a universal rule for every issuance schedule. <bookmark mark='a'/> A policy that neutralizes positive issuer vega may sell options in selected maturity buckets. Expected life alone does not specify that hedge's full sensitivity. <bookmark mark='b'/> Holding state and time fixed, cash rebalancing from issuer gamma is approximately minus spot times issuer gamma times the spot change. State transitions and other effects add terms. The square-root impact expression is an empirical schematic for some execution regimes, not an established causal mapping from these modeled positions to the Chinese market fall."
        ) as vo:
            step(0)
            vo.wait_until("p")
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp))
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def supply(self):
        g = axes([0, 3], [0.15, 0.30], x_length=7.0, y_length=4.0, xlabel=r"option maturity (years)",
                 ylabel=r"implied volatility", xticks=[0.25, 1, 2, 3], yticks=[], font_size=15).to_edge(LEFT, buff=0.8)
        ax = g.ax
        T = np.linspace(0.1, 3, 60)
        base = 0.20 + 0.04 * (1 - np.exp(-T / 0.8))
        push = base - 0.03 * np.exp(-((T - 1.5) / 0.9) ** 2)
        l0 = DashedVMobject(curve(ax, T, base, GREY_B, stroke_width=2.5), num_dashes=40)
        l1 = curve(ax, T, push, IV, stroke_width=3.5)
        arrows = VGroup(*[Arrow(ax.c2p(x, float(np.interp(x, T, base)) + 0.02), ax.c2p(x, float(np.interp(x, T, push))),
                                buff=0.05, stroke_width=3, color=BAD, max_tip_length_to_length_ratio=0.25)
                          for x in (0.8, 1.3, 1.8, 2.3)])
        lab_ = label(r"issuers sell vega", font_size=22, color=BAD).next_to(arrows, UP, buff=0.15)
        tag = label(r"schematic", font_size=20, color=GREY_B).to_corner(UR, buff=0.3)
        side = wrapped_label(r"under a policy of neutralizing positive issuer vega, option selling supplies longer-dated options, which "
                             r"weighs on longer-dated implied volatility; when the barriers break, the supply stops and "
                             r"the dealers may reduce their short-option hedge; actual flows depend on the rest of their book", 4.6, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "This schematic illustrates a conditional mechanism. If issuers are long vega and choose to neutralize it by selling longer-dated options, that hedge adds option supply. <bookmark mark='a'/> Under a downward-sloping demand response it can weigh on implied volatility. If the required hedge then shrinks, buying back the short options can reverse that flow. Neither step is compulsory for every desk: other assets, limits, netting and contract states matter. The arrows are not estimated orders or a fitted volatility response. They separate a plausible channel from a measured causal effect."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Create(l0), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), FadeIn(lab_),
                      TransformFromCopy(l0, l1))
        self.wait(0.4)
        self.clear_scene()

    def record(self):
        cards = VGroup(
            history_card(r"Risk.net", r"peak vega", r"as reported: dealers' vega on autocalls grows as the underlying "
                         r"falls, to a peak typically 20--25\% below the issue level (a UBS strategist's estimate); past "
                         r"the peak they must buy volatility back, which is where hedging costs mount", color=QC.CRISIS,
                         width=6.0, font_size=20),
            history_card(r"Risk.net", r"Korea, 2015--16 and 2024", r"as reported: desks lost money on autocall hedges "
                         r"after the HSCEI fell in 2015--16, and issuers braced again for ``vega misery'' as the index "
                         r"sank toward the same territory; Natixis's 2018 loss (chapter 10) was a hedging model failing "
                         r"in such conditions", color=QC.CRISIS, width=6.0, font_size=20),
        ).arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(UP * 0.3)
        foot = wrapped_label(r"what is arithmetic: the book's vega and gamma, and the direction of the trades they force. "
                             r"What is disputed: how much those trades moved prices", 11.6, 20, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The practitioner record motivates this mechanism but does not turn it into an identity about actual flows. Risk.net reports describe peak-vega regions and difficult autocall hedges; the quoted twenty-to-twenty-five-percent drawdown is a strategist's estimate for particular books. <bookmark mark='a'/> Reports on Korea and Natixis concern their own contracts and market conditions. Our model's aggregate sensitivities are arithmetic conditional on its assumptions. What desks actually traded, and how much those trades moved prices, require separate position and execution evidence. Next, the pricing proxy used in this reconstruction."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
