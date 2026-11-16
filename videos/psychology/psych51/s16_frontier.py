from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ supervising learning machines", r"What changes when the automation "
                     r"learns?", scale=("person", "society"))
        self.new()
        self.assistants()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"opaque failures", r"classic automation fails at known edges; \ a learned system can fail on an input "
                                 r"that looks ordinary to a person", AUTH),
            (r"fluent output", r"an assistant's confident, \ well-written answer invites Part 25's trust in fluency, "
                               r"\ whether or not it is right", PERSON),
            (r"shifting reliability", r"an update can change what the system does well, \ so trust calibrated last "
                                      r"month may be wrong today", MODEL),
            (r"monitoring at scale", r"one supervisor watching many vehicles or agents: \ vigilance and takeover, \ "
                                     r"multiplied", SYMP),
        ], "What changes when the automation learns? <bookmark mark='a'/> Classic automation fails at known edges. A "
           "learned system can fail on an input that looks ordinary to a person. <bookmark mark='b'/> An assistant's "
           "confident, well-written answer invites Part 25's trust in fluency, whether or not it's right. "
           "<bookmark mark='c'/> Reliability shifts. An update can change what the system does well, so trust that "
           "was calibrated last month may be wrong today. <bookmark mark='d'/> And monitoring scales. One supervisor "
           "may watch many vehicles or agents, which is vigilance and takeover, multiplied.", chip_w=3.6, text_w=8.6)

    def assistants(self):
        rows_section(self, r"Decision aids in high-stakes work", [
            (r"radiology, \ pathology and dermatology have tested readers with and without an algorithm's suggestion",
             WHITE),
            (r"correct suggestions improve readers; \ incorrect ones pull them along, \ experts included: \ automation "
             r"bias, \ measured", AUTH),
            (r"the design questions are this part's: \ when to show the suggestion, \ how to show its uncertainty, \ "
             r"and who reads first", MODEL),
            (r"the evaluation question is the human with the machine, \ not the machine alone: \ the team is "
             r"what gets tested, \ in the clinic", YOU),
        ], "Decision aids are already in high-stakes work. <bookmark mark='a'/> Radiology, pathology and dermatology "
           "have tested readers with and without an algorithm's suggestion. <bookmark mark='b'/> Correct suggestions "
           "improve readers. Incorrect ones pull them along, experts included. That's automation bias, measured. "
           "<bookmark mark='c'/> The design questions are this part's: when to show the suggestion, how to show its "
           "uncertainty, and who reads first. <bookmark mark='d'/> And the evaluation question is the human with the "
           "machine, not the machine alone.")

    def open(self):
        chips_section(self, r"Open problems", [
            (r"monitoring", r"driver and operator monitoring that measures readiness, \ not just gaze", MODEL),
            (r"explanations", r"which explanations improve calibration, \ and which only raise trust", PERSON),
            (r"skill", r"keeping human skill alive when the machine does the work most of the time: \ Bainbridge's "
                       r"problem, \ unsolved", AUTH),
            (r"measurement", r"near misses and takeovers as data: \ shared, \ open incident reporting for learned "
                             r"systems", GOOD),
        ], "And the open problems. <bookmark mark='a'/> Monitoring that measures an operator's readiness, not just "
           "where their eyes point. <bookmark mark='b'/> Explanations: which ones improve calibration, and which only "
           "raise trust. <bookmark mark='c'/> Skill: keeping human skill alive when the machine does the work most of "
           "the time. That's Bainbridge's problem, and it's still unsolved. <bookmark mark='d'/> And measurement: near "
           "misses and takeovers treated as data, with shared, open incident reporting for learned systems.")
