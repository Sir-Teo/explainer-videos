from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Intermission(VoiceoverScene):
    def construct(self):
        self.prices()
        self.output()
        self.approvals()

    def output(self):
        Ou = R["output"]
        ip = Ou["ip"]
        ch = line_chart({"output": (ip, LAB)}, x=(1972, 2025), y=(0, 4.5), xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                        yticks=[0, 1, 2, 3, 4], yfmt=lambda v: f"x{v:.0f}", ylabel="US output of medicines, 1972 = 1",
                        width=9.6, height=4.4, center=(-0.6, -0.45), label_end=False)
        end = marker(ch.ax, 2025, ip[2025], f"2025: x{ip[2025]:.1f}", LAB, side=LEFT)
        src = source("Federal Reserve, G.17: industrial production of pharmaceuticals and medicines (IPG3254S), annual "
                     "averages, via FRED", size=12)
        beat(self,
             "Meanwhile, the factories. <bookmark mark='a'/> America's output of medicines, as the Federal Reserve "
             f"measures it, grew more than fourfold from 1972 to {max(ip, key=ip.get)}, then fell by about a quarter to "
             f"2019, <bookmark mark='b'/> and in 2025 stood at {Ou['x']:.1f} times its 1972 level. It moves in long swings "
             "of its own rather than with each recession: people keep taking their medicines in a downturn, and in 2009, "
             "when machinery orders fell by almost a third, medicine output fell six per cent.",
             base=[ch.frame, src], steps=[ch.lines["output"], end])

    def prices(self):
        P = R["prices"]
        rel = {y: v for y, v in P["rel"].items() if y <= 2025}
        ch = line_chart({"drug makers' prices": (rel, BRAND)}, x=(1982, 2025), y=(0.8, 2.8), xticks=[1985, 1995, 2005, 2015, 2025],
                        yticks=[1.0, 1.5, 2.0, 2.5], yfmt=lambda v: f"x{v:.1f}",
                        ylabel="producer prices of medicines against all consumer prices, 1982 = 1", width=9.6, height=4.4,
                        center=(-0.6, -0.45), label_end=False)
        ax = ch.ax
        one = DashedLine(ax.c2p(1982, 1), ax.c2p(2025, 1), stroke_color=GREY_B, stroke_width=1.5, dash_length=0.08)
        end = marker(ax, 2025, rel[2025], f"2025: x{rel[2025]:.2f}", BRAND, side=LEFT)
        hd = tx("Intermission: what medicines cost, and how many new ones arrive", 22, WHITE, bold=True).to_edge(UP, buff=0.3)
        src = source("BLS, producer price index for pharmaceutical preparation manufacturing (PCU325412325412) and CPI-U, "
                     "annual averages, via FRED", size=12)
        beat(self,
             "An intermission, and two pictures. First, prices. <bookmark mark='a'/> Since 1982 the prices American drug "
             f"makers charge, as the Bureau of Labor Statistics measures them, have risen {P['ppi_x']:.1f} times, while "
             f"consumer prices in general rose {P['cpi_x']:.1f} times. <bookmark mark='b'/> Against everything else, "
             f"medicines cost {rel[2025]:.1f} times what they did. The index mixes protected brands with cheap generics, "
             "so the average hides both the cliff and the boom.",
             base=[ch.frame, one, hd, src], steps=[ch.lines["drug makers' prices"], end])

    def approvals(self):
        A = R["approvals"]
        items = [(str(y), v, BRAND, f"{v}") for y, v in sorted(A.items())]
        bars_ = vbars(items, base_y=-2.3, height=3.6, width=1.2, gap=0.8)
        caps = VGroup(*[draw.capsule(0.5, BRAND if k % 2 else LAB).move_to([3.2 + 0.55 * (k % 6), 2.65 - 0.4 * (k // 6), 0]) for k in range(12)])
        src = source("US Food and Drug Administration, Center for Drug Evaluation and Research: Novel Drug Approvals, 2021-2025",
                     size=12)
        beat(self,
             "Second, the new medicines. <bookmark mark='a'/> Each year the FDA's drug centre approves a few dozen drugs "
             f"with ingredients never sold in America before: {A[2021]} in 2021, {A[2022]} in 2022, <bookmark mark='b'/> "
             f"{A[2023]} in 2023, {A[2024]} in 2024 and {A[2025]} in 2025. That is the whole industry's output of new "
             "molecules: about fifty a year, each the survivor of a long funnel.",
             base=[caps, head("New drugs approved by the FDA each year"), src], steps=[VGroup(bars_[0], bars_[1]), VGroup(*bars_[2:])])
