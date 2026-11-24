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
        head = tx("The story so far", 36, GOLD, bold=True).to_edge(UP, buff=0.6)
        lines = ["Some industries earn far more than their capital costs, and keep doing so for years.",
                 "About a fifth of the differences in profit come from the industry, more from the company.",
                 "A few firms earn high returns only if newcomers are kept out and the few do not fight.",
                 "The walls: cost and scale, habit and brands, networks, and the law.",
                 "Next: how even the strongest walls come down."]
        # a small picture for each line
        hill = VGroup(Rectangle(width=0.9, height=0.25, stroke_width=0, fill_color=MOAT, fill_opacity=0.6),
                      draw.castle(0.45, color=STONE))
        hill[1].next_to(hill[0], UP, buff=0)
        net = VGroup(*[Dot(0.28 * np.array([np.cos(a_), np.sin(a_), 0]), radius=0.05, color=GOLD)
                       for a_ in np.linspace(0, TAU, 6, endpoint=False)])
        net.add(*[Line(net[i].get_center(), net[j].get_center(), stroke_width=1, stroke_color="#7EC8F5")
                  for i in range(6) for j in range(i + 1, 6)])
        walls = VGroup(VGroup(*[draw.coin(0.07) for _ in range(3)]).arrange(UP, buff=-0.04), net,
                       RoundedRectangle(corner_radius=0.04, width=0.3, height=0.4, stroke_width=0, fill_color="#E8E4DA",
                                        fill_opacity=1)).arrange(RIGHT, buff=0.12)
        drain = VGroup(draw.castle(0.5, moat=0.25, color=STONE), Arrow(UP * 0.2, DOWN * 0.3, color=COST_, buff=0,
                                                                       stroke_width=4).next_to(ORIGIN, RIGHT, buff=0.35))
        pics = [VGroup(draw.castle(0.5, moat=0.25, color=STONE), VGroup(*[draw.coin(0.07) for _ in range(4)]).arrange(
                    RIGHT, buff=0.02)).arrange(UP, buff=0.04),
                hill,
                VGroup(*[draw.castle(0.28, color=STONE) for _ in range(3)]).arrange(RIGHT, buff=0.05),
                walls, drain]
        rows = VGroup()
        for k, (pic, ln) in enumerate(zip(pics, lines)):
            pic.scale_to_fit_height(0.75)
            t_ = tx(ln, 25 if k < 4 else 23, WHITE if k < 4 else GREY_B)
            rows.add(VGroup(pic, t_).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(head, DOWN, buff=0.7)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        rows.set_x(0)
        for r_ in rows:
            r_[0].move_to([rows.get_left()[0] + 0.45, r_.get_y(), 0])
            r_[1].next_to(r_[0], RIGHT, buff=0.4)
            r_[1].align_to(rows[0][1], LEFT)
        with self.voiceover(
            "The story so far. <bookmark mark='a'/> Some industries earn far more than their capital costs, and keep "
            "doing so for years. <bookmark mark='b'/> About a fifth of the differences in profit come from the "
            "industry a business is in, more from the business itself. <bookmark mark='c'/> A few firms earn high "
            "returns only if newcomers are kept out and the few do not fight. <bookmark mark='d'/> And the walls that "
            "keep newcomers out are made of cost and scale, of habit and brands, of networks, and of the law. "
            "<bookmark mark='e'/> Next: how even the strongest walls come down."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k][0], scale=0.6), FadeIn(rows[k][1], shift=RIGHT * 0.15), run_time=0.9)
        self.clear_scene()
