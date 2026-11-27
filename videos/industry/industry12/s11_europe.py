from __future__ import annotations

from videos.industry.industry12.common import *  # noqa: F403


class Europe(VoiceoverScene):
    def construct(self):
        card(self, 9, "Europe's energy shock", "What happens to the world's oldest chemical industry when its gas gets dear?",
             "Chapter nine. Europe's energy shock.", lit=("change", "map"))
        self.gas()
        self.output()
        self.closures()

    def gas(self):
        E = R["europe"]
        eu, us = E["gas_eu"], E["gas_us"]
        ms = sorted(m for m in eu if m in us)
        pa = viz.plot_axes([2019, mx(ms[-1]) + 0.1], [0, 75], x_length=10.0, y_length=4.4, xticks=[2019, 2020, 2021, 2022, 2023, 2024,
                                                                                               2025, 2026],
                           yticks=[25, 50, 75], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:.0f}",
                           ylabel="dollars per million Btu, monthly", size=14).move_to([-0.3, -0.5, 0])
        le = VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in ms])
        lu = VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), us[m]) for m in ms])
        pk = max(ms, key=lambda m: eu[m])
        d_ = Dot(pa.ax.c2p(mx(pk), eu[pk]), radius=0.07, color=EUROPE)
        pl = tx(f"{mlabel(pk)}: Europe ${eu[pk]:.0f}, America ${us[pk]:.0f}", 16, WHITE, bold=True).next_to(d_, RIGHT, buff=0.15)
        last = ms[-1]
        ll = VGroup(tx(f"{mlabel(last)}:", 15, GREY_A), tx(f"Europe ${eu[last]:.1f}", 16, EUROPE, bold=True),
                    tx(f"America ${us[last]:.1f}", 16, TEXAS, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [5.6, 1.0, 0])
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(t_, 15, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((EUROPE, "Europe (Dutch TTF)"), (TEXAS, "America (Henry Hub)"))]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([-4.0, 2.4, 0])
        head = tx("Natural gas, month by month, since 2019", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("IMF Primary Commodity Prices via FRED (monthly)", size=13)
        with self.voiceover(
            "Now the other side of the shale story. <bookmark mark='a'/> In 2019, European gas cost a few dollars per "
            "million Btu, more than America's but not wildly so. <bookmark mark='b'/> Then, as economies reopened "
            "after the pandemic and Russia cut the gas it sent west, the price exploded. In "
            f"{mlabel(pk)} it reached about {eu[pk]:.0f} dollars, against about {us[pk]:.0f} in America. "
            "<bookmark mark='c'/> It came down, but it never went back. In "
            f"{mlabel(last)}, European gas still cost about {eu[last] / us[last]:.0f} times as much as American gas. "
            "For an industry whose raw material and fuel is gas, that is not a shock that passes. It is a new map."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            p1 = [m for m in ms if m <= "2021-01"]
            self.play(Create(VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in p1])),
                      Create(VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), us[m]) for m in p1])),
                      run_time=2.0, rate_func=linear)
            vo.wait_until("b")
            p2 = [m for m in ms if "2021-01" <= m <= "2023-01"]
            self.play(Create(VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in p2])),
                      Create(VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), us[m]) for m in p2])),
                      run_time=3.0, rate_func=linear)
            self.play(FadeIn(d_, scale=0.5), FadeIn(pl), Flash(d_, color=EUROPE))
            vo.wait_until("c")
            p3 = [m for m in ms if m >= "2023-01"]
            self.play(Create(VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in p3])),
                      Create(VMobject(stroke_color=TEXAS, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), us[m]) for m in p3])),
                      run_time=3.0, rate_func=linear)
            self.play(FadeIn(ll, shift=LEFT * 0.1))
        del le, lu
        self.clear_scene()

    def output(self):
        E = R["europe"]
        de, eu = E["de"], E["eu"]
        ms = sorted(m for m in de if m >= "2015-01" and m in eu)
        pa = viz.plot_axes([2015, mx(ms[-1]) + 0.1], [60, 115], x_length=9.4, y_length=4.4,
                           xticks=[2015, 2017, 2019, 2021, 2023, 2025], yticks=[70, 80, 90, 100, 110], xfmt=lambda v: f"{int(v)}",
                           yfmt=lambda v: f"{v:.0f}", ylabel="chemical output, 2021 = 100, seasonally adjusted", size=14).move_to(
            [-1.3, -0.5, 0])
        ref = DashedLine(pa.ax.c2p(2015, 100), pa.ax.c2p(mx(ms[-1]) + 0.1, 100), stroke_color=GREY_B, stroke_width=1.5,
                         dash_length=0.08)
        ld = VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), de[m]) for m in ms])
        le = VMobject(stroke_color=PLASTIC, stroke_width=2.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in ms])
        last = E["de_last_m"]
        prior = [m for m, v in sorted(de.items()) if m < "2022-01" and v <= E["de_last"]]
        d_ = Dot(pa.ax.c2p(mx(last), de[last]), radius=0.07, color=EUROPE)
        dl = VGroup(tx(f"Germany, {mlabel(last)}: {de[last]:.0f}", 16, EUROPE, bold=True),
                    tx(f"{100 * E['fall']:.0f}% below 2021", 16, EUROPE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [5.8, -1.6, 0])
        el = tx(f"EU: {100 * E['eu_fall']:.0f}% below 2021", 15, PLASTIC, bold=True).move_to([5.8, -0.6, 0])
        key = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, stroke_color=c, stroke_width=4), tx(t_, 15, c)).arrange(RIGHT, buff=0.1)
                       for c, t_ in ((EUROPE, "Germany"), (PLASTIC, "European Union"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.08
                                                                                               ).move_to([-4.6, 2.5, 0])
        low = tx(f"Germany's lowest since {mlabel(prior[-1])}" if prior else " ", 15, GREY_A).move_to([5.8, -2.4, 0])
        head = tx("How much chemistry Europe makes", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("Eurostat, industrial production index (sts_inpr_m), manufacture of chemicals (C20), monthly", size=13)
        with self.voiceover(
            "And here is what it did to how much chemistry Europe makes, by Eurostat's monthly count. "
            "<bookmark mark='a'/> Germany made about as much chemistry in 2021 as in 2015. <bookmark mark='b'/> Then the gas price rose, and output fell, and kept falling. By "
            f"{mlabel(last)}, German chemical output was about {100 * E['fall']:.0f} per cent below 2021"
            + (f", as low as in the depths of the financial crisis in {mlabel(prior[-1])[-4:]}" if prior else "")
            + f". <bookmark mark='c'/> The European Union as a whole, about {100 * E['eu_fall']:.0f} per cent below. "
            "How much of the fall is weak demand, and how much is production moving to cheaper places, is still "
            "argued over. The plants that are closing tell part of the story."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pa), FadeIn(src), Create(ref), FadeIn(key))
            vo.wait_until("a")
            p1 = [m for m in ms if m <= "2022-01"]
            self.play(Create(VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), de[m]) for m in p1])),
                      Create(VMobject(stroke_color=PLASTIC, stroke_width=2.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in p1])),
                      run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            p2 = [m for m in ms if m >= "2022-01"]
            self.play(Create(VMobject(stroke_color=EUROPE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(mx(m), de[m]) for m in p2])),
                      Create(VMobject(stroke_color=PLASTIC, stroke_width=2.5).set_points_as_corners([pa.ax.c2p(mx(m), eu[m]) for m in p2])),
                      run_time=3.0, rate_func=linear)
            self.play(FadeIn(d_, scale=0.5), FadeIn(dl), FadeIn(low))
            vo.wait_until("c")
            self.play(FadeIn(el))
        del ld, le
        self.clear_scene()

    def closures(self):
        R_ = R["run"]
        wm = draw.world_map(9.0, lon=(-11, 22), lat=(45, 59)).move_to([-2.2, -0.3, 0])
        pins = [("Ince, England", -2.82, 53.28, "CF: closed, 2022", BAD), ("Billingham, England", -1.29, 54.60,
                                                                            "CF: ammonia stopped, 2023", BAD),
                ("Antwerp, Belgium", 4.30, 51.28, "INEOS: a new cracker built for American ethane", GOOD),
                ("Böhlen, Germany", 12.38, 51.20, f"Dow: cracker to shut by end-{R_['bohlen']:.0f}", BAD)]
        marks = VGroup()
        for name, lo, la, what, col in pins:
            p = wm.p(lo, la)
            dot = Dot(p, radius=0.09, color=col)
            ring = Circle(0.18, stroke_color=col, stroke_width=2).move_to(p)
            marks.add(VGroup(dot, ring, tx(name, 13, WHITE, bold=True).next_to(dot, UP, buff=0.08)))
        cards = VGroup(*[VGroup(Dot(radius=0.07, color=col), VGroup(tx(name, 15, WHITE, bold=True), tx(what, 14, col)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.03)).arrange(RIGHT, buff=0.15, aligned_edge=UP) for name, _, _, what, col in pins]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 0.0, 0])
        head = tx("What Europe's plants are doing", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("CF Industries, Form 10-K 2023; Dow Inc., Form 10-K 2025; EIA, Today in Energy (30 March 2026)", size=13)
        with self.voiceover(
            "On the map, it looks like this. <bookmark mark='a'/> In England, CF Industries closed its Ince fertilizer "
            "plant in 2022 and stopped making ammonia at Billingham in 2023, citing the cost of gas. <bookmark mark='b'/> "
            f"In Germany, Dow will shut its cracker at Böhlen by the end of {R_['bohlen']:.0f}. <bookmark mark='c'/> And "
            "in Antwerp, INEOS's new cracker, Europe's largest, slated to start in the second half of 2026, is "
            "built to run on ethane shipped from America. "
            "<bookmark mark='d'/> Europe's chemical industry is not disappearing; it still makes a great deal. But at "
            "the root of the tree, where the feedstock is most of the cost, the plants that close are in the place "
            "where the molecules are dear, and the plants that are built use molecules from where they are cheap."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(head), FadeIn(src))
            for m_, idx in zip("abc", ((0, 1), (3,), (2,))):
                vo.wait_until(m_)
                self.play(*[FadeIn(marks[i], scale=0.6) for i in idx], *[FadeIn(cards[i], shift=LEFT * 0.1) for i in idx],
                          *[Flash(marks[i][0], color=pins[i][4]) for i in idx])
            vo.wait_until("d")
            self.play(*[Indicate(m[0], scale_factor=1.4) for m in marks])
        self.clear_scene()
