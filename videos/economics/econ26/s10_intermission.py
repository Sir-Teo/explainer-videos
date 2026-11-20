from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ26.common import *  # noqa: F403

EVENTS = ((2022.21, r"March 2022: \ the Fed starts raising rates", RATE),
          (2023.19, r"March 2023: \ Silicon Valley Bank", RUN),
          (2023.33, r"1 May 2023: \ First Republic fails", RUN))


class Intermission(SoundScene):
    """Deposits at small and large American banks, each set to 100 in the first week of 2022, week by week to the end
    of 2024, with a date counter and three moments marked as they pass; under it, small banks' deposits as a tune;
    then the story so far."""

    def construct(self):
        film = load("film")
        r = load("run")
        L = load("llr")
        clip = ClipStore("econ26").load("intermission.melody")
        t = np.array(film["t"], float)
        sm = 100 * np.array(film["small"]) / film["small"][0]
        lg = 100 * np.array(film["large"]) / film["large"][0]
        ax = plane([2022, 2025], [92, 106], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.2, y_length=5.6,
                   xticks=[2022, 2023, 2024, 2025], yticks=[92, 96, 100, 104],
                   ylabel=r"deposits, \ first week of 2022 $= 100$", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=15)

        def full(series, color):
            return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, y) for x, y in zip(t, series)])
        fs, fl = full(sm, DEPOSIT), full(lg, BOND)
        gs, gl = fs.copy(), fl.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(f):
            def g(m, tt):
                frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
                m.pointwise_become_partial(f, 0, frac)
            return g

        year = DecimalNumber(2022.0, num_decimal_places=1, font_size=48, color=E.ACCENT,
                             group_with_commas=False).move_to(ax.ax.c2p(2024.4, 104.8))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(float(np.clip(yr, t[0], t[-1])))

        marks = VGroup()
        for when, say, c in EVENTS:
            k = int(np.argmin(np.abs(t - when)))
            marks.add(label(say, font_size=16, color=c).next_to(ax.ax.c2p(when, min(sm[k], lg[k])), DOWN, buff=0.35))

        def appear(when, ttl=7.0):
            at = film_time(when)

            def f(m, tt):
                m.set_opacity(float(np.clip((tt - at) / 0.6, 0, 1) * np.clip((at + ttl - tt) / 1.0, 0, 1)))
            return f

        for m in marks:
            m.set_opacity(0)
        legend = VGroup(label(r"small banks", font_size=18, color=DEPOSIT),
                        label(r"the 25 largest banks", font_size=18, color=BOND)).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        legend.move_to(ax.ax.c2p(2022.35, 104.6))
        ends = VGroup(label(rf"small banks: \ {sm[-1]:.0f}", font_size=19, color=DEPOSIT),
                      label(rf"largest banks: \ {lg[-1]:.0f}", font_size=19, color=BOND)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(2024.5, 93.5))
        src = data_tag(r"Federal Reserve, \ H.8, \ weekly, \ via FRED", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ small banks' deposits \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                         buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"deposits at small and large American banks, \ 2022--2024; \ small banks' as a tune")
            snd.show(src, stag)
            for g, f in ((gs, fs), (gl, fl)):
                snd.drive(g, grower(f))
            for mk, (when, _, _) in zip(marks, EVENTS):
                snd.drive(mk, appear(when))
            snd.drive(year, set_year)
            snd.show(ax, gs, gl, year, legend, *marks)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(FadeIn(ends), run_time=0.8)
            self.wait(1.2)
            self.play(*[FadeOut(m) for m in (ax, gs, gl, year, legend, marks, ends, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the bank", r"liquid deposits, \\ illiquid loans", DEPOSIT),
                (r"Diamond--Dybvig", rf"insurance against impatience: \\ {r['c1']:.2f} early, \ "
                                     rf"{r['c2_guaranteed']:.2f} late", STAY),
                (r"the run", rf"first come, \ first served: \\ {100 * r['share_served']:.0f}\% are paid", RUN),
                (r"the cures", r"suspension, \ insurance: \\ 1934's 44 failures", CB),
                (r"Bagehot", rf"a fire sale, \ equity {L['equity_fire']:.1f}; \\ a lender, \ equity "
                             rf"{L['equity_llr']:.0f}", CB),
                (r"the price", r"moral hazard, \\ and capital", EQUITY),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
