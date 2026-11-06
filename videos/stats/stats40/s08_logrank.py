from __future__ import annotations

import numpy as np

from videos.stats.stats40.common import *  # noqa: F403


class LogRank(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.table()
        self.result()
        self.weights()
        self.limits()

    def card(self):
        card = chapter_card(7, r"The log-rank test", r"Observed minus expected, \ at every event", lit=(1965, 1966), part=PART)
        with self.voiceover("Chapter seven. The log-rank test."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def derive(self):
        rows = [
            cmath(r"\text{at } t_k", r":", r"n_k \text{ at risk}, \ n_{1k} \text{ in group 1}, \ d_k \text{ events}", font_size=30),
            cmath(r"H_0", r":", r"d_{1k} \sim \text{Hypergeometric}: \ E_{1k} = d_k\, n_{1k}/n_k", font_size=30),
            cmath(r"V_k", r"=", r"d_k \tfrac{n_{1k}}{n_k}\big(1 - \tfrac{n_{1k}}{n_k}\big)\tfrac{n_k - d_k}{n_k - 1}", font_size=30),
            cmath(r"\chi^2", r"=", r"\big(\textstyle\sum_k (d_{1k} - E_{1k})\big)^2 / \textstyle\sum_k V_k", font_size=32),
        ]
        rows[3][-1].set_color(TAUC)
        whys = [why(r"a 2 $\times$ 2 table at each event time"), why(r"Part 14's Fisher table"), why(r"its variance"),
                why(r"Mantel (1966): \ Cochran--Mantel--Haenszel")]
        with self.voiceover(
            "<bookmark mark='a'/> At each event time, form a two by two table: group by event, among those at risk. "
            "<bookmark mark='b'/> If the groups have the same hazard, the events among the at-risk are shared out at "
            "random, so group one's count is hypergeometric, as in Part fourteen's Fisher test, with expectation d k times "
            "group one's share of the risk set. <bookmark mark='c'/> Its variance is the hypergeometric one. <bookmark "
            "mark='d'/> Sum observed minus expected over all event times, square, and divide by the summed variance: Nathan "
            "Mantel's log-rank statistic of 1966, the Cochran-Mantel-Haenszel test with time as the strata. Under the null "
            "it is chi-squared on one degree of freedom."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("gehan")
        R = np.asarray(d["logrank"]["rows"], float)  # t, n, n1, d, d1, e1, v  (group 1 = 6-MP)
        rows = [[r"week", r"at risk", r"6-MP at risk", r"relapses", r"6-MP relapses", r"expected", r"O $-$ E"]]
        for r in R[:6]:
            rows.append([f"{r[0]:.0f}", f"{r[1]:.0f}", f"{r[2]:.0f}", f"{r[3]:.0f}", f"{r[4]:.0f}", f"{r[5]:.2f}", f"{r[4] - r[5]:+.2f}"])
        rows.append([r"\ldots"] * 7)
        rows.append([r"total", "", "", f"{R[:, 3].sum():.0f}", f"{R[:, 4].sum():.0f}", f"{R[:, 5].sum():.2f}", f"{R[:, 4].sum() - R[:, 5].sum():+.2f}"])
        tab = table_rows(rows, font_size=24, col_buff=0.55, row_buff=0.25, colors=[GREY_A] + [None] * 7 + [TAUC]).move_to([0, 0.3, 0])
        if tab.width > 12.6:
            tab.width = 12.6
        with self.voiceover(
            "<bookmark mark='a'/> The first rows for Gehan's data, counting 6-MP as group one. At week one, forty-two at "
            "risk, half on the drug, two relapses, both on placebo: the drug arm expected one and had none. <bookmark "
            "mark='b'/> Week after week the drug arm has fewer relapses than its share of the risk set predicts. "
            "<bookmark mark='c'/> In total the 6-MP group had " + str(round(R[:, 4].sum())) + " relapses where "
            + say(R[:, 5].sum(), 1) + " were expected."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(*[FadeIn(r) for r in tab[2:8]])
            vo.wait_until("c")
            self.play(FadeIn(tab[8]))
        self.clear_scene()

    def result(self):
        d = load("gehan")
        lr = d["logrank"]
        A = axes([0, 20], [0, 0.5], x_length=7.4, y_length=4.0, xlabel=r"$\chi^2_1$", ylabel=r"density",
                 xticks=[0, 5, 10, 15, 20], yticks=[0, 0.25, 0.5], xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", center=[-2.5, 0.2, 0])
        ax = A.ax
        xs = np.linspace(0.15, 20, 300)
        from scipy import stats as st
        nd = density(ax, xs, st.chi2.pdf(xs, 1), NULLC)
        ob = DashedLine(ax.c2p(lr["chi2"], 0), ax.c2p(lr["chi2"], 0.45), color=OBS, stroke_width=3)
        side = fit_rows(VGroup(
            label(r"grey: \ $\chi^2_1$, \ the null distribution", font_size=22, color=NULLC),
            label(rf"observed: \ $\chi^2 = {lr['chi2']:.1f}$", font_size=22, color=OBS),
            label(rf"$p = {float(f"{lr['p']:.1e}".split("e")[0]):.1f} \times 10^{{{int(f"{lr['p']:.1e}".split("e")[1])}}}$", font_size=22, color=OBS),
            label(rf"Gehan's weighted version: \ $\chi^2 = {lr['gehan_chi2']:.1f}$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Against the chi-squared distribution on one degree of freedom, <bookmark mark='b'/> the "
            "observed statistic is " + say(lr["chi2"], 1) + ", <bookmark mark='c'/> a p-value of about four in a hundred "
            "thousand. <bookmark mark='d'/> Edmund Gehan's 1965 test, which weights each table by the number at risk, gives "
            + say(lr["gehan_chi2"], 1) + ": a little less, because it emphasizes the early weeks, when both arms still had "
            "most patients."
        ) as vo:
            self.add(gehan_tag())
            vo.wait_until("a")
            self.play(FadeIn(A), FadeIn(nd), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ob), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def weights(self):
        rows = [
            cmath(r"Z_w", r"=", r"\textstyle\sum_k w_k (d_{1k} - E_{1k}) \big/ \sqrt{\textstyle\sum_k w_k^2 V_k}", font_size=32),
            cmath(r"w_k = 1", r":", r"\text{log-rank: \ optimal for proportional hazards}", font_size=30),
            cmath(r"w_k = n_k", r":", r"\text{Gehan--Breslow: \ early differences}", font_size=30),
            cmath(r"w_k = \hat S(t_k-)^\rho (1 - \hat S(t_k-))^\gamma", r":", r"\text{Fleming--Harrington: \ choose where to look}", font_size=28),
        ]
        rows[1][-1].set_color(TAUC)
        whys = [why(r"a weighted family"), why(r"Peto \& Peto (1972)"), why(r"Gehan (1965)"), why(r"choose before seeing the data")]
        with self.voiceover(
            "<bookmark mark='a'/> The log-rank test is one member of a family that weights the tables. <bookmark mark='b'/> "
            "Equal weights are optimal when the hazards are proportional. <bookmark mark='c'/> Weighting by the number at "
            "risk stresses early differences. <bookmark mark='d'/> Thomas Fleming and David Harrington's weights can "
            "stress early, late or middle times. The weights must be chosen before looking, or the test is Part "
            "thirty-three's garden of forking paths."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.6, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def limits(self):
        rows = fit_rows(VGroup(
            label(r"a test, \ not an estimate: \ how big is the difference?", font_size=26, color=TAUC),
            label(r"crossing curves: \ early harm and late benefit can cancel to $\chi^2 \approx 0$", font_size=26, color=MISSC),
            label(r"stratified log-rank: \ sum O $-$ E within strata \ (centre, \ stage)", font_size=26, color=GREY_A),
            label(r"the estimate behind it: \ Cox's hazard ratio, \ next", font_size=26, color=SURVC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The log-rank test answers only whether the curves differ, not by how much. <bookmark "
            "mark='b'/> It can miss a real difference when the curves cross, because early harm and late benefit cancel "
            "in the sum. <bookmark mark='c'/> A stratified version sums observed minus expected within strata, such as "
            "hospitals or disease stages. <bookmark mark='d'/> And the estimate behind it, the quantity whose score test it "
            "is, is Cox's hazard ratio, which comes next."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
