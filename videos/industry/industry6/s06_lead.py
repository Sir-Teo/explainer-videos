from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


class Lead(VoiceoverScene):
    def construct(self):
        card(self, 5, "Why the wait makes it worse", "If everyone knows about the cycle, why does it keep happening?",
             "Chapter five. Why the wait makes it worse.", lit=("change", "make"))
        self.leads()
        self.reasons()

    def leads(self):
        F = R["fleet"]
        panels = VGroup()
        for k, L in enumerate((1, 2, 3, 4)):
            rates = F["rates"][L]
            pa = viz.plot_axes([0, len(rates) - 1], [0.4, 1.9], x_length=4.3, y_length=1.8, yticks=[1.0],
                               yfmt=lambda v: "cost", size=13, grid=True)
            line = VMobject(stroke_color=PRICE, stroke_width=3).set_points_as_corners(
                [pa.ax.c2p(i, v) for i, v in enumerate(rates)])
            sw = F["swing"][L]
            head = VGroup(tx(f"ships take {L} year{'s' if L > 1 else ''} to build", 18, WHITE, bold=True),
                          tx(f"swing: {100 * sw:.0f}%", 17, BUST if sw > 0.5 else GREY_B)).arrange(RIGHT, buff=0.3)
            head.next_to(pa, UP, buff=0.08).align_to(pa, LEFT)
            yard = VGroup(*[draw.crane(0.3) for _ in range(L)]).arrange_in_grid(rows=2, cols=2, buff=0.05).next_to(
                pa, LEFT, buff=0.25)
            panels.add(VGroup(pa, line, head, yard))
        panels.arrange_in_grid(rows=2, cols=2, buff=(0.9, 0.8)).move_to([0.1, -0.3, 0])
        if panels.width > 13.4:
            panels.scale_to_fit_width(13.4)
        tag = estimate_tag("the Works' fleet model; demand grows 3% a year in every panel", corner=DR, size=13)
        with self.voiceover(
            "Why does the wait matter so much? Run the same market four times, changing only how long a ship takes "
            "to build. <bookmark mark='a'/> If a ship takes one year, owners who order too many find out quickly, "
            f"and the rate barely moves: a swing of {100 * R['fleet']['swing'][1]:.0f} percent. "
            f"<bookmark mark='b'/> Two years: {100 * R['fleet']['swing'][2]:.0f} percent. "
            f"<bookmark mark='c'/> Three years: {100 * R['fleet']['swing'][3]:.0f} percent. <bookmark mark='d'/> Four "
            f"years, and the rate swings by more than its own average: {100 * R['fleet']['swing'][4]:.0f} percent. "
            "<bookmark mark='e'/> Nothing else changed. The longer the wait, the longer owners keep ordering against "
            "a high rate before the first new ship shows them their mistake, and the bigger the wave that lands at "
            "the end. In the real world the waits differ: months for a house, about a year for a pig, years for a "
            "ship, a chip plant or an oil field. The model says the industries with the longest waits should have "
            "the wildest swings, and the rest of this part is a tour of them."
        ) as vo:
            self.play(FadeIn(tag), LaggedStart(*[AnimationGroup(FadeIn(pn[0]), FadeIn(pn[2]), FadeIn(pn[3]))
                                                 for pn in panels], lag_ratio=0.2), run_time=2.0)
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Create(panels[k][1]), Indicate(panels[k][3], color=ORDER), run_time=1.6, rate_func=linear)
            vo.wait_until("e")
            self.play(Indicate(panels[3][1], color=BUST), Indicate(panels[3][2][1], color=BUST))
        self.clear_scene()

    def reasons(self):
        items = []
        # 1. lumpy plants: one fab is a big share of the market
        fab = VGroup(*[Rectangle(width=0.5, height=0.5, stroke_width=1, stroke_color="#0E1117", fill_color=CAP,
                                 fill_opacity=0.8) for _ in range(9)]).arrange_in_grid(rows=3, cols=3, buff=0)
        newfab = Rectangle(width=1.5, height=0.5, stroke_width=1, stroke_color="#0E1117", fill_color=ORDER,
                           fill_opacity=0.9).next_to(fab, UP, buff=0)
        items.append((VGroup(fab, newfab), "Plants come in lumps", "one new plant can add a big slice of a market at once"))
        # 2. rivals' orders you cannot see
        curtain = VGroup(Rectangle(width=1.6, height=1.3, stroke_width=0, fill_color="#2A3140", fill_opacity=1),
                         tx("?", 44, GREY_B, bold=True))
        items.append((curtain, "Orders are hidden", "you see the price today, not what rivals have ordered"))
        # 3. lenders lend most at the top
        from videos.industry.industry3.s03_ledger import _bank
        bank = VGroup(_bank().scale(2.0), VGroup(*[draw.coin(0.09) for _ in range(5)]).arrange(RIGHT, buff=0.02))
        bank[1].next_to(bank[0], DOWN, buff=0.1)
        items.append((bank, "Lenders lend at the top", "a ship earning a record rate is easy to borrow against"))
        # 4. no one wants to be the one who missed the boom
        crowd = VGroup(*[draw.person(0.4, color=ORDER if k % 3 else STONE) for k in range(6)]).arrange(RIGHT, buff=0.08)
        items.append((crowd, "Nobody wants to miss the boom", "a manager who waits and is right looks no better"))
        rows = VGroup()
        for pic, head, sub in items:
            pic.scale_to_fit_height(min(pic.height, 1.0))
            txt = VGroup(tx(head, 25, WHITE, bold=True), tx(sub, 18, GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.08)
            rows.add(VGroup(pic, txt))
        for r_ in rows:
            r_[1].next_to(r_[0], RIGHT, buff=0.35)
        rows.arrange_in_grid(rows=2, cols=2, buff=(1.0, 0.9), cell_alignment=LEFT).move_to([0, -0.2, 0])
        head = tx("Why knowing about the cycle does not stop it", 26, GOLD, bold=True).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Everyone in these industries knows about the cycle. So why doesn't it get competed away? "
            "<bookmark mark='a'/> First, plants come in lumps. A memory fab or a giant container ship is not a "
            "small step: one new plant can add a large slice of the world's capacity in a single go. "
            "<bookmark mark='b'/> Second, the orders are hidden. Each owner sees today's price, but not the "
            "orders its rivals placed last month, until the ships turn up. <bookmark mark='c'/> Third, lenders "
            "lend most at the top. A ship earning a record rate, or a factory full of orders, is the easiest thing "
            "in the world to borrow against. <bookmark mark='d'/> And fourth, people. A manager who refuses to "
            "build in a boom, and turns out to be right, looks no better than the others when the bust comes, "
            "and much worse while the boom lasts."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(rows[k][0], scale=0.8), FadeIn(rows[k][1], shift=RIGHT * 0.15))
                if k == 0:
                    self.play(Indicate(newfab, color=WHITE))
                elif k == 2:
                    self.play(rows[k][0][1].animate.shift(DOWN * 0.15), rate_func=there_and_back, run_time=0.8)
        self.clear_scene()
