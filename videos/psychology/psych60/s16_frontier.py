from __future__ import annotations

from videos.psychology.psych60.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ two sciences of minds", r"What happens when both kinds of mind are "
                     r"studied together?", scale=("person", "society"))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"models of many experiments", r"networks fine-tuned on trial-level data from many experiments, \ "
                                            r"proposed as general models of human choice; \ judged by held-out "
                                            r"experiments", MODEL),
            (r"interpretability", r"reading features and circuits inside models: \ neuroscience's methods turned "
                                  r"on machines", PERSON),
            (r"field experiments", r"randomized studies of AI tutors, \ advisers and companions in daily use", GOOD),
            (r"people learning with AI", r"what assistance does to skill, \ memory and belief over months", SYMP),
        ], "What happens when both kinds of mind are studied together? First, what's new. <bookmark mark='a'/> "
           "Networks fine-tuned on trial-level data from many experiments are proposed as general models of human "
           "choice, and judged by experiments they haven't seen. <bookmark mark='b'/> Interpretability reads "
           "features and circuits inside models, turning neuroscience's methods on machines. <bookmark mark='c'/> "
           "Field experiments randomize AI tutors, advisers and companions in daily use. <bookmark mark='d'/> And "
           "studies of people learning with AI ask what assistance does to skill, memory and belief over months.",
           chip_w=4.4, text_w=7.8)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"machine behaviour", r"a science of it with psychology's hard-won methods, \ and results dated by "
                                   r"model version", MODEL),
            (r"mechanistic models", r"models of cognition that are also mechanisms you can inspect", PERSON),
            (r"pervasive AI", r"its effects on human learning, \ belief and relationships, \ measured causally", AUTH),
            (r"minds", r"what it would take to know whether a machine has experiences", YOU),
        ], "And the open problems. <bookmark mark='a'/> A science of machine behaviour, with psychology's hard-won "
           "methods, and results dated by model version. <bookmark mark='b'/> Models of cognition that are also "
           "mechanisms you can inspect. <bookmark mark='c'/> The effects of pervasive AI on human learning, belief "
           "and relationships, measured causally. <bookmark mark='d'/> And what it would take to know whether a "
           "machine has experiences.")
