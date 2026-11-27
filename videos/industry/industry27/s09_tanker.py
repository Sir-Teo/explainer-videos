from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Tanker(VoiceoverScene):
    def construct(self):
        card(self, 7, "Tankers and tramps", "What does a ship earn when it is hired by the voyage?",
             "Chapter seven. Tankers and tramps. Container lines run timetables. Most other ships, carrying oil, ore, grain "
             "and coal, are hired by the voyage or by the year, like taxis rather than buses, and earn whatever the market "
             "pays that day.", lit=("change", "dollar"))
        self.gulf()
        self.day()
        self.q4()
        self.charter()
        self.profits()
        self.order()

    def gulf(self):
        K = R["choke"]
        items = [("tankers through Hormuz a day, 2025", K["hormuz_tank25"], TANK, f"{K['hormuz_tank25']:.0f}"),
                 (f"in {K['hormuz_last_m'][:4]}-{K['hormuz_last_m'][5:]}", K["hormuz_tank_last"], BAD, f"{K['hormuz_tank_last']:.1f}")]
        rows = hbars(items, max_value=55, x0=0.8, top=1.0, row=1.2, length=5.4, size=17, bar_h=0.6)
        tk = VGroup(*[draw.tanker(1.1) for _ in range(6)]).arrange(RIGHT, buff=0.15).move_to([0, 2.4, 0])
        src = source("IMF PortWatch, daily chokepoint transit calls (tankers), monthly averages", size=12)
        beat(self,
             "Start with what the Gulf lost. <bookmark mark='a'/> In 2025 about "
             f"{K['hormuz_tank25']:.0f} tankers a day passed through the Strait of Hormuz. <bookmark mark='b'/> In November 2026, "
             f"fewer than one. The oil had to come from further away, and the tankers that remained had further to go.",
             base=[tk, src], steps=[rows[0], rows[1]])

    def day(self):
        T = R["tanker"]
        items = [("what a VLCC needs to break even, in cash", T["be"] / 1e3, GOOD, f"${T['be']:,.0f}"),
                 ("what Frontline's VLCCs earned in the spot market, Q2 2026", T["q2"] / 1e3, RATE, f"${T['q2']:,.0f}"),
                 ("and in Q3 2026", T["q3"] / 1e3, RATE, f"${T['q3']:,.0f}")]
        rows = hbars(items, max_value=160, x0=0.8, top=1.4, row=1.0, length=5.2, size=16, bar_h=0.5)
        lab = tx("a very large crude carrier (VLCC), dollars a day", 17, GREY_A).to_edge(UP, buff=0.8)
        tk = draw.tanker(3.4).move_to([0, -2.2, 0])
        src = source("Frontline plc, third-quarter 2026 report (Form 6-K of 20 November 2026)", size=12)
        beat(self,
             "Frontline owns some of the largest oil tankers, very large crude carriers, or VLCCs. <bookmark mark='a'/> It reckons one needs about "
             f"{T['be']:,.0f} dollars a day to cover its running costs and debt. <bookmark mark='b'/> In the second quarter of "
             f"2026 its tankers earned {T['q2']:,.0f} dollars a day in the spot market, <bookmark mark='c'/> and in the third, "
             f"{T['q3']:,.0f}: six times what they needed.",
             base=[lab, tk, src], steps=[rows[0], rows[1], rows[2]])

    def q4(self):
        T = R["tanker"]
        c = stat_cards([(f"${T['q4']:,.0f}", "a day: what Frontline had booked for its VLCCs' spot days in the fourth quarter of 2026", BAD)],
                       y=0.8, size=56, span=10)
        sub = tx("68% of those days booked by 20 November", 18, GREY_A).move_to([0, -0.4, 0])
        q = tx("'freight rates have moved to all-time highs, with asset values following' (Frontline's chief executive)", 16, WHITE).move_to([0, -1.6, 0])
        src = source("Frontline plc, third-quarter 2026 report", size=12)
        beat(self,
             "And then the fourth quarter. <bookmark mark='a'/> By late November Frontline had booked its VLCCs at an "
             f"average of {T['q4']:,.0f} dollars a day for the quarter, with two-thirds of its spot days fixed. "
             "<bookmark mark='b'/> In its chief executive's words, 'freight rates have moved to all-time highs, with asset "
             "values following'. As Frontline describes it, ships sailed round the Cape, waited for weeks near the Gulf "
             "and carried oil from the Americas to Asia: every voyage took longer, every tanker was busy, and Run it's curve "
             "reached its steep end.",
             base=[src], steps=[[c, sub], q])

    def charter(self):
        T = R["tanker"]
        items = [("time charter, one year from January 2026", T["tc"] / 1e3, SHIP, f"${T['tc']:,.0f}"),
                 ("spot market, Q3 2026", T["q3"] / 1e3, RATE, f"${T['q3']:,.0f}"),
                 ("spot booked for Q4 2026", T["q4"] / 1e3, BAD, f"${T['q4']:,.0f}")]
        rows = hbars(items, max_value=580, x0=0.8, top=1.4, row=1.0, length=5.4, size=16, bar_h=0.5)
        lab = tx("Frontline's VLCCs: a fixed hire against the spot market, dollars a day", 17, GREY_A).to_edge(UP, buff=0.8)
        src = source("Frontline plc, Form 20-F for 2025 and third-quarter 2026 report", size=12)
        beat(self,
             "An owner can take the spot market's gamble, or sell it. <bookmark mark='a'/> In January 2026 Frontline let "
             f"seven of its VLCCs on one-year time charters at an average of {T['tc']:,.0f} dollars a day: three times its "
             "breakeven, locked in. <bookmark mark='b'/> Months later the spot market paid twice that, <bookmark mark='c'/> and "
             "then seven times. The charterer, not the owner, won that bet. A time charter turns a shipowner into a landlord, "
             "with a landlord's steadier and smaller returns.",
             base=[lab, src], steps=[rows[0], rows[1], rows[2]])

    def profits(self):
        F = R["tanker"]["firms"]
        series = {"Frontline (tankers)": ({y: v[1] for y, v in F["Frontline"].items()}, TANK),
                  "Star Bulk (dry bulk)": ({y: v[1] for y, v in F["Star Bulk"].items()}, BOX)}
        ch = line_chart(series, x=(2016, 2025), y=(-0.4, 0.8), xticks=[2016, 2018, 2020, 2022, 2024, 2025],
                        yticks=[-0.4, 0, 0.4, 0.8], yfmt=lambda v: f"${v:.1f}bn", ylabel="net income, $bn a year", width=9.0,
                        height=4.4, center=(-1.2, -0.45))
        zero = DashedLine(ch.ax.c2p(2016, 0), ch.ax.c2p(2025, 0), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        fr, sb = F["Frontline"], F["Star Bulk"]
        src = source("Frontline plc and Star Bulk Carriers, Forms 20-F via SEC company facts", size=12)
        beat(self,
             "Over a decade, <bookmark mark='a'/> Frontline lost money in 2017, 2018 and 2021, and earned "
             f"{fr[2023][1]:.2f} billion dollars in 2023. <bookmark mark='b'/> Star Bulk, which carries iron ore, coal and grain, "
             f"earned {sb[2021][1]:.2f} billion in 2021 after years near zero. Each kind of cargo has its own cycle, and they "
             "rarely peak together.",
             base=[ch.frame, zero, src], steps=[[ch.lines["Frontline (tankers)"], ch.labels["Frontline (tankers)"]],
                                                [ch.lines["Star Bulk (dry bulk)"], ch.labels["Star Bulk (dry bulk)"]]])

    def order(self):
        T = R["tanker"]
        c = stat_cards([(f"{T['order']:.0f}%", "tankers on order, as a share of the fleet in Frontline's classes", BAD),
                        (f"${T['sale']:.0f}m", "what Frontline got for two VLCCs built in 2017", RATE)], y=0.6, size=44, span=10)
        tk = VGroup(draw.tanker(2.0), draw.tanker(2.0), draw.tanker(2.0)).arrange(RIGHT, buff=0.3).move_to([0, -1.6, 0])
        src = source("Frontline plc, third-quarter 2026 report", size=12)
        tag = estimate_tag("this series' reading: Run it's cycle", size=12)
        beat(self,
             "And the cycle is already turning. <bookmark mark='a'/> Tankers on order in Frontline's classes came to "
             f"{T['order']:.0f} per cent of the existing fleet by November 2026: the boom's ships, to arrive in two or three "
             f"years. <bookmark mark='b'/> Frontline, meanwhile, sold two of its nine-year-old tankers for {T['sale']:.0f} million "
             "dollars and paid the money out to its shareholders. Selling into a boom is the contrarian's half of Run it.",
             base=[tk, src, tag], steps=[c[0], c[1]])
