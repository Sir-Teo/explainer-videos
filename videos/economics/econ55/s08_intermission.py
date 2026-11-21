from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ55.common import *  # noqa: F403


class Intermission(SoundScene):
    """The 10-year Treasury yield minus the 3-month bill rate, month by month since 1953, with the NBER's recessions
    shaded as they arrive; under it, the slope as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        P, M, L, I = (load(x) for x in ("puzzle", "schemes_mc", "lpvar", "instruments"))
        clip = ClipStore("econ55").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["spread"], float)
        ax = plane([1952, 2028], [-3.5, 5.0], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[-2, 0, 2, 4],
                   ylabel=r"the 10-year yield minus the 3-month bill, \ points", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:+.0f}".replace("-", "{-}") if y else "0", font_size=15)
        zero = DashedLine(ax.ax.c2p(1952, 0), ax.ax.c2p(2028, 0), color=GREY_C, stroke_width=1.2)
        rec = shade(ax, film["recessions"], -3.5, 5.0, RECESS, 0.6)
        for r_, (a, _) in zip(rec, film["recessions"]):
            r_.ft = film_time(a)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1966, 4.2))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow = VMobject(stroke_color=RATE, stroke_width=2.6)
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

        key = VGroup(label(r"pink: \ the slope of the yield curve", font_size=17, color=RATE),
                     label(r"grey bands: \ recessions \ (NBER)", font_size=17, color=GREY_B),
                     label(r"below zero: \ inverted", font_size=17, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.ax.c2p(2001, -2.6))
        src = data_tag(r"FRED: \ GS10, \ TB3MS, \ USREC", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(
            LEFT, buff=0.3)
        stag = note(r"sound: \ the slope \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the 10-year Treasury yield minus the 3-month bill rate, \ month by month, \ "
                        rf"{film['first'][:4]}--{film['last'][:4]}, \ with the NBER's recessions; \ the slope as a "
                        r"tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for r_ in rec:
                snd.drive(r_, lambda mm, tt: mm.set_opacity(0.6 if tt >= mm.ft else 0.0))
            snd.show(ax, zero, rec, grow, year, key)
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, zero, rec, grow, year, key, src, stag)], run_time=1.0)
            mc = M["methods"]
            story = point_cards([
                (r"the puzzle", rf"American prices rise for {P['months_above_zero']} months after a hike; \ commodity "
                 r"prices undo it", INFL),
                (r"a VAR alone", r"six numbers known, \ nine needed: \ three stories fit equally", DATA),
                (r"Play it", r"you knew a tightening by its signs: \ an assumption", MONEY),
                (r"five schemes", rf"timing wrong; \ instrument and variance right \ "
                 rf"({mc['proxy']['pi']['mean'][0]:.2f} against "
                 rf"{M['truth']['monetary']['pi'][0]:.2f})".replace("-", "{-}"), EST),
                (r"projections", rf"unbiased, \ noisier: \ {L['methods']['lp']['sd'][-1]:.2f} against "
                 rf"{L['methods']['var1']['sd'][-1]:.2f}", GAIN),
                (r"instruments", r"narrative and clean surprises cure the puzzle", MODEL),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        del I
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
