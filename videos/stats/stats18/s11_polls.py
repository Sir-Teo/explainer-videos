from __future__ import annotations

import numpy as np

from videos.stats.stats18.common import *  # noqa: F403


class Polls(VoiceoverScene):
    def construct(self):
        self.card()
        self.quota()
        self.dewey()
        self.phones()
        self.mar_mnar()
        self.y2016()
        self.y2020()
        self.xbox()
        self.lessons()

    def card(self):
        card = chapter_card(10, r"Polls", r"1948, \ 2016, \ 2020", part=PART)
        with self.voiceover("Chapter ten. Polls."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def quota(self):
        rows = [
            cmath(r"\text{quota sampling}", r":", r"\text{fill quotas by sex, \ age, \ region, \ class}", font_size=30),
            cmath(r"\text{who}", r":", r"\text{the interviewer chooses}", font_size=30),
            cmath(r"\text{risk}", r":", r"\text{within each quota, \ the easy-to-find}", font_size=30),
            cmath(r"\text{error}", r":", r"\text{no probability, \ so no formula}", font_size=30),
        ]
        rows[2][2].set_color(RES)
        whys = [why(r"Gallup's method in 1936"), why(r"not a lottery"), why(r"purposive selection, \ chapter three"),
                why(r"Neyman's objection, \ again")]
        with self.voiceover(
            "Gallup's triumph of 1936 used quota sampling. <bookmark mark='a'/> Each interviewer had to fill quotas: so many "
            "men and women, so many young and old, so many from each region and class. <bookmark mark='b'/> But within the "
            "quotas, the interviewer chose whom to ask. <bookmark mark='c'/> And interviewers, reasonably, chose people who were "
            "easy to find and willing to talk, who differ from those who aren't. <bookmark mark='d'/> It's chapter three's "
            "purposive selection in a new form: no lottery, and so no theory of the error."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.4, buff=0.7, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def dewey(self):
        bars = VGroup(share_bar(0.495 / (0.495 + 0.445), width=8.0, center=[0.6, 1.0, 0], left=RED, right=BLUE),
                      share_bar(0.451 / (0.451 + 0.496), width=8.0, center=[0.6, -0.4, 0], left=RED, right=BLUE))
        names = VGroup(label(r"Gallup's final poll", font_size=24).next_to(bars[0], LEFT, buff=0.3),
                       label(r"the election", font_size=24).next_to(bars[1], LEFT, buff=0.3))
        vals = VGroup(label(r"Dewey 49.5", font_size=20).move_to(bars[0][0]), label(r"Truman 44.5", font_size=20).move_to(bars[0][1]),
                      label(r"Dewey 45.1", font_size=20).move_to(bars[1][0]), label(r"Truman 49.6", font_size=20).move_to(bars[1][1]))
        rows = fit_rows(VGroup(
            label(r"1948: \ Gallup, \ Roper and Crossley all called it for Dewey", font_size=24),
            label(r"quotas; \ polling stopped too early; \ undecideds split as the decided", font_size=22, color=GREY_A),
            label(r"afterwards: \ probability sampling of households", font_size=24, color=HIT),
        ), 12.4, 0.3, [0, -2.3, 0])
        tag = historical_tag(r"Mosteller et al., \ \emph{The Pre-election Polls of 1948} (1949)", corner=UR)
        with self.voiceover(
            "<bookmark mark='a'/> In 1948 quota sampling had its own disaster. Gallup's final poll had Thomas Dewey, the "
            "challenger, at forty-nine and a half percent and President Harry Truman at forty-four and a half. "
            "<bookmark mark='b'/> Truman won, with forty-nine point six. <bookmark mark='c'/> All three major pollsters had "
            "called it for Dewey. A committee of the Social Science Research Council, led by Frederick Mosteller, found several "
            "causes: the quota interviewers' choices, polls that stopped weeks before the vote, and the assumption that the "
            "undecided would split like the decided. <bookmark mark='d'/> Afterwards the pollsters moved to probability samples "
            "of households."
        ) as vo:
            self.add(tag)
            vo.wait_until("a")
            self.play(FadeIn(names[0]), FadeIn(bars[0]), FadeIn(vals[0]), FadeIn(vals[1]))
            vo.wait_until("b")
            self.play(FadeIn(names[1]), FadeIn(bars[1]), FadeIn(vals[2]), FadeIn(vals[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def phones(self):
        yrs = [1997, 2000, 2003, 2006, 2009, 2012, 2016, 2018]
        rr = [36, 28, 25, 21, 15, 9, 9, 6]
        A = axes([1995, 2020], [0, 40], x_length=7.6, y_length=4.0, xlabel=r"year", ylabel=r"response rate, \ \%",
                 xticks=[2000, 2005, 2010, 2015, 2020], yticks=[0, 10, 20, 30, 40], center=[-1.8, 0.3, 0])
        ax = A.ax
        ln = polyline(ax, yrs, rr, RES, 3.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=RES) for a, b in zip(yrs, rr)])
        rows = fit_rows(VGroup(
            label(r"random-digit dialling: \ a probability sample of telephones", font_size=22),
            label(r"Pew's typical telephone survey: \ 36\% (1997) \ to 6\% (2018)", font_size=22, color=RES),
            label(r"a probability sample of the people who answer", font_size=22, color=OBS),
            label(r"so every modern poll is weighted", font_size=22, color=WEIGHT),
        ), 4.4, 0.42, [4.7, 0.3, 0])
        tag = historical_tag(r"Pew Research Center (2019), \ read from its chart", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> From the 1970s, polls dialled telephone numbers at random: a true probability sample of "
            "telephones. <bookmark mark='b'/> But people stopped answering. The Pew Research Center's typical telephone survey "
            "reached thirty-six percent of the people it tried in 1997, and six percent by 2018. <bookmark mark='c'/> A random "
            "sample with six percent response is a probability sample of the people who answer the phone, and Meng's "
            "correlation is back. <bookmark mark='d'/> So every modern poll is weighted, and its accuracy depends on whether "
            "the weighting variables capture who answers."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.15), FadeIn(rows[1]))
            for k, m_ in enumerate("cd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def mar_mnar(self):
        d = load("polls")
        A = axes([0.36, 0.53], [0, 4], x_length=8.0, y_length=3.0, xlabel=r"Blue's share, \ average of 200 polls",
                 xticks=[0.38, 0.42, 0.46, 0.5], center=[1.9, 0.8, 0], xfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        tr = DashedLine(ax.c2p(d["truth"], 0), ax.c2p(d["truth"], 3.8), color=S.TRUTH, stroke_width=3)
        trl = label(r"truth", font_size=20, color=S.TRUTH).next_to(ax.c2p(d["truth"], 3.8), UP, buff=0.05)

        def arrow(a, b, y, col):
            return Arrow(ax.c2p(a, y), ax.c2p(b, y), buff=0.0, color=col, stroke_width=5, max_tip_length_to_length_ratio=0.15)

        a1 = arrow(d["mar"]["raw"], d["mar"]["raked"], 2.6, HIT)
        a2 = arrow(d["mnar"]["raw"], d["mnar"]["raked"], 1.2, RES)
        l1 = label(r"answering depends on income and age", font_size=20, color=HIT).next_to(ax.c2p(0.36, 2.6), LEFT, buff=0.15)
        l2 = label(r"... and on the vote", font_size=20, color=RES).next_to(ax.c2p(0.36, 1.2), LEFT, buff=0.15)
        rows = fit_rows(VGroup(
            MathTex(rf"\text{{raw}}\ {100 * d['mar']['raw']:.1f}\% \to \text{{raked}}\ {100 * d['mar']['raked']:.1f}\%", font_size=26, color=HIT),
            MathTex(rf"\text{{raw}}\ {100 * d['mnar']['raw']:.1f}\% \to \text{{raked}}\ {100 * d['mnar']['raked']:.1f}\%", font_size=26, color=RES),
            label(r"20,000 numbers dialled; \ about 8--11\% answer; \ raked to income, \ age and region", font_size=20, color=GREY_A),
        ), 12.4, 0.3, [0, -2.0, 0])
        tag = simulated_tag(r"the World's polling firm", corner=DR)
        with self.voiceover(
            "The World can show why. Its polling firm dials twenty thousand random numbers; about one in ten answers. "
            "<bookmark mark='a'/> First suppose answering depends only on income and age. The raw poll overstates Blue at "
            "forty-two percent; raked to income, age and region it comes back to thirty-nine, close to the truth of "
            "thirty-eight. <bookmark mark='b'/> Now suppose answering also depends on the vote, as it does among the World's "
            "Digest readers. The raw poll says fifty-one, and weighting only brings it to forty-eight. "
            "<bookmark mark='c'/> The same weighting, the same response rate; the difference is whether the response depends on "
            "the answer once the weights' variables are accounted for."
        ) as vo:
            self.play(FadeIn(A), Create(tr), FadeIn(trl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(l1), GrowArrow(a1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(l2), GrowArrow(a2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def y2016(self):
        rows = fit_rows(VGroup(
            label(r"2016: \ national polls were close: \ Clinton won the popular vote by 2.1 points", font_size=24),
            label(r"state polls in the upper Midwest underestimated Trump", font_size=24, color=RES),
            label(r"AAPOR's review (2017): \ late deciders broke for Trump", font_size=22),
            label(r"and many state polls didn't weight by education", font_size=22, color=OBS),
            label(r"college graduates answer polls more, \ and voted Clinton", font_size=22, color=GREY_A),
        ), 12.4, 0.48, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2016, national polls in the United States were close to the result: Hillary Clinton won "
            "the popular vote by two point one points, and the polls averaged about three. <bookmark mark='b'/> But state polls "
            "in Michigan, Wisconsin and Pennsylvania underestimated Donald Trump, and those states decided the election. "
            "<bookmark mark='c'/> The American Association for Public Opinion Research's review found two main causes. Voters "
            "who decided late broke for Trump. <bookmark mark='d'/> And many state polls didn't weight by education, "
            "<bookmark mark='e'/> although college graduates are more likely to answer polls, and that year voted heavily for "
            "Clinton. A missing weighting variable, exactly chapter nine's lesson."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def y2020(self):
        rows = fit_rows(VGroup(
            label(r"2020: \ the national polls overstated Biden's margin by 3.9 points", font_size=24, color=RES),
            label(r"AAPOR (2021): \ the largest error in 40 years", font_size=22),
            label(r"education weighting was in place; \ late deciders didn't explain it", font_size=22, color=GREY_A),
            label(r"the likely cause: \ Trump supporters were less likely to respond, \ within every weighting cell", font_size=22,
                  color=OBS),
            label(r"missing not at random: \ the Digest's problem, \ in miniature", font_size=24, color=RES),
        ), 12.4, 0.48, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2020 the national polls overstated Joe Biden's winning margin by about three point nine "
            "points, <bookmark mark='b'/> the largest polling error in forty years, according to AAPOR's 2021 task force. "
            "<bookmark mark='c'/> This time most polls did weight by education, and late deciders didn't explain the miss. "
            "<bookmark mark='d'/> The task force couldn't prove a cause, but the leading explanation was that Trump's supporters "
            "were less likely to take part in polls, even after accounting for age, education and everything else the polls "
            "weighted on. <bookmark mark='e'/> Nonresponse that depends on the answer itself: the Digest's problem, eighty-four "
            "years later, at a small fraction of the size, and still beyond the reach of weighting."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def xbox(self):
        rows = fit_rows(VGroup(
            label(r"2012: \ an opt-in poll on Microsoft's Xbox games console", font_size=24),
            label(r"345,858 interviews; \ 93\% of respondents men, \ two thirds aged 18--29", font_size=22, color=RES),
            label(r"raw: \ badly skewed toward Romney", font_size=22, color=GREY_A),
            label(r"multilevel regression and post-stratification to the electorate", font_size=22, color=WEIGHT),
            label(r"close to the result, \ and to the best probability polls", font_size=22, color=HIT),
            label(r"Wang, \ Rothschild, \ Goel \& Gelman (2015): \ the model does the work the lottery can't", font_size=20, color=GREY_B),
        ), 12.4, 0.42, [0, 0, 0])
        with self.voiceover(
            "Can a self-selected sample ever be rescued? Sometimes, with a strong model. <bookmark mark='a'/> In 2012 a poll was "
            "run on Microsoft's Xbox games console, open to anyone who wanted to answer. <bookmark mark='b'/> It collected three "
            "hundred and forty-five thousand interviews from respondents who were ninety-three percent men and mostly young: "
            "about as unrepresentative as a poll can be. <bookmark mark='c'/> Taken raw, it favoured Mitt Romney. "
            "<bookmark mark='d'/> Wei Wang, Andrew Gelman and colleagues fitted a multilevel regression of vote on demographics "
            "and then post-stratified it to the composition of the electorate. <bookmark mark='e'/> Their estimates came close "
            "to the result, and to the best probability polls. <bookmark mark='f'/> The model did the work the lottery couldn't, "
            "which only succeeds if, within its cells, the people who answered resemble those who didn't. Part 25 builds the "
            "method."
        ) as vo:
            for k, m_ in enumerate("abcdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lessons(self):
        rows = fit_rows(VGroup(
            label(r"ask how the sample was chosen before asking how big it is", font_size=24),
            label(r"a margin of error covers sampling error only", font_size=24, color=GREY_A),
            label(r"random selection is what makes the data defect correlation vanish", font_size=24, color=HIT),
            label(r"nonresponse brings it back; \ weighting fixes only what it can see", font_size=24, color=RES),
            label(r"next: \ models of the population can help: \ MRP (Part 25), \ missing data (Part 41)", font_size=22, color=WEIGHT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> So: ask how a sample was chosen before you ask how big it is. <bookmark mark='b'/> A margin of "
            "error covers sampling error only. <bookmark mark='c'/> Random selection is what makes the data defect correlation "
            "vanish, <bookmark mark='d'/> nonresponse brings it back, and weighting fixes only what it can see. "
            "<bookmark mark='e'/> Models of the population can help further: multilevel regression and post-stratification in "
            "Part 25, and the theory of missing data in Part 41."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
