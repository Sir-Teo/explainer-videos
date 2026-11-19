from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ14.common import *  # noqa: F403


class Intermission(SoundScene):
    """China and India: GDP per head in 2011 dollars, adjusted for prices (the Maddison Project), year by year from 1950
    to 2022 on a log scale, drawn without narration as a year counter runs; under them, China's line as a tune; then
    the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ14").load("intermission.melody")
        years = np.array(film["years"], float)
        t_of = np.array(film["times"])
        n = len(years)
        lo, hi = np.log10(500), np.log10(30000)
        ticks = (500, 1000, 2000, 5000, 10000, 20000)
        ax = plane([1948, 2024], [lo, hi], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1950, 1970, 1990, 2010], yticks=[np.log10(v) for v in ticks],
                   ylabel=r"GDP per head, \ 2011 dollars adjusted for prices, \ log scale", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{10 ** v:,.0f}")
        series = {"china": (np.log10(np.array(film["china"])), CHINA),
                  "india": (np.log10(np.array(film["india"])), INDIA)}
        full = {k: VMobject(stroke_color=col, stroke_width=3.5).set_points_as_corners(
            [ax.ax.c2p(x, v) for x, v in zip(years, ys)]) for k, (ys, col) in series.items()}
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
            RIGHT, buff=0.1) for t_, c in ((r"China", CHINA), (r"India", INDIA))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(2012, np.log10(800)))
        intro = label(r"two poor countries in 1950, \ of about the same income", font_size=22,
                      color=WHITE).move_to(ax.ax.c2p(1975, np.log10(16000)))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        k78, k91 = list(film["years"]).index(1978), list(film["years"]).index(1991)
        notes_ = [
            (label(r"1978: \ Xiaogang's contract; \\ the countryside reforms first", font_size=18, color=CHINA
                   ).move_to(ax.ax.c2p(1970, np.log10(4200))), t_of[k78] - 0.5, t_of[k78] + 7.0),
            (label(r"1991: \ India's reforms", font_size=18, color=INDIA).move_to(ax.ax.c2p(2000, np.log10(1250))),
             t_of[k91] - 0.5, t_of[k91] + 7.0),
        ]
        src = data_tag(r"the Maddison Project Database 2023 (Bolt and van Zanden)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: China's line, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"China and India, \ 1950--2022: \ GDP per head, \ with China's line as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            snd.drive(intro, window(0.0, 10.0))
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            t_end = float(t_of[-1]) + 0.3
            fills = []
            for k, (ys_, col_) in series.items():
                m_, up_ = area_sweep(ax, years, ys_, col_, t_end, seconds=5.2, opacity=0.14, base=lo)
                snd.drive(m_, up_)
                fills.append(m_)
            snd.show(*fills, ax, *grown.values(), year, legend, intro, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (*fills, ax, *grown.values(), year, legend, intro, src, stag,
                                             *[m for m, _, _ in notes_])], run_time=1.0)
            story = point_cards([
                (r"Play it", r"two-thirds of the harvest: \\ the best share", PAY),
                (r"teams", r"eighteen households, \\ an eighteenth of the effort", TEAM),
                (r"the agency problem", r"pay as an inference \\ about effort", SIGNAL),
                (r"Holmström--Milgrom", r"$\beta^* = 1/(1 + r c \sigma^2)$", E.ACCENT),
                (r"informativeness", r"filter out the weather, \\ and the oil price", NEIGHBOUR_),
                (r"Safelite", r"44\% more: \\ half effort, \ half sorting", EFFORT),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


NEIGHBOUR_ = "#9FB8F2"
