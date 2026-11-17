from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Bloom's tutoring gain was 2 SD. \ What did later reviews of human tutoring find?", PERSON),
    (r"2", r"Psyche studies a list, \ then four reviews crammed into one session or spread over four weeks. \ Recall "
           r"two months later, \ each way?", MODEL),
    (r"3", r"Of studies of feedback on performance, \ what share found that the feedback made performance worse?", AUTH),
    (r"4", r"A growth-mindset lesson given to a whole country's ninth-graders: \ the effect on grades?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ two lists, \ and four numbers", r"Which way of studying will you "
                     r"remember?")
        self.lists()
        self.quiz()

    def lists(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        l1 = VGroup(*[label(w, font_size=24, color=PERSON) for w in (r"harbour", r"violin", r"granite", r"meadow")])
        l1.arrange(DOWN, buff=0.18).move_to([-4.4, 0.4, 0])
        l2 = VGroup(*[label(w, font_size=24, color=MODEL) for w in (r"lantern", r"orchard", r"saddle", r"compass")])
        l2.arrange(DOWN, buff=0.18).move_to([-2.2, 0.4, 0])
        h1 = label(r"massed", font_size=18, color=PERSON).next_to(l1, UP, buff=0.25)
        h2 = label(r"spaced", font_size=18, color=MODEL).next_to(l2, UP, buff=0.25)
        rows = rows_of([
            (r"on the course site: \ two lists of word pairs; \ one is studied three times in a row, \ the other "
             r"three times with other work in between", WHITE),
            (r"first, \ predict which list you will remember better", PERSON),
            (r"the test comes at the end of the page: \ most people predict the massed list, \ and most people "
             r"remember more of the spaced one", MODEL),
            (r"nothing is stored or sent; \ your two scores stay on the page", YOU),
        ], 6.4, 21, 0.4).move_to([3.0, -0.3, 0])
        with self.voiceover(
            "First, an experiment on you. <bookmark mark='a'/> On the course site there are two lists of word pairs. "
            "One is studied three times in a row, and the other three times with other work in between. "
            "<bookmark mark='b'/> First, predict which list you'll remember better. <bookmark mark='c'/> The test "
            "comes at the end of the page. Most people predict the massed list, and most people remember more of the "
            "spaced one. <bookmark mark='d'/> Nothing is stored or sent. Your two scores stay on the page."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(l1), FadeIn(l2), FadeIn(h1), FadeIn(h2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: Bloom's tutoring gain was two standard deviations. What did "
            "later reviews of human tutoring find? <bookmark mark='b'/> Two: Psyche studies a list, then four "
            "reviews, crammed into one session or spread over four weeks. What's its recall two months later, each "
            "way? <bookmark mark='c'/> Three: of studies of feedback on performance, what share found the feedback "
            "made performance worse? <bookmark mark='d'/> And four: a growth-mindset lesson given to a whole "
            "country's ninth-graders. What was the effect on grades? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
