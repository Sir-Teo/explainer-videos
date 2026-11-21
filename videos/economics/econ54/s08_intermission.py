from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ54.common import *  # noqa: F403


class Intermission(SoundScene):
    """America's vehicle miles travelled over the past twelve months (the Federal Highway Administration's moving
    total), month by month since 1971; under it, the miles as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        H, C, M, Gm, L = (load(x) for x in ("history", "commuters", "ma1", "gmm", "lifecycle"))
        clip = ClipStore("econ54").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        ax = plane([1970, 2027], [0.8, 3.6], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[1, 1.5, 2, 2.5, 3, 3.5],
                   ylabel=r"vehicle miles in the past twelve months, \ trillions", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.1f}", font_size=15)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2014, 1.3))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow = VMobject(stroke_color=DATA, stroke_width=3.2)
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

        def mark(tm, val, text, dx, dy, color):
            p = ax.ax.c2p(tm, val)
            lab = label(text, font_size=17, color=color)
            lab.next_to(ax.ax.c2p(tm + dx, val + dy), RIGHT if dx >= 0 else LEFT, buff=0)
            edge = lab.get_left() if dx >= 0 else lab.get_right()
            g = VGroup(lab, Line(p, edge + (LEFT if dx >= 0 else RIGHT) * 0.06, color=color, stroke_width=1.2))
            g.ft = film_time(tm)
            return g

        marks = VGroup(
            mark(film["peak_2007_t"], film["peak_2007"], rf"2007: \ {film['peak_2007']:.2f} trillion, \ then "
                 r"a plateau", -9.0, 0.25, GREY_A),
            mark(film["covid_low_t"], film["covid_low"], rf"the pandemic: \ {film['covid_low']:.2f}", -9.0, -0.9,
                 ERR),
        )
        src = data_tag(r"Federal Highway Administration, \ Traffic Volume Trends, \ via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the miles \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"America's vehicle miles travelled over the past twelve months, \ 1971--2026; \ the miles "
                        r"as a tune")
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
                (r"the railway", r"a model of choices: \ 6.3\%; \ BART carried 6.2\%", EST),
                (r"structural", rf"a line through history: \ {100 * H['charge_line']:.0f}\% drive; \ the "
                 rf"logit {100 * H['charge_logit']:.0f}\%".replace("-", "{-}"), MODEL),
                (r"the logit", rf"a minute's worth: \ \${C['vot']:.2f} an hour \ (planted \${C['vot_truth']:.2f})",
                 DATA),
                (r"Play it", r"patience and caution move every fact the same way", CAUTION),
                (r"GMM", rf"Euler conditions, \ no solving; \ a mispriced asset: \ $J = {Gm['bad_J']:.0f}$", THEORY),
                (r"simulation", rf"indirect inference: \ error {M['ii']['rmse']:.2f}, \ against "
                 rf"{M['naive']['rmse']:.2f}", PATIENCE),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        del L
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
