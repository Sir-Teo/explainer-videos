from __future__ import annotations

import itertools
import math

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


from videos.stats.stats54.checked import separator


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.three()
        self.four()
        self.table()
        self.question()
        self.upgrades()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1971,)).to_edge(UP, buff=0.35)
        rows = fit_rows(VGroup(
            label(r"Moscow, \ 1971: \ Vladimir Vapnik and Alexey Chervonenkis", font_size=28),
            label(r"choose the rule with the fewest mistakes on the sample", font_size=26, color=TRAINC),
            label(r"when will its error on new data be close to its error on the sample?", font_size=26, color=TESTC),
            label(r"not for one rule: \ for all the rules at once, \ uniformly", font_size=26, color=CLASSC),
            label(r"the answer is one number: \ how many ways the class can label points", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, -0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Moscow, 1971. Vladimir Vapnik and Alexey Chervonenkis, working on pattern recognition, "
            "asked a question that became the foundation of learning theory. <bookmark mark='b'/> Suppose you choose, from "
            "some class of rules, the one with the fewest mistakes on your sample. <bookmark mark='c'/> When will its error "
            "on new data be close to its error on the sample? <bookmark mark='d'/> The rule was chosen because it did well "
            "on this sample, so the question must be answered for all rules in the class at once: uniformly. <bookmark "
            "mark='e'/> Their answer turned on a single combinatorial number: how many different ways the class can label a "
            "set of points."
        ) as vo:
            self.play(FadeIn(tl))
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def three(self):
        pts = np.array([[-0.8, -0.6], [0.9, -0.5], [0.0, 0.9]])
        sh = Shatterer(size=1.9)
        panels = VGroup()
        for i, labs in enumerate(itertools.product([0, 1], repeat=3)):
            w, b = separator(pts, labs)
            panels.add(sh.panel(pts, labs, w, b, centre=(-5.1 + 2.25 * (i % 4) + 1.0 * 0, 1.2 - 2.3 * (i // 4), 0)))
        panels.move_to([-1.2, -0.2, 0])
        side = fit_rows(VGroup(
            label(r"three points, \ half-planes", font_size=24),
            label(r"gold: \ labelled 1; \ blue rings: \ 0", font_size=22, color=CLASSC),
            label(r"all $2^3 = 8$ labellings are realized", font_size=22, color=GOODC),
            label(r"the class \emph{shatters} the three points", font_size=22, color=GOODC),
        ), 3.4, 0.45, [5.2, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The idea, drawn with this part's instrument, the shatterer. Three points in the plane, and "
            "the class of half-planes: a rule labels a point one if it lies on one side of a line. <bookmark mark='b'/> Gold "
            "points are labelled one, blue rings zero. <bookmark mark='c'/> All eight ways of labelling three points can be "
            "produced by some half-plane. <bookmark mark='d'/> We say the class shatters the three points: on them it can "
            "fit anything, so a perfect fit tells you nothing."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.15), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def four(self):
        sq = np.array([[-0.8, -0.8], [0.8, -0.8], [-0.8, 0.8], [0.8, 0.8]])
        sh = Shatterer(size=2.4)
        good = sh.panel(sq, [1, 1, 0, 0], *separator(sq, [1, 1, 0, 0]), centre=(-4.2, 0.3, 0))
        good2 = sh.panel(sq, [1, 0, 0, 0], *separator(sq, [1, 0, 0, 0]), centre=(-1.4, 0.3, 0))
        bad = sh.panel(sq, [1, 0, 0, 1], None, centre=(1.4, 0.3, 0))
        d = load("shatter")
        side = fit_rows(VGroup(
            label(r"four points: \ the diagonals labelled alike", font_size=22),
            label(r"no line separates them: \ the XOR pattern", font_size=22, color=BADC),
            label(rf"half-planes realize {d['four_square']} of the 16 labellings here", font_size=22, color=CLASSC),
            label(r"no 4 points can be shattered: \ VC dimension 3", font_size=22, color=GOODC),
        ), 3.6, 0.45, [5.1, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Four points are different. Put them at the corners of a square and label the diagonals "
            f"alike. <bookmark mark='b'/> No line separates one diagonal from the other: the exclusive-or pattern that once "
            f"stalled the perceptron. <bookmark mark='c'/> Of the sixteen labellings of these four points, half-planes "
            f"produce {d['four_square']}. <bookmark mark='d'/> No set of four points in the plane can be shattered by "
            f"half-planes, so their Vapnik–Chervonenkis dimension is three: the size of the largest set the class can fit "
            f"in every possible way."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(good), FadeIn(good2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(bad), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def table(self):
        d = load("shatter")
        rows = [[r"points $n$"] + [str(r["n"]) for r in d["rows"]],
                [r"all labellings $2^n$"] + [f"{r['all']:,}" for r in d["rows"]],
                [r"by half-planes"] + [str(r["dich"]) for r in d["rows"]],
                [r"Sauer--Shelah, \ $d = 3$"] + [str(r["sauer"]) for r in d["rows"]]]
        tab = table_rows(rows, font_size=26, col_buff=0.55, row_buff=0.42, colors=[GREY_B, GREY_A, CLASSC, BOUNDC])
        if tab.width > 12.8:
            tab.width = 12.8
        tab.move_to([0, 0.9, 0])
        foot = label(r"up to $n = 3$, \ everything; \ beyond, \ only polynomially many: \ $\sum_{i \le 3}\binom{n}{i}$", font_size=24, color=GREY_A).move_to([0, -1.2, 0])
        foot2 = label(r"polynomial, \ not exponential: \ that is why learning is possible", font_size=24, color=GOODC).move_to([0, -2.0, 0])
        r9 = d["rows"][-1]
        with self.voiceover(
            f"<bookmark mark='a'/> Counting the labellings half-planes produce on random points, by brute force. Up to "
            f"three points, all of them. Beyond, far fewer: on nine points, {r9['dich']} of the {r9['all']} possible. "
            f"<bookmark mark='b'/> Norbert Sauer and Saharon Shelah proved in 1972, as Vapnik and Chervonenkis had, that a "
            f"class of VC dimension d produces at most the sum of n choose i for i up to d labellings: a polynomial in n. "
            f"<bookmark mark='c'/> Polynomially many effective rules instead of exponentially many is exactly what lets a "
            f"union bound work, and that is why learning from a sample is possible at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(exact_tag(r"exact, \ by brute force")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"this part's questions:", font_size=28, color=GREY_A),
            label(r"how far can the sample error be from the true error, \ uniformly over a class?", font_size=26, color=TRAINC),
            label(r"when is the rate $1/n$ \ instead of $1/\sqrt n$?", font_size=26, color=TESTC),
            label(r"why do boosting and wide margins, \ and averaging posteriors, \ generalize?", font_size=26, color=CLASSC),
            label(r"and why do models that fit the noise exactly sometimes still predict well?", font_size=26, color=BADC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The questions of this part. <bookmark mark='b'/> How far can the sample error be from the "
            "true error, uniformly over a class of rules? <bookmark mark='c'/> When does the gap shrink like one over n "
            "rather than one over the root of n? <bookmark mark='d'/> Why do boosting, wide margins and averaged posteriors "
            "generalize, even when the classes involved are huge? <bookmark mark='e'/> And why do modern models that fit "
            "the noise in their training data exactly sometimes still predict well, which the classical theory seems to "
            "forbid?"
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def upgrades(self):
        cards = [
            upgrade_card(48, r"uniform laws, \ VC classes, \ chaining", r"empirical processes, \ for their own sake",
                         r"chapters 1--4: \ the risk of the rule you chose"),
            upgrade_card(34, r"conformal and calibrated prediction, \ by experiment", r"exchangeability; \ a fixed model",
                         r"chapters 5--9: \ why the learning algorithm generalizes"),
            upgrade_card(53, r"Gibbs posteriors for misspecified models", r"a likelihood or a loss",
                         r"chapter 6: \ PAC-Bayes bounds for them"),
        ]
        for c in cards:
            c.scale(0.86)
        stack = VGroup(*cards).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        with self.voiceover(
            "<bookmark mark='a'/> Three promises come due. Part forty-eight built uniform laws and VC classes for their own "
            "sake; chapters one to four apply them to the rule you actually chose. <bookmark mark='b'/> Part thirty-four "
            "made predictions with guarantees, by experiment; chapters five to nine explain why learning algorithms "
            "generalize. <bookmark mark='c'/> And Part fifty-three's Gibbs posteriors get their risk bounds in chapter six, "
            "from PAC-Bayes."
        ) as vo:
            for k, m_ in enumerate("abc"):
                vo.wait_until(m_)
                self.play(FadeIn(stack[k], shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 54", font_size=34, color=GREY_B), label(r"Statistical Learning Theory", font_size=48)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"ERM and uniform convergence; \ VC bounds; \ Rademacher complexity and contraction",
            r"localization and fast rates; \ margins for boosting and SVMs",
            r"PAC-Bayes; \ stability; \ online learning and regret; \ calibrated surrogate losses",
            r"interpolation: \ double descent and benign overfitting",
        ], color=CLASSC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 34, \ 48, \ 51").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.slt}, \ the shatterer").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-four: statistical learning theory. <bookmark mark='b'/> We'll study empirical "
            "risk minimization and uniform convergence, VC bounds, and Rademacher complexity with its contraction lemma; "
            "localization and fast rates; margins for boosting and support vector machines; PAC-Bayes bounds; algorithmic "
            "stability; online learning and regret; why convex surrogate losses are safe; and finally interpolation, double "
            "descent and benign overfitting, where the classical story needs revision."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
