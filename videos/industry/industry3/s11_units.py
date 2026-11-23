from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry3.common import *  # noqa: F403


def seat(h=1.6, color="#2B5D8C"):
    back = RoundedRectangle(corner_radius=0.18, width=0.9, height=h, fill_color=color, fill_opacity=1, stroke_width=0)
    cushion = RoundedRectangle(corner_radius=0.12, width=1.25, height=0.42, fill_color=color, fill_opacity=1,
                               stroke_width=0).next_to(back, DOWN, buff=-0.08).shift(RIGHT * 0.25)
    head = RoundedRectangle(corner_radius=0.1, width=0.7, height=0.3, fill_color="#3E7BB5", fill_opacity=1,
                            stroke_width=0).next_to(back, UP, buff=-0.12)
    legs = Line(cushion.get_bottom() + LEFT * 0.2, cushion.get_bottom() + LEFT * 0.2 + DOWN * 0.4, color=I.FAINT,
                stroke_width=4)
    return VGroup(legs, back, cushion, head)


class Units(VoiceoverScene):
    def construct(self):
        card(self, 9, "One seat, one member", "What does a company earn on a single unit of what it sells?",
             "Chapter nine. One seat, one member.", lit=("unit", "dollar"))
        self.seat_mile()
        self.amex()

    def seat_mile(self):
        D = R["delta"]
        S = D["seat"]
        st = seat().scale(1.1).move_to(LEFT * 4.9 + UP * 0.6)
        route = VGroup(TB("New York → Los Angeles", 19, I.TEXT), T(f"about {D['miles']:,} miles", 16, I.DIM)).arrange(
            DOWN, buff=0.05).next_to(st, DOWN, buff=0.35)
        L = 8.6
        other = S["cost"] - S["fuel"] - S["labor"]
        parts = [("people", S["labor"], "#7EC8F5"), ("fuel", S["fuel"], "#F2A65A"),
                 ("aircraft, airports, the rest", other, "#5B6578"), ("profit", S["revenue"] - S["cost"], I.PROFIT)]
        bar = VGroup()
        x = -2.9
        for lab, v, c in parts:
            w = L * v / S["revenue"]
            r = Rectangle(width=w, height=0.9, fill_color=c, fill_opacity=0.92, stroke_color=BACKGROUND,
                          stroke_width=1.2).move_to(np.array([x + w / 2, 0.6, 0]))
            t = VGroup(TB(f"${v:.0f}", 20, "#0E1117"), T(lab, 13, "#0E1117")).arrange(DOWN, buff=0.03)
            if t.width > w - 0.1:
                t.scale_to_fit_width(w - 0.1)
            bar.add(VGroup(r, t.move_to(r)))
            x += w
        top = TB(f"${S['revenue']:.0f} of revenue for each seat flown, full or empty", 22, I.MONEY).next_to(
            bar, UP, buff=0.3).align_to(bar, LEFT)
        rates = VGroup(T(f"revenue per seat mile: {D['trasm']:.2f}¢", 19, I.TEXT),
                       T(f"cost per seat mile: {D['casm']:.2f}¢", 19, I.TEXT),
                       T(f"margin: {D['margin']:.2f}¢ × {get('dal.asm') / 1e3:,.0f} billion seat miles = "
                         f"${D['check']:.1f}bn", 19, I.ACCENT),
                       T(f"Delta's reported operating income, 2025: ${get('dal.oi'):.1f}bn", 19, I.ACCENT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).next_to(bar, DOWN, buff=0.5).align_to(bar, LEFT)
        src = source("Delta Form 10-K 2025: TRASM, CASM, fuel, salaries, available seat miles; this film's arithmetic",
                     size=13)
        with self.voiceover(
            "Accounts become vivid when you divide them by the unit the business sells. For an airline, the unit "
            "is one seat flown one mile. <bookmark mark='a'/> In 2025 Delta took in "
            f"{D['trasm']:.2f} cents of revenue for every seat it flew a mile, full or empty, and spent "
            f"{D['casm']:.2f} cents. <bookmark mark='b'/> Take one seat from New York to Los Angeles, about two "
            f"thousand five hundred miles. It brings in about {say_usd(S['revenue'])}. <bookmark mark='c'/> About "
            f"{say_usd(S['labor'])} of that pays Delta's people, {say_usd(S['fuel'])} the fuel, and "
            f"{say_usd(other)} the aircraft, airports, maintenance and everything else. <bookmark mark='d'/> What is "
            f"left is about {say_usd(S['revenue'] - S['cost'])}. <bookmark mark='e'/> And the arithmetic rebuilds "
            f"the accounts: a margin of {D['margin']:.2f} cents, times the 298 billion seat miles Delta flew, is "
            f"{say_bn(D['check'])}, which is Delta's operating income for the year."
        ) as vo:
            self.play(FadeIn(st), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rates[0]), FadeIn(rates[1]))
            vo.wait_until("b")
            ny, la = np.array([-3.5, 2.35, 0]), np.array([-6.5, 2.35, 0])
            path = ArcBetweenPoints(ny, la, angle=0.9)
            ends = VGroup(Dot(ny, radius=0.06, color=I.TEXT), Dot(la, radius=0.06, color=I.TEXT),
                          T("New York", 14, I.DIM).next_to(ny, DOWN, buff=0.08),
                          T("Los Angeles", 14, I.DIM).next_to(la, DOWN, buff=0.08))
            trail = DashedVMobject(path.copy().set_stroke(I.DIM, 1.5), num_dashes=24)
            jet = draw.plane(0.9, windows=False).flip().move_to(ny)  # nose west
            self.play(FadeIn(route), FadeIn(top), FadeIn(ends), Create(trail))
            self.play(MoveAlongPath(jet, path), run_time=2.4, rate_func=smooth)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], LEFT), FadeIn(b[1])) for b in bar[:3]],
                                  lag_ratio=0.3), run_time=1.6)
            vo.wait_until("d")
            self.play(GrowFromEdge(bar[3][0], LEFT), FadeIn(bar[3][1]))
            vo.wait_until("e")
            self.play(FadeIn(rates[2]), FadeIn(rates[3]))
        self.clear_scene()

    def amex(self):
        D = R["delta"]
        S = D["seat"]
        L = 6.0
        mx = max(S["amex"], S["revenue"] - S["cost"])
        a = Rectangle(width=L * S["amex"] / mx, height=0.8, fill_color="#4FA3F7", fill_opacity=0.9, stroke_width=0)
        m = Rectangle(width=L * (S["revenue"] - S["cost"]) / mx, height=0.8, fill_color=I.PROFIT, fill_opacity=0.9,
                      stroke_width=0)
        a.move_to(np.array([-2.0, 0.9, 0]), aligned_edge=LEFT)
        m.move_to(np.array([-2.0, -0.4, 0]), aligned_edge=LEFT)
        la = VGroup(TB("American Express", 22, "#4FA3F7"), T("paid to Delta, per seat", 16, I.DIM)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.03).next_to(a, LEFT, buff=0.3)
        lm = VGroup(TB("Delta's margin", 22, I.PROFIT), T("per seat, after all costs", 16, I.DIM)).arrange(
            DOWN, aligned_edge=RIGHT, buff=0.03).next_to(m, LEFT, buff=0.3)
        va = TB(f"${S['amex']:.0f}", 26, "#4FA3F7").next_to(a, RIGHT, buff=0.15)
        vm = TB(f"${S['revenue'] - S['cost']:.0f}", 26, I.PROFIT).next_to(m, RIGHT, buff=0.15)
        tot = VGroup(T(f"2025: American Express paid ${get('dal.amex'):.1f}bn, up 11%", 19, I.TEXT),
                     T(f"Delta's operating income: ${get('dal.oi'):.1f}bn", 19, I.TEXT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_edge(DOWN, buff=0.8)
        head = T("The same seat, New York to Los Angeles", 24, I.TEXT).to_edge(UP, buff=0.4)
        src = source("Delta Form 10-K 2025: remuneration from American Express; per seat by this film's arithmetic",
                     size=13)
        with self.voiceover(
            "Now one more line from Delta's accounts. <bookmark mark='a'/> Every time someone pays with a Delta "
            "SkyMiles card, American Express buys miles from Delta to give its cardholders, with marketing and other "
            "benefits in the same contract. In 2025 "
            f"those payments came to {say_bn(get('dal.amex'))}, up eleven percent, and Delta expects ten billion "
            f"within a few years. <bookmark mark='b'/> Spread over every seat it flew, that is about "
            f"{say_usd(S['amex'])} on our seat to Los Angeles, <bookmark mark='c'/> more than the "
            f"{say_usd(S['revenue'] - S['cost'])} the airline kept from it after all its costs. Delta's accounts "
            "describe an airline; they also describe a loyalty business attached to one, which sells miles to a "
            "bank. That is unit economics: divide by the right unit, and the business underneath shows through."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(tot[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(a, LEFT), FadeIn(la), FadeIn(va))
            vo.wait_until("c")
            self.play(GrowFromEdge(m, LEFT), FadeIn(lm), FadeIn(vm), FadeIn(tot[1]))
        self.clear_scene()
