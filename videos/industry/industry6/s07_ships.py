from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry6.common import *  # noqa: F403


class Ships(VoiceoverScene):
    def construct(self):
        card(self, 6, "Ships", "How big does the wave of new ships get?",
             "Chapter six. Ships.", lit=("change",))
        self.orderbook()
        self.boxes()

    def orderbook(self):
        S = R["ships"]
        book = S["book"]
        yrs = sorted(book)
        fleet = VGroup(*[draw.ship(1.05) for _ in range(10)]).arrange_in_grid(rows=2, cols=5, buff=(0.15, 0.3))
        fleet.move_to([-3.7, 2.2, 0])
        fl = tx("the world's fleet", 18, GREY_A).next_to(fleet, DOWN, buff=0.15)
        # the orderbook as ghost ships: the share of the fleet already ordered and not yet delivered
        pa = viz.plot_axes([2007.5, 2025.8], [0, 0.6], x_length=7.2, y_length=3.0, yticks=[0.25, 0.5],
                           yfmt=lambda v: f"{100 * v:.0f}%", size=15)
        pa.move_to([2.4, -1.4, 0])
        bars = VGroup()
        for y in yrs:
            p0, p1 = pa.ax.c2p(y, 0), pa.ax.c2p(y, book[y])
            b = Rectangle(width=0.55, height=p1[1] - p0[1], stroke_width=0, fill_color=ORDER, fill_opacity=0.9)
            b.move_to([p0[0], p0[1] + b.height / 2, 0])
            bars.add(VGroup(b, tx(f"{100 * book[y]:.0f}%", 16, WHITE).next_to(b, UP, buff=0.05),
                            tx(str(y), 15, GREY_B).next_to(b, DOWN, buff=0.08)))
        pt = tx("ships on order, as a share of the ships already sailing", 17, ORDER).next_to(pa, UP, buff=0.12).align_to(
            pa, LEFT)
        ghosts = VGroup(*[draw.ship(1.05).set_opacity(0.35) for _ in range(5)]).arrange(RIGHT, buff=0.15).next_to(
            fleet, RIGHT, buff=0.5).align_to(fleet, UP)
        bulk = VGroup(tx("bulk carriers, 2009:", 18, GREY_A), tx(f"{100 * S['bulk2009']:.0f}% of their fleet on order",
                                                                  24, BUST, bold=True)).arrange(DOWN, buff=0.06)
        bulk.move_to([-4.0, -1.6, 0])
        src = source("UNCTAD, Review of Maritime Transport 2024 and 2025 (from Clarksons Research)", size=13)
        lng = VGroup(tx("LNG carriers, early 2025:", 18, GREY_A),
                     tx(f"{100 * get('ships.book.lng.2025'):.0f}% of their fleet on order", 24, ORDER, bold=True)
                     ).arrange(DOWN, buff=0.06).move_to([-4.0, -2.8, 0])
        with self.voiceover(
            "Shipping keeps the best record of the wave. <bookmark mark='a'/> Every ship in the world is "
            "registered, and so is every ship on order. So you can ask: for every ship sailing today, how many more "
            "have been ordered and not yet delivered? <bookmark mark='b'/> In 2009, after the boom of the mid "
            f"2000s, the answer was {100 * book[2009]:.0f} percent, according to the United Nations' trade agency. "
            "For every two ships at sea, another one was coming. <bookmark mark='c'/> For the ships that carry coal, "
            f"ore and grain, it was {100 * S['bulk2009']:.0f} percent. Those ships had been ordered when freight "
            "rates were at records, in 2007 and 2008. They were delivered into the slump of 2009, when world trade "
            "shrank. <bookmark mark='d'/> By 2014 the ratio was down to nineteen percent; by the start of 2023, "
            f"{100 * book[2023]:.0f}. <bookmark mark='e'/> The industry had been burned, and ordered less. "
            f"By early 2025, it was climbing again: {100 * book[2025]:.0f} percent. <bookmark mark='f'/> And the "
            "average hides the hot spots. For the tankers that carry liquefied natural gas, "
            f"the ships on order equalled {100 * get('ships.book.lng.2025'):.0f} "
            "percent of the fleet: one new ship for every two already sailing."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.2) for s_ in fleet], lag_ratio=0.06),
                      FadeIn(fl), run_time=1.8)
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(pt))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(g_, shift=LEFT * 0.2) for g_ in ghosts], lag_ratio=0.15),
                      GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(bulk, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), FadeOut(ghosts[2:]))
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), FadeOut(ghosts[1]))
            vo.wait_until("e")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1:])) for b in bars[3:]],
                                  lag_ratio=0.4), FadeIn(ghosts[1]), run_time=1.6)
            vo.wait_until("f")
            self.play(FadeIn(lng, shift=UP * 0.1))
        self.clear_scene()

    def boxes(self):
        S, K = R["ships"], R["maersk"]
        pa = viz.plot_axes([2018.4, 2025.6], [0, 32], x_length=7.6, y_length=3.4, xticks=K["years"], yticks=[10, 20, 30],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pa.move_to([-2.2, -0.9, 0])
        bars = viz.year_bars(pa, K["years"], K["ebit"], BOOM, width=0.6)
        for b_, v in zip(bars, K["ebit"]):
            b_.set_fill(BOOM if v > 10 else (ORDER if v > 5 else BUST))
        head = tx("Maersk's operating profit", 20, GREY_A).next_to(pa, UP, buff=0.12).align_to(pa, LEFT)
        boxes = VGroup(*[Rectangle(width=0.5, height=0.26, stroke_color="#0E1117", stroke_width=1,
                                   fill_color=c, fill_opacity=0.95)
                         for c in ("#7EC8F5", "#F2A65A", "#7BD88F", "#F2C14E", "#B58CFF", "#E8554E") * 4])
        boxes.arrange_in_grid(rows=4, cols=6, buff=0.02).move_to([4.6, 1.6, 0])
        box_t = VGroup(tx("container ships on order,", 17, GREY_A), tx("early 2025:", 17, GREY_A),
                       tx(f"{100 * S['box2025']:.0f}% of the fleet", 26, ORDER, bold=True)).arrange(DOWN, buff=0.06)
        box_t.next_to(boxes, DOWN, buff=0.25)
        dl = VGroup(tx("of all new ship tonnage", 17, GREY_A), tx("delivered in 2024,", 17, GREY_A),
                    tx(f"{100 * S['box_delivered2024']:.0f}% was container ships", 22, CAP, bold=True)).arrange(
            DOWN, buff=0.06).move_to([4.6, -2.3, 0])
        src = source("Maersk annual reports (ESEF); UNCTAD, Review of Maritime Transport 2024 and 2025", size=13)
        i22 = K["years"].index(2022)
        with self.voiceover(
            "Container shipping has just been round the loop. <bookmark mark='a'/> When the pandemic jammed the "
            "world's ports, every box was booked and freight rates exploded. Maersk's operating profit went from "
            f"under two billion dollars to {K['ebit'][i22]:.0f} billion in three years. <bookmark mark='b'/> And the "
            "shipowners did what the model says: they ordered. In early 2025, ships equal to a quarter of the "
            "whole container fleet were on order. <bookmark mark='c'/> In 2024, container ships made up "
            f"{100 * S['box_delivered2024']:.0f} percent of all the new ship tonnage delivered in the world. "
            "<bookmark mark='d'/> Profits fell anyway. For a while, attacks on ships in the Red Sea, which sent "
            "them the long way round Africa, used up some of the new capacity. Take that away, and the wave of new "
            "ships is still out there."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(head))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:2]], lag_ratio=0.3))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[2:4]], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=DOWN * 0.2) for b_ in boxes], lag_ratio=0.03), FadeIn(box_t),
                      run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(dl, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[4:]], lag_ratio=0.3), run_time=1.6)
            self.play(Indicate(bars[4:], color=BUST, scale_factor=1.04))
        self.clear_scene()
