from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Reforms(VoiceoverScene):
    def construct(self):
        card_section(self, 5, r"System variables and the reforms", r"What can the police control?",
                     scale=("society",))
        self.reforms()
        self.field()

    def reforms(self):
        chips_section(self, r"What the system controls", [
            (r"double-blind", r"the officer running the line-up does not know who the suspect is: \ Part 2's Clever "
                              r"Hans, \ removed", GOOD),
            (r"instructions", r"``the person may or may not be present'': \ permission to pick no one", MODEL),
            (r"fair fillers", r"the suspect should not stand out; \ fillers match the witness's description", PERSON),
            (r"recorded confidence", r"the first statement of confidence, \ in the witness's words, \ before any "
                                     r"feedback", SYMP),
            (r"one line-up", r"a witness shown the same suspect twice has seen him before: \ the second test is "
                             r"contaminated", AUTH),
        ], "System variables are the ones the justice system controls, and the reforms target them. "
           "<bookmark mark='a'/> Double-blind administration: the officer running the line-up doesn't know who the "
           "suspect is. That's Part 2's Clever Hans, removed. <bookmark mark='b'/> Instructions that the person may "
           "or may not be present, which give permission to pick no one. <bookmark mark='c'/> Fair fillers: the "
           "suspect shouldn't stand out, and fillers match the witness's description. <bookmark mark='d'/> The first "
           "statement of confidence, recorded in the witness's own words, before any feedback. "
           "<bookmark mark='e'/> And one line-up only. A witness shown the same suspect twice has seen him before, "
           "so the second test is contaminated. Gary Wells and colleagues' 2020 recommendations set these out.",
           tag=published_tag(r"Wells et al.\ (2020)"), chip_w=3.6, text_w=8.6)

    def field(self):
        rows_section(self, r"In real line-ups", [
            (r"in the field the truth is usually unknown, \ but one kind of error is visible: \ a filler picked is "
             r"always a mistake", WHITE),
            (r"Wixted and colleagues' study of a Houston police department's line-ups: \ filler picks were common at "
             r"low confidence and rare at high confidence", GOOD),
            (r"the same pattern the laboratory predicts: \ a clean first identification made with high confidence is "
             r"usually of the person the witness saw", MODEL),
            (r"the cases that went wrong in the exonerations mostly involved low or unrecorded initial confidence, \ "
             r"suggestive procedure, \ or repeated identifications", AUTH),
        ], "What about real line-ups? <bookmark mark='a'/> In the field the truth is usually unknown, but one kind of "
           "error is visible: a filler picked is always a mistake. <bookmark mark='b'/> In John Wixted and "
           "colleagues' study of a Houston police department's line-ups, filler picks were common at low confidence "
           "and rare at high confidence. <bookmark mark='c'/> That's the pattern the laboratory predicts. A clean "
           "first identification made with high confidence is usually of the person the witness saw. "
           "<bookmark mark='d'/> And the cases that went wrong in the exonerations mostly involved low or unrecorded "
           "initial confidence, suggestive procedure, or repeated identifications.",
           tag=published_tag(r"Wixted et al.\ (2016)"))
