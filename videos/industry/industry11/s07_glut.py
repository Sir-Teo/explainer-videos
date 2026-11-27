from __future__ import annotations

from videos.industry.industry11.common import *  # noqa: F403


class Glut(VoiceoverScene):
    def construct(self):
        card(self, 6, "Half the world's steel", "What happens when one country makes half of everything?",
             "Chapter six. Half the world's steel.", lit=("change",))
        self.rise()
        self.countries()
        self.exports()
        self.walls()

    def rise(self):
        G = R["glut"]
        W, CH = G["world"], G["china"]
        wy = sorted(W)
        cy = sorted(CH)
        pa = viz.plot_axes([1948, 2027], [0, 2100], x_length=10.6, y_length=4.5, xticks=[1950, 1970, 1990, 2010, 2025],
                           yticks=[500, 1000, 1500, 2000], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:,.0f}",
                           ylabel="million tonnes of crude steel a year", size=13).move_to([0, -0.4, 0])
        wl = VMobject(stroke_color=STEELC, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, W[y]) for y in wy])
        ca = Polygon(*[pa.ax.c2p(y, CH[y]) for y in cy], pa.ax.c2p(cy[-1], 0), pa.ax.c2p(cy[0], 0), stroke_width=0,
                     fill_color=CHINA, fill_opacity=0.55)
        cl = VMobject(stroke_color=CHINA, stroke_width=3).set_points_as_corners([pa.ax.c2p(y, CH[y]) for y in cy])
        lw = tx("the world", 16, STEELC, bold=True).next_to(pa.ax.c2p(1975, W[1975]), UP, buff=0.12)
        lc = tx("China", 16, CHINA, bold=True).move_to(pa.ax.c2p(2016, 420))
        s95 = tx(f"1995: {100 * G['share_1995']:.0f}%", 15, CHINA).next_to(pa.ax.c2p(1995, CH[1995]), UP, buff=0.35)
        s25 = VGroup(tx(f"2025: {100 * G['share_2025']:.0f}%", 20, CHINA, bold=True), tx("of the world's steel", 14, GREY_A)
                     ).arrange(DOWN, buff=0.03).move_to(pa.ax.c2p(2003, 1750))
        src = source("World Steel Association: World Steel in Figures 2022, 2024 and 2026; Steel Statistical Yearbooks 2002, "
                     "2011 and 2020", size=13)
        with self.voiceover(
            "Now the world. <bookmark mark='a'/> World steel production grew fast after the war, stalled for twenty years "
            f"from the mid-1970s at around seven or eight hundred million tonnes, <bookmark mark='b'/> and then took off "
            "again. Almost all of the take-off was one country. <bookmark mark='c'/> In 1995 China made about "
            f"{100 * G['share_1995']:.0f} per cent of the world's steel. <bookmark mark='d'/> By 2025 it made "
            f"{100 * G['share_2025']:.0f} per cent: {CH[2025]:,.0f} million tonnes, more than the rest of the world put "
            "together. The cities, railways, factories and apartment towers of the fastest build-out in history were "
            "made of it."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(src))
            vo.wait_until("a")
            k = wy.index(1995)
            part1 = VMobject(stroke_color=STEELC, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(y, W[y]) for y in wy[:k + 1]])
            self.play(Create(part1), FadeIn(lw), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(wl), run_time=2.0)
            self.remove(part1)
            vo.wait_until("c")
            self.play(FadeIn(ca), Create(cl), FadeIn(lc), FadeIn(s95), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(s25, shift=DOWN * 0.1))
        self.clear_scene()

    def countries(self):
        G = R["glut"]
        c = G["countries"]
        names = {"china": "China", "india": "India", "us": "United States", "japan": "Japan", "russia": "Russia",
                 "korea": "South Korea", "turkiye": "Türkiye", "germany": "Germany", "brazil": "Brazil", "iran": "Iran"}
        rows = VGroup()
        for i, (k, v) in enumerate(sorted(c.items(), key=lambda kv: -kv[1])):
            y = 2.5 - 0.52 * i
            b = Rectangle(width=9.0 * v / c["china"], height=0.36, stroke_width=0,
                          fill_color=CHINA if k == "china" else (USA if k == "us" else REST), fill_opacity=0.9).move_to(
                [-3.2, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(tx(names[k], 16, WHITE).next_to([-3.3, y, 0], LEFT, buff=0.1), b,
                            tx(f"{v:,.0f}", 14, WHITE, bold=True).next_to(b, RIGHT, buff=0.08)))
        head = tx("Crude steel, 2025, million tonnes", 22, WHITE, bold=True).to_edge(UP, buff=0.25)
        pc = G["asu_pc"]
        side = VGroup(tx("Steel used per person, 2025", 16, WHITE, bold=True),
                      tx(f"China {pc['china']:.0f} kg", 15, CHINA), tx(f"United States {pc['us']:.0f} kg", 15, USA),
                      tx(f"India {pc['india']:.0f} kg", 15, GREY_A), tx(f"world {pc['world']:.0f} kg", 15, STEELC)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.05).move_to([4.7, -1.6, 0])
        src = source("World Steel Association, World Steel in Figures 2026", size=13)
        with self.voiceover(
            "Here are the ten biggest producers in 2025. <bookmark mark='a'/> China, then a long way behind, India, "
            f"with {c['india']:.0f} million tonnes and growing fastest, then the United States and Japan, each around "
            "eighty. <bookmark mark='b'/> Per person, China now uses more than twice as much steel as the United States, "
            f"{pc['china']:.0f} kilograms a year against {pc['us']:.0f}, and India about a fifth as much as China. India "
            "is where the next great build-out is happening."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[0]), GrowFromEdge(r_[1], LEFT), FadeIn(r_[2])) for r_ in rows],
                                  lag_ratio=0.15), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side, shift=LEFT * 0.2))
        self.clear_scene()

    def exports(self):
        G = R["glut"]
        asu = G["asu"]
        ys = sorted(asu)
        bars = VGroup()
        for i, y in enumerate(ys):
            h = 3.8 * asu[y] / 1000
            b = Rectangle(width=0.8, height=h, stroke_width=0, fill_color=CHINA, fill_opacity=0.75).move_to(
                [-5.6 + 1.05 * i, -2.6, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"{asu[y]:,.0f}", 14, WHITE, bold=True).next_to(b, UP, buff=0.05),
                            tx(str(y), 14, GREY_A).next_to(b, DOWN, buff=0.08)))
        bl = VGroup(tx("Steel used in China", 18, CHINA, bold=True), tx("million tonnes of finished steel", 13, GREY_A)
                    ).arrange(DOWN, buff=0.03).next_to(bars, UP, buff=0.35)
        e21, e25 = G["exports21"], G["exports25"]
        ex = VGroup()
        for i, (y, v) in enumerate(((2021, e21), (2025, e25))):
            h = 3.8 * v / 150
            b = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=PRICE, fill_opacity=0.85).move_to(
                [1.6 + 1.5 * i, -2.6, 0], aligned_edge=DOWN)
            ex.add(VGroup(b, tx(f"{v:.0f}", 18, WHITE, bold=True).next_to(b, UP, buff=0.05),
                          tx(str(y), 14, GREY_A).next_to(b, DOWN, buff=0.08)))
        el = VGroup(tx("China's steel exports", 18, PRICE, bold=True), tx("million tonnes", 13, GREY_A)).arrange(
            DOWN, buff=0.03).next_to(ex, UP, buff=1.2)
        usb = Rectangle(width=1.0, height=3.8 * G["us_crude"] / 150, stroke_width=0, fill_color=USA, fill_opacity=0.8).move_to(
            [5.2, -2.6, 0], aligned_edge=DOWN)
        us = VGroup(usb, tx(f"{G['us_crude']:.0f}", 18, WHITE, bold=True).next_to(usb, UP, buff=0.05),
                    VGroup(tx("all the steel", 13, USA), tx("made in the US,", 13, USA), tx("2025", 13, USA)).arrange(
                        DOWN, buff=0.0).next_to(usb, DOWN, buff=0.08))
        ship = draw.ship(1.6).move_to([3.0, 2.6, 0])
        src = source("World Steel Association: World Steel in Figures 2022 and 2026", size=13)
        with self.voiceover(
            "Then the build-out ended. From 2021, China's property market turned down, and with it the demand for steel. "
            f"<bookmark mark='a'/> The steel China used fell from {asu[2021]:,.0f} million tonnes in 2021 to "
            f"{asu[2025]:,.0f} million in 2025, a drop larger than everything the United States uses in a year. "
            "<bookmark mark='b'/> China's production fell much less. Mills kept running, for all the reasons of the "
            "last two chapters. So the steel went abroad. <bookmark mark='c'/> China's exports went from about "
            f"{e21:.0f} million tonnes in 2021 to {e25:.0f} million in 2025, roughly doubling. <bookmark mark='d'/> That "
            "is more steel than the whole United States makes in a year, offered on the world market, mostly at prices "
            "other mills could not match."
        ) as vo:
            self.play(FadeIn(bl), FadeIn(src), FadeIn(ship), GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars[1:]], lag_ratio=0.2),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(bars[-1], color=CHINA), ship.animate.shift(RIGHT * 2.5), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(el), *[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in ex], run_time=1.6)
            vo.wait_until("d")
            self.play(GrowFromEdge(usb, DOWN), FadeIn(us[1:]), run_time=1.2)
        self.clear_scene()

    def walls(self):
        G = R["glut"]
        wm = draw.world_map(11.0).move_to([0, -0.3, 0])
        cn, us_, eu = wm.p(110, 33), wm.p(-95, 38), wm.p(10, 50)
        arrows = VGroup(*[CurvedArrow(cn, d, angle=a, color=PRICE, stroke_width=3, tip_length=0.18)
                          for d, a in ((us_ + RIGHT * 0.6, -0.6), (eu + RIGHT * 0.3, 0.4), (wm.p(100, 5), -0.4),
                                       (wm.p(45, 25), 0.3), (wm.p(-60, -15), -0.5))])
        walls = VGroup(*[Rectangle(width=0.12, height=0.9, stroke_width=0, fill_color=BAD, fill_opacity=0.95).move_to(p)
                         for p in (us_ + RIGHT * 1.0, eu + RIGHT * 0.65)])
        t1 = VGroup(tx("United States: tariff on imported steel", 16, WHITE, bold=True),
                    tx(f"{G['tariff25']:.0f}% for every country from March 2025,", 15, GREY_A),
                    tx(f"{G['tariff50']:.0f}% from June 2025", 15, BAD, bold=True)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.03).move_to([-4.6, -2.6, 0])
        t2 = VGroup(tx("European Union", 16, WHITE, bold=True), tx(f"imports {G['eu_imports']:.0f} million tonnes (2025);", 15,
                                                                   GREY_A),
                    tx("quotas, and a carbon price at the border from 2026", 15, GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.03).move_to(
            [3.6, 2.6, 0])
        cnl = tx("China", 16, CHINA, bold=True).next_to(cn, DOWN, buff=0.1)
        src = source("USGS, Mineral Commodity Summaries 2026 (Iron and Steel); World Steel Association; Regulation (EU) "
                     "2023/956", size=13)
        with self.voiceover(
            "So the glut became a trade war. <bookmark mark='a'/> China's surplus flowed to every market with a port. "
            "<bookmark mark='b'/> And the walls went up. The United States had put a twenty-five per cent tariff on "
            "most imported steel in 2018. In March 2025 it removed every exception, and in June it doubled the tariff, "
            f"to {G['tariff50']:.0f} per cent. <bookmark mark='c'/> The European Union, which bought about "
            f"{G['eu_imports']:.0f} million tonnes of steel from outside in 2025, kept quotas and began charging a "
            "carbon price at its border in 2026. Steel is one of the few industries every government wants to have at "
            "home: for defence, for jobs, and for the towns built around the mills. That is one more reason capacity "
            "does not close."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src), FadeIn(cnl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in arrows], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(GrowFromCenter(walls[0]), FadeIn(t1))
            vo.wait_until("c")
            self.play(GrowFromCenter(walls[1]), FadeIn(t2))
        self.clear_scene()
