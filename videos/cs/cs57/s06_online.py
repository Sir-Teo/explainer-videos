from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey, as one left-aligned column."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def curve_axes(xr, yr, xl, yl, xticks, yticks, x_length=5.2, y_length=3.4, fx=lambda v: f"{v:g}",
               fy=lambda v: f"{v:g}"):
    ax = CornerAxes(x_range=xr, y_range=yr, x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
    xt = VGroup(*[label(fx(v), font_size=16, color=GREY_B).next_to(ax.c2p(v, yr[0]), DOWN, buff=0.1)
                  for v in xticks])
    yt = VGroup(*[label(fy(v), font_size=16, color=GREY_B).next_to(ax.c2p(xr[0], v), LEFT, buff=0.1)
                  for v in yticks])
    lx = label(xl, font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.4)
    ly = label(yl, font_size=17, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
    return VGroup(ax, xt, yt, lx, ly), ax


def polyline(ax, xs, ys, color, width=2.5):
    return VMobject(color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, v) for x, v in zip(xs, ys)])


def fit_x(g, lo=-6.85, hi=6.85):
    if g.get_right()[0] > hi:
        g.shift(LEFT * (g.get_right()[0] - hi))
    if g.get_left()[0] < lo:
        g.shift(RIGHT * (lo - g.get_left()[0]))
    return g


