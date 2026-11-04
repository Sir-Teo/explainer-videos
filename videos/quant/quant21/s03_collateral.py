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
        q = ask(r"a counterparty posts cash collateral daily with a zero threshold. Name two ways you can still lose "
                r"money when it defaults.")
        with self.voiceover("A counterparty posts cash daily with a zero threshold. Name two ways you can still lose "
                            "money when it defaults."):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
