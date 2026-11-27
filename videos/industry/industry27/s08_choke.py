from __future__ import annotations

from videos.industry.industry27.common import *  # noqa: F403


class Choke(VoiceoverScene):
    def construct(self):
        card(self, 6, "Chokepoints", "What happens when one of the sea's narrow places closes?",
             "Chapter six. Chokepoints. The oceans are wide, but the shortest routes between them pass through a handful of "
             "canals and straits, and since 2021 several of them have been blocked.", lit=("change",))
        self.map()
        self.redsea()
        self.cape()
        self.panama()
        self.malacca()
        self.hormuz()

    def map(self):
        K = R["choke"]["annual"]
        wm = draw.world_map(width=12.0).move_to([0, 0.0, 0])
        dots = VGroup()
        for name, (lo, la) in CHOKE_LONLAT.items():
            d = Dot(wm.p(lo, la), radius=0.12, color=CHOKE_COL[name])
            lab = tx(f"{name.replace(' Strait', '').replace('Strait of ', '')}: {K[name][2025]:.0f} a day", 13, CHOKE_COL[name],
                     bold=True).next_to(d, {"Cape of Good Hope": DOWN, "Malacca Strait": DOWN, "Suez Canal": LEFT, "Strait of Hormuz": RIGHT,
                                         "Bab el-Mandeb Strait": DOWN}.get(name, UP), buff=0.08)
            dots.add(VGroup(d, lab))
        src = source("IMF PortWatch, daily transit calls through chokepoints (estimates from ship positions), 2025 averages", size=12)
        beat(self,
             "Here are six of them, with the number of ships that passed each in an average day of 2025. "
             f"<bookmark mark='a'/> The Suez Canal, {K['Suez Canal'][2025]:.0f}, and at the other end of the Red Sea the "
             f"strait of Bab el-Mandeb, {K['Bab el-Mandeb Strait'][2025]:.0f}. <bookmark mark='b'/> The long way round Africa, "
             f"past the Cape of Good Hope, {K['Cape of Good Hope'][2025]:.0f}. <bookmark mark='c'/> The Panama Canal, "
             f"{K['Panama Canal'][2025]:.0f}. <bookmark mark='d'/> The Strait of Hormuz, the mouth of the Gulf, "
             f"{K['Strait of Hormuz'][2025]:.0f}. <bookmark mark='e'/> And the Strait of Malacca, between Asia's factories and "
             f"everything west of them, {K['Malacca Strait'][2025]:.0f}.",
             base=[wm, src], steps=[VGroup(dots[0], dots[2]), dots[5], dots[1], dots[4], dots[3]])

    def redsea(self):
        M = R["choke"]["monthly"]
        series = {"Suez Canal": (M["Suez Canal"], CHOKE_COL["Suez Canal"]),
                  "Bab el-Mandeb": (M["Bab el-Mandeb Strait"], CHOKE_COL["Bab el-Mandeb Strait"])}
        ch = line_chart(series, x=(2019, 2027), y=(0, 100), xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
                        yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}",
                        ylabel="ships passing each day (monthly average)", width=9.2, height=4.4, center=(-1.0, -0.45),
                        nudge={"Bab el-Mandeb": -0.3})
        K = R["choke"]["annual"]
        src = source("IMF PortWatch, daily chokepoint transit calls; ZIM, Form 20-F for 2023", size=12)
        beat(self,
             "The Red Sea first. <bookmark mark='a'/> Traffic through Suez rose to about "
             f"{K['Suez Canal'][2023]:.0f} ships a day in 2023. <bookmark mark='b'/> Then, from the end of 2023, Yemen's "
             "Houthis attacked ships in the Red Sea, which, in ZIM's words, 'forced many ocean carriers to reroute some of "
             f"their vessels to alternative, longer and more expensive routes'. Suez fell to {K['Suez Canal'][2024]:.0f} a day in "
             f"2024 and has stayed near {K['Suez Canal'][2026]:.0f}.",
             base=[ch.frame, src], steps=[[ch.lines["Suez Canal"], ch.labels["Suez Canal"]], [ch.lines["Bab el-Mandeb"], ch.labels["Bab el-Mandeb"]]])

    def cape(self):
        M = R["choke"]["monthly"]
        K = R["choke"]["annual"]
        ch = line_chart({"Cape of Good Hope": (M["Cape of Good Hope"], CHOKE_COL["Cape of Good Hope"]),
                         "Suez Canal": (M["Suez Canal"], CHOKE_COL["Suez Canal"])},
                        x=(2019, 2027), y=(0, 110), xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], yticks=[0, 25, 50, 75, 100],
                        xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}", ylabel="ships passing each day (monthly average)",
                        width=9.2, height=4.4, center=(-1.0, -0.45))
        src = source("IMF PortWatch, daily chokepoint transit calls", size=12)
        beat(self,
             "Where did the ships go? <bookmark mark='a'/> Round Africa. Traffic past the Cape of Good Hope went from about "
             f"{K['Cape of Good Hope'][2023]:.0f} ships a day in 2023 to {K['Cape of Good Hope'][2024]:.0f} in 2024. "
             f"<bookmark mark='b'/> Since 2024 about twice as many ships have rounded the Cape as used the canal: "
             f"{K['Cape of Good Hope'][2025]:.0f} a day against {K['Suez Canal'][2025]:.0f} in 2025. The detour makes each voyage between Asia and Europe much longer, so the same cargo "
             "needs more ships: a blockade soaks up the surplus that the boom's orders had created.",
             base=[ch.frame, src], steps=[[ch.lines["Cape of Good Hope"], ch.labels["Cape of Good Hope"]],
                                          [ch.lines["Suez Canal"], ch.labels["Suez Canal"]]])

    def panama(self):
        M = R["choke"]["monthly"]["Panama Canal"]
        K = R["choke"]["annual"]["Panama Canal"]
        ch = line_chart({"Panama Canal": (M, CHOKE_COL["Panama Canal"])}, x=(2019, 2027), y=(0, 45),
                        xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="ships passing the Panama Canal each day (monthly average)", width=9.2,
                        height=4.4, center=(-0.6, -0.45), label_end=False)
        lo = min((k for k in M if 2023 <= k <= 2025), key=M.get)
        m = marker(ch.ax, lo, M[lo], f"low: {M[lo]:.0f} a day", BAD, side=DOWN)
        src = source("IMF PortWatch, daily chokepoint transit calls", size=12)
        beat(self,
             "Not every closure is war. <bookmark mark='a'/> The Panama Canal lifts ships over a hill of fresh water, and "
             f"its traffic fell from about {K[2022]:.0f} ships a day in 2022 <bookmark mark='b'/> to as few as {M[lo]:.0f} "
             f"a day in the low months that followed, before recovering to about {K[2025]:.0f} in 2025.",
             base=[ch.frame, src], steps=[ch.lines["Panama Canal"], m])

    def malacca(self):
        M = R["choke"]["monthly"]["Malacca Strait"]
        K = R["choke"]["annual"]["Malacca Strait"]
        ch = line_chart({"Malacca Strait": (M, CHOKE_COL["Malacca Strait"])}, x=(2019, 2027), y=(0, 260),
                        xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], yticks=[0, 100, 200], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="ships passing the Strait of Malacca each day (monthly average)", width=9.2,
                        height=4.4, center=(-0.6, -0.45), label_end=False)
        m1 = marker(ch.ax, 2019.5, K[2019], f"2019: {K[2019]:.0f} a day", ALL, side=DOWN)
        m2 = marker(ch.ax, 2025.5, K[2025], f"2025: {K[2025]:.0f} a day", CHOKE_COL["Malacca Strait"], side=UP)
        src = source("IMF PortWatch, daily chokepoint transit calls", size=12)
        beat(self,
             "And the busiest of them never closed. <bookmark mark='a'/> About "
             f"{K[2019]:.0f} ships a day passed the Strait of Malacca in 2019, between Singapore and Sumatra, <bookmark mark='b'/> "
             f"and {K[2025]:.0f} in 2025, more than the Suez Canal, Bab el-Mandeb and the Cape of Good Hope put together.",
             base=[ch.frame, src], steps=[[ch.lines["Malacca Strait"], m1], m2])

    def hormuz(self):
        K = R["choke"]
        M = K["monthly"]["Strait of Hormuz"]
        ch = line_chart({"Strait of Hormuz": (M, CHOKE_COL["Strait of Hormuz"])}, x=(2019, 2027), y=(0, 110),
                        xticks=[2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026], yticks=[0, 25, 50, 75, 100], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="ships passing the Strait of Hormuz each day (monthly average)", width=9.2,
                        height=4.4, center=(-1.0, -0.45), label_end=False)
        last = max(M)
        m1 = marker(ch.ax, 2026 + 1.5 / 12, K["hormuz_feb"], f"Feb 2026: {K['hormuz_feb']:.0f}", ALL, side=LEFT)
        m2 = marker(ch.ax, 2026 + 2.5 / 12, K["hormuz_mar"], f"Mar 2026: {K['hormuz_mar']:.0f}", BAD, side=RIGHT)
        q = tx("'The Strait of Hormuz remains substantially disrupted for commercial traffic' (Frontline, November 2026)", 15,
               WHITE).to_edge(UP, buff=0.6)
        src = source("IMF PortWatch, daily chokepoint transit calls; Frontline plc, third-quarter 2026 report", size=12)
        beat(self,
             f"And in 2026, the largest of all. <bookmark mark='a'/> About {K['hormuz_2025']:.0f} ships a day passed the "
             f"Strait of Hormuz in 2025, about {K['hormuz_tank25']:.0f} of them tankers. <bookmark mark='b'/> In March 2026, "
             f"with war in the region, traffic fell to about {K['hormuz_mar']:.0f} a day, and by November it was "
             f"{K['hormuz_last']:.0f}: the strait, as the tanker owner Frontline put it, 'substantially disrupted for "
             "commercial traffic'. The next chapter is what that did to the ships that carry oil.",
             base=[ch.frame, src, q], steps=[[ch.lines["Strait of Hormuz"], m1], m2])
