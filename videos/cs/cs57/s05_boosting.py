from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.07, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def best_stump(X, y, w):
    """The decision stump AdaBoost picks under weights w (the instrument's search: every other threshold)."""
    best = (2.0, None)
    for j in range(2):
        for th in np.unique(X[:, j])[::2]:
            for s in (1.0, -1.0):
                e = float(w[np.where(X[:, j] >= th, s, -s) != y].sum())
                if e < best[0]:
                    best = (e, (j, float(th), s))
    return best


class Ring:
    """The ring problem drawn in a square: points sized by their weight, a stump as a line."""

    def __init__(self, X, y, side=4.4, center=ORIGIN):
        self.X, self.y, self.side = X, y, side
        self.frame = Square(side_length=side, stroke_color=GREY_C, stroke_width=1.5).move_to(center)
        self.c = self.frame.get_center()
        self.circle = DashedVMobject(Circle(radius=0.6 * side / 2, color=GREY_B, stroke_width=1.5).move_to(self.c),
                                     num_dashes=40)

    def at(self, x, y):
        return self.c + np.array([x * self.side / 2, y * self.side / 2, 0])

    def dots(self, w=None, scale=0.9):
        n = len(self.y)
        w = np.full(n, 1 / n) if w is None else np.asarray(w)
        return VGroup(*[Dot(self.at(*p), radius=max(0.012, scale * math.sqrt(v)), color=YES if t > 0 else NO,
                            fill_opacity=0.85) for p, t, v in zip(self.X, self.y, w)])

    def stump(self, j, th, s):
        """The stump predicts s where x_j >= th: draw its boundary and shade its positive side."""
        h = self.side / 2
        if j == 0:
            x = self.c[0] + th * h
            line = Line([x, self.c[1] - h, 0], [x, self.c[1] + h, 0], color=HEAD, stroke_width=3)
            lo, hi = (x, self.c[0] + h) if s > 0 else (self.c[0] - h, x)
            shade = Rectangle(width=max(0.01, hi - lo), height=2 * h, stroke_width=0, fill_color=YES,
                              fill_opacity=0.12).move_to([(lo + hi) / 2, self.c[1], 0])
        else:
            yv = self.c[1] + th * h
            line = Line([self.c[0] - h, yv, 0], [self.c[0] + h, yv, 0], color=HEAD, stroke_width=3)
            lo, hi = (yv, self.c[1] + h) if s > 0 else (self.c[1] - h, yv)
            shade = Rectangle(width=2 * h, height=max(0.01, hi - lo), stroke_width=0, fill_color=YES,
                              fill_opacity=0.12).move_to([self.c[0], (lo + hi) / 2, 0])
        return VGroup(shade, line)


