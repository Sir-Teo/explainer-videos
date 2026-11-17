from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Toolbox(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"The toolbox", r"What else can be changed besides the default?")
        self.tools()
        self.opower()

    def tools(self):
        chips_section(self, r"Choice architecture", [
            (r"framing", r"``90\% survive'' against ``10\% die'' (Part 26): \ the same fact, \ a different choice", MODEL),
            (r"salience and simplification", r"put the cost in the headline, \ cut the form to one page: \ college "
                                             r"aid applications pre-filled from tax data raised enrolment", GOOD),
            (r"reminders and planning", r"a text the day before, \ ``when and where will you get your flu shot?''", PERSON),
            (r"commitment devices", r"locking in a choice: \ a savings account you cannot touch, \ a pledge with a "
                                    r"stake", SYMP),
            (r"social norms", r"``most of your neighbours...'': \ Part 34's descriptive norms, \ sent as letters", AUTH),
        ], "Defaults are one tool among several. <bookmark mark='a'/> Framing: ninety percent survive against ten "
           "percent die, Part 26's frames, the same fact and a different choice. <bookmark mark='b'/> Salience and "
           "simplification: put the cost in the headline, cut the form to one page. College aid applications "
           "pre-filled from tax data raised enrolment. <bookmark mark='c'/> Reminders and planning prompts: a text "
           "the day before, or asking when and where you'll get your flu shot. <bookmark mark='d'/> Commitment "
           "devices lock in a choice: a savings account you can't touch, or a pledge with a stake. "
           "<bookmark mark='e'/> And social norms, most of your neighbours do this, which are Part 34's descriptive "
           "norms, sent as letters.", chip_w=4.4, text_w=7.8)

    def opower(self):
        rows_section(self, r"Home energy reports", [
            (r"a utility's mailed report compares each household's energy use with similar neighbours', \ with a "
             r"smiley face for the efficient", WHITE),
            (r"Allcott, \ 2011: \ across about 600,000 households in randomized trials, \ use fell by about 2\%", GOOD),
            (r"small per home, \ and cheap: \ across millions of homes it adds up, \ "
             r"and part of it persisted after the letters stopped", MODEL),
            (r"the effect was larger for heavy users, \ and the first sites chosen for the programme showed larger "
             r"effects than later ones: \ site selection, \ a lesson for chapter six", PERSON),
        ], "The best-measured norm nudge is a letter. <bookmark mark='a'/> A utility's mailed report compares each "
           "household's energy use with similar neighbours', with a smiley face for the efficient. "
           "<bookmark mark='b'/> Hunt Allcott found that across about six hundred thousand households in randomized "
           "trials, use fell by about two percent. <bookmark mark='c'/> That's small per home, and cheap. Across "
           "millions of homes it adds up, and part of it persisted after the letters stopped. <bookmark mark='d'/> "
           "The effect was larger for heavy users, and the first sites chosen for the programme showed larger "
           "effects than later ones. That's site selection, a lesson for chapter six.",
           tag=published_tag(r"Allcott (2011)"))
