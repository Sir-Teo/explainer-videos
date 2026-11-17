from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        card_section(self, 14, r"In practice: \ a selection system, \ designed", r"How would you hire 100 people "
                     r"well?", scale=("society",))
        self.where()
        self.system()

    def where(self):
        chips_section(self, r"Where this is a job", [
            (r"talent assessment", r"designing and validating tests, \ interviews and assessment centres; \ the "
                                   r"standards are professional guidelines and the law", MODEL),
            (r"people analytics", r"turnover, \ performance and engagement data inside a company: \ Part 47's levels "
                                  r"and Part 2's causes apply", PERSON),
            (r"compensation", r"pay systems that reward what matters without crowding out what is not paid for", SYMP),
            (r"engagement surveys", r"Part 46's question writing, \ and honest reporting of change", GOOD),
        ], "Where is this a job? <bookmark mark='a'/> In talent assessment: designing and validating tests, "
           "interviews and assessment centres, under professional guidelines and the law. <bookmark mark='b'/> In "
           "people analytics: turnover, performance and engagement data inside a company, where Part 47's levels and "
           "Part 2's causes apply. <bookmark mark='c'/> In compensation: pay systems that reward what matters "
           "without crowding out what isn't paid for. <bookmark mark='d'/> And in engagement surveys, with Part 46's "
           "question writing and honest reporting of change.", chip_w=3.8, text_w=8.4)

    def system(self):
        u, imp, fr = load("utility"), load("impact"), load("frontier")
        k = int(np.argmax(fr["validity"]))
        rows_section(self, r"A worked design: \ 100 hires from 500 applicants", [
            (r"job analysis first: \ the tasks, \ and the knowledge, \ skills and abilities they need", WHITE),
            (r"predictors: \ a structured interview and a job-knowledge or work-sample test, \ scored by rule, \ "
             r"combined by fixed weights", MODEL),
            (rf"expected validity of the composite about {fr['validity'][k]:.2f}; \ utility over five years in the "
             rf"millions at a plausible $SD_y$, \ against testing costs in the tens of thousands", GOOD),
            (r"adverse impact checked on the pilot sample; \ if the ratio falls below 0.8, \ look for a less "
             r"discriminatory alternative with similar validity (the frontier)", AUTH),
            (r"then a predictive validation: \ collect performance a year later, \ with a good criterion, \ and "
             r"correct only for the restriction that happened", PERSON),
            (r"and a decision log, \ written before the data: \ what counts as success, \ and when the system would "
             r"be changed", YOU),
        ], "Here's a worked design: a hundred hires from five hundred applicants. <bookmark mark='a'/> Start with a "
           "job analysis: the tasks, and the knowledge, skills and abilities they need. <bookmark mark='b'/> Use a "
           "structured interview and a job-knowledge test or a work sample, scored by rule and combined by fixed "
           "weights. <bookmark mark='c'/> The composite's expected validity is in the mid zero point fours, and the "
           "utility over five years is in the millions, against testing costs in the tens of thousands. "
           "<bookmark mark='d'/> Check adverse impact on the pilot sample. If the ratio falls below zero point eight, "
           "look along the frontier for a less discriminatory alternative with similar validity. "
           "<bookmark mark='e'/> Then run a predictive validation: collect performance a year later, with a good "
           "criterion, and correct only for the restriction that actually happened. <bookmark mark='f'/> And keep a "
           "decision log, written before the data: what counts as success, and when the system would be changed.",
           font_size=21, buff=0.36)
