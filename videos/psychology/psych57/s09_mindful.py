from __future__ import annotations

from videos.psychology.psych57.common import *  # noqa: F403


class Mindful(VoiceoverScene):
    def construct(self):
        card_section(self, 8, r"Mindfulness", r"How much of the mindfulness boom is evidence?",
                     scale=("person", "society"))
        self.evidence()
        self.schools()

    def evidence(self):
        rows_section(self, r"The clinical evidence", [
            (r"mindfulness-based cognitive therapy for people with recurrent depression: \ fewer relapses, \ about as "
             r"many as maintenance antidepressants, \ in trials and a meta-analysis", GOOD),
            (r"Goyal and colleagues, \ 2014: \ meditation programmes had small to moderate effects on anxiety, \ "
             r"depression and pain, \ similar to other active treatments", MODEL),
            (r"much of the wider research compares mindfulness with nothing, \ not with an equally credible "
             r"activity: \ chapter three's placebo problem", AUTH),
            (r"adverse effects, \ rarely asked about in trials, \ occur for some participants", PERSON),
        ], "How much of the mindfulness boom is evidence? <bookmark mark='a'/> For people with recurrent depression, "
           "mindfulness-based cognitive therapy reduces relapses, by about as much as maintenance antidepressants, in "
           "trials and a meta-analysis. <bookmark mark='b'/> In 2014 Madhav Goyal and colleagues found that meditation "
           "programmes had small to moderate effects on anxiety, depression and pain, similar to other active "
           "treatments. <bookmark mark='c'/> Much of the wider research compares mindfulness with nothing, not with an "
           "equally credible activity. That's chapter three's placebo problem. <bookmark mark='d'/> And adverse "
           "effects, rarely asked about in trials, do occur for some participants.",
           tag=published_tag(r"Goyal et al.\ (2014)"))

    def schools(self):
        rows_section(self, r"Mindfulness in schools", [
            (r"the MYRIAD trial, \ 2022: \ about 8,000 secondary students in 84 UK schools, \ randomized to "
             r"school-based mindfulness training or usual social-emotional teaching", WHITE),
            (r"no benefit on depression, \ wellbeing or social-emotional outcomes, \ at one year", AUTH),
            (r"few students practised outside the lessons", PERSON),
            (r"an intervention that helps adults who choose it and are at risk may do nothing when given to "
             r"everyone: \ Part 55's scaling, \ in schools", YOU),
        ], "Then came the schools. <bookmark mark='a'/> The MYRIAD trial in 2022 randomized about eight thousand "
           "secondary students in eighty-four UK schools to school-based mindfulness training or usual "
           "social-emotional teaching. <bookmark mark='b'/> There was no benefit on depression, wellbeing or "
           "social-emotional outcomes at one year. <bookmark mark='c'/> Few students practised outside the lessons. "
           "<bookmark mark='d'/> An intervention that helps adults who choose it and are at risk may do nothing when "
           "it's given to everyone. That's Part 55's scaling, in schools.", tag=published_tag(r"Kuyken et al.\ (2022)"))
