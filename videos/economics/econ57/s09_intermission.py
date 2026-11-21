from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ57.common import *  # noqa: F403


class Intermission(SoundScene):
    """The professional forecasters' median probability of a fall in real GDP next quarter (the anxious index),
    every survey since 1968, with the NBER's recessions shaded as they arrive; under it, the index as a tune; then
    the story so far."""

    def construct(self):
        film = load("film")
        R, S_, I_, B, P, SC = (load(x) for x in ("revisions", "seasonal", "island", "bridge", "probit", "score"))
        clip = ClipStore("econ57").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["p"], float)
        ax = plane([1967, 2028], [0, 100], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 25, 50, 75, 100],
                   ylabel=r"chance of a fall in real GDP next quarter, \ \%", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        rec = shade(ax, film["recessions"], 0, 100, RECESS, 0.6)
        for r_, (a, _) in zip(rec, film["recessions"]):
            r_.ft = film_time(a)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2021, 80))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow = VMobject(stroke_color=NOW, stroke_width=2.6)
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

        key = VGroup(label(r"pink: \ the professional forecasters' median chance of a fall next quarter",
                           font_size=17, color=NOW),
                     label(r"grey bands: \ recessions \ (NBER)", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.ax.c2p(2004, 93))
        src = data_tag(r"Philadelphia Fed: \ SPF, \ RECESS2; \ NBER via FRED", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the anxious index \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                       buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the professional forecasters' median chance of a fall in output next quarter, \ every "
                        rf"survey, \ {film['first'][:4]}--{film['last'][:4]}, \ with the NBER's recessions; \ the "
                        r"index as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for r_ in rec:
                snd.drive(r_, lambda mm, tt: mm.set_opacity(0.6 if tt >= mm.ft else 0.0))
            snd.show(ax, rec, grow, year, key)
            self.play(FadeIn(ax), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, rec, grow, year, key, src, stag)], run_time=1.0)
            r0 = SC["rows"]
            story = point_cards([
                (r"two scorecards", r"nine alarms for five recessions; \ 5 of 153 recessions foreseen a year "
                 r"ahead", NOW),
                (r"numbers are made", rf"GDP revised by {R['mae']:.1f} points on average; \ 2008Q4 from "
                 rf"${R['path_2008q4'][0]['growth']:.1f}$ to ${R['path_2008q4'][-1]['growth']:.1f}$", FIRST),
                (r"seasons", r"a filter can invent an April; \ left-out extremes fix it", LATEST),
                (r"nowcasts", rf"errors fall from {I_['rmse'][0]:.1f} to {I_['rmse'][-1]:.1f} as the data come; \ "
                 rf"American bridges {B['rmse_ar']:.1f} to {B['rmse_m3']:.1f}", SPF),
                (r"signals", rf"the yield curve's AUC {P['auc']:.2f}; \ 2022--24's alarms, \ no recession", GB),
                (r"scores", rf"{r0[0]['rmse']:.1f} points now, \ {r0[-1]['rmse']:.1f} a year ahead: \ the "
                 r"average's {:.1f}".format(r0[-1]['rmse_mean']), BENCH),
            ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
