from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey, as one left-aligned column."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def fit_x(g, lo=-6.85, hi=6.85):
    if g.get_right()[0] > hi:
        g.shift(LEFT * (g.get_right()[0] - hi))
    if g.get_left()[0] < lo:
        g.shift(RIGHT * (lo - g.get_left()[0]))
    return g


def log_axes(x_max, y_lo, y_hi, x_length, y_length, xticks):
    """Axes with x = parameters p and y = log10 of an error; tick labels written as powers of ten."""
    ax = CornerAxes(x_range=[0, x_max, 50], y_range=[y_lo, y_hi, 1], x_length=x_length, y_length=y_length,
                    tips=False, axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
    xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, y_lo), DOWN, buff=0.1)
                  for v in xticks])
    yt = VGroup(*[label(rf"$10^{{{v}}}$", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                  for v in range(y_lo, y_hi + 1)])
    return VGroup(ax, xt, yt), ax


def theory(p, n, D, noise):
    """Expected test error of the minimum-norm fit on the first p of D isotropic Gaussian features, for a target
    with squared norm 1 spread evenly: the unseen features act as extra noise (Wishart means; see the scene)."""
    rest = (D - p) / D
    s2 = noise ** 2 + rest
    if p < n - 1:
        return rest + s2 * p / (n - p - 1)
    if p > n + 1:
        return (D - n) / D + s2 * n / (p - n - 1)
    return float("inf")


class Overparam(VoiceoverScene):
    def construct(self):
        self.card()
        self.fit()
        self.random()
        self.minnorm()
        self.implicit()
        self.peak()

    def card(self):
        card = chapter_card(8, r"More parameters than data", r"Why does a model that can fit noise generalize?",
                            lit=(2017, 2019), extra=((2017, r"Zhang et al.: \ random labels"),
                                                     (2019, r"Belkin et al.: \ double descent")), part=PART)
        with self.voiceover("Chapter eight. More parameters than data."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the measured curves
    def fit(self):
        d = load("descent")
        n, D, rows = d["n"], d["D"], d["rows"]
        head = label(r"Fitting perfectly, \ and still predicting", font_size=36).to_edge(UP, buff=0.3)
        g, ax = log_axes(D, -2, 2, 8.6, 4.7, [0, 50, 100, 150, 200])
        g.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=1.0)
        xl = label(rf"parameters $p$ \ (examples: \ $n = {n}$)", font_size=18, color=GREY_A).next_to(ax, DOWN,
                                                                                              buff=0.45)
        floor = 0.01

        def y(v):
            return math.log10(max(v, floor))
        te_l = [r for r in rows if r["p"] <= n]
        te_r = [r for r in rows if r["p"] >= n]
        c_l = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(r["p"], y(r["test"])) for r in te_l])
        c_r = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(r["p"], y(r["test"])) for r in te_r])
        tr = VMobject(color=DATA, stroke_width=3).set_points_as_corners([ax.c2p(r["p"], y(r["train"])) for r in rows])
        dots = VGroup(*[Dot(ax.c2p(r["p"], y(r["test"])), radius=0.05, color=NO if r["p"] < n else YES)
                        for r in rows])
        tdots = VGroup(*[Dot(ax.c2p(r["p"], y(r["train"])), radius=0.05, color=DATA) for r in rows])
        thr = DashedLine(ax.c2p(n, -2), ax.c2p(n, 2), color=HEAD, stroke_width=1.5)
        zero = min(r["train"] for r in rows if r["p"] >= n)
        big = max(r["train"] for r in rows if r["p"] >= n)
        e = math.floor(math.log10(big))
        trl = wrapped_label(rf"training error: \ from $p = {n}$ on, \ below $10^{{{e + 1}}}$, \ zero up to "
                            r"rounding \ (Part 4)", 3.4, font_size=17, color=DATA).next_to(ax.c2p(n + 75, -2), UP,
                                                                                           buff=0.15)
        r0, rp, rb = rows[0], next(r for r in rows if r["p"] == n), rows[-1]
        nums = VGroup(
            label(rf"{r0['test']:.2f}", font_size=17, color=NO).next_to(ax.c2p(r0["p"], y(r0["test"])), UP, buff=0.1),
            label(rf"{rp['test']:.1f}", font_size=17, color=HEAD).next_to(ax.c2p(n, y(rp["test"])), RIGHT, buff=0.12),
            label(rf"{rb['test']:.2f}", font_size=17, color=YES).next_to(ax.c2p(rb["p"], y(rb["test"])), UP,
                                                                         buff=0.1),
        )
        tl = label(r"test error", font_size=18, color=GREY_A).next_to(ax.c2p(110, y(1.45)), UP, buff=0.15)
        under = label(r"$p < n$: \ classical", font_size=18, color=NO).next_to(ax.c2p(n / 2, 2), DOWN, buff=0.1)
        over = label(r"$p > n$: \ interpolating", font_size=18, color=YES).next_to(ax.c2p(n + 75, 2), DOWN, buff=0.1)
        cap = note(rf"minimum-norm least squares on the first $p$ of $D = {D}$ Gaussian features; \ noise "
                   rf"{d['noise']:g}; \ median of 50 trials", font_size=16).to_edge(DOWN, buff=0.25)
        _ = zero
        with self.voiceover(
            "Here is the experiment of the hook again, with both errors. Fifty noisy examples; a linear "
            "model on the first p of two hundred Gaussian features, fitted by least squares, choosing the "
            "smallest solution when there are many. <bookmark mark='a'/> The training error falls as p grows, "
            "and from p equal to fifty on it is zero, up to the rounding of Part 4's floating point: the model "
            "interpolates, noise and all. <bookmark mark='b'/> The test error rises to fifty-two at the "
            "threshold, <bookmark mark='c'/> then falls, to point seven eight at two hundred parameters, "
            "below the one point oh three of the smallest model. Mikhail Belkin, Daniel Hsu, Siyuan Ma and "
            "Soumik Mandal named this double descent in 2019. In this simple setting there is no first valley at "
            "all: a classical textbook would have stopped at the smallest model, and missed the better one beyond."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(xl), FadeIn(cap), Create(thr), FadeIn(under), FadeIn(over))
            vo.wait_until("a")
            self.play(Create(tr), FadeIn(tdots), run_time=2)
            self.play(FadeIn(trl))
            vo.wait_until("b")
            self.play(Create(c_l), FadeIn(dots[:len(te_l) - 1]), FadeIn(tl), run_time=2)
            self.play(FadeIn(nums[0]), FadeIn(nums[1]))
            vo.wait_until("c")
            self.play(Create(c_r), FadeIn(dots[len(te_l) - 1:]), run_time=2)
            self.play(FadeIn(nums[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ random labels
    def random(self):
        head = label(r"A model that can fit noise", font_size=36).to_edge(UP, buff=0.3)
        m = 12
        rng = np.random.default_rng(6)
        xs = np.linspace(-2.6, 2.6, m)
        frame = Rectangle(width=6.0, height=3.6, stroke_color=GREY_D, stroke_width=1.5).next_to(head, DOWN, buff=0.6)
        frame.to_edge(LEFT, buff=0.6)
        cx, cy = frame.get_center()[0], frame.get_center()[1]
        base = DashedLine([cx - 2.9, cy, 0], [cx + 2.9, cy, 0], color=GREY_D, stroke_width=1)

        def labelling(sig):
            pts = [np.array([cx + x, cy + 0.85 * s, 0]) for x, s in zip(xs, sig)]
            dots = VGroup(*[Dot(p, radius=0.08, color=YES if s > 0 else NO) for p, s in zip(pts, sig)])
            curve = VMobject(color=HEAD, stroke_width=2.5)
            curve.set_points_smoothly([np.array([cx - 2.9, cy, 0])] + pts + [np.array([cx + 2.9, cy, 0])])
            return VGroup(curve, dots)
        sigs = [rng.choice([-1, 1], m) for _ in range(4)]
        cur = labelling(sigs[0])
        fl = label(r"random labels $\sigma_i = \pm 1$, \ refitted each time", font_size=17, color=GREY_A).next_to(
            frame, DOWN, buff=0.12).align_to(frame, LEFT)
        ill = note(r"illustrative", font_size=16).next_to(fl, DOWN, buff=0.08).align_to(frame, LEFT)
        fs = 25
        rows = [
            MathTex(r"\hat{\mathfrak R}_S(\mathcal H)", r"=", r"\mathbb E_\sigma\Big[\sup_{h\in\mathcal H}\ "
                    r"\frac1m\sum_i \sigma_i\, h(x_i)\Big]", font_size=fs),
            MathTex(r"\hat{\mathfrak R}_S(\mathcal H)", r"=", r"1", font_size=fs),
            MathTex(r"L_D(h)", r"\le", r"L_S(h) + 2\cdot\tfrac12\, \hat{\mathfrak R}_S(\mathcal H) + \cdots", r"=",
                    r"0 + 1 + \cdots", font_size=fs),
        ]
        rows[2][4].set_color(NO)
        whys = [
            label(r"chapter 3: \ how well the class correlates with pure noise", font_size=17, color=GREY_B),
            label(r"if some $h$ fits every labelling, \ each sum is exactly $m$", font_size=17, color=GREY_B),
            label(r"the 0--1 loss halves it: \ a bound above 1 on an error below 1 says nothing",
                  font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.3).next_to(frame, RIGHT, buff=0.5).align_to(frame, UP)
        fit_x(col)
        zh = wrapped_label(r"Zhang, \ Bengio, \ Hardt, \ Recht and Vinyals \ (2017): \ standard image networks fit "
                           r"CIFAR-10 with \textit{random} labels to zero training error, \ with test accuracy at "
                           r"chance; \ on the true labels the same networks generalize well", 12.2, font_size=20,
                           color=WHITE).to_edge(DOWN, buff=0.45)
        so = label(r"so the explanation is not the class: \ it is \textit{which} interpolant the algorithm picks",
                   font_size=20, color=HEAD).next_to(zh, UP, buff=0.3)
        with self.voiceover(
            "Why is this a puzzle? <bookmark mark='a'/> Chapter three measured a class by how well it fits "
            "pure noise: random signs, and the best correlation the class can achieve with them. "
            "<bookmark mark='b'/> A model with at least as many parameters as examples fits any labelling at "
            "all, so that complexity takes its largest value, one. <bookmark mark='c'/> And the bound becomes "
            "useless: test error at most the training error, zero, plus one, plus more. <bookmark mark='d'/> "
            "Chiyuan Zhang and colleagues showed in 2017 that real networks are like this. Standard image "
            "networks fitted CIFAR-10 with random labels to zero training error, and then of course predicted "
            "at chance; on the true labels the same networks generalize well. <bookmark mark='e'/> So the "
            "answer is not in the class. It is in which interpolating solution the algorithm picks."
        ) as vo:
            self.play(FadeIn(head), Create(frame), Create(base), FadeIn(cur), FadeIn(fl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            for sg in sigs[1:]:
                self.play(Transform(cur, labelling(sg)), run_time=0.8)
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(FadeIn(zh))
            vo.wait_until("e")
            self.play(FadeIn(so))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the min-norm interpolator
    def plane(self):
        """The plane of two parameters, one equation x . beta = y: its line of solutions, and the row space."""
        ax = NumberPlane(x_range=[-1.5, 2.5, 1], y_range=[-1.5, 2.5, 1], x_length=4.6, y_length=4.6,
                         background_line_style={"stroke_color": GREY_E, "stroke_width": 1},
                         axis_config={"stroke_color": GREY_C, "stroke_width": 1.5})
        x = np.array([2.0, 1.0])
        yv = 2.0
        bh = x * yv / (x @ x)
        dirn = np.array([-x[1], x[0]]) / np.linalg.norm(x)
        return ax, x, yv, bh, dirn

    def minnorm(self):
        head = label(r"The smallest interpolator", font_size=36).to_edge(UP, buff=0.3)
        ax, x, yv, bh, dirn = self.plane()
        ax.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        line = Line(ax.c2p(-0.25, 2.5), ax.c2p(1.75, -1.5), color=DATA, stroke_width=3)
        names = VGroup(label(r"$\beta_1$", font_size=20, color=GREY_B).next_to(ax.c2p(2.5, 0), DOWN, buff=0.1),
                       label(r"$\beta_2$", font_size=20, color=GREY_B).next_to(ax.c2p(0, 2.5), LEFT, buff=0.1))
        ll = label(r"all $\beta$ with $2\beta_1 + \beta_2 = 2$", font_size=17, color=DATA).next_to(
            ax.c2p(*(bh + 1.5 * dirn)), LEFT, buff=0.1)
        o = ax.c2p(0, 0)
        unit = np.linalg.norm(ax.c2p(1, 0) - o)
        r_hat = float(np.linalg.norm(bh))
        circ = Circle(radius=0.2 * unit, color=HEAD, stroke_width=2.5).move_to(o)
        circ_end = Circle(radius=r_hat * unit, color=HEAD, stroke_width=2.5).move_to(o)
        pt = Dot(ax.c2p(*bh), radius=0.09, color=YES)
        ptl = label(r"$\hat\beta$", font_size=22, color=YES).next_to(pt, UR, buff=0.05)
        row = DashedLine(ax.c2p(*(-0.7 * x)), ax.c2p(*(1.2 * x)), color=LAM, stroke_width=2.5)
        rl = label(r"multiples of $x$: \ the row space", font_size=17, color=LAM).move_to(ax.c2p(0.2, -1.2))
        ill = note(r"one example, \ two parameters: \ illustrative", font_size=16).next_to(ax, DOWN, buff=0.12)
        fs = 26
        rows = [
            MathTex(r"p > n:", r"\quad", r"\{\beta : X\beta = y\}", r"=", r"\hat\beta + \mathrm{null}(X)",
                    font_size=fs),
            MathTex(r"\hat\beta = \arg\min_{X\beta = y} \|\beta\|", r"\ \Rightarrow\ ", r"\hat\beta = X^\top\lambda",
                    font_size=fs),
            MathTex(r"X X^\top \lambda = y", r"\ \Rightarrow\ ", r"\hat\beta = X^\top (X X^\top)^{-1} y", r"=",
                    r"X^+ y", font_size=fs),
        ]
        rows[2][4].set_color(YES)
        whys = [
            label(r"$n$ equations, \ $p$ unknowns: \ a flat of solutions, \ $p - n$ dimensional", font_size=17,
                  color=GREY_B),
            label(r"Lagrange: \ at the minimum the gradient $2\beta$ is a combination of the rows", font_size=17,
                  color=GREY_B),
            label(r"the pseudo-inverse: \ what our experiment computes", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.35).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP).shift(DOWN * 0.2)
        fit_x(col)
        with self.voiceover(
            "Past the threshold there are more unknowns than equations. <bookmark mark='a'/> Draw the "
            "smallest case: one example, two parameters. Every point on this line fits the example exactly; in"
            " general the solutions form a flat of dimension p minus n. <bookmark mark='b'/> Our experiment "
            "picks the one of smallest length. Grow a circle from the origin until it touches the line. "
            "<bookmark mark='c'/> It touches where the radius is perpendicular to the line, that is, along the"
            " example itself. In general the minimum-norm solution is a combination of the rows of X. "
            "<bookmark mark='d'/> Substitute that into the equations and solve: X transpose, times the inverse "
            "of X X transpose, times y. This is the pseudo-inverse, and the one in our experiment."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(names), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(ll), Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Create(circ))
            self.play(Transform(circ, circ_end), run_time=2)
            self.play(FadeIn(pt), FadeIn(ptl))
            vo.wait_until("c")
            self.play(Create(row), FadeIn(rl), Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ gradient descent's implicit bias
    def implicit(self):
        head = label(r"Gradient descent chooses it for us", font_size=36).to_edge(UP, buff=0.3)
        ax, x, yv, bh, dirn = self.plane()
        ax.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        line = Line(ax.c2p(-0.25, 2.5), ax.c2p(1.75, -1.5), color=DATA, stroke_width=3)
        pt = Dot(ax.c2p(*bh), radius=0.09, color=YES)
        ptl = label(r"$\hat\beta$", font_size=22, color=YES).next_to(pt, UR, buff=0.05)

        def path(b0, eta=0.08, steps=14):
            bs = [np.array(b0, float)]
            for _ in range(steps):
                bs.append(bs[-1] - eta * x * (x @ bs[-1] - yv))
            return bs
        p0 = path([0, 0])
        p1 = path([-1.1, 0.8])
        d0 = Dot(ax.c2p(*p0[0]), radius=0.08, color=HEAD)
        d1 = Dot(ax.c2p(*p1[0]), radius=0.08, color=KERN)
        tr0 = VMobject(color=HEAD, stroke_width=2.5).set_points_as_corners([ax.c2p(*b) for b in p0])
        tr1 = VMobject(color=KERN, stroke_width=2.5).set_points_as_corners([ax.c2p(*b) for b in p1])
        l0 = label(r"from $0$", font_size=17, color=HEAD).next_to(d0, DL, buff=0.05)
        l1 = label(r"from elsewhere", font_size=17, color=KERN).next_to(d1, DOWN, buff=0.1)
        ill = note(r"illustrative", font_size=16).next_to(ax, DOWN, buff=0.12)
        fs = 26
        rows = [
            MathTex(r"\beta_{t+1} = \beta_t - \eta\, X^\top (X\beta_t - y)", font_size=fs),
            MathTex(r"\beta_0 = 0", r"\ \Rightarrow\ ", r"\beta_t \in \mathrm{row}(X)\ \text{ for every } t",
                    font_size=fs),
            MathTex(r"X\beta_\infty = y,\ \ \beta_\infty \in \mathrm{row}(X)", r"\ \Rightarrow\ ",
                    r"\beta_\infty = \hat\beta", font_size=fs),
        ]
        rows[2][2].set_color(YES)
        whys = [
            label(r"gradient descent on the squared error \ (Part 23; \ \textit{AI, Built} 11)", font_size=17,
                  color=GREY_B),
            label(r"every step adds a combination of the rows", font_size=17, color=GREY_B),
            label(r"one interpolant lies in the row space: \ the smallest", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.35).next_to(ax, RIGHT, buff=0.6).align_to(ax, UP).shift(DOWN * 0.2)
        fit_x(col)
        more = wrapped_label(r"nobody asked for the smallest norm: \ the algorithm supplied it, \ an "
                             r"\textbf{implicit bias} \ (\textit{AI, Built} 8); \ for the logistic loss on separable "
                             r"data, \ gradient descent heads for the maximum-margin direction \ (Soudry et al. \ "
                             r"2018), \ chapter 3's margins again", col.width, font_size=18, color=LAM).next_to(
            col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "Nobody trains a network by calling the pseudo-inverse. But they do run gradient descent. "
            "<bookmark mark='a'/> On the squared error, each step subtracts X transpose times the residual: a "
            "combination of the rows. <bookmark mark='b'/> Start at zero, and you never leave the row space. "
            "<bookmark mark='c'/> Watch: the yellow path runs straight along the example's direction and stops"
            " on the line at the smallest solution. <bookmark mark='d'/> Started elsewhere, it lands somewhere"
            " else on the line. So from zero, the limit fits the data and lies in the row space, and only one "
            "solution does both. <bookmark mark='e'/> The algorithm chose the smallest norm by itself: an "
            "implicit bias. For the logistic loss on separable data, gradient descent heads for the maximum "
            "margin, chapter three's margins again."
        ) as vo:
            self.play(FadeIn(head), Create(ax), Create(line), FadeIn(pt), FadeIn(ptl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(FadeIn(d0), FadeIn(l0))
            self.play(Create(tr0), MoveAlongPath(d0, tr0.copy()), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(d1), FadeIn(l1))
            self.play(Create(tr1), MoveAlongPath(d1, tr1.copy()), run_time=2.5)
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            vo.wait_until("e")
            self.play(FadeIn(more))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ why the peak
    def peak(self):
        d = load("descent")
        n, D, noise, rows = d["n"], d["D"], d["noise"], d["rows"]
        head = label(r"Why the peak, \ and why the second descent", font_size=36).to_edge(UP, buff=0.3)
        g, ax = log_axes(D, -1, 2, 5.6, 3.6, [0, 50, 100, 150, 200])
        g.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.9)
        xl = label(r"parameters $p$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.4)
        meas = VGroup(*[Dot(ax.c2p(r["p"], math.log10(r["test"])), radius=0.055, color=WHITE) for r in rows])
        left_ps = [p for p in range(3, n - 2)]
        right_ps = [p for p in range(n + 3, D + 1)]
        th_l = VMobject(color=NO, stroke_width=2.5).set_points_smoothly(
            [ax.c2p(p, math.log10(min(100, theory(p, n, D, noise)))) for p in left_ps])
        th_r = VMobject(color=YES, stroke_width=2.5).set_points_smoothly(
            [ax.c2p(p, math.log10(min(100, theory(p, n, D, noise)))) for p in right_ps])
        pole = DashedLine(ax.c2p(n, -1), ax.c2p(n, 2), color=HEAD, stroke_width=1.5)
        leg = VGroup(label(r"dots: \ measured test error \ (median)", font_size=17, color=WHITE),
                     label(r"lines: \ the formula, \ expected value, \ $\|\beta\|^2 = 1$", font_size=17,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        leg.next_to(xl, DOWN, buff=0.15).align_to(g, LEFT)
        fs = 25
        E = r"\mathbb E\,\|X^+\tilde\varepsilon\|^2"
        rows_ = [
            MathTex(r"\hat\beta - \beta_p", r"=", r"X^+ \tilde\varepsilon\ +\ \text{bias}", font_size=fs),
            MathTex(E, r"=", r"\tilde\sigma^2\, \mathbb E\operatorname{tr}(X^\top X)^{-1}", font_size=fs),
            MathTex(E, r"=", r"\tilde\sigma^2\, \mathbb E\operatorname{tr}(X X^\top)^{-1}", font_size=fs),
        ]
        done = [MathTex(E, r"=", r"\tilde\sigma^2\,\frac{p}{n - p - 1}", font_size=fs),
                MathTex(E, r"=", r"\tilde\sigma^2\,\frac{n}{p - n - 1}", font_size=fs)]
        done[0][2].set_color(NO)
        done[1][2].set_color(YES)
        whys = [
            label(r"$\tilde\varepsilon$: \ the noise \ ($\sigma = " + f"{noise:g}" + rf"$) \ plus the ${D} - p$ "
                  r"features the model cannot see", font_size=17, color=GREY_B),
            label(r"$p < n$: \ the mean of an inverse Wishart matrix, \ which blows up as $p \to n$", font_size=17,
                  color=GREY_B),
            label(r"$p > n$: \ the same, \ transposed: \ $p - n$ spare directions share the noise", font_size=17,
                  color=GREY_B),
        ]
        col = stacked(rows_, whys, buff=0.3).next_to(g, RIGHT, buff=0.45).align_to(g, UP)
        fit_x(col)
        for k in (0, 1):
            done[k].move_to(rows_[k + 1], aligned_edge=LEFT)
        foot = wrapped_label(r"at $p = n$ the matrix $X$ is square and nearly singular: \ its smallest singular "
                             r"value is near zero, \ and Part 52's condition number amplifies the noise", col.width,
                             font_size=18, color=HEAD).next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "Why does the error explode at the threshold, and fall after it? <bookmark mark='a'/> The fitted "
            "parameters miss the true ones by a bias and by the pseudo-inverse applied to the noise, where the "
            "noise includes the features the model cannot see. <bookmark mark='b'/> With fewer parameters than"
            " examples, the noise term's average is the noise variance times p over n minus p minus one: the mean of "
            "an inverse Wishart matrix. <bookmark mark='c'/> With more, the same argument transposed gives n "
            "over p minus n minus one. <bookmark mark='d'/> Both blow up as p approaches n, where X is square "
            "and its smallest singular value is near zero: Part 52's ill-conditioning. <bookmark mark='e'/> "
            "The formula's curves, drawn for a target of norm one, follow our measurements on both sides of the "
            "peak. Past it, the spare directions share the noise, and the smallest solution damps it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(xl), Create(pole))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            self.play(TransformMatchingTex(rows_[1], done[0]))
            vo.wait_until("c")
            self.play(Write(col[2][0]), FadeIn(col[2][1]))
            self.play(TransformMatchingTex(rows_[2], done[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
            vo.wait_until("e")
            self.play(FadeIn(meas), FadeIn(leg))
            self.play(Create(th_l), Create(th_r), run_time=2)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
