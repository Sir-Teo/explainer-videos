from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ52.common import *  # noqa: F403


class Intermission(SoundScene):
    """The top 1%'s and the bottom half's shares of US household wealth, quarter by quarter since 1989, drawn as
    the quarters pass; under it, the top share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        A, W, K, P = (load(x) for x in ("aiyagari", "wealth", "ks", "playit"))
        clip = ClipStore("econ52").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["top1"], float)
        b = np.array(film["bottom50"], float)
        ax = plane([1989, 2027], [0, 40], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 10, 20, 30, 40],
                   ylabel=r"share of US household net worth, \ \%", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2000, 37))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        pts_v = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        pts_b = [ax.ax.c2p(x, y) for x, y in zip(t, b)]
        grow_v = VMobject(stroke_color=DIST, stroke_width=3.4)
        grow_b = VMobject(stroke_color=POOR, stroke_width=3.4)
        grow_v.set_points_as_corners([pts_v[0], pts_v[0]])
        grow_b.set_points_as_corners([pts_b[0], pts_b[0]])

        def make(pts):
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
            return grower

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup(
            label(rf"1989: \ {film['first']:.1f}\%", font_size=17, color=DIST).next_to(pts_v[0], UP, buff=0.15),
            label(rf"{film['last_date'][:4]}: \ {film['last']:.1f}\%", font_size=17, color=DIST).next_to(
                pts_v[-1], UL, buff=0.15),
            label(rf"bottom half, \ {film['b_low_t']:.0f}: \ {film['b_low']:.1f}\%", font_size=17,
                  color=POOR).next_to(ax.ax.c2p(film["b_low_t"], film["b_low"]), UP, buff=0.35),
        )
        marks[0].ft, marks[1].ft, marks[2].ft = film_time(t[0]), film_time(t[-1]), film_time(film["b_low_t"])
        key = VGroup(label(r"purple: \ the richest 1\%", font_size=17, color=DIST),
                     label(r"orange: \ the poorer half", font_size=17, color=POOR)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.ax.c2p(2021, 14))
        src = data_tag(r"Federal Reserve, \ Distributional Financial Accounts, \ via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the top 1\%'s share \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the richest 1\%'s and the poorer half's shares of US household wealth, \ quarterly, \ "
                        r"1989--2026; \ the top share as a tune")
            snd.show(src, stag)
            snd.drive(grow_v, make(pts_v))
            snd.drive(grow_b, make(pts_b))
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, grow_v, grow_b, year, marks, key)
            self.play(FadeIn(ax), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow_v, grow_b, year, marks, key, src, stag)], run_time=1.0)
            story = point_cards([
                (r"Gorman", r"one household is exact only if everyone spends an extra dollar alike", REP),
                (r"incomplete markets", r"uninsured risk pushes the interest rate below time preference", MANY),
                (r"Aiyagari", rf"{100 * A['r']:.1f}\% instead of {100 * A['rho_time']:.1f}\%; "
                              rf"{100 * (A['K'] / A['K_rep'] - 1):.0f}\% more capital", SUPPLY),
                (r"rates fall", r"the poorest respond through incomes; \ the richest through the rate", INDIRECT),
                (r"the top", rf"{W['data']['top1']:.0f}\% in the data, \ {W['models'][0]['top1']:.0f}\% in the "
                             r"model, \ unless returns differ", DIST),
                (r"Krusell and Smith", rf"the mean is nearly enough: \ $R^2$ {K['r2'][1]:.5f}", RULE),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        del P
