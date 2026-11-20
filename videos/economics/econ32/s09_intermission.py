from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ32.common import *  # noqa: F403

EVENTS = ((1917.3, r"1917"), (1941.9, r"1941"), (1946.0, r"1946"), (1981.0, r"1981"), (2008.7, r"2008"),
          (2020.2, r"2020"))


class Intermission(SoundScene):
    """US federal debt held by the public as a share of GDP, quarter by quarter, 1889 to 2026, drawn as it passes,
    with the wars and crises marked; under it, the ratio as a tune; then the story so far."""

    def construct(self):
        film = load("film")
        R = load("rz")
        H = load("hap")
        P = load("playit")
        T = load("taxes")
        clip = ClipStore("econ32").load("intermission.melody")
        t = np.array(film["t"], float)
        v = np.array(film["debt"], float)
        ax = plane([1888, 2028], [0, 125], center=DOWN * 0.2 + LEFT * 0.3, x_length=11.6, y_length=5.4,
                   xticks=[1900, 1925, 1950, 1975, 2000, 2025], yticks=[0, 25, 50, 75, 100, 125],
                   ylabel=r"federal debt held by the public, \ \% of GDP", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{y:.0f}", font_size=15)
        full = VMobject(stroke_color=DEBT, stroke_width=3).set_points_as_corners(
            [ax.ax.c2p(x, y) for x, y in zip(t, v)])
        grow = full.copy()
        t0, t1 = film_time(t[0]), film_time(t[-1])

        def grower(m, tt):
            m.pointwise_become_partial(full, 0, float(np.clip((tt - t0) / (t1 - t0), 1e-3, 1)))

        year = Integer(1889, font_size=52, color=E.ACCENT, group_with_commas=False).move_to(ax.ax.c2p(1960, 110))

        def set_year(m, tt):
            m.set_value(int(np.clip(t[0] + (tt - t0) / (t1 - t0) * (t[-1] - t[0]), t[0], t[-1])))

        marks = VGroup(*[label(n, font_size=15, color=GREY_A).next_to(
            ax.ax.c2p(x, float(np.interp(x, t, v))), UP, buff=0.12) for x, n in EVENTS])
        src = data_tag(r"Ramey and Zubairy (to 1969); \ OMB via FRED (from 1970)", corner=DL, font_size=13).to_edge(
            UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: \ the debt ratio \ (computed)", font_size=13, color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"US federal debt to GDP, \ 1889--2026; \ the ratio as a tune")
            snd.show(src, stag)
            snd.drive(grow, grower)
            snd.drive(year, set_year)
            snd.show(ax, grow, year)
            self.play(FadeIn(ax), run_time=1.2)
            for (x, _), m in zip(EVENTS, marks):
                snd.wait_until(film_time(x))
                self.play(FadeIn(m), run_time=0.3)
            snd.wait_until("film_end")
            self.wait(1.0)
            self.play(*[FadeOut(m) for m in (ax, grow, year, marks, src, stag)], run_time=1.0)
            story = point_cards([
                (r"the 90\% threshold", rf"{H['steps'][0]['means'][3]:+.1f}\% published; \\ "
                                         rf"{H['steps'][-1]['means'][3]:+.1f}\% corrected", INFL),
                (r"r minus g", r"debt grows by itself \\ only when r exceeds g", DEBT),
                (r"the minister", rf"a surplus of {100 * P['stabilizing']:.2f}\% \\ holds debt at 100\%", TAX),
                (r"theory", r"below one with Taylor's rule; \\ above one at the zero bound", SPEND),
                (r"evidence", rf"military news {R['news8']:.2f}; \\ regions about 1.5", OUTPUT),
                (r"taxes", rf"{T['trough']:+.1f}\% after a tax rise \\ of 1\% of GDP", TAX),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
