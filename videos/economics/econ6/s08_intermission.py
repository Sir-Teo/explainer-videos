from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ6.common import *  # noqa: F403

# durables in blues, nondurables in ambers and reds, services in greens and violets (as Part 5's intermission)
CAT_COLOR = {"DMOT": "#5DADEC", "DFDH": "#7EC8F5", "DREQ": "#4F86C6", "DODG": "#9CC9F0",
             "DFXA": "#F2B84B", "DCLO": "#F28C6F", "DGOE": "#E9A3C9", "DONG": "#D9C7A7",
             "DHUT": "#7BD88F", "DHLC": "#F26D6D", "DTRS": "#5BD1C4", "DRCA": "#A6D96A",
             "DFSA": "#C9A0FF", "DIFS": "#8FA8D9", "DOTS": "#9AA5B8"}
SHORT = {"DMOT": "cars", "DFDH": "furniture", "DREQ": "recreational goods", "DODG": "other durables",
         "DFXA": "food at home", "DCLO": "clothing", "DGOE": "gasoline, energy", "DONG": "other nondurables",
         "DHUT": "housing", "DHLC": "health care", "DTRS": "transport services", "DRCA": "recreation services",
         "DFSA": "restaurants, hotels", "DIFS": "finance, insurance", "DOTS": "other services"}
NAMED = ("DREQ", "DHLC", "DFXA", "DCLO", "DGOE", "DFSA")


