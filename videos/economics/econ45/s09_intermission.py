from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ45.common import *  # noqa: F403


class Intermission(SoundScene):
    """The American personal saving rate, quarter by quarter since 1959, drawn as the years pass; under it, the rate
    as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        G = load("gym")
        M = load("mugs")
        S = load("seed")
        N = load("enrol")
        clip = ClipStore("econ45").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        events = ((float(t[0]), rf"1959: \ {film['first']:.0f}\%", UP),
                  (1975.25, r"the 1970s: \ above 10\%", UP),
                  (float(film["low_t"]), rf"2005: \ {film['low']:.1f}\%", DOWN),
                  (float(film["peak_t"]), rf"2020: \ {film['peak']:.0f}\%", LEFT),
                  (float(t[-1]), rf"2026: \ {film['last']:.1f}\%", DOWN))
        ax = plane([1957, 2028], [0, 26], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15, 20, 25],
                   ylabel=r"personal saving, \ percent of disposable income", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        year = Integer(1959, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1995, 21))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=GYM, stroke_width=3.2)
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
        src = data_tag(r"U.S. Bureau of Economic Analysis, \ via FRED: \ PSAVERT \ (quarterly averages)",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the saving rate \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the American personal saving rate, \ 1959--2026; \ the value as a tune")
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
                (r"the gym", rf"forecast {G['forecast']:.0f} visits, \\ made {G['visits']:.1f}: \\ "
                             rf"\${G['price_per_visit']:.0f} a visit", GYM),
                (r"the mug", rf"asks {M['loss']['ratio']:.0f}$\times$ bids; \\ {100 * M['loss']['share_traded']:.0f}\% "
                             r"traded, \\ not 50\%", SELL),
                (r"prospect theory", r"$\lambda$ = 2.25: \\ losses loom larger", LOSS),
                (r"the kink", r"runners bunch \\ under round times", PLAN),
                (r"commitment", rf"{100 * S['take_up']:.0f}\% take a lock; \\ mostly sophisticates", SOPH),
                (r"defaults", rf"{100 * N['opt_in_naif']['participation'][11]:.0f}\% against "
                              rf"{100 * N['auto_naif']['participation'][11]:.0f}\% \\ for naifs", NUDGE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
