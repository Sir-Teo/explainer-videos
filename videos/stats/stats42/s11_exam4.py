from __future__ import annotations

import numpy as np

from videos.stats.stats42.common import *  # noqa: F403

LTOP = 1.45


class ExamModern(ExamMixin, VoiceoverScene):
    def construct(self):
        self.card()
        self.p10()
        self.p11()
        self.p12()

    def card(self):
        card = chapter_card(10, r"Exam IV: \ discoveries, \ guarantees, \ survival", r"Problems 10--12", part=PART)
        with self.voiceover("Chapter ten. The last three problems: many tests at once, a prediction interval with a guarantee, and a survival curve."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------------------------------ Problem 10
    def p10(self):
        d = load("p_bh")
        p = np.asarray(d["p"])
        ps = ", ".join(f"{v:g}" for v in p)
        card = ExamCard(10, r"BH by hand", r"Part 33", [
            rf"Twelve hypotheses give the p-values \ {ps}.",
            r"Apply Benjamini--Hochberg at $q = 0.1$. \ How many discoveries? \ How many would Bonferroni allow?",
            r"What does BH promise, \ and what does it not?"], marks=8, color=S.PRIOR)
        self.pose_voiceover(
            "Problem ten. Twelve hypotheses give the p-values on the card, already sorted. Apply the Benjamini–Hochberg "
            "procedure at a false discovery rate of ten percent. How many discoveries are there, and how many would "
            "Bonferroni allow at the same level? And what exactly does the procedure promise? Pause and try it.", card)
        rows = [
            cmath(r"p_{(i)}", r"\le", r"\tfrac{i}{m} q = \tfrac{i}{120}: \ \text{find the largest such } i", font_size=32),
            cmath(r"i = 8", r":", rf"p_{{(8)}} = {p[7]:g} \le 8/120 = {8 / 120:.4f}; \ \ i = 9: \ {p[8]:g} > 9/120 = 0.075", font_size=30),
            cmath(r"\text{BH}", r":", rf"\text{{reject the {d['k']} smallest}}; \ \ \text{{Bonferroni}} \ (p \le 0.1/12 = 0.0083): \ {d['bonf']}", font_size=30),
            cmath(r"E\Big[\frac{V}{\max(R, 1)}\Big]", r"\le", r"q \ \ \text{(independent or PRDS p-values)}", font_size=30),
        ]
        rows[2][-1].set_color(S.PRIOR)
        whys = [why(r"the step-up rule"), why(r"the last crossing"), why(r"twice the discoveries"), why(r"a rate, \ on average")]
        with self.voiceover(
            f"<bookmark mark='a'/> Compare the i-th smallest p-value with i over twelve times point one, i over a hundred and twenty, and find the largest i where it falls below. <bookmark mark='b'/> The eighth, {say(p[7], 4)}, is below eight over a hundred and twenty, about point oh six seven; the ninth, {say(p[8], 3)}, is above its line, and so are all the rest. <bookmark mark='c'/> So BH rejects the eight smallest, here all eight are also below their own lines. In other examples the step-up rule can include earlier p-values that exceed their individual lines: the procedure steps up from the last crossing. Bonferroni's threshold, point one over twelve, allows only {d['bonf']}. <bookmark mark='d'/> The promise is about an average: over repeated use, the expected share of false discoveries among the discoveries is at most ten percent, for valid null p-values under independence or the specific PRDS positive-dependence condition. Arbitrary positive correlations are not enough. It says nothing about which of the eight are false, and nothing about this particular list."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        A = axes([0, 13], [0, 1.0], x_length=5.0, y_length=3.0, xlabel=r"rank $i$", ylabel=r"$p_{(i)}$", xticks=[1, 4, 8, 12],
                 yticks=[0, 0.1, 0.5, 1.0], center=[-4.0, -1.1, 0])
        ax = A.ax
        line = Line(ax.c2p(0, 0), ax.c2p(13, 13 * 0.1 / 12), color=S.PRIOR, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(i + 1, v), radius=0.07, color=S.PRIOR if i < d["k"] else GREY_B) for i, v in enumerate(p)])
        gs = np.asarray(d["genes_sorted"])
        m = d["genes"]
        B = axes([0, 400], [0, max(.008, float(np.ceil(gs.max()*1000)/1000))], x_length=4.6, y_length=3.0, xlabel=r"rank, \ 6,033 genes", xticks=[0, 200, 400],
                 yticks=[0, 0.004, 0.008], center=[1.6, -1.1, 0])
        bx = B.ax
        gl = Line(bx.c2p(0, 0), bx.c2p(400, 400 * 0.1 / m), color=S.PRIOR, stroke_width=3)
        gd = VGroup(*[Dot(bx.c2p(i + 1, v), radius=0.025, color=S.PRIOR if i < d["genes_k"] else GREY_C) for i, v in enumerate(gs)])
        side = fit_rows(VGroup(
            label(rf"genes: \ BH finds {d['genes_k']}", font_size=22, color=S.PRIOR),
            label(rf"Bonferroni: \ {d['genes_bonf']}", font_size=22, color=GREY_A),
            label(r"the line's slope: \ $q/m$", font_size=22, color=GREY_A),
        ), 2.4, 0.36, [5.6, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The picture is a sorted list of p-values against a line of slope q over m: everything up "
            f"to the last point under the line is a discovery. <bookmark mark='b'/> The same rule on the prostate "
            f"microarray of Part thirty-three, with {m:,} genes: <bookmark mark='c'/> BH at ten percent finds "
            f"{d['genes_k']} genes, Bonferroni only {d['genes_bonf']}. With thousands of tests, the difference between "
            f"controlling the chance of any error and the rate of errors is the difference between a list worth following "
            f"up and almost nothing."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(museum_tag(r"Singh et al. (2002): \ prostate microarray")))
            vo.wait_until("c")
            self.play(Create(gl), FadeIn(gd), FadeIn(side))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------------------------------ Problem 11
    def p11(self):
        d = load("p_conf")
        toy = np.asarray(d["toy"])
        ts = ", ".join(f"{v:g}" for v in toy)
        card = ExamCard(11, r"a conformal interval", r"Part 34", [
            rf"A model fitted on one half of the data leaves nine calibration residuals $|y_i - \hat y_i|$: \ {ts}.",
            r"Give the split-conformal 80\% interval for a new point predicted at $\hat y = 10$, \ and prove its coverage.",
            r"What does the guarantee assume, \ and what does it not give?"], marks=10, color=S.KEPT)
        self.pose_voiceover(
            "Problem eleven. A model fitted on one part of the data leaves nine absolute residuals on a separate calibration "
            "set: the numbers on the card. Give the split-conformal eighty percent prediction interval for a new point whose "
            "prediction is ten, and prove that it covers at least eighty percent of the time. What does the guarantee "
            "assume, and what does it not give? Pause and try it.", card)
        srt = np.sort(toy)
        rows = [
            cmath(r"k", r"=", rf"\lceil (n + 1)(1 - \alpha) \rceil = \lceil 10 \times 0.8 \rceil = {d['kt']}", font_size=32),
            cmath(r"R_{(k)}", r"=", rf"\text{{the {d['kt']}th of }} {', '.join(f'{v:g}' for v in srt)} = {d['qt']:g}", font_size=28),
            cmath(r"\text{interval}", r"=", rf"10 \pm {d['qt']:g} = [{10 - d['qt']:g}, \ {10 + d['qt']:g}]", font_size=32),
            cmath(r"P(R_{n+1} \le R_{(k)})", r"\ge", r"\tfrac{k}{n+1} = 0.8: \ \text{the new rank is uniform on } 1, \dots, n + 1", font_size=28),
        ]
        rows[2][-1].set_color(S.KEPT)
        whys = [why(r"the quantile lemma"), why(r"sort, \ count"), why(r"symmetric"), why(r"exchangeability")]
        with self.voiceover(
            f"<bookmark mark='a'/> With n equal to nine and alpha point two, take k as the ceiling of ten times point eight: {d['kt']}. <bookmark mark='b'/> Sort the residuals; the {d['kt']}th smallest is {say(d['qt'], 1)}. <bookmark mark='c'/> The interval is ten plus or minus {say(d['qt'], 1)}: from {say(10 - d['qt'], 1)} to {say(10 + d['qt'], 1)}. <bookmark mark='d'/> The proof: if the new point and the calibration points are exchangeable, conditional on the separate training sample, its rank is uniform when scores are distinct or ties are randomly broken; ties only make the usual nonrandomized bound conservative, so it is at or below the {d['kt']}th with probability at least {d['kt']} over ten. The guarantee assumes only exchangeability, not a correct model; but it is marginal, an average over new points, not a promise for each kind of point."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=LTOP, x=-0.9, buff=0.8, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        x, y = np.asarray(d["x"]), np.asarray(d["y"])
        b, q = d["b"], d["q"]
        A = axes([55, 100], [-60, 180], x_length=6.6, y_length=3.4, xlabel=r"maximum temperature, \ $^\circ$F", ylabel=r"ozone, \ ppb",
                 xticks=[60, 70, 80, 90, 100], yticks=[0, 60, 120, 180], center=[-2.6, -1.0, 0])
        ax = A.ax
        te = np.asarray(d["te"], int)
        dots = VGroup(*[Dot(ax.c2p(a, c), radius=0.05, color=GREY_B) for a, c in zip(x, y)])
        tdots = VGroup(*[Dot(ax.c2p(x[i], y[i]), radius=0.07, color=S.KEPT) for i in te])
        xs = np.array([56, 99])
        fit = Line(ax.c2p(56, b[0] + b[1] * 56), ax.c2p(99, b[0] + b[1] * 99), color=WHITE, stroke_width=3)
        bnd = band(ax, xs, b[0] + b[1] * xs - q, b[0] + b[1] * xs + q, S.KEPT, 0.2)
        side = fit_rows(VGroup(
            label(rf"New York's ozone: \ 37 fit, \ {d['n_cal']} calibrate, \ 37 test", font_size=22, color=GREY_A),
            label(rf"$k = \lceil 38 \times 0.9 \rceil = {d['k']}$: \ $q = {q:.1f}$ ppb", font_size=22, color=S.KEPT),
            label(rf"at 85$^\circ$F: \ {d['pred0']:.0f} $\pm$ {q:.0f}", font_size=22, color=S.KEPT),
            label(rf"test coverage: \ {100 * d['cover']:.0f}\% of 37", font_size=22, color=S.KEPT),
            label(r"constant width; CQR adapts; day exchangeability is unverified", font_size=20, color=GREY_A),
        ), 4.6, 0.36, [4.45, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The same recipe on New York's ozone: a line in temperature fitted to thirty-seven days, residuals on {d['n_cal']} others, and k equal to the ceiling of thirty-eight times point nine, {d['k']}. <bookmark mark='b'/> The band is the line plus or minus {say(q, 1)} parts per billion; at eighty-five degrees, about {d['pred0']:.0f} plus or minus {q:.0f}. <bookmark mark='c'/> On the thirty-seven held-out days it covered every one. <bookmark mark='d'/> But a constant width is a poor fit to ozone, whose spread grows with temperature: too wide on cool days and close to failing on hot ones, so its coverage is far from even across temperatures. Conformalized quantile regression lets width follow the spread. Both rank guarantees still require exchangeable calibration and future scores conditional on separate training. Seasonal and serial dependence in these air-quality days makes this an illustration, not a verified time-series guarantee."
        ) as vo:
            self.play(FadeIn(A), FadeIn(dots), FadeIn(museum_tag(r"New York air quality, \ 1973")))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(bnd), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(tdots), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
        show_board(self, board_rows("conformal"),
                   "<bookmark mark='a'/> And the Board, over four thousand draws from the World: a split-conformal interval "
            "with ninety-nine calibration points, for a new adult's pressure from age and BMI, covers ninety percent,"
            " within simulation error of the marginal lower bound. The lemma does not require every finite simulation"
            " to produce exactly ninety percent.",
                   [("a", [0])])

    # ------------------------------------------------------------------------------------------ Problem 12
    def p12(self):
        d = load("p_km")
        card = ExamCard(12, r"Kaplan--Meier with Greenwood's variance", r"Part 40", [
            r"Freireich's 6-MP arm, \ 21 patients, \ weeks in remission \ ($+$ censored): \ 6, 6, 6, 6+, 7, 9+, 10, 10+, 11+, 13,",
            r"16, 17+, 19+, 20+, 22, 23, 25+, 32+, 32+, 34+, 35+. \ \ Compute $\hat S(t)$ to week 13,",
            r"its Greenwood standard error at week 13, \ and a log-log 95\% interval."], marks=12, color=S.EST)
        self.pose_voiceover(
            "Problem twelve. The six-MP arm of Freireich's 1963 leukaemia trial: twenty-one patients, with their "
            "weeks in remission, a plus marking those still in remission when last seen. Compute the Kaplan–Meier "
            "estimate up to week thirteen, its Greenwood standard error at week thirteen, and a log-log ninety-five "
            "percent interval. Pause and try it.", card)
        r = d["rows"][:4]
        tab = table_rows([[r"$t$", r"$n_t$", r"$d_t$", r"$1 - d_t/n_t$", r"$\hat S(t)$", r"$\frac{d_t}{n_t(n_t - d_t)}$"]] +
                         [[f"{x['t']:.0f}", f"{x['n']:.0f}", f"{x['d']:.0f}", rf"{x['n'] - x['d']:.0f}/{x['n']:.0f}", f"{x['s']:.3f}",
                           f"{x['d'] / (x['n'] * (x['n'] - x['d'])):.5f}"] for x in r],
                         font_size=26, col_buff=0.6, row_buff=0.18).move_to([0, 0.3, 0])
        gw = r[3]["gw"]
        rows = fit_rows(VGroup(
            label(rf"Greenwood: \ $\widehat{{\text{{Var}}}}\,\hat S(13) = \hat S^2 \sum \frac{{d}}{{n(n - d)}} = {r[3]['s']:.3f}^2 \times {gw:.5f}$, \ \ SE $= {r[3]['se']:.4f}$", font_size=26, color=S.EST),
            label(rf"log-log: \ $\hat S^{{\exp(\pm 1.96\, s)}}$, \ $s = \sqrt{{\sum}} / |\log \hat S| = {np.sqrt(gw) / abs(np.log(r[3]['s'])):.3f}$: \ \ [{r[3]['lo']:.3f}, \ {r[3]['hi']:.3f}]", font_size=26, color=S.EST),
        ), 12.4, 0.35, [0, -2.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Only the times with a relapse change the curve. At week six, twenty-one are at risk and three relapse: the curve falls to eighteen over twenty-one, {say(r[0]['s'], 3)}. <bookmark mark='b'/> The patient censored at six leaves the risk set without a step, so at week seven seventeen are at risk, and one relapses. <bookmark mark='c'/> At ten, fifteen at risk; at thirteen, twelve, after the censorings at nine, ten and eleven. The estimate at thirteen is {say(r[3]['s'], 3)}. <bookmark mark='d'/> Greenwood's formula: the square of the estimate times the sum of d over n times n minus d, which gives a standard error of {say(r[3]['se'], 3)}. <bookmark mark='e'/> The log-log interval transforms, builds a symmetric interval, and transforms back, so it stays inside zero and one: from {say(r[3]['lo'], 2)} to {say(r[3]['hi'], 2)}."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.play(*[FadeOut(m) for m in self.mobjects if m is not card])
        A = axes([0, 36], [0, 1], x_length=6.6, y_length=3.4, xlabel=r"weeks", ylabel=r"still in remission", xticks=[0, 10, 20, 30],
                 yticks=[0, 0.5, 1], center=[-2.6, -1.0, 0])
        ax = A.ax
        k1 = KMStaircase(ax, d["time"], d["event"], color=S.EST)
        k0 = KMStaircase(ax, d["time0"], d["event0"], color=GREY_B)
        km = k1.km
        bd = k1.band(km["loglog"][0], km["loglog"][1], color=S.EST, opacity=0.22)
        side = fit_rows(VGroup(
            label(r"6-MP, \ with its log-log band", font_size=22, color=S.EST),
            label(r"placebo: \ 21 patients, \ none censored", font_size=22, color=GREY_A),
            label(rf"medians: \ {d['median1']:.0f} weeks vs {d['median0']:.0f}", font_size=22),
            label(rf"unstratified log-rank $\chi^2_1 = {d['logrank']['chi2']:.1f}$, \ $p < 0.0001$", font_size=22, color=S.EST),
        ), 4.6, 0.36, [4.45, -1.0, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the whole curve, with its pointwise band, and censored patients marked by ticks. Independent censoring is required; these are pointwise approximate intervals. <bookmark mark='b'/> Beside it, the placebo arm, in which every patient had an observed relapse, most within a few weeks. <bookmark mark='c'/> The median remission is {d['median1']:.0f} weeks on six-MP against {d['median0']:.0f} on placebo, <bookmark mark='d'/> and the ordinary unstratified log-rank statistic of Part forty is {say(d['logrank']['chi2'], 1)} on one degree of freedom. This was an early randomized matched-pair leukaemia trial, and its curves are still the textbook example: the reason survival analysis needed Kaplan, Meier and Greenwood."
        ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Freireich et al. (1963), \ via Gehan (1965)")))
            vo.wait_until("a")
            self.play(FadeIn(bd), Create(k1.curve()), FadeIn(k1.ticks()), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(k0.curve()), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.solved(card)
        self.wait(0.5)
        self.clear_scene()
