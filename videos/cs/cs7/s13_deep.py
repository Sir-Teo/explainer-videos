from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import CLOCK, HEAD, NO, PART, YES, chapter, load


class Deep(WatchScene):
    def construct(self):
        chapter(self, 12, r"Deeper, and the end of the race", r"Why did clocks stop getting faster?",
                lit=(2000, 2004), extra=((2000, r"Pentium 4: 20 stages"), (2004, r"31 stages; Tejas cancelled")))
        self.myth()
        self.depth()
        self.race()
        self.power()

    # ------------------------------------------------------------------
    def myth(self):
        self.wrong_idea(r"A deeper pipeline means a faster clock, \\ so a faster computer",
                        r"Past a point, each wrong guess \\ costs more than the clock saves",
                        narration="Here's an idea that sold a generation of computers. Cut the pipeline finer, the "
                                  "clock gets faster, the computer gets faster.",
                        right_narration="It's half right. The clock does get faster. But every stage you add is "
                                        "another cycle thrown away on each wrong guess.")
        self.clear_scene()

    # ------------------------------------------------------------------
    def depth(self):
        d = load("depth")
        ks, ts = np.array(d["k"]), np.array(d["time_ps"])
        kstar = d["kstar"]
        f = MathTex(r"T(k)", r"=", r"\left(\frac{t}{k} + o\right)", r"\bigl(1 + b\,(k - 1)\bigr)", font_size=42)
        f[0].set_color(HEAD)
        f[2].set_color(CLOCK)
        f[3].set_color(NO)
        f.to_edge(UP, buff=0.45)
        w1 = why(r"the clock: \ shorter as $k$ grows", font_size=24).next_to(f[2], DOWN, buff=0.2).shift(LEFT * 0.6)
        w2 = why(r"each miss loses $k-1$ cycles", font_size=24).next_to(f[3], DOWN, buff=0.2).shift(RIGHT * 0.4)
        ax = Axes(x_range=[0, 80, 10], y_range=[0, 900, 300], x_length=8.4, y_length=3.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 20, "include_numbers": True}).move_to(DOWN * 1.35)
        xl = label(r"stages $k$", font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.2)
        yl = label(r"ps per instruction", font_size=22, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        curve = VMobject(color=YES, stroke_width=4).set_points_smoothly([ax.c2p(k, min(t, 900)) for k, t in
                                                                         zip(ks, ts)])
        k = ValueTracker(1.0)

        def T(x):
            return (d["L_ps"] / x + d["o_ps"]) * (1 + d["b"] * (x - 1))

        dot = always_redraw(lambda: Dot(ax.c2p(k.get_value(), min(T(k.get_value()), 900)), color=HEAD, radius=0.1))
        readout = Meter(r"$k$", k, fmt="{:.0f}", color=HEAD, font_size=28)
        tread = always_redraw(lambda: Text(f"{T(k.get_value()):.0f} ps", font="DejaVu Sans Mono", font_size=26,
                                           color=YES).next_to(readout, DOWN, buff=0.15, aligned_edge=LEFT))
        VGroup(readout).to_corner(DR, buff=0.9).shift(UP * 1.0)
        src = tag("computed", rf"the Job's miss rate $b = {d['b']:.3f}$, $o = {d['o_ps']:.0f}$ ps").to_corner(
            DL, buff=0.3)
        with self.voiceover(
            "Put numbers on it. <bookmark mark='a'/> Time per instruction is the cycle, which shrinks as you add "
            "stages, <bookmark mark='b'/> times one plus the miss rate times the cycles each miss throws away, which "
            "grows. <bookmark mark='c'/> Here it is with the Job's own miss rate."
        ) as vo:
            self.play(Write(f), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(w1, shift=UP * 0.1), Indicate(f[2], color=CLOCK))
            vo.wait_until("b")
            self.play(FadeIn(w2, shift=UP * 0.1), Indicate(f[3], color=NO))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(src))
            self.play(Create(curve), run_time=1.8)
        grp = VGroup(f, w1, w2, ax, xl, yl, curve, src)
        card = self.predict(r"Where is the fastest depth?", [r"about 5 stages", rf"about {kstar:.0f}",
                                                              r"the deeper the better"],
                            narration="Where's the bottom of that curve? Around five stages, like Pebble? Around "
                                      f"{kstar:.0f}? Or is deeper always better?", room=grp)
        self.park(card)
        self.add(dot)
        self.play(FadeIn(readout), FadeIn(tread))
        self.play(k.animate.set_value(80), run_time=4.0, rate_func=smooth)
        self.play(k.animate.set_value(kstar), run_time=2.0)
        best = T(kstar)
        near = [x for x in range(1, 81) if T(x) <= 1.05 * best]
        self.reveal(card, 1, narration=(
            f"About {kstar:.0f}, in this model, and the bottom is flat: anywhere from {near[0]} to {near[-1]} stages "
            f"is within five percent. Five stages is {T(5) / best:.1f} times slower. Intel's Prescott, in 2004, had "
            "thirty-one."))
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self):
        d = load("depth")
        hist = d["history"]
        ax = Axes(x_range=[1992, 2024, 4], y_range=[0, 6500, 1000], x_length=9.2, y_length=4.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18}).move_to(LEFT * 0.8 + DOWN * 0.3)
        ax.x_axis.add_numbers(list(range(1996, 2025, 8)), font_size=18, num_decimal_places=0, group_with_commas=False)
        ax.y_axis.add_numbers(list(range(1000, 7000, 1000)), font_size=18, num_decimal_places=0)
        yl = label(r"top desktop clock, \ MHz", font_size=22, color=GREY_B).next_to(ax, UP, buff=0.15).align_to(
            ax, LEFT)
        pts = [ax.c2p(y, f_) for y, f_, _ in hist]
        t = ValueTracker(0)
        trail = always_redraw(lambda: VMobject(color=CLOCK, stroke_width=4).set_points_as_corners(
            pts[:max(2, int(t.get_value()) + 1)] if t.get_value() >= 1 else [pts[0], pts[0] + RIGHT * 1e-3]))
        head_dot = always_redraw(lambda: Dot(pts[min(len(pts) - 1, int(t.get_value()))], color=HEAD, radius=0.09))
        p4 = next(i for i, (_, _, n) in enumerate(hist) if "Prescott" in n)
        pl = label(r"Prescott: \ 31 stages", font_size=22, color=NO).next_to(pts[p4], UP, buff=0.2)
        c2 = next(i for i, (_, _, n) in enumerate(hist) if n.startswith("Core 2"))
        cl = label(r"Core 2: \ 14 stages, \ slower clock, \ faster", font_size=22, color=YES).next_to(
            pts[c2], DR, buff=0.15)
        src = tag("cited", r"vendor specifications").to_corner(DR, buff=0.3)
        with self.voiceover(
            "That's what happened. <bookmark mark='a'/> Through the nineties, clocks climbed a hundredfold, from "
            "sixty-six megahertz to gigahertz. <bookmark mark='b'/> The Pentium 4 pushed depth to twenty stages, "
            "then thirty-one, and reached three point eight gigahertz. <bookmark mark='c'/> Then Intel cancelled the "
            "next, deeper design, and in 2006 Core 2 arrived with about fourteen stages and a lower clock, and beat "
            "it. <bookmark mark='d'/> Clocks have crept up since, but the race was over."
        ) as vo:
            self.play(Create(ax), FadeIn(yl), FadeIn(src))
            self.add(trail, head_dot)
            vo.wait_until("a")
            self.play(t.animate.set_value(4), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(p4), run_time=2.0, rate_func=linear)
            self.play(FadeIn(pl, shift=DOWN * 0.1), Flash(pts[p4], color=NO))
            vo.wait_until("c")
            self.play(t.animate.set_value(c2), run_time=1.0, rate_func=linear)
            self.play(FadeIn(cl, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(t.animate.set_value(len(pts) - 1), run_time=3.0, rate_func=linear)
        self.clear_scene()

    # ------------------------------------------------------------------
    def power(self):
        eq = VGroup(*[MathTex(t, font_size=96) for t in (r"P", r"\approx", r"\alpha", r"C", r"V^2", r"f")]).arrange(
            RIGHT, buff=0.45, aligned_edge=DOWN).move_to(UP * 1.2)
        eq[0].set_color(NO)
        eq[4].set_color(HEAD)
        eq[5].set_color(CLOCK)
        names = VGroup(*[label(t, font_size=24, color=c).next_to(eq[i], DOWN, buff=0.45) for t, c, i in (
            (r"power", NO, 0), (r"switching", GREY_A, 2), (r"capacitance", GREY_A, 3), (r"voltage", HEAD, 4),
            (r"clock", CLOCK, 5))])
        for j, n in enumerate(names):
            n.shift(DOWN * 0.45 * (j % 2))
        wall = label(r"voltage stopped falling \ (about 2005): \ every extra hertz now cost real watts", font_size=28,
                     color=NO).to_edge(DOWN, buff=1.2)
        then = label(r"so the transistors went into more cores \ (Part 10)", font_size=28, color=YES).next_to(
            wall, DOWN, buff=0.3)
        with self.voiceover(
            "The other wall was power. <bookmark mark='a'/> A chip's switching power is roughly activity, times "
            "capacitance, times voltage squared, times the clock. <bookmark mark='b'/> For decades each new process "
            "lowered the voltage, which paid for the faster clock. Around 2005 voltage stopped falling, because "
            "lower voltages leak. Every extra hertz now cost real watts, and a deep pipeline spends many of them on "
            "work it throws away. <bookmark mark='c'/> The transistors kept coming. They went into more cores, which "
            "is Part 10."
        ) as vo:
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in names], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(eq[4], color=HEAD, scale_factor=1.3), FadeIn(wall))
            vo.wait_until("c")
            self.play(FadeIn(then, shift=UP * 0.1), Indicate(eq[5], color=CLOCK))
        self.clear_scene()
