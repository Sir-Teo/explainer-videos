from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Misinfo(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Misinformation", r"Can people be nudged toward truth?", scale=("society",))
        self.accuracy()
        self.inoculation()

    def accuracy(self):
        rows_section(self, r"Accuracy prompts", [
            (r"Pennycook and colleagues, \ 2021: \ asking people to rate the accuracy of one headline made them more "
             r"discerning about what they then chose to share", WHITE),
            (r"the claim: \ people share falsehoods less from belief than from inattention to accuracy", MODEL),
            (r"replications and a meta-analysis found the effect, \ smaller than first reported, \ and weaker in some "
             r"groups and countries", AUTH),
            (r"in a field experiment on a social platform, \ accuracy messages slightly improved the quality of "
             r"what users shared", GOOD),
        ], "Can people be nudged toward truth? <bookmark mark='a'/> In 2021 Gordon Pennycook and colleagues found "
           "that asking people to rate the accuracy of one headline made them more discerning about what they then "
           "chose to share. <bookmark mark='b'/> The claim is that people share falsehoods less from belief than from "
           "inattention to accuracy. <bookmark mark='c'/> Replications and a meta-analysis found the effect, smaller "
           "than first reported, and weaker in some groups and countries. <bookmark mark='d'/> In a field experiment "
           "on a social platform, accuracy messages slightly improved the quality of what users shared.",
           tag=published_tag(r"Pennycook et al.\ (2021)"))

    def inoculation(self):
        chips_section(self, r"Inoculation", [
            (r"the idea", r"expose people to a weakened manipulation technique, \ with the refutation, \ before they "
                          r"meet the real thing", MODEL),
            (r"the evidence", r"short games and videos improve people's ability to spot manipulative techniques in "
                              r"test items", GOOD),
            (r"the caveat", r"some of the gain is more scepticism of everything, \ true items included: \ Part 12's "
                            r"criterion, \ shifted", AUTH),
            (r"the scale", r"effects decay over weeks; \ boosters help", PERSON),
        ], "A second approach is inoculation. <bookmark mark='a'/> Expose people to a weakened manipulation "
           "technique, with the refutation, before they meet the real thing. <bookmark mark='b'/> Short games and "
           "videos improve people's ability to spot manipulative techniques in test items. <bookmark mark='c'/> But "
           "some of the gain is more scepticism of everything, true items included. That's Part 12's criterion, "
           "shifted, rather than sensitivity gained. <bookmark mark='d'/> And effects decay over weeks, though "
           "boosters help.")
