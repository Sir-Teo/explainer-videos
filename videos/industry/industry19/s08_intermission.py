from __future__ import annotations

from videos.industry.industry19.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.jobs()
        self.capacity()
        self.prices()

    def capacity(self):
        cap = {y: v for y, v in R["cycle"]["cap"].items() if y <= 2025}
        ch = line_chart({"machinery": (cap, MACHINE)}, x=(1967, 2025), y=(50, 100), xticks=[1970, 1980, 1990, 2000, 2010, 2025],
                        yticks=[50, 60, 70, 80, 90, 100], yfmt=lambda v: f"{v:.0f}%",
                        ylabel="US machinery factories: output as a share of capacity", width=9.6, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        ax = ch.ax
        lo = min(cap, key=cap.get)
        m_lo = marker(ax, lo, cap[lo], f"{lo}: {cap[lo]:.0f}%", BAD, side=DOWN)
        m09 = marker(ax, 2009, cap[2009], f"2009: {cap[2009]:.0f}%", BAD, side=DOWN)
        m25 = marker(ax, 2025, cap[2025], f"2025: {cap[2025]:.0f}%", PRICE, side=UP)
        src = source("Federal Reserve, G.17: capacity utilization, machinery (CAPUTLG333S), annual averages, via FRED", size=12)
        beat(self,
             "And how full those factories have been since 1967. <bookmark mark='a'/> In good years machinery plants have "
             f"run at eighty-five per cent or more of what they could make. <bookmark mark='b'/> In {lo} they ran at "
             f"{cap[lo]:.0f} per cent, and in 2009 at {cap[2009]:.0f}. <bookmark mark='c'/> In 2025, "
             f"{cap[2025]:.0f} per cent. A plant two-thirds full still pays for the whole building, which is one more reason "
             "the makers lean on their steadier service businesses.",
             base=[ch.frame, src], steps=[ch.lines["machinery"], [m_lo, m09], m25])

    def jobs(self):
        H = R["history"]
        ip = {y: v for y, v in H["ip"].items() if y <= 2025}
        jb = {y: v for y, v in H["jobs"].items() if y <= 2025}
        ch = line_chart({"output": (ip, MACHINE), "jobs": (jb, BLUE)}, x=(1990, 2025), y=(0.5, 1.5),
                        xticks=[1990, 2000, 2010, 2020, 2025], yticks=[0.5, 0.75, 1.0, 1.25, 1.5], yfmt=lambda v: f"x{v:.2f}",
                        ylabel="US machinery manufacturing, 1990 = 1", width=9.4, height=4.4, center=(-0.8, -0.45),
                        fmt_end=lambda v: f"x{v:.2f}")
        hd = tx("Intermission: more machines, fewer hands", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("Federal Reserve, industrial production: machinery (IPG333S); BLS, employees in machinery manufacturing "
                     "(CES3133300001); annual averages, via FRED", size=12)
        j25 = H["jobs_abs"][2025]
        beat(self,
             "An intermission, and two lines for America's machinery factories since 1990. <bookmark mark='a'/> Their "
             f"output, after two recessions and a pandemic, ended 2025 about {100 * (ip[2025] - 1):.0f} per cent above "
             f"1990. <bookmark mark='b'/> Their jobs ended {100 * (1 - jb[2025]):.0f} per cent below it, from about "
             f"{H['jobs_abs'][1990]:,.0f} thousand people to {j25:,.0f} thousand. Each worker in a machinery plant now "
             "turns out about half as much again as in 1990. The makers of machines have been automating themselves, "
             "with their own products and their customers' robots.",
             base=[ch.frame, hd, src], steps=[[ch.lines["output"], ch.labels["output"]], [ch.lines["jobs"], ch.labels["jobs"]]])

    def prices(self):
        H = R["history"]
        rel = {y: v for y, v in H["farm_rel"].items() if y <= 2025}
        ch = line_chart({"farm machinery": (rel, "#A3D977")}, x=(1947, 2025), y=(0.6, 1.4), xticks=[1950, 1970, 1990, 2010, 2025],
                        yticks=[0.6, 0.8, 1.0, 1.2, 1.4], yfmt=lambda v: f"x{v:.1f}",
                        ylabel="producer prices of farm machinery against all consumer prices, 1947 = 1", width=9.4, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        ax = ch.ax
        one = DashedLine(ax.c2p(1947, 1), ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        end = marker(ax, 2025, rel[2025], f"2025: x{rel[2025]:.2f}", "#A3D977", side=LEFT)
        trac = draw.tractor(1.5).move_to([-4.3, 1.8, 0]) if hasattr(draw, "tractor") else VGroup()
        src = source("BLS, producer price index for farm machinery and equipment manufacturing (PCU333111333111) and CPI-U, "
                     "annual averages, via FRED", size=12)
        beat(self,
             "And one price. <bookmark mark='a'/> Since 1947 the prices farm machinery makers charge have risen "
             f"{H['farm_x']:.0f} times, while consumer prices rose {H['cpi_x']:.0f} times. <bookmark mark='b'/> Against "
             f"everything else, the index for farm machines stands at {rel[2025]:.2f} times its 1947 level. A new car's "
             "price index, in Part 17, fell to about a third of everything else's. The farm machine's did not fall at "
             "all.",
             base=[ch.frame, one, trac, src], steps=[ch.lines["farm machinery"], end])
