from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ16.common import *  # noqa: F403


class Intermission(SoundScene):
    """Ninety years of the Treasury bill: the 3-month bill rate (secondary market, discount basis), annual averages,
    1934-2025 (FRED, TB3MS), drawn without narration as a year counter runs; under it, the same line as a tune; then
    the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ16").load("intermission.melody")
        years = np.array(film["years"], float)
        rate = np.array(film["rate"], float)
        t_of = np.array(film["times"])
        n = len(years)
        ax = plane([1932, 2027], [0, 16], center=UP * 0.1 + LEFT * 0.3, x_length=11.4, y_length=5.4,
                   xticks=[1940, 1960, 1980, 2000, 2020], yticks=[0, 4, 8, 12, 16],
                   ylabel=r"3-month Treasury bill rate, \ percent, \ yearly average", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        full = VMobject(stroke_color=PRICE, stroke_width=4).set_points_as_corners(
            [ax.ax.c2p(x, v) for x, v in zip(years, rate)])
        grown = full.copy()

        def grow(m, t):
            k = float(np.interp(t, t_of, np.arange(n)))
            m.pointwise_become_partial(full, 0, max(k / (n - 1), 1e-3))

        year = Integer(int(years[0]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(years[k]))

        intro = label(r"the yield on the bills the Treasury sells by auction", font_size=22,
                      color=WHITE).move_to(ax.ax.c2p(1965, 14.5))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        idx = {int(y): k for k, y in enumerate(film["years"])}
        notes_ = [
            (label(r"1942--47: \ held at 3/8 of a percent \\ to finance the war", font_size=17, color=PRICE).move_to(
                ax.ax.c2p(1952, 5.5)), t_of[idx[1942]] - 0.5, t_of[idx[1947]] + 4.0),
            (label(rf"{film['peak_month'][:4]}: \ {film['peak_month_rate']:.1f}\% in a single month",
                   font_size=17, color=VALUE).move_to(ax.ax.c2p(1966, 15.3)),
             t_of[idx[film['peak_year']]] - 0.5, t_of[idx[film['peak_year']]] + 6.0),
            (label(r"2009--15: \ close to zero", font_size=17, color=SECOND).move_to(ax.ax.c2p(2014, 9.5)),
             t_of[idx[2009]] - 0.5, t_of[idx[2015]] + 4.0),
            (label(r"2023: \ five percent again", font_size=17, color=FIRST).move_to(ax.ax.c2p(2006, 7.4)),
             t_of[idx[2023]] - 0.5, t_of[idx[2023]] + 6.0),
        ]
        src = data_tag(r"FRED: \ TB3MS (Board of Governors of the Federal Reserve System)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the bill rate, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"ninety years of the Treasury bill, \ 1934--2025, \ with the rate as a tune")
            snd.show(src, stag)
            snd.drive(grown, grow)
            snd.drive(year, set_year)
            snd.drive(intro, window(0.0, 9.0))
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            t_end = float(t_of[-1]) + 0.3
            fill, up_ = area_sweep(ax, years, rate, PRICE, t_end, seconds=5.2, opacity=0.12)
            snd.drive(fill, up_)
            snd.show(fill, ax, grown, year, intro, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (fill, ax, grown, year, intro, src, stag, *[m for m, _, _ in notes_])],
                      run_time=1.0)
            story = point_cards([
                (r"Play it", r"52.5 in sale A, \ 70 in sale B: \\ six shells either way", YOU),
                (r"four formats", r"two games: \ Dutch is sealed; \\ English is Vickrey's, \ nearly", SECOND),
                (r"Vickrey", r"pay the next bid, \\ and truth is dominant", SECOND),
                (r"shading", r"bid $\tfrac{n-1}{n}$ of your value: \\ more rivals, \ less shading", FIRST),
                (r"equivalence", r"who wins fixes \\ what is paid", PRICE),
                (r"failures", r"risk, \ links, \ asymmetry, \\ collusion, \ entry", HOLD),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
