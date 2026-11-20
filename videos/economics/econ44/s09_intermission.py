from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ44.common import *  # noqa: F403


class Intermission(SoundScene):
    """The Madison fleet's average mileage since the last engine rebuild, month by month from 1974 to 1985, drawn as
    the months pass, with each month's rebuilds marked; under it, the mileage as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        R = load("rust")
        C = load("ccp")
        Dq = load("duopoly")
        V = load("vertical")
        Pl = load("platform")
        L = load("lockin")
        clip = ClipStore("econ44").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        reb = np.array(film["rebuilds"])
        ax = plane([1974.5, 1985.8], [0, 160], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1975, 1977, 1979, 1981, 1983, 1985], yticks=[0, 40, 80, 120, 160],
                   ylabel=r"average miles since the last rebuild, \ thousands, \ buses in service",
                   xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}", font_size=15)
        year = Integer(1974, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1977, 145))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=BUS, stroke_width=3.2)
        pts = [ax.ax.c2p(x, y) for x, y in zip(t, v)]
        grow.set_points_as_corners([pts[0], pts[0]])

        def grower(m, tt):
            yr = float(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1]))
            k = int(np.searchsorted(t, yr, side="right"))
            ps = pts[:max(k, 1)]
            if k < len(t):
                f = (yr - t[k - 1]) / (t[k] - t[k - 1])
                ps = ps + [pts[k - 1] + f * (pts[k] - pts[k - 1])]
            if len(ps) < 2:
                ps = [ps[0], ps[0]]
            m.set_points_as_corners(ps)

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for x, k in zip(t, reb):
            if k > 0:
                m = Line(ax.ax.c2p(x, 0), ax.ax.c2p(x, 6 * k), color=REBUILD, stroke_width=3)
                m.ft = film_time(x)
                marks.add(m)
        src = data_tag(r"Rust's data: \ 162 buses; \ red ticks: \ rebuilds that month", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the fleet's mileage \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"Madison's buses, \ 1974--1985: \ miles since the last rebuild; \ the value as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            for m in marks:
                snd.drive(m, lambda mm, tt: mm.set_opacity(1.0 if tt >= mm.ft else 0.0))
            snd.show(ax, grow, year, marks)
            self.play(FadeIn(ax), run_time=1.2)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, year, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"Rust's model", rf"rebuild cost {R['nfxp']['RC']:.1f}, \\ upkeep {R['nfxp']['theta1']:.2f}: \\ "
                                  rf"myopia rejected \\ (LR {R['lr']:.1f})", BUS),
                (r"CCP", rf"no fixed point; \\ with 1,000 buses: \\ $RC$ = {C['sims']['1000']['ccp'][0]:.1f}", CCP_C),
                (r"the duopoly", rf"a race: \\ {Dq['lead_changes']} changes of \\ leader", PATIENT),
                (r"two markups", rf"price {V['p_sep']:.0f} instead \\ of {V['p_int']:.0f}", LOSS),
                (r"platforms", rf"the valuable side \\ pays less, \\ even {Pl['p1'][-1]:.2f}", FIRM2),
                (r"lock-in", rf"the worse technology \\ wins {100 * L['at02']:.0f}\% of runs", MYOPIC),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
