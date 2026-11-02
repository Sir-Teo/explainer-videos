from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, load, real_data


class Debate(VoiceoverScene):
    def construct(self):
        a = load("artefact")
        r = load("roughness")
        self.card()
        self.weekends(a)
        self.estimates(a, r)

    def card(self):
        c = chapter_card(7, r"The debate", r"Is volatility really rough?", part=PART)
        with self.voiceover("Chapter seven. The debate."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def weekends(self, a):
        dv = np.sqrt(np.asarray(a["dow_mean_rv"]))
        names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        g = axes([-0.6, 6.6], [0, 0.6], x_length=6.0, y_length=3.6, xticks=list(range(7)), xfmt=lambda u: names[int(round(u))],
                 ylabel=r"typical realized volatility", yticks=[0, 0.2, 0.4, 0.6], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        bars = VGroup(*[Rectangle(width=0.55, height=abs(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1]), stroke_width=0,
                                  fill_color=BAD if i >= 5 else RV, fill_opacity=0.85).move_to(g.ax.c2p(i, v / 2))
                        for i, v in enumerate(dv)])
        side = VGroup(
            wrapped_label(r"the first trap is in the data: bitcoin's weekends are calm, a weekly rhythm that the estimator "
                          r"reads as extra roughness", 4.6, 20, WHITE),
            MathTex(rf"H:\ {a['btc']:.2f} \to {a['btc_deseasonalized']:.2f}", font_size=34, color=ROUGH),
            label(r"after removing each weekday's average", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        src = real_data(r"geometric mean of daily realized variance by weekday (UTC), 2024--2025")
        with self.voiceover(
            "Not everyone accepts that volatility is rough. Start with a trap in our own data. Bitcoin trades every "
            "day, but its weekends are calm: typical realized volatility on a Saturday is about half a weekday's. "
            "<bookmark mark='a'/> That weekly rhythm jumps up and down from day to day, and the estimator reads it "
            f"as roughness. Remove it, and H rises from {a['btc']:.2f} to {a['btc_deseasonalized']:.2f}. Still rough, "
            "but the number moved because of a calendar, not a law of nature."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def estimates(self, a, r):
        items = [(r"bitcoin", a["btc"], RV), (r"bitcoin, weekdays evened out", a["btc_deseasonalized"], RV)]
        cols = [VAR, IV, BAD]
        for m, c in zip(a["models"], cols):
            items.append((rf"smooth: {m['name']}", m["H_rv"], c))
        g = axes([0, 0.5], [-0.5, len(items) - 0.5], x_length=6.0, y_length=4.0, xlabel=r"estimated $H$",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[], font_size=15).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, (t, v, c) in enumerate(items):
            y = len(items) - 1 - i
            bars.add(Rectangle(width=max(abs(ax.c2p(max(v, 0), 0)[0] - ax.c2p(0, 0)[0]), 1e-3), height=0.42, stroke_width=0,
                               fill_color=c, fill_opacity=0.85).move_to(ax.c2p(max(v, 0) / 2, y)))
            labs.add(VGroup(label(t, font_size=18, color=c), MathTex(f"{v:.2f}", font_size=22))
                     .arrange(RIGHT, buff=0.2).next_to(ax.c2p(0, y), LEFT, buff=0.2))
        half = DashedLine(ax.c2p(0.5, -0.5), ax.c2p(0.5, len(items) - 0.5), stroke_color=GREY_C, stroke_width=1.5)
        side = wrapped_label(r"three smooth volatilities ($H = \tfrac12$), as variable as bitcoin's and measured the same "
                             r"way, through 5-minute realized variance: slow ones read 0.4; one that mean-reverts within "
                             r"hours reads almost 0. At a daily resolution, fast mean reversion and roughness look alike "
                             r"(Cont and Das 2024; Guyon and El Amrani 2023)", 5.6, 19, GREY_A).to_corner(UL, buff=0.5)
        verdict = wrapped_label(r"the case for roughness rests on several measurements agreeing: time series, the skew's "
                                r"term structure, and a microstructure story. Each alone has a smooth explanation", 12.0, 20,
                                ROUGH).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The deeper objection, made by Rama Cont and Purba Das, and by Guyon and El Amrani, is that the estimator "
            "can be fooled. Test it. Simulate three volatilities that are perfectly smooth, H one half, make them as "
            "variable as Bitcoin's, and measure them exactly as we measured Bitcoin, through noisy five-minute "
            "realized variance. <bookmark mark='a'/> The slow ones read about four-tenths: the noise does pull the "
            "estimate down, but not to Bitcoin's level. <bookmark mark='b'/> The one that mean-reverts within a few "
            "hours reads almost zero. At a daily resolution, a very fast smooth process and a rough one look the same. "
            "<bookmark mark='c'/> So the case for roughness rests on several measurements agreeing: the time series, "
            "the skew's term structure, and the order-flow story. Each alone has a smooth explanation. Together they "
            "make rough models the most economical description we have, and the debate is not over."
        ) as vo:
            self.play(FadeIn(g), Create(half), FadeIn(bars[:2]), FadeIn(labs[:2]), FadeIn(side))
            vo.wait_until("a")
            self.play(FadeIn(bars[2:4]), FadeIn(labs[2:4]))
            vo.wait_until("b")
            self.play(FadeIn(bars[4]), FadeIn(labs[4]))
            vo.wait_until("c")
            self.play(FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()
