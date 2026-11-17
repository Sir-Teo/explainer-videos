from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403

QUESTIONS = [
    (r"1", r"Delete a word: \ a keyboard shortcut, \ or the mouse and a menu. \ How much slower is the menu route?",
     PERSON),
    (r"2", r"A test with five users: \ what share of an interface's usability problems does it find?", AUTH),
    (r"3", r"Bar lengths or pie-slice angles: \ how much larger is the typical error when reading angles?", MODEL),
    (r"4", r"How many days does it take to form a new daily habit?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        card_section(self, 1, r"On you: \ point and click, \ and four numbers", r"How fast can you hit a target?")
        self.pointing()
        self.quiz()

    def pointing(self):
        stage = demo_stage(13.2, 6.0, center=[0, -0.3, 0])
        rng = np.random.default_rng(52)
        targets = VGroup()
        for k, (x, y, w) in enumerate([(-4.5, 1.0, 0.25), (-1.0, -1.6, 0.6), (-4.0, -1.8, 0.4), (-0.8, 1.1, 0.18)]):
            targets.add(Circle(w, color=PERSON, fill_opacity=0.35, stroke_width=3).move_to([x, y, 0]))
        start = Dot([-2.6, -0.3, 0], radius=0.09, color=WHITE)
        arrows = VGroup(*[Arrow(start.get_center(), t.get_center(), buff=0.12, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.08) for t in targets])
        rows = rows_of([
            (r"on the course site: \ targets of four sizes at four distances; \ click each as fast as you can", WHITE),
            (r"the page fits your own line: \ time against the index of difficulty, \ $\log_2(D/W + 1)$ bits", MODEL),
            (r"and your throughput in bits per second, \ from where your clicks actually landed", PERSON),
            (r"nothing is stored or sent", YOU),
        ], 5.8, 21, 0.4).move_to([3.3, -0.3, 0])
        with self.voiceover(
            "First, your own hand. <bookmark mark='a'/> On the course site, targets of four sizes appear at four "
            "distances, and you click each as fast as you can. <bookmark mark='b'/> The page fits your own line: time "
            "against the index of difficulty, in bits. <bookmark mark='c'/> And it gives your throughput in bits per "
            "second, from where your clicks actually landed. <bookmark mark='d'/> Nothing is stored or sent."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(start))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(t, scale=0.6) for t in targets], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3))
            for m, r in zip("cd", rows[2:]):
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
            "Now four numbers. <bookmark mark='a'/> One: to delete a word, you can use a keyboard shortcut, or the "
            "mouse and a menu. How much slower is the menu route? <bookmark mark='b'/> Two: a usability test with five "
            "users. What share of an interface's problems does it find? <bookmark mark='c'/> Three: reading bar "
            "lengths or pie-slice angles. How much larger is the typical error with angles? <bookmark mark='d'/> And "
            "four: how many days does it take to form a new daily habit? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
