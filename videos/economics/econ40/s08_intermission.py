from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ40.common import *  # noqa: F403


class Intermission(SoundScene):
    """The share of income received by the top 1% of American tax units, year by year since 1913, drawn as the years
    pass; under it, the share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        P = load("parade")
        Pa = load("pareto")
        S = load("speed")
        W = load("wealth")
        M = load("measures")
        clip = ClipStore("econ40").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        val = dict(zip(film["t"], film["v"]))
        events = ((1913.0, rf"1913: \ {val[1913]:.1f}\%", DOWN),
                  (1928.0, rf"1928: \ {val[1928]:.1f}\%", UP),
                  (float(film["low_y"]), rf"{film['low_y']}: \ {film['low']:.1f}\%, \ the lowest", DOWN),
                  (2022.0, rf"2022: \ {val[2022]:.1f}\%", UP))
        ax = plane([1910, 2025], [0, 25], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 5, 10, 15, 20, 25],
                   ylabel=r"share of income received by the top 1\% of tax units",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}\\%", font_size=15)
        year = Integer(1913, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1955, 22))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=TOP, stroke_width=3.6)
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow.set_points_as_corners([pts[0], pts[0]])

        def grower(m, tt):
            yr = float(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1]))
            k = int(np.searchsorted(t, yr, side="right"))
            ps = pts[:max(k, 1)]
            if k < len(t):
                f = (yr - t[k - 1]) / (t[k] - t[k - 1])
                ps = ps + [pts[k - 1] + f * (pts[k] - pts[k - 1])]
            if len(ps) < 2:
                ps = [ps[0], ps[0]]
            m.set_points_as_corners(ps)

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for x, n, d in events:
            y = float(np.interp(x, t, v))
            m = label(n, font_size=16, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.25)
            m.ft = film_time(x)
            marks.add(m)
        src = data_tag(r"Piketty and Saez (2003), \ updated to 2022: \ income excluding capital gains",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the top 1\% share \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                      buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the top 1\% share, \ 1913--2022; \ the value as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, grow, year, marks)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, year, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the parade", rf"average height at minute {P['minute_mean']:.0f}; \\ the top 0.01\%: \ "
                                rf"{P['h_top001']:.0f} m", TOP),
                (r"the measures", rf"the Island's Gini {M['m']['gini']['value']:.2f}; \\ crossing curves need "
                                  r"\\ a value judgement", LORENZ),
                (r"a U", rf"the top 1\% share: \\ {film['y1928']:.0f}\% in 1928, \\ {film['low']:.0f}\% in "
                        rf"{film['low_y']}, \ {film['last']:.0f}\% in 2022", LOSS),
                (r"Pareto", rf"$\alpha$: \ {Pa['a1970']:.1f} in 1970, \\ {Pa['a2022']:.1f} in 2022", TOP),
                (r"the speed", rf"random growth: \ {S['hl_pure']:.0f} years; \\ fast types: \ "
                               rf"{S['hl_types']:.0f}", TYPES),
                (r"wealth", rf"the top 1\%: \ {W['last']['top1']:.1f}\%; \\ the bottom half: \ "
                            rf"{W['last']['bottom50']:.1f}\%", WEALTH),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
