from __future__ import annotations

from explainer.industry.register import get
from videos.industry.industry8.common import *  # noqa: F403


class Decline(VoiceoverScene):
    def construct(self):
        card(self, 3, "A well, and how it fades", "Why must an oil company keep drilling just to stand still?",
             "Chapter three. A well, and how it fades.", lit=("make", "change"))
        self.spindletop()
        self.curves()
        self.treadmill()

    def spindletop(self):
        rig = draw.derrick(2.6, color="#C9A26B").move_to([-4.3, -0.6, 0])
        ground = Line([-6.6, -1.9, 0], [-2.0, -1.9, 0], stroke_color="#7A6A50", stroke_width=3)
        top = rig.get_top()
        rng = np.random.default_rng(1)
        jet = VGroup(*[Dot(top + [rng.normal(0, 0.06), 0, 0], radius=0.05 + 0.03 * rng.random(), color=CRUDE)
                       for _ in range(60)])
        t = ValueTracker(0)

        def spray(m):
            tt = t.get_value()
            for k, d_ in enumerate(m):
                ph = (tt * 1.3 + k / len(m)) % 1.0
                x = top[0] + (k % 7 - 3) * 0.05 * ph * 4
                y = top[1] + 2.6 * ph - 2.2 * ph * ph
                d_.move_to([x, y, 0]).set_opacity(1 - 0.6 * ph)
        jet.add_updater(spray)
        flow_ = get("spindletop.flow")
        y02 = get("spindletop.1902") * 1e6 / 365
        bars = VGroup()
        vals = [(f"Jan 1901, the gusher", flow_), ("1902, the field's average", y02), ("Feb 1904, the field", 10000)]
        for k, (lab, v) in enumerate(vals):
            b = Rectangle(width=0.9, height=3.2 * v / flow_, stroke_width=0, fill_color=CRUDE,
                          fill_opacity=0.9).move_to([0.4 + 2.2 * k, -1.9, 0], aligned_edge=DOWN)
            n = tx(f"{v:,.0f} b/d", 18, WHITE, bold=True).next_to(b, UP, buff=0.1)
            l_ = VGroup(*[tx(w, 14, GREY_B) for w in lab.split(", ")]).arrange(DOWN, buff=0.03).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, n, l_))
        who = VGroup(tx("born or grown at Spindletop:", 15, GREY_B),
                     tx("the Texas Company (Texaco), Gulf Oil, Humble (later Exxon's US arm)", 15, GREY_A)
                     ).arrange(DOWN, buff=0.04).to_edge(UP, buff=0.4).shift(RIGHT * 1.5)
        src = source("Handbook of Texas Online (Texas State Historical Association), 'Spindletop Oilfield'; this film's "
                     "division of 1902's 17.5 million barrels by 365", size=13)
        with self.voiceover(
            "On the tenth of January 1901, near Beaumont, Texas, a well at a hill called Spindletop blew six tons of "
            "drilling pipe out of the ground, and then oil, a hundred feet into the air. <bookmark mark='a'/> It "
            "flowed, by one estimate, a hundred thousand barrels a day until it was capped nine days later. "
            "<bookmark mark='b'/> Hundreds of wells followed it onto the hill. In 1902 the field produced seventeen and "
            "a half million barrels, about forty-eight thousand a day. <bookmark mark='c'/> By February 1904 it was "
            "down to ten thousand. <bookmark mark='d'/> Some of the biggest names in oil were born or grew up there: "
            "the Texas Company, later Texaco, Gulf Oil, and Humble, which became part of Exxon. And the first lesson "
            "of the oil business was learned there too: every well fades."
        ) as vo:
            self.play(FadeIn(src), Create(ground), FadeIn(rig, shift=UP * 0.2))
            self.add(jet)
            self.play(t.animate.set_value(3), run_time=3, rate_func=linear)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]), t.animate.set_value(5), rate_func=linear)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]), t.animate.set_value(7), rate_func=linear)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0], DOWN), FadeIn(bars[2][1:]), jet.animate.set_opacity(0.2), rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(who))
        jet.clear_updaters()
        self.clear_scene()

    def curves(self):
        T = R["treadmill"]
        well, conv = np.array(T["well"]), np.array(T["conv"])
        P = R["cost"]["prospects"]
        pa = viz.plot_axes([0, 60], [0, 110], x_length=8.4, y_length=4.2, xticks=[0, 12, 24, 36, 48, 60],
                           yticks=[25, 50, 75, 100], xfmt=lambda v: f"{int(v) // 12} yr" if v else "0",
                           yfmt=lambda v: f"{v:g}%", size=14)
        pa.move_to([0.6, -0.4, 0])
        lc = VMobject(stroke_color=GAS, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(m, 100 * v / conv[0]) for m, v in enumerate(conv)])
        ls = VMobject(stroke_color=SHALE, stroke_width=4).set_points_smoothly(
            [pa.ax.c2p(m, 100 * v / well[0]) for m, v in enumerate(well)])
        tc = tx(f"conventional well: -{100 * P[0]['decline']:.0f}% in year one", 18, GAS, bold=True).next_to(
            pa.ax.c2p(36, 100 * conv[36] / conv[0]), UP, buff=0.15)
        ts = tx(f"shale well: -{100 * P[2]['decline']:.0f}% in year one", 18, SHALE, bold=True).next_to(
            pa.ax.c2p(24, 100 * well[24] / well[0]), UP, buff=0.3).shift(RIGHT * 0.8)
        head = tx("Output of one well, as a share of its first day", 18, GREY_A).next_to(pa, UP, buff=0.15).align_to(pa, LEFT)
        eq = MathTex(r"q(t) = \frac{q_0}{(1 + b\,D\,t)^{1/b}}", font_size=34).to_corner(UR, buff=0.6)
        eql = tx(f"Arps ({get('arps.1945'):.0f}): how wells decline", 15, GREY_B).next_to(eq, DOWN, buff=0.1)
        tag = estimate_tag("the Works' model wells", corner=DR, size=14)
        with self.voiceover(
            "Oil flows because the rock is under pressure, and every barrel that comes out lets a little of the "
            "pressure go. So a well's output falls, fast at first and then more slowly. In 1945 an engineer, J. J. "
            "Arps, wrote down the curve that petroleum engineers still use. <bookmark mark='a'/> A conventional well "
            "into a big, porous reservoir fades gently: in our model, by about a tenth in its first year. "
            "<bookmark mark='b'/> A shale well is different. The rock is so tight that the oil comes mostly from the "
            "cracks that were made, close to the well, and once that is drained the flow drops. Our model shale well "
            f"loses {100 * P[2]['decline']:.0f} percent of its output in its first year, and keeps falling."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(head), FadeIn(tag), Write(eq), FadeIn(eql))
            vo.wait_until("a")
            self.play(Create(lc), run_time=2.0)
            self.play(FadeIn(tc))
            vo.wait_until("b")
            self.play(Create(ls), run_time=2.0)
            self.play(FadeIn(ts))
        self.clear_scene()

    def treadmill(self):
        T = R["treadmill"]
        hold, stop = np.array(T["hold"]) / 1e6, np.array(T["stop"]) / 1e6
        months = len(hold)
        pa = viz.plot_axes([0, months], [0, 1.2], x_length=7.0, y_length=3.6, xticks=[0, 12, 24, 36, 48, 60, 72],
                           yticks=[0.5, 1.0], xfmt=lambda v: f"{int(v) // 12} yr" if v else "now",
                           yfmt=lambda v: f"{v:g}m b/d", size=14)
        pa.move_to([2.2, -0.6, 0])
        t1, t2 = ValueTracker(0), ValueTracker(0)

        def line(series, col, t):
            def make():
                k = int(t.get_value())
                pts = [pa.ax.c2p(m, series[m]) for m in range(0, max(k, 1) + 1)]
                return VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(pts)
            return always_redraw(make)
        lh = line(hold, SHALE, t1)
        ls = line(stop, STATE, t2)
        rigs = VGroup(*[draw.derrick(0.45, color=SHALE) for _ in range(12)]).arrange_in_grid(rows=3, cols=4, buff=0.15)
        rigs.move_to([-4.6, 0.6, 0])
        need = VGroup(tx(f"{T['wells']:.0f} new wells a month", 22, SHALE, bold=True),
                      tx("just to hold a million barrels a day", 16, GREY_A)).arrange(DOWN, buff=0.06).next_to(
            rigs, DOWN, buff=0.3)
        fall = tx(f"stop drilling: {100 * T['stop_12']:.0f}% in a year", 20, STATE, bold=True).move_to([2.6, 1.7, 0])
        tag = estimate_tag("the Works' model basin of shale wells", corner=DR, size=14)
        with self.voiceover(
            "Put thousands of such wells together and you have a treadmill. <bookmark mark='a'/> To hold a shale "
            f"basin at a million barrels a day, our model needs about {T['wells']:.0f} new wells every month, for "
            "ever, each one replacing the fading output of the ones before. <bookmark mark='b'/> Stop drilling, and "
            f"output falls by about {abs(100 * T['stop_12']):.0f} percent within a year, and keeps falling. "
            "<bookmark mark='c'/> That is the shale business: less like mining a deposit, more like running a factory "
            "whose product evaporates. It is also why shale can respond to prices within months, in both directions, "
            "as Chapter 11 shows."
        ) as vo:
            self.play(FadeIn(pa), FadeIn(tag), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in rigs], lag_ratio=0.08))
            self.add(lh)
            vo.wait_until("a")
            self.play(FadeIn(need), t1.animate.set_value(months - 1), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.add(ls)
            self.play(rigs.animate.set_opacity(0.15), t2.animate.set_value(months - 1), run_time=4.0, rate_func=linear)
            self.play(FadeIn(fall))
            vo.wait_until("c")
            self.play(Indicate(fall, color=WHITE))
        for m in (lh, ls):
            m.clear_updaters()
        self.clear_scene()
