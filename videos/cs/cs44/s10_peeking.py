from __future__ import annotations

import math
from statistics import NormalDist

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, load, trace

PATH_COLOURS = (DATA, LAM, KERN, TEAL, GREY_B, PINK)


def _upto(ax, pts, t, color, width=2.5):
    """The polyline through ``pts`` (x ascending) drawn as far as x = t, ending exactly at t."""
    P = [p for p in pts if p[0] <= t]
    nxt = next((p for p in pts if p[0] > t), None)
    if P and nxt is not None:
        (x0, y0), (x1, y1) = P[-1], nxt
        P = P + [(t, y0 + (y1 - y0) * (t - x0) / (x1 - x0))]
    if len(P) < 2:
        P = (P or pts[:1]) * 2
    return VMobject(color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, y) for x, y in P])


def _z(p):
    """The |z| a two-sided p-value came from."""
    return NormalDist().inv_cdf(1 - min(max(p, 1e-12), 1.0) / 2)


def _msprt_z(n, tau2, V=2 * 0.05 * 0.95, alpha=0.05):
    """|z| at which the mixture likelihood ratio reaches 1/alpha after n users per arm (the boundary in z units)."""
    r = (V + n * tau2) / (n * tau2)
    return math.sqrt(r * (2 * math.log(1 / alpha) + math.log((V + n * tau2) / V)))


