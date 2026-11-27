from __future__ import annotations

from videos.industry.industry21.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.prices()
        self.output()
        self.clearances()

    def prices(self):
        Hs = R["history"]
        rel = {y: v for y, v in Hs["rel"].items() if y <= 2025}
        ch = line_chart({"instrument prices": (rel, DEVICE)}, x=(1986, 2025), y=(0.4, 1.1),
                        xticks=[1986, 1995, 2005, 2015, 2025], yticks=[0.4, 0.6, 0.8, 1.0], yfmt=lambda v: f"x{v:.1f}",
                        ylabel="producer prices of surgical and medical instruments against all consumer prices, 1986 = 1",
                        width=9.6, height=4.4, center=(-0.6, -0.45), label_end=False)
        ax = ch.ax
        one = DashedLine(ax.c2p(1986, 1), ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        end = marker(ax, 2025, rel[2025], f"2025: x{rel[2025]:.2f}", DEVICE, side=UP)
        hd = tx("Intermission: what instruments cost, and how many are made", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, producer price index for surgical and medical instrument manufacturing (PCU339112339112) and "
                     "CPI-U, annual averages, via FRED", size=12)
        beat(self,
             "An intermission, and three pictures. First, prices. <bookmark mark='a'/> Since 1986 the prices American "
             "makers charge for surgical and medical instruments, as the Bureau of Labor Statistics measures them, rose "
             f"{Hs['ppi_x']:.2f} times, while consumer prices in general rose {Hs['cpi_x']:.2f} times. "
             f"<bookmark mark='b'/> Against everything else, instruments cost about {rel[2025]:.2f} of what they did: half. "
             "Part 20 found the opposite for medicines: against consumer prices, their producer "
             "prices were two and a half times what they were in 1982. The index adjusts for quality where it can, and a protected drug and a cleared catheter "
             "face very different competition.",
             base=[hd, ch.frame, one, src], steps=[ch.lines["instrument prices"], end])

    def output(self):
        Hs = R["history"]
        ip = {y: v for y, v in Hs["ip"].items() if y <= 2025}
        ch = line_chart({"output": (ip, GOOD)}, x=(1972, 2025), y=(0, 6), xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                        yticks=[0, 1, 2, 3, 4, 5, 6], yfmt=lambda v: f"x{v:.0f}", ylabel="US output of medical equipment and supplies, 1972 = 1",
                        width=9.6, height=4.4, center=(-0.6, -0.45), label_end=False)
        end = marker(ch.ax, 2025, ip[2025], f"2025: x{ip[2025]:.1f}", GOOD, side=LEFT)
        src = source("Federal Reserve, G.17: industrial production of medical equipment and supplies (IPN3391S), annual "
                     "averages, via FRED", size=12)
        beat(self,
             "Second, the factories. <bookmark mark='a'/> America's output of medical equipment and supplies, as the "
             f"Federal Reserve measures it, has grown {ip[2025]:.1f} times since 1972, <bookmark mark='b'/> and barely "
             f"noticed the recession of 2009, when it changed by {100 * Hs['ip_2009']:.0f} per cent. Operations are "
             "postponed in a downturn, but people still fall ill.",
             base=[ch.frame, src], steps=[ch.lines["output"], end])

    def clearances(self):
        k = R["history"]["k510"]
        k = {y: v for y, v in k.items() if 1977 <= y <= 2025}
        ch = line_chart({"510(k)": (k, DEVICE)}, x=(1977, 2025), y=(0, 6000), xticks=[1977, 1985, 1995, 2005, 2015, 2025],
                        yticks=[0, 2000, 4000, 6000], yfmt=lambda v: f"{v:,.0f}", ylabel="510(k) clearances a year",
                        width=9.6, height=4.4, center=(-0.6, -0.45), label_end=False)
        pk = max(k, key=k.get)
        top = marker(ch.ax, pk, k[pk], f"{pk}: {k[pk]:,}", DEVICE, side=UP)
        end = marker(ch.ax, 2025, k[2025], f"2025: {k[2025]:,}", DEVICE, side=UP)
        src = source("US Food and Drug Administration via openFDA: 510(k) decisions found substantially equivalent, by year",
                     size=12)
        beat(self,
             "Third, the new devices. <bookmark mark='a'/> The 510(k) road opened with the law of 1976. Clearances rose "
             f"to a peak of {k[pk]:,} in {pk}, <bookmark mark='b'/> and have run at about three thousand a year for two "
             f"decades: {k[2025]:,} in 2025. A steady stream of small improvements, each compared with the last.",
             base=[ch.frame, src], steps=[[ch.lines["510(k)"], top], end])
