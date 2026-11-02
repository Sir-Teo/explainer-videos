from __future__ import annotations

import numpy as np
from scipy import stats as sstats

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import BTC, GAUSS, PART, REAL, TAIL, VOL, day_text, hist_bars, load, real_data, sci


class Tails(VoiceoverScene):
    def construct(self):
        t = load("tails")
        self.card()
        self.histogram(t)
        self.tally(t)
        self.loglog(t)
        self.hill(t)

    def card(self):
        c = chapter_card(5, r"Heavy tails", r"How often do the extreme days come?", lit=(1929, 1987), part=PART)
        with self.voiceover("Chapter five. Heavy tails."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def histogram(self, t):
        e, h = np.asarray(t["hist_edges"]), np.asarray(t["hist"])
        g = axes([-6, 6], [-5, 0], x_length=6.2, y_length=4.6, xlabel=r"daily return, in standard deviations",
                 ylabel=r"density (log scale)", xticks=[-6, -3, 0, 3, 6], yticks=[-4, -2, 0],
                 yfmt=lambda v: f"10^{{{int(v)}}}", font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        lh = np.where(h > 0, np.log10(np.maximum(h, 1e-12)), -9)
        bars_ = VGroup()
        for a, b, y in zip(e[:-1], e[1:], lh):
            if y < -5:
                continue
            p0, p1 = ax.c2p(a, -5), ax.c2p(b, y)
            bars_.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=REAL,
                                fill_opacity=0.8).move_to([(p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0]))
        xs = np.linspace(-6, 6, 300)
        gauss = curve(ax, xs, np.clip(np.log10(sstats.norm.pdf(xs)), -5, 0), GAUSS, stroke_width=3.5)
        # linear-scale inset of the same thing: the peak
        g2 = axes([-4, 4], [0, 0.65], x_length=4.6, y_length=2.6, xlabel=r"the same, ordinary scale",
                  xticks=[-3, 0, 3], font_size=16).to_edge(RIGHT, buff=0.6).shift(UP * 1.4)
        a2 = g2.ax
        mk = (e[:-1] >= -4) & (e[1:] <= 4)
        hb = hist_bars(a2, np.append(e[:-1][mk], e[1:][mk][-1]), h[mk], REAL, opacity=0.8)
        gauss2 = curve(a2, xs[(xs >= -4) & (xs <= 4)], sstats.norm.pdf(xs[(xs >= -4) & (xs <= 4)]), GAUSS, stroke_width=3)
        leg = legend([(REAL, r"US market, 1926--2020 (24{,}896 days)"), (GAUSS, r"bell curve, same variance")],
                     font_size=21).next_to(g2, DOWN, buff=0.5).align_to(g2, LEFT)
        kur = MathTex(rf"\text{{excess kurtosis}} = {t['kurt']:.1f}", font_size=34, color=REAL).next_to(leg, DOWN, buff=0.35)
        kur.align_to(leg, LEFT)
        kur0 = label(r"(a bell curve: 0)", font_size=22, color=GAUSS).next_to(kur, DOWN, buff=0.1).align_to(kur, LEFT)
        with self.voiceover(
            f"Every one of the {t['n']:,} trading days since 1926, measured in standard deviations, against a "
            "bell curve with the same spread. <bookmark mark='a'/> On an ordinary scale the difference looks small: "
            "the real returns have a taller, narrower peak. More quiet days than a bell curve allows. "
            "<bookmark mark='b'/> On a log scale, which magnifies the rare events, the truth comes out. The bell "
            "curve, the grey parabola, falls off a cliff: beyond five standard deviations it expects almost "
            "nothing. The real returns keep going, past ten, out to the edge of the chart. <bookmark mark='c'/> "
            f"One number summarizes it: the excess kurtosis, zero for a bell curve, is {t['kurt']:.1f} for the "
            "market. Quiet days, and then, rarely, enormous ones."
        ) as vo:
            self.play(FadeIn(g2), FadeIn(hb), Create(gauss2), FadeIn(leg))
            vo.wait_until("a")
            self.wait(1.0)
            vo.wait_until("b")
            self.play(FadeIn(g), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_], lag_ratio=0.02, run_time=3))
            self.play(Create(gauss), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(kur), FadeIn(kur0))
        self.wait(0.4)
        self.clear_scene()

    def tally(self, t):
        ks = ["3", "4", "5", "7", "10"]
        hdr = [label(r"days beyond", font_size=24, color=GREY_A), label(r"seen, 1926--2020", font_size=24, color=REAL),
               label(r"a bell curve expects", font_size=24, color=GAUSS)]
        cells = list(hdr)
        rows = [VGroup(*hdr)]
        for k in ks:
            exp = t["expected"][k]
            e_tex = f"{exp:.0f}" if exp >= 10 else (f"{exp:.1f}" if exp >= 0.1 else sci(exp))
            r_ = [MathTex(rf"{k}\,\sigma", font_size=32), MathTex(rf"{t['beyond'][k]}", font_size=32, color=REAL),
                  MathTex(e_tex, font_size=32, color=GAUSS)]
            cells += r_
            rows.append(VGroup(*r_))
        grid = VGroup(*cells).arrange_in_grid(len(ks) + 1, 3, buff=(1.0, 0.3), col_alignments="crr")
        grid.move_to(UP * 0.4)
        foot = wrapped_label(rf"the worst day: {day_text(t['min_date'])}, ${100 * t['min']:.1f}\%$; the best: "
                             rf"{day_text(t['max_date'])}, ${100 * t['max']:+.1f}\%$", 11.0, 24, GREY_A)
        foot.next_to(grid, DOWN, buff=0.6)
        with self.voiceover(
            "Count them. Days more than three standard deviations from the average: the bell curve expects "
            f"{t['expected']['3']:.0f} in ninety-four years; there were {t['beyond']['3']}. <bookmark mark='a'/> "
            f"Beyond four: it expects about {t['expected']['4']:.1f}; there were {t['beyond']['4']}. "
            f"<bookmark mark='b'/> Beyond five: it expects one every seventy lifetimes of the market; there were "
            f"{t['beyond']['5']}. <bookmark mark='c'/> Beyond seven, {t['beyond']['7']} days. Beyond ten, "
            f"{t['beyond']['10']}, where the bell curve's answer has nineteen zeros after the decimal point. "
            f"<bookmark mark='d'/> The worst of them was the {day_text(t['min_date'])}, minus "
            f"{abs(100 * t['min']):.1f} percent; the best, a rally in March 1933, plus {100 * t['max']:.1f}. A bell "
            "curve is not a slightly wrong model of the tails. It is wrong by many orders of magnitude."
        ) as vo:
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            self.play(FadeIn(rows[5]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loglog(self, t):
        g = axes([np.log10(0.6), np.log10(25)], [-5, 0], x_length=7.2, y_length=4.8,
                 xlabel=r"size of the move $u$, in standard deviations (log scale)",
                 ylabel=r"fraction of days with $|r| > u$ (log scale)", xticks=[0, np.log10(3), 1],
                 xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-4, -3, -2, -1, 0], yfmt=lambda v: f"10^{{{int(v)}}}",
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax

        def pts(u, p):
            u, p = np.asarray(u), np.asarray(p)
            m = (p > 0) & (u > 0.6) & (u < 25)
            return np.log10(u[m]), np.log10(p[m])

        x1, y1 = pts(t["u"], t["p"])
        xb, yb = pts(t["btc_u"], t["btc_p"])
        xg, yg = pts(t["gauss_u"], t["gauss_p"])
        mg = yg > -5
        us = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=REAL) for a, b in zip(x1, y1)])
        bt = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=BTC) for a, b in zip(xb, yb)])
        ga = curve(ax, xg[mg], yg[mg], GAUSS, stroke_width=3.5)
        # a slope -3 guide through the US tail at 3 sigma
        p3 = np.interp(np.log10(3), x1, y1)
        gx = np.array([np.log10(2), np.log10(22)])
        guide = DashedLine(ax.c2p(gx[0], p3 - 3 * (gx[0] - np.log10(3))), ax.c2p(gx[1], p3 - 3 * (gx[1] - np.log10(3))),
                           color=TAIL, stroke_width=2.5)
        gl = MathTex(r"P(|r| > u) \propto u^{-3}", font_size=30, color=TAIL).next_to(ax.c2p(np.log10(10), -2.6), UR,
                                                                                    buff=0.1)
        card = theorem_card(r"The inverse cubic law", r"Gopikrishnan, Meyer, Amaral and Stanley (1998): the tails of "
                            r"stock returns fall off like a power, $P(|r| > u) \sim u^{-\alpha}$ with "
                            r"$\alpha \approx 3$: in 40 million five-minute returns of 1{,}000 US stocks, and in the "
                            r"S\&P 500.", width=5.4, font_size=21, kind=r"Fact").to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
        leg = legend([(REAL, r"US market, daily"), (BTC, r"Bitcoin, daily, 2017--2020"), (GAUSS, r"bell curve"),
                      (TAIL, r"slope $-3$: $P(|r| > u) \propto u^{-3}$")],
                     font_size=21).next_to(card, DOWN, buff=0.4).align_to(card, LEFT)
        with self.voiceover(
            "A better picture of a tail: the fraction of days with a move bigger than u, against u, both on log "
            "scales. <bookmark mark='a'/> The bell curve, in grey, dives. <bookmark mark='b'/> The market's tail, in "
            "blue, comes down as a straight line. On log scales a straight line is a power law: the chance of a "
            "move bigger than u falls like u to some power. <bookmark mark='c'/> And the power is close to three. "
            "Twice as large a move is about eight times rarer, not millions of times. <bookmark mark='d'/> Bitcoin, "
            "in orange, with four times the volatility, measured in its own standard deviations, has the same "
            "shape. In 1998 a group of physicists found this exponent of about three in tens of millions of "
            "five-minute returns of American stocks, and called it the inverse cubic law. It has turned up in "
            "nearly every market since."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(ga), FadeIn(leg[2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in us], lag_ratio=0.01, run_time=2.5), FadeIn(leg[0]))
            vo.wait_until("c")
            self.play(Create(guide), FadeIn(leg[3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(d) for d in bt], lag_ratio=0.01, run_time=2), FadeIn(leg[1]))
            self.play(FadeIn(card, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def hill(self, t):
        ks, hc = np.asarray(t["ks"], float), np.asarray(t["hill_curve"])
        g = axes([np.log10(20), np.log10(4200)], [1.5, 5.0], x_length=6.6, y_length=4.2,
                 xlabel=r"$k$: how many of the largest days are used (log scale)", ylabel=r"Hill estimate of $\alpha$",
                 xticks=[np.log10(30), 2, np.log10(300), 3], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[2, 3, 4, 5],
                 font_size=18).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        ln = curve(ax, np.log10(ks), np.clip(hc, 1.5, 5.0), REAL, stroke_width=3.5)
        k2 = 0.02 * t["n"]
        mark = DashedLine(ax.c2p(np.log10(k2), 1.5), ax.c2p(np.log10(k2), 5.0), color=QC.IDEA, stroke_width=2)
        ml = label(r"top 2\%", font_size=20, color=QC.IDEA).next_to(ax.c2p(np.log10(k2), 5.0), DOWN, buff=0.08).shift(RIGHT * 0.5)
        three = DashedLine(ax.c2p(np.log10(20), 3), ax.c2p(np.log10(4200), 3), color=TAIL, stroke_width=1.8)
        hill_def = MathTex(r"\hat\alpha = \Big(\frac1k\sum_{i=1}^{k}\ln\frac{|r|_{(i)}}{|r|_{(k+1)}}\Big)^{-1}",
                           font_size=34).to_edge(RIGHT, buff=0.6).shift(UP * 2.2)
        hw = why(r"Hill (1975): the average log-excess of the $k$ largest moves").next_to(hill_def, DOWN, buff=0.12)
        res = VGroup(
            MathTex(rf"\text{{US, both tails}}\ \ \hat\alpha = {t['alpha']:.2f}", font_size=30, color=REAL),
            MathTex(rf"\text{{US, losses only}}\ \ \hat\alpha = {t['alpha_left']:.2f}", font_size=30, color=REAL),
            MathTex(rf"\text{{Bitcoin}}\ \ \hat\alpha = {t['btc_alpha']:.2f}", font_size=30, color=BTC),
            MathTex(rf"\text{{US, scaled by recent volatility}}\ \ \hat\alpha = {t['alpha_norm']:.2f}", font_size=30,
                    color=VOL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(hw, DOWN, buff=0.5)
        res.align_to(hill_def, LEFT)
        what = wrapped_label(r"$\alpha$ above 2: the variance exists; at 4 or below, the kurtosis does not settle "
                             r"down (chapter 8)", 5.4, 21, GREY_A).next_to(res, DOWN, buff=0.4).align_to(res, LEFT)
        hw = wrapped_label(r"Hill (1975): the average log-excess of the $k$ largest moves", 5.4, 22, GREY_B)
        hw.next_to(hill_def, DOWN, buff=0.12)
        block = VGroup(hill_def, hw, res, what)
        res.next_to(hw, DOWN, buff=0.45)
        what.next_to(res, DOWN, buff=0.35)
        for m in (hw, res, what):
            m.align_to(hill_def, LEFT)
        block.to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The exponent can be estimated directly. Bruce Hill's estimator, from 1975, takes the k largest moves "
            "and averages how far, in logs, each one exceeds the next largest. <bookmark mark='a'/> Plotted "
            "against k it is never perfectly flat: with too few days it is noisy, and with too many it starts "
            "measuring the middle of the distribution instead of the tail. Where the tail is in charge, the top "
            "few hundred days, it passes through three. Using the largest two percent of days, the "
            f"market's exponent is {t['alpha']:.2f}, and for losses alone, {t['alpha_left']:.2f}. Bitcoin's, from its "
            f"first three and a half years, is {t['btc_alpha']:.1f}. <bookmark mark='b'/> And here is a clue for the "
            "next chapter. Divide each day's return by the volatility of the weeks just before it, and the "
            f"exponent rises to {t['alpha_norm']:.1f}: much of the tail comes from calm days and wild days being "
            "mixed together. <bookmark mark='c'/> An exponent near three means the average and the variance exist, "
            "but higher moments barely do. That will matter when we ask, in chapter eight, whether the variance "
            "can be trusted at all."
            " First, a second fact: the big moves come together. Next."
        ) as vo:
            self.play(FadeIn(g), Write(hill_def), FadeIn(hw))
            vo.wait_until("a")
            self.play(Create(ln), Create(three), run_time=2)
            self.play(Create(mark), FadeIn(ml), FadeIn(res[0]), FadeIn(res[1]))
            self.play(FadeIn(res[2]))
            vo.wait_until("b")
            self.play(FadeIn(res[3]))
            vo.wait_until("c")
            self.play(FadeIn(what))
        self.wait(0.4)
        self.clear_scene()
