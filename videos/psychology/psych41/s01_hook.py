from __future__ import annotations

from videos.psychology.psych41.common import *  # noqa: F403


def depth_profile(sign: float, color, width: float = 3.2, depth: float = 0.9) -> VMobject:
    """A face's depth seen from above, with the viewer below: the middle (the nose) recedes from the viewer for a
    hollow mask (sign +1) and comes toward the viewer for a face that bulges out (sign -1)."""
    xs = np.linspace(-width / 2, width / 2, 80)
    pts = [[x, sign * depth * np.cos(np.pi * x / width) ** 2, 0] for x in xs]
    return VMobject(color=color, stroke_width=5).set_points_smoothly(pts)


class Hook(VoiceoverScene):
    def construct(self):
        self.care()
        self.mask()
        self.patients()
        self.question()
        self.objectives()

    def care(self):
        card = care_card().move_to([0, 0, 0])
        with self.voiceover(
            "Before we start. This part is about psychosis, addiction and conditions of development. "
            "<bookmark mark='a'/> It's education, not diagnosis or treatment. If any of it touches your own life, "
            "talk to a doctor, a counsellor, or someone you trust. <bookmark mark='b'/> If you're in danger now, call "
            "your local emergency number. In the United States you can call or text nine eight eight. In the UK and "
            "Ireland, Samaritans are on one one six, one two three. And find a helpline dot com lists free, "
            "confidential lines in other countries."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.head))
            vo.wait_until("a")
            self.play(FadeIn(card.body))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.6), run_time=3.0)
        self.wait(1.5)
        self.clear_scene()

    def mask(self):
        head = heading(r"The face that is not there")
        eye = VGroup(Circle(radius=0.22, color=WHITE), Dot(radius=0.08, color=WHITE)).move_to([-4.2, -2.4, 0])
        eye_l = label(r"you", font_size=18, color=YOU).next_to(eye, DOWN, buff=0.12)
        truth = depth_profile(+1, AUTH).move_to([-4.2, 0.2, 0])
        t_l = label(r"the mask from above: \ hollow", font_size=17, color=AUTH).next_to(truth, UP, buff=0.3)
        seen = depth_profile(-1, GOOD).move_to([-4.2, 0.2, 0])
        s_l = label(r"what you see: \ a face bulging out", font_size=17, color=GOOD).next_to(truth, UP, buff=0.3)
        rays = VGroup(*[DashedLine(eye.get_top(), [x, 0.0, 0], color=GREY_C, stroke_width=1.5)
                        for x in (-5.4, -4.2, -3.0)])
        rows = rows_of([
            (r"turn a mask of a face around and look into its hollow back: \ almost everyone sees a normal face, \ "
             r"bulging toward them", WHITE),
            (r"both eyes say hollow; \ shading says hollow if lit from the right side; \ the brain overrules them", SYMP),
            (r"Part 14's inference: \ a prior that faces bulge outward, \ strong enough to beat the senses", MODEL),
        ], 7.2, 21, 0.4).move_to([2.6, -0.2, 0])
        tag = historical_tag(r"Gregory (1970)")
        with self.voiceover(
            "Take a mask of a face, turn it around, and look into its hollow back. <bookmark mark='a'/> Almost "
            "everyone sees a normal face, bulging toward them, and it seems to follow them as they move. "
            "<bookmark mark='b'/> Both eyes report a hollow. The shading, lit from the right side, does too. The brain "
            "overrules them. <bookmark mark='c'/> It's Part 14's inference, in its starkest form. A prior that faces "
            "bulge outward, strong enough to beat the evidence of the senses. The psychologist Richard Gregory made "
            "it a favourite demonstration of perception as hypothesis."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eye), FadeIn(eye_l), Create(truth), FadeIn(t_l),
                      FadeIn(rays))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Transform(truth, seen), Transform(t_l, s_l), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def patients(self):
        head = heading(r"Not everyone is fooled")
        fooled = VGroup(*[little_person(0.42, color=GOOD) for _ in range(10)]).arrange(RIGHT, buff=0.12)
        notf = VGroup(*[little_person(0.42, color=AUTH if i < 5 else GOOD) for i in range(10)]).arrange(RIGHT,
                                                                                                         buff=0.12)
        g1 = VGroup(label(r"most people", font_size=18, color=GREY_A), fooled).arrange(DOWN, buff=0.15)
        g2 = VGroup(label(r"many people with schizophrenia", font_size=18, color=GREY_A), notf).arrange(DOWN, buff=0.15)
        VGroup(g1, g2).arrange(DOWN, buff=0.5).move_to([-3.6, 0.0, 0])
        key = VGroup(VGroup(Dot(color=GOOD), label(r"sees a face", font_size=15, color=GOOD)).arrange(RIGHT, buff=0.1),
                     VGroup(Dot(color=AUTH), label(r"sees the hollow", font_size=15, color=AUTH)).arrange(RIGHT,
                                                                                                       buff=0.1))
        key.arrange(RIGHT, buff=0.5).next_to(g2, DOWN, buff=0.35)
        sch = label(r"schematic", font_size=13, color=GREY_B).next_to(key, DOWN, buff=0.15)
        rows = rows_of([
            (r"in small studies since 1989, \ people with schizophrenia saw the hollow mask as hollow more often", WHITE),
            (r"they were, \ in this one respect, \ more accurate than everyone else", SYMP),
            (r"one reading: \ the priors that shape perception are weighted differently", MODEL),
            (r"yet hallucinations seem to need priors that are too strong: \ the puzzle runs through the part", YOU),
        ], 6.0, 20, 0.38).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Emrich (1989); \ Dima et al.\ (2009)")
        with self.voiceover(
            "But not everyone is fooled. <bookmark mark='a'/> In small studies since 1989, people with schizophrenia "
            "saw the hollow mask as hollow more often than other people did. <bookmark mark='b'/> In this one "
            "respect, they were more accurate than everyone else. <bookmark mark='c'/> One reading is that the priors "
            "that shape perception are weighted differently. <bookmark mark='d'/> Yet hallucinations, hearing a voice "
            "no one else hears, seem to need priors that are too strong. That puzzle runs through this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g1), FadeIn(g2), FadeIn(key), FadeIn(sch))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ inference and learning, \ set wrongly")
        rows = rows_of([
            (r"psychosis: \ dopamine, \ salience, \ and perception and belief with mis-weighted priors", SYMP),
            (r"addiction: \ a learning system captured by a drug", MODEL),
            (r"autism and ADHD: \ brains that develop along a different path", PERSON),
            (r"and the same few parameters across the diagnoses", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part uses the series' own models as a language for three kinds of condition. "
            "<bookmark mark='a'/> Psychosis: dopamine, salience, and perception and belief with priors weighted "
            "wrongly. <bookmark mark='b'/> Addiction: a learning system captured by a drug. <bookmark mark='c'/> And "
            "autism and ADHD: brains that develop along a different path. <bookmark mark='d'/> At the end, the same "
            "few parameters turn up across the diagnoses."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 41", font_size=34, color=GREY_B),
                      label(r"Psychosis, \ Addiction and Development", font_size=50))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"schizophrenia: \ symptoms, \ course and the dopamine story",
            r"aberrant salience, \ and hallucination as inference",
            r"causes: \ many genes, \ some environments, \ and a theory that did harm",
            r"addiction as reward learning captured by a drug, \ computed",
            r"environment, \ recovery, \ and a treatment built on conditioning",
            r"autism and ADHD: \ histories, \ myths, \ models and evidence",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 41 of Psychology, Built: psychosis, addiction and development. <bookmark mark='a'/> We'll "
            "meet schizophrenia, its course, and the dopamine story. We'll model aberrant salience, and hallucination "
            "as inference. We'll weigh the causes: many genes, some environments, and a theory that did harm. We'll "
            "compute addiction as reward learning captured by a drug, and look at environment, recovery and a "
            "treatment built on conditioning. And we'll take autism and ADHD through their histories, myths, models "
            "and evidence."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
