from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ care in the moment", r"Can help arrive exactly when it is needed?",
                     scale=("person", "society"))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"just-in-time interventions", r"phone sensors and brief questions decide when to offer help: \ tested by "
                                            r"micro-randomized trials (Part 47)", MODEL),
            (r"chatbots in care", r"conversational agents for support and therapy exercises: \ early trials, \ and "
                                  r"Part 60's questions about safety and trust", PERSON),
            (r"causal evidence on stress", r"natural experiments and genetic designs to separate stress from what "
                                           r"comes with it", GOOD),
            (r"precision care", r"predicting who benefits from which step, \ instead of trying each in turn", SYMP),
        ], "Can help arrive exactly when it's needed? <bookmark mark='a'/> Just-in-time adaptive interventions use "
           "phone sensors and brief questions to decide when to offer help, and they're tested by Part 47's "
           "micro-randomized trials. <bookmark mark='b'/> Chatbots offer support and therapy exercises, with early "
           "trials, and Part 60's questions about safety and trust. <bookmark mark='c'/> Natural experiments and "
           "genetic designs are separating stress from what comes with it. <bookmark mark='d'/> And precision care "
           "would predict who benefits from which step, instead of trying each in turn.", chip_w=4.2, text_w=8.0)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"engagement", r"why people stop using help that works, \ and what keeps them", AUTH),
            (r"placebo, \ used ethically", r"how to harness expectation without deception", MODEL),
            (r"measurement", r"outcomes people care about, \ measured cheaply, \ every week", PERSON),
            (r"equity", r"who the systems miss, \ and why", GOOD),
        ], "And the open problems. <bookmark mark='a'/> Engagement: why people stop using help that works, and what "
           "keeps them. <bookmark mark='b'/> Placebo, used ethically: how to harness expectation without deception. "
           "<bookmark mark='c'/> Measurement: outcomes people care about, measured cheaply, every week. "
           "<bookmark mark='d'/> And equity: who the systems miss, and why.")
