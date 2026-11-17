from __future__ import annotations

from videos.psychology.psych55.common import *  # noqa: F403


class Persuasion(VoiceoverScene):
    def construct(self):
        card_section(self, 9, r"Persuasion at scale", r"How much do campaigns and ads change minds?", scale=("society",))
        self.campaigns()
        self.ads()

    def campaigns(self):
        rows_section(self, r"Campaign contact", [
            (r"Kalla and Broockman, \ 2018: \ a meta-analysis of 49 field experiments on campaign contact in US "
             r"elections", WHITE),
            (r"in general elections, \ the average persuasion effect of canvassing, \ mail and calls was essentially "
             r"zero", AUTH),
            (r"effects appeared early in a campaign and vanished by election day, \ or where candidates took unusual "
             r"positions", MODEL),
            (r"turnout is easier to move than choice; \ preferences in a polarized election are hard to shift", PERSON),
        ], "How much do campaigns change minds? <bookmark mark='a'/> In 2018 Joshua Kalla and David Broockman pooled "
           "forty-nine field experiments on campaign contact in American elections. <bookmark mark='b'/> In general "
           "elections, the average persuasion effect of canvassing, mail and calls was essentially zero. "
           "<bookmark mark='c'/> Effects appeared early in a campaign and vanished by election day, or appeared where "
           "candidates took unusual positions. <bookmark mark='d'/> Turnout is easier to move than choice, and "
           "preferences in a polarized election are hard to shift.", tag=published_tag(r"Kalla \& Broockman (2018)"))

    def ads(self):
        rows_section(self, r"Does advertising work?", [
            (r"Lewis and Rao, \ 2015: \ in 25 large online advertising experiments, \ the effect on sales was so "
             r"small relative to the noise in sales that most were nearly impossible to measure", WHITE),
            (r"a campaign that pays for itself may need millions of people per arm to show it", MODEL),
            (r"search ads for a famous brand mostly reached people who would have clicked the free link anyway "
             r"(Blake, \ Nosko and Tadelis, \ 2015)", AUTH),
            (r"Part 4's power analysis, \ applied to marketing: \ most claimed returns were never measurable", YOU),
        ], "And advertising? <bookmark mark='a'/> In 2015 Randall Lewis and Justin Rao analysed twenty-five large "
           "online advertising experiments. The effect on sales was so small relative to the noise in sales that most "
           "were nearly impossible to measure. <bookmark mark='b'/> A campaign that pays for itself may need millions "
           "of people per arm to show it. <bookmark mark='c'/> And search ads for a famous brand mostly reached "
           "people who'd have clicked the free link anyway, as Thomas Blake, Chris Nosko and Steven Tadelis found. "
           "<bookmark mark='d'/> It's Part 4's power analysis, applied to marketing. Most claimed returns were never "
           "measurable.", tag=published_tag(r"Lewis \& Rao (2015)"))
