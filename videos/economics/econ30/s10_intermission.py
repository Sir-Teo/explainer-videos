from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ30.common import *  # noqa: F403


class Intermission(SoundScene):
    """The Atlanta Fed's flexible- and sticky-price inflation (core), month by month, 1968 to 2026, drawn as they
    pass, with a year counter; under it, the flexible series as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        C = load("calvo")
        T = load("taylor")
        M = load("menu")
        clip = ClipStore("econ30").load("intermission.melody")
        t = np.array(film["t"], float)
        fl = np.clip(np.array(film["flex"], float), -4, 20)
        st = np.clip(np.array(film["sticky"], float), -4, 20)
        ax = plane([1967, 2027.5], [-4, 20], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 5, 10, 15, 20],
                   ylabel=r"inflation over 12 months, \ \% \ (food and energy aside)", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        zero = seg(ax, 1967, 0, 2027.5, 0, GREY_D, 1.5)
        full_f = VMobject(stroke_color=FLEX, stroke_width=2.2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, fl)])
        full_s = VMobject(stroke_color=STICKY, stroke_width=3.2).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, st)])
        grow_f, grow_s = full_f.copy(), full_s.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(full):
            def f(m, tt):
                frac = float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1))
                m.pointwise_become_partial(full, 0, frac)
            return f

        year = Integer(1968, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1990, 17))

        def set_year(m, tt):
            yr = t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0])
            m.set_value(int(np.clip(yr, t[0], t[-1])))

        key = VGroup(label(r"flexible prices", font_size=19, color=FLEX),
                     label(r"sticky prices", font_size=19, color=STICKY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.1)
        key.move_to(ax.ax.c2p(2014, 17))
        src = data_tag(r"Federal Reserve Bank of Atlanta: \ sticky- and flexible-price CPIs less food and energy, \ "
                       r"via FRED", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ flexible-price inflation \ (computed)", font_size=13, color=E.ACCENT).to_corner(
            UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"sticky and flexible prices, \ 1968--2026; \ the flexible series as a tune")
            snd.show(src, stag)
            snd.drive(grow_f, grower(full_f))
            snd.drive(grow_s, grower(full_s))
            snd.drive(year, set_year)
            snd.show(ax, zero, grow_f, grow_s, year, key)
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(key), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, zero, grow_f, grow_s, year, key, src, stag)], run_time=1.0)
            story = point_cards([
                (r"how long a price lasts", r"4.3 months with sales; \\ 8--11 without", PRICE),
                (r"menu costs", rf"a 1\% error: \ profit {100 * M['rows'][0]['profit_loss']:.2f}\%, \\ "
                                rf"output {100 * M['rows'][0]['output_loss']:.1f}\%", FLEX),
                (r"Calvo", rf"$\pi = \beta \mathbb{{E}}\pi' + \kappa x$, \\ $\kappa = {C['base']['kappa']:.2f}$", INFL),
                (r"the IS curve", r"the real rate \\ against the natural rate", OUTPUT),
                (r"Taylor", rf"{T['fit']['pi']:.2f} on inflation, \\ {T['fit']['gap']:.2f} on the gap", CB),
                (r"solved", r"the Taylor principle: \\ more than one for one", RATE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