class Intermission(SoundScene):
    """A century of relative prices, without narration: fifteen kinds of American spending as dots, each at its
    price relative to all spending and its quantity per head (both 1929 = 1, log scales), moving year by year from
    1929 to 2025 and leaving a trail; under them, the relative price of recreational goods as a falling tune; at the
    end, the fifteen endpoints and the line through them; then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ6").load("intermission.melody")
        years = list(film["years"])
        codes = list(film["codes"])
        rel = np.log10(np.array(film["rel"]))
        qty = np.log10(np.array(film["qty"]))
        times = np.array(film["times"])
        n = len(years)
        from explainer.ai.viz import axes

        def p10(v):
            x = 10 ** v
            return f"{x:g}" if x < 1 else f"{x:,.0f}".replace(",", "{,}")

        ax = axes([-2.0, 0.7], [-1.0, 3.0], x_length=9.4, y_length=6.1, xticks=[-2, -1, 0], yticks=[-1, 0, 1, 2, 3],
                  xlabel=r"price relative to all spending \ (1929 = 1, log scale)",
                  ylabel=r"quantity per head \ (1929 = 1, log)", font_size=16, xfmt=p10, yfmt=p10,
                  center=LEFT * 1.3 + DOWN * 0.3)
        a = ax.ax

        def at(t):
            k = float(np.interp(t, times, np.arange(n)))
            i = int(min(np.floor(k), n - 2))
            w = k - i
            return i, w

        dots, trails = VGroup(), VGroup()
        for j, c in enumerate(codes):
            full = VMobject(stroke_color=CAT_COLOR[c], stroke_width=2.5, stroke_opacity=0.75).set_points_as_corners(
                [a.c2p(rel[i, j], qty[i, j]) for i in range(n)])
            tr = full.copy()
            tr.full_, tr.j_ = full, j
            trails.add(tr)
            d = Dot(a.c2p(rel[0, j], qty[0, j]), radius=0.085, color=CAT_COLOR[c])
            d.j_ = j
            dots.add(d)

        def move_dot(m, t):
            i, w = at(t)
            j = m.j_
            m.move_to(a.c2p((1 - w) * rel[i, j] + w * rel[i + 1, j], (1 - w) * qty[i, j] + w * qty[i + 1, j]))
            pulse(m, t)

        def grow(m, t):
            k = float(np.interp(t, times, np.arange(n)))
            m.pointwise_become_partial(m.full_, 0, max(k / (n - 1), 1e-3))

        names = VGroup()
        for c in NAMED:
            j = codes.index(c)
            lab = label(SHORT[c], font_size=16, color=CAT_COLOR[c])
            lab.j_ = j
            names.add(lab)

        def follow(m, t):
            i, w = at(t)
            j = m.j_
            m.next_to(a.c2p((1 - w) * rel[i, j] + w * rel[i + 1, j], (1 - w) * qty[i, j] + w * qty[i + 1, j]), UR,
                      buff=0.06)

        year = Integer(years[0], font_size=54, color=E.ACCENT, group_with_commas=False).to_corner(UR, buff=0.5).shift(
            DOWN * 0.5)

        def set_year(m, t):
            i, w = at(t)
            m.set_value(years[i] + (1 if w > 0.5 else 0))

        legend = VGroup(*[VGroup(Dot(radius=0.06, color=CAT_COLOR[c]), label(SHORT[c], font_size=14,
                                                                           color=GREY_A)).arrange(RIGHT, buff=0.08)
                          for c in codes]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        legend.next_to(year, DOWN, buff=0.35).align_to(year, RIGHT)
        slope, icept = film["slope"], film["intercept"]
        xs = np.array([-1.95, 0.65])
        fit_full = Line(a.c2p(xs[0], (icept + slope * xs[0] * np.log(10)) / np.log(10)),
                        a.c2p(xs[1], (icept + slope * xs[1] * np.log(10)) / np.log(10)), color=WHITE,
                        stroke_width=2.5, stroke_opacity=0.85)
        fit = fit_full.copy().set_opacity(0)
        t_end = times[-1] + 0.3

        def show_fit(m, t):
            # after the last year, the line through the fifteen endpoints draws itself across the final hold
            if t < t_end:
                m.set_opacity(0.0)
                return
            m.pointwise_become_partial(fit_full, 0, float(np.clip((t - t_end) / 4.5, 1e-3, 1)))
            m.set_stroke(opacity=0.85)

        def pulse(m, t):
            # the endpoints breathe while the line draws, so the closing seconds are not a still frame
            if t >= t_end:
                k = 1 + 0.25 * np.sin(2 * np.pi * (t - t_end) / 1.6) ** 2
                m.set(width=2 * 0.085 * k)

        verdict = label(rf"fifteen goods, \ 1929--2025: \\ slope {slope:.2f}, \ correlation {film['corr']:.2f} \\ "
                        rf"real spending per head $\times${film['real_ratio']:.1f}: \\ not a demand curve", font_size=19,
                        color=E.ACCENT).next_to(legend, DOWN, buff=0.3).align_to(legend, RIGHT).set_opacity(0)

        def show_verdict(m, t):
            m.set_opacity(1.0 if t >= times[-1] + 0.3 else 0.0)

        intro = label(r"one dot for each of fifteen kinds of spending: \\ its price relative to all spending, "
                      r"across; \ how much is bought per head, up", font_size=24, color=WHITE)
        intro.move_to(a.c2p(-1.0, 2.3))

        def show_intro(m, t):
            # in over the first second and a half, held, out by the ninth second: the opening years barely move
            o = float(np.clip(t / 1.5, 0, 1) * np.clip((9.0 - t) / 1.5, 0, 1))
            m.set_opacity(o)
            m.move_to(a.c2p(-1.0, 2.3) + UP * 0.15 * (1 - o))

        tag = data_tag(r"BEA, personal consumption expenditures by type of product, 1929--2025 (FRED)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: the relative price of recreational goods, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"a century of relative prices, \ under the price of recreational goods as a pitch")
            snd.show(tag, stag)
            for tr in trails:
                snd.drive(tr, grow)
            for d in dots:
                snd.drive(d, move_dot)
            for nm in names:
                snd.drive(nm, follow)
            snd.drive(year, set_year)
            snd.drive(fit, show_fit)
            snd.drive(intro, show_intro)
            snd.drive(verdict, show_verdict)
            snd.show(ax, trails, dots, names, year, legend, fit, verdict, intro)
            self.play(FadeIn(ax), FadeIn(legend), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (ax, trails, dots, names, year, legend, fit, verdict, intro, tag, stag)],
                      run_time=1.0)
            story = point_cards([
                (r"a price falls", r"two effects: \ cheaper relative to, \\ and richer", SUB),
                (r"Slutsky", r"$\varepsilon = \varepsilon^h - w\,\eta$; \\ compensated demand slopes down", INC),
                (r"Giffen", r"inferior, \ a big budget share, \\ no room to substitute: \ Hunan's rice", GIFF),
                (r"duality", r"four functions; \ Roy and Shephard; \\ $e$ concave in prices", HICKS),
                (r"integrability", r"a symmetric Slutsky matrix, \\ or a loop that pumps money", E.ACCENT),
                (r"next", r"Engel curves, \ welfare in dollars, \\ the cost of living", IC),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
