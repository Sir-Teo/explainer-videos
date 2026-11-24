from __future__ import annotations

from explainer.industry.works import cycle
from videos.industry.industry6.common import *  # noqa: F403

A_, B_, C_ = 10.0, 1.0, 0.0  # demand p = 10 - q; supply q = d * p


class Cobweb(VoiceoverScene):
    def construct(self):
        card(self, 2, "The cobweb", "What happens when this year's price decides next year's supply?",
             "Chapter two. The cobweb.", lit=("change",))
        self.web()

    def web(self):
        ax = CornerAxes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=5.6, y_length=5.6,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([-2.6, -0.35, 0])
        xl = tx("hogs brought to market", 17, GREY_B).next_to(ax, DOWN, buff=0.15)
        yl = tx("price", 17, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        dem = ax.plot(lambda q: A_ - B_ * q, x_range=[0, 10], color=CAP, stroke_width=4)
        dem_t = tx("demand: what buyers pay", 16, CAP).next_to(ax.c2p(8.6, 1.4), UP, buff=0.1)

        def supply(d):
            return ax.plot(lambda q: q / d, x_range=[0, min(10, 10 * d)], color=PRICE, stroke_width=4)
        sup = supply(0.8)
        sup_t = tx("supply: what farmers raise\nat last year's price", 16, PRICE).next_to(ax.c2p(7.6, 9.5), RIGHT,
                                                                                      buff=0.05)
        pe, qe = cycle.cobweb_eq(A_, B_, C_, 0.8)
        p, q = cycle.cobweb(A_, B_, C_, 0.8, pe + 2.6, n=8)
        # the farm: pigs that come and go with each year's quantity
        sty = VGroup(*[draw.pig(0.42, color=HOG) for _ in range(10)]).arrange_in_grid(rows=2, cols=5, buff=(0.12, 0.1))
        sty.move_to([4.3, -1.6, 0])
        price_tag = VGroup(RoundedRectangle(corner_radius=0.08, width=1.9, height=0.7, stroke_color=ORDER,
                                            stroke_width=2, fill_color="#2A2410", fill_opacity=1))
        price_tag.move_to([4.3, 1.4, 0])
        pt = ValueTracker(p[0])
        pnum = draw.number(lambda: pt.get_value(), 2, prefix="$", size=30, color=ORDER)
        pnum.add_updater(lambda g: g.move_to(price_tag))
        yr = ValueTracker(0)
        ylab = draw.number(lambda: yr.get_value(), 0, prefix="year ", size=22, color=GREY_B, commas=False)
        ylab.add_updater(lambda g: g.next_to(price_tag, UP, buff=0.2))
        paper = VGroup(RoundedRectangle(corner_radius=0.06, width=3.4, height=1.9, stroke_width=0, fill_color="#E8E4DA",
                                        fill_opacity=1),
                       tx("The Cobweb Theorem", 22, "#1B1F27", bold=True).shift(UP * 0.45),
                       tx("Mordecai Ezekiel", 17, "#1B1F27").shift(UP * 0.05),
                       tx("Quarterly Journal of Economics", 15, "#4A4F5A").shift(DOWN * 0.35),
                       tx("February 1938", 15, "#4A4F5A").shift(DOWN * 0.65)).move_to([4.3, 1.5, 0])
        src = source("Ezekiel, 'The Cobweb Theorem', Quarterly Journal of Economics 52(2), 1938; the curves are "
                     "illustrative", size=13)
        dot = glow_dot(ax.c2p(0, p[0]), color=ORDER, radius=0.1)

        def show(k):
            return VGroup(*[s_.copy().set_opacity(1.0 if i < round(q[k]) else 0.12) for i, s_ in enumerate(sty)])
        with self.voiceover(
            "In 1938 Mordecai Ezekiel, an economist advising the American Secretary of Agriculture, gave this a "
            "name. <bookmark mark='a'/> Think of hog farmers. From breeding a sow to selling the pigs takes about a "
            "year, so a farmer has to decide how many pigs to raise by looking at today's price. "
            "<bookmark mark='b'/> Here is the market. The blue line is demand: the lower the price, the more pork "
            "people buy. <bookmark mark='c'/> The orange line is supply: the higher last year's price, the more pigs "
            "farmers raise. <bookmark mark='d'/> Start with a high price. Farmers see it and raise a lot of pigs. "
            "<bookmark mark='e'/> A year later the pigs arrive, all of them, and to sell them all the price has to "
            "fall, down to the demand line. <bookmark mark='f'/> Now the price is low, so farmers raise few pigs. "
            "<bookmark mark='g'/> The next year pork is scarce, and the price jumps. <bookmark mark='h'/> Round "
            "and round, the path draws a cobweb. Here it spirals in, toward the price where the two lines cross, "
            "because farmers respond to price less strongly than buyers do: each year's surprise is a little smaller "
            "than the last, and the market settles."
        ) as vo:
            self.play(FadeIn(src), FadeIn(paper, shift=UP * 0.2),
                      LaggedStart(*[FadeIn(s_, shift=UP * 0.1) for s_ in sty], lag_ratio=0.08), run_time=1.8)
            vo.wait_until("a")
            self.play(Indicate(sty, color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(FadeOut(paper), Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(dem), FadeIn(dem_t))
            vo.wait_until("c")
            self.play(Create(sup), FadeIn(sup_t))
            vo.wait_until("d")
            self.play(FadeIn(price_tag), FadeIn(pnum), FadeIn(ylab), FadeIn(dot, scale=2))
            # the path: horizontal to supply (farmers plan), then vertical to demand (the market clears)
            trail = VGroup()
            # step k: farmers plan (across to supply), then the market clears (down or up to demand)
            cues = {0: (None, "e"), 1: ("f", "g")}
            for k in range(6):
                a_ = ax.c2p(0 if k == 0 else q[k - 1], p[k])
                b_ = ax.c2p(q[k], p[k])
                c_ = ax.c2p(q[k], p[k + 1])
                h = Line(a_, b_, stroke_color=ORDER, stroke_width=3)
                v = Line(b_, c_, stroke_color=ORDER, stroke_width=3)
                if k in cues:
                    m1, m2 = cues[k]
                    if m1:
                        vo.wait_until(m1)
                    self.play(Create(h), dot.animate.move_to(b_), Transform(sty, show(k)), run_time=1.2)
                    vo.wait_until(m2)
                    self.play(Create(v), dot.animate.move_to(c_), pt.animate.set_value(p[k + 1]),
                              yr.animate.set_value(k + 1), run_time=1.2)
                else:
                    if k == 2:
                        vo.wait_until("h")
                    self.play(Create(h), Create(v), dot.animate.move_to(c_), Transform(sty, show(k)),
                              pt.animate.set_value(p[k + 1]), yr.animate.set_value(k + 1), run_time=0.9)
                trail.add(h, v)
            self.play(Flash(ax.c2p(qe, pe), color=WHITE, line_length=0.2))
        self.explode(ax, dem, sup, trail, dot, sty, pnum, ylab, price_tag, pt, yr, sup_t)

    def explode(self, ax, dem, sup, trail, dot, sty, pnum, ylab, price_tag, pt, yr, sup_t):
        d = 1.25
        pe, qe = cycle.cobweb_eq(A_, B_, C_, d)
        p, q = cycle.cobweb(A_, B_, C_, d, pe + 0.6, n=6)
        sup2 = ax.plot(lambda x: x / d, x_range=[0, 10], color=BUST, stroke_width=4)
        sup2_t = tx("farmers who respond more strongly", 16, BUST).next_to(ax.c2p(9.6, 7.7), UP, buff=0.05).shift(
            LEFT * 0.3)
        two = VGroup(tx("the simple cobweb's prediction:", 19, GREY_A),
                     tx("high, low, high, low:", 22, WHITE, bold=True),
                     tx("a full cycle every two years", 22, ORDER, bold=True)).arrange(DOWN, buff=0.1).move_to(
            [4.3, 1.2, 0])
        flips = VGroup(*[Rectangle(width=0.36, height=0.9 if k % 2 == 0 else 0.35, stroke_width=0,
                                   fill_color=BOOM if k % 2 == 0 else BUST, fill_opacity=0.85) for k in range(6)]
                       ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN).move_to([4.3, -0.3, 0])
        fl = tx("price, year by year", 15, GREY_B).next_to(flips, DOWN, buff=0.1)
        with self.voiceover(
            "If farmers respond more strongly than buyers, the same rules draw a cobweb that spirals out. "
            "<bookmark mark='a'/> Each year's swing is bigger than the last, until something breaks: farmers go "
            "out of business, or learn to look further ahead. <bookmark mark='b'/> Notice one more thing the model "
            "predicts. If a pig takes a year, the price flips every year: high, low, high, low. A full cycle every "
            "two years. Hold on to that prediction: the next chapter tests it."
        ) as vo:
            self.play(FadeOut(trail), FadeOut(sty), FadeOut(sup_t), FadeOut(VGroup(pnum, ylab, price_tag)),
                      ReplacementTransform(sup, sup2), FadeIn(sup2_t), dot.animate.move_to(ax.c2p(0, p[0])))
            pnum.clear_updaters()
            ylab.clear_updaters()
            vo.wait_until("a")
            for k in range(5):
                a_ = ax.c2p(0 if k == 0 else q[k - 1], p[k])
                b_ = ax.c2p(min(q[k], 9.9), p[k])
                c_ = ax.c2p(min(q[k], 9.9), max(p[k + 1], 0.1))
                self.play(Create(Line(a_, b_, stroke_color=BUST, stroke_width=3)),
                          Create(Line(b_, c_, stroke_color=BUST, stroke_width=3)), dot.animate.move_to(c_),
                          run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(two, shift=UP * 0.1))
            self.play(LaggedStart(*[GrowFromEdge(f_, DOWN) for f_ in flips], lag_ratio=0.25), FadeIn(fl),
                      run_time=1.8)
        self.clear_scene()
