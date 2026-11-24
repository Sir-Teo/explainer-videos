from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

MINER = {"BHP": "#E07A3F", "RIO": "#E8554E", "VALE": "#3FA7A0"}
NAME = {"BHP": "BHP", "RIO": "Rio Tinto", "VALE": "Vale"}


class Boom(VoiceoverScene):
    def construct(self):
        card(self, 9, "The supercycle", "What happened when China built a century's worth of cities in a decade?",
             "Chapter nine. The supercycle.", lit=("change", "dollar"))
        self.prices()
        self.profits()

    def prices(self):
        B = R["boom"]
        ys = sorted(B["cu"])
        cu = [B["cu"][y] / B["cu"][2002] for y in ys]
        fe = [B["fe"][y] / B["fe"][2002] for y in ys]
        pa = viz.plot_axes([1992, 2026], [0, 14], x_length=10.4, y_length=4.8,
                           xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025], yticks=[1, 4, 7, 10, 13],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"x{v:g}", size=15).move_to([-0.3, -0.4, 0])
        one = DashedLine(pa.ax.c2p(1992, 1), pa.ax.c2p(2026, 1), stroke_color=GREY_B, stroke_width=1.2)
        t = ValueTracker(1992)

        def line(vals, col):
            def f():
                q = [pa.ax.c2p(y, v) for y, v in zip(ys, vals) if y <= t.get_value()]
                return VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(q) if len(q) > 1 else VMobject()
            return always_redraw(f)
        l_fe, l_cu = line(fe, IRON), line(cu, COPPER)
        yr = draw.number(lambda: t.get_value(), 0, commas=False, size=34, color=GREY_A)
        yr.add_updater(lambda m: m.to_corner(UR, buff=0.5))
        yr.update()
        k11 = ys.index(2011)
        tag_fe = VGroup(tx("iron ore", 18, IRON, bold=True), tx(f"x{B['fe_rise']:.1f} from 2002 to 2011", 16, WHITE)
                        ).arrange(DOWN, buff=0.03, aligned_edge=RIGHT).next_to(pa.ax.c2p(2011, fe[k11]), LEFT, buff=0.2)
        tag_cu = VGroup(tx("copper", 18, COPPER, bold=True), tx(f"x{B['cu_rise']:.1f}", 16, WHITE)).arrange(
            DOWN, buff=0.03).next_to(pa.ax.c2p(2011, cu[k11]), UP, buff=0.35)
        china = VGroup(*[draw.crane(0.9, color="#F2C14E") for _ in range(3)]).arrange(RIGHT, buff=0.15).scale(0.8)
        china.move_to(pa.ax.c2p(1998.5, 9.0))
        clab = tx("China builds", 16, "#F2C14E").next_to(china, UP, buff=0.08)
        head = tx("Annual average prices, 2002 = 1", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("IMF primary commodity prices via FRED (PCOPPUSDM, PIORECRUSDM), nominal", size=13)
        with self.voiceover(
            "Now the decade that made the modern mining industry. <bookmark mark='a'/> In 2002 copper and iron ore were "
            "cheap, and had been for twenty years. Miners had cut costs, closed mines and stopped exploring. "
            "<bookmark mark='b'/> Then China's economy, already growing fast, began to build at a scale the world had "
            "never seen: apartment blocks, railways, power grids, factories, whole new cities, all of them made of "
            "steel and wired with copper. <bookmark mark='c'/> Supply could not keep up, because, as we have seen, a "
            "new mine takes years to find, approve and build. So the price did the rationing. From 2002 to 2011, "
            f"copper rose {B['cu_rise']:.1f} times, and iron ore {B['fe_rise']:.1f} times. Bankers called it a "
            "supercycle. <bookmark mark='d'/> And then the new mines approved in the boom arrived, just as China's "
            "building slowed. By 2016 copper had lost almost half its 2011 price, and iron ore two-thirds."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src), Create(one))
            self.add(l_fe, l_cu, yr)
            vo.wait_until("a")
            self.play(t.animate.set_value(2002), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(china, shift=UP * 0.2), FadeIn(clab))
            vo.wait_until("c")
            self.play(t.animate.set_value(2011), run_time=4.0, rate_func=linear)
            self.play(FadeIn(tag_fe), FadeIn(tag_cu))
            vo.wait_until("d")
            self.play(t.animate.set_value(2025), run_time=4.0, rate_func=linear)
        for m in (l_fe, l_cu, yr):
            m.clear_updaters()
        self.clear_scene()

    def profits(self):
        Mn = R["boom"]["miners"]
        years = list(range(2015, 2026))
        pa = viz.plot_axes([2014.4, 2025.6], [-14, 32], x_length=10.2, y_length=4.6, xticks=years[::2],
                           yticks=[-10, 0, 10, 20, 30], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn",
                           size=15).move_to([-0.4, -0.5, 0])
        zero = Line(pa.ax.c2p(2014.4, 0), pa.ax.c2p(2025.6, 0), stroke_color=GREY_B, stroke_width=1.5)
        bars = VGroup()
        for j, tic in enumerate(["BHP", "RIO", "VALE"]):
            g = VGroup()
            for y in years:
                if y not in Mn[tic]:
                    continue
                v = Mn[tic][y]["profit"]
                x = y + (j - 1) * 0.26
                p0, p1 = pa.ax.c2p(x, 0), pa.ax.c2p(x, v)
                g.add(Rectangle(width=0.24, height=max(abs(p1[1] - p0[1]), 0.01), stroke_width=0,
                                fill_color=MINER[tic], fill_opacity=0.9).move_to([p0[0], (p0[1] + p1[1]) / 2, 0]))
            bars.add(g)
        fe = R["boom"]["fe"]
        pline = VMobject(stroke_color=WHITE, stroke_width=2.5).set_points_smoothly(
            [pa.ax.c2p(y, fe[y] / 6) for y in years])
        pl = tx("iron ore price (right scale)", 14, WHITE).next_to(pa.ax.c2p(2015, fe[2015] / 6), UP, buff=0.12
                                                                   ).shift(RIGHT * 0.6)
        rticks = VGroup(*[tx(f"${v}", 13, GREY_B).next_to(pa.ax.c2p(2025.6, v / 6), RIGHT, buff=0.1)
                          for v in (60, 120, 180)])
        key = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=MINER[t_], fill_opacity=1),
                              tx(NAME[t_], 16, WHITE)).arrange(RIGHT, buff=0.1) for t_ in MINER]).arrange(
            RIGHT, buff=0.5).next_to(pa, UP, buff=0.12)
        lows = VGroup(tx("the bust: write-downs and losses", 16, STATE, bold=True),
                      tx(f"Vale {Mn['VALE'][2015]['profit']:+.1f}bn (2015), BHP {Mn['BHP'][2016]['profit']:+.1f}bn "
                         f"(year to June 2016), Rio {Mn['RIO'][2015]['profit']:+.1f}bn (2015)", 14, WHITE)).arrange(
            DOWN, buff=0.04).move_to(pa.ax.c2p(2018.5, -10.5))
        highs = VGroup(tx("the boom of 2021-22", 16, GREEN_C, bold=True),
                       tx(f"Vale ${Mn['VALE'][2021]['profit']:.1f}bn, Rio ${Mn['RIO'][2021]['profit']:.1f}bn (2021); "
                          f"BHP ${Mn['BHP'][2022]['profit']:.1f}bn (year to June 2022)", 14, WHITE)).arrange(
            DOWN, buff=0.04).move_to(pa.ax.c2p(2017.6, 27))
        head = tx("The three iron ore giants: profit attributable to shareholders, US$ billion", 20, WHITE, bold=True
                  ).to_edge(UP, buff=0.35)
        src = source("SEC EDGAR, Forms 20-F (IFRS); BHP's years end in June; IMF iron ore price via FRED", size=13)
        with self.voiceover(
            "Watch what that did to the miners. Here are the three iron ore giants, year by year, from 2015. "
            "<bookmark mark='a'/> The bust came first. Iron ore fell to about fifty-six dollars a tonne in 2015, and "
            "all three reported losses, as they wrote down the value of mines, projects and other assets they had "
            f"bought or built at the top. Vale lost {abs(Mn['VALE'][2015]['profit']):.1f} billion dollars. "
            "<bookmark mark='b'/> Then the price recovered, and profits came back. <bookmark mark='c'/> By 2021, with "
            f"iron ore near {fe[2021]:.0f} dollars, Vale earned {Mn['VALE'][2021]['profit']:.1f} billion and Rio Tinto "
            f"{Mn['RIO'][2021]['profit']:.1f}, and in its year to June 2022 BHP reported "
            f"{Mn['BHP'][2022]['profit']:.1f} billion, swollen by the profit from its oil business, which it merged "
            "into Woodside that year. "
            "<bookmark mark='d'/> See how much harder profits swing than the price. The miners' costs barely change "
            "when the price moves, so almost every extra dollar on the price is an extra dollar of margin, and every "
            "lost dollar comes out of it. A miner is a bet on the price, made with a fixed cost base: the cost curve "
            "of chapter five, multiplied by billions of tonnes."
        ) as vo:
            self.play(FadeIn(pa), Create(zero), FadeIn(head), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(*[GrowFromEdge(g[0], UP) for g in bars], FadeIn(lows))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] > pa.ax.c2p(0, 0)[1] else UP)
                                    for g in bars for b_ in g[1:6]], lag_ratio=0.03), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN if b_.get_center()[1] > pa.ax.c2p(0, 0)[1] else UP)
                                    for g in bars for b_ in g[6:]], lag_ratio=0.03), FadeIn(highs), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(pline), FadeIn(pl), FadeIn(rticks), run_time=2.0)
        self.clear_scene()
