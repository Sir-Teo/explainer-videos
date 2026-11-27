from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403

COLS = {"China": CHINA, "Japan": BLUE, "South Korea": ROBOT, "Germany": GREY_A, "United States": PRICE}


class China(VoiceoverScene):
    def construct(self):
        card(self, 8, "China's makers", "What happens when the biggest buyer of machines learns to make them?",
             "Chapter eight. China's makers. For years China was the machine makers' biggest customer. Now it is their "
             "competitor.", lit=("change", "moat"))
        self.market()
        self.excavators()
        self.units()

    def market(self):
        c = stat_cards([(f"{R['base']['china']}%+", "of Otis's new elevators and escalators, by units, go to China", BLUE),
                        (f"{100 * R['robots']['inst']['China'][2025] / R['robots']['inst']['World'][2025]:.0f}%",
                         "of the world's new industrial robots were installed in China in 2025", ROBOT)], y=0.5, size=48, span=11)
        note = tx("the largest market for new machines of many kinds, and now a maker of them", 18, CHINA, bold=True).move_to([0, -1.8, 0])
        src = source("Otis Worldwide Corporation, Form 10-K 2025; International Federation of Robotics, 24 September 2026", size=12)
        beat(self,
             "Start with China as a customer. <bookmark mark='a'/> Over half of the new elevators and escalators Otis "
             "installs, counted in units, go into Chinese buildings, though they bring only about a fifth of its new-"
             f"equipment sales. <bookmark mark='b'/> And {100 * R['robots']['inst']['China'][2025] / R['robots']['inst']['World'][2025]:.0f} "
             "per cent of the world's new industrial robots were installed in China in 2025. <bookmark mark='c'/> China "
             "is the largest market for new elevators and for robots, and its own makers, having learned at home, are now "
             "selling abroad. Here is the clearest case.",
             base=[src], steps=[c[0], c[1], note])

    def excavators(self):
        Cn = R["china"]
        ex = Cn["excavators"]
        ser = {k: ({y: v for y, v in ex[k].items() if y >= 2010}, COLS[k]) for k in COLS if k in ex}
        ch = line_chart(ser, x=(2010, 2025), y=(0, 12), xticks=[2010, 2015, 2020, 2025], yticks=[0, 3, 6, 9, 12],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="exports of excavators, $bn a year, as each country reported them",
                        width=9.0, height=4.4, center=(-1.0, -0.45),
                        nudge={"South Korea": 0.12, "Germany": -0.05, "United States": -0.2})
        src = source("UN Comtrade: exports of HS 842952 (excavators with a 360-degree revolving superstructure) to the world, "
                     "as reported by each country", size=12)
        beat(self,
             "Here are the world's biggest exporters of excavators, the machines with a cab that turns all the way "
             "round. <bookmark mark='a'/> For years Japan led, exporting five to ten billion dollars of them a year. "
             f"<bookmark mark='b'/> China's exports were {ex['China'][2015]:.1f} billion dollars in 2015. Then they took "
             f"off: {ex['China'][2022]:.1f} billion in 2022, <bookmark mark='c'/> and {ex['China'][2025]:.1f} billion in "
             f"2025, ahead of Japan's {ex['Japan'][2025]:.1f}.",
             base=[ch.frame, src],
             steps=[[ch.lines[k] for k in ("Japan", "South Korea", "Germany", "United States")] +
                    [ch.labels[k] for k in ("Japan", "South Korea", "Germany", "United States")],
                    ch.lines["China"], ch.labels["China"]])

    def units(self):
        Cn = R["china"]
        u = Cn["excavator_units"]
        ex = Cn["excavators"]
        c15, c25 = u["China"][2015], u["China"][2025]
        j25 = u["Japan"][2025]
        per = 10000
        icons_c = VGroup(*[draw.excavator(0.5, CHINA).move_to([-6.2 + 0.56 * (i % 11), 1.5 - 0.42 * (i // 11), 0]) for i in range(round(c25 / per))])
        icons_j = VGroup(*[draw.excavator(0.5, BLUE).move_to([0.9 + 0.56 * (i % 11), 1.5 - 0.42 * (i // 11), 0]) for i in range(round(j25 / per))])
        lc = tx(f"China, 2025: {c25:,.0f} excavators exported", 17, CHINA, bold=True).next_to(icons_c, UP, buff=0.2).align_to(icons_c, LEFT)
        lj = tx(f"Japan, 2025: {j25:,.0f}", 17, BLUE, bold=True).next_to(icons_j, UP, buff=0.2).align_to(icons_j, LEFT).align_to(lc, UP)
        price = tx(f"average export value: China ${1e6 * ex['China'][2025] / c25:,.0f}k, Japan ${1e6 * ex['Japan'][2025] / j25:,.0f}k a machine",
                   16, GREY_A).to_edge(DOWN, buff=0.75)
        key = tx(f"each icon: {per:,} machines", 14, GREY_B).next_to(price, UP, buff=0.12)
        src = source("UN Comtrade: HS 842952, quantities as reported", size=12)
        beat(self,
             "Count machines instead of dollars and the gap is larger. <bookmark mark='a'/> China exported "
             f"{c15:,.0f} excavators in 2015 and {c25:,.0f} in 2025. <bookmark mark='b'/> Japan exported about "
             f"{j25:,.0f}. <bookmark mark='c'/> China's are, on average, much cheaper: about "
             f"{1e6 * ex['China'][2025] / c25:,.0f} thousand dollars each against Japan's "
             f"{1e6 * ex['Japan'][2025] / j25:,.0f}. Selling the machines is the first step. Whether China's makers can "
             "build the dealers and the installed base that the incumbents live on is the next.",
             base=[key, src], steps=[[icons_c, lc], [icons_j, lj], price])
