from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Order(VoiceoverScene):
    def construct(self):
        card(self, 1, "Run it: the shipowner", "Freight rates are at a record. Do you order a ship?",
             "Chapter one. Run it: the shipowner.", lit=("change",))
        self.choice()
        self.market()

    def choice(self):
        rate = ValueTracker(1.0)
        dial = draw.gauge(rate, 0.5, 2.0, r=1.3, bands=((BUST, 0.25), (ORDER, 0.5), (BOOM, 1.0))).move_to(
            [-4.2, 1.2, 0])
        dl = VGroup(tx("what a ship earns a day", 18, GREY_B),
                    tx("against what it costs to run", 18, GREY_B)).arrange(DOWN, buff=0.04).next_to(dial, DOWN,
                                                                                               buff=0.15)
        num = draw.number(lambda: rate.get_value(), 1, suffix="× its cost", size=30, color=WHITE)
        num.add_updater(lambda g: g.next_to(dl, DOWN, buff=0.15))
        boat = draw.ship(2.4).move_to([-4.2, -2.6, 0])
        yard = VGroup(draw.crane(2.0), draw.crane(1.6).shift(RIGHT * 1.7)).move_to([3.6, 0.9, 0])
        hull = Polygon([-1.1, 0.25, 0], [1.1, 0.25, 0], [0.95, 0, 0], [-1.0, 0, 0], stroke_color="#C0392B",
                       stroke_width=2, fill_opacity=0).move_to([3.6, -0.15, 0])
        quote = VGroup(tx("a new ship", 22, WHITE, bold=True), tx("delivered in three years", 20, ORDER),
                       tx("paid for as it is built", 16, GREY_B)).arrange(DOWN, buff=0.08).next_to(hull, DOWN, buff=0.3)
        rivals = VGroup(*[draw.person(0.5, color=STONE) for _ in range(10)]).arrange(RIGHT, buff=0.2).move_to(
            [2.0, -2.9, 0])
        you = rivals[0].copy().set_color(GOLD)
        rivals[0].become(you)
        rl = tx("you, and nine owners who see the same rate", 17, GREY_B).next_to(rivals, UP, buff=0.15)
        tag = estimate_tag("a model market: this film's illustration", corner=DR)
        with self.voiceover(
            "Play it yourself. You own a ship, and freight rates are the highest anyone can remember. <bookmark "
            "mark='a'/> Every day your ship earns half as much again as it costs to run. <bookmark mark='b'/> A shipyard in "
            "Korea offers you a new one. You pay as it is built, and it will be delivered in three years. "
            "<bookmark mark='c'/> Do you order it? Think about what you know. Today there are not enough ships, "
            "which is why the rate is so high. Trade is growing, a few percent a year. <bookmark mark='d'/> But "
            "you are not the only owner who can see the rate. Every owner sees it, every owner gets the same "
            "offer, and none of them can see what the others have ordered until the ships turn up. Make your "
            "choice, and then watch what a whole market of owners like you does."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(boat, shift=RIGHT * 0.3), FadeIn(dial), FadeIn(dl), FadeIn(num))
            vo.wait_until("a")
            self.play(rate.animate.set_value(1.5), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_, shift=DOWN * 0.3) for c_ in yard], lag_ratio=0.3), Create(hull),
                      FadeIn(quote))
            vo.wait_until("c")
            self.play(Indicate(quote[1], color=ORDER))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.2) for p_ in rivals], lag_ratio=0.08), FadeIn(rl),
                      run_time=1.6)
            self.play(LaggedStart(*[Indicate(p_, color=ORDER) for p_ in rivals], lag_ratio=0.06), run_time=1.6)
        num.clear_updaters()
        self.clear_scene()

    def market(self):
        F = R["fleet"]["run"]
        n = len(F["rate"])
        yrs = list(range(n))
        pa = viz.plot_axes([0, n - 1], [0.5, 1.7], x_length=9.6, y_length=2.5, yticks=[1.0, 1.5],
                           yfmt=lambda v: f"{v:g}×", size=15)
        pa.move_to([0.4, 1.55, 0])
        pb = viz.plot_axes([0, n - 1], [0, 0.6], x_length=9.6, y_length=1.8, yticks=[0.25, 0.5],
                           yfmt=lambda v: f"{100 * v:.0f}%", size=15)
        pb.move_to([0.4, -1.75, 0])
        ta = tx("the rate, against the cost of running a ship", 17, PRICE).next_to(pa, UP, buff=0.12).align_to(pa, LEFT)
        tb = tx("ships on order, as a share of the fleet", 17, ORDER).next_to(pb, UP, buff=0.12).align_to(pb, LEFT)
        cost = DashedLine(pa.ax.c2p(0, 1.0), pa.ax.c2p(n - 1, 1.0), stroke_color=GREY_B, stroke_width=1.5)
        t = ValueTracker(0)

        def rate_line():
            k = max(2, int(t.get_value()) + 1)
            return VMobject(stroke_color=PRICE, stroke_width=4).set_points_as_corners(
                [pa.ax.c2p(i, F["rate"][i]) for i in range(min(k, n))])

        def book_bars():
            k = int(t.get_value()) + 1
            g = VGroup()
            for i in range(min(k, n)):
                v = F["orderbook"][i]
                p0, p1 = pb.ax.c2p(i, 0), pb.ax.c2p(i, v)
                h = max(p1[1] - p0[1], 0.005)
                g.add(Rectangle(width=0.16, height=h, stroke_width=0, fill_color=ORDER, fill_opacity=0.85).move_to(
                    [p0[0], p0[1] + h / 2, 0]))
            return g
        line = always_redraw(rate_line)
        bars = always_redraw(book_bars)
        dem = tx("demand for ships: up 3% every year, never down", 17, BOOM).to_corner(DL, buff=0.35)
        # moments to point at: the first big peak of orders and the trough that follows its deliveries
        ob = F["orderbook"]
        i_pk = int(np.argmax(ob[:30]))
        i_lo = i_pk + int(np.argmin(F["rate"][i_pk:i_pk + 8]))
        tag = estimate_tag("the Works' fleet model: owners order when the rate is above cost; ships arrive in 3 years",
                           corner=DR, size=13)
        with self.voiceover(
            "Here is a market of owners like you, in this series' model. <bookmark mark='a'/> Each year, every "
            "owner looks at today's rate. The further it is above the cost of running a ship, the more ships they "
            "order. The ships arrive three years later. Demand grows three percent every year, steadily, and never "
            "falls. <bookmark mark='b'/> Watch. The rate rises. Orders pile up. For three years nothing arrives, so "
            "the rate stays high, and owners keep ordering. <bookmark mark='c'/> Then the ships come, all of them, "
            "and the rate falls below the cost of running a ship. Nobody orders. <bookmark mark='d'/> Three years "
            "later, with nothing new arriving and trade still growing, there are too few ships again, and the "
            "whole thing starts over. <bookmark mark='e'/> Nothing in this market ever went wrong. Demand rose "
            "smoothly. Every owner made a sensible decision with what they could see. The cycle comes from two "
            "things only: the wait between ordering a ship and sailing it, and owners who look at today's price."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(pa), FadeIn(pb), FadeIn(ta), FadeIn(tb), Create(cost))
            self.add(line, bars)
            vo.wait_until("a")
            self.play(FadeIn(dem, shift=UP * 0.1), t.animate.set_value(3), run_time=1.6, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(i_pk), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(i_lo), run_time=3.0, rate_func=linear)
            lo = glow_dot(pa.ax.c2p(i_lo, F["rate"][i_lo]), color=BUST, radius=0.1)
            self.play(FadeIn(lo, scale=2))
            vo.wait_until("d")
            self.play(t.animate.set_value(n - 1), run_time=7.0, rate_func=linear)
            vo.wait_until("e")
            self.play(Indicate(dem, color=WHITE))
        line.clear_updaters()
        bars.clear_updaters()
        self.clear_scene()
