from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, PAR, PART, ask, fit_right, illustration, load

from videos.quant.quant18.futures_example import delivery_example

CTD = QC.GAIN


class Futures(VoiceoverScene):
    def construct(self):
        f = delivery_example(load("futures"))
        self.card()
        self.contract(f)
        self.factor()
        self.basket(f)
        self.switch(f)

    def card(self):
        c = chapter_card(12, r"Treasury futures and the cheapest to deliver", r"Which bond does the seller hand over?",
                         part=PART)
        with self.voiceover("Chapter twelve. Treasury futures, and the bond the seller chooses."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def contract(self, f):
        n = len(f["notes"])
        spec = VGroup(
            label(r"The 10-year Treasury note future (CBOT)", font_size=30),
            label(r"\$100{,}000 face of a note, delivered in the contract month", font_size=22, color=GREY_A),
            wrapped_label(r"December 2025 grade: 6.5 to under 8 years remaining, rounded down to quarters; original term at most 10 years", 11.8, 22, GREY_A),
            label(rf"grade-corrected saved example: {n} notes, coupons from "
                  rf"{min(q['coupon'] for q in f['notes']):.3g}\% to {max(q['coupon'] for q in f['notes']):.3g}\%",
                  font_size=22, color=PAR),
            label(r"the seller chooses which one, and when in the month", font_size=22, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.7)
        with self.voiceover(
            f"Treasury futures are margined contracts with daily variation settlement and a delivery mechanism. The classic ten-year note contract calls for a hundred thousand dollars of face value. <bookmark mark='a'/> The December 2025 CBOT rule requires six-and-a-half to under eight years remaining, rounded down to quarters, with original term at most ten years. This illustration has {n} rule-eligible notes with synthetic prices. <bookmark mark='b'/> The seller has quality and timing choices, subject to exchange rules. We isolate a carry-free quality-choice approximation rather than reproduce an exchange settlement price."
        ) as vo:
            self.play(FadeIn(spec[0]), FadeIn(spec[1]))
            vo.wait_until("a")
            self.play(FadeIn(spec[2]), FadeIn(spec[3]))
            vo.wait_until("b")
            self.play(FadeIn(spec[4]))
        self.wait(0.4)
        self.clear_scene()

    def factor(self):
        rows = [cmath(r"\text{CF}", r"=", r"\frac{1}{100}\,P\big(\text{coupon},\ \text{term};\ y = 6\%\big)", font_size=42,
                      colors={r"\text{CF}": PAR}),
                cmath(r"\text{invoice}", r"=", r"F \times \text{CF} + \text{accrued interest}", font_size=42,
                      colors={r"\text{invoice}": WHITE}),
                cmath(r"\text{basis}_i", r"=", r"P_i - F \times \text{CF}_i", font_size=42, colors={r"\text{basis}_i": BAD}),
                cmath(r"F^*", r"=", r"\min_i P_i/\mathrm{CF}_i,\quad i^*\in\arg\min_i P_i/\mathrm{CF}_i",
                      font_size=36, colors={r"F^*": CTD})]
        whys = [why(r"each note's factor: clean price per 1 at 6\% nominal yield, compounded semiannually; term rounded down to quarters (House \texttt{conversion\_factor})"),
                why(r"the buyer pays the futures price scaled by the factor, plus the coupon accrued so far"),
                why(r"the seller buys the note at $P_i$ and receives $F\,\text{CF}_i$: the gross basis is what delivering "
                    r"it costs"),
                why(r"at this synthetic zero-minimum-basis price, $i^*$ has zero gross basis and all other bases are nonnegative; arbitrary-$F$ rankings can differ")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "A conversion factor approximates the note's clean price per dollar at a six-percent nominal yield compounded semiannually, using the exchange's maturity-rounding convention. Here the House computes factors; an actual delivery requires the exchange's published factors and rules. <bookmark mark='a'/> Per hundred face, the invoice is the futures price times the factor, plus accrued interest. A hundred-thousand-dollar contract scales this by a thousand. <bookmark mark='b'/> Gross basis is clean cash price minus futures price times the factor. Funding, coupon carry and delivery timing are omitted here. <bookmark mark='c'/> Define the synthetic price F star as the minimum clean-price-to-factor ratio. At that price the selected note has zero gross basis and others are nonnegative. Minimizing gross basis at an arbitrary quoted futures price is not generally identical to minimizing that ratio. Neither rule alone captures full financed delivery economics."
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

    def basket(self, f):
        notes = f["notes"]
        tab = f["table"]
        base = tab[list(f["shifts"]).index(0)]
        basis = np.asarray(base["basis"])
        mat = np.array([q["maturity"] // 10000 + (q["maturity"] // 100 % 100 - 1) / 12 for q in notes])
        g = axes([2032.3, 2034], [0, 1.4], x_length=8.4, y_length=4.4, xlabel=r"maturity of the deliverable note",
                 ylabel=r"gross basis, $P - F\,\text{CF}$, per 100", xticks=[2033, 2034], yticks=[0, 0.5, 1],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        k = base["ctd"]
        dots = VGroup()
        for i, (x, b) in enumerate(zip(mat, basis)):
            col = CTD if i == k else PAR
            dots.add(VGroup(Line(ax.c2p(x, 0), ax.c2p(x, b), color=col, stroke_width=4),
                            Dot(ax.c2p(x, b), radius=0.06, color=col)))
        q = notes[k]
        side = VGroup(
            wrapped_label(r"synthetic prices: 28 November curve, 1 December cash-flow origin", 4.0, 18, GREY_A),
            MathTex(rf"F^* = {f['base_F']:.3f}", font_size=34),
            label(rf"cheapest: {q['coupon']:.3g}\% of {q['maturity'] // 10000}-{q['maturity'] // 100 % 100:02d}", font_size=24,
                  color=CTD),
            MathTex(rf"\text{{CF}} = {q['cf_factor']:.4f}", font_size=30, color=CTD),
            wrapped_label(r"$F^*$ is a carry-free zero-minimum-gross-basis surrogate, not an observed futures quote. Dates, repo and delivery options require full valuation", 4.0, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"The eleven grade-corrected notes use synthetic prices recovered from the original saved basis and price-factor identity. The curve is dated November twenty-eighth, 2025, while cash-flow times and accruals use December first. This mixed-date simplification omits the intervening carry and is not an executable quote. <bookmark mark='a'/> At the unshifted curve, the selected note has coupon {q['coupon']:g} percent and matures in {q['maturity'] // 10000}. F star is {f['base_F']:.3f}, and other notes' gross bases reach about {float(basis.max()):.2f} per hundred. All values are shown. The zero is imposed by the surrogate definition; it is not evidence of a market arbitrage."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08, run_time=3), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(dots[k], color=CTD), LaggedStart(*[FadeIn(s_) for s_ in side[1:]], lag_ratio=0.3))
        self.add(illustration(r"TreasuryDirect records; GSW synthetic prices; House factors; grade: CBOT filing 25-099"))
        self.wait(0.4)
        self.clear_scene()

    def switch(self, f):
        notes = f["notes"]
        tab = f["table"]
        sh = np.asarray(f["shifts"], float)
        B = np.array([r_["basis"] for r_ in tab])  # shifts x notes
        y10 = np.array([r_["y10"] for r_ in tab])
        g = axes([y10[0], y10[-1]], [0, 7], x_length=7.4, y_length=4.4, xlabel=r"10-year continuous zero yield after parallel shift, \%", ylabel=r"gross basis per 100", xticks=[1, 3, 5, 7], yticks=[0, 2, 4, 6],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        mat = np.array([q["maturity"] for q in notes])
        order = np.argsort(mat)
        cols = [interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), r / (len(order) - 1)) for r in
                range(len(order))]
        lines = VGroup()
        for r, i in enumerate(order):
            lines.add(curve(ax, y10, B[:, i], cols[r], stroke_width=2))
        ctd_idx = np.array([r_["ctd"] for r_ in tab])
        floor = VGroup(*[Dot(ax.c2p(y10[j], 0), radius=0.05, color=cols[list(order).index(ctd_idx[j])])
                         for j in range(len(y10))])
        sw = [float(np.interp(s_, sh, y10)) for s_ in f["switch"]]
        switch_txt = ", ".join(f"{v:.1f}" for v in sw)
        leg = legend([(QC.SPOT, r"shortest note"), (QC.OPTION, r"longest note")], font_size=18).to_edge(RIGHT,
                                                                                                  buff=0.5).shift(UP * 1.6)
        side = VGroup(
            label(r"dots on the axis: the colour of the cheapest", font_size=18, color=GREY_A),
            wrapped_label(rf"10 bp shock-grid switch readings, in 10y yield percent: {switch_txt}", 3.4, 19, CTD),
            wrapped_label(r"Six percent is the factor reference yield, not a universal switch threshold. Coupon, maturity, curve shape and carry affect the selected note.", 3.4, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        fit_right(side)
        with self.voiceover(
            f"Now shift the zero curve in ten-basis-point steps from minus four to plus four percentage points, and recompute the corrected basket. Every basis value is retained. <bookmark mark='a'/> Axis dots identify the selected note at each tested shock. The lowest-yield endpoint selects the shortest maturity and the highest-yield endpoint selects the longest in this basket; intermediate selections also occur. <bookmark mark='b'/> The five detected grid switches occur at ten-year yields of {switch_txt} percent. These are grid readings, not exact switching thresholds. The factor's six-percent reference yield is not a universal switch point. <bookmark mark='c'/> Locally, away from a switch, sensitivity scales approximately with the selected bond's risk divided by its conversion factor. The minimum-price envelope changes slope when the deliverable changes. Funding, repo specialness and timing options would change a real contract's hedge."
        ) as vo:
            self.play(FadeIn(g), Create(lines), FadeIn(leg), run_time=3)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in floor], lag_ratio=0.02, run_time=2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.wait(0.5)
        q = ask(r"In this saved model, the 10-year yield falls from 7\% to 5\%. How does the selected note change? Is the same change guaranteed from every starting yield?")
        with self.voiceover('In this saved model, the ten-year yield falls from seven to five percent. How does the selected note change? Is the same change guaranteed from every starting yield?'):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Here it moves to a shorter note after crossing the grid switches. A move that crosses no switch can retain its deliverable. Compute hedge sensitivity with the factor and full delivery economics.", 11.8, 26, CTD).move_to(ORIGIN)
        with self.voiceover("Here it moves to a shorter note after crossing the grid switches. A move that crosses no switch can retain its deliverable. Compute hedge sensitivity with the conversion factor and full delivery economics."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
