from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ46.common import *  # noqa: F403


class Intermission(SoundScene):
    """The share of the world's people below $3.00 a day, year by year since 1981, drawn as the years pass; under
    it, the share as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        N = load("nets")
        A = load("aid")
        T = load("trap")
        G = load("agrigap")
        C = load("credit")
        M = load("cash")
        clip = ClipStore("econ46").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        events = ((1981.0, rf"1981: \ {film['first']:.0f}\%", UP),
                  (1999.0, r"1999: \ 37\%", UP),
                  (2010.0, r"2010: \ 21\%", UP),
                  (2020.0, r"2020: \ the pandemic, \\ the first rise in \\ over twenty years", UP),
                  (float(t[-1]), rf"{int(t[-1])}: \ {film['last']:.0f}\%", DOWN))
        ax = plane([1979, 2026], [0, 50], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 10, 20, 30, 40, 50],
                   ylabel=r"percent of the world below \$3.00 a day", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        year = Integer(1981, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2012, 42))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=POOR, stroke_width=3.4)
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
        for x, n, d in events:
            y = float(np.interp(x, t, v))
            m = label(n, font_size=16, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.2)
            m.ft = film_time(x)
            marks.add(m)
        src = data_tag(r"World Bank, \ World Development Indicators: \ SI.POV.DDAY \ (2021 PPP)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the share in poverty \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                         buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the share of the world below \$3.00 a day, \ 1981--2024; \ the value as a tune")
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
                (r"the nets", rf"demand down {100 * N['drop']:.0f}\% \\ at 60 cents; \\ use unchanged", HEALTH),
                (r"the count", rf"{film['first']:.0f}\% to {film['last']:.0f}\% \\ below \$3.00 a day", POOR),
                (r"the budget", rf"all on nets: {A['all_first']:.1f}; \\ best split: {A['best']:.1f}", GAIN),
                (r"the trap", rf"a threshold at {T['threshold']:.0f}; \\ a transfer of 10 lifts \\ "
                              rf"{100 * T['runs']['10']['share_above_end']:.0f}\%", TRAP),
                (r"farm and town", rf"output per worker \\ {G['median_poorest']:.1f}$\times$ higher \\ off the farm",
                 FARM),
                (r"credit and cash", rf"credit: \ +{C['itt']:.0f} on {C['mean_control']:.0f}; \\ cash: \ a "
                                     rf"multiplier \\ of {M['multiplier']:.1f}", CASH),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
