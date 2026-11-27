from __future__ import annotations

from videos.industry.industry14.common import *  # noqa: F403


class Elsewhere(VoiceoverScene):
    def construct(self):
        card(self, 5, "Public and private elsewhere", "Does the model work differently in America and Brazil?",
             "Chapter five. Public and private elsewhere.", lit=("dollar", "moat"))
        self.america()
        self.brazil()

    def america(self):
        E = R["elsewhere"]["awk"]
        G = R["regulated"]
        rb = E["rb"]
        eq = E["eq"] / 100
        roe = E["roe"] / 100
        box = Rectangle(width=3.2, height=3.0, stroke_width=0, fill_color=WATER, fill_opacity=0.3).move_to([-4.4, -0.3, 0])
        split = Line(box.get_corner(DL) + UP * 3.0 * eq, box.get_corner(DR) + UP * 3.0 * eq, stroke_color=WHITE, stroke_width=2)
        eq_r = Rectangle(width=3.2, height=3.0 * eq, stroke_width=0, fill_color=EQUITY, fill_opacity=0.45).move_to(box.get_bottom(), aligned_edge=DOWN)
        box_l = VGroup(tx(f"rate base ${rb:,.0f}m", 18, WHITE, bold=True), tx("Kentucky American Water, 2025", 13, GREY_A)).arrange(DOWN, buff=0.04).next_to(box, UP, buff=0.12)
        eq_l = tx(f"equity {100 * eq:.1f}%", 15, EQUITY, bold=True).move_to(eq_r)
        debt_l = tx(f"debt {100 * (1 - eq):.1f}%", 15, GREY_A).move_to(box.get_top() + DOWN * 3.0 * (1 - eq) / 2)
        calc = VGroup(tx(f"allowed return on equity: {100 * roe:.2f}%", 22, PRICE, bold=True),
                      tx(f"${rb:,.0f}m x {100 * eq:.1f}% x {100 * roe:.2f}% = ${rb * eq * roe:,.0f}m a year for shareholders", 17, WHITE),
                      tx("set in a rate case before the state's commission", 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([2.6, 1.2, 0])
        comp = VGroup(tx("compare England, 2025-30:", 16, GREY_A),
                      tx(f"{G['roe']:.1f}% after inflation, about 7.2% before", 17, UK, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.05).move_to([2.2, -0.4, 0])
        firm = VGroup(tx(f"American Water: {E['people']:.0f} million people in {E['states']:.0f} states", 17, WHITE, bold=True),
                      tx(f"plans to invest ${E['capex10'][0]:.0f}-{E['capex10'][1]:.0f}bn over ten years", 16, GREY_A),
                      tx("agreed to merge with Essential Utilities; closing expected by early 2027", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([2.6, -2.1, 0])
        src = source("American Water Works, Form 10-K 2025 (Kentucky rate case; capital plan; merger); Independent Water Commission (2025)", size=13)
        with self.voiceover(
            "America does the same arithmetic in fifty different rooms: its investor-owned water companies are "
            "regulated by state commissions, one rate case at a time. <bookmark mark='a'/> Here is one from American Water's 2025 report: its Kentucky "
            f"subsidiary, with a rate base of ${rb:,.0f} million. <bookmark mark='b'/> The commission assumed it was paid "
            f"for {100 * eq:.0f} per cent by shareholders and the rest by lenders. <bookmark mark='c'/> And it allowed the "
            f"shareholders a return of {100 * roe:.2f} per cent: about ${rb * eq * roe:,.0f} million a year on that slice. "
            f"<bookmark mark='d'/> England's regulator allows {G['roe']:.1f} per cent after inflation, about seven before "
            "it. <bookmark mark='e'/> American Water serves about "
            f"{E['people']:.0f} million people in {E['states']:.0f} states, plans to invest {E['capex10'][0]:.0f} to "
            f"{E['capex10'][1]:.0f} billion dollars over ten years, and has agreed to merge with Essential Utilities, "
            "another water company, in a deal it expects to close by early 2027."
        ) as vo:
            ghost = VGroup(box.copy().set_fill(opacity=0.12), tx("One American rate case", 22, WHITE, bold=True).to_edge(UP, buff=0.35))
            self.play(FadeIn(src), FadeIn(ghost))
            vo.wait_until("a")
            self.play(GrowFromCenter(box), FadeIn(box_l))
            vo.wait_until("b")
            self.play(GrowFromEdge(eq_r, DOWN), Create(split), FadeIn(eq_l), FadeIn(debt_l))
            vo.wait_until("c")
            self.play(FadeIn(calc, shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(comp, shift=LEFT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(firm, shift=UP * 0.1))
        self.clear_scene()

    def brazil(self):
        B = R["elsewhere"]["sbs"]
        before, after = B["before"] / 100, B["after"] / 100
        pie_r = 1.3
        t = ValueTracker(before)
        center = np.array([-4.3, 0.0, 0])
        state = always_redraw(lambda: AnnularSector(inner_radius=0, outer_radius=pie_r, angle=TAU * t.get_value(), start_angle=PI / 2,
                                                    fill_color=BR, fill_opacity=0.9, stroke_width=0).move_arc_center_to(center))
        rest = Circle(radius=pie_r, stroke_width=0, fill_color="#3A4152", fill_opacity=1).move_to(center)
        pct = draw.number(lambda: 100 * t.get_value(), 2, suffix="%", size=30, color=BR)
        pct.add_updater(lambda m: m.move_to(center + DOWN * (pie_r + 0.45)))
        pct.update()
        pie_l = VGroup(tx("the State of São Paulo's", 15, GREY_A), tx("share of Sabesp", 15, GREY_A)).arrange(DOWN, buff=0.03).next_to(rest, UP, buff=0.15)
        ys = (2023, 2024, 2025)
        sc = 3.0 / 16
        bars = VGroup()
        for i, y in enumerate(ys):
            v = B["capex"][y]
            b = Rectangle(width=0.8, height=v * sc, stroke_width=0, fill_color=BR, fill_opacity=0.85 if y < 2025 else 1.0).move_to([0.0 + 1.2 * i, -1.6, 0], aligned_edge=DOWN)
            bars.add(VGroup(b, tx(f"R${v:.1f}bn", 17, WHITE, bold=True).next_to(b, UP, buff=0.08), tx(str(y), 14, GREY_A).next_to(b, DOWN, buff=0.08)))
        bh = tx("Sabesp's investment", 16, GREY_A).move_to([1.2, 2.2, 0])
        mark = DashedLine([1.7, -1.9, 0], [1.7, 1.8, 0], stroke_color=PRICE, stroke_width=2, dash_length=0.08)
        mark_l = tx("privatized\nJuly 2024", 13, PRICE).next_to(mark, UP, buff=0.05)
        facts = VGroup(tx(f"water for {B['water']:.1f}m people,", 16, WHITE), tx(f"sewage for {B['sewer']:.1f}m", 16, WHITE),
                       tx(f"R${B['plan']:.0f}bn planned, 2024-2029", 16, BR, bold=True),
                       tx("99% water, 90% sewage:", 15, GREY_A), tx(f"due by {B['target']:.0f}, not 2033", 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([5.3, 0.1, 0])
        src = source("Sabesp, Form 20-F 2025 (privatization, investment, service targets)", size=13)
        with self.voiceover(
            "Brazil went the other way, recently. <bookmark mark='a'/> Sabesp supplies water to about "
            f"{B['water']:.0f} million people in the state of São Paulo. Until 2024, the state owned about half of it. "
            f"<bookmark mark='b'/> On the twenty-second of July 2024 it sold most of its shares, keeping "
            f"{100 * after:.0f} per cent, and signed a new concession that pulled forward the deadline for giving 99 "
            "per cent of the population water, and 90 per cent sewage treatment, from 2033 to 2029. "
            f"<bookmark mark='c'/> Watch the investment. About R${B['capex'][2023]:.1f} billion in 2023, "
            f"R${B['capex'][2024]:.1f} billion in 2024, <bookmark mark='d'/> and R${B['capex'][2025]:.1f} billion in "
            f"2025, more than double, with about R${B['plan']:.0f} billion planned by 2029. Private money, a deadline "
            "and a regulated return can build pipes quickly, if the bills can bear it."
        ) as vo:
            self.play(FadeIn(src), FadeIn(rest), FadeIn(pie_l))
            self.add(state, pct)
            vo.wait_until("b")
            self.play(t.animate.set_value(after), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(bh), Create(mark), FadeIn(mark_l))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2])) for b_ in bars[:2]], lag_ratio=0.4))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1]), FadeIn(bars[2][2]))
            self.play(FadeIn(facts, shift=LEFT * 0.1))
        pct.clear_updaters()
        self.clear_scene()
