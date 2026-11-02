from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, LOSS, PART, TRADE

MARKETS = [
    (r"United States", r"the largest stock market; T+1 settlement since May 2024; most retail orders filled by "
                       r"wholesalers; a fragmented market of many exchanges and dark pools (Parts 35--38)", TRADE),
    (r"Europe and the UK", r"many national exchanges and venues; MiFID II rules on trading and research payments; "
                           r"settlement moving to T+1 in 2027", CASH),
    (r"Japan", r"the Tokyo Stock Exchange; the yen is the world's funding currency, which is why its carry trade "
               r"matters (Part 22)", QC.IDEA),
    (r"India", r"the world's busiest market for index options by number of contracts; SEBI found that 93\% of "
               r"individual futures-and-options traders lost money over FY2022--24, about Rs\,1.8 lakh crore in all",
     QC.GAMMA),
    (r"China (A-shares)", r"shares bought today can be sold only tomorrow (T+1); daily price limits of $\pm$10\% on the "
                          r"main boards and $\pm$20\% on the STAR market and ChiNext; foreign access through Stock "
                          r"Connect from Hong Kong (2014, 2016)", LOSS),
]


class World(VoiceoverScene):
    def construct(self):
        self.card()
        self.markets()
        self.limits()

    def card(self):
        c = chapter_card(9, r"Markets around the world", r"Does the machine work the same everywhere?",
                         lit=(2015,), part=PART)
        with self.voiceover("Chapter nine. Markets around the world."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def markets(self):
        rows = VGroup()
        for name, what, col in MARKETS:
            rows.add(VGroup(label(name, font_size=25, color=col), wrapped_label(what, 9.8, 21, WHITE))
                     .arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(ORIGIN)
        names_w = max(r_[0].width for r_ in rows)
        for r_ in rows:
            r_[1].next_to(r_[0], RIGHT, buff=0.4 + names_w - r_[0].width).align_to(r_[0], UP)
        if rows.width > 13.2:
            rows.scale_to_fit_width(13.2)
        rows.move_to(ORIGIN)
        src = note(r"India: SEBI, press release of 23 September 2024; China: exchange rules", font_size=17).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "The machine is built differently in each country, and the differences matter. The United States has "
            "the largest stock market, settles in one day, routes most retail orders to wholesalers, and splits "
            "trading across many exchanges and dark pools. <bookmark mark='a'/> Europe has many national exchanges "
            "under one set of rules, and plans to move to one-day settlement in 2027. <bookmark mark='b'/> Japan's "
            "yen is the currency the world borrows in, which is why its carry trade, in Part twenty-two, matters "
            "everywhere. <bookmark mark='c'/> India now has the world's busiest market for index options, measured "
            "by contracts traded, much of it from individuals. Its regulator found that ninety-three percent of "
            "individual futures-and-options traders lost money over three years to March 2024, about one point "
            "eight lakh crore rupees in all. <bookmark mark='d'/> And China's A-share market has rules of its own: "
            "a share bought today cannot be sold until tomorrow, and prices may move at most ten percent a day on "
            "the main boards, twenty on the STAR market and ChiNext. Foreign investors reach it through Stock "
            "Connect, from Hong Kong."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(src))
            for i, mk in enumerate("abcd", start=1):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i], shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    def limits(self):
        g = axes([0, 6], [-0.12, 0.12], x_length=7.0, y_length=4.0, xlabel=r"time of day", ylabel=r"return since yesterday's close",
                 yticks=[-0.1, 0, 0.1], yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        cap = DashedLine(ax.c2p(0, -0.10), ax.c2p(6, -0.10), color=LOSS, stroke_width=2.5)
        capl = label(r"limit down: $-10\%$", font_size=22, color=LOSS).next_to(ax.c2p(6, -0.10), UR, buff=0.05)
        import numpy as np
        rng = np.random.default_rng(15)
        xs = np.linspace(0, 6, 200)
        ys = np.cumsum(rng.normal(-0.0009, 0.004, 200))
        ys = np.maximum(ys, -0.10)
        path = curve(ax, xs, ys, TRADE, stroke_width=3)
        txt = VGroup(
            label(r"At the limit, a stock can only trade at the limit price:", font_size=24),
            label(r"sellers queue, buyers vanish, nothing clears.", font_size=24),
            label(r"The selling not done today is carried to tomorrow,", font_size=24),
            label(r"and with T+1, a holder who bought today", font_size=24),
            label(r"cannot sell it at all until then.", font_size=24),
            label(r"schematic", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Rules like these change the statistics of Part one. A stock at its limit can trade only at the limit "
            "price: sellers queue, buyers disappear, and the day's selling that couldn't happen is carried into "
            "tomorrow. <bookmark mark='a'/> So daily returns in China are cut off at ten percent, and big moves are "
            "spread over several days: autocorrelation that looks like a signal, but that no one could have traded on. "
            "The House's data desk records the rules of each market beside its prices, so that no backtest assumes "
            "it could have sold a stock that could not be sold."
        ) as vo:
            self.play(FadeIn(g), Create(cap), FadeIn(capl))
            self.play(Create(path), run_time=3)
            self.play(LaggedStart(*[FadeIn(t_) for t_ in txt[:3]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(FadeIn(txt[3:]))
        self.wait(0.4)
        self.clear_scene()
