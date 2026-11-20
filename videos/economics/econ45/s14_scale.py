from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Scale(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Nudges at scale", r"How big are nudge effects, really?",
             "Chapter twelve. Nudges at scale.", lit={2022: r"DellaVigna and Linos"}, scale=("nation",),
             horizon=("a year",))
        self.two()
        self.funnel()
        self.correct()

    def two(self):
        T = tables.NUDGES_2022.data
        rows = [(r"academic journals", T["academic_effect"], GYM,
                 rf"{T['academic_trials']} trials, \ {T['academic_nudges']} nudges, \ "
                 rf"{T['academic_people']:,} people".replace(",", "{,}")),
                (r"two nudge units, \ every trial", T["unit_effect"], NUDGE,
                 rf"{T['unit_trials']} trials, \ {T['unit_people'] / 1e6:.0f} million people")]
        bars = VGroup()
        for i, (nm, v, col, sub) in enumerate(rows):
            y = 0.8 - 1.7 * i
            w = v * 0.72
            r = Rectangle(width=w, height=0.75, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-2.0 + w / 2, y, 0]))
            nl = VGroup(label(nm, font_size=21, color=col), label(sub, font_size=15, color=GREY_A)).arrange(
                DOWN, aligned_edge=RIGHT, buff=0.1).next_to(np.array([-2.2, y, 0]), LEFT, buff=0.1)
            bars.add(VGroup(nl, r, label(rf"+{v} points", font_size=22, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(rf"the average nudge's effect on take-up \ (control: \ about {T['control']:.0f}\%)", font_size=24,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(rf"selective publication explains about {100 * T['selection_share']:.0f}\% of the gap",
                     font_size=22, color=HOLD).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.NUDGES_2022.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Governments set up nudge units to put these ideas to work: reminder letters, simpler forms, changed "
            "defaults, each tested in a randomized trial. How well do they work? <bookmark mark='a'/> In the "
            f"academic journals, the average nudge raised take-up of the encouraged action by {T['academic_effect']} "
            f"percentage points. <bookmark mark='b'/> Stefano DellaVigna and Elizabeth Linos obtained every trial "
            f"run by two large American nudge units: {T['unit_trials']} trials involving about "
            f"{T['unit_people'] / 1e6:.0f} million people. The average effect was {T['unit_effect']} points: real "
            "and statistically clear, but six times smaller. <bookmark mark='c'/> The authors estimate that about "
            f"{100 * T['selection_share']:.0f} percent of the gap comes from selective publication, made worse by "
            "small samples; most of the rest from differences in the nudges themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bars[0][0]), FadeIn(bars[1][0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][1], LEFT), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][1], LEFT), FadeIn(bars[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def funnel(self):
        N = load("nudges")
        J, U = N["journal"], N["unit"]
        ax = plane([-4, 10], [0, 3.5], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[-4, -2, 0, 2, 4, 6, 8, 10], yticks=[0, 1, 2, 3], xlabel=r"estimated effect, \ points",
                   ylabel=r"standard error \ (larger: \ smaller trial)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        jp = VGroup(*[dot(ax, x, s, GYM, 0.045) for x, s in zip(J["x"], J["se"]) if -4 <= x <= 10 and s <= 3.5])
        up = VGroup(*[dot(ax, x, s, NUDGE, 0.045) for x, s in zip(U["x"], U["se"]) if -4 <= x <= 10 and s <= 3.5])
        sig = path(ax, [0, 1.96 * 3.5], [0, 3.5], LOSS, 2.0, smooth=False)
        siglab = label(r"significant to the right", font_size=15, color=LOSS).next_to(ax.ax.c2p(6.9, 3.5), RIGHT,
                                                                                         buff=0.05)
        true = VGroup(vline(ax, N["mu"], 0, 3.5, WHITE, 1.8), label(rf"truth {N['mu']}", font_size=15,
                                                                    color=WHITE).next_to(ax.ax.c2p(N["mu"], 3.5),
                                                                                         UP, buff=0.08))
        side = VGroup(
            label(rf"gold: \ {J['n']} trials a journal \\ published, \ of {J['run']} run", font_size=18, color=GYM),
            label(rf"their mean: \ {J['mean']:.1f}", font_size=18, color=GYM),
            label(rf"blue: \ {U['n']} larger trials, \\ all reported; \ mean {U['mean']:.1f}", font_size=18,
                  color=NUDGE),
            label(r"small trials get \\ published only when \\ they overshoot", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island shows how the filter works. Every nudge here truly raises take-up by "
            f"{N['mu']} points on average. <bookmark mark='a'/> Researchers run {J['run']} small trials, and a "
            "journal publishes the ones that are statistically significant, plus one in ten of the rest. Each gold "
            "dot is a published trial: its estimate across, its standard error up the side, so small trials sit "
            "high. The red line is the edge of significance. <bookmark mark='b'/> The published mean is "
            f"{J['mean']:.1f}, nearly double the truth: small trials only clear the bar when luck pushes their "
            f"estimates up. <bookmark mark='c'/> A unit that reports all {U['n']} of its larger trials gets "
            f"{U['mean']:.1f}. <bookmark mark='d'/> Nobody cheated. The filter alone did it: the winner's curse, "
            "which Part fifty-six of Statistics, Built treats as inference on winners, and the same arithmetic that "
            "inflates any literature that publishes by significance."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(sig), FadeIn(siglab), FadeIn(true), run_time=1.2)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in jp], lag_ratio=0.01), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p) for p in up], lag_ratio=0.01), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def correct(self):
        N = load("nudges")
        M = N["mle"]
        eq = MathTex(r"L(\mu, \tau, \gamma) = \prod_{i} \frac{p(z_i)\, \phi\!\left(\frac{x_i - \mu}{\sigma_i}\right) / "
                     r"\sigma_i}{\Pr(\text{published}_i)}, \qquad p(z) = \begin{cases} 1 & z \ge 1.96 \\ \gamma & "
                     r"z < 1.96 \end{cases}", font_size=30, color=THEORY).move_to(UP * 1.6)
        rows = VGroup(
            label(rf"naive average of the published: \ {M['naive']:.2f}", font_size=22, color=GYM),
            label(rf"selection model: \ $\hat\mu$ = {M['mu']:.2f}, \ $\hat\gamma$ = {M['gamma']:.2f}", font_size=22,
                  color=E.ACCENT),
            label(rf"the truth: \ $\mu$ = {N['mu']}, \ $\gamma$ = {TRUTH['nudges']['gamma']}", font_size=22,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 0.9)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Can the filter be undone from the published trials alone? <bookmark mark='a'/> Isaiah Andrews and "
            "Maximilian Kasy's approach: model the filter. Each true effect is drawn around mu; each estimate "
            "around its true effect; and an estimate is published for sure if significant, with probability gamma "
            "if not. The likelihood of what was published divides by the chance of being published. "
            f"<bookmark mark='b'/> The naive average is {M['naive']:.2f}. <bookmark mark='c'/> The selection model "
            f"estimates {M['mu']:.2f}, and a publication chance for insignificant trials of {M['gamma']:.2f}. "
            f"<bookmark mark='d'/> The truth is {N['mu']} and {TRUTH['nudges']['gamma']}. The correction is not "
            "perfect, and it rests on the model of the filter being right, but it moves most of the way back."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq), run_time=2.0)
            for mk, r_ in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
