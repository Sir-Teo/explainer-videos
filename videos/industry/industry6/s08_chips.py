from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Chips(VoiceoverScene):
    def construct(self):
        card(self, 7, "Memory chips", "What does the cycle look like in one company's sales?",
             "Chapter seven. Memory chips.", lit=("change", "make"))
        self.quarters()
        self.spending()

    def quarters(self):
        m = R["micron"]
        qs, rv = m["quarters"], m["q_revenue"]
        n = len(qs)
        x0, x1, base, top = -6.0, 5.6, -2.6, 2.6
        w = (x1 - x0) / n
        ymax = ValueTracker(10.0)
        shown = ValueTracker(0)

        def ypos(v):
            return base + (top - base) * v / ymax.get_value()

        def make_bars():
            k = int(shown.get_value())
            g = VGroup()
            for i in range(min(k, n)):
                h = max(ypos(rv[i]) - base, 0.005)
                col = BUST if any(p["low_end"] == qs[i] for p in m["peaks"]) else CAP
                g.add(Rectangle(width=w * 0.8, height=h, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                    [x0 + w * (i + 0.5), base + h / 2, 0]))
            return g
        bars = always_redraw(make_bars)
        floor = Line([x0, base, 0], [x1, base, 0], stroke_color=GREY_B, stroke_width=1.5)
        yrs = VGroup(*[tx(str(y), 14, GREY_B).move_to([x0 + w * (next(i for i, q in enumerate(qs) if q.startswith(str(y)))
                                                                 + 0.5), base - 0.22, 0]) for y in (2010, 2014, 2018, 2022, 2026)])
        tick_lab = draw.memo_redraw(lambda: int(round(ymax.get_value())), lambda v: tx(f"${v}bn a quarter", 15, GREY_B),
                                    lambda g: g.move_to([x0 + 0.9, top + 0.2, 0]))
        head = tx("Micron's sales, every quarter since 2009", 20, GREY_A).to_edge(UP, buff=0.35)
        notes = VGroup()
        for p in m["peaks"]:
            if p["fall"] is None:
                continue
            i, j = qs.index(p["end"]), qs.index(p["low_end"])
            a_ = np.array([x0 + w * (i + 0.5), base + (top - base) * p["value"] / 10.0 + 0.1, 0])
            b_ = np.array([x0 + w * (j + 0.5), base + (top - base) * p["low"] / 10.0 + 0.1, 0])
            notes.add(VGroup(Arrow(a_ + UP * 0.25, b_ + UP * 0.25, buff=0.05, color=BUST, stroke_width=3,
                                   max_tip_length_to_length_ratio=0.2),
                             tx(f"{100 * p['fall']:.0f}%", 17, BUST, bold=True).next_to((a_ + b_) / 2 + UP * 0.25, UP,
                                                                                         buff=0.12)))
        last = m["q4_26"]
        big = VGroup(tx(f"${last['revenue']:.1f}bn", 30, BOOM, bold=True),
                     tx(f"in one quarter, {100 * last['margin']:.0f}% of it operating profit", 17, GREY_A)).arrange(
            DOWN, buff=0.06).move_to([1.6, 1.9, 0])
        wafer = draw.wafer(0.6).move_to([-4.6, 1.7, 0])
        # why memory cycles: chips that are alike, plants that take years, demand that comes in surges
        same = VGroup(draw.chip(0.6), tx("=", 36, WHITE), draw.chip(0.6)).arrange(RIGHT, buff=0.2)
        same_t = tx("one maker's chip does the same job as another's", 17, GREY_A)
        fab = VGroup(draw.factory(1.2, color="#8C929B"), tx("billions of dollars, years to build", 17, GREY_A)).arrange(
            DOWN, buff=0.15)
        monitor = VGroup(RoundedRectangle(corner_radius=0.05, width=0.9, height=0.6, stroke_color=STONE, stroke_width=3,
                                          fill_color="#1B2230", fill_opacity=1),
                         Line(DOWN * 0.3, DOWN * 0.45, stroke_color=STONE, stroke_width=3))
        surges = VGroup(VGroup(monitor, viz.phone(0.7), draw.server_rack(0.8)).arrange(RIGHT, buff=0.35),
                        tx("demand in surges: computers, phones, data centres", 17, GREY_A)).arrange(DOWN, buff=0.15)
        why = VGroup(VGroup(same, same_t).arrange(DOWN, buff=0.15), fab, surges).arrange(RIGHT, buff=0.8).move_to(
            [0.4, -0.3, 0])
        if why.width > 13:
            why.scale_to_fit_width(13)
        src = source("Micron Technology, Forms 10-Q and 10-K (SEC company facts); fourth quarters are the year less "
                     "three quarters", size=13)
        i_last_peak = qs.index(m["peaks"][-2]["end"])
        with self.voiceover(
            "Memory chips may be the purest cycle in modern industry. <bookmark mark='a'/> A memory chip from one "
            "maker does the same job as one from another, so they compete almost entirely on price. A new factory "
            "costs many billions of dollars and takes years to build and fill with machines. Demand comes in surges, "
            "from personal computers, then phones, then data centres. <bookmark mark='b'/> Here are Micron's sales, "
            "every quarter since 2009. <bookmark mark='c'/> Four times, sales peaked, and within two years they "
            "fell: by a fifth, by more than a third, by more than two fifths, and in 2023 by "
            f"{-100 * m['peaks'][3]['fall']:.0f} percent. <bookmark mark='d'/> And then came the boom of 2025 and "
            "2026, driven by the data centres being built for artificial intelligence. "
            f"<bookmark mark='e'/> In its last quarter Micron sold {last['revenue']:.1f} billion dollars of chips, and "
            f"kept {100 * last['margin']:.0f} cents of each dollar as operating profit. A year earlier it had sold "
            f"{m['q4_25']['revenue']:.1f} billion."
        ) as vo:
            self.play(FadeIn(src), FadeIn(wafer, scale=0.8), FadeIn(head))
            self.play(Rotate(wafer, PI / 2), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(wafer.dies, color=WHITE), FadeIn(why[0], shift=UP * 0.2))
            self.play(FadeIn(why[1], shift=UP * 0.2))
            self.play(FadeIn(why[2], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeOut(why), Create(floor), FadeIn(yrs), FadeIn(tick_lab), FadeOut(wafer))
            self.add(bars)
            self.play(shown.animate.set_value(i_last_peak + 4), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(n_, shift=DOWN * 0.1) for n_ in notes], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("d")
            self.play(FadeOut(notes), run_time=0.5)
            self.play(shown.animate.set_value(n - 1), run_time=1.6, rate_func=linear)
            self.play(ymax.animate.set_value(60), shown.animate.set_value(n), run_time=3.0)
            vo.wait_until("e")
            self.play(FadeIn(big, shift=DOWN * 0.1))
        bars.clear_updaters()
        tick_lab.clear_updaters()
        self.clear_scene()

    def spending(self):
        m = R["micron"]
        rd = dict(R["reading"]["micron"])
        yrs = [y for y in m["years"] if y >= 2012]
        pa = viz.plot_axes([2011.4, 2026.6], [0, 35], x_length=9.0, y_length=3.4, xticks=[2012, 2016, 2020, 2024],
                           yticks=[10, 20, 30], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pa.move_to([0.4, -0.7, 0])
        cap = [m["capex"][m["years"].index(y)] for y in yrs]
        dep = [m["depreciation"][m["years"].index(y)] for y in yrs]
        bars = viz.year_bars(pa, yrs, cap, ORDER, width=0.5)
        dl = VMobject(stroke_color=GREY_A, stroke_width=3).set_points_as_corners(
            [pa.ax.c2p(y, v) for y, v in zip(yrs, dep)])
        key = VGroup(VGroup(Square(0.2, stroke_width=0, fill_color=ORDER, fill_opacity=1),
                            tx("spent on new plant and machines", 16, ORDER)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, stroke_color=GREY_A, stroke_width=3),
                            tx("depreciation: the old plant wearing out", 16, GREY_A)).arrange(RIGHT, buff=0.1)
                     ).arrange(RIGHT, buff=0.6).next_to(pa, UP, buff=0.2)
        ratio = VGroup(tx("fiscal 2026", 18, GREY_A), tx(f"{rd[2026]:.1f}×", 40, BUST, bold=True),
                       tx("spending over depreciation", 15, GREY_B)).arrange(DOWN, buff=0.06).move_to([5.6, 1.6, 0])
        src = source("Micron Forms 10-K, fiscal 2012-2026 (SEC company facts)", size=13)
        with self.voiceover(
            "And Micron did what the capital cycle predicts. <bookmark mark='a'/> The orange bars are what it spent "
            "each year on new factories and machines. The grey line is depreciation: roughly what it would need "
            "to spend just to replace the plant that is wearing out. <bookmark mark='b'/> In most years the two "
            "move together, with spending somewhat above depreciation as the company grows. <bookmark mark='c'/> "
            "In fiscal "
            f"2026 Micron spent {m['fy26']['capex']:.1f} billion dollars, {rd[2026]:.1f} times its depreciation: the "
            "biggest gap since at least 2010. <bookmark mark='d'/> Notice too what happened after the peak of 2018: "
            f"in fiscal 2019, with sales down by almost a quarter, Micron spent more on plant than in its record "
            "year, because the plant ordered at the top was still being paid for at the bottom. The factories ordered in "
            "this boom will arrive over the next few years. Whether demand is still there to meet them is the "
            "question every cycle asks."
        ) as vo:
            self.play(FadeIn(src), FadeIn(pa), FadeIn(key[0]),
                      LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.08), run_time=2.2)
            vo.wait_until("a")
            self.play(FadeIn(key[1]), Indicate(bars, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(Create(dl), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(bars[-1], color=BUST, scale_factor=1.1), FadeIn(ratio, shift=LEFT * 0.2))
            vo.wait_until("d")
            i19 = yrs.index(2019)
            self.play(Indicate(bars[i19], color=ORDER, scale_factor=1.2), Indicate(bars[i19 - 1], color=WHITE))
        self.clear_scene()
