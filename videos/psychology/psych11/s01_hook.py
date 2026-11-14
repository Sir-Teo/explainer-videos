from __future__ import annotations

import numpy as np

from videos.psychology.psych11.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.morning()
        self.objection()
        self.patches()
        self.objectives()

    def morning(self):
        f = archive.FECHNER_1860.data
        head = heading(r"Leipzig, \ 22 October 1850")
        bed = VGroup(RoundedRectangle(width=4.2, height=0.5, corner_radius=0.12, color=GREY_B, stroke_width=3,
                                      fill_color=GREY_D, fill_opacity=0.4),
                     Rectangle(width=0.25, height=1.2, stroke_width=0, fill_color=GREY_B, fill_opacity=0.8))
        bed[1].next_to(bed[0], LEFT, buff=0).align_to(bed[0], DOWN)
        sleeper = VGroup(Circle(radius=0.28, color=FECHC, fill_color=FECHC, fill_opacity=0.9),
                         RoundedRectangle(width=2.8, height=0.42, corner_radius=0.2, stroke_width=0, fill_color=FECHC,
                                          fill_opacity=0.6))
        sleeper.arrange(RIGHT, buff=0.08).next_to(bed[0], UP, buff=0.02)
        scene = VGroup(bed, sleeper).scale(1.25).move_to([-3.7, -0.6, 0])
        thought = VGroup(*[Circle(radius=r, color=GREY_B, stroke_width=2).move_to(sleeper[0].get_center() + np.array([x, y, 0]))
                           for r, x, y in ((0.07, 0.3, 0.45), (0.11, 0.55, 0.85))])
        idea = MathTex(r"\text{equal ratios} \;\to\; \text{equal steps}", font_size=34, color=FECHC)
        cloud = RoundedRectangle(width=idea.width + 0.8, height=1.1, corner_radius=0.5, color=GREY_B, stroke_width=2)
        cloud.move_to(sleeper[0].get_center() + np.array([0.4 + cloud.width / 2, 1.9, 0]))
        idea.move_to(cloud)
        name = label(r"Gustav Theodor Fechner, \ 49", font_size=30, color=FECHC).next_to(scene, DOWN, buff=0.35)
        rows = rows_of([
            (r"a physicist, \ worn out by years of illness", WHITE),
            (r"his question: \ how are the body and the mind related?", WHITE),
            (r"his answer that morning: \ by a law that can be measured", THRESH),
            (rf"ten years of experiments later, \ the \emph{{Elements of Psychophysics}}, \ in {f['volumes']} volumes "
             rf"({f['year']})", FECHC),
        ], 5.6, 30, 0.34).move_to([3.7, 0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.FECHNER_1860.cite)
        tag = note(r"the date and the bed: \ Fechner's own account, \ as histories tell it").to_corner(DR, buff=0.3)
        with self.voiceover(
            "On the morning of the twenty-second of October, 1850, a professor in Leipzig was lying in "
            "bed, thinking. Gustav Theodor Fechner was forty-nine. He had been a physicist, and a good "
            "one, until years of illness had worn him out. <bookmark mark='a'/> The question he was "
            "turning over was an old one: how are the body and the mind related? <bookmark mark='b'/> "
            "That morning, by his own account, he saw how to answer it, and the answer was a law that "
            "could be measured. If the stimulus grows by equal ratios, the sensation grows by equal "
            "steps. <bookmark mark='c'/> He spent the next ten years on experiments, and in 1860 "
            "published them in two volumes, the Elements of Psychophysics. Psychophysicists still mark "
            "the twenty-second of October as Fechner Day."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(scene), FadeIn(name), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]), FadeIn(thought, lag_ratio=0.5))
            vo.wait_until("b")
            self.play(Create(cloud), Write(idea), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def objection(self):
        board = wager_board((
            (r"so far: \ times, \ correlations, \ models of cells, \ brains and clocks. \ But no sensation has been "
             r"measured", STATUS_COLOR["contested"]),
            (r"experiments by the dozen: \ assignment by lot, \ lesions, \ twins, \ a cave", STATUS_COLOR["replicated"]),
            (r"instruments that do not ask: \ timers, \ scanners, \ a stopwatch on a sleepy mind", STATUS_COLOR["replicated"]),
        ))
        hl = SurroundingRectangle(board.rows[0], color=KANT, buff=0.15, corner_radius=0.1)
        q = wrapped_label(r"This act's question: \ can anything in the mind be measured?", 12.0,
                          31, THRESH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This is the morning Part 1 promised. Kant's first objection was that the mind admits no "
            "mathematics: a thought has no length and no weight, so there is nothing to put a number on. "
            "Ten parts have timed the mind, correlated it and modelled its machinery, and still not one "
            "sensation has been measured. "
            "<bookmark mark='a'/> Fechner's reply was not to put a ruler to a sensation. It was to "
            "measure the stimulus, and count how many just noticeable steps lie between two stimuli. "
            "<bookmark mark='b'/> This part asks whether that works. And it begins, as Fechner did, with "
            "the smallest difference a person can notice."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r.objection) for r in board.rows], *[FadeIn(r.reply) for r in board.rows])
            vo.wait_until("a")
            self.play(Create(hl))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
        self.clear_scene()

    def patches(self):
        head = heading(r"Which is brighter?")
        easy = patch_pair(100, 124, size=2.0).move_to([-3.4, 0.6, 0])
        hard = patch_pair(102, 100, size=2.0).move_to([3.4, 0.6, 0])
        le = label(r"a difference of 24\%", font_size=30, color=GREY_A).next_to(easy, DOWN, buff=0.3)
        lh = label(r"a difference of 2\%", font_size=30, color=GREY_A).next_to(hard, DOWN, buff=0.3)
        rows = rows_of([
            (r"at 24\%, \ nobody hesitates; \ at 2\%, \ most people are guessing", WHITE),
            (r"somewhere between, \ a difference becomes just noticeable. \ Where, \ and does it follow a law?", THRESH),
        ], 12.4, 31, 0.25).to_edge(DOWN, buff=0.7)
        tag = note(r"your screen and the video change the greys: \ a demonstration, \ not a measurement").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Here are two grey patches. Which is brighter? <bookmark mark='a'/> Easy: the right one, by "
            "twenty-four percent. <bookmark mark='b'/> And these two? The left one, by two percent, and "
            "most people looking at a video are guessing. Your screen and the video's compression change "
            "the greys, so this is a demonstration and not a measurement. <bookmark mark='c'/> Somewhere "
            "between those two differences, a difference becomes just noticeable. Where is that, and does "
            "it follow a law? By chapter five you'll have measured your own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(easy[0]))
            vo.wait_until("a")
            self.play(FadeIn(easy[1]), FadeIn(le))
            vo.wait_until("b")
            self.play(FadeIn(hard), FadeIn(lh), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1], shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 11", font_size=34, color=GREY_B), label(r"The Threshold", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Weber's fraction, \ and Fechner's step from a fraction to a scale",
            r"the classical methods, \ and why a threshold is a curve and not a point",
            r"a threshold of your own, \ fitted by maximum likelihood, \ with an interval",
            r"staircases and a Bayesian rule: \ how to measure a threshold fast",
            r"Stevens's numbers, \ and the quarrel between a logarithm and a power",
            r"where Weber's law comes from, \ and where else it holds",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part eleven: the threshold, and the first act of the series on the senses. "
            "<bookmark mark='a'/> We'll start with Weber's fraction, and Fechner's step from a fraction to "
            "a scale. <bookmark mark='b'/> We'll run the classical methods, and see why a threshold is a "
            "curve and not a point. <bookmark mark='c'/> You'll measure a threshold of your own, and we'll "
            "fit it by maximum likelihood, with an interval. <bookmark mark='d'/> We'll see how a staircase "
            "and a Bayesian rule measure a threshold fast. <bookmark mark='e'/> Then Stevens asks people for "
            "numbers, and a logarithm quarrels with a power. <bookmark mark='f'/> And we'll ask where "
            "Weber's law comes from, and where else it holds."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
