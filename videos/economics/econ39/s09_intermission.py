from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ39.common import *  # noqa: F403


class Intermission(SoundScene):
    """The college premium (the median weekly earnings of full-time college graduates over those of high-school
    graduates), year by year since 1979, drawn as the years pass; under it, the premium as a tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        R = load("resume")
        Rc = load("race")
        Fm = load("firms")
        S = load("stars")
        clip = ClipStore("econ39").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        val = dict(zip(film["t"], film["v"]))
        events = ((1979.0, rf"1979: \ {val[1979]:.2f}", DOWN),
                  (1992.0, rf"1992: \ {val[1992]:.2f}", UP),
                  (float(film["peak_y"]), rf"{film['peak_y']}: \ {film['peak']:.2f}, \ the peak", UP),
                  (2025.0, rf"2025: \ {val[2025]:.2f}", DOWN))
        ax = plane([1977, 2027], [1.2, 2.0], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[1.2, 1.4, 1.6, 1.8, 2.0],
                   ylabel=r"college graduates' median weekly pay over high-school graduates'",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.1f}", font_size=15)
        year = Integer(1979, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2014, 1.35))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=COLLEGE, stroke_width=3.6)
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
        src = data_tag(r"BLS, \ Current Population Survey, \ via FRED: \ LEU0252918500A, \ LEU0252917300A",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the college premium \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                        buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the college premium, \ 1979--2025; \ the value as a tune")
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
                (r"the r\'esum\'es", rf"White names: \\ {100 * (R['ratio'] - 1):.0f}\% more call-backs", WHITE_N),
                (r"the premium", rf"{film['first']:.2f} in 1979, \\ {film['last']:.2f} in 2025", COLLEGE),
                (r"the race", rf"demand for skill: \\ {100 * Rc['d141_rates']['1992-2000']:.1f}\% a year in the 1990s, "
                              rf"\\ {100 * Rc['d141_rates']['2010-2025']:.1f}\% since 2010", DEMAND),
                (r"polarization", r"jobs grew at both ends, \\ shrank in the middle", EMP),
                (r"firms", rf"on the Island: \ {100 * Fm['est']['share_psi']:.0f}\% of the \\ variance; \ "
                           rf"sorting {100 * Fm['est']['share_cov']:.0f}\%", FIRM),
                (r"the labour share", rf"down {100 * (1 - S['ls2025'] / S['ls1980']):.0f}\% since 1980", WAGE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
