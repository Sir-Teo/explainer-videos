from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403

NAMES = {"NEE": "NextEra", "DUK": "Duke", "SO": "Southern", "AEP": "AEP", "D": "Dominion", "EXC": "Exelon", "XEL": "Xcel",
         "ED": "Con Edison", "PCG": "PG&E", "SRE": "Sempra", "ETR": "Entergy", "VST": "Vistra", "CEG": "Constellation",
         "NRG": "NRG", "AES": "AES", "GEV": "GE Vernova"}
GROUP_COL = {"regulated utilities": STORE, "generators": GAS, "equipment": WIND}
SIDE = {"NEE": UP, "DUK": RIGHT, "SO": UP, "AEP": UP, "D": UP, "EXC": RIGHT, "XEL": LEFT, "ED": UP, "PCG": DOWN, "SRE": UP,
        "ETR": LEFT, "VST": UP, "CEG": LEFT, "NRG": DOWN, "AES": LEFT, "GEV": DOWN}


class Landscape(VoiceoverScene):
    def construct(self):
        card(self, 12, "The landscape, November 2026", "Who owns the plants and the wires, and who earns what?",
             "Chapter twelve. The landscape, November 2026.", lit=("unit", "moat", "change"))
        self.bubbles()
        self.steadiness()
        self.watch()

    def bubbles(self):
        C = R["landscape"]["companies"]
        L = {c["ticker"]: c for c in C}
        pa = viz.plot_axes([np.log10(10), np.log10(45)], [-0.01, 0.27], x_length=9.0, y_length=5.0,
                           xticks=[np.log10(v) for v in (10, 15, 20, 30, 40)], yticks=[0, 0.05, 0.1, 0.15, 0.2, 0.25],
                           xfmt=lambda v: f"${10 ** v:,.0f}bn", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="profit kept per dollar of sales, five-year average", size=13).move_to([-1.4, -0.35, 0])
        xl = tx("revenue in the latest year (log scale)", 14, "#9AA3B2").next_to(pa, DOWN, buff=0.1)
        groups = {}
        for c in C:
            col = GROUP_COL[c["group"]]
            p = pa.ax.c2p(np.log10(c["revenue"]), c["margin5"])
            d = VGroup(Circle(0.07 * np.sqrt(c["revenue"]) ** 0.8, stroke_color=col, stroke_width=2, fill_color=col,
                              fill_opacity=0.4).move_to(p), tx(NAMES[c["ticker"]], 12, WHITE, bold=True))
            d[1].next_to(d[0], SIDE[c["ticker"]], buff=0.04)
            groups.setdefault(c["group"], VGroup()).add(d)
        order = ["regulated utilities", "generators", "equipment"]
        key = VGroup(*[VGroup(Dot(radius=0.09, color=GROUP_COL[g]), tx(g, 15, WHITE)).arrange(RIGHT, buff=0.1) for g in order]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([5.3, 2.0, 0])
        note = VGroup(tx("Not drawn (no 10-K):", 13, GREY_A), tx("State Grid, China's generators,", 12, GREY_B),
                      tx("EDF, Enel, Iberdrola, RWE, Orsted,", 12, GREY_B), tx("NTPC, Adani, TEPCO, Siemens", 12, GREY_B),
                      tx("Energy, Vestas", 12, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([5.3, -1.3, 0])
        head = tx("America's listed power companies", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        stamp = as_of("as of November 2026")
        src = source("SEC EDGAR: Forms 10-K (net income attributable to the company, total revenues); fiscal years to 2025", size=13)
        with self.voiceover(
            "Here is the landscape, as of November 2026: America's listed power companies, by revenue and by how much of "
            "each dollar they kept over five years. <bookmark mark='a'/> The regulated utilities cluster together: Duke, "
            f"Southern, AEP, Dominion and the rest, keeping ten to seventeen cents in the dollar, year after year. "
            f"NextEra, which also develops wind and solar farms, about {100 * L['NEE']['margin5']:.0f}. "
            "<bookmark mark='b'/> The generators that sell into markets, Vistra, Constellation, NRG and AES, earn far "
            "less on average, and far less steadily: their years include storms and price spikes on both sides. "
            "<bookmark mark='c'/> And GE Vernova, which makes the turbines and grid equipment, the newest of them, spun "
            "out of General Electric. The steadiest money is in the monopoly, the wires and the regulated plants; the "
            "riskiest is in selling power at whatever the market will pay."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(head), FadeIn(src), FadeIn(key), FadeIn(note), FadeIn(stamp))
            for g, m in zip(order, "abc"):
                vo.wait_until(m)
                self.play(LaggedStart(*[GrowFromCenter(b) for b in groups.get(g, VGroup())], lag_ratio=0.12), run_time=1.5)
        self.clear_scene()

    def steadiness(self):
        Y = R["landscape"]["years"]
        pa = viz.plot_axes([2015, 2025], [-0.6, 0.6], x_length=9.4, y_length=4.8, xticks=list(range(2015, 2026, 2)),
                           yticks=[-0.5, -0.25, 0, 0.25, 0.5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:+.0f}%",
                           ylabel="net income per dollar of revenue, each year", size=13).move_to([-1.0, -0.45, 0])
        zero = DashedLine(pa.ax.c2p(2015, 0), pa.ax.c2p(2025, 0), color=GREY_B, stroke_width=1.5, dash_length=0.08)
        spec = [("DUK", "Duke", STORE), ("SO", "Southern", "#5BC0BE"), ("VST", "Vistra", GAS), ("NRG", "NRG", "#F28C38")]
        lines, labs = VGroup(), VGroup()
        for tk, nm, col in spec:
            pts = sorted(Y[tk].items())
            lines.add(poly(pa, pts, col, 4))
            y_last, v_last = pts[-1]
            labs.add(tx(nm, 15, col, bold=True).next_to(pa.ax.c2p(y_last, v_last), RIGHT, buff=0.12))
        labs[0].shift(UP * 0.16)
        labs[1].shift(DOWN * 0.02)
        labs[2].next_to(pa.ax.c2p(2024, Y["VST"][2024]), UP, buff=0.12)
        labs[3].next_to(pa.ax.c2p(2019, Y["NRG"][2019]), RIGHT, buff=0.15)
        n15, n19 = Y["NRG"][2015], Y["NRG"][2019]
        v21, v24 = Y["VST"][2021], Y["VST"][2024]
        lo_d = min(min(Y["DUK"].values()), min(Y["SO"].values()))
        hi_d = max(max(Y["DUK"].values()), max(Y["SO"].values()))
        band = Rectangle(width=pa.ax.c2p(2025, 0)[0] - pa.ax.c2p(2015, 0)[0], height=pa.ax.c2p(0, hi_d)[1] - pa.ax.c2p(0, lo_d)[1],
                         stroke_width=0, fill_color=STORE, fill_opacity=0.12).move_to(
            [(pa.ax.c2p(2015, 0)[0] + pa.ax.c2p(2025, 0)[0]) / 2, (pa.ax.c2p(0, hi_d)[1] + pa.ax.c2p(0, lo_d)[1]) / 2, 0])
        head = tx("The same years, two kinds of company", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("SEC EDGAR: Forms 10-K (net income, total revenues), fiscal years 2015-2025; Vistra from 2017", size=13)
        with self.voiceover(
            "Averages hide the difference, so here are the same years one at a time. <bookmark mark='a'/> Duke and "
            f"Southern, two of the regulated monopolies: a profit every year, between {100 * lo_d:.0f} and "
            f"{100 * hi_d:.0f} cents in each dollar of revenue, storms, pandemic and all. <bookmark mark='b'/> Now two generators. "
            f"NRG: a loss of about {abs(100 * n15):.0f} cents in the dollar in 2015, a profit of about {100 * n19:.0f} cents "
            f"in 2019. <bookmark mark='c'/> Vistra: a loss in 2021, the year of the Texas freeze, and about "
            f"{100 * v24:.0f} cents of profit in 2024. <bookmark mark='d'/> The regulated company sells the same service "
            "at a price someone else sets, so its profit stays inside that band. The generator sells power at whatever the market "
            "pays, so its profit moves with the weather, the price of gas and the price of power."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(zero), FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(lines[0]), Create(lines[1]), FadeIn(labs[0]), FadeIn(labs[1]), run_time=2.5)
            self.play(FadeIn(band))
            vo.wait_until("b")
            self.play(Create(lines[3]), FadeIn(labs[3]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(labs[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Indicate(band, color=STORE, scale_factor=1.0), lines[2].animate.set_stroke(opacity=0.5),
                      lines[3].animate.set_stroke(opacity=0.5), run_time=1.5)
        self.clear_scene()

    def watch(self):
        D = R["demand"]
        U = R["utility"]
        items = [(draw.server_rack(0.8), "Data centres", f"sales up {D['ytd']:.1f}% in January-August 2026; who pays to connect them"),
                 (draw.pylon(0.8), "Rate cases", f"Duke asks {U['pending'][0][2]:.2f}% in North Carolina, for 2027"),
                 (draw.battery(0.6), "Batteries", f"California at {R['sun']['battery_cap']:.0f} GW; Texas adding them fast"),
                 (draw.gas_plant(0.8), "Gas", "so often the fuel on the margin, and the price of power with it"),
                 (draw.wind_turbine(0.9), "Wind and sun", "a sixth of the world's electricity, and the midday price"),
                 (draw.cooling_tower(0.8), "America's electricity use in 2027", "our call")]
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
        src = source("EIA; Duke Energy, Form 10-K 2025; Potomac Economics; Ember via Our World in Data", size=13)
        with self.voiceover(
            "What to watch. <bookmark mark='a'/> The new load: data centres, and who pays for the plants and wires "
            "they need. <bookmark mark='b'/> The rate cases, like Duke's request for almost eleven per cent. "
            "<bookmark mark='c'/> Batteries, spreading from California to Texas, eating the evening peak that used to "
            "belong to gas. <bookmark mark='d'/> Gas itself, which still sets the price much of the time. "
            "<bookmark mark='e'/> Wind and sun, pushing the midday price towards zero. <bookmark mark='f'/> And how much "
            "electricity America uses, which brings us to our call."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.1), run_time=1.2)
            for m, r_ in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(r_[0].animate.set_opacity(1), FadeIn(r_[1], shift=RIGHT * 0.2), run_time=0.8)
        self.clear_scene()
