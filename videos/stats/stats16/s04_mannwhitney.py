from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats16.common import *  # noqa: F403


class MannWhitney(VoiceoverScene):
    def construct(self):
        self.card()
        self.flights()
        self.rank_sum()
        self.pairs()
        self.null()
        self.auc()
        self.question()

    def card(self):
        card = chapter_card(3, r"Two samples, \ ranked", r"Wilcoxon, \ Mann and Whitney", lit=(1947,), part=PART)
        with self.voiceover("Chapter three. Two samples, ranked."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def strips(self, d, center=(0, 1.0, 0)):
        w, c = np.asarray(d["warm"]), np.asarray(d["cold"])
        A = axes([50, 84], [0, 2], x_length=10.4, y_length=1.8, xlabel=r"launch temperature, \ $^\circ$F", xticks=[50, 60, 70, 80],
                 center=list(center))
        ax = A.ax

        def strip(vals, y, col):
            seen: dict[float, int] = {}
            g = VGroup()
            for v in vals:
                k = seen.get(v, 0)
                seen[v] = k + 1
                g.add(Dot(ax.c2p(v, y + 0.28 * k), radius=0.09, color=col))
            return g

        top = strip(w, 1.25, S.CTRL)
        bot = strip(c, 0.3, RES)
        lt = label(r"no distress (16)", font_size=20, color=S.CTRL).next_to(ax.c2p(50, 1.3), LEFT, buff=0.15)
        lb = label(r"distress (7)", font_size=20, color=RES).next_to(ax.c2p(50, 0.35), LEFT, buff=0.15)
        return A, ax, top, bot, VGroup(lt, lb)

    def flights(self):
        d = load("mw")
        A, ax, top, bot, labs = self.strips(d)
        VGroup(A, top, bot, labs).shift(RIGHT * 0.6)
        rows = fit_rows(VGroup(
            label(r"Part 14's 23 shuttle flights before \emph{Challenger}", font_size=24),
            label(r"temperatures: \ not normal, \ ties, \ small samples", font_size=24),
            label(r"are flights with O-ring distress colder?", font_size=26, color=RES),
        ), 12.0, 0.3, [0, -1.8, 0])
        tag = historical_tag(r"Dalal, \ Fowlkes \& Hoadley (1989)", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Part 14's twenty-three shuttle flights before Challenger return. <bookmark mark='b'/> Sixteen "
            "had no O-ring distress, seven had some. Here are their launch temperatures. <bookmark mark='c'/> The samples are "
            "small, the temperatures aren't normal, and several are tied. <bookmark mark='d'/> Part 14 fitted a logistic "
            "regression. Here's a question that needs no normal model: are the distress flights colder, in the sense that a random "
            "distress flight tends to be colder than a random undistressed one?"
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(labs), LaggedStart(*[FadeIn(x, scale=1.5) for x in [*top, *bot]], lag_ratio=0.04))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def rank_sum(self):
        d = load("mw")
        w, c = np.asarray(d["warm"]), np.asarray(d["cold"])
        allv = np.r_[w, c]
        r = stats.rankdata(allv)
        order = np.argsort(allv, kind="stable")
        xs = np.linspace(-6.2, 6.2, 23)
        cells = VGroup()
        for j, i in enumerate(order):
            col = S.CTRL if i < 16 else RES
            rk = f"{r[i]:g}"
            cells.add(VGroup(MathTex(f"{allv[i]:.0f}", font_size=24, color=col), MathTex(rk, font_size=22, color=col))
                      .arrange(DOWN, buff=0.3).move_to([xs[j], 1.6, 0]))
        rows = [
            cmath(r"R", r"=", r"\text{sum of the distress flights' ranks} = 52.5", font_size=30),
            cmath(r"U", r"=", r"R - \tfrac{7 \cdot 8}{2} = 24.5", font_size=30),
            cmath(r"\text{ties}", r":", r"\text{share the average rank (midranks)}", font_size=30),
        ]
        whys = [why(r"Wilcoxon's rank sum (1945)"), why(r"Mann \& Whitney's $U$ (1947): \ the same test"),
                why(r"70 appears four times: \ ranks 11 to 14, \ each 12.5")]
        with self.voiceover(
            "<bookmark mark='a'/> Pool all twenty-three temperatures, sort them, and rank them from one to twenty-three. Tied "
            "temperatures share the average of their ranks: the four flights at seventy degrees occupy ranks eleven to fourteen, "
            "so each gets twelve and a half. <bookmark mark='b'/> Wilcoxon's rank-sum statistic adds up the ranks of one group. "
            "The distress flights' ranks sum to fifty-two and a half, low, because they sit at the cold end. "
            "<bookmark mark='c'/> Henry Mann and Donald Whitney, at Ohio State in 1947, subtracted the smallest possible value, "
            "seven times eight over two, giving U equals twenty-four and a half, and worked out its distribution. It's the same "
            "test, under two names, and it's called the Wilcoxon–Mann–Whitney test to be fair to both. "
            "<bookmark mark='d'/> The ties need care: with them we recompute the exact conditional law from the pooled midranks rather than use an untied table."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_[0]) for c_ in cells], lag_ratio=0.03))
            self.play(LaggedStart(*[FadeIn(c_[1]) for c_ in cells], lag_ratio=0.03))
            step = ladder(self, rows, whys, keep=3, top=0.2, x=-1.6, buff=0.6, edge=6.9)
            vo.wait_until("b")
            self.play(*[Indicate(c_, color=RES) for j, c_ in enumerate(cells) if order[j] >= 16])
            step(0, transform=False)
            vo.wait_until("c")
            step(1, transform=False)
            vo.wait_until("d")
            step(2, transform=False)
        self.clear_scene()

    def pairs(self):
        d = load("mw")
        w, c = np.sort(np.asarray(d["warm"])), np.sort(np.asarray(d["cold"]))
        cell = 0.36
        grid = VGroup()
        for i, a in enumerate(w):
            for j, b in enumerate(c):
                col = S.CTRL if a > b else (GREY_B if a == b else RES)
                op = 0.9 if a != b else 0.6
                grid.add(Square(cell, stroke_width=1, stroke_color="#101418", fill_color=col, fill_opacity=op)
                         .move_to([(i - 7.5) * cell, (j - 3) * cell, 0]))
        grid.move_to([-2.0, 0.4, 0])
        xl = label(r"16 undistressed flights, \ coldest to warmest", font_size=20, color=S.CTRL).next_to(grid, DOWN, buff=0.2)
        yl = label(r"7 distress flights", font_size=20, color=RES).rotate(PI / 2).next_to(grid, LEFT, buff=0.2)
        rows = fit_rows(VGroup(
            label(r"$16 \times 7 = 112$ pairs", font_size=24),
            label(r"blue: \ the undistressed flight was warmer", font_size=22, color=S.CTRL),
            label(r"grey: \ a tie, \ counts one half", font_size=22, color=GREY_B),
            MathTex(rf"U_{{\text{{no distress}}}} = {d['U']:g}", font_size=32, color=OBS),
            MathTex(r"= 112 - 24.5", font_size=28),
        ), 4.2, 0.34, [4.6, 0.4, 0])
        intro = label('Count all pairs, giving half credit to ties', font_size=36)
        with self.voiceover(
            "Mann and Whitney's form has a direct meaning. <bookmark mark='a'/> Pair every undistressed flight with every distress "
            "flight: sixteen times seven, a hundred and twelve pairs. <bookmark mark='b'/> Colour a pair blue when the "
            "undistressed flight was the warmer, <bookmark mark='c'/> grey for a tie, counted as a half. <bookmark mark='d'/> "
            "The number of blue cells, plus half the grey, is the U statistic for the undistressed group: eighty-seven and a "
            "half. <bookmark mark='e'/> It's a hundred and twelve minus the twenty-four and a half we found from the ranks. "
            "Counting pairs and summing ranks are the same calculation."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(FadeIn(xl), FadeIn(yl), FadeIn(rows[0]), LaggedStart(*[FadeIn(g_) for g_ in grid], lag_ratio=0.005), run_time=1.6)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def null(self):
        d = load("mw")
        pmf = np.asarray(d["pmf"])
        u = np.asarray(d["u_grid"])
        A = axes([-2, 114], [0, 0.03], x_length=8.2, y_length=3.8, xlabel=r"$U$", ylabel=r"conditional probability under $H_0$",
                 xticks=[0, 24.5, 56, 87.5, 112], yticks=[0, 0.01, 0.02, 0.03], center=[-1.4, 0.3, 0])
        ax = A.ax
        hi = np.flatnonzero(np.abs(u - 56) >= abs(d["U"] - 56) - 1e-12).tolist()
        bars = bars_at(ax, u, pmf, 0.42, NULLC, highlight=hi, hcolor=OBS)
        tie_p = d["asymptotic_p"]
        rows = [
            cmath(r"H_0", r":", r"\text{the 23 temperatures exchangeable}", font_size=28),
            cmath(r"P(U = u)", r"=", r"\frac{\#\{\text{rankings giving } u\}}{\binom{23}{7}}", font_size=28),
            cmath(r"p", r"=", rf"{d['p']:.4f}", font_size=30),
            cmath(r"\text{normal approx.}", r":", rf"{tie_p:.3f}", font_size=28),
        ]
        rows[2][2].set_color(OBS)
        g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([4.7, 0.5, 0])
        for r_ in g:
            if r_.width > 4.0:
                r_.width = 4.0
        with self.voiceover(
            "<bookmark mark='a'/> The null hypothesis is that temperature and distress are unrelated: all twenty-three "
            "temperatures exchangeable, so any seven of them were equally likely to be the distress flights. It's chapter one's "
            "permutation test, applied to ranks. <bookmark mark='b'/> With ties, the conditional null depends on these pooled midranks. A subset-sum recursion counts all 245,157 assignments: "
            "here it is, centred at fifty-six; ties need not leave the distribution symmetric. <bookmark mark='c'/> A U as far from fifty-six as eighty-seven and a half: "
            "the exact two-sided p-value, point oh three three five, includes all assignments at least this far from the null mean. <bookmark mark='d'/> The tie-corrected normal approximation is about point oh three eight. Both give evidence of association in these flights under the exchangeability null."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(g[0]))
            vo.wait_until("b")
            self.play(FadeIn(g[1]), LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(g[2]), Indicate(VGroup(*[bars[i] for i in hi]), color=OBS))
            vo.wait_until("d")
            self.play(FadeIn(g[3]))
        self.clear_scene()

    def auc(self):
        d = load("mw")
        rows = [
            cmath(r"\frac{U}{mn}", r"=", rf"\frac{{{d['U']:g}}}{{112}} = {d['auc']:.3f}", font_size=34),
            cmath(r"\ ", r"\approx", r"P(X > Y) + \tfrac12 P(X = Y)", font_size=32),
            cmath(r"\ ", r"=", r"\text{the area under the ROC curve (Part 14)}", font_size=30),
            cmath(r"H_0", r":", r"F_X=F_Y \ \Rightarrow \ \mathrm{AUC}=\tfrac12", font_size=32),
        ]
        rows[0][2].set_color(OBS)
        whys = [why(r"the share of blue cells"), why(r"$X$: \ a random undistressed flight's temperature"),
                why(r"temperature as a score for ``no distress''"), why(r"the usual exact calibration assumes equal distributions")]
        with self.voiceover(
            "<bookmark mark='a'/> Divide U by the number of pairs: point seven eight one. <bookmark mark='b'/> That estimates the "
            "probability that a random undistressed flight was warmer than a random distress flight, counting ties as half. "
            "<bookmark mark='c'/> It's also a number from Part 14: the area under the ROC curve, if temperature is used as a "
            "score to separate the two kinds of flight. The Mann–Whitney statistic and the AUC are the same thing; David Bamber "
            "pointed that out in 1975. <bookmark mark='d'/> The statistic estimates that probability with half credit for ties. The usual exact test assumes equal distributions; AUC equal to one half alone is a weaker null and needs different calibration."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def question(self):
        xs = np.linspace(-6, 6, 400)
        A = axes([-6, 6], [0, 0.85], x_length=5.6, y_length=2.6, xlabel=r"", ylabel=r"", center=[-3.4, 1.0, 0])
        B = axes([-6, 6], [0, 0.85], x_length=5.6, y_length=2.6, xlabel=r"", ylabel=r"", center=[3.4, 1.0, 0])
        a1 = density(A.ax, xs, stats.norm(0, 1).pdf(xs), S.CTRL)
        a2 = density(A.ax, xs, stats.norm(1.2, 1).pdf(xs), RES)
        b1 = density(B.ax, xs, stats.norm(0, 0.5).pdf(xs), S.CTRL)
        b2 = density(B.ax, xs, stats.norm(0, 2.0).pdf(xs), RES)
        ta = label(r"a shift: \ the test is for this", font_size=22, color=HIT).next_to(A, DOWN, buff=0.15)
        tb = label(r"same median, \ different spread", font_size=22, color=RES).next_to(B, DOWN, buff=0.15)
        rows = fit_rows(VGroup(
            label(r"under a shift model, \ the WMW test compares medians, \ and Hodges--Lehmann estimates the shift", font_size=22),
            label(r"exact calibration: \ identical distributions, \ stronger than AUC $=1/2$", font_size=22, color=OBS),
            label(r"with unequal spreads its size is off: \ the rank version of Behrens--Fisher (Part 10)", font_size=22, color=RES),
        ), 12.4, 0.3, [0, -2.2, 0])
        with self.voiceover(
            "A warning about what's tested. <bookmark mark='a'/> If the two distributions have the same shape and differ only "
            "by a shift, the test compares medians, or any other location, and the Hodges–Lehmann median of the pairwise "
            "differences estimates the shift. <bookmark mark='b'/> Without that shape assumption, U estimates the AUC, but its usual permutation calibration still assumes identical distributions. <bookmark mark='c'/> The two symmetric normal distributions pictured have the same median and AUC one half despite different spreads, yet the test, calibrated for identical "
            "distributions, rejects them seven percent of the time with twenty in each group, and with unequal group sizes it can "
            "be off in either direction: the rank version of the Behrens–Fisher problem from "
            "Part 10. Ranks free us from normality, not from thinking about what the null hypothesis says."
        ) as vo:
            self.play(FadeIn(A), FadeIn(B), FadeIn(a1), FadeIn(a2), FadeIn(b1), FadeIn(b2))
            vo.wait_until("a")
            self.play(FadeIn(ta), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(tb), FadeIn(rows[2]))
        self.clear_scene()
