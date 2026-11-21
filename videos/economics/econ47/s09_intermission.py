from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ47.common import *  # noqa: F403


class Intermission(SoundScene):
    """The world's electoral democracy index, year by year since 1900, drawn as the years pass; under it, the index
    as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        R = load("roads")
        S = load("sugar")
        K = load("tokens")
        Se = load("senate")
        M = load("mayors")
        Tl = load("tullock")
        clip = ClipStore("econ47").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        events = ((1900.0, rf"1900: \ {film['first']:.2f}", UP),
                  (1945.0, r"1945: \ the end of the war", UP),
                  (1990.0, r"1990: \ after the Cold War", LEFT),
                  (float(film["peak_t"]), rf"{int(film['peak_t'])}: \ the peak, \ {film['peak']:.2f}", UP),
                  (float(t[-1]), rf"{int(t[-1])}: \ {film['last']:.2f}", DOWN))
        ax = plane([1895, 2030], [0, 0.7], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2025], yticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
                   ylabel=r"V-Dem's electoral democracy index, \ the world's average", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.1f}", font_size=15)
        year = Integer(1900, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1935, 0.6))
        t0, t1 = film_time(t[0]), film_time(t[-1])
        grow = VMobject(stroke_color=DEM, stroke_width=3.4)
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
        src = data_tag(r"V-Dem Institute, \ Democracy Report v16 (2026), \ via Our World in Data", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the index \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"the world's electoral democracy index, \ 1900--2025; \ the value as a tune")
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
                (r"the roads", rf"audits: \ {100 * R['audit']:+.0f} points missing; \ meetings: \ about none"
                 .replace("-", "{-}"), AUDIT),
                (r"sugar", rf"twice the world price: \ \${S['per_farm'] / 1000:,.0f},000 a farm \ against "
                           rf"\${S['per_person']:.0f} a head".replace(",", "{,}"), FEW),
                (r"build or lobby", rf"everyone lobbies: \ {K['nash_payoff']:.0f} each; \ everyone builds: \ "
                                    rf"{K['best_payoff']:.0f}", LOBBY),
                (r"rent seeking", rf"ten players spend \ {100 * Tl['dissipated'][8]:.0f}\% of the prize", LOSS),
                (r"close elections", rf"the Senate: \ winning is worth \ {Se['jump']:.1f} points next time",
                 VOTER),
                (r"lame ducks", rf"take more: \ first-term mayors \ {100 * M['fewer']:.0f}\% less", POL),
            ], width=12.6, cols=3, font_size=21).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