class Online(VoiceoverScene):
    def construct(self):
        self.card()
        self.halving()
        self.weighted()
        self.hedge_proof()
        self.regret_curves()
        self.lower()
        self.ogd()

    def card(self):
        card = chapter_card(5, r"Learning online", r"What if an adversary picks the examples?",
                            lit=(1988, 1997), extra=((1988, r"Littlestone: \ mistake bounds"),
                                                     (1997, r"Freund and Schapire: \ Hedge")), part=PART)
        with self.voiceover("Chapter five. Learning online."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the halving algorithm
    def halving(self):
        h = load("halving")
        N, mist, alive = h["N"], h["mistakes"], h["alive"]
        lgN = int(round(h["bound"]))
        T = len(alive)
        head = label(r"Counting mistakes: \ the halving algorithm", font_size=36).to_edge(UP, buff=0.3)
        fs = 26
        rows = [
            MathTex(r"|V_0| = N", r",\qquad", r"\text{a mistake} \Rightarrow |V| \text{ at least halves}",
                    font_size=fs),
            MathTex(r"1 \le |V_M| \le N\, 2^{-M}", font_size=fs),
            MathTex(r"M \le \log_2 N", font_size=fs),
            MathTex(r"M \le \log_2 N", r"=", rf"\log_2 {N} = {lgN}", font_size=fs),
        ]
        rows[3][2].set_color(YES)
        whys = [
            label(r"$V$: \ the hypotheses still consistent; \ predict with their majority", font_size=17,
                  color=GREY_B),
            label(r"the true hypothesis is never thrown away", font_size=17, color=GREY_B),
            label(r"take logarithms", font_size=17, color=GREY_B),
            label(rf"${N}$ thresholds on a line", font_size=17, color=GREY_B),
        ]
        col = stacked(rows[:3], whys[:3], buff=0.16).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.45)
        rows[3].move_to(rows[2], aligned_edge=LEFT)
        whys[3].move_to(whys[2], aligned_edge=LEFT)
        # the adversary's binary search: the survivors halve on every forced mistake
        W0 = 5.4
        bars = VGroup()
        off = 0.0
        for k in range(lgN + 1):
            w = W0 / 2 ** k
            r = Rectangle(width=max(0.03, w), height=0.16, stroke_width=0, fill_color=NO if k else DATA,
                          fill_opacity=0.85)
            r.move_to([off + w / 2, -0.24 * k, 0])
            t = label(rf"{N >> k}", font_size=16, color=GREY_B).next_to(r, RIGHT, buff=0.1)
            bars.add(VGroup(r, t))
            if k % 2 == 1:
                off += w / 2
        bars.next_to(col, DOWN, buff=0.35).to_edge(LEFT, buff=0.55)
        bcap = wrapped_label(r"an adversary asks about the middle of $V$ and answers against the majority: \ "
                             rf"{lgN} forced mistakes", 6.0, font_size=18, color=NO).next_to(bars, DOWN, buff=0.15)
        bcap.align_to(bars, LEFT)
        # the measured run, on random examples
        g, ax = curve_axes([0, T, 50], [0, lgN, 5], r"round $t$", r"survivors $|V|$, \ random examples",
                           [0, 100, 200], [0, 5, 10], x_length=4.6, y_length=2.9, fy=lambda v: rf"$2^{{{v:g}}}$")
        g.move_to([3.9, 0.75, 0])
        xs = [0] + list(range(1, T + 1))
        ys = [math.log2(N)] + [math.log2(a) for a in alive]
        stair = VMobject(color=DATA, stroke_width=3)
        pts = [ax.c2p(xs[0], ys[0])]
        prev = ys[0]
        for x, yv in zip(xs[1:], ys[1:]):
            pts += [ax.c2p(x, prev), ax.c2p(x, yv)]
            prev = yv
        stair.set_points_as_corners(pts)
        bl = DashedLine(ax.c2p(0, lgN), ax.c2p(T, lgN), color=HEAD, stroke_width=1.5)
        mlab = wrapped_label(rf"{mist} mistakes in {T} random rounds; \ {alive[-1]} thresholds still alive", 5.0,
                             font_size=18, color=DATA).next_to(g, DOWN, buff=0.2).align_to(g, LEFT)
        lit = wrapped_label(r"Littlestone \ (1988): \ the best mistake bound of a class is its \textbf{Littlestone "
                            r"dimension}; \ thresholds on the whole line: \ infinite, \ though their VC dimension "
                            r"is 1", 5.4, font_size=18, color=LAM).next_to(mlab, DOWN, buff=0.3).align_to(g, LEFT)
        fit_x(VGroup(g, mlab, lit))
        with self.voiceover(
            "Now drop the distribution. An adversary picks each example, we predict its label, then see the truth, "
            "and we count mistakes. <bookmark mark='a'/> Suppose one of N hypotheses is perfect. The halving "
            "algorithm keeps those still consistent and predicts with their majority. A mistake means the majority "
            "was wrong, so at least half are thrown away, <bookmark mark='b'/> and the true one never is. "
            "<bookmark mark='c'/> So there are at most log two of N mistakes: for a thousand and twenty-four "
            "thresholds, ten. <bookmark mark='d'/> On random examples it made two in two hundred rounds. "
            "<bookmark mark='e'/> An adversary who asks about the middle of the survivors forces all ten. "
            "<bookmark mark='f'/> Nick Littlestone showed in 1988 that the best mistake bound of a class is one "
            "number, its Littlestone dimension. For thresholds on the whole line it is infinite, though their VC "
            "dimension is one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            self.play(TransformMatchingTex(rows[2], rows[3]), FadeOut(whys[2]), FadeIn(whys[3]))
            vo.wait_until("d")
            self.play(FadeIn(g), Create(bl))
            self.play(Create(stair), run_time=2)
            self.play(FadeIn(mlab))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in bars], lag_ratio=0.25), run_time=2.5)
            self.play(FadeIn(bcap))
            vo.wait_until("f")
            self.play(FadeIn(lit))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ weighted majority
    def weighted(self):
        head = label(r"Weighted majority: \ halve the wrong", font_size=36).to_edge(UP, buff=0.3)
        n, R = 8, 6
        rng = np.random.default_rng(3)
        truth = rng.integers(0, 2, R)
        err = np.array([0.15, 0.5, 0.35, 0.5, 0.6, 0.45, 0.5, 0.4])
        P = np.where(rng.random((R, n)) < err, 1 - truth[:, None], truth[:, None])
        P[:, 0] = truth
        P[2, 0] = 1 - truth[2]
        y0, dy, x_name, x_bar = 2.1, 0.5, -6.4, -5.6
        names = VGroup(*[label(rf"$e_{i + 1}$", font_size=20, color=GREY_A).move_to([x_name, y0 - i * dy, 0])
                         for i in range(n)])

        def bars(w):
            return VGroup(*[Rectangle(width=max(0.02, 2.2 * w[i]), height=0.26, stroke_width=0, fill_color=LAM,
                                      fill_opacity=0.85).move_to([x_bar + 1.1 * w[i], y0 - i * dy, 0])
                            for i in range(n)])
        w = np.ones(n)
        bar = bars(w)
        cx = -2.6
        vote_cells = VGroup(*[Square(side_length=0.34, stroke_width=1.2, stroke_color=GREY_C).move_to(
            [cx, y0 - i * dy, 0]) for i in range(n)])
        vl = label(r"vote", font_size=17, color=GREY_B).next_to(vote_cells, UP, buff=0.1)
        wl = label(r"weight", font_size=17, color=GREY_B).move_to([x_bar + 1.1, y0 + 0.45, 0])
        out = VGroup(label(r"weighted vote", font_size=17, color=GREY_B), label(r"truth", font_size=17,
                                                                                color=GREY_B))
        out.arrange(RIGHT, buff=0.5).next_to(VGroup(names, vote_cells), DOWN, buff=0.35).align_to(names, LEFT)
        ill = note(r"illustrative: \ 8 experts, \ 6 rounds", font_size=16).next_to(out, DOWN, buff=0.65).align_to(
            names, LEFT)
        fs = 26
        rows = [
            MathTex(r"W = \sum_i w_i", r",\qquad", r"W_0 = N", font_size=fs),
            MathTex(r"\text{mistake} \Rightarrow W", r"\le", r"\tfrac12 W + \tfrac12\cdot\tfrac12 W", r"=",
                    r"\tfrac34 W", font_size=fs),
            MathTex(r"2^{-m}", r"\le", r"W_{\text{end}}", r"\le", r"N\, (\tfrac34)^{M}", font_size=fs),
            MathTex(r"M", r"\le", r"\frac{m + \log_2 N}{\log_2 (4/3)}", r"\approx", r"2.41\,(m + \log_2 N)",
                    font_size=fs),
        ]
        rows[3][4].set_color(YES)
        whys = [
            label(r"every expert starts at weight 1; \ wrong experts are halved", font_size=17, color=GREY_B),
            label(r"we erred: \ at least half the weight voted wrong, \ and that half is halved", font_size=17,
                  color=GREY_B),
            label(r"the best expert, \ with $m$ mistakes, \ keeps weight $2^{-m}$", font_size=17, color=GREY_B),
            label(r"take $\log_2$; \ Littlestone and Warmuth \ (1994)", font_size=17, color=YES),
        ]
        col = stacked(rows, whys, buff=0.25).move_to([3.5, 0.0, 0])
        fit_x(col)
        with self.voiceover(
            "Usually no expert is perfect. <bookmark mark='a'/> Littlestone and Manfred Warmuth's weighted majority, "
            "published in 1994, starts every expert at weight one, predicts with the weighted vote, and halves every "
            "expert that is wrong. <bookmark mark='b'/> If the algorithm errs, at least half the weight voted wrong "
            "and is halved, so the total falls to three quarters at most. <bookmark mark='c'/> The best expert, with "
            "m mistakes, still holds a half to the m. <bookmark mark='d'/> Take logarithms: at most about two point "
            "four times the best expert's mistakes, plus log two of N. No deterministic rule can do much better, "
            "since an adversary can make it wrong every round. So we randomize."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), FadeIn(bar), FadeIn(vote_cells), FadeIn(vl), FadeIn(wl),
                      FadeIn(out), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            res = VGroup()
            for t in range(R):
                ps = VGroup(*[mono(str(P[t, i]), size=18, color=WHITE).move_to(vote_cells[i]) for i in range(n)])
                v1 = float(w[P[t] == 1].sum())
                pred = int(v1 >= w.sum() / 2)
                o = VGroup(mono(str(pred), size=20, color=HEAD).next_to(out[0], DOWN, buff=0.1),
                           mono(str(truth[t]), size=20, color=WHITE).next_to(out[1], DOWN, buff=0.1))
                self.play(FadeIn(ps), FadeIn(o) if not len(res) else Transform(res, o), run_time=0.45)
                if not len(res):
                    res = o
                wrong = [i for i in range(n) if P[t, i] != truth[t]]
                self.play(*[ps[i].animate.set_color(NO) for i in wrong],
                          res[0].animate.set_color(YES if pred == truth[t] else NO), run_time=0.35)
                w = w.copy()
                w[wrong] *= 0.5
                self.play(Transform(bar, bars(w)), FadeOut(ps), run_time=0.5)
                if t == 1:
                    vo.wait_until("b")
                    self.play(FadeIn(col[1]))
            vo.wait_until("c")
            self.play(FadeIn(col[2]))
            vo.wait_until("d")
            self.play(FadeIn(col[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Hedge, proved
    def hedge_proof(self):
        hd = load("hedge")
        N, T = hd["N"], hd["T"]
        head = label(r"Hedge: \ regret $\sqrt{T \ln N / 2}$, \ proved", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"p_t(i) = \frac{w_t(i)}{W_t}", r",\qquad", r"w_{t+1}(i) = w_t(i)\, e^{-\eta\, \ell_t(i)}",
                    r",\qquad", r"\ell_t(i) \in [0, 1]", font_size=28),
            MathTex(r"\mathrm{Regret}_T = \sum_t p_t \cdot \ell_t \; - \; \min_i L_i", r",\qquad",
                    r"L_i = \sum_t \ell_t(i)", font_size=28),
        ).arrange(DOWN, buff=0.18).next_to(head, DOWN, buff=0.3)
        fs = 25
        Lw = r"\ln\frac{W_{T+1}}{W_1}"
        rows = [
            MathTex(Lw, r"\ge", r"-\eta L_i - \ln N", font_size=fs),
            MathTex(r"\ln\frac{W_{t+1}}{W_t}", r"=", r"\ln \sum_i p_t(i)\, e^{-\eta \ell_t(i)}", r"\le",
                    r"-\eta\, p_t\cdot \ell_t + \frac{\eta^2}{8}", font_size=fs),
            MathTex(Lw, r"\le", r"-\eta \sum_t p_t\cdot\ell_t + \frac{\eta^2 T}{8}", font_size=fs),
            MathTex(r"\sum_t p_t\cdot\ell_t - L_i", r"\le", r"\frac{\ln N}{\eta} + \frac{\eta T}{8}", font_size=fs),
            MathTex(r"\sum_t p_t\cdot\ell_t - L_i", r"\le", r"\sqrt{\tfrac12 T \ln N}", font_size=fs + 2),
        ]
        rows[4][2].set_color(YES)
        whys = [
            label(r"$W_{T+1} \ge w_{T+1}(i) = e^{-\eta L_i}$, \ and $W_1 = N$", font_size=17, color=GREY_B),
            label(r"Hoeffding's lemma, \ for a variable in $[0, 1]$", font_size=17, color=GREY_B),
            label(r"add up the $T$ rounds: \ the logs telescope", font_size=17, color=GREY_B),
            label(r"put the two bounds together, \ divide by $\eta$", font_size=17, color=GREY_B),
            label(rf"$\eta = \sqrt{{8 \ln N / T}}$; \ for $N = {N}$, \ $T = {T}$: \ "
                  rf"{math.sqrt(T * math.log(N) / 2):.1f}", font_size=17, color=YES),
        ]
        left = stacked(rows[:2], whys[:2], buff=0.3)
        right = stacked(rows[2:4], whys[2:4], buff=0.3)
        body = VGroup(left, right).arrange(RIGHT, buff=0.6, aligned_edge=UP).next_to(defs, DOWN, buff=0.45)
        fit_x(body)
        rows[4].move_to(rows[3], aligned_edge=LEFT)
        whys[4].move_to(whys[3], aligned_edge=LEFT)
        lab_lo = label(r"from below", font_size=18, color=DATA).next_to(left, UP, buff=0.12).align_to(left, LEFT)
        lab_hi = label(r"from above", font_size=18, color=KERN).next_to(right, UP, buff=0.12).align_to(right, LEFT)
        foot = wrapped_label(r"regret per round, \ $\sqrt{\ln N / (2T)}$, \ goes to zero: \ the same multiplicative "
                             r"weights as Part 23 and as boosting's re-weighting", 12.0, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Freund and Schapire's Hedge, from 1997, plays expert i with probability proportional to its weight, and "
            "multiplies each weight by e to the minus eta times that expert's loss. Regret is its expected loss minus"
            " the best expert's. Watch the log of the total weight. <bookmark mark='a'/> From below: the total is at "
            "least the best expert's weight. <bookmark mark='b'/> From above: each round, by Hoeffding's lemma, the "
            "log falls by eta times our expected loss, give or take eta squared over eight. <bookmark mark='c'/> Add "
            "up the rounds, <bookmark mark='d'/> put the two together, <bookmark mark='e'/> and choose eta as the "
            "root of eight log N over T: the regret is at most the root of T log N over two. <bookmark mark='f'/> Per"
            " round it goes to zero. It is Part 23's multiplicative weights again."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defs))
            vo.wait_until("a")
            self.play(FadeIn(lab_lo), Write(left[0][0]), FadeIn(left[0][1]))
            vo.wait_until("b")
            self.play(Write(left[1][0]), FadeIn(left[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(lab_hi), Write(right[0][0]), FadeIn(right[0][1]))
            vo.wait_until("d")
            self.play(Write(right[1][0]), FadeIn(right[1][1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[3], rows[4]), FadeOut(whys[3]), FadeIn(whys[4]))
            self.play(Circumscribe(rows[4], color=YES))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ measured regret
    def regret_curves(self):
        hd = load("hedge")
        N, T = hd["N"], hd["T"]
        reg, ftl = hd["regret"], hd["follow_the_leader"]
        step = T // len(reg)
        xs = [1 + step * i for i in range(len(reg))]
        eta = math.sqrt(8 * math.log(N) / T)
        g0 = math.log(N) / eta
        head = label(r"Regret, \ measured", font_size=36).to_edge(UP, buff=0.3)
        g, ax = curve_axes([0, T, 500], [0, 60, 20], r"round $t$", rf"regret against the best of {N} experts",
                           [0, 1000, 2000], [0, 20, 40, 60], x_length=6.0, y_length=3.9)
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        guar = DashedLine(ax.c2p(0, g0), ax.c2p(T, g0 + eta * T / 8), color=HEAD, stroke_width=2.5)
        gl = label(r"guarantee: \ $\ln N/\eta + \eta t/8$", font_size=19, color=HEAD).move_to(
            ax.c2p(T * 0.3, 50))
        c_h = polyline(ax, xs, reg, DATA, width=3)
        c_f = polyline(ax, xs, ftl, LAM, width=3)
        lh = label(rf"Hedge: \ {reg[-1]:.1f}", font_size=18, color=DATA).next_to(ax.c2p(T, reg[-1]), DOWN,
                                                                                buff=0.12).shift(LEFT * 0.7)
        lf = label(rf"follow the leader: \ {ftl[-1]:.1f}", font_size=18, color=LAM).next_to(ax.c2p(T, ftl[-1]), UP,
                                                                                          buff=0.1).shift(LEFT * 1.1)
        ge = label(rf"{g0 + eta * T / 8:.1f}", font_size=18, color=HEAD).next_to(ax.c2p(T, g0 + eta * T / 8), RIGHT,
                                                                                buff=0.1)
        cap = note(rf"{N} experts, \ random losses, \ one slightly better; \ $\eta = {eta:.3f}$; \ every 10th round",
                   font_size=16).next_to(g, DOWN, buff=0.12).align_to(g, LEFT)
        # follow the leader against an adversary (illustrative)
        A = [0.5] + [0, 1] * 5
        B = [0] + [1, 0] * 5
        cA = cB = cF = 0.0
        trows = []
        for t in range(6):
            pick = "A" if cA <= cB else "B"
            lossF = A[t] if pick == "A" else B[t]
            cA, cB, cF = cA + A[t], cB + B[t], cF + lossF
            trows.append([f"{t + 1}", f"{A[t]:g}", f"{B[t]:g}", pick, f"{lossF:g}"])
        tab = grid_table([r"$t$", r"A", r"B", r"leader", r"its loss"], trows, widths=[0.5, 0.6, 0.6, 0.9, 0.9],
                         row_h=0.36, font_size=18, mono_cols=())
        for r in range(1, 7):
            tab.cells[r][4].set_color(NO)
        tt = label(r"follow the leader, \ adversarial losses", font_size=19, color=NO)
        tsum = wrapped_label(rf"after 6 rounds: \ A {cA:g}, \ B {cB:g}, \ the leader {cF:g}; \ after $T$ rounds "
                             r"about $T/2$ against $T$: \ regret grows linearly", 3.9, font_size=18, color=GREY_A)
        tl = note(r"illustrative", font_size=16)
        right = VGroup(tt, tab, tsum, tl).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.6, -0.2, 0])
        fit_x(right)
        with self.voiceover(
            "Hedge against twenty experts with random losses for two thousand rounds, one slightly better than the "
            "rest. <bookmark mark='a'/> The dashed line is the guarantee for this eta, reaching fifty-four point "
            "seven. <bookmark mark='b'/> The measured regret climbs while Hedge finds the best expert, then flattens "
            "at thirty point seven. <bookmark mark='c'/> On losses this random, following the leader does even "
            "better: nine. <bookmark mark='d'/> But an adversary can ruin it: two experts whose losses alternate, so "
            "the leader is always the one about to lose. Follow the leader loses almost every round, each expert half"
            " of them, and its regret grows linearly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(guar), FadeIn(gl), FadeIn(ge))
            vo.wait_until("b")
            self.play(Create(c_h), run_time=2.5)
            self.play(FadeIn(lh))
            vo.wait_until("c")
            self.play(Create(c_f), FadeIn(lf), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(tt), *[FadeIn(c) for c in tab.cells[0]], FadeIn(tab.rule))
            for r in range(1, 7):
                self.play(*[FadeIn(c) for c in tab.cells[r]], run_time=0.35)
            self.play(FadeIn(tsum), FadeIn(tl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the lower bound
    def lower(self):
        head = label(r"Nobody beats $\sqrt{T}$", font_size=36).to_edge(UP, buff=0.3)
        T, K = 400, 10
        rng = np.random.default_rng(11)
        g, ax = curve_axes([0, T, 100], [-30, 30, 10], r"round $t$", r"$L_1(t) - t/2$: \ expert 1's loss above "
                           r"half", [0, 200, 400], [-20, 0, 20], x_length=4.8, y_length=4.0)
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        walks = VGroup()
        for k in range(K):
            b = rng.integers(0, 2, T)
            d = np.concatenate([[0], np.cumsum(b - 0.5)])
            walks.add(polyline(ax, range(T + 1), d, interpolate_color(ManimColor(DATA), ManimColor(LAM), k / (K - 1)), width=1.6))
        env = VGroup(*[ax.plot(lambda t, s=s: s * math.sqrt(t) / 2, x_range=[0, T], color=HEAD, stroke_width=2)
                       for s in (1, -1)])
        envl = label(r"$\pm\sqrt{t}/2$: \ one standard deviation", font_size=17, color=HEAD).move_to(
            ax.c2p(T, 27), aligned_edge=RIGHT)
        ill = note(rf"illustrative: \ {K} runs of fair coins", font_size=16).next_to(g, DOWN, buff=0.12).align_to(
            g, LEFT)
        fs = 24
        rows = [
            MathTex(r"\ell_t = (b_t,\ 1 - b_t)", r",\qquad", r"b_t \text{ a fair coin}", font_size=fs),
            MathTex(r"\mathbb E[L_{\text{alg}}] = T/2", font_size=fs),
            MathTex(r"\min(L_1, L_2) = T/2 - \big|L_1 - T/2\big|", font_size=fs),
            MathTex(r"\mathbb E[\mathrm{Regret}]", r"=", r"\mathbb E\big|L_1 - T/2\big|", r"\approx",
                    r"\sqrt{T / 2\pi}", r"\approx", r"0.4\sqrt{T}", font_size=fs),
        ]
        rows[3][6].set_color(YES)
        whys = [
            label(r"two experts; \ each round exactly one of them loses", font_size=17, color=GREY_B),
            label(r"whatever we play, \ each round costs $\tfrac12$ on average", font_size=17, color=GREY_B),
            label(r"$L_1 + L_2 = T$", font_size=17, color=GREY_B),
            label(r"$L_1$ is binomial, \ standard deviation $\sqrt{T}/2$", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.25).next_to(g, RIGHT, buff=0.6).align_to(g, UP)
        fit_x(col)
        more = wrapped_label(r"with $N$ experts the same idea gives $\sqrt{\tfrac12 T \ln N}$ as $T$ and $N$ grow: "
                             r"\ Hedge's constant cannot be improved \ (Cesa-Bianchi et al. \ 1997)",
                             col.width, font_size=18, color=LAM).next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "Could a cleverer algorithm beat root T? No. <bookmark mark='a'/> Take two experts and flip a fair coin "
            "each round to decide which one loses. <bookmark mark='b'/> Whatever we play, we lose a half per round on"
            " average: T over two. <bookmark mark='c'/> But the luckier expert loses T over two minus the distance "
            "expert one's count has wandered. <bookmark mark='d'/> That is a random walk; here are ten. Its average "
            "distance is about the root of T over two pi, so every algorithm suffers regret of about point four root "
            "T. <bookmark mark='e'/> With N experts the same idea gives Hedge's own root of T log N over two: its "
            "constant cannot be improved."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(wk) for wk in walks], lag_ratio=0.15), run_time=3)
            self.play(Create(env), FadeIn(envl))
            self.play(Write(col[3][0]), FadeIn(col[3][1]))
            vo.wait_until("e")
            self.play(FadeIn(more))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ online gradient descent
    def ogd(self):
        head = label(r"Online gradient descent, \ and back to batch", font_size=36).to_edge(UP, buff=0.3)
        R = 12
        rng = np.random.default_rng(5)
        z = np.clip(0.62 + 0.18 * rng.standard_normal(R), 0.05, 0.95)
        g, ax = curve_axes([0, 1, 0.5], [0, 1, 0.25], r"the point $w$ we play", r"this round's loss "
                           r"$f_t(w) = (w - z_t)^2$", [0, 0.5, 1], [0, 0.5, 1], x_length=5.4, y_length=3.4)
        g.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        eta = 0.3
        ws = [0.1]
        for t in range(R):
            ws.append(ws[-1] - eta * 2 * (ws[-1] - z[t]))
        best = DashedLine(ax.c2p(float(z.mean()), 0), ax.c2p(float(z.mean()), 1), color=YES, stroke_width=2)
        bestl = label(r"best fixed $w$ in hindsight", font_size=16, color=YES).next_to(ax.c2p(float(z.mean()), 0.9),
                                                                                    RIGHT, buff=0.1)
        ill = note(r"illustrative: \ 12 rounds, \ step $\eta = 0.3$", font_size=16).next_to(g, DOWN, buff=0.12)
        ill.align_to(g, LEFT)
        fs = 25
        rows = [
            MathTex(r"w_{t+1} = \Pi_K\big(w_t - \eta\, \nabla f_t(w_t)\big)", font_size=fs),
            MathTex(r"\mathrm{Regret}_T", r"\le", r"\frac{D^2}{2\eta} + \frac{\eta G^2 T}{2}", font_size=fs),
            MathTex(r"\mathrm{Regret}_T", r"\le", r"D\,G\,\sqrt{T}", font_size=fs),
            MathTex(r"\mathbb E\, R(\bar w) - R(w^*)", r"\le", r"\frac{\mathbb E\,\mathrm{Regret}_T}{T}", r"\le",
                    r"\frac{D\,G}{\sqrt{T}}", font_size=fs),
        ]
        rows[2][2].set_color(YES)
        rows[3][4].set_color(YES)
        whys = [
            label(r"step against the gradient, \ project back into the set $K$", font_size=17, color=GREY_B),
            label(r"$D$: \ the diameter of $K$; \ $G$: \ a bound on the gradients", font_size=17, color=GREY_B),
            label(r"$\eta = D / (G\sqrt{T})$: \ Zinkevich \ (2003)", font_size=17, color=YES),
            label(r"i.i.d.\ examples, \ $\bar w$ the average iterate, \ convexity", font_size=17, color=GREY_B),
        ]
        col = stacked([rows[0], rows[1], rows[3]], [whys[0], whys[1], whys[3]], buff=0.55)
        col.next_to(g, RIGHT, buff=0.7).align_to(g, UP).shift(DOWN * 0.1)
        fit_x(col)
        rows[2].move_to(rows[1], aligned_edge=LEFT)
        whys[2].move_to(whys[1], aligned_edge=LEFT)
        ol = label(r"online-to-batch", font_size=18, color=KERN).next_to(rows[3], UP, buff=0.12).align_to(rows[3],
                                                                                                       LEFT)
        foot = wrapped_label(r"a regret bound is a generalization bound: \ the online game is the harder one",
                             12.0, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The experts are one case of a larger game. <bookmark mark='a'/> Each round we choose a point, then the "
            "adversary reveals a convex loss. Martin Zinkevich showed in 2003 that Part 23's gradient descent works "
            "here: step against this round's gradient, and project back into the allowed set. <bookmark mark='b'/> "
            "Here the losses are parabolas whose centres jump about, and our point chases them. <bookmark mark='c'/> "
            "With D the set's diameter and G a bound on the gradients, the regret is at most D squared over two eta "
            "plus eta G squared T over two; <bookmark mark='d'/> with the best eta, D G root T. <bookmark mark='e'/> "
            "And online turns into batch: feed a training set in one example at a time and average the points played."
            " By convexity the average's expected risk exceeds the best by at most the regret over T."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            dot = Dot(ax.c2p(ws[0], 0), radius=0.09, color=HEAD)
            par = ax.plot(lambda w: (w - z[0]) ** 2, x_range=[0, 1], color=DATA, stroke_width=2.5)
            self.play(FadeIn(dot), Create(par), run_time=0.6)
            for t in range(R):
                newp = ax.plot(lambda w, c=z[t]: (w - c) ** 2, x_range=[0, 1], color=DATA, stroke_width=2.5)
                self.play(Transform(par, newp), run_time=0.3)
                self.play(dot.animate.move_to(ax.c2p(ws[t + 1], 0)), run_time=0.35)
            self.play(Create(best), FadeIn(bestl))
            vo.wait_until("c")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1], rows[2]), FadeOut(whys[1]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(FadeIn(ol), Write(col[2][0]), FadeIn(col[2][1]))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
