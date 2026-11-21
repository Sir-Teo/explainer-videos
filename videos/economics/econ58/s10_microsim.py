from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


def decile_bars(ax, rows, color, key="pct"):
    g = VGroup()
    for r in rows:
        v = r[key]
        p0, p1 = ax.ax.c2p(r["decile"] - 0.34, 0), ax.ax.c2p(r["decile"] + 0.34, v)
        h = max(abs(p1[1] - p0[1]), 0.004)
        g.add(Rectangle(width=p1[0] - p0[0], height=h, fill_color=color if v >= 0 else COST, fill_opacity=0.85,
                        stroke_width=0).move_to(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2, 0)))
    return g


class Microsim(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Microsimulation", r"Who gains and who loses, \ household by household?",
             "Chapter eight. Microsimulation.", lit={1957: r"Orcutt", 1993: r"TAXSIM"},
             scale=("household", "nation"), horizon=("a year",))
        self.calculator()
        self.allowance()
        self.package()

    def calculator(self):
        M = load("microsim")
        b = M["benefits"]
        chain = flow_chain([(r"each adult's earnings, \ from the survey", GREY_B),
                            (r"income tax, \ adult by adult", STATIC),
                            (r"child benefit", BEN),
                            (r"the family credit, \ means-tested", BEHAV),
                            (r"net income", WHITE)], direction=RIGHT, box_w=2.25, box_h=1.25, buff=0.32,
                           font_size=18,
                           notes=[r"6,000 households".replace(",", "{,}"),
                                  r"15,000 free; \ 20\%, \ 35\%, \ 40\%".replace(",", "{,}"),
                                  rf"{b['child']:,.0f} a child".replace(",", "{,}"),
                                  rf"{b['credit']:,.0f}, \ less 30\% above 20,000".replace(",", "{,}"),
                                  r"before and after the reform"], note_size=16)
        chain.move_to(UP * 0.9)
        gross = VGroup(
            label(rf"6,000 records \ $\times$ \ weights \ $=$ \ {M['households']:,.0f} households, \ "
                  rf"{M['people']:,.0f} people".replace(",", "{,}"), font_size=23, color=GREY_A),
            label(rf"income tax {M['tax_total'] / 1000:.2f} billion a year; \ benefits {M['benefit_total']:.0f} "
                  r"million", font_size=23, color=GREY_A),
        ).arrange(DOWN, buff=0.25).next_to(chain, DOWN, buff=0.9)
        hc = history_card(1957, r"Guy Orcutt", r"simulate the economy one household at a time, \ then add them "
                          r"up", color=E.ACCENT, width=6.0, font_size=19).move_to(UP * 0.2)
        tag = island_tag(r"the Island: \ a household survey", corner=DR, font_size=12)
        with self.voiceover(
            "A tax law changes thousands of households in thousands of ways, and the only way to know who gains is "
            "to compute it for each. Guy Orcutt proposed simulating an economy one household at a time in 1957. "
            "<bookmark mark='a'/> A microsimulation model takes a household survey, <bookmark mark='b'/> computes "
            "each adult's income tax under the rules, <bookmark mark='c'/> adds the child benefit, <bookmark "
            "mark='d'/> works out the means-tested credit, which is withdrawn as earnings rise, <bookmark "
            "mark='e'/> and arrives at each household's net income, before and after a reform. <bookmark mark='f'/> "
            f"The Island's survey has six thousand records; their weights gross them up to {M['households']:,.0f} "
            f"households and {M['people']:,.0f} people, paying {M['tax_total'] / 1000:.2f} billion of income tax a "
            "year. Every total in what follows is a weighted sum."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.1))
            for k, mk in enumerate("abcde"):
                vo.wait_until(mk)
                if not k:
                    self.play(FadeOut(hc), run_time=0.5)
                anims = [FadeIn(chain.boxes[k], shift=UP * 0.1), FadeIn(chain.notes[k])]
                if k:
                    anims.append(GrowArrow(chain.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("f")
            self.play(FadeIn(gross, shift=UP * 0.1))
        self.clear_scene()

    def table_axes(self):
        return plane([0.4, 10.6], [-3.5, 2.5], center=LEFT * 3.1 + DOWN * 0.5, x_length=6.4, y_length=5.0,
                     xticks=list(range(1, 11)), yticks=[-3, -2, -1, 0, 1, 2], xlabel=r"decile of household income "
                     r"(poorest to richest)", ylabel=r"change in net income, \ \%", xfmt=lambda v: f"{v:.0f}",
                     yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)

    def allowance(self):
        M = load("microsim")
        A_ = M["allowance"]
        ax = self.table_axes()
        z = Line(ax.ax.c2p(0.4, 0), ax.ax.c2p(10.6, 0), color=GREY_C, stroke_width=1.2)
        bars = decile_bars(ax, A_["rows"], BEN)
        r = A_["rows"]
        side = VGroup(
            label(r"the reform: \ the allowance from 15,000 to 18,000".replace(",", "{,}"), font_size=21,
                  color=BEN),
            label(rf"cost: \ {A_['cost']:.0f} million a year", font_size=21, color=COST),
            label(r"the poorest tenth: \ no taxable income, \ no gain", font_size=19, color=GREY_A),
            label(rf"the middle: \ about {r[3]['pct']:.0f}\% \ ({r[3]['gain']:.0f} a year)", font_size=19,
                  color=GREY_A),
            label(rf"the richest tenth: \ {r[9]['gain']:.0f} a year, \ {r[9]['pct']:.1f}\%", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35).shift(UP * 0.3)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island's survey, \ grossed up", corner=DR, font_size=12)
        with self.voiceover(
            "The output that ministers ask for first is the distribution table. <bookmark mark='a'/> Suppose the "
            "Island raises the tax-free allowance from fifteen to eighteen thousand: popular, and simple. <bookmark "
            f"mark='b'/> It costs {A_['cost']:.0f} million a year. <bookmark mark='c'/> Ranked by household income "
            "and cut into tenths, the poorest tenth gains nothing at all: its members earn too little to pay income "
            f"tax in the first place. <bookmark mark='d'/> The middle gains most as a share of income, about "
            f"{r[3]['pct']:.0f} percent, <bookmark mark='e'/> and the richest tenth gains most in money, "
            f"{r[9]['gain']:.0f} dollars a household, but least as a share. A reform described as help for low "
            "earners passes the lowest earners by; only the table shows it."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.12), FadeIn(side[2]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(bars[3], color=WHITE), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Indicate(bars[9], color=WHITE), FadeIn(side[4]))
        self.clear_scene()

    def package(self):
        M = load("microsim")
        A_, P_ = M["allowance"], M["package"]
        ax = self.table_axes()
        z = Line(ax.ax.c2p(0.4, 0), ax.ax.c2p(10.6, 0), color=GREY_C, stroke_width=1.2)
        before = decile_bars(ax, A_["rows"], BEN).set_opacity(0.35)
        after = decile_bars(ax, P_["rows"], BEN)
        r = P_["rows"]
        side = VGroup(
            label(r"paid for: \ 45\% on income above 80,000".replace(",", "{,}"), font_size=21, color=BEHAV),
            label(rf"net cost: \ {P_['cost']:.0f} million a year \ (static)", font_size=21, color=COST),
            label(rf"the richest tenth: \ ${r[9]['pct']:.1f}\%$, \ {100 * r[9]['losers']:.0f}\% of them lose"
                  .replace("-", "{-}"), font_size=19, color=COST),
            label(r"the tools: \ NBER's TAXSIM; \ EUROMOD for the European Union; \\ \ \ the IFS's TAXBEN; \ "
                  r"the JCT's and the Tax Policy Center's tables", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Now pay for it. <bookmark mark='a'/> A top rate of forty-five percent on income above eighty thousand "
            f"brings the net cost down to {P_['cost']:.0f} million a year, before anyone responds; the Play it "
            "showed how much less it would raise once they do. <bookmark mark='b'/> The bottom eight tenths keep "
            "almost all their gain. <bookmark mark='c'/> The richest tenth loses "
            f"{abs(r[9]['pct']):.1f} percent of its net income on average, and {100 * r[9]['losers']:.0f} percent "
            "of its households are worse off. <bookmark mark='d'/> Real models run the same arithmetic on real "
            "surveys and real rules: NBER's TAXSIM for American taxes, EUROMOD for every country of the European "
            "Union, the Institute for Fiscal Studies' TAXBEN in Britain, and the distribution tables of the Joint "
            "Committee on Taxation and the Tax Policy Center. The arithmetic is the easy part; the survey's "
            "weights, its missing rich and its under-reported benefits are where the work is."
        ) as vo:
            self.play(FadeIn(ax), Create(z), FadeIn(before))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[TransformFromCopy(b0, b1) for b0, b1 in zip(before[:8], after[:8])],
                                  lag_ratio=0.1), run_time=1.6)
            vo.wait_until("c")
            self.play(TransformFromCopy(before[8], after[8]), TransformFromCopy(before[9], after[9]),
                      FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
