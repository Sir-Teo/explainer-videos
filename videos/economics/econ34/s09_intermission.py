from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ34.common import *  # noqa: F403

EVENTS = ((1976.75, r"1976: \ the IMF loan"), (1985.1, r"1985"), (1992.7, r"1992"), (2008.8, r"2008"),
          (2016.5, r"2016: \ the referendum"), (2022.75, r"2022"))


class Intermission(SoundScene):
    """The pound's price in dollars, month by month since 1971, drawn as it passes, with six dates marked; under it,
    the price as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        S = load("story")
        Q = load("ppp")
        U = load("uip")
        M = load("meese")
        D = load("dornbusch")
        clip = ClipStore("econ34").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        ax = plane([1970, 2028], [1.0, 2.7], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[1.0, 1.5, 2.0, 2.5],
                   ylabel=r"dollars per pound, \ monthly", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"\\${y:.2f}",
                   font_size=15)
        full = VMobject(stroke_color=GBP, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            m.pointwise_become_partial(full, 0, float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1)))

        year = Integer(1971, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2012, 2.45))

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(
            ax.ax.c2p(x, float(np.interp(x, t, v))), DOWN, buff=0.15) for x, n in EVENTS])
        for (x, _), m in zip(EVENTS, marks):
            snd_ft = film_time(x)
            m.ft = snd_ft
        src = data_tag(r"Board of Governors (H.10), \ via FRED: \ EXUSUK", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the pound in dollars \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                    buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the pound in dollars, \ 1971--2026; \ the price as a tune")
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
                (r"1992", rf"in the ERM band, \\ then out: \ $-{S['fall']:.0f}\%$ against the mark", GBP),
                (r"the Big Mac", rf"\${Q['pick']['Switzerland']['price']:.2f} in Switzerland, \\ "
                                 rf"\${Q['pick']['India']['price']:.2f} in India", PRICE),
                (r"parity's half-life", rf"{Q['full']['halflife']:.1f} years since 1870, \\ "
                                        rf"{Q['floating']['halflife']:.1f} since 1973", DEM),
                (r"Fama's slope", rf"below zero for \\ {U['negative']} of 7 currencies", CRISIS),
                (r"the random walk", r"no model gains \\ at 1 to 12 months", WHITE),
                (r"overshooting", rf"money +10\%: \\ the currency +{100 * D['jump']:.0f}\% at once", USD),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        del M
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
