from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


def mask_glyph(center, size: float = 1.6) -> VGroup:
    """A pattern mask: overlapping strokes that cover a digit's shape."""
    rng = np.random.default_rng(7)
    c = np.array(center, float)
    g = VGroup()
    for _ in range(26):
        a = c + np.array([rng.uniform(-0.5, 0.5) * size, rng.uniform(-0.6, 0.6) * size, 0])
        b = a + np.array([rng.uniform(-0.45, 0.45) * size, rng.uniform(-0.45, 0.45) * size, 0])
        g.add(Line(a, b, color=WHITE, stroke_width=7))
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.on_you()
        self.story()
        self.question()
        self.objectives()

    def flash(self, digit: str, frames: int):
        c = np.array([0, 0.35, 0])
        d = label(digit, font_size=150, color=WHITE).move_to(c)
        m = mask_glyph(c)
        self.add(d)
        self.wait(frames / config.frame_rate)
        self.remove(d)
        self.add(m)
        self.wait(0.6)
        self.remove(m)

    def on_you(self):
        stage = demo_stage(12.4, 5.4, center=[0, 0.35, 0])
        fix = Cross(scale_factor=0.08, stroke_color=YOU, stroke_width=3).move_to([0, 0.35, 0])
        ask = label(r"A digit, \ then a mask. \ Which digit was it? \ Guess if you must.", font_size=28,
                    color=YOU).to_edge(DOWN, buff=0.75)
        with self.voiceover(
            "Let's start on you. <bookmark mark='a'/> In a moment a digit will flash in the middle of the screen, "
            "for a single frame of this video, about a thirtieth of a second, and then a jumble of lines will cover "
            "it. Watch the cross. Then say which digit it was, and whether you saw it."
        ) as vo:
            self.play(FadeIn(stage), FadeIn(fix))
            vo.wait_until("a")
            self.play(FadeIn(ask))
        self.remove(fix)
        self.flash("7", 1)
        self.add(fix)
        self.wait(2.5)
        with self.voiceover(
            "Did you see it? Many people see nothing but the lines, and when pressed to guess, say seven more often "
            "than chance. <bookmark mark='a'/> Now the same digit, for ten frames."
        ) as vo:
            vo.wait_until("a")
        self.remove(fix)
        self.flash("7", 10)
        self.add(fix)
        note = rows_of([
            (r"the second time you saw a seven; \ the first time, \ perhaps nothing at all", WHITE),
            (r"the same digit, \ the same eyes: \ what changed is whether it reached awareness", SEEN),
        ], 11.6, 25, 0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A seven, both times. <bookmark mark='a'/> The second time you saw it. The first time, perhaps nothing, "
            "though your guess may still have been right. <bookmark mark='b'/> Same digit, same eyes, same brain. "
            "What changed is whether it reached awareness, and that difference is what this part is about."
        ) as vo:
            self.play(FadeOut(ask))
            vo.wait_until("a")
            self.play(FadeIn(note[0]))
            vo.wait_until("b")
            self.play(FadeIn(note[1]))
        self.clear_scene()

    def story(self):
        head = heading(r"Seeing without knowing it")
        items = [
            (r"1973", r"D.\,B., \ after surgery that removed part of his right visual cortex, \ is blind in the left "
                      r"half of his visual field: \ he says he sees nothing there", LOST),
            (r"1974", r"Lawrence Weiskrantz and colleagues ask him to guess: \ where is the light, \ is the line "
                      r"vertical or horizontal? \ he guesses far above chance, \ and is astonished", UNSEEN),
            (r"1986", r"Weiskrantz's book on D.\,B.: \ \emph{blindsight}, \ information the brain uses "
                      r"without the experience of seeing", SEEN),
        ]
        rows = VGroup()
        for yr, txt, c in items:
            rows.add(VGroup(label(yr, font_size=30, color=c), wrapped_label(txt, 10.6, 26, WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=UP))
        for r in rows:
            r[1].shift(RIGHT * (1.4 - r[0].width))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.0, 0])
        tag = historical_tag(r"Weiskrantz, \ Warrington, \ Sanders \& Marshall (1974); \ Weiskrantz (1986)")
        with self.voiceover(
            "The question became an experiment because of one man. <bookmark mark='a'/> D.B. had surgery in 1973 "
            "to remove a malformation at the back of his brain, which took part of his right visual cortex. "
            "Afterwards he was blind in the left half of his field of view. Shown something there, he said he saw "
            "nothing. <bookmark mark='b'/> Lawrence Weiskrantz, Elizabeth Warrington and their colleagues asked him "
            "to guess anyway: where was the light, was the line vertical or horizontal? He guessed far above chance, "
            "and when they showed him his results, he was astonished. <bookmark mark='c'/> Weiskrantz called it "
            "blindsight, and in 1986 wrote a book about D.B.: information the brain uses, without the experience "
            "of seeing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what is the difference between information used and information experienced?")
        rows = rows_of([
            (r"the contrastive method: \ hold the stimulus fixed, \ vary awareness, \ look for what changes", SEEN),
            (r"masking and the criterion problem; \ blindsight, \ and whether it is really unconscious", UNSEEN),
            (r"rivalry, \ and the workspace's ignition, \ computed", GNW),
            (r"integrated information computed for small networks, \ and the theories put to an agreed test", IIT),
            (r"Libet's clock, \ and consciousness lost: \ sleep, \ anaesthesia, \ injury", RPT),
        ], 12.6, 27, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So what is the difference between information the brain uses and information you experience? "
            "<bookmark mark='a'/> We'll start with the method that made the question scientific: hold the stimulus "
            "fixed, vary awareness, and look for what changes. <bookmark mark='b'/> Then masking, the measurement "
            "problem it raises, and blindsight. <bookmark mark='c'/> Then binocular rivalry, and the global "
            "workspace's ignition, computed. <bookmark mark='d'/> Then integrated information, computed for small "
            "networks, and the day the theories agreed in advance on experiments that could embarrass them. "
            "<bookmark mark='e'/> And finally free will on a clock face, and what happens when consciousness is "
            "lost."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 27", font_size=34, color=GREY_B), label(r"Consciousness", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the contrastive method, \ and masking's criterion problem computed",
            r"blindsight, \ and whether it is degraded conscious vision",
            r"binocular rivalry from adaptation and inhibition, \ and the no-report paradigm",
            r"the global workspace's ignition, \ and integrated information computed",
            r"the theories' adversarial test, \ and Libet's clock read as accumulated noise",
            r"losing consciousness: \ sleep, \ anaesthesia, \ covert awareness, \ and the complexity index",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 27 of Psychology, Built, the last part of Act Five, on thinking: consciousness. "
            "<bookmark mark='a'/> We'll compute the criterion problem that haunts every claim of unconscious "
            "perception, and ask whether blindsight is really blind. We'll build binocular rivalry from adaptation "
            "and inhibition, and see how experiments learned to do without reports. We'll compute the workspace's "
            "ignition and a measure of integrated information. We'll look at the adversarial test of the two "
            "leading theories, and read Libet's clock as accumulated noise. And we'll finish with consciousness "
            "lost and found: sleep, anaesthesia, patients who cannot respond, and an index of complexity."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
