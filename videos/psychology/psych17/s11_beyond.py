from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


class Beyond(VoiceoverScene):
    def construct(self):
        self.card()
        self.complications()
        self.distributional()

    def card(self):
        card = chapter_card(10, r"Is dopamine only an error?", r"What else do dopamine neurons say?",
                            lit={2013: r"Howe et al.", 2020: r"Dabney et al."}, part=PART,
                            scale=("neuron", "circuit"), marr=("what", "tissue"))
        with self.voiceover("Chapter ten. Is dopamine only an error?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def complications(self):
        head = heading(r"Where the simple story strains")
        rows = rows_of([
            (r"ramps: \ as a rat nears a distant reward, \ striatal dopamine climbs steadily, \ not in a burst", REWARD),
            (r"movement: \ some dopamine neurons fire as movements start, \ whatever the reward", CUE),
            (r"salience: \ some respond to surprising or intense events, \ pleasant or not", INHIB),
            (r"replies: \ a ramp can be a TD error under uncertainty about time or position; \ or value itself", VALUE),
            (r"the likely answer: \ dopamine neurons are not all alike, \ and the error is one of several messages",
             YOU),
        ], 6.6, 25, 0.4).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
        t = np.linspace(0, 4, 200)
        shapes = [
            (r"a ramp toward a distant reward", REWARD, 0.15 + 0.75 * (t / 4) ** 2),
            (r"a burst as a movement starts", CUE, 0.15 + 0.8 * np.exp(-((t - 1.2) / 0.12) ** 2)),
            (r"a burst to a loud tone, \ no reward", INHIB, 0.15 + 0.6 * np.exp(-((t - 2.0) / 0.12) ** 2)),
        ]
        traces = VGroup()
        for k, (name, col, y) in enumerate(shapes):
            A = axes([0, 4], [0, 1], x_length=4.4, y_length=1.05, xticks=[], yticks=[], center=[3.8, 1.85 - 1.55 * k, 0])
            tr = curve(A.ax, t, y, col, 3)
            nm = label(name, font_size=19, color=col).next_to(A.ax, UP, buff=0.06).align_to(A.ax, LEFT)
            traces.add(VGroup(A, tr, nm))
        mk = VGroup(DashedLine(traces[0][0].ax.c2p(4, 0), traces[0][0].ax.c2p(4, 1), color=REWARD, stroke_width=1.5),
                    label(r"reward", font_size=16, color=REWARD).next_to(traces[0][0].ax.c2p(4, 1), UP, buff=0.04))
        cap = label(r"schematic shapes, \ not recordings", font_size=17, color=GREY_C).next_to(traces, DOWN, buff=0.2)
        tag = published_tag(archive.HOWE_2013.cite)
        with self.voiceover(
            "The prediction-error account is one of psychology's great successes, and it is not the whole story. "
            "<bookmark mark='a'/> In 2013 Mark Howe, Ann Graybiel and colleagues measured dopamine in the striatum as "
            "rats ran a maze toward a reward. It didn't burst; it ramped up steadily as the rats got closer. A pure "
            "TD error, once learning is complete, shouldn't do that. <bookmark mark='b'/> Other recordings found "
            "dopamine neurons that fire as movements begin, whatever the reward. <bookmark mark='c'/> And some respond "
            "to anything surprising or intense, pleasant or not, which sounds more like salience than value. "
            "<bookmark mark='d'/> There are replies. A ramp can be a TD error if the animal is uncertain where it is or "
            "how much time has passed, and some argue ramps encode value directly. <bookmark mark='e'/> The likeliest "
            "resolution is that dopamine neurons aren't all alike, and the reward prediction error is one important "
            "message among several."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cap))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                extra = {"a": [FadeIn(traces[0]), FadeIn(mk)], "b": [FadeIn(traces[1])], "c": [FadeIn(traces[2])]}
                self.play(FadeIn(r, shift=RIGHT * 0.15), *extra.get(m, []))
        self.clear_scene()

    def distributional(self):
        d = load("distrib")
        head = heading(r"A distribution, \ not an average")
        A = axes([0, 10.5], [0, 0.35], x_length=5.4, y_length=2.2, xticks=[0, 2.5, 5, 7.5, 10], yticks=[0, 0.1, 0.2, 0.3],
                 xlabel=r"reward size", ylabel=r"probability", center=[-3.4, 1.45, 0], font_size=17)
        ax = A.ax
        bars = VGroup(*[Rectangle(width=0.22, height=ax.c2p(0, p)[1] - ax.c2p(0, 0)[1], stroke_width=0,
                                  fill_color=REWARD, fill_opacity=0.85).move_to(ax.c2p(r, 0), aligned_edge=DOWN)
                        for r, p in zip(d["rewards"], d["probs"])])
        mean = DashedLine(ax.c2p(d["mean"], 0), ax.c2p(d["mean"], 0.35), color=WHITE, stroke_width=2)
        ml = label(rf"mean {d['mean']:.1f}", font_size=18).next_to(ax.c2p(d["mean"], 0.35), UP, buff=0.05)
        B = axes([0, 1], [0, 10.5], x_length=5.4, y_length=2.2, xticks=[0, 0.5, 1], yticks=[0, 5, 10],
                 xlabel=r"optimism, \ $\tau$", ylabel=r"where it settles", center=[-3.4, -1.75, 0],
                 font_size=17)
        pts = scatter(B.ax, d["taus"], d["values"], DELTA, radius=0.07)
        rows = rows_of([
            (r"each learner weighs good surprises by $\tau$ and bad ones by $1 - \tau$", WHITE),
            (r"a pessimist settles low, \ an optimist high: \ each at an expectile of the rewards", DELTA),
            (r"together they encode the whole distribution", VALUE),
            (r"2020: \ Dabney and colleagues: \ mouse dopamine neurons differ in their optimism in just this way",
             YOU),
            (r"the idea came from AI, \ where distributional learners improved game-playing agents", GREY_A),
        ], 5.6, 23, 0.32).move_to([3.6, -0.3, 0])
        keep_in_frame(rows)
        tag = published_tag(archive.DABNEY_2020.cite)
        tag2 = psyche_tag(r"computed: \ \texttt{rl.distributional\_td}, \ 13 units")
        with self.voiceover(
            "The newest twist came from artificial intelligence. <bookmark mark='a'/> Suppose rewards vary: usually "
            "small, sometimes large. A single prediction error learns the average. But imagine many learners, each "
            "weighing good surprises and bad surprises differently. <bookmark mark='b'/> An optimist, which counts "
            "good news heavily, settles high; a pessimist settles low. Each settles at a particular point of the "
            "distribution, called an expectile. <bookmark mark='c'/> Together, the population encodes the whole "
            "distribution of rewards, not just its mean. <bookmark mark='d'/> In 2020 Will Dabney and colleagues, "
            "working with Naoshige Uchida's recordings in mice, found that dopamine neurons do differ in exactly "
            "this way: some reverse their response at small rewards, some only at large ones, consistently. "
            "<bookmark mark='e'/> The idea had first improved game-playing agents. Here, for once, a trick from "
            "machine learning came back as a discovery about brains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(B), FadeIn(tag), FadeIn(tag2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2), Create(mean), FadeIn(ml),
                      FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.15), FadeIn(rows[1]),
                      run_time=2.0)
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
