from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Nine vegetables, \ every pair: \ what share of people preferred corn to turnips?", PERSON),
    (r"2", r"Two options split 50:50. \ Add a third that is worse than the first on both attributes. \ The first "
           r"option's share becomes?", AUTH),
    (r"3", r"Two unrelated traits, \ each measured by six items all keyed the same way; \ some people agree with "
           r"everything. \ The scales correlate?", MODEL),
    (r"4", r"A net promoter score from 200 customers: \ its margin of error, \ in points?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.compare()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ twelve comparisons, \ and four numbers", r"Can you say which, \ if not "
                            r"how much?", lit=(), part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter one. On you: twelve comparisons, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def compare(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        items = (r"a week by the sea", r"a week in the mountains", r"a week in a city", r"a week at home")
        pairs = ((0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2))
        rows = VGroup()
        for a, b in pairs:
            rows.add(VGroup(word_chip(items[a], color=PERSON, font_size=17, width=4.2), label(r"or", font_size=16,
                                                                                               color=GREY_B),
                            word_chip(items[b], color=SYMP, font_size=17, width=4.2)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.22).move_to([-1.6, -0.2, 0])
        note = rows_of([
            (r"pick one of each pair, \ quickly", WHITE),
            (r"four options make six pairs; \ count your wins", PERSON),
            (r"if you chose the sea over the city, \ and the city over home, \ did you choose the sea over home?", MODEL),
            (r"on the site: \ twelve comparisons of your own, \ turned into a scale, \ and a decoy", YOU),
        ], 3.4, 17, 0.3).move_to([4.6, -0.3, 0])
        with self.voiceover(
            "First, a small version of Thurstone's task. <bookmark mark='a'/> For each pair, pick one, quickly. "
            "<bookmark mark='b'/> Four options make six pairs. Count how often each one won. <bookmark mark='c'/> "
            "And check yourself. If you chose the sea over the city, and the city over home, did you choose the sea "
            "over home? <bookmark mark='d'/> On the course site you can make twelve comparisons of your own, see them "
            "turned into a scale, and meet a decoy."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(note[0]), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.0)
            for m, r in zip("bcd", note[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.wait(1.0)
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers to write down. <bookmark mark='a'/> One: nine vegetables, every pair. What share of "
            "people preferred corn to turnips? <bookmark mark='b'/> Two: two options split fifty-fifty. Add a third "
            "that's worse than the first on both attributes. What becomes of the first option's share? "
            "<bookmark mark='c'/> Three: two unrelated traits, each measured by six items keyed the same way, and some "
            "people agree with everything. How strongly do the scales correlate? <bookmark mark='d'/> And four: a net "
            "promoter score from two hundred customers. What's its margin of error, in points? Pause here, and write "
            "them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
