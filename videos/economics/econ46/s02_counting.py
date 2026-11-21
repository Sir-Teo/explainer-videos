from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403

REG = (("EAS", r"East Asia \\ and Pacific", "#7FD1B9"), ("SAS", r"South Asia", "#C9A0FF"),
       ("SSF", r"sub-Saharan \\ Africa", "#F25F5C"), ("WLD", r"the world", "#F2C14E"))


class Counting(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Counting the poor", r"Who is poor, and how many?",
             "Chapter one. Counting the poor.",
             lit={1990: r"World Bank", 2008: r"Chen and Ravallion", 2010: r"Deaton"}, scale=("world",),
             horizon=("forty years",))
        self.recipe()
        self.lines()
        self.regions()
        self.countries()
        self.prices()

    def recipe(self):
        chain = flow_chain([(r"national \\ poverty lines", POOR),
                            (r"converted at \\ purchasing-power \\ parity", THEORY),
                            (r"one line for \\ the world", POOR), (r"household \\ surveys", DATA),
                            (r"a count", E.ACCENT)],
                           notes=[r"of the poorest \\ countries", r"what a dollar \\ buys in each \\ country",
                                  r"a dollar a day, \\ at first", r"what each \\ household \\ consumes",
                                  r"people below \\ the line"],
                           box_w=2.3, box_h=1.0, buff=0.42, font_size=19, note_size=15)
        chain.move_to(UP * 0.5)
        foot = label(r"every step needs prices: \ what the poor buy, \ in each country, \ in each year",
                     font_size=21, color=GREY_A).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.POVERTY_LINES.tag, corner=DR, font_size=11)
        with self.voiceover(
            "How do you count the world's poor? The World Bank's recipe has five steps. <bookmark mark='a'/> Start "
            "from the poverty lines that the poorest countries set for themselves, each in its own currency. "
            "<bookmark mark='b'/> Convert them at purchasing-power parity: not the market exchange rate, but the "
            "rate at which a dollar buys the same basket of goods in each country, from the price surveys of Part "
            "three. <bookmark mark='c'/> That gives one line for the whole world, in 1990 about a dollar a day. "
            "<bookmark mark='d'/> Then take household surveys, which record what each household consumes. "
            "<bookmark mark='e'/> And count the people below the line. <bookmark mark='f'/> Every step needs prices, "
            "and the prices are the hard part."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcde"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def lines(self):
        T = tables.POVERTY_LINES.data
        ax = plane([1987, 2028], [0, 3.4], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.6,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 1, 2, 3], ylabel=r"dollars a day, \ at that year's PPP",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"\\${v:.0f}", font_size=14)
        steps, dots = VGroup(), VGroup()
        prev = None
        for yr, line, base in T["lines"]:
            d = VGroup(dot(ax, yr, line, POOR, 0.08),
                       label(rf"\${line:.2f} \\ ({base} prices)", font_size=14, color=WHITE).next_to(
                           ax.ax.c2p(yr, line), UP, buff=0.12))
            dots.add(d)
            if prev is not None:
                steps.add(seg(ax, prev[0], prev[1], yr, prev[1], GREY_B, 2.0),
                          seg(ax, yr, prev[1], yr, line, GREY_B, 2.0, dashed=True))
            prev = (yr, line)
        side = VGroup(
            label(r"the line is re-set \\ when new prices arrive", font_size=19, color=WHITE),
            label(rf"2008: \ {T['poor_2005_bn']} billion poor \\ in 2005, \ {T['revision_m']} million \\ more "
                  r"than thought", font_size=19, color=LOSS),
            label(r"the people were the same; \\ the prices were new", font_size=19, color=GREY_A),
            label(r"2025: \ \$3.00 at 2021 \\ prices; \ higher line, \\ not a poorer world", font_size=19,
                  color=POOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.POVERTY_LINES.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The line has been re-set five times since 1990, each time new prices arrived from the International "
            "Comparison Program. <bookmark mark='a'/> A dollar a day at 1985 prices; one dollar 8 at 1993 prices; "
            "one dollar 25 at 2005 prices; one dollar 90 at 2011 prices; two dollars 15 at 2017 prices; and, since "
            "June 2025, three dollars at 2021 prices. <bookmark mark='b'/> Each re-set can move the count. In 2008 "
            "Shaohua Chen and Martin Ravallion reported that "
            f"{T['poor_2005_bn']} billion people had been poor in 2005, about {T['revision_m']} million more than "
            "the old prices had said. <bookmark mark='c'/> Nobody had become poorer; the prices were new. "
            "<bookmark mark='d'/> The 2025 update raised the count again, and the World Bank was careful to say "
            "the same thing: a higher line, not a poorer world."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), FadeIn(dots[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(Create(steps[2 * k]), Create(steps[2 * k + 1]), FadeIn(dots[k + 1]))
                                    for k in range(len(dots) - 1)], lag_ratio=0.7), run_time=8.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(dots[2], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(dots[-1], color=WHITE))
        self.clear_scene()

    def regions(self):
        P = load("poverty")
        ax = plane([1980, 2026], [0, 80], center=LEFT * 1.6 + DOWN * 0.35, x_length=8.8, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 20, 40, 60, 80],
                   ylabel=r"percent below \$3.00 a day \ (2021 prices)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        curves, names = VGroup(), VGroup()
        for code, nm, col in REG:
            d = P[code]
            curves.add(path(ax, d["year"], d["value"], col, 3.4 if code == "WLD" else 2.6, smooth=False))
            nl = label(nm, font_size=15, color=col).next_to(ax.ax.c2p(d["year"][-1], d["value"][-1]), RIGHT, buff=0.12)
            nl.shift({"SAS": UP * 0.42, "EAS": DOWN * 0.12}.get(code, ORIGIN))
            names.add(nl)
        W, A, S, E_ = P["WLD"], P["SSF"], P["SAS"], P["EAS"]
        side = VGroup(
            label(rf"the world: \\ {W['first']:.0f}\% in {W['first_year']} \\ to {W['last']:.0f}\% in "
                  rf"{W['last_year']}", font_size=19, color=REG[3][2]),
            label(rf"East Asia: \\ {E_['first']:.0f}\% to {E_['last']:.0f}\%", font_size=19, color=REG[0][2]),
            label(rf"South Asia: \\ {S['first']:.0f}\% to {S['last']:.1f}\%", font_size=19, color=REG[1][2]),
            label(rf"sub-Saharan Africa: \\ {A['first']:.0f}\% in {A['first_year']}, \\ {A['last']:.0f}\% in "
                  rf"{A['last_year']}", font_size=19, color=REG[2][2]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ World Development Indicators \ (SI.POV.DDAY), \ Nov 2026", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Here is the count at the new line, from the World Bank's own data. <bookmark mark='a'/> In "
            f"{W['first_year']}, {W['first']:.0f} percent of the world's people lived on less than three dollars a "
            f"day at today's prices. By {W['last_year']}, {W['last']:.0f} percent. <bookmark mark='b'/> Most of the "
            f"fall happened in East Asia, from {E_['first']:.0f} percent to {E_['last']:.0f}. <bookmark mark='c'/> "
            f"Then South Asia, from {S['first']:.0f} percent to {S['last']:.1f}. <bookmark mark='d'/> Sub-Saharan "
            f"Africa started at {A['first']:.0f} percent in {A['first_year']}, and is at {A['last']:.0f} percent. "
            "With its population growing fast, the number of poor people there has risen, and most of the world's "
            "poor now live there."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(curves[3]), FadeIn(names[3]), FadeIn(side[0]), run_time=2.0)
            for k, mk in zip((0, 1, 2), "bcd"):
                vo.wait_until(mk)
                self.play(Create(curves[k]), FadeIn(names[k]), FadeIn(side[k + 1]), run_time=1.8)
        self.clear_scene()

    def countries(self):
        P = load("poverty")
        C, I = P["CHN"], P["IND"]
        ax = plane([1980, 2026], [0, 100], center=LEFT * 1.6 + DOWN * 0.35, x_length=8.8, y_length=4.8,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 25, 50, 75, 100],
                   ylabel=r"percent below \$3.00 a day", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        cc = VGroup(path(ax, C["year"], C["value"], "#F25F5C", 3.0, smooth=False),
                    *[dot(ax, x, y, "#F25F5C", 0.05) for x, y in zip(C["year"], C["value"])])
        ii = VGroup(path(ax, I["year"], I["value"], "#7EC8F5", 3.0, smooth=False),
                    *[dot(ax, x, y, "#7EC8F5", 0.06) for x, y in zip(I["year"], I["value"])])
        side = VGroup(
            label(rf"China: \ {C['first']:.0f}\% in {C['first_year']}, \\ under 1\% by 2018", font_size=19,
                  color="#F25F5C"),
            label(rf"India: \ {I['first']:.0f}\% in {I['first_year']}, \\ {I['last']:.1f}\% in {I['last_year']}",
                  font_size=19, color="#7EC8F5"),
            label(r"dots: \ survey years; \\ India's are few, \\ and its survey changed \\ for 2022-23", font_size=17,
                  color=GREY_A),
            label(r"no experiment \\ produced this", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ World Development Indicators \ (SI.POV.DDAY), \ Nov 2026", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Two countries carry most of the story. <bookmark mark='a'/> In China, "
            f"{C['first']:.0f} percent of people were below the line in {C['first_year']}; by 2018, under one "
            f"percent. <bookmark mark='b'/> India: {I['first']:.0f} percent in {I['first_year']}, and "
            f"{I['last']:.1f} percent in the latest survey. <bookmark mark='c'/> The dots are the survey years. "
            "India's surveys are years apart, and its survey's design changed for 2022 and 2023, so the last steps are "
            "less certain "
            "than the line suggests. <bookmark mark='d'/> No randomized experiment produced either fall. They came "
            "with decades of growth, in farms, factories and cities. Keep that in mind when this part turns to "
            "experiments: they answer smaller questions very well."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(cc[0]), FadeIn(cc[1:]), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(ii[0]), FadeIn(ii[1:]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def prices(self):
        cards = point_cards([
            (r"whose basket?", r"price surveys weigh \\ what everyone buys, \\ not what the \\ poor buy", POOR),
            (r"which year?", r"each round of prices \\ re-draws the map; \\ the 2008 round \\ added 400 million", LOSS),
            (r"which survey?", r"consumption in one \\ country, \ income \\ in another", DATA),
            (r"so what?", r"the trend is robust; \\ the level, \ and the \\ ranking of regions, \\ less so", GAIN),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"Deaton's warnings, \ 2010", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.POVERTY_LINES.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In his 2010 presidential address to the American Economic Association, Angus Deaton listed what can go "
            "wrong. <bookmark mark='a'/> Whose basket? The price comparisons weigh goods by what everyone in a "
            "country buys, not what the poor buy. <bookmark mark='b'/> Which year? Each new round of prices redraws "
            "the map, as the 2008 round did. <bookmark mark='c'/> Which survey? Some countries measure consumption, "
            "others income, and the two are not the same. <bookmark mark='d'/> His conclusion was not that the count "
            "is worthless. The fall in poverty since 1980 survives every choice; the exact level, and the ranking "
            "of regions, are softer than the decimal points suggest."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
