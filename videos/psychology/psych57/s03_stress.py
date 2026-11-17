from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Stress(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"Stress and illness", r"Does a hard life make a body ill?", scale=("person", "society"))
        self.load_()
        self.limits()

    def load_(self):
        chips_section(self, r"From a stress response to a life", [
            (r"Part 10's loop", r"a threat raises cortisol and arousal, \ then the loop switches itself off; \ "
                                r"repeated for years, \ it does not fully switch off", MODEL),
            (r"allostatic load", r"McEwen's term for the wear: \ blood pressure, \ inflammation, \ metabolism, \ "
                                 r"measured together", PERSON),
            (r"status and health", r"Marmot's Whitehall studies of British civil servants: \ the lower the grade, \ "
                                   r"the higher the death rate, \ at every step", AUTH),
            (r"adverse childhood experiences", r"Felitti and colleagues, \ 1998: \ the more kinds of childhood "
                                              r"adversity, \ the more adult disease, \ in a graded relation", SYMP),
        ], "Does a hard life make a body ill? <bookmark mark='a'/> Part 10 built the stress loop. A threat raises "
           "cortisol and arousal, and then the loop switches itself off. Repeated for years, it doesn't fully switch "
           "off. <bookmark mark='b'/> Bruce McEwen called the wear allostatic load: blood pressure, inflammation and "
           "metabolism, measured together. <bookmark mark='c'/> Michael Marmot's Whitehall studies of British civil "
           "servants found that the lower the grade, the higher the death rate, at every step of the ladder. "
           "<bookmark mark='d'/> And in 1998 Vincent Felitti and colleagues found that the more kinds of childhood "
           "adversity people reported, the more adult disease they had, in a graded relation.",
           tag=published_tag(r"Felitti et al.\ (1998)"), chip_w=4.2, text_w=8.0)

    def limits(self):
        rows_section(self, r"What the correlations cannot say", [
            (r"most of this evidence is observational: \ stress comes with poverty, \ smoking, \ poor sleep and poor "
             r"care (Part 2's confounding)", AUTH),
            (r"the cold studies are an experiment for the virus, \ not for the stress, \ which was measured, \ not "
             r"assigned", MODEL),
            (r"the strongest designs: \ the viral challenge, \ natural experiments, \ and trials that reduce stress "
             r"and measure a biological outcome", GOOD),
            (r"an ACE score describes groups well and predicts for one person poorly (Part 47): \ it is not a "
             r"screening test", PERSON),
        ], "What can't the correlations say? <bookmark mark='a'/> Most of this evidence is observational. Stress comes "
           "with poverty, smoking, poor sleep and poor care, which is Part 2's confounding. <bookmark mark='b'/> The "
           "cold studies are an experiment for the virus, not for the stress, which was measured, not assigned. "
           "<bookmark mark='c'/> The strongest designs are the viral challenge, natural experiments, and trials that "
           "reduce stress and measure a biological outcome. <bookmark mark='d'/> And a childhood-adversity score "
           "describes groups well and predicts poorly for one person, as Part 47 would warn. It isn't a screening "
           "test.")
