from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, GOOD, IV, OPT, PART, SPOT, illustration, load, real_data, ymd_to_year


class Buyers(VoiceoverScene):
    def construct(self):
        b = load("buyers")
        self.card()
        self.wall(b)
        self.table(b)
        self.record()
        self.derive()

    def card(self):
        c = chapter_card(2, r"Who buys, and what they earned", r"What did a snowball pay the people who bought it?",
                         part=PART)
        with self.voiceover("Chapter two. Who buys, and what they earned."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def wall(self, b):
        t = ymd_to_year(b["date"])
        px = np.asarray(b["close"])
        g = axes([2017, 2026], [3.5, 9.5], x_length=11.0, y_length=4.6, ylabel=r"CSI 500 ETF",
                 xticks=list(range(2017, 2026)), yticks=[4, 6, 8], font_size=15).to_edge(UP, buff=0.5)
        ax = g.ax
        line = curve(ax, t, px, SPOT, stroke_width=2)
        col = {"KO": QC.HOUSE, "KI": BAD, "full": WHITE}
        rows = b["rows"]
        notes = VGroup()
        for r in rows:
            t0, t1 = ymd_to_year([r["start"], r["end"]])
            seg = Line(ax.c2p(t0, r["S0"]), ax.c2p(t1, r["S0"]), stroke_color=col[r["outcome"]], stroke_width=2.2,
                       stroke_opacity=0.8)
            notes.add(VGroup(seg, Dot(ax.c2p(t0, r["S0"]), radius=0.045, color=col[r["outcome"]])))
        tally = {k: ValueTracker(0) for k in ("KO", "KI", "full")}
        ro = VGroup(*[readout(rf"\text{{{nm}}}", lambda k=k: tally[k].get_value(), digits=0, font_size=28, color=c_)
                      for k, nm, c_ in (("KO", "knocked out, 15\\% a year", col["KO"]),
                                        ("KI", "knocked in, a loss", BAD), ("full", "full coupon", WHITE))])
        ro.arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=1.3)
        cnt = {"KO": 0, "KI": 0, "full": 0}
        steps = []
        for r in rows:
            cnt[r["outcome"]] += 1
            steps.append(dict(cnt))
        foot = wrapped_label(r"each line: one note, from its first day to the day it ended, at its starting level. Gold: "
                             r"repaid with its coupon; red: knocked in and repaid below par", 11.5, 19, GREY_A)
        foot.to_edge(DOWN, buff=0.45)
        src = real_data(r"Yahoo Finance: 510500.SS, daily closes; stylized terms, one note a month, 2017--2023")
        by = b["by_year"]
        with self.voiceover(
            "What did buyers actually get? Take one stylized snowball, fifteen percent a year, knock-out at 103 "
            "percent after three months, knock-in at 75, two years, and issue it on the first trading day of every "
            "month from 2017 to 2023 on the CSI 500's real path. <bookmark mark='a'/> Each line is a note, from the "
            "day it was sold to the day it ended. Gold if it was repaid with its coupon, red if it knocked in and "
            "came back below par. <bookmark mark='b'/> Watch the vintages. Notes sold in 2017, near a peak, ran into "
            f"2018's fall: {by['2017']['KI']} of 12 lost money. Every note sold in 2019 and 2020 knocked out within "
            "months, at fifteen percent. And the notes of 2021 to 2023 met January 2024."
        ) as vo:
            self.play(FadeIn(g), Create(line), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(ro), FadeIn(foot))
            vo.wait_until("b")
            per = max(vo.remaining(0.5), 4.0) / len(rows)
            for k, n in enumerate(notes):
                self.play(FadeIn(n), *[tally[x].animate.set_value(steps[k][x]) for x in tally], run_time=per)
        self.wait(0.4)
        self.clear_scene()

    def table(self, b):
        by = b["by_year"]
        head = VGroup(*[label(h, font_size=20, color=GREY_A) for h in
                        (r"sold in", r"knocked out", r"lost", r"note, a year", r"index, same months, a year")])
        tab = VGroup(head)
        for y in range(2017, 2024):
            v = by[str(y)]
            tab.add(VGroup(MathTex(str(y), font_size=28), MathTex(str(v["KO"]), font_size=28, color=QC.HOUSE),
                           MathTex(str(v["KI"]), font_size=28, color=BAD if v["KI"] else GREY_B),
                           MathTex(rf"{100 * v['mean_ann']:+.1f}\%", font_size=28, color=OPT),
                           MathTex(rf"{100 * v['index_ann']:+.1f}\%", font_size=28, color=SPOT)))
        xs = [-5.2, -3.0, -1.0, 1.4, 4.4]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 3.0 - 0.55 * i, 0])
        side = wrapped_label(rf"{b['n']} notes, all ended by November 2025: {b['n_loss']} lost money, the worst "
                             rf"{100 * b['worst']:.0f}\%; the naive average of their annualised returns is "
                             rf"{100 * b['mean_ann']:.1f}\%; {b['beat_index']} of {b['n']} beat holding the index over "
                             r"the same months. One path of history is a description, not a sample of what could "
                             r"have happened", 12.0, 21, GREY_A).to_edge(DOWN, buff=0.5)
        pp = pause_card(r"Notes sold near the index's top, or near its bottom: which did better?", width=7.0)
        with self.voiceover(
            "Pause and predict: did the notes sold near the index's top do better, or the ones sold near its bottom? "
            "<bookmark mark='a'/> Here is the tally by vintage. The bottom did better, by far: a note bought low "
            "is far from its knock-in and close to its knock-out. <bookmark mark='b'/> Over all "
            f"{b['n']} notes, {b['n_loss']} lost money, the worst {100 * abs(b['worst']):.0f} percent. The naive "
            f"average of their annualised returns is {100 * b['mean_ann']:.1f} percent, and {b['beat_index']} of them "
            "beat simply holding the index over the same months. But this is one path of history. It describes what "
            "happened; it is not a sample of what could have."
        ) as vo:
            self.play(FadeIn(pp))
            vo.wait_until("a")
            self.play(FadeOut(pp), FadeIn(tab[0]), LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3,
                                                                run_time=3))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def record(self):
        cards = VGroup(
            history_card(2011, r"Henderson and Pearson", r"Morgan Stanley's SPARQS notes, 2001--2005: priced about 8\% "
                         r"above fair value; expected returns below the risk-free rate", color=QC.IDEA, width=4.2,
                         font_size=19),
            history_card(2017, r"C\'el\'erier and Vall\'ee", r"European retail products: banks raised headline rates by "
                         r"adding complexity, more so when rates were low", color=QC.IDEA, width=4.2, font_size=19),
            history_card(2019, r"Egan", r"US reverse convertibles: brokers sold dominated products, those paying brokers "
                         r"the most", color=QC.IDEA, width=4.2, font_size=19),
            history_card(2020, r"Vokata (working paper)", r"over 28,000 US yield-enhancement products, 2006--2015: "
                         r"attractive yields, negative returns, embedded fees of about 6--7\% a year; often dominated by "
                         r"cheap listed options".replace("28,000", "28{,}000"), color=QC.IDEA, width=4.2, font_size=19),
            history_card(2023, r"Calvet, C\'el\'erier, Sodini, Vall\'ee", r"Sweden: capital-guaranteed products drew "
                         r"cautious households into the stock market. Design can help, too", color=QC.GAIN, width=4.2,
                         font_size=19),
        )
        cards[:3].arrange(RIGHT, buff=0.25, aligned_edge=UP)
        cards[3:].arrange(RIGHT, buff=0.25, aligned_edge=UP)
        VGroup(cards[:3], cards[3:]).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        if VGroup(*cards).height > 7.2:
            VGroup(*cards).scale_to_fit_height(7.2)
        with self.voiceover(
            "The research record is less kind than our lucky vintages. Brian Henderson and Neil Pearson priced Morgan "
            "Stanley's SPARQS notes and found them sold about eight percent above fair value, with expected returns "
            "below the risk-free rate. Claire Célérier and Boris Vallée found European banks raising headline rates "
            "by adding complexity. <bookmark mark='a'/> Mark Egan found US brokers selling reverse convertibles that "
            "were dominated by others on the shelf, the ones that paid the broker most. Pavel Vokata's working paper "
            "studies over twenty-eight thousand US yield-enhancement products: attractive yields, negative returns, "
            "and embedded fees of about six to seven percent a year. <bookmark mark='b'/> But design is not only a "
            "trap. Laurent Calvet and his co-authors found Swedish capital-guaranteed products drawing cautious "
            "households into the stock market, to their benefit."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[:2]], lag_ratio=0.5))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards[2:4]], lag_ratio=0.5))
            vo.wait_until("b")
            self.play(FadeIn(cards[4], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\mathbb E^{\mathbb P}[R]", r"=", r"\mathbb E^{\mathbb P}[\text{payoff}]\,/\,\text{price} - 1",
                      font_size=38, colors={r"\mathbb E^{\mathbb P}[R]": QC.P}),
                cmath(r"\mathbb E^{\mathbb Q}[D\cdot\text{payoff}]\,/\,\text{price}", r"=", r"1 - \text{margin}",
                      font_size=38, colors={r"\mathbb E^{\mathbb Q}[D\cdot\text{payoff}]\,/\,\text{price}": QC.Q}),
                cmath(r"\mathbb E^{\mathbb P}[R] - r", r"\approx", r"\text{crash-put premium} - \text{margin}",
                      font_size=38, colors={r"\mathbb E^{\mathbb P}[R] - r": OPT})]
        whys = [why(r"what the buyer earns is a real-world expectation, measured on the Track Record"),
                why(r"under the pricing measure the note returns the riskless rate, less what the issuer kept"),
                why(r"in the real world the buyer also earns the premium for selling crash insurance (the variance risk "
                    r"premium of Part 12); the record says fees and complexity ate it")]
        step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.5, buff=0.9, edge=6.9)
        with self.voiceover(
            "Why can selling a crash put pay on average, and still leave buyers worse off? Separate the two "
            "measures. What the buyer earns is a real-world expectation of the payoff over the price. "
            "<bookmark mark='a'/> Under the pricing measure, the note returns exactly the riskless rate, minus the "
            "issuer's margin. <bookmark mark='b'/> In the real world the buyer also collects the premium for selling "
            "crash insurance, the variance risk premium of Part twelve. So a fairly priced snowball could pay its "
            "buyers on average. The studies say the margins and the complexity ate that premium, and more."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()
