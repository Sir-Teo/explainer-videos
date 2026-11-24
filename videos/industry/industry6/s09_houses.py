from __future__ import annotations

from videos.industry.industry6.common import *  # noqa: F403


def _x(month: str) -> float:
    return int(month[:4]) + (int(month[5:7]) - 0.5) / 12


class Houses(VoiceoverScene):
    def construct(self):
        card(self, 8, "Houses", "What happens when everyone builds at once?",
             "Chapter eight. Houses.", lit=("change",))
        H = R["housing"]
        S = H["series"]
        street = VGroup(*[draw.house(0.7, color=STONE) for _ in range(9)]).arrange(RIGHT, buff=0.2).move_to(
            [0, 2.55, 0])
        frames = VGroup(*[VGroup(Line(ORIGIN, UP * 0.5), Line(UP * 0.5, UP * 0.5 + RIGHT * 0.6),
                                 Line(RIGHT * 0.6, RIGHT * 0.6 + UP * 0.5), Line(UP * 0.5, RIGHT * 0.3 + UP * 0.85),
                                 Line(RIGHT * 0.3 + UP * 0.85, RIGHT * 0.6 + UP * 0.5)).set_stroke(ORDER, 3)
                          for _ in range(9)]).arrange(RIGHT, buff=0.3).move_to([0, 2.55, 0])
        pa = viz.plot_axes([1999.6, 2026.9], [0, 2.4], x_length=10.4, y_length=2.6, yticks=[1.0, 2.0],
                           yfmt=lambda v: f"{v:g}m", size=15)
        pa.move_to([0.4, 0.05, 0])
        pb = viz.plot_axes([1999.6, 2026.9], [0, 13], x_length=10.4, y_length=1.5,
                           xticks=[2000, 2005, 2010, 2015, 2020, 2025], yticks=[6, 12],
                           xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{v:g}", size=15)
        pb.move_to([0.4, -2.55, 0])

        def line(ax, sid, col, scale=1.0, w=3):
            return VMobject(stroke_color=col, stroke_width=w).set_points_as_corners(
                [ax.ax.c2p(_x(k), v * scale) for k, v in zip(S[sid]["months"], S[sid]["values"])])
        starts = line(pa, "HOUST", ORDER, 1 / 1000)
        built = line(pa, "COMPUTSA", CAP, 1 / 1000)
        supply = line(pb, "MSACSR", BUST)
        key = VGroup(tx("houses started", 17, ORDER, bold=True), tx("houses completed", 17, CAP, bold=True),
                     tx("a year, at the month's pace", 15, GREY_B)).arrange(RIGHT, buff=0.4).next_to(pa, UP, buff=0.08
                                                                                                ).align_to(pa, LEFT)
        kb = tx("new houses for sale: months it would take to sell them all", 16, BUST).next_to(pb, UP, buff=0.08
                                                                                          ).align_to(pb, LEFT)
        (pk_m, pk_v), (tr_m, tr_v) = H["starts_peak"], H["starts_trough"]
        sp_m, sp_v = H["supply_peak"]
        dpk = glow_dot(pa.ax.c2p(_x(pk_m), pk_v / 1000), color=ORDER, radius=0.09)
        dtr = glow_dot(pa.ax.c2p(_x(tr_m), tr_v / 1000), color=BUST, radius=0.09)
        tpk = tx(f"{pk_v / 1000:.2f}m, January 2006", 15, ORDER).next_to(dpk, RIGHT, buff=0.12)
        ttr = tx(f"{tr_v / 1000:.2f}m, April 2009: {100 * H['fall']:.0f}%", 15, BUST).next_to(dtr, DOWN, buff=0.1)
        dsp = glow_dot(pb.ax.c2p(_x(sp_m), sp_v), color=BUST, radius=0.09)
        tsp = tx(f"{sp_v:.1f} months, January 2009", 15, BUST).next_to(dsp, RIGHT, buff=0.12)
        src = source("US Census Bureau via FRED: housing starts, completions, months' supply of new houses "
                     "(seasonally adjusted)", size=13)
        with self.voiceover(
            "Houses take months to build, not years, but there are millions of them, built by thousands of "
            "builders who cannot see each other's plans. <bookmark mark='a'/> In America, the Census Bureau counts "
            "every month how many homes were started, and how many were finished. <bookmark mark='b'/> In the "
            "early 2000s, with prices rising and mortgages easy to get, the number of homes started climbed, to a "
            f"pace of {pk_v / 1000:.2f} million a year in January 2006. <bookmark mark='c'/> Then it collapsed, "
            f"by {-100 * H['fall']:.0f} percent in three years. <bookmark mark='d'/> But look at the blue line: the "
            "homes being finished. They kept coming for a year after the starts had turned, because a house "
            "already begun gets finished. <bookmark mark='e'/> And so the pile of new homes nobody had bought kept "
            f"growing. At its worst, in January 2009, it would have taken {sp_v:.1f} months to sell them all at the "
            "pace they were selling: three years after the building had peaked. <bookmark mark='f'/> And then the "
            "builders, burned, held back for a decade. Starts did not reach one and a half million a year again "
            "until December 2019."
        ) as vo:
            self.play(FadeIn(src), LaggedStart(*[Create(f_) for f_ in frames], lag_ratio=0.1), run_time=1.8)
            self.play(LaggedStart(*[ReplacementTransform(f_, h_) for f_, h_ in zip(frames, street)], lag_ratio=0.1),
                      run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(pa), FadeIn(key[0]), FadeIn(key[2]))
            vo.wait_until("b")
            self.play(Create(starts), run_time=3.0, rate_func=linear)
            self.play(FadeIn(dpk, scale=2), FadeIn(tpk))
            vo.wait_until("c")
            self.play(FadeIn(dtr, scale=2), FadeIn(ttr),
                      LaggedStart(*[h_.animate.set_opacity(0.25) for h_ in street[3:]], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(FadeIn(key[1]), Create(built), run_time=3.0, rate_func=linear)
            vo.wait_until("e")
            self.play(FadeIn(pb), FadeIn(kb), Create(supply), run_time=2.4)
            self.play(FadeIn(dsp, scale=2), FadeIn(tsp))
            vo.wait_until("f")
            self.play(Indicate(starts, color=WHITE), street.animate.set_opacity(1))
        self.clear_scene()
        self.survivor()

    def survivor(self):
        B = R["builder"]
        yrs, rev, ni = B["years"], B["revenue"], B["ni"]
        pa = viz.plot_axes([2008.4, 2026.6], [0, 40], x_length=8.6, y_length=4.0, xticks=[2009, 2014, 2019, 2024],
                           yticks=[10, 20, 30, 40], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"${v:g}bn", size=15)
        pa.move_to([1.2, -0.6, 0])
        bars = viz.year_bars(pa, yrs, rev, CAP, width=0.5)
        head = tx("D.R. Horton: homes sold each fiscal year", 18, GREY_A).next_to(pa, UP, buff=0.15).align_to(pa, LEFT)
        y0, y1 = 2009, 2024
        l0 = tx(f"${rev[yrs.index(y0)]:.1f}bn, a loss of ${-ni[y0]:.2f}bn", 16, BUST).next_to(bars[yrs.index(y0)], UP,
                                                                                         buff=0.1).shift(RIGHT * 0.9)
        l1 = tx(f"${rev[yrs.index(y1)]:.1f}bn, a profit of ${ni[y1]:.1f}bn", 16, BOOM).next_to(bars[yrs.index(y1)], UP,
                                                                                          buff=0.1).shift(LEFT * 0.6)
        crew = VGroup(draw.crane(1.2), draw.house(0.9, color=STONE), draw.house(0.9, color=STONE)).arrange(
            RIGHT, buff=0.2, aligned_edge=DOWN).move_to([-5.0, 1.6, 0])
        src = source("D.R. Horton, Forms 10-K, fiscal years to September 2009-2026 (SEC company facts)", size=13)
        with self.voiceover(
            "Who came out ahead? The builders that cut back hard in the bust, and could still pay their bills. "
            f"<bookmark mark='a'/> D.R. Horton, a Texas homebuilder, sold {rev[yrs.index(y0)]:.1f} billion dollars "
            f"of homes in its fiscal year 2009, and lost {-ni[y0]:.2f} billion. <bookmark mark='b'/> It kept going "
            "through the years when few houses were started. <bookmark mark='c'/> "
            f"By fiscal 2024 it sold {rev[yrs.index(y1)]:.1f} billion dollars of homes in a year and made "
            f"{ni[y1]:.1f} billion of profit. Getting through the bust was the first step to winning the boom that "
            "followed."
        ) as vo:
            self.play(FadeIn(src), FadeIn(crew, shift=UP * 0.2), FadeIn(pa), FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(l0))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[1:8]], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars[8:]], lag_ratio=0.2), run_time=2.0)
            self.play(FadeIn(l1))
        self.clear_scene()
