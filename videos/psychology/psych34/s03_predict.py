from __future__ import annotations

from videos.psychology.psych34.common import *  # noqa: F403
from videos.psychology.psych34.s02_norms import line_card

QUESTIONS = [
    (r"1", r"In Milgram's first published study, \ what share of the 40 men went all the way to 450 volts?", AUTH),
    (r"2", r"In 2023, \ students ran Asch's lines again. \ What share of the critical answers went with the wrong "
           r"majority?", CROWD),
    (r"3", r"Cameras filmed 219 real public fights in three countries. \ In what share did at least one bystander "
           r"step in?", GOOD),
    (r"4", r"787 people at a country fair guessed the weight of an ox. \ How far off was the middle guess?", MODEL),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.quiz()
        self.lines()

    def card(self):
        card = chapter_card(2, r"On you: \ four numbers", r"How strong is the pull of other people?", lit=(),
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter two. On you: four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 23, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Your turn. Write down four numbers before the part answers them. <bookmark mark='a'/> One: in Milgram's "
            "first published study, what share of the forty men went all the way to four hundred and fifty volts? "
            "<bookmark mark='b'/> Two: in 2023, students ran Asch's lines again. What share of the critical answers "
            "went with the wrong majority? <bookmark mark='c'/> Three: cameras filmed two hundred and nineteen real "
            "public fights in three countries. In what share did at least one bystander step in? "
            "<bookmark mark='d'/> And four: seven hundred and eighty-seven people at a country fair guessed the "
            "weight of an ox. How far off was the middle guess? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()

    def lines(self):
        head = heading(r"And Asch's lines, \ on you")
        cards = line_card(comps=(2.0, 2.6, 1.5)).scale(0.8).move_to([-3.0, 0.6, 0])
        answers = VGroup(*[VGroup(Circle(radius=0.24, stroke_width=2, stroke_color=CROWD, fill_color=CROWD,
                                         fill_opacity=0.3), label("B", font_size=18, color=AUTH))
                           for _ in range(5)])
        for a_ in answers:
            a_[1].move_to(a_[0])
        answers.arrange(RIGHT, buff=0.2).next_to(cards, DOWN, buff=0.5)
        you = VGroup(Circle(radius=0.24, stroke_width=3, stroke_color=PERSON, fill_color=PERSON, fill_opacity=0.3),
                     label("?", font_size=20, color=WHITE))
        you[1].move_to(you[0])
        you.next_to(answers, RIGHT, buff=0.35)
        rows = rows_of([
            (r"this part's interactive runs twelve trials alone, \ then twelve with five recorded answers shown "
             r"before yours", YOU),
            (r"on eight of the twelve, \ the five are unanimous and wrong", AUTH),
            (r"the answers are scripted and you know it: \ the pull is weaker than at Asch's table, \ and you can "
             r"measure it anyway", CROWD),
            (r"nothing you answer is stored or sent", GREY_A),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "You can also try Asch's task. <bookmark mark='a'/> This part's interactive runs twelve trials alone, "
            "then twelve more with five recorded answers shown before yours. <bookmark mark='b'/> On eight of the "
            "twelve, the five are unanimous, and wrong. <bookmark mark='c'/> The answers are scripted, and you know "
            "it, so the pull is weaker than at Asch's table, where the others sat beside you. You can measure it "
            "anyway. <bookmark mark='d'/> Nothing you answer is stored or sent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards), FadeIn(answers), FadeIn(you))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
