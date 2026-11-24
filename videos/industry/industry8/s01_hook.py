from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.cushing()
        self.hormuz()
        self.title()

    def cushing(self):
        N = R["negative"]
        lvl = ValueTracker(0.45)
        tanks = VGroup(*[draw.tank(1.05, 0.45) for _ in range(6)]).arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.35))
        tanks.move_to([-4.2, -0.2, 0])

        def refill(m):
            for t_ in m:
                h = max(t_.h * lvl.get_value() * 0.96, 0.001)
                t_.oil.stretch_to_fit_height(h, about_edge=DOWN)
        for t_ in tanks:
            t_.oil.stretch_to_fit_height(t_.h * 0.45 * 0.96, about_edge=DOWN)
        tanks.add_updater(refill)
        where = VGroup(tx("Cushing, Oklahoma", 22, WHITE, bold=True), tx("where WTI futures are delivered", 15, GREY_B)
                       ).arrange(DOWN, buff=0.05).next_to(tanks, UP, buff=0.3)
        full = draw.number(lambda: 100 * lvl.get_value(), 0, suffix="% full", size=28, color=CRUDE)
        full.add_updater(lambda m: m.next_to(tanks, DOWN, buff=0.3))
        price = ValueTracker(N["prior"])
        tick = draw.memo_redraw(lambda: round(price.get_value(), 2),
                                lambda v: tx(("-" if v < 0 else "") + f"${abs(v):.2f}", 64,
                                             STATE if v < 0 else PRICE, bold=True),
                                lambda m: m.move_to([2.9, 1.3, 0]))
        what = VGroup(tx("a barrel of WTI crude for May delivery", 20, GREY_A),
                      tx("New York Mercantile Exchange", 15, GREY_B)).arrange(DOWN, buff=0.05).next_to(
            [2.9, 2.3, 0], UP, buff=0.05)
        days = draw.memo_redraw(lambda: "Friday 17 April 2020" if price.get_value() > 0 else "Monday 20 April 2020",
                                lambda s: tx(s, 22, WHITE), lambda m: m.move_to([2.9, 0.3, 0]))
        brl = draw.barrel(1.3, color="#2F6FA8").move_to([2.9, -1.6, 0])
        coins = VGroup(*[draw.coin(0.16) for _ in range(5)]).arrange(RIGHT, buff=0.06).next_to(brl, RIGHT, buff=0.5)
        src = source("CFTC, Interim Staff Report on NYMEX WTI (2020); EIA, Today in Energy, 27 April 2020", size=13)
        with self.voiceover(
            "On Friday the seventeenth of April 2020, a barrel of American crude oil for delivery in May sold for "
            f"{N['prior']:.2f} dollars. <bookmark mark='a'/> The world had stopped driving and flying, and the oil "
            "nobody was burning had to go somewhere. Much of America's went into the tanks at Cushing, Oklahoma, "
            f"where that contract is delivered. By the seventeenth, the tanks there were {N['cushing']:.0f} percent "
            "full, and some of the empty space was already leased to others. <bookmark mark='b'/> On Monday, anyone still "
            "holding the contract would have to take the oil, with nowhere to put it. <bookmark mark='c'/> So they "
            f"paid others to take it. The contract settled at minus {abs(N['settle']):.2f} dollars a barrel. "
            "<bookmark mark='d'/> For a day, a barrel of oil was worth less than nothing: whoever took it was paid "
            "almost thirty-eight dollars."
        ) as vo:
            self.play(FadeIn(src), FadeIn(tanks), FadeIn(where), FadeIn(what), FadeIn(brl, shift=UP * 0.2))
            self.add(tick, days)
            vo.wait_until("a")
            self.add(full)
            self.play(lvl.animate.set_value(N["cushing"] / 100), run_time=3.5, rate_func=smooth)
            vo.wait_until("b")
            self.play(Indicate(tanks, color=CRUDE, scale_factor=1.03))
            vo.wait_until("c")
            self.play(price.animate.set_value(N["settle"]), run_time=3.0, rate_func=rate_functions.ease_in_cubic)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(c_, shift=LEFT * 0.3) for c_ in coins], lag_ratio=0.15),
                      brl.animate.shift(LEFT * 0.3), run_time=1.4)
        tanks.clear_updaters()
        for m in (tick, days, full):
            m.clear_updaters()
        self.clear_scene()

    def hormuz(self):
        S = R["shock"]
        # a stylized strait: two coasts and a narrow channel
        north = Polygon([-7.2, 3.8, 0], [7.2, 3.8, 0], [7.2, 1.2, 0], [1.2, 1.4, 0], [0.3, 0.55, 0], [-0.8, 0.9, 0],
                        [-7.2, 1.6, 0], stroke_width=0, fill_color="#4B4030", fill_opacity=1)
        south = Polygon([-7.2, -1.2, 0], [-2.0, -1.0, 0], [-0.6, -0.15, 0], [0.4, -0.35, 0], [1.6, -0.9, 0],
                        [7.2, -1.4, 0], [7.2, -1.6, 0], [-7.2, -1.6, 0], stroke_width=0, fill_color="#5C4E3A",
                        fill_opacity=1)
        sea = Rectangle(width=14.4, height=3.4, stroke_width=0, fill_color="#123A5C", fill_opacity=1).move_to([0, 0.1, 0])
        names = VGroup(tx("Iran", 18, GREY_A).move_to([-3.5, 2.4, 0]), tx("Oman", 18, GREY_A).move_to([1.6, -1.25, 0]),
                       tx("the Gulf", 16, BRENT).move_to([-4.6, 0.2, 0]), tx("to Asia and Europe", 16, BRENT).move_to(
                           [4.8, 0.1, 0]))
        ships = VGroup(*[draw.tanker(1.1) for _ in range(4)]).arrange(RIGHT, buff=0.45).move_to([-4.6, 0.25, 0])
        flow = VGroup(tx(f"about {S['hormuz']:.0f} million barrels a day in 2024:", 17, WHITE),
                      tx("a fifth of the world's oil", 17, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(
            [-4.4, -0.55, 0])
        map_ = VGroup(sea, north, south, names, ships, flow)
        map_.shift(UP * 0.9)
        # Brent month by month, 2025-26, beneath
        ms, br = S["months"], S["brent"]
        pa = viz.plot_axes([2025, 2026.9], [40, 140], x_length=9.0, y_length=2.2, xticks=[2025, 2026],
                           yticks=[60, 100, 140], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=13)
        pa.move_to([0.3, -2.45, 0])
        pts = [pa.ax.c2p(mx(m), b) for m, b in zip(ms, br) if b is not None]
        line = VMobject(stroke_color=BRENT, stroke_width=4).set_points_as_corners(pts)
        k_feb = ms.index("2026-02")
        pre, post = VMobject(stroke_color=BRENT, stroke_width=4).set_points_as_corners(pts[:k_feb + 1]), \
            VMobject(stroke_color=STATE, stroke_width=4).set_points_as_corners(pts[k_feb:])
        oct_ = VGroup(tx(f"Oct 2026: ${S['brent_oct']:.0f}", 20, STATE, bold=True)).next_to(pts[-1], LEFT, buff=0.15)
        lab = tx("Brent, monthly average", 14, GREY_B).next_to(pa, UP, buff=0.02).align_to(pa, LEFT)
        src = source("EIA, Today in Energy (7 April 2026; June 2025) and Short-Term Energy Outlook (10 November 2026); "
                     "Brent spot (EIA)", size=13)
        with self.voiceover(
            "Six years later, the opposite. <bookmark mark='a'/> About a fifth of the world's oil sails out of the "
            "Persian Gulf through one narrow strait, between Iran and Oman: some twenty million barrels a day. "
            "<bookmark mark='b'/> On the twenty-eighth of February 2026, war came to the region, and most ships "
            "stopped passing through the Strait of Hormuz. <bookmark mark='c'/> Brent crude had begun the year at "
            f"{S['brent_start']:.0f} dollars a barrel. By the end of March it was {S['brent_q1']:.0f}. In October it "
            f"averaged {S['brent_oct']:.0f}. <bookmark mark='d'/> The same black liquid. Minus thirty-seven dollars "
            f"one spring, a hundred and twenty-four another. This part is about why: what a barrel costs to get out "
            "of the ground, who owns it, and who, or what, decides what it sells for."
        ) as vo:
            self.play(FadeIn(src), FadeIn(sea), FadeIn(north), FadeIn(south), FadeIn(names), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(ships), FadeIn(flow))
            self.play(ships.animate.shift(RIGHT * 3.3), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(ships.animate.shift(RIGHT * 0.5), run_time=1.0, rate_func=rate_functions.ease_out_cubic)
            self.play(ships.animate.set_opacity(0.35), Flash(ships.get_center(), color=STATE, line_length=0.4))
            vo.wait_until("c")
            self.play(FadeIn(pa), FadeIn(lab), Create(pre), run_time=1.5)
            self.play(Create(post), run_time=2.0)
            self.play(FadeIn(oct_))
            vo.wait_until("d")
            self.play(Indicate(oct_, color=WHITE))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part eight: oil and gas. What does a barrel cost, and who decides what it sells for?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
