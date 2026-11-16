from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ predicting what works where", r"Can we know in advance which nudge "
                     r"will work?", scale=("society",))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"forecasting", r"experts and the public predicting megastudy results: \ mostly poor, \ and calibration "
                             r"improves with feedback", MODEL),
            (r"targeting", r"machine-learned models of who responds, \ from large trials, \ to send each person the "
                           r"message that works for them", PERSON),
            (r"fairness", r"targeting can give help to those easiest to move, \ not those who need it most", AUTH),
            (r"living evidence", r"pooled trial registries updated as trials finish, \ instead of one meta-analysis "
                                 r"a decade", GOOD),
        ], "Can we know in advance which nudge will work? <bookmark mark='a'/> Forecasting: experts and the public "
           "predicting megastudy results, mostly poorly, though calibration improves with feedback. "
           "<bookmark mark='b'/> Targeting: models learned from large trials of who responds, used to send each "
           "person the message that works for them. <bookmark mark='c'/> But targeting can give help to those easiest "
           "to move, not those who need it most. <bookmark mark='d'/> And living evidence: pooled trial registries, "
           "updated as trials finish, instead of one meta-analysis a decade.")

    def open(self):
        chips_section(self, r"Open problems", [
            (r"external validity", r"what features of a site predict whether an effect transfers?", MODEL),
            (r"persistence", r"which changes last after the nudge stops, \ and why", PERSON),
            (r"general equilibrium", r"when everyone sends reminders, \ do reminders still work?", AUTH),
            (r"the system frame", r"how to weigh a cheap nudge against a costly rule that would do more", GOOD),
        ], "And the open problems. <bookmark mark='a'/> External validity: what features of a site predict whether "
           "an effect transfers? <bookmark mark='b'/> Persistence: which changes last after the nudge stops, and why? "
           "<bookmark mark='c'/> General equilibrium: when everyone sends reminders, do reminders still work? "
           "<bookmark mark='d'/> And the system frame: how to weigh a cheap nudge against a costly rule that would do "
           "more.")
