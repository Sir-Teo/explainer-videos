from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ11.common import *  # noqa: F403


class Intermission(SoundScene):
    """Two stockpiles: the estimated nuclear warheads of the United States and of the Soviet Union (Russia from
    1992), year by year, 1945-2026, drawn without narration as a year counter runs, with the arms-control treaties
    marked as they arrive; under them, the two stockpiles' total as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ11").load("intermission.melody")
        years = np.array(film["years"], float)
        t_of = np.array(film["times"])
        n = len(years)
        us, su = np.array(film["us"], float), np.array(film["ussr"], float)
        ax = plane([1944, 2027], [0, 45000], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[0, 10000, 20000, 30000, 40000], ylabel=r"warheads",
                   font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v / 1000:.0f}k" if v else "0")
        full = {
            "us": VMobject(stroke_color=US, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(years, us)]),
            "su": VMobject(stroke_color=USSR, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(years, su)]),
        }
        grown = {k: m.copy() for k, m in full.items()}
        for k, m in grown.items():
            m.full_ = full[k]

        def grow(m, t):
            k = float(np.interp(t, t_of, np.arange(n)))
            m.pointwise_become_partial(m.full_, 0, max(k / (n - 1), 1e-3))

        year = Integer(int(years[0]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(years[k]))

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4), label(t_, font_size=17,
                                                                                         color=GREY_A)).arrange(
            RIGHT, buff=0.1) for t_, c in ((r"United States", US), (r"Soviet Union, \ then Russia", USSR))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1958, 41000))
        intro = label(r"two stockpiles: \ a repeated game, \ played for eighty years", font_size=22, color=WHITE
                      ).move_to(ax.ax.c2p(1995, 43500))

        def show_intro(m, t):
            m.set_opacity(float(np.clip(t / 1.5, 0, 1) * np.clip((10.0 - t) / 1.5, 0, 1)))

        marks = VGroup()
        for tr in film["treaties"]:
            x = tr["year"]
            yv = max(us[years == x][0], su[years == x][0])
            tick = DashedLine(ax.ax.c2p(x, 0), ax.ax.c2p(x, min(yv + 6000, 44000)), color=GREY_B, stroke_width=1.5)
            txt = label(rf"{x}: \ {tr['name']}", font_size=15, color=GREY_A).rotate(PI / 2).next_to(
                tick, RIGHT, buff=0.04).align_to(tick, UP)
            g = VGroup(tick, txt)
            g.t0 = tr["t"]
            marks.add(g)

        def show_mark(m, t):
            m.set_opacity(float(np.clip((t - m.t0) / 0.8, 0, 1)))

        src = data_tag(r"Federation of American Scientists, \ via Our World in Data (2026)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the two stockpiles together, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"two nuclear stockpiles, \ 1945--2026, \ their total as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            snd.drive(intro, show_intro)
            for m in marks:
                m.set_opacity(0)
                snd.drive(m, show_mark)
            t_end = float(t_of[-1]) + 0.3
            fills = []
            for ys_, col_ in ((us, US), (su, USSR)):
                m_, up_ = area_sweep(ax, years, ys_, col_, t_end, seconds=5.2)
                snd.drive(m_, up_)
                fills.append(m_)
            snd.show(*fills, ax, *grown.values(), year, legend, intro, *marks)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (*fills, ax, *grown.values(), year, legend, intro, src, stag, *marks)],
                      run_time=1.0)
            story = point_cards([
                (r"the guessing game", r"two-thirds of the average: \\ 0 in theory, \ 13 to 25 in practice", ANA),
                (r"dominance", r"rule out what a rational \\ player never does, \ repeatedly", LEVEL),
                (r"Nash equilibrium", r"nobody gains by \\ changing alone", EQ),
                (r"four games", r"coordination, \ battle, \\ chicken, \ stag hunt", COOP),
                (r"mixing", r"penalty kicks: \ equal \\ success either side", BO),
                (r"time", r"backward induction; \\ empty threats ruled out", DEFECT),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
