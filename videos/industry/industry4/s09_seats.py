from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403

ROWS, ACROSS = 20, 6   # a 120-seat cabin


class Seats(VoiceoverScene):
    def construct(self):
        card(self, 7, "The empty seat", "How full does a plane have to be before it makes money?",
             "Chapter seven. The empty seat.", lit=("dollar", "make"))
        self.cabin()

    def cabin(self):
        Q = R["seats"]
        n = ROWS * ACROSS
        be = Q["break_even"]
        cab = draw.cabin(ROWS, (3, 3), size=0.27, gap=0.06).move_to([-1.2, 1.6, 0])
        seats = cab.seats
        # board front to back, window to aisle, so the fill reads as a share
        order = sorted(range(n), key=lambda i: (i // ACROSS, abs((i % ACROSS) - 2.5)))
        lf = ValueTracker(0.0)
        n_be = int(round(be * n))
        n_lf = int(round(Q["load"] * n))

        def paint(m):
            k = int(round(lf.get_value() * n))
            for rank, i in enumerate(order):
                if rank >= k:
                    col = "#2E3645"
                elif rank < n_be:
                    col = VAR
                else:
                    col = PROFIT
                m[i].set_fill(col, opacity=1)
        seats.add_updater(paint)
        nose = Arc(radius=0.75, start_angle=-PI / 2, angle=PI, stroke_color=GREY_B, stroke_width=2).next_to(
            cab, RIGHT, buff=-0.35)
        head = tx("Delta Air Lines in 2025, per seat flown one mile", 26, bold=True).to_edge(UP, buff=0.3)
        src = source("Delta Air Lines Form 10-K 2025: revenue and cost per available seat mile, load factor")
        lf_n = draw.number(lambda: 100 * lf.get_value(), 0, suffix="%", size=48, color=WHITE)
        lf_n.add_updater(lambda m: m.move_to([5.2, 1.75, 0]), call_updater=True)
        lf_t = tx("of seats filled", 20, GREY_B).move_to([5.2, 1.1, 0])

        # cents per seat mile: cost (all seats) against revenue (filled seats)
        ax = CornerAxes(x_range=[0, 1.0, 0.25], y_range=[0, 27, 5], x_length=7.4, y_length=2.7,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-1.0, -1.95, 0])
        xt = VGroup(*[tx(f"{int(100 * v)}%", 16, GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.06)
                      for v in (0.25, 0.5, 0.75, 1.0)])
        yt = VGroup(*[tx(f"{v}¢", 16, GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.06) for v in (10, 20)])
        cost = ax.plot(lambda x: Q["casm"], x_range=[0, 1.0], color=LOSS, stroke_width=3)
        rev = ax.plot(lambda x: Q["per_rpm"] * x, x_range=[0, 1.0], color=PROFIT, stroke_width=3)
        cost_t = tx(f"cost: {Q['casm']:.2f}¢ for every seat", 17, LOSS).next_to(ax.c2p(0.02, Q["casm"]), UP, buff=0.06).align_to(
            ax.c2p(0.02, 0), LEFT)
        rev_t = tx(f"revenue: {Q['per_rpm']:.1f}¢ for every filled seat", 17, PROFIT).move_to(ax.c2p(0.56, 10.5),
                                                                                              aligned_edge=LEFT)
        dot = always_redraw(lambda: glow_dot(ax.c2p(lf.get_value(), Q["per_rpm"] * lf.get_value()), color=PROFIT,
                                             radius=0.08))
        be_line = DashedLine(ax.c2p(be, 0), ax.c2p(be, 26), stroke_color=PRICE, stroke_width=2)
        be_t = tx(f"break-even: {100 * be:.0f}%", 19, PRICE, bold=True).next_to(ax.c2p(be, 26), UP, buff=0.05)
        with self.voiceover(
            "Airlines are the cleanest case of a business that sells capacity. <bookmark mark='a'/> Once a flight "
            "is scheduled, almost all its costs are set: the plane, the crew, the fuel, the landing fee. Delta's "
            f"costs in 2025 came to {Q['casm']:.1f} cents for every seat it flew one mile, full or empty. "
            "<bookmark mark='b'/> Its revenue, spread over the seats that were filled, came to about "
            f"{Q['per_rpm']:.0f} cents a mile, counting everything it earns, from fares to cargo to selling miles. "
            "<bookmark mark='c'/> So board the plane. The first passengers pay for the flight itself. "
            "<bookmark mark='d'/> Only once about three seats in four are full does the flight break even: at "
            f"{100 * be:.0f} percent. <bookmark mark='e'/> Delta filled {100 * Q['load']:.0f} percent of its seats. "
            "The last few passengers on each flight, the green ones, are the whole profit."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(cab), Create(nose))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), Create(cost), FadeIn(cost_t))
            vo.wait_until("b")
            self.play(Create(rev), FadeIn(rev_t), FadeIn(lf_n), FadeIn(lf_t), FadeIn(dot))
            vo.wait_until("c")
            self.play(lf.animate.set_value(0.55), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(lf.animate.set_value(be), run_time=2.0, rate_func=linear)
            self.play(Create(be_line), FadeIn(be_t))
            vo.wait_until("e")
            self.play(lf.animate.set_value(Q["load"]), run_time=1.6, rate_func=linear)
            gap = Polygon(ax.c2p(be, Q["casm"]), ax.c2p(Q["load"], Q["per_rpm"] * Q["load"]), ax.c2p(Q["load"], Q["casm"]),
                          stroke_width=0, fill_color=PROFIT, fill_opacity=0.35)
            self.play(FadeIn(gap))
        count = VGroup(tx(f"of {n} seats: {n_be} pay for the flight", 20, VAR),
                       tx(f"{n_lf - n_be} more make the profit", 20, PROFIT),
                       tx(f"{n - n_lf} fly empty", 20, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(
            [5.0, -0.3, 0])
        per = Q["per_point"]
        pt = VGroup(tx("one point of load factor", 20, GREY_B),
                    tx(f"${per:.2f}bn a year", 34, PRICE, bold=True),
                    tx(f"against an operating profit of ${Q['oi']:.1f}bn", 18, GREY_B)).arrange(DOWN, buff=0.08).move_to(
            [5.0, -2.35, 0])
        with self.voiceover(
            f"On a plane of {n} seats, that is about {n_be} passengers to pay for the flight, {n_lf - n_be} more who "
            f"make the profit, and {n - n_lf} empty seats. <bookmark mark='a'/> Now look at what one more passenger "
            "is worth. Across Delta's whole network, one percentage point of load factor, one more seat in a hundred "
            f"filled, brings in about {per:.2f} billion dollars a year, and costs almost nothing extra to carry: a "
            "meal, a little fuel. <bookmark mark='b'/> Lose eight points, back down to the break-even, and the whole "
            f"year's operating profit of {Q['oi']:.1f} billion is gone. This is a rough sum, since not all of "
            "Delta's revenue comes from its passengers, but it is why airlines fight so hard for the last seat, and "
            "why that seat is sold at almost any price on the morning of the flight."
        ) as vo:
            self.play(FadeIn(count, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(pt, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(lf.animate.set_value(be), run_time=2.5)
            self.play(lf.animate.set_value(Q["load"]), run_time=1.5)
        seats.clear_updaters()
        self.clear_scene()
