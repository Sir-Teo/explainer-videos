from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Backfire(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"When nudges backfire", r"Can a well-meant message make things worse?")
        self.signs()
        self.norms()

    def signs(self):
        rows_section(self, r"Fatality counts on highway signs", [
            (r"Texas displayed the year's road death toll on motorway message boards, \ one week a month", WHITE),
            (r"Hall and Madsen, \ 2022: \ crashes rose in the stretches after the signs on the weeks they showed the "
             r"toll, \ more when the number was larger", AUTH),
            (r"their reading: \ the message distracted drivers, \ a load on attention (Part 18) at the wrong "
             r"moment", MODEL),
            (r"a message is also a stimulus: \ it costs attention whether or not it persuades", YOU),
        ], "Can a well-meant message make things worse? <bookmark mark='a'/> Texas displayed the year's road death "
           "toll on motorway message boards, one week each month. <bookmark mark='b'/> In 2022 Jonathan Hall and "
           "Joshua Madsen found that crashes rose in the stretches after the signs, in the weeks they showed the "
           "toll, and more when the number was larger. <bookmark mark='c'/> Their reading: the message distracted "
           "drivers, a load on attention at the wrong moment. That's Part 18. <bookmark mark='d'/> A message is also "
           "a stimulus. It costs attention whether or not it persuades.", tag=published_tag(r"Hall \& Madsen (2022)"))

    def norms(self):
        chips_section(self, r"Norms that license", [
            (r"the boomerang", r"in the energy studies, \ households told they used less than their neighbours began "
                               r"to use more (Schultz and colleagues, \ 2007)", AUTH),
            (r"the fix", r"a smiley face for the efficient: \ an injunctive norm (approval) on top of the descriptive "
                         r"one", GOOD),
            (r"the wrong norm", r"``many people evade taxes'' tells people that evasion is normal", PERSON),
            (r"reactance", r"pressure that feels like control invites doing the opposite", MODEL),
        ], "Norms can license the wrong behaviour. <bookmark mark='a'/> In the energy studies of Wesley Schultz and "
           "colleagues, households told they used less than their neighbours began to use more. "
           "<bookmark mark='b'/> The fix was a smiley face for the efficient: an injunctive norm, approval, on top of "
           "the descriptive one. <bookmark mark='c'/> A message that many people evade taxes tells people evasion is "
           "normal. <bookmark mark='d'/> And pressure that feels like control invites doing the opposite. "
           "Psychologists call it reactance.", tag=published_tag(r"Schultz et al.\ (2007)"))
