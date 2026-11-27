from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Making(VoiceoverScene):
    def construct(self):
        card(self, 2, "What the machine makers sell", "What is in a machine, and who buys it?",
             "Chapter two. What the machine makers sell: what is inside a machine, and what the two biggest American "
             "makers actually sold in 2025.", lit=("unit", "make"))
        self.inside()
        self.cat()
        self.deere()
        self.suppliers()

    def suppliers(self):
        Cm = R["components"]
        names = {"CMI": ("Cummins: engines", "#C9D3E0"), "ETN": ("Eaton: power and electrical", BLUE),
                 "PH": ("Parker Hannifin: hydraulics and motion", ROBOT)}
        items = [(names[k][0], v[0], names[k][1], f"${v[0]:.1f}bn, keeping {100 * v[1]:.0f}%") for k, v in Cm.items()]
        rows = hbars(items, max_value=36, x0=-0.4, top=1.2, row=1.0, length=5.0, size=17, bar_h=0.5)
        g = draw.gear(0.9).move_to([-5.2, -1.8, 0])
        src = source("Forms 10-K of Cummins, Eaton and Parker Hannifin via SEC company facts: revenue, latest year; median "
                     "net margin 2021-2025", size=12)

        def turn(vo):
            self.play(Rotate(g, PI / 2), run_time=2, rate_func=linear)

        beat(self,
             "The machine makers have makers of their own. <bookmark mark='a'/> Cummins builds engines: "
             f"{Cm['CMI'][0]:.0f} billion dollars of revenue. "
             f"<bookmark mark='b'/> Eaton makes power and electrical equipment, {Cm['ETN'][0]:.0f} billion. "
             f"<bookmark mark='c'/> Parker Hannifin makes hydraulics, pumps and motion controls, {Cm['PH'][0]:.0f} billion, "
             "and its margin has risen from about six per cent in 2010 to eighteen in 2025. Many of their parts go into machines that, "
             "in turn, need those same parts replaced for decades.",
             base=[rows.axis, head("The makers' makers"), g, src], steps=[rows[0], rows[1], rows[2]], after=turn)

    def inside(self):
        ex = draw.excavator(6.0, MACHINE).move_to([-0.6, 0.2, 0])
        labs = [("the engine: diesel, or electric", [-4.6, 2.4, 0], ex[2].get_center()),
                ("hydraulics: pumps, cylinders, valves", [4.5, 2.4, 0], ex.boom[0].get_center()),
                ("tracks and undercarriage: parts that wear", [-3.4, -2.3, 0], ex.tracks.get_center()),
                ("the cab: controls, screens, software", [-0.2, 3.1, 0], ex.cab.get_center())]
        g = VGroup()
        for text, at, to in labs:
            t = tx(text, 16, WHITE, bold=True).move_to(at)
            ln = Line(t.get_bottom() if at[1] > to[1] else t.get_top(), to, stroke_color=GREY_B, stroke_width=1.5, buff=0.08)
            g.add(VGroup(t, ln, Dot(to, radius=0.06, color=MACHINE)))
        src = source("Caterpillar Inc., Form 10-K 2025; Deere & Company, Form 10-K fiscal 2025", size=12)

        def dig(vo):
            p = ex.pivot.get_center()
            self.play(Rotate(ex.boom, 0.35, about_point=p), rate_func=there_and_back, run_time=2.0)

        beat(self,
             "An excavator, a tractor or a mining truck is a big, simple-looking thing made of four parts that matter. "
             "<bookmark mark='a'/> An engine, still mostly diesel. <bookmark mark='b'/> Hydraulics: pumps, cylinders and "
             "valves that turn the engine's power into force. <bookmark mark='c'/> An undercarriage of tracks, pins and "
             "rollers, which wears as the machine works. <bookmark mark='d'/> And a cab "
             "full of controls, screens and, more and more, software. Every one of those parts wears, breaks or needs "
             "updating, and the maker sells the replacements.",
             base=[ex, src], steps=list(g), after=dig)

    def cat(self):
        M = R["making"]
        segs = M["cat"]
        items = [(k, v[0], {"Construction Industries": MACHINE, "Resource Industries": PRICE, "Power & Energy": BLUE,
                            "Financial Products": SERVICE}[k], f"${v[0]:.1f}bn") for k, v in segs.items()]
        items.sort(key=lambda r: -r[1])
        rows = hbars(items, max_value=34, x0=-1.2, top=1.5, row=0.85, length=6.2, size=17, bar_h=0.5)
        note = tx(f"total ${M['cat_rev']:.1f}bn; operating profit ${M['cat_op']:.1f}bn", 17, GREY_A).to_edge(DOWN, buff=0.7)
        src = source("Caterpillar Inc., Form 10-K 2025: sales and revenues by segment", size=12)
        beat(self,
             f"Caterpillar, founded as Caterpillar Tractor in {M['founded']}, sold {M['cat_rev']:.1f} billion dollars in "
             "2025. <bookmark mark='a'/> The biggest part is no longer the yellow machines: it is Power and Energy, "
             f"{segs['Power & Energy'][0]:.1f} billion dollars of engines, turbines and locomotives, up twelve per cent, "
             "driven by large engines for data centres. <bookmark mark='b'/> Then construction machines, "
             f"{segs['Construction Industries'][0]:.1f} billion; mining machines, {segs['Resource Industries'][0]:.1f}; "
             f"<bookmark mark='c'/> and a lender, Cat Financial, with {segs['Financial Products'][0]:.1f} billion of "
             "revenue from financing the machines it sells.",
             base=[rows.axis, head("Caterpillar's sales and revenues, 2025"), note, src],
             steps=[rows[0], VGroup(rows[1], rows[2]), rows[3]])

    def deere(self):
        M = R["making"]
        lines = [("production agriculture", 16.960), ("small agriculture", 7.215), ("construction", 4.570),
                 ("roadbuilding", 3.552), ("turf", 2.731), ("compact construction", 1.922), ("forestry", 1.124)]
        items = [(n, v, "#A3D977" if "agri" in n or n == "turf" else MACHINE, f"${v:.1f}bn") for n, v in lines]
        items.append(("financial products", M["de_fin"], SERVICE, f"${M['de_fin']:.1f}bn"))
        rows = hbars(items, max_value=18, x0=-1.0, top=2.1, row=0.52, length=6.6, size=15, bar_h=0.34)
        tr = draw.tractor(1.6).move_to([-5.0, -2.2, 0]) if hasattr(draw, "tractor") else VGroup()
        src = source("Deere & Company, Form 10-K fiscal 2025: net sales and revenues by product line", size=12)
        beat(self,
             f"Deere, which has made farm equipment since {M['deere_since']}, sold {M['de_rev']:.1f} billion dollars in its "
             "2025 year. <bookmark mark='a'/> Most of it is farm machinery, the big combines and tractors first, "
             "<bookmark mark='b'/> then construction and road-building machines, <bookmark mark='c'/> and again a "
             f"lender: {M['de_fin']:.1f} billion dollars of revenue from financing, more than Deere's whole construction "
             "line. Both companies sell a machine, and then lend the money to buy it.",
             base=[rows.axis, head("Deere's net sales and revenues, fiscal 2025"), tr, src],
             steps=[VGroup(rows[0], rows[1], rows[4]), VGroup(rows[2], rows[3], rows[5], rows[6]), rows[7]])
