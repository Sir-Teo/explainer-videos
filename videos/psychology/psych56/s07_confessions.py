from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Confessions(VoiceoverScene):
    def construct(self):
        card_section(self, 6, r"False confessions", r"Why would an innocent person confess?")
        self.alt()
        self.tactics()
        self.peace()

    def alt(self):
        rows_section(self, r"The ALT key", [
            (r"Kassin and Kiechel, \ 1996: \ students typing letters were warned not to press the ALT key, \ or the "
             r"computer would crash; \ it crashed, \ and they were accused", WHITE),
            (r"none had pressed it; \ asked to sign a confession, \ about two thirds signed", AUTH),
            (r"when a confederate said she had seen them press it (false evidence) and the pace was fast, \ nearly "
             r"all signed, \ and some came to believe it", PERSON),
            (r"a laboratory confession costs nothing; \ the point is the mechanism: \ false evidence and pressure "
             r"change what people say, \ and sometimes what they remember", MODEL),
        ], "Why would an innocent person confess? <bookmark mark='a'/> In 1996 Saul Kassin and Katherine Kiechel had "
           "students type letters, warned that pressing the ALT key would crash the computer. It crashed, and they "
           "were accused. <bookmark mark='b'/> None had pressed it. Asked to sign a confession, about two thirds "
           "signed. <bookmark mark='c'/> When a confederate said she'd seen them press it, false evidence, and the "
           "pace was fast, nearly all signed, and some came to believe it. <bookmark mark='d'/> A laboratory "
           "confession costs nothing. The point is the mechanism: false evidence and pressure change what people "
           "say, and sometimes what they remember.", tag=published_tag(r"Kassin \& Kiechel (1996)"))

    def tactics(self):
        chips_section(self, r"How interrogation produces them", [
            (r"isolation and time", r"hours of questioning; \ confessions in exonerations followed long "
                                    r"interrogations", AUTH),
            (r"the false evidence ploy", r"lying about evidence is legal in some countries, \ including the US: \ it "
                                         r"shifts the suspect's calculation of what is hopeless", PERSON),
            (r"minimization", r"suggesting leniency without promising it: \ ``anyone would have done it''", MODEL),
            (r"the vulnerable", r"young people and those with intellectual disability confess falsely more often", SYMP),
            (r"the jury", r"a confession weighs with jurors more than almost any other evidence, \ even when they "
                          r"are told it was coerced", GOOD),
        ], "How does interrogation produce false confessions? <bookmark mark='a'/> Isolation and time: confessions in "
           "the exoneration cases followed long interrogations. <bookmark mark='b'/> The false evidence ploy: lying "
           "about evidence is legal in some countries, including the United States, and it shifts the suspect's "
           "sense of what is hopeless. <bookmark mark='c'/> Minimization: suggesting leniency without promising it, "
           "like anyone would have done it. <bookmark mark='d'/> Young people and those with intellectual disability "
           "confess falsely more often. <bookmark mark='e'/> And then the jury: a confession weighs with jurors more "
           "than almost any other evidence, even when they're told it was coerced.", tag=published_tag(r"Kassin et al.\ (2010)"), chip_w=4.2, text_w=8.0)

    def peace(self):
        chips_section(self, r"Interviewing, \ not interrogating", [
            (r"England and Wales", r"after false confessions in the 1970s and 1980s, \ police adopted the PEACE "
                                   r"model in the early 1990s, \ with interviews recorded", MODEL),
            (r"PEACE", r"Preparation and planning, \ Engage and explain, \ Account, \ Closure, \ Evaluate: \ the "
                       r"aim is information, \ not a confession", GOOD),
            (r"the evidence", r"Meissner and colleagues' 2014 review: \ information-gathering interviews kept true "
                              r"confessions and reduced false ones, \ compared with accusatory methods", PERSON),
            (r"recording", r"a full recording lets a court see what was said to the suspect, \ not only what the "
                           r"suspect said", AUTH),
        ], "What's the alternative? <bookmark mark='a'/> After false confessions in the nineteen seventies and "
           "eighties, police in England and Wales adopted the PEACE model in the early nineteen nineties, with "
           "interviews recorded. <bookmark mark='b'/> PEACE stands for preparation and planning, engage and explain, "
           "account, closure, and evaluate. The aim is information, not a confession. <bookmark mark='c'/> In 2014 "
           "Christian Meissner and colleagues reviewed the experiments: information-gathering interviews kept true "
           "confessions and reduced false ones, compared with accusatory methods. <bookmark mark='d'/> And a full "
           "recording lets a court see what was said to the suspect, not only what the suspect said.",
           chip_w=3.8, text_w=8.4)
