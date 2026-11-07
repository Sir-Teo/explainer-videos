from __future__ import annotations

from videos.stats.stats20.common import *  # noqa: F403


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.references()
        self.degree()
        self.transcript()

    def recap(self):
        items = [
            (r"a question $\to$ an estimand", SALT), (r"NHANES: \ strata, \ PSUs, \ weights", DES),
            (r"weighted 123.9 vs raw 127.1", DES), (r"design effect 3.6", DES),
            (r"cleaning: \ 5,533 $\to$ 3,071, \ logged", OBS), (r"age confounds, \ the other way", GREY_A),
            (r"the plan: \ $+0.07$ [$-0.50$, $+0.63$]", SALT), (r"checks: \ curvature, \ no harm", HIT),
            (r"four SEs; \ $t$ with 15 df", DES), (r"64 analyses, \ all near zero", OBS),
            (r"two recalls: \ $r=0.32$; \ conditional calibration 0.06", RES), (r"the trials: \ 2--3 mm Hg per g", HIT),
            (r"the World: \ 0.23, \ 0.74, \ 0.96; \ trial 1.9", WLD), (r"one page; \ one command", SALT),
        ]
        rows = VGroup(*[label(rf"{i + 1}.\ \ {t}", font_size=26, color=c) for i, (t, c) in enumerate(items)])
        cols = VGroup(VGroup(*rows[:7]).arrange(DOWN, aligned_edge=LEFT, buff=0.4),
                      VGroup(*rows[7:]).arrange(DOWN, aligned_edge=LEFT, buff=0.4)).arrange(RIGHT, buff=0.7, aligned_edge=UP)
        if cols.width > 13.3:
            cols.width = 13.3
        head = label(r"Part 20, \ in fourteen lines", font_size=38).to_edge(UP, buff=0.4)
        cols.next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Part twenty in fourteen lines. <bookmark mark='a'/> We turned a question about salt into an estimand for"
            " a stated population. NHANES's strata, PSUs and weights changed the mean pressure by three points and "
            "tripled its variance. Cleaning took five and a half thousand adults to three thousand and seventy-one, "
            "every step logged, and exploration showed age confounding the relationship the other way. The "
            "illustrative plan's model found plus point zero seven millimetres per gram, with an interval from minus "
            "point five to plus point six; the checks found curvature but no harm; the four standard errors differed,"
            " while all four intervals included zero; and sixty-four alternative analyses all stayed near zero. But "
            "the repeat recalls exposed measurement concerns, so the recall-day association is not directly "
            "comparable to randomized diet effects. On repeated World surveys, the recall-day estimate averaged point"
            " two three, calibration point seven four and true intake point nine six; a randomized trial's intervals "
            "covered the structural effect at roughly their promised rate. And it all fits on one page, rebuilt by "
            "one command."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows], lag_ratio=0.5), run_time=36.0)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"optimization: \ how estimates are computed", [21]), (r"the linear model, \ in depth", [23]),
            (r"multilevel models; \ MRP for surveys", [25]), (r"choosing a model", [28]),
            (r"potential outcomes and observational causal inference", [35, 36, 37]),
            (r"measurement error and missing data, \ in full", [41]), (r"inference after selection", [56]),
            (r"privacy, \ guaranteed", [63]),
        ], font_size=22)
        intro = label('The analysis motivates methods in the later parts', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "Where it comes back. <bookmark mark='a'/> The master's begins with Part 21, on how estimates are actually "
            "computed. Part 23 takes the linear model apart properly, and Part 25 builds the multilevel models that surveys use "
            "for small areas. Part 28 compares ways of choosing a model. Parts 35 to 37 are the causal inference this survey "
            "couldn't do. Part 41 gives measurement error and missing data their full theory. Part 56 handles inference after "
            "the data have chosen the analysis, and Part 63 makes privacy a theorem."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), FadeIn(card.head), run_time=0.35)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in card.rows], lag_ratio=0.3), run_time=6.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"CDC / NCHS, \emph{NHANES 2017--2018}: \ data, \ documentation and analytic guidelines",
             r"T. Lumley, \emph{Complex Surveys: A Guide to Analysis Using R} (2010)",
             r"R. Carroll, D. Ruppert, L. Stefanski \& C. Crainiceanu, \emph{Measurement Error in Nonlinear Models} (2nd ed., 2006)",
             r"F. Harrell, \emph{Regression Modeling Strategies} (2nd ed., 2015)"],
            [r"F. Sacks et al., \emph{NEJM} (2001); \ F. He, J. Li \& G. MacGregor, \emph{BMJ} (2013)",
             r"INTERSALT Cooperative Research Group, \emph{BMJ} (1988); \ W. Willett, \emph{Nutritional Epidemiology}",
             r"W. DuMouchel \& G. Duncan (1983); \ G. Solon, S. Haider \& J. Wooldridge (2015); \ J. Rao \& C. Wu (1988)",
             r"U. Simonsohn, J. Simmons \& L. Nelson (2020); \ A. Gelman \& E. Loken (2013)"])
        with self.voiceover(
            "The sources for this part: NHANES's own documentation and analytic guidelines, Thomas Lumley's book on complex "
            "surveys, Carroll and colleagues on measurement error, and Frank Harrell's Regression Modeling Strategies; with "
            "the trials, INTERSALT, and the papers on weights, the survey bootstrap and specification curves."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def degree(self):
        rows = fit_rows(VGroup(
            label(r"Stage I: \ the foundations, \ Parts 1--10", font_size=26, color=GREY_A),
            label(r"Stage II: \ the methods, \ Parts 11--20", font_size=26, color=GREY_A),
            label(r"probability, \ inference, \ regression, \ design, \ Bayes, \ the bootstrap, \ time series, \ surveys, \ prediction", font_size=22),
            label(r"and one analysis, \ start to finish", font_size=26, color=SALT),
            label(r"the Bachelor's", font_size=48, color=S.ACCENT),
        ), 12.4, 0.5, [0, 0, 0])
        intro = label('The course completes its bachelor-level stage', font_size=36)
        if intro.width > 12.5:
            intro.width = 12.5
        with self.voiceover(
            "<bookmark mark='a'/> That completes the first two stages: the foundations, <bookmark mark='b'/> and the "
            "methods. <bookmark mark='c'/> Probability and inference, regression and experimental design, counts and "
            "Bayes, the bootstrap, time series, surveys and prediction, <bookmark mark='d'/> and one real analysis, "
            "done honestly from beginning to end. <bookmark mark='e'/> That completes this course's bachelor-level "
            "stage; the curriculum is not an accredited degree."
        ) as vo:
            self.play(FadeIn(intro))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                self.play(FadeIn(rows[k], shift=UP * 0.15))
        self.wait(1.5)
        self.clear_scene()

    def transcript(self):
        tr = transcript_card(done=20, current=None)
        nxt = VGroup(label(r"Part 21", font_size=30, color=GREY_B), label(r"Optimization for Statistics", font_size=48),
                     label(r"how estimates are computed, \ and what duality reveals", font_size=28, color=GREY_A))
        nxt.arrange(DOWN, buff=0.25)
        tr.to_edge(UP, buff=0.8)
        nxt.next_to(tr, DOWN, buff=1.0)
        with self.voiceover(
            "Twenty parts of sixty-five, and the first milestone. <bookmark mark='a'/> The bachelor's is complete. "
            "<bookmark mark='b'/> The master's begins with a question we've been avoiding: every estimate in this course was "
            "the solution of an optimization problem, from least squares to the lasso. How are those problems solved, and what "
            "does their geometry tell us about the estimators? Part 21: optimization for statistics."
        ) as vo:
            self.play(FadeIn(tr))
            self.play(*[tr.cells[i].animate.set_fill(S.ACCENT, opacity=0.9) for i in range(20)])
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
