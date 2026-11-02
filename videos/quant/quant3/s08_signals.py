from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import GAIN, LOSS, PART, load, real_data

SIG_COLORS = {"AC": QC.LOSS, "OP": QC.GAIN, "INV": QC.SPOT, "BE-ME": QC.IDEA, "E-P": QC.OPTION}
SHORT = {"AC": r"accruals", "OP": r"profitability", "INV": r"investment", "BE-ME": r"book-to-market",
         "E-P": r"earnings yield"}


class Signals(VoiceoverScene):
    def construct(self):
        f = load("factors")
        e = load("envelope")
        self.card()
        self.pead()
        self.curves(f)
        self.decay(f)
        self.counter(e)

    def card(self):
        c = chapter_card(7, r"Accounting signals that became factors", r"Do the statements predict returns?",
                         lit=(1968,), part=PART)
        with self.voiceover("Chapter seven. Accounting signals that became factors."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def pead(self):
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
            "Do the statements move prices? In 1968 Ray Ball and Philip Brown sorted firms by whether their annual "
            "earnings beat the year before, and followed their returns, beyond what the market did, for a year "
            "before and six months after the report. <bookmark mark='a'/> The firms with good news had risen, and "
            "the firms with bad news had fallen, mostly before the report came out: the market learns most of it "
            "from other sources first. <bookmark mark='b'/> But not all of it. After the announcement the prices "
            "kept drifting in the same direction. In 1989 Victor Bernard and Jacob Thomas showed this drift lasts "
            "about sixty trading days, and that it survives every risk adjustment they tried. The market under-reacts "
            "to earnings news. It was one of the first well-documented anomalies, and quant desks still trade it."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(lg), Create(lb), FadeIn(side[1]), run_time=3)
            vo.wait_until("b")
            self.play(Create(drift), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def curves(self, f):
        g = axes([1963, 2021], [np.log10(0.4), np.log10(16)], x_length=6.9, y_length=4.8,
                 ylabel=r"growth of \$1 in the long-short portfolio (log scale)", xticks=[1970, 1990, 2010],
                 xfmt=lambda x: f"{int(x)}", yticks=list(np.log10([0.5, 1, 2, 4, 8, 16])),
                 yfmt=lambda u: f"{10 ** u:g}", font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines, pubs, legs = VGroup(), VGroup(), []
        for k in f["order"]:
            s = f["signals"][k]
            t, c = np.asarray(s["t"]), np.log10(np.asarray(s["cum"]))
            col = SIG_COLORS[k]
            lines.add(curve(ax, t, c, col, stroke_width=2.6))
            i = int(np.searchsorted(t, s["year"] + 1))
            if i < len(t):
                pubs.add(Dot(ax.c2p(t[i], c[i]), radius=0.08, color=col).set_stroke(WHITE, width=1.5))
            legs.append((col, rf"{SHORT[k]}: {s['who']}"))
        leg = legend(legs, font_size=18)
        hint = VGroup(Dot(radius=0.07, color=GREY_B).set_stroke(WHITE, width=1.5),
                      label(r"the year after publication", font_size=19, color=GREY_B)).arrange(RIGHT, buff=0.12)
        how = wrapped_label(r"each line buys the top decile and sells the bottom, value-weighted, rebalanced yearly; "
                            r"before costs", 4.6, 19, GREY_B)
        VGroup(leg, hint, how).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)
        src = real_data(r"Kenneth French's sorts, July 1963 -- December 2020")
        with self.voiceover(
            "Accounting signals became the first factors. Five of them, measured on Kenneth French's public "
            "portfolios since 1963. Each line buys the tenth of stocks with the most attractive value of the signal "
            "and sells the tenth with the least. Low accruals, Sloan's signal. High profitability. Low investment, "
            "firms that grow their assets slowly. Cheap on book value, and cheap on earnings. "
            "<bookmark mark='a'/> Over the whole sample, most of them made money: a dollar in the investment "
            "spread became about eight, in accruals nearly seven. Piotroski's F-score of 2000 combined nine such "
            "accounting tests into one. <bookmark mark='b'/> The dots mark the year after each signal was "
            "published. Look at what the lines do after their dot."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(how))
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3, run_time=5), FadeIn(leg))
            vo.wait_until("a")
            self.play(Indicate(lines[2], scale_factor=1.0), Indicate(lines[0], scale_factor=1.0))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pubs], lag_ratio=0.3), FadeIn(hint))
        self.wait(0.6)
        self.clear_scene()

    def decay(self, f):
        order = f["order"]
        g = axes([0, len(order)], [-0.02, 0.08], x_length=7.6, y_length=4.4, ylabel=r"average return a year",
                 xticks=[], yticks=[-0.02, 0, 0.02, 0.04, 0.06, 0.08], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        w = (ax.c2p(0.3, 0)[0] - ax.c2p(0, 0)[0])
        pre_b, post_b, names = VGroup(), VGroup(), VGroup()
        for i, k in enumerate(order):
            s = f["signals"][k]
            for j, (key, col, grp) in enumerate([("pre", SIG_COLORS[k], pre_b), ("post", GREY_B, post_b)]):
                v = s[key]["mean"]
                x = i + 0.33 + 0.34 * j
                top, bot = ax.c2p(x, max(v, 0)), ax.c2p(x, min(v, 0))
                r = Rectangle(width=w, height=max(top[1] - bot[1], 0.01), stroke_width=0, fill_color=col,
                              fill_opacity=0.9 if j == 0 else 0.6).move_to((top + bot) / 2)
                t_ = MathTex(rf"{100 * v:.1f}", font_size=18, color=col).next_to(r, UP if v >= 0 else DOWN, buff=0.06)
                grp.add(VGroup(r, t_))
            names.add(label(SHORT[k], font_size=17, color=SIG_COLORS[k]).move_to(ax.c2p(i + 0.5, -0.02) + DOWN * 0.3))
        leg = VGroup(
            label(r"bright: before publication", font_size=21, color=WHITE),
            label(r"grey: after publication", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        avg_pre = np.mean([f["signals"][k]["pre"]["mean"] for k in order])
        avg_post = np.mean([f["signals"][k]["post"]["mean"] for k in order])
        side = VGroup(
            leg,
            MathTex(rf"\text{{average: }}{100 * avg_pre:.1f}\% \to {100 * avg_post:.1f}\%", font_size=32),
            wrapped_label(r"McLean and Pontiff (2016), 97 predictors: returns 26\% lower out of sample and 58\% lower "
                          r"after publication", 4.6, 22, QC.IDEA),
            wrapped_label(r"profitability, published in 2013, has too few years after to judge", 4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Split each signal's history at its publication. Before: the bright bars. After: the grey ones. "
            "<bookmark mark='a'/> Accruals fell from five percent a year to two. Investment, from over six to "
            "slightly negative. Book-to-market, from seven to one. Earnings yield, from seven and a half to under "
            "three. Profitability was published too recently to judge. <bookmark mark='b'/> This is not one unlucky "
            "sample. In 2016 David McLean and Jeffrey Pontiff took ninety-seven published predictors and found their "
            "returns were about a quarter lower just outside the original sample, which is what you expect if part "
            "of the effect was luck, and more than half lower after publication, which is what you expect if "
            "investors read the papers and traded the effect away. Either way, a backtest of a published signal "
            "overstates its future."
        ) as vo:
            self.play(FadeIn(g), FadeIn(names), FadeIn(leg))
            self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in pre_b], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(b[1]) for b in pre_b], lag_ratio=0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in post_b], lag_ratio=0.4, run_time=4))
            self.play(FadeIn(side[1]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def counter(self, e):
        big = MathTex(str(e["trials"]), font_size=150, color=QC.HOUSE)
        cap = label(r"the trial counter: configurations tried so far, across the whole series", font_size=26,
                    color=GREY_A).next_to(big, DOWN, buff=0.3)
        add = VGroup(
            label(r"this part: five accounting signals tested, one CAPE forecast registered", font_size=22,
                  color=GREY_B),
            label(r"their hold-outs, 2021 onward, are sealed", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.15).next_to(cap, DOWN, buff=0.5)
        VGroup(big, cap, add).move_to(ORIGIN)
        with self.voiceover(
            "And every signal we look at is a trial. We tested five here, and registered one forecast. The House "
            "counts them all, across the series, because the more configurations a researcher tries, the more one "
            "of them will look good by chance. Part six shows how to deflate a result by that count. The hold-out "
            "years for these signals, 2021 onward, are sealed until then."
        ):
            self.play(FadeIn(big, scale=0.8), FadeIn(cap))
            self.play(FadeIn(add))
        self.wait(0.4)
        self.clear_scene()
