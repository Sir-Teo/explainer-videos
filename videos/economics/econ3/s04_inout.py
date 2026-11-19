from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403


class InOut(VoiceoverScene):
    def construct(self):
        card(self, 3, r"What is in, and what is left out", r"Which work does GDP count, and which does it miss?",
             "Chapter three. What is in, and what is left out.", lit=("households", "firms"),
             scale=("household", "nation", "world"), horizon=("a year",))
        self.boundary()
        self.island()
        self.housework()
        self.elsewhere()

    # ------------------------------------------------------------------
    def boundary(self):
        k = tables.KUZNETS_1934.data
        inside = Circle(radius=2.35, stroke_color=E.ACCENT, stroke_width=3, fill_color=E.ACCENT, fill_opacity=0.06)
        inside.move_to(LEFT * 3.2 + DOWN * 0.3)
        il = label(r"inside GDP", font_size=28, color=E.ACCENT).next_to(inside, UP, buff=0.15)
        ins = VGroup(
            label(r"everything sold at a price", font_size=23),
            label(r"government services, \\ valued at what they cost", font_size=23),
            label(r"the food a farmer grows \\ and eats", font_size=23),
            label(r"the rent a homeowner \\ ``pays'' to herself", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.28).move_to(inside)
        outs = VGroup(
            label(r"cooking, cleaning, childcare at home", font_size=23, color=UNPAID),
            label(r"volunteering", font_size=23, color=UNPAID),
            label(r"leisure", font_size=23, color=UNPAID),
            label(r"free apps \ (only their advertising counts)", font_size=23, color=UNPAID),
            label(r"a fishery run down, \ a river polluted", font_size=23, color=E.MISS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 0.3)
        ol = label(r"outside", font_size=28, color=UNPAID).next_to(outs, UP, buff=0.35)
        rent = label(rf"1934: \ left out (about \${k['imputed_rent_1930'] / 1000:.1f} billion in 1930); \ "
                     r"today: \ counted", font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "GDP measures production, but not all of it. Statisticians draw a line, the production boundary, "
            "and count what falls inside. <bookmark mark='a'/> Inside is everything sold at a price. Government "
            "services are inside too, valued at what they cost to provide, because a school or a court has no "
            "price. So is food a farmer grows and eats herself. <bookmark mark='b'/> And so is something odd: the "
            "rent that people who own their homes would pay if they rented them. Kuznets left that out in 1934, "
            "about two point seven billion dollars in 1930. Today it's counted, so that a country's GDP doesn't "
            "change just because its people buy the homes they used to rent. <bookmark mark='c'/> Outside the line "
            "is most of the work done at home: cooking, cleaning, looking after children. So is volunteering, and "
            "leisure, and most of the value of things given away free online. <bookmark mark='d'/> And a fishery "
            "fished out or a river polluted subtracts nothing at all. GDP counts the catch, not the stock it came "
            "from."
        ) as vo:
            self.play(Create(inside), FadeIn(il))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in ins[:3]], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(ins[3], scale=0.9), FadeIn(rent))
            vo.wait_until("c")
            self.play(FadeIn(ol), LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in outs[:4]], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(FadeIn(outs[4], shift=LEFT * 0.2))
        self.clear_scene()

    def island(self):
        u = load("unpaid")
        k = 0.0115
        x0 = -5.6
        gdp = Rectangle(width=u["gdp"] * k, height=0.85, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.85)
        gdp.move_to([x0 + u["gdp"] * k / 2, 2.0, 0])
        gl = label(r"the Island's GDP: \ \$740", font_size=26, color=BACKGROUND).move_to(gdp)
        x = x0
        blocks = VGroup()
        legend = VGroup()
        cols = [UNPAID, "#B48EF0", "#9D7CE0", "#8A6BD0"]
        for (name, v), c in zip(u["items"], cols):
            r = Rectangle(width=v * k, height=0.85, stroke_color=BACKGROUND, stroke_width=1.5, fill_color=c,
                          fill_opacity=0.85)
            r.move_to([x + v * k / 2, 0.85, 0])
            blocks.add(r)
            legend.add(VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.9),
                              label(rf"{name}: \ \${v:.0f}", font_size=23, color=c)).arrange(RIGHT, buff=0.12))
            x += v * k
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(blocks, RIGHT, buff=0.5).align_to(blocks, UP)
        unl = label(r"unpaid", font_size=22, color=UNPAID).next_to(blocks, LEFT, buff=0.15)
        share = label(rf"unpaid work, valued at the fishing wage: \ \${u['total']:.0f}, \ "
                      rf"{100 * u['share']:.0f}\% of GDP", font_size=27, color=UNPAID).move_to(DOWN * 0.75)
        ana = islander("ana", 0.9, name=True)
        bo = islander("bo", 0.9, name=True)
        pair = VGroup(ana, bo).arrange(RIGHT, buff=1.4).move_to(DOWN * 2.45 + LEFT * 2.5)
        hire = label(r"Bo pays Ana to cook: \ GDP $+$", font_size=24, color=E.GAIN)
        wed = label(r"they marry, \ she cooks for free: \ GDP $-$", font_size=24, color=E.MISS)
        VGroup(hire, wed).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(pair, RIGHT, buff=0.7)
        same = label(r"the same meals", font_size=22, color=GREY_B).next_to(VGroup(hire, wed), DOWN, buff=0.2)
        tag = island_tag(r"simulated: the Island, year 3; unpaid hours valued at the fishing wage", corner=DR,
                         font_size=16)
        with self.voiceover(
            "On the Island we can count what the books leave out, because we planted it. <bookmark mark='a'/> In "
            "the year, the islanders spent hours cooking and cleaning, looking after children, working Crusoe's "
            "garden and mending nets at home. <bookmark mark='b'/> Valued at what the same hours would earn at "
            f"the fishing company, that work was worth {u['total']:.0f} dollars: "
            f"{100 * u['share']:.0f} percent of the Island's GDP, and none of it in the accounts. "
            "<bookmark mark='c'/> It leads to a famous oddity. If Bo pays Ana to cook for his family, her wages are "
            "income and the meals are production, and GDP goes up. If they marry and she cooks the same meals for "
            "nothing, GDP goes down, though nobody eats any less."
        ) as vo:
            self.play(GrowFromEdge(gdp, LEFT), FadeIn(gl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(unl), LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(l))
                                                 for b, l in zip(blocks, legend)], lag_ratio=0.35), run_time=2.4)
            vo.wait_until("b")
            self.play(FadeIn(share))
            vo.wait_until("c")
            self.play(FadeIn(pair), FadeIn(hire))
            self.play(FadeIn(wed))
            self.play(FadeIn(same))
        self.clear_scene()

    def housework(self):
        u = load("unpaid")
        ax = axes([0, 3], [0, 45], x_length=5.0, y_length=4.2, yticks=[0, 10, 20, 30, 40],
                  yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"how much counting home production would add to GDP",
                  font_size=20, center=LEFT * 3.0 + DOWN * 0.3)
        a = ax.ax
        bars = VGroup()
        for i, (yr, v) in enumerate(((1965, u["bea"]["1965"]), (2010, u["bea"]["2010"]))):
            x = 0.9 + 1.2 * i
            lo, hi = a.c2p(x, 0), a.c2p(x, v)
            r = Rectangle(width=0.9, height=hi[1] - lo[1], stroke_width=0, fill_color=UNPAID, fill_opacity=0.85)
            r.move_to((lo + hi) / 2)
            t = label(rf"{v:g}\%", font_size=26).next_to(r, UP, buff=0.1)
            y = label(str(yr), font_size=22, color=GREY_B).next_to(lo, DOWN, buff=0.15)
            bars.add(VGroup(r, t, y))
        why = VGroup(
            label(r"in 1965 the average adult spent \\ 27 hours a week on home production; \\ in 2010, 22",
                  font_size=24, color=GREY_A),
            label(r"as women moved into paid work, \\ part of measured growth was work \\ moving from home "
                  r"to market", font_size=24, color=E.ACCENT),
            label(r"counted, nominal GDP growth \\ 1965--2010: \ 6.9\% $\to$ 6.7\% a year", font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.6).shift(UP * 0.2)
        tag = published_tag(r"Bridgman, Dugan, Lal, Osborne and Villones, Survey of Current Business, May 2012",
                            corner=DL, font_size=16)
        with self.voiceover(
            "This isn't only an Island story. In 2012 economists at the Bureau of Economic Analysis built a "
            "satellite account for the United States, valuing the hours people spend on home production. "
            "<bookmark mark='a'/> Counting it would have made GDP 39 percent larger in 1965, <bookmark mark='b'/> "
            "and 26 percent larger in 2010. <bookmark mark='c'/> The share fell because people spent less time on "
            "it, 27 hours a week on average in 1965 and 22 in 2010, as more women took paid work. "
            "<bookmark mark='d'/> So part of the growth in measured GDP over those decades was work that moved from "
            "the home, where it wasn't counted, to the market, where it was. <bookmark mark='e'/> Counted "
            "properly, growth was a little slower: 6.7 percent a year in current dollars instead of 6.9."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            for mk, w in zip("cde", why):
                vo.wait_until(mk)
                self.play(FadeIn(w, shift=LEFT * 0.2))
        self.clear_scene()

    def elsewhere(self):
        cards = VGroup(
            study_card(r"The informal economy", r"International Labour Organization (2018)",
                       [(r"share", r"more than 61\% of the world's workers have informal jobs: \ about two billion "
                                   r"people"),
                        (r"Africa", r"85.8\% of employment"),
                        (r"in GDP", r"estimated, \ but the hardest part to measure")],
                       design="survey", width=6.5, font_size=24),
            study_card(r"Free goods", r"Brynjolfsson, Collis and Eggers (2019)",
                       [(r"design", r"large online choice experiments: \ what would you need to be paid to give it "
                                    r"up?"),
                        (r"result", r"the median user needed about \$48 to give up Facebook for a month"),
                        (r"in GDP", r"almost nothing: \ the price is zero")],
                       design="survey", width=6.5, font_size=24),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        top = label(r"Two more gaps", font_size=34).to_edge(UP, buff=0.45)
        bottom = label(r"GDP measures market production well, \ and stops at the edge of the market", font_size=26,
                       color=E.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Two more gaps are large. <bookmark mark='a'/> In much of the world most work is informal: street "
            "trade, small farms, jobs with no contract and no tax records. The International Labour Organization "
            "estimated in 2018 that more than 61 percent of the world's workers, about two billion people, "
            "worked informally, and in Africa almost 86 percent. The accounting rules ask countries to estimate "
            "this work, but it's the part they measure worst. <bookmark mark='b'/> And at the other end, the "
            "digital economy gives much away. A search engine, a map or a social network costs its users nothing, "
            "so it adds almost nothing to GDP beyond the advertising it sells. Erik Brynjolfsson and his "
            "colleagues ran large online experiments, asking people what they would need to be paid to give such "
            "things up. The median user wanted about 48 dollars to go without Facebook for a month. "
            "<bookmark mark='c'/> None of this makes GDP wrong. It measures market production, carefully and "
            "consistently, and it stops at the edge of the market, as Kuznets said it would."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(bottom))
        self.clear_scene()
