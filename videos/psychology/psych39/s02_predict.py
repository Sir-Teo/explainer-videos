from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"In a large US survey, \ what share of adults had met the criteria for some mental disorder at some "
           r"point in their lives?", PERSON),
    (r"2", r"Two clinicians diagnose the same patients for major depression. \ Their agreement beyond chance, \ "
           r"Cohen's kappa, \ on a scale from 0 to 1?", SYMP),
    (r"3", r"Among 3{,}703 people diagnosed with depression, \ how many different combinations of symptoms?", MODEL),
    (r"4", r"Across studies comparing clinicians with simple formulas, \ in what share did the clinicians clearly "
           r"win?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.positive()
        self.frequencies()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ a positive screen, \ and four numbers",
                            r"What does a positive test mean?", lit=(), part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter one. On you: a positive screen, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def positive(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = rows_of([
            (r"a condition affects 1\% of people", WHITE),
            (r"a screening questionnaire catches 90\% of those who have it", SYMP),
            (r"and wrongly flags 9\% of those who do not", AUTH),
            (r"someone screens positive: \ what is the chance they have the condition?", YOU),
        ], 10.0, 26, 0.42).move_to([0, -0.2, 0])
        clock = countdown_ring(0.4).move_to([5.6, -2.7, 0])
        with self.voiceover(
            "First, a puzzle you've met before, in Part 12. <bookmark mark='a'/> A condition affects one percent of "
            "people. <bookmark mark='b'/> A screening questionnaire catches ninety percent of those who have it. "
            "<bookmark mark='c'/> And it wrongly flags nine percent of those who don't. <bookmark mark='d'/> Someone "
            "screens positive. What's the chance they have the condition? Give a number now."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(clock))
            self.play(clock.animate.rotate(-TAU), run_time=3.0)
        self.wait(1.0)
        self.clear_scene()

    def frequencies(self):
        d = load("screen")
        head = heading(r"In natural frequencies")
        top = word_chip(r"10{,}000 people", color=WHITE, font_size=22, width=3.0).move_to([0, 2.0, 0])
        sick = word_chip(r"100 have it", color=SYMP, font_size=20, width=2.8).move_to([-3.2, 0.7, 0])
        well = word_chip(r"9{,}900 do not", color=GREY_A, font_size=20, width=2.8).move_to([3.2, 0.7, 0])
        tp = word_chip(rf"{d['tp']:.0f} test positive", color=GOOD, font_size=19, width=2.8).move_to([-4.6, -0.7, 0])
        fn = word_chip(rf"{d['fn']:.0f} test negative", color=GREY_B, font_size=19, width=2.8).move_to([-1.8, -0.7, 0])
        fp = word_chip(rf"{d['fp']:.0f} test positive", color=AUTH, font_size=19, width=2.8).move_to([1.8, -0.7, 0])
        tn = word_chip(rf"{num(d['tn'])} test negative", color=GREY_B, font_size=19, width=2.8).move_to([4.6, -0.7, 0])
        lines = VGroup(*[Line(a.get_bottom(), b.get_top(), color=GREY_D, buff=0.05) for a, b in
                         ((top, sick), (top, well), (sick, tp), (sick, fn), (well, fp), (well, tn))])
        ans = wrapped_label(rf"of {d['tp'] + d['fp']:.0f} positives, \ {d['tp']:.0f} have the condition: \ about "
                            rf"{100 * d['ppv']:.0f}\%", 11.0, 26, YOU).move_to([0, -2.0, 0])
        note = wrapped_label(r"most people guess far higher; \ in natural frequencies the answer is easy to see", 11.0,
                             20, GREY_A).move_to([0, -2.8, 0])
        with self.voiceover(
            "Here it is in natural frequencies. <bookmark mark='a'/> Take ten thousand people. A hundred have the "
            "condition, and nine thousand nine hundred don't. <bookmark mark='b'/> Of the hundred, ninety test "
            "positive. <bookmark mark='c'/> Of the nine thousand nine hundred, nine percent, eight hundred and ninety-"
            "one, test positive too. <bookmark mark='d'/> So of nine hundred and eighty-one positives, ninety have "
            "the condition: about nine percent. Most people guess far higher. Counted out like this, the answer is "
            "easy to see, and it's why a screen is never a diagnosis."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(sick), FadeIn(well), Create(lines[0]), Create(lines[1]))
            vo.wait_until("b")
            self.play(FadeIn(tp), FadeIn(fn), Create(lines[2]), Create(lines[3]))
            vo.wait_until("c")
            self.play(FadeIn(fp), FadeIn(tn), Create(lines[4]), Create(lines[5]))
            vo.wait_until("d")
            self.play(FadeIn(ans), Indicate(tp, color=GOOD), Indicate(fp, color=AUTH))
            self.play(FadeIn(note))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 22, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers to write down before the part answers them. <bookmark mark='a'/> One: in a large "
            "American survey, what share of adults had met the criteria for some mental disorder at some point in "
            "their lives? <bookmark mark='b'/> Two: two clinicians diagnose the same patients for major depression. "
            "What's their agreement beyond chance, Cohen's kappa, on a scale from nought to one? "
            "<bookmark mark='c'/> Three: among three thousand seven hundred people diagnosed with depression, how "
            "many different combinations of symptoms were there? <bookmark mark='d'/> And four: across studies "
            "comparing clinicians with simple formulas, in what share did the clinicians clearly win? Pause here, "
            "and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(4.0)
        self.clear_scene()
