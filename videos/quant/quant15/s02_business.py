from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, CASH, GOOD, IV, OPT, PART, SPOT, illustration, load, axes, data_range, pause_card


class Business(VoiceoverScene):
    def construct(self):
        d = load("decompose")
        self.card()
        self.engine(d)
        self.derive(d)
        self.funding(d)
        self.players()

    def card(self):
        c = chapter_card(1, r"Anatomy of a note, and the margin", r"What is a structured note made of, and who keeps "
                         r"the difference?", part=PART)
        with self.voiceover("Chapter one. The anatomy of a note, and the margin."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def engine(self, d):
        b = d["blocks"]
        c = d["coupon"]
        g = axes([0, 1], [-0.1, 1.1], x_length=1.0, y_length=6.0, ylabel=r"value per 1 of notional", xticks=[],
                 yticks=[0, 0.25, 0.5, 0.75, 1.0], font_size=15).to_edge(LEFT, buff=1.2).shift(DOWN * 0.1)
        ax = g.ax
        w = 1.6
        x = ax.c2p(0.5, 0)[0] + 1.0

        def block(lo, hi, col, op=0.75):
            y0, y1 = ax.c2p(0, lo)[1], ax.c2p(0, hi)[1]
            return Rectangle(width=w, height=abs(y1 - y0), stroke_color=col, stroke_width=2, fill_color=col,
                             fill_opacity=op).move_to([x, (y0 + y1) / 2, 0])
        parts = [("bond", b["bond"], CASH, r"zero-coupon bond, $e^{-rT}$"),
                 ("early", b["early"], GREY_B, r"repaid early: the bond sooner"),
                 ("strip", b["strip"], GOOD, r"coupons paid at knock-out"),
                 ("maturity_coupon", b["maturity_coupon"], IV, r"coupon at maturity, never knocked in")]
        blocks, names, lo = VGroup(), VGroup(), 0.0
        for key, v, col, nm in parts:
            r_ = block(lo, lo + v, col)
            blocks.add(r_)
            t = label(rf"{nm}: {v:.3f}", font_size=19, color=col)
            names.add(t)
            lo += v
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(blocks, RIGHT, buff=0.5).align_to(blocks, UP)
        top = lo
        dip = block(top + b["dip"], top, BAD, 0.85)
        dipn = label(rf"minus the autocall-cancelled knock-in loss leg: ${abs(b['dip']):.3f}$", font_size=19, color=BAD)
        dipn.next_to(names, DOWN, buff=0.18, aligned_edge=LEFT)
        line = DashedLine(ax.c2p(0, 1.0) + LEFT * 0.2, [x + w / 2 + 0.2, ax.c2p(0, 1.0)[1], 0], stroke_color=WHITE,
                          stroke_width=2)
        tot = MathTex(rf"\text{{sum}} = {d['total']:.4f}", font_size=34, color=OPT).next_to(dipn, DOWN, buff=0.35,
                                                                                          aligned_edge=LEFT)
        sub = wrapped_label(rf"all pieces are valued on the same {d['n_paths']:,} paths, at the fair coupon "
                            rf"{100 * c:.2f}\% a year; the pieces add up to the note exactly, because on every path the "
                            r"pieces add pathwise; the same seeds and paths used in the coupon solve make this sample total one".replace(",", "{,}"), 6.4, 19, GREY_A).next_to(tot, DOWN, buff=0.25,
                                                                                                   aligned_edge=LEFT)
        src = illustration(rf"the CSI 500 snowball: 24 months, knock-out 103\%, knock-in 75\%; $\sigma = "
                           rf"{100 * d['sigma']:.1f}\%$, $r = 2\%$")
        with self.voiceover(
            f"A structured note is sold as one security but built from priced pieces. Take chapter seven's contract and value all pieces on the same paths. <bookmark mark='a'/> A zero-coupon bond contributes {b['bond']:.3f}. <bookmark mark='b'/> Earlier repayment adds {b['early']:.3f}. <bookmark mark='c'/> Conditional coupons add {b['strip']:.3f} at knock-out and {b['maturity_coupon']:.3f} at maturity. <bookmark mark='d'/> Subtract {abs(b['dip']):.3f} for losses after knock-in on paths that never knock out. Autocall cancels that loss leg, so it is more specific than an unconditional down-and-in put. The pieces add pathwise to the note. Reusing the coupon solve's forty thousand paths makes this sample total {d['total']:.4f}, exactly one up to rounding; a fresh sample need not equal one. Coupons are paid at redemption or qualifying maturity, rather than in monthly instalments."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(blocks[0], DOWN), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(blocks[1], DOWN), FadeIn(names[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(blocks[2], DOWN), FadeIn(names[2]))
            self.play(GrowFromEdge(blocks[3], DOWN), FadeIn(names[3]))
            vo.wait_until("d")
            self.play(FadeIn(dip, shift=DOWN * 0.3), FadeIn(dipn))
            self.play(VGroup(blocks, dip).animate.set_opacity(0.55), Create(line), FadeIn(tot), FadeIn(sub))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, d):
        rc = d["rc"][0]
        rows = [
            cmath(r"\text{reverse convertible}", r"=", r"(1 + c) - \Big(1 - \tfrac{S_T}{S_0}\Big)^{+}", font_size=36,
                  colors={r"\text{reverse convertible}": OPT}),
            cmath(r"V", r"=", r"e^{-(r+s)T}(1 + c) - P(S_0, T)/S_0", font_size=36, colors={r"V": OPT}),
            cmath(r"c^{*}", r"=", r"e^{(r+s)T}\big(1 + P/S_0\big) - 1", font_size=36, colors={r"c^{*}": IV}),
            cmath(r"V_{\text{snowball}}", r"=", r"\textstyle\sum_m \mathbb E\big[D_m \mathbf 1_{O_m}\big]\big(1 + "
                  r"\tfrac{cm}{12}\big) + \mathbb E\big[D_T \mathbf 1_{N}\big](1 + 2c) + "
                  r"\mathbb E\big[D_T \mathbf 1_{I}\min(S_T, 1)\big]", font_size=34,
                  colors={r"V_{\text{snowball}}": OPT}),
            cmath(r"\text{margin}", r"=", r"\text{issue price} - V(c_{\text{sold}}) = (c^{*} - c_{\text{sold}})\,B",
                  font_size=36, colors={r"\text{margin}": BAD}),
        ]
        whys = [why(r"the simplest note: a bond that pays $1 + c$, minus a put the buyer has sold"),
                why(r"funding-spread illustration: discount the promise at $r+s$, the put at $r$; no default, recovery or wrong-way model"),
                why(r"set $V = 1$: both the put's premium and the issuer's credit spread feed the coupon"),
                why(r"three disjoint events: $O_m$, knocked out in month $m$; $N$, alive and never knocked in; $I$, "
                    r"alive and knocked in"),
                why(r"$V$ is affine in $c$ (chapter 7): every point of coupon withheld is $B$ points of price kept")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.2, buff=0.75, edge=6.9)
        ex = wrapped_label(rf"a one-year reverse convertible at 20\% volatility: the at-the-money put is worth "
                           rf"{rc['put']:.3f}, so the fair coupon is {100 * rc['coupon']:.1f}\%. A snowball: $B = "
                           rf"{d['B']:.3f}$, so selling it at {100 * d['coupon'] - 3:.1f}\% instead of "
                           rf"{100 * d['coupon']:.1f}\% keeps {3 * d['B']:.2f} points", 12.0, 21, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            f"Now the algebra. This reverse convertible pays one plus its coupon minus an at-the-money put payoff. A fall reduces repayment; the coupon remains in this simple contract. <bookmark mark='a'/> For a funding illustration, discount the issuer's promise at r plus s, while pricing the put at r. This is a spread heuristic, not a joint default, recovery and market-risk model. <bookmark mark='b'/> Set that illustrative value to one: the coupon rises with the put price and spread, here {100 * rc['coupon']:.1f} percent with twenty percent volatility and zero spread. <bookmark mark='c'/> The snowball instead separates three disjoint states: knock-out in month m, surviving without knock-in, and surviving after knock-in. <bookmark mark='d'/> Its model value is affine in coupon, with slope B. Reducing the coupon by one percentage point lowers value by {d['B']:.2f} price points. That is an initial model margin before hedging costs, reserves and other expenses."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(FadeIn(ex))
        self.wait(0.4)
        self.clear_scene()

    def funding(self, d):
        f = d["funding"]
        s = np.array([r["s"] for r in f])
        c = np.array([r["coupon"] for r in f])
        g = axes([0, 0.02], [0.12, 0.18], x_length=6.0, y_length=4.0, xlabel=r"issuer's funding spread $s$",
                 ylabel=r"model snowball coupon", xticks=[0, 0.005, 0.01, 0.015, 0.02],
                 xfmt=lambda u: f"{1e4 * u:.0f}" + r"\,\text{bp}", yticks=[0.12, 0.14, 0.16, 0.18],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, s, c, IV, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(a, b_), radius=0.07, color=IV) for a, b_ in zip(s, c)])
        t = ValueTracker(0.0)
        dot = always_redraw(lambda: Dot(ax.c2p(t.get_value(), float(np.interp(t.get_value(), s, c))), radius=0.11,
                                        color=WHITE))
        ro = readout(r"c^{*} =", lambda: 100 * float(np.interp(t.get_value(), s, c)), digits=1, unit=r"\%",
                     font_size=34, color=IV)
        ro2 = readout(r"s =", lambda: 1e4 * t.get_value(), digits=0, unit=r"\,\text{bp}", font_size=34, color=GREY_A)
        side = VGroup(ro2, ro,
                      wrapped_label(r"a wider spread shrinks the bond block and frees room for the coupon: the buyer is "
                                    r"paid for bearing the issuer's default risk too (Part 20). Lehman's note buyers "
                                    r"learned in 2008 that this part of the coupon is not free", 4.6, 19, GREY_A),
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        pp = pause_card(r"The issuer's credit spread widens by 100 bp. Does the coupon it can offer rise or fall?",
                        width=6.0).to_corner(UR, buff=0.3)
        with self.voiceover(
            f"<bookmark mark='p'/> In this funding-spread calculation, does a hundred-basis-point widening raise or lower the model coupon? <bookmark mark='a'/> It raises it: discounting shrinks the promised cash flows, so a larger coupon restores the modeled issue value. The result runs from {100 * c[0]:.1f} percent at zero spread to {100 * c[2]:.1f} at a hundred basis points and {100 * c[-1]:.1f} at two hundred. The extra headline rate compensates for lending to the issuer; it does not make the product safer. Our discount-spread calculation does not simulate issuer default or recovery. Lehman's note holders in 2008 illustrate why the credit exposure belongs in the discussion."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(g), Create(line), FadeIn(dots), FadeIn(side), FadeIn(dot))
            self.play(t.animate.set_value(0.02), run_time=max(vo.remaining(0.5), 1.0), rate_func=linear)
        self.wait(0.4)
        self.clear_scene()

    def players(self):
        cards = VGroup(
            firm_card(r"Buyers", r"Savers and wealthy individuals looking for yield above deposits, usually through a bank, "
                      r"a broker or a private fund. In low-rate years, European banks raised the headline rates of their "
                      r"retail products by making them more complex (C\'el\'erier and Vall\'ee 2017).",
                      source=r"Q.J.E. 2017", width=6.0, font_size=21),
            firm_card(r"Issuers", r"Investment banks in Europe and the US; securities firms and banks in Korea; in China, "
                      r"the OTC derivatives desks of brokers, which sold snowballs through private funds to qualified "
                      r"investors. Each issuer is short the exotic it sold, and hedges it in the futures and options "
                      r"markets.", source=r"public record", width=6.0, font_size=21),
        ).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to(UP * 0.2)
        foot = wrapped_label(r"the risk that stays with the issuer is crowded: thousands of notes with the same index, the same "
                             r"barriers and similar dates, hedged by a handful of desks that must trade in the same direction "
                             r"at the same moment (chapters 9 and 15)", 11.8, 20, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Who are the players? On one side, savers and wealthy individuals looking for more than a deposit pays, "
            "buying through their bank, a broker or a private fund. Claire Célérier and Boris Vallée found European "
            "banks raising the headline rates of retail products, when rates were low, by making them more complex. "
            "<bookmark mark='a'/> On the other side, the issuers: investment banks in Europe and the US, securities "
            "firms and banks in Korea, and in China the over-the-counter desks of brokers. Each is short the exotic it "
            "sold. <bookmark mark='b'/> And the risk that stays with them is crowded: thousands of notes on the same "
            "index, with the same barriers, hedged by a handful of desks that must trade in the same direction at the "
            "same moment."
            " Who is on the other side of these notes? Next."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
