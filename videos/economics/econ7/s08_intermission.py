from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ7.common import *  # noqa: F403

ERAS = [((1935, 1949), r"Depression and war", "#F2B84B"), ((1950, 1979), r"1950--79", "#7EC8F5"),
        ((1980, 2007), r"1980--2007", "#7BD88F"), ((2008, 2025), r"2008--25", "#C9A0FF")]


def era_color(y: int) -> str:
    return next(c for (a, b), _, c in ERAS if a <= y <= b)


class Intermission(SoundScene):
    """Hall's question, without narration: for every year from 1935 to 2025, America's real Treasury bill rate
    (across) against the growth of real consumption per head (up), one dot a year, coloured by era; under them, the
    real rate as a tune; at the end, the fitted line and the instrumented slope; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ7").load("intermission.melody")
        years = list(film["years"])
        r = np.array(film["rate"])
        g = np.array(film["growth"])
        times = np.array(film["times"])
        n = len(years)
        ax = plane([-12, 8], [-4, 11], center=LEFT * 1.4 + DOWN * 0.3, x_length=9.0, y_length=6.0,
                   xticks=[-12, -8, -4, 0, 4, 8], yticks=[-4, 0, 4, 8], xlabel=r"real interest rate on Treasury "
                   r"bills, \ \%", ylabel=r"growth of real consumption per head, \ \%", font_size=16)
        a = ax.ax
        zero = VGroup(DashedLine(a.c2p(0, -4), a.c2p(0, 11), color=GREY_D, stroke_width=1.2),
                      DashedLine(a.c2p(-12, 0), a.c2p(8, 0), color=GREY_D, stroke_width=1.2))
        dots = VGroup()
        for i, y in enumerate(years):
            d = Dot(a.c2p(r[i], g[i]), radius=0.075, color=era_color(y)).set_opacity(0)
            d.k_ = i
            dots.add(d)

        def show_dot(m, t):
            k = float(np.interp(t, times, np.arange(n)))
            m.set_opacity(1.0 if m.k_ <= k + 1e-9 else 0.0)
            # the newest dot glows for a moment
            age = k - m.k_
            m.set(width=2 * 0.075 * (1.0 + (0.9 * max(0.0, 1 - age) if 0 <= age < 1 else 0.0)))

        ring = Circle(radius=0.2, color=WHITE, stroke_width=2).move_to(dots[0])

        def follow_ring(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, times, np.arange(n)))), 0, n - 1))
            m.move_to(dots[k].get_center())
            m.set_stroke(opacity=0.0 if t > times[-1] + 0.5 else 0.8)

        year = Integer(years[0], font_size=54, color=E.ACCENT, group_with_commas=False).to_corner(UR, buff=0.5).shift(
            DOWN * 0.5)

        def set_year(m, t):
            k = int(np.clip(np.floor(float(np.interp(t, times, np.arange(n)))), 0, n - 1))
            m.set_value(years[k])

        legend = VGroup(*[VGroup(Dot(radius=0.07, color=c), label(name, font_size=17, color=GREY_A)).arrange(
            RIGHT, buff=0.1) for _, name, c in ERAS]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.next_to(year, DOWN, buff=0.35).align_to(year, RIGHT)
        named = {1942: r"1942: \ rationing", 1946: r"1946: \ demobilized", 2021: r"2021: \ reopening",
                 2020: r"2020"}
        tags = VGroup()
        for y, txt in named.items():
            i = years.index(y)
            t_ = label(txt, font_size=15, color=era_color(y)).next_to(a.c2p(r[i], g[i]), UR if y != 2020 else DL,
                                                                       buff=0.05).set_opacity(0)
            t_.k_ = i
            tags.add(t_)

        def show_tag(m, t):
            k = float(np.interp(t, times, np.arange(n)))
            m.set_opacity(1.0 if k >= m.k_ else 0.0)

        full = film["full"]
        xs = np.array([-11.5, 7.5])
        fit_full = Line(a.c2p(xs[0], full["ols_const"] + full["ols"] * xs[0]),
                        a.c2p(xs[1], full["ols_const"] + full["ols"] * xs[1]), color=WHITE, stroke_width=2.5)
        fit = fit_full.copy().set_opacity(0)
        t_end = times[-1] + 0.3

        def show_fit(m, t):
            if t < t_end:
                m.set_opacity(0.0)
                return
            m.pointwise_become_partial(fit_full, 0, float(np.clip((t - t_end) / 3.5, 1e-3, 1)))
            m.set_stroke(opacity=0.85)

        verdict = label(rf"{full['n']} years: \\ slope {full['ols']:.2f}, \ correlation {full['corr']:.2f}; \\ "
                        rf"instrumented: \ {signed(full['iv'], 2)} \ (s.e.\ {full['iv_se']:.2f}) \\ the EIS: \ about "
                        r"zero", font_size=19, color=E.ACCENT).next_to(legend, DOWN, buff=0.35).align_to(
            legend, RIGHT).set_opacity(0)

        def show_verdict(m, t):
            m.set_opacity(1.0 if t >= t_end else 0.0)

        intro = label(r"one dot a year: \ the real interest rate, across; \\ how fast consumption per head grew, up",
                      font_size=24, color=WHITE).move_to(a.c2p(-4.0, 9.4))

        def show_intro(m, t):
            o = float(np.clip(t / 1.5, 0, 1) * np.clip((9.0 - t) / 1.5, 0, 1))
            m.set_opacity(o)

        src = data_tag(r"BEA (real PCE, PCE prices, population) and the Federal Reserve (3-month bill), via FRED",
                       corner=DL, font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the real bill rate, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"Hall's question: \ do people save more when saving pays more?")
            snd.show(src, stag)
            for d in dots:
                snd.drive(d, show_dot)
            for t_ in tags:
                snd.drive(t_, show_tag)
            snd.drive(ring, follow_ring)
            snd.drive(year, set_year)
            snd.drive(fit, show_fit)
            snd.drive(verdict, show_verdict)
            snd.drive(intro, show_intro)
            snd.show(ax, zero, dots, tags, ring, year, legend, fit, verdict, intro)
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, zero, dots, tags, ring, year, legend, fit, verdict, intro, src,
                                             stag)], run_time=1.0)
            story = point_cards([
                (r"Fisher", r"the interest rate is a price; \\ the Euler equation", TODAY),
                (r"discounting", r"only exponential \\ is time consistent", LATER),
                (r"expected utility", r"independence: \\ straight, parallel lines", EUL),
                (r"Allais", r"1A with 2B: \\ the lines can't be parallel", FAN),
                (r"risk aversion", r"concavity; \ certainty equivalents; \\ $\tfrac12 A\sigma^2$", UTIL),
                (r"insurance", r"full cover at fair odds; \\ deductibles that make no sense", RISKY),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
