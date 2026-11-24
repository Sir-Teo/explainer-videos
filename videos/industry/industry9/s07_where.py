from __future__ import annotations

from videos.industry.industry9.common import *  # noqa: F403

PLACES = {"chl": ("Chile", -70, -24), "cod": ("Congo (DRC)", 26, -8), "per": ("Peru", -75, -11),
          "chn": ("China", 104, 33), "rus": ("Russia", 95, 58), "usa": ("United States", -105, 38),
          "zmb": ("Zambia", 28, -15), "aus": ("Australia", 134, -25), "idn": ("Indonesia", 137, -4),
          "kaz": ("Kazakhstan", 68, 48), "jpn": ("Japan", 139, 37)}


def r_of(kt):
    return 0.055 * np.sqrt(kt / 100)


class Where(VoiceoverScene):
    def construct(self):
        card(self, 6, "Where metal comes from", "Who digs the copper, and who turns it into metal?",
             "Chapter six. Where metal comes from.", lit=("unit", "moat"))
        self.maps()
        self.reserves()

    def maps(self):
        W = R["where"]
        wm = draw.world_map(12.4).move_to([0, 0.25, 0])
        mines = VGroup()
        mlabs = VGroup()
        for k, v in W["mine"].items():
            name, lo, la = PLACES[k]
            c = Circle(r_of(v), stroke_color=COPPER, stroke_width=2, fill_color=COPPER, fill_opacity=0.55).move_to(
                wm.p(lo, la))
            mines.add(c)
            if v >= 900:
                mlabs.add(VGroup(tx(name, 14, WHITE, bold=True), tx(f"{v:,.0f} kt", 13, COPPER)).arrange(
                    DOWN, buff=0.02).next_to(c, LEFT if lo < -60 else DOWN, buff=0.06))
        refs = VGroup()
        rlabs = VGroup()
        for k, v in W["refined"].items():
            name, lo, la = PLACES[k]
            c = Circle(r_of(v), stroke_color=CHINA, stroke_width=2.5, fill_color=CHINA, fill_opacity=0.25).move_to(
                wm.p(lo, la))
            refs.add(c)
            if v >= 1500:
                rlabs.add(VGroup(tx(name, 15, WHITE, bold=True), tx(f"{v:,.0f} kt refined", 14, CHINA)).arrange(
                    DOWN, buff=0.02).next_to(c, UP, buff=0.06))
        key = VGroup(VGroup(Dot(color=COPPER, radius=0.1), tx("copper mined, 2025", 16, COPPER)).arrange(RIGHT, buff=0.1),
                     VGroup(Circle(0.1, stroke_color=CHINA, stroke_width=2.5), tx("copper refined, 2025", 16, CHINA)
                            ).arrange(RIGHT, buff=0.1)).arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.35)
        tot = VGroup(tx(f"world mined: {W['world_mine'] / 1000:.0f} million tonnes", 18, COPPER, bold=True),
                     tx(f"world refined: {W['world_refined'] / 1000:.0f} million tonnes", 18, CHINA, bold=True)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.06).to_corner(DL, buff=0.55)
        share = VGroup()
        for lab, frac, col in [("China's share of copper mined", W["china_mine_share"], COPPER),
                               ("China's share of copper refined", W["china_share"], CHINA)]:
            bg = Rectangle(width=3.6, height=0.32, stroke_color=GREY_B, stroke_width=1, fill_opacity=0)
            fg = Rectangle(width=3.6 * frac, height=0.32, stroke_width=0, fill_color=col, fill_opacity=0.85).align_to(
                bg, LEFT)
            share.add(VGroup(tx(lab, 15, WHITE), VGroup(bg, fg, tx(f"{100 * frac:.0f}%", 17, WHITE, bold=True).next_to(
                bg, RIGHT, buff=0.1))).arrange(DOWN, aligned_edge=LEFT, buff=0.06))
        share.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.5).shift(LEFT * 0.4)
        china = wm.p(*PLACES["chn"][1:])
        routes = VGroup(*[CurvedArrow(wm.p(*PLACES[k][1:]) + UP * 0.15, china + LEFT * 0.4 + DOWN * 0.1, angle=a,
                                      stroke_width=2, color=COPPER, tip_length=0.12)
                          for k, a in [("chl", -0.9), ("per", -0.9), ("cod", -0.5), ("zmb", -0.4), ("aus", 0.6)]])
        for r_ in routes:
            r_.set_stroke(opacity=0.6)
        rlab = tx("illustrative routes: concentrate and part-refined copper", 13, GREY_B).next_to(share, UP, buff=0.15
                                                                                                    ).align_to(share, LEFT)
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'copper' (2025 estimates)", corner=UL,
                     size=13).shift(DOWN * 0.35)
        with self.voiceover(
            "Copper is mined where geology put it, and refined where industry put the smelters, and those are not the "
            "same places. <bookmark mark='a'/> Here is the world's copper mining in 2025, from the US Geological "
            f"Survey. Chile dug {W['mine']['chl'] / 1000:.1f} million tonnes, the most of any country. Then Congo, "
            "whose copper belt runs into Zambia, then Peru, then China, Russia and the United States. In all, "
            f"about {W['world_mine'] / 1000:.0f} million tonnes. <bookmark mark='b'/> Now the refining. "
            f"China refined {W['refined']['chn'] / 1000:.0f} million tonnes of copper, from mines that dug only "
            f"{W['mine']['chn'] / 1000:.1f}. <bookmark mark='c'/> China mines about "
            f"{100 * W['china_mine_share']:.0f} percent of the world's copper and refines about "
            f"{100 * W['china_share']:.0f} percent of it. The rest of its supply arrives by sea, as concentrate and as "
            "part-refined copper from Chile, Peru, Congo and elsewhere, and as scrap. <bookmark mark='d'/> Notice too "
            f"that the world refined about {(W['world_refined'] - W['world_mine']) / 1000:.0f} million tonnes more "
            "copper than it mined. Copper does not wear out. Old wire, pipes and engines are melted down and refined "
            "again, and that is a large part of the supply. The country that refines the metal sets the terms on which "
            "the miners sell it, and that is a theme that will come back in the chapter on critical minerals."
        ) as vo:
            self.play(FadeIn(wm), FadeIn(src), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(c) for c in mines], lag_ratio=0.15), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in mlabs], lag_ratio=0.15), FadeIn(tot[0]), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeOut(mlabs), FadeIn(key[1]))
            self.play(LaggedStart(*[GrowFromCenter(c) for c in refs], lag_ratio=0.15), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(l_) for l_ in rlabs], lag_ratio=0.15), FadeIn(tot[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(share[0]))
            self.play(FadeIn(share[1]))
            self.play(LaggedStart(*[Create(r_) for r_ in routes], lag_ratio=0.2), FadeIn(rlab), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(tot[1], color=WHITE, scale_factor=1.05))
        self.clear_scene()

    def reserves(self):
        W = R["where"]
        res = get("usgs.cu.reserves")
        years = res / (W["world_mine"] / 1000)
        glass = VGroup(Polygon([-0.9, 1.3, 0], [0.9, 1.3, 0], [0.08, 0, 0], [-0.08, 0, 0], stroke_color=STONE,
                               stroke_width=3, fill_opacity=0),
                       Polygon([-0.9, -1.3, 0], [0.9, -1.3, 0], [0.08, 0, 0], [-0.08, 0, 0], stroke_color=STONE,
                               stroke_width=3, fill_opacity=0),
                       Line([-1.1, 1.3, 0], [1.1, 1.3, 0], stroke_color=STONE, stroke_width=6),
                       Line([-1.1, -1.3, 0], [1.1, -1.3, 0], stroke_color=STONE, stroke_width=6))
        sand = ValueTracker(0.85)
        C = np.array([-4.3, 0.3, 0])

        def top_sand():
            f = sand.get_value()
            y = 1.25 * f
            return Polygon(*[C + q for q in ([-0.08 - 0.82 * f, y, 0], [0.08 + 0.82 * f, y, 0], [0.06, 0.02, 0],
                                             [-0.06, 0.02, 0])], stroke_width=0, fill_color=COPPER, fill_opacity=0.9)

        def bottom_sand():
            f = 1 - sand.get_value()
            y = -1.28 + 1.0 * f
            return Polygon(*[C + q for q in ([-0.9 + 0.62 * f, y, 0], [0.9 - 0.62 * f, y, 0], [0.9, -1.28, 0],
                                             [-0.9, -1.28, 0])], stroke_width=0, fill_color=COPPER, fill_opacity=0.9)
        glass.shift(C)
        stream = Line(C + [0, 0.02, 0], C + [0, -1.2, 0], stroke_color=COPPER, stroke_width=2)
        hour = VGroup(always_redraw(top_sand), always_redraw(bottom_sand), stream, glass)
        big = VGroup(tx(f"{res:,.0f} million tonnes", 40, COPPER, bold=True), tx("of copper in known reserves", 20, WHITE),
                     tx(f"about {years:.0f} years of today's mining", 24, PRICE, bold=True)).arrange(DOWN, buff=0.15
                                                                                                    ).move_to([1.6, 1.3, 0])
        notes = VGroup(tx("A reserve is copper that is known, and worth mining", 19, GREY_A),
                       tx("at today's prices and with today's technology.", 19, GREY_A),
                       tx("Raise the price, or improve the process, and it grows.", 19, WHITE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([1.6, -1.4, 0])
        src = source("US Geological Survey, Mineral Commodity Summaries 2026, 'copper'", size=13)
        with self.voiceover(
            "How long can this last? <bookmark mark='a'/> The Geological Survey counts about "
            f"{res:,.0f} million tonnes of copper in the world's known reserves: about {years:.0f} years at today's "
            "rate of mining. <bookmark mark='b'/> That sounds like a countdown, but it is not one. As with oil in Part "
            "eight, a reserve is an economic number: copper that is known and worth mining at today's prices with "
            "today's methods. When the price rises or the methods improve, poorer rock becomes ore, and the reserves "
            "grow. People have been predicting that copper will run out within a few decades for a long time. What "
            "happens instead is that the grade falls, and the cost of the next tonne rises."
        ) as vo:
            self.play(FadeIn(hour), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(big, shift=UP * 0.1), sand.animate.set_value(0.6), run_time=3.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n) for n in notes], lag_ratio=0.4), run_time=2.0)
            self.play(sand.animate.set_value(0.95), run_time=3.0)
        self.clear_scene()
