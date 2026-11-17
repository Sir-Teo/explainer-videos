from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Writing(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Writing it", r"How is a result written so that it can be trusted?",
                     scale=("person",))
        self.explore()
        self.abstract()
        self.paper()

    def explore(self):
        e = load("explore")
        rows_section(self, r"Exploratory, \ and labelled so", [
            (rf"all {e['all_n']} people, \ mirror trials included: \ reliability {e['all_rel']:.2f} "
             rf"({e['all_ci'][0]:.2f} to {e['all_ci'][1]:.2f}): \ the same answer", WHITE),
            (rf"why the paradox did not bite: \ people's slopes differ, \ SD about {e['between_sd']:.1f} ms per "
             rf"degree around a mean of {e['mean_slope']:.1f}", MODEL),
            (r"Part 59's Stroop effect had a spread about a quarter of its mean; \ rotation's is about a third, \ and "
             r"each person gives many trials per angle", PERSON),
            (r"robustness alone does not doom reliability; \ the ratio of real differences to trial noise does", YOU),
        ], "Then the exploratory analyses, labelled as such. <bookmark mark='a'/> With all fifty-four people, and "
           "mirror trials included, the reliability is zero point seven three, from zero point five seven to zero "
           "point eight three: the same answer. <bookmark mark='b'/> Why didn't the paradox bite? People's slopes "
           "really differ, with a standard deviation of about four milliseconds per degree around a mean of about "
           "twelve. <bookmark mark='c'/> Part 59's Stroop-like effect had a spread about a quarter of its mean. "
           "Rotation's is about a third, and each person gives many trials per angle. <bookmark mark='d'/> So "
           "robustness alone doesn't doom reliability. The ratio of real differences to trial noise does.",
           tag=psyche_tag(r"\texttt{thesis}, \ exploratory"))

    def paper(self):
        chips_section(self, r"The paper", [
            (r"introduction", r"the two results that collide, \ and the question; \ the design's limits, \ stated "
                              r"before the result", MODEL),
            (r"method", r"the registered plan, \ its hash, \ and the deviation with the original rule", PERSON),
            (r"results", r"registered first, \ exploratory after, \ every person's data in one figure", GOOD),
            (r"discussion", r"what the result changes (the paradox is a ratio, \ not a law about robust effects), "
                            r"\ and what it does not", SYMP),
            (r"limits", r"one data set, \ 40 people, \ one session: \ split-half is not test-retest over weeks", AUTH),
        ], "Then the paper. <bookmark mark='a'/> The introduction: the two results that collide, and the question, "
           "with the design's limits stated before the result. <bookmark mark='b'/> The method: the registered plan, "
           "its hash, and the deviation with the original rule. <bookmark mark='c'/> The results: registered first, "
           "exploratory after, and every person's data in one figure. <bookmark mark='d'/> The discussion: what the "
           "result changes, that the paradox is a ratio, not a law about robust effects, and what it doesn't. "
           "<bookmark mark='e'/> And the limits: one data set, forty people, one session. Split-half reliability "
           "isn't test-retest reliability over weeks.")

    def abstract(self):
        d = load("stage2")
        rows_section(self, r"The abstract, \ as it would be written", [
            (r"Is a robust effect a reliable measure of a person? \ We tested the mental-rotation slope, \ in a "
             r"registered report with the analysis written as code and hashed before the data were opened.", WHITE),
            (rf"In open trial-level data ({d['n']} people after one reported deviation), \ the slope's split-half "
             rf"reliability was {d['slope_rel']:.2f} (95\% CI {d['slope_ci'][0]:.2f} to {d['slope_ci'][1]:.2f}); \ "
             rf"the mean response time's was {d['mean_rel']:.2f}.", MODEL),
            (r"The registered test of the reliability paradox was inconclusive; \ the estimate leans against it. \ "
             r"The slope is usable for individual differences at moderate cost.", PERSON),
            (r"Limits: \ one dataset, \ one task, \ one sample; \ a larger replication with the same plan would "
             r"settle it.", AUTH),
        ], "Here is the abstract as it would be written. <bookmark mark='a'/> Is a robust effect a reliable measure "
           "of a person? We tested the mental-rotation slope in a registered report, with the analysis written as "
           "code and hashed before the data were opened. <bookmark mark='b'/> In open trial-level data, forty people "
           "after one reported deviation, the slope's split-half reliability was zero point seven four, with an "
           "interval from zero point five one to zero point eight seven. The mean response time's was zero point "
           "nine four. <bookmark mark='c'/> The registered test of the reliability paradox was inconclusive, and the "
           "estimate leans against it. The slope is usable for individual differences at moderate cost. "
           "<bookmark mark='d'/> Limits: one dataset, one task, one sample. A larger replication with the same "
           "plan would settle it.", font_size=21)
