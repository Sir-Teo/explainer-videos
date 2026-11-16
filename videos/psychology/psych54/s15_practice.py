from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ a course's study plan, \ redesigned", r"What would you change in a "
                     r"course tomorrow?", scale=("person", "society"))
        self.where()
        self.plan()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"course design", r"curricula with cumulative review, \ and assessments that ask for retrieval and "
                               r"application", MODEL),
            (r"edtech", r"flashcard and tutoring products: \ their schedulers and student models are this part's "
                        r"mathematics", PERSON),
            (r"corporate training", r"a one-day workshop is massed practice; \ spacing it costs little and keeps more",
             SYMP),
            (r"evaluation", r"randomized trials of products and programmes, \ judged by later learning, \ not by "
                            r"satisfaction", GOOD),
        ], "Where is this a job? <bookmark mark='a'/> In course design: curricula with cumulative review, and "
           "assessments that ask for retrieval and application. <bookmark mark='b'/> In educational technology: "
           "flashcard and tutoring products, whose schedulers and student models are this part's mathematics. "
           "<bookmark mark='c'/> In corporate training, where a one-day workshop is massed practice, and spacing it "
           "costs little and keeps more. <bookmark mark='d'/> And in evaluation: randomized trials of products and "
           "programmes, judged by later learning, not by how satisfied the learners felt.")

    def plan(self):
        rows_section(self, r"A worked redesign: \ a twelve-week statistics course", [
            (r"before: \ lectures, \ weekly problem sets on that week's topic, \ a midterm and a final; \ students "
             r"reread slides before exams", AUTH),
            (r"retrieval: \ a five-question quiz at the start of each class, \ low stakes, \ with answers discussed",
             GOOD),
            (r"spacing: \ every problem set includes two questions from three and six weeks earlier; \ the final is "
             r"cumulative, \ and says so", MODEL),
            (r"interleaving: \ the last third of each set mixes test types without labels: \ choosing the test is "
             r"the skill", PERSON),
            (r"load: \ worked examples first, \ faded to completion problems, \ then full problems", SYMP),
            (r"evaluation: \ a delayed test of the same items a term later, \ against last year's cohort, \ and the "
             r"students told why the course feels harder", YOU),
        ], "Here's a worked redesign of a twelve-week statistics course. <bookmark mark='a'/> Before: lectures, weekly "
           "problem sets on that week's topic, a midterm and a final, and students rereading slides before exams. "
           "<bookmark mark='b'/> Retrieval: a five-question quiz at the start of each class, low stakes, with the "
           "answers discussed. <bookmark mark='c'/> Spacing: every problem set includes two questions from three and "
           "six weeks earlier, and the final is cumulative, and says so. <bookmark mark='d'/> Interleaving: the last "
           "third of each set mixes kinds of test without labels, because choosing the test is the skill. "
           "<bookmark mark='e'/> Load: worked examples first, faded to completion problems, then full problems. "
           "<bookmark mark='f'/> And evaluation: a delayed test of the same items a term later, against last year's "
           "cohort, with the students told why the course feels harder.", font_size=21, buff=0.36)
