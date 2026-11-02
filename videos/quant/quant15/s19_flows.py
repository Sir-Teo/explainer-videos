from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, VEGA, illustration, load, real_data, ymd_to_year


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
        g1 = axes([2021, 2025], [float(px.min()) * 0.95, float(px.max()) * 1.05], x_length=10.0, y_length=1.9,
                  ylabel=r"CSI 500 ETF", xticks=[], yticks=[], font_size=14)
        g2 = axes([2021, 2025], [min(0.0, float(vg.min())), float(vg.max()) * 1.1], x_length=10.0, y_length=1.7,
                  ylabel=r"book vega", xticks=[], yticks=[0, round(float(vg.max()), 2)], font_size=14)
        g3 = axes([2021, 2025], [0, float(live.max()) + 1], x_length=10.0, y_length=1.5, ylabel=r"notes alive",
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
                             r"notes alive", 2.6, 16, GREY_A).to_edge(RIGHT, buff=0.3)
        src = real_data(r"the index path is real (510500.SS); the book is stylized", corner=DL)
        with self.voiceover(
            "Now add up a whole book. Issue one snowball every month from 2021 to 2023 on the CSI 500, with the "
            "standard terms, and each day read every live note's vega off chapter eight's table, and sum. "
            "<bookmark mark='a'/> Run the clock. While the index rallies, notes knock out after a few months, and "
            "their vega vanishes with them. As the index sinks through 2022 and 2023, notes stop knocking out, they "
            "pile up, and they drift toward their barriers, where each one's vega is largest. The book's vega "
            "climbs. <bookmark mark='b'/> It peaked at "
            f"{pk['vega']:.3f} per vol point, with {pk['live']} notes alive. Then the barriers broke, in January "
            "2024, and the vega collapsed: knocked-in notes have almost none."
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
            cmath(r"\Delta N_t", r"\approx", r"\Gamma_t S_t\,\Delta S_t,\qquad \text{impact} \propto "
                  r"\sigma\sqrt{Q/V}", font_size=34, colors={r"\Delta N_t": QC.GAMMA}),
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
            "The arithmetic behind the picture. The book's vega is a sum over notes, each read from one table by "
            "its moneyness, its age, and whether it has knocked in. <bookmark mark='p'/> Pause and predict: is it "
            "largest after a rally, or just before the barriers break? The picture answered: just before. "
            "<bookmark mark='a'/> A dealer who wants to stay flat must sell that vega, as options at roughly the "
            "notes' expected lives, ten months to two years. <bookmark mark='b'/> And the gamma becomes a daily "
            "futures trade, gamma times spot times the move. Whether that trade moves prices depends on its size "
            "against the market's volume, the square-root law of Part thirty-seven. That ratio is the part the "
            "record argues about."
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
        side = wrapped_label(r"the dealers' hedge of a long-vega book is a supply of longer-dated options, which "
                             r"weighs on longer-dated implied volatility; when the barriers break, the supply stops and "
                             r"the dealers must buy back, in a falling market", 4.6, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Where does all that vega go? A schematic, not data. Issuers who are long volatility on their notes sell "
            "options to stay flat, at the notes' maturities. <bookmark mark='a'/> That steady supply weighs on "
            "implied volatility at those maturities: the arrows push the term structure down. And when the "
            "barriers break and the vega collapses, the dealers find themselves over-hedged, short options they no "
            "longer need, and must buy them back in a falling, volatile market. The supply turns into demand at the "
            "worst moment."
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
            "The practitioner record says the same, in its own words. Risk.net reported the dealers' vega on "
            "autocalls growing as the underlying falls, to a peak that a UBS strategist put at typically twenty to "
            "twenty-five percent below the issue level; past it, they must buy volatility back, and that is where "
            "hedging costs mount. <bookmark mark='a'/> It also reported desks losing money on autocall hedges after "
            "the HSCEI's fall in 2015 and 2016. The book's vega and the direction of its trades are arithmetic; how "
            "much they moved prices is disputed."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
