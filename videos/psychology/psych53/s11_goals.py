from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Goals(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Goals", r"Does ``do your best'' get people's best?")
        self.theory()
        self.limits()

    def theory(self):
        rows_section(self, r"Goal-setting theory", [
            (r"Edwin Locke and Gary Latham, \ from the 1960s: \ specific, \ difficult goals lead to higher performance "
             r"than ``do your best''", WHITE),
            (r"hundreds of studies, \ in laboratories and workplaces, \ found the effect: \ one of the most replicated "
             r"in work psychology", GOOD),
            (r"how it works: \ a goal directs attention, \ raises effort, \ sustains persistence and prompts "
             r"strategies (Part 28's motivation)", MODEL),
            (r"it needs commitment and feedback: \ a goal no one accepts, \ or progress no one can see, \ does "
             r"little", PERSON),
        ], "Does do your best get people's best? <bookmark mark='a'/> From the nineteen sixties, Edwin Locke and Gary "
           "Latham found that specific, difficult goals lead to higher performance than do your best. "
           "<bookmark mark='b'/> Hundreds of studies, in laboratories and workplaces, found the effect. It's one of "
           "the most replicated results in work psychology. <bookmark mark='c'/> A goal directs attention, raises "
           "effort, sustains persistence, and prompts people to look for strategies: Part 28's motivation, at work. "
           "<bookmark mark='d'/> But it needs commitment and feedback. A goal no one accepts, or progress no one can "
           "see, does little.", tag=published_tag(r"Locke \& Latham (2002)"))

    def limits(self):
        chips_section(self, r"When goals go wrong", [
            (r"complex tasks", r"a hard performance goal on a task people have not yet learned can hurt: \ set "
                               r"learning goals first", AUTH),
            (r"narrow targets", r"what is counted improves; \ what is not counted can be neglected or gamed "
                                r"(Goodhart's law)", PERSON),
            (r"cheating", r"people just short of a goal are more likely to misreport (Schweitzer and colleagues)", MODEL),
            (r"the design", r"several goals, \ including quality, \ with honest measurement and room to learn", GOOD),
        ], "Goals can also go wrong. <bookmark mark='a'/> A hard performance goal on a task people haven't learned "
           "yet can hurt. Set learning goals first. <bookmark mark='b'/> What's counted improves, and what isn't "
           "counted can be neglected or gamed. That's Goodhart's law. <bookmark mark='c'/> People just short of a "
           "goal are more likely to misreport, as Maurice Schweitzer and colleagues found. <bookmark mark='d'/> So "
           "design several goals, including quality, with honest measurement and room to learn.")
