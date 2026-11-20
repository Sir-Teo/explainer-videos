from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ37.common import *  # noqa: F403

US = "#7EC8F5"
CN = "#F25F5C"


class Intermission(SoundScene):
    """The share of the world's people living in towns and cities, from 1500 to 2025, drawn as the years pass, with
    America and China beside it; under it, the world's share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        S = load("schelling")
        M = load("mono")
        A = load("agglo")
        Z = load("zipf")
        C = load("cp")
        clip = ClipStore("econ37").load("intermission.melody")
        events = ((1800.0, rf"1800: \ {film['v1800']:.0f}\%", UP), (1900.0, rf"1900: \ {film['v1900']:.0f}\%", UP),
                  (1950.0, rf"1950: \ {film['v1950']:.0f}\%", UP),
                  (float(film["half"]), rf"{film['half']}: \ half the world", LEFT),
                  (2025.0, rf"2025: \ {film['last']:.0f}\%", RIGHT))
        ax = plane([1490, 2035], [0, 100], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1500, 1600, 1700, 1800, 1900, 2000], yticks=[0, 25, 50, 75, 100],
                   ylabel=r"share of people living in towns and cities, \ \%", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)

        t0, t1 = film_time(1500), film_time(2025)

        def series(t, v, col, width):
            t, v = np.array(t, float), np.array(v, float)
            keep = t >= 1500
            t, v = t[keep], v[keep]
            m = VMobject(stroke_color=col, stroke_width=width)
            m.set_points_as_corners([ax.ax.c2p(t[0], v[0]), ax.ax.c2p(t[0] + 0.5, v[0])])
            return (t, v), m

        def grower(tv):
            t, v = tv

            def f(m, tt):
                yr = 1500 + float(np.clip((tt - t0) / (t1 - t0), 0, 1)) * 525
                k = int(np.searchsorted(t, yr, side="right"))
                xs = list(t[:k]) + [yr]
                ys = list(v[:k]) + [float(np.interp(yr, t, v))]
                if len(xs) < 2:
                    xs, ys = [t[0], t[0] + 0.5], [v[0], v[0]]
                m.set_points_as_corners([ax.ax.c2p(x, y) for x, y in zip(xs, ys)])
            return f

        world, grow_w = series(film["t"], film["v"], E.ACCENT, 3.6)
        us, grow_u = series(film["us_t"], film["us_v"], US, 2.2)
        cn, grow_c = series(film["cn_t"], film["cn_v"], CN, 2.2)

        year = Integer(1500, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1620, 80))

        def set_year(m, tt):
            m.set_value(int(np.clip(1500 + (tt - t0) / (t1 - t0) * 525, 1500, 2025)))

        marks = VGroup()
        for x, n, d in events:
            y = float(np.interp(x, film["t"], film["v"]))
            m = label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.15)
            m.ft = film_time(x)
            marks.add(m)
        keys = VGroup(label(r"the world", font_size=16, color=E.ACCENT), label(r"the United States", font_size=16,
                                                                              color=US),
                      label(r"China", font_size=16, color=CN)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(
            ax.ax.c2p(1560, 55))
        src = data_tag(r"HYDE 3.5, \ via Our World in Data", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the world's urban share \ (computed)", font_size=13, color=E.ACCENT).to_corner(
            UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"Five centuries of moving to town, \ 1500--2025; \ the world's share as a tune")
            snd.show(src, stag)
            for g_, full in ((grow_w, world), (grow_u, us), (grow_c, cn)):
                snd.drive(g_, grower(full))
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, grow_w, grow_u, grow_c, year, marks, keys)
            self.play(FadeIn(ax), FadeIn(keys), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow_w, grow_u, grow_c, year, marks, keys, src, stag)],
                      run_time=1.0)
            story = point_cards([
                (r"Schelling", rf"content with a third alike: \\ {100 * S['start']:.0f}\% $\to$ "
                               rf"{100 * S['final']:.0f}\% alike", TEAL),
                (r"the city", rf"the car: \ edge {M['base']['edge']:.0f} $\to$ \\ {M['car']['edge']:.0f} km",
                 CITY),
                (r"agglomeration", rf"across towns {A['naive']:.3f}, \\ movers {A['movers']:.3f}", WAGE),
                (r"Zipf", rf"America's top 100: \\ exponent {Z['zeta_100']:.2f}", GOLD),
                (r"the tomahawk", rf"the even spread \\ breaks at {C['break']:.2f}", RENT),
                (r"half the world", rf"urban since {film['half']}", E.ACCENT),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
