from __future__ import annotations

from videos.industry.industry24.common import *  # noqa: F403

COL = {"manufacturing": "#B58CFF", "power": "#F6C453", "highway": "#7EC8F5", "office": "#7BD88F", "commercial": "#F2A65A"}
NAME = {"manufacturing": "factories", "power": "power", "highway": "highways and streets", "office": "offices",
        "commercial": "shops and warehouses"}


class Intermission(VoiceoverScene):
    def construct(self):
        self.total()
        self.kinds()
        self.jobs()

    def total(self):
        S = R["spending"]
        ch = line_chart({"homes": ({y: v for y, v in S["residential"].items() if y <= 2025}, "#F2A65A"),
                         "everything else": ({y: v for y, v in S["nonresidential"].items() if y <= 2025}, BUILD)},
                        x=(2002, 2025), y=(0, 1400), xticks=[2002, 2006, 2010, 2014, 2018, 2022, 2025],
                        yticks=[0, 200, 400, 600, 800, 1000, 1200, 1400], yfmt=lambda v: f"${v:,.0f}bn",
                        ylabel="American construction spending a year (current dollars)", width=9.4, height=4.4,
                        center=(-0.9, -0.45))
        pk = max((y for y in S["residential"] if y <= 2010), key=lambda y: S["residential"][y])
        lo = min((y for y in S["residential"] if pk <= y <= 2014), key=lambda y: S["residential"][y])
        m = marker(ch.ax, lo, S["residential"][lo], f"{lo}: ${S['residential'][lo]:.0f}bn", "#F2A65A", side=DOWN)
        hd = tx("Intermission: what America is building", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Census Bureau, value of construction put in place (annual averages of SAAR), via FRED", size=12)
        beat(self,
             "An intermission, and three pictures of what America builds. <bookmark mark='a'/> First, homes against "
             f"everything else. Spending on homes peaked in {pk} and fell to {S['residential'][lo]:.0f} billion dollars "
             f"by {lo}, in the housing crash that Part 25 is about. <bookmark mark='b'/> Everything else held up far "
             f"better, and by 2025 reached {S['nonresidential'][2025]:,.0f} billion.",
             base=[hd, ch.frame, src], steps=[[ch.lines["homes"], ch.labels["homes"], m],
                                              [ch.lines["everything else"], ch.labels["everything else"]]])

    def kinds(self):
        S = R["spending"]
        series = {NAME[k]: ({y: v for y, v in S[k].items() if 2012 <= y <= 2025}, COL[k]) for k in COL}
        ch = line_chart(series, x=(2012, 2025), y=(0, 260), xticks=[2012, 2015, 2018, 2021, 2025], yticks=[0, 50, 100, 150, 200, 250],
                        yfmt=lambda v: f"${v:.0f}bn", ylabel="spending a year by kind of building", width=9.0, height=4.4,
                        center=(-1.2, -0.45), nudge={"shops and warehouses": -0.12, "offices": 0.1})
        f = S["manufacturing"]
        src = source("Census Bureau, value of construction put in place by type, via FRED", size=12)
        beat(self,
             "Second, by kind of building. <bookmark mark='a'/> The standout is factories: spending on new manufacturing "
             f"plants went from {f[2021]:.0f} billion dollars in 2021 to {f[2024]:.0f} billion in 2024, almost three "
             f"times as much, before easing to {f[2025]:.0f} in 2025. <bookmark mark='b'/> Power, highways, "
             "offices and shops each grew more steadily.",
             base=[ch.frame, src], steps=[[ch.lines["factories"], ch.labels["factories"]],
                                          [ch.lines[NAME[k]] for k in COL if k != "manufacturing"] +
                                          [ch.labels[NAME[k]] for k in COL if k != "manufacturing"]])

    def jobs(self):
        P = R["productivity"]
        j = {y: v for y, v in R["productivity"]["per"]["construction"].items()}
        ch = line_chart({"construction": (j, BUILD)}, x=(1970, 2025), y=(0.5, 1.2), xticks=[1970, 1980, 1990, 2000, 2010, 2020, 2025],
                        yticks=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2], yfmt=lambda v: f"x{v:.1f}",
                        ylabel="construction's real output per worker, 1970 = 1", width=9.0, height=4.4, center=(-0.6, -0.45),
                        label_end=False)
        one = DashedLine(ch.ax.c2p(1970, 1), ch.ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        lo = min(j, key=j.get)
        m = marker(ch.ax, lo, j[lo], f"{lo}: x{j[lo]:.2f}", BAD, side=DOWN)
        src = source("BEA real value added; BLS construction employment via FRED", size=12)
        beat(self,
             "Third, construction's own line, close up. <bookmark mark='a'/> Output per worker has wandered up and down "
             "with the building cycle, and the trend is down: "
             f"its lowest point here is {lo}, at {j[lo]:.2f} times its 1970 level, and 2025 is at "
             f"{P['per']['construction'][2025]:.2f}. Every recession and recovery has moved the line, and none has "
             "turned it around.",
             base=[ch.frame, one, src], steps=[[ch.lines["construction"], m]])
