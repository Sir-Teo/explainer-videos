from __future__ import annotations

from videos.psychology.psych38.common import *  # noqa: F403


class Origins(VoiceoverScene):
    def construct(self):
        self.card()
        self.rice()
        self.mobility()
        self.kinship()

    def card(self):
        card = chapter_card(4, r"Where differences come from", r"Rice, strangers or cousins?",
                            lit={2014: r"Talhelm et al.", 2018: r"Thomson et al.", 2019: r"Schulz et al."},
                            part=PART, scale=("group", "culture"), marr=("why",))
        with self.voiceover("Chapter four. Where differences come from."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rice(self):
        head = heading(r"The rice theory")
        # a schematic map: north (wheat) above the Yangtze, south (rice) below
        north = Rectangle(width=4.6, height=1.6, stroke_width=0, fill_color=WEST, fill_opacity=0.25)
        south = Rectangle(width=4.6, height=1.6, stroke_width=0, fill_color=WORLD, fill_opacity=0.25)
        VGroup(north, south).arrange(DOWN, buff=0).move_to([-3.8, 0.4, 0])
        river = FunctionGraph(lambda x: 0.12 * np.sin(2.2 * x), x_range=[-2.3, 2.3], color=WEST,
                              stroke_width=4).move_to([-3.8, 0.4, 0])
        ln = label(r"wheat: \ farmed by a household alone", font_size=16, color=WEST).move_to(north)
        ls = label(r"paddy rice: \ shared irrigation, \ exchanged labour", font_size=16, color=WORLD).move_to(south)
        rv = label(r"the Yangtze", font_size=14, color=GREY_B).next_to(river, RIGHT, buff=0.1)
        rows = rows_of([
            (r"Talhelm and colleagues, \ 2014: \ 1{,}162 Han Chinese students from six sites", WHITE),
            (r"people from rice-farming provinces in the south scored more holistic and more interdependent than "
             r"people from wheat-farming provinces in the north", WORLD),
            (r"the idea: \ irrigated rice needs cooperation between households, \ and the habits outlast the "
             r"farming", GOOD),
            (r"critics: \ ``wheat'' lumped corn and other crops with wheat, \ and reanalyses with other data found "
             r"weaker or different patterns; \ the authors replied; \ the Ledger calls it contested", AUTH),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Talhelm et al.\ (2014)")
        with self.voiceover(
            "If cultures differ, why? One answer is ecology. <bookmark mark='a'/> In 2014 Thomas Talhelm and "
            "colleagues tested more than eleven hundred Han Chinese students from six sites. "
            "<bookmark mark='b'/> People from the rice-farming south scored more holistic and more interdependent "
            "than people from the wheat-farming north. <bookmark mark='c'/> The idea: paddy rice needs shared "
            "irrigation and exchanged labour between households, wheat does not, and the habits outlast the "
            "farming. <bookmark mark='d'/> Critics pointed out that the wheat side lumped corn and other crops in "
            "with wheat, and reanalyses with other data found weaker or different patterns. The authors replied. "
            "The Ledger calls it contested."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(north), FadeIn(south), Create(river), FadeIn(rv))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(ln), FadeIn(ls))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def mobility(self):
        head = heading(r"How easily can you make new friends?")
        A = axes([0, 1], [0, 1], x_length=4.6, y_length=3.2, xticks=None, yticks=None,
                 xlabel=r"relational mobility", ylabel=r"self-disclosure, \ trust", center=[-3.5, -0.1, 0],
                 font_size=15)
        rng = np.random.default_rng(38)
        x = rng.uniform(0.1, 0.9, 39)
        y = 0.15 + 0.7 * x + rng.normal(0, 0.08, 39)
        pts = scatter(A.ax, x, y, WEST, radius=0.06)
        note = label(r"schematic: \ 39 societies", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"relational mobility: \ how free people around you are to choose and leave relationships", WHITE),
            (r"Thomson and colleagues, \ 2018: \ nearly 17{,}000 people in 39 societies, \ recruited online", WEST),
            (r"where mobility was high, \ people reported more self-disclosure, \ support and trust; \ mobility was "
             r"highest in the Americas, \ Europe and Australasia, \ lower in the Middle East and East Asia", GOOD),
            (r"and lower where history brought threat and settled farming", WORLD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Thomson et al.\ (2018)")
        with self.voiceover(
            "A second answer is about the market for relationships. <bookmark mark='a'/> Relational mobility is how "
            "free the people around you are to choose new relationships and leave old ones. "
            "<bookmark mark='b'/> In 2018 Robert Thomson and colleagues measured it in nearly seventeen thousand "
            "people in thirty-nine societies, recruited online. <bookmark mark='c'/> Where mobility was high, people "
            "reported more self-disclosure, support and trust. It was highest in the Americas, Europe and "
            "Australasia, and lower in the Middle East and East Asia. <bookmark mark='d'/> And it was lower where "
            "history brought threats like disease and war, and settled farming."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[FadeIn(p, scale=1.4) for p in pts], lag_ratio=0.05))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def kinship(self):
        head = heading(r"Cousins and the Church")
        chain = VGroup(*[word_chip(t, color=c, font_size=18, width=3.1) for t, c in (
            (r"the medieval Western Church", GREY_A), (r"bans on cousin marriage", WEST),
            (r"weaker kin ties", WEST), (r"individualism, \ trust in strangers", GOOD))])
        chain.arrange(DOWN, buff=0.55).move_to([-3.8, -0.2, 0])
        arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B) for a, b in
                          zip(chain[:-1], chain[1:])])
        rows = rows_of([
            (r"Schulz, \ Bahrami-Rad, \ Beauchamp and Henrich, \ 2019: \ 24 psychological outcomes, \ across "
             r"countries, \ European regions and individuals", WHITE),
            (r"longer exposure to the medieval Western Church went with less intensive kinship, \ and less "
             r"intensive kinship with more individualism, \ less conformity and more trust of strangers", WEST),
            (r"a historical argument from correlations: \ the measures of exposure and kinship are "
             r"reconstructions, \ and other histories could produce the same pattern", AUTH),
            (r"three theories, \ none exclusive; \ all of them say a mind is partly made by how its society "
             r"is organized", YOU),
        ], 6.4, 19, 0.36).move_to([3.2, -0.2, 0])
        tag = published_tag(r"Schulz et al.\ (2019)")
        with self.voiceover(
            "A third answer reaches back a thousand years. <bookmark mark='a'/> In 2019 Jonathan Schulz, Joseph "
            "Henrich and colleagues put together twenty-four psychological outcomes, across countries, European "
            "regions and individuals. <bookmark mark='b'/> Longer exposure to the medieval Western Church, with its "
            "bans on cousin marriage, went with less intensive kinship. And less intensive kinship went with more "
            "individualism, less conformity, and more trust of strangers. <bookmark mark='c'/> It's a historical "
            "argument built from correlations. The measures of exposure and kinship are reconstructions, and other "
            "histories could produce the same pattern. <bookmark mark='d'/> Three theories, none exclusive. All of "
            "them say that a mind is partly made by how its society is organized."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(chain[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(c)) for a, c in
                                                     zip(arrows, chain[1:])], lag_ratio=0.6), run_time=3.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
