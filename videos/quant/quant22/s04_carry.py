from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant22.common import BAD, CARRY, FOR, GOOD, PART, USD, ask, fit_right, illustration, load


class Carry(VoiceoverScene):
    def construct(self):
        c = load("carry")
        self.card()
        self.sort(c)
        self.history(c)
        self.distribution(c)
        self.skew(c)
        self.yen(load("yen2024"))
        self.factor()

    def card(self):
        c = chapter_card(3, r"The carry trade and its crashes", r"What does it pay to lend the high-yielding currency?",
                         lit=(2008, 2024), part=PART)
        with self.voiceover("Chapter three. The carry trade: borrowing where money is cheap, lending where it is dear, "
                            "and what happens when everyone does."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sort(self, c):
        snap = c["snap"]["200706"]
        items = sorted(snap.items(), key=lambda kv: kv[1])
        g = axes([-0.6, len(items) - 0.4], [-5.5, 3.5], x_length=8.0, y_length=4.2, xlabel=r"",
                 ylabel=r"3-month rate less the dollar's, \%", xticks=[], yticks=[-4, -2, 0, 2], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        zero = Line(ax.c2p(-0.6, 0), ax.c2p(len(items) - 0.4, 0), color=WHITE, stroke_width=1.2)
        bars = VGroup()
        for i, (ccy, d) in enumerate(items):
            v = 100 * d
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            col = BAD if i < 3 else (CARRY if i >= len(items) - 3 else GREY_B)
            b_ = Rectangle(width=0.6, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                           fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0])
            bars.add(VGroup(b_, label(ccy, font_size=16).next_to(ax.c2p(i, 0), DOWN if v >= 0 else UP, buff=0.12)))
        side = VGroup(
            label(r"June 2007", font_size=24),
            legend([(CARRY, r"long: the three highest rates"), (BAD, r"short: the three lowest")], font_size=17),
            wrapped_label(r"each month: rank nine currencies by their interest rate against the dollar's, borrow the "
                          r"bottom three, lend the top three, equal weights. The return is each currency's move plus "
                          r"its interest", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "If high-yielding currencies do not fall by their extra interest, the extra interest is a return. The "
            "carry trade collects it. <bookmark mark='a'/> Each month, rank currencies by their interest rate against "
            "the dollar's. Here is June 2007: the yen four and a half points below the dollar, the Swiss franc almost "
            "three below, the New Zealand dollar three points above. <bookmark mark='b'/> Borrow the three cheapest, lend "
            "the three dearest, and hold for a month. The yen and the franc were the classic funding currencies, the "
            "New Zealand and Australian dollars the classic targets."
        ) as vo:
            self.play(FadeIn(g), Create(zero), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.12))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def history(self, c):
        t, cum = np.asarray(c["t"]), 100 * np.asarray(c["cum"])
        g = axes([1999, 2026], [-10, 110], x_length=8.2, y_length=4.4, xlabel=r"year",
                 ylabel=r"cumulative log return, \%", xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                 yticks=[0, 25, 50, 75, 100], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, cum, CARRY, stroke_width=2.6)
        st = c["stats"]
        marks = VGroup()
        for w in c["worst"][:3]:
            k = int(np.argmin(np.abs(t - w["t"])))
            marks.add(VGroup(Dot(ax.c2p(t[k], cum[k]), color=BAD, radius=0.06),
                             label(rf"{w['ym'] // 100}-{w['ym'] % 100:02d}: {100 * w['r']:.1f}\%", font_size=15,
                                   color=BAD).next_to(ax.c2p(t[k], cum[k]), DOWN, buff=0.12)))
        side = VGroup(
            MathTex(rf"\text{{mean}}\ {100 * st['mean']:.1f}\%,\ \text{{vol}}\ {100 * st['vol']:.1f}\%", font_size=24),
            MathTex(rf"\text{{Sharpe}}\ {st['sharpe']:.2f},\ \text{{skew}}\ {st['skew']:.2f}", font_size=24, color=CARRY),
            wrapped_label(rf"{st['n']} months, 1999--2025; no costs. The return comes slowly and leaves quickly: the "
                          r"worst months are the autumn of 2008 and March 2020", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Over twenty-six years the trade earned about "
            f"{100 * st['mean']:.0f} percent a year with {100 * st['vol']:.0f} percent volatility: a Sharpe ratio of "
            f"{st['sharpe']:.1f}, before costs. <bookmark mark='a'/> But look at how it earned it. Up, slowly, for "
            "years; then down, fast. <bookmark mark='b'/> October 2008 alone took eleven percent, more than three "
            "years of average returns, as the yen soared and the Australian dollar, already a fifth lower than in the "
            "summer, kept falling. March 2020 "
            "did it again. Traders have a phrase for it: picking up nickels in front of a steamroller."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[0]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.4), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def distribution(self, c):
        h, e = np.asarray(c["hist"], float), 100 * np.asarray(c["edges"])
        st = c["stats"]
        g = axes([e[0], e[-1]], [0, max(h) * 1.15], x_length=7.6, y_length=4.2, xlabel=r"monthly return, \%",
                 ylabel=r"months", xticks=[-10, -5, 0, 5], yticks=[], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bw = e[1] - e[0]
        bars = VGroup(*[Rectangle(width=max(ax.c2p(e[i] + bw, 0)[0] - ax.c2p(e[i], 0)[0] - 0.02, 0.01),
                                  height=max(ax.c2p(0, h[i])[1] - ax.c2p(0, 0)[1], 0.005), stroke_width=0,
                                  fill_color=BAD if e[i] < -4 else CARRY, fill_opacity=0.8).move_to(
            [ax.c2p(e[i] + bw / 2, 0)[0], (ax.c2p(0, h[i])[1] + ax.c2p(0, 0)[1]) / 2, 0]) for i in range(len(h))])
        m, s = 100 * st["mean"] / 12, 100 * st["vol"] / np.sqrt(12)
        xs = np.linspace(e[0], e[-1], 200)
        nrm = curve(ax, xs, h.sum() * bw * np.exp(-0.5 * ((xs - m) / s) ** 2) / (s * np.sqrt(2 * np.pi)), GREY_A,
                    stroke_width=2.5)
        z = (st["worst"] * 100 - m) / s
        from scipy.stats import norm
        odds = 1 / norm.cdf(z)
        odds_words = ("a hundred million" if odds > 1e8 else "ten million" if odds > 1e7 else "a million")
        side = VGroup(
            legend([(CARRY, r"carry, monthly"), (GREY_A, r"a normal with the same mean and volatility")], font_size=17),
            MathTex(rf"\text{{worst month}} = {z:.1f}\,\sigma", font_size=26, color=BAD),
            wrapped_label(rf"negative skewness: many small gains, a few large losses. A normal distribution with the same "
                          rf"volatility gives a month like October 2008 less than one chance in {odds_words}", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The distribution of monthly returns tells the same story. <bookmark mark='a'/> Most months are small "
            "gains. <bookmark mark='b'/> The left tail is long: the worst month is "
            f"{abs(z):.0f} standard deviations below the mean, a month a normal distribution would expect less than once "
            f"in {odds_words}. Markus Brunnermeier, Stefan Nagel and Lasse Pedersen called it carry's crash risk, and "
            "argued that it is the reward: investors are paid for holding currencies that fall when everything else "
            "does, and when traders must unwind at once."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.03), Create(nrm), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def skew(self, c):
        per = c["per"]
        xs = np.array([100 * per[k]["mean_diff"] for k in per])
        ys = np.array([per[k]["skew"] for k in per])
        g = axes([-2.5, 2.5], [-0.8, 0.4], x_length=7.0, y_length=4.2, xlabel=r"average rate less the dollar's, \%",
                 ylabel=r"skewness of monthly excess return", xticks=[-2, -1, 0, 1, 2], yticks=[-0.6, -0.3, 0, 0.3],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[VGroup(Dot(ax.c2p(a, b), color=CARRY if a > 0 else FOR, radius=0.08),
                               label(k, font_size=16).next_to(ax.c2p(a, b), UR, buff=0.06))
                        for k, a, b in zip(per, xs, ys)])
        b_ = np.polyfit(xs, ys, 1)
        fit = Line(ax.c2p(-2.3, np.polyval(b_, -2.3)), ax.c2p(2.3, np.polyval(b_, 2.3)), color=BAD, stroke_width=2.5)
        side = VGroup(
            MathTex(rf"\text{{correlation}} = {c['skew_diff_corr']:.2f}", font_size=28, color=BAD),
            wrapped_label(r"each currency's monthly excess return for a dollar investor, 1999--2025. The currencies that "
                          r"pay more interest are the ones that crash: Brunnermeier, Nagel and Pedersen (2008) found the "
                          r"same across 1986--2006", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Currency by currency. <bookmark mark='a'/> On the horizontal axis, each one's average interest rate "
            "against the dollar's; on the vertical, the skewness of what it paid a dollar investor. "
            "<bookmark mark='b'/> The higher the interest, the more negative the skew. The Australian dollar pays the "
            "most and falls hardest; the Swiss franc pays the least and rises in a crisis, a safe haven. The interest "
            "differential is the price of the crash."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def yen(self, y):
        t, v = np.asarray(y["t"]), np.asarray(y["usdjpy"])
        tn, nk = np.asarray(y["nikkei_t"]), np.asarray(y["nikkei"]) / 1000
        g1 = axes([2024.41, 2024.75], [138, 165], x_length=5.8, y_length=3.6, xlabel=r"2024", ylabel=r"yen per dollar",
                  xticks=[], yticks=[140, 150, 160], font_size=13)
        g2 = axes([2024.41, 2024.75], [30, 43], x_length=5.8, y_length=3.6, xlabel=r"2024", ylabel=r"Nikkei 225, thousands",
                  xticks=[], yticks=[32, 36, 40], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).shift(DOWN * 0.6)
        l1 = curve(g1.ax, t, v, FOR, stroke_width=2.6)
        l2 = curve(g2.ax, tn, nk, BAD, stroke_width=2.6)
        bo = DashedLine(g1.ax.c2p(2024.58, 138), g1.ax.c2p(2024.58, 165), color=GREY_B, stroke_width=1.5)
        bol = label(r"31 July: the Bank of Japan raises rates", font_size=15, color=GREY_A).next_to(
            g1.ax.c2p(2024.58, 165), DOWN, buff=0.1).shift(LEFT * 0.4)
        head = VGroup(
            MathTex(rf"\text{{peak}}\ {y['peak']['v']:.1f}\ (10\ \text{{July}})\ \to\ {y['aug5']:.1f}\ (5\ \text{{August}})",
                    font_size=26, color=FOR),
            MathTex(rf"\text{{Nikkei, 5 August}}: {100 * y['nikkei_aug5']:.1f}\%;\ \text{{6 August}}: "
                    rf"{100 * y['nikkei_aug6']:+.1f}\%", font_size=26, color=BAD),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The latest crash came in the summer of 2024. For years the yen had been the cheapest currency to borrow, "
            "and investors everywhere had borrowed it. <bookmark mark='a'/> In July the yen began to strengthen; on the "
            "thirty-first the Bank of Japan raised its rate, and the unwind began. In four weeks the dollar fell from "
            f"{y['peak']['v']:.0f} yen to {y['aug5']:.0f}. <bookmark mark='b'/> On Monday the fifth of August, "
            f"Japan's stock index fell {abs(100 * y['nikkei_aug5']):.1f} percent, its largest fall since 1987, as "
            "positions financed in yen were sold everywhere at once; the next day it recovered most of it. A "
            "funding currency is a crowded short, and crowded shorts unwind together."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(l1), Create(bo), FadeIn(bol), run_time=2)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(head), run_time=2)
        self.add(illustration(r"FRED: DEXJPUS, NIKKEI225, daily"))
        self.wait(0.4)
        self.clear_scene()

    def factor(self):
        rows = [cmath(r"\mathbb{E}[rx^{j}]", r"=", r"\beta_j\,\lambda_{HML_{FX}}", font_size=42,
                      colors={r"\mathbb{E}[rx^{j}]": CARRY}),
                cmath(r"\beta_j", r"=", r"\frac{\text{cov}(rx^{j},\ HML_{FX})}{\text{var}(HML_{FX})}", font_size=40)]
        whys = [why(r"Lustig, Roussanov and Verdelhan (2011): one factor, the carry trade's own return (high-rate minus "
                    r"low-rate currencies), explains why some currency portfolios earn more than others: their exposure "
                    r"to it, times its price"),
                why(r"and the factor's return is high in calm times and collapses when global volatility jumps: carry is "
                    r"a bet on calm, priced like one. Part 24 meets carry in every asset class")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Is it a risk premium, then? Hanno Lustig, Nikolai Roussanov and Adrien Verdelhan sorted currencies into "
            "portfolios by their interest rates, as we did, and found that one factor explains the lot: the carry "
            "trade's own return. <bookmark mark='a'/> A portfolio earns more the more it moves with that factor, and "
            "the factor itself pays in calm times and collapses when the world's volatility jumps. The carry trade is "
            "selling insurance against global crises. It pays, on average, because the crises are real."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"a carry trade has a Sharpe ratio of 0.4 and a skewness of $-0.8$. How would you size it, and what "
                r"would you add to the book to survive its worst month?")
        with self.voiceover("A carry trade has a Sharpe ratio of point four and a skew of minus point eight. How would you "
                            "size it, and what would you add to the book to survive its worst month?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
