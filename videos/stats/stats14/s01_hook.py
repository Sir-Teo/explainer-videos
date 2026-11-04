from __future__ import annotations

import numpy as np

from videos.stats.stats14.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.teleconference()
        self.chart()
        self.all_flights()
        self.aftermath()
        self.objectives()

    def teleconference(self):
        tl = timeline(lit=(1986,)).to_edge(UP, buff=0.35)
        hc = history_card(1986, r"27 January, \ the evening before the launch of \emph{Challenger}",
                          r"a teleconference between NASA and Morton Thiokol, \ the maker of the solid rocket boosters. \ The "
                          r"forecast for the morning was far colder than any previous launch", color=EVENT, width=10.4, font_size=24).move_to([0, 1.1, 0])
        rows = fit_rows(VGroup(
            label(r"each booster's joints are sealed by rubber O-rings, \ which stiffen in the cold", font_size=24),
            label(r"Thiokol's engineers recommended against launching below 53$^\circ$F, \ the coldest launch so far", font_size=24, color=EVENT),
            label(r"after an off-line caucus, \ Thiokol's managers reversed the recommendation", font_size=24, color=GREY_A),
        ), 12.4, 0.3, [0, -1.6, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the evening of the twenty-seventh of January, 1986, engineers and managers from NASA and "
            "from Morton Thiokol, the company that built the space shuttle's solid rocket boosters, held a teleconference. "
            "The next morning's launch of Challenger was forecast to be far colder than any before it. <bookmark mark='b'/> "
            "The joints between the booster's segments were sealed by rubber O-rings, and rubber stiffens in the cold. "
            "<bookmark mark='c'/> Thiokol's engineers recommended not launching below fifty-three degrees Fahrenheit, the "
            "coldest launch so far. <bookmark mark='d'/> After an off-line caucus, Thiokol's managers reversed the "
            "recommendation. The data at the centre of the argument were a few numbers about past flights."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def chart(self):
        d = load("challenger")
        t, k = np.asarray(d["T"]), np.asarray(d["K"])
        A = axes([50, 85], [0, 3], x_length=7.0, y_length=4.0, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"O-rings with distress",
                 xticks=[50, 55, 60, 65, 70, 75, 80, 85], yticks=[0, 1, 2, 3], center=[-2.4, 0.0, 0])
        ax = A.ax
        inc = k > 0
        seen = {}
        dots = VGroup()
        for a, b in zip(t[inc], k[inc]):
            j = seen.get((a, b), 0)
            seen[(a, b)] = j + 1
            dots.add(Dot(ax.c2p(a, b + 0.12 * j), radius=0.1, color=EVENT))
        rows = fit_rows(VGroup(
            label(r"the flights that had O-ring trouble: \ 7 of them", font_size=24, color=EVENT),
            label(r"distress at 53$^\circ$F, \ but also at 70$^\circ$ and 75$^\circ$", font_size=24),
            MathTex(rf"r = {d['r_incidents']:.2f}", font_size=32),
            label(r"``no correlation with temperature''", font_size=24, color=GREY_A),
            label(r"the argument looked at only the flights with problems", font_size=24, color=OBS),
        ), 4.6, 0.36, [4.4, 0.2, 0])
        tag = historical_tag(r"Dalal, \ Fowlkes \& Hoadley (1989)", corner=DR)
        with self.voiceover(
            "<bookmark mark='a'/> Here is the kind of picture that was discussed: the flights on which O-rings had shown "
            "thermal distress, plotted by launch temperature. There were seven. <bookmark mark='b'/> The coldest, at "
            "fifty-three degrees, had two damaged rings. But so did a flight at seventy-five, and there was damage at seventy "
            "as well. <bookmark mark='c'/> Among these seven flights, the correlation between temperature and damage is "
            "essentially zero. <bookmark mark='d'/> Problems seemed to happen at any temperature. <bookmark mark='e'/> But "
            "the picture shows only the flights that had problems."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.6) for d_ in dots], lag_ratio=0.15), FadeIn(rows[0]))
            for k_, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k_ + 1]))
        self.clear_scene()

    def all_flights(self):
        d = load("challenger")
        t, k = np.asarray(d["T"]), np.asarray(d["K"])
        A = axes([28, 85], [0, 3], x_length=8.0, y_length=3.6, xlabel=r"launch temperature, \ $^\circ$F", ylabel=r"O-rings with distress",
                 xticks=[30, 40, 50, 60, 70, 80], yticks=[0, 1, 2, 3], center=[-1.8, 0.8, 0])
        ax = A.ax
        seen = {}
        inc, non = VGroup(), VGroup()
        for a, b in zip(t, k):
            j = seen.get((a, b), 0)
            seen[(a, b)] = j + 1
            dd = Dot(ax.c2p(a, b + 0.12 * j), radius=0.1, color=EVENT if b > 0 else NOEVENT)
            (inc if b > 0 else non).add(dd)
        cold = Rectangle(width=ax.c2p(65.5, 0)[0] - ax.c2p(28, 0)[0], height=ax.c2p(0, 3)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=S.CTRL, fill_opacity=0.08)
        cold.move_to(ax.c2p(28, 0), aligned_edge=DL)
        launch = DashedLine(ax.c2p(31, 0), ax.c2p(31, 3), color=S.ACCENT, stroke_width=3)
        ll = label(r"31$^\circ$F", font_size=22, color=S.ACCENT).next_to(launch.get_top(), RIGHT, buff=0.12)
        rows = fit_rows(VGroup(
            label(r"add the 16 flights with no distress", font_size=24, color=NOEVENT),
            label(r"every one of them launched at 66$^\circ$F or warmer", font_size=24, color=OBS),
            label(r"below 66$^\circ$F: \ 4 flights, \ 4 with distress", font_size=24, color=EVENT),
            label(r"the morning's forecast: \ about 31$^\circ$F, \ 22 degrees colder than any flight", font_size=24, color=S.ACCENT),
        ), 12.4, 0.24, [0, -2.75, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now add the sixteen flights that had no O-ring distress at all. <bookmark mark='b'/> Every "
            "one of them launched at sixty-six degrees or warmer. <bookmark mark='c'/> Below sixty-six, there were four "
            "flights, and all four had distress. The temperature effect is plain, once the zeros are in the picture. "
            "<bookmark mark='d'/> And the forecast for the launch, in the analysis that statisticians Siddhartha Dalal, "
            "Edward Fowlkes and Bruce Hoadley published three years later, was thirty-one degrees: twenty-two degrees colder "
            "than any shuttle had flown."
        ) as vo:
            self.play(FadeIn(A), FadeIn(inc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.6) for d_ in non], lag_ratio=0.08), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(cold), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(inc, color=EVENT), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(launch), FadeIn(ll), FadeIn(rows[3]))
        self.clear_scene()

    def aftermath(self):
        hc = history_card(1986, r"28 January, \ 11:38 a.m.", r"\emph{Challenger} launched at about 36$^\circ$F. \ A field joint on the "
                          r"right booster failed; \ 73 seconds into the flight the vehicle broke apart, \ and the seven crew were "
                          r"killed", color=EVENT, width=10.4, font_size=24).move_to([0, 1.5, 0])
        rows = fit_rows(VGroup(
            label(r"the Rogers Commission: \ the cause was the O-ring seal, \ made worse by the cold", font_size=24),
            label(r"Richard Feynman, \ at a hearing, \ dropped O-ring rubber in iced water: \ it stayed compressed", font_size=24, color=S.CTRL),
            label(r"Dalal, \ Fowlkes \& Hoadley (1989): \ a logistic model on all 23 flights", font_size=24, color=OBS),
            label(r"Tufte (1997): \ the right chart would have shown it", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the morning of the twenty-eighth of January, Challenger launched at about thirty-six "
            "degrees. A joint on the right booster failed, and seventy-three seconds into the flight the vehicle broke apart. "
            "The seven crew members were killed. <bookmark mark='b'/> The presidential commission that investigated found the "
            "cause in the O-ring seal, made worse by the cold. <bookmark mark='c'/> At one hearing, the physicist Richard "
            "Feynman dropped a piece of the O-ring rubber into a glass of iced water and showed that it didn't spring back. "
            "<bookmark mark='d'/> Three years later Dalal, Fowlkes and Hoadley published the analysis that should have been "
            "possible that night: a logistic regression on all twenty-three flights. <bookmark mark='e'/> And Edward Tufte "
            "later argued that the right chart alone would have shown the danger."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 14", font_size=34, color=GREY_B), label(r"Counts and Categories", font_size=60)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"why least squares fails for yes/no outcomes; \ logistic regression and odds ratios",
            r"fitting by maximum likelihood: \ Newton's method as weighted least squares",
            r"the Challenger fit, \ its intervals, \ and the danger of extrapolating",
            r"Poisson regression with offsets; \ overdispersion",
            r"tables: \ $\chi^2$, \ odds ratios, \ Simpson's paradox, \ Mantel--Haenszel; \ case--control studies; \ scoring predictions",
        ], color=OBS, font_size=26)
        prereq = note(r"prerequisites: \ Parts 10 and 12").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.glm}; \ the Challenger dashboard").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part fourteen: counts and categories. <bookmark mark='b'/> We'll see why least squares "
            "breaks on yes-or-no outcomes, and build logistic regression and the odds ratio; fit it by maximum likelihood, "
            "with Newton's method as a sequence of weighted regressions; redo the Challenger analysis, intervals and all; "
            "regress counts with Poisson models, and meet overdispersion; then read tables: chi-squared, odds ratios, "
            "Simpson's paradox at Berkeley, Mantel and Haenszel's pooling, case–control studies, and how to score a "
            "probability forecast."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
