from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403

GROUP_COL = {"waste": RECYCLE, "water": WATER}
SIDE = {"WM": DOWN, "RSG": UP, "WCN": DOWN, "CWST": UP, "CLH": DOWN, "AWK": UP, "WTRG": DOWN, "AWR": UP, "CWT": RIGHT, "HTO": LEFT}
L0 = np.log10(0.5)


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 12, "The landscape, November 2026", "Who owns the pipes, the trucks and the holes?",
             "Chapter twelve. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.bubbles()
        self.watch()

    def bubbles(self):
        C = R["landscape"]["companies"]
        L = {c["ticker"]: c for c in C}
        pa = viz.plot_axes([0, np.log10(32) - L0], [0, 0.28], x_length=8.8, y_length=4.8,
                           xticks=[np.log10(v) - L0 for v in (0.5, 1, 2, 5, 10, 20)], yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25],
                           xfmt=lambda v: f"${10 ** (v + L0):g}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="profit kept per dollar of revenue, five-year average", size=13).move_to([-1.6, -0.35, 0])
        xl = tx("revenue, 2025 (log scale)", 14, GREY_B).next_to(pa, DOWN, buff=0.1)
        groups = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            p = pa.ax.c2p(np.log10(c["revenue"]) - L0, c["margin5"])
            d = VGroup(Circle(0.12 + 0.09 * np.sqrt(c["revenue"]), stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.4).move_to(p),
                       tx(NAMES[c["ticker"]], 12, WHITE, bold=True))
            d[1].next_to(d[0], SIDE[c["ticker"]], buff=0.04)
            groups.setdefault(c["group"], VGroup()).add(d)
        key = VGroup(*[VGroup(Dot(radius=0.09, color=GROUP_COL[g]), tx(g, 15, WHITE)).arrange(RIGHT, buff=0.1) for g in ("water", "waste")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.2, 2.2, 0])
        note = VGroup(tx("Not drawn (no 10-K):", 13, GREY_A), tx(f"Veolia (Paris): €{R['landscape']['veolia']:.1f}bn of revenue in 2024", 12, GREY_B),
                      tx(f"Sabesp (São Paulo): water for {R['landscape']['sabesp_people']:.0f}m people", 12, GREY_B),
                      tx("GFL Environmental (Toronto)", 12, GREY_B), tx("Severn Trent, United Utilities (London)", 12, GREY_B),
                      tx("Beijing Enterprises Water (Hong Kong)", 12, GREY_B), tx("thousands of town and city utilities", 12, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([5.0, -0.9, 0])
        head = tx("America's listed water and waste companies", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        stamp = as_of("as of November 2026")
        src = source("SEC EDGAR: Forms 10-K (net income, revenue), 2021-2025; Veolia ESEF 2024; Sabesp Form 20-F 2025", size=13)
        wm, awk = L["WM"], L["AWK"]
        with self.voiceover(
            "The landscape, as of November 2026, for the companies that file American accounts. <bookmark mark='a'/> The "
            f"waste haulers are big: Waste Management, about ${wm['revenue']:.0f} billion of revenue, Republic and Waste "
            f"Connections behind it, keeping around ten to twelve cents in the dollar. Clean Harbors, the hazardous "
            "specialist, and Casella, a smaller hauler, keep less. <bookmark mark='b'/> The water "
            f"companies are small by revenue, American Water about ${awk['revenue']:.0f} billion, but keep twenty cents "
            "or more in the dollar: a regulated return on a large base of pipes, with little else on the bill. "
            "<bookmark mark='c'/> Beyond these: Veolia in Paris, with about "
            f"€{R['landscape']['veolia']:.0f} billion of revenue from water, waste and energy services; Sabesp in Brazil; "
            "the listed English water companies; and thousands of public utilities that own pipes and works of their own."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(stamp))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(b) for b in groups["waste"]], lag_ratio=0.12), run_time=1.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromCenter(b) for b in groups["water"]], lag_ratio=0.12), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(note, shift=LEFT * 0.1))
        self.clear_scene()

    def watch(self):
        G = R["regulated"]
        items = [(draw.drop(0.5), "Thames Water", "Ofwat's decision on its creditors' rescue plan"),
                 (draw.tap(0.7), "England's bills", f"about £{G['bill_rise']:.0f} a year more each year to 2030, before inflation"),
                 (draw.water_tower(0.7), "American Water and Essential Utilities", "a merger expected to close by early 2027"),
                 (draw.landfill_section(1.0, 0.45, fill=1.0), "Airspace", "permits won against airspace filled, each year"),
                 (draw.bale(0.45), "Bale prices", "China's ban showed how far they can fall"),
                 (draw.wheelie_bin(0.55), "America's water bills in 2027", "our call")]
        rows = VGroup()
        for i, (ic, h, d) in enumerate(items):
            ic.scale_to_fit_height(min(ic.height, 0.5))
            if ic.width > 0.8:
                ic.scale_to_fit_width(0.8)
            y = 2.0 - 0.82 * i
            ic.move_to([-5.2, y, 0])
            t = VGroup(tx(h, 20, WHITE, bold=True), tx(d, 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-4.5, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(ic, t))
        for r_ in rows:
            r_[0].set_opacity(0.3)
        head = tx("What to watch", 30, GOLD, bold=True).to_edge(UP, buff=0.5)
        src = source("Hansard, 16 June 2026; CMA (March 2026); American Water, Form 10-K 2025; Republic Services, Form 10-K 2025", size=13)
        with self.voiceover(
            "What to watch. <bookmark mark='a'/> Thames Water, and whether Ofwat accepts its lenders' plan. "
            "<bookmark mark='b'/> England's bills, rising every year to 2030. <bookmark mark='c'/> The merger of the "
            "two biggest water companies on our chart. <bookmark mark='d'/> Airspace: each year, do the haulers win more "
            "permitted room than they fill? <bookmark mark='e'/> The price of a bale of paper, which has more than "
            "halved in a single year. <bookmark mark='f'/> And the price of water in America, which brings us to our call."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1), run_time=1.2)
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(r_[0].animate.set_opacity(1), FadeIn(r_[1], shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()
