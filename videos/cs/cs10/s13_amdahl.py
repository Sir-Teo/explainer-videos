from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CTRL, DATA, FUNC, HEAD, NO, PART, YES, load)


def log_axes(xmax_pow=10, ymax_pow=10, x_length=7.0, y_length=4.2, ylabel=r"speedup"):
    ax = Axes(x_range=[0, xmax_pow + 0.2, 1], y_range=[0, ymax_pow + 0.2, 1], x_length=x_length, y_length=y_length,
              tips=False, axis_config={"color": GREY_C, "font_size": 16})
    xt = VGroup(*[label(rf"{2 ** k}", font_size=15, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.1)
                  for k in range(0, xmax_pow + 1, 2)])
    yt = VGroup(*[label(rf"{2 ** k}", font_size=15, color=GREY_B).next_to(ax.c2p(0, k), LEFT, buff=0.1)
                  for k in range(0, ymax_pow + 1, 2)])
    xl = label(r"processors \ (log scale)", font_size=17, color=GREY_B).next_to(ax, DOWN, buff=0.4)
    yl = label(ylabel, font_size=17, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
    return ax, VGroup(xt, yt, xl, yl)


class Amdahl(VoiceoverScene):
    def construct(self):
        self.card()
        self.amdahl()
        self.gustafson()
        self.job()

    def card(self):
        card = chapter_card(12, r"Amdahl and Gustafson", r"How much can more processors help?", lit=(1967, 1988),
                            extra=((1967, r"Amdahl"), (1988, r"Gustafson")), part=PART)
        with self.voiceover("Chapter twelve. Amdahl and Gustafson."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def amdahl(self):
        head = label(r"Amdahl's law \ (1967)", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"S(p) = \frac{1}{s + \frac{1 - s}{p}} \;\longrightarrow\; \frac{1}{s}", font_size=42,
                     color=HEAD).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        der = VGroup(label(r"$s$: \ serial fraction of one-processor time", font_size=20, color=GREY_A),
                     label(r"time on $p$ processors: \ $s + (1 - s)/p$", font_size=20, color=GREY_A),
                     label(r"however many processors, \ at most $1/s$", font_size=20, color=NO)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).next_to(eq, DOWN, buff=0.35)
        ax, deco = log_axes()
        VGroup(ax, deco).to_edge(LEFT, buff=0.7).shift(DOWN * 0.35)
        cols = {"0.01": YES, "0.05": DATA, "0.1": CTRL, "0.25": NO}
        curves, labs = VGroup(), VGroup()
        for s, c in cols.items():
            sv = float(s)
            xs = np.linspace(0, 10, 80)
            ys = [np.log2(1 / (sv + (1 - sv) / 2 ** x)) for x in xs]
            curves.add(ax.plot_line_graph(list(xs), ys, add_vertex_dots=False, line_color=c, stroke_width=3))
            labs.add(label(rf"$s = {100 * sv:g}\%$", font_size=17, color=c).next_to(ax.c2p(10, ys[-1]), RIGHT,
                                                                                      buff=0.1))
        ideal = DashedLine(ax.c2p(0, 0), ax.c2p(10, 10), color=GREY_D, stroke_width=2)
        il = label(r"ideal", font_size=16, color=GREY_B).next_to(ax.c2p(8.5, 8.5), LEFT, buff=0.1)
        with self.voiceover(
            (
            "In 1967 Gene Amdahl, the architect of IBM's System/360, argued that parallel machines would always "
            "disappoint. <bookmark mark='a'/> Suppose a fraction s of the fixed program's one-processor running "
            "time is serial, and the rest divides perfectly among p identical processors, with no extra overhead. "
            "On one processor the time is one. On p it is s, plus one minus s over p. <bookmark mark='b'/> The "
            "speedup is one over that, and as p grows it approaches one over s, and no further. <bookmark "
            "mark='c'/> One percent serial, and a thousand processors give barely ninety-one times. Ten percent "
            "serial, and you never pass ten. Twenty-five percent, never four."
        )
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(deco), Create(ideal), FadeIn(il))
            vo.wait_until("a")
            self.play(FadeIn(der[0]), FadeIn(der[1]))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(der[2]))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.3), FadeIn(labs), run_time=3)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gustafson(self):
        head = label(r"Gustafson's answer \ (1988)", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"S(p) = s + (1 - s)\,p", font_size=44, color=HEAD).next_to(head, DOWN, buff=0.4)
        bars = VGroup()
        for k, p in enumerate((1, 2, 4, 8)):
            ser = Rectangle(width=0.5, height=0.35, stroke_width=0, fill_color=NO, fill_opacity=0.8)
            par = VGroup(*[Rectangle(width=0.5, height=1.4, stroke_width=0, fill_color=YES, fill_opacity=0.6)
                           for _ in range(p)]).arrange(RIGHT, buff=0.04)
            g = VGroup(ser, par).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
            g.add(label(rf"$p = {p}$", font_size=18, color=GREY_B).next_to(g, DOWN, buff=0.1))
            bars.add(g)
        bars.arrange(RIGHT, buff=0.6, aligned_edge=DOWN).move_to(DOWN * 0.6)
        cap = VGroup(label(r"keep the \textit{time} fixed, \ and grow the problem with the machine", font_size=22,
                           color=GREY_A),
                     label(r"strong: \ fixed problem size; \ weak: \ fixed work per processor \ (ideal time stays flat)",
                           font_size=20, color=DATA)).arrange(
            DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        ser = label(r"serial part", font_size=17, color=NO).next_to(bars[0][0], LEFT, buff=0.15)
        par = label(r"parallel part", font_size=17, color=YES).next_to(bars[0][1], LEFT, buff=0.15)
        with self.voiceover(
            (
            "Twenty years later John Gustafson, at Sandia National Laboratories, pointed out what Amdahl had "
            "assumed: that the problem stays the same size. <bookmark mark='a'/> People who buy a thousand "
            "processors do not run yesterday's problem faster. They run a bigger problem in the same time: a "
            "finer weather grid, a larger simulation. The idealized assumption is that serial time stays roughly "
            "fixed while useful parallel work grows; real input and communication costs may also grow. <bookmark "
            "mark='b'/> Measured that way, s is now the serial fraction of the measured parallel runtime, not the "
            "same numerical fraction as in the fixed one-core problem. The scaled speedup is s plus p times one "
            "minus s under those assumptions. <bookmark mark='c'/> Both are right; they answer different "
            "questions. Amdahl's is called strong scaling: the same problem, solved faster. Gustafson motivates "
            "scaled-size reasoning. Weak scaling conventionally holds work per processor fixed and measures how "
            "runtime changes; constant runtime is its ideal outcome, not its definition. Supercomputers live by "
            "weak scaling."
        )
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3), FadeIn(ser), FadeIn(par), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(Write(eq))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def job(self):
        am = load("amdahl")
        job = am["job"]
        head = label(r"The Job's strong scaling", font_size=36).to_edge(UP, buff=0.3)
        ax, deco = log_axes(xmax_pow=5, ymax_pow=6, x_length=6.5, y_length=4.4)
        VGroup(ax, deco).to_edge(LEFT, buff=0.8).shift(DOWN * 0.35)
        ideal = DashedLine(ax.c2p(0, 0), ax.c2p(5, 5), color=GREY_D, stroke_width=2)
        il = label(r"$p$ times", font_size=16, color=GREY_B).next_to(ax.c2p(3.0, 3.0), LEFT, buff=0.15)
        lines = VGroup()
        for key, c, name in (("serial", NO, r"merge on one core"), ("tree", CTRL, r"merge as a tree"),
                             ("partitioned", YES, r"merge partitioned by word")):
            pts = [ax.c2p(np.log2(r["p"]), np.log2(r[key])) for r in job]
            ln = VMobject(color=c, stroke_width=4).set_points_as_corners(pts)
            dots = VGroup(*[Dot(p, radius=0.06, color=c) for p in pts])
            lab = label(rf"{name}: \ {job[-1][key]:.1f}$\times$ at {job[-1]['p']}", font_size=18, color=c).next_to(
                pts[-1], RIGHT, buff=0.15).shift({"serial": DOWN * 0.17, "tree": UP * 0.17}.get(key, ORIGIN))
            lines.add(VGroup(ln, dots, lab))
        side = VGroup(
            label(r"serial merge: \ worse than Amdahl, \\ the serial part grows with $p$", font_size=19, color=NO),
            label(r"partitioned: \ above the ideal line, \\ because each shard's table shrinks", font_size=19,
                  color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=0.4).shift(DOWN * 1.2)
        with self.voiceover(
            f"Here is the Job, scaled from one Pebble core to thirty-two, the same thirty novels each time: strong scaling. <bookmark mark='a'/> With the merge on one core, the speedup climbs to about three and then falls. That is worse than Amdahl's law, because the serial part is not fixed: more cores mean more tables to merge. <bookmark mark='b'/> A tree of merges does a little better at the largest sizes, but not much. <bookmark mark='c'/> And with the merge partitioned by word, the conditional compute-cost speedup can exceed p, {job[-1]['partitioned']:.0f} times on thirty-two cores, because the scan-based algorithm changes its total work as tables shrink. Routing, communication and shared-resource costs are still excluded. Remember where that comes from: an algorithm whose worst case is quadratic, rather than an immutable amount of work. Amdahl's law assumes the total work is fixed; here, splitting the data reduced it."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(deco), Create(ideal), FadeIn(il))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(Create(l[0]), FadeIn(l[1]), FadeIn(l[2]))
                if mk == "a":
                    self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
        self.wait(0.3)
        self.clear_scene()
