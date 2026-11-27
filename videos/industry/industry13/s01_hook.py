from __future__ import annotations

from videos.industry.industry13.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.block()
        self.curves()
        self.ratio()
        self.title()

    def block(self):
        H = R["hook"]
        where = VGroup(tx("Boston, 25 February 1910", 24, WHITE, bold=True),
                       tx("Samuel Insull, who ran Chicago's electricity company,", 17, GREY_A),
                       tx("speaks at a dinner for the men who run power stations", 17, GREY_A)).arrange(
            DOWN, buff=0.06, aligned_edge=LEFT).to_corner(UL, buff=0.45)
        n = int(H["apartments"])
        cols = 14
        wins = VGroup(*[Square(0.2, stroke_width=0, fill_color="#2A3140", fill_opacity=1) for _ in range(n)])
        wins.arrange_in_grid(cols=cols, buff=0.07)
        wall = SurroundingRectangle(wins, buff=0.18, stroke_color="#5B6372", stroke_width=2, fill_color="#171C25",
                                    fill_opacity=1)
        bld = VGroup(wall, wins).move_to([2.8, -0.6, 0])
        lab = tx(f"a block in Chicago: {n} apartments, {H['customers']:.0f} customers", 16, GREY_A).next_to(bld, DOWN, buff=0.15)
        clock = ValueTracker(17.0)
        ck = draw.memo_redraw(lambda: int(clock.get_value()) % 24,
                              lambda k: tx(f"{k:02d}:00", 30, PRICE, bold=True), lambda m: m.next_to(bld, UP, buff=0.2))
        rng = np.random.default_rng(7)
        on = rng.uniform(17.5, 23.0, n)
        dur = rng.uniform(1.0, 3.0, n)

        def lit(k):
            t = clock.get_value()
            return on[k] <= t < on[k] + dur[k]
        for k, w in enumerate(wins):
            w.add_updater(lambda m, k=k: m.set_fill("#F6C453" if lit(k) else "#2A3140"))
        count = draw.number(lambda: sum(lit(k) for k in range(n)), 0, suffix=" lit", size=26, color=PRICE)
        count.add_updater(lambda m: m.move_to([-1.6, 0.4, 0]))
        note = VGroup(tx("each family lights up", 17, WHITE), tx("at its own hour", 17, WHITE)).arrange(DOWN, buff=0.04)
        note.move_to([-1.6, -0.4, 0])
        src = source("Samuel Insull, address of 25 February 1910, in Central-Station Electric Service (1915), pp. 127-130",
                     size=13)
        with self.voiceover(
            "On the twenty-fifth of February 1910, at a dinner in Boston, Samuel Insull, who ran the electricity company "
            "of Chicago, told a room of power-station managers about one block of apartments. <bookmark mark='a'/> It had "
            f"{n} apartments, and {H['customers']:.0f} of them bought electricity from him, ten or eleven lamps each. "
            "<bookmark mark='b'/> Watch an evening. Each family switches on its lamps at its own hour, and off again. "
            "<bookmark mark='c'/> Never are they all on at once."
        ) as vo:
            self.play(FadeIn(where), FadeIn(src), FadeIn(bld))
            vo.wait_until("a")
            self.play(FadeIn(lab), Indicate(wall, color=PRICE, scale_factor=1.02))
            vo.wait_until("b")
            self.add(ck, count, note)
            self.play(clock.animate.set_value(23.9), run_time=7.0, rate_func=linear)
            vo.wait_until("c")
            self.play(Indicate(count, color=PRICE))
        for w in wins:
            w.clear_updaters()
        count.clear_updaters()
        self.clear_scene()

    def curves(self):
        H = R["hook"]
        homes = H["homes"]
        hours = list(range(24))
        top_ = sum(max(h) for h in homes) * 1.12
        pa = viz.plot_axes([0, 23], [0, top_], x_length=6.0, y_length=4.2, xticks=[0, 6, 12, 18, 23],
                           yticks=[1, 2, 3, 4], xfmt=lambda v: f"{int(v)}:00", yfmt=lambda v: f"{v:.0f}",
                           ylabel="kW", size=13).move_to([2.6, -0.6, 0])
        smalls = VGroup()
        for i, h in enumerate(homes):
            sp = viz.plot_axes([0, 23], [0, 0.5], x_length=1.6, y_length=0.55, xticks=[], yticks=[], size=10, grid=False)
            sp.move_to([-5.6 + 1.85 * (i % 3), 2.2 - 0.85 * (i // 3), 0])
            ln = VMobject(stroke_color=PRICE, stroke_width=2).set_points_as_corners([sp.ax.c2p(x, y) for x, y in zip(hours, h)])
            smalls.add(VGroup(sp, ln))
        tot = [sum(h[x] for h in homes) for x in hours]
        sum_peaks = sum(max(h) for h in homes)
        lt = VMobject(stroke_color=WHITE, stroke_width=3.5).set_points_as_corners([pa.ax.c2p(x, y) for x, y in zip(hours, tot)])
        hp = DashedLine(pa.ax.c2p(0, sum_peaks), pa.ax.c2p(23, sum_peaks), stroke_color=BAD, stroke_width=2, dash_length=0.08)
        hpl = tx("if they all peaked together", 14, BAD).next_to(hp, UP, buff=0.05).align_to(hp, LEFT)
        cp = DashedLine(pa.ax.c2p(0, max(tot)), pa.ax.c2p(23, max(tot)), stroke_color=GOOD, stroke_width=2, dash_length=0.08)
        cpl = tx("their actual combined peak", 14, GOOD).next_to(cp, DOWN, buff=0.05).align_to(cp, LEFT)
        head = tx("Twelve households, one evening, and all of them together", 20, WHITE, bold=True).to_edge(UP, buff=0.3)
        tag = estimate_tag("illustration: invented households, the shape Insull described", corner=DR, size=12)
        with self.voiceover(
            "Here is the same idea as a picture, with a dozen made-up households. <bookmark mark='a'/> Each has a short "
            "spike of demand in the evening. <bookmark mark='b'/> If you had to build for every family's own peak, you "
            "would need a plant this big. <bookmark mark='c'/> But add them up, and their spikes fall at different "
            "times. The combined peak, the one the power station actually has to meet, is far lower. Insull called this "
            "the diversity of demand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_[0]) for s_ in smalls], lag_ratio=0.05),
                      LaggedStart(*[Create(s_[1]) for s_ in smalls], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(pa), Create(hp), FadeIn(hpl))
            vo.wait_until("c")
            self.play(TransformFromCopy(VGroup(*[s_[1] for s_ in smalls]), lt), run_time=1.8)
            self.play(Create(cp), FadeIn(cpl))
        self.clear_scene()

    def ratio(self):
        H = R["hook"]
        sc = 4.2 / H["peaks"]
        b1 = Rectangle(width=1.5, height=H["peaks"] * sc, stroke_width=0, fill_color=BAD, fill_opacity=0.8).move_to([-4.0, -2.6, 0],
                                                                                                             aligned_edge=DOWN)
        b2 = Rectangle(width=1.5, height=H["peak"] * sc, stroke_width=0, fill_color=GOOD, fill_opacity=0.85).move_to(
            [-1.6, -2.6, 0], aligned_edge=DOWN)
        l1 = VGroup(tx(f"{H['peaks']:.1f} kW", 22, BAD, bold=True), tx("the customers' own peaks, added up", 13, GREY_A)).arrange(
            DOWN, buff=0.05).next_to(b1, UP, buff=0.1)
        l2 = VGroup(tx(f"{H['peak']:.0f} kW", 22, GOOD, bold=True), tx("the block's peak at the transformer", 13, GREY_A)).arrange(
            DOWN, buff=0.05).next_to(b2, UP, buff=0.1)
        eq = VGroup(tx("load factor = average use ÷ peak", 22, WHITE, bold=True),
                    tx(f"{H['kwh']:,.0f} kWh a year ÷ ({H['peaks']:.1f} kW × 8,760 hours) = {100 * H['lf_alone']:.1f}%", 18, BAD),
                    tx(f"{H['kwh']:,.0f} kWh a year ÷ ({H['peak']:.0f} kW × 8,760 hours) = {100 * H['lf_together']:.0f}%", 18, GOOD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.2, 1.2, 0])
        quote = VGroup(tx("'if your entire plant is only in use 5.5 per cent of the time", 16, WHITE),
                       tx("it is only a question of time when you will be", 16, WHITE),
                       tx("in the hands of a receiver.'", 16, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([3.2, -1.4, 0])
        src = source("Samuel Insull, address of 25 February 1910, in Central-Station Electric Service (1915)", size=13)
        with self.voiceover(
            f"Insull's numbers. The block used {H['kwh']:,.0f} kilowatt-hours a year. <bookmark mark='a'/> Add up each "
            f"customer's own peak and you get {H['peaks']:.1f} kilowatts; measured on that, the plant would be in use "
            f"just {100 * H['lf_alone']:.1f} per cent of the time. 'It is only a question of time,' he said, 'when you "
            "will be in the hands of a receiver.' <bookmark mark='b'/> But the peak at the transformer, all of them "
            f"together, was only {H['peak']:.0f} kilowatts, and the load factor {100 * H['lf_together']:.0f} per cent. "
            "<bookmark mark='c'/> That ratio, average use against peak, is the economics of electricity. A power "
            "station costs what its peak costs, and earns on what it sells on average. Everything in this part "
            "follows from it."
        ) as vo:
            self.play(FadeIn(eq[0]), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(b1, DOWN), FadeIn(l1), FadeIn(eq[1]))
            self.play(FadeIn(quote, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(GrowFromEdge(b2, DOWN), FadeIn(l2), FadeIn(eq[2]))
            vo.wait_until("c")
            self.play(Indicate(eq[0], color=PRICE))
        self.clear_scene()

    def title(self):
        card_ = part_title(PART, ASK)
        if card_.width > 13:
            card_.scale_to_fit_width(13)
        with self.voiceover(
            "Electricity is the one product that has to be made at the very moment it is used, by machines that cost a "
            "fortune and stand idle much of the time. Industry, Built. Part thirteen: electricity. How is a product "
            "that cannot be stored sold every second, and who pays for the wires?"
        ):
            self.play(FadeIn(card_[0]), run_time=0.8)
            self.play(FadeIn(card_[1:3], shift=UP * 0.15), run_time=1.2)
            self.play(Create(card_[3]), Write(card_[4]), run_time=2)
        self.clear_scene()
