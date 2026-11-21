from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ64.common import *  # noqa: F403


class Intermission(SoundScene):
    """The number of transistors on the largest microprocessor of each year, 1971-2021 (log scale), drawn year by
    year; under it, the count as a rising tune; then the story so far."""

    def construct(self):
        film = load("film")
        Cc, K, T, D, X = (load(x) for x in ("courts", "contraction", "targeting", "dml", "text"))
        clip = ClipStore("econ64").load("intermission.melody")
        lv = np.array(film["log10"], float)
        ax = plane([1969, 2023], [3, 11], center=DOWN * 0.25 + LEFT * 0.3, x_length=11.6, y_length=5.2,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[3, 5, 7, 9, 11],
                   ylabel=r"transistors on the largest microprocessor \ (log scale)", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"10^{{{y:.0f}}}", font_size=15)
        yrs, ts = np.array(film["years"], float), np.array(film["t"], float)
        pts = [ax.ax.c2p(x, y) for x, y in zip(yrs, lv)]
        dots_ = VGroup(*[Dot(p_, radius=0.05, color=PROD) for p_ in pts])
        for d_, t_ in zip(dots_, ts):
            d_.ft = t_
            d_.set_opacity(0.0)

        def grower(m, tt):
            k = int(np.searchsorted(ts, tt, side="right"))
            ps = pts[:max(k, 1)]
            if len(ps) < 2:
                ps = [pts[0], pts[0]]
            m.set_points_as_corners(ps)

        line = VMobject(stroke_color=PROD, stroke_width=3.0)
        line.set_points_as_corners([pts[0], pts[0]])
        trend = Line(ax.ax.c2p(1971, lv[0]), ax.ax.c2p(2021, lv[0] + 50 / film["doubling"] * np.log10(2)),
                     color=GREY_C, stroke_width=1.6)
        trend = DashedVMobject(trend, num_dashes=40)
        trend.ft = film_time(2021)
        trend.set_opacity(0.0)
        tl = label(rf"doubling every {film['doubling']:.1f} years", font_size=18, color=GREY_B).next_to(
            ax.ax.c2p(1990, lv[0] + 19 / film["doubling"] * np.log10(2)), UP + LEFT, buff=0.1)
        tl.ft = film_time(2021)
        tl.set_opacity(0.0)
        yr = Integer(1971, font_size=48, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2012, 4.2))

        def set_year(m, tt):
            a, b = FILM_YEARS
            m.set_value(int(np.clip(a + (tt - 2.0) / (FILM_SECONDS - 4.0) * (b - a), 1971, 2021)))

        src = data_tag(r"Rupp, \ Microprocessor Trend Data, \ via Our World in Data", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ each chip's count, \ 1971--2021 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"transistors on the largest microprocessor of each year since 1971, \ on a log scale; \ "
                        r"the count as a rising tune")
            snd.show(src, stag)
            snd.drive(line, grower)
            snd.drive(yr, set_year)
            for m in [*dots_, trend, tl]:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, line, dots_, trend, tl, yr)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            for m in [*dots_, trend, tl, line, yr]:
                m.clear_updaters()
            self.play(*[FadeOut(m) for m in (ax, line, dots_, trend, tl, yr, src, stag)], run_time=1.0)
            P = T["per100"]
            story = point_cards([
                (r"prediction policy", r"bail is an umbrella problem; \ Meehl's formula usually wins", ALGO),
                (r"Play it", r"the algorithm detains the young with missed dates; \ the judge, \ the violent "
                 r"charges", JUDGE),
                (r"selective labels", rf"{100 * Cc['crime_cut']:.0f}\% fewer failures at the judges' rate; \ the "
                 r"contraction design checks it", GAIN),
                (r"not causation", rf"by risk {P['highest risk']:.0f}, \ by estimated effect "
                 rf"{P['largest effect (estimated)']:.0f} per 100 places", NAIVE),
                (r"double ML", rf"{D['double ML']['mean']:.2f} against a truth of 1; \ linear controls "
                 rf"{D['linear controls']['mean']:.2f}", CAUSE),
                (r"predicted labels", rf"prediction-powered: \ a third narrower than {X['labelled']} hand labels, "
                 r"\ and unbiased", TEXT),
            ], width=12.6, cols=3, font_size=19).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.wait(6.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
