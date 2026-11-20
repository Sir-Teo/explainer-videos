from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ23.common import *  # noqa: F403


class Intermission(SoundScene):
    """A real dollar in American stocks and a real dollar in one-year bonds, from January 1871, year by year to 2013,
    on a log scale, with a year counter and the great falls marked as they pass; under it, the stock dollar as a rising
    tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ23").load("intermission.melody")
        years = np.array(film["years"], float)
        ax = plane([1870, 2015], [-0.3, 4.2], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.4, y_length=5.6,
                   xticks=[1880, 1900, 1920, 1940, 1960, 1980, 2000],
                   yticks=[0, 1, 2, 3, 4], ylabel=r"what a real dollar invested in 1871 became \ (log scale)",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: rf"\${10 ** v:,.0f}".replace(",", "{,}"), font_size=15)
        full_s = VMobject(stroke_color=STOCK, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, np.log10(v)) for x, v in zip(years, film["stock"])])
        full_b = VMobject(stroke_color=BILL, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, np.log10(v)) for x, v in zip(years, film["bill"])])
        gs, gb = full_s.copy(), full_b.copy()
        t0, t1 = film_time(years[0]), film_time(years[-1])

        def grower(full):
            def f(m, t):
                frac = float(np.clip((t - t0) / (t1 - t0), 1e-3, 1))
                m.pointwise_become_partial(full, 0, frac)
            return f

        year = Integer(1871, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1895, 3.6))

        def set_year(m, t):
            y = years[0] + (t - t0) / (t1 - t0) * (years[-1] - years[0])
            m.set_value(int(np.clip(y, years[0], years[-1])))

        marks = VGroup()
        for ev in film["events"]:
            k = int(np.argmin(np.abs(years - ev["year"])))
            p = ax.ax.c2p(ev["year"], np.log10(film["stock"][k]))
            tx = label(ev["say"], font_size=15, color=RISK).next_to(p, UP, buff=0.25)
            marks.add(tx)

        def appear(ev, ttl=6.0):
            def f(m, t):
                m.set_opacity(float(np.clip((t - ev["time"]) / 0.6, 0, 1) * np.clip((ev["time"] + ttl - t) / 1.0, 0, 1)))
            return f

        for m in marks:
            m.set_opacity(0)
        ends = VGroup(label(rf"stocks: \ \${commas(film['stock_end'])}", font_size=20, color=STOCK),
                      label(rf"one-year bonds: \ \${film['bill_end']:.0f}", font_size=20, color=BILL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1960, 0.4))
        src = data_tag(r"Shiller, \emph{Market Volatility} ch.\ 26 data, \ updated: \ real returns, \ dividends "
                       r"reinvested", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the stock dollar, \ rising \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"a real dollar in stocks and in bonds, \ 1871--2013; \ the stock dollar as a tune")
            snd.show(src, stag)
            snd.drive(gs, grower(full_s))
            snd.drive(gb, grower(full_b))
            for mk, ev in zip(marks, film["events"]):
                snd.drive(mk, appear(ev))
            snd.drive(year, set_year)
            snd.show(ax, gs, gb, year, *marks)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.play(FadeIn(ends), run_time=0.8)
            self.wait(1.5)
            self.play(*[FadeOut(m) for m in (ax, gs, gb, year, marks, ends, src, stag)], run_time=1.0)
            story = point_cards([
                (r"present value", r"one point on $r$: \\ a fifth off the price", STOCK),
                (r"user cost and $q$", r"build toward a target, \\ slowly", FIRM),
                (r"the option to wait", r"build at twice the cost \\ when value is volatile", FIRM),
                (r"Modigliani--Miller", r"the pie, \ not the slices; \\ and what breaks it", BILL),
                (r"the discount factor", r"one formula \\ prices everything", SDF),
                (r"the puzzle", r"0.35\% in the model, \\ 6\% in the record", RISK),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
