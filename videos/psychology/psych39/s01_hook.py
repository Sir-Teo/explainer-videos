from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.care()
        self.pseudopatients()
        self.doubts()
        self.question()
        self.objectives()

    def care(self):
        card = care_card().move_to([0, 0, 0])
        with self.voiceover(
            "Before we start. This part and the next three are about suffering: anxiety, depression, psychosis, "
            "addiction. <bookmark mark='a'/> They're education, not diagnosis or treatment. If any of it touches your "
            "own life, talk to a doctor, a counsellor, or someone you trust. <bookmark mark='b'/> If you're in danger "
            "now, call your local emergency number. In the United States you can call or text nine eight eight. In "
            "the UK and Ireland, Samaritans are on one one six, one two three. And find a helpline dot com lists free, "
            "confidential lines in other countries."
        ) as vo:
            self.play(FadeIn(card.box), FadeIn(card.head))
            vo.wait_until("a")
            self.play(FadeIn(card.body))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=0.6), run_time=3.0)
        self.wait(1.5)
        self.clear_scene()

    def pseudopatients(self):
        head = heading(r"Sane in insane places")
        people = VGroup(*[little_person(0.7, color=PERSON) for _ in range(8)]).arrange(RIGHT, buff=0.25)
        people.move_to([-3.2, 1.3, 0])
        doors = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.42, height=0.62, stroke_color=GREY_B,
                                          fill_color="#14181F", fill_opacity=1) for _ in range(12)])
        doors.arrange(RIGHT, buff=0.12).move_to([-3.2, -0.4, 0])
        ld = label(r"12 hospitals, \ five states", font_size=16, color=GREY_A).next_to(doors, DOWN, buff=0.2)
        rows = rows_of([
            (r"Rosenhan, \ \emph{Science}, \ 1973: \ eight people with no psychiatric history each asked for "
             r"admission to a psychiatric hospital, \ saying they heard a voice that said ``empty'', \ ``hollow'', \ "
             r"``thud''", WHITE),
            (r"once admitted, \ they stopped the act and behaved normally", SYMP),
            (r"none was detected by staff; \ most were discharged with schizophrenia ``in remission''", AUTH),
            (r"the conclusion: \ psychiatric diagnosis could not tell the sane from the insane", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = historical_tag(r"Rosenhan (1973)")
        with self.voiceover(
            "In 1973 the journal Science published a study that shook psychiatry. <bookmark mark='a'/> David "
            "Rosenhan reported that eight people with no psychiatric history had each asked for admission to a "
            "psychiatric hospital, saying they heard a voice. It said empty, hollow, thud. <bookmark mark='b'/> Once "
            "admitted, they dropped the act and behaved normally. <bookmark mark='c'/> According to the paper, no "
            "staff member detected them, and most were discharged with a diagnosis of schizophrenia in remission. "
            "<bookmark mark='d'/> The conclusion: psychiatric diagnosis couldn't tell the sane from the insane."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(doors), FadeIn(ld))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(p, shift=DOWN * 0.1) for p in people], lag_ratio=0.15))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def doubts(self):
        head = heading(r"What the archive showed")
        rows = rows_of([
            (r"the paper helped force a revolution: \ in 1980 the third edition of the diagnostic manual, \ "
             r"DSM-III, \ replaced descriptions with explicit criteria, \ checked for agreement between clinicians",
             SYMP),
            (r"Cahalan, \ 2019: \ the journalist Susannah Cahalan went looking for the eight; \ she could identify "
             r"only two besides Rosenhan", WHITE),
            (r"one, \ who had a good experience in hospital, \ had been left out of the paper; \ details in "
             r"Rosenhan's notes did not match what he published", AUTH),
            (r"the study's data are in serious doubt; \ the problem it pointed to, \ unreliable diagnosis, \ was "
             r"real, \ and this part measures it", YOU),
        ], 12.4, 21, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Cahalan, \ \emph{The Great Pretender} (2019)")
        with self.voiceover(
            "It changed the field. <bookmark mark='a'/> In 1980 the third edition of the diagnostic manual, "
            "DSM-III, replaced loose descriptions with explicit criteria, checked for agreement between clinicians. "
            "<bookmark mark='b'/> Decades later the journalist Susannah Cahalan went looking for the eight. Besides "
            "Rosenhan himself, she could identify only two. <bookmark mark='c'/> One of them, who'd had a good "
            "experience in hospital, had been left out of the paper. And details in Rosenhan's notes didn't match "
            "what he published. <bookmark mark='d'/> The study's data are now in serious doubt. But the problem it "
            "pointed to, unreliable diagnosis, was real, and this part measures it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what is a disorder?")
        rows = rows_of([
            (r"where the line between suffering and illness has been drawn, \ and by whom", PERSON),
            (r"how far two clinicians agree, \ and why agreement is not enough", SYMP),
            (r"categories or dimensions, \ one factor or many, \ and symptoms that hold each other in place", MODEL),
            (r"how common disorders are, \ what a positive screen means, \ and why formulas beat experts", GOOD),
        ], 12.4, 27, 0.48).move_to([0, -0.2, 0])
        with self.voiceover(
            "So this part asks what a disorder is. <bookmark mark='a'/> Where the line between suffering and illness "
            "has been drawn, and by whom. <bookmark mark='b'/> How far two clinicians agree, and why agreement isn't "
            "enough. <bookmark mark='c'/> Whether disorders are categories or dimensions, one factor or many, and "
            "how symptoms can hold each other in place. <bookmark mark='d'/> And how common disorders are, what a "
            "positive screen means, and why simple formulas beat experts."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 39", font_size=34, color=GREY_B), label(r"What Is a Disorder?", font_size=56))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"a short history of madness and its manuals",
            r"what makes something a disorder: \ distress, \ dysfunction, \ harm",
            r"reliability: \ Cohen's kappa, \ and why reliable is not valid",
            r"categories, \ dimensions, \ the p factor and symptom networks",
            r"prevalence, \ the treatment gap and a positive screen",
            r"clinical against statistical prediction, \ and culture",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 39 of Psychology, Built: what is a disorder?, the first part of Act Ten, when minds suffer. "
            "<bookmark mark='a'/> We'll take a short history of madness and its manuals. We'll ask what makes "
            "something a disorder. We'll derive Cohen's kappa, and see why a reliable diagnosis can still be invalid. "
            "We'll compare categories and dimensions, meet the p factor, and build a network of symptoms. We'll count "
            "how common disorders are, and work out what a positive screen means. And we'll end with clinical "
            "against statistical prediction, and with culture."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=20.0)
        self.clear_scene()
