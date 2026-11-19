from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ8.common import *  # noqa: F403
from videos.economics.econ8.s01_hook import douglas_axes


class Intermission(SoundScene):
    """Douglas's chart, redrawn year by year without narration: capital, labour and output in American
    manufacturing, 1899-1922 (1899 = 100, log scale), each line growing as the year counter runs, with Cobb and
    Douglas's formula dashed beside output; under them, the output index as a tune; at the end, the formula and its
    fit; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ8").load("intermission.melody")
        years = list(film["years"])
        times = np.array(film["times"])
        n = len(years)
        ax = douglas_axes(center=LEFT * 1.4 + DOWN * 0.3, x_length=9.0, y_length=5.8)
        a = ax.ax
        full = {}
        for key, col, w in (("K", CAP, 3.5), ("L", LAB, 3.5), ("Y", OUT, 4.0), ("fitted", WHITE, 2.5)):
            vals = np.array(film[key])
            full[key] = VMobject(stroke_color=col, stroke_width=w).set_points_as_corners(
                [a.c2p(y, np.log10(v)) for y, v in zip(years, vals)])
        grown = {k: m.copy() for k, m in full.items()}
        for k, m in grown.items():
            m.full_ = full[k]
            if k == "fitted":
                m.set_stroke(opacity=0.8)

        def grow(m, t):
            k = float(np.interp(t, times, np.arange(n)))
            m.pointwise_become_partial(m.full_, 0, max(k / (n - 1), 1e-3))

        heads = VGroup()
        for key, col in (("K", CAP), ("L", LAB), ("Y", OUT)):
            d = Dot(a.c2p(years[0], 2.0), radius=0.08, color=col)
            d.vals_ = np.log10(np.array(film[key]))
            heads.add(d)

        def move_head(m, t):
            k = float(np.interp(t, times, np.arange(n)))
            i = int(min(np.floor(k), n - 2))
            w = k - i
            m.move_to(a.c2p(years[i] + w, (1 - w) * m.vals_[i] + w * m.vals_[i + 1]))

        year = Integer(years[0], font_size=54, color=E.ACCENT, group_with_commas=False).to_corner(UR, buff=0.5).shift(
            DOWN * 0.5)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, times, np.arange(n)))), 0, n - 1))
            m.set_value(years[k])

        legend = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.4, color=c, stroke_width=4), label(t_, font_size=17,
                                                                                         color=GREY_A)).arrange(
            RIGHT, buff=0.1) for t_, c in ((r"capital", CAP), (r"labour", LAB), (r"output", OUT),
                                           (r"$1.01\,L^{3/4}C^{1/4}$", WHITE))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.1)
        legend.next_to(year, DOWN, buff=0.35).align_to(year, RIGHT)
        t_end = times[-1] + 0.3
        verdict = label(rf"24 years: \\ output grew $\times${film['Y'][-1] / 100:.1f}, \\ labour "
                        rf"$\times${film['L'][-1] / 100:.2f}, \\ capital $\times${film['K'][-1] / 100:.2f}",
                        font_size=19, color=E.ACCENT).next_to(legend, DOWN, buff=0.35).align_to(legend, RIGHT)
        verdict.set_opacity(0)

        def show_verdict(m, t):
            m.set_opacity(1.0 if t >= t_end else 0.0)

        intro = label(r"Douglas's chart, \ redrawn year by year: \\ capital, labour and output, \ 1899 = 100",
                      font_size=24, color=WHITE).move_to(a.c2p(1905.5, np.log10(380)))

        def show_intro(m, t):
            m.set_opacity(float(np.clip(t / 1.5, 0, 1) * np.clip((9.0 - t) / 1.5, 0, 1)))

        src = data_tag(r"Cobb and Douglas (1928), as reproduced by Felipe and Adams (2005), table 1", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the index of output, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"American manufacturing, 1899--1922, \ under its output as a tune")
            snd.show(src, stag)
            for m in grown.values():
                snd.drive(m, grow)
            for h in heads:
                snd.drive(h, move_head)
            snd.drive(year, set_year)
            snd.drive(verdict, show_verdict)
            snd.drive(intro, show_intro)
            snd.show(ax, *grown.values(), heads, year, legend, verdict, intro)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, *grown.values(), heads, year, legend, verdict, intro, src, stag)],
                      run_time=1.0)
            story = point_cards([
                (r"technology", r"isoquants; \ marginal products; \\ the rate of substitution", ISO),
                (r"Cobb--Douglas", r"$1.01\,L^{3/4}C^{1/4}$: \ shares as \\ exponents; \ fragile", OUT),
                (r"CES", r"$\sigma$, \ the elasticity of \\ substitution", LAB),
                (r"returns to scale", r"geometry, \ the six-tenths rule; \\ why not one firm?", CAP),
                (r"cost", r"tangency; \ the cost function; \\ Shephard", COST),
                (r"the margin", r"$p \cdot MP_L = w$; \ price = marginal \\ cost; \ shut-down and break-even",
                 PRICE),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
