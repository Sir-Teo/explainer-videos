from __future__ import annotations

from videos.industry.industry4.common import *  # noqa: F403


class Leverage(VoiceoverScene):
    def construct(self):
        card(self, 8, "Operating leverage", "Why do some companies' profits swing so much more than their sales?",
             "Chapter eight. Operating leverage.", lit=("dollar", "make"))
        self.two_firms()
        self.delta()

    def two_firms(self):
        F = R["leverage"]["firms"]
        d = ValueTracker(0.0)

        def profit(f):
            return 100 * (1 + d.get_value()) * (1 - F[f]["var_share"]) - F[f]["fixed"]

        # the hotel: a tower whose windows light with occupancy
        tower = VGroup(Rectangle(width=1.7, height=3.0, stroke_width=0, fill_color="#3A4458", fill_opacity=1))
        wins = VGroup(*[Square(0.16, stroke_width=0, fill_color="#2A3446", fill_opacity=1) for _ in range(40)])
        wins.arrange_in_grid(rows=10, cols=4, buff=(0.18, 0.12)).move_to(tower)
        tower.add(wins).move_to([-5.0, 0.9, 0])
        hotel_n = tx("a hotel", 24, FIXED, bold=True).next_to(tower, UP, buff=0.15)
        hotel_c = tx("$70m fixed, 20% variable", 18, GREY_B).next_to(tower, DOWN, buff=0.15)

        def light(m):
            k = int(round(40 * 0.7 * (1 + d.get_value())))
            for i, w in enumerate(m):
                w.set_fill(PRICE if i < k else "#2A3446")
        wins.add_updater(light)

        crowd = draw.crowd(12, 0.42, color="#C9D3E0", cols=4).move_to([5.0, 0.9, 0])
        agency_n = tx("a temp agency", 24, VAR, bold=True).next_to(crowd, UP, buff=0.35)
        agency_c = tx("$10m fixed, 80% variable", 18, GREY_B).next_to(crowd, DOWN, buff=0.35)

        def staff(m):
            k = int(round(12 * (0.65 + 1.5 * d.get_value())))
            for i, p in enumerate(m):
                p.set_opacity(1 if i < k else 0.15)
        crowd.add_updater(staff)

        # profit bars around a zero line
        zero_y = -2.3
        scale = 0.075

        def pbar(f, x):
            def make():
                v = profit(f)
                r_ = Rectangle(width=1.1, height=max(abs(v) * scale, 0.01), stroke_width=0,
                               fill_color=PROFIT if v >= 0 else LOSS, fill_opacity=0.9)
                r_.move_to([x, zero_y, 0], aligned_edge=DOWN if v >= 0 else UP)
                return r_
            return always_redraw(make)
        zero = Line([-3.2, zero_y, 0], [3.2, zero_y, 0], stroke_color=GREY_B, stroke_width=2)
        bars = VGroup(pbar("hotel", -1.2), pbar("agency", 1.2))
        nums = VGroup()

        def money(v):
            return ("-" if v < -0.5 else "+" if v > 0.5 else "") + f"${abs(v):.0f}m"
        for f, x in (("hotel", -1.2), ("agency", 1.2)):
            n_ = draw.memo_redraw(lambda f=f: int(round(profit(f))), lambda v: tx(money(v), 30, WHITE, bold=True),
                                  place=lambda m, f=f, x=x: m.move_to([x, zero_y + 0.3 + max(profit(f), 0) * scale, 0]))
            nums.add(n_)
        labels = VGroup(tx("hotel's profit", 17, FIXED).move_to([-1.2, -3.55, 0]),
                        tx("agency's profit", 17, VAR).move_to([1.2, -3.55, 0]))
        dem = draw.memo_redraw(lambda: int(round(100 * d.get_value())),
                               lambda v: tx(("+" if v > 0 else "-" if v < 0 else "") + f"{abs(v)}%", 40, PRICE, bold=True),
                               place=lambda m: m.move_to([0, 2.7, 0]))
        dem_t = tx("change in sales", 20, GREY_B).move_to([0, 2.1, 0])
        tag = estimate_tag("illustrative: two firms with $100m of sales and $10m of profit", corner=DR)
        with self.voiceover(
            "Fixed costs do something else: they amplify. <bookmark mark='a'/> Take two businesses that each sell a "
            "hundred million dollars a year and each make ten million of profit. <bookmark mark='b'/> A hotel, "
            "whose building, staff and loans cost seventy million a year whatever happens; each guest adds only "
            "twenty cents of cost per dollar, for cleaning and breakfast. <bookmark mark='c'/> And a temp agency, "
            "which owns almost nothing: it pays its workers eighty cents of every dollar it bills, and has ten "
            "million of fixed costs. <bookmark mark='d'/> Same sales, same profit."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tower, shift=UP * 0.2), FadeIn(hotel_n), FadeIn(crowd, shift=UP * 0.2), FadeIn(agency_n),
                      FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(hotel_c), Indicate(tower, color=FIXED, scale_factor=1.03))
            vo.wait_until("c")
            self.play(FadeIn(agency_c), Indicate(crowd, color=VAR, scale_factor=1.05))
            vo.wait_until("d")
            self.play(Create(zero), FadeIn(bars), FadeIn(nums), FadeIn(labels), FadeIn(dem), FadeIn(dem_t))
        with self.voiceover(
            "Now a recession takes a fifth off both their sales. <bookmark mark='a'/> The agency sends fewer workers "
            "out and pays fewer wages; its profit falls from ten million to six. <bookmark mark='b'/> The hotel's "
            "rooms are emptier, but its building costs the same. Its profit falls from ten million to a loss of six. "
            "<bookmark mark='c'/> Run it the other way, a boom with a fifth more sales, and the hotel's profit "
            "jumps to twenty-six million while the agency's rises to fourteen. <bookmark mark='d'/> Economists "
            "call this operating leverage. A one percent change in the hotel's sales moves its profit by eight "
            "percent; the agency's by two."
        ) as vo:
            vo.wait_until("a")
            self.play(d.animate.set_value(-0.2), run_time=3.0)
            vo.wait_until("b")
            self.play(Indicate(bars[0], color=LOSS))
            vo.wait_until("c")
            self.play(d.animate.set_value(0.2), run_time=4.0)
            vo.wait_until("d")
            self.play(d.animate.set_value(0.0), run_time=2.0)
        for m in (wins, crowd):
            m.clear_updaters()
        self.clear_scene()

    def delta(self):
        C = R["leverage"]["covid"]
        head = tx("Delta Air Lines, 2019 and 2020", 28, bold=True).to_edge(UP, buff=0.3)
        base = -1.9
        u = 0.085

        def col(x, v, color, name):
            r_ = Rectangle(width=1.2, height=abs(v) * u, stroke_width=0, fill_color=color, fill_opacity=0.9)
            r_.move_to([x, base, 0], aligned_edge=DOWN if v >= 0 else UP)
            lab = tx(f"${v:.1f}bn" if v >= 0 else f"-${-v:.1f}bn", 20, color, bold=True)
            lab.next_to(r_, UP if v >= 0 else DOWN, buff=0.08)
            return VGroup(r_, lab, tx(name, 17, GREY_B).move_to([x, base - 0.3 if v >= 0 else base + 0.3, 0]))
        groups = []
        for k, (yr, x0) in enumerate(((2019, -4.2), (2020, 2.0))):
            g = VGroup(col(x0, C["rev"][k], FIXED, "revenue"), col(x0 + 1.45, C["cost"][k], VAR, "costs"),
                       col(x0 + 2.9, C["oi"][k], PROFIT if C["oi"][k] >= 0 else LOSS, "operating profit"))
            g.add(tx(f"{yr}", 30, WHITE, bold=True).move_to([x0 + 1.45, 2.85, 0]))
            groups.append(g)
        # keep 2020's labels clear of the falling bar
        groups[1][2][2].move_to([2.0 + 2.9, base + 0.3, 0])
        zero = Line([-5.2, base, 0], [6.3, base, 0], stroke_color=GREY_B, stroke_width=2)
        src = source("Delta Air Lines Forms 10-K 2020 and 2021; 2020 costs as reported, including restructuring "
                     "charges and net of government payroll support")
        fall_r = 1 - C["rev"][1] / C["rev"][0]
        fall_c = 1 - C["cost"][1] / C["cost"][0]
        with self.voiceover(
            "Airlines are hotels with wings, and in 2020 the world ran the experiment. <bookmark mark='a'/> In "
            f"2019 Delta took in {C['rev'][0]:.0f} billion dollars, spent {C['cost'][0]:.0f} and made an operating "
            f"profit of {C['oi'][0]:.1f} billion. <bookmark mark='b'/> In 2020 the pandemic emptied its planes. "
            f"Revenue fell by {100 * fall_r:.0f} percent. <bookmark mark='c'/> Costs, as reported, fell by only "
            f"{100 * fall_c:.0f} percent: the planes, the leases, the airports and much of the staff still had to be "
            "paid, and the year's costs include the price of retiring planes and people early. "
            f"<bookmark mark='d'/> A profit of {C['oi'][0]:.1f} billion became a loss of {-C['oi'][1]:.1f} billion."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(c_[0], DOWN) for c_ in groups[0][:3]], lag_ratio=0.3),
                      *[FadeIn(c_[1:]) for c_ in groups[0][:3]], FadeIn(groups[0][3]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(groups[1][3]), GrowFromEdge(groups[1][0][0], DOWN), FadeIn(groups[1][0][1:]))
            vo.wait_until("c")
            self.play(GrowFromEdge(groups[1][1][0], DOWN), FadeIn(groups[1][1][1:]))
            vo.wait_until("d")
            self.play(GrowFromEdge(groups[1][2][0], UP), FadeIn(groups[1][2][1:]))
        lesson = tx("High fixed costs make good years very good and bad years very bad.", 26, PRICE, bold=True)
        lesson.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "High fixed costs make the good years very good and the bad years very bad. That is why such businesses "
            "borrow carefully, hold cash, and fight for every last customer when demand turns, which is the story of "
            "the last chapters of this part."
        ):
            self.play(FadeIn(lesson, shift=UP * 0.1), FadeOut(src))
        self.clear_scene()
