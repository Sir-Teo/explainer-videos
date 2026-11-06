from __future__ import annotations

import numpy as np

from videos.stats.stats46.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.quarrel()
        self.sizes()
        self.critical()
        self.faithful()
        self.linnik()
        self.upgrades()
        self.objectives()

    def quarrel(self):
        tl = timeline(lit=(1935, 1968)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"two normal samples, \ unequal and unknown variances: \ are the means equal?", font_size=26),
            label(r"1929: \ Walter Behrens; \ 1935: \ Fisher's fiducial answer", font_size=26, color=H1C),
            label(r"Neyman and Bartlett: \ its size is not $\alpha$ for every variance ratio", font_size=26, color=REJC),
            label(r"1938, \ 1947: \ Bernard Welch's approximate degrees of freedom", font_size=26, color=UMPC),
            label(r"1966--68: \ Yuri Linnik: \ no exact test of the natural kind exists", font_size=26, color=S.ACCENT),
        ), 12.4, 0.5, [0, -0.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The oldest open sore in testing. Two normal samples, with variances that are unequal and "
            "unknown: are their means equal? <bookmark mark='b'/> Walter Behrens proposed a test in 1929, and in 1935 Fisher "
            "derived it again from his fiducial argument. <bookmark mark='c'/> Neyman and Maurice Bartlett objected: the "
            "test's chance of a false rejection is not exactly alpha for every ratio of the two variances, so it is not a "
            "test in Neyman's sense. Fisher replied that it did not need to be. <bookmark mark='d'/> Bernard Welch's "
            "approximation, with estimated degrees of freedom, became the practical answer. <bookmark mark='e'/> And in the "
            "1960s Yuri Linnik proved that no exact test of the natural kind exists at all. This part is the theory behind "
            "that quarrel: what an optimal test is, and what an interval can promise."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def sizes(self):
        d = load("bf")
        rows = [[r"$n_1$ (SD)", r"$n_2$ (SD)", r"pooled $t$", r"Welch", r"Behrens--Fisher"]]
        for r in d["rows"]:
            pf = f"{100 * r['pooled']:.2f}" if r["pooled"] < 0.01 else f"{100 * r['pooled']:.1f}"
            rows.append([f"{r['n1']} ({r['s1']:g})", f"{r['n2']} ({r['s2']:g})", pf + "\\%",
                         f"{100 * r['welch']:.1f}\\%", f"{100 * r['bf']:.1f}\\%"])
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.3, colors=[GREY_A, None, None, None, None]).move_to([0, 0.8, 0])
        note_ = fit_rows(VGroup(
            label(r"rejection rates when the means are equal, \ nominal 5\%, \ 20,000 data sets each", font_size=24, color=GREY_A),
            label(r"pooled: \ 30\% or 0.06\%; \ \ Welch: \ close to 5\%; \ \ Behrens--Fisher: \ at most 5\%, \ here", font_size=24, color=S.ACCENT),
        ), 12.4, 0.25, [0, -2.2, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is what is at stake, by simulation, at a nominal five percent. <bookmark mark='b'/> "
            "With equal sizes and equal variances, all three tests are fine. With equal sizes and unequal variances, the "
            "pooled t test drifts a little. <bookmark mark='c'/> But give the small sample the large variance, and the "
            "pooled test rejects a true null thirty percent of the time; swap them, and it almost never rejects. <bookmark "
            "mark='d'/> Welch's test stays near five percent throughout; Behrens and Fisher's test stays at or below it, "
            "here. Neither is exact: their sizes move with the unknown ratio of the variances."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(note_[0]), FadeIn(exact_tag(r"simulated: 20,000 data sets per row")))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            vo.wait_until("d")
            self.play(FadeIn(note_[1]))
        self.clear_scene()

    def critical(self):
        d = load("bf")
        ph = np.degrees(np.asarray(d["phis"]))
        A = axes([0, 90], [1.8, 2.9], x_length=7.4, y_length=4.4, xlabel=r"$\varphi = \arctan\frac{s_1/\sqrt{n_1}}{s_2/\sqrt{n_2}}$ \ (degrees)",
                 ylabel=r"critical value", xticks=[0, 30, 60, 90], yticks=[2.0, 2.4, 2.8], center=[-2.5, 0.2, 0])
        ax = A.ax
        c1 = polyline(ax, ph, d["curves"]["5_25"], H1C, 4)
        c2 = polyline(ax, ph, d["curves"]["10_10"], UMPC, 4)
        z = DashedLine(ax.c2p(0, d["z"]), ax.c2p(90, d["z"]), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(r"Fisher's statistic: \ $d = (\bar x_1 - \bar x_2)/\sqrt{s_1^2/n_1 + s_2^2/n_2}$", font_size=22),
            label(r"fiducially: \ $d \sim T_1 \sin\varphi - T_2 \cos\varphi$, \ $T_i \sim t_{n_i - 1}$", font_size=22, color=GREY_A),
            label(r"teal: \ $n = 5, \ 25$: \ from $t_{24}$ (2.06) to $t_4$ (2.78)", font_size=22, color=H1C),
            label(r"green: \ $n = 10, \ 10$", font_size=22, color=UMPC),
            label(r"the critical value depends on the data's $\varphi$: \ not a fixed-size test", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Fisher's statistic divides the difference in means by the natural standard error. "
            "<bookmark mark='b'/> Fiducially, he treated it as a mixture of two independent t variables, weighted by an "
            "angle phi that measures how much of the standard error comes from each sample. <bookmark mark='c'/> The "
            "critical value then depends on phi: with five and twenty-five observations it runs from the t quantile with "
            "twenty-four degrees of freedom to the one with four. <bookmark mark='d'/> With ten each, the curve is "
            "symmetric and dips in the middle. <bookmark mark='e'/> Because phi is computed from the data, the rejection "
            "region is a curved set, and its probability under the null depends on the true variance ratio."
        ) as vo:
            self.play(FadeIn(A), Create(z), FadeIn(exact_tag(r"exact: \ numerical integration")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def faithful(self):
        d = load("bf")["faithful"]
        rows = [
            cmath(r"\text{Old Faithful, eruption length}", r":", rf"\text{{after waits}} < 70: \ n = {d['n'][0]}, \ \bar x = {d['mean'][0]:.2f}, \ s = {d['sd'][0]:.2f}", font_size=28),
            cmath(r"\phantom{X}", r":", rf"\text{{after waits}} \ge 70: \ n = {d['n'][1]}, \ \bar x = {d['mean'][1]:.2f}, \ s = {d['sd'][1]:.2f}", font_size=28),
            cmath(r"\text{Welch}", r":", rf"t = {d['welch_t']:.1f}, \ \nu = {d['welch_df']:.0f}; \ \ \text{{pooled}}: t = {d['pooled_t']:.1f}, \ \nu = {d['pooled_df']}", font_size=30),
            cmath(r"95\% \text{ CI}", r":", rf"[{d['welch_ci'][0]:.2f}, \ {d['welch_ci'][1]:.2f}] \text{{ minutes longer}}", font_size=32),
        ]
        rows[3][-1].set_color(UMPC)
        whys = [why(r"103 eruptions"), why(r"169 eruptions"), why(r"no contest here"), why(r"the quarrel matters for small $n$")]
        with self.voiceover(
            f"<bookmark mark='a'/> Real data rarely make the choice matter as much as the simulation. Old Faithful's "
            f"eruptions: those that follow a wait of under seventy minutes last {say(d['mean'][0], 2)} minutes on "
            f"average, <bookmark mark='b'/> those after longer waits {say(d['mean'][1], 2)} minutes. <bookmark mark='c'/> "
            f"Welch's statistic is about {d['welch_t']:.0f} on {d['welch_df']:.0f} estimated degrees of freedom, and the "
            f"pooled test agrees: with hundreds of eruptions and similar spreads, there is no contest. <bookmark mark='d'/> "
            f"Long waits come before eruptions about two minutes longer. The Behrens–Fisher problem bites with small, "
            f"unbalanced samples, which is exactly where exactness is hardest."
        ) as vo:
            self.play(FadeIn(museum_tag(r"Old Faithful \ (H\"ardle 1991; \ R's \texttt{faithful})")))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def linnik(self):
        rows = fit_rows(VGroup(
            label(r"a \emph{similar} test: \ size exactly $\alpha$ for every $(\sigma_1, \sigma_2)$", font_size=26),
            label(r"Linnik: \ similar tests that are smooth functions of $(\bar x_1, \bar x_2, s_1, s_2)$ \ do not exist", font_size=26, color=REJC),
            label(r"exact similar tests do exist, \ but they are ugly: \ randomized, \ or wildly irregular", font_size=26, color=GREY_A),
            label(r"so: \ approximate (Welch), \ conservative (Behrens--Fisher), \ or Bayesian", font_size=26, color=UMPC),
            label(r"this part: \ when exact optimal tests exist, \ and what to do when they do not", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The precise question is whether a similar test exists: one whose size is exactly alpha "
            "for every pair of variances. <bookmark mark='b'/> Linnik proved that no similar test is a smooth function of the "
            "sufficient statistics, the two means and the two standard deviations. <bookmark mark='c'/> Similar tests "
            "do exist, but only grotesque ones, randomized or wildly irregular, that nobody would use. <bookmark mark='d'/> "
            "So in practice we choose between an approximate test, a conservative one, and a Bayesian posterior. <bookmark "
            "mark='e'/> This part builds the theory that tells us when exact, optimal tests exist, as for the t test, and "
            "what can and cannot be promised when they do not."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(10, r"tests with size $\alpha$: \ $z$, \ $t$, \ $\chi^2$, \ permutation", r"a test is good if it keeps its size",
                         r"chapters 1--5: \ most powerful, \ unbiased and invariant tests; \ the $t$ test's optimality proved"),
            upgrade_card(11, r"intervals with exact or approximate coverage", r"coverage is the whole promise",
                         r"chapters 6--10: \ optimal sets, \ Fieller's impossibility, \ bounded parameters, \ conditional coverage"),
        ]
        for c in cards:
            c.scale(0.9)
        VGroup(*cards).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Two promises are due. Part ten built tests that keep their size, and judged them by that "
            "alone; chapters one to five ask which level-alpha test is most powerful, and prove that the t test is optimal "
            "among unbiased and invariant tests. <bookmark mark='b'/> Part eleven built intervals with good coverage; "
            "chapters six to ten construct optimal confidence sets, show that some problems need infinite intervals, and "
            "ask what coverage means for the data set in hand."
        ) as vo:
            for k, m_ in enumerate("ab"):
                vo.wait_until(m_)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 46", font_size=34, color=GREY_B), label(r"The Theory of Testing and Confidence", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the Neyman--Pearson lemma in general; \ monotone likelihood ratio; \ Karlin--Rubin",
            r"unbiased tests and Neyman structure; \ invariance; \ the likelihood ratio test on a boundary",
            r"confidence sets by inversion; \ Fieller and Gleser--Hwang; \ Feldman--Cousins",
            r"closed testing; \ recognizable subsets; \ p-values as evidence; \ goodness of fit",
        ], color=S.ACCENT, font_size=26)
        prereq = note(r"prerequisites: \ Parts 10, \ 11, \ 45").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.testing}, \ the Neyman-structure visualizer").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part forty-six: the theory of testing and confidence. <bookmark mark='b'/> We'll prove the "
            "Neyman–Pearson lemma in general, with Karlin and Rubin's one-sided theory; build unbiased tests by Neyman "
            "structure, with a visualizer that shows it slice by slice, and invariant tests; take the likelihood ratio test "
            "to the boundary of its parameter space; invert tests into confidence sets and meet their impossibility "
            "theorems; and finish with closed testing, conditional coverage, p-values as evidence, and goodness of fit."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
