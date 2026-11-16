from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403

CASES = [
    ("switch", r"Switch", r"pull a lever: \ the trolley turns onto a side track, \ where it kills one person "
                          r"instead of five"),
    ("loop", r"Loop", r"pull a lever: \ the trolley turns onto a loop, \ where one person's body stops it before "
                      r"it comes back round to the five"),
    ("footbridge", r"Footbridge", r"push a large man off a bridge: \ his body stops the trolley, \ and he dies "
                                  r"instead of the five"),
]

QUESTIONS = [
    (r"1", r"Across 42 countries, \ what share of people, \ on average, \ would push the man in Footbridge?", PERSON),
    (r"2", r"In how many of those 42 countries was Switch accepted more than Loop, \ and Loop more than "
           r"Footbridge?", WEST),
    (r"3", r"In the largest replication of a famous infant study, \ what share of babies preferred a puppet that "
           r"helped to one that hindered?", GOOD),
    (r"4", r"Across 28 classic findings tested in 36 countries, \ how often did the effect differ between WEIRD "
           r"and less WEIRD samples?", WORLD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.judge()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ three tracks, \ and four numbers",
                            r"Would you sacrifice one to save five?", lit=(), part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter one. On you: three tracks, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def judge(self):
        head = heading(r"Three trolleys")
        pics = VGroup(*[trolley_case(k, width=3.6) for k, _, _ in CASES]).arrange(RIGHT, buff=0.7)
        pics.move_to([0, 1.0, 0])
        names = VGroup(*[label(n, font_size=24, color=WEST).next_to(p, UP, buff=0.3) for p, (_, n, _) in
                         zip(pics, CASES)])
        texts = VGroup(*[wrapped_label(t, 3.7, 17, GREY_A).next_to(p, DOWN, buff=0.45) for p, (_, _, t) in
                         zip(pics, CASES)])
        ask = wrapped_label(r"for each: \ is it acceptable to do it? \ yes or no", 10.0, 24, YOU).to_edge(DOWN,
                                                                                                     buff=0.9)
        clock = countdown_ring(0.4).move_to([5.6, -2.9, 0])
        with self.voiceover(
            "First, three judgments. A runaway trolley will kill five people on the track. "
            "<bookmark mark='a'/> In Switch, you can pull a lever, and the trolley turns onto a side track where it "
            "kills one person instead. <bookmark mark='b'/> In Loop, the side track loops back to the five, and one "
            "person on the loop will stop the trolley with their body. <bookmark mark='c'/> In Footbridge, you "
            "stand on a bridge beside a large man. If you push him off, his body stops the trolley. He dies, and "
            "the five live. <bookmark mark='d'/> For each one: is it acceptable? Yes or no. Decide now."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pics))
            for m, p, n_, t in zip("abc", pics, names, texts):
                vo.wait_until(m)
                self.play(FadeIn(n_), FadeIn(t), Indicate(p, color=PERSON, scale_factor=1.05))
            vo.wait_until("d")
            self.play(FadeIn(ask), FadeIn(clock))
            self.play(clock.animate.rotate(-TAU), run_time=3.0)
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
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: across forty-"
            "two countries, what share of people, on average, would push the man in Footbridge? "
            "<bookmark mark='b'/> Two: in how many of those forty-two countries was Switch more acceptable than "
            "Loop, and Loop more acceptable than Footbridge? <bookmark mark='c'/> Three: in the largest replication "
            "of a famous infant study, what share of babies preferred a puppet that helped to one that hindered? "
            "<bookmark mark='d'/> And four: twenty-eight classic findings were tested in thirty-six countries. How "
            "often did an effect differ between WEIRD and less WEIRD samples? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
