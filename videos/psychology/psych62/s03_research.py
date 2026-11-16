from __future__ import annotations

from videos.psychology.psych62.common import *  # noqa: F403


class Research(VoiceoverScene):
    def construct(self):
        card_section(self, 2, r"How research is done", r"Where does a question come from?", scale=("person",))
        self.question_()
        self.literature()
        self.craft()

    def question_(self):
        chips_section(self, r"Finding a question worth asking", [
            (r"from a collision", r"two results that cannot both be right in general: \ here, \ Part 24's robust "
                                  r"slopes and Part 59's paradox", MODEL),
            (r"from a Frontier", r"every part of this series ends with open problems; \ each is a dissertation", PERSON),
            (r"answerable", r"data you can get, \ an analysis you can specify, \ an answer that would change what "
                            r"someone believes", GOOD),
            (r"small", r"a first project answers one question well, \ not a field's question badly", AUTH),
        ], "Where does a question come from? <bookmark mark='a'/> From a collision: two results that can't both be "
           "right in general. Here, Part 24's robust rotation slopes and Part 59's reliability paradox. "
           "<bookmark mark='b'/> From a frontier: every part of this series ends with open problems, and each is a "
           "dissertation. <bookmark mark='c'/> It must be answerable: data you can get, an analysis you can specify, "
           "and an answer that would change what someone believes. <bookmark mark='d'/> And it should be small. A "
           "first project answers one question well, not a field's question badly.")

    def craft(self):
        rows_section(self, r"The craft", [
            (r"reading: \ the Ledger's habit: \ for each claim, \ the original, \ the record, \ the date checked", WHITE),
            (r"the pilot: \ run the procedure on a few people, \ or on simulated ones, \ to find what breaks", MODEL),
            (r"advisers and collaborators: \ people who will tell you what is wrong while it can still be fixed",
             PERSON),
            (r"a contribution: \ something the field did not know, \ stated so it could be shown false", GOOD),
        ], "Then the craft. <bookmark mark='a'/> Reading, with the Ledger's habit: for each claim, the original, the "
           "record, and the date it was checked. <bookmark mark='b'/> The pilot: run the procedure on a few people, "
           "or on simulated ones, to find what breaks. <bookmark mark='c'/> Advisers and collaborators: people who "
           "will tell you what's wrong while it can still be fixed. <bookmark mark='d'/> And a contribution: "
           "something the field didn't know, stated so that it could be shown false.")

    def literature(self):
        rows_section(self, r"Reading a literature before adding to it", [
            (r"start from the best recent review or meta-analysis, \ then read its strongest and its weakest "
             r"studies in full", WHITE),
            (r"for each study, \ Part 4's questions: \ how many people, \ preregistered or not, \ what was measured "
             r"and how reliably, \ and what the effect would be after Part 50's corrections", MODEL),
            (r"search the registries and preprints for what was run and never published: \ the denominator", PERSON),
            (r"write down, \ before designing anything, \ what the field would believe if your study came out "
             r"either way: \ if nothing would change, \ choose another question", GOOD),
        ], "Before adding to a literature, read it. <bookmark mark='a'/> Start from the best recent review or "
           "meta-analysis, then read its strongest and its weakest studies in full. <bookmark mark='b'/> For each "
           "study, ask Part 4's questions: how many people, preregistered or not, what was measured and how "
           "reliably, and what the effect would be after Part 50's corrections. <bookmark mark='c'/> Search the "
           "registries and preprints for what was run and never published. That's the denominator. "
           "<bookmark mark='d'/> And write down, before designing anything, what the field would believe if your "
           "study came out either way. If nothing would change, choose another question.")
