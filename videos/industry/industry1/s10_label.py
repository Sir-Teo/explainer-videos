from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry1.common import *  # noqa: F403


class Label(VoiceoverScene):
    def construct(self):
        card(self, 10, "Made where?", "What does ‘Made in China’ measure?",
             "Chapter ten. Made where?", lit=("dollar", "change"))
        self.gross_trade()
        self.india()

    def gross_trade(self):
        cost, china = get("iphone3g.cost"), get("iphone3g.china")
        box = Rectangle(width=4.4, height=2.2, fill_color="#3A2A22", fill_opacity=1, stroke_color="#B07A57",
                        stroke_width=3).shift(LEFT * 3.4 + UP * 0.9)
        ribs = VGroup(*[Line(box.get_top() + RIGHT * x + DOWN * 0.1, box.get_bottom() + RIGHT * x + UP * 0.1,
                             color="#7A5440", stroke_width=2) for x in np.linspace(-1.9, 1.9, 9)])
        stencil = VGroup(TB("iPhone 3G", 26, I.TEXT), T("import from China", 22, REGION["China"]),
                         TB(money(cost, 2), 34, I.MONEY)).arrange(DOWN, buff=0.1).move_to(box)
        when = T("United States customs, 2009", 20, I.DIM).next_to(box, UP, buff=0.2)
        L = 6.0
        full = Rectangle(width=L, height=0.7, fill_color="#5A6272", fill_opacity=0.85, stroke_width=0)
        cn = Rectangle(width=L * china / cost, height=0.7, fill_color=REGION["China"], fill_opacity=1,
                       stroke_width=0)
        bar = VGroup(full, cn).move_to(RIGHT * 3.4 + UP * 0.9)
        cn.align_to(full, LEFT)
        l1 = VGroup(TB(money(china, 2), 26, REGION["China"]), T("value added in China: assembly (3.6%)", 18, I.TEXT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(bar, DOWN, buff=0.2).align_to(bar, LEFT)
        l2 = T("parts made in Japan, Germany, Korea, the US and elsewhere", 18, I.DIM).next_to(bar, UP, buff=0.15
                                                                                              ).align_to(bar, RIGHT)
        deficit = VGroup(T("Counted the customs way, iPhones added", 22, I.TEXT),
                         TB(f"${get('iphone3g.deficit'):.1f} billion", 30, I.COST),
                         T("to the 2009 US trade deficit with China", 22, I.TEXT)).arrange(RIGHT, buff=0.2)
        deficit.scale_to_fit_width(min(deficit.width, 12.6)).move_to(DOWN * 1.6)
        tiva = T("Trade in value added (OECD TiVA) counts each country's contribution instead of the last stop",
                 20, I.DIM).move_to(DOWN * 2.5)
        src = source("Xing and Detert (2010), ADBI Working Paper 257, after an iSuppli teardown")
        with self.voiceover(
            "Go back to the label. <bookmark mark='a'/> In 2009, when an iPhone 3G arrived in America from the "
            "factory in China, customs recorded an import from China worth 178 dollars 96, the phone's full "
            "manufacturing cost. <bookmark mark='b'/> Two economists, Yuqing Xing and Neal Detert, took the teardown "
            "apart by country. The work done in China, assembling and testing the phone, came to 6 dollars 50, "
            "3.6 percent of the cost. <bookmark mark='c'/> Everything else was parts made in Japan, Germany, Korea, "
            "the United States and elsewhere, which had merely passed through China. <bookmark mark='d'/> Counted "
            "the customs way, iPhones added 1.9 billion dollars to America's trade deficit with China that year. "
            "<bookmark mark='e'/> Counted by value added, almost all of that deficit was really with the countries "
            "that made the parts. Statisticians now publish trade in value added for exactly this reason."
        ) as vo:
            ship = draw.ship(5.6, boxes=0).move_to(box.get_bottom(), aligned_edge=DOWN).shift(
                DOWN * (0.135 * 5.6 + 0.02) + RIGHT * 0.4)
            sea = VGroup(*[Line([x, ship.get_bottom()[1] + 0.05, 0], [x + 0.5, ship.get_bottom()[1] + 0.05, 0],
                                stroke_color="#3B7DD8", stroke_width=2.5) for x in np.arange(-7.0, 0.0, 0.8)])
            cargo = VGroup(ship, box, ribs, stencil)
            cargo.shift(LEFT * 9)
            self.play(FadeIn(src), FadeIn(sea))
            vo.wait_until("a")
            self.play(cargo.animate.shift(RIGHT * 9), run_time=2.2, rate_func=rate_functions.ease_out_cubic)
            self.play(FadeIn(when))
            vo.wait_until("b")
            self.play(FadeIn(full), GrowFromEdge(cn, LEFT), FadeIn(l1))
            vo.wait_until("c")
            origins = [("Japan", REGION["Japan"]), ("Germany", "#C9D3E0"), ("Korea", REGION["Korea"]),
                       ("US", REGION["US"])]
            parts = VGroup()
            for k, (nm, col) in enumerate(origins):
                c = draw.chip(0.3, color=col)
                t = T(nm, 15, col).next_to(c, DOWN, buff=0.05)
                parts.add(VGroup(c, t).move_to([2.0 + 1.25 * k, 2.95, 0]))
            self.play(LaggedStart(*[FadeIn(p_, shift=DOWN * 0.2) for p_ in parts], lag_ratio=0.15), FadeIn(l2))
            self.play(LaggedStart(*[p_[0].animate.move_to(full.get_center() + RIGHT * (0.6 * k - 0.4)).scale(0.6)
                                    for k, p_ in enumerate(parts)], lag_ratio=0.15), run_time=1.4)
            vo.wait_until("d")
            self.play(FadeIn(deficit, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(tiva))
        self.clear_scene()

    def india(self):
        tiles = viz.region_map(regions=("US", "China", "India", "Taiwan", "Korea", "Japan"), w=1.9, h=0.9, size=21)
        world = VGroup(*tiles.values()).shift(UP * 0.9)
        a1 = CurvedArrow(tiles["China"].get_left() + DOWN * 0.1, tiles["India"].get_top() + RIGHT * 0.2,
                         color=REGION["India"], angle=0.6)
        share = VGroup(T("iPhones assembled in India", 20, I.DIM),
                       TB("2024: 36 million  →  2025: about 55 million", 24, REGION["India"]),
                       T("about one in four new iPhones (Bloomberg's estimate)", 18, I.DIM)
                       ).arrange(DOWN, buff=0.06).move_to(LEFT * 3.3 + DOWN * 1.3)
        tariffs = VGroup(T("From spring 2025 the US added tariffs on imports from", 18, I.DIM),
                         T("China, India, Japan, Korea, Taiwan, Vietnam and the EU", 18, I.TEXT),
                         T("Apple, Form 10-K, fiscal 2026", 15, I.FAINT)).arrange(DOWN, buff=0.05
                                                                                  ).move_to(RIGHT * 3.4 + DOWN * 1.2)
        L = 4.0
        moves = VGroup(
            VGroup(T("Move assembly of one phone from China to India.", 22, I.TEXT)),
            VGroup(Rectangle(width=L * 590 / 600, height=0.42, fill_color="#5A6272", fill_opacity=0.9, stroke_width=0),
                   T("customs records: the whole factory value, about $590, changes country", 18, I.TEXT)
                   ).arrange(RIGHT, buff=0.2),
            VGroup(Rectangle(width=L * amount("assembly") / 600, height=0.42, fill_color=REGION["India"],
                             fill_opacity=1, stroke_width=0),
                   T(f"value added: about {money(amount('assembly'))} of assembly work moves", 18, I.TEXT)
                   ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        moves.scale_to_fit_width(min(moves.width, 12.6)).to_edge(DOWN, buff=0.4)
        src = source("Bloomberg via Tech Wire Asia (2026-03); Apple Form 10-K FY2026", corner=UR)
        with self.voiceover(
            "The same arithmetic matters now that the label is changing. <bookmark mark='a'/> Apple has been moving "
            "iPhone assembly from China to India: about 36 million iPhones were assembled there in 2024 and about 55 "
            "million in 2025, roughly one in four, by Bloomberg's estimate. <bookmark mark='b'/> In the spring of "
            "2025 the United States announced new tariffs on imports from China, India and most of Apple's other "
            "supply countries, as Apple's annual report records, and phones bound for America were routed through "
            "India. <bookmark mark='c'/> Move the assembly of one phone from China to India and the customs "
            "statistics move the phone's whole factory value, about 590 dollars, from one country to the other. "
            "<bookmark mark='d'/> What actually moves is the assembly work: about 30 dollars, plus whatever parts "
            "come to be made locally. The label changes a great deal; where the money goes changes very little."
        ) as vo:
            self.play(FadeIn(world), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(a1), FadeIn(share, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(tariffs, shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeOut(share), FadeOut(tariffs), FadeIn(moves[0]), FadeIn(moves[1]))
            vo.wait_until("d")
            self.play(FadeIn(moves[2]))
        self.clear_scene()
