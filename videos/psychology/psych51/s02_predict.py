from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"A two-hour watch for a rare signal: \ what share of signals is detected in the last half hour, \ against "
           r"about 73\% in the first?", PERSON),
    (r"2", r"Targets present in 1 bag in 100 instead of 1 in 2: \ how does the miss rate change?", AUTH),
    (r"3", r"Automation that fails once in 10,000 demands, \ against once in 10: \ what share of takeovers finish "
           r"within 7 seconds?", MODEL),
    (r"4", r"Hours awake that impair performance like a blood alcohol of 0.05\%?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ watch the clock, \ and four numbers", r"How long can you watch for something "
                     r"rare?")
        self.clock()
        self.quiz()

    def clock(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        face = Circle(1.6, color=GREY_B, stroke_width=3).move_to([-3.6, -0.2, 0])
        ticks = VGroup(*[Line(face.get_center() + 1.45 * np.array([np.cos(a), np.sin(a), 0]),
                              face.get_center() + 1.6 * np.array([np.cos(a), np.sin(a), 0]), color=GREY_B)
                         for a in np.linspace(0, 2 * np.pi, 101)[:-1]])
        hand = Line(face.get_center(), face.get_center() + [0, 1.35, 0], color=PERSON, stroke_width=5)
        rows = rows_of([
            (r"1948: \ Norman Mackworth's clock: \ a pointer jumps one step every second", WHITE),
            (r"now and then it jumps two steps: \ the signal; \ press when you see one", PERSON),
            (r"RAF radar operators watched it for two hours; \ detections fell within the first half hour", AUTH),
            (r"on the course site: \ watch it yourself for ninety seconds; \ your record stays in your browser", YOU),
        ], 6.2, 21, 0.4).move_to([2.8, -0.2, 0])
        tag = published_tag(r"Mackworth (1948)")
        with self.voiceover(
            "First, a watch of your own. <bookmark mark='a'/> In 1948 Norman Mackworth built a clock whose pointer "
            "jumps one step every second. <bookmark mark='b'/> Now and then it jumps two steps. That's the signal, and "
            "the watcher presses a key. <bookmark mark='c'/> Radar operators watched it for two hours, and their "
            "detections fell within the first half hour. <bookmark mark='d'/> On the course site you can watch it "
            "yourself for ninety seconds. Your record stays in your browser."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(face), FadeIn(ticks), FadeIn(hand), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for k in range(3):
                self.play(Rotate(hand, -2 * np.pi / 100, about_point=face.get_center()), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Rotate(hand, -4 * np.pi / 100, about_point=face.get_center()), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def quiz(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rows = VGroup()
        for n, q, c in QUESTIONS:
            rows.add(VGroup(label(n, font_size=34, color=c), wrapped_label(q, 9.4, 21, WHITE),
                            label(r"\underline{\hspace{1.2cm}}", font_size=26, color=YOU)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.3, 0])
        with self.voiceover(
            "Now four numbers. <bookmark mark='a'/> One: in a two-hour watch for a rare signal, about seventy-three "
            "percent of signals are caught in the first half hour. What share in the last? <bookmark mark='b'/> Two: "
            "targets present in one bag in a hundred instead of one in two. How does the miss rate change? "
            "<bookmark mark='c'/> Three: automation that fails once in ten thousand demands, against once in ten. What "
            "share of human takeovers finish within seven seconds? <bookmark mark='d'/> And four: how many hours "
            "awake impair performance like a blood alcohol of zero point zero five percent? Pause here, and write them "
            "down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
