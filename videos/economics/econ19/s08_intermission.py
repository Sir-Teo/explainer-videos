from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ19.common import *  # noqa: F403

LINES = ("GBR", "USA", "JPN", "KOR", "CHN", "IND", "NGA")


class Intermission(SoundScene):
    """The great divergence, and the great convergence: GDP per head 1820-2022 for seven countries (Maddison), on a
    log scale, drawn without narration as a year counter runs; under it, the world's GDP per head as a tune; then the
    story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ19").load("intermission.melody")
        years = np.array(film["years"], float)
        t_of = np.array(film["times"])
        n = len(years)
        ax = plane([1815, 2030], [np.log10(500), np.log10(80000)], center=UP * 0.1 + LEFT * 0.5, x_length=11.2,
                   y_length=5.4, xticks=[1850, 1900, 1950, 2000],
                   yticks=[np.log10(v) for v in (1000, 3000, 10000, 30000)],
                   ylabel=r"GDP per head, \ 2011 dollars \ (log scale)", font_size=16, xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"))
        full, grown, ends = {}, {}, {}
        for c in LINES:
            vals = [np.log10(v) if v else np.nan for v in film[c]]
            pts = [ax.ax.c2p(x, v) for x, v in zip(years, vals) if np.isfinite(v)]
            full[c] = VMobject(stroke_color=COUNTRY[c][1], stroke_width=3.5).set_points_as_corners(pts)
            grown[c] = full[c].copy()
            ends[c] = film[c + "_first"]

        def grower(key):
            first = ends[key]

            def grow(m, t):
                k = float(np.interp(t, t_of, np.arange(n)))
                y_now = years[0] + k
                if y_now <= first:
                    m.pointwise_become_partial(full[key], 0, 1e-3)
                    m.set_stroke(opacity=0)
                    return
                frac = (y_now - first) / (years[-1] - first)
                m.pointwise_become_partial(full[key], 0, float(np.clip(frac, 1e-3, 1)))
                m.set_stroke(opacity=1)
            return grow

        year = Integer(int(years[0]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(years[k]))

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=COUNTRY[c][1], stroke_width=3.5),
                                 label(COUNTRY[c][0], font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.1)
                          for c in LINES]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        legend.move_to(ax.ax.c2p(1855, np.log10(30000)))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        idx = {int(y): k for k, y in enumerate(film["years"])}
        notes_ = [
            (label(r"1820: \ the gap between richest and poorest about four to one", font_size=17,
                   color=WHITE).move_to(ax.ax.c2p(1920, np.log10(60000))), 0.0, 8.0),
            (label(r"1868: \ Japan's Meiji restoration", font_size=17, color=JP).move_to(
                ax.ax.c2p(1900, np.log10(700))), t_of[idx[1868]] - 0.5, t_of[idx[1868]] + 5.0),
            (label(r"1913: \ Britain and the United States far ahead", font_size=17, color=UK).move_to(
                ax.ax.c2p(1960, np.log10(20000))), t_of[idx[1913]] - 0.5, t_of[idx[1913]] + 5.0),
            (label(r"1953: \ South Korea after the war", font_size=17, color=COUNTRY["KOR"][1]).move_to(
                ax.ax.c2p(1985, np.log10(650))), t_of[idx[1953]] - 0.5, t_of[idx[1953]] + 5.0),
            (label(r"1978: \ China's reforms begin", font_size=17, color=CN).move_to(
                ax.ax.c2p(1990, np.log10(1300))), t_of[idx[1978]] - 0.5, t_of[idx[1978]] + 5.0),
            (label(r"1991: \ India's reforms", font_size=17, color=IN).move_to(ax.ax.c2p(2005, np.log10(900))),
             t_of[idx[1991]] - 0.5, t_of[idx[1991]] + 5.0),
        ]
        src = data_tag(r"Maddison Project Database 2023 \ (Bolt and van Zanden)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the world's GDP per head, \ every other year, \ log scale (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the great divergence, \ and the great convergence: \ GDP per head, \ 1820--2022, \ seven "
                        r"countries; \ the world as a tune")
            snd.show(src, stag)
            for c in LINES:
                snd.drive(grown[c], grower(c))
            snd.drive(year, set_year)
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            snd.show(ax, *grown.values(), year, legend, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, *grown.values(), year, legend, src, stag,
                                             *[m for m, _, _ in notes_])], run_time=1.0)
            story = point_cards([
                (r"Play it", r"the line leaves the floor \\ around 1800", GDP),
                (r"the model", r"technology buys \\ people, \ not income", POP),
                (r"England's curve", r"1\% more people, \\ 0.9\% lower wages", WAGE),
                (r"the Black Death", r"the mechanism, \\ run backwards", DEATH),
                (r"why Britain?", r"prices, \ ideas, \\ institutions", TECH),
                (r"why not China?", r"a late accident, \\ or a long lead?", CN),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
