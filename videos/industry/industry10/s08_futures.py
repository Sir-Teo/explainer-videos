from __future__ import annotations

from videos.industry.industry10.common import *  # noqa: F403


class Futures(VoiceoverScene):
    def construct(self):
        card(self, 7, "Selling a crop before it grows", "How does a farmer lock in a price, and who takes the other side?",
             "Chapter seven. Selling a crop before it grows.", lit=("dollar", "change"))
        self.contract()
        self.history()

    def contract(self):
        n = get("cme.corn.contract")
        S = R["run"]["seasons"][1]  # 2014: the price fell
        y = S["year"]
        bu = dict(zip(R["futures"]["months"], R["futures"]["bu"]))
        ms = [f"{y}-{m:02d}" for m in range(4, 11)]
        scale = S["harvest"] / bu[f"{y}-10"]
        path = [bu[m] * scale for m in ms]
        card_ = VGroup(RoundedRectangle(corner_radius=0.12, width=4.4, height=2.0, stroke_color=PRICE, stroke_width=2,
                                        fill_color="#141A24", fill_opacity=1),
                       VGroup(tx("A corn futures contract", 20, PRICE, bold=True),
                              tx(f"{n:,.0f} bushels, delivered in December", 16, WHITE),
                              tx(f"at the price agreed in April: ${S['plant']:.2f}", 16, WHITE),
                              tx("traded in Chicago, settled every day", 14, GREY_A)).arrange(DOWN, buff=0.08)
                       ).move_to([-3.6, 2.0, 0])
        card_[1].move_to(card_[0])
        farmer = VGroup(draw.tractor(0.9), tx("the farmer sells", 15, CORN, bold=True)).arrange(DOWN, buff=0.08).move_to(
            [-5.6, -0.5, 0])
        buyer = VGroup(draw.factory(1.0).scale(0.8), tx("a feed mill, an ethanol plant,", 13, GREY_A),
                       tx("or a speculator buys", 15, TRADE, bold=True)).arrange(DOWN, buff=0.06).move_to([-1.6, -0.5, 0])
        arr = DoubleArrow(farmer.get_right(), buyer.get_left(), buff=0.15, stroke_width=2.5, color=GREY_B, tip_length=0.14)
        pa = viz.plot_axes([0, len(ms) - 1], [2.5, 5.5], x_length=5.2, y_length=2.8, xticks=[0, 6],
                           yticks=[3, 4, 5], xfmt=lambda v: {0: "April", 6: "October"}[int(v)], yfmt=lambda v: f"${v:g}",
                           size=13).move_to([3.6, 1.4, 0])
        pl = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners([pa.ax.c2p(i, v) for i, v in enumerate(path)])
        pt = tx(f"the price of a bushel, {y}", 15, GREY_A).next_to(pa, UP, buff=0.08)
        loss = S["plant"] - S["harvest"]
        ledger = VGroup(tx(f"At harvest the farmer sells the crop at ${S['harvest']:.2f}", 16, WHITE),
                        tx(f"and gains ${loss:.2f} a bushel on the contract", 16, GREEN_C),
                        tx(f"= ${S['plant']:.2f} a bushel, the price locked in April", 18, PRICE, bold=True)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).move_to([3.4, -1.3, 0])
        basis = tx("(less the 'basis': the local price's gap to Chicago, which still moves)", 13, GREY_B).next_to(ledger, DOWN,
                                                                                                             buff=0.12)
        src = source("CME Group, corn futures specifications; USDA ERS (harvest price) and IMF maize (path), 2014", size=13)
        with self.voiceover(
            "In the game, selling ahead meant a forward contract. The tool behind it is the futures market. "
            "<bookmark mark='a'/> A corn futures contract, traded in Chicago, is a promise to deliver "
            f"{n:,.0f} bushels in a given month, December say, at a price agreed today. <bookmark mark='b'/> In the "
            "spring the farmer sells contracts covering part of the crop. On the other side is someone who wants corn "
            "later at a known price, a feed mill or an ethanol plant, or a speculator who simply thinks the price will "
            "rise. <bookmark mark='c'/> Now the price falls through the summer, as it did in 2014. "
            "<bookmark mark='d'/> At harvest the farmer sells the real corn locally at the low price, and closes the "
            "contract with a gain of almost the same amount. The two cancel, and the farmer ends up with roughly the "
            "spring price. Gains and losses on the contract are paid every day, through the exchange, so neither side "
            "can walk away. What the farmer cannot remove is the gap between the local price and Chicago's, and the "
            "risk of having less corn than expected."
        ) as vo:
            self.play(FadeIn(src), FadeIn(farmer, shift=RIGHT * 0.2), FadeIn(buyer, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(card_, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(GrowFromCenter(arr), Indicate(farmer[1], color=CORN), Indicate(buyer[2], color=TRADE))
            vo.wait_until("c")
            self.play(FadeIn(pa), FadeIn(pt))
            self.play(Create(pl), run_time=3.0, rate_func=linear)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in ledger], lag_ratio=0.4), run_time=2.0)
            self.play(FadeIn(basis))
        self.clear_scene()

    def history(self):
        F = R["futures"]
        ms, bu = F["months"], F["bu"]
        xs = [mx(m) for m in ms]
        pa = viz.plot_axes([1992, 2027], [0, 9], x_length=10.8, y_length=4.6, xticks=[1995, 2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[2, 4, 6, 8], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=15).move_to([0.2, -0.4, 0])
        t = ValueTracker(xs[0])

        def line():
            q = [pa.ax.c2p(x, v) for x, v in zip(xs, bu) if x <= t.get_value()]
            return VMobject(stroke_color=CORN, stroke_width=3).set_points_as_corners(q) if len(q) > 1 else VMobject()
        ln = always_redraw(line)
        eps = [(2007.0, "US biofuel mandate"), (2012.6, "the 2012 drought"), (2014.8, "record crops"),
               (2020.4, "the pandemic"), (2022.3, "the invasion of Ukraine")]
        marks = VGroup()
        for x, name in eps:
            v = max(b for xx, b in zip(xs, bu) if abs(xx - x) < 0.5)
            p = pa.ax.c2p(x, v)
            marks.add(VGroup(Dot(p, radius=0.05, color=WHITE), tx(name, 14, WHITE).next_to(p, UP, buff=0.12)))
        marks[2][1].next_to(marks[2][0], DOWN, buff=0.12)
        marks[3][1].next_to(marks[3][0], DOWN, buff=0.12)
        head = tx("Corn, dollars a bushel, month by month (world price)", 22, WHITE, bold=True).to_edge(UP, buff=0.35)
        src = source("IMF maize price (US Gulf) via FRED, converted at 39.37 bushels a tonne", size=13)
        with self.voiceover(
            "Here is the price that every one of those contracts is betting on, for thirty years. "
            "<bookmark mark='a'/> For a decade it hovered around two to three dollars a bushel. "
            "<bookmark mark='b'/> Then American law began to require ethanol in petrol, and a large share of the corn "
            "crop went to fuel. <bookmark mark='c'/> The drought of 2012 took it to a record. <bookmark mark='d'/> Record "
            "crops brought it back down for years. <bookmark mark='e'/> The pandemic, a Chinese buying spree and the "
            "invasion of Ukraine, one of the world's great grain exporters, sent it up again. Each spike lasted a year or "
            "two, because every farmer on Earth answers a high price the same way: by planting more."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(src))
            self.add(ln)
            for k, (m, x1) in enumerate(zip("abcde", (2006.5, 2009.0, 2013.0, 2019.5, 2026.8))):
                vo.wait_until(m)
                self.play(t.animate.set_value(x1), run_time=3.0, rate_func=linear)
                new = [marks[i] for i, (x, _) in enumerate(eps) if (k == 0 and x <= x1) or
                       (k > 0 and (2006.5, 2009.0, 2013.0, 2019.5, 2026.8)[k - 1] < x <= x1)]
                if new:
                    self.play(*[FadeIn(g) for g in new], run_time=0.6)
        ln.clear_updaters()
        self.clear_scene()
