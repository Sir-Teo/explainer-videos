from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ38.common import *  # noqa: F403


class Intermission(SoundScene):
    """America's federal minimum wage in 2025 dollars, year by year since 1938, drawn as the years pass, with its
    milestones marked; under it, the real minimum as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        C = load("ck")
        S = load("supply")
        M = load("market")
        P = load("monopsony")
        B = load("border")
        clip = ClipStore("econ38").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["v"], float)
        nom = dict(zip(film["t"], film["nominal"]))
        real = dict(zip(film["t"], film["v"]))
        events = ((1938.0, rf"1938: \ \$0.25 \ (\${real[1938]:.2f} today)", UP),
                  (float(film["peak_y"]), rf"{film['peak_y']}: \ \${nom[film['peak_y']]:.2f}, \ the peak \ "
                                          rf"(\${real[film['peak_y']]:.2f})", UP),
                  (1992.0, r"1992: \ New Jersey's year", DOWN),
                  (2009.0, r"2009: \ \$7.25", UP),
                  (2025.0, r"2025: \ still \$7.25", RIGHT))
        ax = plane([1936, 2030], [0, 16], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1940, 1960, 1980, 2000, 2020], yticks=[0, 4, 8, 12, 16],
                   ylabel=r"the federal minimum wage, \ 2025 dollars an hour", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        full = VMobject(stroke_color=WAGE, stroke_width=3.4).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            m.pointwise_become_partial(full, 0, float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1)))

        year = Integer(1938, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(2008, 3))

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup()
        for x, n, d in events:
            y = float(np.interp(x, t, v))
            if x == 1938.0:          # below the start, reading rightward, clear of the 1940s
                m = label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, y), DOWN, buff=0.55,
                                                                 aligned_edge=LEFT)
            else:
                m = label(n, font_size=15, color=GREY_A).next_to(ax.ax.c2p(x, y), d, buff=0.6 if d is DOWN else 0.15)
            m.ft = film_time(x)
            marks.add(m)
        src = data_tag(r"Department of Labor and BLS, \ via FRED: \ FEDMINNFRWG, \ CPIAUCNS", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the real minimum wage \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR,
                                                                                                         buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"America's minimum wage, \ 1938--2025, \ in today's dollars; \ the value as a tune")
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
                (r"New Jersey", rf"employment +{C['did']:.2f} \\ per restaurant, \ relative", NJ),
                (r"labour supply", rf"bends back \\ above \${S['peak']:.0f} an hour", SUPPLY),
                (r"the textbook", rf"a floor 19\% higher: \\ {100 * M['drop19']:.0f}\% employment", DEMAND),
                (r"monopsony", rf"a minimum up to \${P['w_c']:.2f} \\ raises employment", MCL),
                (r"the Island's test", rf"competition {B['competitive']['mean_did']:+.2f}, \\ monopsony "
                                       rf"{B['monopsony']['mean_did']:+.2f}", E.ACCENT),
                (r"the minimum", rf"\${film['peak']:.2f} in {film['peak_y']}, \\ \$7.25 now \ (2025 \$)", WAGE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
