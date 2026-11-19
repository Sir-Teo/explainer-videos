from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ17.common import *  # noqa: F403

OTHERS = (("Japan", "#F2788F"), ("Italy", "#7BD88F"), ("Sweden", "#F2C14E"))
US_C = "#9FB8F2"


class Intermission(SoundScene):
    """The oldest matching market: marriages a year per 1,000 people in the United States, 1886-2022 (with Japan,
    Italy and Sweden from 1960), drawn without narration as a year counter runs; under it, the US rate as a tune; then
    the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ17").load("intermission.melody")
        years = np.array(film["years"], float)
        us = np.array(film["us"], float)
        t_of = np.array(film["times"])
        n = len(years)
        ax = plane([1884, 2024], [0, 18], center=UP * 0.1 + LEFT * 0.3, x_length=11.4, y_length=5.4,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2020], yticks=[0, 4, 8, 12, 16],
                   ylabel=r"marriages a year per 1,000 people", font_size=16,
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        full = {"United States": VMobject(stroke_color=US_C, stroke_width=4).set_points_as_corners(
            [ax.ax.c2p(x, v) for x, v in zip(years, us)])}
        for e, c in OTHERS:
            ys, vs = film[e]["year"], film[e]["value"]
            full[e] = VMobject(stroke_color=c, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(ys, vs)])
        grown = {k: m.copy() for k, m in full.items()}
        starts = {"United States": years[0], **{e: film[e]["year"][0] for e, _ in OTHERS}}
        ends = {"United States": years[-1], **{e: film[e]["year"][-1] for e, _ in OTHERS}}

        def grower(key):
            def grow(m, t):
                yr = float(np.interp(t, t_of, years))
                a, b = starts[key], ends[key]
                frac = (yr - a) / max(b - a, 1)
                m.pointwise_become_partial(full[key], 0, float(np.clip(frac, 1e-3, 1)))
                m.set_stroke(opacity=1.0 if yr >= a else 0.0)
            return grow

        year = Integer(int(years[0]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(years[k]))

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4), label(t_, font_size=17,
                                                                                         color=GREY_A)).arrange(
            RIGHT, buff=0.1) for t_, c in (("United States", US_C), *OTHERS)]).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.1)
        legend.move_to(ax.ax.c2p(2004, 15.5))
        intro = label(r"the oldest market with no prices", font_size=22, color=WHITE).move_to(ax.ax.c2p(1925, 16.5))

        def window(a_, b_):
            def f(m, t):
                m.set_opacity(float(np.clip((t - a_) / 1.0, 0, 1) * np.clip((b_ - t) / 1.0, 0, 1)))
            return f

        idx = {int(y): k for k, y in enumerate(film["years"])}
        notes_ = [
            (label(rf"1932: \ {film['y1932']:.1f}, \ the Depression", font_size=17, color=US_C).move_to(
                ax.ax.c2p(1925, 4.6)), t_of[idx[1932]] - 0.5, t_of[idx[1932]] + 6.0),
            (label(rf"{film['peak_year']}: \ {film['peak']:.1f}, \ the soldiers come home", font_size=17,
                   color=US_C).move_to(ax.ax.c2p(1968, 17.2)), t_of[idx[1946]] - 0.5, t_of[idx[1946]] + 7.0),
            (label(r"1989: \ Swedes marry before a widow's pension ends", font_size=17,
                   color="#F2C14E").move_to(ax.ax.c2p(1960, 14.2)), t_of[idx[1989]] - 0.5, t_of[idx[1989]] + 6.0),
            (label(rf"{film['low_year']}: \ {film['low']:.1f}, \ the pandemic", font_size=17, color=US_C).move_to(
                ax.ax.c2p(1996, 2.0)), t_of[idx[2020]] - 0.5, t_of[idx[2020]] + 6.0),
        ]
        src = data_tag(r"OECD, \ US Census Bureau and CDC, \ via Our World in Data", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the US rate, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"marriages per 1,000 people, \ 1886--2022: \ the oldest matching market, \ as a tune")
            snd.show(src, stag)
            for k, m in grown.items():
                snd.drive(m, grower(k))
            snd.drive(year, set_year)
            snd.drive(intro, window(0.0, 9.0))
            for m, a_, b_ in notes_:
                snd.drive(m, window(a_, b_))
            t_end = float(t_of[-1]) + 0.3
            fill, up_ = area_sweep(ax, years, us, US_C, t_end, seconds=5.2, opacity=0.12)
            snd.drive(fill, up_)
            snd.show(fill, ax, *grown.values(), year, legend, intro, *[m for m, _, _ in notes_])
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (fill, ax, *grown.values(), year, legend, intro, src, stag,
                                             *[m for m, _, _ in notes_])], run_time=1.0)
            story = point_cards([
                (r"Play it", r"the Boston rule punished \\ the truth; \ DA did not", YOU),
                (r"mechanisms", r"look only at rules \\ where truth is safe", MECH),
                (r"Clarke's rule", r"pay for the harm you do; \\ the budget won't balance", MONEY),
                (r"no perfect bargain", r"private values waste \\ some good trades", HELD),
                (r"Gale and Shapley", r"a stable matching \\ always exists", STABLE),
                (r"who asks", r"the asking side gets \\ its best stable match", PROPOSE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
