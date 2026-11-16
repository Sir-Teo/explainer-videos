from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Incentives(VoiceoverScene):
    def construct(self):
        card_section(self, 7, r"Incentives", r"Does paying people to change work, \ and does it last?")
        self.smoking()
        self.habits()

    def smoking(self):
        rows_section(self, r"Paying smokers to quit", [
            (r"Volpp and colleagues, \ 2009: \ employees offered up to \$750 to quit smoking quit about three times "
             r"as often as those given information alone", WHITE),
            (r"Halpern and colleagues, \ 2015: \ deposit contracts (your own money at stake) were taken up less, \ "
             r"but worked well for those who took them", MODEL),
            (r"abstinence fell after the payments ended, \ but a gap persisted", PERSON),
            (r"money works when the behaviour is checkable and the payment is soon: \ Part 16's reinforcement, \ at "
             r"work (contingency management in Part 41)", GOOD),
        ], "Does paying people to change work, and does it last? <bookmark mark='a'/> In 2009 Kevin Volpp and "
           "colleagues offered employees up to seven hundred and fifty dollars to quit smoking. They quit about three "
           "times as often as those given information alone. <bookmark mark='b'/> In 2015 Scott Halpern and "
           "colleagues compared deposit contracts, with the smoker's own money at stake. Fewer people took them up, "
           "but they worked well for those who did. <bookmark mark='c'/> Abstinence fell after the payments ended, "
           "but a gap persisted. <bookmark mark='d'/> Money works when the behaviour can be checked and the payment "
           "comes soon. That's Part 16's reinforcement, and Part 41's contingency management.",
           tag=published_tag(r"Volpp et al.\ (2009)"))

    def habits(self):
        rows_section(self, r"Paying for exercise", [
            (r"Charness and Gneezy, \ 2009: \ students paid to attend the gym eight times in a month went more "
             r"afterwards too, \ mostly those who had not gone before", WHITE),
            (r"later and larger studies found smaller persistence: \ most of the extra visits stop when the money "
             r"does", AUTH),
            (r"Part 52's habits take months; \ a month of payment is short", MODEL),
            (r"the design question is the end: \ taper, \ hand over to a commitment device, \ or accept a temporary "
             r"effect", YOU),
        ], "What about exercise? <bookmark mark='a'/> In 2009 Gary Charness and Uri Gneezy paid students to go to the "
           "gym eight times in a month, and they went more afterwards too, mostly those who hadn't gone before. "
           "<bookmark mark='b'/> Later and larger studies found smaller persistence. Most of the extra visits stop "
           "when the money does. <bookmark mark='c'/> Part 52's habits take months, and a month of payment is short. "
           "<bookmark mark='d'/> So the design question is the ending: taper, hand over to a commitment device, or "
           "accept a temporary effect.", tag=published_tag(r"Charness \& Gneezy (2009)"))
