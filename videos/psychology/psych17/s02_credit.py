from __future__ import annotations

import numpy as np

from videos.psychology.psych17.common import *  # noqa: F403


class Credit(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.second()

    def card(self):
        card = chapter_card(1, r"Credit over time", r"Which earlier step earned the reward?",
                            lit={1959: r"Samuel's checkers", 1980: r"second-order conditioning"}, part=PART,
                            scale=("mind",), marr=("what",))
        with self.voiceover("Chapter one. Credit over time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def problem(self):
        head = heading(r"The credit assignment problem")
        chain = VGroup()
        names = [r"cue", r"wait", r"wait", r"lever", r"wait", r"food"]
        cols = [CUE, GREY_B, GREY_B, MB, GREY_B, REWARD]
        for k, (n, c) in enumerate(zip(names, cols)):
            b = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.12, stroke_color=c, stroke_width=3)
            chain.add(VGroup(b, label(n, font_size=24, color=c).move_to(b)))
        chain.arrange(RIGHT, buff=0.45).move_to([0, 1.5, 0])
        arrows = VGroup(*[Arrow(chain[k].get_right(), chain[k + 1].get_left(), buff=0.06, color=GREY_C,
                                stroke_width=3, max_tip_length_to_length_ratio=0.3) for k in range(len(chain) - 1)])
        rows = rows_of([
            (r"the reward arrives at the end; \ the cue and the action that earned it came earlier", WHITE),
            (r"Rescorla-Wagner updates on a trial's outcome: \ it has no time inside a trial", CUE),
            (r"a chess game is won forty moves after the move that won it", REWARD),
            (r"Arthur Samuel's checkers program, \ 1959: \ improve each position's score toward the next one's", DELTA),
        ], 12.4, 28, 0.38).move_to([0, -1.2, 0])
        with self.voiceover(
            "Here's the problem in its plainest form. <bookmark mark='a'/> A cue appears, time passes, an action is "
            "taken, more time passes, and food arrives. The food is the only feedback. Which of the earlier events "
            "deserves the credit? <bookmark mark='b'/> Rescorla and Wagner's rule can't say: it updates once per trial, "
            "on the trial's outcome, and there is no time inside a trial. <bookmark mark='c'/> The problem is much "
            "bigger than rats. A chess game is won forty moves after the move that won it. <bookmark mark='d'/> The "
            "first program to learn a game well, Arthur Samuel's checkers player of 1959, used a trick: don't wait "
            "for the end of the game. Nudge your estimate of how good each position is toward your estimate of the "
            "next one. Learn a guess from a later, better-informed guess. That trick is the subject of this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.3), Create(arrows), FadeIn(rows[0]),
                      run_time=2.5)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def second(self):
        d = load("migration")
        head = heading(r"Second-order conditioning")
        A = axes([0, 60], [0, 1.0], x_length=6.4, y_length=3.4, xticks=[0, 20, 40, 60], yticks=[0, 0.5, 1],
                 xlabel=r"trials of A $\to$ B, \ with no reward", ylabel=r"value of A", center=[-2.6, 0.2, 0])
        ax = A.ax
        c = curve(ax, np.arange(len(d["second"])), d["second"], VALUE, stroke_width=4)
        rows = rows_of([
            (r"first, \ cue B is followed by food", REWARD),
            (r"then cue A is followed by B, \ and never by food", CUE),
            (r"A comes to bring saliva too: \ second-order conditioning, \ found in Pavlov's laboratory", WHITE),
            (r"for Rescorla-Wagner, \ A predicts nothing; \ for a learner of values in time, \ A predicts B, \ and B "
             r"is worth something", DELTA),
        ], 4.6, 24, 0.34).move_to([4.4, 0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ \texttt{rl.second\_order}, \ TD(0) with $\gamma = 0.98$")
        with self.voiceover(
            "Animals solve a small version of it every day. <bookmark mark='a'/> Train a dog that a buzzer means "
            "food. <bookmark mark='b'/> Then pair a light with the buzzer, and never with food. <bookmark mark='c'/> "
            "The light comes to bring saliva too. Pavlov's laboratory called it second-order conditioning, and it "
            "can be chained further. <bookmark mark='d'/> Rescorla and Wagner's rule has trouble with it: the light "
            "is never followed by food, so the outcome on its trials is zero. A learner of values in time has no "
            "trouble. The light predicts the buzzer, the buzzer is worth something, and that value flows back to the "
            "light. Here it is in Psyche, using the equation from the hook."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "d":
                    self.play(Create(c), run_time=2.0)
        self.clear_scene()
