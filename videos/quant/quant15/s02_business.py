from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, CASH, GOOD, IV, OPT, PART, SPOT, illustration, load


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
        dipn = label(rf"minus the down-and-in put the buyer sold: ${b['dip']:.3f}$", font_size=19, color=BAD)
        dipn.next_to(names, DOWN, buff=0.18, aligned_edge=LEFT)
        line = DashedLine(ax.c2p(0, 1.0) + LEFT * 0.2, [x + w / 2 + 0.2, ax.c2p(0, 1.0)[1], 0], stroke_color=WHITE,
                          stroke_width=2)
        tot = MathTex(rf"\text{{sum}} = {d['total']:.4f}", font_size=34, color=OPT).next_to(dipn, DOWN, buff=0.35,
                                                                                          aligned_edge=LEFT)
        sub = wrapped_label(rf"each piece is its own Monte Carlo on the same {d['n_paths']:,} paths, at the fair coupon "
                            rf"{100 * c:.2f}\% a year; the pieces add up to the note exactly, because on every path the "
                            r"payoff is one of them".replace(",", "{,}"), 6.4, 19, GREY_A).next_to(tot, DOWN, buff=0.25,
                                                                                                   aligned_edge=LEFT)
        src = illustration(rf"the CSI 500 snowball: 24 months, knock-out 103\%, knock-in 75\%; $\sigma = "
                           rf"{100 * d['sigma']:.1f}\%$, $r = 2\%$")
        with self.voiceover(
            "A structured note is sold as one security, but it is built from parts, and each part has a price. Take "
            "the snowball we will meet in chapter seven, at its fair coupon, and price every piece on the same "
            f"simulated paths. <bookmark mark='a'/> First a zero-coupon bond: {b['bond']:.3f} for every unit, the "
            "promise to repay in two years, discounted. <bookmark mark='b'/> Most notes are repaid early, and money "
            f"back sooner is worth a little more: {b['early']:.3f}. <bookmark mark='c'/> Then the coupons: "
            f"{b['strip']:.3f} paid at a knock-out, and {b['maturity_coupon']:.3f} paid at maturity on paths that "
            "never knocked in. <bookmark mark='d'/> And then the piece the buyer does not see. She has sold a put "
            f"that comes alive only if the index falls through the barrier, worth {abs(b['dip']):.3f}. It hangs "
            "below the stack, and takes it back down to exactly one. The coupon is the put's premium, paid in "
            "instalments."
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
            cmath(r"V_{\text{snowball}}", r"=", r"\textstyle\sum_m \mathbb E\big[D_m \mathbf 1_{\tau = m}\big]\big(1 + "
                  r"\tfrac{cm}{12}\big) + \mathbb E\big[D_T \mathbf 1_{\text{alive, no KI}}\big](1 + 2c) + "
                  r"\mathbb E\big[D_T \mathbf 1_{\text{alive, KI}}\min(S_T, 1)\big]", font_size=30,
                  colors={r"V_{\text{snowball}}": OPT}),
            cmath(r"\text{margin}", r"=", r"\text{issue price} - V(c_{\text{sold}}) = (c^{*} - c_{\text{sold}})\,B",
                  font_size=36, colors={r"\text{margin}": BAD}),
        ]
        whys = [why(r"the simplest note: a bond that pays $1 + c$, minus a put the buyer has sold"),
                why(r"the issuer discounts its own promise at its funding rate $r + s$; the put is priced at $r$"),
                why(r"set $V = 1$: both the put's premium and the issuer's credit spread feed the coupon"),
                why(r"the snowball's payoff splits on three disjoint events: knocked out in month $m$, alive and never "
                    r"knocked in, alive and knocked in"),
                why(r"$V$ is affine in $c$ (chapter 7): every point of coupon withheld is $B$ points of price kept")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-2.2, buff=0.75, edge=6.9)
        ex = wrapped_label(rf"a one-year reverse convertible at 20\% volatility: the at-the-money put is worth "
                           rf"{rc['put']:.3f}, so the fair coupon is {100 * rc['coupon']:.1f}\%. A snowball: $B = "
                           rf"{d['B']:.3f}$, so selling it at {100 * d['coupon'] - 3:.1f}\% instead of "
                           rf"{100 * d['coupon']:.1f}\% keeps {3 * d['B']:.2f} points", 12.0, 21, GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now the algebra. The simplest note is the reverse convertible: it pays one plus a coupon, unless the "
            "stock has fallen, in which case the buyer bears the fall. That is a bond, minus a put. <bookmark mark='a'/> "
            "Its value: the issuer discounts its own promise at its funding rate, r plus s, and the put is priced as "
            "any put. <bookmark mark='b'/> Set the value to one and solve: the fair coupon grows with the put's "
            f"premium and with the issuer's credit spread. At twenty percent volatility over a year it is "
            f"{100 * rc['coupon']:.1f} percent. <bookmark mark='c'/> The snowball is the same idea with memory: its "
            "payoff splits on three disjoint events, knocked out in month m, alive and never knocked in, alive and "
            "knocked in. <bookmark mark='d'/> And the margin is the issue price minus the fair value of what was "
            "sold. The value is a straight line in the coupon, with slope B. Every point of coupon an issuer "
            f"withholds is worth {d['B']:.2f} points of price to it."
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
                 ylabel=r"fair snowball coupon", xticks=[0, 0.005, 0.01, 0.015, 0.02],
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
            "Pause on that funding spread. <bookmark mark='p'/> If the issuer's own credit spread widens by a "
            "hundred basis points, does the coupon it can offer rise or fall? <bookmark mark='a'/> It rises. A "
            "weaker issuer discounts its promise more heavily, the bond block shrinks, and the room it frees goes "
            f"into the coupon: from {100 * c[0]:.1f} percent at no spread to {100 * c[2]:.1f} at a hundred basis "
            f"points and {100 * c[-1]:.1f} at two hundred. Part of every coupon pays the buyer for lending to the "
            "bank. Lehman Brothers' note buyers learned in 2008 that this part is not free."
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
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
