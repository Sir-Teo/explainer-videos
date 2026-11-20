from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ28.common import *  # noqa: F403

EVENTS = ((1968.0, r"1967: \ Friedman's address", EXPECT, 13.0), (1974.3, r"1973--74: \ oil", WAGE, 15.0),
          (1980.4, r"1979--82: \ Volcker", CB, 13.0), (2022.3, r"2021--23", INFL, 11.0))


class Intermission(SoundScene):
    """American inflation over twelve months and the unemployment rate, month by month from 1948 to the latest month,
    with a date counter and four moments marked as they pass; under it, inflation as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        u = load("us")
        A = load("accelerate")
        C = load("critique")
        clip = ClipStore("econ28").load("intermission.melody")
        t = np.array(film["t"], float)
        ax = plane([1948, 2026], [-3, 16], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.2, y_length=5.6,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15],
                   ylabel=r"percent", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        zero = seg(ax, 1948, 0, 2026, 0, color=GREY_D, width=2)

        def full(series, color):
            return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, y) for x, y in zip(t, series) if np.isfinite(y)])
        fi, fu = full(film["inflation"], INFL), full(film["unemployment"], UNEMP)
        gi, gu = fi.copy(), fu.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(f):
            def g(m, tt):
                frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
                m.pointwise_become_partial(f, 0, frac)
            return g

        year = Integer(1948, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2012, 14))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        marks = VGroup(*[label(say, font_size=16, color=c).move_to(ax.ax.c2p(when, y)) for when, say, c, y in EVENTS])

        def appear(when, ttl=7.0):
            at = film_time(when)

            def f(m, tt):
                m.set_opacity(float(np.clip((tt - at) / 0.6, 0, 1) * np.clip((at + ttl - tt) / 1.0, 0, 1)))
            return f

        for m in marks:
            m.set_opacity(0)
        legend = VGroup(label(r"inflation, \ 12 months", font_size=18, color=INFL),
                        label(r"unemployment rate", font_size=18, color=UNEMP)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        legend.move_to(ax.ax.c2p(1956, 14.5))
        src = data_tag(r"BLS: \ the CPI and the unemployment rate, \ monthly, \ via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ inflation \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"American inflation and unemployment, \ month by month since 1948; \ inflation as a tune")
            snd.show(src, stag)
            for g, f in ((gi, fi), (gu, fu)):
                snd.drive(g, grower(f))
            for mk, (when, _, _, _) in zip(marks, EVENTS):
                snd.drive(mk, appear(when))
            snd.drive(year, set_year)
            snd.show(ax, zero, gi, gu, year, legend, *marks)
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, zero, gi, gu, year, legend, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the menu", rf"the 1960s: \ down to {u['u1969']:.1f}\% \\ unemployment, \ at a price", CB),
                (r"you forecast", r"1973 and 1974: \\ looking back lags", EXPECT),
                (r"the natural rate", rf"hold $u$ below it: \\ inflation climbs {A['fast']['step']} a year", OUTPUT),
                (r"the Great Inflation", r"loops that start \\ higher each time", INFL),
                (r"rational expectations", r"no errors \\ you could predict", SURPRISE),
                (r"Lucas", rf"a fitted slope of {C['slope']:.1f} \\ that vanishes", WAGE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
