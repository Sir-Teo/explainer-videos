from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ24.common import *  # noqa: F403

EVENTS = ((2008.9, r"the financial crisis"), (2020.3, r"the pandemic: \ {peak:.1f}\%"),
          (2022.2, r"two openings per searcher"))


class Intermission(SoundScene):
    """The American Beveridge curve drawn month by month from December 2000 to the latest JOLTS month, with a date
    counter and the three great moves marked as they pass; under it, openings per unemployed worker as a tune; then
    the story so far."""

    def construct(self):
        film = load("film")
        j = load("jolts")
        clip = ClipStore("econ24").load("intermission.melody")
        t = np.array(film["t"], float)
        ax = plane([3, 15], [1.5, 7.5], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.0, y_length=5.6,
                   xticks=[3, 5, 7, 9, 11, 13, 15], yticks=[2, 3, 4, 5, 6, 7],
                   xlabel=r"unemployment rate, \ \%", ylabel=r"job openings rate, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        full = VMobject(stroke_color=TIGHT, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(film["u"], film["v"])])
        grow = full.copy()
        head = Dot(ax.ax.c2p(film["u"][0], film["v"][0]), radius=0.1, color=E.ACCENT)
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
            m.pointwise_become_partial(full, 0, frac)

        def mover(m, tt):
            yr = t[0] + np.clip((tt - t0) / (t1 - t0), 0, 1) * (t[-1] - t[0])
            m.move_to(ax.ax.c2p(float(np.interp(yr, t, film["u"])), float(np.interp(yr, t, film["v"]))))

        year = Integer(2000, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(12.5, 6.6))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        marks = VGroup()
        for when, say in EVENTS:
            p = ax.ax.c2p(float(np.interp(when, t, film["u"])), float(np.interp(when, t, film["v"])))
            say = say.replace("{peak:.1f}", f"{max(film['u']):.1f}")
            marks.add(label(say, font_size=16, color=SEP).next_to(p, UP + RIGHT, buff=0.15))

        def appear(when, ttl=6.0):
            at = film_time(when)

            def f(m, tt):
                m.set_opacity(float(np.clip((tt - at) / 0.6, 0, 1) * np.clip((at + ttl - tt) / 1.0, 0, 1)))
            return f

        for m in marks:
            m.set_opacity(0)
        src = data_tag(r"BLS: \ JOLTS openings and the CPS, \ via FRED", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ openings per unemployed worker \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the American Beveridge curve, \ month by month, \ 2000--2026; \ openings per searcher "
                        r"as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(head, mover)
            snd.drive(year, set_year)
            for mk, (when, _) in zip(marks, EVENTS):
                snd.drive(mk, appear(when))
            snd.show(ax, grow, head, year, *marks)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, head, year, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"stocks and flows", rf"{j['mean_hires'] / 1000:.0f} million hires a month, \\ a net change of "
                                      rf"{j['mean_net']:.0f} thousand", WORKER),
                (r"the reservation wage", r"stop when looking on \\ costs what it gains", BENEFIT),
                (r"the Beveridge curve", r"along it in booms and slumps, \\ out when matching worsens", TIGHT),
                (r"the matching function", r"constant returns, \\ $\eta$ about a half or more", MATCH),
                (r"DMP", r"free entry and bargaining \\ fix tightness", JOB),
                (r"Hosios", r"efficient only if \\ $\beta = \eta$", WAGE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            ttl = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(ttl), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
