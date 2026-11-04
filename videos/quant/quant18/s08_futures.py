from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, PAR, PART, ask, illustration, load

CTD = QC.GAIN


class Futures(VoiceoverScene):
    def construct(self):
        f = load("futures")
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
            label(r"deliverable: any note with 6.5 to 10 years left on the month's first day, first issued for at "
                  r"most 10 years", font_size=22, color=GREY_A),
            label(rf"December 2025: {n} notes qualify, coupons from "
                  rf"{min(q['coupon'] for q in f['notes']):.3g}\% to {max(q['coupon'] for q in f['notes']):.3g}\%",
                  font_size=22, color=PAR),
            label(r"the seller chooses which one, and when in the month", font_size=22, color=GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.7)
        with self.voiceover(
            "A Treasury future is a contract to deliver a bond later at a price agreed now. The ten-year note future on "
            "the Chicago Board of Trade calls for a hundred thousand dollars of face value. <bookmark mark='a'/> But not "
            "of one particular note: of any note with six and a half to ten years left, first issued for at most ten. "
            f"For December 2025, {n} different notes qualify, with different coupons and maturities. "
            "<bookmark mark='b'/> The seller chooses which to deliver. That choice is worth money, and it makes this "
            "contract a small puzzle in curve arithmetic."
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
                cmath(r"\text{CTD}", r"=", r"\arg\min_i\ \big(P_i - F\,\text{CF}_i\big) \approx \arg\min_i\ P_i/\text{CF}_i",
                      font_size=40, colors={r"\text{CTD}": CTD})]
        whys = [why(r"each note's conversion factor: its price per 1 at a 6\% yield, term cut to whole quarters "
                    r"(the House's \texttt{conversion\_factor})"),
                why(r"the buyer pays the futures price scaled by the factor, plus the coupon accrued so far"),
                why(r"the seller buys the note at $P_i$ and receives $F\,\text{CF}_i$: the gross basis is what delivering "
                    r"it costs"),
                why(r"so the seller delivers the cheapest to deliver; ignoring carry, the note with the lowest price "
                    r"per unit of factor")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "To make different notes comparable, the exchange gives each a conversion factor: its price, per dollar of "
            "face, if its yield were six percent. <bookmark mark='a'/> The buyer pays the futures price times that "
            "factor, plus accrued interest. <bookmark mark='b'/> A seller who buys note i in the market at its price "
            "and delivers it receives F times its factor. The difference is the basis. <bookmark mark='c'/> So the "
            "seller delivers whichever note is cheapest relative to its factor: the cheapest to deliver. The futures "
            "price ends up tracking that note."
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
        g = axes([2032.3, 2036], [0, 3.2], x_length=8.4, y_length=4.4, xlabel=r"maturity of the deliverable note",
                 ylabel=r"gross basis, $P - F\,\text{CF}$, per 100", xticks=[2033, 2034, 2035], yticks=[0, 1, 2, 3],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        k = base["ctd"]
        dots = VGroup()
        for i, (x, b) in enumerate(zip(mat, basis)):
            col = CTD if i == k else PAR
            dots.add(VGroup(Line(ax.c2p(x, 0), ax.c2p(x, min(b, 3.2)), color=col, stroke_width=4),
                            Dot(ax.c2p(x, min(b, 3.2)), radius=0.06, color=col)))
        q = notes[k]
        side = VGroup(
            label(r"priced off the Fed's curve, 28 November 2025", font_size=19, color=GREY_A),
            MathTex(rf"F^* = {f['base_F']:.3f}", font_size=34),
            label(rf"cheapest: {q['coupon']:.3g}\% of {q['maturity'] // 10000}-{q['maturity'] // 100 % 100:02d}", font_size=24,
                  color=CTD),
            MathTex(rf"\text{{CF}} = {q['cf_factor']:.4f}", font_size=30, color=CTD),
            wrapped_label(r"$F^*$: the futures price at which delivering the cheapest note costs nothing, ignoring carry "
                          r"and the timing option", 4.0, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "Here is the December 2025 basket, each note priced off the Fed's fitted curve at the end of November. The "
            "height is what delivering it would cost, at the futures price that makes the cheapest one cost nothing. "
            f"<bookmark mark='a'/> With yields near four percent, the cheapest is a short one: the "
            f"{q['coupon']:g} percent note maturing in {q['maturity'] // 10000}. The long notes cost a point or more "
            "to deliver."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.08, run_time=3), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Indicate(dots[k], color=CTD), LaggedStart(*[FadeIn(s_) for s_ in side[1:]], lag_ratio=0.3))
        self.add(illustration(r"TreasuryDirect auction records; the Fed's GSW curve; CBOT conversion factors"))
        self.wait(0.4)
        self.clear_scene()

    def switch(self, f):
        notes = f["notes"]
        tab = f["table"]
        sh = np.asarray(f["shifts"], float)
        B = np.array([r_["basis"] for r_ in tab])  # shifts x notes
        y10 = np.array([r_["y10"] for r_ in tab])
        g = axes([y10[0], y10[-1]], [0, 4], x_length=8.2, y_length=4.4, xlabel=r"10-year zero yield after a parallel "
                 r"shift, \%", ylabel=r"gross basis per 100", xticks=[1, 3, 5, 7], yticks=[0, 1, 2, 3, 4],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        mat = np.array([q["maturity"] for q in notes])
        order = np.argsort(mat)
        cols = [interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), r / (len(order) - 1)) for r in
                range(len(order))]
        lines = VGroup()
        for r, i in enumerate(order):
            lines.add(curve(ax, y10, np.clip(B[:, i], 0, 4), cols[r], stroke_width=2))
        six = DashedLine(ax.c2p(6, 0), ax.c2p(6, 4), color=WHITE, stroke_width=2)
        six_l = label(r"6\%", font_size=18).next_to(six, UP, buff=0.05)
        ctd_idx = np.array([r_["ctd"] for r_ in tab])
        floor = VGroup(*[Dot(ax.c2p(y10[j], 0), radius=0.05, color=cols[list(order).index(ctd_idx[j])])
                         for j in range(len(y10))])
        sw = [float(np.interp(s_, sh, y10)) for s_ in f["switch"]]
        leg = legend([(QC.SPOT, r"shortest note"), (QC.OPTION, r"longest note")], font_size=18).to_edge(RIGHT,
                                                                                                  buff=0.5).shift(UP * 1.6)
        side = VGroup(
            label(r"dots on the axis: the colour of the cheapest", font_size=18, color=GREY_A),
            wrapped_label(rf"the cheapest jumps from the short end to the long end as the 10-year passes about "
                          rf"{max(sw):.1f}\%", 3.8, 19, CTD),
            wrapped_label(r"below 6\% the factors overstate long notes' prices relative to short ones; above 6\%, the "
                          r"reverse. Duration decides which way the error runs", 3.8, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        with self.voiceover(
            "Now move the whole curve up and down by up to four points and recompute every note's basis. Each line is "
            "one note, blue for the shortest, pink for the longest. <bookmark mark='a'/> The dots along the bottom "
            "mark which note is cheapest at each level. At low yields it is always a short note; at high yields, "
            "always the longest. <bookmark mark='b'/> The switch happens near "
            f"{max(sw):.1f} percent. The reason is the six percent in the factor: below six percent, factors understate "
            "how much long notes have gained relative to short ones, so long notes look expensive; above six, the "
            "reverse. <bookmark mark='c'/> So the future's own duration changes with the level of rates: the seller's "
            "option to switch is short convexity for the buyer. This is the contract in Part 2's basis trade."
        ) as vo:
            self.play(FadeIn(g), Create(lines), FadeIn(leg), FadeIn(six), FadeIn(six_l), run_time=3)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in floor], lag_ratio=0.02, run_time=2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.wait(0.5)
        q = ask(r"yields fall two points. Does the cheapest note get shorter or longer, and what happens to the "
                r"future's duration?")
        with self.voiceover("Yields fall two points. Does the cheapest note get shorter or longer? And what happens to "
                            "the future's duration?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
