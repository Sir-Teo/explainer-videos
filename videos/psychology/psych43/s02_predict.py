from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Describing a face before a line-up: \ will 22 labs find fewer correct picks, \ and how many fewer per "
           r"100 people?", PERSON),
    (r"2", r"A demanding task, \ then self-control: \ will 23 labs find ego depletion?", AUTH),
    (r"3", r"How many people per group does a single study need for 95\% power at $d = 0.1$?", MODEL),
    (r"4", r"The ego-depletion study the replication was based on had 23 and 24 people. \ Its power for $d = 0.2$?",
     GOOD),
]

COLOURS = {"RED": "#EF6F6C", "GREEN": "#5BD18B", "BLUE": "#7EC8F5", "YELLOW": "#F2C14E"}


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.stroop()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ colour words, \ and four predictions", r"What do you expect?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: colour words, and four predictions."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def stroop(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rng = np.random.default_rng(43)
        names = list(COLOURS)
        cong = VGroup(*[label(w, font_size=34, color=COLOURS[w]) for w in rng.choice(names, 8)])
        incong = VGroup()
        for w in rng.choice(names, 8):
            ink = rng.choice([n for n in names if n != w])
            incong.add(label(str(w), font_size=34, color=COLOURS[str(ink)]))
        cong.arrange_in_grid(2, 4, buff=(0.7, 0.4)).move_to([0, 0.9, 0])
        incong.arrange_in_grid(2, 4, buff=(0.7, 0.4)).move_to([0, -1.2, 0])
        lab1 = label(r"name the ink colours, \ fast", font_size=18, color=GREY_A).next_to(cong, UP, buff=0.3)
        lab2 = label(r"now these", font_size=18, color=GREY_A).next_to(incong, UP, buff=0.25)
        note = wrapped_label(r"the second row is slower for nearly everyone: \ Stroop, \ 1935, \ and replicated "
                             r"thousands of times", 11.0, 20, YOU).move_to([0, -2.85, 0])
        with self.voiceover(
            "First, try this. <bookmark mark='a'/> Name the colours of the ink, as fast as you can, not the words. "
            "<bookmark mark='b'/> Now these. <bookmark mark='c'/> The second row is slower for nearly everyone. It's "
            "the Stroop effect, from 1935, replicated thousands of times. On the course site you can run it on "
            "yourself, as a participant in this part's third study."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(lab1), FadeIn(cong))
            vo.wait_until("b")
            self.play(FadeIn(lab2), FadeIn(incong))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 22, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four predictions to write down before the part answers them. <bookmark mark='a'/> One: describing a "
            "face before a line-up. Will twenty-two labs find fewer correct picks, and how many fewer per hundred "
            "people? <bookmark mark='b'/> Two: a demanding task, then a test of self-control. Will twenty-three labs "
            "find ego depletion? <bookmark mark='c'/> Three: how many people per group does a single study need for "
            "ninety-five percent power to detect an effect of zero point one? <bookmark mark='d'/> And four: the "
            "ego-depletion study the replication was based on had twenty-three and twenty-four people. What was its "
            "power for an effect of zero point two? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
