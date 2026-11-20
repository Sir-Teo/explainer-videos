from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ25.common import *  # noqa: F403

EVENTS = ((1971.6, r"1971: \ the gold window closes", MONEY), (1979.8, r"1979: \ Volcker", PRICE),
          (2008.8, r"2008: \ the base jumps", CB), (2020.3, r"2020: \ M2 surges", BANK))


class Intermission(SoundScene):
    """American base money, M2 and consumer prices, each set to one in January 1959, month by month to the latest
    month, on a log scale, with a year counter and four moments marked as they pass; under it, M2 as a rising tune;
    then the story so far."""

    def construct(self):
        film = load("film")
        w = load("world")
        bt = load("barter")
        k10 = bt["n"].index(10)
        clip = ClipStore("econ25").load("intermission.melody")
        t = np.array(film["t"], float)
        ax = plane([1959, 2027], [0, np.log10(150)], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.2, y_length=5.6,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 1, 2],
                   ylabel=r"January 1959 $= 1$ \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:.0f}", font_size=15)

        def full(series, color):
            # a missing month (BLS published no October 2025 CPI) is skipped, not drawn
            return VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, np.log10(v)) for x, v in zip(t, series) if np.isfinite(v) and v > 0])
        fb, fm, fp = full(film["base"], CB), full(film["m2"], BANK), full(film["cpi"], PRICE)
        gb, gm, gp = fb.copy(), fm.copy(), fp.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(f):
            def g(m, tt):
                frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
                m.pointwise_become_partial(f, 0, frac)
            return g

        year = Integer(1959, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1970, 1.9))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        marks = VGroup()
        for when, say, c in EVENTS:
            k = int(np.argmin(np.abs(t - when)))
            marks.add(label(say, font_size=16, color=c).next_to(ax.ax.c2p(when, np.log10(film["m2"][k])), UP + LEFT,
                                                                buff=0.15))

        def appear(when, ttl=6.0):
            at = film_time(when)

            def f(m, tt):
                m.set_opacity(float(np.clip((tt - at) / 0.6, 0, 1) * np.clip((at + ttl - tt) / 1.0, 0, 1)))
            return f

        for m in marks:
            m.set_opacity(0)
        legend = VGroup(label(r"base money", font_size=18, color=CB), label(r"M2", font_size=18, color=BANK),
                        label(r"consumer prices", font_size=18, color=PRICE)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.1)
        legend.move_to(ax.ax.c2p(1966, 1.35))
        ends = VGroup(label(rf"base money: \ $\times${film['base_end']:.0f}", font_size=19, color=CB),
                      label(rf"M2: \ $\times${film['m2_end']:.0f}", font_size=19, color=BANK),
                      label(rf"prices: \ $\times${film['cpi_end']:.0f}", font_size=19, color=PRICE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(2014, 0.35))
        src = data_tag(r"Federal Reserve Board and BLS, \ via FRED", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ M2, \ rising \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"American base money, \ M2 and prices since 1959; \ M2 as a tune")
            snd.show(src, stag)
            for g, f in ((gb, fb), (gm, fm), (gp, fp)):
                snd.drive(g, grower(f))
            for mk, (when, _, _) in zip(marks, EVENTS):
                snd.drive(mk, appear(when))
            snd.drive(year, set_year)
            snd.show(ax, gb, gm, gp, year, legend, *marks)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(FadeIn(ends), run_time=0.8)
            self.wait(1.2)
            self.play(*[FadeOut(m) for m in (ax, gb, gm, gp, year, legend, marks, ends, src, stag)], run_time=1.0)
            story = point_cards([
                (r"barter", rf"a double coincidence: \\ 1 in {1 / bt['barter'][k10]:.0f} with ten goods", COCO),
                (r"Kiyotaki--Wright", r"salt becomes money; \\ smoked fish too", SALT),
                (r"coin to paper", r"from Lydia to \\ 15 August 1971", MONEY),
                (r"the quantity theory", rf"slope {w['slope']:.2f} across \\ {w['n']} countries", MONEY),
                (r"hyperinflation", r"the inflation tax \\ and its Laffer curve", PRICE),
                (r"the ends", r"new fiscal regimes, \\ or someone else's money", CB),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
