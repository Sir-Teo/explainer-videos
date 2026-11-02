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
        f = load("sofr_fan")
        rc = load("reserve_curve")
        self.card()
        self.fan(r, f)
        self.reserves(r)
        self.curve_fit(rc)
        self.file(r, f)

    def card(self):
        c = chapter_card(12, r"The day repo broke", r"What happens when the market's cash runs short?",
                         lit=(2019,), part=PART)
        with self.voiceover("Chapter twelve. The day repo broke."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def fan(self, r, f):
        x0, x1 = _x(20190826), _x(20191004)
        g = axes([x0, x1], [1.5, 9.5], x_length=8.6, y_length=4.6, ylabel=r"overnight Treasury repo, percent a year",
                 xticks=[_x(20190903), _x(20190916), _x(20191001)], xfmt=lambda v: {_x(20190903): "3 Sep",
                                                                                      _x(20190916): "16 Sep",
                                                                                      _x(20191001): "1 Oct"}[int(v)],
                 yticks=[2, 4, 6, 8], font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        S = f["series"]

        def xs(key):
            return np.array([_x(z) for z in S[key]["date"]], float), np.asarray(S[key]["value"], float)
        xa, p1 = xs("SOFR1")
        _, p25 = xs("SOFR25")
        _, p75 = xs("SOFR75")
        _, p99 = xs("SOFR99")
        _, med = xs("SOFR")
        xi, ior = xs("IOER")
        k = ValueTracker(0)

        def fanmob():
            n = max(int(k.get_value()), 2)
            return VGroup(band(ax, xa[:n], p1[:n], p99[:n], RATE, 0.15), band(ax, xa[:n], p25[:n], p75[:n], RATE, 0.35),
                          curve(ax, xa[:n], med[:n], RATE, stroke_width=3))
        fm = always_redraw(fanmob)
        il = curve(ax, xi, ior, GREY_B, stroke_width=2)
        leg = legend([(RATE, r"SOFR: median; 25--75th and 1st--99th percentiles of the day's trades"),
                      (GREY_B, r"interest the Fed paid on reserves")], font_size=18).to_edge(UP, buff=0.3).shift(RIGHT * 1.2)
        key = f["key"]
        nums = VGroup(*[MathTex(rf"\text{{{lab}: median}}\ {key[d]['SOFR']:.2f}\%,\ \text{{99th}}\ {key[d]['SOFR99']:.2f}\%",
                                font_size=24, color=RATE)
                        for d, lab in (("20190913", "Fri 13"), ("20190916", "Mon 16"), ("20190917", "Tue 17"),
                                       ("20190918", "Wed 18"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        nums.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        src = real_data(r"FRED: SOFR and its percentiles (SOFR1, SOFR25, SOFR75, SOFR99), IOER; daily")
        i17 = list(S["SOFR"]["date"]).index(20190917)
        with self.voiceover(
            "The crisis file is a day few outside finance noticed. In the summer of 2019 overnight rates sat just above what "
            "the Fed paid on reserves. The New York Fed publishes not only SOFR, the median overnight Treasury repo rate, but "
            "its spread across the day's trades: the fan. <bookmark mark='a'/> On Monday the 16th of September, corporate "
            "taxes fell due and new Treasuries settled, draining cash at once. The median barely moved; the top of the fan "
            f"jumped to {key['20190916']['SOFR99']:.1f}. <bookmark mark='b'/> On Tuesday the whole fan lifted: median "
            f"{key['20190917']['SOFR']:.2f} percent, ninety-ninth percentile {key['20190917']['SOFR99']:.0f}. The New York Fed "
            "offered up to seventy-five billion dollars in repo, its first in a decade; dealers took fifty-three. By Thursday "
            "the fan had folded back."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg), Create(il))
            self.add(fm)
            self.play(k.animate.set_value(i17 - 1), run_time=5, rate_func=linear)
            self.play(FadeIn(nums[0]))
            vo.wait_until("a")
            self.play(k.animate.set_value(i17), FadeIn(nums[1]), run_time=1.2)
            vo.wait_until("b")
            self.play(k.animate.set_value(i17 + 1), FadeIn(nums[2]), run_time=1.2)
            self.play(k.animate.set_value(len(xa)), FadeIn(nums[3]), run_time=3)
        fm.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def reserves(self, r):
        d = np.asarray(r["reserves"]["date"])
        v = np.asarray(r["reserves"]["value"])
        xs = np.array([_x(z) for z in d])
        g = axes([_x(20180101), _x(20201231)], [0, 3.4], x_length=6.6, y_length=4.0,
                 ylabel=r"reserves banks hold at the Fed, \$ trillion", xticks=[_x(20180101), _x(20190101), _x(20200101),
                                                                            _x(20201231)],
                 xfmt=lambda vv: {_x(20180101): "2018", _x(20190101): "2019", _x(20200101): "2020",
                                  _x(20201231): "2021"}[int(vv)], yticks=[0, 1, 2, 3], font_size=17)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, xs, v, CASH, stroke_width=3)
        low = Dot(ax.c2p(_x(r["reserves_low_date"]), r["reserves_low"]), radius=0.09, color=LOSS)
        ll = MathTex(rf"\${r['reserves_low']:.2f}\,\text{{tn}}", font_size=30, color=LOSS).next_to(low, DOWN, buff=0.15)
        rows = [
            MathTex(r"s = r_{\text{repo}} - r_{\text{IOR}}", font_size=34, color=RATE),
            MathTex(r"s(R) = a + b\,e^{-c(R - 1.3)}", font_size=34, color=QC.HOUSE),
        ]
        whys = [wrapped_label(r"a bank lends reserves in repo only if it earns more than leaving them at the Fed", 5.4,
                              20, GREY_B),
                wrapped_label(r"flat when reserves are plentiful, steep when they are scarce", 5.4, 20, GREY_B)]
        right = VGroup(rows[0], whys[0], rows[1], whys[1]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        right[2].shift(DOWN * 0.2)
        right[3].shift(DOWN * 0.2)
        right.to_edge(RIGHT, buff=0.35).shift(UP * 0.8)
        with self.voiceover(
            "Why did one tax date break the market? Since 2017 the Federal Reserve had been shrinking its balance sheet, and "
            f"the reserves banks keep with it fell from about {r['reserves_2018']:.1f} trillion dollars to "
            f"{r['reserves_low']:.2f} trillion the week of the spike. <bookmark mark='a'/> A bank with spare reserves lends "
            "them in repo only if repo pays more than the Fed pays on reserves: that spread is the opportunity cost of holding "
            "them. When reserves are plentiful the spread is near zero; when they are scarce, banks hold on to them for their "
            "own liquidity needs, and the price of cash rises steeply. That's a demand curve for reserves, and it can be "
            "measured."
        ) as vo:
            self.play(FadeIn(g), Create(line), run_time=3)
            self.play(FadeIn(low), FadeIn(ll))
            vo.wait_until("a")
            self.play(FadeIn(right))
        self.wait(0.4)
        self.clear_scene()

    def curve_fit(self, rc):
        R = np.asarray(rc["R"], float)
        s = np.asarray(rc["s"], float)
        path = np.asarray(rc["path"], float)
        loss = np.asarray(rc["loss"], float)
        boot = np.asarray(rc["boot_loss"], float)
        grid = np.asarray(rc["grid"], float)
        L = np.vstack([loss, boot[:, :len(loss)]])
        steps = np.arange(len(loss))
        ck = [0, 1, 2, 4, 8, len(loss) - 1]
        lin = rc["linear"]

        def frame(i):
            th = path[min(ck[i], len(path) - 1)]
            g = axes([1.3, 4.3], [-15, 85], x_length=5.6, y_length=3.8, xlabel=r"reserves, \$ trillion (weekly)",
                     ylabel=r"SOFR $-$ IOR, basis points", xticks=[1.5, 2.5, 3.5], yticks=[0, 40, 80], font_size=15)
            ax = g.ax
            pts = VGroup(*[Dot(ax.c2p(a, min(b, 85)), radius=0.035, color=RATE, fill_opacity=0.7)
                           for a, b in zip(R, s)])
            fit = curve(ax, grid, np.clip(th[0] + th[1] * np.exp(-th[2] * (grid - 1.3)), -15, 85), QC.HOUSE)
            ln = DashedLine(ax.c2p(1.3, np.polyval(lin, 1.3)), ax.c2p(4.3, np.polyval(lin, 4.3)), color=GREY_B,
                            stroke_width=2)
            return VGroup(g, pts, ln, fit)
        rp = TrainingReplay(steps, L, frame, ck, ylabel=r"mean squared error (log)", xlabel=r"Gauss--Newton iteration",
                            log_y=True, color=QC.HOUSE, left=LEFT * 3.3 + DOWN * 0.3, right=RIGHT * 3.6 + UP * 0.6,
                            x_length=4.6, y_length=2.8)
        tab = rc["table"]
        res = VGroup(
            MathTex(rf"\text{{fit MSE}}\ {rc['mse_fit']:.0f}\ \text{{vs linear}}\ {rc['mse_lin']:.0f}", font_size=26,
                    color=QC.HOUSE),
            MathTex(rf"R < \$1.5\text{{tn: mean }}{tab[0]['mean']:+.1f}\,\text{{bp, max }}{tab[0]['max']:+.1f}", font_size=24,
                    color=RATE),
            MathTex(rf"R > \$3.5\text{{tn: mean }}{tab[4]['mean']:+.1f}\,\text{{bp}}", font_size=24, color=RATE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        res.next_to([3.6, -1.7, 0], DOWN, buff=0)
        src = note(r"FRED: SOFR, IOER/IORB, WRESBAL; weekly, April 2018 -- December 2021; band: 8 bootstrap resamples; "
                   r"dashed: the linear baseline", font_size=15).to_edge(DOWN, buff=0.1)
        with self.voiceover(
            "Each dot is a week of 2018 to 2021: reserves across, repo's spread over interest on reserves up. Fit a flat "
            "part plus an exponential wall by Gauss-Newton. <bookmark mark='a'/> Within a few iterations the curve bends into "
            f"the wall; eight bootstrap fits make the band, and it beats a straight line, error {rc['mse_fit']:.0f} against "
            f"{rc['mse_lin']:.0f}. <bookmark mark='b'/> Below one and a half trillion the spread averaged "
            f"{tab[0]['mean']:+.0f} basis points and reached {tab[0]['max']:+.0f}; above three and a half, "
            f"{tab[4]['mean']:+.0f}. In September 2019 the system sat on the steep part without knowing it."
        ) as vo:
            self.play(FadeIn(rp), FadeIn(src))
            vo.wait_until("a")
            rp.play(self, run_time=6)
            vo.wait_until("b")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def file(self, r, f):
        k = r["key"]
        fk = f["key"]
        c = crisis_card(r"17 September 2019", r"The day repo broke",
                        r"Corporate tax payments and Treasury settlements drained cash from a system with reserves on "
                        r"the steep part of their demand curve; overnight secured rates spiked, the fed funds rate left "
                        r"its target range, and the New York Fed lent in repo for the first time since 2008. Afonso, "
                        r"Cipriani, Copeland, Kovner, La Spada and Martin (2021) trace it to reserves concentrated in a "
                        r"few banks that were slow to lend them.",
                        stats=[(rf"{k['20190913']['sofr']:.2f}\%\to{k['20190917']['sofr']:.2f}\%", r"SOFR, Friday to Tuesday"),
                               (rf"{fk['20190917']['SOFR99']:.0f}\%", r"99th percentile, Tuesday"),
                               (rf"\${r['reserves_low']:.2f}\,\text{{tn}}", r"reserves that week")],
                        width=11.0, font_size=22).move_to(UP * 0.6)
        lesson = wrapped_label(r"every leveraged position in this series is funded overnight; the House's funding desk "
                               r"charges SOFR plus a spread, and its stress tests include a day like this one; March "
                               r"2020's dash for cash is Part 41", 11.0, 22, QC.IDEA).next_to(c, DOWN, buff=0.45)
        with self.voiceover(
            f"The file: on the 17th of September 2019 the safest overnight loan cost {k['20190917']['sofr']:.2f} percent at "
            f"the median, and some trades paid {fk['20190917']['SOFR99']:.0f}. Afonso and colleagues at the New York Fed "
            "traced it to reserves concentrated in a few large banks slow to lend them. <bookmark mark='a'/> Every leveraged "
            "position in this series is funded overnight. The House charges SOFR plus a spread, and stress-tests a day like "
            "this; March 2020's worse failure is Part forty-one. The cash in this story went to dealers. Next, the banks "
            "that lend to hedge funds: prime brokers."
        ) as vo:
            self.play(FadeIn(c, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()
