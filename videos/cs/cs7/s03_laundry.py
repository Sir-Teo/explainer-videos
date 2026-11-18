from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (CLOCK, COST, DATA, FUNC, HEAD, NO, PART, STAGE_COLOR, STAGES, YES, chapter, fmt,
                                  load)

STEPS = (("wash", DATA), ("dry", HEAD), ("fold", YES), ("put away", FUNC))


def gantt(pipelined: bool, w=0.6, h=0.46, x0=-5.4, y0=1.0):
    """Four loads against the hours: one block per load and step, placed where it runs."""
    g = VGroup()
    for i in range(4):
        start = i if pipelined else 4 * i
        for k, (name, c) in enumerate(STEPS):
            r = RoundedRectangle(width=w * 0.94, height=h * 0.84, corner_radius=0.06, stroke_width=0, fill_color=c,
                                 fill_opacity=0.75).move_to([x0 + (start + k + 0.5) * w, y0 - i * h, 0])
            t = Text(name, font_size=11, color=WHITE)
            if t.width > r.width * 0.9:
                t.width = r.width * 0.9
            g.add(VGroup(r, t.move_to(r)))
    return g


class Laundry(WatchScene):
    def construct(self):
        chapter(self, 2, r"Pipelining, like laundry", r"How do you finish more without finishing anything sooner?")
        self.laundry()
        self.formulas()
        self.unbalanced()

    # ------------------------------------------------------------------
    def laundry(self):
        w = 0.62
        hours = Axes(x_range=[0, 16, 1], y_range=[0, 1, 1], x_length=16 * w, y_length=0.01, tips=False,
                     axis_config={"color": GREY_D, "include_numbers": True, "font_size": 16}).move_to(UP * 2.55)
        x0 = hours.c2p(0, 0)[0]
        hl = label(r"hours", font_size=20, color=GREY_B).next_to(hours, LEFT, buff=0.25)
        seq = gantt(False, w=w, x0=x0, y0=1.7)
        pip = gantt(True, w=w, x0=x0, y0=-0.9)
        sl = label(r"one at a time", font_size=24, color=NO).next_to(seq, LEFT, buff=0.2).align_to(hl, RIGHT)
        pl = label(r"overlapped", font_size=24, color=YES).next_to(pip, LEFT, buff=0.2).align_to(hl, RIGHT)
        cursor = Line(UP * 0.35, DOWN * 0.35, color=CLOCK, stroke_width=4).move_to(hours.c2p(0, 0))
        with self.voiceover(
            "Patterson and Hennessy picture this as laundry. <bookmark mark='a'/> Each load needs four steps of an hour: "
            "wash, dry, fold, put away. One load at a time, four loads take sixteen hours."
        ) as vo:
            self.play(Create(hours), FadeIn(hl))
            vo.wait_until("a")
            self.add(cursor)
            self.play(FadeIn(sl), LaggedStart(*[GrowFromEdge(b, LEFT) for b in seq], lag_ratio=1.0),
                      cursor.animate.move_to(hours.c2p(16, 0)), run_time=5.0, rate_func=linear)
        card = self.predict(r"Start the next load as soon as the washer is free. \\ How long for all four?",
                            [r"4 hours", r"7 hours", r"16 hours"],
                            narration="But the washer is free after the first hour. Start the next load then. How "
                                      "long for all four: four hours, seven, or still sixteen?",
                            room=VGroup(hours, hl, seq, sl, cursor), where="right")
        drop = pip.get_center()[1] - hours.c2p(0, 0)[1]
        self.play(cursor.animate.move_to(hours.c2p(0, 0) + UP * drop).stretch_to_fit_height(pip.height + 0.2),
                  run_time=0.5)
        self.play(FadeIn(pl), LaggedStart(*[GrowFromEdge(b, LEFT) for b in pip], lag_ratio=0.25),
                  cursor.animate.move_to(hours.c2p(7, 0) + UP * drop), run_time=3.5, rate_func=linear)
        self.reveal(card, 1, narration="Seven hours.")
        one = SurroundingRectangle(VGroup(*pip[12:16]), color=HEAD, buff=0.05)
        lat = label(r"each load: \ still 4 hours \ (latency)", font_size=24, color=HEAD).next_to(pip, DOWN, buff=0.35)
        thr = label(r"one load done every hour \ (throughput)", font_size=24, color=YES).next_to(lat, DOWN, buff=0.15)
        with self.voiceover(
            "Notice what didn't change. <bookmark mark='a'/> Each load still takes four hours from dirty to put away: "
            "the latency is the same. <bookmark mark='b'/> What changed is throughput. Once the line is full, a load "
            "comes out every hour. A processor works the same way. No instruction finishes sooner; more of them "
            "finish per second."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(one), FadeIn(lat, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(thr, shift=UP * 0.1), *[Indicate(pip[4 * i + 3], color=YES) for i in range(4)])
        self.clear_scene()

    # ------------------------------------------------------------------
    def formulas(self):
        st = load("stages")
        o = 70
        t = st["single_ps"] - o
        head = label(r"Cut $t$ of work into $k$ stages", font_size=36).to_edge(UP, buff=0.35)
        f0 = MathTex(r"t_{\text{cycle}}", r"=", r"\frac{t}{k}", r"+", r"o", font_size=48).move_to(UP * 1.5)
        f0[0].set_color(CLOCK)
        f0[4].set_color(COST)
        f1 = MathTex(r"\text{latency}", r"=", r"k\left(\frac{t}{k} + o\right)", r"=", r"t + k\,o", font_size=44)
        f1.next_to(f0, DOWN, buff=0.5)
        f1[0].set_color(NO)
        f2 = MathTex(r"\text{speedup}", r"=", r"\frac{t + o}{t/k + o}", r"\ \xrightarrow{\,k\to\infty\,}\ ",
                     r"1 + \frac{t}{o}", font_size=44).next_to(f1, DOWN, buff=0.5)
        f2[0].set_color(YES)
        w1 = why(r"each register adds $o$", font_size=28).next_to(f1, RIGHT, buff=0.4)
        w2 = why(r"registers, not logic, set the limit", font_size=28).next_to(f2, RIGHT, buff=0.4)
        with self.voiceover(
            "Now the arithmetic. Say an instruction is t of logic, cut into k equal stages, and every pipeline "
            "register adds a little overhead, o. <bookmark mark='a'/> The cycle is t over k, plus o. <bookmark "
            "mark='b'/> One instruction now takes k cycles, so its latency grows: t plus k times o. <bookmark "
            "mark='c'/> But one finishes every cycle, so the speedup is t plus o over t over k plus o. Make k huge "
            "and it stops at one plus t over o. The registers, not the logic, set the limit."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f0))
            vo.wait_until("b")
            self.play(TransformFromCopy(f0[2:], f1[2]), Write(f1[:2]), run_time=1.2)
            self.play(Write(f1[3:]), FadeIn(w1, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(TransformFromCopy(f0[2:], f2[2]), Write(f2[:2]), run_time=1.2)
            self.play(Write(f2[3:]), FadeIn(w2, shift=LEFT * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def unbalanced(self):
        st = load("stages")
        top = max(v["ps"] for v in st["stages"].values())
        head = label(r"Pebble's five stages are not equal", font_size=36).to_edge(UP, buff=0.35)
        scale = 3.6 / st["single_ps"]
        # Part 6's single cycle, one long bar, then cut into its stages
        whole = VGroup()
        x = -5.6
        for s in STAGES:
            wdt = st["stages"][s]["ps"] * scale * 3.0
            whole.add(Rectangle(width=wdt, height=0.6, stroke_color=BLACK, stroke_width=2, fill_color=STAGE_COLOR[s],
                                fill_opacity=0.7).move_to([x + wdt / 2, 1.6, 0]))
            x += wdt
        wl = label(rf"Part 6: \ one cycle, \ {fmt(st['single_ps'])} ps", font_size=24, color=GREY_A).next_to(
            whole, UP, buff=0.2)
        cols = VGroup()
        for k, s in enumerate(STAGES):
            h = st["stages"][s]["ps"] * scale * 1.6
            r = Rectangle(width=1.0, height=h, stroke_width=0, fill_color=STAGE_COLOR[s], fill_opacity=0.75)
            r.move_to([-4.9 + 1.45 * k, -2.2 + h / 2, 0])
            nm = label(s, font_size=24, color=STAGE_COLOR[s]).next_to(r, DOWN, buff=0.12)
            ps = label(rf"{fmt(st['stages'][s]['ps'])}", font_size=20, color=GREY_A).next_to(r, UP, buff=0.08)
            cols.add(VGroup(r, nm, ps))
        src = tag("assumed", r"1 ns memories, 70 ps registers").to_corner(DR, buff=0.4)
        with self.voiceover(
            "Real stages aren't equal. <bookmark mark='a'/> Here is Part 6's single cycle, divided by what each piece "
            "does. <bookmark mark='b'/> Cut it at the stage boundaries and stand the pieces up. The two memories "
            "dominate; decode and write back are slivers."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in whole], lag_ratio=0.3), FadeIn(wl), run_time=1.8)
            vo.wait_until("b")
            self.play(*[ReplacementTransform(whole[k], cols[k][0]) for k in range(5)], FadeOut(wl), run_time=1.6)
            self.play(*[FadeIn(c[1:]) for c in cols])
        cols_all = VGroup(cols)
        card = self.predict(r"Cut into five, \ how short can the clock get?",
                            [rf"{st['single_ps'] / 5:.0f} ps: \ a fifth", rf"{fmt(st['period_ps'])} ps",
                             rf"{fmt(st['single_ps'])} ps: \ no change"],
                            narration="Every stage gets the same clock. How short can that clock be? A fifth of the "
                                      "old cycle? Something longer? Or no faster at all?", room=cols_all)
        self.reveal(card, 1, narration=(
            f"{fmt(st['period_ps'])} picoseconds. The clock must wait for the slowest stage, plus the register."))
        bottom = cols[0][0].get_bottom()[1]
        y = bottom + (top + 70) * scale * 1.6
        line = DashedLine([-5.6, y, 0], [1.8, y, 0], color=NO, stroke_width=3)
        verdict = VGroup(
            label(rf"clock: \ the slowest stage $+$ 70 ps \ $=$ {fmt(st['period_ps'])} ps", font_size=26, color=CLOCK),
            label(rf"{st['clock_ratio']:.1f}$\times$ faster, \ not 5$\times$", font_size=34, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP * 0.6)
        with self.voiceover(
            f"So the clock gets {st['clock_ratio']:.1f} times faster, not five. <bookmark mark='a'/> The memories "
            "set the pace, which is why Part 9 is all about them."
        ) as vo:
            self.play(Create(line), FadeIn(verdict[0], shift=LEFT * 0.2))
            self.play(FadeIn(verdict[1], scale=1.1))
            vo.wait_until("a")
            self.play(Indicate(cols[0][0], color=NO), Indicate(cols[3][0], color=NO))
        self.clear_scene()
