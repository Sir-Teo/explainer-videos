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
                why(r"holding the output gap and neutral rate fixed, the nominal rate rises more than current inflation. Stabilization also depends on expectations, policy timing and the economic model"),
                why(r"the output gap, here from the CBO's estimate of potential output; inflation is the GDP deflator "
                    r"over four quarters, as Taylor used")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "Taylor's 1993 rule is a conditional benchmark for a nominal policy rate. Add a neutral real rate to inflation, then add half the inflation gap and half the output gap, all measured in percentage points. <bookmark mark='a'/> With a two-percent neutral real rate and two-percent inflation target, the formula becomes one plus one-and-a-half times inflation plus half the output gap. <bookmark mark='b'/> Holding other terms fixed, a point more inflation raises the nominal-minus-current-inflation rate by half a point. This illustrates the Taylor principle. It is not a standalone theorem of stability: expectations, inertia, output responses and policy constraints matter. <bookmark mark='c'/> Potential output and the neutral real rate are unobserved. This retrospective chart uses a pinned revised CBO estimate and revised inflation data, not the real-time information available to each historical committee."
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
            wrapped_label(r"some post-crisis quarters: the benchmark is negative. The Fed used a near-zero target range and additional tools; negative nominal rates are not mechanically impossible", 4.0,
                          17, GREY_A),
            wrapped_label(rf"2021--22: {abs(t['dev_2021_22']):.1f} points below, on average; in "
                          rf"{int(t['worst']['t'])} the rule said {t['worst']['rule']:.0f}\%, the Fed was at "
                          rf"{t['worst']['ff']:.1f}\%", 3.6, 17, QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.35, aligned_edge=LEFT)
        notes.shift(LEFT * max(0.0, notes.get_right()[0] - 6.75))
        with self.voiceover(
            f"This is a retrospective comparison of quarterly average federal funds with two versions of the rule, using revised data. <bookmark mark='a'/> Their pre-2008 correlation is {t['corr_1987_2007']:.2f}. Correlation does not establish that this specification was the committee's reaction function. <bookmark mark='b'/> In 2003 through 2005 the saved average rate lies {abs(t['dev_2003_05']):.1f} percentage points below the GDP-deflator benchmark. That difference alone does not identify a cause of the housing boom. <bookmark mark='c'/> The benchmark turns negative in some post-crisis quarters. The Fed chose a near-zero target and other tools; negative nominal rates were not a mathematical impossibility. <bookmark mark='d'/> In the second quarter of 2022 this rule gives about thirteen percent against an actual quarterly average of about zero-point-eight percent. The Fed subsequently raised rates substantially. Using core PCE changes the benchmark, showing the sensitivity to inflation measure, neutral-rate assumptions and revised output gaps."
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
        self.add(illustration(r"Pinned revised FRED/CBO series, quarterly: retrospective comparison, not a real-time policy forecast"))
        self.wait(0.5)
        self.clear_scene()

    def plane(self, t):
        infl, gap, ff, T = (np.asarray(t[k]) for k in ("inflation", "gap", "ff", "t"))
        ax = surf3d_axes([-1, 8, 1], [-10, 4, 2], [-6, 16, 2], x_length=6.4, y_length=5.2, z_length=4.0)
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
            "The formula is a plane over inflation and the output gap. Its complete displayed range is retained, including a fifteen-percent rate at the upper corner. <bookmark mark='a'/> Each dot is one quarter's actual average rate, with a stem to the conditional benchmark evaluated at that quarter's revised inputs. <bookmark mark='b'/> Distances from this plane are specification-dependent residuals, not measured policy mistakes. The neutral rate, inflation target, output-gap estimate, timing and reaction coefficients can all change the comparison. This full-sample retrospective picture does not prove that any alternative policy would have delivered a better outcome."
        ) as vo:
            self.play(Create(ax), FadeIn(key), run_time=1.5)
            self.play(FadeIn(pl), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), Create(stems), run_time=3)
            vo.wait_until("b")
            self.move_camera(theta=-110 * DEGREES, run_time=6)
        q = ask(r"in Q2 2022 one benchmark was about 13\%, versus a 0.8\% quarterly funds rate. Which assumptions and information vintages could change that comparison?").set_z_index(10)
        self.add_fixed_in_frame_mobjects(q)
        self.remove(q)
        with self.voiceover('Pause and predict: name two assumptions or information vintages that could change this comparison, and one independent way to assess the outcomes of the actual policy.'):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)
