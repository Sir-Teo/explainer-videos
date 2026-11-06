from __future__ import annotations

import numpy as np

from videos.stats.stats26.common import *  # noqa: F403


def schools_axes(center=(-1.8, 0.2, 0), y_range=(-35, 60)):
    return axes([-0.6, 7.6], list(y_range), x_length=7.6, y_length=4.8, xlabel=r"school", ylabel=r"estimated effect, \ SAT points",
                xticks=[], yticks=[-20, 0, 20, 40], center=list(center))


def school_bars(ax, y, s, labels, width=2.0, color=None):
    g = VGroup()
    for j, (v, e) in enumerate(zip(y, s)):
        c = color or SCHOOL[j]
        bar = Line(ax.c2p(j, v - width * e), ax.c2p(j, v + width * e), color=c, stroke_width=3)
        dot = Dot(ax.c2p(j, v), radius=0.08, color=c)
        name = label(labels[j], font_size=22, color=c).next_to(ax.c2p(j, -35), DOWN, buff=0.15)
        g.add(VGroup(bar, dot, name))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.data()
        self.two_answers()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1981,)).to_edge(UP, buff=0.35)
        hc = history_card(1981, r"Donald Rubin, \ \emph{Journal of Educational Statistics}",
                          r"the Educational Testing Service ran eight randomized experiments, \ one in each of eight high "
                          r"schools, \ on short coaching courses for the verbal SAT. \ Each school's experiment gave an "
                          r"estimated effect and a standard error. \ What did coaching do, \ school by school?",
                          color=PATH, width=11.0, font_size=23).move_to([0, 1.0, 0])
        rows = fit_rows(VGroup(
            label(r"a test designed so that coaching should not help", font_size=24),
            label(r"eight small experiments: \ every estimate is noisy", font_size=24, color=RES),
        ), 12.0, 0.35, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the late 1970s the Educational Testing Service studied coaching for the verbal SAT. "
            "In each of eight high schools, a separate randomized experiment compared students who took a short coaching "
            "course with students who did not. In 1981 Donald Rubin used the results to show what a Bayesian analysis "
            "could do. <bookmark mark='b'/> The SAT was designed to resist short-term coaching, so large effects would be "
            "surprising. <bookmark mark='c'/> And each experiment was small, so every estimate is noisy."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def data(self):
        d = load("schools")
        y, s, lab = np.asarray(d["y"]), np.asarray(d["sigma"]), d["labels"]
        A = schools_axes()
        ax = A.ax
        zero = DashedLine(ax.c2p(-0.6, 0), ax.c2p(7.6, 0), color=GREY_C, stroke_width=1.5)
        bars = school_bars(ax, y, s, lab, width=1.0)
        bars2 = VGroup(*[Line(ax.c2p(j, v - 2 * e), ax.c2p(j, v + 2 * e), color=SCHOOL[j], stroke_width=1.5).set_opacity(0.6)
                         for j, (v, e) in enumerate(zip(y, s))])
        rows = fit_rows(VGroup(
            label(r"dots: \ each school's estimated effect", font_size=22),
            label(r"thick: \ $\pm 1$ SE; \ thin: \ $\pm 2$ SE", font_size=22, color=GREY_A),
            label(r"school A: \ 28 points; \ school C: \ $-3$", font_size=22, color=SCHOOL[0]),
            label(r"SEs from 9 to 18 points", font_size=22, color=RES),
        ), 3.3, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the eight estimated effects, in SAT points, with their standard errors. "
            "<bookmark mark='b'/> The thick bars are one standard error each way; the thin bars two. <bookmark mark='c'/> "
            "School A's estimate is twenty-eight points; school C's is minus three. <bookmark mark='d'/> But the standard "
            "errors run from nine to eighteen points, and every interval overlaps every other."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b[1], scale=1.5) for b in bars], lag_ratio=0.1), FadeIn(VGroup(*[b[2] for b in bars])),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(b[0]) for b in bars], lag_ratio=0.05), LaggedStart(*[Create(b) for b in bars2], lag_ratio=0.05),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(bars[0][1], scale_factor=1.6), Indicate(bars[2][1], scale_factor=1.6), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def two_answers(self):
        d = load("schools")
        y, s, lab = np.asarray(d["y"]), np.asarray(d["sigma"]), d["labels"]
        A = schools_axes()
        ax = A.ax
        dots = VGroup(*[Dot(ax.c2p(j, v), radius=0.08, color=SCHOOL[j]) for j, v in enumerate(y)])
        names = VGroup(*[label(lab[j], font_size=22, color=SCHOOL[j]).next_to(ax.c2p(j, -35), DOWN, buff=0.15) for j in range(8)])
        pm, pse = d["pooled"], d["pooled_se"]
        band = Rectangle(width=ax.c2p(7.6, 0)[0] - ax.c2p(-0.6, 0)[0], height=ax.c2p(0, pm + 1.96 * pse)[1] - ax.c2p(0, pm - 1.96 * pse)[1],
                         stroke_width=0, fill_color=POOLED, fill_opacity=0.2).move_to(ax.c2p(3.5, pm))
        line = DashedLine(ax.c2p(-0.6, pm), ax.c2p(7.6, pm), color=POOLED, stroke_width=3)
        moves = [dots[j].animate.move_to(ax.c2p(j, pm)) for j in range(8)]
        rows = fit_rows(VGroup(
            label(r"no pooling: \ believe each school's own estimate", font_size=22, color=RAW),
            label(rf"complete pooling: \ one effect, \ ${pm:.1f} \pm {pse:.1f}$", font_size=22, color=POOLED),
            label(rf"test of equal effects: \ $Q = {d['Q']:.1f}$ on 7 df, \ $p = {d['p_Q']:.2f}$", font_size=22),
            label(r"A at 28 and C at $-3$, \ both 7.7?", font_size=22, color=RES),
        ), 3.3, 0.42, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Two obvious answers. No pooling: believe each school's own estimate, so coaching gained "
            "twenty-eight points at A and lost three at C. <bookmark mark='b'/> Complete pooling: the schools are alike, so "
            "combine all eight into one precision-weighted average, seven point seven points, give or take four. "
            "<bookmark mark='c'/> A test of equal effects doesn't come close to rejecting them: the scatter of the eight "
            "estimates is no larger than their standard errors predict. <bookmark mark='d'/> Yet telling school A, whose "
            "own experiment showed twenty-eight, that its effect was seven point seven, feels wrong too."
        ) as vo:
            self.add(schools_tag())
            self.play(FadeIn(A), FadeIn(dots), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(band), Create(line), *moves, FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"no pooling assumes $\tau = \infty$: \ the schools tell us nothing about each other", font_size=26, color=RAW),
            label(r"complete pooling assumes $\tau = 0$: \ the schools are identical", font_size=26, color=POOLED),
            label(r"Part 25's empirical Bayes estimates $\tau$, \ and here gets $\hat\tau = 0$", font_size=26, color=RES),
            label(r"a Bayesian treats $\tau$ as unknown, \ and averages over it", font_size=26, color=SHRUNK),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Both answers are extreme choices of one unknown, tau, the standard deviation of the true "
            "effects across schools. No pooling takes tau to be infinite. <bookmark mark='b'/> Complete pooling takes it to "
            "be zero. <bookmark mark='c'/> Part 25's empirical Bayes estimates tau, and for these data its maximum likelihood "
            "estimate is exactly zero, so empirical Bayes collapses to complete pooling. <bookmark mark='d'/> The Bayesian "
            "answer treats tau itself as unknown, with a prior, and averages over everything the data leave uncertain."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 26", font_size=34, color=GREY_B), label(r"Bayesian Data Analysis", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"hierarchical models, \ exchangeability, \ and the eight schools on a grid",
            r"priors: \ Jeffreys, \ reference, \ weakly informative; \ conjugate families",
            r"Bernstein--von Mises; \ Bayes factors, \ Lindley's paradox, \ Occam's razor",
            r"decisions and the value of information",
            r"checking and workflow; \ the argument; \ the Dirichlet process",
        ], color=SHRUNK, font_size=26)
        prereq = note(r"prerequisites: \ Parts 15 and 25").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.bayes} II; \ the $\tau$ explorer").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part twenty-six: Bayesian data analysis. <bookmark mark='b'/> We'll fit hierarchical models "
            "and justify them by exchangeability; choose priors, from Jeffreys's to weakly informative ones; see when "
            "posteriors and sampling distributions agree; test hypotheses with Bayes factors and meet Lindley's paradox and "
            "Occam's razor; make decisions and price information; check models and follow a workflow; weigh the "
            "philosophical argument honestly; and take a first look at Bayesian nonparametrics."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
