from __future__ import annotations

import math

from videos.philosophy.philosophy16.common import *  # noqa: F403


class Stopping(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Optional stopping", r"Does it matter why you stopped?", lit=(1969,), part=PART)
        with self.voiceover("Chapter five. Optional stopping."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.walk()
        self.rate()
        self.likelihood()
        self.debate()

    def walk(self):
        d = load("stopping")
        path = d["path"]
        looks = d["looks"][:len(path)]
        head = label(r"Test after every 10 observations, \ stop at the first $p < 0.05$", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        sub = label(r"the null is true: \ mean 0, \ standard deviation 1", font_size=21, color=NULLC).next_to(
            head, DOWN, buff=0.2)
        ax = Axes(x_range=[0, d["looks"][-1], 200], y_range=[0, 1, 0.25], x_length=10.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([0, -1.1, 0])
        xl = label(r"observations so far", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(r"$p$", font_size=20, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        five = DashedLine(ax.c2p(0, 0.05), ax.c2p(d["looks"][-1], 0.05), color=BAD, stroke_width=2)
        fl = label(r"0.05", font_size=17, color=BAD).next_to(five, RIGHT, buff=0.08)
        k = next(i for i, p in enumerate(path) if p < 0.05)
        curve = series_plot(ax, path[:k + 1], FISH, xs=looks[:k + 1], width=3)
        hit = Circle(radius=0.16, color=BAD, stroke_width=3).move_to(ax.c2p(looks[k], path[k]))
        hl = label(r"`significant' \ after " + str(looks[k]) + r" observations", font_size=20, color=BAD).move_to(
            ax.c2p(looks[k] + 260, 0.32))
        hl_arrow = Arrow(hl.get_bottom() + LEFT * 0.6, hit.get_top() + RIGHT * 0.05, buff=0.08, color=BAD,
                         stroke_width=2, max_tip_length_to_length_ratio=0.15)
        with self.voiceover(
            "Suppose an experimenter tests after every ten observations, and stops as soon as p drops below point "
            "zero five. <bookmark mark='a'/>And suppose the null hypothesis is true: there is no effect at all. "
            "<bookmark mark='b'/>Here is one run. The p-value wanders up and down as data accumulate. "
            "<bookmark mark='c'/>Sooner or later it dips below point zero five, and the experimenter stops, and "
            "reports a significant result. Every individual test was done correctly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub), FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(five), FadeIn(fl))
            vo.wait_until("b")
            self.play(Create(curve), run_time=4)
            vo.wait_until("c")
            self.play(Create(hit), FadeIn(hl), GrowArrow(hl_arrow))
        self.clear_scene()

    def rate(self):
        d = load("stopping")
        head = label(r"How often does a true null get rejected?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n_looks = len(d["looks"])
        ax = Axes(x_range=[0, n_looks, 20], y_range=[0, 0.5, 0.1], x_length=8.0, y_length=3.8, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 16}).move_to([-1.8, -0.9, 0])
        xl = label(r"number of looks", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        yl = label(r"share of runs ever `significant'", font_size=18, color=GREY_B).next_to(ax.y_axis, UP,
                                                                                          buff=0.1).align_to(
            ax.y_axis, LEFT)
        curve = series_plot(ax, d["ever_rejected"], BAD, xs=list(range(1, n_looks + 1)), width=4)
        five = DashedLine(ax.c2p(0, 0.05), ax.c2p(n_looks, 0.05), color=GREY_B, stroke_width=1.5)
        side = stack([(r"1 look: \ " + f"{100 * d['ever_rejected'][0]:.0f}" + r"\%", WHITE),
                      (r"10 looks: \ " + f"{100 * d['ever_rejected'][9]:.0f}" + r"\%", FISH),
                      (str(n_looks) + r" looks: \ " + f"{100 * d['final']:.0f}" + r"\%", BAD),
                      (r"unlimited looks: \ 100\%", BAD),
                      (r"the law of the iterated logarithm", GREY_A),
                      (r"Armitage, \ McPherson and Rowe \ (1969)", HIST)], font_size=21, aligned_edge=LEFT).move_to(
            [4.7, -0.6, 0])
        with self.voiceover(
            "Run it two thousand times under the null. <bookmark mark='a'/>With one look, five percent of runs "
            "reject, as promised. <bookmark mark='b'/>With ten looks, about nineteen percent. "
            "<bookmark mark='c'/>With a hundred looks, thirty-five percent. <bookmark mark='d'/>With unlimited "
            "patience, the experimenter is certain to reach significance eventually: the law of the iterated "
            "logarithm guarantees that a random walk crosses any fixed significance boundary. Peter Armitage and "
            "his colleagues computed these numbers in 1969. A test's error rate is a property of the whole plan, "
            "including the plan for stopping."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl), Create(five))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            self.play(Create(curve), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in side[3:]], lag_ratio=0.4))
        self.clear_scene()

    def likelihood(self):
        d = load("stopping")
        head = label(r"The likelihood does not care why you stopped", font_size=30, color=CONN).to_edge(UP,
                                                                                                       buff=0.3)
        eq = MathTex(r"L(\mu \mid x_1, \dots, x_n) \propto \exp\!\Big(\mu \sum x_i - \tfrac{n \mu^2}{2}\Big)",
                     font_size=34, color=ALTC).next_to(head, DOWN, buff=0.4)
        same = label(r"the same function of $\mu$, \ whether $n$ was fixed in advance or chosen by peeking",
                     font_size=21, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        srp = label(r"`the rules governing when data collection stops are irrelevant to data interpretation' \ "
                    r"(Edwards, \ Lindman and Savage, \ 1963)", font_size=20, color=BAYC).next_to(same, DOWN, buff=0.4)
        bound = MathTex(r"P\Big(\exists n:\ \frac{L(\mu_1)}{L(0)} \ge k \ \Big|\ \mu = 0\Big) \le \frac{1}{k}",
                        font_size=32, color=GOAL).next_to(srp, DOWN, buff=0.4)
        chk = label(r"the Reasoner: \ a stopper waiting for $L(0.3)/L(0) \ge 10$ \ errs in " +
                    f"{100 * d['lr_ever_10']:.1f}" + r"\% \ of runs, \ however long it looks", font_size=21,
                    color=OK).next_to(bound, DOWN, buff=0.3)
        with self.voiceover(
            "Now look at the same data through the likelihood. <bookmark mark='a'/>For a normal mean, the likelihood "
            "depends on the data only through their sum and their number. <bookmark mark='b'/>It is the same "
            "function of mu whether the sample size was fixed in advance or chosen by peeking. "
            "<bookmark mark='c'/>Ward Edwards, Harold Lindman and Leonard Savage drew the conclusion in 1963: the "
            "rules governing when data collection stops are irrelevant to data interpretation. "
            "<bookmark mark='d'/>And the likelihood ratio has a guarantee of its own. Under the null, the chance "
            "that it ever reaches k, at any sample size, is at most one over k. <bookmark mark='e'/>A stopper that "
            "waits for a likelihood ratio of ten errs in five percent of runs, never more than ten, however long it "
            "is allowed to look."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(same))
            vo.wait_until("c")
            self.play(FadeIn(srp))
            vo.wait_until("d")
            self.play(Write(bound))
            vo.wait_until("e")
            self.play(FadeIn(chk))
        self.clear_scene()

    def debate(self):
        head = label(r"Whose evidence is it?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the frequentist", r"two experimenters with the same data but different stopping plans have different "
                                 r"error rates, \ so different evidence", NEYP),
            (r"the critic", r"then evidence depends on intentions in the experimenter's head \ (Berger and Berry, "
                            r"\ 1988)", BAYC),
            (r"the reply", r"intentions fix which results \textit{would} have counted: \ that is what makes a test "
                           r"severe \ (Mayo)", NEYP),
            (r"the counter-reply", r"with a flat prior, \ a peeking Bayesian can be sure to see an interval excluding "
                                   r"0 \ (Armitage)", BAD),
            (r"and the resolution?", r"Chapter 12: \ tests by betting are valid whatever the stopping rule", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.4, width=8.8, x_text=-2.6)
        with self.voiceover(
            "So whose evidence is it? <bookmark mark='a'/>The frequentist says that two experimenters with the same "
            "data but different stopping plans have tests with different error rates, and so different evidence. "
            "<bookmark mark='b'/>The critic replies that evidence would then depend on intentions locked in the "
            "experimenter's head, which no reader can see. <bookmark mark='c'/>Deborah Mayo answers that "
            "intentions fix which other results would have counted as significant, and that is exactly what "
            "makes a test severe or not. <bookmark mark='d'/>And Peter Armitage pointed out that a Bayesian with a "
            "flat prior who peeks can be sure to see a credible interval that excludes zero, even when the null is "
            "true. <bookmark mark='e'/>Chapter twelve offers a way out: tests by betting, which stay valid whatever "
            "the stopping rule."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
