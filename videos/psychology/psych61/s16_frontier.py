from __future__ import annotations

from videos.psychology.psych61.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ a science that studies itself", r"Can a field measure its own "
                     r"progress?", scale=("society",))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"metascience", r"randomized trials of journal policies, \ peer review and training", MODEL),
            (r"living reviews", r"meta-analyses updated as studies arrive, \ with the Ledger's dates", PERSON),
            (r"global samples by default", r"networks that make cross-cultural testing the first study, \ not the "
                                           r"last", GOOD),
            (r"machine-assisted design", r"surrogate models and adaptive designs choosing the next experiment", SYMP),
        ], "Can a field measure its own progress? First, what's new. <bookmark mark='a'/> Metascience runs "
           "randomized trials of journal policies, peer review and training. <bookmark mark='b'/> Living reviews "
           "update meta-analyses as studies arrive, with dates like the Ledger's. <bookmark mark='c'/> Networks make "
           "cross-cultural testing the first study, not the last. <bookmark mark='d'/> And surrogate models and "
           "adaptive designs choose the next experiment.", chip_w=4.4, text_w=7.8)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"measuring progress", r"how to tell a field that is accumulating knowledge from one that is not", AUTH),
            (r"credit", r"rewarding contributions to big teams, \ data and replications", MODEL),
            (r"theory", r"whether formal theory and integrative design speed discovery, \ tested as interventions",
             PERSON),
            (r"prediction", r"what limits the predictability of human lives, \ and whether it can be raised", GOOD),
        ], "And the open problems. <bookmark mark='a'/> How to tell a field that's accumulating knowledge from one "
           "that isn't. <bookmark mark='b'/> How to reward contributions to big teams, data and replications. "
           "<bookmark mark='c'/> Whether formal theory and integrative design speed discovery, tested as "
           "interventions. <bookmark mark='d'/> And what limits the predictability of human lives, and whether it "
           "can be raised.")
