from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class Farms(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Farms, \ phones and firms", r"Why do profitable technologies go unused?",
             "Chapter eleven. Farms, phones and firms.",
             lit={2011: r"Duflo, Kremer and Robinson", 2016: r"Suri and Jack", 2013: r"Bloom et al."},
             scale=("farm", "firm", "nation"), horizon=("a season", "a decade"))
        self.puzzle()
        self.island()
        self.phones()
        self.firms()

    def puzzle(self):
        T = tables.FARMS_46.data
        chain = flow_chain([(r"harvest: \\ cash in hand", FARM), (r"``I'll buy \\ fertilizer later''", HOLD),
                            (r"planting: \\ the cash is gone", LOSS), (r"no fertilizer", LOSS)],
                           notes=[r"fertilizer would \\ pay well", r"a trip to town \\ can wait", r"school fees, \\ "
                                  r"food, \ a funeral", r"again this year"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 1.0)
        offer = label(r"the offer: \ right after harvest, \ a voucher at the regular price, \ free delivery later",
                      font_size=21, color=GAIN).to_edge(DOWN, buff=1.5)
        res = label(rf"{T['farmers']:,} farmers in western Kenya: \ use rose {T['gain']} points from {T['base']}; \ "
                    r"the same offer later did nothing".replace(",", "{,}"), font_size=20,
                    color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.FARMS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In western Kenya, fertilizer used in modest amounts pays well, yet most farmers do not use it. Esther "
            "Duflo, Michael Kremer and Jonathan Robinson asked why. <bookmark mark='a'/> At harvest a farmer has "
            "cash, <bookmark mark='b'/> and means to buy fertilizer, but the trip to town can wait. <bookmark "
            "mark='c'/> By planting time the cash has gone, on school fees, food, or a funeral. <bookmark "
            "mark='d'/> And another season passes without it. That is Part forty-five's present bias, in a field. "
            "<bookmark mark='e'/> So they offered farmers, right after harvest, a voucher for fertilizer at the "
            "regular price, with free delivery later. No discount: just the chance to commit while the money was "
            f"there. <bookmark mark='f'/> Among {T['farmers']:,} farmers, use rose by {T['gain']} points, from "
            f"{T['base']} percent. The same offer made later in the season had no significant effect, and the "
            "harvest-time offer did about as much as a fifty percent subsidy offered later."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("d")
            self.play(Indicate(chain.boxes[3], color=WHITE))
            vo.wait_until("e")
            self.play(FadeIn(offer))
            vo.wait_until("f")
            self.play(FadeIn(res))
        self.clear_scene()

    def island(self):
        F = load("fert")
        Pt = F["patient"]
        arms = [(r"no offer", F["base"], CONTROL), (r"free delivery, \\ offered at harvest", F["harvest_offer"], GAIN),
                (r"the same, \\ offered at planting", F["late_offer"], HOLD),
                (r"half price, \\ at planting", F["planting_subsidy"], CASH)]
        ax = plane([0, 4], [0, 0.6], center=LEFT * 1.8 + DOWN * 0.35, x_length=7.6, y_length=4.6, xticks=[],
                   yticks=[0, 0.2, 0.4, 0.6], ylabel=r"share who use fertilizer", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(arms):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=14, color=WHITE).next_to(ax.ax.c2p(0.5 + i, 0), DOWN, buff=0.12),
                            label(rf"{100 * v:.0f}\%", font_size=17, color=WHITE).next_to(r, UP, buff=0.06)))
        Tf = TRUTH["fert"]
        side = VGroup(
            label(rf"the Island's farmers: \\ $\beta$ from {Tf['beta_lo']} to 1, \\ {100 * Tf['naive']:.0f}\% naive",
                  font_size=18, color=WHITE),
            label(r"the harvest offer \\ removes the trip \\ while cash is there", font_size=18, color=GAIN),
            label(r"later, \ the cash \\ is already gone", font_size=18, color=HOLD),
            label(rf"if all were patient: \\ {100 * Pt['base']:.0f}\% would use it \\ with no offer", font_size=18,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island's farmers have the same problem, with a planted present bias. <bookmark mark='a'/> With "
            f"no offer, {100 * F['base']:.0f} percent use fertilizer. <bookmark mark='b'/> Offer free delivery "
            f"right after harvest, at the regular price, and {100 * F['harvest_offer']:.0f} percent do. The offer "
            "removes the trip at the one moment the cash is there. <bookmark mark='c'/> Offer the same thing at "
            f"planting, and nothing changes: {100 * F['late_offer']:.0f} percent. The cash is already gone. "
            "<bookmark mark='d'/> Cutting the price in half at planting does about as much as the free harvest "
            f"offer, {100 * F['planting_subsidy']:.0f} percent, at far greater cost. <bookmark mark='e'/> And if "
            f"every farmer were patient, {100 * Pt['base']:.0f} percent would use fertilizer with no offer at all. "
            "The gap is procrastination, and timing closes much of it for almost nothing."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            for mk, b in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[0], DOWN), FadeIn(b[2]))
                if mk == "b":
                    self.play(FadeIn(side[1]))
                if mk == "c":
                    self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def phones(self):
        T = tables.FARMS_46.data
        chain = flow_chain([(r"a phone, \\ not a bank", TOWN), (r"money sent \\ by text", TOWN),
                            (r"help arrives \\ after a shock", RISK), (r"savings, \ and \\ new work", GAIN)],
                           notes=[r"M-PESA, \ Kenya, \\ from 2007", r"agents in every \\ village", r"from relatives \\ "
                                  r"far away", r"especially \\ for women"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 1.0)
        res = VGroup(
            label(rf"about {T['households']:,} households, \ {T['share']}\% of Kenya's, \ out of extreme poverty"
                  .replace(",", "{,}"), font_size=21, color=GAIN),
            label(rf"about {T['women']:,} women moved from farming into business".replace(",", "{,}"), font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.8)
        tag = published_tag(tables.FARMS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Some technologies spread without any help. <bookmark mark='a'/> In 2007 Kenya's largest phone company "
            "launched M-PESA, which lets anyone with a basic phone store and send money by text, <bookmark "
            "mark='b'/> through agents in shops in almost every village. <bookmark mark='c'/> William Jack and "
            "Tavneet Suri found that households using it kept their consumption up after a bad shock, because "
            "relatives far away could send money the same day. Chapter ten's village insurance, stretched across a "
            "country. <bookmark mark='d'/> Later, using how far each household lived from the nearest agent, Suri "
            f"and Jack estimated that mobile money had lifted about {T['households']:,} households, two percent of "
            f"Kenya's, out of extreme poverty, and helped about {T['women']:,} women move from farming into "
            "business or retail."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.6), run_time=2.0)
        self.clear_scene()

    def firms(self):
        T = tables.FARMS_46.data
        cards = point_cards([
            (r"the firms", r"Indian textile \\ plants, \ chosen \\ at random", TOWN),
            (r"the treatment", r"free consulting: \\ inventory, \ quality, \\ maintenance", GAIN),
            (r"the result", rf"productivity up \\ {T['management']}\% in the \\ first year", E.ACCENT),
            (r"why not before?", r"owners did not \\ know what they \\ were missing: \\ Part 62", HOLD),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"firms: \ does management matter?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.FARMS_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Firms leave money on the table too. <bookmark mark='a'/> Nicholas Bloom, David McKenzie and their "
            "coauthors chose Indian textile plants at random <bookmark mark='b'/> and gave them free consulting on "
            "basic practices: recording defects, organizing inventory, maintaining machines. <bookmark mark='c'/> "
            f"Productivity rose {T['management']} percent in the first year, and within three years the treated "
            "firms were opening more plants. <bookmark mark='d'/> Why had the owners not done it already? Mostly, "
            "they did not know what they were missing. Part sixty-two returns to management as a technology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
