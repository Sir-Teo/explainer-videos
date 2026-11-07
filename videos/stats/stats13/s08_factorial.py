from __future__ import annotations

import numpy as np

from explainer.stats.kit.design import Bakery
from videos.stats.stats13.common import *  # noqa: F403

ORDER = [r"(1)", r"n", r"p", r"np", r"k", r"nk", r"pk", r"npk"]


def bakery_map(center, width=6.0, height=4.4, n=40, t_range=(160, 240), m_range=(10, 50)):
    """The bakery's hidden quality surface as a heat map (temperature across, time up) with axes."""
    A = axes(list(t_range), list(m_range), x_length=width, y_length=height, xlabel=r"oven temperature, \ $^\circ$C",
             ylabel=r"time, \ min", xticks=[160, 180, 200, 220, 240], yticks=[10, 20, 30, 40, 50], center=center)
    ax = A.ax
    ts = np.linspace(*t_range, n + 1)
    ms = np.linspace(*m_range, n + 1)
    cells = VGroup()
    for i in range(n):
        for j in range(n):
            q = Bakery.truth((ts[i] + ts[i + 1]) / 2, (ms[j] + ms[j + 1]) / 2)
            t = float(np.clip((q - 20) / 65, 0, 1))
            c = interpolate_color(ManimColor("#1B2733"), ManimColor(S.POST), t ** 1.5)
            p0, p1 = ax.c2p(ts[i], ms[j]), ax.c2p(ts[i + 1], ms[j + 1])
            cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=c, fill_opacity=1).move_to((p0 + p1) / 2))
    return A, ax, cells


