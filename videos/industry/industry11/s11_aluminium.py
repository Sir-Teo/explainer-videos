from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Aluminium(VoiceoverScene):
    def construct(self):
        card(self, 9, "Electricity in solid form", "Why do aluminium smelters go wherever power is cheapest?",
             "Chapter nine. Electricity in solid form.", lit=("make", "change"))
        self.smelter()
        self.china()
        self.shock()

    def smelter(self):
        A = R["aluminium"]
        e = A["energy"]
        pl = draw.potline(6.4, 7).scale(1.3).move_to([0.9, -0.5, 0])
        dam = draw.dam(1.0).move_to([-5.6, -0.3, 0])
        wire = Line(dam.get_right(), pl.bus.get_left(), stroke_color=PRICE, stroke_width=4)
        steps = VGroup(tx("bauxite ore", 16, ORE, bold=True), tx("→  alumina (aluminium oxide)", 16, WHITE),
                       tx("→  pots: a huge electric current splits off the oxygen", 16, PRICE),
                       tx("→  liquid aluminium, tapped from each pot", 16, ALU)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.08).to_corner(UL, buff=0.5)
        kwh = VGroup(tx(f"{e[2025]:,.0f} kWh", 36, PRICE, bold=True), tx("of electricity for each tonne, 2025 world average", 15,
                                                                         GREY_A),
                     tx(f"({e[1980]:,.0f} in 1980)", 14, GREY_B)).arrange(DOWN, buff=0.05).move_to([4.6, 2.2, 0])
        sm = A["smelter"]
        big = VGroup(tx("A smelter making 500,000 tonnes a year", 17, WHITE, bold=True),
                     tx(f"uses about {sm['twh']:.1f} TWh a year: a steady {sm['mw']:,.0f} MW,", 16, GREY_A),
                     tx("the output of a large power station, day and night", 16, GREY_A)).arrange(DOWN, buff=0.05).to_edge(
            DOWN, buff=0.85)
        ps = tx(f"Alcoa, 2025: power is about {A['power_share']:.0f}% of its smelters' costs", 15, ALU).next_to(big, DOWN, buff=0.12)
        pulses = VGroup(*[Dot(radius=0.07, color=HOT) for _ in range(6)])
        t = ValueTracker(0)

        def flow(m):
            a, b = wire.get_start(), wire.get_end()
            for i, d in enumerate(m):
                f = (t.get_value() + i / len(m)) % 1.0
                d.move_to(a + (b - a) * f)
        pulses.add_updater(flow)
        src = source("International Aluminium Institute, statistics (smelting energy intensity, AC); Alcoa, Form 10-K 2025",
                     size=13)
        tag = estimate_tag("500,000 t x IAI's 2025 average: our arithmetic", corner=DR, size=13)
        with self.voiceover(
            "Aluminium is the third heavy material, and a strange one. <bookmark mark='a'/> It starts as bauxite, a red "
            "ore, which is refined into a white powder, alumina, aluminium bound to oxygen. <bookmark mark='b'/> To pull "
            "the oxygen off, alumina is dissolved in molten salt in long rows of pots, and an enormous electric current "
            "is passed through it. Liquid aluminium collects at the bottom. <bookmark mark='c'/> It takes about "
            f"{e[2025]:,.0f} kilowatt-hours of electricity to make one tonne, on the industry's world average for 2025, "
            "down from almost seventeen thousand in 1980. <bookmark mark='d'/> So a smelter making half a million tonnes "
            f"a year draws about {sm['mw']:,.0f} megawatts, day and night: the output of a large power station, all for "
            f"one factory. Alcoa says electricity is about {A['power_share']:.0f} per cent of what its smelters spend. "
            "Aluminium is, in effect, electricity in solid form."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(steps[:2], shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(steps[2:]), FadeIn(dam), Create(wire))
            self.add(pulses)
            self.play(t.animate.set_value(2), pl.tops.animate.set_fill(ALU, 1), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(kwh, shift=DOWN * 0.1), t.animate.set_value(3), run_time=1.5, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(big), t.animate.set_value(4.5), run_time=2.0, rate_func=linear)
            self.play(FadeIn(ps))
        pulses.clear_updaters()
        self.clear_scene()

    def china(self):
        A = R["aluminium"]
        cs = A["china_share"]
        ys = sorted(cs)
        pa = viz.plot_axes([1998, 2026.5], [0, 0.7], x_length=6.2, y_length=3.8, xticks=[2000, 2010, 2020, 2025],
                           yticks=[0.2, 0.4, 0.6], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{100 * v:.0f}%",
                           ylabel="China's share of the world's new aluminium", size=13).move_to([-3.2, 0.0, 0])
        ln = VMobject(stroke_color=CHINA, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, cs[y]) for y in ys])
        lab = tx(f"{100 * cs[2025]:.0f}%", 22, CHINA, bold=True).next_to(pa.ax.c2p(2025, cs[2025]), UP, buff=0.1)
        lab0 = tx(f"{100 * cs[2000]:.0f}%", 16, CHINA).next_to(pa.ax.c2p(2000, cs[2000]), UP, buff=0.1)
        up = A["us_primary"]
        y0 = max(up, key=lambda y: up[y])
        bars = VGroup()
        for i, (y, v) in enumerate(((y0, up[y0]), (2000, up[2000]), (2010, up[2010]), (2025, A["us_primary25"] * 1000))):
            h = 3.2 * v / up[y0]
            b = Rectangle(width=0.75, height=h, stroke_width=0, fill_color=USA, fill_opacity=0.85).move_to(
                [2.4 + 1.1 * i, -2.0, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{v / 1e6:.1f}", 15, WHITE, bold=True).next_to(b, UP, buff=0.05),
                            tx(str(y), 14, GREY_A).next_to(b, DOWN, buff=0.08)))
        bl = VGroup(tx("US primary aluminium", 17, USA, bold=True), tx("million tonnes a year", 13, GREY_A)).arrange(
            DOWN, buff=0.03).move_to([4.05, 2.2, 0])
        where = VGroup(tx("Where power is cheap:", 15, WHITE, bold=True),
                       tx("hydro in Canada, Norway, Iceland;", 14, GREY_A), tx("gas in the Gulf; and China", 14, GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.03).move_to([-3.2, -2.9, 0])
        src = source("International Aluminium Institute, statistics (primary production); USGS Data Series 140 and Mineral "
                     "Commodity Summaries 2026", size=13)
        with self.voiceover(
            "Because power is most of the cost you can control, smelters go wherever electricity is cheap and plentiful: "
            "to the rivers of Canada, Norway and Iceland, to the gas fields of the Gulf, <bookmark mark='a'/> and above "
            f"all, this century, to China. In 2000 China made about {100 * cs[2000]:.0f} per cent of the world's new "
            f"aluminium. <bookmark mark='b'/> By 2025, {100 * cs[2025]:.0f} per cent. <bookmark mark='c'/> America went "
            f"the other way. Its smelters made about {up[y0] / 1e6:.1f} million tonnes in {y0}. In 2025, "
            f"{A['us_primary25'] / 1000:.2f} million, from {A['smelters']:.0f} smelters, two of them shut. As American "
            "power got dearer relative to other places, the pots went cold."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src), FadeIn(where))
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(lab0), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(lab, scale=1.2))
            vo.wait_until("c")
            self.play(FadeIn(bl), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars],
                                              lag_ratio=0.3), run_time=2.5)
        self.clear_scene()

    def shock(self):
        A = R["aluminium"]
        g = A["gcc_monthly"]
        ms = sorted(g)
        pr = A["price"]
        pa = viz.plot_axes([2024.95, 2026.85], [0, 650], x_length=10.0, y_length=4.2, xticks=[2025.04, 2025.5, 2026.04, 2026.5],
                           yticks=[200, 400, 600], xfmt=lambda v: {2025.04: "Jan 2025", 2025.5: "Jul 2025", 2026.04: "Jan 2026",
                                                                    2026.5: "Jul 2026"}.get(round(v, 2), ""),
                           yfmt=lambda v: f"{v:.0f} kt", size=13).move_to([-0.4, -0.4, 0])
        bars = VGroup()
        for m in ms:
            x = mx(m)
            b0, b1 = pa.ax.c2p(x, 0), pa.ax.c2p(x, g[m])
            bars.add(Rectangle(width=0.32, height=b1[1] - b0[1], stroke_width=0, fill_color=ALU,
                               fill_opacity=0.55 if m < "2026-04" else 0.95).move_to(b0, aligned_edge=DOWN))
        pmin, pmax = 2000, 4000
        sc = lambda v: 650 * (v - pmin) / (pmax - pmin)  # noqa: E731
        pms = [m for m in sorted(pr) if m >= "2025-01"]
        pl = VMobject(stroke_color=PRICE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), sc(pr[m])) for m in pms])
        rax = VGroup(*[tx(f"${v:,.0f}", 12, PRICE).next_to(pa.ax.c2p(2026.85, sc(v)), RIGHT, buff=0.1) for v in (2500, 3000, 3500)])
        bl = VGroup(tx("Gulf smelters' output, thousand tonnes a month", 15, ALU, bold=True)).move_to(pa.ax.c2p(2025.5, 620))
        plab = tx("aluminium price, $ a tonne (London), right-hand scale", 15, PRICE, bold=True).move_to(
            pa.ax.c2p(2026.2, 700))
        peak = max(pms, key=lambda m: pr[m])
        pk = VGroup(Dot(pa.ax.c2p(mx(peak), sc(pr[peak])), radius=0.06, color=PRICE),
                    tx(f"{mlabel(peak)}: ${pr[peak]:,.0f}", 14, PRICE, bold=True).next_to(pa.ax.c2p(mx(peak), sc(pr[peak])), UP,
                                                                                         buff=0.1))
        us = VGroup(tx("And in America, behind a 50% tariff:", 16, WHITE, bold=True),
                    tx(f"US market price 2025: {A['us_price25']:.0f} cents a pound,", 15, GREY_A),
                    tx(f"against about {A['lme25_c']:.0f} cents in London", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                               buff=0.04).to_corner(DR, buff=0.45)
        src = source("International Aluminium Institute, statistics (GCC production, monthly); IMF via FRED (PALUMUSDM); "
                     "USGS, Mineral Commodity Summaries 2026", size=12)
        with self.voiceover(
            "Electricity in solid form also means that a shock to energy is a shock to aluminium. <bookmark mark='a'/> "
            "The Gulf states, with their cheap gas, made about one tonne in every twelve of the world's aluminium. Here "
            "is their output, month by month. <bookmark mark='b'/> In April 2026, with the region at war and the Strait "
            f"of Hormuz shut, as in Part eight, it fell from about {A['gcc_base']:.0f} thousand tonnes a month to "
            f"{A['gcc_low']:.0f}. <bookmark mark='c'/> And the world price, which had been creeping up, jumped, to "
            f"{pr[peak]:,.0f} dollars a tonne in {mlabel(peak)}. <bookmark mark='d'/> Americans paid more still: behind "
            f"a fifty per cent tariff, aluminium in the United States averaged {A['us_price25']:.0f} cents a pound in "
            f"2025, against about {A['lme25_c']:.0f} cents in London."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(bl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:15]], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[15:]], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(pl), FadeIn(plab), FadeIn(rax), run_time=2.0)
            self.play(FadeIn(pk))
            vo.wait_until("d")
            self.play(FadeIn(us, shift=UP * 0.1))
        self.clear_scene()
