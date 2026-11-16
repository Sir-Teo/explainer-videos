from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Among people already hired, \ a test that truly correlates 0.5 with performance: \ what correlation "
           r"will you observe?", PERSON),
    (r"2", r"The best single hiring method in the 2022 review: \ which, \ and how valid?", MODEL),
    (r"3", r"Hire the top 20\% on a test of validity 0.3; \ half of all applicants would succeed. \ What share of "
           r"hires succeed?", AUTH),
    (r"4", r"A daycare centre fines parents for picking up late. \ What happens to late pick-ups?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ two candidates, \ and four numbers", r"Whom would you hire?")
        self.choice()
        self.quiz()

    def choice(self):
        d = load("hire")
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        cards = VGroup()
        for name, test, impr, col in ((r"Candidate A", r"test score: \ well above B", r"interview: \ polite, \ a bit "
                                                                                     r"flat", MODEL),
                                      (r"Candidate B", r"test score: \ well below A", r"interview: \ warm, \ "
                                                                                     r"confident, \ memorable", PERSON)):
            box = RoundedRectangle(width=4.6, height=2.0, corner_radius=0.15, color=col, fill_opacity=0.12)
            txt = VGroup(label(name, font_size=26, color=col), label(test, font_size=19), label(impr, font_size=19))
            txt.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(box)
            cards.add(VGroup(box, txt))
        cards.arrange(RIGHT, buff=0.8).move_to([0, 0.9, 0])
        rows = rows_of([
            (r"most people lean towards B: \ the interview felt like evidence", WHITE),
            (rf"in Psyche's world, \ among {d['pairs']:,} such pairs, \ A performed better {100 * d['test_wins']:.0f}\% "
             rf"of the time", MODEL),
            (r"not a sure thing: \ even the better predictor leaves most of performance unexplained; \ that is the "
             r"honest size of this part's numbers", YOU),
        ], 12.0, 21, 0.34).move_to([0, -1.8, 0])
        tag = psyche_tag(r"1{,}000 simulated pairs; \ test validity 0.31, \ unstructured interview 0.19")
        with self.voiceover(
            "First, a choice. <bookmark mark='a'/> Two candidates. A has the much better test score and a polite, "
            "rather flat interview. B has the much lower score and a warm, confident, memorable interview. Whom do "
            "you hire? <bookmark mark='b'/> Most people lean towards B. The interview felt like evidence. "
            "<bookmark mark='c'/> In Psyche's world, with the validities this part will defend, A performed better in "
            "fifty-seven percent of a thousand such pairs. <bookmark mark='d'/> Not a sure thing. Even the better "
            "predictor leaves most of performance unexplained. That's the honest size of this part's numbers."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in cards], lag_ratio=0.4))
            for m, r in zip("bcd", rows):
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
            "Now four numbers. <bookmark mark='a'/> One: a test that truly correlates zero point five with job "
            "performance. Among the people already hired with it, what correlation will you observe? "
            "<bookmark mark='b'/> Two: in the 2022 review of hiring methods, which single method came out best, and "
            "how valid was it? <bookmark mark='c'/> Three: you hire the top fifth on a test of validity zero point "
            "three, where half of all applicants would succeed. What share of your hires succeed? "
            "<bookmark mark='d'/> And four: a daycare centre starts fining parents who pick up their children late. "
            "What happens to late pick-ups? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
