from __future__ import annotations

from videos.industry.industry7.common import *  # noqa: F403


class Homes(VoiceoverScene):
    def construct(self):
        card(self, 5, "When adding up companies works", "Can a market be rebuilt from a few companies' accounts?",
             "Chapter five. When adding up companies works.", lit=("unit", "moat"))
        H = R["homes"]
        u = 0.017
        base = -2.7
        cen = Rectangle(width=1.8, height=H["census"] * u, stroke_width=0, fill_color=FACTORY, fill_opacity=0.9).move_to(
            [-2.4, base, 0], aligned_edge=DOWN)
        hd = Rectangle(width=1.8, height=H["hd"] * u, stroke_width=0, fill_color=GUESS, fill_opacity=0.95).move_to(
            [1.0, base, 0], aligned_edge=DOWN)
        lw = Rectangle(width=1.8, height=H["low"] * u, stroke_width=0, fill_color=UNITS, fill_opacity=0.95).next_to(
            hd, UP, buff=0)
        t_cen = VGroup(tx(f"${H['census']:.0f}bn", 28, FACTORY, bold=True), tx(f"Census, 2022: all {H['firms']} firms",
                                                                               15, GREY_B)).arrange(DOWN, buff=0.04).next_to(
            cen, UP, buff=0.1)
        t_hd = tx(f"Home Depot ${H['hd']:.0f}bn", 17, "#0E1117", bold=True).move_to(hd)
        t_lw = tx(f"Lowe's ${H['low']:.0f}bn", 17, "#0E1117", bold=True).move_to(lw)
        t_both = VGroup(tx(f"${H['both']:.0f}bn", 28, WHITE, bold=True), tx("their revenue, fiscal 2022", 15, GREY_B)
                        ).arrange(DOWN, buff=0.04).next_to(lw, UP, buff=0.1)
        stores = VGroup(draw.shop(1.4, color=GUESS), draw.shop(1.4, color=UNITS)).arrange(RIGHT, buff=0.3).move_to(
            [4.8, 1.6, 0])
        notes = VGroup(tx("their revenue includes Canada and Mexico,", 15, GREY_B),
                       tx("and some sales outside home centers;", 15, GREY_B),
                       tx("the Census includes Menards and smaller chains", 15, GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.04).move_to([4.8, -0.6, 0])
        src = source("US Census Bureau, 2022 Economic Census (home centers, NAICS 444110); Home Depot and Lowe's, Forms 10-K "
                     "for fiscal 2022 (SEC company facts)", size=13)
        with self.voiceover(
            "Adding up companies can work very well, in one kind of market. <bookmark mark='a'/> Part 5 met the "
            f"American home centers: {H['firms']} firms, of which the four largest made {H['cr4']:.0f} percent of the "
            f"sales. The 2022 census counted {H['census']:.0f} billion dollars. <bookmark mark='b'/> Now add up just "
            f"two companies' annual reports. Home Depot: {H['hd']:.0f} billion dollars. <bookmark mark='c'/> Lowe's: "
            f"{H['low']:.0f} billion. <bookmark mark='d'/> Together, {H['both']:.0f} billion: within "
            f"{abs(100 * H['gap']):.0f} or 2 percent of the census. <bookmark mark='e'/> Do not take the closeness too "
            "seriously. The two companies' revenue includes their stores in Canada and Mexico and some business that "
            "is not a home center, while the census includes Menards and smaller chains; the differences happen to "
            "roughly cancel. But the lesson stands: when a few companies hold almost the whole market, their own "
            "accounts are the best bottom-up estimate there is. When thousands of small firms share it, as nail "
            "salons do, adding up companies is hopeless, and only a census will do."
        ) as vo:
            self.play(FadeIn(src), FadeIn(stores, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(GrowFromEdge(cen, DOWN), FadeIn(t_cen))
            vo.wait_until("b")
            self.play(GrowFromEdge(hd, DOWN), FadeIn(t_hd))
            vo.wait_until("c")
            self.play(GrowFromEdge(lw, DOWN), FadeIn(t_lw))
            vo.wait_until("d")
            self.play(FadeIn(t_both, shift=UP * 0.1))
            self.play(Indicate(VGroup(cen, hd, lw), color=WHITE, scale_factor=1.02))
            vo.wait_until("e")
            self.play(FadeIn(notes, shift=LEFT * 0.1))
        self.clear_scene()
