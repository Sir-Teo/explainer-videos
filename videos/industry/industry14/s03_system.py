from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class System(VoiceoverScene):
    def construct(self):
        card(self, 2, "Water as a system", "What does a water company actually own?",
             "Chapter two. Water as a system.", lit=("unit", "make"))
        self.path()
        self.needs()
        self.capital()

    def path(self):
        # a loop: river (left) -> treatment -> tower -> street -> home -> sewer -> works -> river (right)
        river_l = Rectangle(width=1.2, height=2.2, stroke_width=0, fill_color=WATER, fill_opacity=0.55).move_to([-6.4, -1.4, 0])
        river_r = Rectangle(width=1.2, height=2.2, stroke_width=0, fill_color=WATER, fill_opacity=0.55).move_to([6.4, -1.4, 0])
        plant = VGroup(*[VGroup(Rectangle(width=0.7, height=0.45, stroke_color="#8B95A7", stroke_width=2,
                                          fill_color="#1B2230", fill_opacity=1),
                                Rectangle(width=0.62, height=0.25, stroke_width=0, fill_color=WATER, fill_opacity=0.7).shift(DOWN * 0.07))
                         for _ in range(3)]).arrange(RIGHT, buff=0.08).move_to([-4.3, -0.5, 0], aligned_edge=DOWN)
        tower = draw.water_tower(1.9).move_to([-1.7, -0.5, 0], aligned_edge=DOWN)
        home = draw.house(0.9, "#C9D3E0").move_to([1.0, -0.5, 0], aligned_edge=DOWN)
        works = VGroup(*[Circle(radius=0.32, stroke_color="#8B95A7", stroke_width=3, fill_color=SEWAGE, fill_opacity=0.55)
                         for _ in range(2)]).arrange(RIGHT, buff=0.15).move_to([4.2, -1.95, 0])
        mains = VMobject(stroke_color=WATER, stroke_width=8).set_points_as_corners(
            [[-5.8, -0.8, 0], [-4.3, -0.8, 0], [-4.3, -0.5, 0], [-4.3, -0.8, 0], [-1.7, -0.8, 0], [-1.7, -0.5, 0],
             [-1.7, -0.8, 0], [1.0, -0.8, 0], [1.0, -0.5, 0]])
        sewer = VMobject(stroke_color=SEWAGE, stroke_width=10).set_points_as_corners(
            [[1.2, -0.5, 0], [1.2, -1.95, 0], [3.75, -1.95, 0], [4.65, -1.95, 0], [5.8, -1.95, 0]])
        street = Line([-7.2, -0.5, 0], [7.2, -0.5, 0], stroke_color="#3A4152", stroke_width=3)
        under = Rectangle(width=14.4, height=2.6, stroke_width=0, fill_color="#221C16", fill_opacity=1).move_to([0, -1.8, 0])
        labels = VGroup(tx("the river", 15, WATER).next_to(river_l, UP, buff=0.1),
                        tx("treatment: settle,\nfilter, disinfect", 13, GREY_A).next_to(plant, UP, buff=0.12),
                        tx("storage:\nheight is pressure", 13, GREY_A).next_to(tower, RIGHT, buff=0.1).shift(UP * 0.6),
                        tx("mains under\nthe street", 13, WATER).move_to([-0.3, -1.25, 0]),
                        tx("a home", 13, GREY_A).next_to(home, RIGHT, buff=0.1),
                        tx("sewers", 13, SEWAGE).move_to([2.4, -1.6, 0]),
                        tx("sewage works", 13, GREY_A).next_to(works, DOWN, buff=0.1),
                        tx("back to the river", 15, WATER).next_to(river_r, UP, buff=0.1))
        drops = VGroup(*[draw.drop(0.18) for _ in range(10)])
        t = ValueTracker(0)

        def place(m):
            for k, d in enumerate(m):
                a = (t.get_value() + k / len(m)) % 1.0
                d.move_to(mains.point_from_proportion(a))
        drops.add_updater(place)
        muck = VGroup(*[Dot(radius=0.07, color="#C9A66B") for _ in range(8)])
        u = ValueTracker(0)

        def place2(m):
            for k, d in enumerate(m):
                d.move_to(sewer.point_from_proportion((u.get_value() + k / len(m)) % 1.0))
        muck.add_updater(place2)
        weight = VGroup(tx("1 cubic metre of water = 1 tonne", 22, WHITE, bold=True),
                        tx("too heavy to move far: each town has its own pipes", 16, GREY_A)).arrange(DOWN, buff=0.08).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A water company sells something that falls from the sky. What it actually owns is a machine for moving it. "
            "<bookmark mark='a'/> Water is taken from a river, a reservoir or the ground. <bookmark mark='b'/> It is "
            "cleaned: settled, filtered and disinfected. <bookmark mark='c'/> It is stored, often up high, because height "
            "is pressure. <bookmark mark='d'/> Then it runs through mains under the street to every home and business. "
            "<bookmark mark='e'/> What goes down the drain runs the other way, through sewers, to a works that treats it "
            "and returns it to a river. <bookmark mark='f'/> A cubic metre of water weighs a tonne. It is too heavy to "
            "move far, so every town has its own pipes, and the company that owns them has no competitor on the street."
        ) as vo:
            self.play(FadeIn(under), FadeIn(street))
            vo.wait_until("a")
            self.play(FadeIn(river_l), FadeIn(labels[0]))
            vo.wait_until("b")
            self.play(FadeIn(plant), FadeIn(labels[1]), Create(mains), run_time=1.5)
            self.add(drops)
            self.play(t.animate.set_value(0.4), run_time=2, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(tower), FadeIn(labels[2]), t.animate.set_value(0.8), run_time=1.5, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(home), FadeIn(labels[3]), FadeIn(labels[4]), t.animate.set_value(1.6), run_time=2.5, rate_func=linear)
            vo.wait_until("e")
            self.play(Create(sewer), FadeIn(labels[5]), t.animate.set_value(2.0), run_time=1.5, rate_func=linear)
            self.add(muck)
            self.play(FadeIn(works), FadeIn(labels[6]), FadeIn(river_r), FadeIn(labels[7]), u.animate.set_value(1.0),
                      t.animate.set_value(2.8), run_time=3, rate_func=linear)
            vo.wait_until("f")
            self.play(FadeIn(weight, shift=DOWN * 0.1), t.animate.set_value(3.4), u.animate.set_value(1.6), run_time=2.5, rate_func=linear)
        drops.clear_updaters()
        muck.clear_updaters()
        self.clear_scene()

    def needs(self):
        S = R["system"]
        dw = S["dw"]
        parts = [("pipes: distribution and transmission", dw["dist"], WATER), ("treatment", dw["treat"], "#7EC8F5"),
                 ("storage", dw["storage"], "#9AA3B2"), ("source: intakes and wells", dw["source"], "#5D6B82"),
                 ("other", S["dw_total"] - sum(dw.values()), "#3A4152")]
        sc = 6.0 / S["dw_total"]
        x = -6.0
        blocks = VGroup()
        for name, v, col in parts:
            b = Rectangle(width=v * sc, height=1.0, stroke_color="#0E1117", stroke_width=2, fill_color=col, fill_opacity=0.9).move_to(
                [x, 1.2, 0], aligned_edge=LEFT)
            x += v * sc
            blocks.add(b)
        blabs = VGroup(tx(f"pipes ${dw['dist']:.0f}bn", 16, WHITE, bold=True).move_to(blocks[0]),
                       tx(f"treatment\n${dw['treat']:.0f}bn", 12, "#0E1117", bold=True).move_to(blocks[1]))
        dw_head = VGroup(tx(f"Drinking water: ${S['dw_total']:.0f}bn over 20 years", 20, WATER, bold=True)).next_to(blocks, UP, buff=0.15).align_to(blocks, LEFT)
        cw = Rectangle(width=S["cw"] * sc, height=1.0, stroke_width=0, fill_color=SEWAGE, fill_opacity=0.9).move_to([-6.0, -0.9, 0], aligned_edge=LEFT)
        cw_head = tx(f"Sewers, sewage works and storm water: ${S['cw']:.0f}bn", 20, SEWAGE, bold=True).next_to(cw, UP, buff=0.15).align_to(cw, LEFT)
        facts = VGroup(*[VGroup(tx(a_, 30, c_, bold=True), tx(b_, 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
                         for a_, b_, c_ in ((f"{S['pws']:,.0f}", "public water systems", WHITE),
                                            (f"{S['potw']:,.0f}", f"public sewage works,\nserving {S['potw_pop']:.0f} million people", WHITE),
                                            (f"{S['lead']:.0f} million", "lead pipes still joining\nhomes to the mains", BAD))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.9, -0.2, 0])
        head = tx("What America's water systems say they need", 24, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("US EPA, 7th Drinking Water Infrastructure Needs Survey (2023); Clean Watersheds Needs Survey 2022; "
                     "Information about Public Water Systems", size=13)
        with self.voiceover(
            "That machine is almost all fixed cost, in things that last for decades. Every few years America's "
            "Environmental Protection Agency asks the country's water systems what they need to spend over the next "
            f"twenty years. <bookmark mark='a'/> For drinking water, the answer was about ${S['dw_total']:.0f} billion. "
            f"<bookmark mark='b'/> About ${dw['dist']:.0f} billion of it, two dollars in every three, is pipes: replacing "
            "and repairing the mains under the streets. <bookmark mark='c'/> For sewers, sewage works and storm water, "
            f"another ${S['cw']:.0f} billion. <bookmark mark='d'/> All of it spread across more than "
            f"{S['pws']:,.0f} public water systems and {S['potw']:,.0f} public sewage works, with about "
            f"{S['lead']:.0f} million lead pipes still connecting homes to the mains."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(dw_head), LaggedStart(*[GrowFromEdge(b, LEFT) for b in blocks], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(blabs), Indicate(blocks[0], color=WATER, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(cw_head), GrowFromEdge(cw, LEFT), run_time=1.5)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.15), run_time=2.0)
        self.clear_scene()

    def capital(self):
        S = R["system"]
        cd = S["capdep"]["AWK"]
        ys = sorted(cd)
        pa = viz.plot_axes([ys[0] - 0.7, ys[-1] + 0.7], [0, 3.5], x_length=9.0, y_length=4.4, xticks=[2010, 2013, 2016, 2019, 2022, 2025],
                           yticks=[1, 2, 3], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}bn", ylabel="American Water, each year",
                           size=13).move_to([-1.0, -0.4, 0])
        bars, deps = VGroup(), VGroup()
        for y in ys:
            c, d = cd[y]
            x0, y0 = pa.ax.c2p(y, 0)[:2]
            y1 = pa.ax.c2p(y, c)[1]
            y2 = pa.ax.c2p(y, d)[1]
            bars.add(Rectangle(width=0.32, height=y1 - y0, stroke_width=0, fill_color=WATER, fill_opacity=0.85).move_to([x0 - 0.08, y0, 0], aligned_edge=DOWN))
            deps.add(Rectangle(width=0.32, height=y2 - y0, stroke_width=0, fill_color="#8B95A7", fill_opacity=0.9).move_to([x0 + 0.16, y0, 0], aligned_edge=DOWN))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=WATER, fill_opacity=0.85), tx("spent on pipes and plants (capital spending)", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color="#8B95A7", fill_opacity=0.9), tx("worn out, by its accounts (depreciation)", 14, GREY_A)).arrange(RIGHT, buff=0.08)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([2.4, 2.75, 0])
        c25, d25 = cd[ys[-1]]
        note = VGroup(tx(f"{ys[-1]}: ${c25:.1f}bn spent, ${d25:.1f}bn worn out", 18, WHITE, bold=True),
                      tx(f"{S['awk_ratio']:.1f} dollars in for each dollar used up", 16, WATER),
                      tx(f"{S['mains']:,.0f} miles of mains", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-3.0, 0.9, 0])
        src = source("American Water Works, Forms 10-K, 2009-2025 (SEC EDGAR: capital expenditures, depreciation)", size=13)
        with self.voiceover(
            "Watch what that does to a water company's accounts. This is American Water, which describes itself as "
            "the largest regulated water utility in the United States. <bookmark mark='a'/> In blue, what it spends each year on pipes and plants. "
            "<bookmark mark='b'/> In grey, what its accounts say wore out. <bookmark mark='c'/> In 2025 it spent about "
            f"${c25:.1f} billion and used up about ${d25:.1f} billion: {S['awk_ratio']:.1f} dollars in for every dollar "
            "worn out. The pile of assets grows every year. And, as the next chapter shows, a regulated water company "
            "is paid a return on exactly that pile."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.06), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in deps], lag_ratio=0.06), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note, shift=LEFT * 0.1), Indicate(bars[-1], color=WATER))
        self.clear_scene()
