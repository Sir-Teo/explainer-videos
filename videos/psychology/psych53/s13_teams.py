from __future__ import annotations

from videos.psychology.psych53.common import *  # noqa: F403


class Teams(VoiceoverScene):
    def construct(self):
        card_section(self, 12, r"Satisfaction, \ teams and where people work", r"Is a happy worker a productive one?",
                     scale=("person", "society"))
        self.satisfaction()
        self.safety()
        self.home()

    def satisfaction(self):
        rows_section(self, r"Satisfaction and performance", [
            (r"the ``happy worker'' hypothesis is old, \ and was once declared dead: \ early reviews found tiny "
             r"correlations", WHITE),
            (r"Timothy Judge and colleagues, \ 2001: \ correcting for unreliability across 312 samples, \ the "
             r"correlation is about 0.3", MODEL),
            (r"which direction? \ doing well can make people satisfied as much as the reverse; \ a correlation cannot "
             r"say (Part 2)", AUTH),
            (r"engagement surveys measure the same territory, \ with Part 46's cautions about how questions are "
             r"answered", PERSON),
        ], "Is a happy worker a productive one? <bookmark mark='a'/> The hypothesis is old, and it was once declared "
           "dead, because early reviews found tiny correlations. <bookmark mark='b'/> In 2001 Timothy Judge and "
           "colleagues corrected for unreliability across three hundred and twelve samples, and found a correlation "
           "of about zero point three. <bookmark mark='c'/> But which way does it run? Doing well can make people "
           "satisfied as much as the reverse, and a correlation can't say. <bookmark mark='d'/> Engagement surveys "
           "measure the same territory, with Part 46's cautions about how questions get answered.",
           tag=published_tag(r"Judge et al.\ (2001)"))

    def safety(self):
        rows_section(self, r"Psychological safety", [
            (r"Amy Edmondson, \ 1999: \ in a manufacturing company's teams, \ a shared belief that the team is safe "
             r"for interpersonal risk predicted learning behaviour and performance", WHITE),
            (r"in hospital units she found the better teams reported more errors: \ not because they made more, \ "
             r"but because they were willing to say so", GOOD),
            (r"the link to Part 51: \ crew resource management is psychological safety, \ trained", MODEL),
            (r"most of the evidence is correlational and from surveys; \ interventions that raise it are harder to "
             r"test", PERSON),
        ], "Teams have their own psychology. <bookmark mark='a'/> In 1999 Amy Edmondson found that in a "
           "manufacturing company's teams, a shared belief that the team was safe for interpersonal risk predicted "
           "learning behaviour and performance. <bookmark mark='b'/> In hospital units, she had earlier found that "
           "the better teams reported more errors, not because they made more, but because they were willing to say "
           "so. <bookmark mark='c'/> It's the link to Part 51: crew resource management is psychological safety, "
           "trained. <bookmark mark='d'/> Most of the evidence is correlational and from surveys, and interventions "
           "that raise it are harder to test.", tag=published_tag(r"Edmondson (1999)"))

    def home(self):
        rows_section(self, r"Working from home, \ randomized", [
            (r"Nicholas Bloom and colleagues, \ 2015: \ a Chinese travel company's call-centre staff who volunteered "
             r"were randomized to work from home for nine months", WHITE),
            (r"performance rose by about 13\%, \ mostly more calls from fewer breaks and sick days; \ quitting fell by "
             r"about half", GOOD),
            (r"but promotion rates fell for the home workers, \ and many chose to return to the office afterwards", AUTH),
            (r"later trials of hybrid work found little change in performance and lower quitting: \ the answer "
             r"depends on the job and the arrangement", MODEL),
        ], "And where people work can be randomized. <bookmark mark='a'/> In 2015 Nicholas Bloom and colleagues "
           "reported a trial at a Chinese travel company. Call-centre staff who volunteered were randomized to work "
           "from home for nine months. <bookmark mark='b'/> Performance rose by about thirteen percent, mostly more "
           "calls from fewer breaks and sick days, and quitting fell by about half. <bookmark mark='c'/> But "
           "promotion rates fell for the home workers, and many chose to return to the office afterwards. "
           "<bookmark mark='d'/> Later trials of hybrid work found little change in performance and lower quitting. "
           "The answer depends on the job and the arrangement.", tag=published_tag(r"Bloom et al.\ (2015)"))
