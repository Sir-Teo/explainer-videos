from __future__ import annotations

import numpy as np
from scipy import stats

from videos.psychology.psych12.common import *  # noqa: F403


def roc_axes(center, size: float = 4.6, xlabel=r"false-alarm rate", ylabel=r"hit rate"):
    return axes([0, 1], [0, 1], x_length=size, y_length=size, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=xlabel, ylabel=ylabel, center=center)


class Roc(VoiceoverScene):
    def construct(self):
        self.card()
        self.sweep()
        self.family()
        self.crossing()
        self.ratings()

    def card(self):
        card = chapter_card(3, r"The ROC", r"What does an observer look like across every possible line?",
                            lit={1954: r"the ROC"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover(
            "Chapter three. The ROC."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def sweep(self):
        head = heading(r"Slide the line, \ trace the curve")
        A = axes([-3.5, 5.0], [0, 0.45], x_length=6.4, y_length=2.6, xticks=[-2, 0, 2, 4], yticks=[],
                 xfmt=lambda v: f"{v:g}", xlabel=r"evidence", ylabel=r"", center=[-3.4, 0.9, 0])
        ax = A.ax
        g = gauss_pair(ax, 1.5)
        R = roc_axes([3.4, -0.1, 0])
        rx = R.ax
        k = ValueTracker(3.2)
        crit = always_redraw(lambda: DashedLine(ax.c2p(k.get_value(), 0), ax.c2p(k.get_value(), 0.44), color=CRIT,
                                                stroke_width=4))
        hit_area = always_redraw(lambda: area_under(ax, g.x, g.ys, k.get_value(), 5.0, HIT, 0.45))
        fa_area = always_redraw(lambda: area_under(ax, g.x, g.yn, k.get_value(), 5.0, FA, 0.55))

        def point():
            h, f = 1 - stats.norm.cdf(k.get_value() - 1.5), 1 - stats.norm.cdf(k.get_value())
            return Dot(rx.c2p(f, h), radius=0.09, color=CRIT)
        dot = always_redraw(point)
        trace = TracedPath(dot.get_center, stroke_color=ROCC, stroke_width=5)
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        dl = label(r"chance", font_size=22, color=GREY_C).move_to(rx.c2p(0.72, 0.6)).rotate(PI / 4)
        rows = rows_of([
            (r"strict line: \ few false alarms, \ few hits (bottom left)", WHITE),
            (r"lax line: \ many of both (top right)", WHITE),
            (r"every criterion is one point; \ together, \ the receiver operating characteristic", ROCC),
        ], 6.4, 26, 0.22).move_to([-3.4, -2.2, 0])
        tag = psyche_tag(r"computed: \ $d' = 1.5$")
        with self.voiceover(
            "Here's the most useful picture in the theory. On the left, the two distributions and the line. On "
            "the right, a square: false-alarm rate across, hit rate up. <bookmark mark='a'/> Start with a strict "
            "line, far to the right. Few false alarms and few hits: a point near the bottom left corner. "
            "<bookmark mark='b'/> Now slide the line left. Both rates rise, and the point climbs. "
            "<bookmark mark='c'/> A lax line, and both are high: top right. Every possible criterion gives one "
            "point, and together they trace a curve. The radar engineers called it the receiver operating "
            "characteristic, the ROC, and the name stuck. The dashed diagonal is an observer who sees nothing "
            "and says yes at random."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(g), FadeIn(R), Create(diag), FadeIn(dl))
            self.add(hit_area, fa_area, crit, dot, trace)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(k.animate.set_value(0.75), run_time=3.5, rate_func=linear)
            vo.wait_until("c")
            self.play(k.animate.set_value(-2.2), FadeIn(rows[1]), run_time=3.0, rate_func=linear)
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def family(self):
        d = load("roc")
        head = heading(r"Better eyes, \ a bowed curve")
        R = roc_axes([-2.8, -0.2, 0], size=5.0)
        rx = R.ax
        cols = [GREY_C, "#4f7a99", "#5d95bd", ROCC, "#a9dcf9", WHITE]
        curves = VGroup(*[curve(rx, d["fa_grid"], d["curves"][i], cols[i], stroke_width=4) for i in range(len(d["ds"]))])
        labs = VGroup(legend([(cols[i], rf"$d' = {d['ds'][i]:g}$") for i in range(len(d["ds"]))], font_size=21)
                      .move_to(rx.c2p(0.78, 0.27)))
        rows = rows_of([
            (r"$d' = 0$: \ the diagonal, \ guessing", GREY_A),
            (r"the larger $d'$, \ the more the curve bows toward the top left corner", ROCC),
            (rf"the area under it: \ {d['aucs'][3]:.3f} for $d' = 1.5$", MODEL),
            (rf"and that area is a probability: \ the chance of telling which of two trials had the signal, \ "
             rf"$\Phi(d'/\sqrt2) = {d['pc_15']:.3f}$", THRESH),
            (r"the area is the most used number in machine learning's evaluations: \ chapter 13", GREY_A),
        ], 5.6, 27, 0.26).move_to([3.7, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ six observers")
        with self.voiceover(
            "Now give Psyche better and better eyes. <bookmark mark='a'/> With d prime zero, the curve is the "
            "diagonal: no criterion helps an observer who can't tell signal from noise. "
            "<bookmark mark='b'/> As d prime grows, the curve bows up toward the top left corner, where hits are "
            "certain and false alarms never happen. <bookmark mark='c'/> One number summarizes a whole curve: the "
            f"area under it. For d prime one and a half it's {d['aucs'][3]:.2f}. <bookmark mark='d'/> And the area "
            "has a meaning. It's the chance that, given one signal trial and one blank, the observer's evidence "
            "is higher on the signal. That's exactly the score in a two-alternative forced choice, which is "
            "why Part 11 asked which interval was brighter. <bookmark mark='e'/> The same area, under the "
            "name AUC, is how most classifiers in machine learning are scored. We'll come back to that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(R))
            vo.wait_until("a")
            self.play(Create(curves[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in curves[1:]], lag_ratio=0.4), FadeIn(labs), FadeIn(rows[1]),
                      run_time=3.0)
            vo.wait_until("c")
            area = Polygon(*([rx.c2p(0, 0)] + [rx.c2p(float(a), float(b)) for a, b in zip(d["fa_grid"], d["curves"][3])] +
                             [rx.c2p(1, 0)]), stroke_width=0, fill_color=ROCC, fill_opacity=0.25)
            self.play(FadeIn(area), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def crossing(self):
        d = load("crossing")
        head = heading(r"Same area, \ different tests")
        R = roc_axes([-3.2, -0.2, 0], size=4.8)
        rx = R.ax
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        ca = curve(rx, d["fa"], d["hit_a"], ROCC, stroke_width=4)
        cb = curve(rx, d["fa"], d["hit_b"], SIGNALC, stroke_width=4)
        lg = legend([(ROCC, r"test A: \ equal spreads"), (SIGNALC, r"test B: \ signal twice as wide")], font_size=22
                    ).move_to(rx.c2p(0.66, 0.2))
        f2 = DashedLine(rx.c2p(0.02, 0), rx.c2p(0.02, 1), color=CRIT, stroke_width=2)
        a2, b2 = d["at_02"]
        pa = Dot(rx.c2p(0.02, a2), radius=0.08, color=ROCC)
        pb = Dot(rx.c2p(0.02, b2), radius=0.08, color=SIGNALC)
        rows = rows_of([
            (rf"both areas: \ {d['auc']:.3f}", WHITE),
            (rf"the curves cross near a false-alarm rate of {pct(d['cross_fa'])}", GREY_A),
            (rf"screening, \ where false alarms must stay at 2\%: \ B finds {pct(b2)} of targets, \ A {pct(a2)}", SIGNALC),
            (rf"at 30\% false alarms they are level: \ {pct(d['at_30'][0])} and {pct(d['at_30'][1])}", ROCC),
            (r"one number cannot rank two tests: \ look at the part of the curve where you will work", THRESH),
        ], 5.0, 26, 0.28).move_to([3.7, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ two binormal ROCs")
        with self.voiceover(
            "The area is a fine summary, until you have to choose between two tests. <bookmark mark='a'/> Here are "
            "two with exactly the same area. Test A has equal spreads. Test B's signal distribution is twice as "
            "wide: some targets are very obvious and some are buried. <bookmark mark='b'/> Their curves cross. "
            "<bookmark mark='c'/> In screening, where false alarms must be kept to two percent because so many "
            f"healthy people are tested, B finds {100 * b2:.0f} percent of the targets and A only {100 * a2:.0f}. "
            "<bookmark mark='d'/> Allow thirty percent false alarms and they're level. <bookmark mark='e'/> So one "
            "number can't rank two tests. Look at the part of the curve where you'll actually work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(R), Create(diag))
            vo.wait_until("a")
            self.play(Create(ca), Create(cb), FadeIn(lg), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(f2), FadeIn(pa), FadeIn(pb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def ratings(self):
        d = load("roc")
        head = heading(r"A whole curve from one experiment: \ confidence")
        names = [r"sure no", r"probably no", r"maybe no", r"maybe yes", r"probably yes", r"sure yes"]
        cs, cn = d["counts_signal"], d["counts_noise"]
        tbl = VGroup()
        for i, nm in enumerate(names):
            r = VGroup(label(nm, font_size=23, color=GREY_A), label(str(int(cs[i])), font_size=23, color=SIGNALC),
                       label(str(int(cn[i])), font_size=23, color=NOISEC))
            r[0].move_to([0, -0.42 * i, 0], aligned_edge=RIGHT)
            r[1].move_to([0.75, -0.42 * i, 0])
            r[2].move_to([1.65, -0.42 * i, 0])
            tbl.add(r)
        hd = VGroup(label(r"signal", font_size=21, color=SIGNALC).move_to([0.75, 0.45, 0]),
                    label(r"blank", font_size=21, color=NOISEC).move_to([1.65, 0.45, 0]))
        table = VGroup(hd, tbl).move_to([-4.3, 0.4, 0])
        R = roc_axes([0.4, -0.1, 0], size=4.4)
        rx = R.ax
        true = curve(rx, d["fa_grid"], d["curves"][3], ROCC, stroke_width=3)
        pts = VGroup(*[Dot(rx.c2p(float(f), float(h)), radius=0.08, color=YOU) for h, f in zip(d["hit"], d["fa"])])
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        rows = rows_of([
            (r"ask for a rating, \ not a yes or no", WHITE),
            (r"each boundary between ratings is a criterion: \ ``sure yes'' alone, \ then ``sure'' or ``probably'', "
             r"\ and so on", CRIT),
            (r"five boundaries, \ five points, \ one session", YOU),
            (r"they fall on the observer's curve (blue): \ confidence and payoffs move the same line", ROCC),
        ], 4.0, 25, 0.26).move_to([5.0, 0.0, 0])
        keep_in_frame(rows)
        tag = simulated_tag(r"simulated: \ 150 signal and 150 blank trials, \ the middle of 101 studies")
        with self.voiceover(
            "Tracing a curve with payoffs takes a session for every point. There's a faster way. "
            "<bookmark mark='a'/> Instead of yes or no, ask for a rating: sure no, probably no, maybe no, maybe "
            "yes, probably yes, sure yes. Here are the counts from one simulated session. "
            "<bookmark mark='b'/> Each boundary between ratings works as a criterion. Count only sure yes as a "
            "yes, and you get a strict point. Count sure or probably yes, and you get a laxer one. And so on. "
            "<bookmark mark='c'/> Five boundaries, five points, from one session. <bookmark mark='d'/> They fall "
            "on the same curve the payoffs would have traced. That agreement, ratings and payoffs moving one "
            "line, was among the early evidence that the theory describes something real."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(R), Create(diag))
            vo.wait_until("a")
            self.play(FadeIn(table), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts[::-1]], lag_ratio=0.3), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(Create(true), FadeIn(rows[3]))
        self.clear_scene()
