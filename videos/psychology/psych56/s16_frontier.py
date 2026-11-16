from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ machines, \ interviews and tools", r"What will change in the "
                     r"courtroom?", scale=("society",))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"machine face recognition", r"far better than people in good images, \ worse in poor ones, \ and with "
                                          r"error rates that differ across groups; \ a match is a lead, \ not an "
                                          r"identification", AUTH),
            (r"humans with machines", r"examiners and algorithms combined have done better than either alone in "
                                      r"some face-matching studies", GOOD),
            (r"interviewing", r"the cognitive interview and PEACE: \ more correct detail without more errors", MODEL),
            (r"risk tools under audit", r"laws requiring validation and bias audits, \ as for hiring tools (Part 53)",
             PERSON),
        ], "What will change in the courtroom? <bookmark mark='a'/> Machine face recognition is far better than "
           "people in good images, worse in poor ones, and has error rates that differ across groups. A match is a "
           "lead, not an identification. <bookmark mark='b'/> In some face-matching studies, examiners and algorithms "
           "combined did better than either alone. <bookmark mark='c'/> Interviewing methods like the cognitive "
           "interview and PEACE get more correct detail without more errors. <bookmark mark='d'/> And risk tools are "
           "coming under laws that require validation and bias audits, as hiring tools are.", chip_w=4.0, text_w=8.2)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"field ground truth", r"how accurate are real identifications? \ exonerations are a biased sample", MODEL),
            (r"memory over months", r"what a year of retelling does to a witness's account", PERSON),
            (r"juries and statistics", r"how to present a likelihood ratio so that jurors use it correctly", AUTH),
            (r"which fairness", r"what a risk tool owes each group when base rates differ", GOOD),
        ], "And the open problems. <bookmark mark='a'/> Field ground truth: how accurate are real identifications? "
           "Exonerations are a biased sample. <bookmark mark='b'/> Memory over months: what a year of retelling does "
           "to a witness's account. <bookmark mark='c'/> Juries and statistics: how to present a likelihood ratio so "
           "that jurors use it correctly. <bookmark mark='d'/> And which fairness: what a risk tool owes each group "
           "when base rates differ.")
