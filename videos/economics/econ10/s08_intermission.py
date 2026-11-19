from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ10.common import *  # noqa: F403


class Intermission(SoundScene):
    """From bean to shelf: the world price of green arabica coffee and the American shelf price of ground coffee,
    dollars a pound, month by month, 1980-2026, drawn without narration as a year counter runs; under them, the
    shelf price year by year as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ10").load("intermission.melody")
        months = film["months"]
        t_of = np.array(film["times"])
        n = len(months)
        xs = np.array([int(m[:4]) + (int(m[5:7]) - 1) / 12 for m in months])
        shelf, bean = np.array(film["shelf"]), np.array(film["bean"])
        ax = plane([1979, 2027], [0, 10], center=UP * 0.1 + LEFT * 0.4, x_length=11.4, y_length=5.4,
                   xticks=[1980, 1990, 2000, 2010, 2020], yticks=[0, 2, 4, 6, 8, 10], ylabel=r"\$ a pound",
                   font_size=16, xfmt=lambda v: f"{v:.0f}")
        full = {
            "shelf": VMobject(stroke_color=SHELF, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(xs, shelf)]),
            "bean": VMobject(stroke_color=BEAN, stroke_width=3).set_points_as_corners(
                [ax.ax.c2p(x, v) for x, v in zip(xs, bean)]),
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
            RIGHT, buff=0.1) for t_, c in ((r"ground coffee on the shelf (BLS)", SHELF),
                                           (r"green arabica beans (World Bank)", BEAN))]
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.ax.c2p(1990, 9.0))
        intro = label(r"from bean to shelf: \ the same pound of coffee, \ twice", font_size=22, color=WHITE
                      ).move_to(ax.ax.c2p(2004, 9.3))

        def show_intro(m, t):
            m.set_opacity(float(np.clip(t / 1.5, 0, 1) * np.clip((10.0 - t) / 1.5, 0, 1)))

        src = data_tag(r"World Bank Pink Sheet (arabica, \$/kg converted to \$/lb); BLS via FRED (APU0000717311)",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the shelf price, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"coffee, \ 1980--2026: \ beans and the shelf, \ under the shelf price as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            snd.drive(year, set_year)
            snd.drive(intro, show_intro)
            snd.show(ax, *grown.values(), year, legend, intro)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, *grown.values(), year, legend, intro, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the ferry", r"a toll on a free crossing: \\ revenue against waste", BO),
                (r"marginal revenue", r"$MR = MC$; \ the Lerner index \\ $(p - c)/p = -1/\varepsilon$", MR),
                (r"the cost", r"Harberger's triangles, \\ Posner's rectangles", DWL),
                (r"first degree", r"a price for every buyer: \\ efficient, \ all to the seller", PROFIT),
                (r"third degree", r"groups; \ Varian's test: \\ output must rise", STUD),
                (r"second degree", r"menus that sort; \\ the bottom made worse", DEM),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
