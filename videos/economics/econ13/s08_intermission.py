from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ13.common import *  # noqa: F403


class Intermission(SoundScene):
    """Used cars and new: the consumer price indexes for used cars and trucks and for new vehicles, each divided by
    the CPI for all items and set to 100 in January 1953, month by month to October 2026, drawn without narration as
    a year counter runs; under them, the used-car line year by year as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ13").load("intermission.melody")
        months = film["months"]
        t_of = np.array(film["times"])
        n = len(months)
        xs = np.array([int(m[:4]) + (int(m[5:7]) - 1) / 12 for m in months])
        pump, crude = np.array(film["used"]), np.array(film["new"])
        ax = plane([1952, 2027], [0, 120], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1960, 1980, 2000, 2020], yticks=[0, 25, 50, 75, 100], ylabel=r"price relative to all "
                   r"consumer prices, \ January 1953 $= 100$", font_size=16, xfmt=lambda v: f"{v:.0f}")
        full = {
            "pump": VMobject(stroke_color=USED, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(xs, pump)]),
            "crude": VMobject(stroke_color=NEW, stroke_width=3).set_points_as_corners(
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
            RIGHT, buff=0.1) for t_, c in ((r"used cars and trucks (BLS)", USED),
                                           (r"new vehicles (BLS)", NEW))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1990, 16))
        intro = label(r"the market Akerlof wrote about: \ used cars and new", font_size=22,
                      color=WHITE).move_to(ax.ax.c2p(2010, 114))

        def show_intro(m, t):
            m.set_opacity(float(np.clip(t / 1.5, 0, 1) * np.clip((10.0 - t) / 1.5, 0, 1)))

        src = data_tag(r"BLS consumer price indexes (CUSR0000SETA02, \ CUSR0000SETA01, \ CPIAUCSL) via FRED", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the used-car line, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"used cars and new, \ 1953--2026, \ against all prices: \ the used line as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            snd.drive(intro, show_intro)
            t_end = float(t_of[-1]) + 0.3
            fills = []
            for ys_, col_ in ((pump, USED), (crude, NEW)):
                m_, up_ = area_sweep(ax, xs, ys_, col_, t_end, seconds=5.2, opacity=0.16)
                snd.drive(m_, up_)
                fills.append(m_)
            snd.show(*fills, ax, *grown.values(), year, legend, intro)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (*fills, ax, *grown.values(), year, legend, intro, src, stag)],
                      run_time=1.0)
            story = point_cards([
                (r"Akerlof", r"bad goods drive out good; \\ markets unravel", LEMON),
                (r"Play it", r"your best blind offer \\ left most boats unsold", GOOD),
                (r"guarantees", r"cheap only \\ for the honest", SIGNAL),
                (r"Spence", r"school that sorts, \\ and teaches nothing", POOL),
                (r"the GED", r"a certificate worth \\ 10 to 19\% to some", USED),
                (r"Rothschild--Stiglitz", r"menus that sort, \\ and may not exist", LOSS),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
