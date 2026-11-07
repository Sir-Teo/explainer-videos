from __future__ import annotations

import numpy as np

from videos.stats.stats10.common import *  # noqa: F403


class ChiSq(VoiceoverScene):
    def construct(self):
        self.card()
        self.pearson()
        self.statistic()
        self.mendel()
        self.null_check()
        self.too_good()
        self.independence()
        self.confounded()

    def card(self):
        card = chapter_card(8, r"Pearson's $\chi^2$", r"Do the counts fit the model?", lit=(1900,), part=PART)
        with self.voiceover("Chapter eight. Pearson's chi-squared."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pearson(self):
        hc = history_card(1900, r"Karl Pearson, \ \emph{Philosophical Magazine}", r"``On the criterion that a given system of deviations "
                          r"from the probable \dots\ can be reasonably supposed to have arisen from random sampling'': \ the first "
                          r"general test of fit", color=DATA, width=9.2, font_size=24).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"his example: \ Weldon's 26,306 throws of twelve dice; \ earlier (1894), \ Monte Carlo's roulette", font_size=24, color=GREY_A),
            label(r"the degrees of freedom were corrected by Fisher (1922, 1924) when parameters are estimated", font_size=24,
                  color=GREY_A),
        ), 12.6, 0.3, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1900 Karl Pearson published the first general test of whether data fit a model: a "
            "criterion for deciding whether a set of deviations from what was expected could reasonably have arisen by "
            "chance. <bookmark mark='b'/> His example was Raphael Weldon's twenty-six thousand throws of twelve dice; "
            "a few years earlier he had argued, in the same spirit, that the roulette wheels of Monte Carlo were not "
            "random. <bookmark mark='c'/> Pearson got one thing wrong, the degrees of freedom when parameters have to be "
            "estimated from the data, and the young Fisher corrected him, a correction Pearson resisted bitterly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def statistic(self):
        rows = [
            cmath(r"X^2", r"=", r"\sum_{j=1}^{k} \frac{(O_j - E_j)^2}{E_j}", font_size=36),
            cmath(r"X^2", r"\to", r"\chi^2_{k - 1}", r"\quad\text{under } H_0", font_size=36),
            cmath(r"X^2", r"\to", r"\chi^2_{k - 1 - m}", r"\quad m \text{ regular parameters fitted by grouped MLE}", font_size=34),
        ]
        rows[0][2].set_color(OBS)
        whys = [why(r"observed against expected counts, \ each scaled by its own variance"),
                why(r"$k$ counts, \ one constraint (they add to $n$): \ Part 8's Cochran"),
                why(r"Fisher's correction; \ $X^2$ is the score test of the multinomial")]
        with self.voiceover(
            "<bookmark mark='a'/> Pearson's statistic compares each observed count with the count the model expects, "
            "squares the difference, and scales it by the expected count, which is roughly the count's variance. "
            "<bookmark mark='b'/> For independent multinomial trials with fixed categories and expected counts growing, the sum is approximately chi-squared with k minus one degrees "
            "of freedom: k counts, less one because they must add up to the total. <bookmark mark='c'/> And one more "
            "degree is lost per identifiable regular parameter fitted efficiently to the grouped counts, Fisher's correction. Arbitrary estimates or parameters fitted before binning need not yield this reference law. In the language of chapter "
            "six, Pearson's statistic is exactly the score test for a multinomial."
        ) as vo:
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-1.0, buff=0.9, edge=6.9)
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def mendel(self):
        d = load("mendel")
        obs = np.asarray(museum.MENDEL_DIHYBRID)
        exp = np.asarray(d["di"]["expected"])
        names = [r"round yellow", r"round green", r"wrinkled yellow", r"wrinkled green"]
        A = axes([-0.5, 3.5], [0, 340], x_length=6.0, y_length=3.8, ylabel=r"plants", yticks=[0, 100, 200, 300], center=[-3.0, -0.3, 0])
        ax = A.ax
        bo = bars_at(ax, np.arange(4) - 0.18, obs, 0.34, DATA)
        be = bars_at(ax, np.arange(4) + 0.18, exp, 0.34, NULLC, opacity=0.5)
        nl = VGroup(*[label(t, font_size=18, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.2) for i, t in enumerate(names)])
        leg = legend([(DATA, r"observed"), (NULLC, r"expected, \ 9{:}3{:}3{:}1")], font_size=22).next_to(A, UP, buff=0.1).align_to(A, RIGHT)
        rows = fit_rows(VGroup(
            label(r"Mendel (1866): \ seed shape, \ 3{:}1", font_size=24, color=GREY_A),
            MathTex(rf"5474 : 1850 \quad X^2 = {d['shape']['chi2']:.3f},\ \ p = {d['shape']['p']:.2f}", font_size=28),
            label(r"two characters at once, \ 9{:}3{:}3{:}1", font_size=24, color=GREY_A),
            MathTex(r"315 : 108 : 101 : 32", font_size=28),
            MathTex(rf"X^2 = {d['di']['chi2']:.2f}\ \text{{on 3 df}},\ \ p = {d['di']['p']:.2f}", font_size=30, color=OBS),
            label(r"a superb fit", font_size=24, color=GREY_A),
        ), 5.2, 0.3, [3.9, -0.2, 0])
        src = historical_tag(r"Mendel (1866)", corner=DR)
        with self.voiceover(
            "The most famous counts in biology. <bookmark mark='a'/> Gregor Mendel's peas, in 1866. Crossing plants and "
            "then crossing their offspring, his theory predicted round and wrinkled seeds in the ratio three to one. He "
            "counted five thousand four hundred and seventy-four round and one thousand eight hundred and fifty wrinkled. "
            "Pearson's statistic is point two six, and the p-value point six one: no evidence against three to one. "
            "<bookmark mark='b'/> Following two characters at once, shape and colour, the theory predicts nine to three "
            "to three to one. He counted three hundred and fifteen, a hundred and eight, a hundred and one, and "
            "thirty-two. <bookmark mark='c'/> The statistic is point four seven on three degrees of freedom, a p-value "
            "of point nine three. The observed bars sit almost exactly on the expected ones."
        ) as vo:
            self.play(FadeIn(A), FadeIn(nl), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[:2]))
            vo.wait_until("b")
            self.play(FadeIn(bo, lag_ratio=0.2), FadeIn(be, lag_ratio=0.2), FadeIn(rows[2:4]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4:]))
        self.clear_scene()

    def null_check(self):
        d = load("mendel")
        ed, xs = np.asarray(d["edges"]), np.asarray(d["xs"])
        A = axes([0, 14], [0, 0.26], x_length=7.4, y_length=4.2, xlabel=r"$X^2$ \ for 556 plants, \ if 9{:}3{:}3{:}1 is true",
                 xticks=[0.47, 4, 7.81, 12], yticks=[0, 0.1, 0.2], center=[-2.0, -0.3, 0])
        ax = A.ax
        bars = hist_bars(ax, ed, np.asarray(d["hist"]), color=SIM, opacity=0.6)
        cv = curve(ax, xs, np.asarray(d["chi2_3"]), OBS, 3)
        obs = DashedLine(ax.c2p(d["di"]["chi2"], 0), ax.c2p(d["di"]["chi2"], 0.26), color=DATA, stroke_width=2.5)
        cut = DashedLine(ax.c2p(7.81, 0), ax.c2p(7.81, 0.26), color=REJ, stroke_width=2)
        rows = fit_rows(VGroup(
            label(r"100,000 simulated harvests: \ the $\chi^2_3$ curve fits", font_size=24),
            MathTex(rf"P(X^2 > 7.81) = {d['sim_size']:.4f}", font_size=28, color=REJ),
            MathTex(rf"P(X^2 \le 0.47) = {d['sim_below']:.3f}", font_size=28, color=DATA),
            label(r"Mendel's fit beats 93\% of harvests", font_size=24, color=GREY_A),
            label(r"in which his theory is exactly true", font_size=24, color=GREY_A),
        ), 5.0, 0.34, [4.4, -0.2, 0])
        tag = simulated_tag(r"simulated: \ multinomial harvests", corner=UR)
        with self.voiceover(
            "Is the chi-squared approximation good here? <bookmark mark='a'/> Simulate a hundred thousand harvests of "
            "five hundred and fifty-six plants in which the theory is exactly true, and compute Pearson's statistic for "
            "each. The chi-squared curve with three degrees of freedom fits the histogram, <bookmark mark='b'/> and "
            "rejecting beyond seven point eight one happens four point nine nine percent of the time. "
            "<bookmark mark='c'/> Now look at Mendel's value, point four seven, at the far left. Only seven percent of "
            "harvests where the theory is perfectly true fit as well as his did. That's not suspicious by itself. But "
            "Fisher looked at the left tail across all of Mendel's experiments."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.02), Create(cv), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(obs), FadeIn(rows[2:]))
        self.clear_scene()

    def too_good(self):
        hc = history_card(1936, r"R. A. Fisher, \ \emph{Annals of Science} 1", r"``Has Mendel's work been rediscovered?'': \ pooled over "
                          r"the experiments, \ the counts agree with the ratios so closely that a fit this good would arise by chance "
                          r"less than once in ten thousand", color=DATA, width=9.4, font_size=24).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"a test in the \emph{lower} tail: \ data too close to the theory", font_size=26, color=OBS),
            label(r"Fisher suspected an assistant who knew what Mendel expected; \ the debate continues \ (Franklin et al., 2008)",
                  font_size=24, color=GREY_A),
            label(r"the same check catches fabricated data today", font_size=24, color=GREY_A),
        ), 12.6, 0.3, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 1936 Fisher reanalysed all of Mendel's published experiments, and pooled the "
            "chi-squared statistics. The agreement with Mendel's ratios was so close that a fit at least that good would "
            "occur by chance less than once in ten thousand repetitions. <bookmark mark='b'/> This was a significance "
            "test in the other tail: the data were too good to be true. <bookmark mark='c'/> Fisher, who admired "
            "Mendel, suggested an assistant who knew what was expected may have shaded the counts. Historians and "
            "statisticians are still arguing about it. <bookmark mark='d'/> The idea, though, is now a standard forensic "
            "tool: real data are noisy, and data with too little noise deserve a second look."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def independence(self):
        d = load("clinic")
        t, e = d["table"], np.asarray(d["expected"])
        grid = VGroup()
        labs_r = [r"treated", r"untreated"]
        labs_c = [r"recovered", r"not"]
        for i in range(2):
            for j in range(2):
                box = Rectangle(width=2.2, height=1.1, stroke_color=GREY_B, stroke_width=2).move_to([-4.0 + 2.2 * j, 1.0 - 1.1 * i, 0])
                grid.add(VGroup(box, MathTex(str(t[i][j]), font_size=36).move_to(box.get_center() + UP * 0.15),
                                MathTex(rf"({e[i, j]:.1f})", font_size=22, color=NULLC).move_to(box.get_center() + DOWN * 0.3)))
        rl = VGroup(*[label(s_, font_size=22, color=GREY_A).next_to(grid[2 * i], LEFT, buff=0.2) for i, s_ in enumerate(labs_r)])
        cl = VGroup(*[label(s_, font_size=22, color=GREY_A).next_to(grid[j], UP, buff=0.15) for j, s_ in enumerate(labs_c)])
        r1, r2 = t[0][0] / sum(t[0]), t[1][0] / sum(t[1])
        rows = fit_rows(VGroup(
            label(r"200 of the World's clinic patients", font_size=24, color=GREY_A),
            MathTex(rf"\text{{recovered: treated }} {100 * r1:.0f}\%,\ \ \text{{untreated }} {100 * r2:.0f}\%", font_size=28),
            MathTex(r"E_{ij} = \frac{(\text{row total})(\text{column total})}{n}", font_size=28),
            MathTex(rf"X^2 = {d['chi2']:.2f}\ \text{{on 1 df}},\ \ p = {d['p']:.4f}", font_size=30, color=OBS),
            MathTex(rf"\text{{Fisher's exact: }} p = {d['fisher_p']:.4f}", font_size=28),
            label(r"strong evidence that treatment and recovery are associated", font_size=24, color=OBS),
        ), 6.0, 0.3, [3.4, -0.2, 0])
        tag = simulated_tag(r"the World: \ the clinic", corner=DR)
        with self.voiceover(
            "Pearson's statistic also tests independence in a table. <bookmark mark='a'/> Two hundred patients from "
            "the World's clinic, classified by whether they were treated and whether they recovered. "
            "<bookmark mark='b'/> Fifty-seven percent of the treated recovered, against seventy-seven percent of the "
            "untreated. <bookmark mark='c'/> If treatment and recovery were independent, each cell would be expected to "
            "hold its row total times its column total over n: the grey numbers. <bookmark mark='d'/> Pearson's "
            "statistic is nine point three on one degree of freedom, p equals point zero zero two, and Fisher's exact "
            "test agrees. <bookmark mark='e'/> Strong evidence that treatment and recovery are associated. But "
            "associated how?"
        ) as vo:
            self.play(*[FadeIn(g[0]) for g in grid], FadeIn(rl), FadeIn(cl), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(g[1]) for g in grid], FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(g[2]) for g in grid], FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3:5]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def confounded(self):
        rec = W_rates()
        rows = fit_rows(VGroup(
            label(r"the World knows why: \ doctors treat the sicker patients (Part 5's Simpson's paradox)", font_size=26),
            MathTex(rf"\text{{mild: \ treated }} {100 * rec['mild_t']:.0f}\%\ \text{{vs}}\ {100 * rec['mild_u']:.0f}\%;\qquad "
                    rf"\text{{severe: \ treated }} {100 * rec['sev_t']:.0f}\%\ \text{{vs}}\ {100 * rec['sev_u']:.0f}\%", font_size=30, color=S.KEPT),
            label(r"within each severity, \ treatment \emph{helps}; \ the test found a real association with the wrong sign for the cause",
                  font_size=24),
            label(r"a significance test answers ``is there an association?'', \ never ``why?''", font_size=28, color=OBS),
            label(r"causes: \ Parts 35--37", font_size=24, color=GREY_A),
        ), 12.6, 0.42, [0, 0.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The World knows, because we built it: doctors treat the sicker patients, as in Part 5's "
            "Simpson's paradox. <bookmark mark='b'/> Among mild cases, the treated recover more often than the untreated; "
            "among severe cases, too. <bookmark mark='c'/> Within each severity the treatment helps. The test detected a "
            "real association, but the association runs through severity, and its sign is the opposite of the "
            "treatment's effect. <bookmark mark='d'/> A significance test answers the question, is there an "
            "association? It never answers why. <bookmark mark='e'/> That question belongs to Parts 35 to 37."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()


def W_rates():
    from explainer.stats.world import World

    c = World().clinic
    s, t, r = c["severe"], c["treated"], c["recovered"]
    return {"mild_t": float(r[~s & t].mean()), "mild_u": float(r[~s & ~t].mean()), "sev_t": float(r[s & t].mean()),
            "sev_u": float(r[s & ~t].mean())}
