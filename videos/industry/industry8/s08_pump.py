from __future__ import annotations

from videos.industry.industry8.common import *  # noqa: F403

PARTS_ = [("crude_pct", "crude oil", CRUDE), ("refining_pct", "refining", COST), ("distribution_pct",
                                                                                  "distribution and the station", GAS),
          ("taxes_pct", "taxes", STATE)]


class Pump(VoiceoverScene):
    def construct(self):
        card(self, 7, "Where a gallon's dollar goes", "When you pay four dollars for a gallon, who gets what?",
             "Chapter seven. Where a gallon's dollar goes.", lit=("dollar",))
        self.gallon()
        self.history()

    def gallon(self):
        P = R["pump"]
        last = P["last"]
        retail = last["retail"]
        H = 4.2
        jug = RoundedRectangle(corner_radius=0.2, width=2.2, height=H + 0.2, stroke_color=STONE, stroke_width=3,
                               fill_opacity=0).move_to([-3.6, -0.4, 0])
        layers = VGroup()
        y = jug.get_bottom()[1] + 0.1
        for k, (key, name, col) in enumerate(PARTS_):
            h = H * last[key] / 100
            r_ = Rectangle(width=2.0, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [jug.get_x(), y + h / 2, 0])
            cents = retail * last[key]
            t = VGroup(tx(f"{cents:.0f} cents", 22, col, bold=True), tx(f"{name}, {last[key]:.0f}%", 16, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.03).move_to([0.4, y + h / 2, 0], aligned_edge=LEFT)
            ln = Line(r_.get_right(), t.get_left() + LEFT * 0.1, stroke_color=GREY_C, stroke_width=1.2)
            layers.add(VGroup(r_, t, ln))
            y += h
        price = tx(f"${retail:.2f} a gallon, {mlabel(last['month'])}", 28, PRICE, bold=True).next_to(jug, UP, buff=0.25)
        pump = VGroup(RoundedRectangle(corner_radius=0.1, width=1.1, height=2.0, stroke_width=0, fill_color="#C0392B",
                                       fill_opacity=0.95),
                      Rectangle(width=0.8, height=0.5, stroke_width=0, fill_color="#0E1117", fill_opacity=1).shift(UP * 0.5),
                      Line([0.55, 0.3, 0], [0.9, -0.4, 0], stroke_color="#2E3645", stroke_width=5)).move_to([5.4, 1.0, 0])
        src = source("US Energy Information Administration, Gasoline Pump Components History (US regular)", size=13)
        with self.voiceover(
            "Follow the money back from the pump. <bookmark mark='a'/> In August 2026, a gallon of regular gasoline "
            f"in America cost {retail:.2f} dollars on average. <bookmark mark='b'/> About half of it, "
            f"{retail * last['crude_pct']:.0f} cents, paid for the crude oil it was made from. <bookmark mark='c'/> "
            f"{retail * last['refining_pct']:.0f} cents went to refining it: the refiners' costs and their margin, "
            "unusually wide that summer. <bookmark mark='d'/> "
            f"{retail * last['distribution_pct']:.0f} cents paid for pipelines, trucks and the filling station. "
            f"<bookmark mark='e'/> And {retail * last['taxes_pct']:.0f} cents were taxes, federal and state, which "
            "are charged in cents a gallon, not as a share of the price."
        ) as vo:
            self.play(FadeIn(src), Create(jug), FadeIn(pump, shift=LEFT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(price))
            for k, m in enumerate("bcde"):
                vo.wait_until(m)
                self.play(GrowFromEdge(layers[k][0], DOWN), Create(layers[k][2]), FadeIn(layers[k][1], shift=LEFT * 0.1))
        self.clear_scene()

    def history(self):
        P = R["pump"]
        ms = P["months"]
        xs = [mx(m) for m in ms]
        retail = np.array(P["retail"])
        cents = {k: retail * np.array(P["shares"][k]) / 100 for k, _, _ in PARTS_}
        pa = viz.plot_axes([2000, 2027], [0, 5], x_length=9.6, y_length=4.4, xticks=[2000, 2005, 2010, 2015, 2020, 2025],
                           yticks=[1, 2, 3, 4, 5], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}", size=14)
        pa.move_to([0.6, -0.5, 0])
        base = np.zeros(len(ms))
        areas = VGroup()
        for key, name, col in [PARTS_[3], PARTS_[2], PARTS_[1], PARTS_[0]]:
            top = base + cents[key]
            pts = [pa.ax.c2p(x, v) for x, v in zip(xs, top)] + [pa.ax.c2p(x, v) for x, v in zip(xs[::-1], base[::-1])]
            areas.add(Polygon(*pts, stroke_width=0, fill_color=col, fill_opacity=0.85))
            base = top
        key_ = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=c, fill_opacity=1), tx(n, 14, c)).arrange(RIGHT, buff=0.08)
                        for _, n, c in PARTS_]).arrange(RIGHT, buff=0.35).next_to(pa, UP, buff=0.15)
        t0, t1 = P["shares"]["taxes_pct"][0], P["shares"]["taxes_pct"][-1]
        tx0 = tx(f"2000: taxes {t0:.0f}% of the price", 17, STATE, bold=True).move_to([-2.6, -1.7, 0])
        tx1 = tx(f"2026: {t1:.0f}%", 17, STATE, bold=True).move_to([4.6, -1.8, 0])
        k22 = ms.index("2022-06")
        peak = tx(f"June 2022: ${retail[k22]:.2f}", 17, WHITE, bold=True).next_to(pa.ax.c2p(xs[k22], retail[k22]), UP, buff=0.1)
        src = source("US Energy Information Administration, Gasoline Pump Components History, monthly since 2000", size=13)
        with self.voiceover(
            "Watch the shares move over twenty-six years. <bookmark mark='a'/> The crude-oil layer swells and shrinks "
            "with the price of a barrel: the peak of 2008, the collapse of 2009, the long slump after 2014, the spike "
            "after Russia invaded Ukraine in 2022. <bookmark mark='b'/> The tax layer barely moves, because it is so "
            f"many cents a gallon. So when prices were low, in 2000, taxes were {t0:.0f} percent of the price; in 2026, "
            f"{t1:.0f} percent. <bookmark mark='c'/> And the refining layer, thin in most years, fattens whenever "
            "refineries are short of capacity, as Chapter 12 shows. The price at the pump is mostly a price of crude "
            "oil, set far away."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(key_))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a_) for a_ in areas], lag_ratio=0.3), run_time=3.0)
            self.play(FadeIn(peak))
            vo.wait_until("b")
            self.play(FadeIn(tx0), FadeIn(tx1), Indicate(areas[0], color=WHITE))
            vo.wait_until("c")
            self.play(Indicate(areas[2], color=WHITE))
        self.clear_scene()
