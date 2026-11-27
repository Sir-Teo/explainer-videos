from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Run(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: a cracker for forty years", "It is 2012. Where do you build a six-billion-dollar plant?",
             "Chapter one. Run it: a cracker for forty years.", lit=("make", "change"))
        self.setup_()
        self.costs()
        self.cash()
        self.real()

    def setup_(self):
        G = R["run"]
        cu = draw.cracker_unit(4.2).move_to([-3.6, -0.6, 0])
        sites = VGroup(
            VGroup(tx("A.  Texas, on ethane", 28, TEXAS, bold=True), tx("from America's new shale gas fields,", 19, GREY_A),
                   tx("priced like natural gas", 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05),
            VGroup(tx("B.  Europe, on naphtha", 28, EUROPE, bold=True), tx("a light oil fraction from refineries,", 19, GREY_A),
                   tx("priced like crude oil", 19, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.05)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.0, 1.3, 0])
        facts = VGroup(tx(f"{G['capacity']:.1f} million tonnes of ethylene a year", 20, WHITE, bold=True),
                       tx(f"${G['capex'] / 1000:.0f} billion to build, about forty years to run", 20, WHITE, bold=True),
                       tx("the world price: set by the dearest crackers still needed,", 17, GREY_A),
                       tx("naphtha crackers in Asia, plus more when the market is tight", 17, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.0, -1.8, 0])
        tag = estimate_tag("the Works (cracker.py): EIA's yields; prices of ethane and naphtha, fuel and other costs assumed",
                           corner=DR, size=12)
        with self.voiceover(
            "Play it yourself. It is 2012. You run a chemical company, and you are about to build a steam cracker, the "
            f"furnace at the root of the plastics industry: {G['capacity']:.1f} million tonnes of ethylene a year, about "
            f"{G['capex'] / 1000:.0f} billion dollars, and a life of forty years. <bookmark mark='a'/> You can build it "
            "in Texas, and feed it ethane, a gas that comes out of the ground with natural gas, now pouring from "
            "America's shale fields and priced like natural gas. <bookmark mark='b'/> Or in Europe, near your customers, "
            "and feed it naphtha, a light oil from refineries, priced like crude. <bookmark mark='c'/> Ethylene is sold "
            "around the world at one price, set by the dearest crackers still needed to supply it, naphtha crackers in "
            "Asia, plus a bit more when plants are full. Pause, and choose."
        ) as vo:
            self.play(FadeIn(cu), FadeIn(tag))
            self.play(*[f.animate.scale(1.2) for f in cu.flames], run_time=0.8)
            vo.wait_until("a")
            self.play(FadeIn(sites[0], shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(sites[1], shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(facts))
        self.clear_scene()

    def costs(self):
        G = R["run"]
        ys = G["years"]
        pa = viz.plot_axes([2012.5, ys[-1] + 0.5], [0, 1700], x_length=9.0, y_length=4.4, xticks=[2013, 2016, 2019, 2022, 2025],
                           yticks=[500, 1000, 1500], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:,.0f}",
                           ylabel="a tonne of ethylene", size=13).move_to([-1.4, -0.3, 0])
        lt = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, G["cost_t"][y]) for y in ys])
        le = VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, G["cost_e"][y]) for y in ys])
        lp = VMobject(stroke_color=WHITE, stroke_width=2.5).set_points_as_corners([pa.ax.c2p(y, G["price"][y]) for y in ys])
        gap = Polygon(*[pa.ax.c2p(y, G["price"][y]) for y in ys], *[pa.ax.c2p(y, G["cost_t"][y]) for y in reversed(ys)],
                      stroke_width=0, fill_color=TEXAS, fill_opacity=0.18)
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(t_, 15, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((WHITE, "world price"), (EUROPE, "Europe's cash cost"), (TEXAS, "Texas's cash cost"))]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.8, 1.8, 0])
        side = VGroup(tx("Texas's margin a tonne", 16, TEXAS, bold=True),
                      *[tx(f"{y}: ${G['texas'][y]:,.0f}", 14, GREY_A) for y in (2013, 2016, 2020, 2023, ys[-1])],
                      tx("Europe's margin a tonne", 16, EUROPE, bold=True),
                      *[tx(f"{y}: ${G['europe'][y]:,.0f}", 14, GREY_A) for y in (2013, 2021, ys[-1])]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.8, -1.2, 0])
        tag = estimate_tag("the Works (cracker.py), with the IMF's gas and Brent prices, year by year", corner=DR, size=12)
        with self.voiceover(
            "Here is what a tonne of ethylene would have cost each plant to make, year by year, with the real prices "
            "of gas and oil. <bookmark mark='a'/> The world price, set by the dearest crackers. <bookmark mark='b'/> "
            "The European cracker on naphtha: it is one of those dear crackers, so the price barely covers its costs. "
            "<bookmark mark='c'/> And the Texas cracker on ethane: hundreds of dollars a tonne cheaper, every single "
            f"year, in 2013 almost a thousand dollars. <bookmark mark='d'/> That gap is its margin: about "
            f"{G['texas'][2016]:.0f} dollars a tonne even in a bad year like 2016, against "
            f"{G['europe'][2016]:.0f} in Europe."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(tag), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(lp), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(le), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lt), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(gap), FadeIn(side, shift=LEFT * 0.2))
        self.clear_scene()

    def cash(self):
        G = R["run"]
        ys = G["years"]
        top = max(max(G["cum_texas"]), G["capex"]) * 1.1
        pa = viz.plot_axes([2012.5, ys[-1] + 0.5], [-2000, top], x_length=9.0, y_length=4.4,
                           xticks=[2013, 2016, 2019, 2022, 2025], yticks=[0, 4000, 8000, 12000], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"${v / 1000:.0f}bn", ylabel="cash earned since 2013, after fixed costs", size=13).move_to(
            [-1.2, -0.3, 0])
        zero = Line(pa.ax.c2p(2012.5, 0), pa.ax.c2p(ys[-1] + 0.5, 0), stroke_color=GREY_B, stroke_width=1.2)
        cap = DashedLine(pa.ax.c2p(2012.5, G["capex"]), pa.ax.c2p(ys[-1] + 0.5, G["capex"]), stroke_color=PRICE,
                         stroke_width=2, dash_length=0.1)
        cl = tx(f"what it cost to build: ${G['capex'] / 1000:.0f}bn", 14, PRICE).next_to(cap, UP, buff=0.05).align_to(cap, LEFT)
        lt = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners(
            [pa.ax.c2p(y, c) for y, c in zip(ys, G["cum_texas"])])
        le = VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners(
            [pa.ax.c2p(y, c) for y, c in zip(ys, G["cum_europe"])])
        pb = G["payback"]
        mk = VGroup(Dot(pa.ax.c2p(pb, G["capex"]), radius=0.07, color=TEXAS),
                    tx(f"paid back by {pb}", 15, TEXAS, bold=True).next_to(pa.ax.c2p(pb, G["capex"]), DOWN + RIGHT, buff=0.1))
        res = VGroup(tx(f"Texas: ${G['cum_texas'][-1] / 1000:.1f}bn by {ys[-1]}", 18, TEXAS, bold=True),
                     tx(f"Europe: ${G['cum_europe'][-1] / 1000:.1f}bn by {ys[-1]}", 18, EUROPE, bold=True),
                     tx("never near its cost of building", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to(
            [4.9, -0.8, 0])
        tag = estimate_tag("the Works (cracker.py)", corner=DR, size=12)
        with self.voiceover(
            f"Now add it up, after {G['fixed']:.0f} million dollars a year of fixed costs. <bookmark mark='a'/> The Texas "
            f"cracker earned back its {G['capex'] / 1000:.0f} billion dollars by {pb}, <bookmark mark='b'/> and about "
            f"{G['cum_texas'][-1] / 1000:.0f} billion by {ys[-1]}. <bookmark mark='c'/> The European cracker earned "
            "barely enough to keep running, and nothing like enough to pay for itself. In this industry, the choice "
            "that matters most is made once, when you pick the site and the feedstock, and it decides the next forty "
            "years."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), Create(cap), FadeIn(cl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lt), run_time=2.5)
            self.play(FadeIn(mk))
            vo.wait_until("b")
            self.play(FadeIn(res[0]))
            vo.wait_until("c")
            self.play(Create(le), FadeIn(res[1:]), run_time=2.0)
        self.clear_scene()

    def real(self):
        G = R["run"]
        rows = VGroup()
        items = [(draw.cracker_unit(1.2), "America built", f"US ethylene capacity: about {G['cap13']:.0f} million tonnes a year in "
                  f"early 2013, almost {G['cap20']:.0f} million by 2020 (EIA)"),
                 (draw.factory(1.0), "Europe is closing", f"Dow will shut its ethylene cracker at Böhlen, Germany, by the end "
                  f"of {G['bohlen']:.0f} (10-K)"),
                 (draw.ship(1.3), "or importing the feedstock", f"INEOS's new cracker in Antwerp, Europe's largest, is built to run on "
                  f"about {G['ineos']:.0f},000 barrels a day of American ethane, shipped across the Atlantic (EIA)")]
        for ic, h, d in items:
            ic.scale_to_fit_height(0.8)
            if ic.width > 1.4:
                ic.scale_to_fit_width(1.4)
            rows.add(VGroup(ic, VGroup(tx(h, 22, WHITE, bold=True), tx(d, 16, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.05)).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        head = tx("What the industry actually did", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("EIA, Today in Energy (21 May 2021; 30 March 2026); Dow Inc., Form 10-K 2025", size=13)
        with self.voiceover(
            "And that is what the industry did. <bookmark mark='a'/> From 2013, America built the first new crackers in "
            f"more than a decade, raising its capacity from about {G['cap13']:.0f} to almost {G['cap20']:.0f} million "
            "tonnes of ethylene a year by 2020. <bookmark mark='b'/> Europe has been closing them: Dow will shut its "
            f"cracker at Böhlen in Germany by the end of {G['bohlen']:.0f}. <bookmark mark='c'/> And the one big new "
            "cracker in Europe, INEOS's in Antwerp, was built to run on American ethane, carried across the ocean in "
            "special ships. If you cannot move the plant to the gas, you move the gas."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for m_, r_ in zip("abc", rows):
                vo.wait_until(m_)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
