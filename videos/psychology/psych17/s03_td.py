from __future__ import annotations

from videos.psychology.psych17.common import *  # noqa: F403


class TD(VoiceoverScene):
    def construct(self):
        self.card()
        self.value()
        self.bellman()
        self.delay_line()

    def card(self):
        card = chapter_card(2, r"Temporal-difference learning", r"How do you learn a prediction from a later "
                            r"prediction?", lit={1988: r"Sutton", 1957: r"Bellman"}, part=PART, scale=("mind",),
                            marr=("what", "how"))
        with self.voiceover("Chapter two. Temporal-difference learning."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def value(self):
        head = heading(r"Value: \ all the reward still to come")
        eq = MathTex(r"V(s_t)", r"=", r"\mathbb{E}\big[\,r_t + \gamma\,r_{t+1} + \gamma^2 r_{t+2} + \cdots\,\big]",
                     font_size=54).move_to([0, 1.4, 0])
        eq[0].set_color(VALUE)
        rows = rows_of([
            (r"$s_t$: \ the state at time $t$ \ (what the animal knows: \ the light came on 0.3 s ago)", CUE),
            (r"$r_t$: \ the reward at time $t$; \ usually zero", REWARD),
            (r"$\gamma$, \ between 0 and 1: \ a reward a step later counts a little less", WHITE),
            (r"value is a prediction of the whole future, \ not of the next reward", VALUE),
        ], 12.0, 28, 0.36).move_to([0, -1.1, 0])
        with self.voiceover(
            "First, what is being predicted. <bookmark mark='a'/> Not the next reward, but all the reward still to "
            "come, from this moment on: the reward now, plus the reward a step later, discounted a little, plus the "
            "one after that, discounted a little more. That sum, averaged over what might happen, is the value of the "
            "state you're in. <bookmark mark='b'/> The state is whatever the animal knows about where it is: here, "
            "that a light came on three tenths of a second ago. <bookmark mark='c'/> Rewards are mostly zero. "
            "<bookmark mark='d'/> And gamma, the discount, a number just below one, says that a reward a step later "
            "is worth a little less than the same reward now."
        ) as vo:
            self.play(FadeIn(head), Write(eq))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bellman(self):
        head = heading(r"Derived: \ from the Bellman equation to the TD error")
        lines = VGroup(
            MathTex(r"V(s_t) = \mathbb{E}\big[\,r_t + \gamma\,V(s_{t+1})\,\big]", font_size=44),
            MathTex(r"\delta_t = r_t + \gamma\,V(s_{t+1}) - V(s_t)", font_size=44, color=DELTA),
            MathTex(r"V(s_t) \leftarrow V(s_t) + \alpha\,\delta_t", font_size=44),
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([-3.0, 1.0, 0])
        notes = VGroup(
            wrapped_label(r"the sum is the reward now plus the discounted value of the next state", 4.6, 22, GREY_A),
            wrapped_label(r"if the predictions were right, \ its average would be zero", 4.6, 22, DELTA),
            wrapped_label(r"so move each prediction toward the next one", 4.6, 22, GREY_A),
        )
        for n, l in zip(notes, lines):
            n.next_to(l, RIGHT, buff=0.5)
            keep_in_frame(n)
        rows = rows_of([
            (r"Richard Bellman, \ 1957: \ a value is the reward now plus the value of what follows", WHITE),
            (r"Richard Sutton, \ 1988: \ learn from the difference between successive predictions", DELTA),
            (r"no need to wait for the end: \ each step teaches the step before it", VALUE),
            (r"the same algorithm learned backgammon, \ and later Go: \ \emph{AI, \ Built}, \ Part 26", REWARD),
        ], 12.4, 26, 0.3).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Now the trick. <bookmark mark='a'/> Pull the first reward out of the sum, and what's left is just gamma "
            "times the value of the next state. So the value of now equals the reward now plus the discounted value "
            "of next. Richard Bellman wrote that equation for engineering problems in the 1950s. "
            "<bookmark mark='b'/> If your predictions were right, the two sides would agree on average, so their "
            "difference, the reward plus the next value minus the current value, would average zero. That difference "
            "is the temporal-difference error, delta. <bookmark mark='c'/> When it isn't zero, move the current "
            "prediction a little toward the target. Richard Sutton set this out as a learning method in 1988. "
            "<bookmark mark='d'/> Notice what it doesn't need: the end of the game. Every step teaches the step "
            "before it, so value flows backward in time, a step per experience. <bookmark mark='e'/> A program "
            "built on it taught itself backgammon to world-class level in the early 1990s, and its descendants "
            "learned Go. AI, Built takes that road in Part 26."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(lines[0]), FadeIn(notes[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(lines[2]), FadeIn(notes[2]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def delay_line(self):
        head = heading(r"Time inside a trial: \ a tapped delay line")
        boxes = VGroup()
        for k in range(10):
            b = Square(0.55, stroke_color=CUE if k == 0 else GREY_C, stroke_width=2)
            boxes.add(b)
        boxes.arrange(RIGHT, buff=0.12).move_to([0, 1.3, 0])
        lab = VGroup(*[label(rf"{0.1 * k:.1f}", font_size=16, color=GREY_B).next_to(b, DOWN, buff=0.08)
                       for k, b in enumerate(boxes)])
        cap = label(r"seconds since the cue", font_size=20, color=GREY_A).next_to(lab, DOWN, buff=0.12)
        dot = Dot(boxes[0].get_center(), color=CUE, radius=0.12)
        rows = rows_of([
            (r"the cue starts a clock: \ a different unit is active at each moment after it", CUE),
            (r"each unit learns its own value: \ how much reward is still to come from that moment", VALUE),
            (r"a crude model of timing, \ called the complete serial compound; \ enough to show the logic", GREY_A),
        ], 12.4, 27, 0.32).move_to([0, -1.6, 0])
        tag = psyche_tag(r"\texttt{rl.td\_conditioning}: \ 30 steps of 0.1 s, \ cue at step 5, \ juice at step 20")
        with self.voiceover(
            "To use TD on Pavlov's task, the animal needs states within a trial. <bookmark mark='a'/> The simplest "
            "assumption is a clock: the cue starts a chain of units, each active at one moment after the cue, like "
            "the taps on a delay line. <bookmark mark='b'/> Each moment gets its own value, the reward still to come "
            "from then. <bookmark mark='c'/> It's a crude model of how brains keep time, and Part 16 showed that real "
            "timing is scalar and fuzzy. But it's enough to show the logic, and it's the representation Schultz, "
            "Dayan and Montague used."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(boxes), FadeIn(lab), FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(dot), FadeIn(rows[0]))
            self.play(dot.animate.move_to(boxes[-1].get_center()), run_time=2.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
