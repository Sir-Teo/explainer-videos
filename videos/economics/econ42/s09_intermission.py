from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ42.common import *  # noqa: F403


class Intermission(SoundScene):
    """Continued claims for state unemployment insurance, quarter by quarter since 1967, drawn on a log scale as the
    years pass; under it, the claims as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        P = load("pooling")
        B = load("baily")
        W = load("weekly")
        H = load("health")
        clip = ClipStore("econ42").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.log10(np.array(film["v"], float))
        events = ((1967.0, r"1967: \ 1.2 million", UP),
                  (1982.75, rf"1982--83: \ {film['y1982']:.1f} million", UP),
                  (2009.25, rf"2009: \ {film['y2009']:.1f} million", UP),
                  (float(film["peak_t"]), rf"2020: \ {film['peak']:.0f} million", LEFT),
                  (float(t[-1]), rf"2026: \ {film['last']:.1f} million", DOWN))
        ax = plane([1965, 2028], [np.log10(0.8), np.log10(25)], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6,
                   y_length=5.4, xticks=[1970, 1980, 1990, 2000, 2010, 2020],
                   yticks=[np.log10(x) for x in (1, 2, 5, 10, 20)],
                   ylabel=r"continued claims for state unemployment insurance, \ millions \ (log scale)",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{10 ** y:.0f}", font_size=15)
        year = Integer(1967, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1985, 1.25))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=UNEMP, stroke_width=3.2)
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
        src = data_tag(r"Employment and Training Administration, \ via FRED: \ CCSA \ (quarterly averages)",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the claims \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"continued claims for unemployment insurance, \ 1967--2026; \ the value as a tune")
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
                (r"pooling", rf"recessions keep the \\ spread above {100 * P['floor']:.0f}\%: \\ the state can borrow",
                 RISK),
                (r"the best benefit", rf"{100 * B['bstar']:.0f}\% of the wage \\ on the Island", GAIN),
                (r"the formula", r"$\gamma\,\Delta c/c \approx \varepsilon$", THEORY),
                (r"durations", rf"elasticity {W['level']:.2f} \\ on the Island; \\ 0.4 to 0.8 measured", COST),
                (r"health care", rf"the best plan: \\ pay {100 * H['cstar']:.0f}\% of each bill", HEALTH),
                (r"Oregon", r"more care, \ less strain \\ and depression; \\ blood pressure unclear", LOTTO),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
