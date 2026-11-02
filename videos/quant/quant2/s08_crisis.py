from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import CASH, LOSS, PART, RATE, load, real_data


def _x(d):
    d = int(d)
    return date(d // 10000, (d // 100) % 100, d % 100).toordinal()


class Crisis(VoiceoverScene):
    def construct(self):
        r = load("repo")
        self.card()
        self.rates(r)
        self.reserves(r)
        self.file(r)

    def card(self):
        c = chapter_card(7, r"The day repo broke", r"What happens when the market's cash runs short?", part=PART)
        with self.voiceover("Chapter seven. The day repo broke."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rates(self, r):
        x0, x1 = _x(20190826), _x(20191004)
        g = axes([x0, x1], [1.5, 5.6], x_length=9.6, y_length=4.6, ylabel=r"overnight rate, percent a year",
                 xticks=[_x(20190903), _x(20190916), _x(20191001)], xfmt=lambda v: {_x(20190903): "3 Sep",
                                                                                      _x(20190916): "16 Sep",
                                                                                      _x(20191001): "1 Oct"}[int(v)],
                 yticks=[2, 3, 4, 5], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines = {}
        for key, col in (("IOER", GREY_B), ("DFF", QC.GAIN), ("SOFR", RATE)):
            d = np.asarray(r[key]["date"])
            v = np.asarray(r[key]["value"])
            m = (d >= 20190826) & (d <= 20191004)
            xs = np.array([_x(z) for z in d[m]])
            lines[key] = VMobject(stroke_width=3.5 if key == "SOFR" else 2.5, color=col).set_points_as_corners(
                [ax.c2p(a, b) for a, b in zip(xs, v[m])])
        leg = legend([(RATE, r"SOFR: overnight Treasury repo"), (QC.GAIN, r"effective fed funds rate"),
                      (GREY_B, r"interest the Fed paid on bank reserves")], font_size=21).to_edge(RIGHT, buff=0.3)
        leg.shift(UP * 2.0)
        k = r["key"]
        peak = MathTex(rf"{k['20190917']['sofr']:.2f}\%", font_size=40, color=LOSS).next_to(ax.c2p(_x(20190917), 5.25),
                                                                                           RIGHT, buff=0.15)
        nums = VGroup(*[MathTex(rf"\text{{{lab}}}\ \ {k[d]['sofr']:.2f}\%", font_size=28, color=RATE)
                        for d, lab in (("20190913", "Fri 13"), ("20190916", "Mon 16"), ("20190917", "Tue 17"),
                                       ("20190918", "Wed 18"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        nums.next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        src = real_data(r"FRED (Federal Reserve Bank of St.\ Louis): SOFR, DFF, IOER, daily")
        with self.voiceover(
            "The crisis file for this part is a day few people outside finance noticed. In the summer of 2019 the "
            "overnight rates of the American money market sat in a tight band just above the interest the Federal "
            "Reserve paid banks on their reserves, about two percent. <bookmark mark='a'/> On Monday the 16th of "
            "September, two things drained cash at once: corporate taxes fell due, and buyers paid for a large "
            "batch of new Treasury bonds. Repo rose. <bookmark mark='b'/> On Tuesday the 17th, SOFR, the overnight "
            f"Treasury repo rate, printed {k['20190917']['sofr']:.2f} percent: more than double the previous Friday, "
            "and some trades that day were done as high as nine. The fed funds rate broke above the top of the Fed's "
            "own target range. <bookmark mark='c'/> That morning the New York Fed lent cash in repo for the first "
            "time in a decade, and kept doing so for months. By Wednesday SOFR was back near two and a half."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg))
            self.play(Create(lines["IOER"]), Create(lines["DFF"]))
            vo.wait_until("a")
            self.play(Create(lines["SOFR"]), run_time=3)
            self.play(FadeIn(nums[0]), FadeIn(nums[1]))
            vo.wait_until("b")
            self.play(FadeIn(peak, scale=1.3), FadeIn(nums[2]))
            vo.wait_until("c")
            self.play(FadeIn(nums[3]))
        self.wait(0.4)
        self.clear_scene()

    def reserves(self, r):
        d = np.asarray(r["reserves"]["date"])
        v = np.asarray(r["reserves"]["value"])
        xs = np.array([_x(z) for z in d])
        g = axes([_x(20180101), _x(20201231)], [0, 3.4], x_length=9.0, y_length=4.2,
                 ylabel=r"reserves banks hold at the Fed, \$ trillion", xticks=[_x(20180101), _x(20190101), _x(20200101),
                                                                            _x(20201231)],
                 xfmt=lambda vv: {_x(20180101): "2018", _x(20190101): "2019", _x(20200101): "2020",
                                  _x(20201231): "2021"}[int(vv)], yticks=[0, 1, 2, 3], font_size=18)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, xs, v, CASH, stroke_width=3)
        low = Dot(ax.c2p(_x(r["reserves_low_date"]), r["reserves_low"]), radius=0.09, color=LOSS)
        ll = MathTex(rf"\${r['reserves_low']:.2f}\,\text{{tn}}", font_size=30, color=LOSS).next_to(low, DOWN, buff=0.15)
        side = VGroup(
            label(r"the Fed shrank its balance sheet,", font_size=24),
            label(r"so banks held fewer reserves;", font_size=24),
            label(r"the banks that had cash were not", font_size=24),
            label(r"always free, or willing, to lend it", font_size=24),
            label(r"(the explanation is still debated)", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        with self.voiceover(
            "Why did one tax date break the market? The answer is debated, but this is the background. Since 2017 "
            "the Federal Reserve had been shrinking its balance sheet, and the reserves banks hold with it fell from "
            f"about {r['reserves_2018']:.1f} trillion dollars to {r['reserves_low']:.2f} trillion the day after the "
            "spike. <bookmark mark='a'/> There was still a lot of cash in the system, but not where it was needed, "
            "and the banks that held it were constrained, by regulation and by their own caution, in how freely "
            "they lent it. In March 2020 the same plumbing failed again, far worse, in the dash for cash."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=3)
            self.play(FadeIn(low), FadeIn(ll))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def file(self, r):
        k = r["key"]
        c = crisis_card(r"17 September 2019", r"The day repo broke",
                        r"Corporate tax payments and Treasury settlements drained cash from a system with reserves at a "
                        r"multiyear low; overnight secured rates spiked, the fed funds rate left its target range, and "
                        r"the New York Fed began lending in repo for the first time since 2008.",
                        stats=[(rf"{k['20190913']['sofr']:.2f}\%\to{k['20190917']['sofr']:.2f}\%", r"SOFR, Friday to Tuesday"),
                               (rf"+{100 * (k['20190917']['sofr'] - k['20190917']['ioer']):.0f}\,\text{{bp}}",
                                r"above the rate on reserves"),
                               (rf"\${r['reserves_low']:.2f}\,\text{{tn}}", r"reserves, the next day")],
                        width=11.0, font_size=23).move_to(UP * 0.6)
        lesson = wrapped_label(r"every leveraged position in this series is funded overnight; the House's funding desk "
                               r"charges SOFR plus a spread, and its stress tests include a day like this one (Part 41)",
                               11.0, 23, QC.IDEA).next_to(c, DOWN, buff=0.5)
        with self.voiceover(
            "The file. On the 17th of September 2019 the market's cheapest, safest loan, an overnight loan against "
            f"Treasury bonds, cost {k['20190917']['sofr']:.2f} percent, "
            f"{100 * (k['20190917']['sofr'] - k['20190917']['ioer']):.0f} basis points above what banks could earn by "
            "simply leaving cash at the Fed. <bookmark mark='a'/> Every leveraged position in this series is "
            "funded this way, overnight, again and again. The House's funding desk charges every backtest SOFR plus "
            "a spread, and its stress tests include a day like this one."
        ) as vo:
            self.play(FadeIn(c, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()