class Peeking(VoiceoverScene):
    def construct(self):
        self.card()
        self.paths()
        self.climb()
        self.why()
        self.always_valid()
        self.trade()

    def card(self):
        card = chapter_card(9, r"Looking too often", r"Why does checking an experiment every day break it?",
                            lit=(1970, 2017), extra=((1970, r"Robbins: \ mixture sequential tests"),
                                                     (2017, r"Johari et al.: \ always-valid "
                                                            r"p-values")), part=PART)
        with self.voiceover("Chapter nine. Looking too often."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def paths(self):
        pk = load("peeking")
        days = pk["days"]
        head = label(r"An A/A test, \ checked every morning", font_size=36).to_edge(UP, buff=0.3)
        names = {-2: "0.01", -1: "0.1", 0: "1"}
        g = axes([0, days, 5], [-2, 0, 1], x_length=7.6, y_length=4.4, x_label=r"day of the experiment",
                 y_label=r"p-value so far \ (log scale)", xticks=range(0, days + 1, 5), yticks=(-2, -1, 0),
                 fy=lambda v: names[int(v)]).move_to([-2.5, -0.35, 0])
        ax = g.ax
        y05 = math.log10(0.05)
        zone = Polygon(ax.c2p(0, -2), ax.c2p(days, -2), ax.c2p(days, y05), ax.c2p(0, y05), stroke_width=0,
                       fill_color=NO, fill_opacity=0.15)
        line = DashedLine(ax.c2p(0, y05), ax.c2p(days, y05), color=NO)
        ll = label(r"$p = 0.05$", font_size=17, color=NO).next_to(ax.c2p(days, y05), RIGHT, buff=0.1)
        pts = [[(d + 1, math.log10(max(p, 0.01))) for d, p in enumerate(path)] for path in pk["paths"]]
        t = ValueTracker(1.0)
        curves = VGroup(*[always_redraw(lambda P=P, c=c: _upto(ax, P, t.get_value(), c))
                          for P, c in zip(pts, PATH_COLOURS)])
        heads = VGroup(*[always_redraw(lambda P=P, c=c: Dot(_upto(ax, P, t.get_value(), c).get_end(), radius=0.05,
                                                              color=c)) for P, c in zip(pts, PATH_COLOURS)])
        hits = VGroup(*[Dot(ax.c2p(*P[k]), radius=0.09, color=NO) for P, path in zip(pts, pk["paths"])
                        for k in range(len(path)) if path[k] < 0.05])
        n_hit = len({i for i, path in enumerate(pk["paths"]) if min(path) < 0.05})
        notes = VGroup(
            wrapped_label(rf"two identical versions; \ {pk['per_day']:,} users a day in each; \ 5\% convert", 4.3,
                          font_size=19, color=GREY_A),
            wrapped_label(r"each morning: \ the z-test of Chapter 8 on everything so far", 4.3, font_size=19,
                          color=WHITE),
            wrapped_label(r"with no real difference, \ the p-value is equally likely to be anywhere in $[0, 1]$ "
                          r"on any one day, \ and it wanders", 4.3, font_size=19, color=HEAD),
            wrapped_label(rf"{len(pts)} experiments: \ {n_hit} below the line at some look", 4.3, font_size=19,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Here is an experiment with nothing in it: two identical versions, an A/A test, with a thousand users "
            "a day in each and a conversion rate of five percent. <bookmark mark='a'/> Every morning someone runs "
            "last chapter's z-test on everything so far. <bookmark mark='b'/> With no difference, the p-value has "
            "nowhere to settle. On any one day it is equally likely to be anywhere between zero and one, and from "
            "day to day it wanders, <bookmark mark='c'/> sometimes close to the red line. Of these six, one falls "
            "below it, on the last morning. Look often enough, and any of them might."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(zone), Create(line), FadeIn(ll), FadeIn(notes[0]))
            self.add(curves, heads)
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), t.animate.set_value(8), run_time=3, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(notes[2]), t.animate.set_value(22), run_time=6, rate_func=linear)
            vo.wait_until("c")
            self.play(t.animate.set_value(days), run_time=3, rate_func=linear)
            self.play(FadeIn(hits, scale=1.5), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def climb(self):
        pk = load("peeking")
        fpr = pk["fpr_peeking"]
        days = pk["days"]
        head = label(r"Stop at the first $p < 0.05$", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, days, 5], [0, 0.3, 0.05], x_length=7.6, y_length=4.4, x_label=r"days of daily checking",
                 y_label=r"experiments that declared a winner", xticks=range(0, days + 1, 5),
                 yticks=[0.05 * k for k in range(1, 7)], fy=lambda v: f"{100 * v:.0f}\\%").move_to([-2.5, -0.35, 0])
        ax = g.ax
        five = DashedLine(ax.c2p(0, 0.05), ax.c2p(days, 0.05), color=YES)
        fl = label(r"the promised 5\%", font_size=17, color=YES).next_to(ax.c2p(days, 0.05), UP, buff=0.08).shift(
            LEFT * 1.0)
        pts = [(d + 1, v) for d, v in enumerate(fpr)]
        t = ValueTracker(1.0)
        curve = always_redraw(lambda: _upto(ax, pts, t.get_value(), NO, width=3.5))
        dot = always_redraw(lambda: Dot(curve.get_end(), radius=0.07, color=NO))
        readout = always_redraw(lambda: label(
            rf"day {int(round(t.get_value()))}: \ {100 * fpr[int(round(t.get_value())) - 1]:.1f}\%", font_size=24,
            color=NO).move_to([4.5, 1.9, 0]))
        once = Dot(ax.c2p(days, pk["fpr_final_only"]), radius=0.09, color=YES)
        notes = VGroup(
            wrapped_label(r"4,000 simulated A/A experiments, \ each stopped the first morning its p-value is below "
                          r"0.05", 4.3, font_size=19, color=GREY_A),
            wrapped_label(rf"the same experiments looked at once, \ on day {days}: \ "
                          rf"{100 * pk['fpr_final_only']:.1f}\% \ (green dot)", 4.3, font_size=19, color=YES),
            wrapped_label(r"0.05 is a promise about one look, \ not thirty", 4.3, font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.5, -0.6, 0])
        f = [round(100 * fpr[k]) for k in (0, 6, 13)]
        with self.voiceover(
            "Now simulate four thousand of them, and stop each one the first morning its p-value "
            "falls below five percent, declaring a winner. <bookmark mark='a'/> On the first day, "
            f"{f[0]} percent stop, as promised. After a week, {f[1]} percent have stopped. After "
            f"two weeks, {f[2]}. <bookmark mark='b'/> By day thirty, {100 * fpr[-1]:.0f} percent of experiments with "
            "no effect at all have announced one. <bookmark mark='c'/> The same experiments, looked at only once, "
            f"at the end, give {100 * pk['fpr_final_only']:.0f} percent. The test was never wrong; the stopping rule "
            "was. Five percent is a promise about one look, not thirty."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(five), FadeIn(fl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.add(curve, dot, readout)
            self.play(t.animate.set_value(14), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(days), run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(once, scale=1.5), FadeIn(notes[1]))
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def _zgraph(self, pk, ymax=4):
        days = pk["days"]
        g = axes([0, days, 5], [0, ymax, 1], x_length=7.6, y_length=4.4, x_label=r"day of the experiment",
                 y_label=r"$|z|$ so far", xticks=range(0, days + 1, 5), yticks=range(1, ymax)).move_to(
            [-2.5, -0.35, 0])
        ax = g.ax
        zs = [[(d + 1, _z(p)) for d, p in enumerate(path)] for path in pk["paths"]]
        curves = VGroup(*[trace(ax, P, c, width=2.2) for P, c in zip(zs, PATH_COLOURS)])
        band = DashedLine(ax.c2p(0, 1.96), ax.c2p(days, 1.96), color=NO)
        bl = label(r"$1.96$", font_size=17, color=NO).next_to(ax.c2p(days, 1.96), RIGHT, buff=0.1)
        return g, ax, curves, band, bl

    def why(self):
        pk = load("peeking")
        head = label(r"Many looks, \ many chances", font_size=36).to_edge(UP, buff=0.3)
        g, ax, curves, band, bl = self._zgraph(pk)
        lil = MathTex(r"\limsup_{n\to\infty} \frac{|S_n|}{\sqrt{2n\,\log\log n}} = 1", font_size=32, color=HEAD)
        indep = 1 - 0.95 ** pk["days"]
        notes = VGroup(
            wrapped_label(r"the same six experiments, \ as the z-statistic each p-value came from; \ the test "
                          r"rejects above 1.96", 4.3, font_size=19, color=GREY_A),
            wrapped_label(r"with no effect, \ $z_n = S_n/\sqrt{n}$ is a random walk scaled by its length \ "
                          r"(Part 20)", 4.3, font_size=19, color=WHITE),
            lil,
            wrapped_label(r"the law of the iterated logarithm \ (Khinchin, \ 1924): \ the walk's peaks keep "
                          r"reaching $\sqrt{2\log\log n}$, \ which grows without limit", 4.3, font_size=19,
                          color=HEAD),
            wrapped_label(rf"so watched forever, \ $|z|$ crosses any fixed line; \ {pk['days']} independent tests "
                          rf"would give {100 * indep:.0f}\%, \ overlapping looks give "
                          rf"{100 * pk['fpr_peeking'][-1]:.0f}\%", 4.3, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, -0.3, 0])
        with self.voiceover(
            "Why does looking hurt? <bookmark mark='a'/> Turn each p-value back into its z-statistic. The test "
            "rejects when z rises above one point nine six. <bookmark mark='b'/> With no real difference, z is a "
            "random walk divided by the square root of its length: Part 20's concentration, in motion. "
            "<bookmark mark='c'/> The law of the iterated logarithm, proved by Aleksandr Khinchin in 1924, says its "
            "peaks keep returning to about the square root of two log log n, which grows without limit. "
            "<bookmark mark='d'/> So a walk watched forever crosses any fixed line. Thirty separate tests would "
            f"give {100 * indep:.0f} percent false positives; daily looks share most of their data, so we saw "
            f"{100 * pk['fpr_peeking'][-1]:.0f}, but every look adds some."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(band), FadeIn(bl), FadeIn(notes[0]))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(notes[2]), FadeIn(notes[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    def always_valid(self):
        pk = load("peeking")
        days, per_day = pk["days"], pk["per_day"]
        head = label(r"A test that is safe to watch", font_size=36).to_edge(UP, buff=0.3)
        ymax = 5
        g, ax, curves, band, bl = self._zgraph(pk, ymax=ymax)
        bounds = VGroup()
        for lift, col in ((0.05, YES), (0.10, LAM)):
            tau2 = (0.05 * lift) ** 2
            P = [(d, _msprt_z(d * per_day, tau2)) for d in [k / 4 for k in range(4, 4 * days + 1)]]
            bounds.add(trace(ax, [q for q in P if q[1] <= ymax], col, width=3.5))
        bnames = VGroup(
            label(r"stop here: \ mixture for 5\% lifts", font_size=17, color=YES),
            label(r"mixture for 10\% lifts", font_size=17, color=LAM),
        )
        bnames[0].move_to(ax.c2p(20, 4.2))
        bnames[1].move_to(ax.c2p(20, 2.6))
        lam = MathTex(r"\Lambda_n = \int \frac{L_n(\theta)}{L_n(0)}\, \mathcal{N}(\theta;\,0,\tau^2)\,d\theta",
                      font_size=28, color=WHITE)
        rule = MathTex(r"\text{stop when } \Lambda_n \ge 1/\alpha", font_size=28, color=YES)
        ville = MathTex(r"P\!\left(\sup_n \Lambda_n \ge 1/\alpha\right) \le \alpha", font_size=28, color=HEAD)
        notes = VGroup(
            wrapped_label(r"mixture SPRT \ (Robbins, \ 1970): \ the likelihood ratio, \ averaged over plausible "
                          r"effects", 4.3, font_size=19, color=GREY_A),
            lam, rule,
            wrapped_label(r"with no effect, \ $\Lambda_n$ is a fair bet: \ a martingale with mean 1, \ so by Ville's "
                          r"inequality \ (1939)", 4.3, font_size=19, color=WHITE),
            ville,
            wrapped_label(r"always-valid p-value: \ $p_n = \min(1,\ 1/\max_{m\le n}\Lambda_m)$ \ (Johari, \ "
                          r"Koomen, \ Pekelis and Walsh, \ 2017)", 4.3, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, -0.35, 0])
        with self.voiceover(
            "The fix is a test built to be watched. <bookmark mark='a'/> Abraham Wald's sequential test compared "
            "the likelihood of the data under an effect with its likelihood under none; Herbert Robbins, in 1970, "
            "averaged that ratio over a range of plausible effects. <bookmark mark='b'/> Stop when it reaches one "
            "over alpha, twenty. <bookmark mark='c'/> With no effect, the ratio is a fair bet: its expected value "
            "stays one however long you play, and Ville's inequality says it ever reaches twenty with probability "
            "at most one in twenty. <bookmark mark='d'/> In z units the boundary is no longer flat: it starts high "
            "and comes down slowly. <bookmark mark='e'/> Ramesh Johari, Pete Koomen, Leonid Pekelis and David "
            "Walsh turned this into always-valid p-values, safe to check every morning."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(band), FadeIn(bl), FadeIn(curves))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), Write(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]), FadeIn(notes[4]))
            vo.wait_until("d")
            self.play(Create(bounds[0]), Create(bounds[1]), run_time=2)
            self.play(FadeIn(bnames))
            vo.wait_until("e")
            self.play(FadeIn(notes[5]))
        self.wait(0.4)
        self.clear_scene()

    def trade(self):
        pk = load("peeking")
        sq = load("sequential")
        fx = sq["fixed_n_lift10"]
        head = label(r"Valid at every look, \ at a price", font_size=36).to_edge(UP, buff=0.3)
        rows = [
            (r"z-test, \ checked daily", pk["fpr_peeking"][-1], None, None, NO),
            (r"z-test, \ one look on day 30", pk["fpr_final_only"], 0.8, None, GREY_B),
            (r"mixture SPRT, \ $\tau$ for 5\% lifts", sq["null"]["rejected"], sq["lift10"]["rejected"],
             sq["lift10"]["median_day"], YES),
            (r"mixture SPRT, \ $\tau$ for 10\% lifts", sq["null_tau"]["rejected"], sq["lift10_tau"]["rejected"],
             sq["lift10_tau"]["median_day"], LAM),
        ]
        x_fp, w_fp, x_pw, w_pw = -2.3, 2.9, 1.9, 3.6
        top = 1.6
        rowh = 0.95
        names, fp_bars, pw_bars = VGroup(), VGroup(), VGroup()
        for k, (nm, fp, pw, md, col) in enumerate(rows):
            y = top - k * rowh
            n = VGroup(label(nm, font_size=19, color=col))
            if md is not None:
                n.add(label(rf"median stop: \ day {md:.0f}", font_size=16, color=GREY_B))
            n.arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([-4.7, y, 0]).align_to([-6.7, 0, 0], LEFT)
            names.add(n)
            b = Rectangle(width=max(0.02, fp / 0.3 * w_fp), height=0.42, stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to([x_fp, y, 0], aligned_edge=LEFT)
            vt = label(rf"{100 * fp:.1f}\%", font_size=18, color=col).next_to(b, RIGHT, buff=0.1)
            vt.set_x(max(vt.get_x(), x_fp + 0.05 / 0.3 * w_fp + 0.1 + vt.width / 2))
            fp_bars.add(VGroup(b, vt))
            if pw is None:
                pw_bars.add(VGroup(label(r"---", font_size=18, color=GREY_C).move_to([x_pw + 0.3, y, 0])))
                continue
            b2 = Rectangle(width=pw * w_pw, height=0.42, stroke_width=0, fill_color=col,
                           fill_opacity=0.4 if md is None else 0.85).move_to([x_pw, y, 0], aligned_edge=LEFT)
            txt = rf"{100 * pw:.0f}\%" + (r" \ (design)" if md is None else "")
            pw_bars.add(VGroup(b2, label(txt, font_size=18, color=col).next_to(b2, RIGHT, buff=0.1)))
        base_y = top + 0.55
        heads = VGroup(
            label(r"false positives, \ no real effect", font_size=19, color=GREY_A).move_to([x_fp, base_y, 0],
                                                                                         aligned_edge=LEFT),
            label(r"power for a real 10\% lift, \ within 30 days", font_size=19, color=GREY_A).move_to(
                [x_pw, base_y, 0], aligned_edge=LEFT),
        )
        bot = top - (len(rows) - 1) * rowh - 0.4
        five = DashedLine([x_fp + 0.05 / 0.3 * w_fp, top + 0.3, 0], [x_fp + 0.05 / 0.3 * w_fp, bot, 0], color=YES,
                          stroke_width=2)
        fl = label(r"5\%", font_size=16, color=YES).next_to([x_fp + 0.05 / 0.3 * w_fp, bot, 0], DOWN, buff=0.08)
        axes_l = VGroup(fl, Line([x_fp, top + 0.3, 0], [x_fp, bot, 0], color=GREY_C),
                        Line([x_pw, top + 0.3, 0], [x_pw, bot, 0], color=GREY_C))
        foot = VGroup(
            wrapped_label(rf"a fixed-horizon test needs {fx['n_per_arm']:,.0f} users per arm for a 10\% lift on "
                          rf"5\% \ (80\% power): \ the whole {pk['days']} days, \ looked at once", 12.6, font_size=19,
                          color=GREY_A),
            wrapped_label(r"the sequential test may be read every morning and stops early when the effect is "
                          r"large; \ it pays in power, \ and $\tau$ should match the effects you expect", 12.6,
                          font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "We ran the mixture test on the same traffic, checked daily. <bookmark mark='a'/> Daily z-tests had "
            f"{100 * pk['fpr_peeking'][-1]:.0f} percent false positives. <bookmark mark='b'/> The mixture test, its "
            f"spread tuned to five percent lifts, had {100 * sq['null']['rejected']:.1f} percent; tuned to ten "
            f"percent lifts, {100 * sq['null_tau']['rejected']:.1f}. Both under five. "
            "<bookmark mark='c'/> Now give the new version a real ten percent lift. Within thirty days the first "
            f"catches it {100 * sq['lift10']['rejected']:.0f} percent of the time, at a median of day "
            f"{sq['lift10']['median_day']:.0f}, and the second {100 * sq['lift10_tau']['rejected']:.0f} percent, by "
            f"day {sq['lift10_tau']['median_day']:.0f}. <bookmark mark='d'/> A fixed test with eighty percent power "
            "needs almost thirty thousand users per arm: the whole month, and one look. That is the trade: valid "
            "at every look, paid for in power."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads), Create(axes_l), Create(five), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(GrowFromEdge(fp_bars[0][0], LEFT), FadeIn(fp_bars[0][1]), FadeIn(pw_bars[0]),
                      FadeIn(names[1]), GrowFromEdge(fp_bars[1][0], LEFT), FadeIn(fp_bars[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(names[2]), FadeIn(names[3]), *[GrowFromEdge(fp_bars[k][0], LEFT) for k in (2, 3)],
                      *[FadeIn(fp_bars[k][1]) for k in (2, 3)])
            vo.wait_until("c")
            self.play(*[GrowFromEdge(pw_bars[k][0], LEFT) for k in (2, 3)], *[FadeIn(pw_bars[k][1]) for k in (2, 3)])
            vo.wait_until("d")
            self.play(GrowFromEdge(pw_bars[1][0], LEFT), FadeIn(pw_bars[1][1]), FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, HEAD, KERN)
