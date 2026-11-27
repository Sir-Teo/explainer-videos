from __future__ import annotations

from videos.industry.industry29.common import *  # noqa: F403


class Trucks(VoiceoverScene):
    def construct(self):
        card(self, 4, "Half a million trucking firms", "Why can't a trucker earn what a railway earns?",
             "Chapter four. Half a million trucking firms. Anyone with a truck, a licence and insurance can enter, and "
             "that is the whole story of the industry's margins.", lit=("moat", "change"))
        self.census()
        self.truck()
        self.margins()
        self.prices()
        self.cycle()

    def census(self):
        T = R["trucks"]
        items = [(k, np.log10(v), TRUCK if i < 2 else (LTL if i < 4 else RAIL), f"{v:,.0f}") for i, (k, v) in enumerate(T["sizes"])]
        cols = vbars(items, base_y=-2.2, height=3.8, width=1.2, gap=0.45, size=15, max_value=5.6)
        lab = tx("active for-hire interstate trucking firms, by the number of trucks they report (log scale)", 16, GREY_A).to_edge(UP, buff=0.7)
        xl = tx("trucks in the fleet", 15, GREY_B).next_to(cols, DOWN, buff=0.5)
        src = source("FMCSA Company Census File via data.transportation.gov, counted by this series on 27 November 2026", size=12)
        beat(self,
             f"Here are the {T['total']:,.0f} trucking firms by size. <bookmark mark='a'/> {T['sizes'][0][1]:,.0f} report one "
             f"truck, and {T['sizes'][1][1]:,.0f} two to five. <bookmark mark='b'/> About {T['sizes'][2][1] + T['sizes'][3][1]:,.0f} run "
             f"between six and a hundred. <bookmark mark='c'/> Only {T['sizes'][4][1] + T['sizes'][5][1]:,.0f} run more "
             "than a hundred. The scale is logarithmic: each step up is ten times the last. Nothing stops the next firm "
             "starting tomorrow, and nothing stops the last one leaving.",
             base=[lab, xl, src], steps=[VGroup(*cols[:2]), VGroup(*cols[2:4]), VGroup(*cols[4:])])

    def truck(self):
        K = R["trucks"]["knx"]
        s = draw.semi(4.6, cab_color=TRUCK).move_to([0, 1.7, 0])
        c = stat_cards([(f"${K['revpt']:,.0f}", "revenue a truck a year, before fuel surcharges", GOOD),
                        (f"{K['miles']:,.0f}", "miles a truck a year", ALL), (f"{K['empty']:.1f}%", "of them empty", BAD),
                        (f"{K['op']:.1f}%", "operating ratio", TRUCK)], y=-0.9, size=34, span=12.6)
        src = source("Knight-Swift Transportation, Form 10-K for 2025: Truckload segment", size=12)
        beat(self,
             "Inside one of the big ones. <bookmark mark='a'/> Each of Knight-Swift's "
             f"{K['tractors']:,.0f} truckload tractors brought in about {K['revpt']:,.0f} dollars in 2025, before fuel "
             f"surcharges. <bookmark mark='b'/> Each drove about {K['miles']:,.0f} miles, <bookmark mark='c'/> "
             f"{K['empty']:.1f} per cent of them empty. <bookmark mark='d'/> And the segment spent {K['op']:.0f} cents of "
             "every dollar it earned. Even with the scale to keep its empty miles down, the large carrier competes with "
             "the one-truck firm on price, load by load.",
             base=[s, src], steps=[c[0], c[1], c[2], c[3]])

    def margins(self):
        M = R["trucks"]["margins"]
        cols = {"Knight-Swift": TRUCK, "Schneider": "#F08A84", "Werner": "#C9706A", "Heartland": "#F2A7B5"}
        ch = line_chart({k: (M[k], c) for k, c in cols.items()}, x=(2015, 2025), y=(-10, 25),
                        xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[-10, 0, 10, 20], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="operating profit per dollar of revenue", width=9.0, height=4.4, center=(-1.2, -0.45),
                        nudge={"Schneider": 0.28, "Knight-Swift": -0.02})
        zero = DashedLine(ch.ax.c2p(2015, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        src = source("Forms 10-K via SEC company facts", size=12)
        k, h = M["Knight-Swift"], M["Heartland"]
        beat(self,
             "Now the profits of the large truckload carriers. <bookmark mark='a'/> In 2021 and 2022, when trucks were "
             f"scarce and rates high, Knight-Swift kept about {k[2021]:.0f} cents of operating profit "
             f"on each dollar and Heartland {h[2022]:.0f}. <bookmark mark='b'/> By 2025, Knight-Swift kept "
             f"{k[2025]:.0f} cents, and Heartland lost {abs(h[2025]):.0f}. Knight-Swift calls it 'a prolonged downcycle', "
             "beginning in 2023, as shoppers turned from goods back to services.",
             base=[ch.frame, zero, src], steps=[VGroup(*[VGroup(ch.lines[n], ch.labels[n]) for n in ("Knight-Swift", "Heartland")]),
                                                VGroup(*[VGroup(ch.lines[n], ch.labels[n]) for n in ("Schneider", "Werner")])])

    def prices(self):
        T = R["trucks"]
        a = T["ppi_tl_a"]
        ch = line_chart({"truckload prices": (T["ppi_tl"], TRUCK)}, x=(2004, 2027), y=(80, 250),
                        xticks=[2004, 2008, 2012, 2016, 2020, 2024], yticks=[100, 150, 200, 250], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="producer price index, long-distance truckload (December 2003 = 100)",
                        width=9.2, height=4.4, center=(-0.6, -0.45), label_end=False)
        pk = T["ppi_peak"]
        m1 = marker(ch.ax, 2019.5, a[2019], f"2019: {a[2019]:.0f}", ALL, side=DOWN)
        m2 = marker(ch.ax, pk + 0.5, a[pk], f"{pk}: {a[pk]:.0f}", BAD, side=UP)
        m3 = marker(ch.ax, 2025.5, a[2025], f"2025: {a[2025]:.0f}", TRUCK, side=DOWN)
        lm = max(T["ppi_tl"])
        m4 = marker(ch.ax, lm, T["ppi_tl"][lm], f"Oct 2026: {T['ppi_tl'][lm]:.0f}", BAD, side=LEFT)
        src = source("BLS, PPI for general freight trucking, long-distance truckload, via FRED", size=12)
        beat(self,
             "The same story in prices. <bookmark mark='a'/> The government's index of long-distance truckload prices "
             f"stood at {a[2019]:.0f} in 2019. <bookmark mark='b'/> In {pk} it averaged {a[pk]:.0f}, "
             f"{100 * (a[pk] / a[2019] - 1):.0f} per cent higher. <bookmark mark='c'/> By 2025 it had fallen back to "
             f"{a[2025]:.0f}. <bookmark mark='d'/> In 2026, with diesel dearer after the Gulf war, it jumped again, to "
             f"{T['ppi_tl'][lm]:.0f} in October. Carriers pass most of a rise in fuel on to shippers through surcharges, as "
             "Knight-Swift says it does.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["truckload prices"], m1), m2, m3, m4])

    def cycle(self):
        C = R["trucks"]["cycle"]
        rate = {i: v for i, v in enumerate(C["rate"])}
        cap = {i: 2.4 * v for i, v in enumerate(C["capacity"])}
        ch = line_chart({"spot rate": (rate, TRUCK), "trucks (scaled)": (cap, SKY)}, x=(0, 96), y=(1.0, 4.0),
                        xticks=[0, 12, 24, 36, 48, 60, 72, 84, 96], yticks=[1, 2, 3, 4], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"${v:.0f}", ylabel="the Works' truckload market: the spot rate a mile, by month",
                        width=9.0, height=4.4, center=(-1.0, -0.45))
        cost = DashedLine(ch.ax.c2p(0, C["cost"]), ch.ax.c2p(96, C["cost"]), stroke_color=GREY_B, stroke_width=2)
        cl = tx("the marginal truck's cost", 13, GREY_B).next_to(ch.ax.c2p(96, C["cost"]), DOWN, buff=0.08, aligned_edge=RIGHT)
        boom = Rectangle(width=ch.ax.c2p(C["boom"][1], 0)[0] - ch.ax.c2p(C["boom"][0], 0)[0], height=4.4, stroke_width=0,
                         fill_color=GOOD, fill_opacity=0.08).move_to([(ch.ax.c2p(C["boom"][0], 0)[0] + ch.ax.c2p(C["boom"][1], 0)[0]) / 2, -0.45, 0])
        r = C["rate"]
        pk, tr = int(np.argmax(r)), int(np.argmin(r))
        m1 = marker(ch.ax, pk, r[pk], f"month {pk}: ${r[pk]:.2f}", BAD, side=UP)
        m2 = marker(ch.ax, tr, r[tr], f"month {tr}: ${r[tr]:.2f}", TRUCK, side=DOWN)
        tag = estimate_tag(f"the Works: demand 15% above trend for 20 months; new trucks arrive {C['entry']} months after the money; they leave slowly", size=12)
        beat(self,
             "Why does it swing so hard? The Works has a market of trucks to show it. <bookmark mark='a'/> Demand jumps for "
             "twenty months, and with too few trucks the spot rate leaps, "
             f"<bookmark mark='b'/> to {r[pk]:.2f} dollars a mile. <bookmark mark='c'/> High rates pull in new trucks, which "
             f"take about {C['entry']} months to arrive, and by then the boom is ending. <bookmark mark='d'/> Now there are "
             f"too many trucks, the rate falls to {r[tr]:.2f}, and since owners leave slowly, hoping for better, it stays "
             f"below cost for {C['below']} of the next months. Easy entry does not make a market calm; it makes it swing.",
             base=[ch.frame, cost, cl, boom, tag], steps=[ch.lines["spot rate"], m1, VGroup(ch.lines["trucks (scaled)"], ch.labels["trucks (scaled)"]),
                                                       VGroup(m2, ch.labels["spot rate"])])
