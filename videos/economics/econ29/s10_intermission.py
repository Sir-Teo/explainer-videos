from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ29.common import *  # noqa: F403


class Intermission(SoundScene):
    """The cycle in American real GDP (its gap from a Hodrick-Prescott trend), quarter by quarter, 1947 to 2026, with
    each recession shaded as the line reaches it and a year counter; under it, the same series as a tune; then the
    story so far."""

    def construct(self):
        film = load("film")
        K = load("cake")
        C = load("chains")
        F = load("frisch")
        R = load("rbc")
        lead = -load("play")["series"]["A011RA3Q086SBEA"]["peak_q"]
        clip = ClipStore("econ29").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["cycle"], float)
        ax = plane([1946, 2027.5], [-10, 6], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[-8, -4, 0, 4],
                   ylabel=r"real GDP, \ \% from its trend", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:+.0f}" if y else "0", font_size=15)
        zero = seg(ax, 1946, 0, 2027.5, 0, GREY_D, 1.5)
        full = VMobject(stroke_color=OUTPUT, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, max(y, -10)) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
            m.pointwise_become_partial(full, 0, frac)

        year = Integer(1947, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1956, 4.6))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        bands = shade(ax, film["recessions"], -10, 6)

        def appear(start):
            at = film_time(start)

            def f(m, tt):
                m.set_fill(opacity=float(np.clip((tt - at) / 0.4, 0, 1)) * 0.55)
            return f

        for b in bands:
            b.set_fill(opacity=0)
        n_rec = len(film["recessions"])
        ends = label(rf"{n_rec} recessions; \ the deepest gaps: \ 1982 \ ({min(v[(t > 1981) & (t < 1984)]):.1f}\%) "
                     rf"\ and 2020 \ ({min(v[(t > 2019.9) & (t < 2021)]):.1f}\%)", font_size=19,
                     color=GREY_A).move_to(ax.ax.c2p(1990, -8.6))
        src = data_tag(r"BEA: \ real GDP, \ quarterly; \ NBER recession dates; \ via FRED; \ HP trend", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the cycle in real GDP \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                          buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"America's business cycle, \ 1947--2026; \ the same series as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            for b, (a, _) in zip(bands, film["recessions"]):
                snd.drive(b, appear(a))
            snd.drive(year, set_year)
            snd.show(ax, zero, bands, grow, year)
            self.play(FadeIn(ax), FadeIn(zero), run_time=1.2)
            snd.wait_until("film_end")
            self.play(FadeIn(ends), run_time=0.8)
            self.wait(1.2)
            self.play(*[FadeOut(m) for m in (ax, zero, bands, grow, year, ends, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the cycle", r"a wobble around a trend; \\ the filter decides its size", OUTPUT),
                (r"Play it", rf"housing turns first, \\ about {lead} quarters ahead", HOUSING),
                (r"the cake", rf"eat {100 * (1 - K['beta']):.0f}\% of what is left; \\ found by iteration", POLICY),
                (r"contraction", rf"each step shrinks the error \\ by $\beta$; \ {K['iterations']} steps", VALUE),
                (r"shocks as chains", rf"Rouwenhorst exact; \\ Tauchen stuck at $\rho = {C['rhos'][1]}$", TECH),
                (r"the saddle path", rf"roots {R['moduli'][0]:.2f}, {R['moduli'][1]:.2f}, {R['moduli'][2]:.2f}: "
                                     r"\\ one path in", INVEST),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            del F
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
