from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import GAIN, LOSS, PART, VALUE, load, real_data

CAR_CODE = [
    "def car(returns, market, day0, window=(-5, 60)):",
    "    a, b = window",
    "    lo, hi = day0 + a, day0 + b + 1",
    "    if lo < 0 or hi > len(returns):",
    "        return np.full(b - a + 1, np.nan)",
    "    return np.cumsum(returns[lo:hi] - market[lo:hi])",
    "",
    "def sue(x, lookback=8):              # seasonal random walk",
    "    d = x[4:] - x[:-4]               # this quarter less a year ago",
    "    ...                              # over the s.d. of the last 8",
]


class Earnings(VoiceoverScene):
    def construct(self):
        pe = load("pead")
        self.card()
        self.ball_brown()
        self.define()
        self.lab(pe)
        self.clock(pe)
        self.history(pe)

    def card(self):
        c = chapter_card(13, r"Earnings announcements and the drift", r"How fast do prices read the news?",
                         lit=(1968,), part=PART)
        with self.voiceover("Chapter thirteen. Earnings announcements, and the drift."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ball_brown(self):
        m = np.linspace(-12, 6, 181)
        good = 0.07 * (1 / (1 + np.exp(-(m + 3) / 2.2)) - 1 / (1 + np.exp(9 / 2.2))) + 0.012 * np.clip(m, 0, None) / 6
        bad = -0.09 * (1 / (1 + np.exp(-(m + 3) / 2.2)) - 1 / (1 + np.exp(9 / 2.2))) - 0.018 * np.clip(m, 0, None) / 6
        g = axes([-12, 6], [-0.12, 0.10], x_length=7.4, y_length=4.6, xlabel=r"months from the annual report",
                 ylabel=r"cumulative abnormal return", xticks=[-12, -6, 0, 6], yticks=[-0.1, -0.05, 0, 0.05, 0.1],
                 yfmt=lambda u: f"{100 * u:+.0f}\\%".replace("+0", "0"), font_size=18).to_edge(LEFT, buff=0.7)
        g.shift(DOWN * 0.2)
        ax = g.ax
        lg = curve(ax, m, good, GAIN, stroke_width=4)
        lb = curve(ax, m, bad, LOSS, stroke_width=4)
        zero = DashedLine(ax.c2p(0, -0.12), ax.c2p(0, 0.10), color=GREY_B, stroke_width=2)
        drift = SurroundingRectangle(VGroup(Dot(ax.c2p(0, 0.08)), Dot(ax.c2p(6, -0.12))), buff=0.02, color=YELLOW,
                                     stroke_width=2, corner_radius=0.05)
        side = VGroup(
            label(r"schematic, after Ball and Brown (1968)", font_size=19, color=GREY_B),
            legend([(GAIN, r"earnings above last year's"), (LOSS, r"earnings below")], font_size=22),
            wrapped_label(r"most of the news is in the price before the report; but prices keep drifting the same "
                          r"way after it: post-earnings-announcement drift (Bernard and Thomas 1989)", 4.6, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Do the statements move prices? In 1968 Ray Ball and Philip Brown sorted firms by whether annual earnings beat the "
            "year before, and followed their returns beyond the market's. <bookmark mark='a'/> Good news had risen and bad news "
            "fallen, mostly before the report: the market learns most of it elsewhere first. <bookmark mark='b'/> But prices kept "
            "drifting the same way afterwards. In 1989 Bernard and Thomas showed the drift lasts about sixty trading days."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lg), Create(lb), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(Create(drift), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def define(self):
        rows = [
            cmath(r"\text{SUE}_{q}", r"=", r"\frac{X_q - X_{q-4}}{\sigma\big(X_{q-j} - X_{q-4-j}\big)_{j=1..8}}",
                  font_size=40, colors={r"\text{SUE}_{q}": VALUE}),
            cmath(r"\text{CAR}(0, \tau)", r"=", r"\sum_{s=0}^{\tau} \big(r_{i,s} - r_{m,s}\big)", font_size=40,
                  colors={r"\text{CAR}(0, \tau)": QC.HOUSE}),
            cmath(r"\text{day } 0", r"=", r"\text{the first session after the 8-K, item 2.02, was accepted}",
                  font_size=34),
        ]
        whys = [why(r"surprise against a seasonal random walk: this quarter less the same quarter a year ago, in units "
                    r"of how much that difference usually moves (Foster, Olsen and Shevlin 1984)"),
                why(r"returns beyond the market's, summed in event time"),
                why(r"the earnings release is filed as an 8-K, item 2.02; after 4 p.m.\ it can be traded only the next day")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-1.0, buff=0.9, edge=6.9)
        with self.voiceover(
            "To measure the drift you need two definitions. The surprise: this quarter's earnings minus the same quarter last year, "
            "divided by how much that seasonal difference usually moves, called standardised unexpected earnings. "
            "<bookmark mark='a'/> The reaction: the stock's return minus the market's, summed day by day from the announcement, the "
            "cumulative abnormal return. <bookmark mark='b'/> And the clock starts when the news was public: American companies "
            "file their earnings releases as an 8-K, item 2.02, with a time stamp, so day zero is the first trading session after it."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, pe):
        card = lab_card(r"an event study", CAR_CODE, source="explainer/quant/house/fundamentals.py", width=7.0,
                        font_size=17).to_corner(UL, buff=0.3)
        L = pe["lab"]
        f = str(L["filed"])
        d0 = str(L["day0"])
        pp = desk_question(r"Pause and predict: a firm beats by three standard deviations and the stock jumps 5\% "
                           r"overnight. Do you buy at the next open?", width=5.4, font_size=20).to_edge(RIGHT, buff=0.3)
        pp.shift(DOWN * 0.8)
        with self.voiceover(
            "The House's event study is six lines: take the window around day zero, subtract the market, add up. "
            f"<bookmark mark='a'/> Run it on one Apple announcement, filed after the close: a surprise of {L['sue']:.2f} standard "
            f"deviations, {100 * L['car0']:+.1f} percent against the market on the day, {100 * L['car60']:+.1f} over sixty "
            "sessions. One event says little; you need many. <bookmark mark='b'/> Pause and predict before we run them all: a "
            "firm beats by three standard deviations and jumps five percent. Do you buy at the next open?"
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, [f"car(aapl, spy, day0={d0[:4]}-{d0[4:6]}-{d0[6:]}, window=(-5, 60))",
                                 f"SUE {L['sue']:+.2f}   day 0-1 {100 * L['car0']:+.1f}%   to +60 {100 * L['car60']:+.1f}%"])
            vo.wait_until("b")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def clock(self, pe):
        days = np.asarray(pe["days"])
        C, S = np.asarray(pe["car"]), np.asarray(pe["sue"])
        g = axes([-5, 60], [-0.15, 0.2], x_length=6.8, y_length=4.6, xlabel=r"trading days from the announcement",
                 ylabel=r"cumulative return beyond SPY", xticks=[-5, 0, 20, 40, 60], yticks=[-0.1, 0, 0.1, 0.2],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        base = C[:, 4:5]
        paths = VGroup(*[curve(ax, days, np.clip(c - b, -0.15, 0.2), GAIN if s > 0 else LOSS, stroke_width=1.2)
                         .set_stroke(opacity=0.45) for c, b, s in zip(C, base, S)])
        mp = curve(ax, days, np.clip(np.asarray(pe["mean_pos"]) - np.asarray(pe["mean_pos"])[4], -0.15, 0.2), GAIN,
                   stroke_width=5)
        mn = curve(ax, days, np.clip(np.asarray(pe["mean_neg"]) - np.asarray(pe["mean_neg"])[4], -0.15, 0.2), LOSS,
                   stroke_width=5)
        zero = DashedLine(ax.c2p(0, -0.15), ax.c2p(0, 0.2), color=GREY_B, stroke_width=1.5)
        dp, dn = pe["drift_pos"], pe["drift_neg"]
        right = dp > dn
        side = VGroup(
            wrapped_label(rf"Apple, {pe['n_events']} announcements, Oct.\ 2015 -- Dec.\ 2020", 4.8, 21, GREY_A),
            label(rf"green: positive surprise ({pe['n_pos']}); red: negative ({pe['n_neg']})", font_size=19,
                  color=GREY_B),
            MathTex(rf"\text{{corr(SUE, day-0 move)}} = {pe['jump_corr']:.2f}", font_size=28),
            MathTex(rf"\text{{drift, day }}+1\text{{ to }}+60:\ {100 * dp:+.1f}\%\ \text{{vs}}\ {100 * dn:+.1f}\%",
                    font_size=26),
            wrapped_label((r"the drift has the textbook sign" if right else
                           r"the drift runs the wrong way: one firm's handful of events is noise"), 4.4, 21,
                          GAIN if right else LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35)
        src = real_data(r"SEC EDGAR 8-K item 2.02 and company facts; Yahoo Finance daily closes")
        sign_line = "That is the textbook sign, on very few events. " if right else "That is the wrong way round. "
        with self.voiceover(
            "Now all of Apple's announcements from late 2015 to 2020, each path started at its own day zero, green when earnings "
            "beat the seasonal forecast, red when they missed. <bookmark mark='a'/> The thick lines are the averages. The day-zero "
            f"move barely lines up with the surprise: a correlation of {pe['jump_corr']:.2f}. <bookmark mark='b'/> After day one, "
            f"the beats drifted {100 * dp:+.1f} percent and the misses {100 * dn:+.1f}. {sign_line}But {pe['n_events']} "
            "events of one company are a lab exercise, not a test, and a seasonal forecast of net income is a crude stand-in for "
            "what analysts expected."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(src), FadeIn(side[:2]))
            self.play(LaggedStart(*[Create(p_) for p_ in paths], lag_ratio=0.15, run_time=5))
            vo.wait_until("a")
            self.play(Create(mp), Create(mn), FadeIn(side[2]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def history(self, pe):
        o, ot = pe["osap"], pe["osap_t"]
        t, cum = np.asarray(pe["osap_cum_t"]), np.asarray(pe["osap_cum"])
        top = np.log10(cum.max() * 2.2)  # headroom for the two date labels inside the plot
        g = axes([1974, 2021], [0, top], x_length=7.0, y_length=4.4,
                 ylabel=r"growth of \$1, long high SUE, short low (log scale)", xticks=[1980, 1990, 2000, 2010, 2020],
                 xfmt=lambda v: f"{int(v)}", yticks=[0, 1], yfmt=lambda v: f"{10 ** v:g}", font_size=17)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        k = ValueTracker(0)
        line = tracing(ax, t, np.log10(cum), k, VALUE)
        marks = VGroup()
        for yr, txt, col in ((o["year"] + 1, r"published", QC.IDEA), (2006, r"2006", GREY_B)):
            marks.add(VGroup(DashedLine(ax.c2p(yr, 0), ax.c2p(yr, top), color=col, stroke_width=2),
                             label(txt, font_size=18, color=col).next_to(ax.c2p(yr, top), DR, buff=0.06)))
        rows = VGroup(
            label(r"Foster, Olsen and Shevlin's SUE long-short, \% a month:", font_size=20, color=GREY_A),
            MathTex(rf"\text{{their sample }}{o['start']}\text{{--}}{o['end']}:\ {o['in']:.2f}\ (t = {ot['in']:.1f})",
                    font_size=27),
            MathTex(rf"\text{{to publication, }}{o['end'] + 1}\text{{--}}{o['year']}:\ {o['pre']:.2f}", font_size=27),
            MathTex(rf"\text{{after, }}{o['year'] + 1}\text{{--2020}}:\ {o['post']:.2f}\ (t = {ot['post']:.1f})",
                    font_size=27),
            MathTex(rf"\text{{2006--2020}}:\ {o['after2006']:.2f}\ (t = {ot['after2006']:.1f})", font_size=27,
                    color=LOSS if abs(ot["after2006"]) < 2 else GAIN),
            wrapped_label(r"Martineau (2022), ``Rest in peace post-earnings announcement drift'': for all but the "
                          r"smallest stocks, prices now absorb the surprise on the day", 4.6, 19, QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.35)
        src = real_data(r"Chen and Zimmermann, open-source asset pricing, release 2024.10: EarningsSurprise")
        gone = abs(ot["after2006"]) < 2
        after_line = ("which is statistically indistinguishable from zero. " if gone else
                      "which is still clearly positive. ")
        with self.voiceover(
            "Thousands of firms is what the open-source replication of the anomaly literature provides. Its version of Foster, "
            "Olsen and Shevlin's 1984 portfolio buys the highest earnings surprises and sells the lowest, every month since 1974. "
            f"<bookmark mark='a'/> In the original sample it earned {o['in']:.2f} percent a month; after publication, "
            f"{o['post']:.2f}, still significant. <bookmark mark='b'/> But look at the line after 2006: {o['after2006']:.2f} "
            f"percent a month, {after_line}Charles Martineau's 2022 paper is titled Rest in Peace Post-Earnings Announcement Drift: "
            "for all but the smallest stocks, prices now absorb the surprise on the day. Others argue that it survives with "
            "different samples; it is contested. <bookmark mark='c'/> So, the desk question: buy at the next open after a big beat? "
            "On today's evidence for large stocks, the news is already in the price."
            " Earnings surprises were one of many accounting signals that once predicted returns. Next: the others, and what became of them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(rows[0]))
            self.add(line)
            self.play(k.animate.set_value(len(t) - 1), run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(marks[0]), FadeIn(rows[1:4]))
            vo.wait_until("b")
            self.play(FadeIn(marks[1]), FadeIn(rows[4]), FadeIn(rows[5]))
        line.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
