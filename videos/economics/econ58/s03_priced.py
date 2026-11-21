from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Priced(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Valuing what has a price", r"What is a bridge worth to the people who cross it?",
             "Chapter two. Valuing what has a price.", lit={1844: r"Dupuit", 1997: r"Norway's cost of public funds"},
             scale=("person", "market"), horizon=("a year",))
        self.surplus()
        self.transfers()
        self.shadow()

    def surplus(self):
        B = load("bridge")
        y, p = B["year"], B["params"]
        a, b = p["a"], p["b"]
        ax = plane([0, 2.0], [0, 24], center=LEFT * 2.6 + DOWN * 0.35, x_length=7.0, y_length=5.6,
                   xticks=[0, 0.5, 1.0, 1.5, 2.0], yticks=[0, 4, 8, 12, 16, 20, 24],
                   xlabel=r"crossings a year, \ millions", ylabel=r"cost of a crossing, \ Island dollars \ "
                   r"(fare $+$ time)", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        q = np.linspace(0, a, 50)
        dem = path(ax, q, (a - q) / b, WHITE, 3.0, smooth=False)
        dl = label(r"demand", font_size=18, color=WHITE).next_to(ax.ax.c2p(0.25, (a - 0.25) / b), RIGHT, buff=0.1)
        q0, q1, g0, g1 = y["q0"], y["q1"], y["g0"], y["g1"]
        fare_line = g0 - p["fare"]

        def rect(x0, x1, y0, y1, col, op=0.55):
            p0, p1 = ax.ax.c2p(x0, y0), ax.ax.c2p(x1, y1)
            return Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=col, fill_opacity=op,
                             stroke_width=0).move_to((p0 + p1) / 2)

        fares = rect(0, q0, fare_line, g0, BO)
        time = rect(0, q0, g1, fare_line, TRAV)
        tri = Polygon(ax.ax.c2p(q0, g0), ax.ax.c2p(q0, g1), ax.ax.c2p(q1, g1), fill_color=BEN, fill_opacity=0.6,
                      stroke_width=0)
        f_pt = dot(ax, q0, g0, BO, 0.09)
        b_pt = dot(ax, q1, g1, BEN, 0.09)
        f_l = label(rf"the ferry: \ {p['fare']:.0f} fare $+$ {g0 - p['fare']:.0f} of time", font_size=17,
                    color=BO).next_to(f_pt, UR, buff=0.08)
        b_l = label(rf"the bridge: \ {g1:.1f}", font_size=17, color=BEN).next_to(b_pt, UR, buff=0.08)
        g0l = DashedLine(ax.ax.c2p(0, g0), ax.ax.c2p(q0, g0), color=BO, stroke_width=1.5)
        g1l = DashedLine(ax.ax.c2p(0, g1), ax.ax.c2p(q1, g1), color=BEN, stroke_width=1.5)
        side = VGroup(
            MathTex(r"\Delta CS = q_0\,(g_0 - g_1) + \tfrac12\,(q_1 - q_0)(g_0 - g_1)", font_size=27, color=WHITE),
            label(rf"blue: \ time on today's {q0:.2f}m crossings, \ {y['time']:.1f}", font_size=19, color=TRAV),
            label(rf"lilac: \ fares no longer paid, \ {y['fares']:.1f}", font_size=19, color=BO),
            label(rf"green: \ new crossings, \ half the saving, \ {y['new trips']:.1f}", font_size=19, color=BEN),
            label(r"the rule of a half", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
        tag = island_tag(r"the Island: \ demand for crossings, \ $q = 1.8 - 0.08\,g$", corner=DR, font_size=12)
        with self.voiceover(
            "Dupuit's answer, drawn. <bookmark mark='a'/> The demand for crossings: the cheaper a crossing, the more "
            "people make. Its cost to a traveller is the fare plus the value of the time it takes. <bookmark "
            f"mark='b'/> On the ferry that is {p['fare']:.0f} dollars of fare and {g0 - p['fare']:.0f} dollars of "
            f"time, and the Island makes {q0:.2f} million crossings a year. <bookmark mark='c'/> On a free bridge, "
            f"eight minutes cost {g1:.1f} dollars, and crossings rise to {q1:.2f} million. <bookmark mark='d'/> The "
            "gain to travellers is the area between the two prices, under the demand curve. On the crossings already "
            f"made, each saves the whole difference: {y['time']:.1f} million a year in time, <bookmark mark='e'/> and "
            f"{y['fares']:.1f} million in fares. <bookmark mark='f'/> The new crossings gain less: the first was "
            "almost worth taking on the ferry and gains almost the whole saving, the last was barely worth taking "
            "even on the bridge and gains nothing. On average they gain half, which is why appraisers call it the "
            f"rule of a half: {y['new trips']:.1f} million."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(dem), FadeIn(dl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(f_pt), Create(g0l), FadeIn(f_l))
            vo.wait_until("c")
            self.play(FadeIn(b_pt), Create(g1l), FadeIn(b_l))
            vo.wait_until("d")
            self.play(FadeIn(time), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(fares), FadeIn(side[2]))
            vo.wait_until("f")
            self.play(FadeIn(tri), FadeIn(side[3]), FadeIn(side[4]))
        self.clear_scene()

    def transfers(self):
        B = load("bridge")
        y, p = B["year"], B["params"]
        bo = y["Bo's profit"]
        freed = y["fares"] + bo
        bars = [(r"fares saved \\ by travellers", y["fares"], BO), (r"Bo's lost \\ profit", bo, COST),
                (r"what is left: \\ the ferry's \\ resources freed", freed, BEN)]
        ax = plane([-0.5, 2.5], [-2.5, 4.0], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.0, y_length=4.8,
                   xticks=[], yticks=[-2, 0, 2, 4], ylabel=r"millions a year", yfmt=lambda v: f"{v:+.0f}".replace(
                       "-", "{-}") if v else "0", font_size=15)
        rects, labs, vals = VGroup(), VGroup(), VGroup()
        for k, (t_, v, c_) in enumerate(bars):
            p0, p1 = ax.ax.c2p(k - 0.3, 0), ax.ax.c2p(k + 0.3, v)
            r_ = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), fill_color=c_, fill_opacity=0.8,
                           stroke_width=0).move_to((p0 + p1) / 2)
            rects.add(r_)
            labs.add(label(t_, font_size=16, color=c_).next_to(ax.ax.c2p(k, -2.5), DOWN, buff=0.12))
            vals.add(label(f"${v:+.2f}$".replace("-", "{-}"), font_size=19, color=c_).next_to(
                r_, UP if v >= 0 else DOWN, buff=0.08))
        z = Line(ax.ax.c2p(-0.5, 0), ax.ax.c2p(2.5, 0), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            label(rf"Bo's costs: \ {p['ferry_unit_cost']:.1f} a crossing, \ {p['ferry_fixed']:.1f} a year",
                  font_size=20, color=BO),
            label(rf"{p['ferry_unit_cost']:.1f} $\times$ {y['q0']:.2f} $+$ {p['ferry_fixed']:.1f} $=$ "
                  rf"{freed:.2f}", font_size=22, color=BEN),
            label(r"a transfer is not a benefit: \\ count it on both sides, \ or not at all", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "But the fares are not a gain to the Island. <bookmark mark='a'/> Every dollar of fare a traveller no "
            "longer pays is a dollar Bo no longer receives. <bookmark mark='b'/> Bo counts too: he loses his ferry's "
            f"profit, {abs(bo):.1f} million a year. <bookmark mark='c'/> Add the two, and what is left, "
            f"{freed:.2f} million, is exactly what the ferry cost to run: the boat's fuel, the crew, the upkeep, "
            "resources that can now do something else. <bookmark mark='d'/> That is the rule for every transfer in "
            "an appraisal, from fares to taxes: it is a gain to one side and a loss to the other, and it nets out, "
            "as long as both sides have standing."
        ) as vo:
            self.play(FadeIn(ax), Create(z))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(rects[k], DOWN if bars[k][1] >= 0 else UP), FadeIn(labs[k]), FadeIn(vals[k]))
                if k == 2:
                    self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def shadow(self):
        B = load("bridge")
        base = B["by_rate"]["0.035"]["npv"]
        cards = point_cards([
            (r"shadow prices", r"when a market price misstates a resource's cost to society, \ use what it really "
             r"gives up: \ a builder who would otherwise be idle costs less than the wage", TRAV),
            (r"the shadow wage", rf"if half the bridge's labour would be idle, \ paid at half its wage in the "
             rf"appraisal: \ the cost falls by {B['shadow_saving']:.0f} million, \ the NPV rises from {base:.0f} to "
             rf"{B['npv_shadow']:.0f}", BEN),
            (r"the cost of public funds", rf"taxes distort, \ so a public dollar costs society more than a dollar: "
             rf"\ Norway's guidance adds 20\%; \ applied to the bridge, \ the NPV falls from {base:.0f} to "
             rf"{B['npv_mcpf']:.0f}", COST),
        ], width=12.8, cols=3, font_size=21).move_to(DOWN * 0.2)
        head = label(r"prices that lie, \ and the price of a public dollar", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        tag = published_tag(r"NOU 1997:27 \ (Norway); \ the Island's bridge at 3.5\%", corner=DL, font_size=12)
        with self.voiceover(
            "Two more corrections to market prices. <bookmark mark='a'/> A shadow price is what a resource really "
            "costs society when its market price says otherwise. A builder who would otherwise have been "
            "unemployed gives up much less than the wage to build the bridge. <bookmark mark='b'/> If half the "
            f"bridge's labour came from idle hands, valued at half the wage, the cost would fall by "
            f"{B['shadow_saving']:.0f} million, and the net present value would rise from {base:.0f} million to "
            f"{B['npv_shadow']:.0f}. Most guidance assumes full employment and does not allow this; it is the "
            "first thing a project's promoters ask for. <bookmark mark='c'/> The other correction runs the other "
            "way. A public dollar is raised by taxes that distort, so it costs society more than a dollar: Part "
            "forty-one's marginal cost of public funds. Norway's guidance has long added twenty percent to every "
            f"krone of public spending. Applied to the bridge, the net present value falls to {B['npv_mcpf']:.0f} "
            "million. The bridge is still worth building, but only just."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
