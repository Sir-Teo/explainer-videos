from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

# the delivery route (illustrative): a day's driving that is the same however many parcels, and a fixed time per stop
HOUSES, DRIVE, STOP = 120, 100.0, 1.67   # houses on the route; $ of van and driver for the loop; $ per stop


def per_parcel(share: float) -> float:
    stops = max(HOUSES * share, 1e-6)
    return (DRIVE + STOP * stops) / stops


class Scope(VoiceoverScene):
    def construct(self):
        card(self, 5, "Scope and density", "Why is the second product, or the second customer, so cheap?",
             "Chapter five. Scope and density.", lit=("make", "dollar"))
        self.belly()
        self.street()

    # --- scope: a second product from the same asset --------------------------------------------------------------
    def belly(self):
        S = R["scope"]
        jet = draw.plane(7.5).move_to([0, 1.55, 0])
        hold = RoundedRectangle(corner_radius=0.1, width=4.6, height=0.42, stroke_color=VAR, stroke_width=2,
                                fill_color="#141A24", fill_opacity=0.9).move_to(jet.get_center() + DOWN * 0.22 + LEFT * 0.4)
        boxes = VGroup(*[RoundedRectangle(corner_radius=0.03, width=0.34, height=0.28, stroke_width=0, fill_color=VAR,
                                          fill_opacity=0.95) for _ in range(10)]).arrange(RIGHT, buff=0.08)
        boxes.move_to(hold)
        start = [b.get_center().copy() for b in boxes]
        for b in boxes:
            b.shift(DOWN * 1.6 + LEFT * 3.5).set_opacity(0)
        pax = tx("passengers pay for the flight", 20, GREY_B).next_to(jet, UP, buff=0.2)
        cargo_t = tx(f"cargo in the hold: ${S['cargo'] * 1000:.0f} million in 2025", 22, VAR).next_to(jet, DOWN,
                                                                                                         buff=0.35)
        eq = MathTex(r"C(\text{flights}, \text{cargo}) \;<\; C(\text{flights}) + C(\text{cargo})", font_size=36).move_to(
            [0, -0.9, 0])
        src = source("Delta Air Lines Form 10-K 2025")
        with self.voiceover(
            "Scale is about making more of one thing. Scope is about making a second thing with what you already "
            "have. <bookmark mark='a'/> A Delta flight to Boston carries passengers, who pay for the plane, the "
            "fuel and the crew. <bookmark mark='b'/> Under their feet is a hold with room to spare, and Delta fills "
            "it with freight: nine hundred million dollars of cargo revenue in 2025, carried mostly in the holds "
            "of flights that would have flown anyway. <bookmark mark='c'/> That is an economy of scope: making two "
            "things together costs less than making them apart. The plane, the airport slot and the crew are shared."
        ) as vo:
            self.play(FadeIn(jet, shift=RIGHT * 0.5), FadeIn(pax), FadeIn(src))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(Create(hold))
            self.play(LaggedStart(*[b.animate.move_to(p).set_opacity(0.95) for b, p in zip(boxes, start)],
                                  lag_ratio=0.12), run_time=2.4)
            self.play(FadeIn(cargo_t))
            vo.wait_until("c")
            self.play(Write(eq))
        self.play(FadeOut(VGroup(hold, boxes, cargo_t, eq, pax)), jet.animate.scale(0.5).move_to([-4.3, 2.6, 0]))

        # the miles: Delta's customers, sold a second time to a bank
        card_ = VGroup(RoundedRectangle(corner_radius=0.14, width=2.2, height=1.38, stroke_width=0,
                                        fill_color="#2E6BB8", fill_opacity=1),
                       RoundedRectangle(corner_radius=0.03, width=0.36, height=0.27, stroke_width=0,
                                        fill_color="#E9C46A", fill_opacity=1).shift(LEFT * 0.6 + UP * 0.1),
                       tx("co-brand card", 16, WHITE).shift(DOWN * 0.38 + RIGHT * 0.25)).move_to([4.2, 2.45, 0])
        arrow = Arrow(card_.get_left(), jet.get_right() + RIGHT * 0.1, buff=0.25, color=PRICE, stroke_width=4)
        miles_t = tx("miles bought by American Express", 18, PRICE).next_to(arrow, DOWN, buff=0.08)
        coins = VGroup(*[draw.coin(0.1) for _ in range(6)])
        base = -2.9
        u = 0.55

        def bar(x, v, color, name):
            r_ = Rectangle(width=1.6, height=v * u, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to(
                [x, base, 0], aligned_edge=DOWN)
            return VGroup(r_, tx(name, 18, color).next_to(r_, DOWN, buff=0.12),
                          tx(f"${v:.1f}bn", 24, color, bold=True).next_to(r_, UP, buff=0.08))
        amex = bar(-1.3, S["amex"], PRICE, "paid by Amex for miles")
        oi = bar(1.3, S["oi"], PROFIT, "Delta's operating profit")
        with self.voiceover(
            "Scope reaches further than the hold. <bookmark mark='a'/> Delta's frequent flyers collect miles; Delta "
            "sells those miles to American Express, which hands them out to people who carry a Delta credit card. "
            "<bookmark mark='b'/> In 2025 American Express paid Delta about eight point two billion dollars, under "
            "that deal. <bookmark mark='c'/> Delta's operating profit for the whole year was five point eight "
            "billion. The two numbers are not like for like: the miles cost Delta seats it gives away. But the "
            "network, the brand and the customers that make the miles worth buying are the same ones that fly the "
            "planes. That is scope."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(card_, shift=LEFT * 0.3), GrowArrow(arrow), FadeIn(miles_t))
            for c in coins:
                c.move_to(card_.get_left())
            self.play(LaggedStart(*[MoveAlongPath(c, Line(card_.get_left(), jet.get_right()), rate_func=smooth)
                                    for c in coins], lag_ratio=0.15), run_time=2.0)
            self.remove(coins)
            vo.wait_until("b")
            self.play(GrowFromEdge(amex[0], DOWN), FadeIn(amex[1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(oi[0], DOWN), FadeIn(oi[1:]))
        self.clear_scene()

    # --- density: the second customer on the same street ----------------------------------------------------------
    def street(self):
        share = ValueTracker(0.05)
        road = VMobject(stroke_color="#3A4250", stroke_width=26)
        pts = [np.array([x, 0.55 * np.sin(x * 0.9) + 0.6, 0]) for x in np.linspace(-6.8, 6.8, 120)]
        road.set_points_smoothly(pts)
        lane = DashedLine(pts[0], pts[-1], stroke_width=0)
        lane = VMobject(stroke_color="#C9D3E0", stroke_width=1.5).set_points_smoothly(pts)
        lane = DashedVMobject(lane, num_dashes=60)
        houses = VGroup()
        n_show = 40
        rng = np.random.default_rng(3)
        order = rng.permutation(n_show)
        for i in range(n_show):
            x = -6.5 + 13.0 * (i + 0.5) / n_show
            y = 0.55 * np.sin(x * 0.9) + 0.6
            h = draw.house(0.3, color="#8C96A8")
            side = 1 if i % 2 == 0 else -1
            h.move_to([x, y + side * 0.42, 0])
            houses.add(h)
        parcels = VGroup(*[RoundedRectangle(corner_radius=0.02, width=0.14, height=0.12, stroke_width=0,
                                            fill_color=VAR, fill_opacity=1).next_to(h, UP, buff=0.04)
                           for h in houses])

        def upd_houses(m):
            k = int(round(n_show * share.get_value()))
            lit = set(order[:k].tolist())
            for i, (h, p) in enumerate(zip(m, parcels)):
                on = i in lit
                h[0].set_fill("#E8EAED" if on else "#5B6372")
                p.set_opacity(1 if on else 0)
        houses.add_updater(upd_houses)
        van = draw.truck(0.7, color=VAR)
        t = ValueTracker(0.0)
        van.add_updater(lambda m: m.move_to(road.point_from_proportion(t.get_value() % 1.0) + UP * 0.12))
        tag = estimate_tag("illustrative: $100 of van and driver a day, 1 minute and $1.67 a stop", corner=DR)

        ax = CornerAxes(x_range=[0, 0.6, 0.1], y_range=[0, 22, 5], x_length=5.2, y_length=2.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-2.9, -2.3, 0])
        curve = ax.plot(per_parcel, x_range=[0.04, 0.6, 0.005], color=VAR, stroke_width=4)
        xt = VGroup(*[tx(f"{int(100 * v)}%", 15, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.06) for v in (0.2, 0.4, 0.6)])
        yt = VGroup(*[tx(f"${v}", 15, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.06) for v in (10, 20)])
        xl = tx("share of houses that order", 16, GREY_B).next_to(ax, DOWN, buff=0.32)
        dot = always_redraw(lambda: glow_dot(ax.c2p(share.get_value(), per_parcel(share.get_value())), color=VAR,
                                             radius=0.08))
        cost = draw.number(lambda: per_parcel(share.get_value()), 2, prefix="$", size=46, color=VAR)
        cost.add_updater(lambda m: m.move_to([4.6, -2.1, 0]), call_updater=True)
        cost_t = tx("cost per parcel", 20, GREY_B).move_to([4.6, -1.45, 0])
        stops = draw.number(lambda: HOURS_STOPS(share.get_value()), 0, size=30, color=WHITE)
        stops.add_updater(lambda m: m.move_to([4.6, -3.2, 0]), call_updater=True)
        stops_t = tx("parcels on the route", 18, GREY_B).move_to([4.6, -2.75, 0])
        with self.voiceover(
            "Density is scope's cousin: the second customer on the same street. <bookmark mark='a'/> A delivery "
            "van drives the same loop every day. The van and the driver cost about a hundred dollars for the loop, "
            "however many parcels it carries; each stop adds a minute and a little under two dollars. "
            "<bookmark mark='b'/> If one house in twenty orders, the van drives past nineteen doors for every one it "
            f"stops at, and each parcel costs about {per_parcel(0.05):.0f} dollars to deliver. <bookmark mark='c'/> "
            f"Fill the street. At one house in five, the cost falls to under {per_parcel(0.2) + 0.5:.0f} dollars; at "
            f"half the street, about {per_parcel(0.5):.2f}. The road, the van and the driver are shared over more "
            "parcels."
        ) as vo:
            self.play(Create(road), FadeIn(lane), FadeIn(houses), FadeIn(parcels), FadeIn(tag))
            self.add(van)
            self.play(t.animate.set_value(0.35), run_time=2.0, rate_func=linear)
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(cost_t), FadeIn(cost), FadeIn(stops_t),
                      FadeIn(stops), t.animate.set_value(0.7), run_time=2.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(dot), t.animate.set_value(1.0), run_time=2.0, rate_func=linear)
            vo.wait_until("c")
            self.play(share.animate.set_value(0.2), t.animate.set_value(1.5), run_time=3.0, rate_func=linear)
            self.play(share.animate.set_value(0.5), t.animate.set_value(2.0), run_time=3.0, rate_func=linear)
        lesson = tx("Density is why the first network on a street is so hard to catch.", 26, PRICE, bold=True)
        lesson.to_edge(UP, buff=0.3)
        with self.voiceover(
            "This is why delivery firms, postal services, cable companies and power lines care so much about "
            "density, and why a second network on the same street finds it hard to catch the first: with half the "
            "customers per mile, every one of them costs more to serve. <bookmark mark='a'/> Density is why the "
            "first network on a street is so hard to catch."
        ) as vo:
            self.play(share.animate.set_value(0.25), t.animate.set_value(2.6), run_time=3.0, rate_func=linear)
            vo.wait_until("a")
            self.play(FadeIn(lesson, shift=DOWN * 0.1))
        for m in (houses, van, cost, stops):
            m.clear_updaters()
        self.clear_scene()


def HOURS_STOPS(share: float) -> float:
    return HOUSES * share
