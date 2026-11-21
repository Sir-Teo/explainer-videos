from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Health(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Health", r"Why do cheap cures go unused, and how should we test them?",
             "Chapter nine. Health.", lit={2004: r"Miguel and Kremer", 2008: r"Thornton", 2015: r"the worm wars"},
             scale=("school", "village"), horizon=("a year",))
        self.worms()
        self.island()
        self.wars()
        self.thornton()
        self.distance()

    def worms(self):
        T = tables.HEALTH_46.data
        chain = flow_chain([(r"intestinal worms: \\ tired, \ anaemic \\ children", HEALTH),
                            (r"a pill twice \\ a year, \ at school", HEALTH),
                            (r"fewer worms \\ in the soil", GAIN), (r"untreated \\ classmates gain", GAIN)],
                           notes=[r"common in \\ western Kenya", r"cents a dose",
                                  r"eggs spread \\ by contact with soil",
                                  r"a spillover"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        design = label(rf"so randomize schools, \ not children: \ {T['schools']} schools in Busia, \ phased in at "
                       r"random", font_size=22, color=TRIAL).to_edge(DOWN, buff=1.4)
        res = label(rf"absence cut by {T['absence_cut']}; \ untreated pupils nearby gained too; \ no measurable "
                    r"effect on test scores", font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.HEALTH_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Intestinal worms infect hundreds of millions of children, leaving them tired and anaemic. <bookmark "
            "mark='a'/> A pill twice a year, given at school, costs a few cents a dose. <bookmark mark='b'/> The "
            "worms spread through soil contaminated by infected children, so treating one child means fewer eggs "
            "around the school, <bookmark mark='c'/> and that protects classmates who took no pill. <bookmark "
            "mark='d'/> That spillover makes a careful design essential. Edward Miguel and Michael Kremer "
            f"randomized whole schools, {T['schools']} of them in Busia in western Kenya, phased in over several "
            "years. <bookmark mark='e'/> Deworming cut absence from school by a quarter, and pupils who were not "
            "treated, in treated schools and nearby ones, gained as well. Test scores did not measurably change."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("d")
            self.play(FadeIn(design))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.clear_scene()

    def island(self):
        W = load("worms")
        N0 = W["no_spill"]
        rows = [(r"within treated schools: \\ treated minus untreated pupils", W["within"], CONTROL),
                (r"untreated pupils: \\ treated schools minus control", W["spillover"], HEALTH),
                (r"whole schools: \\ treated minus control", W["between_schools"], GAIN)]
        ax = plane([0, 3], [-0.12, 0], center=LEFT * 1.6 + UP * 0.35, x_length=6.6, y_length=4.2, xticks=[],
                   yticks=[-0.12, -0.08, -0.04, 0], ylabel=r"change in the share of days absent",
                   yfmt=lambda v: f"{100 * v:+.0f}".replace("-", "{-}"), font_size=14)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=13, color=WHITE).next_to(ax.ax.c2p(0.5 + i, -0.12), DOWN,
                                                                                buff=0.15),
                            label(rf"{100 * v:+.1f}".replace("-", "{-}"), font_size=16, color=WHITE).next_to(r, DOWN,
                                                                                                      buff=0.06)))
        side = VGroup(
            label(rf"control schools: \\ {100 * W['absence_control']:.0f}\% of days absent", font_size=18, color=WHITE),
            label(r"the within-school \\ comparison misses \\ the spillover", font_size=18, color=HOLD),
            label(rf"with no spillover: \\ within {100 * N0['within']:+.1f}, \\ "
                  rf"whole schools {100 * N0['between_schools']:+.1f}".replace("-", "{-}"), font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The Island's schools show why. In control schools, children miss {100 * W['absence_control']:.0f} "
            "percent of days. <bookmark mark='a'/> Compare, within treated schools, the pupils who took the pill "
            f"with those who did not: absence is {100 * abs(W['within']):.1f} points lower. <bookmark mark='b'/> "
            "But the untreated pupils in treated schools are themselves "
            f"{100 * abs(W['spillover']):.1f} points better off than pupils in control schools, because there are "
            "fewer worms around them. <bookmark mark='c'/> So the comparison within a school understates what "
            "the pill does to each treated child, and misses entirely what it does for the others. Compare whole "
            f"schools, and the programme cuts absence by {100 * abs(W['between_schools']):.1f} points for every "
            "pupil enrolled. <bookmark mark='d'/> Where there is no spillover, the within-school comparison "
            "would have been the right one. A design must match how the treatment spreads."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            for mk, b in zip("abc", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], UP), FadeIn(b[2]))
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def wars(self):
        cards = point_cards([
            (r"2004", r"Miguel and Kremer: \\ absence down \\ a quarter, \ with \\ spillovers", HEALTH),
            (r"2015", r"two re-analyses in \\ an epidemiology \\ journal: \ the effects \\ are fragile", LOSS),
            (r"the reply", r"the authors: \ the \\ main results \\ survive the \\ corrections", GAIN),
            (r"the lesson", r"open data and \\ re-analysis are \\ how a result \\ earns trust", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"the worm wars", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HEALTH_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The result made deworming one of the most recommended charities in the world, and then it was "
            "attacked. <bookmark mark='a'/> In 2004, absence down by a quarter, with spillovers. <bookmark "
            "mark='b'/> In 2015 two teams of epidemiologists re-analysed the data, which the authors had shared, "
            "and published in the International Journal of Epidemiology. They found coding errors, and argued "
            "that with other reasonable choices the attendance effects were much weaker. The press called it the "
            "worm wars. <bookmark mark='c'/> The authors replied that after the corrections the main results, "
            "including the spillovers, still held, and that the disagreement was mostly about methods. "
            "<bookmark mark='d'/> Economists and epidemiologists still disagree about parts of it. But the episode "
            "is a model of how evidence should work: data shared, analyses repeated, and the argument conducted "
            "in the open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def thornton(self):
        Th = load("thornton")
        n = len(Th["rates"])
        ax = plane([-0.5, n - 0.5], [0, 1], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.0, y_length=4.6, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"share who collected their result",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bars = VGroup()
        for i, (lab_, r) in enumerate(zip(Th["labels"], Th["rates"])):
            p0, p1 = ax.ax.c2p(i - 0.32, 0), ax.ax.c2p(i + 0.32, r)
            col = CONTROL if i == 0 else HEALTH
            rect = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                             fill_opacity=0.85).move_to((p0 + p1) / 2)
            nm = r"none" if i == 0 else rf"\${lab_.replace('-', '--')}"
            bars.add(VGroup(rect, label(nm, font_size=13, color=WHITE).next_to(ax.ax.c2p(i, 0), DOWN, buff=0.12),
                            label(rf"{100 * r:.0f}\%", font_size=15, color=WHITE).next_to(rect, UP, buff=0.05)))
        xl = label(r"the cash incentive, \ drawn at random", font_size=15, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        side = VGroup(
            label(rf"Thornton's Malawi, \ 2004: \\ {Th['n']:,} people tested \\ at home".replace(",", "{,}"),
                  font_size=18, color=WHITE),
            label(rf"no incentive: \ {100 * Th['none']:.0f}\% \\ went to get the result", font_size=18,
                  color=CONTROL),
            label(rf"any incentive: \ {100 * Th['any']:.0f}\%", font_size=18, color=HEALTH),
            label(r"the first cents do \\ most of the work", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Thornton (2008), \ via the R package causaldata 0.1.4", corner=DL, font_size=12)
        with self.voiceover(
            "Prices matter in the other direction too. In rural Malawi in 2004, Rebecca Thornton's team offered "
            "free HIV tests at people's homes; to learn the result, people had to walk to a clinic later. <bookmark "
            "mark='a'/> Each person drew a voucher worth between nothing and about three dollars, to be paid on "
            f"collecting the result. Here are her data, {Th['n']:,} people. <bookmark mark='b'/> With no "
            f"incentive, {100 * Th['none']:.0f} percent went. <bookmark mark='c'/> With any incentive, "
            f"{100 * Th['any']:.0f} percent. <bookmark mark='d'/> And the first few cents did most of the work: "
            f"a voucher worth under a quarter of a dollar raised the share to {100 * Th['rates'][1]:.0f} percent. "
            "The nets in the hook were the same lesson in reverse. For goods that protect health, the step between "
            "free and almost free matters more than any later step."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(xl), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars],
                      run_time=1.0)
            vo.wait_until("a")
            self.play(Indicate(xl, color=WHITE), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(bars[0], color=WHITE))
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[2])) for b in bars[1:]],
                                  lag_ratio=0.3), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(bars[1], color=WHITE), FadeIn(side[3]))
        self.clear_scene()

    def distance(self):
        Th = load("thornton")
        labs = [r"under 1 km", r"1--2 km", r"2--3 km", r"3--5 km"]
        ax = plane([-0.5, 3.5], [0.5, 0.8], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.0, y_length=4.2, xticks=[],
                   yticks=[0.5, 0.6, 0.7, 0.8], ylabel=r"share who collected their result",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bars = VGroup()
        for i, (nm, r) in enumerate(zip(labs, Th["dist_rates"])):
            p0, p1 = ax.ax.c2p(i - 0.3, 0.5), ax.ax.c2p(i + 0.3, r)
            rect = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=TOWN,
                             fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(rect, label(nm, font_size=14, color=WHITE).next_to(ax.ax.c2p(i, 0.5), DOWN, buff=0.12),
                            label(rf"{100 * r:.0f}\%", font_size=15, color=WHITE).next_to(rect, UP, buff=0.05)))
        side = VGroup(
            label(r"the clinics were \\ placed at random too", font_size=18, color=WHITE),
            label(rf"{100 * Th['dist_rates'][0]:.0f}\% within a kilometre, \\ {100 * Th['dist_rates'][-1]:.0f}\% at "
                  r"three to five", font_size=18, color=TOWN),
            label(r"a walk costs time, \\ and time is money \\ the poor do not have", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Thornton (2008), \ via the R package causaldata 0.1.4", corner=DL, font_size=12)
        with self.voiceover(
            "Distance acts like a price. <bookmark mark='a'/> Thornton's team also placed the clinics at random, "
            "so the distance people had to walk was as good as drawn by lottery. <bookmark mark='b'/> Of those "
            f"within a kilometre, {100 * Th['dist_rates'][0]:.0f} percent collected their result; of those three "
            f"to five kilometres away, {100 * Th['dist_rates'][-1]:.0f}. <bookmark mark='c'/> A walk costs hours, "
            "and for people who earn by the day, hours are money. Many of the cheapest ways to help are ways of "
            "making the right choice a little easier, a little closer, or a little cheaper."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[2]))
                                                     for b in bars], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Indicate(bars[0], color=WHITE), Indicate(bars[-1], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
