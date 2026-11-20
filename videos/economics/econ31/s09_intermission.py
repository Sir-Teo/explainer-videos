from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ31.common import *  # noqa: F403

CHAIRS = ((1951.25, r"Martin"), (1970.1, r"Burns"), (1979.6, r"Volcker"),
          (1987.6, r"Greenspan"), (2006.1, r"Bernanke"), (2014.1, r"Yellen"), (2018.1, r"Powell"))


class Intermission(SoundScene):
    """The effective federal funds rate, month by month, 1954 to 2026, drawn as it passes, with the chairs of the
    Federal Reserve marked as their terms begin; under it, the rate as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        M = load("mc")
        P = load("playit")
        U = load("usvar")
        clip = ClipStore("econ31").load("intermission.melody")
        t = np.array(film["t"], float)
        ff = np.array(film["ff"], float)
        ax = plane([1953.5, 2027.5], [0, 20], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"the effective federal funds rate, \ \%", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        full = VMobject(stroke_color=RATE, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, ff)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
            m.pointwise_become_partial(full, 0, frac)

        year = Integer(1954, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2008, 17))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        marks = VGroup()
        for k, (yr_, name) in enumerate(CHAIRS):
            x = max(yr_, 1954.0)
            ln = DashedLine(ax.ax.c2p(x, 0), ax.ax.c2p(x, 19.5), color=GREY_C, stroke_width=1.2)
            nm = label(name, font_size=15, color=GREY_A).rotate(PI / 2).next_to(ax.ax.c2p(x, 19.5), DOWN,
                                                                                  buff=0.1).shift(RIGHT * 0.14)
            marks.add(VGroup(ln, nm))
        src = data_tag(r"Federal Reserve Board: \ the effective federal funds rate, \ via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the funds rate \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the federal funds rate, \ 1954--2026, \ with the Fed's chairs; \ the rate as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            snd.show(ax, grow, year)
            self.play(FadeIn(ax), run_time=1.2)
            for (yr_, _), m in zip(CHAIRS, marks):
                snd.wait_until(film_time(max(yr_, t[0])))
                self.play(FadeIn(m), run_time=0.3)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, year, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the balance sheet", r"reserves: \ a corridor before 2008, \\ a floor since", CB),
                (r"the chair, \ 1979", rf"the gap of the day {P['gap_rt']:+.1f}\%; \\ today's "
                                      rf"{P['gap_today']:+.1f}\%", OUTPUT),
                (r"transmission", r"rates, \ credit, \ assets, \\ the currency, \ expectations", RATE),
                (r"the problem", r"the bank acts on what it sees: \\ rate rises predict booms", HOLD),
                (r"four answers", rf"narrative and clean surprises \\ find the truth; \ {M['reps']} Islands", PRICE),
                (r"the consensus", rf"output {U['commod']['ip_trough']['value']:+.1f}\% after "
                                   rf"{U['commod']['ip_trough']['h']} months; \\ prices later", INFL),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
