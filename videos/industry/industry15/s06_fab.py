from __future__ import annotations

from videos.industry.industry15.common import *  # noqa: F403

CAPEX, REV = "#F2A65A", "#7EC8F5"


class Fab(VoiceoverScene):
    def construct(self):
        card(self, 5, "The fab", "What does it take to run fabs at TSMC's scale?",
             "Chapter five. The fab.", lit=("make", "dollar"))
        self.capex()
        self.utilization()
        self.people()

    def capex(self):
        F = R["fab"]
        cap, rev = F["capex_twd"], F["rev_twd"]
        ys = [y for y in sorted(cap) if y >= 2015 and y in rev]
        pa = viz.plot_axes([2014.4, 2025.6], [0, 4000], x_length=8.4, y_length=4.4, xticks=[2015, 2017, 2019, 2021, 2023, 2025],
                           yticks=[1000, 2000, 3000, 4000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"NT${v / 1000:.0f}tn",
                           ylabel="TSMC, each year", size=13).move_to([-1.4, -0.4, 0])
        rb, cb = VGroup(), VGroup()
        for y in ys:
            x0, y0 = pa.ax.c2p(y, 0)[:2]
            rb.add(Rectangle(width=0.34, height=pa.ax.c2p(y, rev[y])[1] - y0, stroke_width=0, fill_color=REV, fill_opacity=0.8).move_to([x0 - 0.17, y0, 0], aligned_edge=DOWN))
            cb.add(Rectangle(width=0.34, height=pa.ax.c2p(y, cap[y])[1] - y0, stroke_width=0, fill_color=CAPEX, fill_opacity=0.9).move_to([x0 + 0.17, y0, 0], aligned_edge=DOWN))
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=REV, fill_opacity=0.8), tx("revenue", 14, GREY_A)).arrange(RIGHT, buff=0.08),
                     VGroup(Square(0.2, stroke_width=0, fill_color=CAPEX, fill_opacity=0.9), tx("spent on fabs and tools", 14, GREY_A)).arrange(RIGHT, buff=0.08)).arrange(
            RIGHT, buff=0.5).move_to([0.2, 2.75, 0])
        share = F["capex_share"]
        side = VGroup(tx(f"2025: ${F['capex25']:.1f}bn spent", 18, CAPEX, bold=True),
                      tx(f"2026 plan: ${F['capex26'][0]:.0f}-{F['capex26'][1]:.0f}bn", 16, WHITE),
                      tx(f"a third to a half of revenue, every year", 15, GREY_A),
                      tx(f"in America alone: ${F['us']:.0f}bn planned", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.6, 0.6, 0])
        src = source("SEC EDGAR: TSMC, Forms 20-F (IFRS, NT$), 2015-2025; Form 6-K of 4 March 2025 (US investment)", size=13)
        with self.voiceover(
            f"A fab is a building full of machines, and TSMC writes its machines off over {get('tsm.tool_life'):.0f} "
            "years, so a chipmaker never stops buying them. <bookmark mark='a'/> Here is TSMC's revenue, year by year. <bookmark mark='b'/> And "
            f"here is what it spent on fabs and tools: between {100 * min(share[y] for y in ys):.0f} and "
            f"{100 * max(share[y] for y in ys):.0f} per cent of its revenue, every year. <bookmark mark='c'/> In 2025 that "
            f"came to about ${F['capex25']:.0f} billion; for 2026 it planned {F['capex26'][0]:.0f} to "
            f"{F['capex26'][1]:.0f} billion. And it has said it expects to invest ${F['us']:.0f} billion in America alone: "
            "six fabs, two packaging plants and a research centre."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(key), FadeIn(ghost(rb, cb)))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in rb], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cb], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side, shift=LEFT * 0.1))
        self.clear_scene()

    def utilization(self):
        F = R["fab"]
        G = R["run"]
        wc = G["wafer_cost"]
        vs = sorted(wc)
        pa = viz.plot_axes([0, 52_000], [0, 90_000], x_length=6.0, y_length=4.2, xticks=[10_000, 20_000, 30_000, 40_000, 50_000],
                           yticks=[20_000, 40_000, 60_000, 80_000], xfmt=lambda v: f"{v / 1000:.0f}k", yfmt=lambda v: f"${v / 1000:.0f}k",
                           ylabel="the Works' fab: cost of a wafer", size=12).move_to([-3.2, -0.4, 0])
        from explainer.industry.works import fab as W
        f = W.Fab()
        pts = [(v, f.cost_per_wafer(v)) for v in range(5_000, 50_001, 1_000)]
        ln = poly(pa, pts, CAPEX, 4)
        xl = tx("wafers started a month", 13, GREY_B).next_to(pa, DOWN, buff=0.1)
        gauge = VGroup(Rectangle(width=4.0, height=0.45, stroke_color=GREY_B, stroke_width=2),
                       Rectangle(width=4.0 * F["util"], height=0.45, stroke_width=0, fill_color=GOOD, fill_opacity=0.85)).move_to([3.6, 1.6, 0])
        gauge[1].align_to(gauge[0], LEFT)
        gl = VGroup(tx("TSMC, 2025: wafers shipped / capacity", 15, GREY_A),
                    tx(f"{F['ship'][2025]:.1f}m of {F['capacity']:.0f}m+ = {100 * F['util']:.0f}%", 20, GOOD, bold=True)).arrange(DOWN, buff=0.06).next_to(gauge, UP, buff=0.12)
        pw = VGroup(tx("revenue per 12-inch wafer, on average", 15, GREY_A),
                    tx(f"2023: NT${F['per_wafer_twd'][2023] / 1000:.0f}k", 17, WHITE),
                    tx(f"2025: NT${F['per_wafer_twd'][2025] / 1000:.0f}k, about ${round(F['per_wafer_usd'], -2):,.0f}", 19, PRICE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([3.6, -0.6, 0])
        why = tx("'mainly attributable to higher capacity utilization and cost improvement'", 13, GREY_B).move_to([3.4, -2.2, 0])
        tag = estimate_tag("left: the Works' fab, an illustration", corner=DR, size=12)
        src = source("TSMC, Form 20-F 2025 (capacity, shipments, revenue, gross margin)", size=13)
        with self.voiceover(
            "Because the fab costs the same whether it is busy or idle, how full it is decides everything. "
            "<bookmark mark='a'/> In the Works' fab, a wafer costs about "
            f"${wc[5_000] / 1000:.0f} thousand to make when the fab runs at a tenth of its capacity, and about "
            f"${wc[50_000] / 1000:.0f} thousand when it is full. <bookmark mark='b'/> TSMC had capacity for more than "
            f"{F['capacity']:.0f} million wafers in 2025 and shipped about {F['ship'][2025]:.0f} million: about "
            f"{100 * F['util']:.0f} per cent full. <bookmark mark='c'/> And it earned more for each one: about NT$"
            f"{F['per_wafer_twd'][2023] / 1000:.0f} thousand a wafer in 2023, NT${F['per_wafer_twd'][2025] / 1000:.0f} "
            f"thousand in 2025, about ${round(F['per_wafer_usd'], -2):,.0f}, as more of its wafers were on its newest processes. "
            "Its margin rose, it said, mainly because of higher utilization and lower costs."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(xl), FadeIn(tag), FadeIn(src), FadeIn(gauge[0]))
            vo.wait_until("a")
            self.play(Create(ln), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromEdge(gauge[1], LEFT), FadeIn(gl), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(pw, shift=UP * 0.1), FadeIn(why))
        self.clear_scene()

    def people(self):
        F = R["fab"]
        hist = F["staff_hist"]
        per = 1000
        n = {y: int(round(v / per)) for y, v in hist.items()}
        grid = VGroup(*[draw.person(0.32, GREY_B) for _ in range(n[2025])]).arrange_in_grid(rows=7, buff=(0.07, 0.1)).move_to([-2.6, -0.2, 0])
        for i, p_ in enumerate(grid):
            p_.set_opacity(0)
        yl = {y: tx(f"{y}: {hist[y]:,.0f} people", 20 if y == 2025 else 17, WHITE if y == 2025 else GREY_A, bold=y == 2025) for y in hist}
        ylab = VGroup(*yl.values()).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.4, 1.4, 0])
        key = tx("each figure: 1,000 employees", 13, GREY_B).next_to(grid, DOWN, buff=0.2)
        rev = get("tsm.rev.2025.usd")
        per_head = rev * 1e9 / hist[2025]
        side = VGroup(tx("revenue per employee, 2025", 15, GREY_A), tx(f"about ${per_head / 1e6:.1f} million", 22, PRICE, bold=True),
                      tx(f"(${rev:.0f}bn / {hist[2025]:,.0f})", 13, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.4, -1.4, 0])
        src = source("TSMC, Form 20-F 2025 (employees at year end; net revenue)", size=13)
        with self.voiceover(
            "And the people. <bookmark mark='a'/> At the end of 2023 TSMC employed about "
            f"{hist[2023]:,.0f} people. <bookmark mark='b'/> By the end of 2025, about {hist[2025]:,.0f}. "
            f"<bookmark mark='c'/> That is about ${per_head / 1e6:.1f} million of revenue for each of them. A fab is a "
            "building full of machines, and the money goes on the machines: as we saw, a third to a half of TSMC's revenue "
            "every year. Very few industries take in so much for each person they employ."
        ) as vo:
            self.play(FadeIn(src), FadeIn(key), FadeIn(ghost(*[p_.copy().set_opacity(1) for p_ in grid[:n[2025]]], opacity=0.3)),
                      FadeIn(ghost(ylab, side, opacity=0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[p_.animate.set_opacity(1) for p_ in grid[:n[2023]]], lag_ratio=0.01), FadeIn(yl[2023]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(yl[2024]), LaggedStart(*[p_.animate.set_opacity(1).set_color(DIE) for p_ in grid[n[2023]:n[2024]]], lag_ratio=0.05), run_time=1.0)
            self.play(FadeIn(yl[2025]), LaggedStart(*[p_.animate.set_opacity(1).set_color(PRICE) for p_ in grid[n[2024]:n[2025]]], lag_ratio=0.05), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(side, shift=UP * 0.1))
        self.clear_scene()
