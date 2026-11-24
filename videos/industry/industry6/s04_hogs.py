from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Hogs(VoiceoverScene):
    def construct(self):
        card(self, 3, "Sixty years of hogs", "Did real hog farmers draw the cobweb?",
             "Chapter three. Sixty years of hogs.", lit=("change",))
        self.levels()
        self.swings()

    def levels(self):
        H = R["hogs"]
        yrs = H["years"]
        pa = viz.plot_axes([1880, 1940], [0, 20], x_length=9.0, y_length=2.3, yticks=[10, 20],
                           yfmt=lambda v: f"${v:g}", size=14)
        pb = viz.plot_axes([1880, 1940], [0, 5], x_length=9.0, y_length=2.3, xticks=[1880, 1900, 1920, 1940],
                           yticks=[2.5, 5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}m", size=14)
        pa.move_to([0.9, 1.55, 0])
        pb.move_to([0.9, -1.75, 0])
        la = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(y, v) for y, v in zip(yrs, H["price"])])
        lb = VMobject(stroke_color=HOG, stroke_width=3).set_points_as_corners(
            [pb.ax.c2p(y, v / 1000) for y, v in zip(yrs, H["slaughter"])])
        ta = tx("price of hogs at Chicago, dollars per hundred pounds", 16, PRICE).next_to(pa, UP, buff=0.1).align_to(
            pa, LEFT)
        tb = tx("hogs slaughtered in the United States, millions a month", 16, HOG).next_to(pb, UP, buff=0.1).align_to(
            pb, LEFT)
        pig = draw.pig(1.3, color=HOG).move_to([-5.6, 1.4, 0])
        # the yards: pens of hogs, and a board where the day's price was chalked
        pens = VGroup()
        for j in range(3):
            pen = VGroup(Rectangle(width=2.6, height=1.1, stroke_color="#8C6B4A", stroke_width=3, fill_opacity=0),
                         VGroup(*[draw.pig(0.5, color=HOG) for _ in range(4)]).arrange(RIGHT, buff=0.08))
            pens.add(pen)
        pens.arrange(RIGHT, buff=0.25).move_to([1.2, 1.2, 0])
        board = VGroup(RoundedRectangle(corner_radius=0.06, width=3.4, height=1.4, stroke_color="#8C6B4A",
                                        stroke_width=3, fill_color="#1F2A22", fill_opacity=1),
                       tx("hogs, today", 18, "#E8E4DA").shift(UP * 0.35),
                       tx("$5.25 per 100 lb", 26, "#E8E4DA", bold=True).shift(DOWN * 0.15)).move_to([1.2, -1.4, 0])
        board_t = tx("illustrative board", 13, GREY_C).next_to(board, DOWN, buff=0.08)
        yards = VGroup(tx("Union Stock Yards", 18, GREY_A, bold=True), tx("Chicago", 15, GREY_B)).arrange(
            DOWN, buff=0.05).next_to(pig, DOWN, buff=0.2)
        src = source("NBER Macrohistory Database via FRED: wholesale price of hogs, Chicago; hogs slaughtered, US "
                     "(annual averages of monthly figures)", size=13)
        with self.voiceover(
            "Ezekiel's model makes a sharp prediction, and America kept the records to test it. "
            "<bookmark mark='a'/> For decades the price of hogs was set at the stock yards of Chicago, and the "
            "National Bureau of Economic Research later gathered the prices, month by month. "
            "<bookmark mark='b'/> Here they are, from 1880 to 1940. <bookmark mark='c'/> And here is how many hogs "
            "were slaughtered across the country, over the same years. Both lines wander: wars, depressions, and a "
            "country growing. <bookmark mark='d'/> But look closely, and both lines are also shaking, with a rhythm "
            "of a few years. That shaking is what we are after."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pig, shift=RIGHT * 0.3), FadeIn(yards),
                      LaggedStart(*[Create(pn[0]) for pn in pens], lag_ratio=0.2), run_time=1.4)
            self.play(LaggedStart(*[FadeIn(pn[1], shift=RIGHT * 0.2) for pn in pens], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("a")
            self.play(FadeIn(board, shift=UP * 0.2), FadeIn(board_t))
            vo.wait_until("b")
            self.play(FadeOut(pens), FadeOut(board), FadeOut(board_t), FadeIn(pa), FadeIn(ta))
            self.play(Create(la), run_time=2.6, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(pb), FadeIn(tb))
            self.play(Create(lb), run_time=2.6, rate_func=linear)
            vo.wait_until("d")
            self.play(Indicate(la, color=WHITE), Indicate(lb, color=WHITE), run_time=1.6)
        self.clear_scene()

    def swings(self):
        H = R["hogs"]
        n = len(H["dev_months"])
        t0 = 1885

        def yr(i):
            return t0 + i / 12
        pa = viz.plot_axes([1885, 1936], [-0.42, 0.42], x_length=11.0, y_length=3.2, xticks=[1890, 1900, 1910, 1920, 1930],
                           xfmt=lambda v: f"{int(v)}", size=14, grid=False)
        pa.move_to([0.3, 0.75, 0])
        zero = DashedLine(pa.ax.c2p(1885, 0), pa.ax.c2p(1936, 0), stroke_color=GREY_C, stroke_width=1)
        lp = VMobject(stroke_color=PRICE, stroke_width=3).set_points_smoothly(
            [pa.ax.c2p(yr(i), H["dev_price"][i]) for i in range(0, n, 3)])
        lq = VMobject(stroke_color=HOG, stroke_width=3).set_points_smoothly(
            [pa.ax.c2p(yr(i), H["dev_slaughter"][i]) for i in range(0, n, 3)])
        key = VGroup(tx("price", 18, PRICE, bold=True), tx("hogs slaughtered", 18, HOG, bold=True)).arrange(
            RIGHT, buff=0.5).next_to(pa, UP, buff=0.1).align_to(pa, LEFT)
        sub = tx("each against its own five-year trend", 15, GREY_B).next_to(key, RIGHT, buff=0.4)
        same, lag, per = H["same"], H["best_lag"], H["period_slaughter"]
        cards = VGroup(
            VGroup(tx("same month", 17, GREY_B), tx(f"{same:+.2f}", 34, BUST, bold=True),
                   tx("more hogs, lower price", 15, GREY_A)).arrange(DOWN, buff=0.06),
            VGroup(tx(f"price, then hogs {lag // 12}½ years later" if lag % 12 else f"price, then hogs {lag // 12} years later",
                      17, GREY_B),
                   tx(f"{H['best']:+.2f}", 34, BOOM, bold=True), tx("a high price brings more hogs", 15, GREY_A)
                   ).arrange(DOWN, buff=0.06),
            VGroup(tx("one full swing of the hogs", 17, GREY_B), tx(f"{per:.1f} years", 34, ORDER, bold=True),
                   tx("the simple cobweb said 2", 15, GREY_A)).arrange(DOWN, buff=0.06)).arrange(RIGHT, buff=1.0)
        cards.move_to([0.3, -2.45, 0])
        src = source("NBER via FRED; this film's arithmetic: 12-month averages, against a 61-month moving average, "
                     "correlations of the two", size=13)
        with self.voiceover(
            "Take away the slow wandering, and keep only the swings around it. <bookmark mark='a'/> In orange, the "
            "hog price above or below its own trend. <bookmark mark='b'/> In pink, the number of hogs slaughtered. "
            "<bookmark mark='c'/> When one is up, the other is usually down: the correlation between them in the "
            f"same month is {same:.2f}. More hogs, lower price, exactly as the demand line says. "
            f"<bookmark mark='d'/> And a high price is followed, about {lag // 12} and a half years later, by more "
            "hogs. Farmers did respond to price, with a delay. <bookmark mark='e'/> But the delay is longer than "
            f"Ezekiel's model allows. One full swing of the hogs took about {per:.1f} years, not two. Part of the "
            "reason is biology: to raise more pigs, a farmer first keeps young sows back from market to breed them, "
            "so a high price cuts the supply of pork before it raises it. Part of it is people: farmers do not all "
            "react at once, and they remember last year as well as this one. Ronald Coase, years before his Nobel "
            "prize, made the same objection about British pigs in 1935. The cobweb is the right shape. The real "
            "wait is just longer than one season."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), Create(zero), FadeIn(key[0]), FadeIn(sub))
            vo.wait_until("a")
            self.play(Create(lp), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(key[1]), Create(lq), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(cards[0], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            self.play(Indicate(cards[1][1], color=BOOM), run_time=1.2)
            vo.wait_until("e")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
            self.play(Indicate(cards[2][1], color=ORDER))
        self.clear_scene()
