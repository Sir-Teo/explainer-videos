from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Instruments(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Taxes, \ permits and standards", r"Which instrument should put the price on carbon?",
             "Chapter nine. Taxes, permits and standards.", lit={1974: r"Weitzman", 2005: r"EU ETS",
                                                                2008: r"British Columbia"},
             scale=("firm", "nation"), horizon=("a year", "a decade"))
        self.prices_quantities()
        self.bc()
        self.ets()
        self.others()

    def prices_quantities(self):
        ax = plane([0, 10], [0, 10], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.0, y_length=4.6, xticks=[],
                   yticks=[], xlabel=r"tonnes cut", ylabel=r"dollars a tonne", font_size=15)
        md = seg(ax, 0, 5, 10, 5, LOSS, 3.0)
        lo = seg(ax, 0, 1, 10, 7, CLEAN, 2.6)
        hi = seg(ax, 0, 3, 10, 9, DIRTY, 2.6)
        # flat damage at 5; costs low: cut where 1 + 0.6 q = 5 -> 6.67; high: 3 + 0.6 q = 5 -> 3.33; cap at 5
        cap = vline(ax, 5, 0, 10, POLICY)
        tri_hi = Polygon(ax.ax.c2p(3.33, 5), ax.ax.c2p(5, 5), ax.ax.c2p(5, 6), stroke_width=0, fill_color=POLICY,
                         fill_opacity=0.5)
        tri_lo = Polygon(ax.ax.c2p(5, 4), ax.ax.c2p(5, 5), ax.ax.c2p(6.67, 5), stroke_width=0, fill_color=POLICY,
                         fill_opacity=0.5)
        labs = VGroup(label(r"damage of a tonne", font_size=15, color=LOSS).next_to(ax.ax.c2p(10, 5), UP, buff=0.08),
                      label(r"cost of cutting, \ if cheap", font_size=15, color=CLEAN).next_to(ax.ax.c2p(10, 7), RIGHT,
                                                                                              buff=0.08),
                      label(r"if dear", font_size=15, color=DIRTY).next_to(ax.ax.c2p(10, 9), RIGHT, buff=0.08),
                      label(r"a cap", font_size=15, color=POLICY).next_to(ax.ax.c2p(5, 10), UP, buff=0.05))
        side = VGroup(
            label(r"a year's emissions \\ barely change the \\ stock in the air, \\ so the damage of a \\ tonne is "
                  r"nearly flat", font_size=18, color=WHITE),
            label(r"a tax at the damage: \\ firms cut just enough, \\ whatever their costs", font_size=18,
                  color=LOSS),
            label(r"a cap fixed in advance: \\ too much cutting if \\ costs are high, \ too \\ little if low "
                  r"(purple)", font_size=18, color=POLICY),
            label(r"Part 15's rule: \ when \\ damage is flat, \\ set the price", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = published_tag(r"Weitzman, \ Review of Economic Studies (1974), \ as in Part 15", corner=DR, font_size=11)
        with self.voiceover(
            "A carbon price can be set directly, as a tax, or indirectly, by capping emissions and letting firms "
            "trade permits. Part fifteen showed which is better when costs are uncertain. <bookmark mark='a'/> "
            "Carbon dioxide is a stock pollutant: one year's emissions add little to what is already in the air, "
            "so the damage of one more tonne hardly depends on how many are emitted this year. The damage line is "
            "nearly flat. <bookmark mark='b'/> Nobody knows in advance how cheap cutting will be. A tax set at the "
            "damage lets firms cut until their cost of cutting reaches it, the right amount whether cutting proves "
            "cheap or dear. <bookmark mark='c'/> A cap fixes the amount instead. If cutting turns out dear, it "
            "forces too much; if cheap, too little; the purple triangles are the waste. <bookmark mark='d'/> Martin "
            "Weitzman's rule from 1974: when damage is flat and costs uncertain, set the price. That favours a "
            "carbon tax, or a permit market with a floor and a ceiling on its price."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(md), FadeIn(labs[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(lo), Create(hi), FadeIn(labs[1]), FadeIn(labs[2]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(cap), FadeIn(labs[3]), FadeIn(tri_hi), FadeIn(tri_lo), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def bc(self):
        T = tables.INSTRUMENTS_48.data
        known = [(2008.5, 10), (2009.5, 15), (2010.5, 20), (2011.5, 25), (2012.5, 30)]
        ax = plane([2007, 2026.5], [0, 90], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[2008, 2012, 2016, 2020, 2024], yticks=[0, 20, 40, 60, 80], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"British Columbia's carbon tax, \ C\$ a tonne", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = []
        for (x, y), (x2, _) in zip(known, known[1:] + [(2018.0, 30)]):
            pts += [ax.ax.c2p(x, y), ax.ax.c2p(x2, y)]
        steps = VMobject(stroke_color=POLICY, stroke_width=3.2)
        steps.set_points_as_corners(pts)
        later = VGroup(DashedLine(ax.ax.c2p(2018.0, 30), ax.ax.c2p(2019.3, 40), color=POLICY, stroke_width=2.6),
                       DashedLine(ax.ax.c2p(2019.3, 40), ax.ax.c2p(2024.3, 80), color=POLICY, stroke_width=2.6),
                       Line(ax.ax.c2p(2024.3, 80), ax.ax.c2p(2025.25, 80), color=POLICY, stroke_width=3.2),
                       Line(ax.ax.c2p(2025.25, 80), ax.ax.c2p(2025.25, 0), color=LOSS, stroke_width=3.2),
                       Line(ax.ax.c2p(2025.25, 0), ax.ax.c2p(2026.3, 0), color=LOSS, stroke_width=3.2))
        dots = VGroup(*[dot(ax, x, y, WHITE, 0.06) for x, y in known + [(2019.3, 40), (2024.3, 80)]])
        side = VGroup(
            label(rf"July 2008: \ C\${T['bc_2008']}, \\ rising \$5 a year \\ to C\${T['bc_2012']} in 2012",
                  font_size=18, color=POLICY),
            label(r"revenue returned \\ by cutting income \\ taxes", font_size=18, color=WHITE),
            label(rf"C\${T['bc_2019']} in 2019, \\ C\${T['bc_2024']} in 2024", font_size=18, color=POLICY),
            label(r"April 2025: \\ the consumer tax \\ is abolished", font_size=19, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        foot = label(r"dashed: \ the steps between 2018, \ 2019 and 2024 are not shown", font_size=15,
                     color=GREY_A).next_to(ax, DOWN, buff=0.55)
        tag = published_tag(tables.INSTRUMENTS_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "British Columbia ran the textbook experiment. <bookmark mark='a'/> In July 2008 the province taxed "
            f"carbon at {T['bc_2008']} Canadian dollars a tonne, rising five dollars a year to {T['bc_2012']} in 2012. "
            "<bookmark mark='b'/> It was designed to be revenue neutral: every dollar raised was returned by "
            "cutting income taxes, so the tax changed what was cheap, not how much the government took. <bookmark "
            f"mark='c'/> The rate was held for years, then rose again, to {T['bc_2019']} dollars in 2019 and "
            f"{T['bc_2024']} in 2024, by then within Canada's national price. <bookmark mark='d'/> In March 2025 "
            "Canada's new prime minister ended the national consumer carbon price, and British Columbia abolished "
            "its own from the first of April. A tax that economists had held up for seventeen years lost the vote "
            "it needed. The economics of a carbon price is simple; its politics, as Part forty-seven showed, is not."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(foot), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(steps), FadeIn(dots[:5]), FadeIn(side[0]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(later[:3]), FadeIn(dots[5:]), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(later[3:]), FadeIn(side[3]))
        self.clear_scene()

    def ets(self):
        T = tables.INSTRUMENTS_48.data
        chain = flow_chain([(r"a cap on \\ total emissions", POLICY), (r"permits, \\ auctioned or given", POLICY),
                            (r"firms trade \\ the permits", GAIN), (r"one price for \\ every tonne", CO2)],
                           notes=[r"power plants and \\ heavy industry", r"one per tonne", r"who can cut \\ cheaply, "
                                                                                          r"sells", r"cuts where "
                                                                                                    r"they \\ "
                                                                                                    r"cost least"],
                           box_w=2.8, font_size=20, note_size=16).move_to(UP * 1.2)
        facts = VGroup(
            label(rf"the EU's market began in {T['eu_start']}", font_size=22, color=WHITE),
            label(r"too many permits, \ a recession: \ for years the price stayed low", font_size=21, color=GREY_A),
            label(rf"after reforms that withdrew permits, \ above EUR {T['eu_peak']} a tonne for the first time "
                  r"in February 2023", font_size=21, color=CO2),
        ).arrange(DOWN, buff=0.28).move_to(DOWN * 1.9)
        tag = published_tag(tables.INSTRUMENTS_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The European Union chose permits. <bookmark mark='a'/> A cap on the total emissions of its power "
            "plants and heavy industry, <bookmark mark='b'/> one permit for each tonne, auctioned or handed out, "
            "<bookmark mark='c'/> traded among the firms, so that those who can cut cheaply sell their spare permits "
            "to those who cannot, <bookmark mark='d'/> until every tonne carries the same price, and the cutting is "
            f"done wherever it costs least. <bookmark mark='e'/> The market began in {T['eu_start']}. <bookmark "
            "mark='f'/> For years it issued too many permits, a recession cut emissions further, and the price "
            "stayed low, the cap's weakness that the last diagram warned of. <bookmark mark='g'/> Reforms withdrew "
            f"surplus permits, and in February 2023 the price passed {T['eu_peak']} euros a tonne for the first time."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            for mk, f_ in zip("efg", facts):
                vo.wait_until(mk)
                self.play(FadeIn(f_, shift=UP * 0.1))
        self.clear_scene()

    def others(self):
        cards = point_cards([
            (r"a carbon price", r"one price everywhere: \\ cuts happen where \\ they are cheapest", CO2),
            (r"standards", r"fuel economy, \\ appliances: \ visible, \\ popular, \ but the \\ cost of a tonne "
                           r"\\ differs by rule", POLICY),
            (r"subsidies", r"for clean power \\ and cars: \ paid \\ for by taxpayers, \\ partly for what \\ would "
                           r"happen anyway", POLICY),
            (r"why use them", r"politics; \ and where \\ prices work badly: \\ new technology, \\ inattentive "
                              r"buyers", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"the other instruments", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Most climate policy is neither a tax nor a cap. <bookmark mark='a'/> A single carbon price makes every "
            "tonne cost the same, so cuts happen wherever they are cheapest. <bookmark mark='b'/> Standards, for "
            "the fuel economy of cars or the efficiency of appliances, are visible and popular, but each rule "
            "implies its own cost per tonne, and some are far dearer than others. <bookmark mark='c'/> Subsidies "
            "for clean power and electric cars are paid for by taxpayers, and partly reward what buyers would have "
            "done anyway. <bookmark mark='d'/> Why use them? Partly politics: subsidies are easier to pass than "
            "taxes, as British Columbia just showed. And partly because prices work badly in places: for "
            "technologies too new to be learned by anyone but the first buyer, the subject of chapter eleven, and "
            "for buyers who do not notice running costs, as Part forty-five's inattention suggests."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
