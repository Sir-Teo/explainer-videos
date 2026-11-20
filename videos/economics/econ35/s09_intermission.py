from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ35.common import *  # noqa: F403

EVENTS = ((1930.5, r"1930: \ Smoot-Hawley", RIGHT), (1934.5, r"1934: \ reciprocal agreements", RIGHT),
          (1947.8, r"1947: \ the GATT", DOWN), (1967.5, r"1967: \ the Kennedy Round", UP),
          (1995.0, r"1995: \ the WTO", UP), (2018.5, r"2018", UP), (2025.0, r"2025", LEFT))


class Intermission(SoundScene):
    """America's customs duties as a share of its imports of goods, year by year since 1929, drawn as it passes, with
    seven dates marked; under it, the rate as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        P = load("playit")
        R = load("ricardo")
        J = load("japan")
        S = load("stolper")
        L = load("leontief")
        clip = ClipStore("econ35").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        ax = plane([1928, 2027], [0, 20], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"customs duties, \ \% of the value of goods imported", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}\\%", font_size=15)
        full = VMobject(stroke_color=TARIFF, stroke_width=3.2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            m.pointwise_become_partial(full, 0, float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1)))

        year = Integer(1929, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2010, 17))

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for x, n, d in EVENTS:
            y = float(np.interp(x, t, v))
            m = label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.15)
            m.ft = film_time(x)
            marks.add(m)
        src = data_tag(r"BEA, \ via FRED: \ B235RC1A027NBEA \ over A255RC1A027NBEA", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ America's tariff \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"America's average tariff on goods, \ 1929--2025; \ the rate as a tune")
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
                (r"four numbers", rf"the weaker island gains \\ {100 * P['island']['gain']:.0f}\%, \ the stronger "
                                  rf"{100 * P['arch']['gain']:.0f}\%", ISLAND),
                (r"Ricardo", rf"wine for cloth at {R['p']:.0f}: \\ both save labour", WINE),
                (r"Japan, \ 1868--75", rf"the test passes \\ in {J['negative']} of 8 years", CLOTH),
                (r"factor proportions", r"each exports \\ its abundant factor", CAPITAL),
                (r"Stolper-Samuelson", rf"cloth +10\%: \\ wage {100 * S['dw']:+.0f}\%, \ rent {100 * S['dr']:+.0f}\%",
                 LABOUR),
                (r"the missing trade", rf"right sign {100 * L['sign_test']:.0f}\% \\ of the time", TARIFF),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
