from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ evaluating a biomarker claim", r"A start-up says its test predicts "
                     r"which antidepressant will work. \ What do you ask?", scale=("society",))
        self.where()
        self.claim()
        self.questions()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"computational psychiatry labs", r"tasks, \ models and large online and clinical samples", MODEL),
            (r"digital health companies", r"apps, \ sensing and prediction models sold to health systems", PERSON),
            (r"health technology assessment", r"deciding whether a test or device is worth paying for", GOOD),
            (r"regulators", r"clearing devices and software as medical devices", SYMP),
        ], "Where is this a job? <bookmark mark='a'/> In computational psychiatry labs: tasks, models, and large "
           "online and clinical samples. <bookmark mark='b'/> In digital health companies: apps, sensing, and "
           "prediction models sold to health systems. <bookmark mark='c'/> In health technology assessment, which "
           "decides whether a test or device is worth paying for. <bookmark mark='d'/> And at regulators, who clear "
           "devices and software as medical devices.")

    def claim(self):
        stage = demo_stage(12.8, 3.4, tag=r"A made-up press release", center=[0, 0.4, 0])
        text = wrapped_label(r"``Our 20-minute game and an AI model predict which of two antidepressants will work "
                             r"for you, \ with 85\% accuracy, \ in a study of 120 patients.''", 11.6, 26, WHITE)
        text.move_to(stage.box.get_center())
        foot = wrapped_label(r"invented for this exercise; \ no company or product", 12.0, 18, GREY_B)
        foot.next_to(stage, DOWN, buff=0.3)
        with self.voiceover(
            "Here's a claim of the kind you'll meet. It's invented for this exercise, and describes no real company. "
            "<bookmark mark='a'/> Our twenty-minute game and an AI model predict which of two antidepressants will "
            "work for you, with eighty-five percent accuracy, in a study of a hundred and twenty patients. "
            "<bookmark mark='b'/> What do you ask?"
        ) as vo:
            self.play(FadeIn(stage))
            vo.wait_until("a")
            self.play(FadeIn(text))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(2.0)
        self.clear_scene()

    def questions(self):
        rows_section(self, r"Six questions", [
            (r"was the 85\% measured on patients the model never saw, \ from another site? \ (chapter 8)", AUTH),
            (r"were features chosen using all 120 patients? \ (chapter 8's leak)", MODEL),
            (r"what is the game's retest reliability? \ (chapter 6)", PERSON),
            (r"did each patient get both drugs, \ or was the ``right'' drug inferred? \ a choice rule needs an "
             r"interaction, \ and about 1,400 patients to show one (chapter 9)", SYMP),
            (r"compared with what: \ the better drug for everyone, \ or a clinician's choice?", GOOD),
            (r"has a randomized trial of choosing by the test against usual care been registered?", YOU),
        ], "Six questions. <bookmark mark='a'/> Was the eighty-five percent measured on patients the model never saw, "
           "from another site? That's chapter eight. <bookmark mark='b'/> Were the features chosen using all hundred "
           "and twenty patients? That's chapter eight's leak. <bookmark mark='c'/> What's the game's retest "
           "reliability? That's chapter six. <bookmark mark='d'/> Did each patient get both drugs, or was the right "
           "drug inferred? A choice rule needs an interaction, and about fourteen hundred patients to show one. That's "
           "chapter nine. <bookmark mark='e'/> Compared with what: the better drug for everyone, or a clinician's "
           "choice? <bookmark mark='f'/> And has a randomized trial of choosing by the test, against usual care, been "
           "registered?", font_size=21, buff=0.36)
