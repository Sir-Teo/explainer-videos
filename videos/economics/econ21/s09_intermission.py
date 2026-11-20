from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ21.common import *  # noqa: F403

COLORS = {"candle": "#FFD580", "lamp": "#E8A0B4", "town gas": "#9FB8F2", "kerosene lamp": "#F29E8E",
          "electric lamp": "#7BD88F"}


class Intermission(SoundScene):
    """Two centuries of light: every lamp Nordhaus priced from 1800 to 1993, appearing as a year counter runs, with
    the cheapest light at each date drawn as a falling line; under it, that line as a falling tune; then the story so
    far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ21").load("intermission.melody")
        ax = plane([1795, 2000], [np.log10(0.00005), np.log10(30)], center=DOWN * 0.2 + LEFT * 0.4, x_length=11.4,
                   y_length=5.6, xticks=[1800, 1850, 1900, 1950, 2000],
                   yticks=[np.log10(v) for v in (0.0001, 0.001, 0.01, 0.1, 1, 10)],
                   ylabel=r"hours of work per 1{,}000 lumen-hours \ (log scale)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{10 ** v:g}", font_size=15)
        pts = film["points"]
        dots = VGroup()
        labs = VGroup()
        for r in pts:
            d = Dot(ax.ax.c2p(r["year"], np.log10(r["hours"])), radius=0.08, color=COLORS[r["device"]])
            d.set_opacity(0)
            dots.add(d)
            t = label(r["tech"].replace("'", "'"), font_size=13, color=COLORS[r["device"]]).next_to(d, UR, buff=0.04)
            t.set_opacity(0)
            labs.add(t)
        fy = np.array(film["frontier_years"], float)
        fv = np.log10(np.array(film["frontier"]))
        full = VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(fy, fv)])
        grown = full.copy()
        t_first, t_last = film_time(fy[0]), film_time(fy[-1])

        def grow(m, t):
            frac = float(np.clip((t - t_first) / (t_last - t_first), 1e-3, 1))
            m.pointwise_become_partial(full, 0, frac)

        def appear(i):
            t0 = film["times"][i]

            def f(m, t):
                m.set_opacity(float(np.clip((t - t0) / 0.6, 0, 1)))
            return f

        def appear_label(i):
            t0 = film["times"][i]

            def f(m, t):
                m.set_opacity(float(np.clip((t - t0) / 0.6, 0, 1) * np.clip((t0 + 6 - t) / 1.0, 0, 1)))
            return f

        year = Integer(1800, font_size=56, color=E.ACCENT, group_with_commas=False).move_to(
            ax.ax.c2p(1975, np.log10(8)))

        def set_year(m, t):
            y = 1800 + (t - film_time(1800)) / (film_time(1993) - film_time(1800)) * 193
            m.set_value(int(np.clip(y, 1800, 1993)))

        leg = VGroup(*[VGroup(Dot(radius=0.07, color=c), label(k, font_size=16, color=c)).arrange(RIGHT, buff=0.08)
                       for k, c in COLORS.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(
            ax.ax.c2p(1830, np.log10(0.0006)))
        src = data_tag(r"Nordhaus (1996), \ table 1.6", corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(
            LEFT, buff=0.3)
        stag = note(r"sound: \ the cheapest light's labour price, \ falling \ (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"two centuries of light: \ hours of work for 1{,}000 lumen-hours, \ 1800--1993; \ the "
                        r"cheapest light as a falling tune")
            snd.show(src, stag)
            snd.drive(grown, grow)
            for i, (d, t_) in enumerate(zip(dots, labs)):
                snd.drive(d, appear(i))
                snd.drive(t_, appear_label(i))
            snd.drive(year, set_year)
            snd.show(ax, grown, *dots, *labs, year, leg)
            self.play(FadeIn(ax), FadeIn(leg), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, grown, *dots, *labs, year, leg, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the price of light", r"45{,}000 times cheaper \\ since 1800", LIGHT),
                (r"non-rival ideas", r"increasing returns; \\ room for monopoly", IDEA),
                (r"AK and spillovers", r"growth without end, \\ on a knife edge", OUTPUT),
                (r"Romer", r"research for profit; \\ too little of it", RESEARCH),
                (r"creative destruction", r"too much or too little, \\ by step size", WEDGE),
                (r"harder to find", r"researchers $\times$23, \\ growth flat", HOLD),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
