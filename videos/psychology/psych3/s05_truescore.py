from __future__ import annotations

import numpy as np

from videos.psychology.psych3.common import *  # noqa: F403


class TrueScore(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_person()
        self.variance()
        self.twin()

    def card(self):
        card = chapter_card(4, r"True score and error", r"How much of a score is the person, and how much is the day?",
                            lit={1904: r"Spearman on errors of measurement"}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover(
            "Chapter four. True score and error."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def one_person(self):
        d = load("truescore")
        head = heading(rf"One person, the same {d['k']} questions, 300 times")
        lo, hi = 22.5, 43.5
        edges, dens = density(d["retakes"], lo, hi, int(hi - lo))
        top = float(dens.max()) * 1.2
        A = axes([lo, hi], [0, top], x_length=7.6, y_length=3.5, xticks=[25, 30, 35, 40],
                 xlabel=r"score on one occasion (10 to 50)", center=[-2.6, -0.6, 0])
        ax = A.ax
        bars = hist(ax, edges, dens, OBS, 0.7)
        t = d["person_true"]
        truth = DashedLine(ax.c2p(t, 0), ax.c2p(t, top), color=TRUE, stroke_width=3)
        tlab = label(rf"true score \ {t:.1f}", font_size=24, color=TRUE).next_to(truth, UP, buff=0.06)
        y_b = ax.c2p(0, top * 0.93)[1]
        brace = VGroup(Line([ax.c2p(t - d["sem"], 0)[0], y_b, 0], [ax.c2p(t + d["sem"], 0)[0], y_b, 0], color=ERRC,
                            stroke_width=4))
        blab = label(rf"$\pm${d['sem']:.1f} points", font_size=24, color=ERRC).next_to(brace, RIGHT, buff=0.15)
        eq = VGroup(label(r"$X$", font_size=64, color=OBS), label(r"$=$", font_size=64),
                    label(r"$T$", font_size=64, color=TRUE), label(r"$+$", font_size=64),
                    label(r"$E$", font_size=64, color=ERRC)).arrange(RIGHT, buff=0.25).move_to([4.5, 1.7, 0])
        names = VGroup(
            label(r"$X$: \ the score you observe", font_size=26, color=OBS),
            wrapped_label(r"$T$: \ the true score, the average of all the scores this person would get", 4.6, 26, TRUE),
            wrapped_label(r"$E$: \ error, whatever is left; \ it averages zero", 4.6, 26, ERRC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(eq, DOWN, buff=0.45)
        tag = simulated_tag()
        with self.voiceover(
            "Take one person from the Pool, and give them a ten-item questionnaire about how conscientious they "
            "are. Then wipe their memory and give it to them again, three hundred times. Only a simulation can do "
            f"that, which is why we have one. <bookmark mark='a'/> They don't give the same answers every time. "
            f"The totals run from {d['person_min']:.0f} to {d['person_max']:.0f}. People misread a question, or "
            "hesitate between two answers, or are in a different mood. <bookmark mark='b'/> But the scores "
            "pile up around a centre. Call that centre the person's true score. It's defined as the average of "
            "all the scores they would get. <bookmark mark='c'/> Then every observed score is the true score "
            "plus an error, and the errors average out to zero. That is the whole of classical test theory in "
            "one line, and it's a definition, not a discovery. The true score isn't the person's real "
            "conscientiousness, whatever that is. It's what this test would say about them in the long run. "
            f"<bookmark mark='d'/> The spread of the errors has a name, the standard error of measurement. Here "
            f"it's {d['sem']:.1f} points. So a single score of thirty-three means: somewhere around thirty-three, "
            "give or take five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.06), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(tlab))
            vo.wait_until("c")
            self.play(FadeIn(eq, shift=UP * 0.15))
            self.play(LaggedStart(*[FadeIn(n, shift=RIGHT * 0.1) for n in names], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("d")
            self.play(Create(brace), FadeIn(blab))
        self.clear_scene()

    def variance(self):
        d = load("truescore")
        head = heading(rf"{fmt_int(d['n'])} people: \ why do their scores differ?")
        unit = 0.2
        wx, wt, we = d["var_x"] * unit, d["var_t"] * unit, d["var_e"] * unit
        x0 = -6.2
        bx = Rectangle(width=wx, height=0.6, stroke_width=0, fill_color=OBS, fill_opacity=0.85).move_to([x0 + wx / 2, 1.9, 0])
        bt = Rectangle(width=wt, height=0.6, stroke_width=0, fill_color=TRUE, fill_opacity=0.9).move_to([x0 + wt / 2, 0.8, 0])
        be = Rectangle(width=we, height=0.6, stroke_width=0, fill_color=ERRC, fill_opacity=0.9).move_to(
            [x0 + wt + we / 2, 0.8, 0])
        lx = label(rf"variance of the scores: \ {d['var_x']:.1f}", font_size=26, color=OBS).next_to(bx, UP, buff=0.1)
        lx.align_to(bx, LEFT)
        lt = label(rf"true scores: \ {d['var_t']:.1f}", font_size=26, color=TRUE).next_to(bt, DOWN, buff=0.12)
        lt.align_to(bt, LEFT)
        le = label(rf"error: \ {d['var_e']:.1f}", font_size=26, color=ERRC).next_to(be, DOWN, buff=0.12)
        steps = VGroup(
            label(r"$X = T + E$, \ and the errors are unrelated to the true scores, so", font_size=28, color=GREY_A),
            label(r"$\mathrm{Var}(X) = \mathrm{Var}(T) + \mathrm{Var}(E)$", font_size=40, color=WHITE),
            label(rf"reliability $\;=\; \dfrac{{\mathrm{{Var}}(T)}}{{\mathrm{{Var}}(X)}} \;=\; "
                  rf"\dfrac{{{d['var_t']:.1f}}}{{{d['var_x']:.1f}}} \;=\; {d['var_t'] / d['var_x']:.2f}$", font_size=44,
                  color=P.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to([0, -1.9, 0])
        tag = simulated_tag()
        with self.voiceover(
            f"Now twenty thousand people, one occasion each. <bookmark mark='a'/> Their scores differ. The "
            f"variance of the scores is {d['var_x']:.1f}. Those differences have two sources: the people really "
            "differ, and each person's score has error in it. <bookmark mark='b'/> Because the error has nothing "
            "to do with the true score, the two variances simply add. In the Pool we know every person's true "
            f"score, so we can do the split: {d['var_t']:.1f} from true scores, {d['var_e']:.1f} from error. "
            "<bookmark mark='c'/> The share that is true-score variance is called the reliability of the test. "
            f"Here it's {d['var_t'] / d['var_x']:.2f}. Eighty-three per cent of the differences between these "
            "people's scores are differences between the people. Notice what reliability depends on. It's a "
            "ratio. The same questionnaire, given to a group who are all alike, has less true variance to show, "
            "and a lower reliability. So reliability belongs to a test in a population, not to a test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bx, LEFT), FadeIn(lx))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            self.play(GrowFromEdge(bt, LEFT), FadeIn(lt))
            self.play(GrowFromEdge(be, LEFT), FadeIn(le))
            vo.wait_until("c")
            self.play(FadeIn(steps[2], shift=UP * 0.15))
        self.clear_scene()

    def twin(self):
        d = load("truescore")
        head = heading(r"But nobody ever sees a true score")
        A = axes([8, 52], [8, 52], x_length=4.6, y_length=4.6, xticks=[10, 30, 50], yticks=[10, 30, 50],
                 xlabel=r"form A", ylabel=r"form B", center=[-3.9, -0.45, 0])
        ax = A.ax
        rng_ = np.random.default_rng(5)
        jit = lambda v: np.asarray(v) + rng_.uniform(-0.35, 0.35, len(v))  # noqa: E731
        pts = scatter(ax, jit(d["form_a"]), jit(d["form_b"]), OBS, radius=0.03, opacity=0.6)
        rlab = label(rf"$r = {r2(d['parallel_r'])}$", font_size=40, color=P.ACCENT).next_to(A, UP, buff=0.05)
        steps = VGroup(
            wrapped_label(r"Write a second form of the test: \ different questions, equally good.", 6.4, 28, WHITE),
            label(r"$X = T + E, \qquad X' = T + E'$", font_size=36, color=WHITE),
            wrapped_label(r"The two forms share the true score and nothing else, so", 6.4, 26, GREY_A),
            label(r"$\mathrm{Cov}(X, X') = \mathrm{Var}(T)$", font_size=36, color=TRUE),
            label(r"$\mathrm{corr}(X, X') = \dfrac{\mathrm{Var}(T)}{\mathrm{Var}(X)}$", font_size=40, color=P.ACCENT),
            label(r"the correlation of a test with its twin is its reliability", font_size=27, color=P.ACCENT),
        ).arrange(DOWN, buff=0.24).move_to([3.2, -0.3, 0])
        tag = simulated_tag()
        with self.voiceover(
            "There's a catch. All of that needed the true scores, and outside a simulation nobody has them. "
            "The way out is the cleverest step in the theory. <bookmark mark='a'/> Write a second form of the "
            "test: different questions, just as good. <bookmark mark='b'/> A person's score on each form is "
            "the same true score plus a different error. So the only thing the two forms have in common is "
            "the true score. <bookmark mark='c'/> That means their covariance is the true-score variance, "
            "<bookmark mark='d'/> and their correlation is the true variance over the total variance, which "
            "is the reliability. <bookmark mark='e'/> Check it on the Pool. Two forms, five hundred people "
            f"shown: the correlation is {d['parallel_r']:.2f}, and the reliability we computed from the hidden "
            "true scores was the same. A quantity defined by something unobservable can be estimated from "
            "two things you can observe. Every reliability coefficient you'll ever meet is a version of this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(FadeIn(steps[1]), FadeIn(steps[2]))
            vo.wait_until("c")
            self.play(FadeIn(steps[3], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(steps[4], shift=UP * 0.1), FadeIn(steps[5]))
            vo.wait_until("e")
            self.play(FadeIn(pts, lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(rlab))
        self.clear_scene()
