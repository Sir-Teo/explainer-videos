from __future__ import annotations

from videos.psychology.psych29.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.machines()
        self.policy()
        self.therapy()

    def card(self):
        card = chapter_card(14, r"In practice: \ machines that read faces, \ well-being, \ therapy",
                            r"Where does the science of emotion change what people do?",
                            lit={2011: r"ONS well-being questions", 2019: r"Barrett et al.", 2025: r"EU AI Act"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: machines that read faces, well-being, and therapy."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def machines(self):
        head = heading(r"Emotion recognition by machine")
        rows = rows_of([
            (r"products have claimed to read emotion from faces: \ in job interviews, \ classrooms, \ call "
             r"centres, \ cars", WHITE),
            (r"a camera can measure facial movements reliably; \ the weak step is from a movement to a feeling, "
             r"\ the step chapter three's review found unreliable", FACE),
            (r"HireVue removed facial analysis from its hiring assessments in 2020, \ saying the words people "
             r"used predicted as well without it", COG),
            (r"the EU's AI Act has prohibited emotion recognition in workplaces and schools since February 2025, "
             r"\ except for medical or safety reasons", UNPL),
            (r"what remains defensible: \ detecting movements, \ or states like drowsiness, \ and saying so", PLEAS),
        ], 12.2, 25, 0.38).move_to([0, -0.2, 0])
        tag = published_tag(r"Barrett et al.\ (2019); \ Regulation (EU) 2024/1689, \ Art.\ 5")
        with self.voiceover(
            "The basic-emotion view became a product. <bookmark mark='a'/> Companies have sold software that claims "
            "to read emotion from faces, for job interviews, classrooms, call centres and cars. "
            "<bookmark mark='b'/> A camera can measure facial movements reliably. The weak step is the inference "
            "from a movement to a feeling, the step that chapter three's review found unreliable. "
            "<bookmark mark='c'/> The hiring company HireVue removed facial analysis from its assessments in 2020, "
            "saying that what candidates said predicted as well without it. <bookmark mark='d'/> And since "
            "February 2025 the European Union's AI Act has prohibited emotion recognition in workplaces and "
            "schools, except for medical or safety reasons. <bookmark mark='e'/> What remains defensible is "
            "detecting movements, or physical states like drowsiness in a driver, and calling them that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def policy(self):
        head = heading(r"Measuring well-being for policy")
        qs = VGroup(*[word_chip(t, color=c, font_size=20, width=5.4) for t, c in (
            (r"satisfied with your life nowadays?", COG), (r"what you do is worthwhile?", COG),
            (r"how happy did you feel yesterday?", PLEAS), (r"how anxious did you feel yesterday?", UNPL))])
        qs.arrange(DOWN, buff=0.25).move_to([-3.5, 0.0, 0])
        scale = label(r"each 0 to 10", font_size=20, color=GREY_B).next_to(qs, DOWN, buff=0.25)
        rows = rows_of([
            (r"the UK's Office for National Statistics has asked four questions in its large household survey "
             r"since April 2011", WHITE),
            (r"two evaluate a life; \ two report feelings: \ chapter eleven's two measures, \ kept apart", COG),
            (r"they take about a minute and a half, \ and answers given on the phone run higher than face to "
             r"face: \ the mode of asking is part of the measure \ (Part 3)", UNPL),
            (r"what well-being data are used for: \ comparing places and groups, \ and valuing policies by "
             r"their effect on lives", PLEAS),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Office for National Statistics, \ personal well-being user guide")
        with self.voiceover(
            "Governments now measure feelings. <bookmark mark='a'/> Since April 2011 the United Kingdom's Office "
            "for National Statistics has asked four questions in its large household survey, each answered from "
            "zero to ten. <bookmark mark='b'/> Two evaluate a life: how satisfied you are with it, and whether what "
            "you do is worthwhile. Two report feelings: how happy, and how anxious, you felt yesterday. They are "
            "chapter eleven's two kinds of measure, kept apart. <bookmark mark='c'/> They take about a minute and a "
            "half to ask. And people answering by phone give higher ratings than people interviewed at home, so "
            "the way a question is asked is part of the measure, as Part 3 warned. <bookmark mark='d'/> The data "
            "are used to compare places and groups, and to value policies by what they do to people's lives."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(q) for q in qs], lag_ratio=0.2),
                      FadeIn(scale))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def therapy(self):
        head = heading(r"Regulation, \ taught")
        rows = rows_of([
            (r"cognitive therapies teach chapter nine's reappraisal: \ notice the thought behind a feeling, \ test "
             r"it, \ and try another reading of the event", WHITE),
            (r"chapter seven's appraisal model is the theory underneath: \ change the appraisal, \ and the emotion "
             r"follows", COG),
            (r"suppression is the strategy people reach for first, \ and the one chapter nine found costly", UNPL),
            (r"whether teaching reappraisal makes people better, \ against what control, \ and for how long, \ "
             r"is a question for trials: \ Part 42", PLEAS),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "And regulation is taught. <bookmark mark='a'/> Cognitive therapies teach chapter nine's reappraisal: "
            "notice the thought behind a feeling, test it against the evidence, and try another reading of the "
            "event. <bookmark mark='b'/> Chapter seven's appraisal model is the theory underneath it: change the "
            "appraisal, and the emotion follows. <bookmark mark='c'/> Suppression, holding the feeling in, is often "
            "what people reach for first, and chapter nine found it costly. <bookmark mark='d'/> Whether teaching "
            "reappraisal makes people better, compared with what, and for how long, is a question for clinical "
            "trials, and Part 42 asks it."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
