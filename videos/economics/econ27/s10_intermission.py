from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ27.common import *  # noqa: F403

# (when, what, colour, where the label sits on the chart's scale)
EVENTS = ((1929.8, r"October 1929: \ the crash", PRICE, 11.5), (1933.2, r"March 1933: \ the banks close", PRICE, 2.9),
          (1937.6, r"1937--38: \ a second slump", HOLD, 12.0), (1941.9, r"December 1941: \ war", GOV, 6.5))


class Intermission(SoundScene):
    """American industrial production, month by month, 1919 to 1945, on a log scale, with a year counter and four
    moments marked as they pass; under it, the same series as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        cr = load("cross")
        co = load("coop_path")
        clip = ClipStore("econ27").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["ip"], float)
        ax = plane([1919, 1946], [np.log10(2.5), np.log10(20)], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.2,
                   y_length=5.6, xticks=[1920, 1925, 1930, 1935, 1940, 1945],
                   yticks=[np.log10(x) for x in (3, 5, 10, 20)], ylabel=r"industrial production, \ 2017 $= 100$ \ "
                   r"(log scale)", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{10 ** y:.0f}", font_size=15)
        full = VMobject(stroke_color=OUTPUT, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, np.log10(y)) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
            m.pointwise_become_partial(full, 0, frac)

        year = Integer(1919, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(
            ax.ax.c2p(1923, np.log10(15)))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        marks = VGroup()
        for when, say, c, y in EVENTS:
            marks.add(label(say, font_size=16, color=c).move_to(ax.ax.c2p(when, np.log10(y))))

        def appear(when, ttl=6.0):
            at = film_time(when)

            def f(m, tt):
                m.set_opacity(float(np.clip((tt - at) / 0.6, 0, 1) * np.clip((at + ttl - tt) / 1.0, 0, 1)))
            return f

        for m in marks:
            m.set_opacity(0)
        ends = VGroup(label(rf"1929 peak \ {film['peak29']:.1f}; \ 1932 trough \ {film['trough']:.1f}", font_size=19,
                            color=PRICE),
                      label(rf"wartime peak \ {film['peak_war']:.1f}", font_size=19, color=GOV)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1938, np.log10(3.2)))
        src = data_tag(r"Federal Reserve Board: \ industrial production, \ monthly, \ via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ industrial production \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                         buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"American industrial production, \ 1919--1945; \ the same series as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            for mk, (when, _, _, _) in zip(marks, EVENTS):
                snd.drive(mk, appear(when))
            snd.drive(year, set_year)
            snd.show(ax, grow, year, *marks)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.play(FadeIn(ends), run_time=0.8)
            self.wait(1.2)
            self.play(*[FadeOut(m) for m in (ax, grow, year, marks, ends, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the co-op", rf"too few coupons: \\ {co['before']:.2f} evenings, \ not {co['potential']:.2f}",
                 COUPON),
                (r"the Depression", r"output down a quarter, \\ prices down a quarter", PRICE),
                (r"effective demand", rf"a multiplier of \\ $1/(1-b) = {cr['base']['multiplier']:.1f}$", SPEND),
                (r"thrift", r"saving more \\ can mean saving less", SAVE),
                (r"IS--LM", r"goods and money \\ settle together", RATE),
                (r"the trap", r"at zero, \ money does little; \\ spending does a lot", GOV),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
