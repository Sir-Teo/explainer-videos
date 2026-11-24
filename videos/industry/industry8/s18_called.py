from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403


class Called(VoiceoverScene):
    def construct(self):
        card(self, 16, "Called it?", "How well did the most famous oil forecast do?",
             "Chapter sixteen. Called it?", lit=("change",))
        self.hubbert()
        self.world()
        self.ours()

    def hubbert(self):
        U = R["us"]
        ys, kbd = U["years"], U["kbd"]
        pa = viz.plot_axes([1900, 2050], [0, 15], x_length=10.0, y_length=4.4,
                           xticks=[1900, 1925, 1950, 1975, 2000, 2025, 2050], yticks=[5, 10, 15],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=14)
        pa.move_to([0.2, -0.6, 0])
        pre = [(y, v / 1000) for y, v in zip(ys, kbd) if 1900 <= y <= 1956]
        post = [(y, v / 1000) for y, v in zip(ys, kbd) if y >= 1956]
        lpre = VMobject(stroke_color=WHITE, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in pre])
        lpost = VMobject(stroke_color=WHITE, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in post])
        curves = VGroup()
        for U_, col in ((150, PRICE), (200, CRUDE)):
            h = U["hubbert"][U_]
            curves.add(DashedVMobject(VMobject(stroke_color=col, stroke_width=3).set_points_smoothly(
                [pa.ax.c2p(y, v / 1000) for y, v in zip(h["years"], h["kbd"])]), num_dashes=70))
        l150 = tx("Hubbert: 150bn barrels in all, peak about 1965", 16, PRICE).move_to(pa.ax.c2p(1925, 12.6), aligned_edge=LEFT)
        l200 = tx("Hubbert: 200bn barrels in all, peak about 1970", 16, CRUDE).next_to(l150, DOWN, buff=0.1).align_to(l150, LEFT)
        lab56 = DashedLine(pa.ax.c2p(1956, 0), pa.ax.c2p(1956, 14), stroke_color=GREY_C, stroke_width=1.2)
        t56 = tx("1956: what Hubbert could see", 14, GREY_B).next_to(pa.ax.c2p(1956, 14), UP, buff=0.05)
        pk = tx(f"1970: {U['peak1970'] / 1000:.2f}m", 16, WHITE, bold=True).next_to(pa.ax.c2p(1970, U["peak1970"] / 1000), UP, buff=0.1)
        now = tx(f"2025: {U['y2025'] / 1000:.2f}m", 16, WHITE, bold=True).next_to(pa.ax.c2p(2025, U["y2025"] / 1000), LEFT, buff=0.15)
        cum = tx(f"produced so far: {U['cum_2025']:.0f}bn barrels", 18, GOLD, bold=True).move_to(pa.ax.c2p(2030, 2.5))
        head = tx("US crude oil production, barrels a day", 18, GREY_A).next_to(pa, UP, buff=0.15).align_to(pa, LEFT)
        tag = estimate_tag("Hubbert's two curves redrawn as logistics through 1955's cumulative output", corner=DR, size=14)
        src = source("Hubbert (1956); EIA, US field production of crude oil, annual since 1859", size=13)
        with self.voiceover(
            "Perhaps the most famous oil forecast of all was made in March 1956, in a hotel in San Antonio, by a Shell "
            "geologist, M. King Hubbert. <bookmark mark='a'/> He had the record of American production to 1956. "
            "<bookmark mark='b'/> He argued that a field's, or a country's, output rises and falls in a bell shape, "
            "and that the area under the bell is the oil that will ever come out. If America held a hundred and fifty "
            "billion barrels in all, its output would peak around 1965. Even if it held two hundred billion, the peak "
            "would come only around 1970. <bookmark mark='c'/> Then American production "
            f"peaked in 1970, at {U['peak1970'] / 1000:.2f} million barrels a day, almost exactly on his upper curve, "
            "and fell for nearly forty years. <bookmark mark='d'/> And then shale. By 2025 production was "
            f"{U['y2025'] / 1000:.1f} million barrels a day, and the United States had produced {U['cum_2025']:.0f} "
            "billion barrels, more than either of Hubbert's totals. He was right about the date of the peak and wrong "
            "about the end, because he could not count oil that the technology of 1956 could not produce."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(lpre), run_time=2.0)
            self.play(Create(lab56), FadeIn(t56))
            vo.wait_until("b")
            self.play(Create(curves[0]), FadeIn(l150), run_time=1.6)
            self.play(Create(curves[1]), FadeIn(l200), run_time=1.6)
            vo.wait_until("c")
            k70 = [y for y, _ in post].index(1970) + 1
            part1 = VMobject(stroke_color=WHITE, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v) for y, v in post[:k70]])
            self.play(Create(part1), run_time=1.5)
            self.play(FadeIn(pk))
            k08 = [y for y, _ in post].index(2008) + 1
            part2 = VMobject(stroke_color=WHITE, stroke_width=4).set_points_as_corners(
                [pa.ax.c2p(y, v) for y, v in post[k70 - 1:k08]])
            self.play(Create(part2), run_time=1.5)
            vo.wait_until("d")
            part3 = VMobject(stroke_color=SHALE, stroke_width=5).set_points_as_corners(
                [pa.ax.c2p(y, v) for y, v in post[k08 - 1:]])
            self.play(Create(part3), run_time=1.8)
            self.play(FadeIn(now), FadeIn(cum))
        self.clear_scene()

    def world(self):
        W = R["world"]
        ys, w = W["years"], W["world"]
        pa = viz.plot_axes([1972, 2026], [0, 100], x_length=8.4, y_length=3.8, xticks=[1975, 1985, 1995, 2005, 2015, 2025],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=14)
        pa.move_to([0.4, -0.6, 0])
        ln = VMobject(stroke_color=BRENT, stroke_width=4).set_points_as_corners([pa.ax.c2p(y, v / 1000) for y, v in zip(ys, w)])
        y2k = DashedLine(pa.ax.c2p(2000, 0), pa.ax.c2p(2000, 95), stroke_color=PRICE, stroke_width=2)
        l2k = tx("Hubbert's world peak: 'about the year 2000'", 16, PRICE).next_to(pa.ax.c2p(2000, 95), UP, buff=0.05)
        end = tx(f"2025: {w[-1] / 1000:.1f}m barrels a day", 17, WHITE, bold=True).next_to(pa.ax.c2p(2025, w[-1] / 1000), DOWN, buff=0.6).shift(LEFT * 1.2)
        head = tx("World crude oil production", 18, GREY_A).next_to(pa, UP, buff=0.15).align_to(pa, LEFT)
        src = source("Hubbert (1956); EIA, International Energy Statistics", size=13)
        with self.voiceover(
            "He made a world forecast too. <bookmark mark='a'/> With twelve hundred and fifty billion barrels in all, "
            "world output would peak at about the year 2000. <bookmark mark='b'/> It did not. In 2025 the world "
            f"produced {w[-1] / 1000:.1f} million barrels of crude a day, more than ever. Higher prices kept paying "
            "for new ways to reach oil that had once been out of reach: deep water, oil sands, shale. The lesson is not that peaks never "
            "come. It is that the ceiling of a resource is set by price and technology as much as by geology."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(Create(y2k), FadeIn(l2k))
            vo.wait_until("b")
            self.play(Create(ln), run_time=2.5)
            self.play(FadeIn(end))
        self.clear_scene()

    def ours(self):
        S = R["shock"]
        c = R["call"]
        box = RoundedRectangle(corner_radius=0.15, width=12.2, height=2.6, fill_color="#141A24", fill_opacity=1,
                               stroke_color=GOLD, stroke_width=2).move_to(UP * 1.9)
        body = VGroup(tx("This series' call, made 24 November 2026", 22, GOLD, bold=True),
                      tx(f"Brent crude will average less than ${c['threshold']} a barrel in 2027", 20),
                      tx(f"(EIA's November forecast: ${S['brent_2027']:.0f}; 2026 so far: about ${S['brent_2026']:.0f}).", 18, GREY_A),
                      tx(f"Probability: {100 * c['prob']:.0f}%. Scored on EIA's annual Brent average, January 2028.", 17, GOLD)
                      ).arrange(DOWN, buff=0.12).move_to(box)
        forv = VGroup(tx("For", 20, GAS, bold=True), tx("shut-ins down from 10.9m to 2.5m b/d", 16, WHITE),
                      tx("demand and flows recovering", 16, WHITE), tx("stocks being rebuilt", 16, WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([-3.2, -1.5, 0])
        agv = VGroup(tx("Against", 20, STATE, bold=True), tx("the strait's flows remain at risk", 16, WHITE),
                     tx("stocks start the year low", 16, WHITE), tx("a market where small shortages move prices a lot", 16, WHITE)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.2, -1.5, 0])
        with self.voiceover(
            "And this series' own call. <bookmark mark='a'/> Brent crude will average less than ninety dollars a "
            f"barrel in 2027. The Energy Information Administration expects about {S['brent_2027']:.0f}. "
            "<bookmark mark='b'/> For it: the oil shut in has fallen from almost eleven million barrels a day to two and "
            "a half, demand is recovering, and stocks are being rebuilt. <bookmark mark='c'/> Against it: the strait "
            "is still at risk, stocks start the year low, and this chapter has shown how hard a small shortage can "
            f"move the price. We put it at {100 * c['prob']:.0f} percent, and will score it in January 2028."
        ) as vo:
            self.play(DrawBorderThenFill(box))
            vo.wait_until("a")
            self.play(FadeIn(body, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(forv, shift=RIGHT * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(agv, shift=LEFT * 0.1))
        self.clear_scene()
