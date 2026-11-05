from __future__ import annotations

import numpy as np

from explainer.stats.world import World
from videos.stats.stats18.common import *  # noqa: F403


class DesignBased(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.purposive()
        self.principle()
        self.superpop()
        self.lottery()
        self.contrast()

    def card(self):
        card = chapter_card(3, r"Design-based inference", r"The randomness is in the selection", lit=(1934,), part=PART)
        with self.voiceover("Chapter three. Design-based inference."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def history(self):
        rows = fit_rows(VGroup(
            label(r"1895: \ Anders Kiær, \ Norway's statistics office: \ the ``representative method''", font_size=24),
            label(r"a partial count can stand for a census, \ if the parts are chosen to resemble the whole", font_size=22,
                  color=GREY_A),
            label(r"1912: \ Arthur Bowley, \ Reading: \ one house in twenty from the street lists", font_size=24, color=HIT),
            label(r"and an estimate of his error, \ from the theory of chance", font_size=22, color=GREY_A),
            label(r"1934: \ Jerzy Neyman: \ random selection, \ stratification, \ and confidence intervals", font_size=24, color=OBS),
        ), 12.4, 0.42, [0, 0.2, 0])
        with self.voiceover(
            "Sampling a population, rather than counting it, was once controversial. <bookmark mark='a'/> In 1895 Anders "
            "Kiær, director of Norway's statistics office, proposed his representative method to the International Statistical "
            "Institute: <bookmark mark='b'/> a partial count could stand for a full census, if the parts were chosen to "
            "resemble the whole. Many delegates thought anything short of a complete count unscientific. "
            "<bookmark mark='c'/> In 1912 Arthur Bowley surveyed working-class households in Reading, taking one house in twenty "
            "from the street lists, a selection free of the surveyor's judgment, <bookmark mark='d'/> and attached to his estimates a margin of error from the theory of "
            "chance. <bookmark mark='e'/> In 1934 Jerzy Neyman, in London, settled the argument with a paper on the two ways of "
            "choosing a representative sample: random selection, or deliberately picking units to match the population."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def purposive(self):
        rows = fit_rows(VGroup(
            label(r"purposive selection: \ Gini \& Galvani's sample of the 1921 Italian census", font_size=24),
            label(r"29 of 214 districts, \ chosen so their averages matched the nation's on several controls", font_size=22),
            label(r"the controls matched; \ other characteristics did not", font_size=24, color=RES),
            label(r"Neyman: \ with purposive choice, \ there is no way to say how far off you might be", font_size=24, color=OBS),
            label(r"random choice gives both an estimate and its error", font_size=24, color=HIT),
        ), 12.4, 0.48, [0, 0, 0])
        with self.voiceover(
            "Neyman's main exhibit was a careful purposive sample. <bookmark mark='a'/> Corrado Gini and Luigi Galvani had "
            "summarized the 1921 Italian census by keeping the returns of a sample of districts, <bookmark mark='b'/> twenty-nine "
            "of two hundred and fourteen, chosen so that their averages matched the country's on several control variables. "
            "<bookmark mark='c'/> The controls matched. But on other characteristics, the sample was far off. "
            "<bookmark mark='d'/> Neyman's point was that with purposive selection there's no theory of the error: nothing "
            "tells you how far off you might be on the things you didn't control. <bookmark mark='e'/> Random selection gives "
            "both an estimate and a measure of its error, and that's why it won."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def principle(self):
        rows = [
            cmath(r"y_1, \ldots, y_N", r":", r"\text{fixed numbers, \ not random}", font_size=32),
            cmath(r"\text{the design}", r":", r"p(s) = P(\text{sample } s \text{ is chosen}),\ \ \text{known}", font_size=30),
            cmath(r"E_p[\hat\theta]", r"=", r"\textstyle\sum_s p(s)\,\hat\theta(s)", font_size=32),
            cmath(r"\text{no model}", r":", r"\text{the probability statements come from the lottery}", font_size=30),
        ]
        rows[3][2].set_color(OBS)
        whys = [why(r"the World's votes: \ what they are"), why(r"the statistician's own randomization"),
                why(r"average over the samples we might have drawn"), why(r"as Part 13's randomization test did for experiments")]
        with self.voiceover(
            "The logic of design-based inference is worth stating carefully, because it differs from everything since Part 8. "
            "<bookmark mark='a'/> The population's values are fixed numbers: the World's votes are what they are. Nothing about "
            "them is random. <bookmark mark='b'/> What's random is the sample, chosen by a lottery the statistician designs, "
            "with known probabilities for every possible sample. <bookmark mark='c'/> An estimator's expectation and variance "
            "are averages over the samples the lottery might have produced. <bookmark mark='d'/> So no model for the data is "
            "needed: the probability in a confidence statement comes from the lottery itself, just as in Part 13 the "
            "probability came from randomizing treatments."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def superpop(self):
        rows = [
            cmath(r"\text{finite population}", r":", r"\text{the 741,311 adults; \ a census would end all doubt}", font_size=28),
            cmath(r"\text{superpopulation}", r":", r"\text{a process that could have produced other populations}", font_size=28),
            cmath(r"\text{survey question}", r":", r"\text{what share of these people vote Blue?}", font_size=28),
            cmath(r"\text{scientific question}", r":", r"\text{how does income affect the vote?}", font_size=28),
        ]
        rows[2][2].set_color(HIT)
        rows[3][2].set_color(OBS)
        whys = [why(r"the World as it is"), why(r"the laws the World was drawn from"),
                why(r"descriptive: \ design-based inference fits"), why(r"a model's parameter: \ Parts 22--24")]
        with self.voiceover(
            "<bookmark mark='a'/> There's a subtlety about what is being estimated. A survey targets a finite population: these "
            "seven hundred and forty-one thousand adults, about whom a complete census would settle every question. "
            "<bookmark mark='b'/> Most of this course has targeted something else: a superpopulation, the process that could have "
            "produced many populations, like the laws from which the World itself was drawn. <bookmark mark='c'/> What share of "
            "these people will vote Blue is a question about the finite population, and design-based inference answers it "
            "with no model. <bookmark mark='d'/> How income affects voting is a question about the process, and needs a "
            "model, which is what Parts 22 to 24 take up. Being clear about which question you're asking decides which "
            "uncertainty you should report."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def lottery(self):
        Wd = World()
        mp = IslandMap(Wd.towns, center=[-2.4, 0.0, 0], scale=0.72)
        g = np.random.Generator(np.random.PCG64(1934))
        rows = fit_rows(VGroup(
            label(r"every adult has a ticket", font_size=24),
            label(r"draw 1,000 tickets at random", font_size=24, color=RESP),
            label(r"draw again: \ a different sample, \ a different estimate", font_size=24),
            label(r"the spread of those estimates is the error we report", font_size=24, color=HIT),
        ), 4.6, 0.45, [4.6, 0.2, 0])
        pops = np.asarray(Wd.towns["weight"])
        with self.voiceover(
            "<bookmark mark='a'/> Picture it on the island. Every adult has a ticket. <bookmark mark='b'/> Draw a thousand at "
            "random: here are the towns they live in, roughly in proportion to the towns' sizes. <bookmark mark='c'/> Draw again "
            "and you get different people and a different estimate. <bookmark mark='d'/> The spread of those estimates over all "
            "the samples the lottery could produce is the uncertainty we report. It's a property of the procedure, which we "
            "control, not of the population, which we can't see."
        ) as vo:
            self.play(Create(mp.coast), FadeIn(mp.dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            pick = g.choice(200, 25, replace=False, p=pops)
            self.play(mp.highlight(pick, RESP), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(*[d.animate.set_color(GREY_B).set_opacity(0.4).scale(1 / 1.4) if i in set(pick) else d.animate.set_opacity(0.4)
                        for i, d in enumerate(mp.dots)], run_time=0.6)
            pick2 = g.choice(200, 25, replace=False, p=pops)
            self.play(*[mp.dots[i].animate.set_color(HIT).set_opacity(1).scale(1.4) for i in pick2], FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def contrast(self):
        tab = table_rows([
            [r"", r"design-based", r"model-based"],
            [r"random", r"who is sampled", r"the values $y_i$"],
            [r"needs", r"known selection probabilities", r"a model for $y$"],
            [r"robust to", r"any population", r"the model being right"],
            [r"fails when", r"people select themselves", r"the model is wrong"],
        ], font_size=26, colors=[GREY_B, None, None, None, RES]).move_to([0, 0.6, 0])
        foot = label(r"weighting and multilevel models (Parts 25, \ 41) blend the two", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "<bookmark mark='a'/> It helps to set the two views side by side. In design-based inference the randomness is in who "
            "is sampled; in model-based inference, in the values themselves. <bookmark mark='b'/> The first needs known "
            "selection probabilities; the second, a model for y. <bookmark mark='c'/> The first holds for any population; the "
            "second, only if the model is right. <bookmark mark='d'/> And each has its failure: design-based inference breaks "
            "when people select themselves, as in the Digest, because the selection probabilities are no longer known; "
            "model-based inference breaks when the model is wrong. <bookmark mark='e'/> Modern survey practice blends them, as "
            "Parts 25 and 41 will show."
        ) as vo:
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
