from __future__ import annotations

import numpy as np

from videos.psychology.psych1.common import *  # noqa: F403
from explainer.psychology import battery


class Devices(VoiceoverScene):
    def construct(self):
        self.card()
        self.psyche()
        self.pool()
        self.the_battery()
        self.the_map()

    def card(self):
        card = chapter_card(11, r"What the series builds", r"Four devices that run through all sixty-two parts.",
                            lit=(), part=PART, scale=("mind", "person", "group"), marr=("what", "how"))
        with self.voiceover(
            "Chapter eleven. What the series builds."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    # ------------------------------------------------------------------
    def psyche(self):
        mark = butterfly(2.8).move_to([-4.2, 1.1, 0])
        name = VGroup(label(r"Psyche", font_size=72, color=P.PSYCHE),
                      label(r"Greek: \ breath, \ the soul, \ a butterfly", font_size=30, color=GREY_A))
        name.arrange(DOWN, buff=0.15).next_to(mark, DOWN, buff=0.4)
        rules = VGroup()
        for t, sub in ((r"It runs the tasks people do", r"and produces the same kind of data, trial by trial"),
                       (r"It is checked", r"every model against a closed form or an independent reference"),
                       (r"It is fitted, not tuned by eye", r"to named human data, including the errors")):
            rules.add(VGroup(label(t, font_size=40, color=WHITE), label(sub, font_size=27, color=GREY_A))
                      .arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rules.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([2.9, 0.7, 0])
        if rules.get_right()[0] > 6.9:
            rules.scale_to_fit_width(rules.width - (rules.get_right()[0] - 6.9)).move_to([2.9, 0.7, 0])
        key = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.9, color=P.HUMAN, stroke_width=6), label(r"people", font_size=30,
                                                                                 color=P.HUMAN)).arrange(RIGHT, buff=0.2),
            VGroup(Line(ORIGIN, RIGHT * 0.9, color=P.PSYCHE, stroke_width=6), label(r"Psyche", font_size=30,
                                                                                  color=P.PSYCHE)).arrange(RIGHT, buff=0.2),
            VGroup(Line(ORIGIN, RIGHT * 0.9, color=P.POOL, stroke_width=6), label(r"the Pool", font_size=30,
                                                                                color=P.POOL)).arrange(RIGHT, buff=0.2),
        ).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Four devices run through all sixty-two parts. The first you've met. <bookmark mark='a'/> Psyche. "
            "It's the Greek word for breath, for the soul, and for a butterfly. Here it's a library of small "
            "models, one faculty for each part of the series. <bookmark mark='b'/> Each one is a program that "
            "does the same task a person does, and produces the same kind of data. <bookmark mark='c'/> Each is "
            "checked against something independent. <bookmark mark='d'/> And each earns its place by matching "
            "what people do, including their mistakes. <bookmark mark='e'/> The colours never change. People in "
            "white. Psyche in orange."
        ) as vo:
            self.play(FadeIn(mark, scale=0.7))
            vo.wait_until("a")
            self.play(FadeIn(name, shift=UP * 0.15))
            for m, r in zip("bcd", rules):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=LEFT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(key[0]), FadeIn(key[1]))
        self.key = key
        self.clear_scene(key[0], key[1])

    def pool(self):
        d = load("pool_study")
        st = d["stats_400"]
        est = np.asarray(d["est_400"])
        key = self.key
        cloud = pool_cloud(900, width=12.4, height=5.0, seed=3).move_to([0, 0.35, 0])
        head = heading(r"The Pool: \ 100,000 simulated people")
        tag = simulated_tag()
        rng = np.random.default_rng(5)
        picked = VGroup(*[cloud[i] for i in rng.choice(len(cloud), 300, replace=False)])
        truth = label(r"In a real study the truth is hidden. \ In the Pool we wrote it.", font_size=32, color=P.POOL)
        truth.to_edge(DOWN, buff=1.35)
        # the experiment's result
        edges = np.arange(-40.0, 261.0, 12.0)
        dens = np.histogram(est, edges)[0]
        A = axes([-40, 260], [0, float(dens.max()) * 1.15], x_length=9.6, y_length=3.7,
                 xlabel=r"each person's \ $b - c$ \ (ms), \ from 400 trials of each method",
                 xticks=[0, 50, 100, 150, 200, 250], center=[-0.4, -0.35, 0])
        ax = A.ax
        bars = hist(ax, edges, dens, P.POOL, 0.75)
        top = float(dens.max()) * 0.55  # the mean line stops short of the label beside the spike
        mean_line = DashedLine(ax.c2p(st["mean"], 0), ax.c2p(st["mean"], top), color=P.ACCENT, stroke_width=3)
        mean_lab = label(rf"the group's average: \ {st['mean']:.0f} ms", font_size=28, color=P.ACCENT)
        mean_lab.next_to(ax.c2p(st["mean"], top), UR, buff=0.05)
        lab0 = VGroup(label(r"they decide in go/no-go:", font_size=24, color=GONOGO),
                      label(r"no difference", font_size=24, color=GONOGO)).arrange(DOWN, buff=0.05)
        lab0.next_to(ax.c2p(14, float(dens.max()) * 0.87), RIGHT, buff=0.1)
        lab1 = VGroup(label(r"they do not:", font_size=24, color=CHOOSE),
                      label(rf"about {d['true_bc_nondeciders']:.0f} ms", font_size=24, color=CHOOSE)).arrange(DOWN, buff=0.05)
        lab1.next_to(ax.c2p(d["true_bc_nondeciders"] + 52, float(dens.max()) * 0.24), UR, buff=0.05)
        nobody = label(r"the average describes no one", font_size=34, color=P.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The second device is the Pool: a hundred thousand simulated people, each one a Psyche with its own "
            "settings. Faster and slower, older and younger. <bookmark mark='a'/> In a real experiment the truth "
            "is hidden. That's why you're doing the experiment. In the Pool we know the truth, because we wrote "
            "it. So of any method we can ask: does it find what's really there? <bookmark mark='b'/> Here's "
            f"Donders' experiment, run on {d['n_people']} people from the Pool. <bookmark mark='c'/> On average, "
            f"b minus c comes to {st['mean']:.0f} milliseconds. So a choice takes {st['mean']:.0f} milliseconds. "
            "<bookmark mark='d'/> Except that it doesn't, for anyone. We built the Pool on Wundt's objection. "
            "About half its people decide in the go/no-go task, so for them b and c take the same time. "
            f"<bookmark mark='e'/> For the rest, the choice takes about {d['true_bc_nondeciders']:.0f}. The "
            "average of the group describes no one in it. <bookmark mark='f'/> That will matter in every act of "
            "this series, and the Pool is how we'll see it. Whatever comes from the Pool is labelled simulated. "
            "It can show what a method does. It is never evidence about people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cloud, lag_ratio=0.002), FadeIn(key[2]), FadeIn(tag), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(truth, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeOut(truth), cloud.animate.set_opacity(0.25), picked.animate.set_color(WHITE).set_opacity(1))
            self.play(FadeOut(cloud), FadeIn(A))
            self.play(FadeIn(bars, lag_ratio=0.05), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(mean_line), FadeIn(mean_lab))
            vo.wait_until("d")
            self.play(FadeIn(lab0, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(lab1, shift=LEFT * 0.15))
            self.play(FadeIn(nobody, shift=UP * 0.15), FadeOut(key))
            vo.wait_until("f")
            self.play(Indicate(tag, color=P.POOL, scale_factor=1.3))
        self.clear_scene()

    def the_battery(self):
        head = heading(r"The Battery: \ twelve tasks and one questionnaire")
        cols = VGroup(*[label(t, font_size=26, color=c) for t, c in ((r"people", P.HUMAN), (r"Psyche", P.PSYCHE),
                                                                     (r"you", P.ACCENT))])
        rows = VGroup()
        for t in battery.TASKS:
            num = label(str(t.number), font_size=22, color=GREY_B)
            nm = label(t.name.replace("&", r"\&"), font_size=23, color=WHITE if t.first_part == 1 else GREY_A)
            cells = VGroup(*[Square(side_length=0.26, stroke_color=c, stroke_width=1.5, fill_color=c,
                                    fill_opacity=0.9 if t.first_part == 1 else 0.0)
                             for c in (P.HUMAN, P.PSYCHE, P.ACCENT)]).arrange(RIGHT, buff=0.75)
            part = label(rf"Part {t.first_part}", font_size=20, color=GREY_B)
            row = VGroup(num, nm, cells, part)
            num.move_to([-5.6, 0, 0])
            nm.move_to([-5.2, 0, 0], aligned_edge=LEFT)
            cells.move_to([2.9, 0, 0])
            part.move_to([5.4, 0, 0], aligned_edge=LEFT)
            row.cells = cells
            rows.add(row)
        rows.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        for r in rows:
            r[0].set_x(-5.6)
            r[1].set_x(-5.2 + r[1].width / 2)
            r.cells.set_x(2.9)
            r[3].set_x(5.4 + r[3].width / 2)
        rows.move_to([0, -0.45, 0])
        for ctitle, cell in zip(cols, rows[0].cells):
            ctitle.next_to(cell, UP, buff=0.28)
        private = label(r"On the course site each part's interactive is the experiment itself. \ Your data stay "
                        r"in your browser.", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The third device is the Battery: twelve classic tasks and one questionnaire, fixed for the whole "
            "series. <bookmark mark='a'/> For each there are three columns. What people do. What Psyche does. "
            "And what you do, because on the course site each part's interactive is the experiment itself, and "
            "your data never leave your browser. <bookmark mark='b'/> Today we filled in the first row. In the "
            "last part of the series, Psyche sits the whole Battery. <bookmark mark='c'/> And the fourth device "
            "is the Ledger, which gets the next chapter to itself."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[3])) for r in rows], lag_ratio=0.08),
                      run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(cols), LaggedStart(*[FadeIn(r.cells) for r in rows], lag_ratio=0.05), FadeIn(private),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(Indicate(VGroup(rows[0][1], rows[0].cells), color=P.ACCENT, scale_factor=1.06))
        self.clear_scene()

    def the_map(self):
        smap = series_map(current=1, done=0)
        with self.voiceover(
            "And this is where we're going. Thirteen acts. <bookmark mark='a'/> First, how to ask a mind a "
            "question without fooling yourself. <bookmark mark='b'/> Then what the mind is made of, and how a "
            "world gets in. <bookmark mark='c'/> Learning, and then thinking, the longest act. "
            "<bookmark mark='d'/> Feeling, growing, the ways people differ, and other people. "
            "<bookmark mark='e'/> What happens when minds suffer, and what helps. That completes a degree. "
            "<bookmark mark='f'/> Then the graduate toolkit, psychology at work, and the frontier."
        ) as vo:
            self.play(FadeIn(smap))
            for mark, acts in zip("abcdef", ((0,), (1, 2), (3, 4), (5, 6, 7, 8), (9,), (10, 11, 12))):
                vo.wait_until(mark)
                self.play(*[Indicate(smap.acts[i].head, color=P.ACCENT, scale_factor=1.12) for i in acts])
        self.clear_scene()
