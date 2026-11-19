from __future__ import annotations

from explainer.music.monochord.audio import ClipStore
from explainer.music.sound import SoundScene

from videos.economics.econ5.common import *  # noqa: F403

# durables in blues, nondurables in ambers and reds, services in greens and violets
CAT_COLOR = {"DMOT": "#5DADEC", "DFDH": "#7EC8F5", "DREQ": "#4F86C6", "DODG": "#9CC9F0",
             "DFXA": "#F2B84B", "DCLO": "#F28C6F", "DGOE": "#E9A3C9", "DONG": "#D9C7A7",
             "DHUT": "#7BD88F", "DHLC": "#F26D6D", "DTRS": "#5BD1C4", "DRCA": "#A6D96A",
             "DFSA": "#C9A0FF", "DIFS": "#8FA8D9", "DOTS": "#9AA5B8"}
SHORT = {"DMOT": "cars", "DFDH": "furniture", "DREQ": "recreational goods", "DODG": "other durables",
         "DFXA": "food at home", "DCLO": "clothing", "DGOE": "gasoline, energy", "DONG": "other nondurables",
         "DHUT": "housing, utilities", "DHLC": "health care", "DTRS": "transport services",
         "DRCA": "recreation services", "DFSA": "restaurants, hotels", "DIFS": "finance, insurance",
         "DOTS": "other services"}


