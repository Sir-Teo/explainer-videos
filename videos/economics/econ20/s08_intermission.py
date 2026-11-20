from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ20.common import *  # noqa: F403


class Intermission(SoundScene):
    """The world saves: each country's investment share (five-year average) against its GDP per head relative to the
    United States, 1960-2023 (Penn World Table 11.0), drawn without narration as a year counter runs; eight countries
    named; under it, South Korea's investment share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ20").load("intermission.melody")
        years = np.array(film["years"], float)
        t_of = np.array(film["times"])
        n = len(years)
        ax = plane([0, 0.6], [np.log10(0.008), np.log10(3.0)], center=DOWN * 0.25 + LEFT * 0.4, x_length=10.6,
                   y_length=5.6, xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                   yticks=[np.log10(v) for v in (0.01, 0.03, 0.1, 0.3, 1.0)],
                   xlabel=r"investment, \ share of GDP \ (five-year average)",
                   ylabel=r"GDP per head, \ United States $= 1$ \ (log)", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{10 ** v:g}", font_size=15)
        highlight = film["highlight"]
        dots, tags = {}, {}

        def series(c):
            d = film["countries"][c]
            s = np.array([np.nan if v is None else v for v in d["s"]], float)
            y = np.array([np.nan if v is None else np.log10(v) for v in d["y"]], float)
            return s, y

        data_ = {c: series(c) for c in film["countries"]}
        for c, d in film["countries"].items():
            pops = [p for p in d["pop"] if p]
            r = float(np.clip(0.03 + 0.0045 * np.sqrt(np.median(pops) if pops else 1.0), 0.03, 0.17))
            col = COUNTRY[c][1] if c in highlight else GREY_B
            dots[c] = Dot(ax.ax.c2p(0, 0), radius=r, color=col).set_opacity(0)
            if c in highlight:
                tags[c] = label(COUNTRY[c][0], font_size=15, color=col)

        def pos(c, t):
            s, y = data_[c]
            k = float(np.interp(t, t_of, np.arange(n)))
            i0 = int(np.clip(np.floor(k), 0, n - 1))
            i1 = min(i0 + 1, n - 1)
            f = k - i0
            if not (np.isfinite(s[i0]) and np.isfinite(y[i0])):
                return None
            if np.isfinite(s[i1]) and np.isfinite(y[i1]):
                sv, yv = s[i0] + f * (s[i1] - s[i0]), y[i0] + f * (y[i1] - y[i0])
            else:
                sv, yv = s[i0], y[i0]
            sv = float(np.clip(sv, 0.0, 0.6))
            yv = float(np.clip(yv, np.log10(0.008), np.log10(3.0)))
            return ax.ax.c2p(sv, yv)

        def mover(c):
            hi = c in highlight

            def f(m, t):
                p = pos(c, t)
                if p is None:
                    m.set_opacity(0)
                    return
                m.move_to(p)
                m.set_opacity(0.95 if hi else 0.35)
            return f

        def tagger(c):
            def f(m, t):
                p = pos(c, t)
                if p is None:
                    m.set_opacity(0)
                    return
                m.next_to(p, UR, buff=0.06)
                m.set_opacity(1)
            return f

        year = Integer(int(years[0]), font_size=56, color=E.ACCENT, group_with_commas=False).move_to(
            ax.ax.c2p(0.5, np.log10(0.015)))

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(years[k]))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        notes_ = [
            (label(r"dot size: \ population", font_size=16, color=GREY_B).move_to(ax.ax.c2p(0.08, np.log10(2.2))),
             0.0, 9.0),
            (label(r"South Korea: \ investment climbs past 30\%, \ and income follows", font_size=17,
                   color=COUNTRY["KOR"][1]).move_to(ax.ax.c2p(0.38, np.log10(2.2))), film_time(1975),
             film_time(1990)),
            (label(r"China: \ the highest investment of any large country", font_size=17,
                   color=COUNTRY["CHN"][1]).move_to(ax.ax.c2p(0.38, np.log10(2.2))), film_time(2002),
             film_time(2016)),
            (label(r"investment is not enough: \ Zambia and Mozambique invest over 30\% \ and stay poor",
                   font_size=17,
                   color=WHITE).move_to(ax.ax.c2p(0.36, np.log10(2.2))), film_time(2016) + 0.5, film_time(2023) + 4),
        ]
        src = data_tag(r"Penn World Table 11.0 \ (csh\_i, \ rgdpe, \ pop)", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ South Korea's investment share, \ 1960--2023 \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the world saves: \ investment and income, \ 1960--2023, \ 146 countries; \ South Korea's "
                        r"investment as a tune")
            snd.show(src, stag)
            for c in film["countries"]:
                snd.drive(dots[c], mover(c))
            for c in tags:
                snd.drive(tags[c], tagger(c))
            snd.drive(year, set_year)
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            others = [dots[c] for c in film["countries"] if c not in highlight]
            front = [dots[c] for c in highlight]
            snd.show(ax, *others, *front, *tags.values(), year, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, *dots.values(), *tags.values(), year, src, stag,
                                             *[m for m, _, _ in notes_])], run_time=1.0)
            story = point_cards([
                (r"Kaldor's facts", r"steady growth, \\ steady ratios", OUTPUT),
                (r"Harrod--Domar", r"a knife edge, \\ and a failed promise", SAVE),
                (r"Solow", r"saving sets the level, \\ not the growth rate", CAPITAL),
                (r"the golden rule", r"save capital's share, \\ about a third", CONS),
                (r"the speed", r"5\% in theory, \\ 1--2\% in the data", BREAK),
                (r"convergence", r"conditional, \ yes; \\ absolute, \ no", E.ACCENT),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
