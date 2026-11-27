from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Land(VoiceoverScene):
    def construct(self):
        card(self, 11, "Land: who keeps the gain", "If farming barely pays, why is farmland so valuable?",
             "Chapter eleven. Land: who keeps the gain.", lit=("moat", "dollar"))
        self.value()
        self.returns()
        self.residual()

    def value(self):
        L = R["land"]
        r = L["real"]
        ys = sorted(r)
        pa = viz.plot_axes([1929, 2027], [0, 4200], x_length=10.8, y_length=4.6, xticks=[1930, 1950, 1970, 1990, 2010, 2026],
                           yticks=[1000, 2000, 3000, 4000], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"${v / 1000:g}tn", size=14).move_to([0.2, -0.45, 0])
        t = ValueTracker(ys[0])

        def line():
            q = [pa.ax.c2p(y, r[y]) for y in ys if y <= t.get_value()]
            return VMobject(stroke_color=LAND, stroke_width=3.5).set_points_as_corners(q) if len(q) > 1 else VMobject()
        ln = always_redraw(line)
        pk = Dot(pa.ax.c2p(1980, r[1980]), color=WHITE, radius=0.07)
        pkl = VGroup(tx("1980", 15, WHITE, bold=True), tx(f"${r[1980] / 1000:.1f}tn", 14, GREY_A)).arrange(DOWN, buff=0.02).next_to(
            pk, UP, buff=0.1)
        lo = Dot(pa.ax.c2p(1991, r[1991]), color=STATE, radius=0.07)
        lol = VGroup(tx("1991", 15, STATE, bold=True), tx(f"-{100 * (1 - r[1991] / r[1980]):.0f}%", 14, STATE)).arrange(
            DOWN, buff=0.02).next_to(lo, DOWN, buff=0.1)
        now = VGroup(tx(f"2026: ${L['nominal'][2026] / 1000:.1f} trillion", 18, LAND, bold=True),
                     tx(f"about ${L['acre_value']:,.0f} an acre of farmland (2025)", 15, GREY_A)).arrange(DOWN, buff=0.04).next_to(
            pa.ax.c2p(2026, r[2026]), LEFT, buff=0.25).shift(DOWN * 0.2)
        head = tx("The value of US farm real estate, in 2026 dollars", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("USDA ERS, Farm Income and Wealth Statistics (3 September 2026), deflated with ERS's GDP deflator; "
                     "acres: USDA NASS", size=13)
        with self.voiceover(
            "So where did the gains of a century of better farming go? Partly to everyone who eats. And partly into "
            "the land. <bookmark mark='a'/> Here is the value of all the farmland and farm buildings in the United "
            "States, after inflation. <bookmark mark='b'/> It rose through the 1970s boom, when farmers borrowed to buy "
            "more land at rising prices, <bookmark mark='c'/> and then collapsed, losing about half its real value "
            "by 1991, as interest rates soared and crop prices fell. Thousands of farms failed. "
            f"<bookmark mark='d'/> Since then it has climbed almost without a break, to about "
            f"{L['nominal'][2026] / 1000:.1f} trillion dollars in 2026: about {L['acre_value']:,.0f} dollars for every "
            "acre of American farmland, more than five times what an acre of corn earns in a good year."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src))
            self.add(ln)
            vo.wait_until("a")
            self.play(t.animate.set_value(1970), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(1980), run_time=1.5, rate_func=linear)
            self.play(FadeIn(pk), FadeIn(pkl))
            vo.wait_until("c")
            self.play(t.animate.set_value(1991), run_time=1.5, rate_func=linear)
            self.play(FadeIn(lo), FadeIn(lol))
            vo.wait_until("d")
            self.play(t.animate.set_value(2026), run_time=3.0, rate_func=linear)
            self.play(FadeIn(now))
        ln.clear_updaters()
        self.clear_scene()

    def returns(self):
        L = R["land"]
        ri, rg = L["ret_income"], L["ret_gains"]
        ys = [y for y in sorted(ri) if y in rg]
        pa = viz.plot_axes([1959.4, 2026.6], [-16, 22], x_length=10.8, y_length=4.4, xticks=[1960, 1980, 2000, 2020],
                           yticks=[-15, -10, -5, 0, 5, 10, 15, 20], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:+g}%" if v else "0",
                           size=14).move_to([0.2, -0.55, 0])
        z = Line(pa.ax.c2p(1959.4, 0), pa.ax.c2p(2026.6, 0), stroke_color=GREY_B, stroke_width=1.2)
        inc = VGroup()
        gain = VGroup()
        for y in ys:
            a, b = ri[y], rg[y]
            p0, p1 = pa.ax.c2p(y, 0), pa.ax.c2p(y, a)
            inc.add(Rectangle(width=0.3, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0, fill_color=CORN,
                              fill_opacity=0.95).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
            base = a if b >= 0 else 0
            q0, q1 = pa.ax.c2p(y, base), pa.ax.c2p(y, base + b)
            gain.add(Rectangle(width=0.3, height=max(abs(q1[1] - q0[1]), 0.01), stroke_width=0,
                               fill_color=LAND if b >= 0 else STATE, fill_opacity=0.9).move_to([q0[0], (q0[1] + q1[1]) / 2, 0]))
        key = VGroup(VGroup(Square(0.18, stroke_width=0, fill_color=CORN, fill_opacity=1),
                            tx(f"return from farming: {L['avg_income']:.1f}% a year since 1990", 15, WHITE)).arrange(RIGHT, buff=0.1),
                     VGroup(Square(0.18, stroke_width=0, fill_color=LAND, fill_opacity=1),
                            tx(f"from the rising value of the land: {L['avg_gains']:.1f}%", 15, WHITE)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.6).next_to(pa, UP, buff=0.15)
        head = tx("The return on US farm assets each year", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("USDA ERS, Farm Income and Wealth Statistics: rate of return on farm assets, current income and capital "
                     "gains", size=13)
        with self.voiceover(
            "This is the deepest clue to our question. <bookmark mark='a'/> The Department of Agriculture splits the "
            "yearly return on all farm assets in two. The gold part is the return from farming: what the crops and "
            f"animals earn on the land and machines. Since 1990 it has averaged about {L['avg_income']:.1f} percent a "
            "year. <bookmark mark='b'/> The brown part is the return from the land itself becoming more valuable: about "
            f"{L['avg_gains']:.1f} percent a year. <bookmark mark='c'/> And the red is what happens when that reverses, "
            "as it did in the 1980s. For most of the last seventy years, American farmers have made more money from "
            "owning land than from farming it. They live poor, as the old saying goes, and die rich."
        ) as vo:
            self.play(FadeIn(pa), Create(z), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(key[0]), LaggedStart(*[GrowFromEdge(b, DOWN) for b in inc], lag_ratio=0.01), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(key[1]), LaggedStart(*[GrowFromEdge(b, DOWN) for b, y in zip(gain, ys) if rg[y] >= 0],
                                                  lag_ratio=0.01), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, UP) for b, y in zip(gain, ys) if rg[y] < 0], lag_ratio=0.05), run_time=1.5)
        self.clear_scene()

    def residual(self):
        A = R["acre"]
        acre = Square(3.2, stroke_color=SOIL, stroke_width=3, fill_color="#3C5A2A", fill_opacity=1).move_to([-4.2, -0.3, 0])
        rows = VGroup(*[Line(acre.get_left() + RIGHT * 0.15 + UP * (y_), acre.get_right() + LEFT * 0.15 + UP * (y_),
                             stroke_color=FARM, stroke_width=2) for y_ in np.linspace(-1.4, 1.4, 12)])
        al = tx("one acre of corn, 2025", 18, WHITE, bold=True).next_to(acre, UP, buff=0.15)
        lines = VGroup(tx(f"the crop: ${A['revenue']:.0f}", 20, CORN, bold=True),
                       tx(f"all costs except the land: ${A['cost'] - A['land']:.0f}", 20, COST),
                       tx(f"left to pay for the land: ${A['land_residual']:.0f}", 22, LAND, bold=True),
                       tx(f"what renting such land costs: ${A['land']:.0f}", 20, WHITE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.18).move_to([2.2, 0.6, 0])
        ric = VGroup(tx("David Ricardo, 1817: rent is what is left", 17, GREY_A),
                     tx("after paying for everything else.", 17, GREY_A),
                     tx("Good years are bid into the price of land;", 17, WHITE),
                     tx("bad years are paid by whoever farms it.", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06
                                                                                      ).move_to([2.2, -2.1, 0])
        src = source("USDA ERS, commodity costs and returns, corn, 2025; computed, the Works (farm.py)", size=13)
        with self.voiceover(
            "Why does the land capture the gains? <bookmark mark='a'/> Go back to our acre of corn. The crop brought in "
            f"{A['revenue']:.0f} dollars. <bookmark mark='b'/> Everything except the land cost about "
            f"{A['cost'] - A['land']:.0f}. <bookmark mark='c'/> So the most a farmer could pay for that acre this year, "
            f"and still break even, was about {A['land_residual']:.0f} dollars. <bookmark mark='d'/> But land like it "
            f"rents for about {A['land']:.0f}. The rent was set in better years, by farmers competing to farm more "
            "acres, and a bad year does not change it at once. <bookmark mark='e'/> The economist David Ricardo "
            "explained this two centuries ago: rent is what is left over after every other cost. When a new seed or a "
            "high price makes farming more profitable, farmers bid the gain into the rent and the price of land. When "
            "the price falls, whoever farms the land takes the loss. The landowner keeps the good years; the farmer "
            "lives through the bad ones."
        ) as vo:
            self.play(FadeIn(src), FadeIn(acre), Create(rows), FadeIn(al))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(lines[k], shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in ric], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()
