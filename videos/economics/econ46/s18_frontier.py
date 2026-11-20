from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ scaling, \ satellites and phones", r"What is still being worked out?",
             "Chapter sixteen. Frontier: scaling, satellites and phones.",
             lit={2015: r"Blumenstock et al.", 2016: r"Jean et al.", 2017: r"Muralidharan and Niehaus",
                  2022: r"Aiken et al."}, scale=("nation",), horizon=("a decade",))
        self.scaling()
        self.maps()
        self.togo()

    def scaling(self):
        cards = point_cards([
            (r"the unit", r"randomize what \\ governments decide: \\ whole districts, \\ not villages", TRIAL),
            (r"the market", r"measure prices \\ and wages too: \\ chapter six's \\ multiplier", TOWN),
            (r"the implementer", r"the civil service, \\ not a charity's \\ best staff", HOLD),
            (r"the politics", r"who keeps a \\ programme going \\ when the \\ researchers leave", HIST),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"experiments at scale", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.FRONTIER46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The first frontier is a reply to Deaton. Karthik Muralidharan and Paul Niehaus argued for running "
            "experiments at the scale at which policy is made. <bookmark mark='a'/> Randomize the unit a government "
            "actually decides about, whole districts or states, not a handful of villages. <bookmark mark='b'/> "
            "Measure what happens to markets, prices and wages, not only to the people treated, as the Kenyan "
            "cash study did. <bookmark mark='c'/> Let the government's own staff run the programme, since they "
            "will run it afterwards. <bookmark mark='d'/> And study the politics of what survives. A trial built "
            "this way answers much of the critique, at the cost of being much harder to run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def maps(self):
        T = tables.FRONTIER46.data
        chain = flow_chain([(r"a few thousand \\ surveyed households", DATA), (r"a model learns \\ from images and \\ "
                                                                              r"phone records", THEORY),
                            (r"predict wealth \\ everywhere else", POOR), (r"a map of poverty", E.ACCENT)],
                           notes=[r"consumption, \\ assets", r"night lights, \ roofs, \\ roads; \ calls, \\ top-ups",
                                  r"where no survey \\ has been", r"in weeks, \\ not years"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        rows = VGroup(
            label(rf"satellites: \ up to {T['satellite']}\% of the variation in local wealth, \ five African countries",
                  font_size=20, color=POOR),
            label(rf"phones: \ Rwanda, \ {T['rwanda_subs']} million subscribers mapped from {T['rwanda_n']} "
                  r"surveyed", font_size=20, color=TOWN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.FRONTIER46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The second frontier is measurement. Household surveys are slow and expensive, and many poor countries "
            "go years without one. <bookmark mark='a'/> Start instead from a few thousand surveyed households, "
            "<bookmark mark='b'/> and train a model to recognise wealth in other data: satellite images of night "
            "lights, roofs and roads, or the records of mobile phones, who calls whom and how much credit they "
            "buy. <bookmark mark='c'/> Then predict wealth everywhere else, <bookmark mark='d'/> and draw a map of "
            f"poverty in weeks. Neal Jean and his coauthors explained up to {T['satellite']} percent of the "
            "variation in local wealth across five African countries from satellite images. Joshua Blumenstock "
            f"and his coauthors mapped wealth across Rwanda from the phone records of {T['rwanda_subs']} million "
            f"subscribers, trained on just {T['rwanda_n']} surveyed people."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rows], lag_ratio=0.6), run_time=2.0)
        self.clear_scene()

    def togo(self):
        Tg = load("target")
        T = tables.FRONTIER46.data
        rules = [(r"at random", Tg["random"], CONTROL), (r"by village", Tg["geographic"], HIST),
                 (r"by phone records", Tg["phone"], TOWN), (r"by a full survey", Tg["registry"], GAIN)]
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rules):
            y = 1.6 - 0.95 * i
            w = v * 9.0
            r = Rectangle(width=w, height=0.6, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-3.0 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=20, color=col).next_to(np.array([-3.2, y, 0]), LEFT, buff=0.1), r,
                            label(rf"{100 * v:.0f}\%", font_size=20, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(rf"the poorest {100 * Tg['share']:.0f}\%: \ the share each rule misses", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.6)
        foot = label(rf"Togo, \ 2020: \ phone-based targeting cut exclusion errors by {T['togo_lo']}--{T['togo_hi']}\% "
                     r"against the geographic options, \\ but did worse than a full registry would have", font_size=19,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In April 2020, as the pandemic closed markets, Togo's government wanted to send emergency cash to its "
            "poorest people, and had no register of who they were. Emily Aiken, Suzanne Bellue, Dean Karlan, "
            "Chris Udry and Joshua Blumenstock helped target it from phone records. The Island can show the "
            "trade-off. <bookmark mark='a'/> A transfer meant for the poorest "
            f"{100 * Tg['share']:.0f} percent, given at random, misses {100 * Tg['random']:.0f} percent of them. "
            f"<bookmark mark='b'/> Given to the poorest villages, it misses {100 * Tg['geographic']:.0f} percent, "
            "because many poor people live in villages that are not poor on average. <bookmark mark='c'/> Ranked "
            f"by a prediction from phone records, {100 * Tg['phone']:.0f} percent. <bookmark mark='d'/> A full "
            f"survey of every household would miss {100 * Tg['registry']:.0f} percent, but would take years. "
            f"<bookmark mark='e'/> In Togo, the phone method cut exclusion errors by {T['togo_lo']} to "
            f"{T['togo_hi']} percent against the geographic options the government considered, and did worse than "
            "a full registry would have. The frontier is to make such tools accurate, fair, and accountable to "
            "the people they sort."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b[0]) for b in bars])
            for mk, b in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[1], LEFT), FadeIn(b[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
