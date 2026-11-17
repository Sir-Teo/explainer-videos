from __future__ import annotations

import numpy as np

from videos.psychology.psych3.common import *  # noqa: F403

LEVEL, COST = "#7EC8F5", "#F2A65A"


def arrows(middle_right: bool, flank_right: bool, size: float = 0.85) -> VGroup:
    """Five arrowheads in a row; the middle one is the target."""
    g = VGroup()
    for i in range(5):
        right = middle_right if i == 2 else flank_right
        g.add(label(r"$>$" if right else r"$<$", font_size=int(90 * size), color=P.ACCENT if i == 2 else GREY_B))
    return g.arrange(RIGHT, buff=0.12)


class Paradox(VoiceoverScene):
    def construct(self):
        self.card()
        self.robust()
        self.retest()
        self.trade()

    def card(self):
        card = chapter_card(11, r"The reliability paradox", r"Can a task be a good experiment and a poor test?",
                            lit={2018: r"the reliability paradox"}, part=PART, scale=("person", "group"),
                            marr=("what",))
        with self.voiceover(
            "Chapter eleven. The reliability paradox."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def robust(self):
        d = load("paradox")
        head = heading(r"A task that never fails")
        con = VGroup(arrows(True, True), label(r"the neighbours agree", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.2)
        inc = VGroup(arrows(True, False), label(r"the neighbours disagree", font_size=26, color=COST)).arrange(DOWN, buff=0.2)
        stim = VGroup(con, inc).arrange(RIGHT, buff=1.6).move_to([0, 1.35, 0])
        ask = label(r"which way does the middle arrow point?", font_size=28, color=WHITE).next_to(stim, UP, buff=0.3)
        unit = 0.011
        base = 430.0
        b1 = Rectangle(width=base * unit, height=0.5, stroke_width=0, fill_color=LEVEL, fill_opacity=0.85)
        b2 = Rectangle(width=(base + d["mean_cost"]) * unit, height=0.5, stroke_width=0, fill_color=COST, fill_opacity=0.85)
        bars = VGroup(b1, b2).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([-1.5, -1.2, 0])
        bl = VGroup(label(r"agree", font_size=24, color=LEVEL).next_to(b1, LEFT, buff=0.2),
                    label(r"disagree", font_size=24, color=COST).next_to(b2, LEFT, buff=0.2))
        gap = label(rf"$+{d['mean_cost']:.0f}$ ms", font_size=40, color=COST).next_to(b2, RIGHT, buff=0.3)
        found = VGroup(
            label(rf"{fmt_int(d['studies'])} studies of {d['study_n']} people each:", font_size=28, color=GREY_A),
            label(rf"the effect is found in {100 * d['found']:.0f}\% of them", font_size=36, color=TRUE),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.7)
        tag = simulated_tag()
        with self.voiceover(
            "One more warning, and it's a recent one. It shows that the two halves of psychology, the people who "
            "run experiments and the people who measure individuals, mean opposite things by a good task. "
            "<bookmark mark='a'/> Here's a classic. Five arrows flash up, and you press a key for the direction "
            "of the middle one. Sometimes its neighbours point the same way. Sometimes they point the other "
            "way, and you have to ignore them. <bookmark mark='b'/> Everybody is slower when the neighbours "
            f"disagree. In the Pool the cost is {d['mean_cost']:.0f} milliseconds. Tasks like this are the "
            "workhorses of attention research, and they're loved for one reason: they always work. "
            f"<bookmark mark='c'/> Run two thousand studies of only {d['study_n']} people each, and every single "
            "one finds the effect. If you wanted an experiment that replicates, you couldn't ask for better. "
            "So it seems natural to use the same task as a test: to say that a person with a big cost has poor "
            "control of attention, and to go looking for what that predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ask), FadeIn(con))
            self.wait(3.5)
            self.play(FadeIn(inc))
            vo.wait_until("b")
            self.play(GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT), FadeIn(bl))
            self.play(FadeIn(gap))
            vo.wait_until("c")
            self.play(FadeIn(found, shift=UP * 0.15))
        self.clear_scene()

    def retest(self):
        d = load("paradox")
        h = d["hedge"]
        head = heading(r"The same people, the same task, another day")

        def plot(x, y, lo, hi, ticks, color, cx, title, icc):
            A = axes([lo, hi], [lo, hi], x_length=3.4, y_length=3.4, xticks=ticks, yticks=ticks,
                     xlabel=r"first session (ms)", ylabel=r"second", center=[cx, -0.05, 0], font_size=18)
            pts = scatter(A.ax, np.clip(x, lo, hi), np.clip(y, lo, hi), color, radius=0.028, opacity=0.6)
            t = label(title, font_size=28, color=color).next_to(A, UP, buff=0.3)
            r = label(rf"agreement: \ {r2(icc)}", font_size=34, color=color).next_to(A, DOWN, buff=0.3)
            return VGroup(A, pts, t, r)

        left = plot(d["level_1"], d["level_2"], 250, 650, [300, 450, 600], LEVEL, -4.8, r"how fast a person is",
                    d["level_icc_at"])
        mid = plot(d["cost_1"], d["cost_2"], 0, 130, [0, 60, 120], COST, -0.3, r"a person's cost", d["icc_at"])
        pub = VGroup(
            label(r"in the laboratory, three weeks apart:", font_size=24, color=GREY_A),
            label(rf"Stroop cost: \ {r2(h['stroop'][0])} and {r2(h['stroop'][1])}", font_size=28, color=WHITE),
            label(rf"flanker cost: \ {r2(h['flanker'])}", font_size=28, color=COST),
            wrapped_label(rf"though the two flanker conditions themselves: \ {r2(h['flanker_components'][0])} and "
                          rf"{r2(h['flanker_components'][1])}", 3.9, 24, GREY_A),
            wrapped_label(rf"{h['tasks']} classic tasks: \ from {h['range'][0]:.0f} to {r2(h['range'][1])}", 3.9, 24,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.75, 0.1, 0])
        src = published_tag(archive.HEDGE_2018.cite)
        tag = simulated_tag(r"scatter plots: simulated, the Pool")
        with self.voiceover(
            "So do what any test must survive. Bring the same people back and run it again. "
            "<bookmark mark='a'/> First, how fast each person is overall. People who were quick the first time "
            f"are quick the second. The agreement between sessions is {d['level_icc_at']:.2f}. As a measure of "
            "a person's speed, the task is excellent. <bookmark mark='b'/> Now the cost, the thing the task is "
            f"famous for. The agreement is {d['icc_at']:.2f}. A person's cost today tells you only roughly what "
            "it'll be next time. <bookmark mark='c'/> That's the Pool, built to behave like the real thing. And "
            "here's the real thing. In 2018 Craig Hedge and his colleagues brought people back after three "
            "weeks, on seven of the best-known tasks in cognitive psychology. The Stroop cost came out at about "
            "point six. The flanker cost, the arrows you just saw, at point four. And yet the two conditions "
            "that the flanker cost is the difference between were each perfectly respectable. Across the seven "
            "tasks the figures ran from zero to point eight two. Most were too low to rank individuals by."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left[0]), FadeIn(left[2]), FadeIn(left[1], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(left[3]))
            vo.wait_until("b")
            self.play(FadeIn(mid[0]), FadeIn(mid[2]), FadeIn(mid[1], lag_ratio=0.01), run_time=2.0)
            self.play(FadeIn(mid[3]))
            vo.wait_until("c")
            self.play(FadeIn(src), LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in pub], lag_ratio=0.8), run_time=14.0)
        self.clear_scene()

    def trade(self):
        d = load("paradox")
        head = heading(r"Why: \ what makes an experiment work makes a test fail")
        sds = np.asarray(d["trade_sd"])
        A = axes([0, 62], [0, 1.0], x_length=6.6, y_length=3.9, xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1.0],
                 xlabel=r"how much people differ in the effect (SD, ms)", center=[-2.9, -0.5, 0])
        ax = A.ax
        rel = curve(ax, sds, d["trade_rel"], COST, stroke_width=4)
        dz_max = float(np.max(d["trade_dz"]))
        dz = curve(ax, sds, np.asarray(d["trade_dz"]) / dz_max, TRUE, stroke_width=4)
        here = DashedLine(ax.c2p(d["planted_sd"], 0), ax.c2p(d["planted_sd"], 1.0), color=GREY_B, stroke_width=2)
        here_l = label(rf"the Pool: \ {d['planted_sd']:.0f} ms", font_size=22, color=GREY_A).next_to(here, UP, buff=0.05)
        leg = legend([(TRUE, r"how reliably a study finds the effect (scaled to its maximum)"),
                      (COST, r"how reliably the task ranks people")], font_size=22).next_to(A, DOWN, buff=0.2)
        leg.align_to(A, LEFT)
        i20, i480 = d["trials"].index(20), d["trials"].index(480)
        notes = VGroup(
            wrapped_label(r"An experiment wants everyone to show the same effect: \ differences between people are "
                          r"its noise.", 5.4, 27, TRUE),
            wrapped_label(r"A test wants people to differ: \ differences between people are its signal.", 5.4, 27, COST),
            wrapped_label(r"Subtracting two conditions also subtracts what a person has in common across them, and "
                          r"keeps both errors.", 5.4, 25, GREY_A),
            wrapped_label(rf"More trials help: \ agreement {r2(d['cost_icc'][i20])} with {d['trials'][i20]} trials "
                          rf"a condition, {r2(d['cost_icc'][i480])} with {d['trials'][i480]}.", 5.4, 25, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([4.0, -0.1, 0])
        tag = simulated_tag(r"computed: the Pool's conflict task")
        with self.voiceover(
            "How can one task be so dependable and so undependable? Because the word reliable is being used for "
            "two different ratios. <bookmark mark='a'/> An experimenter asks whether the effect shows up in the "
            "group. That's the size of the effect compared with how much people vary around it. For the "
            "experimenter, differences between people are noise, and the ideal task is one where everybody shows "
            "the same effect. <bookmark mark='b'/> A tester asks whether the task tells people apart. That's "
            "reliability as this part defined it: true differences between people, over everything. For the "
            "tester, differences between people are the signal. <bookmark mark='c'/> Slide along the axis: let "
            "people differ more in the size of their effect. The tester's curve rises and the experimenter's "
            "falls. The tasks that became classics were selected, over decades, for the left-hand end. "
            "<bookmark mark='d'/> There's a second reason, which you can now derive yourself. A cost is a "
            "difference of two scores. Subtracting removes what the two conditions share, which is most of the "
            "stable difference between people, and it keeps the error of both. <bookmark mark='e'/> More trials "
            "help, and so do better models of the task, which we build in Parts 25 and 47. But the general "
            "point stands: a finding that replicates is not thereby a measure of anyone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dz), FadeIn(leg[0]), FadeIn(notes[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(rel), FadeIn(leg[1]), FadeIn(notes[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(here), FadeIn(here_l))
            vo.wait_until("d")
            self.play(FadeIn(notes[2], shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(notes[3], shift=UP * 0.1))
        self.clear_scene()
