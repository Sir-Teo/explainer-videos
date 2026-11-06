from __future__ import annotations

import numpy as np

from videos.stats.stats37.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.streets()
        self.table()
        self.grand()
        self.question()
        self.objectives()

    def story(self):
        tl = timeline(lit=(1855,)).to_edge(UP, buff=0.35)
        hc = history_card(1855, r"John Snow, \ \emph{On the Mode of Communication of Cholera}, \ second edition",
                          r"In 1854 cholera returned to London. \ Snow believed it spread through water fouled by the "
                          r"evacuations of the sick, \ against the reigning theory of miasma, \ bad air. \ South of the "
                          r"Thames two companies supplied water: \ one drew it below the city's sewer outfalls, \ the other "
                          r"had moved its intake upstream two years before",
                          color=Y1C, width=11.2, font_size=22).move_to([0, 0.9, 0])
        rows = fit_rows(VGroup(
            label(r"Southwark \& Vauxhall: \ the Thames at Battersea, \ downstream of the sewers", font_size=24, color=Y1C),
            label(r"Lambeth: \ since 1852, \ the Thames at Thames Ditton, \ above the tide and the sewage", font_size=24, color=Y0C),
        ), 12.0, 0.35, [0, -1.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In the summer of 1854 cholera returned to London. The physician John Snow had argued for "
            "years that it spread through water contaminated by the evacuations of the sick, against the reigning theory "
            "that disease rose from miasma, bad air. That September he traced an outbreak in Soho to a single pump on Broad "
            "Street. But his strongest evidence came from south of the river. <bookmark mark='b'/> There, two companies "
            "supplied water. The Southwark and Vauxhall Company drew it from the Thames at Battersea, downstream of the "
            "city's sewer outfalls. <bookmark mark='c'/> The Lambeth Company, in 1852, had moved its intake upstream to Thames "
            "Ditton, above the reach of the tide and of London's sewage."
        ) as vo:
            self.play(FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def streets(self):
        g = np.random.default_rng(1855)
        cols, rws = 26, 9
        lam = g.random((rws, cols)) < 0.40
        cell, gap = 0.36, 0.1
        houses = VGroup()
        for i in range(rws):
            for j in range(cols):
                c = Y0C if lam[i, j] else Y1C
                houses.add(Square(side_length=cell, stroke_width=1.2, stroke_color=c, fill_color=c, fill_opacity=0.25)
                           .move_to([(j - cols / 2 + 0.5) * (cell + gap), (rws / 2 - i - 0.5) * (cell + gap) + 0.6, 0]))
        # deaths, at the rates of Table IX (scaled up 6x so that a few hundred houses show them)
        rate = np.where(lam, 37 / 10000 * 6, 315 / 10000 * 6)
        dead = g.random((rws, cols)) < rate
        marks = VGroup(*[Dot(houses[i * cols + j].get_center(), radius=0.07, color=WHITE)
                         for i in range(rws) for j in range(cols) if dead[i, j]])
        cap = fit_rows(VGroup(
            label(r"the pipes of both companies ran down the same streets: \ neighbours drew different water", font_size=24),
            label(r"blue: \ Lambeth; \ red: \ Southwark \& Vauxhall; \ white: \ a death \ (schematic)", font_size=22, color=GREY_A),
        ), 12.4, 0.3, [0, -2.7, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What made this a test was that the two companies had competed for customers street by "
            "street, in the 1840s, and their pipes ran side by side down the same roads. Which company supplied a house was "
            "decided long before, by a landlord or a previous tenant, and had nothing to do with who now lived there. "
            "<bookmark mark='b'/> So neighbours, rich and poor, breathing the same air, drew different water. <bookmark "
            "mark='c'/> Snow went house to house, through the first weeks of the epidemic, asking where the water came from "
            "in every house where someone had died. When residents did not know, he tested the water's salt content, which "
            "differed between the two sources."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h) for h in houses], lag_ratio=0.004), run_time=3.0)
            self.play(FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(FadeIn(cap[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in marks], lag_ratio=0.1), run_time=4.0)
        self.clear_scene()

    def table(self):
        rows = [[r"water supply", r"houses", r"cholera deaths", r"per 10,000 houses"]]
        for name, h, d, r in museum.SNOW:
            rows.append([name.replace("&", r"\&"), f"{h:,}", f"{d:,}", f"{r}"])
        tab = table_rows(rows, font_size=28, col_buff=0.9, row_buff=0.32, colors=[GREY_A, Y1C, Y0C, GREY_B]).move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"Snow's Table IX: \ the first seven weeks of the 1854 epidemic", font_size=24, color=GREY_A),
            label(r"315 against 37: \ eight and a half times the risk", font_size=28, color=TAUC),
        ), 12.4, 0.35, [0, -1.8, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is his Table Nine. <bookmark mark='b'/> In the forty thousand houses supplied by "
            "Southwark and Vauxhall, twelve hundred and sixty-three cholera deaths in the first seven weeks: three hundred "
            "and fifteen for every ten thousand houses. <bookmark mark='c'/> In the twenty-six thousand houses supplied by "
            "Lambeth, ninety-eight deaths: thirty-seven per ten thousand. <bookmark mark='d'/> In the rest of London, "
            "fifty-nine. <bookmark mark='e'/> Houses on the same streets, with the dirty water, carried eight and a half times "
            "the risk."
        ) as vo:
            self.add(snow_tag())
            vo.wait_until("a")
            self.play(FadeIn(tab[0]), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab[3]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def grand(self):
        quote = VGroup(
            label(r"\emph{``No fewer than three hundred thousand people of both sexes, of every age and occupation,}", font_size=26, color=GREY_A),
            label(r"\emph{and of every rank and station, \ldots \ were divided into two groups without their choice,}", font_size=26, color=GREY_A),
            label(r"\emph{and in most cases, without their knowledge.''}", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.18)
        if quote.width > 12.0:
            quote.width = 12.0
        quote.move_to([0, 1.7, 0])
        rows = fit_rows(VGroup(
            label(r"nobody flipped a coin: \ history assigned the water, \ for reasons unrelated to the people", font_size=26, color=TAUC),
            label(r"a natural experiment: \ treatment as good as random, \ found rather than made", font_size=26, color=BANDC),
            label(r"it convinced almost no one at the time: \ the sewers were rebuilt for the smell", font_size=26, color=MISSC),
        ), 12.4, 0.5, [0, -1.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Snow saw what kind of evidence this was. \"No fewer than three hundred thousand people of "
            "both sexes, of every age and occupation, and of every rank and station, were divided into two groups without "
            "their choice, and in most cases, without their knowledge.\" He called it a grand experiment. <bookmark "
            "mark='b'/> Nobody had flipped a coin. History had assigned the water, for reasons that had nothing to do with the "
            "people drinking it. <bookmark mark='c'/> That is a natural experiment: treatment that is as good as random, "
            "found rather than made. <bookmark mark='d'/> It convinced almost no one at the time. London did rebuild its "
            "sewers, after the Great Stink of 1858, but to remove the smell."
        ) as vo:
            self.add(snow_tag())
            vo.wait_until("a")
            self.play(FadeIn(quote))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def question(self):
        rows = fit_rows(VGroup(
            label(r"Part 36: \ measure every confounder, \ and say how wrong you might be", font_size=26, color=GREY_A),
            label(r"here: \ find a piece of the world that was randomized by accident", font_size=26, color=TAUC),
            label(r"a lottery or a birthday that nudges treatment: \ an instrument", font_size=26, color=IVC),
            label(r"a rule with a cutoff: \ a discontinuity", font_size=26, color=CUTC),
            label(r"a policy that starts in some places and not others: \ differences-in-differences", font_size=26, color=Y0C),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-six adjusted for measured confounders, and asked how wrong an unmeasured one "
            "could make us. <bookmark mark='b'/> This part looks instead for a piece of the world that was randomized by "
            "accident, and asks how to read it. <bookmark mark='c'/> A lottery, or a birthday, that nudges some people into "
            "treatment: an instrument. <bookmark mark='d'/> A rule with a cutoff, such as a scholarship for a score of sixty: "
            "a discontinuity. <bookmark mark='e'/> A policy that starts in some places and not others: "
            "differences-in-differences, and its descendants."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 37", font_size=34, color=GREY_B), label(r"Natural Experiments", font_size=56)).arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"the credibility revolution; \ instruments, \ 2SLS, \ weak and many instruments",
            r"Mendelian randomization; \ regression discontinuity and its validity",
            r"differences-in-differences, \ its inference, \ staggered adoption",
            r"honest parallel trends; \ synthetic control; \ synthetic DiD",
            r"panel data and fixed effects; \ partial identification and bounds",
        ], color=TAUC, font_size=26)
        prereq = note(r"prerequisites: \ Parts 35 and 36").to_corner(DL, buff=0.3)
        built = note(r"built: \ \texttt{statkit.quasi}; \ the cutoff lens; \ data: \ Snow, \ Card--Krueger, \ Prop 99").to_corner(DR, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Part thirty-seven: natural experiments. <bookmark mark='b'/> We'll follow the credibility "
            "revolution in economics; estimate effects with instruments, and see how weak or numerous instruments mislead; "
            "use genes as instruments; read regression discontinuities and check them; estimate "
            "differences-in-differences, with honest standard errors, with treatments that start at different times, and "
            "with pre-trends we cannot rule out; build synthetic controls; handle panels with fixed effects; and, when no "
            "design identifies the answer, bound it."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(head), FadeIn(obj, shift=UP * 0.2), FadeIn(prereq), FadeIn(built))
        self.wait(1.0)
        self.clear_scene()
