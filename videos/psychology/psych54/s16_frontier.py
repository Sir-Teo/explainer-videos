from __future__ import annotations

from videos.psychology.psych54.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ AI tutors and what transfers", r"Will a machine tutor close the two "
                     r"sigma?", scale=("person", "society"))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"language-model tutors", r"conversational tutors for every student; \ early randomized trials are "
                                       r"mixed, \ and the details of design matter", MODEL),
            (r"the crutch problem", r"students who use an assistant to answer practice problems can do better during "
                                    r"practice and worse on a later test without it: \ performance against learning, "
                                    r"\ again", AUTH),
            (r"guardrails", r"tutors designed to give hints rather than answers aim to keep the desirable difficulty",
             GOOD),
            (r"better memory models", r"schedulers learned from millions of reviews, \ evaluated by randomized "
                                      r"comparison", PERSON),
        ], "Will a machine tutor close the two sigma? <bookmark mark='a'/> Conversational tutors built on language "
           "models can reach every student. Early randomized trials are mixed, and the details of design matter. "
           "<bookmark mark='b'/> There's a crutch problem. Students who use an assistant to answer practice problems "
           "can do better during practice and worse on a later test without it. That's performance against "
           "learning, again. <bookmark mark='c'/> Tutors designed to give hints rather than answers aim to keep the "
           "desirable difficulty. <bookmark mark='d'/> And schedulers are being learned from millions of reviews, and "
           "should be judged by randomized comparison.", chip_w=3.8, text_w=8.4)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"transfer", r"what learning carries to new problems and new settings, \ and how to teach for it", MODEL),
            (r"motivation", r"the best technique fails if the learner stops: \ how to make effective study "
                            r"chosen", PERSON),
            (r"scale", r"why effects shrink from pilot to system, \ and how to stop it", AUTH),
            (r"measurement", r"tests that measure lasting learning, \ not performance on the day", GOOD),
        ], "And the open problems. <bookmark mark='a'/> Transfer: what learning carries to new problems and new "
           "settings, and how to teach for it. <bookmark mark='b'/> Motivation: the best technique fails if the "
           "learner stops, so how do we make effective study the one people choose? <bookmark mark='c'/> Scale: why "
           "effects shrink from pilot to system, and how to stop it. <bookmark mark='d'/> And measurement: tests that "
           "measure lasting learning, not performance on the day.")
