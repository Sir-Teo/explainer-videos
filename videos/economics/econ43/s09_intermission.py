from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ43.common import *  # noqa: F403


class Intermission(SoundScene):
    """Corporate profits after tax as a share of GDP, quarter by quarter since 1947, drawn as the years pass; under it,
    the share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        S = load("scp")
        G = load("playit")
        C = load("cars")
        B = load("blpdata")
        clip = ClipStore("econ43").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)

        def at(year):
            return float(v[int(np.argmin(np.abs(t - year)))])
        events = ((1947.0, rf"1947: \ {film['first']:.1f}\%", DOWN),
                  (1966.0, rf"1966: \ {at(1966.0):.1f}\%", UP),
                  (1986.75, rf"1986: \ {at(1986.75):.1f}\%", DOWN),
                  (2011.75, rf"2011: \ {at(2011.75):.1f}\%", UP),
                  (float(t[-1]), rf"2026: \ {film['last']:.1f}\%", LEFT))
        ax = plane([1945, 2028], [2, 13], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[2, 4, 6, 8, 10, 12],
                   ylabel=r"corporate profits after tax, \ percent of GDP", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}\\%", font_size=15)
        year = Integer(1947, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1985, 11.5))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=PROFIT, stroke_width=3.2)
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
        src = data_tag(r"BEA, \ via FRED: \ CPATAX \ (with inventory and capital consumption adjustments) \ over GDP",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the profit share \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"corporate profits after tax as a share of GDP, \ 1947--2026; \ the value as a tune")
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
            x, y = G["x"], G["y"]
            story = point_cards([
                (r"structure", rf"concentration and \\ margins correlate \\ ({S['corr']:.2f}) with no \\ collusion "
                               r"at all", LOSS),
                (r"the merger game", rf"the small twins: \\ +{100 * x['merged']:.0f}\%; \ the two \\ largest: "
                                     rf"+{100 * y['merged']:.0f}\%", NEST[2]),
                (r"conduct", r"a rotation of \\ demand reveals it", THEORY),
                (r"logit", r"one parameter of \\ substitution; \ the \\ red bus problem", IV_C),
                (r"BLP", rf"centred on the \\ truth: \ $\alpha$ = {C['mean']['blp_alpha']:.2f} \\ against "
                         rf"{C['alpha']}", BLP_C),
                (r"real cars", rf"plain logit: \\ {B['iv']['inelastic']} impossible \\ answers, \ even by IV", PRICE),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
