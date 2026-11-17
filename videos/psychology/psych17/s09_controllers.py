from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403

class Controllers(VoiceoverScene):
    def construct(self):
        self.card()
        self.devaluation()
        self.twostep_task()
        self.signatures()
        self.argued()

    def card(self):
        card = chapter_card(8, r"Habits and plans", r"When do we repeat, \ and when do we plan?",
                            lit={1981: r"Adams \& Dickinson", 2011: r"Daw et al."}, part=PART,
                            scale=("circuit", "mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter eight. Habits and plans."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def devaluation(self):
        head = heading(r"Devalue the reward, \ and see who notices")
        rows = rows_of([
            (r"rats press a lever for sugar pellets", WHITE),
            (r"then the pellets are devalued: \ paired with mild sickness, \ or eaten to the full", REWARD),
            (r"tested without any pellets: \ do the rats still press?", CUE),
            (r"after moderate training they press less: \ the action is aimed at its goal", MB),
            (r"after extensive training they press as before: \ a habit, \ blind to the goal's value", MF),
            (r"in reinforcement learning: \ a planner sees the change at once; \ cached values cannot", VALUE),
        ], 12.4, 26, 0.3).move_to([0, -1.05, 0])
        phases = VGroup()
        for k, (txt, col) in enumerate([(r"1 \ train: \ press the lever, \ get a pellet", WHITE),
                                        (r"2 \ devalue: \ pellets and mild sickness, \ outside the box", REWARD),
                                        (r"3 \ test: \ the lever, \ and no pellets at all", CUE)]):
            r = RoundedRectangle(width=3.5, height=0.95, corner_radius=0.12, stroke_color=col, stroke_width=2.5)
            phases.add(VGroup(r, wrapped_label(txt, 3.2, 21, col).move_to(r)))
        phases.arrange(RIGHT, buff=0.75).move_to([0, 2.05, 0])
        links = VGroup(*[Arrow(phases[k].get_right(), phases[k + 1].get_left(), buff=0.08, color=GREY_B,
                               stroke_width=3) for k in range(2)])
        tag = historical_tag(archive.ADAMS_DICKINSON_1981.cite)
        with self.voiceover(
            "How can you tell whether an animal is planning or acting from habit? Tony Dickinson and Christopher "
            "Adams found a way in the early 1980s. <bookmark mark='a'/> Rats learn to press a lever for sugar "
            "pellets. <bookmark mark='b'/> Then the pellets are devalued, outside the box: paired with mild sickness, "
            "or eaten until the rats are sick of them. <bookmark mark='c'/> Back in the box the lever delivers "
            "nothing, so the rats can only act on what they know. Do they still press? <bookmark mark='d'/> After "
            "moderate training they press much less: the action is aimed at a goal they no longer want. "
            "<bookmark mark='e'/> After extensive training they press as hard as ever. The action has become a habit, "
            "triggered by the box, and blind to what the goal is now worth. <bookmark mark='f'/> In the terms of this "
            "part: a model-based planner, which values an action by what it leads to, sees the change at once. A "
            "model-free learner, which has cached a value for the action itself, cannot until it experiences the "
            "new outcome."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                extra = {"a": [FadeIn(phases[0])], "b": [GrowArrow(links[0]), FadeIn(phases[1])],
                         "c": [GrowArrow(links[1]), FadeIn(phases[2])]}.get(m, [])
                self.play(FadeIn(r, shift=RIGHT * 0.15), *extra)
        self.clear_scene()

    def twostep_task(self):
        head = heading(r"The two-step task, \ 2011")
        s1 = VGroup(*[RoundedRectangle(width=1.0, height=0.8, corner_radius=0.1, stroke_color=WHITE, stroke_width=3)
                      for _ in range(2)]).arrange(RIGHT, buff=0.6).move_to([0, 2.0, 0])
        l1 = VGroup(label(r"A", font_size=28), label(r"B", font_size=28))
        for l_, b in zip(l1, s1):
            l_.move_to(b)
        s2 = VGroup(*[VGroup(*[RoundedRectangle(width=0.8, height=0.7, corner_radius=0.1, stroke_color=c,
                                                stroke_width=3) for _ in range(2)]).arrange(RIGHT, buff=0.25)
                      for c in (MB, CUE)]).arrange(RIGHT, buff=2.6).move_to([0, -0.2, 0])
        common = VGroup(Arrow(s1[0].get_bottom(), s2[0].get_top(), color=GREY_A, buff=0.1, stroke_width=5),
                        Arrow(s1[1].get_bottom(), s2[1].get_top(), color=GREY_A, buff=0.1, stroke_width=5))
        rare = VGroup(DashedLine(s1[0].get_bottom(), s2[1].get_top(), color=GREY_C, stroke_width=2),
                      DashedLine(s1[1].get_bottom(), s2[0].get_top(), color=GREY_C, stroke_width=2))
        tl = VGroup(label(r"70\%: \ common", font_size=20, color=GREY_A).move_to([-2.4, 1.0, 0]),
                    label(r"30\%: \ rare", font_size=20, color=GREY_C).move_to([0, 0.8, 0]))
        pl = label(r"each second-stage option pays with a probability that drifts slowly", font_size=21,
                   color=REWARD).next_to(s2, DOWN, buff=0.3)
        rows = rows_of([
            (r"a model-free learner repeats a first choice that was followed by reward, \ however it got there", MF),
            (r"a planner knows the transitions: \ a reward after a rare transition argues for the other first "
             r"choice", MB),
        ], 12.4, 25, 0.24).to_edge(DOWN, buff=0.85)
        tag = published_tag(archive.DAW_2011.cite)
        with self.voiceover(
            "In 2011 Nathaniel Daw and colleagues built a task that separates the two strategies trial by trial. "
            "<bookmark mark='a'/> A first choice, between A and B. <bookmark mark='b'/> A usually leads to the pink "
            "state and B to the blue, seventy percent of the time; the other thirty percent, the transition is rare "
            "and you land in the other state. <bookmark mark='c'/> In each second state you choose again, and each "
            "option there pays with a probability that drifts slowly, so there's always something to learn. "
            "<bookmark mark='d'/> Now suppose you chose A, had a rare transition to blue, and were rewarded. A "
            "model-free learner credits A with the reward and repeats it. <bookmark mark='e'/> A planner reasons "
            "differently: blue is what's good now, and the way to reach blue is usually B. So after a rewarded rare "
            "transition, a planner switches."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(s1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(s2), GrowArrow(common[0]), GrowArrow(common[1]), Create(rare), FadeIn(tl))
            vo.wait_until("c")
            self.play(FadeIn(pl))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def signatures(self):
        d = load("twostep")
        head = heading(r"Two signatures, \ and people show both")
        panels = VGroup()
        for k, (name, title, col) in enumerate((("model_free", r"model-free", MF), ("model_based", r"model-based", MB),
                                                ("hybrid", r"a mixture, \ $w = 0.5$", YOU))):
            A = axes([0, 4], [0.3, 1.0], x_length=3.4, y_length=2.6, xticks=[], yticks=[0.4, 0.6, 0.8, 1.0],
                     ylabel=r"P(stay)" if k == 0 else "", center=[-4.4 + 4.4 * k, 0.4, 0], font_size=16)
            bars = VGroup()  # bars start at the axis floor, 0.3
            for x, v, j in zip([0.6, 1.4, 2.6, 3.4], d[name], range(4)):
                h = A.ax.c2p(0, v)[1] - A.ax.c2p(0, 0.3)[1]
                bars.add(Rectangle(width=0.62, height=max(h, 0.01), stroke_width=0,
                                   fill_color=col if j % 2 == 0 else GREY_B, fill_opacity=0.85)
                         .move_to(A.ax.c2p(x, 0.3), aligned_edge=DOWN))
            t = label(title, font_size=23, color=col).next_to(A.ax, UP, buff=0.15)
            xl = VGroup(label(r"rewarded", font_size=17, color=GREY_A).move_to(A.ax.c2p(1.0, 0.3) + DOWN * 0.25),
                        label(r"not", font_size=17, color=GREY_A).move_to(A.ax.c2p(3.0, 0.3) + DOWN * 0.25))
            panels.add(VGroup(A, bars, t, xl))
        lg = legend([(WHITE, r"coloured: \ after a common transition"), (GREY_B, r"grey: \ after a rare one")],
                    font_size=19).arrange(RIGHT, buff=0.6).next_to(panels, DOWN, buff=0.35)
        rows = rows_of([
            (r"model-free: \ reward matters, \ the transition does not", MF),
            (r"model-based: \ the effect of reward flips after a rare transition", MB),
            (r"Daw's 17 participants looked like the mixture, \ and their striatum carried both errors", YOU),
        ], 12.4, 24, 0.18).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ \texttt{rl.two\_step}, \ 30 runs of 400 trials each")
        with self.voiceover(
            "The two strategies leave different fingerprints in how often people repeat their first choice. "
            "<bookmark mark='a'/> A model-free learner repeats after reward and switches after no reward, whatever "
            "the transition was: the coloured and grey bars match. <bookmark mark='b'/> A model-based learner shows "
            "an interaction: after a rare transition, the effect of reward reverses. <bookmark mark='c'/> And a "
            "mixture shows both. Daw's seventeen participants looked like the mixture, and their striatum, in "
            "functional imaging, carried prediction errors computed both ways. People are neither pure creatures of "
            "habit nor pure planners."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(p[0]) for p in panels], *[FadeIn(p[2]) for p in panels],
                      *[FadeIn(p[3]) for p in panels], FadeIn(lg))
            for m, p, r in zip("abc", panels, rows):
                vo.wait_until(m)
                self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in p[1]], lag_ratio=0.2), FadeIn(r), run_time=1.5)
        self.clear_scene()

    def argued(self):
        head = heading(r"What the signature means is argued")
        rows = rows_of([
            (r"the mixture weight became a measure: \ lower in compulsive disorders, \ under stress, \ under load",
             YOU),
            (r"but a clever model-free learner, \ given the right states, \ can mimic the planner's signature", MF),
            (r"and when the task is explained very carefully, \ people look almost entirely model-based", MB),
            (r"the Ledger keeps the pattern \ (replicated) \ apart from its reading \ (contested)", GREY_A),
        ], 12.4, 29, 0.42).move_to([0, -0.1, 0])
        tag = published_tag(archive.FEHER_DA_SILVA_2020.cite)
        with self.voiceover(
            "The task became famous, and its interpretation became an argument. <bookmark mark='a'/> The weight on "
            "planning became a measure: it's lower, on average, in people with compulsive symptoms, under stress, and "
            "when people are distracted by a second task. <bookmark mark='b'/> But a model-free learner given the "
            "right states, for instance one that treats a rare transition as a different situation, can produce the "
            "planner's signature without planning. <bookmark mark='c'/> And in 2020 Carolina Feher da Silva and Todd "
            "Hare found that when the task is explained very carefully, people look almost purely model-based; much of "
            "the apparent habit may be misunderstanding. <bookmark mark='d'/> The Ledger keeps the two apart: the "
            "pattern replicates; what it measures is contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
