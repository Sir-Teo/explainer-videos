from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403

FORKS = [
    (r"slice-timing correction", r"on or off", 2),
    (r"motion correction", r"two algorithms", 2),
    (r"motion regressors", r"none, \ 6 or 24", 3),
    (r"scrubbing high-motion scans", r"yes or no", 2),
    (r"registration template", r"two templates", 2),
    (r"smoothing", r"4, \ 6 or 8 mm", 3),
    (r"haemodynamic response", r"canonical, \ or with derivatives", 2),
    (r"high-pass filter", r"two cut-offs", 2),
    (r"threshold", r"four rules", 4),
    (r"software package", r"three packages", 3),
]

QUESTIONS = [
    (r"1", r"72 defensible pipelines run on one dataset: \ how many different maps?", PERSON),
    (r"2", r"Pure noise, \ 1,000 voxels: \ choose the 50 best voxels using all the data, \ then cross-validate a "
           r"decoder. \ What accuracy?", MODEL),
    (r"3", r"A true brain-behaviour correlation of 0.1, \ studied with 25 people: \ among the significant results, "
           r"\ what is the average reported $|r|$?", AUTH),
    (r"4", r"How many people for 80\% power to detect $r = 0.1$?", GOOD),
]


class Predict(VoiceoverScene):
    def construct(self):
        self.card()
        self.forks()
        self.quiz()

    def card(self):
        card = chapter_card(1, r"On you: \ count the forks, \ and four numbers", r"How many ways are there to "
                            r"analyse one scan?", lit=(), part=PART, scale=("brain",), marr=("how",))
        with self.voiceover("Chapter one. On you: count the forks, and four numbers."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def forks(self):
        stage = demo_stage(13.2, 6.2, center=[0, -0.2, 0])
        rows = VGroup()
        for name, opts, k in FORKS:
            rows.add(VGroup(label(name, font_size=20, color=WHITE), label(opts, font_size=17, color=GREY_A),
                            label(rf"$\times {k}$", font_size=22, color=THRESH)))
        for r in rows:
            r[0].move_to([-4.4, 0, 0], aligned_edge=LEFT)
            r[1].move_to([-0.6, 0, 0], aligned_edge=LEFT)
            r[2].move_to([3.6, 0, 0])
        rows.arrange(DOWN, buff=0.17).move_to([-0.6, 0.05, 0])
        for r in rows:
            r[0].align_to(rows, LEFT)
        total = int(np.prod([k for _, _, k in FORKS]))
        ans = label(rf"$= {num(total)}$ \ pipelines", font_size=34, color=THRESH).move_to([4.3, -2.6, 0])
        note = wrapped_label(r"Carp, \ 2012: \ one dataset, \ thousands of pipelines, \ and maps that differed in where "
                             r"and whether effects appeared", 7.6, 18, GREY_A).move_to([-2.4, -2.75, 0])
        tag = published_tag(r"Carp (2012)")
        with self.voiceover(
            "First, count the forks yourself. <bookmark mark='a'/> Here are ten ordinary choices in analysing one "
            "brain scan, each with two to four defensible options: slice timing, motion correction, motion "
            "regressors, scrubbing, the template, smoothing, the response model, the filter, the threshold and the "
            "software. <bookmark mark='b'/> Multiply them. <bookmark mark='c'/> Six thousand nine hundred and twelve "
            "pipelines. In 2012 Joshua Carp ran thousands of pipelines like these on one dataset, and the maps "
            "differed in where, and whether, effects appeared. On the course site you can make each choice yourself "
            "and watch the map change."
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.4), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Indicate(r[2], color=THRESH) for r in rows], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(ans, scale=1.2), FadeIn(note), FadeIn(tag))
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
            "Now four numbers. <bookmark mark='a'/> One: seventy-two defensible pipelines run on one dataset. How "
            "many different maps come out? <bookmark mark='b'/> Two: pure noise, a thousand voxels. Choose the fifty "
            "best voxels using all the data, then cross-validate a decoder. What accuracy does it report? "
            "<bookmark mark='c'/> Three: a true brain-behaviour correlation of zero point one, studied with twenty-five "
            "people. Among the significant results, what's the average correlation reported? <bookmark mark='d'/> "
            "And four: how many people does it take to have eighty percent power for a correlation of zero point "
            "one? Pause here, and write them down."
        ) as vo:
            self.play(FadeIn(stage))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.wait(1.0)
        self.clear_scene()
