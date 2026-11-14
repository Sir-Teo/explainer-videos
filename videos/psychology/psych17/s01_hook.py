from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


def raster_panel(d, name, title, center, color):
    """A spike raster (ten trials) over a firing-rate curve, with the cue and the reward marked."""
    A = axes([-0.5, 2.5], [0, 40], x_length=3.9, y_length=1.5, xticks=[0, 1, 2], yticks=[0, 20, 40],
             xlabel=r"seconds from the cue", ylabel="", center=center, font_size=16)
    ax = A.ax
    t = d["t"]
    rate = curve(ax, t, d[f"rate_{name}"], color, stroke_width=3)
    top = ax.c2p(-0.5, 40)[1]
    ras = VGroup()
    for k, sp in enumerate(d[f"spikes_{name}"]):
        y = top + 0.22 + 0.09 * k
        for s in sp:
            if -0.5 <= s <= 2.5:
                x = ax.c2p(s, 0)[0]
                ras.add(Line([x, y - 0.035, 0], [x, y + 0.035, 0], color=GREY_B, stroke_width=1.5))
    cue = DashedLine(ax.c2p(0, 0), [ax.c2p(0, 0)[0], top + 1.2, 0], color=CUE, stroke_width=1.5)
    rew = DashedLine(ax.c2p(1.5, 0), [ax.c2p(1.5, 0)[0], top + 1.2, 0], color=REWARD, stroke_width=1.5)
    t_ = label(title, font_size=22, color=color).next_to([ax.c2p(1.0, 0)[0], top + 1.2, 0], UP, buff=0.1)
    return VGroup(A, rate, ras, cue, rew, t_)


