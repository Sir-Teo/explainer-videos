from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import MKT, PART, POLICY, ask, illustration, load, surf3d_axes

RULE = QC.DELTA
CORE = QC.IMPLIED


class Taylor(VoiceoverScene, ThreeDScene):
    def construct(self):
        t = load("taylor")
        self.card()
        self.rule()
        self.history(t)
        self.plane(t)

    def card(self):
        c = chapter_card(3, r"The Taylor rule", r"Where should the policy rate be?", part=PART)
        with self.voiceover("Chapter three. The Taylor rule."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def rule(self):
        rows = [cmath(r"i", r"=", r"r^* + \pi + \tfrac12(\pi - \pi^*) + \tfrac12\,y", font_size=44,
                      colors={r"i": RULE}),
                cmath(r"r^* = \pi^* = 2", r"\Rightarrow", r"i = 1 + 1.5\,\pi + 0.5\,y", font_size=42,
                      colors={r"\Rightarrow": WHITE}),
                cmath(r"\frac{\partial (i - \pi)}{\partial \pi}", r"=", r"0.5 > 0", font_size=42,
                      colors={r"\frac{\partial (i - \pi)}{\partial \pi}": QC.GAIN}),
                cmath(r"y", r"=", r"100\,\frac{\text{GDP} - \text{potential GDP}}{\text{potential GDP}}", font_size=38,
                      colors={r"y": QC.SPOT})]
        whys = [why(r"Taylor (1993): the neutral real rate $r^*$, plus inflation $\pi$, plus half the inflation gap and "
                    r"half the output gap $y$, in percent"),
                why(r"his own numbers: 2\% for both. Each point of inflation raises the rate by one and a half"),
                why(r"the Taylor principle: the real rate rises when inflation does, which leans against it. A "
                    r"coefficient below one would let inflation feed itself"),
                why(r"the output gap, here from the CBO's estimate of potential output; inflation is the GDP deflator "
                    r"over four quarters, as Taylor used")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "In 1993 John Taylor proposed a rule of thumb for the policy rate. Take the neutral real rate, add "
            "inflation, then lean against two gaps: half of inflation's distance from its target, and half of output's "
            "distance from its potential. <bookmark mark='a'/> With his numbers, two percent for each, every point of "
            "inflation adds one and a half points to the rate. <bookmark mark='b'/> That one and a half is the point: "
            "the real rate rises when inflation rises, so policy pushes back. A coefficient below one would let "
            "inflation lower real rates and feed itself. <bookmark mark='c'/> The output gap needs an estimate of "
            "potential output, which nobody observes; here it is the Congressional Budget Office's."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def history(self, t):
        T, ff, rule, core = (np.asarray(t[k]) for k in ("t", "ff", "rule", "rule_core"))
        g = axes([1987, 2026], [-6, 14], x_length=8.4, y_length=4.6, xlabel=r"year", ylabel=r"percent",
                 xticks=[1990, 2000, 2010, 2020], yticks=[-5, 0, 5, 10], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        zero = DashedLine(ax.c2p(1987, 0), ax.c2p(2026, 0), color=GREY_D, stroke_width=1.5)
        lf = curve(ax, T, ff, MKT, stroke_width=3)
        lr = curve(ax, T, rule, RULE, stroke_width=3)
        lc = DashedVMobject(curve(ax, T, core, CORE, stroke_width=2.5), num_dashes=120)
        leg = legend([(MKT, r"fed funds (quarterly average)"), (RULE, r"Taylor (1993), GDP deflator"),
                      (CORE, r"the same rule, core PCE inflation")], font_size=17).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)

        def shade(a, b, col):
            return Rectangle(width=ax.c2p(b, 0)[0] - ax.c2p(a, 0)[0], height=ax.c2p(0, 14)[1] - ax.c2p(0, -6)[1],
                             stroke_width=0, fill_color=col, fill_opacity=0.12).move_to(
                [(ax.c2p(a, 0)[0] + ax.c2p(b, 0)[0]) / 2, (ax.c2p(0, 14)[1] + ax.c2p(0, -6)[1]) / 2, 0])
        sh = VGroup(shade(2003, 2006, QC.SPOT), shade(2009, 2016, GREY_B), shade(2021, 2023, QC.LOSS))
        notes = VGroup(
            MathTex(rf"\rho_{{1987-2007}} = {t['corr_1987_2007']:.2f}", font_size=28, color=WHITE),
            wrapped_label(rf"2003--05: funds rate {abs(t['dev_2003_05']):.1f} points below the rule, on average", 4.0, 17,
                          QC.SPOT),
            wrapped_label(r"2009--15: the rule went below zero; the funds rate could not, so the Fed bought bonds", 4.0,
                          17, GREY_A),
            wrapped_label(rf"2021--22: {abs(t['dev_2021_22']):.1f} points below, on average; in "
                          rf"{t['worst']['t']:.0f} the rule said {t['worst']['rule']:.0f}\%, the Fed was at "
                          rf"{t['worst']['ff']:.1f}\%", 3.6, 17, QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.35, aligned_edge=LEFT)
        notes.shift(LEFT * max(0.0, notes.get_right()[0] - 6.75))
        with self.voiceover(
            "Here is the rule against what the Fed actually did, every quarter since 1987. <bookmark mark='a'/> From "
            "1987 to 2007 they moved together, with a correlation of "
            f"{t['corr_1987_2007']:.2f}; this is why Taylor's rule became the benchmark. <bookmark mark='b'/> But "
            f"from 2003 to 2005 the Fed held rates about {abs(t['dev_2003_05']):.0f} points below it, a gap that "
            "Taylor himself later blamed for the housing boom. <bookmark mark='c'/> After 2008 the rule called for "
            "negative rates, which the Fed could not set, so it bought bonds instead. <bookmark mark='d'/> And in 2021 "
            "and 2022, with inflation high and the economy hot, the rule called for double digits while the Fed sat "
            "near zero. Core inflation, in orange, tells a milder story, but the same one."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(lf), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lr), FadeIn(leg[1]), FadeIn(notes[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(sh[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(sh[1]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(sh[2]), Create(lc), FadeIn(leg[2]), FadeIn(notes[3]), run_time=2)
        self.add(illustration(r"FRED: FEDFUNDS, GDPDEF, PCEPILFE, GDPC1, GDPPOT"))
        self.wait(0.5)
        self.clear_scene()

    def plane(self, t):
        infl, gap, ff, T = (np.asarray(t[k]) for k in ("inflation", "gap", "ff", "t"))
        ax = surf3d_axes([-1, 8, 1], [-10, 4, 2], [-6, 14, 2], x_length=6.4, y_length=5.2, z_length=4.0)
        ax.shift(RIGHT * 0.9 + DOWN * 0.4)
        pl = Surface(lambda u, v: ax.c2p(u, v, 1 + 1.5 * u + 0.5 * v), u_range=(-1, 8), v_range=(-10, 4),
                     resolution=(12, 12), fill_color=RULE, fill_opacity=0.35, stroke_color=RULE, stroke_width=0.6,
                     checkerboard_colors=False)
        cols = [interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.LOSS), (x - T[0]) / (T[-1] - T[0])) for x in T]
        dots = VGroup(*[Dot3D(ax.c2p(a, b, c), radius=0.045, color=col) for a, b, c, col in zip(infl, gap, ff, cols)])
        stems = VGroup(*[Line(ax.c2p(a, b, 1 + 1.5 * a + 0.5 * b), ax.c2p(a, b, c), color=col, stroke_width=1,
                              stroke_opacity=0.5) for a, b, c, col in zip(infl, gap, ff, cols)])
        key = VGroup(label(r"inflation (across), output gap (back), rate (up)", font_size=19, color=GREY_A),
                     legend([(RULE, r"the rule: a plane"), (QC.SPOT, r"each quarter's funds rate: 1987 (blue) to 2025 "
                                                                      r"(red)")], font_size=17),
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "Another way to see it. The rule is a plane: the rate it prescribes over every combination of inflation and "
            "output gap. <bookmark mark='a'/> Each dot is one quarter's actual funds rate, standing above or hanging "
            "below the plane, with a thread to the point the rule called for. <bookmark mark='b'/> The early, blue "
            "quarters hug the plane. The red ones of 2021 and 2022 hang far beneath it, where high inflation met a rate "
            "near zero. A rule is a summary of past behaviour, not a law; the neutral rate it assumes is itself a guess, "
            "and the next parts treat it as one."
        ) as vo:
            self.play(Create(ax), FadeIn(key), run_time=1.5)
            self.play(FadeIn(pl), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), Create(stems), run_time=3)
            vo.wait_until("b")
            self.move_camera(theta=-110 * DEGREES, run_time=6)
        q = ask(r"in 2022 the rule said 13\%; the Fed was at 1\%. Name two reasons the rule could be wrong, and one "
                r"reason the Fed could be.").set_z_index(10)
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover("Pause on this one: name two reasons the rule could have been wrong in 2022, and one reason "
                            "the Fed could have been."):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
