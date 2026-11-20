from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ33.common import *  # noqa: F403

EVENTS = ((1907, r"1907"), (1931, r"1931"), (1991, r"1991"), (2008, r"2008"))


class Intermission(SoundScene):
    """The median of bank loans to GDP across eighteen economies, year by year from 1870 to 2020, drawn as it passes,
    with each year's new crises as red ticks along the bottom; under it, the median as a tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        F = load("fisher")
        B = load("bgg")
        K = load("km")
        L = load("leverage")
        G = load("gfc")
        clip = ClipStore("econ33").load("intermission.melody")
        t = np.array(film["years"], float)
        v = np.array(film["median"], float)
        cr = np.array(film["crises"], int)
        ax = plane([1868, 2022], [-12, 120], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1870, 1900, 1930, 1960, 1990, 2020], yticks=[0, 30, 60, 90, 120],
                   ylabel=r"bank loans to GDP, \ \%, \ the median of 18 economies", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        full = VMobject(stroke_color=CREDIT, stroke_width=3.2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            m.pointwise_become_partial(full, 0, float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1)))

        year = Integer(1870, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1915, 100))

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        ticks = VGroup(*[Line(ax.ax.c2p(x, -11), ax.ax.c2p(x, -11 + 2.2 * n), color=CRISIS, stroke_width=4)
                         for x, n in zip(t, cr) if n > 0])
        tick_t = [x for x, n in zip(t, cr) if n > 0]
        marks = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, -11 + 2.2 * cr[int(x - 1870)]),
                                                                   UP, buff=0.08) for x, n in EVENTS])
        src = data_tag(r"Jord\`a, \ Schularick and Taylor, \ Macrohistory Database R6", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the median loans ratio \ (computed); \ red ticks: \ new crises that year",
                    font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"bank loans to GDP in 18 economies, \ 1870--2020; \ the median as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            snd.show(ax, grow, year)
            self.play(FadeIn(ax), run_time=1.2)
            k = 0
            for x, m in zip(tick_t, ticks):
                snd.wait_until(film_time(x))
                anims = [GrowFromEdge(m, DOWN)]
                while k < len(EVENTS) and EVENTS[k][0] <= x:
                    anims.append(FadeIn(marks[k]))
                    k += 1
                self.play(*anims, run_time=0.25)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, year, ticks, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the pattern", r"displacement, \ credit boom, \\ euphoria, \ distress, \ panic", HOUSE),
                (r"debt deflation", rf"loans $-{F['loans_fall']:.0f}\%$, \ yet \\ loans to GDP "
                                    rf"{F['ratio29']:.0f}\% $\to$ {F['ratio32']:.0f}\%", CREDIT),
                (r"the accelerator", rf"net worth $-{100 * B['N_fall']:.0f}\%$: \\ investment "
                                     rf"{B['K_fall']:.1f}\%", RATE),
                (r"collateral", rf"a 1\% shock moves \\ farmers' land {K['dynamic']:.1f}\%", HOUSE),
                (r"leverage", rf"price {L['cycle']['p0']:.2f} $\to$ {L['cycle']['pD']:.2f}; \\ margins "
                              rf"{100 * L['cycle']['margin0']:.0f}\% $\to$ {100 * L['cycle']['marginD']:.0f}\%",
                 CRISIS),
                (r"2008", rf"the Fed's assets \\ \${G['wal_before']:.2f} $\to$ \${G['wal_after']:.2f} trillion",
                 CB),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
