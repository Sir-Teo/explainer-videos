from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.compute import load


class Hook(VoiceoverScene):
    def construct(self):
        self.chain()
        self.runs()
        self.plan()

    # ------------------------------------------------------------------
    def chain(self):
        n = 30
        steps = VGroup(*[Circle(radius=0.16, stroke_color=GREY_B, stroke_width=2) for _ in range(n)]).arrange(RIGHT, buff=0.18)
        steps.scale_to_fit_width(12.6).move_to(UP * 0.4)
        links = VGroup(*[Line(a.get_right(), b.get_left(), color=GREY_D, stroke_width=2) for a, b in zip(steps, steps[1:])])
        p = 0.97
        fail_at = 22  # one run, for illustration: the chance of any run getting through is computed below
        bar = VGroup(label(r"each step right $97\%$ of the time", font_size=28, color=C.BITS)).to_edge(UP, buff=0.6)
        res = label(rf"$30$ steps in a row: \ $0.97^{{30}} = {p ** n:.2f}$", font_size=34, color=WHITE).to_edge(DOWN, buff=1.0)
        tag = note(r"one illustrative run").to_corner(DR, buff=0.3)
        cl = label(r"a chatbot: \ one answer", font_size=28, color=GREY_A).next_to(steps[0], UP, buff=0.35).align_to(steps[0], LEFT)
        al = label(r"an agent: \ a whole job, \ each step depending on the last", font_size=28, color=GREY_A).next_to(steps, UP, buff=0.35)
        with self.voiceover(
            "A chatbot answers one question. <bookmark mark='j'/> An agent has to do a whole job: thirty steps, a "
            "hundred, a thousand, each depending on the last. <bookmark mark='a'/> Even at ninety-seven percent per "
            f"step, thirty steps in a row succeed only {100 * p ** n:.0f} percent of the time."
        ) as vo:
            self.play(FadeIn(steps[0], scale=1.5), FadeIn(cl))
            vo.wait_until("j")
            self.play(ReplacementTransform(cl, al), LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.1) for s_ in steps[1:]], lag_ratio=0.04),
                      LaggedStart(*[Create(l_) for l_ in links], lag_ratio=0.04), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(tag))
            for i in range(n):
                if fail_at is not None and i == fail_at:
                    self.play(steps[i].animate.set_fill(C.SURPRISE, opacity=0.9).set_stroke(C.SURPRISE), run_time=0.3)
                    self.play(*[s_.animate.set_stroke(GREY_D) for s_ in steps[i + 1:]], run_time=0.3)
                    break
                self.play(steps[i].animate.set_fill(C.INTERVAL, opacity=0.8).set_stroke(C.INTERVAL), run_time=0.1)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def runs(self):
        h = load("horizon")
        fails = np.sort(np.asarray(h["runs_fail"]))[::-1]  # longest-lived runs on top: the edge traces the survival curve
        R, N = len(fails), 30
        cw, ch = 0.3, 0.075
        grid = VGroup(*[Rectangle(width=cw * 0.86, height=ch * 0.8, stroke_width=0, fill_color=GREY_D, fill_opacity=0.35)
                        .move_to([(c - (N - 1) / 2) * cw, ((R - 1) / 2 - r) * ch, 0]) for r in range(R) for c in range(N)])
        grid.move_to(DOWN * 0.2)
        front = ValueTracker(0.0)
        ok_c, bad_c, dead_c = ManimColor(C.INTERVAL), ManimColor(C.SURPRISE), ManimColor(GREY_D)

        def paint(m):
            t = front.get_value()
            for i, sq in enumerate(m):
                r, c = divmod(i, N)
                f = fails[r] - 1  # the step (0-based) where this run first goes wrong
                if c >= t:
                    sq.set_fill(dead_c, opacity=0.35)
                elif c < f:
                    sq.set_fill(ok_c, opacity=0.85)
                elif c == f:
                    sq.set_fill(bad_c, opacity=1.0)
                else:
                    sq.set_fill(bad_c, opacity=0.22)

        xl = label(r"step $1$ \ $\longrightarrow$ \ step $30$", font_size=22, color=GREY_A).next_to(grid, UP, buff=0.2)
        yl = label(rf"${R}$ runs", font_size=22, color=GREY_A).rotate(PI / 2).next_to(grid, LEFT, buff=0.2)
        k = int((fails > N).sum())
        res = label(rf"${k}$ of ${R}$ runs reach the end \ ($0.97^{{30}} = {0.97 ** 30:.2f}$)", font_size=30,
                    color=C.INTERVAL).to_edge(DOWN, buff=0.4)
        tag = note(r"simulated: \\ each step right with \\ probability $0.97$").to_corner(DR, buff=0.25)
        with self.voiceover(
            f"Here are {R} attempts at once. <bookmark mark='a'/> Each step, a few more runs go wrong, and a run that "
            f"has gone wrong stays wrong. <bookmark mark='b'/> By step thirty, {k} of {R} are still on track."
        ) as vo:
            self.play(FadeIn(grid, lag_ratio=0.002), FadeIn(xl), FadeIn(yl), FadeIn(tag), run_time=1.2)
            vo.wait_until("a")
            grid.add_updater(paint)
            self.play(front.animate.set_value(N), run_time=5.0, rate_func=linear)
            grid.remove_updater(paint)
            vo.wait_until("b")
            # p^n: the expected number of runs still on track after n steps, as a curve over the grid's edge
            top, left = grid.get_top()[1], grid.get_left()[0]
            surv = VMobject(color=WHITE, stroke_width=3).set_points_smoothly(
                [[left + n * cw, top - R * 0.97 ** n * ch, 0] for n in np.linspace(0, N, 61)])
            sl = MathTex(r"0.97^{\,n}", font_size=32, color=WHITE).next_to(surv.get_end(), RIGHT, buff=0.15)
            self.play(FadeIn(res), Create(surv), FadeIn(sl), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 18: \ Agents and Worlds", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"beliefs, \ long horizons, \ world models, \ robots", font_size=30, color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=18, done=17).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about agents: acting on a belief, surviving long chains of steps, imagining the future, "
            "<bookmark mark='a'/> and moving in the physical world."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
