from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ18.common import *  # noqa: F403

LINES = (("World", "#F2C14E", 5.0), ("United States", "#9FB8F2", 3.0), ("United Kingdom", "#F2788F", 3.0),
         ("France", "#7BD88F", 3.0), ("India", "#C9A0FF", 3.0))


class Intermission(SoundScene):
    """Two centuries of democracy: V-Dem's electoral democracy index, 1789-2025, for the world and four countries,
    drawn without narration as a year counter runs; under it, the world's index as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ18").load("intermission.melody")
        years = np.array(film["years"], float)
        t_of = np.array(film["times"])
        n = len(years)
        ax = plane([1785, 2030], [0, 1], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1800, 1850, 1900, 1950, 2000], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   ylabel=r"electoral democracy index, \ 0 to 1 \ (V-Dem)", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}")
        full = {k: VMobject(stroke_color=c, stroke_width=w).set_points_as_corners(
            [ax.ax.c2p(x, v) for x, v in zip(years, film[k])]) for k, c, w in LINES}
        grown = {k: m.copy() for k, m in full.items()}

        def grower(key):
            def grow(m, t):
                k = float(np.interp(t, t_of, np.arange(n)))
                m.pointwise_become_partial(full[key], 0, max(k / (n - 1), 1e-3))
            return grow

        year = Integer(int(years[0]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(years[k]))

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=w), label(t_, font_size=17,
                                                                                         color=GREY_A)).arrange(
            RIGHT, buff=0.1) for t_, c, w in LINES]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.move_to(ax.ax.c2p(1830, 0.82))
        intro = label(r"free elections, \ the vote for all, \ free speech: \ measured", font_size=22,
                      color=WHITE).move_to(ax.ax.c2p(1900, 0.95))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        idx = {int(y): k for k, y in enumerate(film["years"])}
        notes_ = [
            (label(r"1848: \ revolutions across Europe", font_size=17, color="#7BD88F").move_to(ax.ax.c2p(1848, 0.55)),
             t_of[idx[1848]] - 0.5, t_of[idx[1848]] + 5.0),
            (label(r"1918--28: \ women vote in Britain", font_size=17, color="#F2788F").move_to(ax.ax.c2p(1905, 0.86)),
             t_of[idx[1918]] - 0.5, t_of[idx[1928]] + 4.0),
            (label(r"1940--44: \ France occupied", font_size=17, color="#7BD88F").move_to(ax.ax.c2p(1925, 0.12)),
             t_of[idx[1940]] - 0.5, t_of[idx[1944]] + 4.0),
            (label(r"1950: \ India's republic; \ 1975--77: \ the Emergency", font_size=17,
                   color="#C9A0FF").move_to(ax.ax.c2p(1945, 0.95)), t_of[idx[1950]] - 0.5, t_of[idx[1977]] + 4.0),
            (label(r"1965: \ the US Voting Rights Act", font_size=17, color="#9FB8F2").move_to(ax.ax.c2p(1990, 0.97)),
             t_of[idx[1965]] - 0.5, t_of[idx[1965]] + 5.0),
            (label(rf"{film['world_peak_year']}: \ the world's peak", font_size=17, color="#F2C14E").move_to(
                ax.ax.c2p(1995, 0.3)), t_of[idx[film['world_peak_year']]] - 0.5,
             t_of[idx[film['world_peak_year']]] + 6.0),
        ]
        src = data_tag(r"V-Dem v16 (2026), \ via Our World in Data", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the world's index, \ every other year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"two centuries of democracy, \ 1789--2025: \ the world and four countries, \ the world as a "
                        r"tune")
            snd.show(src, stag)
            for k, _, _ in LINES:
                snd.drive(grown[k], grower(k))
            snd.drive(year, set_year)
            snd.drive(intro, window(0.0, 9.0))
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            t_end = float(t_of[-1]) + 0.3
            fill, up_ = area_sweep(ax, years, np.array(film["World"]), "#F2C14E", t_end, seconds=5.2, opacity=0.12)
            snd.drive(fill, up_)
            snd.show(fill, ax, *grown.values(), year, legend, intro, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (fill, ax, *grown.values(), year, legend, intro, src, stag,
                                             *[m for m, _, _ in notes_])], run_time=1.0)
            story = point_cards([
                (r"Play it", r"five rules, \\ five winners", VOTE["A"]),
                (r"Condorcet", r"majorities can \\ go in circles", CYCLE),
                (r"the agenda", r"whoever sets the order \\ picks the winner", VOTE["B"]),
                (r"Arrow", r"no rule meets four \\ modest conditions", RULE),
                (r"single peaks", r"the median voter \\ wins; \ May's majority", WELF),
                (r"strategy", r"every rule can be gamed; \\ Duverger's two parties", VOTE["D"]),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
