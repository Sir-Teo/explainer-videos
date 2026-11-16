from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Feedback(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Feedback", r"Does feedback always help?")
        self.kluger()
        self.content()
        self.good()

    def kluger(self):
        rows_section(self, r"A third of the time, \ worse", [
            (r"Kluger and DeNisi, \ 1996: \ a meta-analysis of over 600 effects of feedback on performance", WHITE),
            (r"the average effect was positive, \ about 0.4 SD", GOOD),
            (r"but in over a third of the comparisons, \ feedback made performance worse", AUTH),
            (r"feedback that pointed attention at the self, \ praise or criticism of the person, \ tended to hurt; \ "
             r"feedback about the task and how to improve tended to help", MODEL),
            (r"the same word, \ ``feedback'', \ names interventions with opposite effects", YOU),
        ], "Does feedback always help? <bookmark mark='a'/> In 1996 Avraham Kluger and Angelo DeNisi pooled over six "
           "hundred effects of feedback on performance. <bookmark mark='b'/> The average effect was positive, about "
           "zero point four standard deviations. <bookmark mark='c'/> But in over a third of the comparisons, "
           "feedback made performance worse. <bookmark mark='d'/> Feedback that pointed attention at the self, "
           "praise or criticism of the person, tended to hurt. Feedback about the task, and how to improve it, "
           "tended to help. <bookmark mark='e'/> The same word names interventions with opposite effects.",
           tag=published_tag(r"Kluger \& DeNisi (1996)"))

    def good(self):
        chips_section(self, r"Feedback that works", [
            (r"about the task", r"what was right, \ what to change, \ and the next step", GOOD),
            (r"timely", r"while the attempt is still in memory; \ for retrieval practice, \ right after the answer", MODEL),
            (r"acted on", r"a chance to try again: \ feedback without a second attempt is information without "
                          r"practice", PERSON),
            (r"not a grade alone", r"a mark tells where you stand, \ not how to improve", AUTH),
        ], "So what does feedback that works look like? <bookmark mark='a'/> It's about the task: what was right, "
           "what to change, and the next step. <bookmark mark='b'/> It's timely, while the attempt is still in "
           "memory. For retrieval practice, that's right after the answer. <bookmark mark='c'/> It's acted on, with a "
           "chance to try again. Feedback without a second attempt is information without practice. "
           "<bookmark mark='d'/> And it's not a grade alone. A mark tells you where you stand, not how to improve.")

    def content(self):
        rows_section(self, r"What the feedback says", [
            (r"after a wrong answer, \ ``wrong'' alone does little: \ the learner still lacks the right answer "
             r"(Pashler and colleagues, \ 2005)", AUTH),
            (r"the correct answer is what helps; \ an explanation helps most when the task needs understanding, \ "
             r"not only recall", GOOD),
            (r"after a right answer given with low confidence, \ feedback helps too: \ it turns a guess into "
             r"something known (Butler, \ Karpicke and Roediger, \ 2008)", MODEL),
            (r"and errors made with high confidence are corrected best: \ the surprise marks them (Part 17's "
             r"prediction error)", PERSON),
        ], "What should the feedback say? <bookmark mark='a'/> After a wrong answer, being told \"wrong\" alone does "
           "little, because the learner still lacks the right answer. Harold Pashler and colleagues found this in "
           "2005. <bookmark mark='b'/> The correct answer is what helps, and an explanation helps most when the task "
           "needs understanding rather than recall. <bookmark mark='c'/> After a right answer given with low "
           "confidence, feedback helps too. Andrew Butler, Jeffrey Karpicke and Henry Roediger showed it turns a "
           "guess into something known. <bookmark mark='d'/> And, surprisingly, errors made with high confidence "
           "are corrected best. The surprise marks them, like Part 17's prediction error.")
