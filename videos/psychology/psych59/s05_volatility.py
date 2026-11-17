from __future__ import annotations

from videos.psychology.psych59.common import *  # noqa: F403


class Volatility(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"Learning under uncertainty", r"Does anxiety change how fast people learn?")
        self.browning()
        self.hgf()

    def browning(self):
        rows_section(self, r"Volatility and anxiety", [
            (r"Behrens and colleagues, \ 2007: \ people raise their learning rate when the world is volatile, \ as "
             r"Part 17's Bayesian learner should", WHITE),
            (r"Browning and colleagues, \ 2015: \ in a task alternating stable and volatile blocks, \ people high in "
             r"trait anxiety adjusted their learning rate less", AUTH),
            (r"the account: \ anxiety as a difficulty in using the world's statistics to set how much to learn", MODEL),
            (r"later studies with larger samples found the adjustment deficit inconsistently", PERSON),
        ], "Does anxiety change how fast people learn? <bookmark mark='a'/> In 2007 Timothy Behrens and colleagues "
           "found that people raise their learning rate when the world is volatile, as Part 17's Bayesian learner "
           "should. <bookmark mark='b'/> In 2015 Michael Browning and colleagues found that in a task alternating "
           "stable and volatile blocks, people high in trait anxiety adjusted their learning rate less. "
           "<bookmark mark='c'/> The account: anxiety as a difficulty in using the world's statistics to set how much "
           "to learn. <bookmark mark='d'/> Later studies with larger samples found the deficit inconsistently.",
           tag=published_tag(r"Browning et al.\ (2015)"))

    def hgf(self):
        chips_section(self, r"The hierarchical Gaussian filter, \ in outline", [
            (r"level 1", r"what happens on each trial (reward or not)", PERSON),
            (r"level 2", r"the tendency the outcomes come from, \ drifting over time", MODEL),
            (r"level 3", r"how fast that tendency drifts: \ the volatility", SYMP),
            (r"learning rate", r"falls out of the model: \ higher when volatility is believed high, \ as a Kalman "
                               r"filter's gain", GOOD),
            (r"the parameters", r"how much a person believes the world changes, \ and how fast they update that "
                                r"belief: \ candidate computational targets", AUTH),
        ], "A model built for this is the hierarchical Gaussian filter, here in outline. <bookmark mark='a'/> Level "
           "one is what happens on each trial, reward or not. <bookmark mark='b'/> Level two is the tendency the "
           "outcomes come from, drifting over time. <bookmark mark='c'/> Level three is how fast that tendency "
           "drifts: the volatility. <bookmark mark='d'/> The learning rate falls out of the model, higher when "
           "volatility is believed to be high, like a Kalman filter's gain. <bookmark mark='e'/> And the parameters, "
           "how much a person believes the world changes and how fast they update that belief, are candidate "
           "computational targets.", tag=published_tag(r"Mathys et al.\ (2011)"))
