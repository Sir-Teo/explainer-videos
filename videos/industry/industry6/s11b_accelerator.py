from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry6.common import *  # noqa: F403

# a bakery chain's demand for bread, year by year (thousands of loaves a day), the ovens it needs (one oven bakes a
# thousand a day) and the ovens it orders: replacements for the tenth that wear out each year, plus any growth
DEMAND = [100, 100, 110, 121, 121, 115, 115, 121]


def orders(demand, life=10):
    out = []
    for k, d in enumerate(demand):
        prev = demand[k - 1] if k else d
        out.append(max(prev / life + (d - prev), 0.0))
    return out


class Accelerator(VoiceoverScene):
    def construct(self):
        card(self, 10, "The accelerator", "Why do the makers of machines feel the cycle hardest?",
             "Chapter ten. The accelerator.", lit=("change", "make"))
        od = orders(DEMAND)
        n = len(DEMAND)
        bake = VGroup(*[draw.shop(0.55, color=PRICE) for _ in range(6)]).arrange(RIGHT, buff=0.12).move_to([-4.0, 2.6, 0])
        bl = tx("a chain of bakeries", 17, PRICE).next_to(bake, DOWN, buff=0.1)
        ovens = VGroup(*[draw.factory(0.7, color="#8C929B") for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to(
            [3.6, 2.6, 0])
        ol = tx("the company that makes its ovens", 17, GREY_A).next_to(ovens, DOWN, buff=0.1)
        arrow = Arrow(bake.get_right(), ovens.get_left(), buff=0.3, color=GREY_B, stroke_width=3)
        pa = viz.plot_axes([-0.5, n - 0.5], [0, 130], x_length=5.4, y_length=2.6, yticks=[50, 100], size=14)
        pa.move_to([-3.4, -1.3, 0])
        pb = viz.plot_axes([-0.5, n - 0.5], [0, 24], x_length=5.4, y_length=2.6, yticks=[10, 20], size=14)
        pb.move_to([3.6, -1.3, 0])
        ta = tx("bread sold, thousands of loaves a day", 16, PRICE).next_to(pa, UP, buff=0.1).align_to(pa, LEFT)
        tb = tx("new ovens ordered that year", 16, ORDER).next_to(pb, UP, buff=0.1).align_to(pb, LEFT)
        da = viz.year_bars(pa, list(range(n)), DEMAND, PRICE, width=0.42)
        db = viz.year_bars(pb, list(range(n)), od, ORDER, width=0.42)
        yrs = VGroup(*[tx(f"year {k + 1}", 12, GREY_B).next_to(pa.ax.c2p(k, 0), DOWN, buff=0.08) for k in range(n)],
                     *[tx(f"year {k + 1}", 12, GREY_B).next_to(pb.ax.c2p(k, 0), DOWN, buff=0.08) for k in range(n)])
        nums = VGroup(*[tx(f"{v:.0f}", 14, WHITE).next_to(b_, UP, buff=0.04) for b_, v in zip(db, od)])
        tag = estimate_tag("a model: ovens last ten years; one oven bakes a thousand loaves a day", corner=DR, size=13)
        paper = tx(f"J. Maurice Clark, 'Business Acceleration and the Law of Demand', {get('clark.1917'):.0f}", 15,
                   GREY_B).to_corner(DL, buff=0.28)
        with self.voiceover(
            "There is a second way a small wobble becomes a big swing, and it hits the companies that make the "
            "machines. <bookmark mark='a'/> Take a chain of bakeries that sells a hundred thousand loaves a day. "
            "Each oven bakes a thousand, so it needs a hundred ovens. Ovens last ten years, so each year it buys ten "
            "new ones to replace those that wear out. <bookmark mark='b'/> The oven maker sells ten ovens a year. "
            "<bookmark mark='c'/> Now bread sales grow by a tenth. The chain needs ten more ovens, on top of the ten "
            "replacements. The oven maker's orders double, to twenty, while bread grew by only ten percent. "
            "<bookmark mark='d'/> Next year sales grow another tenth. Orders stay high. <bookmark mark='e'/> Then "
            "sales stop growing. They do not fall: the bakeries sell more bread than ever. But they need no new "
            "ovens, only replacements, and the oven maker's orders fall by almost half. <bookmark mark='f'/> Let "
            "sales slip by five percent, and the chain replaces only some of its worn ovens: orders fall to about "
            "six, barely a quarter of their peak. <bookmark mark='g'/> The economist John Maurice Clark described this "
            "in 1917, and called it the acceleration principle. The makers of machines, ships and factories sell "
            "not to the level of demand, but to its growth. A slowdown that a shopper would barely notice can halve "
            "their business."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bake], lag_ratio=0.1),
                      FadeIn(bl), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(ta), FadeIn(yrs[:n]), GrowFromEdge(da[0], DOWN))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(ovens, shift=LEFT * 0.2), FadeIn(ol))
            self.play(FadeIn(pb), FadeIn(tb), FadeIn(yrs[n:]), GrowFromEdge(db[0], DOWN), FadeIn(nums[0]))
            self.play(GrowFromEdge(da[1], DOWN), GrowFromEdge(db[1], DOWN), FadeIn(nums[1]))
            for k, m in ((2, "c"), (3, "d"), (4, "e"), (5, "f")):
                vo.wait_until(m)
                self.play(GrowFromEdge(da[k], DOWN), GrowFromEdge(db[k], DOWN), FadeIn(nums[k]), run_time=1.2)
                if k == 2:
                    self.play(Indicate(db[2], color=WHITE, scale_factor=1.1))
                if k == 5:
                    self.play(Indicate(db[5], color=BUST, scale_factor=1.3))
            vo.wait_until("g")
            self.play(FadeIn(paper), *[GrowFromEdge(b_, DOWN) for b_ in (da[6], da[7], db[6], db[7])],
                      FadeIn(nums[6:]))
        self.clear_scene()
