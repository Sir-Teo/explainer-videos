from __future__ import annotations

from explainer.industry.data.fetch import read
from videos.industry.industry5.common import *  # noqa: F403

PICK = [("Tobacco", "Tobacco", "#C9A26B"), ("Beverage (Soft)", "Soft drinks", "#E8554E"),
        ("Software (System & Application)", "Software", "#B58CFF"), ("Retail (Building Supply)", "Home centers",
                                                                    "#F2A65A"),
        ("Restaurant/Dining", "Restaurants", "#7BD88F"), ("Air Transport", "Airlines", "#7EC8F5"),
        ("Auto & Truck", "Carmakers", "#8C929B"), ("Oil/Gas (Production and Exploration)", "Oil and gas", "#3B7DD8")]


class Intermission(VoiceoverScene):
    def construct(self):
        rows = read("damodaran_roc")
        by = {}
        for r in rows:
            if isinstance(r["roc"], float):
                by.setdefault(r["name"], {})[int(r["year"])] = r["roc"]
        pick = [p for p in PICK if p[0] in by]
        years = sorted(y for y in by[pick[0][0]] if all(y in by[p[0]] for p in pick))
        L, H = 7.4, 0.48
        x0 = -2.2

        def frame(y):
            vals = [(p, by[p[0]][y]) for p in pick]
            order = sorted(vals, key=lambda t: -t[1])
            g = VGroup()
            for k, (p, v) in enumerate(order):
                yy = 2.35 - 0.62 * k
                w = max(L * min(max(v, -0.1), 0.7) / 0.7, 0.03)
                bar = Rectangle(width=w, height=H, stroke_width=0, fill_color=p[2], fill_opacity=0.9).move_to(
                    [x0, yy, 0], aligned_edge=LEFT)
                name = tx(p[1], 20, WHITE).next_to([x0, yy, 0], LEFT, buff=0.15)
                val = tx(f"{100 * v:.0f}%", 18, p[2], bold=True).next_to(bar, RIGHT, buff=0.12)
                g.add(VGroup(name, bar, val))
            return g
        head = tx("Intermission: return on capital, eight industries, 2015 to 2025", 24).to_edge(UP, buff=0.3)
        yr = tx(str(years[0]), 44, GREY_A, bold=True).to_corner(DR, buff=0.6)
        cur = frame(years[0])
        src = source("Damodaran, Excess Returns by industry, US companies, 2015-2025")
        with self.voiceover(
            "An intermission: the same eight industries, every year from 2015 to 2025, ranked by their return on "
            "capital. <bookmark mark='a'/> Watch the order rather than the numbers. Oil and gas swing with the "
            "price of oil; airlines fall off the bottom in the pandemic and climb back; software and soft drinks "
            "barely move. Carmakers sit near the bottom in good years and bad. <bookmark mark='b'/> And tobacco stays "
            "at the top the whole way through. The ranking changes much less than the numbers do: that is the "
            "persistence of chapter two, seen year by year."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(cur), FadeIn(yr))
            vo.wait_until("a")
            for y in years[1:]:
                nxt = frame(y)
                ny = tx(str(y), 44, GREY_A, bold=True).move_to(yr)
                self.play(Transform(cur, nxt), Transform(yr, ny), run_time=1.0)
                self.wait(0.25)
            vo.wait_until("b")
            self.play(Indicate(cur[0], color=GOLD, scale_factor=1.05))
        self.clear_scene()
        self.story()

    def story(self):
        so = VGroup(tx("The story so far", 36, GOLD, bold=True),
                    tx("Some industries earn far more than their capital costs, and keep doing so for years.", 23),
                    tx("About a fifth of the differences in profit come from the industry, more from the company.", 23),
                    tx("A few firms earn high returns only if newcomers are kept out and the few do not fight.", 23),
                    tx("The walls: cost and scale, habit and brands, networks, and the law.", 23),
                    tx("Next: how even the strongest walls come down.", 21, GREY_B)).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "The story so far. Some industries earn far more than their capital costs, and keep doing so for "
            "years. About a fifth of the differences in profit come from the industry a business is in, more from "
            "the business itself. A few firms earn high returns only if newcomers are kept out and the few do not "
            "fight. And the walls that keep newcomers out are made of cost and scale, of habit and brands, of "
            "networks, and of the law. Next: how even the strongest walls come down."
        ):
            self.play(LaggedStart(*[FadeIn(x_, shift=UP * 0.1) for x_ in so], lag_ratio=0.5), run_time=5)
        self.clear_scene()