class Intermission(SoundScene):
    """A century of the American basket, without narration: the shares of fifteen kinds of spending, 1929 to 2025,
    year by year in one bar, with food at home and health care traced below; under it, food's share as a tune that
    falls (Engel's law, Part 6); then the story so far."""

    def construct(self):
        film = load("film")
        clip = ClipStore("econ5").load("intermission.melody")
        years = list(film["years"])
        shares = np.array(film["shares"])
        codes = list(film["codes"])
        real = np.array(film["real_total"])
        times = np.array(film["times"])
        n = len(years)
        bx0, bx1, by, bh = -6.2, 6.2, 1.55, 0.75

        def frac(t):
            k = float(np.interp(t, times, np.arange(n)))
            i = int(min(np.floor(k), n - 2))
            w = k - i
            return i, w, (1 - w) * shares[i] + w * shares[i + 1]

        segs = VGroup(*[Rectangle(width=0.1, height=bh, stroke_width=0.6, stroke_color=BACKGROUND,
                                  fill_color=CAT_COLOR[c], fill_opacity=0.95) for c in codes])

        def bar(m, t):
            _, _, sh = frac(t)
            x = bx0
            for r, s in zip(m, sh):
                w = max((bx1 - bx0) * s, 1e-3)
                r.stretch_to_fit_width(w).move_to([x + w / 2, by, 0])
                x += w

        legend = VGroup()
        for c in codes:
            legend.add(VGroup(Square(0.16, stroke_width=0, fill_color=CAT_COLOR[c], fill_opacity=0.95),
                              label(SHORT[c], font_size=15, color=GREY_A)).arrange(RIGHT, buff=0.08))
        legend.arrange_in_grid(rows=3, cols=5, buff=(0.25, 0.1), col_alignments="lllll")
        legend.next_to([0, by + bh / 2, 0], UP, buff=0.25)
        year = Integer(years[0], font_size=54, color=E.ACCENT, group_with_commas=False).move_to([-4.7, -0.2, 0])

        def set_year(m, t):
            i, w, _ = frac(t)
            m.set_value(years[i] + (1 if w > 0.5 else 0))

        spend = DecimalNumber(real[0], num_decimal_places=0, font_size=30, color=WHITE, group_with_commas=True)
        spend_l = label(r"real spending per head, 2017 \$", font_size=17, color=GREY_B)
        sp = VGroup(spend, spend_l).arrange(DOWN, buff=0.08).move_to([-4.7, -1.4, 0])

        def set_spend(m, t):
            i, w, _ = frac(t)
            m.set_value((1 - w) * real[i] + w * real[i + 1])

        # food at home and health care, traced as time runs
        from explainer.ai.viz import axes

        ax = axes([1929, 2025], [0, 26], x_length=7.6, y_length=2.6, xticks=[1929, 1950, 1975, 2000, 2025],
                  yticks=[0, 10, 20], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}\\%", font_size=15,
                  center=RIGHT * 1.6 + DOWN * 1.55)
        a = ax.ax
        food = shares[:, codes.index("DFXA")] * 100
        health = shares[:, codes.index("DHLC")] * 100
        lines = {}
        for key, ser, col in (("food", food, CAT_COLOR["DFXA"]), ("health", health, CAT_COLOR["DHLC"])):
            lines[key] = VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(
                [a.c2p(y, v) for y, v in zip(years, ser)])
        tl = VGroup(label(r"food at home", font_size=17, color=CAT_COLOR["DFXA"]).next_to(a.c2p(1933, food[4]), UP,
                                                                                         buff=0.08),
                    label(r"health care", font_size=17, color=CAT_COLOR["DHLC"]).next_to(a.c2p(2016, health[87]), UP,
                                                                                         buff=0.12))

        def trace(m, t):
            k = float(np.interp(t, times, np.arange(n)))
            m.pointwise_become_partial(lines[m.key_], 0, max(k / (n - 1), 1e-3))

        tf = lines["food"].copy()
        tf.key_ = "food"
        th = lines["health"].copy()
        th.key_ = "health"
        verdict = label(rf"food at home \ {food[0]:.0f}\% $\to$ {food[-1]:.1f}\%; \ health care \ {health[0]:.0f}\% "
                        rf"$\to$ {health[-1]:.1f}\%; \ real spending per head $\times${real[-1] / real[0]:.1f}",
                        font_size=21, color=E.ACCENT).to_edge(DOWN, buff=0.25).set_opacity(0)

        def show_verdict(m, t):
            m.set_opacity(1.0 if t >= times[-1] + 0.3 else 0.0)

        tag = data_tag(r"BEA, personal consumption expenditures by type of product, 1929--2025 (FRED)", corner=DL,
                       font_size=13).to_edge(UP, buff=0.12).to_edge(LEFT, buff=0.3)
        stag = note(r"sound: food's share of spending, \ year by year (computed)", font_size=13,
                    color=E.ACCENT).to_corner(UR, buff=0.15)
        with self.listen(clip) as snd:
            snd.caption(r"a century of the American basket, \ under food's share as a pitch")
            snd.show(tag, stag)
            snd.drive(segs, bar)
            snd.drive(year, set_year)
            snd.drive(spend, set_spend)
            snd.drive(tf, trace)
            snd.drive(th, trace)
            snd.drive(verdict, show_verdict)
            snd.show(segs, legend, year, sp, ax, tf, th, tl, verdict)
            self.play(FadeIn(legend), FadeIn(ax), FadeIn(tl), FadeIn(spend_l), run_time=1.2)
            snd.wait_until("film_end")
            self.play(*[FadeOut(m) for m in (segs, legend, year, sp, ax, tf, th, tl, tag, stag, verdict)],
                      run_time=1.0)
            story = point_cards([
                (r"a ranking", r"complete, transitive, continuous: \\ the money pump punishes cycles", IC),
                (r"utility as a label", r"only the order counts; \\ the MRS survives relabelling", E.ACCENT),
                (r"shapes", r"substitutes, complements, \\ Cobb--Douglas, CES", "#C9A0FF"),
                (r"the tangency", r"MRS = price ratio; \\ $\lambda$, the value of a dollar", BUDGET),
                (r"corners and kinks", r"jumps at a bulk price; \\ bunching at a tax credit's kink", VIOL),
                (r"your eleven choices", r"next: \ do they fit together?", PASS),
            ], width=12.6, cols=3, font_size=22).move_to(DOWN * 0.3)
            head = label(r"The story so far", font_size=40).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in story.cards], lag_ratio=0.6),
                      run_time=max(3.0, snd.remaining() - 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
