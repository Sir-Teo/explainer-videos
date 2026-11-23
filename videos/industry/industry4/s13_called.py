from __future__ import annotations

from explainer.industry.calls import calls
from videos.industry.industry4.common import *  # noqa: F403

SOLAR, COAL = TECH["solar"], TECH["coal"]


class Called(VoiceoverScene):
    def construct(self):
        card(self, 12, "Called it?", "Did the forecasters see the cost curve coming?",
             "Chapter twelve. Called it?", lit=("next",))
        self.iea()
        self.ours()

    def iea(self):
        C = R["called"]
        cap = R["solar"]["capacity"]
        ax = CornerAxes(x_range=[2005, 2051, 5], y_range=[0, 3200, 500], x_length=10.2, y_length=4.8,
                        axis_config=dict(color=GREY_B, include_ticks=False)).move_to([0.3, -0.4, 0])
        xt = VGroup(*[tx(f"{y}", 17, GREY_B).next_to(ax.c2p(y, 0), DOWN, buff=0.08) for y in (2010, 2020, 2030, 2040, 2050)])
        yt = VGroup(*[tx(f"{v:,}", 17, GREY_B).next_to(ax.c2p(2005, v), LEFT, buff=0.08) for v in (1000, 2000, 3000)])
        yl = tx("world solar capacity, gigawatts", 18, GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        road = [(2010, cap[2010]), (2020, C["iea_2020"]), (2030, 900), (2040, C["iea_2040"]), (2050, 3000)]
        iea = DashedVMobject(VMobject(stroke_color=GREY_A, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, v) for x, v in road]), num_dashes=40)
        iea_dots = VGroup(*[Dot(ax.c2p(x, v), radius=0.06, color=GREY_A) for x, v in road[1:]])
        iea_t = tx("the IEA's 2010 roadmap", 19, GREY_A).move_to(ax.c2p(2045, 1500), aligned_edge=LEFT)
        yrs = [y for y in sorted(cap) if y >= 2005]
        t = ValueTracker(2005)

        def actual():
            pts = [ax.c2p(y, cap[y]) for y in yrs if y <= t.get_value()]
            if len(pts) < 2:
                pts = pts + pts
            return VMobject(stroke_color=SOLAR, stroke_width=5).set_points_as_corners(pts)
        line = always_redraw(actual)
        head_dot = always_redraw(lambda: glow_dot(ax.c2p(max(y for y in yrs if y <= t.get_value()),
                                                         cap[max(y for y in yrs if y <= t.get_value())]),
                                                  color=SOLAR, radius=0.09))
        act_t = tx("what was built", 19, SOLAR, bold=True).next_to(ax.c2p(2025, cap[2025]), LEFT, buff=0.3)
        src = source("IEA, Technology Roadmap: Solar PV Energy (2010); IRENA via Our World in Data")
        with self.voiceover(
            "Every part ends by checking forecasts. This one has a famous pair. <bookmark mark='a'/> In 2010 the "
            "International Energy Agency published a roadmap for solar power. It was meant to be ambitious: world "
            "capacity could reach two hundred gigawatts by 2020, nine hundred by 2030 and two thousand by 2040. "
            "<bookmark mark='b'/> Here is what was built. <bookmark mark='c'/> By 2020 the world had over seven "
            "hundred gigawatts, more than three times the roadmap. <bookmark mark='d'/> By 2025, about two thousand "
            "four hundred: the roadmap's figure for 2040, fifteen years early."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(yl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(iea), FadeIn(iea_dots), FadeIn(iea_t), run_time=2.0)
            vo.wait_until("b")
            self.add(line, head_dot)
            self.play(t.animate.set_value(2015), run_time=2.0, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(2020), run_time=1.5, rate_func=linear)
            gap = DoubleArrow(ax.c2p(2020, C["iea_2020"]), ax.c2p(2020, C["actual_2020"]), buff=0.05, color=PRICE,
                              stroke_width=3, tip_length=0.15)
            self.play(GrowFromCenter(gap))
            vo.wait_until("d")
            self.play(t.animate.set_value(2025), run_time=2.0, rate_func=linear)
            arr = Arrow(ax.c2p(2040, C["iea_2040"]), ax.c2p(2025.6, C["actual_2025"]), buff=0.12, color=PRICE,
                        stroke_width=4)
            early = tx("15 years early", 22, PRICE, bold=True).next_to(arr, UP, buff=0.05)
            self.play(GrowArrow(arr), FadeIn(early), FadeIn(act_t))
        why = tx("They forecast the market. The learning curve moved the cost.", 24, WHITE, bold=True).to_edge(
            DOWN, buff=0.2)
        with self.voiceover(
            "Why so wrong? Not for lack of expertise. The roadmap assumed costs would fall, but not as fast as they "
            "did, and it did not let the falling cost feed back into demand. Each doubling made panels cheaper; "
            "cheaper panels sold more; more panels made the next doubling come sooner. Forecasts of solar have "
            "erred in the same direction again and again. When an industry rides a learning curve, the safe bet is "
            "that the curve keeps going."
        ):
            self.play(FadeOut(src), FadeIn(why, shift=UP * 0.1))
        self.clear_scene()

    def ours(self):
        C = R["called"]
        call = calls(4, ours=True)[0]
        head = tx("This part's call", 30, PRICE, bold=True).to_edge(UP, buff=0.35)
        claim = tx("In at least one month of 2027, America's solar farms\nwill make more electricity than its coal plants.",
                   28, WHITE).next_to(head, DOWN, buff=0.35)
        prob = tx("Probability: 55%.  Due: March 2028.", 22, GREY_A).next_to(claim, DOWN, buff=0.2)
        base = -3.0
        u = 0.0036

        def bar(x, v, col, name):
            r_ = Rectangle(width=1.1, height=v * u, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                [x, base, 0], aligned_edge=DOWN)
            return VGroup(r_, tx(f"{v:.0f}", 19, col, bold=True).next_to(r_, UP, buff=0.06),
                          tx(name, 16, GREY_B).next_to(r_, DOWN, buff=0.08))
        a = VGroup(bar(-4.6, C["coal_2025"], COAL, "coal"), bar(-3.3, C["solar_2025"], SOLAR, "solar"),
                   tx("2025", 22, WHITE, bold=True).move_to([-3.95, 0.4, 0]))
        b = VGroup(bar(-0.65, C["coal_2027"], COAL, "coal"), bar(0.65, C["solar_2027"], SOLAR, "solar"),
                   tx("2027, EIA's forecast", 22, WHITE, bold=True).move_to([0, 0.4, 0]))
        q2c, q2s = 135.0, C["q2_2027"]
        u2 = u * 3
        c = VGroup(bar(3.3, q2c, COAL, "coal"), bar(4.6, q2s, SOLAR, "solar"),
                   tx("April to June 2027", 22, WHITE, bold=True).move_to([3.95, 0.4, 0]))
        for g_, v in zip(c[:2], (q2c, q2s)):
            g_[0].stretch_to_fit_height(v * u2, about_edge=DOWN)
            g_[1].next_to(g_[0], UP, buff=0.06)
        unit = tx("terawatt-hours (the right-hand pair drawn three times taller)", 16, GREY_B).to_corner(DR, buff=0.28)
        src = source("EIA, Short-Term Energy Outlook, November 2026, Table 7d: forecasts, not outcomes", corner=DL)
        with self.voiceover(
            "And this part's own call, on the record. <bookmark mark='a'/> In at least one month of 2027, America's "
            "utility-scale solar farms will generate more electricity than its coal plants. <bookmark mark='b'/> In "
            f"2025 coal still made {C['coal_2025']:.0f} terawatt-hours against solar's {C['solar_2025']:.0f}. "
            "<bookmark mark='c'/> The Energy Information Administration expects about forty percent more solar by "
            "2027, as seventy gigawatts of new panels come on line, and less coal. <bookmark mark='d'/> Over the "
            f"whole of April to June 2027, it expects {q2s:.0f} terawatt-hours of solar against {q2c:.0f} of coal: "
            "close. Spring is when the sun climbs and coal plants close for maintenance, so a single month, April or "
            "May, could tip. We put it at fifty-five percent, a little better than a coin toss, and it will be "
            "scored on the final 2027 figures."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(claim), FadeIn(prob))
            vo.wait_until("b")
            self.play(GrowFromEdge(a[0][0], DOWN), GrowFromEdge(a[1][0], DOWN), FadeIn(a[0][1:]), FadeIn(a[1][1:]),
                      FadeIn(a[2]), FadeIn(src))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[0][0], DOWN), GrowFromEdge(b[1][0], DOWN), FadeIn(b[0][1:]), FadeIn(b[1][1:]),
                      FadeIn(b[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(c[0][0], DOWN), GrowFromEdge(c[1][0], DOWN), FadeIn(c[0][1:]), FadeIn(c[1][1:]),
                      FadeIn(c[2]), FadeIn(unit))
        del call
        self.clear_scene()
