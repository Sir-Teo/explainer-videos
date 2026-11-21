from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ49.common import *  # noqa: F403


class Intermission(SoundScene):
    """The world's children per woman, year by year since 1950, drawn as the years pass; under it, the series as a
    tune; then the story so far."""

    def construct(self):
        film = load("film")
        O = load("offenders")
        Pl = load("police")
        M = load("marriage")
        A = load("angrist")
        B = load("bargain")
        clip = ClipStore("econ49").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        events = ((1950.0, rf"1950: \ {film['first']:.2f}", DR),
                  (float(film["peak_t"]), rf"{int(film['peak_t'])}: \ the peak, \ {film['peak']:.2f}", UP),
                  (1980.0, rf"1980: \ {film['v1980']:.2f}", UR),
                  (2000.0, rf"2000: \ {film['v2000']:.2f}", UR),
                  (float(t[-1]), rf"{int(t[-1])}: \ {film['last']:.2f}", DOWN))
        ax = plane([1948, 2026], [1.5, 5.6], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[2, 3, 4, 5],
                   ylabel=r"children per woman, \ the world", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}",
                   font_size=15)
        rep = DashedLine(ax.ax.c2p(1948, 2.1), ax.ax.c2p(2026, 2.1), color=GREY_B, stroke_width=1.4)
        year = Integer(1950, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2010, 5.0))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=CHILD, stroke_width=3.4)
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
            m = label(n, font_size=16, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.2)
            m.ft = film_time(x)
            marks.add(m)
        src = data_tag(r"UN World Population Prospects, \ via Our World in Data", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the series \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the world's children per woman, \ 1950--2023; \ the value as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, rep, grow, year, marks)
            self.play(FadeIn(ax), FadeIn(rep), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, rep, grow, year, marks, src, stag)], run_time=1.0)
            rn = O["play"]
            story = point_cards([
                (r"crime as a choice", rf"offend if the gain beats \ $p \times S$: \ "
                                       rf"{100 * rn['risk-neutral']['start']:.0f}\% do", CRIME),
                (r"the chance or the sentence", r"for those who discount the \ future, \ the chance", CHANCE),
                (r"police, \ measured", rf"naive \ {Pl['naive']:+.2f}; \ random \ {Pl['experiment']:+.2f}"
                 .replace("-", "{-}"), POLICE),
                (r"marriage", rf"like marries like: \ {M['sorting']:.1f} times chance", CHILD),
                (r"a third child", rf"about {abs(A['wald']['wald']):.0f} weeks less work a year", WOMEN),
                (r"whose purse", rf"a tenth to her: \ child spending \ {100 * B['rise']:+.0f}\%", GAIN),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
