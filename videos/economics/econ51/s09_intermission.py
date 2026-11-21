from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ51.common import *  # noqa: F403


def _num(v):
    if v >= 1e9:
        return f"{v / 1e9:.1f} billion"
    if v >= 1e6:
        return f"{v / 1e6:.1f} million"
    return f"{v:,.0f}".replace(",", "{,}")


class Intermission(SoundScene):
    """Transistors on the largest microprocessor of each year since 1971, on a log scale, drawn as the years pass;
    under it, the series as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        G, Gr, It, Hh = (load(x) for x in ("growth", "grids", "interp", "household"))
        clip = ClipStore("econ51").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["log10"], float)
        marks_at = [(t[0], DR), (1985.0, UL), (2000.0, UL), (2010.0, UL), (t[-1], DOWN)]
        ax = plane([1969, 2023], [3, 11], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[3, 5, 7, 9, 11],
                   ylabel=r"transistors on the largest microprocessor, \ $\log_{10}$", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"10^{{{y:.0f}}}", font_size=15)
        trend = path(ax, [t[0], t[-1]], [v[0], v[0] + (t[-1] - t[0]) * np.log10(2) / 2], GREY_B, 1.4)
        trend = DashedVMobject(trend, num_dashes=40)
        year = Integer(int(t[0]), font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1980, 10))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=VALUE, stroke_width=3.4)
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
        raw = np.array(film["v"], float)
        for x, d in marks_at:
            y = float(np.interp(x, t, v))
            val = float(10 ** y) if x not in t else float(raw[list(t).index(x)])
            m = label(rf"{int(x)}: \ {_num(val)}", font_size=16, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.2)
            m.ft = film_time(x)
            marks.add(m)
        tl = label(r"dashed: \ doubling every two years", font_size=15, color=GREY_B).next_to(
            ax.ax.c2p(2008, v[0] + (2008 - t[0]) * np.log10(2) / 2), DR, buff=0.2)
        tl.ft = film_time(1990)
        src = data_tag(r"Rupp (2022), \ via Our World in Data", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the series \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"transistors on the largest microprocessor of each year, \ 1971--2021, \ log scale; \ the "
                        r"value as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in (*marks, tl):
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, trend, grow, year, marks, tl)
            self.play(FadeIn(ax), FadeIn(trend), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, trend, grow, year, marks, tl, src, stag)], run_time=1.0)
            g30 = Gr["rows"][0]
            story = point_cards([
                (r"a contraction", rf"the change shrinks by $\beta$ each round: \ {G['vfi_iters']} rounds", VALUE),
                (r"policy iteration", rf"{G['howard_iters']} rounds, \ the same answer", HOWARD),
                (r"grids", rf"30 points put the steady state {100 * (1 - g30['steady']):.0f}\% too low", ERR),
                (r"interpolation", rf"a spline: \ one dollar in "
                                   rf"{10 ** (-It['cubic']['ee']['max']) / 1e6:.1f} million", POLICY),
                (r"endogenous grids", rf"no root finding: \ {1000 * Hh['egm_seconds']:.0f} ms", EGM),
                (r"projection", r"each degree about four times more accurate", PROJ),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
