from __future__ import annotations

from videos.economics.econ2.common import *  # noqa: F403


class Elasticity(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Elasticity", r"How much do people respond when a price changes?",
             "Chapter six. Elasticity.", scale=("person", "market"), horizon=("a day", "a year"))
        self.define()
        self.along()
        self.midpoint()
        self.runs()

    # ------------------------------------------------------------------
    def define(self):
        eq = MathTex(r"\varepsilon \;=\; \frac{\%\ \text{change in quantity}}{\%\ \text{change in price}}",
                     font_size=52).to_edge(UP, buff=0.6)
        ax = price_axes(10, (0, 5), x_length=6.2, y_length=4.0, qticks=None, pticks=None, qlabel=r"quantity",
                        plabel=r"price", center=LEFT * 3.0 + DOWN * 1.0)
        a = ax.ax
        steep = line_on(a, 4.2, 4.6, 5.8, 0.4, E.DEMAND)
        flat = line_on(a, 0.6, 3.1, 9.4, 1.9, E.ACCENT)
        pt = Dot(a.c2p(5.0, 2.5), radius=0.08, color=WHITE)
        ls = label(r"steep: \ inelastic", font_size=24, color=E.DEMAND).next_to(a.c2p(5.8, 0.4), RIGHT, buff=0.15)
        lf = label(r"flat: \ elastic", font_size=24, color=E.ACCENT).next_to(a.c2p(9.4, 1.9), UP, buff=0.15)
        ex = VGroup(
            label(r"the price rises 10\%", font_size=28, color=WHITE),
            label(r"insulin, \ or petrol this month: \ $-2\%$ \ \ ($\varepsilon = -0.2$)", font_size=24, color=E.DEMAND),
            label(r"one brand of cereal: \ $-30\%$ \ \ ($\varepsilon = -3$)", font_size=24, color=E.ACCENT),
            label(r"below 1 in size: \ inelastic; \ above 1: \ elastic", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.6)
        tag = illustrative_tag(corner=DR, font_size=17)
        units = label(r"percentages: \ litres or gallons, \ dollars or yen, \ the same answer", font_size=26,
                      color=GREY_A).next_to(eq, DOWN, buff=0.5)
        with self.voiceover(
            "A demand curve says that people buy less when a price rises. Elasticity says how much less. "
            "<bookmark mark='a'/> It's the percentage change in the quantity bought, divided by the percentage "
            "change in the price that caused it. Percentages, so that it doesn't matter whether you count in "
            "litres or gallons, dollars or yen. <bookmark mark='b'/> Through the same point you can draw a steep "
            "demand curve or a flat one. <bookmark mark='c'/> Raise the price ten percent. For something people "
            "can't easily do without, insulin, or petrol this month, purchases might fall two percent: an "
            "elasticity of minus point two. For one brand of cereal on a shelf full of others, they might fall "
            "thirty percent: minus three. <bookmark mark='d'/> Below one in size, demand is called inelastic; above "
            "one, elastic."
        ) as vo:
            self.play(Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(units, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeOut(units), FadeIn(ax), FadeIn(pt), FadeIn(tag))
            self.play(Create(steep), FadeIn(ls))
            self.play(Create(flat), FadeIn(lf))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in ex[:3]], lag_ratio=0.6), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(ex[3]))
        self.clear_scene()

    def along(self):
        f = load("fish")
        e = load("elasticity")
        L = Linear(**f["line"])
        choke = L.choke
        ax = price_axes(400, (0, 6), x_length=6.6, y_length=4.6, qticks=[0, 100, 200, 300, 400], pticks=[0, 1, 2, 3, 4, 5, 6],
                        qlabel=r"fish bought in a day", plabel=r"price of a fish", center=LEFT * 2.9 + DOWN * 0.35)
        a = ax.ax
        dem = line_on(a, 0, choke, L.a, 0, E.DEMAND)
        truth = DashedLine(a.c2p(0, choke), a.c2p(L.a, 0), color=E.TRUTH, stroke_width=2).set_opacity(0.0)
        p = ValueTracker(5.2)

        def qof(x):
            return float(L.qd(x))

        rect = always_redraw(lambda: Rectangle(width=a.c2p(qof(p.get_value()), 0)[0] - a.c2p(0, 0)[0],
                                               height=a.c2p(0, p.get_value())[1] - a.c2p(0, 0)[1], stroke_width=0,
                                               fill_color=E.ACCENT, fill_opacity=0.28)
                             .move_to((a.c2p(0, 0) + a.c2p(qof(p.get_value()), p.get_value())) / 2))
        dot = always_redraw(lambda: Dot(a.c2p(qof(p.get_value()), p.get_value()), radius=0.08, color=WHITE))
        read = always_redraw(lambda: VGroup(
            label(rf"price \ {dollars(p.get_value())}", font_size=26, color=WHITE),
            label(rf"elasticity \ {(-L.b * p.get_value() / max(qof(p.get_value()), 1e-9)):.2f}".replace("-", "$-$"),
                  font_size=26, color=E.DEMAND),
            label(rf"spending \ {dollars(p.get_value() * qof(p.get_value()), 0)} a day", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.6).shift(DOWN * 0.6))
        # spending as a curve, beneath the read-out
        rax = price_axes(6, (0, 650), x_length=4.2, y_length=2.2, qticks=[0, 3, 6], pticks=[0, 600], qlabel=r"price",
                         plabel=r"spending", money=False, font_size=17)
        rax.to_corner(DR, buff=0.5)
        ra = rax.ax
        rc = VMobject(stroke_color=E.ACCENT, stroke_width=3).set_points_smoothly(
            [ra.c2p(x, float(x * L.qd(x))) for x in np.linspace(0.05, choke - 0.02, 60)])
        peak = Dot(ra.c2p(choke / 2, choke / 2 * float(L.qd(choke / 2))), radius=0.06, color=E.ACCENT)
        unit = label(rf"elasticity $-1$ \ at {dollars(choke / 2)}: \ spending is greatest", font_size=22,
                     color=E.ACCENT).next_to(rax, UP, buff=0.2).align_to(rax, RIGHT)
        tag = island_tag(r"simulated: the Island's fish market (planted line)", corner=DL, font_size=16)
        with self.voiceover(
            "Elasticity isn't the slope of a curve, and it changes as you move along one. Here is the planted demand "
            "line of the Island's fish market. <bookmark mark='a'/> Near the top, at five dollars and more, few "
            "fish are bought, so a small price cut is a big percentage gain in sales: demand is elastic. "
            "<bookmark mark='b'/> Slide down the line and the elasticity falls in size, though the slope never "
            "changes. <bookmark mark='c'/> The shaded rectangle is the price times the quantity: what buyers "
            "spend, and what sellers take in. While demand is elastic, cutting the price raises spending. "
            f"<bookmark mark='d'/> At {money_words(choke / 2)}, halfway down, the elasticity is exactly minus one, "
            "and spending is as large as it gets. <bookmark mark='e'/> Below that, demand is inelastic, and every "
            "cut in price takes in less. That's why a seller with any choice over his price never sets it where "
            "demand is inelastic, a fact Part ten will put to work."
        ) as vo:
            self.play(FadeIn(ax), Create(dem), FadeIn(tag))
            self.add(rect, dot)
            self.play(FadeIn(read))
            self.add(read)
            vo.wait_until("a")
            self.play(p.animate.set_value(4.6), run_time=2)
            vo.wait_until("b")
            self.play(p.animate.set_value(3.8), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rax), Create(rc), run_time=1.5)
            vo.wait_until("d")
            self.play(p.animate.set_value(choke / 2), run_time=2)
            self.play(FadeIn(peak, scale=0.5), FadeIn(unit))
            vo.wait_until("e")
            self.play(p.animate.set_value(1.2), run_time=3)
        rect.clear_updaters()
        dot.clear_updaters()
        read.clear_updaters()
        self.clear_scene()

    def midpoint(self):
        e = load("elasticity")
        f = load("fish")
        (q0, p0), (q1, p1) = e["calm"], e["storm"]
        rows = VGroup(
            label(rf"calm days: \ {q0:.0f} fish at {dollars(p0)}", font_size=28, color=E.FISH),
            label(rf"stormy days: \ {q1:.0f} fish at {dollars(p1)}", font_size=28, color=STORM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.6)
        up = MathTex(rf"\text{{calm}}\to\text{{storm}}:\quad \frac{{{100 * (q1 - q0) / q0:.1f}\%}}"
                     rf"{{+{100 * (p1 - p0) / p0:.1f}\%}} = {e['naive_up']:.2f}", font_size=36)
        down = MathTex(rf"\text{{storm}}\to\text{{calm}}:\quad \frac{{+{100 * (q0 - q1) / q1:.1f}\%}}"
                       rf"{{{100 * (p0 - p1) / p1:.1f}\%}} = {e['naive_down']:.2f}", font_size=36)
        mid = MathTex(r"\text{midpoint}:\quad \frac{\Delta Q\,/\,\bar Q}{\Delta P\,/\,\bar P} = "
                      + f"{e['arc']:.2f}", font_size=40, color=E.ACCENT)
        VGroup(up, down, mid).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(rows, DOWN, buff=0.6)
        for m in (up, down):
            m.set_color(GREY_A)
        truth = label(rf"the planted line, over this stretch: \ from {f['elasticity_true']['demand']:.2f} at the calm "
                      rf"price to {(-Linear(**f['line']).b * p1 / float(Linear(**f['line']).qd(p1))):.2f} at the "
                      r"stormy one".replace("-", "$-$"), font_size=22, color=E.TRUTH).to_edge(DOWN, buff=0.7)
        tag = island_tag(rf"simulated: the Island, {len(f['days'])} market days, {f['n_storms']} with storms",
                         corner=DR, font_size=16)
        with self.voiceover(
            "In practice you rarely have a curve. You have two points, and the answer depends on which you start "
            "from. <bookmark mark='a'/> On the Island, storms keep a third of the boats ashore. On calm days the "
            f"market sells about {q0:.0f} fish at {money_words(p0)}; on stormy days, {q1:.0f} at "
            f"{money_words(p1)}. <bookmark mark='b'/> Going from calm to storm, quantity falls "
            f"{100 * (q0 - q1) / q0:.0f} percent and the price rises {100 * (p1 - p0) / p0:.0f} percent: an "
            f"elasticity of {say_num(e['naive_up'])}. Going back, from storm to calm, the same two points give "
            f"{say_num(e['naive_down'])}. <bookmark mark='c'/> The fix is to measure each change against the average "
            f"of the two points. This midpoint formula gives {say_num(e['arc'])} in both directions. "
            "<bookmark mark='d'/> And on the Island we can check it against the truth. Along this stretch of the "
            "planted line the elasticity runs from about minus point nine to minus one point four, and the "
            "midpoint number sits inside that range. Notice what made this work: the storms moved supply, and "
            "the price slid along demand. Part four is about when that trick is safe."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1), FadeIn(rows[1], shift=RIGHT * 0.1))
            vo.wait_until("b")
            self.play(Write(up))
            self.play(Write(down))
            vo.wait_until("c")
            self.play(Write(mid))
            vo.wait_until("d")
            self.play(FadeIn(truth, shift=UP * 0.1))
        self.clear_scene()

    def runs(self):
        dial = dials.DIALS["elasticity_staples"]
        sr = next(x for x in dial.estimates if "short run" in x.sample)
        lr = next(x for x in dial.estimates if "long run" in x.sample)
        ax = price_axes(2, (0, 0.4), x_length=5.2, y_length=3.8, qticks=None, pticks=[0, 0.1, 0.2, 0.3, 0.4],
                        qlabel="", plabel=r"elasticity of petrol demand, \ in size", money=False,
                        center=LEFT * 2.8 + DOWN * 0.4)
        a = ax.ax
        bars = VGroup()
        for k, (est, name) in enumerate(((sr, r"a year or less"), (lr, r"the long run"))):
            b = Rectangle(width=1.2, height=a.c2p(0, abs(est.value))[1] - a.c2p(0, 0)[1], stroke_width=0,
                          fill_color=E.DEMAND if k == 0 else E.ACCENT, fill_opacity=0.8)
            b.move_to((a.c2p(k + 0.5, 0) + a.c2p(k + 0.5, abs(est.value))) / 2)
            v = label(f"${est.value:.2f}$".replace("-", "-"), font_size=26, color=WHITE).next_to(b, UP, buff=0.1)
            n = label(name, font_size=22, color=GREY_A).next_to(a.c2p(k + 0.5, 0), DOWN, buff=0.2)
            bars.add(VGroup(b, v, n))
        why = VGroup(
            label(r"this month: \ the same car, \ the same commute", font_size=24, color=E.DEMAND),
            label(r"over years: \ a smaller car, \ a closer job, \ a bus pass", font_size=24, color=E.ACCENT),
            label(r"published averages were about twice as large: \ a bias Part 4 explains", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        src = published_tag(r"Havranek, Irsova and Janda (2012), \emph{Energy Economics} 34: 201--207, "
                            r"corrected for publication bias", corner=DL, font_size=16)
        with self.voiceover(
            "Elasticities grow with time. <bookmark mark='a'/> In 2012 three economists in Prague, Tomas Havranek, "
            "Zuzana Irsova and Karel Janda, pooled the published estimates for petrol. Corrected for a bias in "
            f"which estimates get published, the average short-run elasticity was {say_num(sr.value)}, close to nothing. "
            f"<bookmark mark='b'/> In the long run it was {say_num(lr.value)}, more than three times as large. "
            "<bookmark mark='c'/> This month you have the same car and the same commute. Over years you can buy a "
            "smaller car, move closer to work, or take the bus. <bookmark mark='d'/> They also found that the "
            "average published estimate was about twice the corrected one: studies that found a strong response "
            "were more likely to be published. Part four is about how that happens, and how to correct for it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(src))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], DOWN), FadeIn(bars[0][1:]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]))
            vo.wait_until("c")
            self.play(FadeIn(why[0], shift=LEFT * 0.1), FadeIn(why[1], shift=LEFT * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(why[2]))
        self.clear_scene()
