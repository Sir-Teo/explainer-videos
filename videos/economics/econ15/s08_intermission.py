from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ15.common import *  # noqa: F403


class Intermission(SoundScene):
    """A century of sulphur: sulphur dioxide emissions from all sectors in the United States, the United Kingdom,
    China and India, million tonnes a year, 1900-2022 (CEDS via Our World in Data), drawn without narration as a year
    counter runs; under them, the US line as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ15").load("intermission.melody")
        years = np.array(film["years"], float)
        t_of = np.array(film["times"])
        n = len(years)
        ax = plane([1898, 2024], [0, 42], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2020], yticks=[0, 10, 20, 30, 40],
                   ylabel=r"sulphur dioxide emitted, \ million tonnes a year", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        names = (("United States", USA_C), ("United Kingdom", UK_C), ("China", CHINA_C), ("India", INDIA_C))
        full = {k: VMobject(stroke_color=c, stroke_width=3.5).set_points_as_corners(
            [ax.ax.c2p(x, v) for x, v in zip(years, film[k])]) for k, c in names}
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
            RIGHT, buff=0.1) for t_, c in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(
            ax.ax.c2p(1915, 33))
        intro = label(r"the gas that makes acid rain, \ from coal and oil", font_size=22,
                      color=WHITE).move_to(ax.ax.c2p(1940, 40))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        idx = {y: k for k, y in enumerate(film["years"])}
        notes_ = [
            (label(r"1970: \ the US Clean Air Act", font_size=17, color=USA_C).move_to(ax.ax.c2p(1950, 36)),
             t_of[idx[1970]] - 0.5, t_of[idx[1970]] + 6.0),
            (label(r"1990: \ the acid-rain market", font_size=17, color=USA_C).move_to(ax.ax.c2p(1995, 31)),
             t_of[idx[1990]] - 0.5, t_of[idx[1990]] + 6.0),
            (label(r"China fits scrubbers \\ to its coal plants", font_size=17, color=CHINA_C).move_to(
                ax.ax.c2p(1986, 38)), t_of[idx[2007]] - 0.5, t_of[idx[2007]] + 7.0),
        ]
        src = data_tag(r"CEDS (Hoesly et al.\ 2024) via Our World in Data", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the US line, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"sulphur dioxide, \ 1900--2022: \ four countries, \ with the US line as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            snd.drive(intro, window(0.0, 10.0))
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            t_end = float(t_of[-1]) + 0.3
            fills = []
            for k, c in names:
                m_, up_ = area_sweep(ax, years, np.array(film[k]), c, t_end, seconds=5.2, opacity=0.1)
                snd.drive(m_, up_)
                fills.append(m_)
            snd.show(*fills, ax, *grown.values(), year, legend, intro, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (*fills, ax, *grown.values(), year, legend, intro, src, stag,
                                             *[m for m, _, _ in notes_])], run_time=1.0)
            story = point_cards([
                (r"Play it", r"keep your shells: \\ best for you, \ worst for all", POT),
                (r"the wedge", r"45 pots, \ not 36: \\ the market can't see Ana's fish", SOCIAL),
                (r"Pigou", r"tax the damage at the margin; \\ the right smoke isn't zero", GOOD),
                (r"Coase", r"bargain, \ if bargaining is cheap; \\ rights matter when it isn't", DEMAND),
                (r"the bees", r"a market for the spillover, \\ running for decades", FISH),
                (r"public goods", r"add the values up; \\ the lighthouse's harbour", PRIVATE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
