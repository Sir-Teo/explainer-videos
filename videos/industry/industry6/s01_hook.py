from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.micron()
        self.maersk()
        self.title()

    def micron(self):
        m = R["micron"]
        a, b = m["fy23"], m["fy26"]
        t = ValueTracker(0.0)
        base, u = -1.6, 0.026  # inches per $bn
        fab = VGroup(draw.factory(2.2, color="#8C929B"), draw.wafer(0.55)).arrange(RIGHT, buff=0.35).move_to(
            [-4.3, 2.0, 0])
        who = VGroup(tx("Micron Technology", 24, WHITE, bold=True), tx("memory chips, Boise, Idaho", 16, GREY_B)
                     ).arrange(DOWN, buff=0.06).next_to(fab, DOWN, buff=0.2)

        def rev():
            return a["revenue"] + t.get_value() * (b["revenue"] - a["revenue"])

        def oi():
            return a["oi"] + t.get_value() * (b["oi"] - a["oi"])

        def bar(fn, x, color_up, color_down):
            def make():
                v = fn()
                h = max(abs(v) * u, 0.02)
                r_ = Rectangle(width=1.3, height=h, stroke_width=0, fill_color=color_up if v >= 0 else color_down,
                               fill_opacity=0.9)
                return r_.move_to([x, base, 0], aligned_edge=DOWN if v >= 0 else UP)
            return always_redraw(make)
        rb = bar(rev, 1.0, CAP, CAP)
        ob = bar(oi, 3.6, BOOM, BUST)
        zero = Line([-0.2, base, 0], [4.8, base, 0], stroke_color=GREY_B, stroke_width=1.5)
        rn = draw.number(rev, 1, prefix="$", suffix="bn", size=30, color=CAP)
        on = draw.number(oi, 1, prefix="$", suffix="bn", size=30, color=WHITE, sign=True)
        rn.add_updater(lambda g: g.next_to([1.0, base + max(rev(), 0) * u, 0], UP, buff=0.12))
        on.add_updater(lambda g: g.next_to([3.6, base + max(oi(), 0) * u, 0], UP, buff=0.12))
        labs = VGroup(tx("sales", 18, CAP).move_to([1.0, base - 0.45, 0]),
                      tx("operating profit", 18, GREY_A).move_to([3.6, base - 0.45, 0]))
        yr = draw.memo_redraw(lambda: "fiscal 2023" if t.get_value() < 0.5 else "fiscal 2026",
                         lambda k: tx(k, 30, GOLD, bold=True), lambda g: g.move_to([2.3, 3.2, 0]))
        heap = VGroup(*[draw.chip(0.32) for _ in range(28)]).arrange_in_grid(rows=4, cols=7, buff=0.06).move_to(
            [-4.3, -1.6, 0])
        few = VGroup(*[draw.chip(0.32) for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to([-4.3, -1.6, 0])
        tag_lo = VGroup(tx("2023: too many", 20, BUST, bold=True)).next_to(heap, DOWN, buff=0.2)
        tag_hi = VGroup(tx("2026: too few", 20, BOOM, bold=True)).next_to(few, DOWN, buff=0.85)
        src = source("Micron Technology, Forms 10-K for fiscal 2023 and 2026 (SEC company facts)", size=13)
        with self.voiceover(
            "In the year to August 2023, Micron Technology, America's largest maker of memory chips, sold "
            f"{a['revenue']:.1f} billion dollars' worth of them, <bookmark mark='a'/> and lost "
            f"{-a['oi']:.1f} billion dollars on its operations. <bookmark mark='b'/> Three years later, in the year "
            f"to September 2026, it sold {b['revenue']:.1f} billion dollars' worth, and made an operating profit of "
            f"{b['oi']:.1f} billion. In its last quarter it kept {100 * m['q4_26']['margin']:.0f} cents of every "
            "dollar of sales as operating profit. <bookmark mark='c'/> Same company. Mostly the same factories. The "
            "same kind of chip. What changed was the price of memory, and the price changed because in 2023 the "
            "world had too many memory chips, <bookmark mark='d'/> and in 2026 it had too few."
        ) as vo:
            self.play(FadeIn(src), FadeIn(fab, shift=UP * 0.2), FadeIn(who), FadeIn(yr), Create(zero))
            self.add(rb, rn)
            self.play(FadeIn(labs[0]), run_time=0.6)
            vo.wait_until("a")
            self.add(ob, on)
            self.play(FadeIn(labs[1]), Indicate(on, color=BUST))
            vo.wait_until("b")
            self.play(t.animate.set_value(1.0), run_time=4.0, rate_func=rate_functions.ease_in_out_cubic)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c_, scale=0.6) for c_ in heap], lag_ratio=0.03), FadeIn(tag_lo),
                      run_time=1.6)
            vo.wait_until("d")
            self.play(ReplacementTransform(heap, few), ReplacementTransform(tag_lo, tag_hi), run_time=1.4)
            self.play(Indicate(few, color=BOOM, scale_factor=1.3))
        for g in (rb, ob, rn, on, yr):
            g.clear_updaters()
        self.clear_scene()

    def maersk(self):
        k = R["maersk"]
        pa = viz.plot_axes([2018.4, 2025.6], [0, 32], x_length=8.4, y_length=3.6, xticks=k["years"],
                           yticks=[10, 20, 30], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=16)
        pa.move_to([0.6, -1.3, 0])
        bars = viz.year_bars(pa, k["years"], k["ebit"], BOOM, width=0.62)
        for b_, v in zip(bars, k["ebit"]):
            b_.set_fill(BOOM if v > 10 else (ORDER if v > 5 else BUST))
        nums = VGroup(*[tx(f"${v:.1f}bn", 16, WHITE).next_to(b_, UP, buff=0.06) for b_, v in zip(bars, k["ebit"])])
        head = tx("A.P. Moller-Maersk: operating profit each year", 20, GREY_A).next_to(pa, UP, buff=0.3).align_to(
            pa, LEFT)
        boat = draw.ship(2.6).move_to([-8.5, 2.6, 0])
        sea = VGroup(*[FunctionGraph(lambda x, j=j: 0.05 * np.sin(2.5 * x + j), x_range=[-7.2, 7.2],
                                     color="#3B7DD8", stroke_width=2, stroke_opacity=0.5).shift(UP * (2.15 - 0.15 * j))
                       for j in range(3)])
        src = source("A.P. Moller-Maersk annual reports 2020-2025 (ESEF filings): EBIT", size=13)
        i19, i22, i23 = (k["years"].index(y) for y in (2019, 2022, 2023))
        with self.voiceover(
            "The same thing happens at sea. <bookmark mark='a'/> A.P. Moller-Maersk, the Danish container shipping "
            f"company, made {k['ebit'][i19]:.1f} billion dollars of operating profit in 2019. "
            f"<bookmark mark='b'/> In 2022, with the world's ports jammed and every container booked, it made "
            f"{k['ebit'][i22]:.1f} billion. <bookmark mark='c'/> A year later, {k['ebit'][i23]:.1f} billion. "
            "<bookmark mark='d'/> Booms like these do not last, because everyone can see them. Every chip maker and "
            "every shipowner sees the same high price, and orders more factories and more ships. They take years to "
            "build. And when they arrive, they all arrive together."
        ) as vo:
            self.play(FadeIn(src), Create(sea), FadeIn(pa), FadeIn(head))
            self.play(boat.animate.move_to([-3.6, 2.6, 0]), run_time=2.0, rate_func=rate_functions.ease_out_quad)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[:2]], lag_ratio=0.3),
                      FadeIn(nums[:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[2:4]], lag_ratio=0.4), FadeIn(nums[2:4]),
                      boat.animate.move_to([0.5, 2.6, 0]).scale(1.1), run_time=2.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[4], DOWN), FadeIn(nums[4]), boat.animate.move_to([3.6, 2.45, 0]).scale(0.9))
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[5:]], lag_ratio=0.3), FadeIn(nums[5:]))
            vo.wait_until("d")
            fleet = VGroup(*[draw.ship(1.1) for _ in range(6)]).arrange(RIGHT, buff=0.15).move_to([0.8, 2.55, 0])
            self.play(ReplacementTransform(boat, fleet[2]),
                      LaggedStart(*[FadeIn(s_, shift=LEFT * 0.4) for j, s_ in enumerate(fleet) if j != 2],
                                  lag_ratio=0.2), run_time=2.2)
            self.play(Indicate(bars[4:], color=BUST, scale_factor=1.04))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        with self.voiceover(
            "Industry, Built. Part six: the cycle. Why do industries keep building too much at the top?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