def curve_axes(xr, yr, xl, yl, xticks, yticks, x_length=5.2, y_length=3.4, fy=lambda v: f"{v:g}"):
    ax = CornerAxes(x_range=xr, y_range=yr, x_length=x_length, y_length=y_length, tips=False,
                    axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": False})
    xt = VGroup(*[label(f"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(v, yr[0]), DOWN, buff=0.1)
                  for v in xticks])
    yt = VGroup(*[label(fy(v), font_size=16, color=GREY_B).next_to(ax.c2p(xr[0], v), LEFT, buff=0.1)
                  for v in yticks])
    lx = label(xl, font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.4)
    ly = label(yl, font_size=17, color=GREY_A).next_to(ax, UP, buff=0.08).align_to(ax, LEFT)
    return VGroup(ax, xt, yt, lx, ly), ax


def polyline(ax, xs, ys, color, width=2.5):
    return VMobject(color=color, stroke_width=width).set_points_as_corners([ax.c2p(x, v) for x, v in zip(xs, ys)])


class Boosting(VoiceoverScene):
    def construct(self):
        self.card()
        self.weak()
        self.reweight()
        self.proof()
        self.game()
        self.margins()
        self.noise()

    def card(self):
        card = chapter_card(4, r"Boosting", r"Can many weak rules make a strong one?", lit=(1990, 1997, 2003),
                            extra=((1990, r"Schapire: \ weak learning is strong"),
                                   (1997, r"Freund and Schapire: \ AdaBoost"), (2003, r"G\"odel Prize")), part=PART)
        with self.voiceover("Chapter four. Boosting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def weak(self):
        b = load("boost")["clean"]
        X, y = np.array(b["X"]), np.array(b["y"])
        n = len(y)
        head = label(r"Weak learners", font_size=36).to_edge(UP, buff=0.3)
        ring = Ring(X, y, side=4.6, center=[-3.9, -0.35, 0])
        dots = ring.dots()
        e1, s1 = best_stump(X, y, np.full(n, 1 / n))
        w1 = np.array(b["weights"]["1"])
        e2, s2 = best_stump(X, y, w1)
        st2 = ring.stump(*s2)
        pos = float((y > 0).mean())
        cap = note(rf"{n} points, \ green inside radius 0.6; \ stumps: \ one coordinate against one threshold",
                   font_size=16).next_to(ring.frame, DOWN, buff=0.15)
        W = 6.0
        side = VGroup(
            wrapped_label(r"a \textbf{strong} learner reaches any error $\epsilon$ with any confidence; \ a "
                          r"\textbf{weak} learner only promises error at most $\tfrac12 - \gamma$, \ on every "
                          r"distribution", W, font_size=19, color=WHITE),
            wrapped_label(rf"the best single stump on equal weights says ``outside'' everywhere: \ error "
                          rf"{b['train'][0]:.3f}, \ the share of green points \ ({pos:.3f})", W, font_size=19,
                          color=GREY_A),
            wrapped_label(rf"re-weighted, \ the next stump cuts at $x_1 = {s2[1]:.2f}$: \ weighted error "
                          rf"{e2:.2f}, \ an edge of $\gamma \approx {0.5 - e2:.2f}$", W, font_size=19, color=HEAD),
            wrapped_label(r"Kearns and Valiant asked whether weak learning implies strong; \ Schapire \ (1990) \ "
                          r"proved it does, \ by construction", W, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "A strong learner reaches any error with any confidence. A weak learner promises only an error "
            "a little below a half, on every distribution. <bookmark mark='a'/> Here no single rule will "
            "do: four hundred points, green inside a circle. Our weak learner draws decision stumps, one "
            "threshold on one coordinate. <bookmark mark='b'/> With equal weights, the best stump says "
            "outside everywhere, wrong on the green twenty-eight and a half per cent. <bookmark mark='c'/> "
            "Change the weights and the best stump changes: now it cuts at about point six, with weighted "
            "error a third. <bookmark mark='d'/> Michael Kearns and Leslie Valiant asked whether weak "
            "learning is really weaker. In 1990 Robert Schapire proved it is not."
        ) as vo:
            self.play(FadeIn(head), Create(ring.frame), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots), Create(ring.circle), FadeIn(cap))
            vo.wait_until("b")
            self.play(Indicate(VGroup(*[d for d, t in zip(dots, y) if t > 0]), color=WHITE, scale_factor=1.15),
                      FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Transform(dots, ring.dots(w1)), FadeIn(st2), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        _ = (e1, s1)
        self.wait(0.4)
        self.clear_scene()

    def reweight(self):
        b = load("boost")["clean"]
        X, y = np.array(b["X"]), np.array(b["y"])
        head = label(r"AdaBoost: \ re-weight the hard points", font_size=36).to_edge(UP, buff=0.3)
        ring = Ring(X, y, side=4.8, center=[-3.85, -0.45, 0])
        rounds = [int(k) for k in sorted(b["weights"], key=int)]
        Ws = {t: np.array(b["weights"][str(t)]) for t in rounds}
        dots = ring.dots()
        tl = label(r"equal weights", font_size=20, color=HEAD).next_to(ring.frame, UP, buff=0.12)
        fs = 28
        algo = VGroup(
            MathTex(r"\epsilon_t = \sum_i D_t(i)\,\mathbf 1\big[h_t(x_i) \ne y_i\big]", font_size=fs),
            MathTex(r"\alpha_t = \tfrac12 \ln\frac{1 - \epsilon_t}{\epsilon_t}", font_size=fs),
            MathTex(r"D_{t+1}(i) = \frac{D_t(i)\, e^{-\alpha_t y_i h_t(x_i)}}{Z_t}", font_size=fs),
            MathTex(r"H(x) = \operatorname{sign}\Big(\sum_t \alpha_t h_t(x)\Big)", font_size=fs, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        whys = VGroup(
            label(r"the weak learner's weighted error on round $t$", font_size=17, color=GREY_B),
            label(r"its vote: \ large when $\epsilon_t$ is small", font_size=17, color=GREY_B),
            label(r"mistakes gain weight by $e^{\alpha_t}$, \ hits lose it; \ $Z_t$ normalizes", font_size=17,
                  color=GREY_B),
            label(r"the final rule: \ a weighted majority vote", font_size=17, color=GREY_B),
        )
        col = stacked(list(algo), list(whys), buff=0.2).move_to([3.3, 0.3, 0])
        if col.get_right()[0] > 6.85:
            col.shift(LEFT * (col.get_right()[0] - 6.85))
        foot = wrapped_label(r"the weight piles up on the points near the circle, \ where every stump is unsure", 5.2,
                             font_size=19, color=HEAD).next_to(col, DOWN, buff=0.35).align_to(col, LEFT)
        with self.voiceover(
            "Freund and Schapire's AdaBoost, from 1995, made boosting practical. <bookmark mark='a'/> Keep "
            "a weight on every example, equal at first. Each round, ask the weak learner for a rule with "
            "small weighted error, <bookmark mark='b'/> and give it a vote that grows as its error shrinks."
            " <bookmark mark='c'/> Then re-weight: examples it got wrong are multiplied up, the rest down, "
            "and the weights are normalized. <bookmark mark='d'/> Watch after one, two, five and twenty "
            "rounds: easy points far from the circle shrink, and weight piles up on the boundary, where the"
            " heaviest point carries about four and a half times its first share. <bookmark mark='e'/> The "
            "final classifier is a weighted majority vote."
        ) as vo:
            self.play(FadeIn(head), Create(ring.frame), Create(ring.circle), FadeIn(dots), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(col[0]))
            vo.wait_until("b")
            self.play(FadeIn(col[1]))
            vo.wait_until("c")
            self.play(FadeIn(col[2]))
            vo.wait_until("d")
            stump = None
            for t in rounds:
                _, s = best_stump(X, y, Ws[t])
                new_st = ring.stump(*s)
                tl2 = label(rf"weights after round {t}; \ stump of round {t + 1}", font_size=20,
                            color=HEAD).move_to(tl)
                anims = [Transform(dots, ring.dots(Ws[t])), Transform(tl, tl2)]
                if stump is None:
                    stump = new_st
                    anims.append(FadeIn(stump))
                else:
                    anims.append(Transform(stump, new_st))
                self.play(*anims, run_time=1.6)
                self.wait(0.5)
            self.play(FadeIn(foot))
            vo.wait_until("e")
            self.play(FadeIn(col[3]))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        b = load("boost")["clean"]
        tr = b["train"]
        zero = next(i + 1 for i, v in enumerate(tr) if v == 0)
        stays = max(i + 1 for i, v in enumerate(tr) if v > 0) + 1
        head = label(r"Why the training error falls exponentially", font_size=36).to_edge(UP, buff=0.3)
        fs = 25
        E = r"\frac{1}{m}\sum_i e^{-y_i F(x_i)}"
        Z = r"2\sqrt{\epsilon_t(1 - \epsilon_t)}"
        rows = [
            MathTex(r"D_{T+1}(i) = \frac{e^{-y_i F(x_i)}}{m \prod_t Z_t}, \qquad F = \sum_t \alpha_t h_t",
                    font_size=fs),
            MathTex(r"\frac{1}{m}\sum_i \mathbf 1\big[y_i F(x_i) \le 0\big]", r"\le", E, font_size=fs),
            MathTex(E, r"=", r"\prod_t Z_t", font_size=fs),
            MathTex(r"Z_t = (1 - \epsilon_t)\, e^{-\alpha_t} + \epsilon_t\, e^{\alpha_t}", r"=", Z, font_size=fs),
            MathTex(Z, r"=", r"\sqrt{1 - 4\gamma_t^2}", r"\le", r"e^{-2\gamma_t^2}", font_size=fs),
            MathTex(r"\text{training error}", r"\le", r"\exp\Big(-2\sum_t \gamma_t^2\Big)", font_size=fs + 3),
        ]
        rows[5][2].set_color(YES)
        whys = [
            label(r"unroll the update \ $T$ times", font_size=16, color=GREY_B),
            label(r"a mistake has $yF \le 0$, \ and $\mathbf 1[z \le 0] \le e^{-z}$", font_size=16, color=GREY_B),
            label(r"the weights $D_{T+1}(i)$ sum to one", font_size=16, color=GREY_B),
            label(r"with AdaBoost's $\alpha_t$, \ which is exactly the $\alpha$ that minimizes $Z_t$", font_size=16,
                  color=GREY_B),
            label(r"write $\epsilon_t = \tfrac12 - \gamma_t$; \ $1 + x \le e^x$", font_size=16, color=GREY_B),
            label(r"an edge $\gamma$ every round: \ at most $e^{-2\gamma^2 T}$", font_size=16, color=YES),
        ]
        col = stacked(rows, whys, buff=0.17).next_to(head, DOWN, buff=0.3).to_edge(LEFT, buff=0.4)
        T = min(150, len(tr))
        g, ax = curve_axes([0, T, 25], [0, 0.3, 0.1], r"round $t$", r"training error, \ measured",
                           [0, 50, 100, 150], [0, 0.1, 0.2, 0.3], x_length=4.6, y_length=3.2)
        g.move_to([4.5, 0.2, 0])
        c = polyline(ax, range(1, T + 1), tr[:T], DATA)
        zl = DashedLine(ax.c2p(zero, 0), ax.c2p(zero, 0.15), color=YES, stroke_width=2)
        zl2 = DashedLine(ax.c2p(stays, 0), ax.c2p(stays, 0.1), color=YES, stroke_width=2)
        zt = label(rf"first zero: \ round {zero}", font_size=17, color=YES).next_to(ax.c2p(zero, 0.15), UP,
                                                                                    buff=0.08)
        zt2 = label(rf"zero for good: \ {stays}", font_size=17, color=YES).next_to(ax.c2p(stays, 0.1), UP,
                                                                                  buff=0.08).shift(RIGHT * 0.3)
        with self.voiceover(
            "Freund and Schapire proved that the training error falls exponentially. <bookmark mark='a'/> "
            "Unroll the update: each final weight is e to the minus y F, F being the weighted vote, over m "
            "and the product of the normalizers. <bookmark mark='b'/> On a training mistake y F is not "
            "positive, so e to the minus y F is at least one, and the training error is at most the average"
            " of e to the minus y F. <bookmark mark='c'/> The final weights sum to one, so that average is "
            "the product of the normalizers. <bookmark mark='d'/> With AdaBoost's vote, each normalizer is "
            "two root epsilon times one minus epsilon. <bookmark mark='e'/> With error a half minus the "
            "edge gamma, that is root of one minus four gamma squared, at most e to the minus two gamma "
            "squared. <bookmark mark='f'/> So the training error is at most e to the minus twice the sum of"
            " squared edges. <bookmark mark='g'/> On our circle it first hit zero at round fifty-seven, and"
            " stayed there from round a hundred and eight."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("b")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(col[2][1]))
            vo.wait_until("d")
            self.play(Write(col[3][0]), FadeIn(col[3][1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(col[4][1]))
            vo.wait_until("f")
            self.play(Write(col[5][0]), FadeIn(col[5][1]))
            vo.wait_until("g")
            self.play(FadeIn(g), Create(c), run_time=2)
            self.play(Create(zl), FadeIn(zt), Create(zl2), FadeIn(zt2))
        self.wait(0.4)
        self.clear_scene()

    def game(self):
        head = label(r"Boosting as a zero-sum game", font_size=36).to_edge(UP, buff=0.3)
        # illustrative: 8 examples, 8 weak rules; rule j is wrong on examples j, j+1, j+2 (mod 8)
        n = 8
        M = np.ones((n, n))
        for j in range(n):
            for k in range(3):
                M[(j + k) % n, j] = -1
        cell = 0.42
        x0, y0 = -3.3, 2.0
        cells = VGroup(*[Square(side_length=cell * 0.92, stroke_width=0, fill_color=YES if M[i, j] > 0 else NO,
                                fill_opacity=0.75).move_to([x0 + j * cell, y0 - i * cell, 0])
                         for i in range(n) for j in range(n)])
        rl = label(r"examples $i$", font_size=17, color=GREY_A).next_to(cells, LEFT, buff=1.55).rotate(PI / 2)
        cl = label(r"weak rules $j$: \ green where $y_i h_j(x_i) = +1$", font_size=17, color=GREY_A).next_to(
            cells, UP, buff=0.12)
        bx = x0 - cell * 0.5 - 0.15

        def bars(D):
            return VGroup(*[Rectangle(width=max(0.02, 1.0 * D[i] * n * 0.5), height=cell * 0.7, stroke_width=0,
                                      fill_color=LAM, fill_opacity=0.85).move_to(
                [bx - max(0.02, D[i] * n * 0.5) / 2, y0 - i * cell, 0]) for i in range(n)])
        D = np.full(n, 1 / n)
        bar = bars(D)
        bl = label(r"booster: \ weights $D$", font_size=17, color=LAM).next_to(cells, DOWN, buff=0.15).align_to(
            bar, LEFT)
        eta = 0.5
        seq = []
        for _ in range(5):
            j = int(np.argmax(D @ M))
            D = D * np.exp(-eta * M[:, j])
            D = D / D.sum()
            seq.append((j, D.copy()))
        ill = note(r"illustrative", font_size=16).next_to(bl, DOWN, buff=0.08).align_to(bar, LEFT)
        W = 6.3
        side = VGroup(
            wrapped_label(r"the booster picks a distribution over \textbf{rows}; \ the weak learner answers with "
                          r"the best \textbf{column}; \ the payoff is its edge $\sum_i D(i)\, y_i h_j(x_i)$", W,
                          font_size=19, color=WHITE),
            MathTex(r"\min_{D}\ \max_{j}\ \sum_i D(i)\, M_{ij} \ \ge\ 2\gamma", font_size=30, color=HEAD),
            label(r"weak learning: \ on every distribution, \ some rule has edge $2\gamma$", font_size=17,
                  color=GREY_B),
            MathTex(r"\max_{\lambda}\ \min_{i}\ \sum_j \lambda_j M_{ij} \ \ge\ 2\gamma", font_size=30, color=YES),
            label(r"von Neumann's minimax theorem: \ one weighted vote has margin $2\gamma$ on \textit{every} example",
                  font_size=17, color=GREY_B),
            wrapped_label(r"AdaBoost's re-weighting is the multiplicative-weights update of Part 23, \ played on the "
                          r"rows: \ it finds such a vote", W, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.55, -0.35, 0])
        side[2].shift(UP * 0.1)
        side[4].shift(UP * 0.1)
        if side.get_right()[0] > 6.85:
            side.shift(LEFT * (side.get_right()[0] - 6.85))
        with self.voiceover(
            "Freund and Schapire also showed that boosting is a game. <bookmark mark='a'/> Make a matrix "
            "with a row per example and a column per weak rule, green where the rule is right. The booster "
            "picks a distribution over rows; the weak learner answers with the best column. "
            "<bookmark mark='b'/> Weak learnability says some column always has an edge of two gamma. "
            "<bookmark mark='c'/> Von Neumann's minimax theorem then gives a weighted vote of columns that "
            "is right by a margin of two gamma on every row. <bookmark mark='d'/> AdaBoost's re-weighting "
            "is multiplicative weights, from Part 23, played on the rows: watch weight move onto the rows "
            "the last chosen rule got wrong. Its vote approaches the minimax one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cl), FadeIn(rl))
            self.play(FadeIn(bar), FadeIn(bl), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Write(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
            hl = None
            for j, Dn in seq:
                box = SurroundingRectangle(VGroup(*[cells[i * n + j] for i in range(n)]), color=HEAD, buff=0.03,
                                           stroke_width=3)
                if hl is None:
                    hl = box
                    self.play(Create(hl), run_time=0.5)
                else:
                    self.play(Transform(hl, box), run_time=0.5)
                self.play(Transform(bar, bars(Dn)), run_time=0.9)
        self.wait(0.4)
        self.clear_scene()

    def margins(self):
        b = load("boost")["clean"]
        tr, te = b["train"], b["test"]
        T = len(tr)
        zero = max(i + 1 for i, v in enumerate(tr) if v > 0) + 1      # zero from here on
        head = label(r"Why it keeps working after zero training error", font_size=36).to_edge(UP, buff=0.3)
        g1, a1 = curve_axes([0, T, 50], [0, 0.3, 0.1], r"round $t$", r"error", [0, 100, 200, 300],
                            [0, 0.1, 0.2, 0.3], x_length=5.4, y_length=3.0)
        g1.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.9)
        c_tr = polyline(a1, range(1, T + 1), tr, DATA)
        c_te = polyline(a1, range(1, T + 1), te, YES)
        ltr = label(r"training", font_size=17, color=DATA).next_to(a1.c2p(T, 0), UP, buff=0.1).shift(LEFT * 0.4)
        lte = label(r"test", font_size=17, color=YES).next_to(a1.c2p(T, te[-1]), UP, buff=0.1).shift(LEFT * 0.3)
        zl = DashedLine(a1.c2p(zero, 0), a1.c2p(zero, 0.3), color=GREY_B, stroke_width=1.5)
        best = min(range(T), key=lambda i: te[i])
        nums = wrapped_label(rf"test error {te[zero - 1]:.3f} at round {zero}, \ {te[best]:.3f} at round "
                             rf"{best + 1}, \ {te[-1]:.3f} at round {T}: \ it barely rises", 5.6, font_size=18,
                             color=YES).next_to(g1, DOWN, buff=0.2).align_to(g1, LEFT)
        # the margin distribution: the fraction of training points with margin at most theta
        ks = [k for k in ("5", "20", "100", str(T)) if k in b["margins"]]
        cols = {ks[0]: GREY_B, ks[1]: LAM, ks[2]: DATA, ks[3]: YES}
        g2, a2 = curve_axes([-0.6, 0.6, 0.2], [0, 1, 0.25], r"margin $\theta$", r"fraction of points with margin "
                            r"$\le \theta$", [-0.6, -0.3, 0, 0.3, 0.6], [0, 0.5, 1], x_length=4.6, y_length=3.0)
        g2.next_to(g1, RIGHT, buff=1.3).align_to(g1, UP)
        if g2.get_right()[0] > 6.85:
            g2.shift(LEFT * (g2.get_right()[0] - 6.85))
        cdfs, cl = VGroup(), VGroup()
        for k in ks:
            ms = b["margins"][k]
            n = len(ms)
            xs = [max(-0.6, min(0.6, v)) for v in ms]
            cdfs.add(polyline(a2, xs, [(i + 1) / n for i in range(n)], cols[k], width=2.5))
            cl.add(label(rf"round {k}: \ smallest {min(ms):+.3f}", font_size=17, color=cols[k]))
        cl.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(g2, DOWN, buff=0.2).align_to(g2, LEFT)
        v0 = DashedLine(a2.c2p(0, 0), a2.c2p(0, 1), color=GREY_D, stroke_width=1.5)
        thm = MathTex(r"\Pr_D\big[yf(x) \le 0\big] \le \Pr_S\big[yf(x) \le \theta\big] + "
                      r"\tilde O\Big(\sqrt{\tfrac{d}{m\,\theta^2}}\Big)", font_size=28, color=HEAD)
        thm.to_edge(DOWN, buff=0.3)
        tn = label(r"Schapire, \ Freund, \ Bartlett and Lee \ (1998); \ $f$ = the normalized vote, \ $d$ = VC "
                   r"dimension of the weak rules", font_size=16, color=GREY_B).next_to(thm, UP, buff=0.1)
        with self.voiceover(
            "Then came a surprise. <bookmark mark='a'/> Training error is zero for good from round a "
            "hundred and eight, and classical intuition says more rounds only add complexity, so test error"
            " should rise. <bookmark mark='b'/> It does not: it hovers near three per cent for two hundred "
            "more rounds. <bookmark mark='c'/> The explanation, from Schapire, Freund, Peter Bartlett and "
            "Wee Sun Lee in 1998, is the margin: how decisively the normalized vote gets an example right. "
            "Here are the training margins after five, twenty, a hundred and three hundred rounds: long "
            "after every point is correct, boosting keeps pushing the smallest up. <bookmark mark='d'/> "
            "Their theorem bounds test error by the fraction of training margins below theta, plus a term "
            "in the weak rules' VC dimension and theta, not the number of rounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1))
            vo.wait_until("a")
            self.play(Create(c_tr), FadeIn(ltr), run_time=2)
            self.play(Create(zl))
            vo.wait_until("b")
            self.play(Create(c_te), FadeIn(lte), run_time=2)
            self.play(FadeIn(nums))
            vo.wait_until("c")
            self.play(FadeIn(g2), Create(v0))
            for cd, lb in zip(cdfs, cl):
                self.play(Create(cd), FadeIn(lb), run_time=1.0)
            vo.wait_until("d")
            self.play(Write(thm), FadeIn(tn))
        self.wait(0.4)
        self.clear_scene()

    def noise(self):
        b = load("boost")["noisy"]
        X, y = np.array(b["X"]), np.array(b["y"])
        tr, te = b["train"], b["test"]
        T = len(tr)
        flipped = np.where(np.hypot(X[:, 0], X[:, 1]) < 0.6, 1.0, -1.0) != y
        last = str(max(int(k) for k in b["weights"]))
        w = np.array(b["weights"][last])
        share = float(w[flipped].sum())
        head = label(r"When some labels are wrong", font_size=36).to_edge(UP, buff=0.3)
        ring = Ring(X, y, side=4.4, center=[-4.1, -0.4, 0])
        dots = ring.dots()
        heavy = ring.dots(w, scale=1.0)
        rings = VGroup(*[Circle(radius=0.1, color=WHITE, stroke_width=1.5).move_to(ring.at(*p))
                         for p, f in zip(X, flipped) if f])
        rl = label(rf"weights after round {last}; \ circled: \ the {int(flipped.sum())} flipped labels", font_size=17,
                   color=GREY_A).next_to(ring.frame, DOWN, buff=0.15)
        g, ax = curve_axes([0, T, 50], [0, 0.35, 0.1], r"round $t$", r"error", [0, 100, 200, 300],
                           [0, 0.1, 0.2, 0.3], x_length=5.0, y_length=2.8)
        g.move_to([3.7, 1.05, 0])
        c_tr = polyline(ax, range(1, T + 1), tr, DATA)
        c_te = polyline(ax, range(1, T + 1), te, NO)
        ltr = label(r"training", font_size=17, color=DATA).next_to(ax.c2p(T, tr[-1]), DOWN, buff=0.1).shift(
            LEFT * 0.4)
        lte = label(r"test", font_size=17, color=NO).next_to(ax.c2p(T, te[-1]), UP, buff=0.1).shift(LEFT * 0.3)
        best = min(range(T), key=lambda i: te[i])
        W = 5.6
        side = VGroup(
            wrapped_label(rf"{b['noise']:.0%} of labels flipped, \ in training and test alike: \ the flipped "
                          rf"{flipped.mean():.1%} of points hold {share:.0%} of the weight by round {last}"
                          .replace("%", r"\%"), W, font_size=19, color=WHITE),
            wrapped_label(rf"test error is lowest, \ {te[best]:.3f}, \ at round {best + 1}, \ and {te[-1]:.3f} by "
                          rf"round {T}: \ the exponential loss chases the noise", W, font_size=19, color=NO),
            wrapped_label(r"so stop early, \ or shrink each vote; \ gradient boosting \ (Friedman, \ 2001) \ "
                          r"generalizes the idea to any loss", W, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(g, DOWN, buff=0.35).align_to(g[0], LEFT)
        if side.get_right()[0] > 6.85:
            side.shift(LEFT * (side.get_right()[0] - 6.85))
        with self.voiceover(
            "The same mechanism is boosting's weakness. <bookmark mark='a'/> Flip five per cent of the "
            "labels. Every sensible rule gets a flipped point wrong, so its weight is multiplied up round "
            "after round. <bookmark mark='b'/> By round twenty the twenty-three flipped points, under six "
            "per cent of the data, hold eighteen per cent of the weight. <bookmark mark='c'/> Test error, "
            "on equally noisy test labels, is lowest at round twenty-seven and then creeps up, as boosting "
            "memorizes the mistakes. <bookmark mark='d'/> The remedies are to stop early or shrink each "
            "vote; Jerome Friedman's gradient boosting of 2001 extended the idea to any loss. AdaBoost won "
            "Freund and Schapire the Gödel Prize in 2003."     ) as vo:
            self.play(FadeIn(head), Create(ring.frame), Create(ring.circle), FadeIn(dots), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(rings), FadeIn(rl))
            vo.wait_until("b")
            self.play(Transform(dots, heavy), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(c_tr), FadeIn(ltr), Create(c_te), FadeIn(lte), run_time=2)
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
