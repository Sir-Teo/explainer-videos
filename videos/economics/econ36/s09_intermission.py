from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ36.common import *  # noqa: F403

EVENTS = ((1990.0, r"1990", UP), (2001.95, r"2001: \ China joins the WTO", LEFT), (2009.0, r"2009", DOWN),
          (2018.5, r"2018: \ the tariffs", UP), (2025.0, r"2025", RIGHT))


class Intermission(SoundScene):
    """America's imports of goods from China, year by year since 1985, drawn as they pass, with five dates marked;
    under them, the imports as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        P = load("playit")["pairs"]
        G = load("gravity")
        F = load("firms")
        M = load("melitz")
        K = load("krugman")
        clip = ClipStore("econ36").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        ax = plane([1984, 2027], [0, 600], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1985, 1995, 2005, 2015, 2025], yticks=[0, 100, 200, 300, 400, 500, 600],
                   ylabel=r"US imports of goods from China, \ \$ billion a year", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        full = VMobject(stroke_color=CHINA, stroke_width=3.2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            m.pointwise_become_partial(full, 0, float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1)))

        year = Integer(1985, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1993, 480))

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for x, n, d in EVENTS:
            y = float(np.interp(x, t, v))
            m = label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.15)
            m.ft = film_time(x)
            marks.add(m)
        src = data_tag(r"US Census Bureau, \ via FRED: \ IMPCH", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ imports from China \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"America's imports from China, \ 1985--2025; \ the value as a tune")
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
                (r"cars for cars", r"two-way trade \\ in the same goods", FISH),
                (r"variety", rf"two islands: \\ real wages +{100 * K['gain2']:.0f}\%", ARCH),
                (r"gravity", rf"Spain sells Portugal \\ \${P['PRT']['actual']:.0f}bn, \ Japan "
                             rf"\${P['JPN']['actual']:.0f}bn", GAIN),
                (r"distance", rf"elasticity {G['ppml'][0]:.2f} \\ (PPML)", WHITE),
                (r"firms", rf"{100 * F['share_exporters']:.0f}\% export, \\ selling "
                           rf"{100 * F['sales_share_exporters']:.0f}\%", FIRM),
                (r"selection", rf"opening: \ productivity \\ +{100 * M['welfare_gain']:.1f}\%", TARIFF),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
