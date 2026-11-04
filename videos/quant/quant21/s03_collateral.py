from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant21.common import BAD, COLL, EXPO, PART, ask, fit_right, illustration, load


class Collateral(VoiceoverScene):
    def construct(self):
        c = load("collateral")
        self.card()
        self.csa()
        self.profiles(c)
        self.mpor(c)
        self.mta(load("calls"))
        self.haircut(load("haircut"))
        self.reuse()

    def card(self):
        c = chapter_card(2, r"Collateral and the margin period of risk", r"If they post collateral, what is left?",
                         part=PART)
        with self.voiceover("Chapter two. Collateral: and why even a fully collateralised trade still has exposure."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def csa(self):
        rows = [cmath(r"C(t)", r"=", r"\text{sign}(V)\,\max\big(|V(t - \text{MPOR})| - H,\ 0\big)", font_size=38,
                      colors={r"C(t)": COLL}),
                cmath(r"E(t)", r"=", r"\max\big(V(t) - C(t),\ 0\big)", font_size=40, colors={r"E(t)": EXPO})]
        whys = [why(r"a credit support annex: the side that owes posts variation margin above a threshold $H$, called "
                    r"daily; but when a counterparty stops paying, the last margin you received is from the margin period "
                    r"of risk ago, typically 10 business days to close out"),
                why(r"what remains is the change in value over those days: 'gap risk'")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Most derivatives between banks are collateralised. Under a credit support annex, whichever side the "
            "trade is against posts margin every day, above an agreed threshold. <bookmark mark='a'/> But collateral "
            "lags. When a counterparty defaults, the last margin it paid was some days before, and closing out its "
            "trades takes days more: the margin period of risk, typically ten business days. The exposure that "
            "remains is how far the value moved in that gap."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def profiles(self, c):
        t = np.asarray(c["times"])
        p = c["profiles"]
        g = axes([0, 10], [0, 8], x_length=7.6, y_length=4.4, xlabel=r"years", ylabel=r"EE, \$ million",
                 xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 2, 4, 6, 8], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        cols = {"none": BAD, "threshold 2m": QC.IMPLIED, "threshold 0": COLL}
        lines = VGroup(*[curve(ax, np.r_[0, t], np.r_[0, p[k]["EE"]], c_, stroke_width=3) for k, c_ in cols.items()])
        side = VGroup(
            legend([(BAD, r"uncollateralised"), (QC.IMPLIED, r"threshold \$2m"), (COLL, r"zero threshold")], font_size=17),
            *[MathTex(rf"\text{{EPE}}: {p[k]['EPE']:.2f}", font_size=24, color=c_) for k, c_ in cols.items()],
            wrapped_label(r"monthly grid, so a one-month margin period here; the netting set of chapter 1", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The netting set again, three ways. <bookmark mark='a'/> With no collateral, the expected exposure of "
            f"chapter one, averaging {p['none']['EPE']:.1f} million. <bookmark mark='b'/> With a two-million threshold, "
            f"it falls to {p['threshold 2m']['EPE']:.1f}: the counterparty only posts beyond that. <bookmark mark='c'/> "
            f"With no threshold, to {p['threshold 0']['EPE']:.1f}. What is left is the movement during the margin "
            "period, and it never goes to zero."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[4]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(Create(lines[i]), FadeIn(side[i + 1]))
        self.wait(0.4)
        self.clear_scene()

    def mta(self, k):
        rows = k["rows"]
        hx = [-3.2, 0.2, 3.4]
        heads = [r"minimum transfer amount", r"margin calls a year", r"EPE, \$ million"]
        tab = VGroup(VGroup(*[label(h_, font_size=19, color=GREY_A).move_to([x, 2.0, 0]) for h_, x in zip(heads, hx)]))
        for i, r_ in enumerate(rows):
            y = 1.25 - 0.6 * i
            tab.add(VGroup(MathTex(rf"\${r_['mta']:g}\text{{m}}", font_size=28).move_to([hx[0], y, 0]),
                           MathTex(f"{r_['calls']:.0f}", font_size=28).move_to([hx[1], y, 0]),
                           MathTex(f"{r_['EPE']:.3f}", font_size=28).move_to([hx[2], y, 0])))
        foot = wrapped_label(r"daily calls with a 10-day margin period, over the netting set's first year. A small minimum "
                             r"transfer removes most of the operational traffic for little extra exposure: every call is "
                             r"a payment, a reconciliation and a possible dispute", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.5)
        title = label(r"How often to call", font_size=28).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Why not call margin on every cent? Because every call is a payment, a reconciliation, and a possible "
            "dispute. <bookmark mark='a'/> With no minimum transfer, the netting set triggers a call on almost every "
            f"business day, {rows[0]['calls']:.0f} a year. A minimum transfer of a quarter of a million halves that; "
            f"two million brings it to {rows[-1]['calls']:.0f}, for {100 * (rows[-1]['EPE'] / rows[0]['EPE'] - 1):.0f} "
            "percent more expected exposure. Collateral terms are a trade between credit risk and operations."
        ) as vo:
            self.play(FadeIn(title), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.2), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def mpor(self, c):
        w = c["weekly"]
        t, n0, n10 = np.asarray(w["t"]), np.asarray(w["none"]), np.asarray(w["mpor10"])
        g = axes([0, 1], [0, max(n0) * 1.15], x_length=7.4, y_length=4.2, xlabel=r"years (daily grid)",
                 ylabel=r"EE, \$ million", xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        l0 = curve(ax, t, n0, BAD, stroke_width=3)
        l1 = curve(ax, t, n10, COLL, stroke_width=3.5)
        side = VGroup(
            legend([(BAD, r"uncollateralised"), (COLL, r"daily margin, 10-day MPOR")], font_size=17),
            MathTex(rf"\text{{EPE ratio}} = {w['ratio']:.2f}", font_size=28),
            wrapped_label(r"the collateralised exposure grows like $\sigma\sqrt{\text{MPOR}}$, not $\sigma\sqrt t$; but in a "
                          r"crisis volatility jumps and the close-out takes longer, exactly when the counterparty fails",
                          3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "On a daily grid, with margin called every day and a ten-day margin period of risk. "
            "<bookmark mark='a'/> Uncollateralised, exposure grows with the square root of time. Collateralised, it "
            "stays at the size of ten days' moves. <bookmark mark='b'/> In the first year here it is "
            f"{w['ratio']:.2f} of the uncollateralised exposure, and falling further relative to it as time passes. "
            "But the ten days are an assumption: in a crisis, volatility jumps and close-outs take longer, just when "
            "counterparties fail."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l0), Create(l1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()


    def haircut(self, h):
        p = h["profiles"]
        rows = [cmath(r"C_{\text{held}}", r"=", r"(1 - h)\times\text{market value of the bonds}", font_size=38,
                      colors={r"C_{\text{held}}": COLL})]
        whys = [why(r"collateral other than cash is counted after a haircut $h$, sized to how far the bond's own price "
                    r"can fall over the margin period; Basel's supervisory haircut for a sovereign bond over five years "
                    r"is 4\%")]
        step = ladder(self, rows, whys, keep=1, top=2.7, x=-0.4, buff=0.8, edge=6.9)
        hx = [-3.4, 0.6, 3.6]
        tab = VGroup(VGroup(*[label(t_, font_size=19, color=GREY_A).move_to([x, 0.5, 0]) for t_, x in
                              zip([r"collateral received", r"EPE, first year, \$ thousand", r"against cash"], hx)]))
        cash = p["cash"]["EPE"]
        for i, (k, nm) in enumerate((("cash", r"cash"), ("bonds, no haircut", r"10-year Treasuries, no haircut"),
                                     ("bonds, 4% haircut", r"10-year Treasuries, 4\% haircut"))):
            y = -0.2 - 0.6 * i
            v = p[k]["EPE"]
            tab.add(VGroup(label(nm, font_size=19).move_to([hx[0], y, 0]),
                           MathTex(f"{1e3 * v:.0f}", font_size=28).move_to([hx[1], y, 0]),
                           MathTex(rf"{100 * (v / cash - 1):+.1f}\%", font_size=28,
                                   color=BAD if v > cash else COLL).move_to([hx[2], y, 0])))
        foot = wrapped_label(r"this netting set pays fixed, so it gains when rates rise, exactly when Treasuries fall: the "
                             r"collateral loses value as the exposure grows. Daily margin, zero threshold, 10-day margin "
                             r"period; only collateral received is in bonds", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.4)
        nb, hb = p["bonds, no haircut"]["EPE"], p["bonds, 4% haircut"]["EPE"]
        with self.voiceover(
            "Collateral need not be cash. Many agreements accept government bonds, counted after a haircut sized to "
            "how far the bond itself can fall during the margin period. <bookmark mark='a'/> Here the haircut "
            "matters for a reason beyond volatility. This netting set pays fixed, so its value rises with interest "
            "rates; and when rates rise, Treasuries fall. Posted in ten-year Treasuries with no haircut, the "
            f"collateral weakens exactly as the exposure grows, and expected exposure is {100 * (nb / cash - 1):.1f} "
            f"percent higher than with cash. <bookmark mark='b'/> The supervisory four percent haircut more than "
            f"covers it, {100 * (1 - hb / cash):.1f} percent below cash. Collateral correlated with the exposure is a "
            "mild form of the wrong-way risk of chapter four; collateral correlated with the counterparty, like "
            "Archegos's shares, is the severe one."
        ) as vo:
            step(0)
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]), FadeIn(foot))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def reuse(self):
        def box(t, c_, pos, w=3.6):
            r_ = RoundedRectangle(corner_radius=0.15, width=w, height=1.0, stroke_color=c_, stroke_width=2.5).move_to(pos)
            return VGroup(r_, wrapped_label(t, w - 0.3, 18).move_to(r_))
        poster = box(r"the poster", GREY_B, LEFT * 4.6 + UP * 1.4)
        taker = box(r"the receiver", GREY_B, UP * 1.4)
        third = box(r"the receiver's own creditor", BAD, RIGHT * 4.6 + UP * 1.4)
        custod = box(r"a third-party custodian", COLL, DOWN * 0.6)
        a1 = Arrow(poster.get_right(), taker.get_left(), buff=0.1, color=GREY_B)
        a2 = Arrow(taker.get_right(), third.get_left(), buff=0.1, color=BAD)
        a3 = Arrow(poster.get_bottom(), custod.get_left(), buff=0.1, color=COLL)
        l1 = label(r"variation margin: title transfers", font_size=16, color=GREY_A).next_to(a1, UP, buff=0.1)
        l2 = label(r"re-used, 'rehypothecated'", font_size=16, color=BAD).next_to(a2, UP, buff=0.1)
        l3 = label(r"initial margin: segregated, not re-used", font_size=16, color=COLL).next_to(custod, DOWN, buff=0.15)
        foot = wrapped_label(r"re-used collateral funds the receiver, and becomes an unsecured claim if the receiver fails: "
                             r"hedge funds whose assets Lehman's London broker-dealer had re-used waited years in its "
                             r"administration. After 2008, initial margin was required to sit with a custodian, out of "
                             r"reach of both sides' creditors", 12.4, 17, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Who holds the collateral matters as much as how much there is. <bookmark mark='a'/> Variation margin "
            "usually changes hands outright, and the receiver may use it again, to fund itself or to post to someone "
            "else. <bookmark mark='b'/> That makes collateral a source of funding, and a danger: if the receiver "
            "fails, the poster's collateral is gone and its claim is unsecured. Hedge funds whose assets Lehman's "
            "London broker-dealer had re-used waited years to recover them. <bookmark mark='c'/> So the rules after "
            "2008 put initial margin with a third-party custodian, segregated, out of reach of either side's "
            "creditors: protection that works only because it cannot be lent out."
        ) as vo:
            self.play(FadeIn(poster), FadeIn(taker))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(third), GrowArrow(a2), FadeIn(l2), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(custod), GrowArrow(a3), FadeIn(l3))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"a counterparty posts cash collateral daily with a zero threshold. Name two ways you can still lose "
                r"money when it defaults.")
        with self.voiceover("A counterparty posts cash daily with a zero threshold. Name two ways you can still lose "
                            "money when it defaults."):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
