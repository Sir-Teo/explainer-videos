from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ56.common import *  # noqa: F403


class Intermission(SoundScene):
    """The median duration of unemployment in the United States, month by month since 1967, with the NBER's
    recessions shaded as they arrive; under it, the duration as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        M1, M2, M3, M4, A1, A2 = (load(x) for x in ("micro1", "micro2", "micro3", "micro4", "macro1", "macro2"))
        clip = ClipStore("econ56").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["weeks"], float)
        ax = plane([1966, 2028], [0, 28], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15, 20, 25],
                   ylabel=r"median duration of unemployment, \ weeks", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        rec = shade(ax, film["recessions"], 0, 28, RECESS, 0.6)
        for r_, (a, _) in zip(rec, film["recessions"]):
            r_.ft = film_time(a)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1976, 24))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow = VMobject(stroke_color=MACRO, stroke_width=2.6)
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

        key = VGroup(label(r"orange: \ half of the unemployed have been out longer than this", font_size=17,
                           color=MACRO),
                     label(r"grey bands: \ recessions \ (NBER)", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.ax.c2p(2002, 25.5))
        src = data_tag(r"FRED: \ UEMPMED, \ USREC \ (BLS, \ NBER)", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the median duration \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                         buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the median duration of unemployment in the United States, \ month by month, \ "
                        rf"{film['first'][:4]}--{film['last'][:4]}, \ with the NBER's recessions; \ the duration as "
                        r"a tune")
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
            story = point_cards([
                (r"1. \ a kinked budget", rf"demand {M1['x']:.0f} on the second segment; \ the income effect on "
                 rf"$x - \bar x$ only: \ ${M1['total']:.0f}$".replace("-", "{-}"), MICRO),
                (r"2. \ an externality", rf"equilibrium at the endowment; \ efficient $x_A = {M2['xa_po']:.2f}$; \ "
                 rf"Pigou's tax {M2['tax']:.1f}", MICRO),
                (r"3. \ a reserve price", rf"$\beta(v) = (v^2 + r^2)/2v$; \ revenue {M3['rev']:.3f} against "
                 rf"{M3['rev0']:.3f}", MICRO),
                (r"4. \ screening", rf"no distortion at the top; \ $q_L = {M4['q_l']:.1f}$; \ $q(\theta) = 2\theta "
                 r"- 2$", MICRO),
                (r"5. \ a tax on capital", rf"$k^*$ {A1['k_old']:.2f} to {A1['k_new']:.2f}; \ $c$ jumps up, \ then "
                 r"falls below where it began", MACRO),
                (r"6. \ benefits that expire", rf"reservation wage {A2['res'][-1]:.3f} falling to "
                 rf"{A2['res'][0]:.3f} at exhaustion", MACRO),
            ], width=12.6, cols=3, font_size=20).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
