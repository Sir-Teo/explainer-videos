from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ12.common import *  # noqa: F403


class Intermission(SoundScene):
    """Crude and the pump: the price of West Texas Intermediate crude per gallon and the American pump price of
    regular gasoline, month by month, 1986-2026, in October 2026 dollars, drawn without narration as a year counter
    runs; under them, the pump price year by year as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ12").load("intermission.melody")
        months = film["months"]
        t_of = np.array(film["times"])
        n = len(months)
        xs = np.array([int(m[:4]) + (int(m[5:7]) - 1) / 12 for m in months])
        pump, crude = np.array(film["pump"]), np.array(film["crude"])
        ax = plane([1985, 2027], [0, 7], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 1, 2, 3, 4, 5, 6, 7],
                   ylabel=r"\$ a gallon, \ October 2026 dollars", font_size=16, xfmt=lambda v: f"{v:.0f}")
        full = {
            "pump": VMobject(stroke_color=PUMP, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(xs, pump)]),
            "crude": VMobject(stroke_color=CRUDE, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(xs, crude)]),
        }
        grown = {k: m.copy() for k, m in full.items()}
        for k, m in grown.items():
            m.full_ = full[k]

        def grow(m, t):
            k = float(np.interp(t, t_of, np.arange(n)))
            m.pointwise_become_partial(m.full_, 0, max(k / (n - 1), 1e-3))

        year = Integer(int(months[0][:4]), font_size=50, color=E.ACCENT, group_with_commas=False).to_corner(
            UR, buff=0.45).shift(DOWN * 0.35)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, t_of, np.arange(n)))), 0, n - 1))
            m.set_value(int(months[k][:4]))

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4), label(t_, font_size=17,
                                                                                         color=GREY_A)).arrange(
            RIGHT, buff=0.1) for t_, c in ((r"regular gasoline at the pump (BLS)", PUMP),
                                           (r"West Texas crude, \ per gallon (EIA)", CRUDE))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1993, 6.3))
        intro = label(r"a few sellers on every corner: \ the pump and the oil beneath it", font_size=22,
                      color=WHITE).move_to(ax.ax.c2p(2010, 6.7))

        def show_intro(m, t):
            m.set_opacity(float(np.clip(t / 1.5, 0, 1) * np.clip((10.0 - t) / 1.5, 0, 1)))

        src = data_tag(r"BLS (APU000074714) and EIA (MCOILWTICO) via FRED, \ deflated by the CPI-U", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the pump price, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"crude and the pump, \ 1986--2026: \ under the pump price as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            snd.drive(intro, show_intro)
            t_end = float(t_of[-1]) + 0.3
            fills = []
            for ys_, col_ in ((pump, PUMP), (crude, CRUDE)):
                m_, up_ = area_sweep(ax, xs, ys_, col_, t_end, seconds=5.2, opacity=0.16)
                snd.drive(m_, up_)
                fills.append(m_)
            snd.show(*fills, ax, *grown.values(), year, legend, intro)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (*fills, ax, *grown.values(), year, legend, intro, src, stag)],
                      run_time=1.0)
            story = point_cards([
                (r"lysine", r"a price war, \ a cartel, \\ and the tapes", CARTEL),
                (r"Cournot", r"quantities: \ \$40 with two, \\ toward cost with many", LEADER),
                (r"Bertrand", r"prices: \ two firms \\ are enough", CRUSOE),
                (r"the escapes", r"capacity, \ difference, \\ repetition", COMPETE),
                (r"Hotelling", r"together for customers, \\ apart for prices", PUMP),
                (r"variety", r"many firms, \ each a little \\ monopoly", ENTRANT),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
