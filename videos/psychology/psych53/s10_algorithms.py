from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Algorithms(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Algorithms in hiring", r"What does a model learn from past hiring?",
                     scale=("society",))
        self.learned()
        self.audit()

    def learned(self):
        rows_section(self, r"A screen that learned the past", [
            (r"a model trained to predict who was hired, \ or who was rated well, \ learns whatever those decisions "
             r"rewarded", WHITE),
            (r"2018: \ reports described a large company's experimental r\'esum\'e screen that marked down words "
             r"associated with women, \ learned from a decade of mostly male hires; \ it was dropped", AUTH),
            (r"the criterion problem again: \ the model's target was past human judgement, \ not performance", MODEL),
            (r"removing a group label does not remove the group: \ colleges, \ clubs and gaps in a career are "
             r"proxies", PERSON),
        ], "What does a model learn from past hiring? <bookmark mark='a'/> A model trained to predict who was hired, "
           "or who was rated well, learns whatever those decisions rewarded. <bookmark mark='b'/> In 2018, reports "
           "described a large company's experimental resume screen that marked down words associated with women, "
           "learned from a decade of mostly male hires. The company dropped it. <bookmark mark='c'/> It's the "
           "criterion problem again. The model's target was past human judgement, not performance. "
           "<bookmark mark='d'/> And removing a group label doesn't remove the group. Colleges, clubs and gaps in a "
           "career are proxies.")

    def audit(self):
        chips_section(self, r"Auditing an algorithm", [
            (r"validity", r"does the score predict performance, \ measured well, \ in a new sample? \ the same "
                          r"question as for any test", GOOD),
            (r"impact", r"selection rates by group and the impact ratio, \ computed on real applicants", MODEL),
            (r"bias audits by law", r"New York City has required yearly independent bias audits of automated "
                                    r"hiring tools since 2023", PERSON),
            (r"transparency", r"candidates told that a tool is used, \ and what it measures", SYMP),
        ], "So how do you audit an algorithm? <bookmark mark='a'/> Ask the same question as for any test: does the "
           "score predict performance, measured well, in a new sample? <bookmark mark='b'/> Compute selection rates "
           "by group and the impact ratio, on real applicants. <bookmark mark='c'/> Some laws now require it. New "
           "York City has required yearly independent bias audits of automated hiring tools since 2023. "
           "<bookmark mark='d'/> And tell candidates that a tool is used, and what it measures.")