class Factorial(VoiceoverScene):
    def construct(self):
        self.card()
        self.ofat()
        self.factorial_square()
        self.cube()
        self.effects()
        self.yates_alg()
        self.interaction()
        self.halfnormal()
        self.hidden_replication()

    def card(self):
        card = chapter_card(7, r"Factorials", r"Ask Nature several questions at once", lit=(1935,), part=PART)
        with self.voiceover("Chapter seven. Factorial experiments."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def ofat(self):
        d = load("factorial")["ofat"]
        A, ax, cells = bakery_map([-2.6, -0.1, 0])
        s0, s1, s2 = d["start"], d["after_temp"], d["after_time"]
        p0 = Dot(ax.c2p(*s0), radius=0.1, color=WHITE)
        sweep1 = Line(ax.c2p(160, s0[1]), ax.c2p(240, s0[1]), color=S.CTRL, stroke_width=3)
        p1 = Dot(ax.c2p(*s1), radius=0.1, color=S.CTRL)
        sweep2 = Line(ax.c2p(s1[0], 10), ax.c2p(s1[0], 50), color=S.TREAT, stroke_width=3)
        p2 = Dot(ax.c2p(*s2), radius=0.11, color=S.TREAT)
        best = Star(n=5, outer_radius=0.17, color=EXACT, fill_opacity=1).move_to(ax.c2p(205, 31))
        rows = fit_rows(VGroup(
            label(r"quality vs temperature and time", font_size=24),
            label(rf"start: \ 180$^\circ$C, \ 20 min: \ {d['q_start']:.0f}", font_size=24),
            label(rf"temperature alone: \ best {s1[0]:.0f}$^\circ$C", font_size=24, color=S.CTRL),
            label(rf"then time alone: \ {s2[1]:.1f} min: \ {d['quality']:.1f}", font_size=24, color=S.TREAT),
            label(rf"the real best: \ 205$^\circ$C, \ 31 min: \ {d['optimum']:.0f}", font_size=24, color=EXACT),
            label(r"a diagonal ridge: \ the knobs interact", font_size=24, color=OBS),
            label(r"one pass stops early; it does not estimate interaction", font_size=22, color=GREY_A),
        ), 5.2, 0.32, [3.9, 0.1, 0])
        tag = simulated_tag(r"the island bakery (hidden truth shown)", corner=DR)
        with self.voiceover(
            "First, why a single pass of one-factor-at-a-time optimization can fail. <bookmark mark='a'/> The island's bakery wants the best bread. "
            "Its quality depends on two knobs, oven temperature and baking time, through a surface it can't see; we'll show "
            "it, brightest where the bread is best. <bookmark mark='b'/> The baker starts at one eighty degrees and twenty "
            "minutes, and the bread is poor. <bookmark mark='c'/> Following the old aphorism, he varies one factor at a time. "
            "Holding time at twenty minutes, he tries temperatures from one sixty to two forty, and finds the best at two "
            "twenty-five. <bookmark mark='d'/> Then, holding that temperature, he varies the time: best at twenty-six and a "
            "half minutes, quality seventy-nine and a half. He stops, satisfied. <bookmark mark='e'/> The real best is at two "
            "oh five degrees and thirty-one minutes, quality eighty-five. <bookmark mark='f'/> The bright ridge runs diagonally: "
            "a hotter oven wants a shorter bake. The two knobs interact. <bookmark mark='g'/> Moving one knob at a time, "
            "along the grid lines, you can only crawl up a diagonal ridge, and you can easily stop too soon. Repeating coordinate searches can converge on this smooth surface, but this one pass did not."
        ) as vo:
            self.play(FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(p0, scale=2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(sweep1), run_time=1.5)
            self.play(FadeIn(p1, scale=2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(sweep2), run_time=1.5)
            self.play(FadeIn(p2, scale=2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(best, scale=2), FadeIn(rows[4]))
            for k, m_ in enumerate("fg"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 5]))
        self.clear_scene()

    def factorial_square(self):
        A, ax, cells = bakery_map([-2.6, -0.1, 0])
        pts = [(185, 22), (215, 22), (185, 34), (215, 34)]
        q = [Bakery.truth(t, m) for t, m in pts]
        dots = VGroup(*[Dot(ax.c2p(t, m), radius=0.11, color=WHITE) for t, m in pts])
        vals = VGroup(*[label(rf"{v:.0f}", font_size=22, color=WHITE).next_to(dd, UR, buff=0.05) for v, dd in zip(q, dots)])
        sq = Polygon(*[ax.c2p(*p) for p in (pts[0], pts[1], pts[3], pts[2])], color=GREY_A, stroke_width=2)
        temp_eff = (q[1] + q[3] - q[0] - q[2]) / 2
        time_eff = (q[2] + q[3] - q[0] - q[1]) / 2
        inter = (q[0] + q[3] - q[1] - q[2]) / 2
        rows = fit_rows(VGroup(
            label(r"change both knobs, \ in all combinations", font_size=24),
            label(r"a $2^2$ factorial: \ four corners", font_size=24),
            MathTex(rf"\text{{temperature effect}} = {temp_eff:.1f}", font_size=28, color=S.CTRL),
            MathTex(rf"\text{{time effect}} = {time_eff:.1f}", font_size=28, color=S.TREAT),
            MathTex(rf"\text{{interaction}} = {inter:.1f}", font_size=28, color=OBS),
            label(r"the best time depends on the temperature", font_size=22, color=OBS),
        ), 5.2, 0.34, [3.9, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The factorial alternative changes both knobs together, in every combination. <bookmark mark='b'/> "
            "Two levels of temperature, one eighty-five and two fifteen, crossed with two levels of time, twenty-two and "
            "thirty-four minutes: four bakes at the corners of a square. Here are the true qualities. <bookmark mark='c'/> The temperature "
            "effect is the average change from the cool side to the hot side: fourteen points. <bookmark mark='d'/> The time "
            "effect, nineteen. <bookmark mark='e'/> And the interaction: the hotter oven gains twenty-nine points on a short "
            "bake but nothing on a long one, and half that change, minus fifteen, is the interaction. <bookmark mark='f'/> A big interaction is the diagonal ridge, "
            "detected by four bakes. This baseline-and-one-change design cannot estimate the interaction, because it omits the corner where "
            "both knobs have moved."
        ) as vo:
            self.play(FadeIn(A), FadeIn(cells))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(sq), LaggedStart(*[FadeIn(d_, scale=2) for d_ in dots], lag_ratio=0.2), FadeIn(vals), FadeIn(rows[1]))
            for k, m_ in enumerate("cdef"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def cube_points(self, center):
        cx, cy = center
        ex, ey, ez = np.array([2.3, 0]), np.array([0, 2.1]), np.array([1.25, 0.85])

        def P(x):
            v = np.array([cx, cy]) + 0.5 * (x[0] * ex + x[1] * ey + x[2] * ez)
            return np.array([v[0], v[1], 0])
        return P

    def cube(self):
        d = load("factorial")
        X = np.asarray(d["X"])
        y = np.asarray(d["y"])
        P = self.cube_points((-3.4, -0.5))
        edges = VGroup()
        for i in range(8):
            for j in range(i + 1, 8):
                if np.sum(X[i] != X[j]) == 1:
                    edges.add(Line(P(X[i]), P(X[j]), color=GREY_C, stroke_width=2))
        dots = VGroup(*[Dot(P(x), radius=0.1, color=WHITE) for x in X])
        names = VGroup(*[label(ORDER[i], font_size=22, color=GREY_B).next_to(dots[i], LEFT, buff=0.1) for i in range(8)])
        vals = VGroup(*[label(rf"{v:.1f}", font_size=24, color=S.LIK).next_to(dots[i], RIGHT, buff=0.1) for i, v in enumerate(y)])
        for t in list(names) + list(vals):
            t.add_background_rectangle(color=BLACK, opacity=0.85, buff=0.04)
        axl = VGroup(label(r"N $\to$", font_size=22, color=S.TREAT).next_to(P([0, -1, -1]), DOWN, buff=0.35),
                     label(r"P $\uparrow$", font_size=22, color=S.ALT).next_to(P([-1, 0, -1]), LEFT, buff=0.35),
                     label(r"K $\nearrow$", font_size=22, color=S.PRIOR).next_to(P([1, -1, 0]), RIGHT, buff=0.2))
        rows = fit_rows(VGroup(
            label(r"N, \ P, \ K: \ each absent or present", font_size=24),
            label(r"a $2^3$ factorial: \ 8 corners, \ 2 plots each", font_size=24),
            label(r"a letter: \ that nutrient is present", font_size=22, color=GREY_A),
            label(r"truth: \ N 6, \ P 2, \ K 0.5, \ NP 2, \ rest 0", font_size=22, color=GREY_A),
        ), 4.6, 0.34, [4.5, 0.8, 0])
        tag = simulated_tag(r"simulated NPK trial, \ plot SD 1.5", corner=DR)
        with self.voiceover(
            "Now the classic agricultural case, with three factors. <bookmark mark='a'/> Nitrogen, phosphate and potash, each "
            "either withheld or applied. <bookmark mark='b'/> Every combination makes a two-to-the-three factorial: the eight "
            "corners of a cube. With two plots of each, sixteen plots. <bookmark mark='c'/> Frank Yates named each corner by "
            "the nutrients present: one in brackets for none, n for nitrogen alone, n p for both, up to n p k. "
            "<bookmark mark='d'/> In our simulation, the true averaged high-minus-low effects are six bushels for nitrogen, two for phosphate and half a bushel for potash; "
            "the NP interaction effect is two, half the four-bushel difference between the nitrogen effects at the two phosphate levels. Here are the average "
            "yields at each corner."
        ) as vo:
            self.play(Create(edges), FadeIn(axl), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d_, scale=2) for d_ in dots], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(names), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(vals), FadeIn(rows[3]))
        self.clear_scene()

    def effects(self):
        d = load("factorial")
        X = np.asarray(d["X"])
        y = np.asarray(d["y"])
        e = d["effects"]
        P = self.cube_points((-4.2, -0.8))
        edges = VGroup()
        for i in range(8):
            for j in range(i + 1, 8):
                if np.sum(X[i] != X[j]) == 1:
                    edges.add(Line(P(X[i]), P(X[j]), color=GREY_C, stroke_width=2))
        dots = VGroup(*[Dot(P(x), radius=0.1, color=WHITE) for x in X])
        hi = [i for i in range(8) if X[i][0] > 0]
        lo = [i for i in range(8) if X[i][0] < 0]
        face_hi = Polygon(*[P(X[i]) for i in (1, 3, 7, 5)], stroke_width=0, fill_color=S.TREAT, fill_opacity=0.25)
        face_lo = Polygon(*[P(X[i]) for i in (0, 2, 6, 4)], stroke_width=0, fill_color=S.CTRL, fill_opacity=0.25)
        diag = [i for i in range(8) if X[i][0] * X[i][1] > 0]
        rows = [
            cmath(r"\text{N}", r"=", rf"\bar y_{{\text{{N face}}}} - \bar y_{{\text{{no-N face}}}} = {np.mean(y[hi]):.2f} - {np.mean(y[lo]):.2f} = {e['N']:.2f}", font_size=28),
            cmath(r"\text{NP}", r"=", rf"\bar y_{{x_N x_P = +1}} - \bar y_{{x_N x_P = -1}} = {e['NP']:.2f}", font_size=28),
            cmath(r"\text{every effect}", r":", r"\text{all 16 plots, \ 8 against 8}", font_size=28),
            cmath(r"\mathrm{SE}", r"=", rf"2\sigma/\sqrt{{16}};\ \ \widehat{{\mathrm{{SE}}}} = {d['se']:.2f}", font_size=28),
        ]
        rows[2][2].set_color(OBS)
        whys = [why(r"a main effect: \ one face against the opposite face"), why(r"an interaction: \ the product column's sign"),
                why(r"no plot is wasted on any question"), why(r"from the two replicates")]
        for r in rows:
            r.scale(0.95)
        with self.voiceover(
            "Every effect is a contrast between two halves of the cube. <bookmark mark='a'/> The nitrogen effect: the average of "
            "the four corners with nitrogen, the front face, minus the average of the four without. Forty-three minus "
            "thirty-six point eight: six point two. <bookmark mark='b'/> An interaction uses the sign of a product: corners "
            "where nitrogen and phosphate are both present or both absent, against corners where exactly one is. The NP "
            "interaction is one point three four. <bookmark mark='c'/> Each of the seven effects uses all sixteen plots, eight "
            "against eight. Nothing is set aside to answer only one question. <bookmark mark='d'/> So each effect has the "
            "standard error of a difference between two means of eight plots, estimated from the replicates as point five "
            "three."
        ) as vo:
            self.play(Create(edges), FadeIn(dots))
            step = ladder(self, rows, whys, keep=4, top=2.9, x=2.0, buff=0.55, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
                if k == 0:
                    self.play(FadeIn(face_hi), FadeIn(face_lo))
                    self.play(*[dots[i].animate.set_color(S.TREAT) for i in hi], *[dots[i].animate.set_color(S.CTRL) for i in lo])
                if k == 1:
                    self.play(FadeOut(face_hi), FadeOut(face_lo),
                              *[dots[i].animate.set_color(OBS if i in diag else GREY_B) for i in range(8)])
        self.clear_scene()

    def yates_alg(self):
        d = load("factorial")
        y = np.asarray(d["y"])
        cols = [y]
        c = y.copy()
        for _ in range(3):
            c = np.concatenate([c[0::2] + c[1::2], c[1::2] - c[0::2]])
            cols.append(c)
        names = [r"", r"N", r"P", r"NP", r"K", r"NK", r"PK", r"NPK"]
        x0 = [-5.6, -3.6, -1.6, 0.4, 2.4, 4.6]
        head = VGroup(*[label(t, font_size=22, color=GREY_B).move_to([x, 2.9, 0]) for t, x in
                        zip([r"run", r"$y$", r"pass 1", r"pass 2", r"pass 3", r"$\div 4$"], x0)])
        grid = VGroup()
        for i in range(8):
            row = VGroup(label(ORDER[i], font_size=22, color=GREY_B).move_to([x0[0], 2.3 - i * 0.6, 0]))
            for k in range(4):
                row.add(label(rf"{cols[k][i]:.1f}", font_size=22, color=S.LIK if k == 0 else (OBS if k == 3 else WHITE)).move_to([x0[k + 1], 2.3 - i * 0.6, 0]))
            eff = rf"{names[i]} \ {cols[3][i] / 4:.2f}" if i else rf"mean \ {cols[3][0] / 8:.2f}"
            row.add(label(eff, font_size=22, color=OBS if i else GREY_A).move_to([x0[5], 2.3 - i * 0.6, 0]))
            grid.add(row)
        foot = label(r"each pass: \ sums of pairs on top, \ differences of pairs below", font_size=22, color=GREY_A).move_to([0, -2.9, 0])
        with self.voiceover(
            "Frank Yates, Fisher's successor at Rothamsted, gave a way to compute all the effects by hand. <bookmark mark='a'/> "
            "Write the eight yields in standard order. <bookmark mark='b'/> In each pass, write the sums of consecutive pairs, "
            "then their differences: second minus first. <bookmark mark='c'/> Do it again on the new column. "
            "<bookmark mark='d'/> And a third time, one pass per factor. <bookmark mark='e'/> The top of the last column is "
            "the grand total; every other entry, divided by four, is an effect, in standard order: N, P, NP, K, NK, PK and "
            "NPK. Nitrogen six point two, phosphate three point oh, their interaction one point three; the rest are small. "
            "Yates published it in 1937, in The Design and Analysis of Factorial Experiments. It's the Walsh-Hadamard transform "
            "for the group of the cube's corners, later familiar in fast transform algorithms."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(*[FadeIn(VGroup(r[0], r[1])) for r in grid])
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(r[k + 2], shift=RIGHT * 0.2) for r in grid], lag_ratio=0.08))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(r[5], shift=RIGHT * 0.2) for r in grid], lag_ratio=0.08), FadeIn(foot))
        self.clear_scene()

    def interaction(self):
        d = load("factorial")
        X = np.asarray(d["X"])
        y = np.asarray(d["y"])
        A = axes([-1.4, 1.4], [34, 47], x_length=5.6, y_length=4.4, xlabel=r"nitrogen", ylabel=r"mean yield", xticks=[], yticks=[36, 40, 44],
                 center=[-2.8, 0.0, 0])
        ax = A.ax
        lines, dots = VGroup(), VGroup()
        for pv, col in ((-1, S.CTRL), (1, S.ALT)):
            m = [y[(X[:, 0] == nv) & (X[:, 1] == pv)].mean() for nv in (-1, 1)]
            lines.add(Line(ax.c2p(-1, m[0]), ax.c2p(1, m[1]), color=col, stroke_width=4))
            dots.add(Dot(ax.c2p(-1, m[0]), color=col, radius=0.09), Dot(ax.c2p(1, m[1]), color=col, radius=0.09))
        lab = VGroup(label(r"without P", font_size=22, color=S.CTRL).next_to(lines[0].get_end(), RIGHT, buff=0.15),
                     label(r"with P", font_size=22, color=S.ALT).next_to(lines[1].get_end(), RIGHT, buff=0.15))
        ticks = VGroup(label(r"none", font_size=20, color=GREY_B).move_to(ax.c2p(-1, 34) + DOWN * 0.3),
                       label(r"applied", font_size=20, color=GREY_B).move_to(ax.c2p(1, 34) + DOWN * 0.3))
        rows = fit_rows(VGroup(
            label(r"N's effect, \ without and with P", font_size=24),
            label(r"parallel lines: \ no interaction", font_size=24),
            label(r"diverging: \ N is worth more with P", font_size=24, color=OBS),
            label(r"N's main effect is an average", font_size=24),
            label(r"so report each level's effect", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.4, 0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Interactions are best seen in a plot: the mean yield without and with nitrogen, one line for "
            "the plots without phosphate, one for the plots with it. <bookmark mark='b'/> If the two nutrients acted "
            "separately, the lines would be parallel. <bookmark mark='c'/> They diverge: nitrogen is worth more when phosphate "
            "is present, because a crop short of phosphate can't use all the nitrogen it's given. <bookmark mark='d'/> So the "
            "main effect of nitrogen, six point two, is an average over the two phosphate levels. <bookmark mark='e'/> When "
            "the interaction is large, that average can mislead, and the honest report gives the effect of each factor at each "
            "level of the other."
        ) as vo:
            self.play(FadeIn(A), FadeIn(ticks))
            vo.wait_until("a")
            self.play(Create(lines), FadeIn(dots), FadeIn(lab), FadeIn(rows[0]))
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 1]))
        self.clear_scene()

    def halfnormal(self):
        d = load("factorial")
        h = d["halfnorm"]
        A = axes([0, 2.0], [0, 7], x_length=6.0, y_length=4.4, xlabel=r"half-normal quantile", ylabel=r"$|\text{effect}|$",
                 xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 2, 4, 6], center=[-2.8, 0.0, 0])
        ax = A.ax
        dots, labs = VGroup(), VGroup()
        for q, a, nm in zip(h["q"], h["abs"], h["names"]):
            big = nm in ("N", "P")
            dd = Dot(ax.c2p(q, a), radius=0.09, color=OBS if big else GREY_B)
            dots.add(dd)
            if nm in ("N", "P", "NP"):
                labs.add(label(nm, font_size=22, color=OBS if big else GREY_B).next_to(dd, UL, buff=0.08))
        labs.add(label(r"K, \ NK, \ PK, \ NPK", font_size=20, color=GREY_B).move_to(ax.c2p(0.45, 1.3)))
        small = np.array(h["abs"][:5]) / np.array(h["q"][:5])
        slope = float(np.median(small))
        ln = DashedLine(ax.c2p(0, 0), ax.c2p(2.0, 2.0 * slope), color=GREY_C)
        rows = fit_rows(VGroup(
            label(r"Daniel (1959): \ sorted $|$effects$|$", font_size=24),
            label(r"pure noise: \ a line through 0", font_size=24),
            label(r"N and P stand off it: \ evidence of activity", font_size=24, color=OBS),
            label(r"NP: \ 1.34 vs SE 0.53, \ borderline", font_size=24),
            label(r"the tool for unreplicated designs", font_size=22, color=GREY_A),
        ), 4.6, 0.36, [4.4, 0.1, 0])
        with self.voiceover(
            "How do you judge seven effects at once? <bookmark mark='a'/> Cuthbert Daniel's 1959 idea: sort the absolute "
            "effects and plot them against the quantiles of a half-normal distribution. <bookmark mark='b'/> If no effect were "
            "real, all seven would be noise, and the points would lie roughly on a straight line through zero. "
            "<bookmark mark='c'/> Nitrogen and phosphate stand far off the line: evidence of active effects, rather than a calibrated multiple-testing guarantee. <bookmark mark='d'/> The NP "
            "interaction is borderline here, one point three four against a standard error of point five three, about two and "
            "a half standard errors: real in truth, but just at the edge of what sixteen plots can see. <bookmark mark='e'/> "
            "In industrial experiments, which often have no replicates, Daniel's plot is a useful screening plot, relying on effect sparsity rather than guaranteeing that every marked effect is real."
        ) as vo:
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd, scale=1.5) for dd in dots], lag_ratio=0.15), FadeIn(labs), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(rows[1]))
            for k, m_ in enumerate("cde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k + 2]))
        self.clear_scene()

    def hidden_replication(self):
        rows = [
            cmath(r"\text{OFAT, \ 16 plots}", r":", r"\text{4 settings} \times 4\ \text{plots};\ \ \mathrm{SE} = \sigma\sqrt{2/4} = 0.71\sigma", font_size=28),
            cmath(r"2^3\text{ factorial, \ 16 plots}", r":", r"\mathrm{SE} = \sigma\sqrt{2/8} = 0.50\sigma", font_size=28),
            cmath(r"\text{efficiency}", r":", r"\text{twice the plots for these simple contrasts; estimands differ}", font_size=28),
            cmath(r"\text{and}", r":", r"\text{only the factorial sees the interactions}", font_size=28),
        ]
        rows[1][2].set_color(OBS)
        whys = [why(r"baseline + one change per factor"), why(r"every plot used for every effect"),
                why(r"Fisher's ``hidden replication''"), why(r"and its conclusions hold over a range of conditions")]
        with self.voiceover(
            "So the factorial wins twice. <bookmark mark='a'/> With sixteen plots, one factor at a time would use four "
            "settings, the baseline plus one change per factor, four plots each. Each effect is a difference of two means of "
            "four: standard error point seven one sigma. <bookmark mark='b'/> The factorial compares eight plots with eight "
            "for every effect: point five oh sigma. <bookmark mark='c'/> Under an additive mean model these target the same effects, and the one-factor design needs twice the "
            "plots. Fisher called this hidden replication: every plot replicates every comparison. <bookmark mark='d'/> And "
            "only the factorial measures interactions. Fisher added a third advantage: because each effect is averaged over "
            "the other factors' levels, its reported main effects average over the tested factor combinations; interactions still require reporting simple effects. That's the questionnaire."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.0, buff=0.65, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
