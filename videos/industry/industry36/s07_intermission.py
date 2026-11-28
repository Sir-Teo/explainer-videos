from __future__ import annotations

from videos.industry.industry36.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.share()
        self.prices()
        self.jobs()

    def share(self):
        T = R["traffic"]
        ch = line_chart({"business spending on software, % of GDP": (T["share"], SUB)}, x=(1960, 2027), y=(0, 3),
                        xticks=[1960, 1980, 2000, 2020], yticks=[0, 1, 2, 3], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}%",
                        ylabel="US private fixed investment in software, share of GDP", width=8.6, height=4.3, center=(-1.0, -0.45))
        k = max(T["share"])
        hd = tx("Intermission: software in the economy", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BEA, private fixed investment in software, and GDP, via FRED", size=12)
        beat(self,
             "An intermission, and three pictures. <bookmark mark='a'/> In 1960, American businesses spent almost nothing on "
             "software they bought or built to use for years. By 2000 it was one and a half per cent of the whole economy; "
             f"in 2026, {T['share'][k]:.1f} per cent, about {T['soft'][k]:.0f} billion dollars a year. The national accounts "
             "count that as investment, like machinery: software is a tool businesses build up and keep.",
             base=[ch.frame, hd, src], steps=[VGroup(*ch.lines.values(), *ch.labels.values())])

    def prices(self):
        T = R["traffic"]
        ch = line_chart({"software publishers' prices": (T["ppi"], SUB), "all consumer prices": (T["cpi"], GREY_B)}, x=(1998, 2027), y=(80, 220),
                        xticks=[1998, 2005, 2012, 2019, 2026], yticks=[80, 120, 160, 200], xfmt=lambda v: f"{int(v)}",
                        yfmt=lambda v: f"{v:.0f}", ylabel="price indexes, December 1997 = 100", width=8.6, height=4.3, center=(-1.0, -0.45))
        src = source("BLS producer price index for software publishers and CPI-U (not seasonally adjusted), via FRED", size=12)
        beat(self,
             "<bookmark mark='a'/> Consumer prices have roughly doubled since 1997. <bookmark mark='b'/> The prices software "
             f"publishers charge, as the Bureau of Labor Statistics measures them, are about where they started: "
             f"{T['ppi'][max(T['ppi'])]:.0f} against 100. The statisticians adjust for quality, and a program that does more for "
             "the same money counts as cheaper. Software is one of the few things in the economy that has steadily become "
             "better value.",
             base=[ch.frame, src], steps=[VGroup(ch.lines["all consumer prices"], ch.labels["all consumer prices"]),
                                          VGroup(ch.lines["software publishers' prices"], ch.labels["software publishers' prices"])])

    def jobs(self):
        J = R["traffic"]["jobs"]
        ch = line_chart({"computer systems design jobs": ({k: v / 1e3 for k, v in J.items()}, ENG)}, x=(1990, 2027), y=(0, 2.6),
                        xticks=[1990, 2000, 2010, 2020, 2027], yticks=[0, 1, 2], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:.0f}m",
                        ylabel="Americans employed in computer systems design and related services, millions", width=8.6, height=4.3,
                        center=(-1.0, -0.45))
        src = source("BLS, all employees in computer systems design and related services (seasonally adjusted), via FRED", size=12)
        beat(self,
             f"<bookmark mark='a'/> And the people. In 1990 about {J[min(J)] / 1e3:.1f} million Americans worked in designing "
             f"computer systems and related services; today about {J[max(J)] / 1e3:.1f} million. In this series' reading, much software is written not "
             "by software companies but by programmers working for everyone else: banks, retailers, governments, and these "
             "contractors.",
             base=[ch.frame, src], steps=[VGroup(*ch.lines.values(), *ch.labels.values())])