class Hook(VoiceoverScene):
    def construct(self):
        self.recordings()
        self.equation()
        self.question()
        self.objectives()

    def recordings(self):
        d = load("schultz")
        head = heading(r"Three recordings from one neuron's point of view")
        p1 = raster_panel(d, "unpredicted", r"juice, \ unannounced", [-4.6, 0.2, 0], DELTA)
        p2 = raster_panel(d, "predicted", r"a cue, \ then juice", [0.0, 0.2, 0], DELTA)
        p3 = raster_panel(d, "omitted", r"a cue, \ and no juice", [4.6, 0.2, 0], INHIB)
        keys = VGroup(label(r"dashed: \ cue", font_size=20, color=CUE), label(r"juice due", font_size=20, color=REWARD),
                      label(r"ticks: \ spikes, \ ten trials; \ curve: \ firing rate, \ 0 to 40 a second",
                            font_size=20, color=GREY_A))
        keys.arrange(RIGHT, buff=0.6).move_to([0, -1.25, 0])
        rows = rows_of([
            (r"before training: \ a burst when juice arrives", DELTA),
            (r"after training: \ the burst moves to the cue; \ the juice itself brings nothing", DELTA),
            (r"and when promised juice does not come, \ silence, \ exactly when it was due", INHIB),
        ], 12.6, 25, 0.2).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"drawn from Psyche's TD learner, \ after Schultz's recordings in monkeys; \ not his data")
        with self.voiceover(
            "In the late 1980s and 1990s, in Fribourg, Wolfram Schultz recorded single dopamine neurons in the "
            "midbrains of monkeys while they worked for drops of fruit juice. Here is what he saw, drawn on Psyche "
            "rather than copied from his figures. <bookmark mark='a'/> A drop of juice, unannounced: the neuron, "
            "ticking along at a few spikes a second, fires a burst. Juice is good, dopamine is pleasure; so far, the "
            "obvious story. <bookmark mark='b'/> Now a light comes on a second and a half before every drop. After "
            "training, the burst has moved. The neuron fires at the light, and when the juice arrives, nothing: the "
            "same juice, no burst. <bookmark mark='c'/> And on a trial when the light comes on but the juice doesn't, "
            "the neuron falls silent, briefly, at exactly the moment the juice was due. It isn't signalling reward. It "
            "is signalling the difference between the reward it got and the reward it expected."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(keys))
            vo.wait_until("a")
            self.play(FadeIn(p1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(p2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(p3), FadeIn(rows[2]))
        self.clear_scene()

    def equation(self):
        head = heading(r"1997: \ a recording beside an equation")
        eq = MathTex(r"\delta_t", r"=", r"r_t", r"+", r"\gamma\,V(s_{t+1})", r"-", r"V(s_t)", font_size=72)
        eq[0].set_color(DELTA)
        eq[2].set_color(REWARD)
        eq[4].set_color(VALUE)
        eq[6].set_color(VALUE)
        eq.move_to([0, 1.3, 0])
        rows = rows_of([
            (r"the temporal-difference error of reinforcement learning, \ from computer science", WHITE),
            (r"Schultz, \ Dayan and Montague: \ dopamine neurons report $\delta$", DELTA),
            (r"Part 16's prediction error, \ with time put back in", YOU),
        ], 12.0, 30, 0.4).move_to([0, -1.3, 0])
        tag = historical_tag(archive.SCHULTZ_1997.cite)
        with self.voiceover(
            "In 1997 Schultz, with the theorists Peter Dayan and Read Montague, laid those recordings beside an "
            "equation. <bookmark mark='a'/> It comes from reinforcement learning, the branch of computer science "
            "that teaches machines to act: the temporal-difference error. The reward you got, plus the value of where "
            "you are now, minus the value you expected a moment ago. <bookmark mark='b'/> Every feature of the three "
            "recordings falls out of it. <bookmark mark='c'/> It is Part 16's prediction error, with one thing added "
            "back: time."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ learning when the reward comes later")
        rows = rows_of([
            (r"how can a brain credit a reward to a cue or an action that came seconds, \ or moves, \ before it?", CUE),
            (r"is dopamine really the error signal of a learning algorithm?", DELTA),
            (r"how do animals, \ and people, \ balance trying the new against using what works?", REWARD),
            (r"and when do we plan, \ with a map of the world, \ instead of repeating what paid?", MB),
        ], 11.8, 31, 0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Part 16 ended with a rule written for trials, as if nothing happened between a cue and its reward. "
            "<bookmark mark='a'/> Real rewards come later: a chess game is won forty moves after the move that "
            "won it. How can a brain give credit to a cue or an action that came long before? <bookmark mark='b'/> "
            "Is dopamine really the error signal of a learning algorithm, or does the story break somewhere? "
            "<bookmark mark='c'/> How do animals and people balance trying something new against using what works? "
            "<bookmark mark='d'/> And when do we plan, using a map of the world, rather than just repeating what "
            "paid off before?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 17", font_size=34, color=GREY_B), label(r"Reward and Prediction", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"credit over time, \ and temporal-difference learning derived from the Bellman equation",
            r"the TD error on Pavlov's task, \ and Schultz's dopamine neurons",
            r"from prediction to action: \ actor-critic, \ Q-learning, \ the basal ganglia's Go and NoGo",
            r"a bandit you can play, \ your learning rate fitted, \ and how to explore",
            r"Tolman's maps, \ place and grid cells, \ habits against plans, \ the successor representation",
            r"what dopamine is beyond the error; \ addiction; \ recommenders and medication at the frontier",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 17 of Psychology, Built: reward and prediction. <bookmark mark='a'/> We'll start with "
            "the problem of credit over time, and derive temporal-difference learning from the Bellman equation. "
            "We'll run it on Pavlov's task and watch Schultz's recordings appear. Then from prediction to action: "
            "actor and critic, Q-learning, and the Go and NoGo pathways of the basal ganglia. Then a bandit game, "
            "with your learning rate fitted, and the mathematics of exploring. Then Tolman's rats and their maps, place "
            "and grid cells, habits against plans, and a representation that sits between them. And at the end, "
            "what dopamine does besides the error, how a drug can hijack it, and where this mathematics runs your "
            "life: in the recommendations you're shown, and in the side effects of a medicine."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
