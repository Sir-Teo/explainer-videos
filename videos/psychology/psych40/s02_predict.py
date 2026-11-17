from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"A network meta-analysis compared 21 antidepressants with placebo. \ How many trials did it combine?",
     PERSON),
    (r"2", r"On a 52-point depression scale, \ how far apart were antidepressant and placebo on average in the "
           r"trials sent to the US regulator?", MODEL),
    (r"3", r"A famous finding: \ a serotonin gene variant makes stress more likely to cause depression. \ Did it hold "
           r"in tens of thousands of people?", SYMP),
    (r"4", r"After fifty years of research, \ how much better than chance is the prediction of suicidal behaviour "
           r"from risk factors?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.probe()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ a dot, \ and four numbers", r"Where does your attention go?", lit=(),
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: a dot, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def probe(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        fix = label(r"$+$", font_size=40, color=WHITE).move_to([0, -0.3, 0])
        top = label(r"THREAT", font_size=30, color=WHITE).move_to([0, 0.9, 0])
        bot = label(r"TABLE", font_size=30, color=WHITE).move_to([0, -1.5, 0])
        dot = Dot([0, 0.9, 0], radius=0.12, color=YOU)
        ask = wrapped_label(r"press the key for where the dot appears, \ as fast as you can", 10.0, 22,
                            GREY_A).move_to([0, -2.7, 0])
        note = wrapped_label(r"no score is kept: \ this only shows how the task works", 10.0, 18, GREY_B).move_to(
            [0, 2.0, 0])
        with self.voiceover(
            "First, a trial from a classic task. <bookmark mark='a'/> Look at the cross. Two words flash, one above "
            "and one below. <bookmark mark='b'/> They vanish, and a dot appears where one of them was. Your job is to "
            "say where the dot is, as fast as you can. <bookmark mark='c'/> If your attention was already drawn to "
            "the threatening word, you find the dot a little faster when it replaces that word. That speed-up is "
            "called attentional bias to threat. Nothing is scored here. This only shows how the task works."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(fix))
            vo.wait_until("a")
            self.play(FadeIn(top), FadeIn(bot), run_time=0.3)
            self.wait(0.5)
            vo.wait_until("b")
            self.play(FadeOut(top), FadeOut(bot), run_time=0.2)
            self.play(FadeIn(dot), FadeIn(ask), run_time=0.3)
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
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: a network "
            "meta-analysis compared twenty-one antidepressants with placebo. How many trials did it combine? "
            "<bookmark mark='b'/> Two: on a fifty-two-point depression scale, how far apart were antidepressant and "
            "placebo, on average, in the trials sent to the American regulator? <bookmark mark='c'/> Three: a famous "
            "finding said that a serotonin gene variant makes stress more likely to cause depression. Did it hold "
            "up in tens of thousands of people? <bookmark mark='d'/> And four: after fifty years of research, how "
            "much better than chance is the prediction of suicidal behaviour from risk factors? Pause here, and "
            "write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
