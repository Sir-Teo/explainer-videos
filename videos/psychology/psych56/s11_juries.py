from __future__ import annotations

from videos.psychology.psych56.common import *  # noqa: F403


class Juries(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Juries and judges", r"How are verdicts and sentences reached?",
                     scale=("person", "society"))
        self.story()
        self.hungry()

    def story(self):
        chips_section(self, r"Jurors and judges", [
            (r"the story model", r"Pennington and Hastie: \ jurors build a story from the evidence, \ and choose the "
                                 r"verdict that fits it best; \ evidence presented in story order persuades more", MODEL),
            (r"anchoring", r"Englich, \ Mussweiler and Strack: \ experienced judges' sentences moved toward a number "
                           r"from a die they had thrown themselves (Part 26)", AUTH),
            (r"deliberation", r"groups correct some individual errors and amplify others (Part 34's group "
                              r"polarization)", PERSON),
            (r"instructions", r"jurors told to ignore evidence often cannot (Part 21's misinformation)", SYMP),
        ], "How are verdicts and sentences reached? <bookmark mark='a'/> Nancy Pennington and Reid Hastie's story "
           "model: jurors build a story from the evidence, and choose the verdict that fits it best. Evidence "
           "presented in story order persuades more. <bookmark mark='b'/> Anchoring: Birte Englich, Thomas Mussweiler "
           "and Fritz Strack found that experienced judges' sentences moved toward a number from a die they'd thrown "
           "themselves. That's Part 26. <bookmark mark='c'/> Deliberation: groups correct some individual errors, "
           "and amplify others, as in Part 34's group polarization. <bookmark mark='d'/> And jurors told to ignore "
           "evidence often can't.", tag=published_tag(r"Englich, \ Mussweiler \& Strack (2006)"), chip_w=3.4,
           text_w=8.8)

    def hungry(self):
        rows_section(self, r"Hungry judges?", [
            (r"Danziger, \ Levav and Avnaim-Pesso, \ 2011: \ Israeli parole boards granted about 65\% of requests "
             r"after a food break, \ falling to near zero just before the next", WHITE),
            (r"read as mental fatigue or hunger, \ it became one of psychology's most quoted findings", PERSON),
            (r"Weinshall-Margel and Shapard: \ the order of cases was not random; \ prisoners without lawyers, \ "
             r"usually refused, \ were heard last in each session", AUTH),
            (r"Gl\"ockner's simulations: \ the boards' practice of ending a session before an expected long case "
             r"could produce much of the pattern by itself", MODEL),
            (r"contested: \ the decline is real in the data; \ what causes it is not settled", YOU),
        ], "Then there are the hungry judges. <bookmark mark='a'/> In 2011 Shai Danziger, Jonathan Levav and Liora "
           "Avnaim-Pesso reported that Israeli parole boards granted about sixty-five percent of requests after a "
           "food break, falling to near zero just before the next. <bookmark mark='b'/> Read as mental fatigue or "
           "hunger, it became one of psychology's most quoted findings. <bookmark mark='c'/> But Keren "
           "Weinshall-Margel and John Shapard noted that the order of cases wasn't random. Prisoners without lawyers, "
           "who were usually refused, were heard last in each session. <bookmark mark='d'/> And Andreas Glockner's "
           "simulations showed that the boards' practice of ending a session before an expected long case could "
           "produce much of the pattern by itself. <bookmark mark='e'/> The Ledger says contested. The decline is "
           "real in the data, and what causes it is not settled.", tag=published_tag(r"Danziger et al.\ (2011)"))
